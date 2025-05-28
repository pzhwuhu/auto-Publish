@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Build Script - Hexo Publisher

echo =======================================
echo    Build Script - Hexo Publisher
echo    Fixing tkinter and ctypes DLL issues
echo =======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python 3.6+
    pause
    exit /b 1
)

echo Detecting Python environment...
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.prefix)"') do set PYTHON_PATH=%%i
echo Python directory: %PYTHON_PATH%

echo.
echo Detecting Python environment type...
python -c "import sys; print('Anaconda' if 'anaconda' in sys.executable.lower() or 'conda' in sys.executable.lower() else 'Standard')" > temp_env.txt
set /p PYTHON_ENV=<temp_env.txt
del temp_env.txt
echo Python environment: %PYTHON_ENV%

echo.
echo Testing key modules...
python -c "import tkinter; import _tkinter; import ctypes; import _ctypes; print('All key modules OK')"
if errorlevel 1 (
    echo Error: Key modules cannot be imported
    pause
    exit /b 1
)

echo.
echo Installing/updating PyInstaller...
pip install --upgrade pyinstaller

echo.
echo Cleaning previous build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo Checking necessary DLL file locations...

REM Set DLL paths
if "%PYTHON_ENV%"=="Anaconda" (
    set DLL_BASE=%PYTHON_PATH%\Library\bin
    set PYD_BASE=%PYTHON_PATH%\DLLs
    set LIB_BASE=%PYTHON_PATH%\Library\lib
) else (
    set DLL_BASE=%PYTHON_PATH%\DLLs
    set PYD_BASE=%PYTHON_PATH%\DLLs
    set LIB_BASE=%PYTHON_PATH%\libs
)

REM tkinter related DLLs
set TCL_DLL=%DLL_BASE%\tcl86t.dll
set TK_DLL=%DLL_BASE%\tk86t.dll
set TKINTER_PYD=%PYD_BASE%\_tkinter.pyd

REM ctypes related DLLs
set CTYPES_PYD=%PYD_BASE%\_ctypes.pyd
set LIBFFI_DLL=%DLL_BASE%\ffi-7.dll
set LIBFFI_DLL2=%DLL_BASE%\ffi-8.dll
set LIBFFI_DLL3=%DLL_BASE%\ffi.dll

REM Other necessary DLLs
set ZLIB_DLL=%DLL_BASE%\zlib.dll
set SQLITE_DLL=%DLL_BASE%\sqlite3.dll

echo Checking file existence...
echo TCL DLL: %TCL_DLL%
if exist "%TCL_DLL%" (echo OK: exists) else (echo WARNING: not found)

echo TK DLL: %TK_DLL%
if exist "%TK_DLL%" (echo OK: exists) else (echo WARNING: not found)

echo TKINTER PYD: %TKINTER_PYD%
if exist "%TKINTER_PYD%" (echo OK: exists) else (echo WARNING: not found)

echo CTYPES PYD: %CTYPES_PYD%
if exist "%CTYPES_PYD%" (echo OK: exists) else (echo WARNING: not found)

echo LIBFFI DLL: %LIBFFI_DLL%
if exist "%LIBFFI_DLL%" (echo OK: exists) else (echo WARNING: not found)

echo LIBFFI DLL2: %LIBFFI_DLL2%
if exist "%LIBFFI_DLL2%" (echo OK: exists) else (echo WARNING: not found)

echo LIBFFI DLL3: %LIBFFI_DLL3%
if exist "%LIBFFI_DLL3%" (echo OK: exists) else (echo WARNING: not found)

REM Check critical files
if not exist "%TKINTER_PYD%" (
    echo Error: Cannot find _tkinter.pyd
    pause
    exit /b 1
)

if not exist "%CTYPES_PYD%" (
    echo Error: Cannot find _ctypes.pyd
    pause
    exit /b 1
)

echo.
echo Building exe file with all necessary DLLs...

