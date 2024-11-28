from docx import Document
import pandas as pd
from pathlib import Path
import logging


class ContentInserter:
    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.logger = logging.getLogger(__name__)

    def insert_content(self, mapping_file):
        """Inserta contenido de documentos origen en apartados específicos de documentos destino, según las indicaciones del archivo Excel de mapeo."""
        try:
            # Leer el archivo de mapeo
            mapping = pd.read_excel(mapping_file)

            for _, row in mapping.iterrows():
                origen = row['keyword'].strip()
                destino = row['plantilla'].strip()

                origen_path = self.input_dir / origen
                destino_path = self.output_dir / destino

                if not origen_path.exists():
                    self.logger.warning(f"Documento origen no encontrado: {origen_path}")
                    continue

                if not destino_path.exists():
                    self.logger.warning(f"Documento destino no encontrado: {destino_path}")
                    continue

                # Cargar documentos
                doc_origen = Document(origen_path)
                doc_destino = Document(destino_path)

                # Extraer contenido del documento origen
                contenido_origen = self._extract_content(doc_origen)

                # Insertar contenido en el documento destino
                self._insert_content_in_section(doc_destino, apartado, contenido_origen)

                # Guardar cambios en el documento destino
                doc_destino.save(destino_path)
                self.logger.info(f"Contenido de '{origen}' insertado en el apartado '{apartado}' del documento '{destino}'.")

        except Exception as e:
            self.logger.exception(f"Error al insertar contenido: {e}")

    def _extract_content(self, doc):
        """
        Extrae todo el contenido de un documento Word.
        """
        content = []
        for para in doc.paragraphs:
            if para.text.strip():
                content.append(para.text)
        return content

    def _insert_content_in_section(self, doc, apartado, contenido):
        """
        Inserta contenido en el apartado especificado dentro del documento.
        """
        found = False
        for paragraph in doc.paragraphs:
            if apartado.lower() in paragraph.text.lower():
                found = True
                self.logger.info(f"Apartado encontrado: {paragraph.text}")
                for line in contenido:
                    doc.add_paragraph(line)
                break

        if not found:
            self.logger.warning(f"Apartado '{apartado}' no encontrado en el documento destino.")
