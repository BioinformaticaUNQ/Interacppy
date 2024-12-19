import networkx as nx
import matplotlib.pyplot as plt
import json
import os

def visualizar_interacciones(interacciones_data, proteina_principal, formato="grafo", salida="U", ruta_archivo=None):
    """
    Visualiza las interacciones de la proteína en diferentes formatos.

    :param interacciones_data: Lista con las interacciones.
    :param proteina_principal: Nombre o identificador de la proteína principal.
    :param formato: "grafo" para graficar, "json" para exportar a formato JSON.
    :param salida: Carácter para indicar el formato de salida: "U" (UniProt), "E" (Ensembl), "P" (PDB), etc.
    :param ruta_archivo: Nombre del archivo para guardar la imagen del grafo (sin extensión).
    """
    salida = salida or "U"

    if not interacciones_data:
        print("No se encontraron interacciones.")
        return

    formatos = {"U": "UniProt ID", "E": "Ensembl ID", "P": "PDB ID"}
    tipo_salida = formatos.get(salida.upper(), "Otro formato")

    if formato == "grafo":
        G = nx.Graph()

        edge_colors = []
        edge_widths = []
        node_color = "lightgray"

        for interaccion in interacciones_data:
            proteina_1 = interaccion["proteina_1"]
            proteina_2 = interaccion["proteina_2"]
            combined_score = interaccion["scores"]["combined_score"]

            G.add_edge(proteina_1, proteina_2, weight=combined_score)

            if combined_score >= 0.8:
                edge_colors.append("red")
            elif 0.6 <= combined_score < 0.8:
                edge_colors.append("orange")
            elif 0.4 <= combined_score < 0.6:
                edge_colors.append("yellow")
            else:
                edge_colors.append("gray")

            edge_widths.append(combined_score * 2)

        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, seed=42)

        nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_color, alpha=0.9)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="Arial", font_color="black")
        nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.8)

        plt.title(f"Interacciones de la proteína principal: {proteina_principal} ({tipo_salida})", fontsize=14)
        plt.gcf().canvas.manager.set_window_title(f"Grafo de {proteina_principal} ({tipo_salida})")

        legend_labels = {
            "red": "Very high score (>= 0.8)",
            "orange": "High score (0.6-0.8)",
            "yellow": "Medium score (0.4-0.6)",
            "gray": "Low score (< 0.4)",
        }
        for color, label in legend_labels.items():
            plt.plot([], [], color=color, marker='o', linestyle='None', markersize=10, label=label)
        plt.legend(loc="best", fontsize=10)

        if ruta_archivo:
            # Asegurar que la carpeta "resultados" exista
            if not os.path.exists('resultados'):
                os.makedirs('resultados')

            # Añadir extensión .png si no está presente
            if not ruta_archivo.lower().endswith('.png'):
                ruta_archivo = f"{ruta_archivo}.png"

            # Crear la ruta completa
            ruta_completa = os.path.join('resultados', os.path.basename(ruta_archivo))

            try:
                plt.savefig(ruta_completa, format='png', dpi=300)
                print(f"Grafo guardado correctamente en: {ruta_completa}")
            except Exception as e:
                print(f"Error al guardar el grafo: {e}")

        plt.show()

    elif formato == "json":
        interacciones_json = json.dumps(interacciones_data, indent=4)
        print("Interacciones en formato JSON:")
        print(interacciones_json)
    else:
        print(f"Formato {formato} no soportado. Use 'grafo' o 'json'.")
