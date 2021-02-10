REM rmdir dist /s /q
REM rmdir build /s /q
REM conda env remove -n alphamapinstaller
call conda create -n alphamapinstaller python=3.8 pip=20.2 -y
REM call conda create -n alphamapinstaller python=3.8 -y
call conda activate alphamapinstaller
REM call conda install git -y
REM call pip install 'git+https://github.com/MannLabs/alphamap.git#egg=alphamap[gui]'
REM call conda install freetype
call pip install ../../.[gui]
call pip install pyinstaller
call pip install numpy==1.19.3
REM
call pyinstaller ../pyinstaller/alphamap.spec -y
call conda deactivate
call "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" alphamap_innoinstaller.iss
REM call iscc alphamap_innoinstaller.iss
