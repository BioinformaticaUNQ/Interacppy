import json
import os

def guardar_interacciones_json(interacciones, ruta_archivo):
    """
    Guarda las interacciones en un archivo JSON.

    :param interacciones: Lista con las interacciones a guardar.
    :param ruta_archivo: Ruta del archivo donde se guardarán las interacciones.
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
        
        # Guardar las interacciones en formato JSON
        with open(ruta_completa, 'w', encoding='utf-8') as file:
            json.dump(interacciones, file, indent=4, ensure_ascii=False)
        print(f"Interacciones guardadas en: {ruta_completa}")
    
    except Exception as e:
        print(f"Error al guardar las interacciones en JSON: {e}")