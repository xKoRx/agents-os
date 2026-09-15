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
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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

CORE_SKILL_RE = re.compile(r"80-agents/skills/([^/]+)/SKILL\.md")
FEDERATED_SKILL_RE = re.compile(r"30-resources/agents/skills/([^/]+)/SKILL\.md")

DOMAIN_NEUTRAL_HOT_PATH = (
    "80-agents/agents-os/agent-constitution.md",
    "80-agents/agents-os/context-router.md",
    "80-agents/skills/agents-os-bootstrap/SKILL.md",
    "80-agents/skills/INDEX.md",
)
DOMAIN_OPERATIONAL_MARKERS = re.compile(
    r"\b(?:Meli|Aranea|Echo|RIO|Zord|Fury|Spellbook|Grimoire|O11y)\b|"
    r"mcp__aranea-|~/fuentes|~/go/src/github\.com/xKoRx",
    re.IGNORECASE,
)

# Structured domain references are forbidden across the portable artifact. Body
# prose is inspected where it can execute or reproduce behavior (startup and
# templates); frontmatter is inspected everywhere because routing consumes it.
ARTIFACT_DOMAIN_MARKERS = re.compile(
    r"\[\[(?:Meli|Aranea|Echo|RIO)(?:[|#][^\]]*)?\]\]|"
    r"(?:#?area/)(?:meli|aranea|echo|rio)(?=$|[\s/\"'\],}])|"
    r"(?:10-projects|20-areas|30-resources)/(?:Meli|Aranea|Echo|RIO)(?:/|\.md|\b)|"
    r"mcp__aranea-|\b(?:Zord|Fury|Spellbook|Grimoire|O11y)\b",
    re.IGNORECASE,
)
AREA_FIELD_RE = re.compile(
    r'^area:\s*["\']?\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]["\']?\s*$',
    re.IGNORECASE,
)

