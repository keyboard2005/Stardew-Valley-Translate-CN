#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON文件合并工具
将default_all.json中存在但zh_all.json中不存在的键值对追加到zh_all.json中
"""

import json
import os
from typing import Dict, Any

def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    加载JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        解析后的JSON数据字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        return {}
    except json.JSONDecodeError as e:
        print(f"错误: 文件 '{file_path}' JSON格式错误: {e}")
        return {}
    except Exception as e:
        print(f"错误: 读取文件 '{file_path}' 时发生错误: {e}")
        return {}

def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """
    保存JSON文件
    
    Args:
        file_path: 要保存的文件路径
        data: 要保存的数据字典
        
    Returns:
        保存是否成功
    """
    try:
        # 创建备份文件
        backup_path = file_path + '.backup'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as src, \
                 open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        
        # 保存新文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"成功保存文件: {file_path}")
        print(f"备份文件: {backup_path}")
        return True
    except Exception as e:
        print(f"错误: 保存文件 '{file_path}' 时发生错误: {e}")
        return False

def merge_json_files(default_file: str, target_file: str) -> bool:
    """
    合并JSON文件
    将default_file中存在但target_file中不存在的键值对追加到target_file中
    
    Args:
        default_file: 源文件路径 (default_all.json)
        target_file: 目标文件路径 (zh_all.json)
        
    Returns:
        合并是否成功
    """
    print("正在加载JSON文件...")
    
    # 加载两个JSON文件
    default_data = load_json_file(default_file)
    target_data = load_json_file(target_file)
    
    if not default_data:
        print(f"错误: 无法加载源文件 '{default_file}'")
        return False
    
    if not target_data:
        print(f"警告: 目标文件 '{target_file}' 为空或不存在，将创建新文件")
        target_data = {}
    
    print(f"源文件包含 {len(default_data)} 个键")
    print(f"目标文件包含 {len(target_data)} 个键")
    
    # 找出需要添加的键
    missing_keys = []
    for key in default_data:
        if key not in target_data:
            missing_keys.append(key)
    
    if not missing_keys:
        print("✅ 所有键都已存在，无需添加")
        return True
    
    print(f"发现 {len(missing_keys)} 个缺失的键")
    
    # 询问用户是否继续
    while True:
        choice = input(f"是否要将这 {len(missing_keys)} 个键添加到目标文件？ (y/n/s): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            break
        elif choice in ['n', 'no', '否']:
            print("用户取消操作")
            return False
        elif choice in ['s', 'show', '显示']:
            print("\n缺失的键（前10个）:")
            for i, key in enumerate(missing_keys[:10]):
                print(f"  {i+1}. {key}: {default_data[key]}")
            if len(missing_keys) > 10:
                print(f"  ... 还有 {len(missing_keys) - 10} 个键")
            print()
        else:
            print("请输入 y(是), n(否), 或 s(显示缺失的键)")
    
    # 添加缺失的键值对
    print("正在添加缺失的键值对...")
    added_count = 0
    
    for key in missing_keys:
        target_data[key] = default_data[key]
        added_count += 1
    
    # 保存更新后的文件
    if save_json_file(target_file, target_data):
        print(f"✅ 成功添加 {added_count} 个键值对到 '{target_file}'")
        print(f"目标文件现在包含 {len(target_data)} 个键")
        return True
    else:
        return False

def main():
    """主函数"""
    print("=== JSON文件合并工具 ===")
    print("将default_all.json中缺失的键值对添加到zh_all.json中\n")
    
    # 文件路径
    default_file = "default_all.json"
    target_file = "zh_all.json"
    
    # 检查文件是否存在
    if not os.path.exists(default_file):
        print(f"错误: 源文件 '{default_file}' 不存在")
        return
    
    print(f"源文件: {default_file}")
    print(f"目标文件: {target_file}")
    print()
    
    # 执行合并操作
    success = merge_json_files(default_file, target_file)
    
    if success:
        print("\n🎉 合并操作完成！")
    else:
        print("\n❌ 合并操作失败")

if __name__ == "__main__":
    main()
