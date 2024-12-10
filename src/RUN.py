import os
import logging
from decouple import config
from logging_config import setup_logging
from procesar import DocumentProcessor
from exportar import DocumentExporter
from organizar import DocumentOrganizer
from insertar import ContentInserter

# Configuración del logging
log_file_path = setup_logging()
logger = logging.getLogger(__name__)

try:
    # Rutas desde el archivo .env o configuración de Docker Compose
    input_dir = config("INPUT_FOLDER")
    output_dir = config("OUTPUT_FOLDER")
    map_file_path = config("MAP_FILE")
    keywords_file_path = config("KEYWORDS_FILE")

    logger.info("Configuración y rutas cargadas correctamente.")
except Exception as e:
    logger.exception(f"Error al leer las variables de entorno: {e}")
    raise


def load_keywords(file_path):
    """Carga las palabras clave desde un archivo."""
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

# Flujo principal
try:
    # Pedir al usuario el nombre del cliente
    cliente_name = input("Ingrese la ruta a la carpeta del cliente: ").strip()
    logger.info(f"Nombre de cliente introducido: {cliente_name}")
    if not cliente_name:
        raise ValueError("El nombre del cliente no puede estar vacío.")

    # Cargar las keywords
    keywords = load_keywords(keywords_file_path)
    if not keywords:
        logger.error("No se pudieron cargar las keywords. Finalizando.")
        exit()

    # Procesar documentos
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        processor = DocumentProcessor(file_path)
        processor.load_document()
        processor.identify_sections(keywords)

        sections = processor.get_sections()
        if sections:
            exporter = DocumentExporter(sections, output_dir)
            exporter.export_all_sections(export_format="docx")
        
        inserter = ContentInserter(input_dir=output_dir, config_dir="config", exporter=exporter)
        proyecto_menor = input("¿Es un proyecto menor? (s/n): ").strip().lower() == 's'
        inserter.process_files(mapping_file=map_file_path, proyecto_menor=proyecto_menor)

    logger.info("Procesamiento y exportación completados exitosamente.")

    # Organizar documentos
    organizer = DocumentOrganizer(output_dir)
    organizer.organize_documents(map_file_path, cliente_name, proyecto_menor)  # Aquí se usa cliente_base_path

    logger.info("Documentos organizados en carpetas correctamente.")

except Exception as e:
    logger.exception("Error durante el procesamiento del documento.")
