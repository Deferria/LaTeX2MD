from extract import to_json
from convert import json_to_json
from display import to_markdown
from macroexcape import replace

import argparse

EXTRACTED_JSON = './extracted.json'
FORMATTED_JSON = './formatted.json'
REPLACED_JSON = './replaced.json'

parser = argparse.ArgumentParser(description='Process LaTeX file and convert to Markdown.')
parser.add_argument('-i', '--input', type=str, default='./for_testing.txt', help='Path to the input LaTeX file')
parser.add_argument('-o', '--output', type=str, default='./output.md', help='Path to the output Markdown file')
args = parser.parse_args()

if __name__ == '__main__':
    tex = args.input
    markdown = args.output
    to_json(tex, EXTRACTED_JSON)
    print("Part 1: Extract TeX to JSON, done.")
    json_to_json(EXTRACTED_JSON, FORMATTED_JSON)
    print("Part 2: Markdown escape, done.")
    replace(FORMATTED_JSON, REPLACED_JSON)
    print("Part 3: Convert LaTeX macros to KaTeX compatible, done.")
    to_markdown(REPLACED_JSON, markdown)
    print("Part 4: Render Markdown, done.")