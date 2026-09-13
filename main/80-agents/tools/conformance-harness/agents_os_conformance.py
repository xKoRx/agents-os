#!/usr/bin/env python3
"""AGENTS OS Conformance Harness — Test Model V1.

Implements the conformance suite defined in
`80-agents/tools/conformance-harness/artifacts/conformance-spec-v1.md`
(sections 3-10 are binding) and
`artifacts/conformance-scenarios.md` (25 scenarios).

Layers:
- L0 STATIC CONFORMANCE (8 scenarios): deterministic parse/grep of real files.
- L1 SIMULATED CONFORMANCE (16 scenarios): faithful executable transcription of
  the real bootstrap rules — lives in rules.py (single rules module, authority
  cited per rule) — run against real vault fixtures.
- L2 LIVE-EXPOSURE SMOKE (1 scenario, automated part): inspection of the
  machine surface MCP configs (read-only, names only) + context baseline.

Result states: PASS / FAIL / WARN / SKIP only (spec section 5).
Side-effect policy: read-only on the whole vault except results/ here
(spec section 7). No MCP invocation, no network, no mutation.

Python 3.9+ stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import rules  # noqa: E402  (local module: the single rules transcription)
from rules import (  # noqa: E402
    Session,
    Vault,
    normalize_area,
)

MARKER = "80-agents/agents-os/agents-os.md"

# Canonical sweep exclusions (spec section 4; doctor Check 1 + .graphifyignore):
# packaging copies, archive, journal, git, graphify state.
EXCLUDE_REL_PREFIXES = (
    "40-archive/",
    "80-agents/journal/",
    "30-resources/agents-os/",
    "80-agents/tools/conformance-harness/results/",
)
EXCLUDE_DIR_NAMES = {
    ".git", ".obsidian", ".trash", ".github", ".idea", ".vscode",
    "node_modules", "output", "graphify-out", "95-graphify", "00-inbox",
    "trash", "_sources",
}
EXCLUDE_FILE_PREFIXES = (".graphify", "graph.")


# ---------------------------------------------------------------------------
# Minimal frontmatter parser (spec section 6: no PyYAML). Supports `key: value`
# and simple `- item` lists; strips surrounding quotes.
# ---------------------------------------------------------------------------
def _unquote(val: str) -> str:
    val = val.strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        return val[1:-1].strip()
    return val


def parse_frontmatter(text: str) -> Dict[str, Any]:
    fm: Dict[str, Any] = {}
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.startswith("---"):
        return fm
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            end = i
            break
    if end is None:
        return fm
    current: Optional[str] = None
    for line in lines[1:end]:
        if re.match(r"^\S", line):
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$", line)
            if m:
                current = m.group(1)
                val = m.group(2).strip()
                fm[current] = [] if val == "" else _unquote(val)
        elif current is not None and re.match(r"^\s+-\s+", line):
            item = _unquote(re.sub(r"^\s+-\s+", "", line))
            cur = fm[current]
            if isinstance(cur, list):
                cur.append(item)
            else:
                fm[current] = [cur, item] if cur != "" else [item]
    return fm


# ---------------------------------------------------------------------------
# Vault sweeps and helpers
# ---------------------------------------------------------------------------
def iter_vault_md(root: str, subpath: str = "") -> List[str]:
    """All live *.md files under root/subpath with the canonical exclusions."""
    out: List[str] = []
    base = os.path.join(root, subpath) if subpath else root
    for dirpath, dirnames, filenames in os.walk(base):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel_dir == ".":
            rel_dir = ""
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in EXCLUDE_DIR_NAMES and not d.startswith(".")
            and not any((rel_dir + "/" + d).startswith(p) or (rel_dir + "/" + d) == p.rstrip("/")
                        for p in EXCLUDE_REL_PREFIXES)
        )
        full_rel_dir = (rel_dir + "/") if rel_dir else ""
        if any(full_rel_dir.startswith(p) for p in EXCLUDE_REL_PREFIXES):
            continue
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            if fn.startswith(EXCLUDE_FILE_PREFIXES):
                continue
            out.append(full_rel_dir + fn)
    return out


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def fm_of(root: str, rel: str) -> Dict[str, Any]:
    try:
        return parse_frontmatter(read_text(os.path.join(root, rel)))
    except OSError:
        return {}


def state_worst(states: List[str]) -> str:
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    for candidate in ("FAIL", "WARN", "PASS"):
        if candidate in states:
            return candidate
    return "SKIP"


def require_files(vault: Vault, rels: List[str]) -> List[str]:
    return [r for r in rels if not vault.exists(r)]


class Ctx(object):
    """Per-run context shared by scenarios."""

    def __init__(self, vault_root: str, no_live: bool):
        self.vault = Vault(vault_root, parse_frontmatter)
        self.root = vault_root
        self.no_live = no_live
        self.machine_surface: Optional[List[Dict[str, Any]]] = None
        if not no_live:
            self.machine_surface = read_surface_configs()


# ---------------------------------------------------------------------------
# L0 — STATIC CONFORMANCE
# ---------------------------------------------------------------------------
ANCHOR_CHECK_ID = "RULES-FIDELITY-ANCHORS"


def sc_rules_fidelity_anchors(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Adversarial-verification D2: static pre-flight guard (runs in every
    layer BEFORE the scenarios) asserting that the exact authority quotes the
    transcription module claims to transcribe (rules.FIDELITY_ANCHORS) still
    exist verbatim in the authority files: bootstrap SKILL.md domain gate
    lines, cold set lines, warm turn lines, entity swap lines and superseded
    rule; doctor Check 3 club lines. A missing anchor means rules.py went
    stale: the harness results for gate-dependent scenarios are not
    trustworthy (FAIL; in full/--layer runs the L0 gate then cuts L1/L2).
    A missing authority file FAILS (never crashes). Matching collapses
    whitespace runs only (line wraps): the words must be exact."""
    problems: List[str] = []
    evidence: List[str] = []
    by_authority: Dict[str, List[Tuple[str, str]]] = {}
    for aid, authority, quote in rules.FIDELITY_ANCHORS:
        by_authority.setdefault(authority, []).append((aid, quote))
    for authority in sorted(by_authority):
        entries = by_authority[authority]
        try:
            text = read_text(os.path.join(ctx.root, authority))
        except OSError:
            problems.append("archivo de autoridad ausente o ilegible: %s — la transcripcion de rules.py no es verificable contra el texto vigente" % authority)
            continue
        flat = " ".join(text.split())
        missing = ["[%s] %s" % (aid, quote) for aid, quote in entries
                   if " ".join(quote.split()) not in flat]
        evidence.append("%s: %d anclas verificadas (%s)%s" % (
            authority, len(entries), ", ".join(aid for aid, _ in entries),
            ("; %d ausente(s)" % len(missing)) if missing else ""))
        problems.extend(
            "ancla de fidelidad ausente en %s: %s — la transcripcion quedo obsoleta y los resultados de los escenarios dependientes del gate no son confiables" % (authority, m)
            for m in missing)
    if problems:
        return "FAIL", "la transcripcion de rules.py no coincide con el texto vigente de las autoridades (D2)", problems + evidence
    return ("PASS",
            "todas las anclas de fidelidad de rules.py (%d) existen en el texto vigente de las autoridades" % len(rules.FIDELITY_ANCHORS),
            evidence)


