conda create -n alphamap python=3.8 -y
conda activate alphamap
pip install -e '../.[stable,development-stable]'
alphamap
conda deactivate
