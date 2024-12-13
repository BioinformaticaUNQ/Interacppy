import requests

def convertir_a_uniprot(ids, from_db="STRING", to_db="UniProtKB"):
    """
    Convierte identificadores desde una base de datos (ej. STRING) a UniProt IDs.
    
    Args:
    ids (list): Lista de IDs a convertir.
    from_db (str): Base de datos de origen (por defecto "STRING").
    to_db (str): Base de datos destino (por defecto "UniProtKB").
    
    Returns:
    dict: Diccionario con mapeos {id_original: id_uniprot}.
    """
    # Endpoint de UniProt para realizar el mapeo
    url = "https://rest.uniprot.org/idmapping/run"

    # Preparar los datos de la solicitud
    data = {
        "from": from_db,
        "to": to_db,
        "ids": ",".join(ids)
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        # Hacer la solicitud de mapeo
        response = requests.post(url, data=data, headers=headers)
        
        # Verificar si la respuesta fue exitosa
        if response.status_code != 200:
            print(f"Error en la solicitud: {response.status_code}")
            print(f"Detalles del error: {response.text}")
            return {}

        # Obtener el Job ID para el mapeo
        job_id = response.json().get("jobId")
        if not job_id:
            print("Error: no se pudo obtener un jobId.")
            return {}

        print(f"Job ID recibido: {job_id}")

        # Verificar el estado del trabajo hasta que esté listo
        result_url = f"https://rest.uniprot.org/idmapping/results/{job_id}"

        # Consultar el estado del trabajo una sola vez
        status_response = requests.get(f"{result_url}/status")
        if status_response.status_code == 404:
            print(f"Error: El jobId no se encuentra en el servidor. Verifique si el mapeo fue completado.")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"Error al convertir IDs: {e}")
        return {}



def obtener_interacciones(proteina_id):
    """
    Obtiene las interacciones proteicas a partir de la base de datos STRING
    usando el identificador de proteína (Uniprot ID o PDB ID).
    
    Args:
    proteina_id (str): El identificador de la proteína (Uniprot o PDB).
    
    Returns:
    list: Una lista de interacciones (tuplas de proteínas con UniProt IDs).
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

        # Recolectar todos los identificadores para la conversión
        ids_para_convertir = set()
        for item in data:
            ids_para_convertir.add(item['stringId_A'])
            ids_para_convertir.add(item['stringId_B'])
        
        # Convertir a UniProt IDs
        mapeo_ids = convertir_a_uniprot(list(ids_para_convertir))

        # Crear la lista de interacciones con UniProt IDs
        for item in data:
            proteina_1 = mapeo_ids.get(item['stringId_A'], item['stringId_A'])
            proteina_2 = mapeo_ids.get(item['stringId_B'], item['stringId_B'])
            interacciones.append((proteina_1, proteina_2))

        return interacciones
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return []
