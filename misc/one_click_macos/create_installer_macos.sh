rm -rf dist
rm -rf build
conda env remove -n alphamapinstaller
conda create -n alphamapinstaller python=3.8 pip=20.2 -y
# conda create -n alphamapinstaller python=3.8
conda activate alphamapinstaller
# call conda install git -y
# call pip install 'git+https://github.com/MannLabs/alphamap.git#egg=alphamap[gui]' --use-feature=2020-resolver
# brew install freetype
pip install '../../.'
#pip install pyinstaller
pip install git+https://github.com/pyinstaller/pyinstaller.git # @todo fix to stable release 4.3 once out to be compatible with Big Sur
pyinstaller ../pyinstaller/alphamap.spec -y
mv dist/alphamap dist/alphamap.app
tar -czf dist/alphamap.app.zip dist/alphamap.app
# chmod +x dist/alphatims.app
# TODO No console is opened and program not blocked untill close, meaning loose threads!
conda deactivate
