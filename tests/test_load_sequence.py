import unittest
import requests
from unittest.mock import patch
from io import StringIO
from src.load_sequence import load_sequence_from_pdb, load_sequence_from_uniprot



class TestLoadSequenceMethods(unittest.TestCase):

    @patch('requests.get')
    def test_load_sequence_from_pdb_success(self, mock_get):
        # Simula la respuesta de requests.get para un PDB válido
        pdb_data = """>SEQRES   1 A  20  MET ALA VAL GLY SER GLU TYR LEU CYS GLN
                    PRO LYS GLU ASP ILE GLY ASN CYS ASP GLU ASN PHE THR"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = pdb_data

        # Llamar a la función con un ID de PDB
        pdb_id = "1A2B"
        sequence = load_sequence_from_pdb(pdb_id)

        self.assertIsNotNone(sequence)
        self.assertEqual(sequence, "METALAVGLYSEGLTYRCYSGQNPROLYSDILEASNCDASNFM")

    @patch('requests.get')
    def test_load_sequence_from_pdb_error(self, mock_get):
        # Simula un error de solicitud para un PDB no válido
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Error: PDB no encontrado."

        pdb_id = "INVALID_PDB"
        sequence = load_sequence_from_pdb(pdb_id)

        self.assertIsNone(sequence)

    @patch('requests.get')
    def test_load_sequence_from_uniprot_success(self, mock_get):
        # Simula la respuesta de requests.get para un ID de UniProt válido
        fasta_data = """>sp|P69905|HBB_HUMAN Hemoglobin subunit beta OS=Homo sapiens OX=9606 GN=HBB
                        MDSQFEGHLVLSPADKKYFGGFLPSRQALETRFLTIYEDLLRRLEKGGYAKFGRN"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = fasta_data

        # Llamar a la función con un ID de UniProt
        uniprot_id = "P69905"
        sequence = load_sequence_from_uniprot(uniprot_id)

        self.assertIsNotNone(sequence)
        self.assertEqual(sequence, "MDSQFEGHLVLSPADKKYFGGFLPSRQALETRFLTIYEDLLRRLEKGGYAKFGRN")

    @patch('requests.get')
    def test_load_sequence_from_uniprot_error(self, mock_get):
        # Simula un error de solicitud para un ID de UniProt no válido
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Error: UniProt no encontrado."

        uniprot_id = "INVALID_ID"
        sequence = load_sequence_from_uniprot(uniprot_id)

        self.assertIsNone(sequence)


if __name__ == '__main__':
    unittest.main()
