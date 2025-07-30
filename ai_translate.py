import json
import re
import os
import asyncio
from typing import Dict, Any
from openai import AsyncOpenAI
import openai
import dotenv

# 加载环境变量
dotenv.load_dotenv()

# 初始化OpenAI客户端
openai_client = AsyncOpenAI(
    api_key=os.getenv("TOKEN"),
    base_url=os.getenv("BASE_URL")
)

def remove_json_comments(json_string: str) -> str:
    """移除JSON字符串中的注释"""
    # 移除单行注释 // ...
    json_string = re.sub(r'//.*?$', '', json_string, flags=re.MULTILINE)
    # 移除多行注释 /* ... */
    json_string = re.sub(r'/\*.*?\*/', '', json_string, flags=re.DOTALL)
    return json_string

async def translate_text_ai(text: str, model: str = "aws/claude-opus-4-20250514") -> str:
    """使用AI翻译文本到中文"""
    if not text.strip():
        return text
    
    try:
        response = await openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的游戏汉化i18n英文到中文翻译器 游戏是星露谷物语。请将用户提供的英文文本翻译成自然流畅的中文。保持原文的语气和风格，特别注意游戏文本的表达习惯。对于包含特殊符号（如$1, $2等）的文本，请保持这些符号不变。重要：只返回翻译结果，不要添加任何解释、说明或其他文字。"},
                {"role": "user", "content": text}
            ]
        )
        translated = response.choices[0].message.content.strip()
        print(f"翻译: {text} -> {translated}")
        return translated
        
    except openai.BadRequestError as e:
        print(f"翻译请求错误: {str(e)}")
        return text
    except Exception as e:
        print(f"翻译发生错误: {str(e)}")
        return text

def translate_text(text: str) -> str:
    """翻译文本到中文 - 同步包装器"""
    return asyncio.run(translate_text_ai(text))

def translate_json_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """递归翻译JSON中的所有字符串值"""
    translated = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # 翻译字符串值
            translated[key] = translate_text(value)
        elif isinstance(value, dict):
            # 递归处理嵌套字典
            translated[key] = translate_json_values(value)
        elif isinstance(value, list):
            # 处理列表
            translated[key] = [
                translate_text(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            # 保持其他类型不变
            translated[key] = value
    
    return translated

async def translate_json_values_async(data: Dict[str, Any], output_path: str, model: str = "gpt-4o") -> Dict[str, Any]:
    """异步递归翻译JSON中的所有字符串值，实时写入"""
    translated = {}
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    for key, value in data.items():
        if isinstance(value, str):
            # 异步翻译字符串值
            translated[key] = await translate_text_ai(value, model)
            # 实时写入当前翻译结果
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(translated, file, ensure_ascii=False, indent=2)
            print(f"已保存进度: {key}")
        elif isinstance(value, dict):
            # 递归处理嵌套字典
            translated[key] = await translate_json_values_async(value, output_path, model)
        elif isinstance(value, list):
            # 处理列表
            translated_list = []
            for i, item in enumerate(value):
                if isinstance(item, str):
                    translated_item = await translate_text_ai(item, model)
                    translated_list.append(translated_item)
                    # 更新列表进度并写入
                    translated[key] = translated_list + value[i+1:]  # 包含未翻译的项目
                    with open(output_path, 'w', encoding='utf-8') as file:
                        json.dump(translated, file, ensure_ascii=False, indent=2)
                    print(f"已保存列表进度: {key}[{i}]")
                else:
                    translated_list.append(item)
            translated[key] = translated_list
        else:
            # 保持其他类型不变
            translated[key] = value
    
    return translated

async def process_json_file_async(input_path: str, output_path: str, model: str = "gpt-4o"):
    """异步处理JSON文件：读取、翻译、写入"""
    try:
        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 移除注释
        clean_content = remove_json_comments(content)
        
        # 解析JSON
        data = json.loads(clean_content)
        
        # 异步翻译所有值（实时写入）
        translated_data = await translate_json_values_async(data, output_path, model)
        
        # 最终写入完整结果
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(translated_data, file, ensure_ascii=False, indent=2)
        
        print(f"翻译完成: {input_path} -> {output_path}")
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_path}")
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 - {e}")
    except Exception as e:
        print(f"错误: {e}")

def translate_json_file(input_path: str, output_path: str, model: str = "gpt-4o"):
    """处理JSON文件：读取、翻译、写入"""
    asyncio.run(process_json_file_async(input_path, output_path, model))

if __name__ == "__main__":
    # 示例使用
    input_file = "translations/TenebrousNova.EliDylan.CP/default.json"
    output_file = "translations/TenebrousNova.EliDylan.CP/zh.json"
    
    # 使用 gpt-4o 模型
    translate_json_file(input_file, output_file, model="gpt-4o")