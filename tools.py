# tools.py
"""
Filesystem tools for CrewAI agents.

Usage (CrewAI):
- Import functions via their tool names, e.g., add to an agent's `tools=[...]`.

Provided tools:
- make_dir(path, create_parents=True) -> str
- write_file(path, content, create_parents=True) -> str
- append_file(path, content, create_parents=True) -> str
- exists(path) -> bool
- read_file(path, encoding="utf-8") -> str
- list_dir(path) -> list[str]
- file_contains(path, text, encoding="utf-8") -> bool
"""

from __future__ import annotations

import os
from typing import List, Optional

# CrewAI's tool decorator (correct import)
from crewai.tools import tool


def _normalize_dir(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def _normalize_file(path: str) -> str:
    # Ensure directory part is normalized as well
    path = os.path.expanduser(path)
    return os.path.abspath(path)


@tool
def make_dir(path: str, create_parents: Optional[bool] = None) -> str:
    """
    Create a directory at `path`.
    - create_parents: if True, create intermediate directories. Defaults to True if not specified.
    Returns a human-readable confirmation message.
    """
    if create_parents is None:
        create_parents = True
    
    try:
        abs_path = _normalize_dir(path)
        if create_parents:
            os.makedirs(abs_path, exist_ok=True)
        else:
            os.mkdir(abs_path)
        return f"Created directory: {abs_path}"
    except Exception as e:
        return f"ERROR creating directory '{path}': {e}"


@tool
def write_file(path: str, content: str, create_parents: Optional[bool] = None) -> str:
    """
    Write `content` to `path` (overwrites).
    - create_parents: if True, makes parent dirs as needed. Defaults to True if not specified.
    Returns a human-readable confirmation message.
    """
    if create_parents is None:
        create_parents = True
    
    try:
        abs_path = _normalize_file(path)
        dir_ = os.path.dirname(abs_path)
        if create_parents and dir_:
            os.makedirs(dir_, exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content if content is not None else "")
        return f"Wrote file: {abs_path} ({len(content or '')} bytes)"
    except Exception as e:
        return f"ERROR writing file '{path}': {e}"


@tool
def append_file(path: str, content: str, create_parents: Optional[bool] = None) -> str:
    """
    Append `content` to `path`.
    - create_parents: if True, makes parent dirs as needed. Defaults to True if not specified.
    Returns a human-readable confirmation message.
    """
    if create_parents is None:
        create_parents = True
    
    try:
        abs_path = _normalize_file(path)
        dir_ = os.path.dirname(abs_path)
        if create_parents and dir_:
            os.makedirs(dir_, exist_ok=True)
        with open(abs_path, "a", encoding="utf-8") as f:
            f.write(content if content is not None else "")
        return f"Appended to file: {abs_path} (+{len(content or '')} bytes)"
    except Exception as e:
        return f"ERROR appending to file '{path}': {e}"


@tool
def exists(path: str) -> bool:
    """
    Return True if `path` exists (file or directory), else False.
    """
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
        return os.path.exists(abs_path)
    except Exception:
        # Conservative: claim it doesn't exist on unexpected errors.
        return False


# --- Tester / verification helpers ---


@tool
def read_file(path: str, encoding: Optional[str] = None) -> str:
    """
    Read and return the full contents of a text file at `path`.
    Returns the file text or an 'ERROR ...' string.
    - encoding: defaults to 'utf-8' if not specified.
    """
    if encoding is None:
        encoding = "utf-8"
    
    try:
        abs_path = _normalize_file(path)
        with open(abs_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return f"ERROR reading file '{path}': {e}"


@tool
def list_dir(path: str) -> List[str]:
    """
    List directory entries (names only) for `path`.
    Returns a list of names or a single-item list with an 'ERROR ...' string.
    """
    try:
        abs_path = _normalize_dir(path)
        return sorted(os.listdir(abs_path))
    except Exception as e:
        return [f"ERROR listing directory '{path}': {e}"]


@tool
def file_contains(path: str, text: str, encoding: Optional[str] = None) -> bool:
    """
    Return True if file at `path` exists and contains `text` (substring match).
    - encoding: defaults to 'utf-8' if not specified.
    """
    if encoding is None:
        encoding = "utf-8"
    
    try:
        abs_path = _normalize_file(path)
        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            return False
        with open(abs_path, "r", encoding=encoding) as f:
            return (text or "") in f.read()
    except Exception:
        return False


__all__ = [
    "make_dir",
    "write_file",
    "append_file",
    "exists",
    "read_file",
    "list_dir",
    "file_contains",
]