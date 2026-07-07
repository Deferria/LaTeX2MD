from extract import extract_json
from convert import convert_json
from display import display_markdown
from macroexcape import replace_json

import argparse

EXTRACTED_JSON = './extracted.json'
FORMATTED_JSON = './formatted.json'
REPLACED_JSON = './replaced.json'

parser = argparse.ArgumentParser(description='Process LaTeX file and convert to Markdown.')
parser.add_argument('-i', '--input', type=str, default='./for_testing.txt', help='Path to the input LaTeX file')
parser.add_argument('-o', '--output', type=str, default='./output.md', help='Path to the output Markdown file')
parser.add_argument('-u', '--unsafe', action='store_false', help='If true, do not escape unsafe characters in Markdown')
args = parser.parse_args()

if __name__ == '__main__':
    tex = args.input
    markdown = args.output
    extract_json(tex, EXTRACTED_JSON)
    print("Extract TeX to JSON, done.")
    if not args.unsafe:
        replace_json(EXTRACTED_JSON, REPLACED_JSON)
    else:
        convert_json(EXTRACTED_JSON, FORMATTED_JSON)
        print("Markdown escape, done.")
        replace_json(FORMATTED_JSON, REPLACED_JSON)
    print("Convert LaTeX macros to KaTeX compatible, done.")
    display_markdown(REPLACED_JSON, markdown)
    print("Render Markdown, done.")