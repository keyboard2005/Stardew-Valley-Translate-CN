#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
翻译缺失检测工具 (Translation Missing Detector)

功能：
1. 遍历translations文件夹下的所有模组
2. 对比每个模组的default.json和zh.json文件
3. 找出zh.json中缺失的翻译或值与default.json相同的项目
4. 将需要翻译的内容导出到missing_translations.json

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

def find_default_json_dirs(root_dir):
    """查找所有包含default.json的目录"""
    default_dirs = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob("default.json"):
        default_dirs.append(file_path.parent)
    
    return default_dirs

def check_missing_translations(dir_path):
    """检查单个目录中的翻译缺失"""
    default_json_path = dir_path / "default.json"
    zh_json_path = dir_path / "zh.json"
    
    mod_name = dir_path.name
    print(f"\n检查模组: {mod_name}")
    
    # 读取default.json
    default_data = load_json_with_comments(default_json_path)
    if default_data is None:
        print(f"  跳过: 无法读取 {default_json_path}")
        return {}
    
    # 读取zh.json（如果存在）
    if zh_json_path.exists():
        zh_data = load_json_with_comments(zh_json_path)
        if zh_data is None:
            print(f"  zh.json 文件损坏，将所有default.json内容标记为缺失")
            zh_data = {}
    else:
        print(f"  zh.json 不存在，将所有default.json内容标记为缺失")
        zh_data = {}
    
    missing_translations = {}
    total_keys = 0
    missing_count = 0
    untranslated_count = 0
    
    # 检查每个键
    for key, default_value in default_data.items():
        total_keys += 1
        
        if key not in zh_data:
            # 键不存在，需要翻译
            missing_translations[key] = default_value
            missing_count += 1
            print(f"    缺失键: {key}")
        elif zh_data[key] == default_value:
            # 键存在但值相同，可能未翻译
            if is_english_text(default_value):
                missing_translations[key] = default_value
                untranslated_count += 1
                print(f"    未翻译: {key} = {default_value}")
        # 如果zh_data[key]存在且不同于default_value，说明已经翻译了
    
    print(f"  总计: {total_keys} 个键")
    print(f"  缺失: {missing_count} 个键")
    print(f"  未翻译: {untranslated_count} 个键")
    print(f"  需要翻译: {len(missing_translations)} 个键")
    
    return {mod_name: missing_translations} if missing_translations else {}

def main():
    """主函数"""
    print("翻译缺失检测工具")
    print("=" * 60)
    
    # 文件夹路径
    translations_dir = "Mods"
    output_file = "missing_translations.json"
    
    # 检查translations目录是否存在
    if not os.path.exists(translations_dir):
        print(f"错误: {translations_dir} 目录不存在")
        return
    
    print(f"开始检测 {translations_dir} 文件夹中的翻译缺失...")
    
    # 查找所有包含default.json的目录
    default_dirs = find_default_json_dirs(translations_dir)
    
    if not default_dirs:
        print(f"在 {translations_dir} 中没有找到任何 default.json 文件")
        return
    
    print(f"找到 {len(default_dirs)} 个包含 default.json 的模组:")
    for dir_path in default_dirs:
        print(f"  - {dir_path.name}")
    
    # 收集所有缺失的翻译
    all_missing_translations = {}
    
    for dir_path in default_dirs:
        missing = check_missing_translations(dir_path)
        all_missing_translations.update(missing)
    
    # 统计总体情况
    total_missing = 0
    for mod_name, translations in all_missing_translations.items():
        total_missing += len(translations)
    
    print(f"\n" + "=" * 60)
    print(f"检测完成！")
    print(f"共检测 {len(default_dirs)} 个模组")
    print(f"有翻译缺失的模组: {len(all_missing_translations)} 个")
    print(f"总计缺失翻译: {total_missing} 个")
    
    # 写入结果文件
    if all_missing_translations:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_missing_translations, f, ensure_ascii=False, indent=2)
            
            print(f"缺失翻译已导出到: {output_file}")
            print(f"文件大小: {os.path.getsize(output_file)} 字节")
            
            # 显示每个模组的缺失情况
            print(f"\n各模组缺失翻译数量:")
            for mod_name, translations in all_missing_translations.items():
                print(f"  {mod_name}: {len(translations)} 个")
                
        except Exception as e:
            print(f"错误: 写入文件时出错: {e}")
    else:
        print("所有模组翻译完整，无需导出文件")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
