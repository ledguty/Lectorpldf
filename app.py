import streamlit as st
import PyPDF2
import io

def extraer_texto_pdf(archivo_pdf):
    texto_completo = ""
    lector_pdf = PyPDF2.PdfReader(archivo_pdf)
    
    for pagina in lector_pdf.pages:
        texto = pagina.extract_text()
        texto = ' '.join(texto.split())
        texto_completo += texto + " "
    
    return texto_completo.strip()

st.title("Extractor de Texto PDF")

archivo_subido = st.file_uploader("Sube tu archivo PDF", type="pdf")

if archivo_subido is not None:
    texto_extraido = extraer_texto_pdf(archivo_subido)
    
    st.subheader("Texto extraído:")
    st.text_area("", texto_extraido, height=300)
    
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
