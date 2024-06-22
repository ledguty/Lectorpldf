import streamlit as st
import fitz
import io

def modificar_pdf(archivo):
    try:
        # Abrir el PDF
        doc = fitz.open(stream=archivo.read(), filetype="pdf")
        
        for pagina in doc:
            # Obtener el texto de la página con información de estilo
            blocks = pagina.get_text("dict")["blocks"]
            for b in blocks:
                if "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            if "italic" in s["font"].lower():
                                # Obtener las coordenadas del texto
                                x0, y0, x1, y1 = s["bbox"]
                                texto_original = s["text"]
                                texto_modificado = f"_{texto_original}_"
                                
                                # Crear un rectángulo blanco para cubrir el texto original
                                pagina.draw_rect([x0, y0, x1, y1], color=(1, 1, 1), fill=(1, 1, 1))
                                
                                # Insertar el nuevo texto
                                pagina.insert_text((x0, y0), texto_modificado, fontsize=s["size"], color=(0, 0, 0))

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
