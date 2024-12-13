import networkx as nx
import matplotlib.pyplot as plt
import json

def visualizar_interacciones(interacciones, formato="grafo"):
    """
    Visualiza las interacciones de la proteína en diferentes formatos usando UniProt IDs.

    :param interacciones: Lista de tuplas o diccionarios con las interacciones de la proteína.
    :param formato: "grafo" para graficar, "json" para exportar a formato JSON.
    """
    if not interacciones:
        print("No se encontraron interacciones.")
        return

    # Convertir tuplas a diccionarios con un peso predeterminado
    interacciones_dict = []
    for interactivo in interacciones:
        if isinstance(interactivo, tuple):
            # Si es una tupla, convertirla a un diccionario con un peso predeterminado
            interacciones_dict.append({
                'interactor_a': interactivo[0],  # Asegúrate que sea un UniProt ID
                'interactor_b': interactivo[1],  # Asegúrate que sea un UniProt ID
                'peso': 1.0  # Peso predeterminado
            })
        elif isinstance(interactivo, dict):
            # Si ya es un diccionario, usarlo tal cual
            interacciones_dict.append(interactivo)
        else:
            print(f"Interacción en formato desconocido: {interactivo}")
            continue

    if formato == "grafo":
        # Crear un grafo de las interacciones usando NetworkX
        G = nx.Graph()
        
        for interactivo in interacciones_dict:
            G.add_edge(interactivo['interactor_a'], interactivo['interactor_b'], weight=interactivo['peso'])
        
        # Dibujar el grafo usando matplotlib
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)  # Diseño para los nodos
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue', alpha=0.6)
        nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.7)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family="Arial")
        plt.title("Interacciones de Proteína (UniProt IDs)")
        plt.show()

    elif formato == "json":
        # Exportar las interacciones en formato JSON
        interacciones_json = json.dumps(interacciones_dict, indent=4)
        print("Interacciones en formato JSON:")
        print(interacciones_json)

    else:
        print(f"Formato {formato} no soportado. Use 'grafo' o 'json'.")
