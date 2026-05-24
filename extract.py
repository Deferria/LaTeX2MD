# extract contents from the TeX environments
# TeX -> JSON
import re
import json

from typing import List, Literal

basic_ptn = re.compile(r'\s{8}\\begin\{(.+)\}\n\s{12}([\s\S]*?)\n\s{8}\\end\{(.*?)\}')
content_ptn_1 = re.compile(r"^\[(.*?)\]\n\s+\{(.*?)\}\n\s+\[(.*?)\]\n\s+([\s\S]+)")
content_ptn_2 = re.compile(r"^\[(.*?)\]\n\s+\{(.*?)\}\n\s+([\s\S]+)")
content_ptn_3 = re.compile(r"^\{(.*?)\}\n\s+\[(.*?)\]\n\s+([\s\S]+)")
content_ptn_4 = re.compile(r"^\{(.*?)\}\n\s+([\s\S]+)")
content_ptn_5 = re.compile(r"^\[(.*?)\]\n\s+([\s\S]+)")

def extract(tex: str) -> List[str]:
    formatted = []
    for m in basic_ptn.finditer(tex):
        env_name, raw_content, _ = m.groups()
        #print(f"Extracting from environment: {env_name}")
        
        if content_ptn_1.match(raw_content):
            uuid, name1, name2, content = content_ptn_1.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append({
                "env": env_name,
                "uuid": uuid,
                "name": name1,
                "alias": name2,
                "content": content
            })
            
        elif content_ptn_2.match(raw_content):
            uuid, name1, content = content_ptn_2.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append({
                "env": env_name,
                "uuid": uuid,
                "name": name1,
                "alias": None,
                "content": content
            })
            
        elif content_ptn_3.match(raw_content):
            name1, name2, content = content_ptn_3.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append({
                "env": env_name,
                "uuid": None,
                "name": name1,
                "alias": name2,
                "content": content
            })
            
        elif content_ptn_4.match(raw_content):
            name1, content = content_ptn_4.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append({
                "env": env_name,
                "uuid": None,
                "name": name1,
                "alias": None,
                "content": content
            })
            
        elif content_ptn_5.match(raw_content):
            name1, content = content_ptn_5.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append({
                "env": env_name,
                "uuid": None,
                "name": None,
                "alias": None,
                "content": content
            })
            
        else:
            formatted.append({
                "env": env_name,
                "uuid": None,
                "name": None,
                "alias": None,
                "content": raw_content.replace(' '*4, '')
            })

    return formatted

def to_json(tex_path: str, json_path: str):
    with open(tex_path, 'r', encoding='utf-8') as f:
        tex = f.read()
    formatted = extract(tex)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(formatted, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    to_json('./for_testing.txt', './extracted.json')