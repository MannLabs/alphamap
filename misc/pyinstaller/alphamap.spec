# -*- mode: python ; coding: utf-8 -*-

import pkgutil
import os
import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, BUNDLE, TOC
import PyInstaller.utils.hooks
from PyInstaller.utils.hooks import copy_metadata
import pkg_resources
import importlib.metadata


##################### User definitions
exe_name = 'alphamap_gui'
script_name = 'alphamap_pyinstaller.py'
if sys.platform[:6] == "darwin":
	icon = '../alpha_logo.icns'
else:
	icon = '../alpha_logo.ico'
block_cipher = None
location = os.getcwd()
project = "alphamap"
remove_tests = True
bundle_name = "AlphaMap"
#####################


datas, binaries, hidden_imports = PyInstaller.utils.hooks.collect_all(
	project,
	include_py_files=True
)
hidden_imports = [h for h in hidden_imports if "__pycache__" not in h]
datas = [d for d in datas if ("__pycache__" not in d[0]) and (d[1] not in [".", "Resources", "scripts"])]

a = Analysis(
	[script_name],
	pathex=[location],
	binaries=binaries,
	datas=datas,
	hiddenimports=hidden_imports,
	hookspath=['./release/pyinstaller/hookdir'],
	runtime_hooks=[],
	excludes=[],
    win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher,
	noarchive=False
)
pyz = PYZ(
	a.pure,
	a.zipped_data,
	cipher=block_cipher
)

if sys.platform[:5] == "linux":
	exe = EXE(
		pyz,
		a.scripts,
		a.binaries,
		a.zipfiles,
		a.datas,
		name=bundle_name,
		debug=False,
		bootloader_ignore_signals=False,
		strip=False,
		upx=True,
		console=True,
		upx_exclude=[],
		icon=icon
	)
else:
	exe = EXE(
		pyz,
		a.scripts,
		# a.binaries,
		a.zipfiles,
		# a.datas,
		exclude_binaries=True,
		name=exe_name,
		debug=False,
		bootloader_ignore_signals=False,
		strip=False,
		upx=True,
		console=True,
		icon=icon
	)
	coll = COLLECT(
		exe,
		a.binaries,
		# a.zipfiles,
		a.datas,
		strip=False,
		upx=True,
		upx_exclude=[],
		name=exe_name
	)