@echo off
chcp 936 >nul
title Clean Build Files

echo ========================================
echo    Clean Hexo Publisher Build Files
echo ========================================
echo.

echo Cleaning following files and directories:
echo - build\ directory (build temp files)
echo - dist\ directory (output files)  
echo - __pycache__\ directory (Python cache)
echo - *.spec files (PyInstaller config)
echo.

set /p confirm=Are you sure to clean these files? (y/N): 
if /i not "%confirm%"=="y" (
    echo Cleaning cancelled
    pause
    exit /b 0
)

echo.
echo Start cleaning...

REM Delete directories
if exist "build" (
    rmdir /s /q "build"
    echo OK: Deleted build\ directory
)

if exist "dist" (
    rmdir /s /q "dist"
    echo OK: Deleted dist\ directory
)

if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo OK: Deleted __pycache__\ directory
)

REM Delete spec files
if exist "*.spec" (
    del /q "*.spec"
    echo OK: Deleted *.spec files
)

REM Delete Python compiled files
for /r %%f in (*.pyc) do (
    if exist "%%f" (
        del /q "%%f"
        echo OK: Deleted %%f
    )
)

echo.
echo ========================================
echo    Cleaning completed!
echo ========================================
echo.
echo All build-related temp files have been cleaned
echo You can now rebuild the exe file
echo.
pause 