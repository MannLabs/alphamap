#!python -m unittest tests.test_utils
"""This module provides unit tests for alphamap.cli."""

# builtin
import unittest
import os
import numpy as np

# local
from alphamap.uniprot_integration import extract_note, \
    extract_note_end, \
    resolve_unclear_position, \
    extract_positions, \
    preprocess_uniprot

THIS_FOLDER = os.path.dirname(__file__)
path_to_test_file = os.path.join(
    f"{os.path.dirname(THIS_FOLDER)}",
    "nbs",
    "testdata",
    "P11532_test_file.txt"
)

class TestUniprot(unittest.TestCase):
    def test_extract_note_not_splitted(self, ):
        string = 'FT                   /note="Missing (in isoform 2)"'
        output = extract_note(string)
        assert "Missing (in isoform 2)" == output[0]
        
    def test_extract_note_splitted(self, ):
        string = 'FT                   /note="MAAALFVLLGF -> MKQSD'
        output = extract_note(string, splitted=True)
        assert "MAAALFVLLGF -> MKQSD" == output[0]
        
    def test_extract_note_end_finished(self, ):
        string = 'FT                   ASPQER (in isoform 4)"'
        output = extract_note_end(string)
        assert "ASPQER (in isoform 4)" == output[0]
        
    def test_extract_note_end_not_finished(self, ):
        string = 'FT                   ASPQER (in isoform 4)'
        output = extract_note_end(string, has_mark=False)
        assert "ASPQER (in isoform 4)" == output[0]

    def test_extract_positions(self, ):
        string = '34..65'
        isoform, start, end = extract_positions(string)
        np.testing.assert_equal(['', 34, 65], [isoform, start, end])

    def test_extract_positions_with_isoform(self, ):
        string = 'P35613-2:195..199'
        isoform, start, end = extract_positions(string)
        np.testing.assert_equal(['P35613-2', 195, 199], [isoform, start, end])

    def test_extract_positions_start_with_isoform(self, ):
        string = 'Q9C0I9-2:256'
        isoform, start, end = extract_positions(string)
        np.testing.assert_equal(['Q9C0I9-2', 256, np.nan], [isoform, start, end])
        
    def test_extract_positions_start(self, ):
        string = '256'
        isoform, start, end = extract_positions(string)
        np.testing.assert_equal(['', 256, np.nan], [isoform, start, end])

    def test_resolve_unclear_position_unknown(self, ):
        string = '?'
        message = f"For unknown position resolve_unclear_position function returns wrong output instead of -1."
        assert -1 == resolve_unclear_position(string), message
        
    def test_resolve_unclear_position_unclear(self, ):
        string1 = '>117'
        string2 = '<1'
        string3 = '?327'
        string4 = '?10'
        message = f"For unclear position resolve_unclear_position function returns wrong output."
        assert 117 == resolve_unclear_position(string1), message
        assert 1 == resolve_unclear_position(string2), message
        assert 327 == resolve_unclear_position(string3), message
        assert 10 == resolve_unclear_position(string4), message

    def test_preprocess_uniprot(self, ):
        test_df = preprocess_uniprot(path_to_test_file)
        np.testing.assert_equal((167, 6), test_df.shape, err_msg = 'The shape of the returned file is incorrect.')
        assert test_df.feature.dtype == 'category', 'The type of the feature column is not a category.'
        # to check the cases when protein had no note but had feature, start and end, f.e.
        # FT   HELIX           14..31
        # FT                   /evidence="ECO:0000244|PDB:1DXX"
        np.testing.assert_array_equal(['P11532', 'HELIX', '', 14.0, 31.0, ''], 
                                    test_df[(test_df.feature == 'HELIX') & (test_df.start == 14)].values.tolist()[0],
                                    err_msg = "The output for the protein that doesn't have a note but has \
                                    feature information, a start and an end position is incorrect.")
        # to check the cases when protein had a note written in one line and doesn't have end, f.e.
        # FT   MOD_RES         3500
        # FT                   /note="Phosphoserine"
        np.testing.assert_array_equal(['P11532', 'MOD_RES', '', 3500.0, np.nan, 'Phosphoserine'],
                                    test_df[(test_df.feature == 'MOD_RES') & (test_df.start == 3500)].values.tolist()[0],
                                    err_msg = "The output for the protein that has the note written in one line \
                                    and doesn't have an end position for the feature is incorrect.")
        # to check the cases when protein had a note split into several line, f.e.
        # FT   VARIANT         3340
        # FT                   /note="C -> Y (in DMD; results in highly reduced protein
        # FT                   levels and expression at the sarcolemma)"
        assert 'C -> Y (in DMD; results in highly reduced protein levels and expression at the sarcolemma)' == \
        test_df[(test_df.feature == 'VARIANT') & (test_df.start == 3340)]['note'].values[0], \
        "The output for the protein that has a note split into several lines is incorrect."
        # to check the cases when protein had protein_ids written in several line, f.e.
        # AC   P11532; A1L0U9; E7EQR9; E7EQS5; E7ESB2; E9PDN1; E9PDN5; F5GZY3; F8VX32;
        # AC   Q02295; Q14169; Q14170; Q5JYU0; Q6NSJ9; Q7KZ48; Q8N754; Q9UCW3; Q9UCW4;
        assert 1 == test_df.protein_id.nunique(), "A preprocess_uniprot function returns a non-unique protein_id."
        assert 'P11532' == test_df.protein_id.unique()[0], 'A preprocess_uniprot function returns a wrong protein_id.'


if __name__ == "__main__":
    unittest.main()
