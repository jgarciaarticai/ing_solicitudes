import os
import logging
from decouple import config
from logging_config import setup_logging
from procesar import DocumentProcessor
from exportar import DocumentExporter

# Definir el directorio base de la solución
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración del logging
log_file_path = setup_logging()
logger = logging.getLogger(__name__)  # Logger específico para este script

try:
    # Rutas del archivo del documento y de las keywords
    input_dir = config("INPUT_FOLDER")
    output_dir = config("OUTPUT_FOLDER")
    keywords_file_path = config("KEYWORDS_FILE")

    logger.info("Configuración y rutas cargadas correctamente.")
except Exception as e:
    logger.exception(f"Error al leer las variables de entorno: {e}")


def load_keywords(file_path):
    logger.debug(f"Intentando abrir el archivo: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            logger.debug(f"Archivo abierto exitosamente: {file_path}")
            keywords = [line.strip() for line in file if line.strip()]
            logger.info(f"Keywords cargadas: {keywords}")
            return keywords
    except Exception as e:
        logger.exception(f"Error al cargar las keywords desde {file_path}: {e}")
        return []

# Cargar las keywords desde el archivo
keywords = load_keywords(keywords_file_path)

if not keywords:
    logger.error("No se pudieron cargar las keywords. Finalizando.")
else:
    try:
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
        processor = DocumentProcessor(file_path)
        processor.load_document()
        processor.identify_sections(keywords)

        # Exportar las secciones
        sections = processor.get_sections()
        if sections:
            exporter = DocumentExporter(sections, output_dir)
            exporter.export_all_sections(export_format="docx")

        logger.info("Procesamiento y exportación completados exitosamente.")

    except Exception as e:
        logger.exception("Error durante el procesamiento del documento.")