# These files exercise intentionally-invalid metadata. The allowlist is exact,
# reviewable and never applies to templates or startup.
ARTIFACT_DOMAIN_ALLOWLIST = {
    "80-agents/skills/agents-os-entity-lifecycle/scripts/fixtures/valid/application-valid.md":
        "schema fixture whose domain link is part of its test payload",
    "80-agents/skills/agents-os-entity-lifecycle/scripts/fixtures/invalid/missing-status.md":
        "negative schema fixture whose domain link is part of its test payload",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()


def read_selection() -> tuple[list[tuple[str, str]], set[str]]:
    """Expand sources.list into an ordered, deduplicated (category, relpath) list."""
    picked: list[tuple[str, str]] = []
    seen: set[str] = set()
    excluded: set[str] = set()

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
        if mode == "exclude":
            source = VAULT_ROOT / rel
            if not source.is_file():
                sys.exit(f"Missing source selected for exclusion: {rel}")
            excluded.add(rel)
        elif mode == "file":
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

    unmatched = excluded - seen
    if unmatched:
        sys.exit("Excluded source was not selected by any include rule: " + ", ".join(sorted(unmatched)))

    picked = [(category, rel) for category, rel in picked if rel not in excluded]
    for _, rel in picked:
        if rel.startswith(FORBIDDEN):
            sys.exit(f"Selection would ship private material: {rel}")
    return picked, excluded


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


def filter_skill_index(
    target: Path,
    shipped_core: set[str],
    shipped_federated: set[str],
) -> int:
    """Project the source registry to exactly the skills shipped.

    The source vault keeps core skills under ``80-agents/skills`` and curated
    portable skills under ``30-resources/agents/skills``. The distribution
    preserves both locations and must retain discoverable rows for both.
    """
    index = target / "80-agents/skills/INDEX.md"
    source_lines = index.read_text(encoding="utf-8").splitlines(keepends=True)
    kept: list[str] = []
    dropped = 0
    for line in source_lines:
        if line.startswith("## 🌐 Registro federado"):
            break
        if line.startswith("- **Core AGENTS OS:**"):
            line = f"- **Core AGENTS OS:** {len(shipped_core)} skills de comportamiento del sistema.\n"
        elif line.startswith(("- **Federadas (vault):**", "- **Federadas transversales:**")):
            line = f"- **Federadas transversales:** {len(shipped_federated)} skills portables incluidas.\n"
        elif line.startswith(("- **App-owned:**", "- **Domain/app-owned:**")):
            line = "- **Domain/app-owned:** se registran durante la instalación; no forman parte del índice always-load.\n"
        match = CORE_SKILL_RE.search(line)
        if match and match.group(1) not in shipped_core:
            dropped += 1
            continue
        kept.append(line)

    federated_rows: list[str] = []
    for line in source_lines:
        match = FEDERATED_SKILL_RE.search(line)
        if not match:
            continue
        if match.group(1) in shipped_federated:
            federated_rows.append(line)
        else:
            dropped += 1

    kept.extend([
        "## 🌐 Registro federado incluido\n",
        "\n",
        "Estas skills portables conservan su ubicación canónica fuera del core y\n",
        "siguen siendo descubribles desde el índice cargado por bootstrap.\n",
        "\n",
        "| Skill | Una línea | Dominio / uso |\n",
        "|---|---|---|\n",
    ])
    kept.extend(federated_rows)
    index.write_text("".join(kept), encoding="utf-8")
    return dropped


def frontmatter_lines(path: Path) -> list[tuple[int, str]]:
    """Return numbered frontmatter lines, or an empty list when absent."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return []
    try:
        end = lines.index("---", 1)
    except ValueError:
        return []
    return list(enumerate(lines[1:end], 2))


def collect_artifact_domain_failures(
    target: Path,
    full_scan_paths: set[str] | None = None,
) -> list[str]:
    """Find domain coupling on executable surfaces and routing metadata."""
    failures: list[str] = []
    full_scan_paths = full_scan_paths or set()
    for path in sorted(target.rglob("*.md")):
        rel = path.relative_to(target).as_posix()
        if rel in ARTIFACT_DOMAIN_ALLOWLIST:
            continue

        scan_full = (
            rel in DOMAIN_NEUTRAL_HOT_PATH
            or rel.startswith(("70-templates/", "80-agents/templates/"))
            or rel in full_scan_paths
        )
        numbered = (
            list(enumerate(path.read_text(encoding="utf-8").splitlines(), 1))
            if scan_full
            else frontmatter_lines(path)
        )
        for lineno, line in numbered:
            if ARTIFACT_DOMAIN_MARKERS.search(line):
                failures.append(f"{rel}:{lineno}: domain reference: {line.strip()}")

        for lineno, line in frontmatter_lines(path):
            match = AREA_FIELD_RE.match(line.strip())
            if not match or "{{" in match.group(1):
                continue
            area_name = match.group(1).strip()
            area_path = target / "20-areas" / f"{area_name}.md"
            if not area_path.is_file():
                failures.append(
                    f"{rel}:{lineno}: unresolved distributed area [[{area_name}]]"
                )
    return failures


def validate_domain_neutral_artifact(
    target: Path,
    full_scan_paths: set[str] | None = None,
) -> None:
    """Fail when the package depends on a domain absent from DEFAULT installs."""
    failures: list[str] = []
    for rel in DOMAIN_NEUTRAL_HOT_PATH:
        path = target / rel
        if not path.is_file():
            failures.append(f"missing hot-path file: {rel}")
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if DOMAIN_OPERATIONAL_MARKERS.search(line):
                failures.append(f"{rel}:{lineno}: {line.strip()}")
    failures.extend(collect_artifact_domain_failures(target, full_scan_paths))
    if failures:
        sys.exit("Domain-specific policy reached the portable artifact:\n" + "\n".join(failures))


def load_schema_contract(target: Path) -> dict:
    path = target / "80-agents/skills/_shared/schema-contract.md"
    text = path.read_text(encoding="utf-8")
    try:
        payload = text.split("<!-- AGENTS_OS_SCHEMA_START -->", 1)[1].split(
            "<!-- AGENTS_OS_SCHEMA_END -->", 1
        )[0]
    except IndexError as exc:
        raise ValueError("schema markers are missing from the built artifact") from exc
    match = re.search(r"```json\s*(\{.*\})\s*```", payload, re.DOTALL)
    if not match:
        raise ValueError("schema JSON is missing from the built artifact")
    return json.loads(match.group(1))


def verify_default_install_materialization(target: Path) -> int:
    """Materialize every creatable schema type inside an isolated DEFAULT vault."""
    contract = load_schema_contract(target)
    creatable = sorted(
        note_type
        for config in contract["systems"].values()
        for note_type, spec in config["types"].items()
        if spec.get("template")
    )
    with tempfile.TemporaryDirectory(prefix="agents-os-default-install-") as temp_dir:
        probe_root = Path(temp_dir) / "vault"
        shutil.copytree(target, probe_root)
        materializer = (
            probe_root
            / "80-agents/skills/_shared/scripts/materialize_schema_note.py"
        )
        generated: set[str] = set()
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        for note_type in creatable:
            slug = re.sub(r"[^a-z0-9]+", "-", note_type.lower()).strip("-")
            rel = f"00-inbox/default-install-probe-{slug}.md"
            result = subprocess.run(
                [sys.executable, str(materializer), note_type, rel],
                cwd=probe_root,
                env=env,
                text=True,
                capture_output=True,
                check=False,
                timeout=30,
            )
            if result.returncode:
                detail = (result.stderr or result.stdout).strip()
                sys.exit(f"DEFAULT materialization failed for {note_type}: {detail}")
            if not (probe_root / rel).is_file():
                sys.exit(f"DEFAULT materialization produced no entity for {note_type}")
            generated.add(rel)

        validate_domain_neutral_artifact(probe_root, full_scan_paths=generated)
    return len(creatable)


def main() -> None:
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (VAULT_ROOT.parent / "agents-os").resolve()
    if target == VAULT_ROOT or VAULT_ROOT in target.parents:
        sys.exit(f"Refusing to build into the source vault or below it: {target}")

    selection, excluded = read_selection()
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

    shipped_core = {
        Path(rel).parts[-2]
        for _, rel, _, _ in rows
        if rel.startswith("80-agents/skills/") and rel.endswith("/SKILL.md")
    }
    shipped_federated = {
        Path(rel).parts[-2]
        for _, rel, _, _ in rows
        if rel.startswith("30-resources/agents/skills/") and rel.endswith("/SKILL.md")
    }
    dropped_rows = filter_skill_index(target, shipped_core, shipped_federated)
    # Count real skills, not path segments: `_shared` and `INDEX.md` also live
    # one level under skills/ and must not inflate the reported total.
    skill_count = sum(
        1 for _, rel, _, _ in rows
        if rel.startswith(("80-agents/skills/", "30-resources/agents/skills/"))
        and rel.endswith("/SKILL.md")
    )

    validate_domain_neutral_artifact(target)
    materialized_count = verify_default_install_materialization(target)

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
                f"- **Scoped source files excluded:** {len(excluded)}\n",
                f"- **DEFAULT entity types materialized:** {materialized_count}\n",
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
    print(f"Scoped exclusions: {len(excluded)}")
    print(f"Types materialized:{materialized_count}")
    print(f"Index rows dropped:{dropped_rows}")
    print("Validation:        passed")


if __name__ == "__main__":
    main()
