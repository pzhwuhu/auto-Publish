@echo off
chcp 65001 >nul
title 自动生成的构建脚本

echo 开始构建...

pyinstaller ^
    --onefile ^
    --windowed ^
    --noconsole ^
    --clean ^
    --name=HexoPublisher ^
    --add-data="example_template.md;." ^
    --add-binary="D:\Application\Anaconda\Library\bin\tcl86t.dll;." ^
    --add-binary="D:\Application\Anaconda\Library\bin\tk86t.dll;." ^
    --add-binary="D:\Application\Anaconda\Library\bin\zlib.dll;." ^
    --add-binary="D:\Application\Anaconda\Library\bin\sqlite3.dll;." ^
    --add-binary="D:\Application\Anaconda\DLLs\_tkinter.pyd;." ^
    --add-binary="D:\Application\Anaconda\DLLs\_ctypes.pyd;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=_tkinter ^
    --hidden-import=ctypes ^
    --hidden-import=_ctypes ^
    --hidden-import=ctypes.wintypes ^
    --collect-all=tkinter ^
    --collect-all=ctypes ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=scipy ^
    --exclude-module=IPython ^
    --exclude-module=jupyter ^
    --exclude-module=notebook ^
    --exclude-module=PIL ^
    --exclude-module=cv2 ^
    --exclude-module=tensorflow ^
    --exclude-module=torch ^
    --noupx ^
    hexo_publisher.py

echo 构建完成！
pause
