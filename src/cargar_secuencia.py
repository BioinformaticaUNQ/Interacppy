import requests
from io import StringIO
from Bio import SeqIO


def load_sequence_from_pdb(pdb_id):
    """
    Carga la secuencia de proteína desde un archivo PDB usando el identificador PDB.
    """
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        print(f"Error al descargar el archivo PDB con ID {pdb_id}")
        return None
    file = response.content.decode('utf-8')

    # Ahora, extraemos la secuencia de aminoácidos del PDB
    sequence = []
    
    for line in file.splitlines():
        if line.startswith("SEQRES"):
            sequence.append("".join(line[19:].split()))
    
    # Unir todas las cadenas de la secuencia
    sequence = "".join(sequence)
    if not sequence:
        print(f"No se pudo extraer la secuencia del PDB con ID {pdb_id}")
        return None
    return sequence

def load_sequence_from_uniprot(uniprot_id):
    """
    Carga la secuencia de proteína desde UniProt usando el ID de UniProt.
    """
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error al descargar el archivo de UniProt con ID {uniprot_id}")
        return None

    # Usamos BioPython para leer la secuencia en formato FASTA
    fasta_data = response.text
    try:
        # SeqIO.read para leer una sola entrada FASTA
        record = SeqIO.read(StringIO(fasta_data), "fasta")
        
        return str(record.seq)
    except Exception as e:
        print(f"Error al leer el archivo FASTA de UniProt: {e}")
        return None

def load_sequence_from_file(file_path):
    """
    Carga la secuencia de la proteína y el ID de PDB desde un archivo PDB.
    
    :param file_path: Ruta del archivo PDB local.
    :return: Tuple (secuencia, pdb_id) o (None, None) si no se encuentra la información.
    """
    secuencia = []
    pdb_id = None  # Cambié 'uniprot_id' por 'pdb_id' para extraer el ID de PDB
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Extraer la secuencia de la proteína
        for line in lines:
            if line.startswith("SEQRES"):  # Las líneas que contienen la secuencia de la proteína
                secuencia.append("".join(line[19:].split()))  # Concatenar las cadenas de aminoácidos
        
        secuencia = "".join(secuencia)  # Unir todas las cadenas de la secuencia
        
        # Buscar el ID de PDB en las líneas DBREF
        for line in lines:
            if line.startswith("DBREF"):
                # La estructura de la línea DBREF es: DBREF <pdb_id> <cadena> <inicio> <fin> <base> <id_uniprot> <nombre_uniprot> ...
                parts = line.split()  # Separar la línea en partes
                if len(parts) > 1:  # Asegurarse de que haya al menos 2 partes
                    pdb_id = parts[1]  # El ID de PDB está en la segunda columna (índice 1)
                    break  # Salir del bucle una vez encontrado
        
        if not secuencia:
            print("No se pudo encontrar la secuencia de la proteína en el archivo PDB.")
            return None, None
        
        if not pdb_id:
            print("No se encontró un ID de PDB en el archivo PDB.")
            return secuencia, None
        
        return secuencia, pdb_id
    
    except Exception as e:
        print(f"Error al procesar el archivo PDB: {e}")
        return None, None