REM Build add-binary parameters
set ADD_BINARIES=
if exist "%TCL_DLL%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%TCL_DLL%;."
if exist "%TK_DLL%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%TK_DLL%;."
if exist "%TKINTER_PYD%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%TKINTER_PYD%;."
if exist "%CTYPES_PYD%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%CTYPES_PYD%;."
if exist "%LIBFFI_DLL%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%LIBFFI_DLL%;."
if exist "%LIBFFI_DLL2%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%LIBFFI_DLL2%;."
if exist "%LIBFFI_DLL3%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%LIBFFI_DLL3%;."
if exist "%ZLIB_DLL%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%ZLIB_DLL%;."
if exist "%SQLITE_DLL%" set ADD_BINARIES=!ADD_BINARIES! --add-binary="%SQLITE_DLL%;."

echo Using binary files: !ADD_BINARIES!

pyinstaller ^
    --onefile ^
    --windowed ^
    --noconsole ^
    --clean ^
    --name=HexoPublisher ^
    --add-data="template.md;." ^
    !ADD_BINARIES! ^
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
    main.py

if errorlevel 1 (
    echo Build failed, trying backup solution...
    echo.
    echo Trying solution 2: using --onedir mode...
    
    pyinstaller ^
        --onedir ^
        --windowed ^
        --noconsole ^
        --clean ^
        --name=HexoPublisher ^
        --add-data="template.md;." ^
        !ADD_BINARIES! ^
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
        main.py
    
    if errorlevel 1 (
        echo All build solutions failed
        pause
        exit /b 1
    )
)

echo.
echo Build successful!

echo.
echo Copying necessary files to dist directory...
copy "template.md" "dist\" >nul 2>&1
copy "README.md" "dist\" >nul 2>&1

echo.
echo Testing exe file...
if exist "dist\HexoPublisher.exe" (
    echo exe file exists
    
    REM Get file size
    for %%A in ("dist\HexoPublisher.exe") do (
        set size=%%~zA
        set /a sizeMB=!size!/1024/1024
    )
    echo File size: !sizeMB! MB
    
    echo.
    echo exe file location: dist\HexoPublisher.exe
) else if exist "dist\HexoPublisher\HexoPublisher.exe" (
    echo Found onedir mode exe file
    echo exe file location: dist\HexoPublisher\HexoPublisher.exe
) else (
    echo exe file does not exist
    pause
    exit /b 1
)

echo.
echo Cleaning build temporary files...
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.spec" del /q "*.spec"

echo.
echo Creating portable package...
cd dist
if exist "HexoPublisher.exe" (
    if exist "HexoPublisher_Portable.zip" del "HexoPublisher_Portable.zip"
    powershell -command "Compress-Archive -Path '*.exe','*.md' -DestinationPath 'HexoPublisher_Portable.zip' -Force"
) else if exist "HexoPublisher" (
    if exist "HexoPublisher_Portable.zip" del "HexoPublisher_Portable.zip"
    powershell -command "Compress-Archive -Path 'HexoPublisher','*.md' -DestinationPath 'HexoPublisher_Portable.zip' -Force"
)
cd ..

echo.
echo =======================================
echo    Build and test completed!
echo =======================================
echo.
if exist "dist\HexoPublisher.exe" (
    echo exe file location: dist\HexoPublisher.exe
) else if exist "dist\HexoPublisher\HexoPublisher.exe" (
    echo exe file location: dist\HexoPublisher\HexoPublisher.exe
)
echo Portable package location: dist\HexoPublisher_Portable.zip
echo.
echo Included key DLL files:
echo - tcl86t.dll (tkinter)
echo - tk86t.dll (tkinter)
echo - _tkinter.pyd (tkinter)
echo - _ctypes.pyd (ctypes)
echo - libffi-7.dll or libffi.dll (ctypes dependency)
echo - Other necessary system DLLs
echo.
echo If the program still cannot run, please:
echo 1. Install Visual C++ Redistributable 2015-2022
echo 2. Run as administrator
echo 3. Check Windows version compatibility
echo 4. Try testing on other machines
echo.
echo Press any key to open dist folder...
pause >nul

explorer dist

echo.
echo Build completed!
echo.
pause 