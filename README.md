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

## 🛠️ Instalación rápida

```sh
git clone https://github.com/tu_usuario/tu_repo.git
cd tu_repo
python3 -m pip install --upgrade pip
python3 scripts/setup_env.py
