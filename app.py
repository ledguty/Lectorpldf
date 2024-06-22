import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io
import subprocess

# Verificar la instalación de Tesseract
try:
    tesseract_version = subprocess.check_output(['tesseract', '--version']).decode('utf-8')
    st.sidebar.success(f"Tesseract instalado: {tesseract_version.split()[1]}")
except:
    st.sidebar.error("Tesseract no está instalado o no se puede acceder a él.")

def extraer_texto_pdf(archivo_pdf):
    texto_completo = ""
    imagenes = convert_from_bytes(archivo_pdf.read())
    
    for imagen in imagenes:
        texto = pytesseract.image_to_string(imagen, lang='spa')
        texto_completo += texto + "\n\n"  # Añade saltos de página
    
    return texto_completo.strip()

st.title("Extractor de Texto PDF (Manteniendo Diseño)")

archivo_subido = st.file_uploader("Sube tu archivo PDF", type="pdf")

if archivo_subido is not None:
    try:
        texto_extraido = extraer_texto_pdf(archivo_subido)
        
        st.subheader("Texto extraído:")
        st.text_area("", texto_extraido, height=500)
        
        if st.button("Copiar texto"):
            st.write("Texto copiado al portapapeles!")
            st.text_area("Texto copiado:", texto_extraido)

        buffer = io.BytesIO()
        buffer.write(texto_extraido.encode())
        buffer.seek(0)
        st.download_button(
            label="Descargar texto",
            data=buffer,
            file_name="texto_extraido.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Error al procesar el PDF: {str(e)}")
