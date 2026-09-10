#!/usr/bin/env python3
"""Assemble the shareable AGENTS OS core from the canonical vault sources.

The output is a standalone vault skeleton: rules, executable contracts, skills,
templates, a standard profile and the install prompt, with no personal content.

Usage, from anywhere:

    python3 30-resources/agents-os/core-export/build-core.py [TARGET_DIR]

TARGET_DIR defaults to a sibling `agents-os/` directory next to VAULT_ROOT. No
absolute machine path is persisted anywhere: VAULT_ROOT is resolved from this
script's own location, per constitution invariant 11.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parents[2]
SOURCES = SCRIPT_DIR / "sources.list"
DIST_FILES = SCRIPT_DIR / "dist-files"

# Empty scaffolding the installer needs to exist before it writes anything.
SCAFFOLD_DIRS = [
    "00-inbox",
    "10-projects",
    "20-areas",
    "30-resources/tools",
    "40-archive",
    "80-agents/journal/agent-runs",
    "80-agents/journal/feedback/graphify",
    "80-agents/journal/feedback/kaizen-reports",
    "80-agents/journal/feedback/system-1",
    "80-agents/journal/hygiene",
    "80-agents/journal/logs",
    "80-agents/journal/sessions/raw",
    "80-agents/memory/internal/agent-memory/global",
    "80-agents/memory/public/decision",
    "80-agents/memory/public/known-error",
    "80-agents/memory/public/learning",
    "80-agents/memory/public/pattern",
    "80-agents/memory/public/runbook",
    "80-agents/memory/public/user-preference",
    "90-system/attachments",
]

# Never shipped, whatever the selection says.
FORBIDDEN = (
    "80-agents/memory/internal/",
    "80-agents/journal/",
)

# The one exception: an authored seed for the single always-load global
# continuity note. It ships from dist-files, never copied from the source vault,
# and carries only transferable behavior.
SEED_ALLOWED = {
    "80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md",
}

PRESERVE_IN_TARGET = {".git", ".obsidian"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()


def read_selection() -> list[tuple[str, str]]:
    """Expand sources.list into an ordered, deduplicated (category, relpath) list."""
    picked: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(category: str, path: Path) -> None:
        rel = path.relative_to(VAULT_ROOT).as_posix()
        if rel in seen or path.name == ".DS_Store":
            return
        seen.add(rel)
        picked.append((category, rel))

    def add_tree(category: str, root: Path) -> None:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            add(category, path)

    for raw in SOURCES.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        mode, category, rel = line.split("|", 2)
        if mode == "file":
            source = VAULT_ROOT / rel
            if not source.is_file():
                sys.exit(f"Missing required source: {rel}")
            add(category, source)
        elif mode == "tree":
            root = VAULT_ROOT / rel
            if not root.is_dir():
                sys.exit(f"Missing source tree: {rel}")
            add_tree(category, root)
        elif mode == "globtree":
            parent, pattern = rel.rsplit("/", 1)
            matches = sorted(p for p in (VAULT_ROOT / parent).glob(pattern) if p.is_dir())
            if not matches:
                sys.exit(f"Source glob matched nothing: {rel}")
            for root in matches:
                add_tree(category, root)
        else:
            sys.exit(f"Unknown selection mode: {mode}")

    for _, rel in picked:
        if rel.startswith(FORBIDDEN):
            sys.exit(f"Selection would ship private material: {rel}")
    return picked


def clear_target(target: Path) -> None:
    if not target.exists():
        target.mkdir(parents=True)
        return
    marker = target / "AGENTS.md"
    contents = [p for p in target.iterdir() if p.name not in PRESERVE_IN_TARGET]
    if contents and not marker.is_file():
        sys.exit(
            f"Refusing to clear {target}: it has content but no AGENTS.md marker.\n"
            "Point TARGET_DIR at an empty directory or at a previous core export."
        )
    for path in contents:
        shutil.rmtree(path) if path.is_dir() else path.unlink()


def filter_skill_index(target: Path, shipped: set[str]) -> int:
    """Keep only rows whose skill actually shipped; drop the federated registry.

    An index that lists skills absent from disk fails `agents-os-doctor`, so the
    distribution needs its own view rather than the source vault's.
    """
    index = target / "80-agents/skills/INDEX.md"
    kept, dropped = [], 0
    federated = False
    for line in index.read_text(encoding="utf-8").splitlines(keepends=True):
        if line.startswith("## 🌐 Registro federado"):
            federated = True
            kept.append(
                "## 🌐 Registro federado (fuentes fuera del core)\n\n"
                "El registry **enlaza, no copia**. El core vive arriba en `80-agents/skills/`.\n"
                "Las skills transversales curadas del vault viven bajo `30-resources/agents/skills/`\n"
                "y las de una aplicación viven en el repo que las posee, referenciadas por\n"
                "`repo + path relativo`, nunca por un path absoluto de máquina.\n\n"
                "Esta distribución no trae ninguna: el registry se puebla durante la instalación.\n"
            )
            continue
        if federated:
            continue
        match = re.search(r"80-agents/skills/([^/]+)/SKILL\.md", line)
        if match and match.group(1) not in shipped:
            dropped += 1
            continue
        kept.append(line)
    index.write_text("".join(kept), encoding="utf-8")
    return dropped


def main() -> None:
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (VAULT_ROOT.parent / "agents-os").resolve()
    if target == VAULT_ROOT or VAULT_ROOT in target.parents:
        sys.exit(f"Refusing to build into the source vault or below it: {target}")

    selection = read_selection()
    clear_target(target)

    total_bytes = 0
    rows = []
    for category, rel in selection:
        source = VAULT_ROOT / rel
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        source_hash, dest_hash = sha256(source), sha256(dest)
        if source_hash != dest_hash:
            sys.exit(f"Hash mismatch after copy: {rel}")
        size = source.stat().st_size
        total_bytes += size
        rows.append((category, rel, size, source_hash))

    dist_count = 0
    for path in sorted(p for p in DIST_FILES.rglob("*") if p.is_file()):
        if path.name == ".DS_Store":
            continue
        rel = path.relative_to(DIST_FILES)
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        dist_count += 1

    for rel in SCAFFOLD_DIRS:
        directory = target / rel
        directory.mkdir(parents=True, exist_ok=True)
        if not any(directory.iterdir()):
            (directory / ".gitkeep").touch()

    shipped = {rel.split("/")[2] for _, rel, _, _ in rows if rel.startswith("80-agents/skills/")}
    dropped_rows = filter_skill_index(target, shipped)
    # Count real skills, not path segments: `_shared` and `INDEX.md` also live
    # one level under skills/ and must not inflate the reported total.
    skill_count = sum(
        1 for _, rel, _, _ in rows
        if rel.startswith("80-agents/skills/") and rel.endswith("/SKILL.md")
    )

    leaked = [rel for _, rel, _, _ in rows if rel.startswith(FORBIDDEN)]
    stray = [
        rel
        for rel in (p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file())
        if rel.startswith(FORBIDDEN)
        and rel not in SEED_ALLOWED
        and not rel.endswith("/.gitkeep")
    ]
    if leaked or stray:
        sys.exit(f"Private material reached the output: {leaked + stray}")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    manifest = ["# AGENTS OS core — Manifest\n", "\n",
                f"- **Generated:** {stamp}\n",
                "- **Authority:** generated snapshot. Canonical paths are listed below; edits go there, never here.\n",
                f"- **Canonical files copied:** {len(rows)}\n",
                f"- **Distribution-authored files:** {dist_count}\n",
                f"- **Skill index rows dropped (skill not shipped):** {dropped_rows}\n",
                "- **Internal memory included:** no\n",
                "- **Journal contents included:** no (empty scaffolding only)\n",
                "- **Hash validation:** source/copy SHA-256 equality for every file\n",
                "\n",
                "| Category | Canonical source | Bytes | SHA-256 |\n", "|---|---|---:|---|\n"]
    for category, rel, size, digest in rows:
        manifest.append(f"| {category} | `{rel}` | {size} | `{digest}` |\n")
    (target / "MANIFEST.md").write_text("".join(manifest), encoding="utf-8")

    print(f"Target:            {target}")
    print(f"Canonical files:   {len(rows)} ({total_bytes} bytes)")
    print(f"Authored files:    {dist_count}")
    print(f"Skills shipped:    {skill_count}")
    print(f"Index rows dropped:{dropped_rows}")
    print("Validation:        passed")


if __name__ == "__main__":
    main()
