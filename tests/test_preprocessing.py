#!python -m unittest tests.test_utils
"""This module provides unit tests for alphamap.cli."""

# builtin
import unittest

import os
import pandas as pd
import numpy as np
from pyteomics import fasta
import warnings

# local
from alphamap.preprocessing import extract_uniprot_id, \
    expand_protein_ids, \
    pep_position_helper, \
    get_peptide_position, \
    get_ptm_sites, \
    get_modifications, \
    format_input_data

THIS_FOLDER = os.path.dirname(__file__)
TEST_FOLDER = os.path.join(
    f"{os.path.dirname(THIS_FOLDER)}",
    "nbs",
    "testdata",
)

test_df = pd.DataFrame(data={'all_protein_ids': ["A0A024R161;A0A087WT10;A0A087WTH1", 
                                                 "A0A024R161;A0A087WT10", 
                                                 "A0A087WTH5","A0A087WTH5",
                                                 "Nonsense"], 
                            'modified_sequence': ["PEPT[Phospho (STY)]IDER", 
                                                  "SEQ[GlyGly (K)]UENCE[GlyGly (K)]R", 
                                                  "VIEWER","NONSEQ",
                                                  "NONSENSE"],
                            'naked_sequence': ["PEPTIDER", 
                                               "SEQUENCER", 
                                               "VIEWER","NONSEQ",
                                               "NONSENSE"]})

test_df_expanded = pd.DataFrame(data={'unique_protein_id': ["A0A024R161", "A0A087WT10", "A0A087WTH1", 
                                                            "A0A024R161", "A0A087WT10", 
                                                            "A0A087WTH5","A0A087WTH5",
                                                            "Nonsense"], 
                                      'modified_sequence': ["PEPT[Phospho (STY)]IDER", "PEPT[Phospho (STY)]IDER", "PEPT[Phospho (STY)]IDER",
                                                            "SEQ[GlyGly (K)]UENCE[GlyGly (K)]R", "SEQ[GlyGly (K)]UENCE[GlyGly (K)]R", 
                                                            "VIEWER","NONSEQ",
                                                            "NONSENSE"],
                                      'naked_sequence': ["PEPTIDER", "PEPTIDER", "PEPTIDER", 
                                                         "SEQUENCER", "SEQUENCER", 
                                                         "VIEWER","NONSEQ",
                                                         "NONSENSE"],
                                      'all_protein_ids': ["A0A024R161;A0A087WT10;A0A087WTH1", "A0A024R161;A0A087WT10;A0A087WTH1", "A0A024R161;A0A087WT10;A0A087WTH1", 
                                                 "A0A024R161;A0A087WT10", "A0A024R161;A0A087WT10", 
                                                 "A0A087WTH5","A0A087WTH5",
                                                 "Nonsense"]})
     
test_df_expanded_peptide_position = pd.DataFrame(data={'unique_protein_id': ["A0A024R161", "A0A087WT10", "A0A087WTH1", 
                                                                             "A0A024R161", "A0A087WT10", 
                                                                             "A0A087WTH5"], 
                                                       'modified_sequence': ["PEPT[Phospho (STY)]IDER", "PEPT[Phospho (STY)]IDER", "PEPT[Phospho (STY)]IDER",
                                                                             "SEQ[GlyGly (K)]UENCE[GlyGly (K)]R", "SEQ[GlyGly (K)]UENCE[GlyGly (K)]R", 
                                                                             "VIEWER"],
                                                       'naked_sequence': ["PEPTIDER", "PEPTIDER", "PEPTIDER", 
                                                                          "SEQUENCER", "SEQUENCER", 
                                                                          "VIEWER"],
                                                       'all_protein_ids': ["A0A024R161;A0A087WT10;A0A087WTH1", "A0A024R161;A0A087WT10;A0A087WTH1", "A0A024R161;A0A087WT10;A0A087WTH1", 
                                                                             "A0A024R161;A0A087WT10", "A0A024R161;A0A087WT10", 
                                                                             "A0A087WTH5"],
                                                       'start':[3,28,107,95,150,1],
                                                       'end':[10,35,114,103,158,6]})

