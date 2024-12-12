import argparse
import load_sequence
import obtener_interacciones
import visualizar_interacciones

def main():
    # Configuración de argparse para manejar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Análisis de proteínas: carga de secuencias, mutación y análisis de interacciones.")
    parser.add_argument("--pdb", type=str, help="ID de PDB para cargar la secuencia de proteína.")
    parser.add_argument("--uniprot", type=str, help="ID de UniProt para cargar la secuencia de proteína.")
    parser.add_argument("--visualizar", action="store_true", help="Visualizar las interacciones de la proteína.")
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    # Cargar la secuencia de la proteína usando PDB o UniProt
    if args.pdb:
        secuencia = load_sequence.load_sequence_from_pdb(args.pdb)
        if secuencia:
            print(f"Secuencia cargada desde PDB {args.pdb}: {secuencia[:50]}...")
    elif args.uniprot:
        secuencia = load_sequence.load_sequence_from_uniprot(args.uniprot)
        if secuencia:
            print(f"Secuencia cargada desde UniProt {args.uniprot}: {secuencia[:50]}...")
    else:
        print("Debe proporcionar un ID de PDB o UniProt.")
        return
    
    # Obtener y visualizar las interacciones si se requiere
    if args.pdb or args.uniprot:
        interacciones = obtener_interacciones.obtener_interacciones(uniprot_id=args.uniprot, pdb_id=args.pdb)
        if interacciones:
            print(f"Interacciones obtenidas: {interacciones}")
        
        if args.visualizar:
            visualizar_interacciones.visualizar_interacciones(interacciones)

if __name__ == "__main__":
    main()


