import streamlit as st
import fitz
import io

def modificar_pdf(archivo):
    try:
        # Abrir el PDF
        doc = fitz.open(stream=archivo.read(), filetype="pdf")
        
        for pagina in doc:
            texto_cursiva = ""
            for bloque in pagina.get_text("dict")["blocks"]:
                if "lines" in bloque:
                    for linea in bloque["lines"]:
                        for span in linea["spans"]:
                            if "italic" in span["font"].lower():
                                texto_original = span["text"]
                                texto_modificado = f"_{texto_original}_"
                                
                                # Reemplazar directamente el texto
                                pagina.search_for(texto_original)
                                pagina.add_redact_annot(span["bbox"])
                                pagina.apply_redactions()
                                pagina.insert_text(span["origin"], texto_modificado, fontname=span["font"], fontsize=span["size"])

        # Guardar el PDF modificado en memoria
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
