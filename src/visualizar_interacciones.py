import networkx as nx
import matplotlib.pyplot as plt
import json

def visualizar_interacciones(interacciones_data, proteina_principal, formato="grafo", salida="U"):
    """
    Visualiza las interacciones de la proteína en diferentes formatos.

    :param interacciones_data: Lista con las interacciones.
    :param proteina_principal: Nombre o identificador de la proteína principal.
    :param formato: "grafo" para graficar, "json" para exportar a formato JSON.
    :param salida: Carácter para indicar el formato de salida: "U" (UniProt), "E" (Ensembl), "P" (PDB), etc.
    """
    interacciones = interacciones_data

    if not interacciones:
        print("No se encontraron interacciones.")
        return

    # Traducción del carácter `salida` a texto completo
    formatos = {"U": "UniProt ID", "E": "Ensembl ID", "P": "PDB ID"}
    tipo_salida = formatos.get(salida.upper(), "Otro formato")

    if formato == "grafo":
        # Crear un grafo de las interacciones usando NetworkX
        G = nx.Graph()
        
        # Configuración de colores y pesos para las aristas
        edge_colors = []
        edge_widths = []
        node_color = "lightgray"  # Color único para todos los nodos

        # Añadir nodos y aristas con sus pesos y colores
        for interaccion in interacciones:
            proteina_1 = interaccion["proteina_1"]
            proteina_2 = interaccion["proteina_2"]
            combined_score = interaccion["scores"]["combined_score"]

            # Añadir al grafo con el peso del score
            G.add_edge(proteina_1, proteina_2, weight=combined_score)

            # Definir colores según el score combinado
            if combined_score >= 0.8:
                edge_colors.append("red")
            elif 0.6 <= combined_score < 0.8:
                edge_colors.append("orange")
            elif 0.4 <= combined_score < 0.6:
                edge_colors.append("yellow")
            else:
                edge_colors.append("gray")

            # Definir el grosor de la línea proporcional al score
            edge_widths.append(combined_score * 2)

        # Dibujar el grafo usando matplotlib
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, seed=42)  # Diseño para los nodos (estable reproducibilidad)

        # Dibujar nodos y etiquetas
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_color, alpha=0.9)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="Arial", font_color="black")

        # Dibujar aristas con colores y grosores
        nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.8)

        # Títulos dinámicos
        plt.title(f"Interacciones de la proteína principal: {proteina_principal} ({tipo_salida})", fontsize=14)
        plt.gcf().canvas.manager.set_window_title(f"Grafo de {proteina_principal} ({tipo_salida})")

        # Crear la leyenda manualmente
        legend_labels = {
            "red": "Very high score (>= 0.8)",
            "orange": "High score (0.6-0.8)",
            "yellow": "Medium score (0.4-0.6)",
            "gray": "Low score (< 0.4)",
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
