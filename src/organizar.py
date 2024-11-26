import os
import shutil
import logging
import pandas as pd

class DocumentOrganizer:
    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.logger = logging.getLogger(__name__)

    def organize_documents(self, mapping_file, cliente_base_path):
        """Organiza documentos en carpetas basadas en el mapeo del archivo Excel. Reemplaza 'cliente' en la ruta con la ruta base proporcionada por el usuario."""
        try:
            # Leer el mapeo desde el archivo Excel
            mapping = pd.read_excel(mapping_file)

            for _, row in mapping.iterrows():
                keyword = row['keyword']
                raw_path = row['ruta']

                # Reemplazar 'cliente' en la ruta con la ruta base del cliente proporcionada
                replaced_path = raw_path.replace("cliente\\", "")
                target_folder = os.path.normpath(os.path.join(cliente_base_path, replaced_path)).replace("\\","/")  # Normalizar ruta final
                # Crear la carpeta de destino completa si no existe
                os.makedirs(target_folder, exist_ok=True)

                # Buscar el archivo en la carpeta de entrada
                moved = False
                for filename in os.listdir(self.input_dir):
                    if keyword.lower() in filename.lower():
                        file_path = os.path.join(self.input_dir, filename)
                        # Mover el archivo al destino final
                        shutil.move(file_path, os.path.join(target_folder, filename))
                        self.logger.info(f"Documento movido: {filename} -> {target_folder}")
                        moved = True
                        break

                if not moved:
                    self.logger.warning(f"No se encontró un archivo para la keyword: {keyword}")

        except Exception as e:
            self.logger.exception(f"Error organizando documentos: {e}")
