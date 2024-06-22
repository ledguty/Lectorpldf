import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io
import base64

def pdf_to_img(pdf_bytes):
    return convert_from_bytes(pdf_bytes)

def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

st.title("Visualizador de PDF (Manteniendo Diseño)")

archivo_subido = st.file_uploader("Sube tu archivo PDF", type="pdf")

if archivo_subido is not None:
    try:
        imagenes = pdf_to_img(archivo_subido.read())
        
        for i, img in enumerate(imagenes):
            st.subheader(f"Página {i+1}")
            st.image(img, use_column_width=True)
            
            # Botón para descargar la imagen
            st.markdown(get_image_download_link(img, f"pagina_{i+1}.png", f"Descargar página {i+1}"), unsafe_allow_html=True)
            
            st.write("---")  # Separador entre páginas

    except Exception as e:
        st.error(f"Error al procesar el PDF: {str(e)}")
