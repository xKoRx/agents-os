#!/usr/bin/env python3
"""Read-only AGENTS OS structural doctor.

Outputs findings without printing matched secret values.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    severity: str
    check: str
    path: str
    message: str


ROOT = Path(__file__).resolve().parents[4]
AGENTS = ROOT / "80-agents"
PROFILE_DIR = "80-agents/memory/public/user-preference"
FIXED_ALWAYS_ALLOWED = {
    "80-agents/agents-os/agent-constitution.md",
    "80-agents/skills/agents-os-bootstrap/SKILL.md",
    "80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md",
}


def _always_profiles() -> list[str]:
    """The global profile is named by whoever installs; resolve it, don't hardcode it.

    Exactly one note under the profile directory may be always-load. Returning
    every candidate lets check_always report a second one as a club violation.
    """
    directory = ROOT / PROFILE_DIR
    if not directory.is_dir():
        return []
    return sorted(
        f"{PROFILE_DIR}/{path.name}"
        for path in directory.glob("*.md")
        if frontmatter_value(path, "load_policy") == "always"
    )


def always_allowed() -> set[str]:
    profiles = _always_profiles()
    return FIXED_ALWAYS_ALLOWED | set(profiles[:1])


def startup_files() -> list[Path]:
    return [ROOT / path for path in sorted(always_allowed())]
GLOBAL_INTERNAL_MEMORY = ROOT / "80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md"
GLOBAL_INTERNAL_TOKEN_LIMIT = 1000
MEMORY_STATES = {"active", "superseded", "archived"}
PROJECT_LEDGER_SIGNAL = re.compile(
    r"(?i)(PASS\s*/\s*CLOSED|NEXT EXACT|\borigin/(?:master|main)\b|"
    r"\brelease\s+`?\d+\.\d+|\bFlowRun\b|\bRequestID\b|"
    r"\bcommit\s+`?[0-9a-f]{7,40})"
)
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|contrase(?:ñ|n)a|secret|api[_ -]?key|token|pwd)\s*[:=]"
)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def frontmatter_value(path: Path, key: str) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return None
    frontmatter = text.split("---", 2)[1]
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.*?)\s*$", frontmatter)
    return match.group(1).strip("\"'") if match else None


def check_paths(findings: list[Finding]) -> None:
    agents_file = ROOT / "AGENTS.md"
    if not agents_file.is_file():
        findings.append(Finding("HIGH", "path", "AGENTS.md", "missing surface hook"))
        return
    text = agents_file.read_text(encoding="utf-8")
    if re.search(r"`/(?:Users|home)/", text):
        findings.append(
            Finding("HIGH", "path", "AGENTS.md",
                    "machine-specific absolute path; use VAULT_ROOT-relative references")
        )
    for raw in re.findall(r"`((?:10|20|30|70|80|90|95)-[^`]+)`", text):
        if "<" not in raw and not (ROOT / raw.rstrip("/")).exists():
            findings.append(
                Finding("HIGH", "path", "AGENTS.md",
                        f"broken VAULT_ROOT-relative path: {raw}")
            )
    portability_targets = [
        ROOT / "AGENTS.md",
        AGENTS / "agents-os",
        AGENTS / "skills",
    ]
    candidates: list[Path] = []
    for target in portability_targets:
        if target.is_file():
            candidates.append(target)
        elif target.is_dir():
            candidates.extend(
                path for path in target.rglob("*")
                if path.is_file() and (
                    path.suffix in {".md", ".py", ".sh", ".yaml", ".yml"}
                    or path.name == "graphify-obsidian"
                )
            )
    machine_path = re.compile(r"(?:file://)?/(?:Users|home)/[A-Za-z0-9._-]+/")
    # Remote runtime paths inside a remote-access command are legitimate
    # operational evidence (e.g. `ssh kor@worker '/home/kor/...'`), not local
    # non-portable vault paths. Only flag machine paths on non-remote lines.
    remote_cmd = re.compile(r"(?:^|[|&;`(]|\bsudo\s+)\s*(?:ssh|scp|rsync|sftp)\b")
    for path in candidates:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not machine_path.search(line) or remote_cmd.search(line):
                continue
            findings.append(
                Finding("HIGH", "portability", relative(path),
                        "machine-specific absolute path in AGENTS OS core")
            )
            break


def check_always(findings: list[Finding]) -> None:
    allowed = always_allowed()
    profiles = _always_profiles()
    if not profiles:
        findings.append(
            Finding("HIGH", "always", PROFILE_DIR,
                    "no always-load global profile found; install is incomplete")
        )
    actual: set[str] = set()
    for path in AGENTS.rglob("*.md"):
        if frontmatter_value(path, "load_policy") == "always":
            actual.add(relative(path))
    for path in sorted(actual - allowed):
        findings.append(
            Finding("HIGH", "always", path, "outside the always-load closed club")
        )
    for path in sorted(allowed - actual):
        findings.append(
            Finding("HIGH", "always", path, "required always-load member is missing")
        )


def check_graphifyignore(findings: list[Finding]) -> None:
    path = ROOT / ".graphifyignore"
    if not path.is_file():
        findings.append(Finding("HIGH", "graphifyignore", ".graphifyignore", "missing"))
        return
    text = path.read_text(encoding="utf-8")
    # Generic exclusions only: a fresh install has no packaging subdirectories
    # yet, and 30-resources/agents-os/ covers every one of them by prefix.
    required = (".obsidian/", "00-inbox/", "40-archive/", "80-agents/journal/",
                "95-graphify/", "trash/", "30-resources/agents-os/")
    for entry in required:
        if entry not in text:
            findings.append(
                Finding("MEDIUM", "graphifyignore", ".graphifyignore",
                        f"missing exclusion: {entry}")
            )


def check_skill_index(findings: list[Finding]) -> None:
    index = AGENTS / "skills" / "INDEX.md"
    if not index.is_file():
        findings.append(Finding("HIGH", "skills", relative(index), "missing index"))
        return
    text = index.read_text(encoding="utf-8")
    # Core vault registry: anchor to 80-agents/skills/ so federated targets
    # hosted elsewhere (e.g. 30-resources/agents/skills/) are not miscounted.
    indexed = set(re.findall(r"80-agents/skills/([^/]+)/SKILL\.md", text))
    actual = {
        path.parent.name
        for path in (AGENTS / "skills").glob("*/SKILL.md")
        if path.parent.name != "_shared"
    }
    for name in sorted(actual - indexed):
        findings.append(Finding("MEDIUM", "skills", relative(index),
                                f"skill missing from index: {name}"))
    for name in sorted(indexed - actual):
        findings.append(Finding("HIGH", "skills", relative(index),
                                f"indexed skill missing on disk: {name}"))
    # Federated registry: skills hosted outside the vault core must resolve.
    for target in re.findall(r"(30-resources/agents/skills/[^|\]]+?/SKILL\.md)", text):
        if not (ROOT / target).is_file():
            findings.append(Finding("HIGH", "skills", relative(index),
                                    f"federated skill target missing on disk: {target}"))


def check_skill_frontmatter(findings: list[Finding]) -> None:
    """Every skill must carry the fields the schema contract requires.

    Without them the corpus lint skips the file entirely and retrieval has
    nothing to decide load timing or ranking with.
    """
    required = ("type", "schema_version", "name", "description",
                "scope", "load_policy", "indexable", "index_priority")
    for path in sorted((AGENTS / "skills").glob("*/SKILL.md")):
        missing = [key for key in required if frontmatter_value(path, key) in (None, "")]
        if missing:
            findings.append(Finding("MEDIUM", "skill-frontmatter", relative(path),
                                    f"missing required frontmatter: {', '.join(missing)}"))
        name = frontmatter_value(path, "name")
        if name and name != path.parent.name:
            findings.append(Finding("HIGH", "skill-frontmatter", relative(path),
                                    f"name {name!r} does not match folder {path.parent.name!r}"))


def check_skill_refs(findings: list[Finding]) -> None:
    pattern = re.compile(r"`((?:\.\.?/)+[^`\n]+?\.md)`")
    for path in (AGENTS / "skills").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for reference in pattern.findall(text):
            if not (path.parent / reference).resolve().is_file():
                findings.append(
                    Finding("HIGH", "skill-ref", relative(path),
                            f"broken relative reference: {reference}")
                )


def check_secrets(findings: list[Finding]) -> None:
    base = AGENTS / "memory" / "internal"
    for path in base.rglob("*.md"):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
        ):
            if SECRET_ASSIGNMENT.search(line):
                findings.append(
                    Finding(
                        "HIGH",
                        "secret",
                        f"{relative(path)}:{line_number}",
                        "credential-like assignment; value suppressed",
                    )
                )


def check_startup(findings: list[Finding]) -> int:
    files = startup_files()
    missing = [path for path in files if not path.is_file()]
    for path in missing:
        findings.append(Finding("HIGH", "startup", relative(path), "missing startup file"))
    chars = sum(len(path.read_text(encoding="utf-8")) for path in files if path.is_file())
    tokens = round(chars / 4)
    if tokens > 6000:
        findings.append(
            Finding("MEDIUM", "startup", "always-load set",
                    f"approx {tokens} tokens exceeds 6k soft target")
        )
    return tokens


def check_global_internal_memory(findings: list[Finding]) -> None:
    if not GLOBAL_INTERNAL_MEMORY.is_file():
        return
    text = GLOBAL_INTERNAL_MEMORY.read_text(encoding="utf-8", errors="ignore")
    tokens = round(len(text) / 4)
    if tokens > GLOBAL_INTERNAL_TOKEN_LIMIT:
        findings.append(
            Finding(
                "MEDIUM",
                "global-memory",
                relative(GLOBAL_INTERNAL_MEMORY),
                f"approx {tokens} tokens exceeds {GLOBAL_INTERNAL_TOKEN_LIMIT}-token transferable-memory limit",
            )
        )
    body = text.split("---", 2)[-1]
    if PROJECT_LEDGER_SIGNAL.search(body):
        findings.append(
            Finding(
                "HIGH",
                "global-memory",
                relative(GLOBAL_INTERNAL_MEMORY),
                "contains project-ledger signals; keep only transferable behavior and route domain state by entity",
            )
        )
    if frontmatter_value(GLOBAL_INTERNAL_MEMORY, "memory_state") != "active":
        findings.append(
            Finding(
                "HIGH",
                "global-memory",
                relative(GLOBAL_INTERNAL_MEMORY),
                "the canonical always-load memory must be memory_state active",
            )
        )


def check_internal_memory_scope(findings: list[Finding]) -> None:
    base = AGENTS / "memory" / "internal"
    for path in base.rglob("*.md"):
        if path == GLOBAL_INTERNAL_MEMORY:
            continue
        if frontmatter_value(path, "type") != "agent_memory":
            continue
        if frontmatter_value(path, "scope") == "global":
            findings.append(
                Finding(
                    "HIGH",
                    "memory-scope",
                    relative(path),
                    "domain memory declares global scope; route it by project, application, error or manual trigger",
                )
            )


def check_internal_memory_lifecycle(findings: list[Finding]) -> None:
    base = AGENTS / "memory" / "internal"
    active_by_key: dict[str, list[Path]] = {}
    for path in base.rglob("*.md"):
        if frontmatter_value(path, "type") != "agent_memory":
            continue
        state = frontmatter_value(path, "memory_state")
        key = frontmatter_value(path, "continuity_key")
        policy = frontmatter_value(path, "load_policy")
        priority = frontmatter_value(path, "index_priority")
        if not state and not key:
            continue
        if not state or state not in MEMORY_STATES:
            findings.append(Finding("HIGH", "memory-lifecycle", relative(path), "continuity_key requires memory_state active, superseded or archived"))
            continue
        if not key:
            continue
        if state == "active":
            active_by_key.setdefault(key, []).append(path)
            if not policy or policy in {"manual", "never"}:
                findings.append(Finding("HIGH", "memory-lifecycle", relative(path), "active continuity requires an automatic scoped load_policy"))
        else:
            if policy not in {"manual", "never"}:
                findings.append(Finding("HIGH", "memory-lifecycle", relative(path), f"{state} continuity must use load_policy manual or never"))
            if priority not in {"low", "never"}:
                findings.append(Finding("MEDIUM", "memory-lifecycle", relative(path), f"{state} continuity should use index_priority low or never"))
            if state == "superseded" and not frontmatter_value(path, "superseded_by"):
                findings.append(Finding("HIGH", "memory-lifecycle", relative(path), "superseded continuity requires superseded_by"))
    for key, paths in sorted(active_by_key.items()):
        if len(paths) > 1:
            rendered = ", ".join(relative(path) for path in sorted(paths))
            findings.append(Finding("HIGH", "memory-lifecycle", rendered, f"continuity_key {key!r} has {len(paths)} active notes; keep exactly one"))


def check_projects(findings: list[Finding]) -> None:
    parent = ROOT / "10-projects" / "AGENTS OS" / "AGENTS OS.md"
    if not parent.is_file():
        return
    text = parent.read_text(encoding="utf-8")
    bridges = re.findall(
        r"(?m)^> - \[[ /rxX-]\] \[\[(AGENTS OS - Hot Path[^\]]*)\]\].*#type/supervision",
        text,
    )
    if len(bridges) > 1:
        findings.append(
            Finding("HIGH", "project", relative(parent),
                    f"multiple Hot Path supervision bridges: {len(bridges)}")
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero on MEDIUM as well as HIGH")
    args = parser.parse_args()
    findings: list[Finding] = []
    check_paths(findings)
    check_always(findings)
    check_graphifyignore(findings)
    check_skill_index(findings)
    check_skill_frontmatter(findings)
    check_skill_refs(findings)
    check_secrets(findings)
    check_global_internal_memory(findings)
    check_internal_memory_scope(findings)
    check_internal_memory_lifecycle(findings)
    startup_tokens = check_startup(findings)
    check_projects(findings)

    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda item: (order[item.severity], item.check, item.path))
    counts = {severity: sum(f.severity == severity for f in findings)
              for severity in order}
    print(
        "AGENTS OS doctor: "
        f"HIGH={counts['HIGH']} MEDIUM={counts['MEDIUM']} LOW={counts['LOW']} "
        f"startup_tokens≈{startup_tokens}"
    )
    for finding in findings:
        print(
            f"{finding.severity} [{finding.check}] "
            f"{finding.path} — {finding.message}"
        )
    if counts["HIGH"] or (args.strict and counts["MEDIUM"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
