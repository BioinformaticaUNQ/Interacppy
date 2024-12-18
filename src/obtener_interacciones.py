import requests

import requests

import requests

def convertir_a_uniprot(ids):
    """
    Convierte identificadores usando la API de Ensembl para obtener UniProt IDs.
    
    Args:
    ids (list): Lista de IDs a convertir (por ejemplo, identificadores de Ensembl).
    
    Returns:
    dict: Diccionario con mapeos {id_original: id_uniprot}.
    """
    # URL base de la API de Ensembl
    server = "https://rest.ensembl.org"
    headers = {"Content-Type": "application/json"}

    mapeo_resultado = {}

    for id_ in ids:
        # Eliminar el prefijo "9606." si está presente
        id_sanitizado = id_.split(".")[-1]

        # Construir la URL del endpoint
        ext = f"/xrefs/id/{id_sanitizado}"

        try:
            # Realizar la solicitud
            response = requests.get(server + ext, headers=headers)
            response.raise_for_status()  # Lanza un error si la solicitud falla

            # Procesar la respuesta
            data = response.json()
            if data:
                # Asumimos que el primer resultado es el más relevante
                mapeo_resultado[id_] = data[0].get("primary_id")
            else:
                # Si no hay resultados, dejamos el ID original
                mapeo_resultado[id_] = None

        except requests.exceptions.RequestException as e:
            print(f"Error al procesar el ID {id_}: {e}")
            mapeo_resultado[id_] = None

    return mapeo_resultado


import requests

def convertir_a_pdb(ids):
    """
    Convierte identificadores de Ensembl a identificadores PDB usando la API de Ensembl.
    
    Args:
    ids (list): Lista de Ensembl IDs a convertir a PDB IDs.
    
    Returns:
    dict: Diccionario con mapeos {id_ensembl: id_pdb}.
    """
    # URL base de la API de Ensembl
    ensembl_server = "https://rest.ensembl.org"

    mapeo_resultado = {}

    for id_ in ids:
        # Eliminar el prefijo "9606." si está presente en el ID (aunque podría no ser necesario)
        id_sanitizado = id_.split(".")[-1]

        try:
            # Consultamos Ensembl para obtener los datos de XREF de Ensembl
            ext_ensembl = f"/xrefs/id/{id_sanitizado}"
            response_ensembl = requests.get(ensembl_server + ext_ensembl, headers={"Content-Type": "application/json"})
            response_ensembl.raise_for_status()  # Verifica si la solicitud fue exitosa
            
            # Procesar la respuesta de Ensembl
            data_ensembl = response_ensembl.json()

            pdb_ids = []
            for entry in data_ensembl:
                if entry.get("dbname") == "PDB":  # Filtramos solo los XREF de PDB
                    pdb_ids.append(entry.get("primary_id"))

            if pdb_ids:
                # Usamos el primer PDB ID relacionado con el Ensembl ID
                mapeo_resultado[id_] = pdb_ids[0]
            else:
                # Si no se encuentra PDB, asignamos None
                mapeo_resultado[id_] = None

        except requests.exceptions.RequestException as e:
            print(f"Error al procesar el ID {id_}: {e}")
            mapeo_resultado[id_] = None

    return mapeo_resultado



