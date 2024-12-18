# Análizador de Interacciones Proteicas

Este proyecto permite realizar el mapeo de interacciones proteicas a partir de datos provenientes de diversas fuentes como PDB, UniProt o archivos locales. Utilizando la base de datos STRING, el programa genera un mapeo de todas las proteínas que interactúan con la proteína objetivo, permitiendo además la visualización y almacenamiento de estas interacciones en formato JSON.

## Descripción

La herramienta permite:
- Cargar secuencias de proteínas a partir de un ID PDB, archivo PDB local, o ID UniProt.
- Consultar las interacciones de proteínas en la base de datos STRING.
- Visualizar las interacciones obtenidas.
- Guardar las interacciones en un archivo JSON.

## Instalación

Pasos para la Instalación

1. **Crear un entorno virtual con Python 3.10.12**:
   ```bash
   python3.10 -m venv myenv
   ```

2. **Activar el entorno virtual**:
   - **Windows**:
     ```bash
     myenv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source myenv/bin/activate
     ```

3. **Instalar las dependencias necesarias**:
   ```bash
   pip install biopython matplotlib networkx
   ```

## Requerimientos

El proyecto ha sido desarrollado utilizando Python y hace uso de varias bibliotecas. Los requisitos específicos para su ejecución son los siguientes:

- Python 3.7 o superior
- Librerías necesarias:
  - `argparse`: Para el manejo de argumentos de línea de comandos.
  - `re`: Para validación de expresiones regulares.
  - `requests`: Para la comunicación con las APIs de UniProt y STRING.
  - `json`: Para trabajar con archivos JSON.

## Parámetros Principales

--pdb : ID de PDB para cargar la secuencia de proteína.
--archivo : Ruta a un archivo local en formato .pdb.
--uniprot : ID de UniProt para cargar la secuencia de proteína.
--visualizar : Visualiza las interacciones proteicas.
--salida : Formato de salida (uniprot, ensembl, pdb).
--guardar : Ruta para guardar el archivo JSON con las interacciones.

## Ejemplo de uso

Cargar un ID de PDB y visualizar interacciones:
"python main.py --pdb 1A2B --visualizar"

Guardar interacciones en un archivo JSON:
"python main.py --uniprot P12345 --guardar interacciones.json"
