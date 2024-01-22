#!python -m unittest tests.test_utils
"""This module provides unit tests for alphamap.cli."""

# builtin
import unittest
import numpy as np

# local
from alphamap.proteolytic_cleavage import get_cleavage_sites

class TestProteolytic(unittest.TestCase):
    def test_get_cleavage_sites(self, ):
        cleavage_sites = get_cleavage_sites("PEPTIDERANGEKATRAT", "trypsin")
        np.testing.assert_equal(cleavage_sites, [7, 12, 15])
        cleavage_sites2 = get_cleavage_sites("PEPTIDERANGEKATRAT", "lysc")
        np.testing.assert_equal(cleavage_sites2, [12])
        cleavage_sites3 = get_cleavage_sites("PEPTIDERANGEKATRAT", "caspase 2")
        np.testing.assert_equal(cleavage_sites3, [])
        cleavage_sites4 = get_cleavage_sites("PEPVDVADTIDE", "caspase 2")
        np.testing.assert_equal(cleavage_sites4, [7])

if __name__ == "__main__":
    unittest.main()
