# JSON -> Markdown
import json

env_to_md = {
    'dfn': '定义',
    'rmk': '注',
    'thm': '定理',
    'ppt': '性质',
    'crl': '推论',
    'prf': '证明',
    'xmp': '例',
    'ins': '实例',
    'cxmp': '反例',
    'intrormk': '引入',
    'vardfn': '\\*定义',
    'varthm': '\\*定理',
}

label_prefix = {
    'dfn': 'dfn',
    'thm': 'thm',
    'ppt': 'ppt',
    'crl': 'crl',
    'xmp': 'xmp',
    'ins': 'xmp',
    'cxmp': 'cxmp',
    'vardfn': 'dfn',
    'varthm': 'thm',
}

def display(json_path: str) -> str:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    markdown = []
    for item in data:
        content = item.get('content', '')
        if item['env'] == "rmk":
            markdown.append(f"> *{env_to_md.get(item['env'], item['env'])}*: {content.replace('\n', '\n> ')}")
        elif item['env'] == "prf":
            markdown.append(f"> *{env_to_md.get(item['env'], item['env'])}*: {content.replace('\n', '\n> ')}")
            
        else:
            disp_str = f"#### {env_to_md.get(item['env'], item['env'])}: {item['name']}"
            if item['alias']:
                disp_str += f" ({item['alias']})"
                
            if item['uuid']:
                disp_str += f" <span id=\"{label_prefix.get(item['env'], item['env'])}:{item['uuid']}\"></span>"
                
            disp_str += f"\n\n{item['content']}"
            markdown.append(disp_str)

    return markdown

def to_markdown(json_path: str, md_path: str):
    markdown_content_list = display(json_path)
    markdown_content = '\n\n'.join(markdown_content_list)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == '__main__':
    to_markdown('./formatted.json', './output.md')