"""Module for persistent storage using pickle."""

import pickle
from pathlib import Path
from typing import Any

BASE_DIR = Path.home() / ".assistant"
BASE_DIR.mkdir(parents=True, exist_ok=True)

def _full_path(name: str) -> Path:
    """Convert a short file name to a full path inside ~/.assistant"""
    return BASE_DIR / name

def load(filename: str, default_factory):
    """Load object from ~/.assistant/<filename> or return default."""
    path = _full_path(filename)
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return default_factory()

def save(obj: Any, filename: str) -> None:
    """Save object using pickle to ~/.assistant/<filename>"""
    path = _full_path(filename)
    with open(path, 'wb') as file:
        pickle.dump(obj, file)
