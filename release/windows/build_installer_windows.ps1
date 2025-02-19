# Build the installer for Windows.
# This script must be run from the root of the repository.

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./build_pyinstaller
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./dist_pyinstaller


$WHL_NAME = (Get-ChildItem -Path "dist" -Filter "*.whl").Name
pip install "dist/$WHL_NAME[stable,structuremap-stable]"

New-Item -ItemType Directory -Force -Path dist/alphamap_gui/alphamap/data
Copy-Item alphamap/data/*.fasta dist/alphamap_gui/alphamap/data
Copy-Item alphamap/data/*.csv dist/alphamap_gui/alphamap/data

# Creating the stand-alone pyinstaller folder
pyinstaller release/pyinstaller/alphamap.spec --distpath dist_pyinstaller --workpath build_pyinstaller -y