def obtener_interacciones(proteina_id, formato_salida="uniprot"):
    """
    Obtiene las interacciones proteicas a partir de la base de datos STRING
    usando el identificador de proteína (UniProt ID o PDB ID).
    
    Args:
    proteina_id (str): El identificador de la proteína (UniProt o PDB).
    
    Returns:
    dict: Un diccionario con la lista de interacciones y los atributos
          destacados para la proteína principal.
    """
    # URL de la API de STRING
    url = f"https://string-db.org/api/json/network?identifiers={proteina_id}&species=9606"

    try:
        # Hacer la solicitud a la API
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        
        # Procesar la respuesta JSON
        data = response.json()

        print(data)

        # Lista para almacenar las interacciones
        interacciones = []

        # Recolectar todos los identificadores para la conversión
        ids_para_convertir = set()
        for item in data:
            ids_para_convertir.add(item['stringId_A'])
            ids_para_convertir.add(item['stringId_B'])
        

        # Si el formato es UniProt, convertimos los IDs a UniProt
        if formato_salida == "uniprot":
            print(f"Convirtiendo a UniProt...")
            mapeo_ids = convertir_a_uniprot(list(ids_para_convertir))
            # Crear la lista de interacciones con UniProt IDs
            for item in data:
                proteina_1 = mapeo_ids.get(item['stringId_A'], item['stringId_A'])
                proteina_2 = mapeo_ids.get(item['stringId_B'], item['stringId_B'])

                # Guardar la interacción con los scores
                interacciones.append({
                    "proteina_1": proteina_1,
                    "proteina_2": proteina_2,
                    "scores": {
                        "combined_score": item.get("score", 0),
                        "tscore": item.get("transferred_score", 0),
                        "dscore": item.get("database_score", 0),
                        "escore": item.get("experiments_score", 0),
                        "pscore": item.get("prediction_score", 0),
                        "nscore": item.get("neighborhood_score", 0),
                    },
                })

        elif formato_salida == "ensembl":
            # Si el formato es Ensembl, usamos los Ensembl IDs directamente
            print(f"Usando Ensembl IDs...")
            for item in data:
                proteina_1 = item['stringId_A']  # Usamos los IDs de Ensembl tal cual
                proteina_2 = item['stringId_B']  # Usamos los IDs de Ensembl tal cual

                # Guardar la interacción con los scores
                interacciones.append({
                    "proteina_1": proteina_1,
                    "proteina_2": proteina_2,
                    "scores": {
                        "combined_score": item.get("score", 0),
                        "tscore": item.get("transferred_score", 0),
                        "dscore": item.get("database_score", 0),
                        "escore": item.get("experiments_score", 0),
                        "pscore": item.get("prediction_score", 0),
                        "nscore": item.get("neighborhood_score", 0),
                    },
                })

        elif formato_salida == "pdb":
            print(f"Convirtiendo a PDB...")
            mapeo_ids = convertir_a_pdb(list(ids_para_convertir))
            # Crear la lista de interacciones con PDB IDs
            for item in data:
                proteina_1 = mapeo_ids.get(item['stringId_A'], item['stringId_A'])
                proteina_2 = mapeo_ids.get(item['stringId_B'], item['stringId_B'])

            # Verificar si alguno de los nodos es None
                if proteina_1 is None or proteina_2 is None:
                    continue  # Saltar esta iteración si hay un nodo None

                # Guardar la interacción con los scores
                interacciones.append({
                    "proteina_1": proteina_1,
                    "proteina_2": proteina_2,
                    "pdb_id_original": proteina_id,
                    "scores": {
                        "combined_score": item.get("score", 0),
                        "tscore": item.get("transferred_score", 0),
                        "dscore": item.get("database_score", 0),
                        "escore": item.get("experiments_score", 0),
                        "pscore": item.get("prediction_score", 0),
                        "nscore": item.get("neighborhood_score", 0),
                    },
                })
            

        else:
            print(f"Formato {formato_salida} no soportado.")
            return None

        

        # Retornar las interacciones 
        return interacciones
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return {
            "interacciones": []
        }
    

def obtener_interacciones_desde_pdb(pdb_id, formato_salida="uniprot"):
    """
    Obtiene las interacciones de una proteína a partir de su ID PDB, conservando el ID original.
    """
    # Obtener el UniProt ID desde el PDB
    uniprot_id = obtener_uniprot_desde_pdb(pdb_id)
    if not uniprot_id:
        print(f"No se pudo obtener el UniProt ID para {pdb_id}.")
        return []

    # Obtener las interacciones desde STRING
    interacciones = obtener_interacciones(uniprot_id, formato_salida)
    
    # Añadir el PDB ID original a cada interacción
    for interaccion in interacciones:
        interaccion["pdb_id_original"] = pdb_id
    
    return interacciones

def obtener_uniprot_desde_pdb(pdb_id):
    """
    Obtiene el ID de UniProt de una proteína a partir de su código PDB.
    """
    url = f"https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/{pdb_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if pdb_id.upper() in data:
            for molecule in data[pdb_id.upper()]:
                for cross_ref in molecule.get("cross_references", []):
                    if cross_ref["database"] == "UniProt":
                        return cross_ref["id"]
        print(f"No se encontró un ID de UniProt para el PDB {pdb_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el UniProt desde PDB {pdb_id}: {e}")
        return None