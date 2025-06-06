import os
import gc
import torch
import numpy as np
from datasets import DatasetDict, load_dataset

# === LIBERACIÓN DE VRAM Y RAM ===
def clear_vram():
    """Libera la memoria de la GPU (VRAM) y fuerza recolección de basura."""
    torch.cuda.empty_cache()
    gc.collect()
    print("🪛 VRAM liberada")

def clear_ram():
    """Fuerza la recolección de basura y muestra el uso de RAM actual (si psutil está disponible)."""
    gc.collect()
    try:
        import psutil
        process = psutil.Process(os.getpid())
        before = process.memory_info().rss / 1024 / 1024
        print(f"🪛 RAM antes: {before:.2f} MB")
    except:
        print("🪛 RAM liberada")

# === CARGA O DESCARGA DEL DATASET ===
DATASET_PROCESADO_PATH = "./preprocessed_data"
os.makedirs(DATASET_PROCESADO_PATH, exist_ok=True)

# Si ya existe un dataset preprocesado en disco, cárgalo
if os.path.exists(os.path.join(DATASET_PROCESADO_PATH, "dataset_dict.json")):
    print("✅ Cargando dataset preprocesado desde disco...")
    ds = DatasetDict.load_from_disk(DATASET_PROCESADO_PATH)
else:
    # Si no, descárgalo desde Hugging Face y prepáralo
    print("⬇  Descargando dataset desde Hugging Face...")
    ds = load_dataset("RebecaLeyva/UNAM_ParraPostPartum_dataset")

    # Tokenizador Whisper específico para español y tarea de transcripción
    from transformers import WhisperTokenizer
    tokenizer = WhisperTokenizer.from_pretrained("RebecaLeyva/STT-ParraPostPartum-v1", language="Spanish", task="transcribe")

    # --- Filtrado de muestras demasiado largas (máximo 400 tokens) ---
    def is_short_enough(batch):
        return len(tokenizer(batch["transcription"]).input_ids) <= 400

    ds["train"] = ds["train"].filter(is_short_enough)
    ds["test"] = ds["test"].filter(is_short_enough)

    # --- Añadir campo "split" para identificar train/test ---
    ds["train"] = ds["train"].map(lambda x: {**x, "split": "train"})
    ds["test"] = ds["test"].map(lambda x: {**x, "split": "test"})

    # --- Extraer arreglo de audio en float32 ---
    def extract_audio_array(batch):
        batch["audio_array"] = np.array(batch["audio"]["array"], dtype=np.float32)
        return batch

    ds["train"] = ds["train"].map(extract_audio_array, num_proc=1)
    ds["test"] = ds["test"].map(extract_audio_array, num_proc=1)

    # --- AUMENTACIÓN DE DATOS ---
    # Añade ruido, cambio de pitch, time stretch y desplazamiento (shift)
    from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift
    augmenter = Compose([
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5),
        TimeStretch(min_rate=0.85, max_rate=1.15, p=0.4),
        PitchShift(min_semitones=-2, max_semitones=2, p=0.4),
        Shift(min_shift=-0.1, max_shift=0.1, shift_unit="fraction", rollover=False, fade_duration=0.005, p=0.4),
    ])

    def augment_audio(batch):
        """Aplica aumentaciones solo sobre la señal de audio."""
        if not isinstance(batch["audio_array"], np.ndarray):
            batch["audio_array"] = np.array(batch["audio_array"], dtype=np.float32)
        batch["audio_array"] = augmenter(samples=batch["audio_array"], sample_rate=16000)
        return batch

    ds["train"] = ds["train"].map(augment_audio, num_proc=1)

    # --- EXTRACCIÓN DE FEATURES Y LABELS PARA WHISPER ---
    from transformers import WhisperProcessor
    processor = WhisperProcessor.from_pretrained("RebecaLeyva/STT-ParraPostPartum-v1", language="Spanish", task="transcribe")

    def prepare_dataset(batch):
        # Convierte el audio a features para el modelo y la transcripción a etiquetas de texto (tokens)
        batch["input_features"] = processor.feature_extractor(
            batch["audio_array"], sampling_rate=16000
        ).input_features[0]
        batch["labels"] = processor.tokenizer(batch["transcription"]).input_ids
        return batch

    ds["train"] = ds["train"].map(prepare_dataset, remove_columns=ds["train"].column_names)
    ds["test"] = ds["test"].map(prepare_dataset, remove_columns=ds["test"].column_names)

    # --- Guarda el dataset preprocesado en disco para acelerar futuras ejecuciones ---
    ds.save_to_disk(DATASET_PROCESADO_PATH)
    print(f"💾 Dataset preprocesado guardado en {DATASET_PROCESADO_PATH}")

