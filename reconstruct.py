import json

from typing import Dict

# Based on the extracted JSON, this script will reconstruct the original LaTeX file. It is not guaranteed to be exactly the same as the original, but it should be functionally equivalent.

def reconstruct_str(info_dict: Dict[str, str]) -> str:
    env = info_dict.get('env', '')
    uuid = info_dict.get('uuid', '')
    name = info_dict.get('name', '')
    alias = info_dict.get('alias', '')
    contrib = info_dict.get('contrib', '')
    content = info_dict.get('content', '')

    # Reconstruct the LaTeX string
    if env == 'prf':
        reconstructed_str = f"\\begin{{{env}}}\n    {content}\n\\end{{{env}}}"
        
    elif env == 'rmk':
        reconstructed_str = f"\\begin{{{env}}}\n    [{contrib}]\n    {content}\n\\end{{{env}}}"
        
    else:
        if uuid is not None:
            if contrib is not None:
                if alias is not None:
                    reconstructed_str = f"\\begin{{{env}}}\n    [{uuid}]\n    {{{name}}}\n    [{alias}]\n    [{contrib}]\n    {content}\n\\end{{{env}}}"
                else:
                    reconstructed_str = f"\\begin{{{env}}}\n    [{uuid}]\n    {{{name}}}\n    []\n    [{contrib}]\n    {content}\n\\end{{{env}}}"
                    
            else:
                if alias is not None:
                    reconstructed_str = f"\\begin{{{env}}}\n    [{uuid}]\n    {{{name}}}\n    [{alias}]\n    {content}\n\\end{{{env}}}"
                else:
                    reconstructed_str = f"\\begin{{{env}}}\n    [{uuid}]\n    {{{name}}}\n    {content}\n\\end{{{env}}}"
                    
        else:
            if contrib is not None:
                if alias is not None:
                    reconstructed_str = f"\\begin{{{env}}}\n    {{{name}}}\n    [{alias}]\n    [{contrib}]\n    {content}\n\\end{{{env}}}"
                else:
                    reconstructed_str = f"\\begin{{{env}}}\n    {{{name}}}\n    []\n    [{contrib}]\n    {content}\n\\end{{{env}}}"
                    
            else:
                if alias is not None:
                    reconstructed_str = f"\\begin{{{env}}}\n    {{{name}}}\n    [{alias}]\n    {content}\n\\end{{{env}}}"
                else:
                    reconstructed_str = f"\\begin{{{env}}}\n    {{{name}}}\n    {content}\n\\end{{{env}}}"
                
    return reconstructed_str

def reconstruct_json(json_path: str, file_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    reconstructed_tex = []
    for item in data:
        reconstructed_tex.append(reconstruct_str(item))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(reconstructed_tex))