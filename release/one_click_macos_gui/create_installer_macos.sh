#!bash

# Initial cleanup
rm -rf dist
rm -rf build
FILE=alphamap.pkg
if test -f "$FILE"; then
  rm alphamap.pkg
fi
cd ../..
rm -rf dist
rm -rf build

# Creating a conda environment
conda create -n alphamapinstaller python=3.8 -y
conda activate alphamapinstaller

# Creating the wheel
python setup.py sdist bdist_wheel

# Setting up the local package
cd release/one_click_macos_gui
pip install "../../dist/alphamap-0.0.1-py3-none-any.whl[stable]"

# Creating the stand-alone pyinstaller folder
pip install pyinstaller==4.2
pyinstaller ../pyinstaller/alphamap.spec -y
conda deactivate

# If needed, include additional source such as e.g.:
# cp ../../alphamap/data/*.fasta dist/alphamap/data

# Wrapping the pyinstaller folder in a .pkg package
mkdir -p dist/alphamap/Contents/Resources
cp ../logos/alpha_logo.icns dist/alphamap/Contents/Resources
mv dist/alphamap_gui dist/alphamap/Contents/MacOS
cp Info.plist dist/alphamap/Contents
cp alphamap_terminal dist/alphamap/Contents/MacOS
cp ../../LICENSE.txt Resources/LICENSE.txt
cp ../logos/alpha_logo.png Resources/alpha_logo.png
chmod 777 scripts/*

pkgbuild --root dist/alphamap --identifier de.mpg.biochem.alphamap.app --version 0.0.1 --install-location /Applications/alphamap.app --scripts scripts alphamap.pkg
productbuild --distribution distribution.xml --resources Resources --package-path alphamap.pkg dist/alphamap_gui_installer_macos.pkg
