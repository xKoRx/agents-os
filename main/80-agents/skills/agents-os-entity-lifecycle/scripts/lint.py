#!/usr/bin/env python3
"""Read-only contract-driven AGENTS OS lint for Sistema 1 and Sistema 2.

The executable Markdown contract in ``80-agents/skills/_shared/schema-contract.md``
is the only schema authority. The lint never modifies the vault.

Modes:
  --check           Report findings; exit 1 when any ERROR exists.
  --strict PATHS    Treat PATHS as new/changed; require the current schema and
                    exit 1 on any finding.
  --gate            Compare findings with the contracted baseline and block
                    only new debt. Existing findings may disappear but no new
                    fingerprint may appear.
  --emit-baseline   Print a deterministic baseline candidate as JSON to stdout.

Explicit PATHS bypass corpus exclusions so fixtures and pilots can be tested.
No mode depends on Git or writes files.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import fnmatch
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[4]
SHARED_SCRIPTS = ROOT / "80-agents/skills/_shared/scripts"
sys.path.insert(0, str(SHARED_SCRIPTS))

from validate_schema_contract import load_contract  # noqa: E402


BASELINE_FORMAT = 1
TEMPLATE_ROOTS = ("70-templates", "80-agents/templates")
TAG_PATTERN = re.compile(r"^[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)+$")
WIKILINK_PATTERN = re.compile(r"^\[\[[^\[\]]+\]\]$")


@dataclass(frozen=True)
class Finding:
    severity: str
    check: str
    path: str
    message: str


@dataclass(frozen=True)
class Note:
    fields: dict[str, str]
    lists: dict[str, list[str]]
    block: str
    body: str


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _inline_list(value: str) -> list[str] | None:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [_unquote(item) for item in next(csv.reader([inner], skipinitialspace=True))]


def parse_frontmatter(path: Path) -> Note | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return None
    body_start = text[3:].lstrip("\r").lstrip("\n")
    end = body_start.find("\n---")
    if end == -1:
        return None
    block = body_start[:end]
    body = body_start[end + 4:].lstrip("\r").lstrip("\n")
    fields: dict[str, str] = {}
    lists: dict[str, list[str]] = {}
    current: str | None = None
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)[ \t]*$", line)
        if match:
            current = match.group(1)
            raw = match.group(2).strip()
            fields[current] = _unquote(raw)
            inline = _inline_list(raw)
            if inline is not None:
                lists[current] = inline
            continue
        item = re.match(r"^[ \t]+-[ \t]+(.*?)[ \t]*$", line)
        if current and item:
            lists.setdefault(current, []).append(_unquote(item.group(1)))
    return Note(fields=fields, lists=lists, block=block, body=body)


def scalar(note: Note, key: str) -> str | None:
    value = note.fields.get(key, "").strip()
    return value or None


def load_ignore_patterns() -> list[str]:
    path = ROOT / ".graphifyignore"
    if not path.is_file():
        return []
    return [line for raw in path.read_text(encoding="utf-8").splitlines() if (line := raw.strip()) and not line.startswith("#")]


def _match(rel: str, parts: list[str], pattern: str) -> bool:
    if pattern.endswith("/**"):
        base = pattern[:-3].rstrip("/")
        return rel == base or rel.startswith(base + "/")
    if pattern.startswith("**/") and pattern.endswith("/"):
        return pattern[3:-1] in parts[:-1]
    if pattern.endswith("/"):
        base = pattern[:-1]
        return rel == base or rel.startswith(base + "/") or base in parts[:-1]
    if pattern.startswith("**/"):
        tail = pattern[3:]
        return fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(parts[-1], tail) or fnmatch.fnmatch(rel, "*/" + tail)
    return fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(parts[-1], pattern)


def is_ignored(rel: str, patterns: list[str]) -> bool:
    parts = rel.split("/")
    if any(part.startswith(".") for part in parts[:-1]):
        return True
    if "fixtures" in parts:
        return True
    return any(_match(rel, parts, pattern) for pattern in patterns)


def contract_types(contract: dict) -> dict[str, tuple[str, dict]]:
    index: dict[str, tuple[str, dict]] = {}
    for system, config in contract["systems"].items():
        for note_type, spec in config["types"].items():
            if note_type in index:
                raise ValueError(f"ambiguous schema type: {note_type}")
            index[note_type] = (system, spec)
    return index


def required_fields(contract: dict, system: str, note_type: str, spec: dict, *, legacy: bool) -> set[str]:
    if legacy:
        config = contract["lint"]["legacy_required"]
        return set(config[system]) | set(config["types"].get(note_type, []))
    envelope = contract["envelope"]
    return set(envelope["common"]["required"]) | set(envelope[system]["required"]) | set(spec["required"])


def forbidden_fields(contract: dict, system: str, spec: dict) -> set[str]:
    envelope = contract["envelope"]
    return set(envelope["common"]["forbidden"]) | set(envelope[system]["forbidden"]) | set(spec["forbidden"])


def require_fields(note: Note, fields: set[str], rel: str, findings: list[Finding], *, is_template: bool) -> None:
    field_types = set(note.lists)
    for key in sorted(fields):
        if key not in note.fields:
            findings.append(Finding("ERROR", "missing-field", rel, f"required frontmatter field '{key}' is missing"))
        elif not is_template and key not in field_types and not scalar(note, key):
            findings.append(Finding("ERROR", "empty-field", rel, f"required frontmatter field '{key}' must not be empty"))


def validate_field_type(key: str, rule: dict, note: Note, rel: str, findings: list[Finding], *, is_template: bool, required: bool) -> None:
    if key not in note.fields:
        return
    raw = note.fields[key].strip()
    if is_template and not raw and key not in note.lists:
        return
    kind = rule["kind"]
    value = scalar(note, key)
    valid = True
    detail = kind
    if kind == "list":
        valid = key in note.lists or raw == ""
        items = note.lists.get(key, [])
        item_kind = rule.get("items")
        if valid and item_kind == "canonical_wikilink":
            valid = all(WIKILINK_PATTERN.fullmatch(item) for item in items)
            detail = "list[canonical_wikilink]"
        elif valid:
            valid = all(bool(item.strip()) for item in items)
            detail = f"list[{item_kind or 'string'}]"
    elif value is None:
        valid = is_template or not required
    elif kind == "integer":
        valid = bool(re.fullmatch(r"-?[0-9]+", value))
        if valid:
            number = int(value)
            valid = number >= rule.get("minimum", number) and number <= rule.get("maximum", number)
    elif kind == "boolean":
        valid = value in {"true", "false"}
    elif kind == "date":
        valid = bool(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value))
        if valid:
            try:
                dt.date.fromisoformat(value)
            except ValueError:
                valid = False
    elif kind == "canonical_wikilink":
        valid = bool(WIKILINK_PATTERN.fullmatch(value))
    elif kind == "string":
        valid = bool(value)
    if valid and value is not None and isinstance(rule.get("values"), list):
        valid = value in rule["values"]
        detail = "one of " + repr(rule["values"])
    if valid and value is not None and rule.get("pattern"):
        valid = bool(re.fullmatch(rule["pattern"], value))
        detail = f"pattern {rule['pattern']}"
    if not valid:
        findings.append(Finding("ERROR", "field-type", rel, f"field '{key}' must satisfy {detail}; got {raw!r}"))


def validate_tags(contract: dict, system: str, note_type: str, note: Note, rel: str, findings: list[Finding]) -> None:
    tags = note.lists.get("tags", [])
    expected = "kind/" + note_type.replace("_", "-")
    if expected not in tags:
        findings.append(Finding("ERROR", "missing-tag", rel, f"current note requires canonical tag '{expected}'"))
    if system == "s1":
        scope = scalar(note, "scope")
        expected_scope = f"scope/{scope}" if scope else None
        if expected_scope and expected_scope not in tags:
            findings.append(Finding("ERROR", "missing-tag", rel, f"Sistema 1 note requires routing tag '{expected_scope}'"))
    forbidden = set(contract["tags"]["forbidden"])
    for tag in tags:
        if tag in forbidden:
            findings.append(Finding("ERROR", "forbidden-tag", rel, f"generic tag '{tag}' is forbidden"))
        elif not TAG_PATTERN.fullmatch(tag):
            findings.append(Finding("ERROR", "bad-tag", rel, f"tag '{tag}' must use namespaced path syntax"))


def validate_sections(spec: dict, note: Note, rel: str, findings: list[Finding]) -> None:
    headings = {line.strip() for line in note.body.splitlines() if line.startswith("#")}
    for heading in spec["sections"]:
        if heading not in headings:
            findings.append(Finding("ERROR", "missing-section", rel, f"required section {heading!r} is missing"))


def apply_semantic_rules(spec: dict, note: Note, rel: str, findings: list[Finding], *, is_template: bool) -> None:
    if is_template:
        return
    for rule in spec.get("rules", []):
        if rule == "project_parent_or_root":
            root = scalar(note, "root")
            parent = scalar(note, "parent")
            if root == "true" and parent:
                findings.append(Finding("ERROR", "project-root-parent", rel, "root project must not declare parent"))
            elif root != "true" and not parent:
                findings.append(Finding("ERROR", "project-parent", rel, "non-root project requires canonical 'parent'; roots use root: true"))
        elif rule == "source_location":
            source_url = scalar(note, "source_url")
            repo = scalar(note, "repo")
            source_path = scalar(note, "path")
            if not source_url and not (repo and source_path):
                findings.append(Finding("ERROR", "source-location", rel, "source requires 'source_url' or both 'repo' and 'path'"))
        else:
            findings.append(Finding("ERROR", "contract-rule", rel, f"unsupported semantic rule '{rule}'"))


def lint_note(contract: dict, type_index: dict[str, tuple[str, dict]], rel: str, path: Path, findings: list[Finding], *, strict: bool) -> None:
    note = parse_frontmatter(path)
    if note is None:
        findings.append(Finding("ERROR" if strict else "WARN", "no-frontmatter", rel, "note has no frontmatter/type"))
        return
    note_type = scalar(note, "type")
    if not note_type:
        findings.append(Finding("ERROR" if strict else "WARN", "no-type", rel, "frontmatter present but 'type' is missing"))
        return
    resolved = type_index.get(note_type)
    if not resolved:
        findings.append(Finding("ERROR", "unknown-type", rel, f"unknown type '{note_type}'; define it in schema-contract.md"))
        return
    system, spec = resolved
    is_template = any(rel == root or rel.startswith(root + "/") for root in TEMPLATE_ROOTS)
    expected_root = contract["systems"][system]["template_root"]
    if is_template and not (rel == expected_root or rel.startswith(expected_root + "/")):
        findings.append(Finding("ERROR", "template-boundary", rel, f"{system} template type '{note_type}' belongs under {expected_root}/"))

    version = scalar(note, "schema_version")
    legacy = version is None
    if legacy and strict:
        findings.append(Finding("ERROR", "legacy-modified", rel, f"new/modified notes must declare current schema_version {contract['schema_versions']['current']}"))
    if version is not None:
        supported = {str(item) for item in contract["schema_versions"]["supported"]}
        if not re.fullmatch(r"[0-9]+", version) or version not in supported:
            findings.append(Finding("ERROR", "schema-version", rel, f"unsupported schema_version {version!r}; supported: {sorted(supported)}"))
            return

    required = required_fields(contract, system, note_type, spec, legacy=legacy)
    require_fields(note, required, rel, findings, is_template=is_template)
    forbidden = forbidden_fields(contract, system, spec) if not legacy else ({"status"} if system == "s1" else set())
    for key in sorted(forbidden & set(note.fields)):
        findings.append(Finding("ERROR", "forbidden-field", rel, f"field '{key}' is forbidden for type '{note_type}'"))

    statuses = spec.get("statuses", [])
    status = scalar(note, "status")
    if status and not statuses:
        findings.append(Finding("WARN", "status-without-lifecycle", rel, f"type '{note_type}' defines no status lifecycle"))
    elif status and status not in statuses:
        findings.append(Finding("ERROR", "bad-status", rel, f"invalid status '{status}' for type '{note_type}'; allowed: {sorted(statuses)}"))

    if not legacy:
        for key, rule in contract["field_types"].items():
            validate_field_type(key, rule, note, rel, findings, is_template=is_template, required=key in required)
        validate_tags(contract, system, note_type, note, rel, findings)
        validate_sections(spec, note, rel, findings)
    elif note_type == "project":
        owner = scalar(note, "owner")
        allowed = contract["field_types"]["owner"]["values"]
        if owner and owner not in allowed:
            findings.append(Finding("ERROR", "bad-owner", rel, f"invalid project owner '{owner}'; allowed: {sorted(allowed)}"))
    apply_semantic_rules(spec, note, rel, findings, is_template=is_template)


def collect_targets(paths: list[str]) -> tuple[list[tuple[str, Path]], list[Finding]]:
    patterns = load_ignore_patterns()
    targets: dict[str, Path] = {}
    findings: list[Finding] = []
    if paths:
        for raw in paths:
            candidate = Path(raw)
            base = candidate if candidate.is_absolute() else ROOT / candidate
            if not base.exists():
                findings.append(Finding("ERROR", "missing-target", raw, "explicit lint target does not exist"))
                continue
            files = [base] if base.is_file() else sorted(base.rglob("*.md"))
            for path in files:
                try:
                    rel = str(path.resolve().relative_to(ROOT))
                except ValueError:
                    rel = str(path.resolve())
                targets[rel] = path
        return sorted(targets.items()), findings
    for path in sorted(ROOT.rglob("*.md")):
        rel = str(path.relative_to(ROOT))
        if not is_ignored(rel, patterns):
            targets[rel] = path
    return sorted(targets.items()), findings


def finding_fingerprint(finding: Finding) -> str:
    canonical = "\0".join((finding.severity, finding.check, finding.path, finding.message))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def scope_paths(paths: list[str], targets: list[tuple[str, Path]]) -> list[str]:
    del targets
    if not paths:
        return []
    normalized: list[str] = []
    for raw in paths:
        candidate = Path(raw)
        path = candidate if candidate.is_absolute() else ROOT / candidate
        try:
            normalized.append(str(path.resolve().relative_to(ROOT)))
        except ValueError:
            normalized.append(str(path.resolve()))
    return sorted(set(normalized))


def baseline_payload(contract: dict, findings: list[Finding], paths: list[str], targets: list[tuple[str, Path]]) -> dict:
    return {
        "format_version": BASELINE_FORMAT,
        "contract_version": contract["contract_version"],
        "schema_version": contract["schema_versions"]["current"],
        "fingerprint_algorithm": contract["lint"]["fingerprint_algorithm"],
        "scope_paths": scope_paths(paths, targets),
        "counts": {
            "ERROR": sum(item.severity == "ERROR" for item in findings),
            "WARN": sum(item.severity == "WARN" for item in findings),
        },
        "fingerprints": sorted({finding_fingerprint(item) for item in findings}),
    }


def baseline_path(contract: dict, raw: str | None) -> Path:
    configured = raw or contract["lint"]["baseline"]
    path = Path(configured)
    return path if path.is_absolute() else ROOT / path


def run_gate(contract: dict, findings: list[Finding], paths: list[str], targets: list[tuple[str, Path]], raw_baseline: str | None) -> int:
    path = baseline_path(contract, raw_baseline)
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR lint baseline unavailable or invalid: {path} ({exc})")
        return 1
    expected_meta = {
        "format_version": BASELINE_FORMAT,
        "contract_version": contract["contract_version"],
        "schema_version": contract["schema_versions"]["current"],
        "fingerprint_algorithm": contract["lint"]["fingerprint_algorithm"],
        "scope_paths": scope_paths(paths, targets),
    }
    mismatches = [key for key, value in expected_meta.items() if baseline.get(key) != value]
    if mismatches:
        print(f"ERROR lint baseline metadata mismatch: {mismatches}")
        return 1
    current = {finding_fingerprint(item): item for item in findings}
    accepted = set(baseline.get("fingerprints", []))
    new = sorted(set(current) - accepted)
    resolved = accepted - set(current)
    errors = sum(item.severity == "ERROR" for item in findings)
    warns = sum(item.severity == "WARN" for item in findings)
    baseline_counts = baseline.get("counts", {})
    print(f"AGENTS OS lint gate: ERROR={errors} WARN={warns} baseline_ERROR={baseline_counts.get('ERROR', '?')} baseline_WARN={baseline_counts.get('WARN', '?')} new={len(new)} resolved={len(resolved)}")
    if new:
        print("NO-GO: findings nuevos fuera del baseline")
        for fingerprint in new:
            finding = current[fingerprint]
            print(f"{finding.severity} [{finding.check}] {finding.path} — {finding.message}")
        return 1
    print("GO: no-new-debt; los findings actuales son subconjunto del baseline")
    return 0


def print_report(findings: list[Finding], targets: list[tuple[str, Path]], paths: list[str], mode: str) -> None:
    errors = sum(item.severity == "ERROR" for item in findings)
    warns = sum(item.severity == "WARN" for item in findings)
    no_type = sum(item.check in {"no-type", "no-frontmatter"} for item in findings)
    unknown = sum(item.check == "unknown-type" for item in findings)
    scope = f"{len(paths)} explicit path(s)" if paths else "all-vault"
    print(f"AGENTS OS lint ({mode}, {scope}): ERROR={errors} WARN={warns} notes_scanned={len(targets)} sin_type={no_type} tipos_desconocidos={unknown}")
    for item in findings:
        print(f"{item.severity} [{item.check}] {item.path} — {item.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="AGENTS OS contract-driven S1/S2 lint")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report; exit 1 on ERROR (default)")
    mode.add_argument("--strict", action="store_true", help="new/changed explicit paths; current schema and zero findings required")
    mode.add_argument("--gate", action="store_true", help="block only findings not present in the baseline")
    mode.add_argument("--emit-baseline", action="store_true", help="print deterministic baseline JSON; never writes")
    parser.add_argument("--baseline", help="baseline path override for --gate")
    parser.add_argument("paths", nargs="*", help="optional files/dirs; explicit paths bypass corpus exclusions")
    args = parser.parse_args()
    if args.strict and not args.paths:
        parser.error("--strict requires at least one explicit path")
    if args.baseline and not args.gate:
        parser.error("--baseline is only valid with --gate")
    try:
        contract = load_contract()
        type_index = contract_types(contract)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR schema contract is invalid: {exc}")
        return 1
    targets, findings = collect_targets(args.paths)
    for rel, path in targets:
        lint_note(contract, type_index, rel, path, findings, strict=args.strict)
    findings.sort(key=lambda item: ({"ERROR": 0, "WARN": 1}[item.severity], item.check, item.path, item.message))
    if args.emit_baseline:
        print(json.dumps(baseline_payload(contract, findings, args.paths, targets), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.gate:
        return run_gate(contract, findings, args.paths, targets, args.baseline)
    mode_name = "strict" if args.strict else "check"
    print_report(findings, targets, args.paths, mode_name)
    if args.strict:
        return 1 if findings else 0
    return 1 if any(item.severity == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
