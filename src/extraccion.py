from docx import Document

class DocumentExporter:
    def __init__(self, sections, output_dir="output"):
        self.sections = sections
        self.output_dir = output_dir

    def export_sections(self, export_format="docx"):
        """Genera documentos nuevos basados en las secciones extraídas."""
        if not self.sections:
            print("No hay secciones para exportar.")
            return

        for i, section in enumerate(self.sections):
            new_doc = Document()
            for paragraph in section:
                new_doc.add_paragraph(paragraph)
            file_name = f"{self.output_dir}/seccion_{i + 1}.{export_format}"
            new_doc.save(file_name)
            print(f"Documento exportado: {file_name}")

# Ejemplo de uso
# exporter = DocumentExporter(sections=processor.get_sections())
# exporter.export_sections()
