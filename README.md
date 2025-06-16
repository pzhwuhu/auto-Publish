# 🚀 Hexo博客自动发布工具 v2.0

一款用Python开发的GUI工具，用于将Markdown笔记软链接为Hexo博客文章并发布。

![](https://cdn.jsdelivr.net/gh/pzhwuhu/Image-Hosting/Posts%20insert/PixPin_2025-05-28_09-36-17.png)

## 📁 项目结构

```
auto-Publish/
├── main.py                 # 主程序文件
├── template.md             # 博客文章模板
├── config.json             # 配置文件
├── requirements.txt        # Python依赖
├── build.bat              # 构建exe可执行文件
├── clean.bat              # 清理构建文件
├── run.bat                # 启动程序
├── README.md              # 说明文档
└── tests/                 # 测试文件夹
    ├── diagnose_dll.py    # DLL诊断工具
    └── ...                # 其他测试文件
```

## 🎯 主要功能

- **配置管理**：一次配置，永久保存博客目录和模板设置
- **文件选择**：直观的文件浏览器选择源笔记文件
- **标题自定义**：支持自定义文章标题或默认使用文件名
- **分类标签**：支持添加文章分类(categories)和标签(tags)
- **智能Front Matter处理**：直接在源文件开头添加YAML元数据
- **软链接创建**：自动获取管理员权限，在博客目录创建指向源文件的软链接
- **一键发布**：可选择是否执行`hexo g && hexo d`命令发布博客
- **exe程序**：可打包成独立的exe文件，无需Python环境

## 🔄 工作流程

1. **选择源笔记文件** → 2. **添加Front Matter到源文件** → 3. **创建软链接到博客目录** → 4. **可选发布博客**

这样的好处是：
- 源笔记文件本身包含博客元数据，便于管理
- 博客目录中只是**软链接**，节省空间
- 修改源文件内容会**自动同步**到博客

## 🎨 界面特色

- 中文界面，操作简单直观
- 实时执行结果显示，带emoji图标
- 响应式布局，支持窗口缩放
- 独立的设置窗口，配置更清晰
- 自动管理员权限提升

## 📦 快速开始

### 🚀 一键启动（推荐）
```bash
start.bat
```
启动脚本会提供菜单选择：
- 运行Python程序
- 运行exe程序
- 构建exe程序

### 方式一：使用exe文件
如果已有exe文件，直接运行：
```bash
dist\HexoPublisher.exe
```

如需构建exe文件：
```bash
build.bat
```
构建脚本已解决已知的DLL问题，支持Anaconda和标准Python环境。

### 方式二：运行Python程序
```bash
python main.py
```

## ⚙️ 首次配置

1. 点击程序右上角的 **"⚙️ 设置"** 按钮
2. 配置以下路径：
   - **📁 博客文章目录**：你的Hexo博客的 `source/_posts` 目录
   - **🏠 博客根目录**：你的Hexo博客根目录
   - **📄 模板文件**：选择 `scaffolds/post.md` 或使用提供的 `template.md`
3. 点击 **"💾 保存"** 按钮

## 📝 发布文章

1. **选择源文件**：点击 **"📁 浏览"** 选择你的Markdown笔记文件
2. **设置标题**：输入文章标题，或点击 **"📝 使用文件名"**
3. **添加分类**：在分类框中输入分类，用空格分隔（如：`技术 编程`）
4. **添加标签**：在标签框中输入标签，用空格分隔（如：`Python Hexo 博客`）
5. **选择发布**：勾选 **"🚀 发布到博客"** 如果要立即发布
6. **执行**：点击 **"🚀 添加Front Matter并创建链接"** 按钮

程序会：
- 在源文件开头添加Front Matter（如果已存在会询问是否替换）
- 在博客目录创建软链接指向源文件
- 可选执行hexo发布命令

## 📋 使用示例

假设你要发布一篇关于Python的文章：

- **源笔记文件**：`D:\notes\Python学习笔记.md`
- **文章标题**：`Python基础语法详解`
- **分类**：`编程 教程`
- **标签**：`Python 基础 语法 编程`

**执行过程：**

1. **原始文件**：`D:\notes\Python学习笔记.md`
   ```markdown
   # Python学习笔记
   
   Python是一种高级编程语言...
   ```

2. **添加Front Matter后**：
   ```yaml
   ---
   title: Python基础语法详解
   date: 2024-01-15 14:30:00
   categories:
   - 编程
   - 教程
   tags:
   - Python
   - 基础
   - 语法
   - 编程
   ---
   
   # Python学习笔记
   
   Python是一种高级编程语言...
   ```

3. **在博客目录创建软链接**：
   - `D:\myblog\source\_posts\Python基础语法详解.md` → `D:\notes\Python学习笔记.md`

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

## 📁 文件结构

```
auto-Publish/
├── main.py               # 主程序文件
├── hexo_publisher.py     # 原版程序文件（备用）
├── template.md          # 博客文章模板
├── build.bat            # 构建可执行文件脚本
├── clean.bat            # 清理构建文件脚本
├── run.bat              # 启动程序脚本
├── requirements.txt     # Python依赖列表
├── README.md           # 说明文档（本文件）
├── config.json         # 配置文件（运行后自动生成）
├── tests/              # 测试文件夹
│   ├── diagnose_dll.py # DLL诊断工具
│   └── ...             # 其他测试文件
└── dist/               # 构建后的exe文件目录
    ├── HexoPublisher.exe
    └── HexoPublisher_Portable.zip
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

## 🔧 技术实现

- **GUI框架**：tkinter + ttk
- **配置管理**：JSON格式存储
- **软链接**：Windows mklink命令
- **进程管理**：subprocess模块
- **权限检测**：ctypes.windll.shell32

## 📋 安装要求

- Python 3.6+
- Windows 10/11（支持软链接创建）
- 已安装并配置好的Hexo博客环境

## 🔄 更新日志

### v2.0.0
- 🎨 ~~全新深色主题界面设计~~(TODO)
- ✨ 添加分类和标签输入功能
- 🔧 独立的设置窗口
- 🛡️ 自动管理员权限获取
- 📦 支持打包成exe文件
- 🎯 优化用户体验和界面布局
- 🔧 解决Anaconda环境下的构建问题

### v1.0.0
- 初始版本发布
- 实现基本的GUI界面
- 支持配置管理和软链接创建
- 集成Hexo发布功能

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具！

---

🎉 **享受便捷的博客发布体验吧！**
