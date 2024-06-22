import streamlit as st
import fitz
import base64

def procesar_texto(texto):
    lineas = texto.split('\n')
    texto_procesado = ""
    for i, linea in enumerate(lineas):
        linea = linea.strip()
        if linea:
            if i < len(lineas) - 1 and not linea.endswith(('.', ':', ')', '?', '_')) and not linea[-1].isdigit():
                texto_procesado += linea + " "
            else:
                texto_procesado += linea + "\n"
    return texto_procesado

def extraer_texto_pdf(archivo_pdf):
    texto_completo = ""
    try:
        doc = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
        for pagina in doc:
            texto_completo += pagina.get_text()
        doc.close()
    except Exception as e:
        st.error(f"Error al procesar el archivo PDF: {str(e)}")
    return texto_completo

def mostrar_pdf(archivo_pdf):
    base64_pdf = base64.b64encode(archivo_pdf.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.title("Visualizador de PDF con Extracción de Texto")
st.write("Sube un archivo PDF para visualizarlo y extraer su texto sin saltos de línea innecesarios.")

archivo = st.file_uploader("Subir archivo PDF", type="pdf")

if archivo is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Visualización del PDF")
        mostrar_pdf(archivo)
    
    with col2:
        st.subheader("Texto Extraído")
        texto_original = extraer_texto_pdf(archivo)
        texto_procesado = procesar_texto(texto_original)
        st.text_area("Texto sin saltos de línea innecesarios:", value=texto_procesado, height=400)
        
        # Botón para copiar el texto al portapapeles
        st.markdown(
            f"""
            <textarea id="texto_para_copiar" style="position: absolute; left: -9999px;">{texto_procesado}</textarea>
            <button onclick="copyToClipboard()">Copiar Texto</button>
            <script>
            function copyToClipboard() {{
                var copyText = document.getElementById("texto_para_copiar");
                copyText.select();
                document.execCommand("copy");
                alert("Texto copiado al portapapeles");
            }}
            </script>
            """,
            unsafe_allow_html=True
        )
