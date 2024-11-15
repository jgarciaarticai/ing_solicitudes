from docx import Document
import re


class DocumentProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.document = None
        self.sections = []

    def load_document(self):
        """Carga el documento Word y lo prepara para el procesamiento."""
        try:
            self.document = Document(self.file_path)
            print("Documento cargado con éxito.")
        except Exception as e:
            print(f"Error al cargar el documento: {e}")

    def identify_sections(self, keywords, custom_patterns=None):
        """Identifica secciones basadas en palabras clave y patrones personalizados."""
        if self.document is None:
            raise ValueError("El documento no ha sido cargado.")

        pattern = '|'.join(re.escape(keyword) for keyword in keywords)
        if custom_patterns:
            pattern += '|' + '|'.join(custom_patterns)
        regex = re.compile(pattern, re.IGNORECASE)

        current_section = []
        for para in self.document.paragraphs:
            if regex.search(para.text):
                if current_section:
                    self.sections.append(current_section)
                    current_section = []
            current_section.append(para.text)
        if current_section:
            self.sections.append(current_section)

        print(f"Secciones identificadas: {len(self.sections)}")

    def get_sections(self):
        """Devuelve las secciones identificadas para revisión o exportación."""
        return self.sections
