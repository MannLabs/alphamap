rm -rf dist
rm -rf build
FILE=alphamap.pkg
if test -f "$FILE"; then
  rm alphamap.pkg
fi
conda env remove -n alphamapinstaller
conda create -n alphamapinstaller python=3.8 -y
# conda create -n alphamapinstaller python=3.8
conda activate alphamapinstaller
# call conda install git -y
# call pip install 'git+https://github.com/MannLabs/alphamap.git#egg=alphamap[gui]' --use-feature=2020-resolver
# brew install freetype
cd ../..
rm -rf dist
rm -rf build
python setup.py sdist bdist_wheel
cd misc/one_click_macos
pip install pyinstaller==4.2
pip install "../../dist/alphamap-0.0.2-py3-none-any.whl"
conda list
pyinstaller ../pyinstaller/alphamap.spec -y
conda deactivate
mkdir -p dist/alphamap/Contents/Resources
cp ../alpha_logo.icns dist/alphamap/Contents/Resources
mv dist/alphamap_gui dist/alphamap/Contents/MacOS
cp Info.plist dist/alphamap/Contents
cp alphamap_terminal dist/alphamap/Contents/MacOS
cp ../../LICENSE Resources/LICENSE
cp ../alpha_logo.png Resources/alpha_logo.png

if false; then
  # https://scriptingosx.com/2019/09/notarize-a-command-line-tool/
  for f in $(find dist/alphamap -name '*.so' -or -name   '*.dylib'); do codesign --sign "Developer ID Application: Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (7QSY5527AQ)" $f; done
  codesign --sign "Developer ID Application: Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (7QSY5527AQ)" dist/alphamap/Contents/MacOS/alphamap_gui --force --options=runtime --entitlements entitlements.xml
  codesign --sign "Developer ID Application: Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (7QSY5527AQ)" dist/alphamap/Contents/MacOS/kaleido/executable/bin/kaleido --force --options=runtime --entitlements entitlements.xml
  pkgbuild --root dist/alphamap --identifier de.mpg.biochem.alphamap.app --version 0.0.2 --install-location /Applications/AlphaMap.app --scripts scripts alphamap.pkg --sign "Developer ID Installer: Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (7QSY5527AQ)"
  productbuild --distribution distribution.xml --resources Resources --package-path alphamap.pkg dist/alphamap_gui_installer_macos.pkg --sign "Developer ID Installer: Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (7QSY5527AQ)"
  requestUUID=$(xcrun altool --notarize-app --primary-bundle-id "de.mpg.biochem.alphamap.app" --username "willems@biochem.mpg.de" --password "@keychain:Alphatims-develop" --asc-provider 7QSY5527AQ --file dist/alphamap_gui_installer_macos.pkg 2>&1 | awk '/RequestUUID/ { print $NF; }')
  request_status="in progress"
  while [[ "$request_status" == "in progress" ]]; do
      echo "$request_status"
      sleep 10
      request_status=$(xcrun altool --notarization-info "$requestUUID" --username "willems@biochem.mpg.de" --password "@keychain:Alphatims-develop" | awk -F ': ' '/Status:/ { print $2; }' )
  done
  xcrun altool --notarization-info "$requestUUID" --username "willems@biochem.mpg.de" --password "@keychain:Alphatims-develop"
  xcrun stapler staple dist/alphamap_gui_installer_macos.pkg
else
  pkgbuild --root dist/alphamap --identifier de.mpg.biochem.alphamap.app --version 0.0.2 --install-location /Applications/AlphaMap.app --scripts scripts alphamap.pkg
  productbuild --distribution distribution.xml --resources Resources --package-path alphamap.pkg dist/alphamap_gui_installer_macos.pkg
fi
