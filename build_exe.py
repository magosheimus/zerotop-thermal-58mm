"""
Script para criar executável do TopStart Thermal
"""

import PyInstaller.__main__
import os

# Diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Configuração do PyInstaller
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--name=ZeroTop Thermal 58mm',
    '--clean',
    '--noconfirm',
    '--add-data=printer.ico;.',
    '--icon=printer.ico',
])

print("\n" + "="*50)
print("Executável criado com sucesso!")
print("Localização: dist/TopStart Thermal.exe")
print("="*50)
