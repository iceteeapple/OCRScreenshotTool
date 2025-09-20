# Python-Skript zum Installieren der Bibliotheken
import subprocess
import sys

def install_packages():
    packages = [
        "opencv-python",
        "pytesseract",
        "reportlab",
        "Pillow"
    ]

    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_packages()

