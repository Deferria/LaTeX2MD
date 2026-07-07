# extract contents from the TeX environments
# TeX -> JSON
import re
import json

from typing import List, Callable, Literal

# This is an ANNOYING constraint: Your TeX envs must be indented by 2*4 spaces and the inner content must be indented by 3*4 spaces. Otherwise, the extraction will fail.
# There are no both easy and feasible solutions.
basic_ptn = re.compile(r'\s{8}\\begin\{(.+)\}\n\s{12}([\s\S]*?)\n\s{8}\\end\{(.*?)\}')
content_ptn_0 = re.compile(r"^\[(.*?)\]\n\s+\{(.*?)\}\n\s+\[(.*?)\]\n\s+\[(.*?)\]\n\s+([\s\S]+)")
content_ptn_1 = re.compile(r"^\[(.*?)\]\n\s+\{(.*?)\}\n\s+\[(.*?)\]\n\s+([\s\S]+)")
content_ptn_2 = re.compile(r"^\[(.*?)\]\n\s+\{(.*?)\}\n\s+([\s\S]+)")
content_ptn_6 = re.compile(r"^\{(.*?)\}\n\s+\[(.*?)\]\n\s+\[(.*?)\]\n\s+([\s\S]+)")
content_ptn_3 = re.compile(r"^\{(.*?)\}\n\s+\[(.*?)\]\n\s+([\s\S]+)")
content_ptn_4 = re.compile(r"^\{(.*?)\}\n\s+([\s\S]+)")
content_ptn_7 = re.compile(r"^\{(.*?)\}")
content_ptn_5 = re.compile(r"^\[(.*?)\]\n\s+([\s\S]+)")

def basic_appender(envname: str, uuid: str, name: str, alias: str, contrib: str, content: str) -> dict:
    return {
        "env": envname,
        "uuid": uuid,
        "name": name,
        "alias": alias,
        "contrib": contrib,
        "content": content
    }

def extract(tex: str, append_option: Callable[[str, str, str, str, str, str], dict]) -> List[str]:
    formatted = []
    for m in basic_ptn.finditer(tex):
        env_name, raw_content, _ = m.groups()
        #print(f"Extracting from environment: {env_name}")
        
        if content_ptn_0.match(raw_content):
            uuid, name1, name2, name_3, content = content_ptn_0.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append(append_option(env_name, uuid, name1, name2, name_3, content))
            
        elif content_ptn_1.match(raw_content):
            uuid, name1, name2, content = content_ptn_1.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append(append_option(env_name, uuid, name1, name2, None, content))
            
        elif content_ptn_2.match(raw_content):
            uuid, name1, content = content_ptn_2.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append(append_option(env_name, uuid, name1, None, None, content))
            
        elif content_ptn_6.match(raw_content):
            name1, name2, name_3, content = content_ptn_6.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append(append_option(env_name, None, name1, name2, name_3, content))
            
        elif content_ptn_3.match(raw_content):
            name1, name2, content = content_ptn_3.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append(append_option(env_name, None, name1, name2, None, content))
            
        elif content_ptn_4.match(raw_content):
            name1, content = content_ptn_4.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append(append_option(env_name, None, name1, None, None, content))
            
        elif content_ptn_7.match(raw_content):
            name1 = content_ptn_7.match(raw_content).groups()
            formatted.append(append_option(env_name, None, name1, None, None, ''))
            
        elif content_ptn_5.match(raw_content):
            name1, content = content_ptn_5.match(raw_content).groups()
            content = content.replace(' '*4, '')
            formatted.append(append_option(env_name, None, None, None, name1, content))
            
        else:
            formatted.append(append_option(env_name, None, None, None, None, raw_content.replace(' '*4, '')))

    return formatted

def extract_json(tex_path: str, json_path: str):
    with open(tex_path, 'r', encoding='utf-8') as f:
        tex = f.read()
    formatted = extract(tex, append_option=basic_appender)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(formatted, f, ensure_ascii=False, indent=4)
