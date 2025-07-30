#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import argparse
from pathlib import Path

def remove_json_comments(json_string):
    """
    移除JSON字符串中的注释，支持 // 和 /* */ 格式
    """
    # 移除 // 行注释
    json_string = re.sub(r'//.*?$', '', json_string, flags=re.MULTILINE)
    # 移除 /* */ 块注释
    json_string = re.sub(r'/\*.*?\*/', '', json_string, flags=re.DOTALL)
    return json_string

def load_json_with_comments(file_path):
    """
    加载可能包含注释的JSON文件
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 保存原始内容用于后续更新
        original_content = content
        
        # 移除注释后解析JSON
        clean_content = remove_json_comments(content)
        data = json.loads(clean_content)
        
        return data, original_content
    except Exception as e:
        print(f"错误：无法读取文件 {file_path}: {e}")
        return None, None

def update_json_content(original_content, updates):
    """
    更新JSON内容，保持原有格式和注释
    """
    updated_content = original_content
    
    for key, new_value in updates.items():
        # 构建正则表达式来匹配key-value对
        # 支持不同的引号风格和空格
        pattern = rf'("{re.escape(key)}"\s*:\s*)"([^"\\]*(\\.[^"\\]*)*)"'
        
        # 转义新值中的特殊字符
        escaped_value = new_value.replace('\\', '\\\\').replace('"', '\\"')
        replacement = rf'\1"{escaped_value}"'
        
        # 替换值
        updated_content = re.sub(pattern, replacement, updated_content)
    
    return updated_content

def find_target_files(mods_path):
    """
    递归查找Mods文件夹中的default.json和zh.json文件
    """
    target_files = []
    mods_path = Path(mods_path)
    
    if not mods_path.exists():
        print(f"错误：Mods路径不存在: {mods_path}")
        return target_files
    
    # 递归搜索目标文件
    for file_path in mods_path.rglob("*.json"):
        if file_path.name in ["default.json", "zh.json"]:
            target_files.append(file_path)
    
    return target_files

def update_translation_files(en1end_path, mods_path, dry_run=False):
    """
    主函数：更新翻译文件
    """
    # 加载en1end.json文件
    print(f"正在加载翻译源文件: {en1end_path}")
    source_data, _ = load_json_with_comments(en1end_path)
    
    if source_data is None:
        print("错误：无法加载翻译源文件")
        return
    
    print(f"翻译源文件包含 {len(source_data)} 个条目")
    
    # 查找目标文件
    print(f"正在搜索Mods文件夹: {mods_path}")
    target_files = find_target_files(mods_path)
    
    if not target_files:
        print("未找到任何target文件 (default.json 或 zh.json)")
        return
    
    print(f"找到 {len(target_files)} 个目标文件")
    
    # 处理每个目标文件
    total_updated = 0
    
    for file_path in target_files:
        print(f"\n正在处理: {file_path}")
        
        # 加载目标文件
        target_data, original_content = load_json_with_comments(file_path)
        
        if target_data is None:
            continue
        
        # 找到需要更新的key
        updates = {}
        for key in target_data.keys():
            if key in source_data:
                updates[key] = source_data[key]
        
        if not updates:
            print(f"  未找到匹配的key")
            continue
        
        print(f"  找到 {len(updates)} 个匹配的key")
        
        if dry_run:
            print(f"  [DRY RUN] 将更新以下条目:")
            for key, value in list(updates.items())[:5]:  # 只显示前5个
                print(f"    {key}: {value[:50]}...")
            if len(updates) > 5:
                print(f"    ... 还有 {len(updates) - 5} 个条目")
        else:
            # 更新文件内容
            updated_content = update_json_content(original_content, updates)
            
            # 写回文件
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"  ✓ 成功更新 {len(updates)} 个条目")
                total_updated += len(updates)
            except Exception as e:
                print(f"  ✗ 写入文件失败: {e}")
    
    if not dry_run:
        print(f"\n总计更新了 {total_updated} 个翻译条目")
    else:
        print(f"\n[DRY RUN] 预计将更新 {total_updated} 个翻译条目")

def main():
    parser = argparse.ArgumentParser(description='更新Mod翻译文件')
    parser.add_argument('--source', '-s', 
                       default='./en1end.json',
                       help='翻译源文件路径 (默认: ./en1end.json)')
    parser.add_argument('--mods', '-m',
                       default='./Mods',
                       help='Mods文件夹路径 (默认: ./Mods)')
    parser.add_argument('--dry-run', '-d',
                       action='store_true',
                       help='试运行模式，不实际修改文件')
    
    args = parser.parse_args()
    
    # 转换为绝对路径
    en1end_path = Path(args.source).resolve()
    mods_path = Path(args.mods).resolve()
    
    print("=== Stardew Valley Mod 翻译更新工具 ===")
    print(f"翻译源文件: {en1end_path}")
    print(f"Mods路径: {mods_path}")
    
    if args.dry_run:
        print("模式: 试运行 (不会修改文件)")
    else:
        print("模式: 实际更新")
    
    # 检查文件是否存在
    if not en1end_path.exists():
        print(f"错误：翻译源文件不存在: {en1end_path}")
        return
    
    # 执行更新
    update_translation_files(en1end_path, mods_path, args.dry_run)

if __name__ == "__main__":
    main()
