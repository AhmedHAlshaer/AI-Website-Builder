# tools.py
"""
Filesystem tools for CrewAI agents.
"""

from __future__ import annotations
import os
from typing import List
from crewai.tools import tool


def _normalize_dir(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


def _normalize_file(path: str) -> str:
    path = os.path.expanduser(path)
    return os.path.abspath(path)


@tool("make_dir")
def make_dir(path: str, create_parents: bool = True) -> str:
    """Create a directory at `path`. If create_parents is True, create intermediate directories."""
    try:
        abs_path = _normalize_dir(path)
        if create_parents:
            os.makedirs(abs_path, exist_ok=True)
        else:
            os.mkdir(abs_path)
        return f"Created directory: {abs_path}"
    except Exception as e:
        return f"ERROR creating directory '{path}': {e}"


@tool("write_file")
def write_file(path: str, content: str, create_parents: bool = True) -> str:
    """Write content to path (overwrites). If create_parents is True, makes parent dirs as needed."""
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


@tool("append_file")
def append_file(path: str, content: str, create_parents: bool = True) -> str:
    """Append content to path. If create_parents is True, makes parent dirs as needed."""
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


@tool("exists")
def exists(path: str) -> bool:
    """Return True if path exists (file or directory), else False."""
    try:
        abs_path = os.path.abspath(os.path.expanduser(path))
        return os.path.exists(abs_path)
    except Exception:
        return False


@tool("read_file")
def read_file(path: str, encoding: str = "utf-8") -> str:
    """Read and return the full contents of a text file at path."""
    try:
        abs_path = _normalize_file(path)
        with open(abs_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return f"ERROR reading file '{path}': {e}"


@tool("list_dir")
def list_dir(path: str) -> List[str]:
    """List directory entries (names only) for path."""
    try:
        abs_path = _normalize_dir(path)
        return sorted(os.listdir(abs_path))
    except Exception as e:
        return [f"ERROR listing directory '{path}': {e}"]


@tool("file_contains")
def file_contains(path: str, text: str, encoding: str = "utf-8") -> bool:
    """Return True if file at path exists and contains text (substring match)."""
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