import matplotlib.pyplot as plt
import networkx as nx

def visualizar_interacciones(interacciones):
    """
    Visualiza las interacciones proteicas usando NetworkX y Matplotlib.

    Args:
    interacciones (list of tuple): Lista de tuplas donde cada tupla representa una interacción entre dos proteínas.
    """
    # Crear un grafo vacío
    G = nx.Graph()

    # Añadir interacciones como bordes al grafo
    for proteina_1, proteina_2 in interacciones:
        G.add_edge(proteina_1, proteina_2)

    # Dibujar el grafo
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)  # Distribución de los nodos
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=12)
    plt.title("Interacciones Proteicas")
    plt.show()

# Lista de interacciones (ejemplo)
interacciones = [
    ("Proteína A", "Proteína B"),
    ("Proteína A", "Proteína C"),
    ("Proteína B", "Proteína D"),
    ("Proteína C", "Proteína D"),
    ("Proteína D", "Proteína E"),
]

# Llamamos a la función para visualizar las interacciones
visualizar_interacciones(interacciones)
