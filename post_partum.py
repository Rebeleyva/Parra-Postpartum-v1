# Importa módulos estándar de Python para manejo de archivos y argumentos
import os
import sys

# Importa funciones personalizadas desde tu módulo 'funciones'
from funciones.procesamiento_de_audio import procesamiento_de_audio
from funciones.diarizacion import realizar_diarizacion
from funciones.transcripcion import transcripcion_de_audio
from funciones.convertir_video_a_audio import convertir_video_a_mp3

# Extensiones soportadas para archivos de audio y video
AUDIO_EXTS = (".wav", ".mp3", ".m4a")
VIDEO_EXTS = (".mp4", ".mkv", ".mov", ".avi", ".webm")

# Función para verificar si un archivo es de audio según la extensión
def es_audio(path):
    return path.lower().endswith(AUDIO_EXTS)

# Función para verificar si un archivo es de video según la extensión
def es_video(path):
    return path.lower().endswith(VIDEO_EXTS)

# Imprime un banner decorativo al inicio del programa
def print_banner():
    print("="*60)
    print(" Procesador de Audio y Video con IA ".center(60, "="))
    print("="*60)

# Función principal del script
def main():
    print_banner()
    
    # Verifica que se haya pasado un argumento (el archivo a procesar)
    if len(sys.argv) < 2:
        print("Uso: python post_partum.py <archivo_audio_o_video>")
        print("Ejemplo: python post_partum.py entrevista.mp3")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # Checa si el archivo existe
    if not os.path.exists(input_path):
        print(f"❌ Archivo no encontrado: {input_path}")
        sys.exit(1)
    
    # Define el nombre base del archivo (sin extensión) y la carpeta de resultados
    nombre_base = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.join("resultados", nombre_base)
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n📂 Carpeta de salida: {output_dir}")

    # Detecta si el archivo es video, y si lo es, lo convierte a audio (mp3)
    if es_video(input_path):
        print(f"\n🎥 Archivo detectado como video, convirtiendo a MP3...")
        audio_path = convertir_video_a_mp3(input_path, output_dir=output_dir)
        print(f"✅ Video convertido: {audio_path}")
    # Si es audio, simplemente toma la ruta original
    elif es_audio(input_path):
        audio_path = input_path
        print(f"\n🎵 Archivo detectado como audio, usando directamente: {audio_path}")
    else:
        print("❌ Archivo no es audio ni video válido.")
        sys.exit(1)

    # Preprocesa el archivo de audio (ruido, normalización, etc)
    print("\n🎧 Preprocesando audio...")
    processed_audio = procesamiento_de_audio(audio_path, output_dir=output_dir)
    print(f"✅ Audio preprocesado: {processed_audio}")

    # Realiza diarización (separar intervenciones de diferentes hablantes)
    print("\n🗣️ Ejecutando diarización...")
    diarization_results = realizar_diarizacion(processed_audio, output_dir=output_dir)
    print(f"✅ Diarización completada: {diarization_results}")

    # Ejecuta transcripción automática del audio procesado
    print("\n✍️ Ejecutando transcripción...")
    transcribed = transcripcion_de_audio(processed_audio, diarization_results, output_dir=output_dir)
    print(f"✅ Transcripción completada: {transcribed}")

    # Mensaje de éxito final
    print("\n🎉 ¡Proceso finalizado! Todos los resultados están en la carpeta indicada.\n")

# Ejecuta la función principal solo si el script es llamado directamente
if __name__ == "__main__":
    main()
