# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = []
datas += collect_data_files('TKinterModernThemes')


a = Analysis(
    ['M:\\new_mrubiodev\\Regex2Excel\\Regex2Excel.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['git', 'openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Regex2Excel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['M:\\new_mrubiodev\\Regex2Excel\\res\\app_icon.ico'],
)
