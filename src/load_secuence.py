import requests
from Bio import SeqIO
from io import StringIO

def load_sequence_from_pdb(pdb_id):
    """
    Carga la secuencia de proteína desde un archivo PDB usando el identificador PDB.
    """
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error al descargar el archivo PDB con ID {pdb_id}")
        return None
    
    pdb_data = response.text
    # Ahora, extraemos la secuencia de aminoácidos del PDB
    sequence = []
    
    for line in pdb_data.splitlines():
        if line.startswith("SEQRES"):
            sequence.append("".join(line[19:].split()))
    
    # Unir todas las cadenas de la secuencia
    sequence = "".join(sequence)
    
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
    record = SeqIO.read(StringIO(fasta_data), "fasta")
    
    return str(record.seq)


if __name__ == "__main__":
    pdb_id = "1A2B"  # Sustituir con un ID de PDB válido
    uniprot_id = "P69905"  # Sustituir con un ID de UniProt válido

    # Prueba de carga de secuencia desde PDB
    pdb_sequence = load_sequence_from_pdb(pdb_id)
    if pdb_sequence:
        print(f"Secuencia de proteína del PDB {pdb_id}: {pdb_sequence[:50]}...")  # Mostrar los primeros 50 aminoácidos

    # Prueba de carga de secuencia desde UniProt
    uniprot_sequence = load_sequence_from_uniprot(uniprot_id)
    if uniprot_sequence:
        print(f"Secuencia de proteína de UniProt {uniprot_id}: {uniprot_sequence[:50]}...")  # Mostrar los primeros 50 aminoácidos

