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
                        for span in linea["spans"]:
                            if "italic" in span["font"].lower():
                                # Modificar el texto en cursiva
                                palabras = re.findall(r'\w+', span["text"])
                                nuevo_texto = " ".join([f"_{palabra}_" for palabra in palabras])
                                
                                # Reemplazar el texto original con el nuevo texto
                                pagina.add_redact_annot(span["bbox"], text=nuevo_texto)
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
st.write("Sube un archivo PDF para añadir guiones bajos a las palabras en cursiva y descarga el PDF modificado.")

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
