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

async def translate_text_ai(text: str, model: str = "claude-sonnet-4-20250514") -> str:
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

def load_existing_translations(output_path: str) -> Dict[str, Any]:
    """加载已存在的翻译文件"""
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():
                    return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"读取已存在翻译文件失败: {e}")
    return {}

def merge_translations(existing: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
    """合并已存在的翻译和新数据，保留已翻译的内容"""
    merged = existing.copy()
    
    for key, value in new_data.items():
        if key not in merged:
            merged[key] = value
        elif isinstance(value, dict) and isinstance(merged[key], dict):
            # 递归合并嵌套字典
            merged[key] = merge_translations(merged[key], value)
        elif isinstance(value, list) and isinstance(merged[key], list):
            # 合并列表，保持原有长度
            if len(merged[key]) < len(value):
                merged[key].extend(value[len(merged[key]):])
    
    return merged

def get_untranslated_items(source_data: Dict[str, Any], existing_translations: Dict[str, Any]) -> Dict[str, Any]:
    """获取需要翻译的项目（排除已翻译的）"""
    untranslated = {}
    
    for key, value in source_data.items():
        if isinstance(value, str):
            # 如果不存在翻译或翻译为空，则需要翻译
            if key not in existing_translations or not existing_translations[key].strip():
                untranslated[key] = value
        elif isinstance(value, dict):
            if key not in existing_translations:
                existing_translations[key] = {}
            nested_untranslated = get_untranslated_items(value, existing_translations[key])
            if nested_untranslated:
                untranslated[key] = nested_untranslated
        elif isinstance(value, list):
            if key not in existing_translations:
                existing_translations[key] = []
            
            # 确保已存在的列表长度足够
            while len(existing_translations[key]) < len(value):
                existing_translations[key].append("")
            
            untranslated_list = []
            for i, item in enumerate(value):
                if isinstance(item, str):
                    if i >= len(existing_translations[key]) or not existing_translations[key][i].strip():
                        untranslated_list.append(item)
                    else:
                        untranslated_list.append(None)  # 标记为已翻译
                else:
                    untranslated_list.append(item)
            
            # 只有包含需要翻译的项目时才添加
            if any(item is not None and isinstance(item, str) for item in untranslated_list):
                untranslated[key] = untranslated_list
    
    return untranslated

async def translate_json_values_async(data: Dict[str, Any], output_path: str, model: str = "gpt-4o", max_concurrent: int = 5) -> Dict[str, Any]:
    """异步递归翻译JSON中的所有字符串值，真正实时写入，支持并发，支持增量翻译"""
    
    # 加载已存在的翻译
    existing_translations = load_existing_translations(output_path)
    print(f"已加载 {len(existing_translations)} 个已存在的翻译条目")
    
    # 获取需要翻译的项目
    untranslated_data = get_untranslated_items(data, existing_translations)
    
    if not untranslated_data:
        print("所有条目已翻译完成，无需重新翻译")
        return existing_translations
    
    print(f"发现 {len(untranslated_data)} 个需要翻译的条目")
    
    # 初始化翻译结果为已存在的翻译
    translated = existing_translations.copy()
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 创建信号量限制并发数
    semaphore = asyncio.Semaphore(max_concurrent)
    # 创建文件写入锁
    write_lock = asyncio.Lock()
    
    async def translate_and_save(text: str, key: str) -> str:
        """翻译并实时保存单个条目"""
        async with semaphore:
            result = await translate_text_ai(text, model)
            
            # 实时写入文件
            async with write_lock:
                translated[key] = result
                with open(output_path, 'w', encoding='utf-8') as file:
                    json.dump(translated, file, ensure_ascii=False, indent=2)
                print(f"已保存进度: {key}")
            
            return result
    
    # 处理所有需要翻译的数据项
    tasks = []
    for key, value in untranslated_data.items():
        if isinstance(value, str):
            # 创建翻译任务
            task = asyncio.create_task(translate_and_save(value, key))
            tasks.append((key, task))
        elif isinstance(value, dict):
            # 递归处理嵌套字典
            if key not in translated:
                translated[key] = {}
            nested_result = await translate_json_values_async(value, output_path, model, max_concurrent)
            translated[key].update(nested_result)
        elif isinstance(value, list):
            # 处理列表
            if key not in translated:
                translated[key] = []
            
            # 确保列表长度足够
            while len(translated[key]) < len(value):
                translated[key].append("")
            
            list_tasks = []
            for i, item in enumerate(value):
                if isinstance(item, str) and item is not None:  # None表示已翻译
                    async def translate_list_item(text, index, list_key):
                        async with semaphore:
                            result = await translate_text_ai(text, model)
                            
                            # 实时更新列表并写入文件
                            async with write_lock:
                                translated[list_key][index] = result
                                with open(output_path, 'w', encoding='utf-8') as file:
                                    json.dump(translated, file, ensure_ascii=False, indent=2)
                                print(f"已保存列表进度: {list_key}[{index}]")
                            
                            return result
                    
                    task = asyncio.create_task(translate_list_item(item, i, key))
                    list_tasks.append(task)
            
            # 等待所有列表项翻译完成
            if list_tasks:
                await asyncio.gather(*list_tasks)
    
    # 等待所有主要任务完成
    if tasks:
        for key, task in tasks:
            await task
    
    return translated

async def process_json_file_async(input_path: str, output_path: str, model: str = "gpt-4o", max_concurrent: int = 5):
    """异步处理JSON文件：读取、翻译、写入"""
    try:
        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 移除注释
        clean_content = remove_json_comments(content)
        
        # 解析JSON
        data = json.loads(clean_content)
        
        print(f"开始翻译，最大并发数: {max_concurrent}")
        
        # 异步翻译所有值（实时写入，并发执行）
        translated_data = await translate_json_values_async(data, output_path, model, max_concurrent)
        
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

def translate_json_file(input_path: str, output_path: str, model: str = "gpt-4o", max_concurrent: int = 5):
    """处理JSON文件：读取、翻译、写入"""
    asyncio.run(process_json_file_async(input_path, output_path, model, max_concurrent))

if __name__ == "__main__":
    # 示例使用
    input_file = "translations/TenebrousNova.EliDylan.CP/default.json"
    output_file = "translations/TenebrousNova.EliDylan.CP/zh.json"
    
    # 使用并发翻译，可以调整max_concurrent参数控制并发数
    translate_json_file(input_file, output_file, model="gpt-4o", max_concurrent=10)