#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用于把all.json里的翻译填充到任何模组的zh.json中

import os
import json
import re
from pathlib import Path

def remove_json_comments(json_string):
    """移除JSON字符串中的注释"""
    # 移除 // 单行注释
    json_string = re.sub(r'//.*$', '', json_string, flags=re.MULTILINE)
    
    # 移除 /* */ 多行注释
    json_string = re.sub(r'/\*.*?\*/', '', json_string, flags=re.DOTALL)
    
    # 移除多余的逗号（在}或]前的逗号）
    json_string = re.sub(r',\s*([}\]])', r'\1', json_string)
    
    return json_string

def load_json_with_comments(file_path):
    """加载带注释的JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        # 移除注释
        clean_content = remove_json_comments(raw_content)
        
        # 解析JSON
        return json.loads(clean_content)
    except Exception as e:
        print(f"错误: 无法读取文件 {file_path}: {e}")
        return None

def find_default_json_dirs(root_dir):
    """查找所有包含default.json的目录"""
    default_dirs = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob("default.json"):
        default_dirs.append(file_path.parent)
    
    return default_dirs

def process_directory(dir_path, all_translations):
    """处理单个包含default.json的目录"""
    default_json_path = dir_path / "default.json"
    zh_json_path = dir_path / "zh.json"
    
    print(f"\n处理目录: {dir_path}")
    
    # 读取default.json
    default_data = load_json_with_comments(default_json_path)
    if default_data is None:
        print(f"  跳过: 无法读取 {default_json_path}")
        return
    
    # 检查zh.json是否存在
    if not zh_json_path.exists():
        print(f"  创建新的 zh.json 文件")
        zh_data = default_data.copy()
    else:
        print(f"  读取现有的 zh.json 文件")
        zh_data = load_json_with_comments(zh_json_path)
        if zh_data is None:
            print(f"  zh.json 文件损坏，使用 default.json 内容")
            zh_data = default_data.copy()
    
    # 确保zh.json包含所有default.json的键
    for key in default_data:
        if key not in zh_data:
            zh_data[key] = default_data[key]
    
    # 用all.json中的翻译填充zh.json
    updated_count = 0
    for key in zh_data:
        if key in all_translations:
            if zh_data[key] != all_translations[key]:
                zh_data[key] = all_translations[key]
                updated_count += 1
    
    print(f"  更新了 {updated_count} 个翻译")
    
    # 写入zh.json文件
    try:
        with open(zh_json_path, 'w', encoding='utf-8') as f:
            json.dump(zh_data, f, ensure_ascii=False, indent=2)
        print(f"  成功写入 {zh_json_path}")
    except Exception as e:
        print(f"  错误: 写入文件时出错: {e}")

def main():
    # 文件夹路径
    translations_dir = "translations"
    all_json_path = "tmp/all.json"
    
    # 检查all.json是否存在
    if not os.path.exists(all_json_path):
        print(f"错误: {all_json_path} 文件不存在，请先运行第一步")
        return
    
    # 读取all.json
    print(f"读取 {all_json_path}...")
    try:
        with open(all_json_path, 'r', encoding='utf-8') as f:
            all_translations = json.load(f)
        print(f"加载了 {len(all_translations)} 个翻译条目")
    except Exception as e:
        print(f"错误: 无法读取 {all_json_path}: {e}")
        return
    
    # 检查translations目录是否存在
    if not os.path.exists(translations_dir):
        print(f"错误: {translations_dir} 目录不存在")
        return
    
    print(f"\n开始遍历 {translations_dir} 文件夹...")
    
    # 查找所有包含default.json的目录
    default_dirs = find_default_json_dirs(translations_dir)
    
    if not default_dirs:
        print(f"在 {translations_dir} 中没有找到任何 default.json 文件")
        return
    
    print(f"找到 {len(default_dirs)} 个包含 default.json 的目录:")
    for dir_path in default_dirs:
        print(f"  - {dir_path}")
    
    # 处理每个目录
    for dir_path in default_dirs:
        process_directory(dir_path, all_translations)
    
    print(f"\n处理完成！")

if __name__ == "__main__":
    main()