# === ENTRENAMIENTO ===

# --- Cargar el procesador Whisper ---
from transformers import WhisperProcessor
processor = WhisperProcessor.from_pretrained("RebecaLeyva/STT-ParraPostPartum-v1", language="Spanish", task="transcribe")

# --- COLLATOR PARA AGRUPAR LOTES Y PADDING DINÁMICO ---
from dataclasses import dataclass
from typing import Any, Dict, List, Union

@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    """Cola lotes de entrada y salida para entrenamiento, haciendo padding automático."""
    processor: Any
    decoder_start_token_id: int

    def _call_(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # Junta los features de entrada
        input_features = [{"input_features": f["input_features"]} for f in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")
        # Junta los labels (transcripciones como tokens)
        label_features = [{"input_ids": f["labels"]} for f in features]
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
        # Elimina el token de inicio si todos los labels lo tienen
        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]
        batch["labels"] = labels
        return batch

data_collator = DataCollatorSpeechSeq2SeqWithPadding(
    processor=processor,
    decoder_start_token_id=processor.tokenizer.bos_token_id,
)

# --- MÉTRICAS ---
from jiwer import wer

def compute_metrics(pred):
    """Calcula WER (Word Error Rate) usando jiwer."""
    pred_ids = pred.predictions
    label_ids = pred.label_ids
    label_ids[label_ids == -100] = processor.tokenizer.pad_token_id
    pred_str = processor.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = processor.tokenizer.batch_decode(label_ids, skip_special_tokens=True)
    wer_score = wer(label_str, pred_str) * 100
    return {"wer": wer_score}

# --- CONFIGURACIÓN DEL ENTRENADOR ---
from transformers import Seq2SeqTrainingArguments, EarlyStoppingCallback

training_args = Seq2SeqTrainingArguments(
    output_dir="./whisper-finetuned",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    learning_rate=5e-6,
    num_train_epochs=10,
    warmup_steps=500,
    evaluation_strategy="steps",
    eval_steps=200,
    save_steps=200,
    logging_steps=50,
    save_total_limit=2,
    predict_with_generate=True,
    fp16=True,  # usa precisión mixta para GPU moderna (reduce RAM y acelera)
    push_to_hub=False,
    load_best_model_at_end=True,
    metric_for_best_model="wer",
    greater_is_better=False,
    generation_max_length=444,
)

# --- LIMPIEZA DE MEMORIA ---
clear_vram()
clear_ram()

# --- CARGA DEL MODELO BASE (Whisper fine-tuneable) ---
from transformers import WhisperForConditionalGeneration
model = WhisperForConditionalGeneration.from_pretrained("RebecaLeyva/STT-ParraPostPartum-v1")
model.generation_config.max_length = 444
clear_vram()
clear_ram()

# --- INICIALIZACIÓN DEL ENTRENADOR ---
from transformers import Seq2SeqTrainer
trainer = Seq2SeqTrainer(
    args=training_args,
    model=model,
    train_dataset=ds["train"],
    eval_dataset=ds["test"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    tokenizer=processor.feature_extractor,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)

clear_vram()
clear_ram()

# --- ENTRENAMIENTO DEL MODELO ---
trainer.train()
clear_vram()
clear_ram()

# --- GUARDADO FINAL DEL MODELO Y DEL PROCESSOR ---
output_dir = "./whisper-finetuned-augment"
model.save_pretrained(output_dir)
processor.save_pretrained(output_dir)
print(f"✅ Modelo y processor guardados en: {output_dir}")