test_df_modifications = pd.DataFrame(data={'unique_protein_id': ["A0A024R161", "A0A087WT10", "A0A087WTH1", 
                                                                             "A0A024R161", "A0A087WT10", 
                                                                             "A0A087WTH5"], 
                                            'modified_sequence': ["PEPT[Phospho (STY)]IDER", "PEPT[Phospho (STY)]IDER", "PEPT[Phospho (STY)]IDER",
                                                                             "SEQ[GlyGly (K)]UENCE[GlyGly (K)]R", "SEQ[GlyGly (K)]UENCE[GlyGly (K)]R", 
                                                                             "VIEWER"],
                                            'naked_sequence': ["PEPTIDER", "PEPTIDER", "PEPTIDER", 
                                                                          "SEQUENCER", "SEQUENCER", 
                                                                          "VIEWER"],
                                           'all_protein_ids': ["A0A024R161;A0A087WT10;A0A087WTH1", "A0A024R161;A0A087WT10;A0A087WTH1", "A0A024R161;A0A087WT10;A0A087WTH1", 
                                                                             "A0A024R161;A0A087WT10", "A0A024R161;A0A087WT10", 
                                                                             "A0A087WTH5"],
                                                       'start':[3,28,107,95,150,1],
                                                       'end':[10,35,114,103,158,6], 
                                           'PTMsites':[[3],[3],[3],[2,7],[2,7],[]],
                                           'PTMtypes':[["[Phospho (STY)]"],["[Phospho (STY)]"],["[Phospho (STY)]"],["[GlyGly (K)]","[GlyGly (K)]"],["[GlyGly (K)]","[GlyGly (K)]"],[]]})

test_fasta = fasta.IndexedUniProt(os.path.join(TEST_FOLDER,'test.fasta'))

class TestPreprocessing(unittest.TestCase):
    def test_extract_uniprot_id(self, ):
        prot_id_1 = 'sp|P02769|ALBU_BOVIN'
        assert 'P02769' == extract_uniprot_id(prot_id_1)
        prot_id_2 = 'CON__P02769'
        assert 'P02769' == extract_uniprot_id(prot_id_2)

    def test_expand_protein_ids(self, ):
        res = expand_protein_ids(test_df)
        pd.testing.assert_frame_equal(res,test_df_expanded)

    def test_pep_position_helper(self, ):
        start, end = pep_position_helper("PEPTIDER","A0A024R161",test_fasta)
        np.testing.assert_equal([start, end], [3,10])

    def test_get_peptide_position(self, ):
        with warnings.catch_warnings(record=True) as w:
            res = get_peptide_position(test_df_expanded, test_fasta)
            assert len(w) == 2
            assert "Peptide sequence NONSEQ could not be mached" in str(w[0].message)
            assert "No matching entry for Nonsense" in str(w[1].message)
        pd.testing.assert_frame_equal(res,test_df_expanded_peptide_position)

    def test_get_ptm_sites(self, ):
        myPep = "PEPT[Phospho]IDE[GlyGly (K)]R"
        res = get_ptm_sites(myPep, modification_reg=r'\[.*?\]')
        np.testing.assert_equal(res, [3,6])
        myPep = "[Ac]PEPTIDE[GlyGly (K)]R"
        res = get_ptm_sites(myPep, modification_reg=r'\[.*?\]')
        np.testing.assert_equal(res, [0,6])

    def test_get_modifications(self, ):
        res = get_modifications(test_df_expanded_peptide_position, mod_reg = r'\[.*?\]')
        pd.testing.assert_frame_equal(res, test_df_modifications)

    def test_format_input_data(self, ):
        with warnings.catch_warnings(record=True) as w:
            res = format_input_data(df=test_df, fasta = test_fasta, modification_exp = r'\[.*?\]')
            assert len(w) == 2
            assert "Peptide sequence NONSEQ could not be mached" in str(w[0].message)
            assert "No matching entry for Nonsense" in str(w[1].message)   
        pd.testing.assert_frame_equal(res, test_df_modifications)

if __name__ == "__main__":
    unittest.main()
