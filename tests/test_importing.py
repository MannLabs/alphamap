#!python -m unittest tests.test_utils
"""This module provides unit tests for alphamap.cli."""

# builtin
import unittest

import os
import pandas as pd

# local
from alphamap.importing import read_file, \
    extract_rawfile_unique_values, \
    import_spectronaut_data, \
    import_maxquant_data, \
    convert_ap_mq_mod, \
    import_alphapept_data, \
    convert_diann_mq_mod, \
    import_diann_data, \
    convert_fragpipe_mq_mod, \
    import_fragpipe_data, \
    import_data

THIS_FOLDER = os.path.dirname(__file__)
TEST_FOLDER = os.path.join(
    f"{os.path.dirname(THIS_FOLDER)}",
    "nbs",
    "testdata",
)

class TestImporting(unittest.TestCase):

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

    def test_import_spectronaut_data(self, ):
        # test entire input test data
        data = import_spectronaut_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.csv'))
        #print(data.shape[0])
        assert data.shape[0] == 40
        data_t = import_spectronaut_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.tsv'))
        #print(data_t.shape[0])
        pd.testing.assert_frame_equal(data, data_t)
        test = pd.read_csv(os.path.join(TEST_FOLDER, 'test_spectronaut_imported.csv'), sep=',') 
        #print(test.shape[0])
        pd.testing.assert_frame_equal(data, test)
        
        # test single sample
        data = import_spectronaut_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.csv'), 
                                    sample="raw_01")
        #print(data.shape[0])
        assert data.shape[0] == 40
        data = import_spectronaut_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.csv'), 
                                    sample="raw_02")
        #print(data.shape[0])
        assert data.shape[0] == 20
        
        # test multiple samples
        data = import_spectronaut_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.csv'), 
                                    sample=["raw_01","raw_02"])
        #print(data.shape[0])
        assert data.shape[0] == 40

    def test_import_maxquant_data(self, ):
        data = import_maxquant_data(os.path.join(TEST_FOLDER, 'test_maxquant_input.txt'))
        test = pd.read_csv(os.path.join(TEST_FOLDER, 'test_maxquant_imported.csv'), sep=',') 
        pd.testing.assert_frame_equal(data, test)
        
        data_s = import_maxquant_data(os.path.join(TEST_FOLDER, 'test_maxquant_input.txt'), 
                                    sample = "raw_1")
        assert data_s.shape[0] == 85
        
        data_s = import_maxquant_data(os.path.join(TEST_FOLDER, 'test_maxquant_input.txt'), 
                                    sample = "raw_2")
        assert data_s.shape[0] == 77
        
        data_s = import_maxquant_data(os.path.join(TEST_FOLDER, 'test_maxquant_input.txt'), 
                                    sample = ["raw_1", "raw_2"])
        assert data_s.shape[0] == 136

    def test_convert_ap_mq_mod(self, ):
        # test oxidation
        seq1 = 'HAEoxMVHTGLK' 
        assert "HAEM[Oxidation (M)]VHTGLK" == convert_ap_mq_mod(seq1)
        seq2 = 'HAEoxPVHTGLK' 
        assert "HAEP[Oxidation (MP)]VHTGLK" == convert_ap_mq_mod(seq2)
        # test acetylation
        seq4 = 'aMDEPSPLAQPLELNQHSR' 
        assert "[Acetyl (N-term)]MDEPSPLAQPLELNQHSR" == convert_ap_mq_mod(seq4)
        seq5 = 'MDEPSaKPLA' 
        assert "MDEPSK[Acetyl (K)]PLA" == convert_ap_mq_mod(seq5)
        # test amidation
        seq6 = 'MDEPSKPLamA' 
        assert "MDEPSKPLA[Amidated (C-term)]" == convert_ap_mq_mod(seq6)
        # test deamidation
        seq7 = 'MDEPSdeamNKPLA' 
        assert "MDEPSN[Deamidation (NQ)]KPLA" == convert_ap_mq_mod(seq7)
        seq8 = 'MDEPSdeamQKPLA' 
        assert "MDEPSQ[Deamidation (NQ)]KPLA" == convert_ap_mq_mod(seq8)
        # test phosporylation
        seq9 = 'MDEPSpSKPLA' 
        assert "MDEPSS[Phospho (STY)]KPLA" == convert_ap_mq_mod(seq9)
        # test pyro-Glu
        seq10 = 'MDpgEPSNKPLA' 
        assert "MDE[Glu->pyro-Glu]PSNKPLA" == convert_ap_mq_mod(seq10)
        seq11 = 'MDpgQPSNKPLA' 
        assert "MDQ[Gln->pyro-Glu]PSNKPLA" == convert_ap_mq_mod(seq11)
        # test disylfide bonds
        seq12 = 'cCVNTTLQIK'
        assert "C[Cys-Cys]VNTTLQIK" == convert_ap_mq_mod(seq12)
        seq1_several_dif_mods = 'AcCLDYPVTSVLPPASLoxMK'
        assert "AC[Cys-Cys]LDYPVTSVLPPASLM[Oxidation (M)]K" == convert_ap_mq_mod(seq1_several_dif_mods)
        seq2_several_same_mods = 'LFTToxMELoxMR'
        assert "LFTTM[Oxidation (M)]ELM[Oxidation (M)]R" == convert_ap_mq_mod(seq2_several_same_mods)
        seq3_several_same_mods = 'LFTToxMELoxMRoxM'
        assert "LFTTM[Oxidation (M)]ELM[Oxidation (M)]RM[Oxidation (M)]" == convert_ap_mq_mod(seq3_several_same_mods)
        seq4_several_same_mods = 'LFTTdeamNELdeamNR'
        assert "LFTTN[Deamidation (NQ)]ELN[Deamidation (NQ)]R" == convert_ap_mq_mod(seq4_several_same_mods)
        seq_no_mod = 'CVNTTLQIK'
        assert "CVNTTLQIK" == convert_ap_mq_mod(seq_no_mod)

    def test_import_alphapept_data(self, ):
        data = import_alphapept_data(os.path.join(TEST_FOLDER, 'test_alphapept_input.csv'))
        assert data.shape == (4228, 3)
        
        data_s1 = import_alphapept_data(os.path.join(TEST_FOLDER, 'test_alphapept_input.csv'), 
                                    sample = "exp_1")
        assert data_s1.shape[0] == 2127
        
        data_s2 = import_alphapept_data(os.path.join(TEST_FOLDER, 'test_alphapept_input.csv'), 
                                    sample = "exp_2")
        assert data_s2.shape[0] == 2101
        
        data_s_both = import_alphapept_data(os.path.join(TEST_FOLDER, 'test_alphapept_input.csv'), 
                                    sample = ["exp_1", "exp_2"])
        assert data_s_both.shape[0] == 4228

    def test_convert_diann_mq_mod(self, ):
        seq1 = 'VSHGSSPSLLEALSSDFLAC(UniMod:4)K'
        assert 'VSHGSSPSLLEALSSDFLAC[Carbamidomethyl (C)]K' == convert_diann_mq_mod(seq1)
        seq2 = 'VSVINTVDTSHEDMIHDAQM(UniMod:35)DYYGTR'
        assert 'VSVINTVDTSHEDMIHDAQM[Oxidation (M)]DYYGTR' == convert_diann_mq_mod(seq2)
        seq3 = 'HAEMPVHTGLK(UniMod:2)' 
        assert 'HAEMPVHTGLK[Amidated (C-term)]' == convert_diann_mq_mod(seq3)
        seq4 = 'HAEMPVHTGLKS(UniMod:23)A'
        assert 'HAEMPVHTGLKS[Dehydrated (ST)]A' == convert_diann_mq_mod(seq4)
        seq5 = 'HAEMPVHTGLKY(UniMod:23)A' 
        assert 'HAEMPVHTGLKY[Dehydrated (Y)]A' == convert_diann_mq_mod(seq5)
        
        seq1_several_dif_mods = '(UniMod:1)VSHGSSPSLLEALSSDFLAC(UniMod:4)K'
        assert '[Acetyl (N-term)]VSHGSSPSLLEALSSDFLAC[Carbamidomethyl (C)]K' == convert_diann_mq_mod(seq1_several_dif_mods)
        seq2_several_same_mods = 'CAALVATAEENLC(UniMod:4)C(UniMod:4)EELSSK'
        assert 'CAALVATAEENLC[Carbamidomethyl (C)]C[Carbamidomethyl (C)]EELSSK' == convert_diann_mq_mod(seq2_several_same_mods)
        seq_no_mod = 'CVNTTLQIK'
        assert "CVNTTLQIK" == convert_diann_mq_mod(seq_no_mod)

    def test_import_diann_data(self, ):
        data = import_diann_data(os.path.join(TEST_FOLDER, 'test_diann_input.tsv'))
        assert data.shape == (44, 3)
        
        data_s1 = import_diann_data(os.path.join(TEST_FOLDER, 'test_diann_input.tsv'), 
                                    sample = "20201218_tims03_Evo03_PS_SA_HeLa_200ng_high_speed_21min_8cm_S2-B2_1_22648")
        assert data_s1.shape[0] == 39
        
        data_s_both = import_diann_data(os.path.join(TEST_FOLDER, 'test_diann_input.tsv'), 
                                        sample = ["20201218_tims03_Evo03_PS_SA_HeLa_200ng_high_speed_21min_8cm_S2-B2_1_22648", 
                                                  "20201218_tims03_Evo03_PS_SA_HeLa_200ng_high_speed_21min_8cm_S2-A2_1_22636"])
        assert data_s_both.shape[0] == 42

    def test_convert_fragpipe_mq_mod(self, ):
        seq1 = 'AAEREPPPLGDGKPTDFEDLEDGEDLFTSTVSTLE'
        modif1 = 'N-term(42.0106)'
        assert '[Acetyl (N-term)]AAEREPPPLGDGKPTDFEDLEDGEDLFTSTVSTLE' == convert_fragpipe_mq_mod(seq1, modif1)
        seq2 = 'AAEVISDARENIQRFFGHGAEDSLADQAANEWGRSGKDPNHFRPAGLPEKY'
        modif2 = 'C-term(-0.9840)'
        assert 'AAEVISDARENIQRFFGHGAEDSLADQAANEWGRSGKDPNHFRPAGLPEKY[Amidated (C-term)]' == convert_fragpipe_mq_mod(seq2, modif2)
        seq3 = 'QESQSEEIDCNDKDLFKA'
        modif3 = '1Q(-17.0265)'
        assert 'Q[Gln->pyro-Glu]ESQSEEIDCNDKDLFKA' == convert_fragpipe_mq_mod(seq3, modif3)
        seq4 = 'EKPLLEKSHCIAEVENDEMPA'
        modif4 = '1E(-18.0106)'
        assert 'E[Glu->pyro-Glu]KPLLEKSHCIAEVENDEMPA' == convert_fragpipe_mq_mod(seq4, modif4)
        seq5 = 'SKPLLEKSHCIAEVENDEMPA'
        modif5 = '1S(-18.0106)'
        assert 'S[Dehydrated (ST)]KPLLEKSHCIAEVENDEMPA' == convert_fragpipe_mq_mod(seq5, modif5)
        seq6 = 'YKPLLEKSHCIAEVENDEMPA'
        modif6 = '1Y(-18.0106)'
        assert 'Y[Dehydrated (Y)]KPLLEKSHCIAEVENDEMPA' == convert_fragpipe_mq_mod(seq6, modif6)
        seq1_several_dif_mods = 'AAAAECDVVMAATEPELLDDQEAK'
        seq1_several_dif_mods_modifs = '10M(15.9949),6C(57.0215),N-term(42.0106)'
        assert '[Acetyl (N-term)]AAAAEC[Carbamidomethyl (C)]DVVM[Oxidation (M)]AATEPELLDDQEAK' == convert_fragpipe_mq_mod(
            seq1_several_dif_mods, seq1_several_dif_mods_modifs)
        seq2_several_dif_mods = 'PGFSIADKKR'
        seq2_several_dif_mods_modifs = '8K(114.0429),9K(114.0429)'
        assert 'PGFSIADK[GlyGly (K)]K[GlyGly (K)]R' == convert_fragpipe_mq_mod(
            seq2_several_dif_mods, seq2_several_dif_mods_modifs)
        seq_no_mod = 'CVNTTLQIK'
        seq_no_mod_modifs = ''
        assert "CVNTTLQIK" == convert_fragpipe_mq_mod(seq_no_mod, seq_no_mod_modifs)

    def test_import_fragpipe_data(self, ):
        data = import_fragpipe_data(os.path.join(TEST_FOLDER, 'test_fragpipe_input.tsv'))
        assert data.shape == (50, 3)
        
        sample = 'Y731F1'
        file = os.path.join(TEST_FOLDER, 'combined_peptide.txt')
        assert import_fragpipe_data(file, sample).shape == (23, 3)
        
        two_samples = ['Y731F1', 'Y731F2']
        assert import_fragpipe_data(file, two_samples).shape == (26, 3)

    def test_import_data(self, ):
        data_MQ = import_data(os.path.join(TEST_FOLDER, 'test_maxquant_input.txt'), verbose=False)
        test = pd.read_csv(os.path.join(TEST_FOLDER, 'test_maxquant_imported.csv'), sep=',') 
        pd.testing.assert_frame_equal(data_MQ, test)
        
        data_S_csv = import_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.csv'), verbose=False)
        data_S_tsv = import_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.tsv'), verbose=False)
        pd.testing.assert_frame_equal(data_S_csv, data_S_tsv)
        test = pd.read_csv(os.path.join(TEST_FOLDER, 'test_spectronaut_imported.csv'), sep=',') 
        pd.testing.assert_frame_equal(data_S_csv, test)
        
        data_S_sub = import_data(os.path.join(TEST_FOLDER, 'test_spectronaut_input.csv'), 
                                sample = "raw_01", 
                                verbose=False)
        assert data_S_sub.shape[0] == 40
        
        data_alphapept = import_data(os.path.join(TEST_FOLDER, 'test_alphapept_input.csv'), 
                                sample = "exp_1", 
                                verbose=False)
        assert data_alphapept.shape[0] == 2127
        
        data_diann = import_data(os.path.join(TEST_FOLDER, 'test_diann_input.tsv'), 
                                    sample = "20201218_tims03_Evo03_PS_SA_HeLa_200ng_high_speed_21min_8cm_S2-B2_1_22648", 
                                    verbose=False)
        assert data_diann.shape[0] == 39
        
        data_fragpipe = import_data(os.path.join(TEST_FOLDER, 'test_fragpipe_input.tsv'),  
                                    verbose=False)
        assert data_fragpipe.shape[0] == 50
        
        try:
            out = import_data(os.path.join(TEST_FOLDER, 'test_uniprot_df.csv'))
        except TypeError as e:
            out = e
        assert str(out) == "Input data format for "+os.path.join(TEST_FOLDER, 'test_uniprot_df.csv')+" not known."
   

if __name__ == "__main__":
    unittest.main()
