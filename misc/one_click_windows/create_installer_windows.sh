rm -rf dist
rm -rf build
conda create -n alphamapinstaller python=3.8 -y
conda activate alphamapinstaller
cd ../..
rm -rf dist
rm -rf build
python setup.py sdist bdist_wheel
cd misc/one_click_windows
pip install "../../dist/alphamap-0.1.9-py3-none-any.whl"
pip install pyinstaller==4.2
# TODO https://stackoverflow.com/questions/54175042/python-3-7-anaconda-environment-import-ssl-dll-load-fail-error/60405693#60405693
pyinstaller ../pyinstaller/alphamap.spec -y
conda deactivate

FILE="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if test -f "$FILE"; then
  "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" alphamap_innoinstaller.iss
else
  mkdir inno
  is.exe //SILENT //DIR=inno
  "inno/ISCC.exe" alphamap_innoinstaller.iss
fi


# if false; then
#   is.exe /SILENT /DIR=.
#   inno\ISCC.exe alphamap_innoinstaller.iss
# else
#   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" alphamap_innoinstaller.iss
# fi
