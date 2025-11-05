import os

def make_dir(path: str, create_parents: bool = True):
    """
    Create a directory at the given path.
    """
    if create_parents:
        os.makedirs(path, exist_ok=True)
    else:
        os.mkdir(path)

def write_file(path: str, content: str, create_parents: bool = True):
    """
    Write content to a file. Creates parent directories if necessary.
    """
    directory = os.path.dirname(path)
    if create_parents and directory:
        os.makedirs(directory, exist_ok=True)
    # Write text content (utf-8 encoding)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def append_file(path: str, content: str, create_parents: bool = True):
    """
    Append content to a file. Creates the file and parent directories if necessary.
    """
    directory = os.path.dirname(path)
    if create_parents and directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)

def exists(path: str) -> bool:
    """
    Check if a file or directory exists.
    """
    return os.path.exists(path)
