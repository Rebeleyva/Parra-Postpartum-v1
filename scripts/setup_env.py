import os
import sys
import subprocess
import platform
import shutil

VENV_NAME = "Parra-Postpartum-v1"

# Detect OS
is_windows = platform.system() == "Windows"
is_mac = platform.system() == "Darwin"
is_linux = platform.system() == "Linux"

# 1. Crear el entorno virtual
if not os.path.exists(VENV_NAME):
    python_executable = shutil.which("python3.10") or shutil.which("python3")
    if python_executable is None:
        print("❌ Python 3.10 no encontrado. Instala Python 3.10 primero.")
        sys.exit(1)
    subprocess.check_call([python_executable, "-m", "venv", VENV_NAME])
else:
    print(f"🔵 El entorno virtual '{VENV_NAME}' ya existe.")

# 2. Activar el entorno virtual
if is_windows:
    activate_cmd = f"{VENV_NAME}\\Scripts\\activate"
    python_in_venv = f"{VENV_NAME}\\Scripts\\python.exe"
    pip_in_venv = f"{VENV_NAME}\\Scripts\\pip.exe"
else:
    activate_cmd = f"source ./{VENV_NAME}/bin/activate"
    python_in_venv = f"./{VENV_NAME}/bin/python"
    pip_in_venv = f"./{VENV_NAME}/bin/pip"

# 3. Actualizar pip
print("🔄 Actualizando pip...")
subprocess.check_call([python_in_venv, "-m", "pip", "install", "--upgrade", "pip"])

# 4. Instalar PyTorch con CUDA 12.1 solo si se requiere/cuadra con el sistema
#   En Mac NO se instala con CUDA, sólo CPU
if is_windows or is_linux:
    print("⚡ Instalando PyTorch (CUDA 12.1) + TorchVision + TorchAudio...")
    subprocess.check_call([
        pip_in_venv, "install",
        "torch==2.3.0+cu121",
        "torchvision==0.18.0+cu121",
        "torchaudio==2.3.0+cu121",
        "--index-url", "https://download.pytorch.org/whl/cu121"
    ])
else:
    print("⚡ Instalando PyTorch CPU para MacOS (sin CUDA)...")
    subprocess.check_call([
        pip_in_venv, "install", "torch", "torchvision", "torchaudio"
    ])

# 5. Instalar el resto de requirements.txt
print("📦 Instalando dependencias de requirements.txt...")
subprocess.check_call([pip_in_venv, "install", "-r", "requirements.txt"])

print("\n✅ Entorno virtual configurado exitosamente.")
if is_windows:
    print(f"Para activarlo: {activate_cmd}")
else:
    print(f"Para activarlo:\n{activate_cmd}")
