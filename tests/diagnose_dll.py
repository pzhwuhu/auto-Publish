#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DLL诊断脚本
用于检查Python环境中的关键DLL文件
"""

import sys
import os
import platform
from pathlib import Path

def check_python_info():
    """检查Python基本信息"""
    print("=" * 50)
    print("Python环境信息")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"Python前缀: {sys.prefix}")
    print(f"平台: {platform.platform()}")
    print(f"架构: {platform.architecture()}")
    
    # 检查是否是Anaconda环境
    is_anaconda = 'anaconda' in sys.executable.lower() or 'conda' in sys.executable.lower()
    print(f"Anaconda环境: {'是' if is_anaconda else '否'}")
    print()
    
    return is_anaconda

def check_modules():
    """检查关键模块"""
    print("=" * 50)
    print("模块导入测试")
    print("=" * 50)
    
    modules_to_test = [
        'tkinter',
        '_tkinter', 
        'ctypes',
        '_ctypes',
        'json',
        'os',
        'subprocess',
        'threading'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}: 正常")
        except ImportError as e:
            print(f"❌ {module}: 失败 - {e}")
        except Exception as e:
            print(f"⚠️  {module}: 异常 - {e}")
    print()

def find_dll_files(is_anaconda):
    """查找DLL文件"""
    print("=" * 50)
    print("DLL文件检查")
    print("=" * 50)
    
    python_path = Path(sys.prefix)
    
    if is_anaconda:
        dll_paths = [
            python_path / "Library" / "bin",
            python_path / "DLLs",
            python_path / "Library" / "lib"
        ]
    else:
        dll_paths = [
            python_path / "DLLs",
            python_path / "libs"
        ]
    
    # 要查找的关键DLL文件
    critical_dlls = [
        'tcl86t.dll',
        'tk86t.dll', 
        '_tkinter.pyd',
        '_ctypes.pyd',
        'libffi-7.dll',
        'libffi.dll',
        'zlib.dll',
        'sqlite3.dll'
    ]
    
    found_files = {}
    
    for dll_path in dll_paths:
        if dll_path.exists():
            print(f"检查目录: {dll_path}")
            for dll_name in critical_dlls:
                dll_file = dll_path / dll_name
                if dll_file.exists():
                    found_files[dll_name] = str(dll_file)
                    print(f"  ✅ {dll_name}")
                else:
                    print(f"  ❌ {dll_name}")
        else:
            print(f"目录不存在: {dll_path}")
    
    print()
    print("找到的关键文件:")
    for name, path in found_files.items():
        print(f"  {name}: {path}")
    
    print()
    return found_files

def check_pyinstaller():
    """检查PyInstaller"""
    print("=" * 50)
    print("PyInstaller检查")
    print("=" * 50)
    
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装")
        print("请运行: pip install pyinstaller")
    print()

def generate_build_command(found_files, is_anaconda):
    """生成构建命令"""
    print("=" * 50)
    print("推荐的构建命令")
    print("=" * 50)
    
    # 基础命令
    cmd_parts = [
        "pyinstaller",
        "--onefile",
        "--windowed", 
        "--noconsole",
        "--clean",
        "--name=HexoPublisher",
        "--add-data=\"example_template.md;.\""
    ]
    
    # 添加找到的DLL文件
    for dll_name, dll_path in found_files.items():
        cmd_parts.append(f"--add-binary=\"{dll_path};.\"")
    
    # 添加隐藏导入
    hidden_imports = [
        "tkinter",
        "tkinter.ttk", 
        "tkinter.filedialog",
        "tkinter.messagebox",
        "_tkinter",
        "ctypes",
        "_ctypes",
        "ctypes.wintypes"
    ]
    
    for imp in hidden_imports:
        cmd_parts.append(f"--hidden-import={imp}")
    
    # 添加收集选项
    cmd_parts.extend([
        "--collect-all=tkinter",
        "--collect-all=ctypes"
    ])
    
    # 排除大型模块
    exclude_modules = [
        "matplotlib", "numpy", "pandas", "scipy", 
        "IPython", "jupyter", "notebook", "PIL",
        "cv2", "tensorflow", "torch"
    ]
    
    for mod in exclude_modules:
        cmd_parts.append(f"--exclude-module={mod}")
    
    cmd_parts.extend([
        "--noupx",
        "hexo_publisher.py"
    ])
    
    # 输出命令
    print("完整命令:")
    print(" ^\n    ".join(cmd_parts))
    print()
    
    # 保存到文件
    with open("build_generated.bat", "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("chcp 65001 >nul\n")
        f.write("title 自动生成的构建脚本\n\n")
        f.write("echo 开始构建...\n\n")
        f.write(" ^\n    ".join(cmd_parts))
        f.write("\n\necho 构建完成！\npause\n")
    
    print("✅ 构建脚本已保存到: build_generated.bat")

def main():
    """主函数"""
    print("DLL诊断工具")
    print("用于检查Python环境和生成PyInstaller构建命令")
    print()
    
    # 检查Python信息
    is_anaconda = check_python_info()
    
    # 检查模块
    check_modules()
    
    # 查找DLL文件
    found_files = find_dll_files(is_anaconda)
    
    # 检查PyInstaller
    check_pyinstaller()
    
    # 生成构建命令
    generate_build_command(found_files, is_anaconda)
    
    print("诊断完成！")
    input("按回车键退出...")

if __name__ == "__main__":
    main() 