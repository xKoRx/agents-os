#!/usr/bin/env python3
"""Discover local Git repositories without reading repository content."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


PRUNE = {
    ".cache",
    ".idea",
    ".venv",
    ".vscode",
    "build",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

MANIFESTS = {
    "build.gradle": "Java/Gradle",
    "build.gradle.kts": "Kotlin/Gradle",
    "go.mod": "Go",
    "package.json": "JavaScript/TypeScript",
    "pom.xml": "Java/Maven",
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "Cargo.toml": "Rust",
}

INSTRUCTIONS = ("AGENTS.md", "CLAUDE.md", ".cursorrules", "README.md")


def clean_remote(remote: str) -> str:
    remote = remote.strip()
    if "://" not in remote:
        return remote
    parts = urlsplit(remote)
    hostname = parts.hostname or ""
    if parts.port:
        hostname += f":{parts.port}"
    return urlunsplit((parts.scheme, hostname, parts.path, "", ""))


def git_remote(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "remote", "get-url", "origin"],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return clean_remote(result.stdout) if result.returncode == 0 else ""


def describe(repo: Path) -> dict[str, object]:
    manifests = [name for name in MANIFESTS if (repo / name).is_file()]
    stacks = sorted({MANIFESTS[name] for name in manifests})
    instructions = [name for name in INSTRUCTIONS if (repo / name).is_file()]
    return {
        "name": repo.name,
        "path": str(repo.resolve()),
        "remote": git_remote(repo),
        "stack": stacks,
        "manifests": manifests,
        "instructions": instructions,
    }


def discover(root: Path, max_depth: int) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"workspace root does not exist: {root}")
    repos: list[Path] = []
    for current, dirs, _files in os.walk(root, followlinks=False):
        path = Path(current)
        depth = len(path.relative_to(root).parts)
        dirs[:] = [d for d in dirs if d not in PRUNE and not d.startswith(".")]
        if (path / ".git").exists():
            repos.append(path)
            dirs[:] = []
            continue
        if depth >= max_depth:
            dirs[:] = []
    return repos


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", action="append", required=True, type=Path)
    parser.add_argument("--max-depth", type=int, default=4)
    args = parser.parse_args()
    if args.max_depth < 0:
        raise SystemExit("--max-depth must be non-negative")

    found: dict[str, Path] = {}
    try:
        for root in args.root:
            for repo in discover(root, args.max_depth):
                found[str(repo.resolve())] = repo
    except ValueError as error:
        raise SystemExit(str(error)) from error

    print(json.dumps([describe(found[key]) for key in sorted(found)], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
