import logging
from procesamiento import DocumentProcessor
from logging_config import setup_logging

log_file_path = setup_logging()
logger = logging.getLogger(__name__)  # Logger específico para este script

file_path = "\\\\server19\\Digitalizacion\\PROYECTOS INTERNOS\\INGENIERIA Solicitudes\\Ejemplo test\\399-PE-Memoria.docx"
keywords = ["FLUIDOS", "ELECTRICIDAD", "CLIMATIZACIÓN"]

try:
    processor = DocumentProcessor(file_path)
    processor.load_document()
    processor.identify_sections(keywords)

    logger.info("Procesamiento completado exitosamente.")

except Exception as e:
    logger.exception("Error durante el procesamiento del documento.")