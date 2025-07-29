#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
星露谷翻译整合工具 (Stardew Valley Translation Merger)

功能：
1. 收集翻译数据文件夹中所有zh.json文件的内容，合并为all.json
2. 将all.json中的翻译应用到translations文件夹中的所有模组

作者：AI Assistant
"""

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

def is_english_text(text):
    """判断文本是否为英文"""
    if not isinstance(text, str):
        return False
    
    # 移除空格、标点符号和数字
    clean_text = re.sub(r'[^\w]', '', text)
    
    if not clean_text:
        return False
    
    # 计算英文字符的比例
    english_chars = sum(1 for char in clean_text if ord(char) < 128 and char.isalpha())
    total_chars = len(clean_text)
    
    # 如果英文字符占比超过90%，认为是英文
    english_ratio = english_chars / total_chars if total_chars > 0 else 0
    
    return english_ratio > 0.9

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

def find_zh_json_files(root_dir):
    """递归遍历目录，查找所有zh.json文件"""
    zh_json_files = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob("zh.json"):
        zh_json_files.append(file_path)
    
    return zh_json_files

def merge_zh_json_files(json_files):
    """合并所有zh.json文件的内容"""
    merged_data = {}
    
    for file_path in json_files:
        try:
            print(f"正在处理: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            # 移除注释
            clean_content = remove_json_comments(raw_content)
            
            # 解析JSON
            data = json.loads(clean_content)
                
            # 如果是字典，直接合并
            if isinstance(data, dict):
                for key, value in data.items():
                    if key in merged_data:
                        print(f"警告: 键 '{key}' 重复，来自文件 {file_path}")
                    merged_data[key] = value
            else:
                print(f"警告: {file_path} 不是JSON对象格式，跳过")
                
        except json.JSONDecodeError as e:
            print(f"错误: 无法解析JSON文件 {file_path}: {e}")
        except Exception as e:
            print(f"错误: 处理文件 {file_path} 时出错: {e}")
    
    return merged_data

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
    skipped_count = 0
    for key in zh_data:
        if key in all_translations:
            translation_value = all_translations[key]
            
            # 检查翻译是否为英文，如果是英文则跳过
            if is_english_text(translation_value):
                skipped_count += 1
                print(f"    跳过英文翻译: {key} = {translation_value}")
                continue
            
            if zh_data[key] != translation_value:
                zh_data[key] = translation_value
                updated_count += 1
    
    print(f"  更新了 {updated_count} 个翻译，跳过了 {skipped_count} 个英文翻译")
    
    # 写入zh.json文件
    try:
        with open(zh_json_path, 'w', encoding='utf-8') as f:
            json.dump(zh_data, f, ensure_ascii=False, indent=2)
        print(f"  成功写入 {zh_json_path}")
    except Exception as e:
        print(f"  错误: 写入文件时出错: {e}")

def step1_collect_translations():
    """第一步：收集所有翻译数据"""
    print("=" * 60)
    print("第一步：收集翻译数据")
    print("=" * 60)
    
    # 翻译数据文件夹路径
    translation_dir = "翻译数据"
    output_file = "tmp/all.json"
    
    # 确保tmp目录存在
    os.makedirs("tmp", exist_ok=True)
    
    print(f"开始遍历 {translation_dir} 文件夹...")
    
    # 查找所有zh.json文件
    zh_json_files = find_zh_json_files(translation_dir)
    
    if not zh_json_files:
        print(f"在 {translation_dir} 中没有找到任何 zh.json 文件")
        return False
    
    print(f"找到 {len(zh_json_files)} 个 zh.json 文件:")
    for file_path in zh_json_files:
        print(f"  - {file_path}")
    
    print("\n开始合并文件...")
    
    # 合并所有JSON文件
    merged_data = merge_zh_json_files(zh_json_files)
    
    print(f"\n合并完成，共收集到 {len(merged_data)} 个键值对")
    
    # 写入all.json文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        
        print(f"成功写入 {output_file} 文件")
        print(f"文件大小: {os.path.getsize(output_file)} 字节")
        return True
        
    except Exception as e:
        print(f"错误: 写入文件时出错: {e}")
        return False

def step2_apply_translations():
    """第二步：应用翻译到模组"""
    print("=" * 60)
    print("第二步：应用翻译到模组")
    print("=" * 60)
    
    # 文件夹路径
    translations_dir = "translations"
    all_json_path = "tmp/all.json"
    
    # 检查all.json是否存在
    if not os.path.exists(all_json_path):
        print(f"错误: {all_json_path} 文件不存在，请先运行第一步")
        return False
    
    # 读取all.json
    print(f"读取 {all_json_path}...")
    try:
        with open(all_json_path, 'r', encoding='utf-8') as f:
            all_translations = json.load(f)
        print(f"加载了 {len(all_translations)} 个翻译条目")
    except Exception as e:
        print(f"错误: 无法读取 {all_json_path}: {e}")
        return False
    
    # 检查translations目录是否存在
    if not os.path.exists(translations_dir):
        print(f"错误: {translations_dir} 目录不存在")
        return False
    
    print(f"\n开始遍历 {translations_dir} 文件夹...")
    
    # 查找所有包含default.json的目录
    default_dirs = find_default_json_dirs(translations_dir)
    
    if not default_dirs:
        print(f"在 {translations_dir} 中没有找到任何 default.json 文件")
        return False
    
    print(f"找到 {len(default_dirs)} 个包含 default.json 的目录:")
    for dir_path in default_dirs:
        print(f"  - {dir_path}")
    
    # 处理每个目录
    for dir_path in default_dirs:
        process_directory(dir_path, all_translations)
    
    print(f"\n第二步处理完成！")
    return True

def main():
    """主函数"""
    print("星露谷翻译整合工具")
    print("=" * 60)
    
    # 第一步：收集翻译数据
    if not step1_collect_translations():
        print("第一步失败，程序终止")
        return
    
    print("\n")
    
    # 第二步：应用翻译到模组
    if not step2_apply_translations():
        print("第二步失败")
        return
    
    print("\n" + "=" * 60)
    print("所有步骤完成！翻译已成功应用到所有模组。")
    print("=" * 60)

if __name__ == "__main__":
    main()
