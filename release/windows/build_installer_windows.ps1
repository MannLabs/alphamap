# Build the installer for Windows.
# This script must be run from the root of the repository.

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./build_pyinstaller
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./dist_pyinstaller


$WHL_NAME = (Get-ChildItem -Path "dist" -Filter "*.whl").Name
pip install "dist/$WHL_NAME[stable,structuremap-stable]"

# Creating the stand-alone pyinstaller folder
pyinstaller release/pyinstaller/alphamap.spec --distpath dist_pyinstaller --workpath build_pyinstaller -y

# copy files excluded in MANIFEST.in
New-Item -ItemType Directory -Force -Path dist_pyinstaller/alphamap/data
Copy-Item alphamap/data/*.fasta dist_pyinstaller/alphamap/data
Copy-Item alphamap/data/*.csv dist_pyinstaller/alphamap/data