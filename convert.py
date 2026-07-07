import json
import re
    
from typing import List, Tuple, Callable

def escape_markdown(text: str) -> str:
    return text.replace('~', '\\~').replace('`', '\\`').replace('|', '\\|')

def enumerate_join_items(items: List[str]) -> str:
    enumerated_items = [str(i+1) + '. ' + item.strip() for i, item in enumerate(items)]
    return '\n'.join(enumerated_items)

def itemize_join_items(items: List[str]) -> str:
    itemized_items = ['- ' + item.strip() for item in items]
    return '\n'.join(itemized_items)

def escape_enumitem(text: str, envname: str, env_callback: Callable[[List[str]], str]) -> Tuple[str, str]:
    env_pattern = r'\\begin\{' + envname + r'\}(?:\[(.*?)\])?\s*(.*?)\\end\{' + envname + r'\}'
    if re.search(env_pattern, text, re.DOTALL):
        opt, body = re.search(env_pattern, text, re.DOTALL).groups()
        item_pattern = r'\\item\s*(.*?)(?=\\item|\Z)'
        items = re.findall(item_pattern, body, re.DOTALL)
        item_str = env_callback(items)
        return opt, item_str
    else:
        return '', text

def convert(json_path: str) -> str:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    formatted = []
    for item in data:
        env = item.get('env', '')
        uuid = item.get('uuid', '')
        name = item.get('name', '')
        alias = item.get('alias', '')
        content_1 = escape_markdown(item.get('content', ''))
        content_2 = escape_enumitem(content_1, 'enumerate', enumerate_join_items)[1]
        content_3 = escape_enumitem(content_2, 'itemize', itemize_join_items)[1]
        
        formatted.append({
            "env": env,
            "uuid": uuid,
            "name": name,
            "alias": alias,
            "content": content_3
        })

    return formatted

def convert_json(json_path: str, formatted_json_path: str):
    formatted_content = convert(json_path)
    with open(formatted_json_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_content, f, ensure_ascii=False, indent=4)
