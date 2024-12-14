import argparse
import load_sequence
import obtener_interacciones
import visualizar_interacciones

def main():
    # Configuración de argparse para manejar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Análisis de proteínas: carga de secuencias, mutación y análisis de interacciones.")
    
    # Argumentos de entrada
    parser.add_argument("--pdb", type=str, help="ID de PDB para cargar la secuencia de proteína (ej. 1A2B).")
    parser.add_argument("--archivo", type=str, help="Ruta a un archivo .pdb local para cargar la secuencia de proteína.")
    parser.add_argument("--uniprot", type=str, help="ID de UniProt para cargar la secuencia de proteína.")
    parser.add_argument("--visualizar", action="store_true", help="Visualizar las interacciones de la proteína.")
    
    # Argumento para la salida
    parser.add_argument("--salida", type=str, choices=["uniprot", "ensembl", "pdb", "ncbi"], help="Formato de salida: uniprot, ensembl, pdb, ncbi.")
    
    # Parsear los argumentos
    args = parser.parse_args()
    secuencia = None
    id_iter = None
    
    # Cargar la secuencia de la proteína desde PDB ID o archivo PDB o UniProt
    if args.pdb:
        secuencia = load_sequence.load_sequence_from_pdb(args.pdb)
        if secuencia:
            print(f"Secuencia cargada desde PDB {args.pdb}: {secuencia[:50]}...")
            id_iter = args.pdb
    elif args.archivo:
        secuencia, uniprot_id_archivo = load_sequence.load_sequence_from_file(args.archivo)  # Nueva función para cargar desde archivo
        if secuencia:
            print(f"Secuencia cargada desde archivo PDB {args.archivo}: {secuencia[:50]}...")
            id_iter = uniprot_id_archivo
    elif args.uniprot:
        secuencia = load_sequence.load_sequence_from_uniprot(args.uniprot)
        if secuencia:
            print(f"Secuencia cargada desde UniProt {args.uniprot}: {secuencia[:50]}...")
            id_iter = args.uniprot
    else:
        print("Debe proporcionar un ID de PDB, un archivo PDB o un ID de UniProt.")
        return
    
    # Obtener las interacciones de la proteína si es posible
    if id_iter:
        print(f"ID utilizado para interacciones: {id_iter}")
        interacciones = obtener_interacciones.obtener_interacciones(id_iter, args.salida)
        if interacciones:
            print(f"Interacciones obtenidas: {interacciones}")
        
        if args.visualizar:
            visualizar_interacciones.visualizar_interacciones(interacciones)

if __name__ == "__main__":
    main()
