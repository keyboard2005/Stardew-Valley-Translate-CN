import json
import re
import os
from typing import Dict, Any

def load_name_mapping(name_file: str) -> Dict[str, str]:
    """加载NPC名字映射"""
    try:
        with open(name_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"错误: 找不到名字映射文件 {name_file}")
        return {}
    except json.JSONDecodeError as e:
        print(f"错误: 名字映射文件JSON解析失败 - {e}")
        return {}

def replace_names_in_text(text: str, name_mapping: Dict[str, str]) -> str:
    """替换文本中的NPC名字"""
    if not isinstance(text, str):
        return text
    
    result = text
    for english_name, chinese_name in name_mapping.items():
        # 使用单词边界来精确匹配名字，避免部分匹配
        pattern = r'\b' + re.escape(english_name) + r'\b'
        result = re.sub(pattern, chinese_name, result, flags=re.IGNORECASE)
    
    return result

def replace_names_in_json(data: Dict[str, Any], name_mapping: Dict[str, str]) -> Dict[str, Any]:
    """递归替换JSON中所有字符串值的NPC名字"""
    result = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # 替换字符串值中的名字
            result[key] = replace_names_in_text(value, name_mapping)
        elif isinstance(value, dict):
            # 递归处理嵌套字典
            result[key] = replace_names_in_json(value, name_mapping)
        elif isinstance(value, list):
            # 处理列表
            result[key] = [
                replace_names_in_text(item, name_mapping) if isinstance(item, str) else item
                for item in value
            ]
        else:
            # 保持其他类型不变
            result[key] = value
    
    return result

def process_name_replacement(input_file: str, output_file: str, name_mapping_file: str):
    """处理名字替换的主函数"""
    try:
        # 加载名字映射
        name_mapping = load_name_mapping(name_mapping_file)
        if not name_mapping:
            print("没有找到有效的名字映射，退出处理")
            return
        
        print(f"加载了 {len(name_mapping)} 个名字映射:")
        for eng, chi in name_mapping.items():
            print(f"  {eng} -> {chi}")
        
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 替换名字
        processed_data = replace_names_in_json(data, name_mapping)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=2)
        
        print(f"名字替换完成: {input_file} -> {output_file}")
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_file}")
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 - {e}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    # 示例使用
    input_file = "translations/TenebrousNova.EliDylan.CP/zh.json"
    output_file = "translations/TenebrousNova.EliDylan.CP/zh_named.json"
    name_mapping_file = "npc_name.json"
    
    process_name_replacement(input_file, output_file, name_mapping_file)