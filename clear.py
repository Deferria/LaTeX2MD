import os
from typing import List

FILE_LIST = [
    "./extracted.json",
    "./formatted.json",
    "./replaced.json",
    "./output.md"
]

def clear(files: List[str] = FILE_LIST):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"已删除文件: {file}")
        else:
            print(f"文件不存在: {file}")
    
if __name__ == '__main__':
    clear()