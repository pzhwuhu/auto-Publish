"""
构建exe文件的脚本
使用PyInstaller将Python程序打包成exe文件
解决tkinter DLL依赖问题
"""

import os
import sys
import subprocess
import shutil
import zipfile

def install_pyinstaller():
    """安装/更新PyInstaller"""
    print("正在安装/更新PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])
        print("✅ PyInstaller安装/更新成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller安装失败")
        return False

def clean_previous_build():
    """清理之前的构建文件"""
    print("清理之前的构建文件...")
    dirs_to_remove = ["build", "dist", "__pycache__"]
    files_to_remove = ["*.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 已删除 {dir_name} 目录")
    
    # 删除spec文件
    import glob
    for spec_file in glob.glob("*.spec"):
        os.remove(spec_file)
        print(f"✅ 已删除 {spec_file}")

def create_icon():
    """创建图标文件（如果需要的话）"""
    # 这里可以添加创建图标的代码
    # 暂时跳过，使用默认图标
    pass

def build_exe():
    """构建exe文件"""
    print("开始构建exe文件...")
    
    # PyInstaller命令参数 - 添加更多参数解决tkinter问题
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个exe文件
        "--windowed",  # 不显示控制台窗口
        "--noconsole",  # 不显示控制台
        "--clean",  # 清理临时文件
        "--name=HexoPublisher",  # exe文件名
        "--add-data=example_template.md;.",  # 包含示例模板文件
        "--hidden-import=tkinter",  # 确保包含tkinter
        "--hidden-import=tkinter.ttk",  # 确保包含ttk
        "--hidden-import=tkinter.filedialog",  # 确保包含filedialog
        "--hidden-import=tkinter.messagebox",  # 确保包含messagebox
        "--collect-all=tkinter",  # 收集所有tkinter相关文件
        "hexo_publisher.py"  # 主程序文件
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ exe文件构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ exe文件构建失败: {e}")
        return False

def create_desktop_shortcut():
    """创建桌面快捷方式"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        # 获取桌面路径
        desktop = winshell.desktop()
        
        # exe文件路径
        exe_path = os.path.join(os.getcwd(), "dist", "HexoPublisher.exe")
        
        if not os.path.exists(exe_path):
            print("❌ 找不到exe文件")
            return False
        
        # 创建快捷方式
        shortcut_path = os.path.join(desktop, "Hexo博客发布工具.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = exe_path
        shortcut.Description = "Hexo博客自动发布工具"
        shortcut.save()
        
        print(f"✅ 桌面快捷方式已创建: {shortcut_path}")
        return True
        
    except ImportError:
        print("⚠️ 需要安装winshell和pywin32来创建桌面快捷方式")
        print("运行: pip install winshell pywin32")
        return False
    except Exception as e:
        print(f"❌ 创建桌面快捷方式失败: {e}")
        return False

def copy_files():
    """复制必要文件到dist目录"""
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        files_to_copy = [
            "example_template.md",
            "README.md"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, dist_dir)
                print(f"✅ 已复制 {file} 到 {dist_dir}")

def clean_build_files():
    """清理构建过程中的临时文件"""
    print("清理构建临时文件...")
    dirs_to_remove = ["build", "__pycache__"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 已删除 {dir_name} 目录")
    
    # 删除spec文件
    import glob
    for spec_file in glob.glob("*.spec"):
        os.remove(spec_file)
        print(f"✅ 已删除 {spec_file}")

def create_portable_package():
    """创建便携包"""
    print("创建便携包...")
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        print("❌ dist目录不存在")
        return False
    
    zip_path = os.path.join(dist_dir, "HexoPublisher_Portable.zip")
    
    # 删除已存在的zip文件
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加exe文件
            exe_file = os.path.join(dist_dir, "HexoPublisher.exe")
            if os.path.exists(exe_file):
                zipf.write(exe_file, "HexoPublisher.exe")
            
            # 添加文档文件
            doc_files = ["README.md", "example_template.md"]
            for doc_file in doc_files:
                doc_path = os.path.join(dist_dir, doc_file)
                if os.path.exists(doc_path):
                    zipf.write(doc_path, doc_file)
        
        print(f"✅ 便携包已创建: {zip_path}")
        return True
    except Exception as e:
        print(f"❌ 创建便携包失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始构建Hexo博客发布工具exe文件")
    print("=" * 50)
    
    # 清理之前的构建文件
    clean_previous_build()
    
    # 检查是否安装了PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
    except ImportError:
        if not install_pyinstaller():
            return
    
    # 更新PyInstaller
    install_pyinstaller()
    
    # 构建exe文件
    if not build_exe():
        return
    
    # 复制文件
    copy_files()
    
    # 清理构建临时文件
    clean_build_files()
    
    # 创建便携包
    create_portable_package()
    
    # 尝试创建桌面快捷方式
    create_desktop_shortcut()
    
    print("=" * 50)
    print("🎉 构建完成！")
    print("📁 exe文件位置: dist/HexoPublisher.exe")
    print("📦 便携包位置: dist/HexoPublisher_Portable.zip")
    print("🧹 已清理构建临时文件")
    print("💡 您可以将dist文件夹复制到任何地方使用")

if __name__ == "__main__":
    main() 