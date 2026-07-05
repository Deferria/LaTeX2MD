# 为 Markdown 转义字符添加 \，以便在 Markdown 中正确显示
import json

def escape_markdown(text: str) -> str:
    # 转义 Markdown 特殊字符
    return text.replace('~', '\\~').replace('`', '\\`').replace('|', '\\|')

def format(json_path: str) -> str:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    formatted = []
    for item in data:
        env = item.get('env', '')
        uuid = item.get('uuid', '')
        name = item.get('name', '')
        alias = item.get('alias', '')
        content = escape_markdown(item.get('content', ''))
        
        formatted.append({
            "env": env,
            "uuid": uuid,
            "name": name,
            "alias": alias,
            "content": content
        })
        
    return formatted

def json_to_json(json_path: str, formatted_json_path: str):
    formatted_content = format(json_path)
    with open(formatted_json_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_content, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    json_to_json('./extracted.json', './formatted.json')
        