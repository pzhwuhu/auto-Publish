## 🔧 构建exe文件

### 🔧 DLL问题诊断
如果遇到DLL加载问题，请先运行：
```bash
cd tests
python diagnose_dll.py
```
该脚本会：
1. 检测Python环境类型（Anaconda/标准Python）
2. 测试关键模块导入（tkinter, ctypes等）
3. 查找所有必要的DLL文件位置
4. 自动生成适合你环境的构建命令

### 构建exe文件
```bash
build.bat
```
构建脚本已集成终极修复方案，解决所有已知DLL问题，支持Anaconda和标准Python环境。

### 手动构建
```bash
# 安装PyInstaller
pip install pyinstaller

# 构建exe文件
pyinstaller --onefile --windowed --name=HexoPublisher hexo_publisher.py

# exe文件将生成在 dist/HexoPublisher.exe
```


## 🚨 故障排除

| 问题                      | 解决方案                                                                      |
| ------------------------- | ----------------------------------------------------------------------------- |
| tkinter DLL加载失败       | 1. 运行 `cd tests && python diagnose_dll.py` 诊断<br>2. 使用 `build.bat` 构建 |
| _ctypes DLL加载失败       | 使用 `build.bat`，自动包含libffi DLL                                          |
| 软链接创建失败            | 确保程序以管理员身份运行                                                      |
| Hexo命令执行失败          | 检查Hexo是否正确安装，博客根目录是否正确                                      |
| 界面显示异常              | 检查Python版本（需要3.6+）                                                    |
| 配置丢失                  | 检查程序目录下的`config.json`文件是否存在                                     |
| exe文件无法在其他电脑运行 | 安装Visual C++ Redistributable 2015-2022                                      |
| Anaconda环境构建失败      | 使用 `build.bat`，会自动检测环境类型                                          |

## 💡 小贴士

- 第一次使用时记得先配置设置
- 可以使用提供的 `template.md` 作为模板参考
- 分类和标签支持中文，用空格分隔即可
- 程序会记住你的配置，下次使用无需重新设置
- 遇到DLL问题时，先运行 `cd tests && python diagnose_dll.py` 进行诊断
- 推荐使用 `build.bat` 构建脚本，已完全解决所有已知DLL问题

## 📋 安装要求

- Python 3.6+
- Windows 10/11（支持软链接创建）
- 已安装并配置好的Hexo博客环境

