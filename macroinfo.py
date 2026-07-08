import re

from typing import List, Tuple, Callable, Dict, Any

"""
This script is used to extract the defined macros and commands from a TeX file.
"""

def escape_special_chars(text: str) -> str:
    """
    Escape special characters in the given text.

    Args:
        text (str): The input text.
    """
    special_chars = ['\\', '{', '}', '[', ']', '(', ')', '$', '^', '_', '&', '%', '#']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return rf'{text}'

def get_command(tex: str) -> List[List[Any]]:
    """
    Extract the defined commands from the given TeX string.

    Args:
        tex (str): The input TeX string.
    """
    newcommand_ptn : re.Pattern[str] = re.compile(r'\\newcommand\{\\(.*?)\}\{(.+)\}')
    
    cmd_list_raw : List[Tuple[str,str]] = re.findall(newcommand_ptn, tex)
    cmd_list : List[List[Any]] = [['\\' + cmd[0] + '{}', cmd[1], 'string'] for cmd in cmd_list_raw]
    return cmd_list

def get_command_from_file(tex_path: str) -> List[List[Any]]:
    """
    Extract the defined commands from the given TeX file.

    Args:
        tex_path (str): The path to the input TeX file.
    """
    with open(tex_path, 'r', encoding='utf-8') as f:
        tex = f.read()
    return get_command(tex)