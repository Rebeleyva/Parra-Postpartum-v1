import torch              # Para detectar y usar GPU si está disponible
import json               # Para guardar resultados en formato JSON
import os                 # Para manejo de archivos y variables de entorno
from dotenv import load_dotenv   # Para cargar variables del archivo .env
from pyannote.audio import Pipeline  # Modelo de diarización

# Cargar variables del archivo .env, especialmente el token de HuggingFace
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

def realizar_diarizacion(audio_path, output_dir="."):
    """
    Ejecuta la diarización de hablantes sobre un archivo de audio usando pyannote.
    
    Args:
        audio_path (str): Ruta al archivo de audio.
        output_dir (str): Carpeta donde se guardarán los resultados.
        
    Returns:
        list: Lista de diccionarios con los turnos y hablantes detectados.
    """
    # Mensaje inicial para indicar que comienza la diarización
    print("🔄 Ejecutando diarización con pyannote/speaker-diarization-3.1...")

    # Convierte la ruta de salida a absoluta y crea el directorio si no existe
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Selecciona el dispositivo: GPU (cuda) si está disponible, si no CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Inicializa el pipeline de diarización con el modelo preentrenado y tu token de HuggingFace
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=HUGGINGFACE_TOKEN
    )
    pipeline.to(device)  # Asigna el pipeline al dispositivo adecuado

    # Ejecuta la diarización sobre el audio
    diarization = pipeline(audio_path)
    diarization_results = []

    # Itera sobre los segmentos detectados y los agrega a la lista de resultados
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diarization_results.append({
            "start_time": round(turn.start, 2),  # Inicio del segmento
            "end_time": round(turn.end, 2),      # Fin del segmento
            "speaker": speaker                   # Identificador del hablante
        })

    # Guarda los resultados en un archivo JSON dentro del output_dir
    output_path = os.path.join(output_dir, "diarization_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(diarization_results, f, ensure_ascii=False, indent=4)

    # Informa al usuario dónde se guardaron los resultados
    print(f"✅ Diarización completada. Guardado en '{output_path}'.")

    return diarization_results
