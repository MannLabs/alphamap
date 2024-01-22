#!python -m unittest tests.test_utils
"""This module provides unit tests for alphamap.cli."""

# builtin
import unittest

# local
from alphamap.organisms_data import import_fasta, \
    import_uniprot_annotation

class TestOrganisms(unittest.TestCase):

    def test_import_fasta(self, ):
        # Test if exception works
        try:
            out = import_fasta(organism='rat')
        except ValueError as e:
            out = e
        assert str(out) == "Organism rat is not available. Please select one of the following: ['Human', 'Mouse', 'Rat', 'Cow', 'Zebrafish', 'Drosophila', 'Caenorhabditis elegans', 'Slime mold', 'Arabidopsis thaliana', 'Rice', 'Escherichia coli', 'Bacillus subtilis', 'Saccharomyces cerevisiae', 'SARS-CoV', 'SARS-CoV2']" 
        # Test if fasta is read correctly
        ecoli_fasta = import_fasta('Escherichia coli')
        assert ecoli_fasta[0].sequence == "MSQNTLKVHDLNEDAEFDENGVEVFDEKALVEQEPSDNDLAEEELLSQGATQRVLDATQLYLGEIGYSPLLTAEEEVYFARRALRGDVASRRRMIESNLRLVVKIARRYGNRGLALLDLIEEGNLGLIRAVEKFDPERGFRFSTYATWWIRQTIERAIMNQTRTIRLPIHIVKELNVYLRTARELSHKLDHEPSAEEIAEQLDKPVDDVSRMLRLNERITSVDTPLGGDSEKALLDILADEKENGPEDTTQDDDMKQSIVKWLFELNAKQREVLARRFGLLGYEAATLEDVGREIGLTRERVRQIQVEGLRRLREILQTQGLNIEALFRE"
    
    def test_import_uniprot_annotation(self, ):
        # Test if exception works
        try:
            out = import_uniprot_annotation(organism='rat')
        except ValueError as e:
            out = e
        assert str(out) == "Organism rat is not available. Please select one of the following: ['Human', 'Mouse', 'Rat', 'Cow', 'Zebrafish', 'Drosophila', 'Caenorhabditis elegans', 'Slime mold', 'Arabidopsis thaliana', 'Rice', 'Escherichia coli', 'Bacillus subtilis', 'Saccharomyces cerevisiae', 'SARS-CoV', 'SARS-CoV2']" 
        # Test if fasta is read correctly
        ecoli_uniprot = import_uniprot_annotation('Escherichia coli')
        assert ecoli_uniprot.protein_id[0] == "P27685"

if __name__ == "__main__":
    unittest.main()
