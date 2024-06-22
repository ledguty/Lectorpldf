import streamlit as st
import fitz
import io
import re

def modificar_pdf(archivo):
    try:
        # Abrir el PDF
        doc = fitz.open(stream=archivo.read(), filetype="pdf")
        
        for pagina in doc:
            # Obtener los bloques de texto de la página
            bloques = pagina.get_text("dict")["blocks"]
            for bloque in bloques:
                if "lines" in bloque:
                    for linea in bloque["lines"]:
                        texto_cursiva = ""
                        bbox_cursiva = None
                        for span in linea["spans"]:
                            if "italic" in span["font"].lower():
                                if not texto_cursiva:
                                    bbox_cursiva = span["bbox"]
                                texto_cursiva += span["text"] + " "
                            else:
                                if texto_cursiva:
                                    # Procesar el texto en cursiva acumulado
                                    nuevo_texto = f"_{texto_cursiva.strip()}_"
                                    pagina.add_redact_annot(bbox_cursiva, text=nuevo_texto)
                                    pagina.apply_redactions()
                                    texto_cursiva = ""
                                    bbox_cursiva = None
                        
                        # Procesar cualquier texto en cursiva restante al final de la línea
                        if texto_cursiva:
                            nuevo_texto = f"_{texto_cursiva.strip()}_"
                            pagina.add_redact_annot(bbox_cursiva, text=nuevo_texto)
                            pagina.apply_redactions()

        # Guardar el PDF modificado en memoria
        output_buffer = io.BytesIO()
        doc.save(output_buffer)
        doc.close()
        
        return output_buffer
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        return None

st.title("Modificador de PDF - Añadir guiones bajos a texto en cursiva")
st.write("Sube un archivo PDF para añadir guiones bajos a las frases en cursiva y descarga el PDF modificado.")

archivo = st.file_uploader("Subir archivo PDF", type="pdf")

if archivo is not None:
    if st.button("Procesar PDF"):
        pdf_modificado = modificar_pdf(archivo)
        if pdf_modificado:
            st.download_button(
                label="Descargar PDF modificado",
                data=pdf_modificado,
                file_name="pdf_modificado.pdf",
                mime="application/pdf"
            )
