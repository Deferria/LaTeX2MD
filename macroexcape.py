import regex
import json

def replace_norm_recursive(text):
    pattern = r'\\norm(\{(?:[^{}]+|(?1))*\})'
    
    return regex.sub(pattern, lambda m: r'\left\lVert ' + m.group(1)[1:-1] + r' \right\rVert', text)

def replace_abs_recursive(text):
    pattern = r'\\abs(\{(?:[^{}]+|(?1))*\})'
    
    return regex.sub(pattern, lambda m: r'\left\lvert ' + m.group(1)[1:-1] + r' \right\rvert', text)

def replace_textbf(text):
    pattern = r'\\textbf\{(.*?)\}'
    
    return regex.sub(pattern, r'**\1**', text)

def replace_textit(text):
    pattern = r'\\textit\{((?:[^{}]+|\{(?R)\})*)\}'
    
    return regex.sub(pattern, r'*\1*', text)

def replace_dd(text):
    pattern = r'\\dd(\{(?:[^{}]+|(?1))*\})'
    
    return regex.sub(pattern, lambda m: r'\\mathrm{d}\{' + m.group(1)[1:-1] + r'\}', text)

def replace_N(text):
    pattern = r'\\N(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathbb{N} ', text)

def replace_Z(text):
    pattern = r'\\Z(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathbb{Z} ', text)

def replace_Q(text):
    pattern = r'\\Q(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathbb{Q} ', text)

def replace_R(text):
    pattern = r'\\R(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathbb{R} ', text)

def replace_C(text):
    pattern = r'\\C(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathbb{C} ', text)

def replace_F(text):
    pattern = r'\\F(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathbb{F} ', text)

def replace_D(text):
    pattern = r'\\D(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathbb{D} ', text)

def replace_B(text):
    pattern = r'\\B(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathcal{B} ', text)

def replace_newline(text):
    pattern = r'\\\\'
    
    return regex.sub(pattern, r'\n', text)

def replace_tcbline(text):
    pattern = r'\\tcbline'
    
    return regex.sub(pattern, r'\n---\n', text)

def replace_i(text):
    pattern = r'\\ii(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathrm{i} ', text)

def replace_op_distance(text):
    pattern = r'\\dist'
    
    return regex.sub(pattern, r'\\operatorname{dist} ', text)

def replace_op_span(text):
    pattern = r'\\spn'
    
    return regex.sub(pattern, r'\\operatorname{span} ', text)

def replace_op_card(text):
    pattern = r'\\card'
    
    return regex.sub(pattern, r'\\operatorname{card} ', text)

def replace_op_intr(text):
    pattern = r'\\interior'
    
    return regex.sub(pattern, r'\\operatorname{int} ', text)

def replace_op_im(text):
    pattern = r'\\img'
    
    return regex.sub(pattern, r'\\operatorname{im} ', text)

def replace_op_esssum(text):
    pattern = r'\\esssum'
    
    return regex.sub(pattern, r'\\operatorname*{esssum} ', text)

def replace_mlim(text):
    pattern = r'\\mlim'
    
    return regex.sub(pattern, r'\\xrightarrow{m} ', text)

def replace_wlim(text):
    pattern = r'\\wlim'
    
    return regex.sub(pattern, r'\\xrightarrow{w} ', text)

def replace_wslim(text):
    pattern = r'\\wslim'
    
    return regex.sub(pattern, r'\\xrightarrow{w^*} ', text)

def replace_aelim(text):
    pattern = r'\\aelim'
    
    return regex.sub(pattern, r'\\xrightarrow{\\text{a.e.}} ', text)

def replace_st(text):
    pattern = r'\\st(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\text{s.t. } ', text)

def replace_blo(text):
    pattern = r'\\blo(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathscr{B} ', text)

def replace_Cont(text):
    pattern = r'\\Cont(?![a-zA-Z0-9])'
    
    return regex.sub(pattern, r'\\mathrm{C} ', text)

def replace_ordinal(text):
    pattern = r'\\ordinal'
    
    return regex.sub(pattern, r'\\mathbb{O} ', text)

def replace_qty(text):
    pattern = r'\\qty(\{(?:[^{}]+|(?1))*\})'
    
    return regex.sub(pattern, lambda m: r'\\left\\{ ' + m.group(1)[1:-1] + r' \\right\\{', text)

def replace_qty2(text):
    pattern = r'\\qty(\((?:[^()]+|(?1))*\))'
    
    return regex.sub(pattern, lambda m: r'\\left( ' + m.group(1)[1:-1] + r' \\right)', text)

def replace_implies(text):
    pattern = r'\\implies'
    
    return regex.sub(pattern, r'\\Rightarrow ', text)

def replace_iff(text):
    pattern = r'\\iff'
    
    return regex.sub(pattern, r'\\Leftrightarrow ', text)

def replace_impliedby(text):
    pattern = r'\\impliedby'
    
    return regex.sub(pattern, r'\\Leftarrow ', text)

def replace_hyperref(text):
    pattern = r'\\hyperref\[(.*?)\]\{(.*?)\}'
    
    return regex.sub(pattern, r'[\2](#\1)', text)

def replace_all(text):
    text = replace_norm_recursive(text)
    text = replace_abs_recursive(text)
    text = replace_textbf(text)
    text = replace_textit(text)
    text = replace_dd(text)
    text = replace_N(text)
    text = replace_Z(text)
    text = replace_Q(text)
    text = replace_R(text)
    text = replace_C(text)
    text = replace_F(text)
    text = replace_D(text)
    text = replace_B(text)
    text = replace_newline(text)
    text = replace_tcbline(text)
    text = replace_i(text)
    text = replace_op_distance(text)
    text = replace_op_span(text)
    text = replace_op_card(text)
    text = replace_op_intr(text)
    text = replace_op_im(text)
    text = replace_op_esssum(text)
    text = replace_mlim(text)
    text = replace_wlim(text)
    text = replace_wslim(text)
    text = replace_aelim(text)
    text = replace_st(text)
    text = replace_blo(text)
    text = replace_Cont(text)
    text = replace_ordinal(text)
    text = replace_qty(text)
    text = replace_qty2(text)
    text = replace_implies(text)
    text = replace_iff(text)
    text = replace_impliedby(text)
    text = replace_hyperref(text)
    return text

def replace(json_path: str, output_json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        item['content'] = replace_all(item['content'])
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)