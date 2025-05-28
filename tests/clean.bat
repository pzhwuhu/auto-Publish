@echo off
chcp 65001 >nul
title 清理构建文件

echo ========================================
echo    清理Hexo博客发布工具构建文件
echo ========================================
echo.

echo 正在清理以下文件和目录：
echo - build\ 目录（构建临时文件）
echo - dist\ 目录（输出文件）
echo - __pycache__\ 目录（Python缓存）
echo - *.spec 文件（PyInstaller配置）
echo.

set /p confirm=确定要清理这些文件吗？(y/N): 
if /i not "%confirm%"=="y" (
    echo 取消清理操作
    pause
    exit /b 0
)

echo.
echo 开始清理...

REM 删除目录
if exist "build" (
    rmdir /s /q "build"
    echo ✅ 已删除 build\ 目录
)

if exist "dist" (
    rmdir /s /q "dist"
    echo ✅ 已删除 dist\ 目录
)

if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo ✅ 已删除 __pycache__\ 目录
)

REM 删除spec文件
for %%f in (*.spec) do (
    if exist "%%f" (
        del /q "%%f"
        echo ✅ 已删除 %%f
    )
)

REM 删除Python编译文件
for /r %%f in (*.pyc) do (
    if exist "%%f" (
        del /q "%%f"
        echo ✅ 已删除 %%f
    )
)

echo.
echo ========================================
echo    清理完成！
echo ========================================
echo.
echo 已清理所有构建相关的临时文件
echo 现在可以重新构建exe文件了
echo.
pause 