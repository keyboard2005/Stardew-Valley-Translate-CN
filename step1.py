#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户获取所有zh.json文件并合并为all.json的脚本

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

def find_zh_json_files(root_dir):
    """递归遍历目录，查找所有zh.json文件"""
    zh_json_files = []
    root_path = Path(root_dir)
    
    for file_path in root_path.rglob("zh.json"):
        zh_json_files.append(file_path)
    
    return zh_json_files

def merge_json_files(json_files):
    """合并所有JSON文件的内容"""
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
            print(f"尝试显示前200个字符: {raw_content[:200]}...")
        except Exception as e:
            print(f"错误: 处理文件 {file_path} 时出错: {e}")
    
    return merged_data

def main():
    # 翻译数据文件夹路径
    translation_dir = "翻译数据"
    output_file = "tmp/all.json"
    
    print(f"开始遍历 {translation_dir} 文件夹...")
    
    # 查找所有zh.json文件
    zh_json_files = find_zh_json_files(translation_dir)
    
    if not zh_json_files:
        print(f"在 {translation_dir} 中没有找到任何 zh.json 文件")
        return
    
    print(f"找到 {len(zh_json_files)} 个 zh.json 文件:")
    for file_path in zh_json_files:
        print(f"  - {file_path}")
    
    print("\n开始合并文件...")
    
    # 合并所有JSON文件
    merged_data = merge_json_files(zh_json_files)
    
    print(f"\n合并完成，共收集到 {len(merged_data)} 个键值对")
    
    # 写入all.json文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        
        print(f"成功写入 {output_file} 文件")
        print(f"文件大小: {os.path.getsize(output_file)} 字节")
        
    except Exception as e:
        print(f"错误: 写入文件时出错: {e}")

if __name__ == "__main__":
    main()
