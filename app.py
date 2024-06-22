import streamlit as st
import fitz
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def procesar_pdf(archivo):
    try:
        doc = fitz.open(stream=archivo.read(), filetype="pdf")
        buffer = io.BytesIO()
        pdf_output = canvas.Canvas(buffer, pagesize=letter)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            pdf_output.setPageSize((page.rect.width, page.rect.height))
            
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        text = ""
                        for span in line["spans"]:
                            if "italic" in span["font"].lower():
                                text += f"_{span['text']}_"
                            else:
                                text += span["text"]
                        
                        # Aplicar lógica similar a la macro
                        if text.strip() and not text.strip().endswith(('.', ':', ')', '?', '_')) and not text.strip()[-1].isdigit():
                            text += " "
                        else:
                            text += "\n"
                        
                        pdf_output.setFont("Helvetica", 10)
                        y = page.rect.height - line["bbox"][1]
                        pdf_output.drawString(line["bbox"][0], y, text)
            
            pdf_output.showPage()
        
        pdf_output.save()
        doc.close()
        
        buffer.seek(0)
        return buffer
    
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        return None

st.title("Modificador de PDF - Eliminar ciertos saltos de línea")
st.write("Sube un archivo PDF para eliminar ciertos saltos de línea y mantener el formato.")

archivo = st.file_uploader("Subir archivo PDF", type="pdf")

if archivo is not None:
    if st.button("Procesar PDF"):
        pdf_modificado = procesar_pdf(archivo)
        if pdf_modificado:
            st.download_button(
                label="Descargar PDF modificado",
                data=pdf_modificado,
                file_name="pdf_modificado.pdf",
                mime="application/pdf"
            )
