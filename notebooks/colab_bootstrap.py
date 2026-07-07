"""Bootstrap helpers for Google Colab and local Jupyter notebooks."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def git_remote_url(start: Path | None = None) -> str | None:
    """Return origin remote URL if this directory is inside a git repo."""
    start = start or Path.cwd()
    for path in [start, *start.parents]:
        if not (path / ".git").exists():
            continue
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=path,
        )
        if result.returncode != 0:
            return None
        url = result.stdout.strip()
        if url.startswith("git@"):
            # git@github.com:user/repo.git → https://github.com/user/repo.git
            url = url.replace(":", "/", 1).replace("git@", "https://")
        if not url.endswith(".git"):
            url += ".git"
        return url
    return None


def find_project_root() -> Path:
    """Walk upward until we find the repo root (agent/ + requirements.txt)."""
    candidates: list[Path] = []

    ipynb = globals().get("__vsc_ipynb_file__")
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
        "Could not find project root. If you're on Colab, run the bootstrap cell first."
    )


def bootstrap_colab(repo_url: str | None = None) -> Path:
    """Clone repo (if needed), install package, load API key. Returns project root."""
    root = Path.cwd()
    project_dir = root / "bookly-cs-agent"

    if not (root / "agent").exists() and not project_dir.exists():
        resolved = repo_url or git_remote_url(root) or os.environ.get("BOOKLY_REPO_URL")
        if not resolved or "YOUR_USERNAME" in resolved:
            raise RuntimeError(
                "Could not find the project code.\n"
                "Fix: open this notebook from GitHub (recommended), or set REPO_URL in the bootstrap cell.\n"
                "Example: https://github.com/<you>/bookly-cs-agent.git"
            )
        subprocess.run(["git", "clone", resolved, "bookly-cs-agent"], check=True)

    if project_dir.exists() and not (root / "agent").exists():
        os.chdir(project_dir)

    path = Path.cwd()
    found = False
    for _ in range(5):
        if (path / "agent").is_dir() and (path / "requirements.txt").exists():
            os.chdir(path)
            found = True
            break
        if path.parent == path:
            break
        path = path.parent

    if not found:
        raise RuntimeError("agent/ folder not found after bootstrap.")

    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-e", "."], check=True)

    try:
        from google.colab import userdata

        os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
        print("✓ OpenAI API key loaded from Colab Secrets")
    except Exception:
        print("○ No OPENAI_API_KEY secret — mock mode (still works for demo)")

    project_root = Path.cwd()
    print(f"✓ Colab ready — project root: {project_root}")
    return project_root


def bootstrap_local() -> Path:
    """Find project root when running outside Colab."""
    root = find_project_root()
    print(f"✓ Local ready — project root: {root}")
    return root
