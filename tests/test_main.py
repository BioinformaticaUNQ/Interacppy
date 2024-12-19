import unittest
from unittest.mock import patch, MagicMock
import argparse
import sys

class TestProteinaSecuencias(unittest.TestCase):

    @patch("builtins.print") 
    def test_main_script_pdb(self, mock_print):
        test_args = ["main.py", "--pdb", "1A2B", "--salida", "uniprot"]
        sys.argv = test_args 
        import main as a 
        a.main() 

    @patch("builtins.print") 
    def test_main_script_uniprot(self, mock_print):
        test_args = ["main.py", "--uniprot", "1A2B", "--salida", "pdb"]
        sys.argv = test_args 
        import main as a 
        a.main() 

    @patch("builtins.print") 
    def test_main_script_archivo(self, mock_print):
        test_args = ["main.py", "--archivo", "1a2b.pdb", "--salida", "uniprot"]
        sys.argv = test_args 
        import main as a 
        a.main() 

if __name__ == "__main__":
    unittest.main()
