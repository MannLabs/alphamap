conda activate alphamap
python -m unittest test_importing
python -m unittest test_preprocessing
python -m unittest test_gui
conda deactivate
