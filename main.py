#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hexo博客自动发布工具 - 版本3.0
支持两种模式：模式1（原有功能）和模式2（批量处理，不插入模板）
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import subprocess
import threading
from datetime import datetime
import ctypes
import sys

class HexoPublisher:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Hexo博客自动发布工具 v3.0")
        self.root.geometry("900x750")
        self.root.configure(bg='#f0f0f0')
        
        # 配置文件路径
        self.config_file = "config.json"
        self.config = {}
        
        # 当前模式：1=原有功能，2=批量处理
        self.current_mode = tk.IntVar(value=1)
        
        # 源文件列表（模式2使用）
        self.source_files = []
        
        # 加载配置
        self.load_config()
        
        # 居中窗口
        self.center_window()
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置到界面
        self.load_config_to_ui()
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题栏
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # 标题和设置按钮
        title_label = ttk.Label(title_frame, text="📝 Hexo博客自动发布工具 v3.0", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        settings_btn = ttk.Button(title_frame, text="⚙️ 设置", command=self.open_settings, 
                                 width=10)
        settings_btn.pack(side=tk.RIGHT)
        
        # 模式切换区域
        mode_frame = ttk.LabelFrame(main_frame, text="🔄 工作模式", padding="15")
        mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 模式选择
        mode1_radio = ttk.Radiobutton(mode_frame, text="📝 模式1: 添加Front Matter并创建软链接", 
                                     variable=self.current_mode, value=1, 
                                     command=self.on_mode_change)
        mode1_radio.pack(anchor=tk.W, pady=5)
        
        mode2_radio = ttk.Radiobutton(mode_frame, text="📦 模式2: 批量处理，直接创建软链接", 
                                     variable=self.current_mode, value=2, 
                                     command=self.on_mode_change)
        mode2_radio.pack(anchor=tk.W, pady=5)
        
        # 主要功能区域
        self.main_func_frame = ttk.LabelFrame(main_frame, text="📄 发布设置", padding="15")
        self.main_func_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 创建模式1的界面组件
        self.create_mode1_widgets()
        
        # 创建模式2的界面组件
        self.create_mode2_widgets()
        
        # 是否发布选项（将在模式切换时动态创建）
        self.publish_var = tk.BooleanVar()
        
        # 执行按钮
        execute_frame = ttk.Frame(main_frame)
        execute_frame.grid(row=3, column=0, columnspan=3, pady=15)
        
        self.execute_btn = ttk.Button(execute_frame, text="🚀 开始执行", 
                                     command=self.execute_publish, width=25)
        self.execute_btn.pack()
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="📊 执行结果", padding="10")
        result_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         pady=(0, 10))
        
        # 创建文本框和滚动条
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=12, wrap=tk.WORD, 
                                  font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        self.main_func_frame.columnconfigure(1, weight=1)
        
        # 初始化界面状态
        self.on_mode_change()
        
        # 添加欢迎信息
        self.log_result("🎉 欢迎使用Hexo博客自动发布工具 v3.0！")
        self.log_result("✅ 管理员权限已获取")
        self.log_result("🔄 支持两种工作模式，请在上方选择")
        if self.config.get("posts_dir") and self.config.get("blog_root"):
            self.log_result("✅ 配置已加载")
        else:
            self.log_result("⚠️ 请先在设置中配置博客目录")
    
    def create_mode1_widgets(self):
        """创建模式1的界面组件"""
        # 源笔记文件选择
        ttk.Label(self.main_func_frame, text="源笔记文件:").grid(
            row=0, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.source_file_var = tk.StringVar()
        self.source_file_entry = ttk.Entry(self.main_func_frame, textvariable=self.source_file_var, 
                                          width=50)
        self.source_file_entry.grid(row=0, column=1, padx=(0, 10), pady=8, sticky=(tk.W, tk.E))
        ttk.Button(self.main_func_frame, text="📁 浏览", command=self.browse_source_file).grid(
            row=0, column=2, padx=5, pady=8)
        
        # 文章标题
        ttk.Label(self.main_func_frame, text="文章标题:").grid(
            row=1, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.main_func_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=1, column=1, padx=(0, 10), pady=8, sticky=(tk.W, tk.E))
        ttk.Button(self.main_func_frame, text="📝 使用文件名", command=self.use_filename_as_title).grid(
            row=1, column=2, padx=5, pady=8)
        
        # 分类
        ttk.Label(self.main_func_frame, text="分类 (categories):").grid(
            row=2, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.categories_var = tk.StringVar()
        self.categories_entry = ttk.Entry(self.main_func_frame, textvariable=self.categories_var, 
                                         width=50)
        self.categories_entry.grid(row=2, column=1, padx=(0, 10), pady=8, sticky=(tk.W, tk.E))
        ttk.Label(self.main_func_frame, text="💡 用空格分隔").grid(row=2, column=2, padx=5, pady=8)
        
        # 标签
        ttk.Label(self.main_func_frame, text="标签 (tags):").grid(
            row=3, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.tags_var = tk.StringVar()
        self.tags_entry = ttk.Entry(self.main_func_frame, textvariable=self.tags_var, width=50)
        self.tags_entry.grid(row=3, column=1, padx=(0, 10), pady=8, sticky=(tk.W, tk.E))
        ttk.Label(self.main_func_frame, text="💡 用空格分隔").grid(row=3, column=2, padx=5, pady=8)
    
    def create_mode2_widgets(self):
        """创建模式2的界面组件"""
        # 源文件列表
        ttk.Label(self.main_func_frame, text="源文件列表:").grid(
            row=0, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        
        # 文件列表显示区域
        list_frame = ttk.Frame(self.main_func_frame)
        list_frame.grid(row=0, column=1, padx=(0, 10), pady=8, sticky=(tk.W, tk.E))
        
        # 创建Listbox和滚动条
        self.files_listbox = tk.Listbox(list_frame, height=6, width=50)
        files_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
        
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 文件操作按钮
        files_btn_frame = ttk.Frame(self.main_func_frame)
        files_btn_frame.grid(row=0, column=2, padx=5, pady=8)
        
        ttk.Button(files_btn_frame, text="📁 添加文件", 
                  command=self.browse_source_files, width=15).pack(pady=2)
        ttk.Button(files_btn_frame, text="🗑️ 清空列表", 
                  command=self.clear_source_files, width=15).pack(pady=2)
        ttk.Button(files_btn_frame, text="❌ 删除选中", 
                  command=self.remove_selected_file, width=15).pack(pady=2)
        
        # 说明文字
        ttk.Label(self.main_func_frame, text="💡 模式2: 直接创建软链接，不修改源文件", 
                 font=('Arial', 9)).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
    
    def on_mode_change(self):
        """模式切换时的处理"""
        if self.current_mode.get() == 1:
            # 模式1：显示原有界面
            self.show_mode1_widgets()
            self.execute_btn.configure(text="🚀 添加Front Matter并创建链接")
        else:
            # 模式2：显示批量处理界面
            self.show_mode2_widgets()
            self.execute_btn.configure(text="🚀 批量创建软链接")
    
    def show_mode1_widgets(self):
        """显示模式1的组件"""
        # 隐藏所有组件
        for widget in self.main_func_frame.winfo_children():
            widget.grid_remove()
        
        # 重新创建并显示模式1的组件
        self.create_mode1_widgets()
        
        # 重新显示发布选项
        publish_frame = ttk.Frame(self.main_func_frame)
        publish_frame.grid(row=4, column=0, columnspan=3, pady=15)
        
        self.publish_check = ttk.Checkbutton(publish_frame, 
                                           text="🚀 发布到博客 (执行 hexo g && hexo d)", 
                                           variable=self.publish_var)
        self.publish_check.pack()
    
    def show_mode2_widgets(self):
        """显示模式2的组件"""
        # 隐藏所有组件
        for widget in self.main_func_frame.winfo_children():
            widget.grid_remove()
        
        # 重新创建并显示模式2的组件
        self.create_mode2_widgets()
        
        # 重新显示发布选项
        publish_frame = ttk.Frame(self.main_func_frame)
        publish_frame.grid(row=4, column=0, columnspan=3, pady=15)
        
        self.publish_check = ttk.Checkbutton(publish_frame, 
                                           text="🚀 发布到博客 (执行 hexo g && hexo d)", 
                                           variable=self.publish_var)
        self.publish_check.pack()
    
    def browse_source_files(self):
        """浏览并添加多个源文件"""
        files = filedialog.askopenfilenames(
            title="选择源文件",
            filetypes=[("Markdown文件", "*.md"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if files:
            for file in files:
                if file not in self.source_files:
                    self.source_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
            
            self.log_result(f"✅ 已添加 {len(files)} 个文件到处理列表")
    
    def clear_source_files(self):
        """清空源文件列表"""
        self.source_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.log_result("🗑️ 已清空文件列表")
    
    def remove_selected_file(self):
        """删除选中的文件"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            removed_file = self.source_files.pop(index)
            self.files_listbox.delete(index)
            self.log_result(f"❌ 已移除文件: {os.path.basename(removed_file)}")
        else:
            messagebox.showwarning("警告", "请先选择要删除的文件")
    
    def open_settings(self):
        """打开设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ 设置")
        settings_window.geometry("600x400")
        settings_window.resizable(False, False)
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 居中显示
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (400 // 2)
        settings_window.geometry(f"600x400+{x}+{y}")
        
        # 设置窗口内容
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="⚙️ 博客配置设置", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 配置项
        config_frame = ttk.Frame(main_frame)
        config_frame.pack(fill=tk.BOTH, expand=True)
        
        # 博客文章目录
        ttk.Label(config_frame, text="📁 博客文章目录:").grid(
            row=0, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        posts_dir_var = tk.StringVar(value=self.config.get("posts_dir", ""))
        posts_dir_entry = ttk.Entry(config_frame, textvariable=posts_dir_var, width=40)
        posts_dir_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", 
                  command=lambda: self.browse_directory(posts_dir_var, "选择博客文章目录")).grid(
                  row=0, column=2, padx=5, pady=10)
        
        # 博客根目录
        ttk.Label(config_frame, text="🏠 博客根目录:").grid(
            row=1, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        blog_root_var = tk.StringVar(value=self.config.get("blog_root", ""))
        blog_root_entry = ttk.Entry(config_frame, textvariable=blog_root_var, width=40)
        blog_root_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", 
                  command=lambda: self.browse_directory(blog_root_var, "选择博客根目录")).grid(
                  row=1, column=2, padx=5, pady=10)
        
        # 模板文件
        ttk.Label(config_frame, text="📄 模板文件:").grid(
            row=2, column=0, sticky=tk.W, pady=10, padx=(0, 10))
        template_file_var = tk.StringVar(value=self.config.get("template_file", ""))
        template_file_entry = ttk.Entry(config_frame, textvariable=template_file_var, width=40)
        template_file_entry.grid(row=2, column=1, padx=(0, 10), pady=10, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", 
                  command=lambda: self.browse_file(template_file_var, "选择模板文件")).grid(
                  row=2, column=2, padx=5, pady=10)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
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
        
        ttk.Button(button_frame, text="💾 保存", command=save_settings, width=15).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ 取消", command=settings_window.destroy, width=15).pack(
            side=tk.LEFT, padx=10)
        
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
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # 创建默认配置
                self.config = {
                    "posts_dir": "",
                    "blog_root": "",
                    "template_file": ""
                }
        except Exception as e:
            print(f"加载配置失败: {e}")
            self.config = {}
    
    def load_config_to_ui(self):
        """将配置加载到界面"""
        pass  # 配置在设置窗口中加载
    
    def browse_source_file(self):
        """浏览源文件"""
        file_path = filedialog.askopenfilename(
            title="选择源笔记文件",
            filetypes=[
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.source_file_var.set(file_path)
    
    def use_filename_as_title(self):
        """使用文件名作为标题"""
        source_file = self.source_file_var.get()
        if source_file:
            filename = os.path.splitext(os.path.basename(source_file))[0]
            self.title_var.set(filename)
        else:
            messagebox.showwarning("警告", "请先选择源文件")
    
    def log_result(self, message):
        """记录结果到文本框"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.result_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def parse_tags_categories(self, text):
        """解析标签和分类"""
        if not text.strip():
            return []
        return [item.strip() for item in text.split() if item.strip()]
    
    def create_symlink(self, source, target):
        """创建软链接"""
        try:
            # 检查是否已存在
            if os.path.exists(target):
                if os.path.islink(target):
                    os.unlink(target)
                else:
                    self.log_result(f"⚠️ 目标文件已存在且不是软链接: {target}")
                    return False
            
            # 创建软链接
            if os.name == 'nt':  # Windows
                # 使用mklink命令
                cmd = f'mklink "{target}" "{source}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    self.log_result(f"✅ 软链接创建成功: {target}")
                    return True
                else:
                    self.log_result(f"❌ 软链接创建失败: {result.stderr}")
                    return False
            else:  # Unix/Linux
                os.symlink(source, target)
                self.log_result(f"✅ 软链接创建成功: {target}")
                return True
                
        except Exception as e:
            self.log_result(f"❌ 创建软链接时出错: {str(e)}")
            return False
    
    def generate_front_matter_from_template(self, title, categories, tags):
        """从模板文件生成Front Matter和额外内容"""
        template_file = self.config.get("template_file", "")
        
        if template_file and os.path.exists(template_file):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                # 替换模板中的变量
                template_content = template_content.replace('{{ title }}', title)
                template_content = template_content.replace('{{ date }}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                
                # 处理categories和tags
                if template_content.count('---') >= 2:
                    # 找到第一个和第二个---的位置
                    first_dash = template_content.find('---')
                    second_dash = template_content.find('---', first_dash + 3)
                    
                    if first_dash != -1 and second_dash != -1:
                        front_matter_content = template_content[first_dash + 3:second_dash]
                        rest_content = template_content[second_dash + 3:]
                        
                        # 处理front matter中的categories和tags
                        lines = front_matter_content.split('\n')
                        new_lines = []
                        skip_next = False
                        
                        for i, line in enumerate(lines):
                            if skip_next:
                                # 跳过categories或tags下的列表项
                                if line.strip().startswith('- ') or line.strip() == '':
                                    continue
                                else:
                                    skip_next = False
                            
                            line_stripped = line.strip()
                            if line_stripped == 'categories:':
                                new_lines.append('categories:')
                                if categories:
                                    for category in categories:
                                        new_lines.append(f'- {category}')
                                skip_next = True
                            elif line_stripped == 'tags:':
                                new_lines.append('tags:')
                                if tags:
                                    for tag in tags:
                                        new_lines.append(f'- {tag}')
                                skip_next = True
                            elif not skip_next:
                                new_lines.append(line)
                        
                        # 重新组装
                        new_front_matter = '\n'.join(new_lines)
                        return f"---{new_front_matter}---{rest_content}"
                
                return template_content
                
            except Exception as e:
                self.log_result(f"⚠️ 读取模板文件失败: {e}")
        
        # 如果没有模板文件，使用默认的Front Matter
        return self.generate_front_matter(title, categories, tags)
    
    def generate_front_matter(self, title, categories, tags):
        """生成默认的Front Matter（备用方案）"""
        front_matter = "---\n"
        front_matter += f"title: {title}\n"
        front_matter += f"date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if categories:
            front_matter += "categories:\n"
            for category in categories:
                front_matter += f"- {category}\n"
        
        if tags:
            front_matter += "tags:\n"
            for tag in tags:
                front_matter += f"- {tag}\n"
        
        front_matter += "---\n\n"
        return front_matter
    
    def execute_hexo_commands(self, blog_root):
        """执行Hexo命令"""
        try:
            self.log_result("🚀 开始执行Hexo命令...")
            
            # 切换到博客根目录
            original_dir = os.getcwd()
            os.chdir(blog_root)
            
            # 执行hexo g
            self.log_result("📦 正在生成静态文件 (hexo g)...")
            result = subprocess.run('hexo g', shell=True, capture_output=True, text=True, 
                                  encoding='utf-8', errors='ignore')
            
            if result.returncode == 0:
                self.log_result("✅ 静态文件生成成功")
                if result.stdout.strip():
                    pass
                    #self.log_result(f"输出: {result.stdout.strip()}")
            else:
                self.log_result(f"❌ 静态文件生成失败")
                if result.stderr.strip():
                    self.log_result(f"错误: {result.stderr.strip()}")
                if result.stdout.strip():
                    self.log_result(f"输出: {result.stdout.strip()}")
                return False
            
            # 执行hexo d
            self.log_result("🌐 正在部署到远程 (hexo d)...")
            result = subprocess.run('hexo d', shell=True, capture_output=True, text=True, 
                                  encoding='utf-8', errors='ignore')
            
            if result.returncode == 0:
                self.log_result("✅ 部署成功！")
                return True
            else:
                self.log_result(f"❌ 部署失败")
                if result.stderr.strip():
                    self.log_result(f"错误: {result.stderr.strip()}")
                if result.stdout.strip():
                    self.log_result(f"输出: {result.stdout.strip()}")
                return False
                
        except Exception as e:
            self.log_result(f"❌ 执行Hexo命令时出错: {str(e)}")
            return False
        finally:
            # 恢复原目录
            os.chdir(original_dir)
    
    def validate_inputs(self):
        """验证输入"""
        if self.current_mode.get() == 1:
            # 模式1：原有验证逻辑
            if not self.source_file_var.get():
                messagebox.showerror("错误", "请选择源笔记文件")
                return False
            
            if not os.path.exists(self.source_file_var.get()):
                messagebox.showerror("错误", "源文件不存在")
                return False
            
            if not self.title_var.get():
                messagebox.showerror("错误", "请输入文章标题")
                return False
        else:
            # 模式2：批量处理验证
            if not self.source_files:
                messagebox.showerror("错误", "请添加要处理的源文件")
                return False
            
            # 检查所有文件是否存在
            for file_path in self.source_files:
                if not os.path.exists(file_path):
                    messagebox.showerror("错误", f"文件不存在: {file_path}")
                    return False
        
        # 通用验证
        if not self.config.get("posts_dir"):
            messagebox.showerror("错误", "请在设置中配置博客文章目录")
            return False
        
        if not os.path.exists(self.config.get("posts_dir")):
            messagebox.showerror("错误", "博客文章目录不存在")
            return False
        
        if self.publish_var.get():
            if not self.config.get("blog_root"):
                messagebox.showerror("错误", "要发布博客，请在设置中配置博客根目录")
                return False
            
            if not os.path.exists(self.config.get("blog_root")):
                messagebox.showerror("错误", "博客根目录不存在")
                return False
        
        return True
    
    def execute_publish(self):
        """执行发布"""
        if not self.validate_inputs():
            return
        
        if self.current_mode.get() == 1:
            self.execute_mode1()
        else:
            self.execute_mode2()
    
    def execute_mode1(self):
        """执行模式1：添加Front Matter并创建链接"""
        def publish_thread():
            try:
                self.execute_btn.configure(state='disabled')
                self.log_result("🚀 开始模式1发布流程...")
                
                source_file = self.source_file_var.get()
                title = self.title_var.get()
                categories = self.parse_tags_categories(self.categories_var.get())
                tags = self.parse_tags_categories(self.tags_var.get())
                
                # 生成目标文件名
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '-')
                target_filename = f"{safe_title}.md"
                target_path = os.path.join(self.config["posts_dir"], target_filename)
                
                self.log_result(f"📝 目标链接文件: {target_path}")
                
                # 读取源文件内容
                try:
                    with open(source_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(source_file, 'r', encoding='gbk') as f:
                        content = f.read()
                
                # 检查源文件是否已经有Front Matter
                if content.startswith('---'):
                    # 如果已有Front Matter，询问是否覆盖
                    from tkinter import messagebox
                    replace = messagebox.askyesno(
                        "检测到Front Matter", 
                        "源文件已包含Front Matter，是否替换为新的？\n\n"
                        "选择'是'：替换现有的Front Matter\n"
                        "选择'否'：保持现有的Front Matter"
                    )
                    
                    if replace:
                        # 移除现有的Front Matter
                        if '---' in content[3:]:  # 寻找第二个---
                            second_marker = content.find('---', 3)
                            content = content[second_marker + 3:].lstrip('\n')
                        else:
                            self.log_result("⚠️ 无法解析现有的Front Matter格式")
                    else:
                        self.log_result("📝 保持现有的Front Matter")
                        # 创建软链接
                        if self.create_symlink(source_file, target_path):
                            self.log_result("✅ 软链接创建成功")
                            
                            # 如果选择发布，执行Hexo命令
                            if self.publish_var.get():
                                success = self.execute_hexo_commands(self.config["blog_root"])
                                if success:
                                    self.log_result("🎉 发布完成！")
                                else:
                                    self.log_result("❌ 发布失败")
                            else:
                                self.log_result("✅ 文章已准备就绪，未执行发布")
                        else:
                            self.log_result("❌ 软链接创建失败")
                        return
                
                # 生成Front Matter
                front_matter = self.generate_front_matter_from_template(title, categories, tags)
                
                # 在源文件开头添加Front Matter
                new_content = front_matter + '\n\n' + content
                
                # 写回源文件
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.log_result("✅ Front Matter已添加到源文件")
                
                # 创建软链接
                if self.create_symlink(source_file, target_path):
                    self.log_result("✅ 软链接创建成功")
                    
                    # 如果选择发布，执行Hexo命令
                    if self.publish_var.get():
                        success = self.execute_hexo_commands(self.config["blog_root"])
                        if success:
                            self.log_result("🎉 发布完成！")
                        else:
                            self.log_result("❌ 发布失败")
                    else:
                        self.log_result("✅ 文章已准备就绪，未执行发布")
                else:
                    self.log_result("❌ 软链接创建失败")
                
            except Exception as e:
                self.log_result(f"❌ 发布过程中出错: {str(e)}")
            finally:
                self.execute_btn.configure(state='normal')
        
        # 在新线程中执行发布
        thread = threading.Thread(target=publish_thread)
        thread.daemon = True
        thread.start()
    
    def execute_mode2(self):
        """执行模式2：批量创建软链接"""
        def batch_thread():
            try:
                self.execute_btn.configure(state='disabled')
                self.log_result("🚀 开始模式2批量处理流程...")
                
                success_count = 0
                total_count = len(self.source_files)
                
                for i, source_file in enumerate(self.source_files, 1):
                    try:
                        self.log_result(f"📝 处理文件 {i}/{total_count}: {os.path.basename(source_file)}")
                        
                        # 生成目标文件名（使用原文件名）
                        filename = os.path.basename(source_file)
                        target_path = os.path.join(self.config["posts_dir"], filename)
                        
                        # 检查目标文件是否已存在
                        if os.path.exists(target_path):
                            self.log_result(f"⚠️ 目标文件已存在，跳过: {filename}")
                            continue
                        
                        # 创建软链接
                        if self.create_symlink(source_file, target_path):
                            self.log_result(f"✅ 软链接创建成功: {filename}")
                            success_count += 1
                        else:
                            self.log_result(f"❌ 软链接创建失败: {filename}")
                    
                    except Exception as e:
                        self.log_result(f"❌ 处理文件时出错: {os.path.basename(source_file)} - {str(e)}")
                
                self.log_result(f"🎉 批量处理完成！成功: {success_count}/{total_count}")
                
                # 如果选择发布，执行Hexo命令
                if self.publish_var.get() and success_count > 0:
                    self.log_result("🚀 开始发布到博客...")
                    success = self.execute_hexo_commands(self.config["blog_root"])
                    if success:
                        self.log_result("🎉 发布完成！")
                    else:
                        self.log_result("❌ 发布失败")
                elif success_count > 0:
                    self.log_result("✅ 软链接创建完成，未执行发布")
                
            except Exception as e:
                self.log_result(f"❌ 批量处理过程中出错: {str(e)}")
            finally:
                self.execute_btn.configure(state='normal')
        
        # 在新线程中执行批量处理
        thread = threading.Thread(target=batch_thread)
        thread.daemon = True
        thread.start()

def check_admin():
    """检查是否有管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员身份运行"""
    if check_admin():
        return True
    else:
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            return False
        except:
            return False

def main():
    """主函数"""
    # 检查管理员权限
    if not check_admin():
        print("需要管理员权限，正在重新启动...")
        if not run_as_admin():
            print("无法获取管理员权限")
            return
        else:
            return
    
    # 创建主窗口
    root = tk.Tk()
    app = HexoPublisher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 