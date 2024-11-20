from docx import Document
import os
import re
import logging
from docx.shared import Inches
from docx.oxml.ns import qn
from PIL import Image
from io import BytesIO
import base64

class DocumentExporter:
    def __init__(self, sections, output_dir):
        self.sections = sections
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)  # Logger para el exportador

    def export_section(self, title, export_format="docx"):
        """Exporta una sección específica basada en el título."""
        try:
            if title not in self.sections:
                self.logger.error(f"Título no encontrado: {title}")
                return

            # Crear directorio si no existe
            os.makedirs(self.output_dir, exist_ok=True)

            # Crear documento
            new_doc = Document()
            new_doc.add_heading(title, level=1)

            for element in self.sections[title]:
                if element["type"] == "text":
                    para = new_doc.add_paragraph()
                    self._add_formatted_text(para, element["content"])
                elif element["type"] == "image":
                    self._add_image_to_document(new_doc, element["content"])

            # Guardar archivo
            sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)  # Evitar caracteres no válidos en nombres de archivo
            file_name = f"{self.output_dir}/{sanitized_title}.{export_format}"
            new_doc.save(file_name)
            self.logger.info(f"Documento exportado: {file_name}")
        except Exception as e:
            self.logger.exception(f"Error al exportar la sección '{title}': {e}")


    def _add_formatted_text(self, para, text_elements):
        """Agrega texto con formato al párrafo."""
        try:
            for element in text_elements:
                run = para.add_run(element["text"])
                run.bold = element.get("bold", False)
                run.italic = element.get("italic", False)
                run.underline = element.get("underline", False)
        except Exception as e:
            self.logger.exception(f"Error al agregar texto con formato: {e}")


    def _add_image_to_document(self, doc, run):
        """Agrega una imagen extraída a un documento."""
        try:
            # Buscar el elemento blip en el XML de la imagen
            blip_elements = run._element.xpath(".//a:blip")
            for blip in blip_elements:
                # Obtener la relación de la imagen
                embed = blip.get(qn("r:embed"))
                if embed:
                    # Acceder al paquete de imágenes
                    part = run.part.related_parts[embed]
                    image_data = part.blob  # Datos binarios de la imagen

                    # Guardar temporalmente la imagen
                    temp_image = BytesIO(image_data)
                    img = Image.open(temp_image)
                    img_format = img.format.lower()

                    # Guardar la imagen como archivo temporal
                    temp_image_path = f"temp_image.{img_format}"
                    img.save(temp_image_path)

                    # Insertar la imagen en el documento
                    doc.add_picture(temp_image_path, width=Inches(4))

                    # Eliminar el archivo temporal
                    os.remove(temp_image_path)

        except Exception as e:
            self.logger.exception(f"Error al agregar imagen al documento: {e}")

    def export_all_sections(self, export_format="docx"):
        """Exporta todas las secciones disponibles."""
        if not self.sections:
            self.logger.warning("No hay secciones para exportar.")
            return

        try:
            os.makedirs(self.output_dir, exist_ok=True)
            for title in self.sections:
                self.export_section(title, export_format=export_format)
            self.logger.info("Todas las secciones se han exportado correctamente.")
        except Exception as e:
            self.logger.exception(f"Error al exportar las secciones: {e}")
