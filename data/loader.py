"""Reliable data file loading for local dev, editable installs, and Streamlit Cloud."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

_DATA_FILES = frozenset({"orders.json", "catalog.json", "policies.json"})


def _read_json_file(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _candidate_paths(filename: str) -> list[Path]:
    if filename not in _DATA_FILES:
        raise ValueError(f"Unknown data file: {filename}")

    candidates: list[Path] = []
    here = Path(__file__).resolve().parent

    for base in (here, here.parent, Path.cwd()):
        candidates.append(base / filename)
        candidates.append(base / "data" / filename)

    # Streamlit Community Cloud mount path
    candidates.append(Path("/mount/src/booklydemo") / "data" / filename)

    seen: set[Path] = set()
    unique: list[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def load_json(filename: str) -> Any:
    """Load a JSON data file from package resources or filesystem fallbacks."""
    try:
        text = resources.files("data").joinpath(filename).read_text(encoding="utf-8")
        return json.loads(text)
    except (FileNotFoundError, ModuleNotFoundError, TypeError, OSError):
        pass

    for path in _candidate_paths(filename):
        if path.is_file():
            return _read_json_file(path)

    tried = ", ".join(str(p) for p in _candidate_paths(filename))
    raise FileNotFoundError(
        f"Could not locate {filename}. Tried package resources and paths: {tried}"
    )


def load_orders() -> dict[str, Any]:
    return load_json("orders.json")


def load_policies() -> dict[str, Any]:
    return load_json("policies.json")


def load_catalog() -> dict[str, Any]:
    return load_json("catalog.json")
