import argparse

def main():
    # Crear el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Herramienta de mapeo de interacciones proteicas."
    )

    # Agregar argumentos
    parser.add_argument(
        "-pdb", "--pdb_id",
        type=str,
        help="Código PDB de la proteína objetivo (por ejemplo, 1XYZ)."
    )

    parser.add_argument(
        "-u", "--uniprot_id",
        type=str,
        help="ID de UniProt de la proteína objetivo."
    )

    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Archivo de texto con IDs (uno por línea)."
    )

    # Parsear los argumentos
    args = parser.parse_args()

    # Mostrar qué input se recibió
    if args.pdb_id:
        print(f"Se recibió un código PDB: {args.pdb_id}")
    elif args.uniprot_id:
        print(f"Se recibió un ID de UniProt: {args.uniprot_id}")
    elif args.file:
        print(f"Se procesará el archivo: {args.file}")
    else:
        print("No se proporcionó ningún argumento. Usa --help para más información.")

if __name__ == "__main__":
    main()
