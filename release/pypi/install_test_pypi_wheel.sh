conda create -n alphamap_pip_test python=3.8 -y
conda activate alphamap_pip_test
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple "alphamap[stable]"
alphamap
conda deactivate
