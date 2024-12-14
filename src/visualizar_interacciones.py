import networkx as nx
import matplotlib.pyplot as plt
import json

def visualizar_interacciones(interacciones_data, formato="grafo"):
    """
    Visualiza las interacciones de la proteína en diferentes formatos usando UniProt IDs.

    :param interacciones_data: Diccionario con las interacciones y la proteína principal.
    :param formato: "grafo" para graficar, "json" para exportar a formato JSON.
    """
    interacciones = interacciones_data

    if not interacciones:
        print("No se encontraron interacciones.")
        return

    if formato == "grafo":
        # Crear un grafo de las interacciones usando NetworkX
        G = nx.Graph()
        
        # Configuración de colores y pesos para las aristas
        edge_colors = []
        edge_widths = []
        node_colors = []

        # Añadir nodos y aristas con sus pesos y colores
        for interaccion in interacciones:
            proteina_1 = interaccion["proteina_1"]
            proteina_2 = interaccion["proteina_2"]
            combined_score = interaccion["scores"]["combined_score"]

            # Añadir al grafo con el peso del score
            G.add_edge(proteina_1, proteina_2, weight=combined_score)

            # Definir colores según el score combinado
            if combined_score >= 0.8:
                edge_colors.append("red")  # Muy alta proximidad
            elif 0.6 <= combined_score < 0.8:
                edge_colors.append("orange")  # Alta proximidad
            elif 0.4 <= combined_score < 0.6:
                edge_colors.append("yellow")  # Proximidad media
            else:
                edge_colors.append("gray")  # Baja proximidad

            # Definir el grosor de la línea proporcional al score
            edge_widths.append(combined_score*2)

        # Asignar colores a los nodos
        for node in G.nodes():
            node_colors.append("lightgray")

        # Dibujar el grafo usando matplotlib
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, seed=42)  # Diseño para los nodos (estable reproducibilidad)

        # Dibujar nodos y etiquetas
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, alpha=0.9)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="Arial", font_color="black")

        # Dibujar aristas con colores y grosores
        nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.8)

        # Título y leyenda personalizada
        plt.title("Interacciones de Proteína (UniProt IDs)", fontsize=14)

        # Crear la leyenda manualmente
        legend_labels = {
            "red": "Muy alta proximidad (>= 0.8)",
            "orange": "Alta proximidad (0.6-0.8)",
            "yellow": "Proximidad media (0.4-0.6)",
            "gray": "Baja proximidad (< 0.4)",
        }
        for color, label in legend_labels.items():
            plt.plot([], [], color=color, marker='o', linestyle='None', markersize=10, label=label)
        plt.legend(loc="best", fontsize=10)

        # Mostrar el grafo
        plt.show()

    elif formato == "json":
        # Exportar las interacciones en formato JSON
        interacciones_json = json.dumps(interacciones, indent=4)
        print("Interacciones en formato JSON:")
        print(interacciones_json)

    else:
        print(f"Formato {formato} no soportado. Use 'grafo' o 'json'.")
