from docx import Document
import os

class DocumentExporter:
    def __init__(self, sections, output_dir="output"):
        self.sections = sections
        self.output_dir = output_dir

    def export_section(self, title, export_format="docx"):
        """Exporta una sección específica basada en el título."""
        if not self.sections:
            print("No hay secciones para exportar.")
            return

        if title not in self.sections:
            print(f"Título no encontrado: {title}")
            return

        # Crear directorio si no existe
        os.makedirs(self.output_dir, exist_ok=True)

        # Crear documento
        new_doc = Document()
        for paragraph in self.sections[title]:
            new_doc.add_paragraph(paragraph)

        # Guardar archivo
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)  # Evitar caracteres no válidos en nombres de archivo
        file_name = f"{self.output_dir}/{sanitized_title}.{export_format}"
        new_doc.save(file_name)
        print(f"Documento exportado: {file_name}")
