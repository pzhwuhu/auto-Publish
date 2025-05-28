# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('example_template.md', '.')]
binaries = [('D:\\Application\\Anaconda\\Library\\bin\\tcl86t.dll', '.'), ('D:\\Application\\Anaconda\\Library\\bin\\tk86t.dll', '.'), ('D:\\Application\\Anaconda\\DLLs\\_tkinter.pyd', '.'), ('D:\\Application\\Anaconda\\DLLs\\_ctypes.pyd', '.'), ('D:\\Application\\Anaconda\\Library\\bin\\ffi-7.dll', '.'), ('D:\\Application\\Anaconda\\Library\\bin\\ffi-8.dll', '.'), ('D:\\Application\\Anaconda\\Library\\bin\\ffi.dll', '.'), ('D:\\Application\\Anaconda\\Library\\bin\\zlib.dll', '.'), ('D:\\Application\\Anaconda\\Library\\bin\\sqlite3.dll', '.')]
hiddenimports = ['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', '_tkinter', 'ctypes', '_ctypes', 'ctypes.wintypes']
tmp_ret = collect_all('tkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('ctypes')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['hexo_publisher_safe.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'IPython', 'jupyter', 'notebook', 'PIL', 'cv2', 'tensorflow', 'torch'],
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
    name='HexoPublisher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
