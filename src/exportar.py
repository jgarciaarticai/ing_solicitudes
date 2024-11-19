from docx import Document
import os
import re
import logging

class DocumentExporter:
    def __init__(self, sections, output_dir):
        self.sections = sections
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)  # Logger para el exportador

    def export_section(self, title, export_format="docx"):
        """Exporta una sección específica basada en el título."""
        if not self.sections:
            self.logger.warning("No hay secciones para exportar.")
            return

        if title not in self.sections:
            self.logger.warning(f"Título no encontrado: {title}")
            return

        try:
            os.makedirs(self.output_dir, exist_ok=True)
            new_doc = Document()
            # Agregar el título al principio del documento
            new_doc.add_heading(title, level=1)
            # Agregar contenido de la sección
            section_content = self.sections[title]
            for paragraph in section_content.split("\n"):
                new_doc.add_paragraph(paragraph)

            # Sanitizar título para evitar caracteres no válidos en nombres de archivo
            sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
            file_name = f"{self.output_dir}/{sanitized_title}.{export_format}"

            # Guardar archivo
            new_doc.save(file_name)
            self.logger.info(f"Documento exportado: {file_name}")
        except Exception as e:
            self.logger.exception(f"Error al exportar la sección '{title}': {e}")


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
