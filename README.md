# ING_SOLICITUDES

**ING_SOLICITUDES** es una solución diseñada para la extracción automatizada de contenido estructurado desde documentos Word, basada en títulos e índices predefinidos. La herramienta permite identificar secciones específicas dentro de los documentos y exportarlas en archivos independientes de forma eficiente.

## Funcionalidades Principales

1. **Identificación de Secciones:**
A través del procesamiento de documentos Word, se detectan títulos en el índice que contienen palabras clave específicas. El sistema identifica automáticamente las secciones relacionadas.

2. **Extracción de Contenido por Estilo:**
Utiliza los estilos aplicados en los documentos Word para determinar de manera precisa dónde comienzan y terminan las secciones.

3: **Exportación Automatizada:**
Las secciones identificadas se exportan en documentos Word separados, nombrados automáticamente según el título correspondiente.

4: **Gestión de Keywords:**
Las palabras clave para la búsqueda se cargan desde un archivo de texto externo, facilitando la actualización y personalización sin necesidad de modificar el código.

## Componentes Clave

- **Procesamiento de Documentos**: Clase principal que maneja la lectura del archivo Word, extracción de títulos y búsqueda de contenido basado en estilos aplicados.
- **Exportación de Documentos**: Módulo que toma las secciones extraídas y las guarda en archivos Word independientes en un directorio de salida predefinido.
- **Sistema de Logging**: Infraestructura que registra cada paso del proceso en un archivo de log con formato detallado.

## Requisitos

- Python 3.11+
- Dependencias especificadas en requirements.txt
- Docker (opcional, para despliegues en contenedores)

## Configuración

La configuración de la aplicación se realiza a través de variables de entorno definidas en un archivo .env. Estas incluyen:

`INPUT_FILE`: Ruta al archivo Word que se desea procesar.
`OUTPUT_FOLDER`: Carpeta donde se guardarán los archivos exportados.
`KEYWORDS_FILE`: Archivo de texto que contiene las palabras clave, una por línea.

## Ejecución

1. Coloca el archivo Word que deseas procesar en el directorio especificado en `INPUT_FILE`.
2. Define las palabras clave en el archivo de texto indicado por `KEYWORDS_FILE`.
3. Ejecuta la solución. Los documentos generados se guardarán automáticamente en la carpeta especificada por `OUTPUT_FOLDER`.

## Licencia

Esta aplicación ha sido desarrollada por Artica+i.
