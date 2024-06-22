import streamlit as st
import fitz
import io
from docx import Document
from docx.shared import Pt
import re

def es_cursiva(font):
    return "italic" in font.lower() or "oblique" in font.lower()

def modificar_pdf(archivo):
    try:
        doc = fitz.open(stream=archivo.read(), filetype="pdf")
        texto_completo = ""
        
        for pagina in doc:
            texto = pagina.get_text("dict")
            for bloque in texto["blocks"]:
                if "lines" in bloque:
                    for linea in bloque["lines"]:
                        for span in linea["spans"]:
                            if es_cursiva(span["font"]):
                                texto_completo += f"_{span['text']}_"
                            else:
                                texto_completo += span["text"]
                        texto_completo += "\n"
                    texto_completo += "\n"
        
        doc.close()
        return texto_completo
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        return None

def procesar_texto(texto):
    # Eliminar saltos de línea específicos
    lineas = texto.split('\n')
    texto_procesado = ""
    for i in range(len(lineas)):
        if i < len(lineas) - 1:
            linea_actual = lineas[i].strip()
            if linea_actual and not linea_actual.endswith(('.', ':', ')', '?', '_')) and not linea_actual[-1].isdigit():
                texto_procesado += linea_actual + " "
            else:
                texto_procesado += linea_actual + "\n"
        else:
            texto_procesado += lineas[i]
    
    return texto_procesado

def crear_documento_word(texto):
    doc = Document()
    for parrafo in texto.split('\n'):
        p = doc.add_paragraph()
        partes = re.split(r'(_[^_]+_)', parrafo)
        for parte in partes:
            if parte.startswith('_') and parte.endswith('_'):
                run = p.add_run(parte[1:-1])
                run.italic = True
            else:
                p.add_run(parte)
    
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    return output_buffer.getvalue()

st.title("Convertir PDF a Word con modificaciones")
st.write("Sube un archivo PDF para convertirlo a Word, añadiendo guiones bajos a las cursivas y aplicando formato específico.")

archivo = st.file_uploader("Subir archivo PDF", type="pdf")

if archivo is not None:
    if st.button("Procesar PDF"):
        texto_modificado = modificar_pdf(archivo)
        if texto_modificado:
            texto_procesado = procesar_texto(texto_modificado)
            docx_modificado = crear_documento_word(texto_procesado)
            st.download_button(
                label="Descargar documento Word modificado",
                data=docx_modificado,
                file_name="documento_modificado.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
