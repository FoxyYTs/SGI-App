import os
import subprocess

# Ruta a designer.exe
designer_path = os.path.join(os.path.dirname(os.__file__), "site-packages", "PySide6", "designer.exe")

# Ejecutar Qt Designer
subprocess.Popen([designer_path])