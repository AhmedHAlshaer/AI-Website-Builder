# Expose file-system helper functions for import like:
# from tools import make_dir, write_file, append_file, exists

import os

def make_dir(path: str, create_parents: bool = True):
    if create_parents:
        os.makedirs(path, exist_ok=True)
    else:
        os.mkdir(path)

def write_file(path: str, content: str, create_parents: bool = True):
    dir_ = os.path.dirname(path)
    if create_parents and dir_:
        os.makedirs(dir_, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def append_file(path: str, content: str, create_parents: bool = True):
    dir_ = os.path.dirname(path)
    if create_parents and dir_:
        os.makedirs(dir_, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

def exists(path: str) -> bool:
    return os.path.exists(path)
