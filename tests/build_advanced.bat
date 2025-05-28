@echo off
chcp 65001 >nul
title 高级构建Hexo博客发布工具

echo ========================================
echo    高级构建Hexo博客发布工具exe文件
echo    (解决tkinter DLL依赖问题)
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

echo 检测Python安装路径...
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_EXE=%%i
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.prefix)"') do set PYTHON_PATH=%%i
echo Python可执行文件: %PYTHON_EXE%
echo Python安装目录: %PYTHON_PATH%

echo.
echo 检测Python环境类型...
python -c "import sys; print('Anaconda' if 'anaconda' in sys.executable.lower() or 'conda' in sys.executable.lower() else 'Standard')" > temp_env.txt
set /p PYTHON_ENV=<temp_env.txt
del temp_env.txt
echo Python环境: %PYTHON_ENV%

echo.
echo 正在安装/更新必要的包...
pip install --upgrade pyinstaller
pip install --upgrade setuptools
pip install --upgrade wheel

echo.
echo 清理之前的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo 开始高级构建exe文件...
echo 使用参数解决tkinter DLL依赖问题...
echo.

REM 检查DLL文件是否存在
set DLL_FOUND=0
if exist "%PYTHON_PATH%\DLLs\tcl86t.dll" set DLL_FOUND=1
if exist "%PYTHON_PATH%\Library\bin\tcl86t.dll" set DLL_FOUND=1

if %DLL_FOUND%==1 (
    echo 找到tkinter DLL文件，使用高级构建...
    
    REM 高级构建命令 - 根据环境类型选择DLL路径
    if "%PYTHON_ENV%"=="Anaconda" (
        echo 使用Anaconda环境构建...
        pyinstaller ^
            --onefile ^
            --windowed ^
            --noconsole ^
            --clean ^
            --name=HexoPublisher ^
            --add-data="example_template.md;." ^
            --hidden-import=tkinter ^
            --hidden-import=tkinter.ttk ^
            --hidden-import=tkinter.filedialog ^
            --hidden-import=tkinter.messagebox ^
            --hidden-import=tkinter.simpledialog ^
            --collect-all=tkinter ^
            --collect-binaries=tkinter ^
            --collect-data=tkinter ^
            --exclude-module=matplotlib ^
            --exclude-module=numpy ^
            --exclude-module=pandas ^
            --exclude-module=scipy ^
            --exclude-module=IPython ^
            --exclude-module=jupyter ^
            --optimize=2 ^
            hexo_publisher.py
    ) else (
        echo 使用标准Python环境构建...
        pyinstaller ^
            --onefile ^
            --windowed ^
            --noconsole ^
            --clean ^
            --name=HexoPublisher ^
            --add-data="example_template.md;." ^
            --hidden-import=tkinter ^
            --hidden-import=tkinter.ttk ^
            --hidden-import=tkinter.filedialog ^
            --hidden-import=tkinter.messagebox ^
            --hidden-import=tkinter.simpledialog ^
            --collect-all=tkinter ^
            --collect-binaries=tkinter ^
            --collect-data=tkinter ^
            --add-binary="%PYTHON_PATH%\DLLs\tcl86t.dll;." ^
            --add-binary="%PYTHON_PATH%\DLLs\tk86t.dll;." ^
            --exclude-module=matplotlib ^
            --exclude-module=numpy ^
            --exclude-module=pandas ^
            --exclude-module=scipy ^
            --optimize=2 ^
            hexo_publisher.py
    )
) else (
    echo 未找到tkinter DLL文件，使用基础构建...
    pyinstaller ^
        --onefile ^
        --windowed ^
        --name=HexoPublisher ^
        --add-data="example_template.md;." ^
        --hidden-import=tkinter ^
        --hidden-import=tkinter.ttk ^
        --collect-all=tkinter ^
        hexo_publisher.py
)

if errorlevel 1 (
    echo.
    echo 高级构建失败，尝试最简构建...
    echo.
    
    REM 最简构建作为备选方案
    pyinstaller ^
        --onefile ^
        --windowed ^
        --name=HexoPublisher ^
        --hidden-import=tkinter ^
        --hidden-import=tkinter.ttk ^
        hexo_publisher.py
    
    if errorlevel 1 (
        echo.
        echo 构建失败，请检查错误信息
        echo.
        echo 可能的解决方案：
        echo 1. 重新安装Python（确保包含tkinter）
        echo 2. 使用conda环境：conda install tk
        echo 3. 检查Python版本是否支持tkinter
        echo 4. 尝试在虚拟环境中构建
        pause
        exit /b 1
    )
)

echo.
echo exe文件构建成功！

echo.
echo 复制必要文件到dist目录...
copy "example_template.md" "dist\" >nul 2>&1
copy "README.md" "dist\" >nul 2>&1

echo.
echo 测试exe文件...
if exist "dist\HexoPublisher.exe" (
    echo exe文件存在
    
    REM 获取文件大小
    for %%A in ("dist\HexoPublisher.exe") do (
        set size=%%~zA
        set /a sizeMB=!size!/1024/1024
    )
    setlocal enabledelayedexpansion
    echo 文件大小: !sizeMB! MB
    endlocal
) else (
    echo exe文件不存在
)

echo.
echo 清理构建临时文件...
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.spec" del /q "*.spec"

echo.
echo 创建便携包...
cd dist
if exist "HexoPublisher_Portable.zip" del "HexoPublisher_Portable.zip"
powershell -command "Compress-Archive -Path '*.exe','*.md' -DestinationPath 'HexoPublisher_Portable.zip'"
cd ..

echo.
echo ========================================
echo    构建完成！
echo ========================================
echo.
echo exe文件位置: dist\HexoPublisher.exe
echo 便携包位置: dist\HexoPublisher_Portable.zip
echo.
echo 已应用的优化：
echo - 自动检测Python环境类型
echo - 排除了大型科学计算库
echo - 针对%PYTHON_ENV%环境优化
echo - 自动处理tkinter依赖
echo.
echo 如果仍有问题，请尝试：
echo 1. 在目标机器上安装Visual C++ Redistributable
echo 2. 确保目标机器有.NET Framework
echo 3. 以管理员身份运行exe文件
echo.
echo 按任意键打开dist文件夹...
pause >nul

explorer dist

echo.
echo 构建完成！您可以：
echo 1. 直接运行 dist\HexoPublisher.exe
echo 2. 使用 dist\HexoPublisher_Portable.zip 便携包
echo 3. 将dist文件夹复制到其他电脑使用
echo.
pause 