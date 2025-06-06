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

1. **Conversión de video a audio:** Si el archivo es video, lo convierte automáticamente a MP3 usando ffmpeg, sin que tengas que hacer nada extra.
2. **Preprocesamiento y ecualización:** Aplica filtrado y normalización al audio, enfocándose en la banda de la voz humana (300–3400 Hz) para máxima claridad.
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

---

## 🛠️ Instalación rápida

    ```sh
    git clone https://github.com/tu_usuario/tu_repo.git
    cd tu_repo
    python3 -m pip install --upgrade pip
    python3 scripts/setup_env.py

---

1.  shCopyEditpython3 -m pip install --upgrade pippython3 setup\_env.pyEsto instalará todas las dependencias en un entorno virtual llamado **Parra-Postpartum-v1**.
    
2.  Copia el ejemplo y pega tu token de HuggingFace:shCopyEditcp .env.example .envEdita el archivo .env para incluir tu token:iniCopyEditHUGGINGFACE\_TOKEN=tu\_token\_de\_huggingface\_aqui
    
3.  **(Opcional) Instala ffmpeg si no lo tienes**
    
    *   **Ubuntu/Debian:** sudo apt install ffmpeg
        
    *   **MacOS:** brew install ffmpeg
        
    *   **Windows:** Descarga desde [ffmpeg.org](https://ffmpeg.org/)
        

⚡ Uso del programa
------------------

### Activar entorno virtual

*   shCopyEditsource Parra-Postpartum-v1/bin/activate
    
*   shCopyEditParra-Postpartum-v1\\Scripts\\activate
    

### Procesar un archivo (audio o video)

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`shCopyEditpython post_partum.py` 

#### **Ejemplo de uso:**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   shCopyEditpython post_partum.py entrevista.mp3  python post_partum.py reunion_familiar.mp4   `

> El programa detecta automáticamente el tipo de archivo y realiza todas las etapas de conversión, procesamiento, diarización y transcripción, guardando todo en una carpeta /resultados//.

🏭 Funcionamiento detallado del script principal (post\_partum.py)
------------------------------------------------------------------

1.  **Detecta el tipo de archivo:**
    
    *   Si es audio soportado (.wav, .mp3, .m4a), lo procesa directo.
        
    *   Si es video (.mp4, .avi, .mov, etc.), extrae el audio a MP3 automáticamente.
        
2.  **Preprocesa el audio:**
    
    *   Convierte a WAV, fuerza 16kHz mono.
        
    *   Aplica filtrado pasa banda (300–3400 Hz) para mejorar calidad.
        
    *   Normaliza el volumen para evitar clipping.
        
3.  **Diariza:**
    
    *   Usa pyannote para detectar intervalos y asignar un label a cada hablante.
        
    *   jsonCopyEdit\[ {"start\_time": 0.0, "end\_time": 11.5, "speaker": "SPEAKER\_00"}, {"start\_time": 11.5, "end\_time": 22.7, "speaker": "SPEAKER\_01"}\]
        
4.  **Transcribe:**
    
    *   Toma cada segmento identificado y lo transcribe usando Whisper.
        
    *   jsonCopyEdit\[ {"start\_time": 0.0, "end\_time": 11.5, "speaker": "SPEAKER\_00", "transcript": "buenos días a todos..."}, {"start\_time": 11.5, "end\_time": 22.7, "speaker": "SPEAKER\_01", "transcript": "gracias por venir."}\]
        
5.  **Guarda resultados en /resultados//:**
    
    *   Audio original
        
    *   Audio convertido (si aplica)
        
    *   Audio procesado (\*\_processed.wav)
        
    *   diarization\_results.json
        
    *   aligned\_transcription.json
        


📝 Ejemplo de salida de resultados
----------------------------------

*   jsonCopyEdit\[ {"start\_time": 0.0, "end\_time": 9.8, "speaker": "SPEAKER\_00"}, {"start\_time": 9.8, "end\_time": 16.5, "speaker": "SPEAKER\_01"}\]
    
*   jsonCopyEdit\[ {"start\_time": 0.0, "end\_time": 9.8, "speaker": "SPEAKER\_00", "transcript": "buenos días, doctor..."}, {"start\_time": 9.8, "end\_time": 16.5, "speaker": "SPEAKER\_01", "transcript": "buenos días, cómo está."}\]
    

🛠️ Troubleshooting
-------------------

*   **No se activa el entorno virtual:**Asegúrate de usar python3.10 o superior y de estar en la carpeta raíz del proyecto.
    
*   **Error “No module named X”:**Verifica que el entorno virtual está activado antes de correr el script.
    
*   nginxCopyEditpip install torch torchvision torchaudio
    
*   **ffmpeg no encontrado:**Instálalo según tu sistema (ver sección de requisitos).
    
*   **Token de HuggingFace inválido:**Genera un nuevo token desde [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) y colócalo en tu .env.
    

🔑 Variables de entorno
-----------------------

Copia .env.example a .env y coloca tu token de HuggingFace:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   shCopyEditcp .env.example .env   `

Luego edita el archivo .env:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   iniCopyEditHUGGINGFACE_TOKEN=tu_token_de_huggingface_aqui   `

Este token es necesario para descargar modelos privados de pyannote/Whisper.

🙋‍♂️ ¿Cómo contribuir?
-----------------------

1.  Haz un fork del repositorio y clona tu copia.
    
2.  shCopyEditgit checkout -b mi-nueva-funcionalidad
    
3.  Haz tus mejoras y comenta el código.
    
4.  shCopyEditgit add .git commit -m "Agregada nueva funcionalidad de X"git push origin mi-nueva-funcionalidad
    
5.  Haz un Pull Request desde tu fork.¡Tus sugerencias, mejoras y fixes son bienvenidos!
    

📚 Créditos y referencias
-------------------------

*   [pyannote.audio](https://github.com/pyannote/pyannote-audio)
    
*   [Whisper (OpenAI)](https://github.com/openai/whisper)
    
*   Transformers (Hugging Face)
    
*   [ffmpeg](https://ffmpeg.org/)
    

🪪 Licencia
-----------

MIT — puedes usar y modificar este proyecto libremente.