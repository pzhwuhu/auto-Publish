import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import subprocess
import datetime
import re
from pathlib import Path
import ctypes
import sys

class HexoPublisher:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexo博客自动发布工具 v2.0")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # 配置文件路径
        self.config_file = "config.json"
        self.config = self.load_config()
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置到界面
        self.load_config_to_ui()
        
        # 设置窗口图标和居中
        self.center_window()
    

    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):
        """设置界面样式"""
        try:
            style = ttk.Style()
            # 使用默认主题，避免兼容性问题
            available_themes = style.theme_names()
            if 'clam' in available_themes:
                style.theme_use('clam')
            elif 'alt' in available_themes:
                style.theme_use('alt')
            else:
                style.theme_use(available_themes[0])
            
            # 简化样式配置，避免过度自定义
            try:
                style.configure('Title.TLabel', font=('Microsoft YaHei', 20, 'bold'))
                style.configure('Heading.TLabel', font=('Microsoft YaHei', 14, 'bold'))
                style.configure('Custom.TButton', font=('Microsoft YaHei', 10))
                style.configure('Custom.TEntry', font=('Microsoft YaHei', 10))
                style.configure('Custom.TLabel', font=('Microsoft YaHei', 11))
                style.configure('Custom.TCheckbutton', font=('Microsoft YaHei', 11))
            except Exception as e:
                # 如果字体设置失败，使用默认字体
                print(f"字体设置失败，使用默认字体: {e}")
                style.configure('Title.TLabel', font=('Arial', 20, 'bold'))
                style.configure('Heading.TLabel', font=('Arial', 14, 'bold'))
                style.configure('Custom.TButton', font=('Arial', 10))
                style.configure('Custom.TEntry', font=('Arial', 10))
                style.configure('Custom.TLabel', font=('Arial', 11))
                style.configure('Custom.TCheckbutton', font=('Arial', 11))
                
        except Exception as e:
            print(f"样式设置失败，使用默认样式: {e}")
            # 如果样式设置完全失败，就不设置任何自定义样式
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="30", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题栏
        title_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 30))
        
        # 标题和设置按钮
        title_label = ttk.Label(title_frame, text="📝 Hexo博客自动发布工具", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        settings_btn = ttk.Button(title_frame, text="⚙️ 设置", command=self.open_settings, 
                                 style='Custom.TButton', width=10)
        settings_btn.pack(side=tk.RIGHT)
        
        # 主要功能区域
        main_func_frame = ttk.LabelFrame(main_frame, text="📄 发布设置", padding="20")
        main_func_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # 源笔记文件选择
        ttk.Label(main_func_frame, text="源笔记文件:", style='Custom.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        self.source_file_var = tk.StringVar()
        self.source_file_entry = ttk.Entry(main_func_frame, textvariable=self.source_file_var, 
                                          width=50, style='Custom.TEntry')
        self.source_file_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(main_func_frame, text="📁 浏览", command=self.browse_source_file, 
                  style='Custom.TButton').grid(row=0, column=2, padx=5, pady=10)
        
        # 文章标题
        ttk.Label(main_func_frame, text="文章标题:", style='Custom.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(main_func_frame, textvariable=self.title_var, 
                                    width=50, style='Custom.TEntry')
        self.title_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(main_func_frame, text="📝 使用文件名", command=self.use_filename_as_title, 
                  style='Custom.TButton').grid(row=1, column=2, padx=5, pady=10)
        
        # 分类
        ttk.Label(main_func_frame, text="分类 (categories):", style='Custom.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        self.categories_var = tk.StringVar()
        self.categories_entry = ttk.Entry(main_func_frame, textvariable=self.categories_var, 
                                         width=50, style='Custom.TEntry')
        self.categories_entry.grid(row=2, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Label(main_func_frame, text="💡 用空格分隔", style='Custom.TLabel', 
                 font=('Microsoft YaHei', 9)).grid(row=2, column=2, padx=5, pady=10)
        
        # 标签
        ttk.Label(main_func_frame, text="标签 (tags):", style='Custom.TLabel').grid(
            row=3, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        self.tags_var = tk.StringVar()
        self.tags_entry = ttk.Entry(main_func_frame, textvariable=self.tags_var, 
                                   width=50, style='Custom.TEntry')
        self.tags_entry.grid(row=3, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Label(main_func_frame, text="💡 用空格分隔", style='Custom.TLabel', 
                 font=('Microsoft YaHei', 9)).grid(row=3, column=2, padx=5, pady=10)
        
        # 是否发布选项
        publish_frame = ttk.Frame(main_func_frame, style='Custom.TFrame')
        publish_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.publish_var = tk.BooleanVar()
        self.publish_check = ttk.Checkbutton(publish_frame, 
                                           text="🚀 发布到博客 (执行 hexo g && hexo d)", 
                                           variable=self.publish_var,
                                           style='Custom.TCheckbutton')
        self.publish_check.pack()
        
        # 执行按钮
        execute_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        execute_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        self.execute_btn = ttk.Button(execute_frame, text="🚀 执行发布", 
                                     command=self.execute_publish, style='Custom.TButton')
        self.execute_btn.configure(width=25)
        self.execute_btn.pack()
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="📊 执行结果", padding="15")
        result_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         pady=(0, 10))
        
        # 创建文本框和滚动条
        text_frame = ttk.Frame(result_frame, style='Custom.TFrame')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=12, wrap=tk.WORD, 
                                  font=('Consolas', 10), bg='#2c3e50', fg='#ecf0f1',
                                  insertbackground='#ecf0f1', selectbackground='#3498db')
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_func_frame.columnconfigure(1, weight=1)
        
        # 添加欢迎信息
        self.log_result("🎉 欢迎使用Hexo博客自动发布工具！")
        self.log_result("✅ 管理员权限已获取")
        if self.config.get("posts_dir") and self.config.get("blog_root"):
            self.log_result("✅ 配置已加载")
        else:
            self.log_result("⚠️ 请先在设置中配置博客目录")
    
    def open_settings(self):
        """打开设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ 设置")
        settings_window.geometry("600x400")
        settings_window.configure(bg='#34495e')
        settings_window.resizable(False, False)
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 居中显示
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (400 // 2)
        settings_window.geometry(f"600x400+{x}+{y}")
        
        # 设置窗口内容
        main_frame = ttk.Frame(settings_window, padding="30", style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="⚙️ 博客配置设置", 
                               font=('Microsoft YaHei', 16, 'bold'),
                               foreground='#3498db', background='#34495e')
        title_label.pack(pady=(0, 20))
        
        # 配置项
        config_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        config_frame.pack(fill=tk.BOTH, expand=True)
        
        # 博客文章目录
        ttk.Label(config_frame, text="📁 博客文章目录:", style='Custom.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        posts_dir_var = tk.StringVar(value=self.config.get("posts_dir", ""))
        posts_dir_entry = ttk.Entry(config_frame, textvariable=posts_dir_var, 
                                   width=40, style='Custom.TEntry')
        posts_dir_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", 
                  command=lambda: self.browse_directory(posts_dir_var, "选择博客文章目录"), 
                  style='Custom.TButton').grid(row=0, column=2, padx=5, pady=10)
        
        # 博客根目录
        ttk.Label(config_frame, text="🏠 博客根目录:", style='Custom.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        blog_root_var = tk.StringVar(value=self.config.get("blog_root", ""))
        blog_root_entry = ttk.Entry(config_frame, textvariable=blog_root_var, 
                                   width=40, style='Custom.TEntry')
        blog_root_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", 
                  command=lambda: self.browse_directory(blog_root_var, "选择博客根目录"), 
                  style='Custom.TButton').grid(row=1, column=2, padx=5, pady=10)
        
        # 模板文件
        ttk.Label(config_frame, text="📄 模板文件:", style='Custom.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        template_file_var = tk.StringVar(value=self.config.get("template_file", ""))
        template_file_entry = ttk.Entry(config_frame, textvariable=template_file_var, 
                                       width=40, style='Custom.TEntry')
        template_file_entry.grid(row=2, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", 
                  command=lambda: self.browse_file(template_file_var, "选择模板文件"), 
                  style='Custom.TButton').grid(row=2, column=2, padx=5, pady=10)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.pack(pady=20)
        
        def save_settings():
            self.config = {
                "posts_dir": posts_dir_var.get(),
                "blog_root": blog_root_var.get(),
                "template_file": template_file_var.get()
            }
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
                self.log_result("✅ 配置保存成功！")
                settings_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"保存配置失败: {str(e)}")
        
        ttk.Button(button_frame, text="💾 保存", command=save_settings, 
                  style='Custom.TButton', width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ 取消", command=settings_window.destroy, 
                  style='Custom.TButton', width=15).pack(side=tk.LEFT, padx=10)
        
        # 配置网格权重
        config_frame.columnconfigure(1, weight=1)
    
    def browse_directory(self, var, title):
        """浏览目录"""
        directory = filedialog.askdirectory(title=title)
        if directory:
            var.set(directory)
    
    def browse_file(self, var, title):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if file_path:
            var.set(file_path)
    
    def load_config(self):
        """加载配置文件"""
        default_config = {
            "posts_dir": "",
            "blog_root": "",
            "template_file": ""
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_config
        return default_config
    
    def load_config_to_ui(self):
        """将配置加载到界面"""
        # 配置已在设置窗口中处理，这里不需要显示
        pass
    
    def browse_source_file(self):
        """浏览源笔记文件"""
        file_path = filedialog.askopenfilename(
            title="选择源笔记文件",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if file_path:
            self.source_file_var.set(file_path)
            # 自动设置标题为文件名（不含扩展名）
            filename = os.path.splitext(os.path.basename(file_path))[0]
            self.title_var.set(filename)
            self.log_result(f"📁 已选择源文件: {os.path.basename(file_path)}")
    
    def use_filename_as_title(self):
        """使用文件名作为标题"""
        source_file = self.source_file_var.get()
        if source_file:
            filename = os.path.splitext(os.path.basename(source_file))[0]
            self.title_var.set(filename)
            self.log_result(f"📝 标题已设置为: {filename}")
        else:
            messagebox.showwarning("警告", "请先选择源笔记文件")
    
    def log_result(self, message):
        """记录结果到文本框"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.result_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def parse_tags_categories(self, text):
        """解析标签和分类字符串"""
        if not text.strip():
            return []
        # 按空格分割，过滤空字符串
        items = [item.strip() for item in text.split() if item.strip()]
        return items
    
    def create_symlink(self, source, target):
        """创建软链接"""
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(target), exist_ok=True)
            
            # 如果目标文件已存在，先删除
            if os.path.exists(target):
                os.remove(target)
            
            # 在Windows上创建软链接
            if os.name == 'nt':
                # 使用mklink命令创建软链接
                cmd = f'mklink "{target}" "{source}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    return True, "软链接创建成功"
                else:
                    return False, f"软链接创建失败: {result.stderr}"
            else:
                # Unix/Linux系统
                os.symlink(source, target)
                return True, "软链接创建成功"
        except Exception as e:
            return False, f"软链接创建失败: {str(e)}"
    
    def generate_front_matter(self, title, categories, tags):
        """生成Front Matter"""
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        front_matter = f"---\ntitle: {title}\ndate: {date_str}\n"
        
        # 添加分类
        if categories:
            if len(categories) == 1:
                front_matter += f"categories: {categories[0]}\n"
            else:
                front_matter += "categories:\n"
                for cat in categories:
                    front_matter += f"- {cat}\n"
        
        # 添加标签
        if tags:
            front_matter += "tags:\n"
            for tag in tags:
                front_matter += f"- {tag}\n"
        
        front_matter += "---\n\n"
        return front_matter
    
    def execute_hexo_commands(self, blog_root):
        """执行hexo命令"""
        try:
            # 切换到博客根目录
            original_dir = os.getcwd()
            os.chdir(blog_root)
            
            self.log_result("🔄 开始执行 hexo generate...")
            
            # 执行 hexo g
            result_g = subprocess.run(['hexo', 'g'], capture_output=True, text=True, shell=True)
            if result_g.returncode != 0:
                self.log_result(f"❌ hexo generate 失败: {result_g.stderr}")
                return False
            
            self.log_result("✅ hexo generate 完成")
            self.log_result("🚀 开始执行 hexo deploy...")
            
            # 执行 hexo d
            result_d = subprocess.run(['hexo', 'd'], capture_output=True, text=True, shell=True)
            if result_d.returncode != 0:
                self.log_result(f"❌ hexo deploy 失败: {result_d.stderr}")
                return False
            
            self.log_result("✅ hexo deploy 完成")
            return True
            
        except Exception as e:
            self.log_result(f"❌ 执行hexo命令失败: {str(e)}")
            return False
        finally:
            # 恢复原目录
            os.chdir(original_dir)
    
    def validate_inputs(self):
        """验证输入"""
        if not self.config.get("posts_dir"):
            messagebox.showerror("错误", "请在设置中配置博客文章目录")
            return False
        
        if not self.config.get("blog_root"):
            messagebox.showerror("错误", "请在设置中配置博客根目录")
            return False
        
        if not self.source_file_var.get():
            messagebox.showerror("错误", "请选择源笔记文件")
            return False
        
        if not self.title_var.get():
            messagebox.showerror("错误", "请输入文章标题")
            return False
        
        if not os.path.exists(self.source_file_var.get()):
            messagebox.showerror("错误", "源笔记文件不存在")
            return False
        
        if not os.path.exists(self.config.get("posts_dir")):
            messagebox.showerror("错误", "博客文章目录不存在")
            return False
        
        if not os.path.exists(self.config.get("blog_root")):
            messagebox.showerror("错误", "博客根目录不存在")
            return False
        
        return True
    
    def execute_publish(self):
        """执行发布"""
        # 验证输入
        if not self.validate_inputs():
            return
        
        # 清空结果显示
        self.result_text.delete(1.0, tk.END)
        
        # 禁用执行按钮
        self.execute_btn.configure(state='disabled')
        
        try:
            source_file = self.source_file_var.get()
            title = self.title_var.get()
            posts_dir = self.config.get("posts_dir")
            blog_root = self.config.get("blog_root")
            
            # 解析分类和标签
            categories = self.parse_tags_categories(self.categories_var.get())
            tags = self.parse_tags_categories(self.tags_var.get())
            
            self.log_result("🚀 开始执行发布流程...")
            self.log_result(f"📄 文章标题: {title}")
            if categories:
                self.log_result(f"📂 分类: {', '.join(categories)}")
            if tags:
                self.log_result(f"🏷️ 标签: {', '.join(tags)}")
            
            # 生成目标文件路径
            target_file = os.path.join(posts_dir, f"{title}.md")
            
            self.log_result(f"📁 源文件: {source_file}")
            self.log_result(f"📁 目标文件: {target_file}")
            
            # 创建软链接
            self.log_result("🔗 正在创建软链接...")
            success, message = self.create_symlink(source_file, target_file)
            
            if not success:
                self.log_result(f"❌ 软链接创建失败: {message}")
                messagebox.showerror("错误", f"软链接创建失败: {message}")
                return
            
            self.log_result("✅ 软链接创建成功")
            
            # 如果选择发布
            if self.publish_var.get():
                self.log_result("🌐 开始发布到博客...")
                if self.execute_hexo_commands(blog_root):
                    self.log_result("🎉 博客发布成功！")
                    messagebox.showinfo("成功", "🎉 博客发布成功！")
                else:
                    self.log_result("❌ 博客发布失败")
                    messagebox.showerror("错误", "博客发布失败，请查看详细信息")
            else:
                self.log_result("⏭️ 跳过博客发布")
                messagebox.showinfo("成功", "✅ 软链接创建成功！")
            
            self.log_result("✅ 发布流程完成")
            
        except Exception as e:
            error_msg = f"执行过程中发生错误: {str(e)}"
            self.log_result(f"❌ {error_msg}")
            messagebox.showerror("错误", error_msg)
        
        finally:
            # 重新启用执行按钮
            self.execute_btn.configure(state='normal')

def main():
    root = tk.Tk()
    app = HexoPublisher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 