import streamlit as st
import fitz
import io

def modificar_pdf(archivo, modo_frase=True):
    try:
        doc = fitz.open(stream=archivo.read(), filetype="pdf")
        
        for pagina in doc:
            texto = pagina.get_text("dict")
            for bloque in texto["blocks"]:
                if "lines" in bloque:
                    for linea in bloque["lines"]:
                        frase_cursiva = ""
                        for span in linea["spans"]:
                            if span["flags"] & 2**3:  # Verifica si el texto está en cursiva
                                if modo_frase:
                                    frase_cursiva += span["text"] + " "
                                else:
                                    pagina.draw_rect(span["bbox"], color=(1, 1, 1), fill=(1, 1, 1))
                                    pagina.insert_text((span["origin"][0], span["origin"][1]), f"_{span['text']}_", fontsize=span["size"])
                            else:
                                if modo_frase and frase_cursiva:
                                    bbox = fitz.Rect(linea["bbox"])
                                    pagina.draw_rect(bbox, color=(1, 1, 1), fill=(1, 1, 1))
                                    pagina.insert_text((bbox.x0, bbox.y0), f"_{frase_cursiva.strip()}_", fontsize=linea["spans"][0]["size"])
                                    frase_cursiva = ""
                        if modo_frase and frase_cursiva:
                            bbox = fitz.Rect(linea["bbox"])
                            pagina.draw_rect(bbox, color=(1, 1, 1), fill=(1, 1, 1))
                            pagina.insert_text((bbox.x0, bbox.y0), f"_{frase_cursiva.strip()}_", fontsize=linea["spans"][0]["size"])

        output_buffer = io.BytesIO()
        doc.save(output_buffer, garbage=4, deflate=True, clean=True)
        doc.close()
        
        return output_buffer
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        return None

st.title("Modificador de PDF - Añadir guiones bajos a texto en cursiva")
st.write("Sube un archivo PDF para añadir guiones bajos a las frases en cursiva y descarga el PDF modificado.")

archivo = st.file_uploader("Subir archivo PDF", type="pdf")

modo_frase = st.checkbox("Añadir guiones bajos a frases completas en cursiva", value=True)

if archivo is not None:
    if st.button("Procesar PDF"):
        pdf_modificado = modificar_pdf(archivo, modo_frase)
        if pdf_modificado:
            st.download_button(
                label="Descargar PDF modificado",
                data=pdf_modificado,
                file_name="pdf_modificado.pdf",
                mime="application/pdf"
            )
