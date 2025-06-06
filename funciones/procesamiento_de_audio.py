import numpy as np                    # Para operaciones numéricas
import soundfile as sf                # Para guardar archivos de audio
import os                             # Para manejo de rutas y archivos
import subprocess                     # Para ejecutar comandos del sistema (ffmpeg)
import librosa                        # Para cargar y procesar archivos de audio
from scipy.signal import butter, sosfiltfilt   # Para filtros de audio

def convert_mp3_to_wav(mp3_path, wav_path):
    """
    Convierte un archivo MP3 a WAV usando ffmpeg.
    
    Args:
        mp3_path (str): Ruta al archivo mp3 de entrada.
        wav_path (str): Ruta donde se guardará el archivo wav.
    
    Returns:
        str: Ruta al archivo wav generado, o None si hay error.
    """
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", mp3_path, wav_path],
            check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL  # Silencia la salida
        )
        return wav_path
    except Exception as e:
        print(f"❌ Error al convertir mp3 a wav: {e}")
        return None

def ecualizar_audio(audio, sr, low=300, high=3400, orden=4):
    """
    Aplica un filtro pasa-banda para dejar solo frecuencias típicas de voz humana (300–3400 Hz).
    
    Args:
        audio (np.array): Señal de audio.
        sr (int): Frecuencia de muestreo.
        low (int): Frecuencia mínima (Hz).
        high (int): Frecuencia máxima (Hz).
        orden (int): Orden del filtro.
    
    Returns:
        np.array: Señal de audio filtrada.
    """
    # Define el filtro pasa-banda usando Butterworth
    sos = butter(N=orden, Wn=[low, high], btype='bandpass', fs=sr, output='sos')
    # Aplica el filtro al audio
    audio_filtrado = sosfiltfilt(sos, audio)
    return audio_filtrado

def procesamiento_de_audio(audio_file, output_dir="."):
    """
    Preprocesa un archivo de audio:
    - Convierte mp3 a wav si es necesario.
    - Ecualiza para resaltar voz humana.
    - Normaliza y guarda resultado en wav limpio.
    
    Args:
        audio_file (str): Ruta al archivo de audio de entrada.
        output_dir (str): Carpeta donde se guardará el resultado.
    
    Returns:
        str: Ruta al archivo wav procesado.
    """
    print(f"🔄 Procesando: {audio_file}...")

    # Convierte la ruta de salida a absoluta y crea el directorio si no existe
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Si el archivo es mp3, conviértelo a wav para procesamiento posterior
    if audio_file.lower().endswith(".mp3"):
        wav_file = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(audio_file))[0] + "_converted.wav"
        )
        audio_file = convert_mp3_to_wav(audio_file, wav_file)
        if not audio_file or not os.path.exists(audio_file):
            raise ValueError("No se pudo convertir MP3 a WAV")

    # Carga el audio en mono y fuerza la frecuencia a 16 kHz
    audio_data, sr = librosa.load(audio_file, sr=16000, mono=True)

    # Filtra el audio para dejar solo la banda de voz humana (300–3400 Hz)
    audio_eq = ecualizar_audio(audio_data, sr, low=300, high=3400, orden=4)

    # Normaliza el audio para evitar saturación o clipping
    audio_eq = audio_eq / (np.max(np.abs(audio_eq)) + 1e-8)

    # Genera el nombre de salida y guarda el archivo como WAV (PCM_16)
    nombre_base = os.path.splitext(os.path.basename(audio_file))[0]
    output_path = os.path.join(output_dir, f"{nombre_base}_processed.wav")
    sf.write(output_path, audio_eq, 16000, subtype='PCM_16')

    print(f"✅ Audio convertido y ecualizado a WAV: '{output_path}'\n")
    return output_path
