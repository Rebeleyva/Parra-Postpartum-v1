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
   python3 scripts/setup_env.py
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

¡Por supuesto! Aquí tienes una **descripción de uso** profesional y clara, lista para README, que incluye:

* Versión de Python requerida
* Especificación de CUDA
* Recomendación de GPU
* Nota de uso de Vast.ai
* Indicación de que el ambiente virtual de este repo ya permite hacer fine-tuning

---

## 🧩 Descripción del Finetuning realizado para Whisper v3

Este script permite realizar **fine-tuning de modelos Whisper para transcripción de voz en español**, integrando todo el pipeline: descarga/preprocesamiento del dataset, aumentación de datos, extracción de features y entrenamiento supervisado, todo en un entorno controlado y reproducible.

* **Python requerido:** 3.10
* **CUDA recomendado:** CUDA 12.1+ (se ha probado exitosamente con PyTorch 2.3.0/cu121)
* **Ambiente:** El entorno virtual definido en este repositorio (`Parra-Postpartum-v1`) incluye todas las dependencias necesarias para ejecutar el preprocesamiento y entrenamiento, tanto en CPU como GPU.
* **Plataforma usada:** Este fine-tuning se realizó originalmente en un servidor cloud de **Vast.ai**, lo que garantiza compatibilidad y rendimiento óptimo en entornos con GPU dedicadas (por ejemplo, NVIDIA RTX 3090/4090, A100, V100, etc.).
* **Entrenamiento en CPU es posible**, pero muy lento y no recomendado para datasets medianos/grandes.

### **¿Cómo usarlo?**

1. **Activa el ambiente virtual del repositorio:**

   * En Mac/Linux:

     ```sh
     source Parra-Postpartum-v1/bin/activate
     ```
   * En Windows:

     ```sh
     Parra-Postpartum-v1\Scripts\activate
     ```

2. **Asegúrate de tener CUDA 12.1+ instalado y drivers NVIDIA actualizados** si vas a entrenar en GPU.
   Puedes revisar la instalación con:

   ```sh
   nvcc --version
   ```

3. **Ejecuta el script:**

   ```sh
   python scripts/finetuning-Whisper-v3.py
   ```

   El script se encargará de descargar/preprocesar el dataset, realizar aumentación de audio, preparar features y entrenar el modelo Whisper. Los modelos y procesadores fine-tuneados se guardan automáticamente en la carpeta `./whisper-finetuned-augment`.

4. **Customización:**
   Si deseas usar otro dataset o modelo base, edita las rutas/identificadores dentro del script antes de ejecutarlo.

### **Requisitos computacionales**

| Recurso          | Mínimo                             | Ideal/Recomendado                         |
| ---------------- | ---------------------------------- | ----------------------------------------- |
| **Python**       | 3.10                               | 3.10 (mismo entorno que el repo)          |
| **CUDA**         | No necesario (pero lento en CPU)   | CUDA 12.1+ (NVIDIA, compatible PyTorch)   |
| **GPU**          | Opcional (CPU posible, pero lento) | NVIDIA 3090/4090, A100, V100, 16 GB+ VRAM |
| **RAM**          | 16 GB                              | 32 GB+                                    |
| **Disco**        | 20 GB libres                       | 50 GB+ si usas datasets grandes           |
| **SO**           | Ubuntu 20.04+, MacOS, Windows 10+  | Ubuntu 22.04 LTS o similar                |
| **Dependencias** | Incluidas en el ambiente virtual   | Incluidas en el ambiente virtual          |

**Notas:**

* Si tienes una GPU NVIDIA y los drivers/CUDA instalados correctamente, el entrenamiento aprovechará automáticamente la aceleración por hardware.
* Se recomienda entrenar en plataformas tipo **Vast.ai**, Paperspace o Google Colab Pro+ para acelerar el proceso.
* El entorno virtual proporcionado en este repositorio te permite no solo inferencia sino también **entrenar y hacer fine-tuning de modelos Whisper** sin pasos adicionales.


---

## 📚 Créditos y referencias

* [pyannote.audio](https://github.com/pyannote/pyannote-audio)
* [Whisper (OpenAI)](https://github.com/openai/whisper)
* [Transformers (Hugging Face)](https://huggingface.co/docs/transformers/index)
* [ffmpeg](https://ffmpeg.org/)

---

¡Perfecto! Aquí tienes la **cita formal** para el dataset **CIEMPIESS TEST** y un bloque listo para incluir en tu README, documentación, artículo o sección de agradecimientos.
Incluyo también un párrafo de reconocimiento y la referencia en formato BibTeX.

---

## 📂 Dataset utilizado: CIEMPIESS TEST

Este proyecto utiliza el **CIEMPIESS TEST CORPUS** para la evaluación y prueba de modelos de reconocimiento automático de voz en español mexicano.

> **CIEMPIESS TEST** es un corpus equilibrado por género, compuesto por más de 3,500 grabaciones de voz espontánea en español mexicano, recopiladas y transcritas por el programa de servicio social "Desarrollo de Tecnologías del Habla" de la Facultad de Ingeniería de la UNAM.
> Las grabaciones provienen de "RADIO-IUS", estación de la Facultad de Derecho de la UNAM, y el corpus fue cuidadosamente anotado y verificado para asegurar su calidad.
> Se distribuye bajo la licencia [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) y está disponible en [Hugging Face Datasets](https://huggingface.co/datasets/ciempiess/ciempiess_test) y en [LDC2019S07](https://catalog.ldc.upenn.edu/LDC2019S07).

**Referencia:**

```bibtex
@misc{carlosmenaciempiesstest2019,
  title={CIEMPIESS TEST CORPUS: Audio and Transcripts of Mexican Spanish Broadcast Conversations.},
  ldc_catalog_no={LDC2019S07},
  DOI={https://doi.org/10.35111/xdx5-n815},
  author={Hernandez Mena, Carlos Daniel},
  journal={Linguistic Data Consortium, Philadelphia},
  year={2019},
  url={https://catalog.ldc.upenn.edu/LDC2019S07},
}
```

**Cómo citar este recurso en tu trabajo:**

> Hernandez Mena, Carlos Daniel. *CIEMPIESS TEST CORPUS: Audio and Transcripts of Mexican Spanish Broadcast Conversations.* Linguistic Data Consortium, Philadelphia, 2019. DOI: [10.35111/xdx5-n815](https://doi.org/10.35111/xdx5-n815).

**Reconocimientos especiales:**

* Al programa de servicio social "Desarrollo de Tecnologías del Habla" de la Facultad de Ingeniería, UNAM.
* A la Lic. César Gabriel Alanis Merchand y el Mtro. Ricardo Rojas Arévalo de la Facultad de Derecho, UNAM, por la donación de grabaciones.
* A Mónica Alejandra Ruiz López por la verificación de las transcripciones.


---

## 🪪 Licencia

MIT — puedes usar y modificar este proyecto libremente.



---

