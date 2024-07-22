rm -rf dist
rm -rf build
FILE=alphamap.pkg
if test -f "$FILE"; then
  rm alphamap.pkg
fi
conda env remove -n alphamapinstaller
conda create -n alphamapinstaller python=3.8 -y
conda activate alphamapinstaller

cd ../..
rm -rf dist
rm -rf build
pip install build
python -m build
pip install "dist/alphamap-0.1.11-py3-none-any.whl[stable]"

conda list

cd misc/one_click_macos
pip install pyinstaller==5.6.2
pyinstaller ../pyinstaller/alphamap.spec -y

conda deactivate

CONTENTS_DIR=dist/alphamap/Contents
RESOURCES_DIR=$CONTENTS_DIR/Resources
MACOS_DIR=$CONTENTS_DIR/MacOS

mkdir -p $RESOURCES_DIR
cp ../alpha_logo.icns $RESOURCES_DIR
mv dist/alphamap_gui $MACOS_DIR
cp Info.plist $CONTENTS_DIR
cp alphamap_terminal $MACOS_DIR
cp ../../LICENSE $RESOURCES_DIR
cp ../alpha_logo.png $RESOURCES_DIR

# copy data
mkdir -p $MACOS_DIR/alphamap/data
cp ../../alphamap/data/*.fasta $MACOS_DIR/alphamap/data
cp ../../alphamap/data/*.csv $MACOS_DIR/alphamap/data

# link _internal folder containing the python libraries to the Frameworks folder where they are expected
# to avoid e.g. "Failed to load Python shared library '/Applications/AlphaMap.app/Contents/Frameworks/libpython3.8.dylib'"
cd $CONTENTS_DIR
ln -s ./MacOS/_internal ./Frameworks
cd -

pkgbuild --root dist/alphamap --identifier de.mpg.biochem.alphamap.app --version 0.1.11 --install-location /Applications/AlphaMap.app --scripts scripts alphamap.pkg
productbuild --distribution distribution.xml --resources Resources --package-path alphamap.pkg dist/alphamap_gui_installer_macos.pkg
