import regex
import json

from typing import Callable, List, Literal

"""
Replace some LaTeX commands with their Markdown equivalents in a given text. 

The order should be:

1. Primitive LaTeX markups (e.g. \\textbf{})
2. Math operators in other LaTeX packages (e.g. \\norm{}). They might be nested, so we need to use recursive regex patterns.
3. Declared math operators in the preamble (e.g. \\N, \\R, \\C, etc.)
4. Hyperlinks (e.g. \\hyperref[sec:label]{text}). **They must be substituted last!**
    
"""

def replace_math_operator(text: str, source: str | List[str], target: str | List[str], mode: Literal['normal', 'recursive', "legacy", "simple", "isolated"] = 'normal') -> str:
    """
    Replace math operators in the given text with their Markdown equivalents.

    Args:
        text (str): The input text containing LaTeX commands.
        source (str | List[str]): The source string(s) to be replaced.
        target (str | List[str]): The replacement pattern(s).
        mode (Literal['normal', 'recursive', "legacy", "simple", "isolated"]): The mode of replacement. 
            'normal' for parametered non-nested patterns, 'recursive' for nested patterns, "legacy" for legacy patterns, "simple" for simple patterns (with no parameters), and "isolated" for simple patterns that are not part of a larger word.
    """
    
    if mode == 'normal':
        if isinstance(source, str):
            pattern = source + r'\{(.*?)\}'
        elif isinstance(source, List):
            pattern = source[0] + r'\{(.*?)\}' + source[1]
        
        if isinstance(target, List):
            target_pattern = target[0] + r'\1' + target[1]
            return regex.sub(pattern, target_pattern, text)
        elif isinstance(target, str):
            target_pattern = target + '{' + r'\1' + '}'
            return regex.sub(pattern, target_pattern, text)
        else:
            raise ValueError("Target must be a string or a list of strings.")
        
    elif mode == 'recursive':
        if isinstance(source, str):
            pattern = source + r"\{(?P<arg>(?:[^{}]+|\{(?P>arg)\})*)\}"
        elif isinstance(source, List):
            pattern = source[0] + r"(?P<arg>(?:[^{}]+|\{(?P>arg)\})*)" + source[1]
            
        pattern = regex.compile(pattern)
        
        if isinstance(target, List):
            target_1, target_2 = target[0], target[1]
            while pattern.search(text):
                text = pattern.sub(target_1 + r'\g<arg>' + target_2, text)
            return text
        elif isinstance(target, str):
            while pattern.search(text):
                text = pattern.sub(target + r'{\g<arg>}', text)
            return text
        else:
            raise ValueError("Target must be a string or a list of strings.")
        
    elif mode == 'legacy':
        assert isinstance(source, str), "Source must be a string for legacy mode."
        pattern = source + r"(\{(?:[^{}]+|(?1))*\})"
        
        if isinstance(target, str):    
            return regex.sub(pattern, lambda m: target + '{' + m.group(1)[1:-1] + '}', text)
        elif isinstance(target, List):
            target_1, target_2 = target[0], target[1]
            return regex.sub(pattern, lambda m: target_1 + m.group(1)[1:-1] + target_2, text)
        else:
            raise ValueError("Target must be a string or a list of strings.")
        
    elif mode == 'simple':
        assert type(target) is str, "Target must be a string for simple mode."
        return regex.sub(source, target, text)
    
    elif mode == 'isolated':
        assert type(target) is str, "Target must be a string for isolated mode."
        pattern = source + r'(?![a-zA-Z0-9])'
        return regex.sub(pattern, target, text)
    
    else:
        raise ValueError("Mode must be one of 'normal', 'recursive', 'legacy', 'simple', or 'isolated'.")
    
TASK_LIST = [
    [r"\\norm", [r'\\left\\lVert ', r' \\right\\rVert'], 'recursive'],
    [r"\\abs", [r'\\left\\lvert ', r' \\right\\rvert'], 'recursive'],
    [r"\\textbf", [r'**', r'**'], 'normal'],
    [r"\\textit", [r'*', r'*'], 'normal'],
    [r"\\dd", [r'\\mathrm{d} ', ' '], 'normal'],
    [r"\\expval", [r'\\left\\langle ', r'\\right\\rangle '], 'recursive'],
    [r"\\N", r'\\mathbb{N} ', 'isolated'],
    [r"\\Z", r'\\mathbb{Z} ', 'isolated'],
    [r"\\Q", r'\\mathbb{Q} ', 'isolated'],
    [r"\\R", r'\\mathbb{R} ', 'isolated'],
    [r"\\C", r'\\mathbb{C} ', 'isolated'],
    [r"\\F", r'\\mathbb{F} ', 'isolated'],
    [r"\\D", r'\\mathbb{D} ', 'isolated'],
    [r"\\B", r'\\mathcal{B} ', 'isolated'],
    [r"\\\\", r'\n', 'simple'],
    [r"\\tcbline", r'\n---\n', 'simple'],
    [r"\\ii", r'\\mathrm{i} ', 'isolated'],
    [r"\\dist", r'\\operatorname{dist} ', 'simple'],
    [r"\\spn", r'\\operatorname{span} ', 'simple'],
    [r"\\card", r'\\operatorname{card} ', 'simple'],
    [r"\\interior", r'\\operatorname{int} ', 'simple'],
    [r"\\img", r'\\operatorname{im} ', 'simple'],
    [r"\\esssum", r'\\operatorname*{esssum} ', 'simple'],
    [r"\\mlim", r'\\xrightarrow{m} ', 'simple'],
    [r"\\wlim", r'\\xrightarrow{w} ', 'simple'],
    [r"\\wslim", r'\\xrightarrow{w^*} ', 'simple'],
    [r"\\aelim", r'\\xrightarrow{\\text{a.e.}} ', 'simple'],
    [r"\\st", r'\\text{s.t. } ', 'isolated'],
    [r"\\blo", r'\\mathscr{B} ', 'isolated'],
    [r"\\cpt", r'\\mathscr{K} ', 'isolated'],
    [r"\\fnrank", r'\\mathscr{F} ', 'isolated'],
    [r"\\Cont", r'\\mathrm{C} ', 'isolated'],
    [r"\\Lp", r'\\mathrm{L} ', 'isolated'],
    [r"\\ordinal", r'\\mathbb{O} ', 'simple'],
    [r"\\qty", [r'\\left\\{ ', r' \\right\\}'], 'recursive'],
    [[r"\\qty\(", r"\)"], [r'\\left( ', r' \\right)'], 'recursive'],
    [[r"\\qty\[", r"\]"], [r'\\left[ ', r' \\right]'], 'recursive'],
    [r"\\implies", r'\\Rightarrow ', 'simple'],
    [r"\\iff", r'\\Leftrightarrow ', 'simple'],
    [r"\\impliedby", r'\\Leftarrow ', 'simple'],
]

def replace_hyperref(text):
    pattern = r'\\hyperref\[(.*?)\]\{(.*?)\}'
    
    return regex.sub(pattern, r'[\2](#\1)', text)


def replace_all(text: str) -> str:
    """
    Replace all LaTeX commands in the given text with their Markdown equivalents.
    """
    for task in TASK_LIST:
        text = replace_math_operator(text, task[0], task[1], task[2])
        
    text = replace_hyperref(text)
        
    return text

def replace_json(json_path: str, output_json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        #print(type(item))
        item['content'] = replace_all(item['content'])
        #print(f"Processed {i+1}/{n} items.")
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)