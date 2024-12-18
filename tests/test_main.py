import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import argparse

from cargar_secuencia import load_sequence_from_pdb, load_sequence_from_uniprot

import main

class TestMainMethods(unittest.TestCase):

    # Simulamos requests.get para probar la carga de secuencias desde PDB y UniProt
    @patch('requests.get')
    def test_load_sequence_from_pdb_success(self, mock_get):
        pdb_data = """>SEQRES   1 A  20  MET ALA VAL GLY SER GLU TYR LEU CYS GLN
                        PRO LYS GLU ASP ILE GLY ASN CYS ASP GLU ASN PHE THR"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = pdb_data

        # Simulamos la llamada a la función con un ID de PDB
        pdb_id = "1A2B"
        sequence = None
        sequence = load_sequence_from_pdb(pdb_id)

        self.assertIsNotNone(sequence)
        self.assertEqual(sequence, "METALAVGLYSEGLTYRCYSGQNPROLYSDILEASNCDASNFM")

    @patch('requests.get')
    def test_load_sequence_from_uniprot_success(self, mock_get):
        fasta_data = """>sp|P69905|HBB_HUMAN Hemoglobin subunit beta OS=Homo sapiens OX=9606 GN=HBB
                        MDSQFEGHLVLSPADKKYFGGFLPSRQALETRFLTIYEDLLRRLEKGGYAKFGRN"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = fasta_data

        # Simulamos la llamada a la función con un ID de UniProt
        uniprot_id = "P69905"
        sequence = load_sequence_from_uniprot(uniprot_id)

        self.assertIsNotNone(sequence)
        self.assertEqual(sequence, "MDSQFEGHLVLSPADKKYFGGFLPSRQALETRFLTIYEDLLRRLEKGGYAKFGRN")

    # Test para la función del main que verifica la interacción y guarda en JSON
    @patch('obtener_interacciones.obtener_interacciones')
    @patch('guardar_interacciones.guardar_interacciones_json')
    @patch('visualizar_interacciones.visualizar_interacciones')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_interactions(self, mock_parse_args, mock_visualizar, mock_guardar, mock_obtener):
        # Definir los valores de entrada simulados para los argumentos de línea de comandos
        mock_parse_args.return_value = argparse.Namespace(
            pdb="1A2B",
            salida="uniprot",
            guardar="resultados/interacciones.json",
            visualizar=True
        )

        # Simular las interacciones obtenidas por la función
        mock_obtener.return_value = ["INTERACCION1", "INTERACCION2"]

        # Llamar a la función main
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            main.main()

        # Comprobar que las interacciones fueron obtenidas correctamente
        mock_obtener.assert_called_with("1A2B", "U")
        mock_guardar.assert_called_once_with(mock_obtener.return_value, "resultados/interacciones.json")
        mock_visualizar.assert_called_once()

    # Test para cuando no se pasan secuencias ni interacciones
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_no_sequence(self, mock_parse_args):
        # Definir los valores de entrada simulados para los argumentos de línea de comandos
        mock_parse_args.return_value = argparse.Namespace(
            pdb=None,
            archivo=None,
            uniprot=None,
            salida="uniprot",
            guardar=None,
            visualizar=False
        )

        # Llamar a la función main
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            main.main()

        # Verificar que el programa imprime el mensaje adecuado para la falta de secuencia
        mock_stdout.write.assert_any_call("Debe proporcionar un ID de PDB, un archivo PDB o un ID de UniProt.\n")

    # Test para validar que se maneja el error al no poder cargar la secuencia
    @patch('cargar_secuencia.load_sequence_from_pdb')
    def test_main_with_pdb_loading_error(self, mock_load):
        # Simulamos que la función de carga de PDB falla
        mock_load.return_value = None

        # Configuramos el argumento
        args = argparse.Namespace(
            pdb="INVALID_PDB",
            salida="uniprot",
            guardar=None,
            visualizar=False
        )

        # Llamar a la función main
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            main.main()

        # Verificar que el error al cargar la secuencia es manejado
        mock_stdout.write.assert_any_call("Error: No se pudo cargar la secuencia de proteína.\n")

    # Test para validar la validación de formatos incorrectos para UniProt
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_invalid_uniprot_format(self, mock_parse_args):
        # Definir los valores de entrada simulados para los argumentos de línea de comandos
        mock_parse_args.return_value = argparse.Namespace(
            pdb=None,
            archivo=None,
            uniprot="INVALID_UNIPROT",
            salida="uniprot",
            guardar=None,
            visualizar=False
        )

        # Llamar a la función main
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            main.main()

        # Verificar que el error es manejado para un formato inválido de UniProt
        mock_stdout.write.assert_any_call("Error: El ID de UniProt no tiene un formato válido.\n")

if __name__ == '__main__':
    unittest.main()