import argparse
import os
import re
import cargar_secuencia
import obtener_interacciones
import visualizar_interacciones
import guardar_interacciones

def main():
    # Configuración de argparse para manejar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Análisis de proteínas: carga de secuencias, mutación y análisis de interacciones.")
    
    # Argumentos de entrada
    parser.add_argument("--pdb", type=str, help="ID de PDB para cargar la secuencia de proteína (ej. 1A2B).")
    parser.add_argument("--archivo", type=str, help="Ruta a un archivo .pdb local para cargar la secuencia de proteína.")
    parser.add_argument("--uniprot", type=str, help="ID de UniProt para cargar la secuencia de proteína.")
    parser.add_argument("--visualizar", action="store_true", help="Visualizar las interacciones de la proteína.")
    
    # Argumento para la salida
    parser.add_argument("--salida", type=str, choices=["uniprot", "ensembl", "pdb"], help="Formato de salida: uniprot, ensembl, pdb.")
    parser.add_argument("--guardar", type=str, help="Ruta del archivo JSON donde guardar las interacciones.")
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    secuencia = None
    id_iter = None

    # Determinar el formato de salida
    if args.salida:
        formato_salida_map = {"uniprot": "U", "ensembl": "E", "pdb": "P"}
        salida = formato_salida_map.get(args.salida.lower(), "U") if args.salida else "U"  # Por defecto "U, de Uniprot"
    
    # Validar que si se pasa un archivo, este tenga la extensión .pdb
    if args.archivo and not args.archivo.endswith(".pdb"):
        print("Error: El archivo debe tener la extensión .pdb.")
        return
    
    # Verificación del formato de ID de UniProt
    if args.uniprot and not re.match(r"^[A-Za-z0-9]{6,10}$", args.uniprot):
        print("Error: El ID de UniProt no tiene un formato válido.")
        return
    
    # Cargar la secuencia de la proteína desde PDB ID o archivo PDB o UniProt
    if args.pdb:
        secuencia = cargar_secuencia.load_sequence_from_pdb(args.pdb)
        if secuencia:
            print(f"Secuencia cargada desde PDB {args.pdb}: {secuencia[:50]}...")
            id_iter = args.pdb
    elif args.archivo:
        secuencia, uniprot_id_archivo = cargar_secuencia.load_sequence_from_file(args.archivo)  # Nueva función para cargar desde archivo
        if secuencia:
            print(f"Secuencia cargada desde archivo PDB {args.archivo}: {secuencia[:50]}...")
            id_iter = uniprot_id_archivo
    elif args.uniprot:
        secuencia = cargar_secuencia.load_sequence_from_uniprot(args.uniprot)
        if secuencia:
            print(f"Secuencia cargada desde UniProt {args.uniprot}: {secuencia[:50]}...")
            id_iter = args.uniprot
    else:
        print("Debe proporcionar un ID de PDB, un archivo PDB o un ID de UniProt.")
        return
    
    # Verificar que la secuencia se haya cargado correctamente
    if not secuencia:
        print("Error: No se pudo cargar la secuencia de proteína.")
        return
    
    # Obtener las interacciones de la proteína si es posible
    if id_iter:
        print(f"ID utilizado para interacciones: {id_iter}")
        if args.salida:
            interacciones = obtener_interacciones.obtener_interacciones(id_iter, args.salida)
        else:
            interacciones = obtener_interacciones.obtener_interacciones(id_iter)

        if interacciones:
            print(f"Interacciones obtenidas: {interacciones}")
            # Guardar las interacciones en un archivo JSON si se especifica
            if args.guardar:
                guardar_interacciones.guardar_interacciones_json(interacciones, args.guardar)
        if args.visualizar:
            # Verificar si se pueden visualizar las interacciones
            if not interacciones:
                print("Error: No hay interacciones para visualizar.")
                return
            # Enviar las interacciones, el identificador de la proteína principal y el formato de salida
            visualizar_interacciones.visualizar_interacciones(interacciones, id_iter, salida=salida)

if __name__ == "__main__":
    main()