def sc_schema_validator_green(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: 80-agents/skills/_shared/metadata-schema.md ("Este gate debe
    quedar verde..."), 90-system/convenciones.md, C17, scenario
    SCHEMA-VALIDATOR-GREEN. The validator is invoked read-only (verification
    mode); the materializer is NOT executed (spec section 7)."""
    validator = os.path.join(
        ctx.root, "80-agents/skills/_shared/scripts/validate_schema_contract.py")
    if not os.path.isfile(validator):
        return "SKIP", "validador no encontrado en el vault", []
    try:
        proc = subprocess.run(
            [sys.executable, validator], cwd=ctx.root, capture_output=True,
            text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "FAIL", "validador excedio el timeout (120s)", []
    tail = [ln for ln in (proc.stdout.strip().splitlines() + proc.stderr.strip().splitlines()) if ln][-6:]
    if proc.returncode == 0:
        return "PASS", "validador del schema-contract en verde (exit 0)", tail
    return ("FAIL",
            "validador del schema-contract en rojo (exit %d); contrato exige exit 0 "
            "(C17: estado observado verde al 2026-09-09 — drift del corpus)" % proc.returncode,
            tail)


STARTUP_WATCHED_RELS = ["AGENTS.md", "80-agents/agents-os/agents-os.md"]
_BASE_PATH_RE = re.compile(
    r"(agent-constitution\.md|memory/public/user-preference/|"
    r"agents-os-operating-continuity|skills/INDEX\.md)", re.I)
_IMPERATIVE_START_RE = re.compile(
    r"^\s*(?:[-*+]\s+)?(?:\d+[.)]\s+)?"
    r"(load|loads|carga|cargar|cargue|lee|leer|lea|read|abrir|abre|open|incluye)\b",
    re.I)
_NUM_LINE_RE = re.compile(r"^\s*\d+[.)]\s+")
_BASE_WORD_RE = re.compile(
    r"(constituci|constitution|perfil global|profile|INDEX|continuidad|continuity|bootstrap)", re.I)
_LOAD_VERB_RE = re.compile(r"\b(load|carga|cargar|leer|lee|read|abrir)\b", re.I)


def _startup_dup_hits(root: str, rel: str) -> List[str]:
    """Harness-defined heuristic for doctor Check 4 (no authority defines the
    'procedural startup steps' boundary — contract-audit C01/C03 Unknown;
    boundary fixed by documented definition, not by authority):
    D1 imperative load instruction at line/list-item start mentioning a
    base-stack path; D2 numbered sequences (>=2 lines) combining load verbs
    with base-stack words; D3 'Load:/Carga:' checklists."""
    hits: List[str] = []
    try:
        lines = read_text(os.path.join(root, rel)).splitlines()
    except OSError:
        return hits
    num_hits = 0
    for i, line in enumerate(lines):
        if _BASE_PATH_RE.search(line) and _IMPERATIVE_START_RE.match(line):
            hits.append("%s:%d D1 instruccion imperativa de carga sobre path base: %s" % (rel, i + 1, line.strip()[:120]))
        if _NUM_LINE_RE.match(line) and _BASE_WORD_RE.search(line) and _LOAD_VERB_RE.search(line):
            num_hits += 1
        elif num_hits and not _NUM_LINE_RE.match(line) and line.strip():
            num_hits = 0
        if num_hits >= 2:
            hits.append("%s:%d D2 secuencia numerada de arranque con verbos de carga" % (rel, i + 1))
            num_hits = 0
    joined = "\n".join(lines)
    if re.search(r"(?im)^\s*(load|carga)\s*:\s*\S", joined):
        block = re.search(r"(?im)^\s*(load|carga)\s*:\s*\S.*(?:\n.*){0,4}", joined).group(0)
        if len(_BASE_WORD_RE.findall(block)) >= 2:
            hits.append("%s D3 checklist 'Load:' de stack base fuera de bootstrap" % rel)
    return hits


def sc_startup_duplication(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: bootstrap Hard Rules ("This skill is the only startup
    procedure..."), constitucion Autoridad, doctor Check 4, C01."""
    watched: List[str] = list(STARTUP_WATCHED_RELS)
    watched += [os.path.join("80-agents/crew", f) for f in sorted(os.listdir(os.path.join(ctx.root, "80-agents/crew"))) if f.endswith(".md")] if os.path.isdir(os.path.join(ctx.root, "80-agents/crew")) else []
    watched += iter_vault_md(ctx.root, "10-projects")
    watched += iter_vault_md(ctx.root, "20-areas")
    hits: List[str] = []
    for rel in watched:
        hits.extend(_startup_dup_hits(ctx.root, rel))
    if hits:
        return "FAIL", "pasos procedimentales de startup fuera de agents-os-bootstrap/SKILL.md (doctor Check 4 / C01)", hits[:20]
    return "PASS", "el unico texto procedimental de startup vive en agents-os-bootstrap/SKILL.md (AGENTS.md solo lo invoca; agents-os.md es mapa+routing; heuristicas D1/D2/D3 sin hits)", []


CLUB_MEMBERS = {
    "80-agents/agents-os/agent-constitution.md",
    "80-agents/skills/agents-os-bootstrap/SKILL.md",
    "80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md",
}


def sc_closed_club_always(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: doctor Check 3, bootstrap Hard Rules, C08 (scenario
    CLOSED-CLUB-ALWAYS). Frontmatter-only scan over all live md."""
    found: List[str] = []
    pref_always: List[str] = []
    for rel in iter_vault_md(ctx.root):
        fm = fm_of(ctx.root, rel)
        if str(fm.get("load_policy", "")).strip().strip("\"'") == "always":
            found.append(rel)
            if rel.startswith("80-agents/memory/public/user-preference/"):
                pref_always.append(rel)
    evidence = ["always encontrados (%d): %s" % (len(found), ", ".join(found) or "-")]
    profile = [f for f in found if f.startswith("80-agents/memory/public/user-preference/")]
    problems: List[str] = []
    for member in sorted(CLUB_MEMBERS):
        if member not in found:
            problems.append("miembro del club ausente o sin always: %s" % member)
    for f in found:
        if f not in CLUB_MEMBERS and not f.startswith("80-agents/memory/public/user-preference/"):
            problems.append("quinto archivo con always (violacion C08): %s" % f)
    if len(pref_always) != 1:
        problems.append("user-preference/ debe contener EXACTAMENTE una nota always (doctor Check 3); hoy: %d %s" % (len(pref_always), pref_always))
    if problems:
        return "FAIL", "closed club load_policy: always violado", evidence + problems
    return ("PASS",
            "closed club exacto: constitucion + bootstrap + perfil global (%s) + continuidad interna global; 0 terceros" % os.path.basename(profile[0]),
            evidence)


BASE_VOCAB_OK = {"manual", "never", "when_project_loaded", "when_application_loaded", "when_error_matches"}
WARN_VOCAB = {"when_area_loaded", "when_echo_forge_loaded", "when_entity_loaded", "when_installing_graphify_obsidian"}
GLOBAL_INTERNAL_REL = rules.GLOBAL_INTERNAL


def sc_load_policy_vocabulary(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: schema-contract ("concrete runtime trigger"), bootstrap Hard
    Rules enumeration, constitucion Memoria Interna, doctor Check 7, C09
    (scenario LOAD-POLICY-VOCABULARY; detects Hallazgos 7, 11 y 12). Declared
    extras are WARN by design (spec section 5); abstract triggers,
    always outside the club and superseded/archived with automatic trigger are
    FAIL."""
    fails: List[str] = []
    warns: List[str] = []
    counts: Dict[str, int] = {}
    scanned = 0
    for sub in ("80-agents/memory", "30-resources/agents/skills", "80-agents/skills"):
        for rel in iter_vault_md(ctx.root, sub):
            fm = fm_of(ctx.root, rel)
            if "load_policy" not in fm:
                continue
            scanned += 1
            lp = str(fm.get("load_policy", "")).strip().strip("\"'").lower()
            counts[lp] = counts.get(lp, 0) + 1
            state = str(fm.get("memory_state", "")).strip().strip("\"'").lower()
            if lp == "always":
                if rel not in CLUB_MEMBERS and not rel.startswith("80-agents/memory/public/user-preference/"):
                    fails.append("always fuera del closed club: %s" % rel)
            elif lp in BASE_VOCAB_OK:
                pass
            elif lp in WARN_VOCAB:
                if lp == "when_area_loaded" and rel.endswith("rjara-vpn-routing-preferences.md"):
                    warns.append("Hallazgo 7: %s usa %s con scope=%s sin campo area (trigger no resoluble por area; cross-domain sin arbitro)" % (rel, lp, fm.get("scope")))
                else:
                    warns.append("trigger when_*_loaded fuera de la enumeracion literal de bootstrap (C09 WARN): %s -> %s" % (rel, lp))
            else:
                fails.append("trigger no clasificable como concrete runtime trigger: %s -> %s" % (rel, lp))
            # doctor Check 7: internal non-global scope; lifecycle consistency.
            if rel.startswith("80-agents/memory/internal/") and rel != GLOBAL_INTERNAL_REL:
                scope = str(fm.get("scope", "")).strip().strip("\"'").lower()
                if scope == "global":
                    fails.append("memoria interna no-global con scope: global (doctor Check 7): %s" % rel)
            if state in ("superseded", "archived"):
                if lp not in ("manual", "never"):
                    fails.append("nota %s con trigger automatico (%s): %s (C14)" % (state, lp, rel))
                ip = str(fm.get("index_priority", "")).strip().strip("\"'").lower()
                if ip and ip not in ("low", "never"):
                    fails.append("nota %s con index_priority=%s (esperado low/never): %s" % (state, ip, rel))
                elif not ip:
                    warns.append("nota %s sin index_priority (legacy sin lifecycle completo, note-types): %s" % (state, rel))
    evidence = ["notas con load_policy escaneadas: %d" % scanned,
                "distribucion: %s" % json.dumps(counts, sort_keys=True, ensure_ascii=False)]
    evidence += sorted(warns)[:24]
    if fails:
        return "FAIL", "vocabulario load_policy con violaciones", evidence + sorted(fails)[:20]
    if warns:
        return ("WARN",
                "extras de vocabulario documentados (C09/Hallazgos 7+12) sin autoridad que fije precedencia entre enumeraciones; sin FAILs",
                evidence)
    return "PASS", "vocabulario load_policy conformante", evidence


def _parse_index_tables(text: str) -> Dict[str, List[str]]:
    """Extract INDEX.md rows per section (core / federated / app-owned)."""
    sections = {"core": [], "federated": [], "app-owned": []}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = "core" if "Catálogo core" in line else None
        elif line.startswith("### "):
            if "Dominio y transversales" in line:
                current = "federated"
            elif "App-owned" in line:
                current = "app-owned"
            elif current == "federated":
                current = None
        if current and line.startswith("|") and not line.startswith("|--") and not line.startswith("| ---"):
            if current == "app-owned":
                m = re.search(r"\|\s*`([^`]+)`\s*→\s*`([^`]+)`\s*\|", line)
                if m:
                    sections["app-owned"].append(line.strip())
            else:
                m = re.search(r"\[\[(?:80-agents/skills|30-resources/agents/skills)/([^/#|\]]+)/SKILL", line)
                if m:
                    sections[current].append(line.strip())
    return sections


def _row_name(row: str) -> str:
    m = re.search(r"\[\[[^\]|]+/SKILL(?:\.md)?\|([^\]]+)\]\]", row)
    if m:
        return m.group(1).strip()
    m = re.search(r"/([^/]+)/SKILL", row)
    return m.group(1) if m else ""


def _parse_index_declared_counts(text: str) -> Dict[str, int]:
    """Counts declared by the INDEX.md callout (Core/Federadas/App-owned)."""
    declared: Dict[str, int] = {}
    for key, pat in (
            ("core", r"\*\*Core AGENTS OS:\*\*\s*(\d+)"),
            ("federated", r"\*\*Federadas \(vault\):\*\*\s*(\d+)"),
            ("app-owned", r"\*\*App-owned:\*\*\s*(\d+)")):
        m = re.search(pat, text)
        if m:
            declared[key] = int(m.group(1))
    return declared


def sc_registry_disk_parity(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: doctor Check 8, bootstrap paso 3 + Lazy Skill Routing, C12
    (scenario REGISTRY-DISK-PARITY). Bidirectional parity INDEX.md <-> disk."""
    text = read_text(os.path.join(ctx.root, "80-agents/skills/INDEX.md"))
    sections = _parse_index_tables(text)
    core_index = sorted({_row_name(r) for r in sections["core"]})
    fed_index = sorted({_row_name(r) for r in sections["federated"]})
    core_disk = sorted(
        d for d in os.listdir(os.path.join(ctx.root, "80-agents/skills"))
        if os.path.isfile(os.path.join(ctx.root, "80-agents/skills", d, "SKILL.md")) and not d.startswith("_"))
    fed_disk = sorted(
        d for d in os.listdir(os.path.join(ctx.root, "30-resources/agents/skills"))
        if os.path.isfile(os.path.join(ctx.root, "30-resources/agents/skills", d, "SKILL.md")))
    problems: List[str] = []
    evidence = [
        "INDEX core=%d federadas=%d app-owned=%d (callout declara 28/19/3)" % (len(core_index), len(fed_index), len(sections["app-owned"])),
        "disco core=%d federadas=%d" % (len(core_disk), len(fed_disk)),
    ]
    # Callout counts: what INDEX.md DECLARES vs what the tables actually
    # contain (mismatch is a registry integrity drift -> WARN, not FAIL).
    declared = _parse_index_declared_counts(text)
    parsed_counts = {"core": len(core_index), "federated": len(fed_index),
                     "app-owned": len(sections["app-owned"])}
    count_mismatch: List[str] = []
    if declared:
        evidence.append("conteos declarados por el callout de INDEX: %s" % json.dumps(declared, sort_keys=True))
        for key in sorted(declared):
            if declared[key] != parsed_counts[key]:
                count_mismatch.append("callout de INDEX declara %s=%d pero el registro parseado tiene %d filas" % (key, declared[key], parsed_counts[key]))
    else:
        evidence.append("callout de conteos declarado no encontrado en INDEX.md: sub-check de conteos declarados no ejecutable")
    for name in sorted(set(core_disk) - set(core_index)):
        problems.append("skill en disco ausente de INDEX (core): %s" % name)
    for name in sorted(set(core_index) - set(core_disk)):
        problems.append("fila core de INDEX sin SKILL.md en disco: %s" % name)
    for name in sorted(set(fed_disk) - set(fed_index)):
        problems.append("skill en disco ausente de INDEX (federada): %s" % name)
    for name in sorted(set(fed_index) - set(fed_disk)):
        problems.append("fila federada de INDEX sin SKILL.md en disco: %s" % name)
    # App-owned rows: repo + relative path, never an absolute machine path
    # (INDEX: "El registry enlaza por repo + path relativo", constitucion inv. 11).
    app_rows = sections["app-owned"]
    parsed_app: List[Tuple[str, str]] = []
    for row in app_rows:
        m = re.search(r"`([^`]+)`\s*→\s*`([^`]+)`", row)
        if not m or "→" not in row:
            problems.append("fila app-owned mal formada (esperado `repo` → `.agents/skills/...`): %s" % row[:100])
            continue
        repo, rel = m.group(1), m.group(2)
        parsed_app.append((repo, rel))
        if not re.match(r"^[^/]+/[^/]+ \.", rel) and not rel.startswith(".agents/skills/"):
            problems.append("fila app-owned sin path relativo `.agents/skills/`: %s" % row[:100])
        if "/home/" in row or "~/" in row or "file://" in row:
            problems.append("fila app-owned persiste path absoluto de maquina (violacion inv. 11): %s" % row[:100])
    # Physical existence verified only if the owner workspace is reachable
    # (repo lives outside VAULT_ROOT, constitucion regla 12) — SKIP sub-check
    # otherwise (scenario REGISTRY-DISK-PARITY observable_evidence).
    repo_dir = None
    home = os.path.expanduser("~")
    for cand in ("go/src/github.com/xKoRx/symphony", "src/github.com/xKoRx/symphony",
                 "code/xKoRx/symphony", "dev/xKoRx/symphony", "xKoRx/symphony"):
        p = os.path.join(home, cand)
        if os.path.isdir(p):
            repo_dir = p
            break
    if repo_dir:
        for repo, rel in parsed_app:
            if not os.path.isfile(os.path.join(repo_dir, rel)):
                problems.append("skill app-owned inexistente en repo owner %s: %s" % (repo, rel))
        evidence.append("repo owner alcanzable en disco: verificacion fisica de %d filas app-owned" % len(parsed_app))
    else:
        evidence.append("SKIP sub-check: workspace del repo owner (%s) no alcanzable desde esta maquina" % (parsed_app[0][0] if parsed_app else "xKoRx/symphony"))
    if problems:
        return "FAIL", "paridad INDEX.md <-> disco violada", evidence + problems[:20]
    if count_mismatch:
        return ("WARN",
                "paridad bidireccional OK; el callout de conteos declarado por INDEX.md no coincide con las filas parseadas",
                evidence + count_mismatch)
    return "PASS", "paridad exacta en ambas direcciones (core y federadas); conteos del callout verificados contra las filas parseadas; filas app-owned por repo+path relativo", evidence


def _classify_index_use(use: str, name: str) -> str:
    u = use.lower()
    if name == "meli-agent-dev":
        return "meli"
    if name in ("aranea-agent-dev", "aranea-mcps-expert"):
        return "aranea"
    if re.search(r"v[ií]a\s+`?meli-agent-dev", u):
        return "meli-dual" if "obra propia" in u else "meli"
    if "dominio aranea" in u or "homelab" in u:
        return "aranea"
    if "corporativo meli" in u:
        return "meli"
    return "transversal"


def sc_dual_registry_domain_sync(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: Hallazgo 16 ("las clasificaciones de ambos registros deben
    coincidir skill a skill"), C13, scenario DUAL-REGISTRY-DOMAIN-SYNC."""
    index_text = read_text(os.path.join(ctx.root, "80-agents/skills/INDEX.md"))
    federated = _parse_index_tables(index_text)["federated"]
    wiki_text = read_text(os.path.join(ctx.root, "30-resources/agents/00-index.md"))
    wiki: Dict[str, str] = {}
    for line in wiki_text.splitlines():
        m = re.search(r"\|\s*\[\[30-resources/agents/skills/([^/#|\]]+)/SKILL[^\]]*\]\]", line)
        if m:
            cls = "meli" if "Meli-only" in line else "aranea" if "Aranea-only" in line else "transversal" if "transversal" in line else ""
            if cls:
                wiki[m.group(1)] = cls
    problems: List[str] = []
    warns: List[str] = []
    compared = 0
    evidence: List[str] = []
    for row in federated:
        name = _row_name(row)
        cells = [c.strip() for c in row.strip("|").split("|")]
        use = cells[-1] if cells else ""
        icls = _classify_index_use(use, name)
        wcls = wiki.get(name, "")
        if not wcls:
            evidence.append("sin fila equivalente en 00-index para %s (no comparada)" % name)
            continue
        compared += 1
        if icls == "meli-dual":
            if wcls != "transversal" and wcls != "meli":
                problems.append("dual de INDEX contradicho por 00-index (%s): %s" % (name, wcls))
            else:
                warns.append("pr-description: INDEX declara clausula dual ('Vía meli-agent-dev u obra propia del vault') y 00-index la clasifica %s; ninguna autoridad define la semantica exacta de la columna (WARN de escenario)" % ("transversal" if wcls == "transversal" else "Meli-only"))
        elif icls != wcls and not (icls == "transversal" and wcls == "transversal"):
            problems.append("clasificacion divergente sin clausula dual: %s INDEX=%s vs 00-index=%s" % (name, icls, wcls))
    if "se excluyen mutuamente" not in wiki_text:
        problems.append("00-index no declara la exclusividad mutua de los routers en 'MCP Aranea y dominios de agente'")
    if not re.search(r"Excluye", index_text):
        problems.append("INDEX.md no declara exclusion de dominio en las filas de routers")
    evidence.append("skills comparadas skill a skill: %d/%d" % (compared, len(federated)))
    if problems:
        return "FAIL", "registros duales desincronizados (Hallazgo 16)", evidence + problems
    if warns:
        return "WARN", "sincronia de dominio OK; divergencia dual pr-description registrada como WARN documentado", evidence + warns
    return "PASS", "clasificacion de dominio coincide skill a skill en ambos registros", evidence


SECRET_KW = r"(?i)\b(?:password|passwd|pgpassword|secret|api[_-]?key|apikey|access[_-]?key|token|pwd|bearer)\b"
P_ASSIGN = re.compile(SECRET_KW + r"\s*[:=]\s*[\"']?([^\s\"'`]{6,})")
P_BEARER = re.compile(r"(?i)\bBearer\s+([A-Za-z0-9_\-.=+/]{12,})")
P_AKIA = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
P_QUOTED = re.compile(SECRET_KW + r"[^:=\n]{0,24}[\"'`]([A-Za-z0-9][A-Za-z0-9_\-.:/]{11,})[\"'`]")
P_PRIVKEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
# Placeholders/templates that are never values: angle-bracket refs, templating,
# secret-refs, examples, code fragments (trailing ')'), version templates.
P_PLACEHOLDER = re.compile(
    r"(^\s*<|\{\{|\$\(|\}\}|secret-ref|example|changeme|your[-_]|xxxx|\.\.\.|^\s*\{|\)$|[Xx]\.[Yy]\.[Zz]\b)")
P_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def _bearer_is_value(tok: str) -> bool:
    """A bearer VALUE looks like a credential: contains a digit or is long
    (>=20). Prose after the word 'Bearer' (p. ej. 'Bearer constant-time') is
    not a value."""
    return any(c.isdigit() for c in tok) or len(tok) >= 20


def _scan_secret_line(line: str) -> List[str]:
    """Returns pattern ids whose VALUE class is: 'hard' (credential-shaped) or
    'soft' (ambiguo, p.ej. UUID de identidad). Never returns the value."""
    out: List[str] = []
    if P_PRIVKEY.search(line):
        out.append("hard:privkey")
    if P_AKIA.search(line):
        out.append("hard:akia")
    m = P_BEARER.search(line)
    if m and not P_PLACEHOLDER.search(m.group(1)) and _bearer_is_value(m.group(1)):
        out.append("hard:bearer")
    m = P_ASSIGN.search(line)
    if m and not P_PLACEHOLDER.search(m.group(1)):
        out.append("hard:assign")
    m = P_QUOTED.search(line)
    if m and not P_PLACEHOLDER.search(m.group(1)):
        out.append("soft:uuid" if P_UUID.match(m.group(1)) else "hard:quoted")
    return out


def _secret_scan_scope_a(ctx: Ctx) -> List[Tuple[str, int, str]]:
    hits: List[Tuple[str, int, str]] = []
    for rel in iter_vault_md(ctx.root, "80-agents/memory/internal"):
        try:
            lines = read_text(os.path.join(ctx.root, rel)).splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            for cls in _scan_secret_line(line):
                hits.append((rel, i + 1, cls))
    return hits


def _secret_scan_scope_b(ctx: Ctx) -> List[Tuple[str, int, str]]:
    hits: List[Tuple[str, int, str]] = []
    for rel in iter_vault_md(ctx.root):
        try:
            text = read_text(os.path.join(ctx.root, rel))
        except OSError:
            continue
        lines = text.split("\n")
        # frontmatter block
        fm_end = 0
        if text.startswith("---"):
            for i in range(1, len(lines)):
                if lines[i].rstrip() == "---":
                    fm_end = i
                    break
        # fenced code blocks
        in_code = False
        for i, line in enumerate(lines):
            if i <= fm_end or (in_code and i > fm_end):
                for cls in _scan_secret_line(line):
                    hits.append((rel, i + 1, cls))
            if line.lstrip().startswith("```"):
                in_code = not in_code
    return hits


def sc_no_secrets_in_markdown(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: constitucion regla 9, aranea-mcps-expert Hard Rules, doctor
    Check 7 (scope (a) exacto: 80-agents/memory/internal/**), C16. Scope (b):
    frontmatter + code blocks de todo md vivo. Values are never printed
    (doctor: "The script never prints matched secret values")."""
    a = _secret_scan_scope_a(ctx)
    b = _secret_scan_scope_b(ctx)
    hard = [h for h in a + b if h[2].startswith("hard")]
    soft = [h for h in a + b if h[2].startswith("soft")]
    evidence = [
        "scope (a) internal/**: %d linea(s) con patron de valor" % len(a),
        "scope (b) frontmatter+code de todo md vivo: %d linea(s)" % len(b),
        "valores jamas impresos; clases: %s" % (", ".join(sorted({h[2] for h in a + b})) or "-"),
    ]
    evidence += ["soft (posible identificador, no credencial demostrada): %s:%d %s" % h for h in soft[:10]]
    if hard:
        evidence += ["hard: %s:%d %s" % h for h in hard[:20]]
        return "FAIL", "valor de secreto/credencial en Markdown vivo del alcance", evidence
    if soft:
        return ("WARN",
                "0 valores credenciales; %d patron(es) ambiguo(s) keyword+UUID registrados como riesgo verificable (identidad vs token)" % len(soft),
                evidence)
    return "PASS", "0 hits con valores en el alcance (bearers viven en configs de maquina, fuera del vault — Hallazgo 15)", evidence


CANON_AREAS = {"meli": "meli", "echo": "aranea", "aranea": "aranea"}
PUBLIC_DOMAIN_FOLDERS = {
    "rio": "meli", "meli": "meli",
    "symphony": "aranea", "aranea": "aranea", "echo": "aranea", "echo-forge": "aranea",
}
SLUG_DOMAIN_HINTS = {
    "meli": ("meli", "rio", "fury", "signals", "spellbook", "playmaker"),
    "aranea": ("echo", "symphony", "forge", "aranea", "hermes", "sqx"),
}


def sc_active_memory_domain_purity(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """Authority: bootstrap Hard Rules ("one active checkpoint per
    continuity_key"), constitucion Memoria Interna, doctor Check 7, C14;
    area mapping per bootstrap paso 6. WARN dims: [[Echo Forge]] area drift
    (Hallazgo 11); 'cero activas Meli' es estado observado, no invariante."""
    fails: List[str] = []
    warns: List[str] = []
    evidence: List[str] = []
    actives_by_key: Dict[str, List[str]] = {}
    domain_counts = {"meli": 0, "aranea": 0, "global": 0, "otro": 0}
    internal_rels = iter_vault_md(ctx.root, "80-agents/memory/internal")
    for rel in internal_rels:
        fm = fm_of(ctx.root, rel)
        state = str(fm.get("memory_state", "")).strip().strip("\"'").lower()
        if state != "active":
            continue
        key = str(fm.get("continuity_key", "")).strip().strip("\"'")
        actives_by_key.setdefault(key, []).append(rel)
        area = normalize_area(fm.get("area"))
        if rel == rules.GLOBAL_INTERNAL:
            domain_counts["global"] += 1
            continue
        dom = CANON_AREAS.get(area or "")
        slug = os.path.basename(rel)
        hint = None
        for d, kws in SLUG_DOMAIN_HINTS.items():
            if any(k in slug.lower() for k in kws):
                hint = d
                break
        if dom:
            domain_counts[dom] += 1
            if hint and hint != dom:
                fails.append("fuga de dominio en memoria activa: %s declara area %s (=%s) pero su contenido apunta a %s" % (rel, fm.get("area"), dom, hint))
        elif area == "echo forge":
            warns.append("activa con area no canonica del gate (Hallazgo 11): %s -> [[Echo Forge]] no es valor del gate (solo Meli/Echo/Aranea)" % rel)
            domain_counts["otro"] += 1
        else:
            warns.append("activa con area no reconocida por el gate: %s -> %s" % (rel, fm.get("area")))
            domain_counts["otro"] += 1
    for key, rels in sorted(actives_by_key.items()):
        if len(rels) > 1:
            fails.append("continuity_key '%s' tiene %d notas active (debe ser exactamente una): %s" % (key, len(rels), ", ".join(rels)))
    # Public scoped notes: declared area vs canonical area of its domain folder.
    public_checked = 0
    for rel in iter_vault_md(ctx.root, "80-agents/memory/public"):
        parts = rel.split("/")
        if len(parts) < 5:
            continue
        folder = parts[3] if len(parts) > 4 else ""
        leaf = parts[4] if len(parts) > 4 else ""
        dom = PUBLIC_DOMAIN_FOLDERS.get(leaf)
        if not dom or "." in leaf:
            continue
        fm = fm_of(ctx.root, rel)
        area = normalize_area(fm.get("area"))
        if not area:
            continue
        public_checked += 1
        cdom = CANON_AREAS.get(area)
        if cdom is None:
            warns.append("public scoped con area no canonica (Hallazgo 11): %s -> [[%s]] en carpeta de dominio %s" % (rel, area, leaf))
        elif cdom != dom:
            warns.append("public scoped con area de otro dominio (Hallazgo 11): %s -> [[%s]] en carpeta %s" % (rel, area, leaf))
    evidence.append("activas internas por dominio: %s (conteo = estado observado, no invariante)" % json.dumps(domain_counts))
    evidence.append("continuity_keys activos: %d; notas public scoped comparadas: %d" % (len(actives_by_key), public_checked))
    evidence.append("fixture C14: %s" % rules.CONTINUITY_ARCHIVE)
    if fails:
        return "FAIL", "pureza de dominio de memoria activa violada", evidence + sorted(fails)
    if warns:
        return "WARN", "unicidad de continuity_key OK; drift de areas [[Echo Forge]]/[[Personal]] documentado (Hallazgo 11) registrado como WARN", evidence + sorted(warns)[:16]
    return "PASS", "un checkpoint activo por continuity_key; areas canonicas conformantes", evidence


# ---------------------------------------------------------------------------
# L1 — SIMULATED CONFORMANCE (replicates rules.py against real fixtures)
# ---------------------------------------------------------------------------
BASE_4 = [rules.CONSTITUTION, rules.USER_PREF_DIR + "rjara-agent-profile.md",
          rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX]
NOT_LOAD_DEFAULT = [
    rules.ROUTERS["meli"], rules.ROUTERS["aranea"], rules.ARANEA_MCPS_EXPERT,
    rules.ROUTER_PREFS["meli"][0], rules.ROUTER_PREFS["aranea"][0],
    rules.AGENTS_OS_MAP, rules.FEDERATED_DOMAIN_INDEX, rules.AGENTS_OS_PROJECT,
    rules.CONTINUITY_ARCHIVE,
]
MELI_ECHO_ACTIVE_NOTES = [
    "80-agents/memory/internal/agent-memory/2026-09-04-echo-forge-mt5-6180-parser-cert-continuity.md",
    "80-agents/memory/internal/agent-memory/2026-09-05-echo-forge-full-golden-flow-continuity.md",
    "80-agents/memory/internal/agent-memory/2026-09-06-echo-forge-finalist-model-v2.md",
    "80-agents/memory/internal/agent-memory/2026-09-06-echo-forge-mt5-slot-pool-long-running-v2.md",
]
FURY_NOTE = "80-agents/memory/public/known-error/rio/2026-08-19-rio-fury-segment-suffix-breaks-last-token-profile-resolution.md"
PLAYMAKER_NOTE = "80-agents/memory/public/decision/rio/2026-08-25-playmaker-cp-idempotency-boundary.md"
MT5_NOTE = MELI_ECHO_ACTIVE_NOTES[0]


def _base_assertions(s: Session, evidence: List[str]) -> List[str]:
    """Common cold-set contract (bootstrap pasos 1-3, C02)."""
    problems: List[str] = []
    opens = s.all_opens()
    for f in [rules.CONSTITUTION, rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX]:
        if f not in opens:
            problems.append("archivo base no cargado en cold start: %s" % f)
    if s.profile_note is None or s.profile_note not in opens:
        problems.append("perfil global (unica always de user-preference) no resuelto/cargado")
    if agents_os_map_opened(opens):
        problems.append("agents-os.md abierto por ritual (paso 4 lo prohibe)")
    if s.bootstrap_runs != 1:
        problems.append("bootstrap ejecutado %d veces (debe ser 1)" % s.bootstrap_runs)
    evidence.append("stack base cargado: %s" % ", ".join(opens[:4]))
    return problems


def agents_os_map_opened(opens: List[str]) -> bool:
    return rules.AGENTS_OS_MAP in opens


def _assert_absent(not_load: List[str], opens: List[str], evidence: List[str]) -> List[str]:
    problems = []
    for f in not_load:
        if f in opens:
            problems.append("carga prohibida detectada: %s" % f)
    evidence.append("expected_not_load verificado (%d paths): ninguno abierto" % len(not_load))
    return problems


def _load_policy_note(fm: Dict[str, Any]) -> str:
    return str(fm.get("load_policy", ""))


def sc_cold_default(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """COLD-DEFAULT: casual request, no entity -> no router (contrato literal,
    bootstrap pasos 5-7)."""
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    missing = s.cold_start({"entity_title": "entidad-fantasma-xyz", "casual": True})
    if missing:
        return "FAIL", "archivo del stack base inexistente en disco", ["faltantes: %s" % missing]
    ghost = ctx.vault.resolve_entity("entidad-fantasma-xyz")
    evidence.append("entidad fantasma 'entidad-fantasma-xyz' no resuelve a ninguna nota (fixture): %s" % (ghost is None))
    problems = _base_assertions(s, evidence)
    problems += _assert_absent(NOT_LOAD_DEFAULT, s.all_opens(), evidence)
    if s.active_domain is not None:
        problems.append("router activo sin entidad resoluble: %s" % s.active_domain)
    if s.active_entity is not None:
        problems.append("entidad activa inesperada: %s" % s.active_entity.get("title"))
    if s.pack_files:
        problems.append("pack de dominio cargado en DEFAULT: %s" % s.pack_files)
    evidence.append("estado: session_mode=%s active_entity=%s active_domain=%s bootstrap_runs=%d" % (
        s.session_mode, s.active_entity, s.active_domain, s.bootstrap_runs))
    evidence.append("gate: %s" % s.gate_note)
    # WARN obligatorio (Hallazgo 6 / Hallazgos 4): la clausula de evidencia de
    # superficie del paso 6 + conexion permanente de mcp__aranea-* puede
    # colapsar la ejecucion real a ARANEA; la replicacion usa la lectura de
    # contrato literal y registra la ambiguedad sin resolverla.
    surface = ""
    if ctx.machine_surface:
        surface = "; configs de maquina observadas: %s" % ", ".join(
            "%s aranea=%d meli=%d" % (c["surface"], c["aranea"], c["meli"]) for c in ctx.machine_surface)
    state = "FAIL" if problems else "WARN"  # WARN declarado por diseno (spec section 5)
    details = "cold start DEFAULT sin router (contrato literal del paso 6)" if not problems else "cold start DEFAULT violo el contrato"
    evidence += problems + ["WARN declarado (Hallazgo 6): la clausula de evidencia de superficie del paso 6 no distingue evidencia ambiental de evidencia de tarea; con mcp__aranea-* conectados permanentemente%s una sesion real sin entidad puede colapsar a ARANEA. Registrado como WARN, no resuelto (COLD-DEFAULT observable_evidence)." % surface]
    return state, details, evidence


def sc_cold_meli(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """COLD-MELI: entity RIO (area [[Meli]]) -> meli router + scoped prefs."""
    missing = require_files(ctx.vault, ["30-resources/applications/RIO.md"] + rules.ROUTER_PREFS["meli"] + [rules.ROUTERS["meli"]])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    problems = _base_assertions(s, evidence)
    ent = s.active_entity
    if not ent or ent.get("path") != "30-resources/applications/RIO.md":
        problems.append("entidad resuelta no es el fixture RIO.md: %s" % (ent,))
    else:
        fm = ctx.vault.frontmatter("30-resources/applications/RIO.md")
        evidence.append("fixture real 30-resources/applications/RIO.md: area=%s (frontmatter leido, sin escanear carpetas)" % fm.get("area"))
        if normalize_area(fm.get("area")) != "meli":
            problems.append("fixture RIO ya no declara area [[Meli]]: %s" % fm.get("area"))
    if s.active_domain != "meli":
        problems.append("gate no activo meli: %s (%s)" % (s.active_domain, s.gate_note))
    expected_pack = [rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"]
    if sorted(s.pack_files) != sorted(expected_pack):
        problems.append("pack meli != {router + 2 preferencias scoped}: %s" % s.pack_files)
    not_load = [rules.ROUTERS["aranea"], rules.ARANEA_MCPS_EXPERT,
                rules.ROUTER_PREFS["aranea"][0], "30-resources/aranea/00-index.md"] + MELI_ECHO_ACTIVE_NOTES
    problems += _assert_absent(not_load, s.all_opens(), evidence)
    opens = s.all_opens()
    if any(p.startswith("30-resources/agents/skills/") and p != rules.ROUTERS["meli"] for p in opens):
        problems.append("skill de dominio alcanzada sin router: %s" % [p for p in opens if p.startswith("30-resources/agents/skills/")])
    evidence.append("estado: active_entity=%s active_domain=%s pack=%s" % (
        ent.get("title") if ent else None, s.active_domain, s.pack_files))
    evidence.append("gate: %s" % s.gate_note)
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "cold start Meli: router meli-agent-dev + preferencias scoped (meli work + vpn routing)" if not problems
        else "cold start Meli violo el contrato (C10/C11)",
        evidence + problems)


def sc_cold_aranea(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """COLD-ARANEA: entity Echo Forge (area [[Echo]]) -> aranea router (mapeo
    Echo->Aranea explicito)."""
    missing = require_files(ctx.vault, ["10-projects/Echo Forge/Echo Forge.md", rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "Echo Forge"})
    problems = _base_assertions(s, evidence)
    ent = s.active_entity
    if not ent or ent.get("path") != "10-projects/Echo Forge/Echo Forge.md":
        problems.append("entidad resuelta no es el fixture Echo Forge.md: %s" % (ent,))
    else:
        fm = ctx.vault.frontmatter("10-projects/Echo Forge/Echo Forge.md")
        evidence.append("fixture real 10-projects/Echo Forge/Echo Forge.md: area=%s -> mapeo [[Echo]]->aranea-agent-dev verificado (distinto del [[Aranea]] directo)" % fm.get("area"))
    if s.active_domain != "aranea":
        problems.append("gate no activo aranea con area [[Echo]]: %s (%s)" % (s.active_domain, s.gate_note))
    expected_pack = [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"]
    if sorted(s.pack_files) != sorted(expected_pack):
        problems.append("pack aranea != {router + aranea ops prefs}: %s" % s.pack_files)
    not_load = [rules.ROUTERS["meli"], rules.ROUTER_PREFS["meli"][0],
                "30-resources/agents/skills/signals-code-review/SKILL.md",
                "30-resources/agents/skills/signals-func-spec-authoring/SKILL.md",
                "30-resources/agents/skills/fury-lib-consumer-deploy/SKILL.md",
                rules.FEDERATED_DOMAIN_INDEX] + [
        "80-agents/memory/public/known-error/rio/" + os.path.basename(FURY_NOTE)]
    problems += _assert_absent(not_load, s.all_opens(), evidence)
    evidence.append("estado: active_entity=%s active_domain=%s pack=%s" % (
        ent.get("title") if ent else None, s.active_domain, s.pack_files))
    state = "FAIL" if problems else "WARN"  # WARN declarado por diseno (Hallazgo 7)
    details = "cold start Aranea via area [[Echo]]: router aranea-agent-dev + aranea ops prefs" if not problems else "cold start Aranea violo el contrato (C10)"
    evidence += problems + [
        "WARN declarado (Hallazgo 7): rjara-vpn-routing-preferences.md tiene trigger when_area_loaded sin campo area y el router Aranea no la lista en su Minimal Read; su carga on-demand via el enlace del perfil no se afirma ni se prohíbe (C11)."]
    return state, details, evidence


def sc_cold_conflicting(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """COLD-CONFLICTING-EVIDENCE-FAILS-CLOSED: entity RIO + task/surface
    evidence aranea -> fail closed, no router (bootstrap paso 6)."""
    missing = require_files(ctx.vault, ["30-resources/applications/RIO.md"])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "RIO", "task_evidence": "aranea", "surface_evidence": "aranea"})
    problems = _base_assertions(s, evidence)
    if s.active_domain is not None:
        problems.append("gate eligio router ante evidencia conflictiva: %s (%s)" % (s.active_domain, s.gate_note))
    if s.pack_files:
        problems.append("pack cargado en fail-closed: %s" % s.pack_files)
    if not s.active_entity or s.active_entity.get("title") != "RIO":
        problems.append("entidad RIO debia quedar resuelta con conflicto declarado: %s" % s.active_entity)
    opens = s.all_opens()
    if any(p in opens for p in (rules.ROUTERS["meli"], rules.ROUTERS["aranea"], rules.ARANEA_MCPS_EXPERT)):
        problems.append("router/expert cargado ante conflicto (debe fallar cerrado)")
    evidence.append("entrada del gate: {entity_area=[[Meli]], surface=mcp__aranea-*, task_mentions=aranea} -> salida: %s" % s.gate_note)
    evidence.append("estado: active_entity=%s active_domain=%s (fail closed, sin router)" % (
        s.active_entity.get("title") if s.active_entity else None, s.active_domain))
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "evidencia conflictiva fallo cerrado: ningun router (bootstrap paso 6)" if not problems
        else "el gate no fallo cerrado ante evidencia conflictiva (C10)",
        evidence + problems)


def _warm_no_base_reopen(s: Session, turn: int, evidence: List[str]) -> List[str]:
    problems: List[str] = []
    base = [rules.CONSTITUTION, rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX, "80-agents/skills/agents-os-bootstrap/SKILL.md"] + ([s.profile_note] if s.profile_note else [])
    reopened = [p for p in s.opens_in_turn(turn) if p in base]
    if reopened:
        problems.append("relectura de base en turno warm (C06): %s" % reopened)
    evidence.append("turno %d: file-opens = %s (cero aperturas de base)" % (turn, s.opens_in_turn(turn) or "-"))
    return problems


def sc_warm_default(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """WARM-DEFAULT: segundo mensaje casual; reuse, delta-only."""
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"casual": True})
    s.turn = 2
    s.warm_turn({})
    problems = _warm_no_base_reopen(s, 2, evidence)
    if any(rules.ROUTERS[d] in s.opens_in_turn(2) for d in ("meli", "aranea")):
        problems.append("router cargado en turno warm casual")
    if s.session_mode != "warm" or s.bootstrap_runs != 1:
        problems.append("modo/ritual incorrecto: mode=%s runs=%d" % (s.session_mode, s.bootstrap_runs))
    evidence.append("estado: session_mode=%s active_entity=%s active_domain=%s (sin output ritual, bootstrap Output)" % (
        s.session_mode, s.active_entity, s.active_domain))
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "turno warm sin dominio: cero relecturas, delta vacio para turno casual" if not problems
        else "turno warm re-leo base (C06)",
        evidence + problems)


def sc_warm_meli(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """WARM-MELI: mismo dominio; delta = known-error RIO; sin releer base ni
    recargar preferencias."""
    missing = require_files(ctx.vault, [FURY_NOTE, "30-resources/applications/RIO.md"])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    pack_t1 = list(s.pack_files)
    s.turn = 2
    s.warm_turn({})
    candidates = s.retrieve("error")
    problems = _warm_no_base_reopen(s, 2, evidence)
    if FURY_NOTE not in candidates:
        problems.append("el known-error del fury segment suffix no fue seleccionado por el filtro de retrieval: %s" % candidates)
    miss = s.open_delta(FURY_NOTE)  # cuerpo del delta declarado por el turno
    if miss:
        problems.append("delta declarado inexistente en disco: %s" % miss)
    if any(p in candidates or p in s.opens_in_turn(2) for p in pack_t1):
        problems.append("recarga del pack de dominio en turno que pide un hecho (C06/C11)")
    if any(p in candidates or p in s.opens_in_turn(2) for p in (rules.ROUTERS["aranea"], rules.ROUTER_PREFS["aranea"][0])):
        problems.append("pieza Aranea en turno Meli")
    evidence.append("candidatos del filtro (%d): %s" % (len(candidates), ", ".join(candidates) or "-"))
    evidence.append("cuerpo abierto (delta unico del turno): %s" % FURY_NOTE)
    evidence.append("estado: session_mode=%s active_entity=%s active_domain=%s sin cambio" % (
        s.session_mode, s.active_entity.get("title"), s.active_domain))
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "turno warm Meli: delta = known-error RIO (when_error_matches); base y pack intactos" if not problems
        else "turno warm Meli violo el contrato (C06/C11)",
        evidence + problems)


def sc_warm_aranea(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """WARM-ARANEA: mismo dominio; delta = continuidad interna Echo Forge."""
    missing = require_files(ctx.vault, [MT5_NOTE, "10-projects/Echo Forge/Echo Forge.md"])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "Echo Forge"})
    s.turn = 2
    s.warm_turn({})
    candidates = s.retrieve("continuity")
    problems = _warm_no_base_reopen(s, 2, evidence)
    if MT5_NOTE not in candidates:
        problems.append("la continuidad activa del MT5 parser cert no fue seleccionada por el filtro: %s" % candidates)
    miss = s.open_delta(MT5_NOTE)  # cuerpo del delta declarado por el turno
    if miss:
        problems.append("delta declarado inexistente en disco: %s" % miss)
    for p in candidates:
        fm_p = ctx.vault.frontmatter(p)
        if rules.domain_from_area(fm_p.get("area")) == "meli":
            problems.append("memoria del dominio Meli en turno Aranea: %s" % p)
    if any(p in candidates or p in s.opens_in_turn(2) for p in (rules.ROUTERS["meli"], rules.ROUTER_PREFS["meli"][0])):
        problems.append("pieza Meli en turno Aranea")
    evidence.append("candidatos del filtro (%d): %s" % (len(candidates), ", ".join(candidates) or "-"))
    evidence.append("cuerpo abierto (delta unico del turno): %s" % MT5_NOTE)
    evidence.append("trigger del fixture: %s (vocabulario no canonico = WARN de LOAD-POLICY-VOCABULARY, no invalida este escenario)" % _load_policy_note(ctx.vault.frontmatter(MT5_NOTE)))
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "turno warm Aranea: delta = continuidad activa Echo Forge; base intacta" if not problems
        else "turno warm Aranea violo el contrato (C06)",
        evidence + problems)


def sc_bootstrap_not_rerun(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """BOOTSTRAP-NOT-RERUN-ON-WARM: N>=3 turnos consecutivos sin releer base
    ni re-invocar bootstrap (warm paso 4, AGENTS.md, C01/C06)."""
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"casual": True})
    base = [rules.CONSTITUTION, rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX,
            "80-agents/skills/agents-os-bootstrap/SKILL.md"] + ([s.profile_note] if s.profile_note else [])
    problems: List[str] = []
    for t in range(2, 6):  # turnos 2..5 (N=4 >= 3)
        s.turn = t
        s.warm_turn({})
        reopened = [p for p in s.opens_in_turn(t) if p in base]
        if reopened:
            problems.append("turno %d re-abrio base/bootstrap sin invalidacion declarada: %s" % (t, reopened))
    if s.bootstrap_runs != 1:
        problems.append("bootstrap re-ejecutado en turnos 2..N: %d runs" % s.bootstrap_runs)
    evidence.append("turnos 2..5 sin aperturas de base/bootstrap: %s" % (["[]" if not s.opens_in_turn(t) else s.opens_in_turn(t) for t in range(2, 6)]))
    evidence.append("bootstrap_runs=%d; session_mode estable=%s" % (s.bootstrap_runs, s.session_mode))
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "4 turnos warm consecutivos sin releer base ni re-invocar bootstrap" if not problems
        else "bootstrap re-emitido o base re-leida en turnos warm (C01/C06)",
        evidence + problems)


def sc_switch_meli_to_aranea(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """SWITCH-MELI-TO-ARANEA: swap explicito, un solo pack, base sin relectura."""
    missing = require_files(ctx.vault, ["30-resources/applications/RIO.md", "10-projects/Echo Forge/Echo Forge.md", rules.ROUTERS["aranea"]])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    pack_meli = list(s.pack_files)
    base_before = set(s.opens_in_turn(1))
    s.turn = 2
    s.swap_entity("Echo Forge")
    problems: List[str] = []
    reopened_base = [p for p in s.opens_in_turn(2) if p in base_before]
    if reopened_base:
        problems.append("swap re-leo archivos base (deben persistir sin relectura): %s" % reopened_base)
    if rules.GLOBAL_INTERNAL in s.opens_in_turn(2):
        problems.append("nota interna global re-cargada en swap (Session Modes: skip global internal reload)")
    old_pack_used = [p for p in pack_meli if p in s.opens_in_turn(2)]
    if old_pack_used:
        problems.append("piezas del pack anterior (meli) usadas o re-abiertas en el turno del swap (swap paso 4: el pack anterior sale del razonamiento activo): %s" % old_pack_used)
    if s.holds_two_packs():
        problems.append("dos packs de dominio activos tras el swap (Hard Rule)")
    if s.active_domain != "aranea":
        problems.append("dominio post-swap != aranea: %s (%s)" % (s.active_domain, s.gate_note))
    if sorted(s.pack_files) != sorted([rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"]):
        problems.append("pack post-swap != pack aranea: %s" % s.pack_files)
    if any(p in s.pack_files for p in pack_meli):
        problems.append("pack Meli persiste tras el swap (swap paso 3: drop router + scoped preferences): %s" % [p for p in pack_meli if p in s.pack_files])
    if s.active_entity is None or s.active_entity.get("title") != "Echo Forge":
        problems.append("active_entity post-swap != Echo Forge: %s" % s.active_entity)
    evidence.append("antes: domain=%s pack=%s" % ("meli", pack_meli))
    evidence.append("despues: domain=%s pack=%s entity=%s" % (s.active_domain, s.pack_files, s.active_entity.get("title") if s.active_entity else None))
    evidence.append(s.swap_note or "")
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "swap Meli->Aranea: pack reemplazado explicitamente, un solo pack, base persistente" if not problems
        else "swap Meli->Aranea violo el contrato (C07)",
        evidence + problems)


def sc_switch_aranea_to_meli(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """SWITCH-ARANEA-TO-MELI: swap, router Meli + prefs, skill especializada
    solo por la tabla del router (C12), una sola."""
    missing = require_files(ctx.vault, ["30-resources/applications/RIO.md", "10-projects/Echo Forge/Echo Forge.md",
                                        rules.ROUTERS["meli"], "30-resources/agents/skills/signals-code-review/SKILL.md"])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "Echo Forge"})
    pack_aranea = list(s.pack_files)
    base_before = set(s.opens_in_turn(1))
    s.turn = 2
    s.swap_entity("RIO")
    spec = s.route_specialist("meli", "code_review")
    problems: List[str] = []
    reopened_base = [p for p in s.opens_in_turn(2) if p in base_before]
    if reopened_base:
        problems.append("swap re-leo archivos base: %s" % reopened_base)
    if s.holds_two_packs():
        problems.append("dos packs activos tras el swap")
    if s.active_domain != "meli":
        problems.append("dominio post-swap != meli: %s" % s.active_domain)
    if sorted(s.pack_files) != sorted([rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"]):
        problems.append("pack post-swap != {meli router + meli prefs + vpn prefs}: %s" % s.pack_files)
    if rules.ROUTERS["aranea"] in s.pack_files or rules.ROUTER_PREFS["aranea"][0] in s.pack_files:
        problems.append("pack Aranea persiste tras el swap")
    old_pack_used = [p for p in pack_aranea if p in s.opens_in_turn(2)]
    if old_pack_used:
        problems.append("piezas del pack anterior (aranea) usadas o re-abiertas en el turno del swap (swap paso 4: el pack anterior sale del razonamiento activo): %s" % old_pack_used)
    if rules.ARANEA_MCPS_EXPERT in s.all_opens():
        problems.append("aranea-mcps-expert activado en turno meli (MUST NOT, C13)")
    opens = s.all_opens()
    if spec:
        if opens.index(rules.ROUTERS["meli"]) > opens.index(spec):
            problems.append("skill especializada cargada antes que el router (debe rutear via tabla del router, C12)")
        if len(s.specialist_skills) != 1:
            problems.append("mas de una skill especializada: %s" % s.specialist_skills)
        evidence.append("routing: %s via tabla del router meli-agent-dev (Procedure 3), no directo desde INDEX" % spec)
    else:
        problems.append("signals-code-review no rut-eada por la tabla del router para code review")
    if rules.SKILLS_INDEX in s.opens_in_turn(2):
        problems.append("INDEX.md re-cargado en el swap (registry ya en contexto)")
    evidence.append("despues: domain=%s pack=%s especialista=%s" % (s.active_domain, s.pack_files, s.specialist_skills))
    evidence.append("VPN por rjara-vpn-routing-preferences.md antes del primer acceso corporativo (router Procedure 4): incluida en pack")
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "swap Aranea->Meli: router + preferencias, signals-code-review solo via tabla del router" if not problems
        else "swap Aranea->Meli violo el contrato (C07/C12)",
        evidence + problems)


def _switch_from_default(ctx: Ctx, title: str, expected_domain: str, pack: List[str]) -> Tuple[str, str, List[str]]:
    missing = require_files(ctx.vault, pack)
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"casual": True})
    base_before = set(s.opens_in_turn(1))
    s.turn = 2
    s.swap_entity(title)
    problems: List[str] = []
    reopened_base = [p for p in s.opens_in_turn(2) if p in base_before]
    if reopened_base:
        problems.append("resolucion tardia re-leo la base (warm paso 3 / AGENTS.md): %s" % reopened_base)
    if s.bootstrap_runs != 1:
        problems.append("bootstrap re-ejecutado al resolver la entidad")
    if s.active_domain != expected_domain:
        problems.append("dominio != %s: %s (%s)" % (expected_domain, s.active_domain, s.gate_note))
    if sorted(s.pack_files) != sorted(pack):
        problems.append("pack != esperado: %s" % s.pack_files)
    other = "aranea" if expected_domain == "meli" else "meli"
    if rules.ROUTERS[other] in s.pack_files or rules.ROUTERS[other] in s.all_opens():
        problems.append("pack del dominio ajeno (%s) cargado" % other)
    evidence.append("transicion: active_entity none->%s; active_domain none->%s" % (title, s.active_domain))
    evidence.append("gate: %s" % s.gate_note)
    state = "FAIL" if problems else "WARN"  # WARN de clasificacion de modo, por diseno
    warn = ("WARN declarado (C02/C07 unknown): con entidad previa=none, la definicion de cold ('no entity loaded yet') y la de swap "
            "('switches to a different entity') convergen en el mismo observable; ninguna autoridad fija la clasificacion del modo.")
    details = "resolucion tardia %s: gate aplicado, base intacta, sin re-ejecutar bootstrap" % title if not problems else "resolucion tardia desde DEFAULT violo el contrato"
    return state, details, evidence + problems + [warn]


def sc_switch_default_to_meli(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """SWITCH-DEFAULT-TO-MELI."""
    return _switch_from_default(ctx, "RIO", "meli", [rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"])


def sc_switch_default_to_aranea(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """SWITCH-DEFAULT-TO-ARANEA (mapeo [[Echo]] verificado explicitamente)."""
    state, details, ev = _switch_from_default(
        ctx, "Echo Forge", "aranea", [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"])
    ev = list(ev)
    if state != "SKIP":
        ev.append("mapeo [[Echo]]->aranea-agent-dev verificado explicitamente (bootstrap paso 6)")
    return state, details, ev


def sc_meli_negative_aranea_tool(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """MELI-NEGATIVE-ARANEA-TOOL: decision de frontera con dominio meli activo
    (C13). La presencia de las tools en superficie no es violacion."""
    missing = require_files(ctx.vault, ["30-resources/applications/RIO.md", rules.ROUTERS["meli"]])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    decision, reason = s.aranea_tool_decision("estado-de-sistema")
    problems: List[str] = []
    if decision != "no-invoke":
        problems.append("decision de frontera incorrecta: %s (%s)" % (decision, reason))
    if rules.ARANEA_MCPS_EXPERT in s.all_opens():
        problems.append("aranea-mcps-expert activado en dominio meli (MUST NOT: aranea-mcps-expert Purpose)")
    if rules.ROUTERS["aranea"] in s.all_opens():
        problems.append("router aranea activo en dominio meli")
    evidence.append("replica determinista: {domain=meli, surface_tools=mcp__aranea-*} -> decision='%s' (%s)" % (decision, reason))
    evidence.append("PRESENCIA de las tools en la superficie NO es violacion: el aislamiento es instruccional, no mecanico (Hallazgo 4 y gaps de enforcement)")
    if ctx.machine_surface:
        evidence.append("estado observado de configs (nombres only): %s" % ", ".join(
            "%s aranea=%d meli=%d" % (c["surface"], c["aranea"], c["meli"]) for c in ctx.machine_surface))
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "en dominio meli las capabilities mcp__aranea-* no se invocan aunque esten expuestas" if not problems
        else "frontera de tools violada en dominio meli (C13)",
        evidence + problems)


def sc_aranea_negative_meli_tool(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """ARANEA-NEGATIVE-MELI-TOOL: desde aranea, tarea meli sin identidad
    demostrable -> rechazo, sin skills Meli, sin Zord (defensa en profundidad:
    gate -> router Procedure 1 -> gate propio de signals-code-review)."""
    missing = require_files(ctx.vault, ["10-projects/Echo Forge/Echo Forge.md", rules.ROUTERS["aranea"]])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "Echo Forge"})
    decision, reason = s.aranea_tool_decision("meli")
    problems: List[str] = []
    if decision != "reject":
        problems.append("la cadena no rechazo la tarea meli sin identidad: %s (%s)" % (decision, reason))
    opens = s.all_opens()
    for skill in ("signals-code-review", "signals-func-spec-authoring", "signals-tech-spec-authoring", "fury-lib-consumer-deploy"):
        rel = "30-resources/agents/skills/%s/SKILL.md" % skill
        if rel in opens:
            problems.append("skill Meli domain-gated alcanzada sin router ni identidad (never directly, C12): %s" % rel)
    if rules.ROUTERS["meli"] in opens:
        problems.append("meli-agent-dev cargado sin identidad demostrable")
    if s.active_domain != "aranea":
        problems.append("dominio cambio indebidamente: %s" % s.active_domain)
    evidence.append("cadena replicada: gate (domain-gated never directly) -> aranea-agent-dev Procedure 1 (rechazo y deriva a meli-agent-dev antes de leer documentacion o abrir conexiones) -> gate propio de signals-code-review ('Fuera de Meli termina como NOT_APPLICABLE antes de invocar Zord', Hallazgo 2)")
    evidence.append("resultado: %s (%s); tarea rechazada/derivada con motivo declarado; zord/fury no existen como MCP ni estan instalados (Hallazgo 5)" % (decision, reason))
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "tarea meli sin identidad demostrable: rechazada sin fuentes ni tools corporativas" if not problems
        else "defensa en profundidad violada desde aranea (C12/C13)",
        evidence + problems)


def sc_deprecated_doc_not_default_load(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """DEPRECATED-DOC-NOT-DEFAULT-LOAD: la continuidad superseded no entra al
    startup ni al retrieval normal aunque comparta continuity_key (C14)."""
    missing = require_files(ctx.vault, [rules.GLOBAL_INTERNAL, rules.CONTINUITY_ARCHIVE])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    # STATIC previo: cuadruple de retiro del archive + misma key que la activa.
    fm_a = ctx.vault.frontmatter(rules.CONTINUITY_ARCHIVE)
    fm_v = ctx.vault.frontmatter(rules.GLOBAL_INTERNAL)
    quad = (str(fm_a.get("memory_state", "")) == "superseded"
            and str(fm_a.get("load_policy", "")).strip().strip("\"'") == "manual"
            and str(fm_a.get("index_priority", "")).strip().strip("\"'") == "low"
            and bool(fm_a.get("superseded_by")))
    if not quad:
        return "FAIL", "fixture archive sin el cuadruple de retiro completo (C14)", [
            "memory_state=%s load_policy=%s index_priority=%s superseded_by=%s" % (
                fm_a.get("memory_state"), fm_a.get("load_policy"), fm_a.get("index_priority"), fm_a.get("superseded_by"))]
    same_key = str(fm_a.get("continuity_key", "")).strip() == str(fm_v.get("continuity_key", "")).strip()
    evidence.append("STATIC: archive declara memory_state=superseded, load_policy=manual, index_priority=low, superseded_by -> cuadruple completo; misma continuity_key que la activa: %s" % same_key)
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"casual": True})
    delta = s.retrieve("context")  # sin pedido historico: solo candidatos del filtro
    problems: List[str] = []
    if rules.CONTINUITY_ARCHIVE in s.all_opens() or rules.CONTINUITY_ARCHIVE in delta:
        problems.append("la nota superseded entero al stack o al retrieval normal (Hard Rule bootstrap / context-retrieval paso 5)")
    if rules.GLOBAL_INTERNAL not in s.all_opens():
        problems.append("la nota interna global activa no cargo por su ruta canonica")
    superseded_hits = [p for p in delta if "/global/" in p and p.endswith("archive.md")]
    if superseded_hits:
        problems.append("retrieval normal devolvio notas superseded: %s" % superseded_hits)
    active_count = sum(1 for p in s.all_opens() if p == rules.GLOBAL_INTERNAL)
    if active_count != 1:
        problems.append("el stack debe contener exactamente UNA nota interna global: %d" % active_count)
    evidence.append("SIMULATED: candidatos del filtro retrieval normal (sin historico): %d; archive ausente" % len(delta))
    evidence.append("stack: exactamente una nota interna global (%s)" % rules.GLOBAL_INTERNAL)
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "la continuidad superseded queda fuera de startup y retrieval normal (mismo continuity_key)" if not problems
        else "memoria superseded entro al startup o retrieval (C14)",
        evidence + problems)


def sc_unrelated_domain_not_loaded(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """UNRELATED-DOMAIN-NOT-LOADED: retrieval en dominio meli (RIO) no trae
    memoria ni preferencias del dominio ajeno (C11; filtro por entidad
    resuelta, comparacion contra el area de la entidad activa)."""
    missing = require_files(ctx.vault, ["30-resources/applications/RIO.md", FURY_NOTE, PLAYMAKER_NOTE])
    if missing:
        return "SKIP", "fixtures no disponibles en el vault actual", ["faltantes: %s" % missing]
    evidence: List[str] = []
    s = Session(ctx.vault)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    delta = s.retrieve("context")  # candidatos del filtro por entidad/area activa
    problems: List[str] = []
    if FURY_NOTE not in delta:
        problems.append("known-error RIO (when_error_matches) no seleccionado: %s" % FURY_NOTE)
    if PLAYMAKER_NOTE not in delta:
        problems.append("decision RIO (when_application_loaded, application [[rio-playmaker]]) no seleccionada: %s" % PLAYMAKER_NOTE)
    foreign_markers = ("symphony", "aranea", "echo", "hermes", "sqx")
    for p in delta:
        if any(m in p for m in foreign_markers):
            problems.append("pieza del dominio ajeno en turno meli: %s" % p)
        fm = ctx.vault.frontmatter(p)
        n_area = normalize_area(fm.get("area"))
        if n_area and n_area != "meli":
            problems.append("candidato con area != [[Meli]] seleccionado en turno meli: %s (%s)" % (p, fm.get("area")))
    if rules.ROUTER_PREFS["aranea"][0] in delta or rules.ROUTER_PREFS["aranea"][0] in s.all_opens():
        problems.append("preferencia aranea seleccionada/cargada en dominio meli")
    if rules.FEDERATED_DOMAIN_INDEX in s.all_opens():
        problems.append("indice federado aranea abierto en dominio meli")
    if any(p in s.all_opens() for p in MELI_ECHO_ACTIVE_NOTES):
        problems.append("memoria interna Echo/Echo Forge activa en turno meli")
    meli_internal_active = [p for p in delta if p.startswith("80-agents/memory/internal/")]
    evidence.append("candidatos del filtro (%d, todos area [[Meli]] o referenciando RIO): %s" % (len(delta), ", ".join(sorted(delta))[:400] or "-"))
    evidence.append("continuidad interna meli activa: %s (Hallazgo 10: toda la continuidad Meli esta archived/manual — estado observado, no invariante)" % (meli_internal_active or "ninguna hoy"))
    evidence.append("semantica: las preferencias Meli y Aranea son scoped (perfil); el router ya cargo las de meli en cold start; retrieval no trae prefs")
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "retrieval meli: solo memoria del dominio/entidad activa; cero piezas Echo/Aranea" if not problems
        else "retrieval trajo memoria del dominio ajeno (C11)",
        evidence + problems)


# ---------------------------------------------------------------------------
# L2 — LIVE-EXPOSURE SMOKE (automated part)
# ---------------------------------------------------------------------------
MELI_SERVER_MARKERS = ("zord", "fury", "spellbook", "melisource")


def read_surface_configs() -> List[Dict[str, Any]]:
    """Parse machine surface MCP configs (names + enabled only; never URLs,
    headers or credentials). Returns [] when none exist."""
    home = os.path.expanduser("~")
    out: List[Dict[str, Any]] = []

    def summarize(surface: str, path: str, servers: Optional[Dict[str, bool]], error: Optional[str] = None) -> Dict[str, Any]:
        if servers is None:
            return {"surface": surface, "path": path, "servers": None, "error": error or "ilegible",
                    "aranea": 0, "meli": 0}
        aranea = [n for n in servers if "aranea" in n.lower() and servers[n]]
        meli = [n for n in servers if any(m in n.lower() for m in MELI_SERVER_MARKERS)]
        return {"surface": surface, "path": path, "servers": servers,
                "aranea": len(aranea), "meli": len(meli)}

    zc = os.path.join(home, ".zcode/cli/config.json")
    if os.path.isfile(zc):
        try:
            cfg = json.loads(read_text(zc))
            servers = cfg.get("mcp", {}).get("servers", {})
            out.append(summarize("zcode", "~/.zcode/cli/config.json",
                                 {name: bool(srv.get("enabled", True)) for name, srv in servers.items()}))
        except (ValueError, AttributeError):
            out.append(summarize("zcode", "~/.zcode/cli/config.json", None, "json invalido"))
    cu = os.path.join(home, ".cursor/mcp.json")
    if os.path.isfile(cu):
        try:
            cfg = json.loads(read_text(cu))
            out.append(summarize("cursor", "~/.cursor/mcp.json", {name: True for name in cfg.get("mcpServers", {})}))
        except (ValueError, AttributeError):
            out.append(summarize("cursor", "~/.cursor/mcp.json", None, "json invalido"))
    cx = os.path.join(home, ".codex/config.toml")
    if os.path.isfile(cx):
        servers: Dict[str, bool] = {}
        for line in read_text(cx).splitlines():
            m = re.match(r"^\s*\[mcp_servers\.([A-Za-z0-9_.-]+)\]\s*$", line)
            if m:
                servers[m.group(1)] = True
        out.append(summarize("codex", "~/.codex/config.toml", servers))
    return out


def sc_session_surface_exposure(ctx: Ctx) -> Tuple[str, str, List[str]]:
    """SESSION-SURFACE-EXPOSURE (parte automatizada): assert aranea-* presente
    y cero servers Meli (zord/fury/spellbook/melisource) en cada config de
    superficie presente. La sonda manual de auto-reporte queda SKIP por
    defecto (documentada en README). Spec section 3."""
    if ctx.no_live:
        return "SKIP", "--no-live: parte de configs de maquina omitida", []
    if not ctx.machine_surface:
        return "SKIP", "ninguna config de superficie presente (~/.zcode/cli/config.json, ~/.cursor/mcp.json, ~/.codex/config.toml)", []
    evidence: List[str] = []
    problems: List[str] = []
    for cfg in ctx.machine_surface:
        servers = cfg.get("servers")
        if servers is None:
            problems.append("%s: config ilegible (%s)" % (cfg["surface"], cfg.get("error")))
            continue
        names = sorted(servers)
        aranea = [n for n in names if "aranea" in n.lower()]
        meli = [n for n in names if any(m in n.lower() for m in MELI_SERVER_MARKERS)]
        enabled_aranea = [n for n in aranea if servers[n]]
        evidence.append("%s (%s): servers=%s" % (cfg["surface"], cfg["path"], names))
        if not aranea:
            problems.append("%s: sin servers aranea-* configurados (contradice el estado de la maquina del owner; Hallazgo 4)" % cfg["surface"])
        elif not enabled_aranea:
            problems.append("%s: servers aranea-* presentes pero ninguno habilitado" % cfg["surface"])
        if meli:
            problems.append("%s: servers Meli configurados (deben ser cero): %s" % (cfg["surface"], meli))
    evidence.append("assert por config: aranea-* presente y habilitado; cero servers Meli (zord/fury/spellbook/melisource)")
    evidence.append("SKIP permanente: sonda manual de auto-reporte de sesion real (documentada en README; el orchestrator la ejecuta y registra a mano; el router auto-declarado queda como dato WARN, Hallazgo 6)")
    return (state_worst(["PASS"] if not problems else ["FAIL"]), 
        "superficie observada: aranea-* configurados y cero servers Meli en todas las configs presentes" if not problems
        else "superficie de exposicion desviada del estado declarado",
        evidence + problems)


# ---------------------------------------------------------------------------
# Context baseline (spec section 9; C04: baseline-only, chars/4, sin optimizar)
# ---------------------------------------------------------------------------
def _size(vault: Vault, rel: str) -> Optional[Dict[str, int]]:
    text = vault.read(rel)
    if text is None:
        return None
    raw = os.path.getsize(vault.abspath(rel))
    return {"bytes": raw, "chars": len(text), "approx_tokens_chars_over_4": len(text) // 4}


def context_baseline(ctx: Ctx) -> Dict[str, Any]:
    note = ("baseline-only: tokens aproximados = chars/4 (metrica declarada sin "
            "autoridad de tokenizador, C04); sin optimizacion ni gates (spec section 9)")
    out: Dict[str, Any] = {"label": "context_baseline", "note": note, "always_load": {}, "scope_packs": {}}
    profile = ctx.vault.resolve_profile_note()
    always = [rules.CONSTITUTION, profile or "", rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX]
    for rel in always:
        if not rel:
            out["always_load"]["user-preference/ (perfil no resuelto)"] = None
            continue
        out["always_load"][rel] = _size(ctx.vault, rel)
    total = sum((v or {}).get("approx_tokens_chars_over_4", 0) for v in out["always_load"].values() if v)
    out["always_load_total_approx_tokens"] = total
    for domain, files in (("meli", [rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"]),
                          ("aranea", [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"])):
        pack = {rel: _size(ctx.vault, rel) for rel in files}
        ptot = sum((v or {}).get("approx_tokens_chars_over_4", 0) for v in pack.values() if v)
        out["scope_packs"][domain] = {"files": pack, "total_approx_tokens": ptot}
    return out


# ---------------------------------------------------------------------------
# Registry, runner, output
# ---------------------------------------------------------------------------
SCENARIOS: List[Tuple[str, str, Any]] = [
    # L0 (orden de ejecucion sugerido, conformance-scenarios.md)
    ("SCHEMA-VALIDATOR-GREEN", "L0", sc_schema_validator_green),
    ("STARTUP-DUPLICATION", "L0", sc_startup_duplication),
    ("CLOSED-CLUB-ALWAYS", "L0", sc_closed_club_always),
    ("LOAD-POLICY-VOCABULARY", "L0", sc_load_policy_vocabulary),
    ("REGISTRY-DISK-PARITY", "L0", sc_registry_disk_parity),
    ("DUAL-REGISTRY-DOMAIN-SYNC", "L0", sc_dual_registry_domain_sync),
    ("NO-SECRETS-IN-MARKDOWN", "L0", sc_no_secrets_in_markdown),
    ("ACTIVE-MEMORY-DOMAIN-PURITY", "L0", sc_active_memory_domain_purity),
    # L1
    ("COLD-DEFAULT", "L1", sc_cold_default),
    ("COLD-MELI", "L1", sc_cold_meli),
    ("COLD-ARANEA", "L1", sc_cold_aranea),
    ("COLD-CONFLICTING-EVIDENCE-FAILS-CLOSED", "L1", sc_cold_conflicting),
    ("WARM-DEFAULT", "L1", sc_warm_default),
    ("WARM-MELI", "L1", sc_warm_meli),
    ("WARM-ARANEA", "L1", sc_warm_aranea),
    ("BOOTSTRAP-NOT-RERUN-ON-WARM", "L1", sc_bootstrap_not_rerun),
    ("SWITCH-MELI-TO-ARANEA", "L1", sc_switch_meli_to_aranea),
    ("SWITCH-ARANEA-TO-MELI", "L1", sc_switch_aranea_to_meli),
    ("SWITCH-DEFAULT-TO-MELI", "L1", sc_switch_default_to_meli),
    ("SWITCH-DEFAULT-TO-ARANEA", "L1", sc_switch_default_to_aranea),
    ("MELI-NEGATIVE-ARANEA-TOOL", "L1", sc_meli_negative_aranea_tool),
    ("ARANEA-NEGATIVE-MELI-TOOL", "L1", sc_aranea_negative_meli_tool),
    ("DEPRECATED-DOC-NOT-DEFAULT-LOAD", "L1", sc_deprecated_doc_not_default_load),
    ("UNRELATED-DOMAIN-NOT-LOADED", "L1", sc_unrelated_domain_not_loaded),
    # L2
    ("SESSION-SURFACE-EXPOSURE", "L2", sc_session_surface_exposure),
]


def detect_vault_root() -> Optional[str]:
    """Default vault root: walk up from this script's directory until the
    folder contains 80-agents/agents-os/agents-os.md (spec section 8)."""
    d = HERE
    while True:
        if os.path.isfile(os.path.join(d, MARKER)):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def git_head(root: str) -> Optional[str]:
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            return proc.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


def run(args: argparse.Namespace) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    root = args.vault_root or detect_vault_root()
    if root is None:
        print("ERROR: no se pudo autodetectar VAULT_ROOT (carpeta que contiene %s). Usa --vault-root." % MARKER, file=sys.stderr)
        sys.exit(2)
    root = os.path.abspath(root)
    marker_ok = os.path.isfile(os.path.join(root, MARKER))
    ctx = Ctx(root, args.no_live)

    requested = SCENARIOS
    if args.layer:
        requested = [s for s in SCENARIOS if s[1] == args.layer]
    if args.scenario:
        if args.scenario == ANCHOR_CHECK_ID:
            requested = []  # run dirigido: solo el guard de fidelidad (pre-flight)
        else:
            requested = [s for s in SCENARIOS if s[0] == args.scenario]
            if not requested:
                print("ERROR: escenario desconocido: %s" % args.scenario, file=sys.stderr)
                sys.exit(2)
    need_gate = any(s[1] != "L0" for s in requested) and args.scenario is None
    # Nota: un run --scenario <ID> es un run dirigido por el operador (spec
    # section 8) y no aplica el corte por FAIL-L0; los runs full y --layer
    # siempre aplican el gate de la spec section 3.

    results: List[Dict[str, Any]] = []
    if not marker_ok:
        results.append({"id": ANCHOR_CHECK_ID, "level": "L0", "state": "SKIP",
                        "details": "marker %s ausente bajo la raiz indicada: las reglas de AGENTS OS no aplican (AGENTS.md / spec section 6)" % MARKER,
                        "evidence": []})
        for sid, level, _fn in requested:
            results.append({"id": sid, "level": level, "state": "SKIP",
                            "details": "marker %s ausente bajo la raiz indicada: las reglas de AGENTS OS no aplican (AGENTS.md / spec section 6)" % MARKER,
                            "evidence": []})
    else:
        # Pre-flight RULES-FIDELITY-ANCHORS: corre en TODA capa antes de los
        # escenarios (adversarial-verification D2). Si falla, la transcripcion
        # de rules.py quedo obsoleta respecto del texto vigente de las
        # autoridades y los resultados de los escenarios dependientes del gate
        # no son interpretables: el FAIL entra al gate L0 (corta L1/L2 en runs
        # full/--layer; los runs --scenario son dirigidos por el operador).
        gate_failed: List[str] = []
        try:
            a_state, a_details, a_evidence = sc_rules_fidelity_anchors(ctx)
        except Exception as exc:  # pragma: no cover — defensive; the check itself fails closed
            a_state, a_details, a_evidence = "SKIP", "no ejecutable: %s: %s" % (type(exc).__name__, exc), []
        results.append({"id": ANCHOR_CHECK_ID, "level": "L0", "state": a_state,
                        "details": a_details, "evidence": a_evidence})
        if a_state == "FAIL":
            gate_failed.append(ANCHOR_CHECK_ID)
        # L0 gate: si se piden escenarios L1/L2, L0 corre completo primero
        # (spec section 3: cualquier FAIL en L0 detiene L1/L2).
        l0_all = [s for s in SCENARIOS if s[1] == "L0"]
        l0_requested = [s for s in requested if s[1] == "L0"]
        run_l0 = l0_all if need_gate else l0_requested
        done_ids = set()
        for sid, level, fn in run_l0:
            try:
                state, details, evidence = fn(ctx)
            except Exception as exc:  # D3: fixture L0 ausente u otro error inesperado -> SKIP con motivo (spec section 5), nunca traceback ni UNKNOWN->PASS
                state, details, evidence = "SKIP", "no ejecutable: %s: %s" % (type(exc).__name__, exc), []
            results.append({"id": sid, "level": level, "state": state, "details": details, "evidence": evidence})
            done_ids.add(sid)
            if state == "FAIL":
                gate_failed.append(sid)
        blocked = bool(gate_failed) and need_gate
        for sid, level, fn in requested:
            if sid in done_ids:
                continue
            if blocked:
                results.append({"id": sid, "level": level, "state": "SKIP",
                                "details": "gate L0: FAIL en %s; los resultados L1/L2 no serian interpretables sobre un corpus no conformante (spec section 3)" % ", ".join(gate_failed),
                                "evidence": []})
                continue
            try:
                state, details, evidence = fn(ctx)
            except Exception as exc:  # scenario bug or unreadable fixture: honest SKIP
                state, details, evidence = "SKIP", "no ejecutable: %s: %s" % (type(exc).__name__, exc), []
            results.append({"id": sid, "level": level, "state": state, "details": details, "evidence": evidence})

    counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "SKIP": 0}
    for r in results:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    baseline = {
        "context_baseline": context_baseline(ctx) if marker_ok else {"note": "no capturado: marker ausente"},
        "git_head": git_head(root),
        "label": "baseline-only (spec sections 1 y 9); sin optimizacion ni gates",
    }
    levels = {lvl: [s[0] for s in SCENARIOS if s[1] == lvl] for lvl in ("L0", "L1", "L2")}
    levels["L0"] = [ANCHOR_CHECK_ID] + levels["L0"]
    doc = {
        "run": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "python": sys.version.split()[0],
            "vault_root_arg": args.vault_root or "auto",
            "layer_arg": args.layer or "all",
            "scenario_arg": args.scenario or None,
            "no_live": bool(args.no_live),
        },
        "baseline": baseline["git_head"],
        "levels": levels,        "scenarios": results,
        "counts": counts,
        "context_baseline": baseline["context_baseline"],
    }
    return results, doc


def human_summary(results: List[Dict[str, Any]], doc: Dict[str, Any], root: str) -> str:
    lines: List[str] = []
    lines.append("=" * 72)
    lines.append("AGENTS-OS CONFORMANCE")
    lines.append("=" * 72)
    run = doc["run"]
    lines.append("run %s · vault: %s · git %s · python %s" % (
        run["timestamp"], run["vault_root_arg"], (doc["baseline"] or "?")[:9], run["python"]))
    for r in results:
        lines.append("%s %s %s" % (r["id"].ljust(38, "."), r["level"].ljust(4), r["state"]))
    c = doc["counts"]
    lines.append("-" * 72)
    lines.append("counts: PASS %d · FAIL %d · WARN %d · SKIP %d" % (c["PASS"], c["FAIL"], c["WARN"], c["SKIP"]))
    cb = doc.get("context_baseline") or {}
    if "always_load_total_approx_tokens" in cb:
        packs = cb.get("scope_packs", {})
        lines.append("context baseline (baseline-only, chars/4): always-load ≈ %d tok · pack meli ≈ %s tok · pack aranea ≈ %s tok" % (
            cb["always_load_total_approx_tokens"],
            packs.get("meli", {}).get("total_approx_tokens", "?"),
            packs.get("aranea", {}).get("total_approx_tokens", "?")))
    for r in results:
        if r["state"] == "FAIL":
            lines.append("FAIL %s: %s" % (r["id"], r["details"]))
    lines.append("=" * 72)
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="agents_os_conformance.py",
        description="AGENTS OS Conformance Harness (Test Model V1). Read-only.")
    ap.add_argument("--layer", choices=["L0", "L1", "L2"], help="corre solo una capa")
    ap.add_argument("--scenario", help="corre un solo escenario por id")
    ap.add_argument("--json", action="store_true", help="salida machine-readable a stdout y results/run-<timestamp>.json")
    ap.add_argument("--vault-root", help="ruta del vault (default: autodeteccion por marker)")
    ap.add_argument("--no-live", action="store_true", help="omite la parte de configs de maquina de L2 (para correr fuera de la maquina del owner)")
    args = ap.parse_args(argv)

    results, doc = run(args)

    results_dir = os.path.join(HERE, "results")
    os.makedirs(results_dir, exist_ok=True)  # unica escritura permitida (spec section 7)
    ts = time.strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(results_dir, "run-%s.json" % ts)
    n = 1
    while os.path.exists(out_path):
        n += 1
        out_path = os.path.join(results_dir, "run-%s-%d.json" % (ts, n))
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)

    if args.json:
        json.dump(doc, sys.stdout, indent=2, ensure_ascii=False)
        print()
        print("[results] %s" % out_path, file=sys.stderr)
        print(human_summary(results, doc, doc["run"].get("vault_root_arg", "")), file=sys.stderr)
    else:
        print(human_summary(results, doc, doc["run"].get("vault_root_arg", "")))
        print("[results] %s" % out_path)

    return 1 if doc["counts"].get("FAIL", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
