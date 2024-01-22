#!python -m unittest tests.test_utils
"""This module provides unit tests for alphamap.cli."""

# builtin
import unittest
import os
import pandas as pd
import numpy as np

# local
from alphamap.sequenceplot import format_uniprot_annotation
from alphamap.uniprot_integration import uniprot_feature_dict

THIS_FOLDER = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(
    f"{os.path.dirname(THIS_FOLDER)}",
    "alphamap",
    "data",
)

class TestSequenceplot(unittest.TestCase):
    def test_format_uniprot_annotation(self, ):
        in_df = pd.read_csv(os.path.join(DATA_FOLDER,'preprocessed_uniprot_human.csv'))
        id_df_structure = in_df[in_df.protein_id  == "P43166"]
        id_df_structure_form = format_uniprot_annotation(id_df_structure, uniprot_feature_dict)
        
        np.testing.assert_equal(np.unique(id_df_structure_form[id_df_structure_form.feature=="STRUCTURE"].annotation), 
                                ['Beta strand', 'Helix', 'Turn'])
        
        id_df_nan = in_df[in_df.protein_id  == "Q8IYX3"]
        id_df_nan_form = format_uniprot_annotation(id_df_nan, uniprot_feature_dict)
        np.testing.assert_equal(id_df_nan_form[id_df_nan_form.feature=="COILED"].annotation.values,
                                'Coiled coil')

if __name__ == "__main__":
    unittest.main()
