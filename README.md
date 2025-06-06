# Procesador de Audio y Video con IA — Parra Postpartum v1

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/tu_usuario/tu_repo)
![Platform](https://img.shields.io/badge/platform-linux--mac--win-green)

---

## 🚀 Descripción

**Parra Postpartum v1** es un pipeline automatizado para el procesamiento, diarización y transcripción de archivos de audio y video, pensado para análisis clínico, entrevistas, investigación en salud, lingüística y mucho más.

**Incluye:**
- Conversión automática de video a audio (MP3)
- Preprocesamiento y ecualización de voz humana para mejorar la calidad de la transcripción
- Diarización automática (identificación de hablantes) usando [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- Transcripción segmentada por hablante usando un modelo Whisper fine-tuneado

---

## 🧠 ¿Cómo funciona el pipeline?

El programa sigue este **flujo automático** para cualquier archivo de audio o video que proceses:

1. **Conversión de video a audio:** Si el archivo es video, lo convierte automáticamente a MP3 usando ffmpeg.
2. **Preprocesamiento y ecualización:** Filtra y normaliza el audio, enfocándose en la banda de la voz humana (300–3400 Hz) para máxima claridad.
3. **Diarización automática de hablantes:** Con modelos deep learning (pyannote.audio), identifica cuándo y quién está hablando en cada segmento.
4. **Transcripción segmentada:** Utiliza un modelo Whisper fine-tuneado para transcribir cada segmento, alineando texto, tiempo y hablante.
5. **Organización y guardado de resultados:** Todos los outputs (audio procesado, segmentos, transcripciones alineadas) se guardan ordenadamente en una carpeta dedicada a cada archivo de entrada.

**Todo esto ocurre de forma automática con una sola línea de comando.**

---

## 📦 Requisitos

- **Python 3.10+**
- Sistema operativo: Windows, MacOS, o Linux
- [ffmpeg](https://ffmpeg.org/) instalado (para conversión de video a audio)
- Un [token de HuggingFace](https://huggingface.co/settings/tokens) válido (para descargar modelos pyannote/Whisper)
- GPU NVIDIA (opcional, recomendado para grandes volúmenes)

---

## 🛠️ Instalación paso a paso

1. **Clona el repositorio**
   ```sh
   git clone https://github.com/tu_usuario/tu_repo.git
   cd tu_repo


2. **Instala las dependencias en un entorno virtual**

   ```sh
   python3 -m pip install --upgrade pip
   python3 setup_env.py
   ```

   > Esto instalará todas las dependencias en un entorno virtual llamado **Parra-Postpartum-v1**.

3. **Copia el ejemplo y pega tu token de HuggingFace:**

   ```sh
   cp .env.example .env
   ```

   Edita el archivo `.env` para incluir tu token:

   ```ini
   HUGGINGFACE_TOKEN=tu_token_de_huggingface_aqui
   ```

4. **(Opcional) Instala ffmpeg si no lo tienes**

   * **Ubuntu/Debian:**

     ```sh
     sudo apt install ffmpeg
     ```
   * **MacOS:**

     ```sh
     brew install ffmpeg
     ```
   * **Windows:**
     Descarga desde [ffmpeg.org](https://ffmpeg.org/)

---

## ⚡ Uso del programa

### Activar entorno virtual

* **En Mac/Linux:**

  ```sh
  source Parra-Postpartum-v1/bin/activate
  ```
* **En Windows:**

  ```sh
  Parra-Postpartum-v1\Scripts\activate
  ```

### Procesar un archivo (audio o video)

```sh
python post_partum.py <archivo_audio_o_video>
```

**Ejemplo de uso:**

```sh
python post_partum.py entrevista.mp3
python post_partum.py reunion_familiar.mp4
```

El programa detecta automáticamente el tipo de archivo y realiza todas las etapas de conversión, procesamiento, diarización y transcripción, guardando todo en una carpeta `/resultados/<nombre_archivo>/`.

---

## 🏭 Funcionamiento detallado del script principal (`post_partum.py`)

1. **Detecta el tipo de archivo:**

   * Si es audio soportado (`.wav`, `.mp3`, `.m4a`), lo procesa directo.
   * Si es video (`.mp4`, `.avi`, `.mov`, etc.), extrae el audio a MP3 automáticamente.

2. **Preprocesa el audio:**

   * Convierte a WAV, fuerza 16kHz mono.
   * Aplica filtrado pasa banda (300–3400 Hz) para mejorar calidad.
   * Normaliza el volumen para evitar clipping.

3. **Diariza:**

   * Usa pyannote para detectar intervalos y asignar un label a cada hablante.
   * Guarda un JSON tipo:

     ```json
     [
       {"start_time": 0.0, "end_time": 11.5, "speaker": "SPEAKER_00"},
       {"start_time": 11.5, "end_time": 22.7, "speaker": "SPEAKER_01"}
     ]
     ```

4. **Transcribe:**

   * Toma cada segmento identificado y lo transcribe usando Whisper.
   * Asigna la transcripción a cada segmento, ejemplo:

     ```json
     [
       {"start_time": 0.0, "end_time": 11.5, "speaker": "SPEAKER_00", "transcript": "buenos días a todos..."},
       {"start_time": 11.5, "end_time": 22.7, "speaker": "SPEAKER_01", "transcript": "gracias por venir."}
     ]
     ```

5. **Guarda resultados en `/resultados/<nombre_archivo>/`:**

   * Audio original
   * Audio convertido (si aplica)
   * Audio procesado (`*_processed.wav`)
   * `diarization_results.json`
   * `aligned_transcription.json`

---

## 📝 Ejemplo de salida de resultados

* **diarization\_results.json**

  ```json
  [
    {"start_time": 0.0, "end_time": 9.8, "speaker": "SPEAKER_00"},
    {"start_time": 9.8, "end_time": 16.5, "speaker": "SPEAKER_01"}
  ]
  ```
* **aligned\_transcription.json**

  ```json
  [
    {"start_time": 0.0, "end_time": 9.8, "speaker": "SPEAKER_00", "transcript": "buenos días, doctor..."},
    {"start_time": 9.8, "end_time": 16.5, "speaker": "SPEAKER_01", "transcript": "buenos días, cómo está."}
  ]
  ```

---

## 🛠️ Troubleshooting

* **No se activa el entorno virtual:**
  Asegúrate de usar `python3.10` o superior y de estar en la carpeta raíz del proyecto.

* **Error “No module named X”:**
  Verifica que el entorno virtual está activado antes de correr el script.

* **Problemas con torch/cu121 en Mac o sin GPU:**
  Cambia las líneas de torch en `requirements.txt` por versiones sin `+cu121` ni el index extra y corre:

  ```sh
  pip install torch torchvision torchaudio
  ```

* **ffmpeg no encontrado:**
  Instálalo según tu sistema (ver sección de requisitos).

* **Token de HuggingFace inválido:**
  Genera un nuevo token desde [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) y colócalo en tu `.env`.

---

## 🔑 Variables de entorno

Copia `.env.example` a `.env` y coloca tu token de HuggingFace:

```sh
cp .env.example .env
```

Luego edita el archivo `.env`:

```ini
HUGGINGFACE_TOKEN=tu_token_de_huggingface_aqui
```

Este token es necesario para descargar modelos privados de pyannote/Whisper.

---

## 🙋‍♂️ ¿Cómo contribuir?

1. Haz un fork del repositorio y clona tu copia.
2. Crea una rama nueva para tus cambios:

   ```sh
   git checkout -b mi-nueva-funcionalidad
   ```
3. Haz tus mejoras y comenta el código.
4. Haz un commit claro y push:

   ```sh
   git add .
   git commit -m "Agregada nueva funcionalidad de X"
   git push origin mi-nueva-funcionalidad
   ```
5. Haz un Pull Request desde tu fork.
   ¡Tus sugerencias, mejoras y fixes son bienvenidos!

---

## 📚 Créditos y referencias

* [pyannote.audio](https://github.com/pyannote/pyannote-audio)
* [Whisper (OpenAI)](https://github.com/openai/whisper)
* [Transformers (Hugging Face)](https://huggingface.co/docs/transformers/index)
* [ffmpeg](https://ffmpeg.org/)

---

## 🪪 Licencia

MIT — puedes usar y modificar este proyecto libremente.



---

