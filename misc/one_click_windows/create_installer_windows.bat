call rmdir dist /s /q
call rmdir build /s /q
call conda env remove -n alphamapinstaller
call conda create -n alphamapinstaller python=3.8 -y
REM call conda create -n alphamapinstaller python=3.8 -y
call conda activate alphamapinstaller
REM call conda install git -y
REM call pip install 'git+https://github.com/MannLabs/alphamap.git#egg=alphamap[gui]'
REM call conda install freetype
REM call pip install ../../.[plotting]
REM call pip install pyinstaller==4.2
REM call pyinstaller ../pyinstaller/alphamap.spec -y
call cd ../..
call rmdir dist /s /q
call rmdir build /s /q
call python setup.py sdist bdist_wheel
call cd misc/one_click_windows
call pip install "../../dist/alphamap-0.0.4-py3-none-any.whl"
call pip install pyinstaller==4.2
call pyinstaller ../pyinstaller/alphamap.spec -y
call conda deactivate


call "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" alphamap_innoinstaller.iss
