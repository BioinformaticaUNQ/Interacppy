import networkx as nx
import matplotlib.pyplot as plt
import json

def visualizar_interacciones(interacciones, formato="grafo"):
    """
    Visualiza las interacciones de la proteína en diferentes formatos.

    :param interacciones: Diccionario con las interacciones de la proteína.
    :param formato: "grafo" para graficar, "json" para exportar a formato JSON.
    """
    if not interacciones:
        print("No se encontraron interacciones.")
        return
    
    if formato == "grafo":
        # Crear un grafo de las interacciones usando NetworkX
        G = nx.Graph()
        
        for interactivo in interacciones:
            # Suponemos que 'interacciones' es una lista de pares de interacciones
            G.add_edge(interactivo['interactor_a'], interactivo['interactor_b'], weight=interactivo['peso'])
        
        # Dibujar el grafo usando matplotlib
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)  # Diseño para los nodos
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue', alpha=0.6)
        nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.7)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family="Arial")
        plt.title("Interacciones de Proteína")
        plt.show()
    
    elif formato == "json":
        # Exportar las interacciones en formato JSON
        interacciones_json = json.dumps(interacciones, indent=4)
        print("Interacciones en formato JSON:")
        print(interacciones_json)
    
    else:
        print(f"Formato {formato} no soportado. Use 'grafo' o 'json'.")

def obtener_interacciones(uniprot_id=None, pdb_id=None):
    """
    Obtiene las interacciones de proteínas a partir de UniProt o PDB.
    Utiliza el ID de UniProt o el ID de PDB para obtener las interacciones.

    :param uniprot_id: El ID de UniProt de la proteína.
    :param pdb_id: El ID de PDB de la proteína.
    :return: Lista de interacciones en formato dict o None si no se pueden obtener.
    """
    interacciones = []
    
    # Aquí puedes implementar un llamado a la API de STRING o alguna otra fuente para obtener las interacciones
    # Este es un ejemplo de cómo podrían ser las interacciones obtenidas
    if uniprot_id:
        # Realizamos un mock-up de las interacciones (esto debe ser sustituido por la llamada real)
        interacciones = [
            {'interactor_a': uniprot_id, 'interactor_b': 'P12345', 'peso': 0.8},
            {'interactor_a': uniprot_id, 'interactor_b': 'Q67890', 'peso': 0.6},
            {'interactor_a': 'P12345', 'interactor_b': 'Q67890', 'peso': 0.7},
        ]
    elif pdb_id:
        # Realizamos un mock-up para PDB (esto debe ser sustituido por la llamada real)
        interacciones = [
            {'interactor_a': pdb_id, 'interactor_b': 'P12345', 'peso': 0.85},
            {'interactor_a': pdb_id, 'interactor_b': 'Q67890', 'peso': 0.65},
        ]
    
    return interacciones
