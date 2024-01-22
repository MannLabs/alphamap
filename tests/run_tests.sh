conda activate alphamap
python -m unittest test_importing
python -m unittest test_preprocessing
python -m unittest test_sequenceplot
python -m unittest test_uniprot_integration
python -m unittest test_organisms_data
python -m unittest test_proteolytic_cleavage
python -m unittest test_gui
conda deactivate
