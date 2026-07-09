"""Resolve the Bookly project root when running from Jupyter / VS Code notebooks."""

from __future__ import annotations

import sys
from pathlib import Path


def find_project_root() -> Path:
    """Walk upward until we find the repo root (contains agent/ + requirements.txt)."""
    candidates: list[Path] = []

    ipynb = globals().get("__vsc_ipynb_file__")  # set by VS Code's notebook runtime
    if ipynb:
        candidates.append(Path(ipynb).resolve().parent)

    candidates.append(Path.cwd().resolve())

    for start in candidates:
        path = start
        for _ in range(8):
            if (path / "agent").is_dir() and (path / "requirements.txt").exists():
                return path
            if path.parent == path:
                break
            path = path.parent

    raise RuntimeError(
        "Could not find the bookly-cs-agent project root. "
        "Open the notebook from the project notebooks/ directory."
    )


def setup_project() -> Path:
    """Add project root to sys.path and return it."""
    root = find_project_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root
