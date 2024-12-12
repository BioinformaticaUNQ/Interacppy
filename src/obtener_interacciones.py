import requests

def obtener_interacciones(proteina_id):
    """
    Obtiene las interacciones proteicas a partir de la base de datos STRING
    usando el identificador de proteína (Uniprot ID o PDB ID).
    
    Args:
    proteina_id (str): El identificador de la proteína (Uniprot o PDB).
    
    Returns:
    list: Una lista de interacciones (tuplas de proteínas).
    """
    # URL de la API de STRING
    url = f"https://string-db.org/api/json/network?identifiers={proteina_id}&species=9606"

    try:
        # Hacer la solicitud a la API
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        
        # Procesar la respuesta JSON
        data = response.json()

        # Lista para almacenar las interacciones
        interacciones = []

        # Recorremos los datos obtenidos para extraer las interacciones
        for item in data:
            proteina_1 = item['stringId_A']
            proteina_2 = item['stringId_B']
            interacciones.append((proteina_1, proteina_2))

        return interacciones
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return []
    
    '''
    
    

# Ejemplo de uso (luego pasar a tests)
proteina_id = "P12345"  # Sustituir por el Uniprot ID de la proteína que desees
interacciones = obtener_interacciones_string(proteina_id)

# Mostrar las interacciones
if interacciones:
    print(f"Interacciones obtenidas para la proteína {proteina_id}:")
    for interaccion in interacciones:
        print(f"- {interaccion[0]} <-> {interaccion[1]}")
else:
    print("No se obtuvieron interacciones.")

    '''