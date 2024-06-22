import streamlit as st
import fitz
import base64
import io

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
        # Leemos el archivo en memoria
        pdf_bytes = archivo_pdf.getvalue()
        
        # Verificamos si el archivo está vacío
        if len(pdf_bytes) == 0:
            raise ValueError("El archivo PDF está vacío")
        
        # Abrimos el PDF desde los bytes en memoria
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Verificamos si el documento tiene páginas
        if doc.page_count == 0:
            raise ValueError("El PDF no contiene páginas")
        
        for pagina in doc:
            texto_completo += pagina.get_text()
        doc.close()
    except Exception as e:
        st.error(f"Error al procesar el archivo PDF: {str(e)}")
        return None
    return texto_completo

def mostrar_pdf(archivo_pdf):
    base64_pdf = base64.b64encode(archivo_pdf.getvalue()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.title("Visualizador de PDF con Extracción de Texto")
st.write("Sube un archivo PDF para visualizarlo y extraer su texto sin saltos de línea innecesarios.")

archivo = st.file_uploader("Subir archivo PDF", type="pdf")

if archivo is not None:
    # Verificamos si el archivo tiene contenido
    if archivo.size == 0:
        st.error("El archivo subido está vacío. Por favor, sube un PDF válido.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Visualización del PDF")
            mostrar_pdf(archivo)
        
        with col2:
            st.subheader("Texto Extraído")
            texto_original = extraer_texto_pdf(archivo)
            if texto_original:
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
            else:
                st.error("No se pudo extraer texto del PDF. El archivo podría estar dañado o protegido.")
