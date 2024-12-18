import json
import os

def guardar_interacciones_json(interacciones, ruta_archivo, identificadores=None):
    """
    Guarda las interacciones en un archivo JSON, asegurando que incluyan los identificadores correctos.

    :param interacciones: Lista de diccionarios con las interacciones a guardar.
    :param ruta_archivo: Ruta del archivo donde se guardarán las interacciones.
    :param identificadores: Diccionario opcional que mapea nombres genéricos a identificadores reales (ej. Uniprot o PDB IDs).
    """
    try:
        # Asegurarse de que la carpeta "resultados" exista
        if not os.path.exists('resultados'):
            os.makedirs('resultados')
            

        # Asegurarse de que el archivo tenga la extensión .json
        if not ruta_archivo.lower().endswith('.json'):
            ruta_archivo = f"{os.path.splitext(ruta_archivo)[0]}.json"

        # Crear la ruta completa del archivo en la carpeta "resultados"
        ruta_completa = os.path.join('resultados', os.path.basename(ruta_archivo))

        # Verificar si el archivo ya existe y modificar el nombre si es necesario
        if os.path.exists(ruta_completa):
            base, ext = os.path.splitext(ruta_completa)
            i = 1
            # Generar un nuevo nombre con un número añadido al final
            while os.path.exists(f"{base}_{i}{ext}"):
                i += 1
            ruta_completa = f"{base}_{i}{ext}"

        # Si se proporcionaron identificadores, reemplazar nombres genéricos por los reales
        if identificadores:
            for interaccion in interacciones:
                if "proteina_1" in interaccion:
                    interaccion["proteina_1"] = identificadores.get(interaccion["proteina_1"], interaccion["proteina_1"])
                if "proteina_2" in interaccion:
                    interaccion["proteina_2"] = identificadores.get(interaccion["proteina_2"], interaccion["proteina_2"])

        # Guardar las interacciones en formato JSON
        with open(ruta_completa, 'w', encoding='utf-8') as file:
            json.dump(interacciones, file, indent=4, ensure_ascii=False)
        print(f"Interacciones guardadas en: {ruta_completa}")
    
    except Exception as e:
        print(f"Error al guardar las interacciones en JSON: {e}")
