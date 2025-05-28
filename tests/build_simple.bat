@echo off
chcp 65001 >nul
title 构建Hexo博客发布工具

echo ========================================
echo    构建Hexo博客发布工具exe文件
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

echo 正在安装/更新PyInstaller...
pip install --upgrade pyinstaller

echo.
echo 清理之前的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo.
echo 开始构建exe文件...
echo.

REM 构建exe文件 - 添加更多参数解决tkinter问题
pyinstaller ^
    --onefile ^
    --windowed ^
    --name=HexoPublisher ^
    --add-data="example_template.md;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --collect-all=tkinter ^
    --noconsole ^
    --clean ^
    hexo_publisher.py

if errorlevel 1 (
    echo.
    echo 构建失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo 复制必要文件到dist目录...
copy "example_template.md" "dist\" >nul 2>&1
copy "README.md" "dist\" >nul 2>&1

echo.
echo 清理构建过程中的临时文件...
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.spec" del /q "*.spec"

echo.
echo 创建发布包...
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
echo 已清理的文件：
echo - build\ 目录（构建临时文件）
echo - __pycache__\ 目录（Python缓存）
echo - *.spec 文件（PyInstaller配置）
echo.
echo 按任意键打开dist文件夹...
pause >nul

explorer dist

echo.
echo 构建完成！您可以：
echo 1. 直接运行 dist\HexoPublisher.exe
echo 2. 使用 dist\HexoPublisher_Portable.zip 便携包
echo 3. 创建桌面快捷方式指向exe文件
echo 4. 将dist文件夹复制到其他电脑使用
echo.
pause 