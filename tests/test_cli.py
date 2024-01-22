#!python -m unittest tests.test_utils
"""This module provides unit tests for alphamap.cli."""

# builtin
import unittest

import os
import pandas as pd

# local
from alphamap.importing import read_file, \
    extract_rawfile_unique_values

THIS_FOLDER = os.path.dirname(__file__)
TEST_FOLDER = os.path.join(
    f"{os.path.dirname(THIS_FOLDER)}",
    "nbs",
    "testdata",
)

class TestAll(unittest.TestCase):

    def test_read_file(self,):
        file_with_missing_col = os.path.join(TEST_FOLDER,'test_not_all_columns_spectronaut.csv')
        spectronaut_columns = ["PEP.AllOccurringProteinAccessions","EG.ModifiedSequence","R.FileName"]
        
        try:
            out = read_file(file_with_missing_col, spectronaut_columns)
        except ValueError as e:
            out = e
        assert str(out) == "The list of specified column names cannot be extracted from the file." 
    
    def test_extract_rawfile_unique_values(self, ):
        data_Spectronaut_csv = os.path.join(TEST_FOLDER, 'test_spectronaut_input.csv')
        data_Spectronaut_tsv = os.path.join(TEST_FOLDER, 'test_spectronaut_input.tsv')
        assert ['raw_01', 'raw_02'] == extract_rawfile_unique_values(data_Spectronaut_csv)
        assert extract_rawfile_unique_values(data_Spectronaut_csv) == extract_rawfile_unique_values(data_Spectronaut_tsv)
        
        data_MQ = os.path.join(TEST_FOLDER, 'test_maxquant_input.txt')
        assert len(extract_rawfile_unique_values(data_MQ)) == 381
        
        data_wrong = os.path.join(TEST_FOLDER, 'test_maxquant_imported.csv')
        try:
            out = extract_rawfile_unique_values(data_wrong)
        except ValueError as e:
            out = e
        assert str(out) == "A column with the raw file names is not in the file." 
        
        data_fragpipe_combined = os.path.join(TEST_FOLDER, 'combined_peptide.txt')
        assert ['Y731F1', 'Y731F2', 'wt1', 'wt2'] == extract_rawfile_unique_values(data_fragpipe_combined)



if __name__ == "__main__":
    unittest.main()
