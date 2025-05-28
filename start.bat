@echo off
chcp 65001 >nul
title Hexo发布工具

echo ======================================
echo    Hexo博客发布工具 v2.0
echo ======================================
echo.
echo 请选择启动方式:
echo 1. 运行Python程序
echo 2. 运行exe程序
echo 3. 构建exe程序
echo 4. 退出
echo.

set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" (
    echo 启动Python程序...
    python main.py
) else if "%choice%"=="2" (
    if exist "dist\HexoPublisher.exe" (
        echo 启动exe程序...
        cd dist
        HexoPublisher.exe
        cd ..
    ) else (
        echo exe文件不存在，请先构建！
        pause
    )
) else if "%choice%"=="3" (
    echo 开始构建exe程序...
    call build.bat
) else if "%choice%"=="4" (
    echo 再见！
    exit /b 0
) else (
    echo 无效选择！
    pause
)

pause