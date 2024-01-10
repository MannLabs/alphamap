conda create -n alphamap_pip_test python=3.8 -y
conda activate alphamap_pip_test
pip install "alphamap[stable]"
alphamap
conda deactivate
