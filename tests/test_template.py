#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试模板功能
"""

import os
from datetime import datetime

def generate_front_matter(title, categories, tags):
    """生成Front Matter使用模板文件"""
    template_content = ""
    template_file = "template.md"
    
    if os.path.exists(template_file):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
            print(f"✅ 已读取模板文件: {template_file}")
        except Exception as e:
            print(f"⚠️ 读取模板文件失败: {e}")
            return None
    
    # 替换模板变量
    result = template_content
    result = result.replace("{{ title }}", title)
    result = result.replace("{{ date }}", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # 处理分类
    if categories:
        categories_str = "\n"
        for category in categories:
            categories_str += f"- {category}\n"
        result = result.replace("{{ categories }}", categories_str)
    else:
        result = result.replace("{{ categories }}", "\n")
    
    # 处理标签
    if tags:
        tags_str = "\n"
        for tag in tags:
            tags_str += f"- {tag}\n"
        result = result.replace("{{ tags }}", tags_str)
    else:
        result = result.replace("{{ tags }}", "\n")
    
    return result

def test_template():
    """测试模板功能"""
    print("🧪 开始测试模板功能")
    
    # 测试数据
    title = "我的第一篇博客"
    categories = ["技术", "编程"]
    tags = ["Python", "GUI", "Hexo"]
    
    # 生成Front Matter
    result = generate_front_matter(title, categories, tags)
    
    if result:
        print("\n📄 生成的Front Matter:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        # 模拟原始笔记内容
        original_content = """
# 我的笔记

这是我的第一篇笔记。

## 内容

- 学习Python
- 学习GUI开发
- 学习Hexo博客

## 代码示例

```python
print("Hello World!")
```
"""
        
        # 合并内容
        final_content = result + original_content
        
        print("\n📝 最终生成的文章内容:")
        print("=" * 50)
        print(final_content)
        print("=" * 50)
        
        print("✅ 模板测试成功！")
        print("💡 可以看到模板中的其他内容（如 index_img、banner_img、{% note info %}）都被保留了")
    else:
        print("❌ 模板测试失败")

if __name__ == "__main__":
    test_template() 