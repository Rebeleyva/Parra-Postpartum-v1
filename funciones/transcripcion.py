import torch                                    # Para manejo de GPU y memoria
import json                                     # Para guardar resultados como JSON
import os                                       # Para manejo de rutas y archivos
import numpy as np                              # Para operaciones numéricas
import soundfile as sf                          # Para leer archivos de audio
import gc                                       # Para liberar memoria durante el proceso
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

MODEL_PATH = "RebecaLeyva/whisper-finetuned-parra-v2"  # Ruta o nombre del modelo en HuggingFace

def transcripcion_de_audio(audio_path, diarization_results, output_dir="."):
    """
    Transcribe segmentos de audio (por turnos de hablante) usando un modelo Whisper fine-tuneado.
    
    Args:
        audio_path (str): Ruta al archivo de audio preprocesado.
        diarization_results (list): Lista de segmentos/turnos con tiempos y hablantes detectados.
        output_dir (str): Carpeta donde guardar la transcripción alineada.
    
    Returns:
        list: Lista de segmentos con la transcripción añadida.
    """
    print("🔄 Ejecutando transcripción con whisper-finetuned-parra-v2 en español...")

    # Convierte la ruta de salida a absoluta y crea el directorio si no existe
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Selecciona GPU si está disponible, si no CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Carga el modelo de transcripción desde HuggingFace (formato seq2seq)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float32,   # Forzar tipo de dato por compatibilidad
        low_cpu_mem_usage=True       # Para optimizar el uso de memoria
    ).to(device)

    # Carga el procesador (tokenizer y extractor) asociado al modelo
    processor = AutoProcessor.from_pretrained(MODEL_PATH)
    
    # Construye el pipeline ASR (Automatic Speech Recognition)
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        return_timestamps=False,     # No regresa timestamps, ya se tiene la segmentación
        chunk_length_s=30,           # Divide en chunks de 30s para evitar errores de memoria
        stride_length_s=5,           # Sobreposición de 5s entre chunks
        batch_size=2,                # Procesa 2 segmentos por batch
        device=0 if torch.cuda.is_available() else -1  # Usa GPU si está, si no CPU
    )

    # Carga el audio (puede ser mono o estéreo)
    audio_data, sample_rate = sf.read(audio_path)
    if len(audio_data.shape) > 1:
        # Si es multicanal, lo convierte a mono promediando canales
        audio_data = np.mean(audio_data, axis=1)

    transcriptions = []
    # Procesa cada segmento generado por la diarización
    for i, segment in enumerate(diarization_results):
        # Calcula los índices de inicio y fin en muestras (samples)
        start_sample = int(segment["start_time"] * sample_rate)
        end_sample = int(segment["end_time"] * sample_rate)
        segment_audio = audio_data[start_sample:end_sample]

        if len(segment_audio) == 0:
            # Si el segmento está vacío, agrega string vacío
            transcriptions.append("")
            continue

        # Llama al pipeline para obtener la transcripción del segmento
        result = asr_pipeline(
            {"raw": segment_audio, "sampling_rate": sample_rate},
            # generate_kwargs={"language": "<|es|>"}  # Puedes descomentar si usas forcing de idioma
        )
        transcriptions.append(result["text"].lower())  # Agrega la transcripción en minúsculas

        # Limpia memoria de vez en cuando para evitar saturar la RAM/GPU
        if i % 3 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

    # Asigna la transcripción resultante a cada segmento
    for i, segment in enumerate(diarization_results):
        segment["transcript"] = transcriptions[i]

    # Guarda los resultados alineados (con transcripción y tiempos) en un JSON
    aligned_path = os.path.join(output_dir, "aligned_transcription.json")
    with open(aligned_path, "w", encoding="utf-8") as f:
        json.dump(diarization_results, f, ensure_ascii=False, indent=4)

    print(f"✅ Transcripción completada y guardada en '{aligned_path}'.")
    return diarization_results
