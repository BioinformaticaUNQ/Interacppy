import argparse
import os
import re
import src.cargar_secuencia as cargar_secuencia
import src.obtener_interacciones as obtener_interacciones
import src.visualizar_interacciones as visualizar_interacciones
import src.guardar_interacciones as guardar_interacciones

def main():
    # Configuración de argparse para manejar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Análisis de proteínas: carga de secuencias, mutación y análisis de interacciones.")
    
    # Argumentos de entrada
    parser.add_argument("--pdb", type=str, help="ID de PDB para cargar la secuencia de proteína (ej. 1A2B).")
    parser.add_argument("--archivo", type=str, help="Ruta a un archivo .pdb local para cargar la secuencia de proteína.")
    parser.add_argument("--uniprot", type=str, help="ID de UniProt para cargar la secuencia de proteína.")
    parser.add_argument("--visualizar", action="store_true", help="Visualizar las interacciones de la proteína.")

    # Argumento para la salida, ahora acepta hasta 3 formatos
    parser.add_argument("--salida", type=str, choices=["uniprot", "ensembl", "pdb"], help="Formatos de salida: uniprot, ensembl, pdb.", nargs='+')
    parser.add_argument("--guardar", type=str, help="Ruta base del archivo para guardar las interacciones.")
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    secuencia = None
    id_iter = None
    especie = None  # Nueva variable para almacenar la especie detectada

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
        secuencia, especie = cargar_secuencia.load_sequence_from_pdb(args.pdb)
        if secuencia:
            print(f"Secuencia cargada desde PDB {args.pdb}: {secuencia[:50]}...")
            id_iter = args.pdb
    elif args.archivo:
        secuencia, _, especie = cargar_secuencia.load_sequence_from_file(args.archivo)  # Ajuste para incluir especie
        if secuencia:
            print(f"Secuencia cargada desde archivo PDB {args.archivo}: {secuencia[:50]}...")
            id_iter = args.archivo
    elif args.uniprot:
        secuencia = cargar_secuencia.load_sequence_from_uniprot(args.uniprot)
        if secuencia:
            print(f"Secuencia cargada desde UniProt {args.uniprot}: {secuencia[:50]}...")
            id_iter = args.uniprot
    else:
        print("Debe proporcionar un ID de PDB, un archivo PDB o un ID de UniProt.")
        return
    
    # Mostrar especie si se detectó
    if especie:
        print(f"Especie detectada: {especie}")
    
    # Verificar que la secuencia se haya cargado correctamente
    if not secuencia:
        print("Error: No se pudo cargar la secuencia de proteína.")
        return
    
    # Obtener las interacciones de la proteína si es posible
    if id_iter:
        print(f"ID utilizado para interacciones: {id_iter}")
        
        # Se requiere obtener las interacciones para cada formato de salida
        for salida in args.salida:
            print(f"Procesando interacciones para formato: {salida}")
            interacciones = obtener_interacciones.obtener_interacciones(id_iter, salida)

            if interacciones:
                print(f"Interacciones obtenidas para {salida}: {interacciones}")
                
                # Guardar las interacciones en un archivo JSON y generar gráfico
                if args.guardar:
                    guardar_interacciones.guardar_interacciones_json(interacciones, f"{args.guardar}_{salida}.json")
                
                # Si se solicita, visualizar las interacciones para cada formato
                if args.visualizar:
                    visualizar_interacciones.visualizar_interacciones(interacciones, id_iter, salida=salida, ruta_archivo=f"{args.guardar}_{salida}")
            else:
                print(f"No se pudieron obtener interacciones para {salida}.")
        
if __name__ == "__main__":
    main()
