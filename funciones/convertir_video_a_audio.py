import subprocess  # Para ejecutar comandos de sistema (como ffmpeg)
import os          # Para manipular rutas y archivos

def convertir_video_a_mp3(video_path, output_dir="resultados"):
    """
    Convierte un archivo de video a MP3 usando ffmpeg.
    
    Args:
        video_path (str): Ruta al archivo de video de entrada.
        output_dir (str): Carpeta donde se guardará el archivo MP3.
    
    Returns:
        str: Ruta al archivo MP3 generado, o None si hubo error.
    """
    # Obtiene el nombre base del archivo sin extensión
    nombre_base = os.path.splitext(os.path.basename(video_path))[0]
    # Construye la ruta de salida del archivo MP3
    mp3_path = os.path.join(output_dir, f"{nombre_base}.mp3")

    # Informa al usuario que iniciará la conversión
    print(f"🎬 Convirtiendo video a MP3 con ffmpeg: {video_path}")
    
    try:
        # Crea el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Comando para ejecutar ffmpeg y extraer solo el audio en formato MP3
        command = [
            "ffmpeg",
            "-i", video_path,      # Archivo de entrada
            "-vn",                # No incluir video
            "-acodec", "libmp3lame",  # Usa el códec MP3
            "-q:a", "2",          # Calidad de audio (2 = buena calidad)
            mp3_path,             # Archivo de salida
            "-y"                  # Sobrescribe archivo existente sin preguntar
        ]
        
        # Ejecuta el comando ffmpeg en la terminal, ocultando la salida estándar y de errores
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Retorna la ruta del archivo MP3 si todo fue bien
        return mp3_path
    except subprocess.CalledProcessError as e:
        # Captura cualquier error de ejecución de ffmpeg e informa al usuario
        print(f"❌ Error al convertir con ffmpeg: {e}")
        return None
