#!/bin/bash

# Instalar Tesseract OCR
sudo apt-get update
sudo apt-get install -y tesseract-ocr
sudo apt-get install -y tesseract-ocr-spa  # Para soporte en español

# Verificar la instalación
tesseract --version

# Crear un enlace simbólico si es necesario
sudo ln -s /usr/bin/tesseract /usr/local/bin/tesseract
