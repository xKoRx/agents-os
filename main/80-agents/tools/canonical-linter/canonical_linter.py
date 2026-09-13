#!/usr/bin/env python3
"""AGENTS OS Canonical / Deprecation Linter (PHASE 3, P3-B).

Implementa la tool definida por dos documentos vinculantes (autoridad de esta
implementación):
- artifacts/p3-canonical-model.md      (P3-A: autoridades, hot path en 4 clases,
  checks CL-01..CL-20, desduplicación sección 6, recomendación sección 8)
- artifacts/p3-canonical-linter-spec.md (spec del parent: decisiones A1-A10,
  checks ratificados, semántica de veredictos, write scope, output schema)

El linter es un CONSUMIDOR del tooling existente (fork prohibido, precedente
context-budget P2):
- `iter_vault_md` / `fm_of` / `parse_frontmatter` / `_parse_index_tables` del
  Conformance Harness (`80-agents/tools/conformance-harness/`), importado
  resolviendo su ruta relativa a VAULT_ROOT en runtime (constitución regla 11).
- `load_contract()` de `validate_schema_contract.py`: ÚNICA fuente de enums,
  tipos y estados (jamás copiar listas de status/fields).
- Constantes de hot path desde `rules.py` (BASE_STACK_FILES, GLOBAL_INTERNAL,
  SKILLS_INDEX, ROUTERS, ROUTER_PREFS, DOMAIN_GATED_SKILLS).

Principios duros (spec sección 2 y modelo sección 4):
- Sólo MACHINE-DETERMINISTIC produce FAIL; HEURISTIC como máximo WARN;
  findings se REGISTRAN, nunca se auto-corrijen.
- Desduplicación por scope: no re-emitir lo ya cubierto por lint.py, doctor,
  harness L0 o context-budget M16/M14; los solapes se citan en `dedup_cites`.
- Corpus = `iter_vault_md` + exclusión explícita de fixtures sintéticas (A8).
- Read-only en todo el vault salvo `results/` propio. Python 3.9+ stdlib only.
  Determinista. Sin daemon, sin DB, sin red.

Clase unificada (A5 ratificado): no_vigente = memory_state ∈ {superseded,
archived} ∪ status ∈ {archived, superseded}; deprecated/deprecating = sub-clase
"en retiro". Algoritmo de resolución de wikilinks (A9 ratificado): path
relativo al origen > path VAULT_ROOT-relativo (regla 11 de la constitución) >
basename exacto > basename casefold único > alias declarado exacto; múltiples
candidatos → hallazgo WARN "ambiguo".
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

sys.dont_write_bytecode = True  # sin __pycache__ fuera del write scope

HERE = os.path.dirname(os.path.abspath(__file__))
MARKER = "80-agents/agents-os/agents-os.md"
HARNESS_REL = "80-agents/tools/conformance-harness"
SCHEMA_SCRIPT_REL = "80-agents/skills/_shared/scripts/validate_schema_contract.py"
RESULTS_DIR = os.path.join(HERE, "results")

TOOL = "canonical-linter"

# A8 ratificado: fixtures sintéticas fuera del corpus. El spec fija
# `_shared/fixtures/`; se extiende a los fixtures del entity-lifecycle (misma
# clase de notas sintéticas valid/invalid; diferencia con .graphifyignore se
# registra como observación del record).
FIXTURE_REL_PREFIXES = (
    "80-agents/skills/_shared/fixtures/",
    "80-agents/skills/agents-os-entity-lifecycle/scripts/fixtures/",
)

# Clases de vida (A5). Valores de memory_state son enum a nivel de campo del
# contract; los de status se validan SIEMPRE contra el enum del tipo vía
# load_contract() (ver LintCtx.life_state()).
NO_VIGENTE_MS = ("superseded", "archived")
NO_VIGENTE_ST = ("archived", "superseded")
EN_RETIRO_ST = ("deprecated", "deprecating")
HIGH_PRIORITY = ("critical", "high")

# Campos de routing frontmatter (CL-11; hygiene-review canonical naming 4).
ROUTING_FIELDS = ("area", "project", "application", "entities", "related",
                  "parent", "supersedes", "superseded_by")
# CL-04 es el check específico de los campos de sucesión → CL-11 los excluye.
SUCCESSION_FIELDS = ("supersedes", "superseded_by")
# Proxy declarado de CL-05 (modelo sección 4: frontmatter related/entities).
CL05_PROXY_FIELDS = ("related", "entities")

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
# Patrón de paths VAULT_ROOT-relativos entre backticks (doctor check_paths,
# declarado aquí con su extensión de alcance: mismos patrones, más archivos).
BACKTICK_PATH_RE = re.compile(r"`((?:10|20|30|40|70|80|90|95)-[^`]+)`")

# CL-10 (heurística self-declared, A1: veredicto máximo WARN).
CL10_NAME_RE = re.compile(r"archiv", re.I)
CL10_MIN_NOTES = 2
CL10_MIN_RATIO = 0.5
# Scope excluido del content-rule de CL-10: el lifecycle de memory/internal es
# territorio del doctor (Check 7), no un directorio de archivo.
CL10_EXCLUDED_PREFIXES = ("80-agents/memory/internal/",)

# Umbrales declarados en el record (comparabilidad entre runs).
THRESHOLDS = {
    "cl05_proxy_fields": list(CL05_PROXY_FIELDS),
    "cl06_whitelist": "ninguna: toda colisión casefold se reporta; los grupos "
                      "estructurales (SKILL/00-index/log/...) se anotan como "
                      "mandados por autoridad en la evidencia",
    "cl08_alias_match": "exacto (string), sobre S2 y 80-agents/memory/public",
    "cl10": {"name_regex": "archiv (case-insensitive)", "min_notes": CL10_MIN_NOTES,
             "min_retired_ratio": CL10_MIN_RATIO,
             "excluded_prefixes": list(CL10_EXCLUDED_PREFIXES),
             "max_verdict": "WARN"},
    "cl12_code_fences": "los wikilinks dentro de fenced code blocks no se "
                        "cuentan como enlaces de cuerpo",
    "fixtures_excluded": list(FIXTURE_REL_PREFIXES),
}

DECLARED_AMBIGUITIES: List[str] = [
    "A5 (ratificado): clase unificada no_vigente = memory_state {superseded, archived} U "
    "status {archived, superseded} dentro del enum por tipo via load_contract(); "
    "deprecated/deprecating = sub-clase en retiro. Para tipos s1 (status forbidden) o tipo "
    "ausente, un status en el set se cuenta como estado observado con dedup_cite a "
    "lint.py:forbidden-field/bad-status/unknown-type (A3).",
    "A9 (ratificado): resolución de wikilinks = path relativo al origen > path VAULT_ROOT-"
    "relativo (constitución regla 11, para targets con '/') > basename exacto > casefold "
    "único > alias exacto; múltiples candidatos -> WARN ambiguo. Los heading/block refs "
    "([[n#sec]], [[n#^b]], [[^b]]) se resuelven por su nota; no se valida la existencia del "
    "anchor. hygiene-review + graphify-contract citados.",
    "A1: archive/ raíz no declarado por autoridad; CL-10 lo reporta WARN report-only; la "
    "decisión de migración/exclusión es del owner (hallazgo de sistema).",
    "A3: práctica de deprecación de S1 federado con status fuera de contrato (caso "
    "signals-code-review): lint.py forbidden-field/bad-status lo cubre; CL-03 sólo emite "
    "WARN del par indexable/index_priority.",
    "A10: doble registro de skills INDEX.md <-> 30-resources/agents/00-index.md permanece "
    "WARN declarado (DUAL-REGISTRY-DOMAIN-SYNC); CL-14/15/16 lo citan y jamás lo convierten "
    "en FAIL.",
    "A2: archivos sueltos en la raíz del vault SIN check (ninguna autoridad fija el layout "
    "de raíz); limitación declarada.",
]


# ---------------------------------------------------------------------------
# VAULT_ROOT + harness/schema como librería (precedente context-budget)
# ---------------------------------------------------------------------------
def resolve_vault_root(explicit: Optional[str] = None) -> Optional[str]:
    """Resuelve VAULT_ROOT: el argumento explícito, o subiendo desde la carpeta
    de esta tool hasta encontrar el marker (mismo contrato que el harness)."""
    if explicit:
        return os.path.abspath(explicit)
    d = HERE
    while True:
        if os.path.isfile(os.path.join(d, MARKER)):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def load_harness(vault_root: str):
    """Importa el harness resolviendo su ruta relativa a VAULT_ROOT en runtime
    (sys.path insert; jamás paths absolutos persistidos). PROHIBIDO fork.
    Devuelve (rules|None, harness): rules puede faltar sin invalidar harness."""
    harness_dir = os.path.join(vault_root, HARNESS_REL)
    if not os.path.isdir(harness_dir):
        raise ImportError("harness no disponible bajo %s" % HARNESS_REL)
    if harness_dir not in sys.path:
        sys.path.insert(0, harness_dir)
    import agents_os_conformance as harness  # noqa: E402
    globals()["harness"] = harness
    try:
        import rules  # noqa: E402  (transcripción única del hot path; NUNCA se copia)
        globals()["rules"] = rules
        return rules, harness
    except Exception:
        return None, harness


def load_contract_module(vault_root: str):
    """Importa validate_schema_contract.py del vault indicado y devuelve el
    módulo (load_contract() resuelve el schema-contract relativo a su propio
    archivo, que vive bajo el vault)."""
    script_dir = os.path.join(vault_root, os.path.dirname(SCHEMA_SCRIPT_REL))
    if not os.path.isdir(script_dir):
        raise ImportError("validate_schema_contract no disponible bajo %s" % SCHEMA_SCRIPT_REL)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    import validate_schema_contract as vsc  # noqa: E402
    return vsc


def git_head(root: str) -> Optional[str]:
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                              capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            return proc.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


# ---------------------------------------------------------------------------
# Helpers de texto/links
# ---------------------------------------------------------------------------
def as_list(value: Any) -> List[str]:
    """Normaliza un valor de frontmatter a lista de strings no vacíos."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    s = str(value).strip()
    return [s] if s else []


def clean_link_target(raw: str) -> Optional[str]:
    """Target de wikilink: texto antes de `|` (label) y de `#` (heading/block).
    `[[^bloque]]` y targets vacíos se ignoran (A9)."""
    s = raw.strip()
    if "|" in s:
        s = s.split("|", 1)[0].strip()
    if s.startswith("^"):
        return None
    if "#" in s:
        s = s.split("#", 1)[0].strip()
    if s.startswith("^") or not s:
        return None
    s = s.strip("\"'")
    return s or None


def strip_md(name: str) -> str:
    return name[:-3] if name.endswith(".md") else name


def parse_links_with_lines(text: str) -> List[Tuple[int, str, str]]:
    """Wikilinks de CUERPO con número de línea 1-based. Omite el bloque de
    frontmatter y los fenced code blocks (umbral declarado en THRESHOLDS)."""
    lines = text.split("\n")
    fm_end = -1
    if text.startswith("---"):
        for i in range(1, len(lines)):
            if lines[i].rstrip() == "---":
                fm_end = i
                break
    out: List[Tuple[int, str, str]] = []
    in_code = False
    for i, line in enumerate(lines):
        if i <= fm_end:
            continue
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in WIKILINK_RE.finditer(line):
            target = clean_link_target(m.group(1))
            if target:
                out.append((i + 1, m.group(0), target))
    return out


def fm_key_line(text: str, key: str) -> Optional[int]:
    """Línea 1-based de la primera aparición de `key:` dentro del bloque de
    frontmatter; None si no está."""
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            end = i
            break
    if end is None:
        return None
    pat = re.compile(r"^%s:" % re.escape(key))
    for i in range(1, end):
        if pat.match(lines[i]):
            return i + 1
    return None


def fm_field_links(fm: Dict[str, Any], fields: Tuple[str, ...]) -> List[Tuple[str, str]]:
    """Wikilinks declarados en campos de frontmatter indicados (soporta listas
    multilínea vía el parser del harness; valores quoting-tolerantes)."""
    out: List[Tuple[str, str]] = []
    for field in fields:
        for value in as_list(fm.get(field)):
            for m in WIKILINK_RE.finditer(value):
                target = clean_link_target(m.group(1))
                if target:
                    out.append((field, target))
    return out


# ---------------------------------------------------------------------------
# Contexto por run
# ---------------------------------------------------------------------------
class LintCtx(object):
    """Estado compartido por los checks: corpus vivo, mapa físico, frontmatter
    cacheado, índices de identidad y resolución de wikilinks (A9)."""

    def __init__(self, root: str, harness_mod, rules_mod, contract: Dict[str, Any]):
        self.root = root
        self.harness = harness_mod
        self.rules = rules_mod
        self.contract = contract
        # Corpus vivo = iter_vault_md del harness - fixtures (A8).
        self.corpus = [r for r in harness_mod.iter_vault_md(root)
                       if not r.startswith(FIXTURE_REL_PREFIXES)]
        # Mapa físico: todo .md del vault salvo dotdirs/basura/fixtures/
        # resultados derivados. Clases: live | archive_path | no_corpus.
        self.physical = self._walk_physical(root)
        for rel in self.corpus:
            self.physical[rel] = "live"
        self._fm_cache: Dict[str, Dict[str, Any]] = {}
        self._by_base: Dict[str, List[str]] = {}
        self._by_base_cf: Dict[str, List[str]] = {}
        self._alias_map: Dict[str, List[str]] = {}
        self._alias_built = False
        self._type_index: Optional[Dict[str, Tuple[str, dict]]] = None

    # -- walks ---------------------------------------------------------------
    def _walk_physical(self, root: str) -> Dict[str, str]:
        out: Dict[str, str] = {}
        ex_dirs = set(self.harness.EXCLUDE_DIR_NAMES)
        ex_prefixes = self.harness.EXCLUDE_FILE_PREFIXES
        for dirpath, dirnames, filenames in os.walk(root):
            rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
            if rel_dir == ".":
                rel_dir = ""
            dirnames[:] = sorted(
                d for d in dirnames
                if d not in ex_dirs and not d.startswith(".")
                and not any((rel_dir + "/" + d).startswith(FIXTURE_REL_PREFIXES)))
            full_rel_dir = (rel_dir + "/") if rel_dir else ""
            if any(full_rel_dir.startswith(p) for p in FIXTURE_REL_PREFIXES):
                continue
            for fn in sorted(filenames):
                if not fn.endswith(".md") or fn.startswith(ex_prefixes):
                    continue
                rel = full_rel_dir + fn
                if rel.startswith("80-agents/tools/canonical-linter/results/"):
                    continue  # derivados propios, jamás corpus
                if rel.startswith("40-archive/"):
                    out[rel] = "archive_path"
                else:
                    out[rel] = "no_corpus"
        return out

    # -- frontmatter / texto ---------------------------------------------------
    def text(self, rel: str) -> Optional[str]:
        path = os.path.join(self.root, rel)
        if not os.path.isfile(path):
            return None
        try:
            return self.harness.read_text(path)
        except OSError:
            return None

    def fm(self, rel: str) -> Dict[str, Any]:
        if rel not in self._fm_cache:
            try:
                self._fm_cache[rel] = self.harness.parse_frontmatter(
                    self.text(rel) or "")
            except Exception:
                self._fm_cache[rel] = {}
        return self._fm_cache[rel]

    def scalar(self, rel: str, key: str) -> str:
        """Valor escalar de frontmatter, sin quotes y en minúsculas."""
        v = self.fm(rel).get(key)
        if isinstance(v, list):
            v = v[0] if v else ""
        return str(v or "").strip().lower()

    # -- contrato (enums SIEMPRE vía load_contract) -----------------------------
    def type_index(self) -> Dict[str, Tuple[str, dict]]:
        if self._type_index is None:
            idx: Dict[str, Tuple[str, dict]] = {}
            for system, cfg in self.contract.get("systems", {}).items():
                for note_type, spec in cfg.get("types", {}).items():
                    idx[note_type] = (system, spec)
            self._type_index = idx
        return self._type_index

    def type_of(self, rel: str) -> str:
        return str(self.fm(rel).get("type") or "").strip()

    def life_state(self, rel: str) -> Dict[str, Any]:
        """Clasificación de vida de una nota (A5 + A3). Devuelve {ms, st,
        no_vigente, en_retiro, cites}: `cites` son dedup-citas a check-ids
        ajenos cuando el status observado está fuera de contrato."""
        fm = self.fm(rel)
        ms = str(fm.get("memory_state") or "").strip().lower()
        st = str(fm.get("status") or "").strip().lower()
        cites: List[str] = []
        no_vig = ms in NO_VIGENTE_MS
        en_ret = False
        if st:
            note_type = self.type_of(rel)
            spec = self.type_index().get(note_type)
            if spec:
                system, spec_cfg = spec
                statuses = spec_cfg.get("statuses") or []
                if statuses:
                    if st in statuses:
                        no_vig = no_vig or st in NO_VIGENTE_ST
                        en_ret = st in EN_RETIRO_ST
                    else:
                        # fuera del enum del tipo: lint.py bad-status, no clasifica aquí
                        cites.append("lint.py:bad-status (status '%s' fuera del enum de %s)" % (st, note_type))
                else:
                    # s1 (status forbidden) o tipo sin lifecycle: estado observado
                    # fuera de contrato (A3); lint.py forbidden-field lo cubre.
                    if st in NO_VIGENTE_ST or st in EN_RETIRO_ST:
                        cites.append("lint.py:forbidden-field (status en tipo s1 '%s', A3)" % note_type)
                        no_vig = no_vig or st in NO_VIGENTE_ST
                        en_ret = st in EN_RETIRO_ST
            else:
                if st in NO_VIGENTE_ST or st in EN_RETIRO_ST:
                    cites.append("lint.py:unknown-type (tipo '%s' no resuelto)" % (note_type or "-"))
                    no_vig = no_vig or st in NO_VIGENTE_ST
                    en_ret = st in EN_RETIRO_ST
        return {"ms": ms, "st": st, "no_vigente": no_vig, "en_retiro": en_ret,
                "cites": cites}

    # -- índices de identidad -----------------------------------------------------
    def _ensure_indexes(self) -> None:
        if self._alias_built:
            return
        for rel in sorted(self.physical):
            base = os.path.splitext(os.path.basename(rel))[0]
            self._by_base.setdefault(base, []).append(rel)
            self._by_base_cf.setdefault(base.casefold(), []).append(rel)
            fm = self.fm(rel)
            for alias in as_list(fm.get("aliases")):
                a = alias.strip()
                if a:
                    self._alias_map.setdefault(a, []).append(rel)
        self._alias_built = True

    def by_base(self) -> Dict[str, List[str]]:
        self._ensure_indexes()
        return self._by_base

    def by_base_cf(self) -> Dict[str, List[str]]:
        self._ensure_indexes()
        return self._by_base_cf

    def alias_map(self) -> Dict[str, List[str]]:
        self._ensure_indexes()
        return self._alias_map

    # -- resolución de wikilinks (A9 ratificado) ---------------------------------
    def resolve(self, target: str, src_rel: str) -> Dict[str, Any]:
        """Devuelve {status: ok|ambiguous|missing, candidates, step}.
        Pasos: (1a) path relativo al origen; (1b) path VAULT_ROOT-relativo
        (regla 11, targets con '/'); (2) basename exacto único; (3) basename
        casefold único; (4) alias declarado exacto. Sin match único en ningún
        paso pero con candidatos -> ambiguous."""
        self._ensure_indexes()
        cands: List[str] = []
        # 1a: relativo al directorio del archivo origen.
        p = os.path.normpath(os.path.join(os.path.dirname(src_rel), target)).replace(os.sep, "/")
        for cand in (p, p + ".md"):
            if cand in self.physical and cand not in cands:
                cands.append(cand)
        # 1b: VAULT_ROOT-relativo (constitución regla 11) para targets con '/'.
        if "/" in target:
            for cand in (target, target + ".md"):
                cand = os.path.normpath(cand).replace(os.sep, "/")
                if cand in self.physical and cand not in cands:
                    cands.append(cand)
        if len(cands) == 1:
            return {"status": "ok", "candidates": cands, "step": "path"}
        base = os.path.basename(strip_md(target))
        # 2: basename exacto único.
        exact = self._by_base.get(base, [])
        cands = self._merge(cands, exact)
        if len(cands) == 1:
            return {"status": "ok", "candidates": cands, "step": "basename-exacto"}
        # 3: basename casefold único.
        cf = self._by_base_cf.get(base.casefold(), [])
        cands = self._merge(cands, cf)
        if len(cands) == 1:
            return {"status": "ok", "candidates": cands, "step": "basename-casefold"}
        # 4: alias declarado exacto.
        alias_hits = self._alias_map.get(target, []) or self._alias_map.get(base, [])
        cands = self._merge(cands, alias_hits)
        if len(cands) == 1:
            return {"status": "ok", "candidates": cands, "step": "alias"}
        if cands:
            return {"status": "ambiguous", "candidates": cands, "step": "ambiguo"}
        return {"status": "missing", "candidates": [], "step": "sin-candidatos"}

    @staticmethod
    def _merge(base_list: List[str], extra: List[str]) -> List[str]:
        out = list(base_list)
        for item in sorted(extra):
            if item not in out:
                out.append(item)
        return out


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------
def finding(check_id: str, category: str, status: str, severity: str, path: str,
            observed: str, expected: str, evidence: str, authority: str,
            recommended_action: str, line: Optional[int] = None,
            confidence: str = "EXACT") -> Dict[str, Any]:
    """Finding del spec sección 3 (check_id, category, status, severity, path,
    line, observed, expected, evidence, confidence, recommended_action,
    authority). Los findings se REGISTRAN; nunca se auto-corrijen."""
    return {
        "check_id": check_id,
        "category": category,
        "status": status,  # FAIL | WARN (veredicto del finding)
        "severity": severity,  # severidad máxima del check (FAIL|WARN|report)
        "path": path,
        "line": line,
        "observed": observed,
        "expected": expected,
        "evidence": evidence,
        "confidence": confidence,
        "recommended_action": recommended_action,
        "authority": authority,
    }


def new_check(check_id: str, category: str, severity: str) -> Dict[str, Any]:
    return {"check_id": check_id, "category": category, "verdict": "SKIP",
            "severity": severity, "findings": [], "details": "",
            "skip_reason": None, "dedup_cites": [], "evidence": []}


def finish_check(rec: Dict[str, Any], findings: List[Dict[str, Any]],
                 pass_details: str, fail_details: str = "",
                 warn_details: str = "") -> Dict[str, Any]:
    rec["findings"] = findings
    if any(f["status"] == "FAIL" for f in findings):
        rec["verdict"] = "FAIL"
        rec["details"] = fail_details or ("FAIL: %d findings" % len(findings))
    elif findings:
        rec["verdict"] = "WARN"
        rec["details"] = warn_details or ("WARN: %d findings" % len(findings))
    else:
        rec["verdict"] = "PASS"
        rec["details"] = pass_details
    return rec


def skip_check(rec: Dict[str, Any], reason: str) -> Dict[str, Any]:
    rec["verdict"] = "SKIP"
    rec["skip_reason"] = reason
    rec["details"] = "no ejecutable: %s" % reason
    return rec


# ---------------------------------------------------------------------------
# CL-01..CL-20
# ---------------------------------------------------------------------------
AUTH_LINTPY = "80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py"
AUTH_DOCTOR = "80-agents/skills/agents-os-doctor/SKILL.md + scripts/doctor.py"
AUTH_HYGIENE = "80-agents/skills/agents-os-hygiene-review/SKILL.md (Link And Alias Checks)"
AUTH_RELMAINT = "80-agents/skills/agents-os-relation-maintenance/SKILL.md"
AUTH_WIKI = "30-resources/00-RESOURCE-WIKI.md"
AUTH_BOOT = "80-agents/skills/agents-os-bootstrap/SKILL.md"
AUTH_META = "80-agents/skills/_shared/metadata-schema.md"
AUTH_NOTETYPES = "80-agents/skills/_shared/note-types.md"


def _pointer_fields_nonempty(ctx: LintCtx, rel: str) -> List[str]:
    fm = ctx.fm(rel)
    out = []
    for field in SUCCESSION_FIELDS:
        if as_list(fm.get(field)):
            out.append(field)
    return out


def cl_01(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Notas active con superseded_by/supersedes no vacío (segunda autoridad
    activa). MACHINE -> FAIL. metadata-schema + 00-RESOURCE-WIKI + note-types."""
    findings: List[Dict[str, Any]] = []
    evidence: List[str] = []
    for rel in ctx.corpus:
        fm = ctx.fm(rel)
        ms = str(fm.get("memory_state") or "").strip().lower()
        st = str(fm.get("status") or "").strip().lower()
        pointers = _pointer_fields_nonempty(ctx, rel)
        if not pointers:
            continue
        if "active" not in (ms, st):
            continue
        line = None
        text = ctx.text(rel) or ""
        line = fm_key_line(text, pointers[0]) or fm_key_line(text, "status") or fm_key_line(text, "memory_state")
        findings.append(finding(
            "CL-01", "STATUS", "FAIL", "FAIL", rel,
            "estado %s con %s no vacío" % ("memory_state: active" if ms == "active" else "status: active", "+".join(pointers)),
            "una nota que declara un sucesor no debe permanecer active (no se conserva como segunda autoridad activa)",
            "campos: %s; estado: memory_state=%s status=%s" % (", ".join(pointers), ms or "-", st or "-"),
            "%s; %s (%s); %s" % (AUTH_META, AUTH_WIKI, "fuente reemplazada pasa a superseded", AUTH_NOTETYPES),
            "retirar la nota o su estado active: proposed fix para el owner (p.ej. memory_state/status -> superseded + load_policy manual); nunca auto-corregido",
            line=line))
    dedup = ["doctor:check_internal_memory_lifecycle (slice continuity bajo memory/internal: "
             "el doctor no emite esta regla cross-campo; se cita el scope adyacente)"]
    evidence.append("notas active con puntero de sucesión escaneadas sobre %d archivos del corpus" % len(ctx.corpus))
    return ("notas active con puntero de sucesión: segunda autoridad activa (metadata-schema)", findings, dedup, evidence)


def cl_02(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """superseded sin superseded_by. FAIL en agent_memory y source; WARN en el
    resto. Dentro de memory/internal el doctor ya emite el FAIL -> no
    re-emitir (dedup). `superseded_by:` vacío = ausente (template source)."""
    findings: List[Dict[str, Any]] = []
    skipped_internal = 0
    for rel in ctx.corpus:
        fm = ctx.fm(rel)
        ms = str(fm.get("memory_state") or "").strip().lower()
        st = str(fm.get("status") or "").strip().lower()
        if "superseded" not in (ms, st):
            continue
        if as_list(fm.get("superseded_by")):
            continue
        note_type = ctx.type_of(rel)
        if rel.startswith("80-agents/memory/internal/") and note_type == "agent_memory":
            skipped_internal += 1  # doctor Check 7 cubre exactamente este slice
            continue
        if note_type == "agent_memory":
            status = "FAIL"
            why = "agent_memory superseded exige superseded_by (note-types Internal Continuity + doctor Check 7)"
            auth = "%s; %s" % (AUTH_NOTETYPES, AUTH_DOCTOR)
        elif note_type == "source":
            status = "FAIL"
            why = "source reemplazada exige superseded_by (00-RESOURCE-WIKI)"
            auth = AUTH_WIKI
        else:
            status = "WARN"
            why = "estado superseded sin campo normalizado fuera de agent_memory/source (autoridad parcial; la práctica S2 usa callout)"
            auth = "%s (regla 5); %s" % ("80-agents/agents-os/agent-constitution.md", AUTH_WIKI)
        text = ctx.text(rel) or ""
        line = fm_key_line(text, "memory_state" if ms == "superseded" else "status")
        findings.append(finding(
            "CL-02", "DEPRECATION", status, "FAIL", rel,
            "estado superseded (%s) sin superseded_by no vacío" % ("memory_state" if ms == "superseded" else "status"),
            "toda nota superseded enlaza su sucesora vía superseded_by (vacío = ausente)",
            "type=%s; memory_state=%s; status=%s" % (note_type or "-", ms or "-", st or "-"),
            auth, "proponer al owner añadir superseded_by con el wikilink canónico de la sucesora; nunca auto-corregido",
            line=line, confidence="EXACT"))
    dedup = []
    if skipped_internal:
        dedup.append("doctor:check_internal_memory_lifecycle (%d nota(s) agent_memory bajo memory/internal omitidas: el doctor ya emite ese FAIL)" % skipped_internal)
    details = "notas superseded sin superseded_by (FAIL agent_memory/source, WARN resto); %d omitidas por dedup doctor" % skipped_internal
    return (details, findings, dedup, [])


def cl_03(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Estado de vida no-vigente/en-retiro + indexable true + index_priority
    critical/high. WARN fuera de memory/internal (dentro ya lo emite el
    doctor -> dedup). MACHINE (valores), autoridad explícita sólo memoria."""
    findings: List[Dict[str, Any]] = []
    skipped_internal = 0
    extra_cites: set = set()
    for rel in ctx.corpus:
        state = ctx.life_state(rel)
        if not (state["no_vigente"] or state["en_retiro"]):
            continue
        if ctx.scalar(rel, "indexable") != "true":
            continue
        if ctx.scalar(rel, "index_priority") not in HIGH_PRIORITY:
            continue
        if rel.startswith("80-agents/memory/internal/"):
            skipped_internal += 1
            continue
        line_txt = ctx.text(rel) or ""
        line = fm_key_line(line_txt, "index_priority")
        evidence = "memory_state=%s; status=%s; indexable=true; index_priority=%s%s" % (
            state["ms"] or "-", state["st"] or "-",
            ctx.scalar(rel, "index_priority"),
            ("; " + "; ".join(state["cites"])) if state["cites"] else "")
        findings.append(finding(
            "CL-03", "STATUS", "WARN", "WARN", rel,
            "estado de vida %s con indexable=true e index_priority=%s" % (
                "en retiro" if state["en_retiro"] and not state["no_vigente"] else "no-vigente",
                ctx.scalar(rel, "index_priority")),
            "una nota no-vigente o en retiro no debe conservar preferencia de índice máxima (superseded -> index_priority: low)",
            evidence,
            "80-agents/agents-os/agent-constitution.md (Memoria Interna); %s; %s (Hard Rules)" % (AUTH_DOCTOR, AUTH_BOOT),
            "proponer al owner bajar index_priority (low/never) o revisar el estado de vida; nunca auto-corregido",
            line=line, confidence="EXACT"))
        for cite in state["cites"]:
            extra_cites.add(cite)
    dedup = ["doctor:check_internal_memory_lifecycle (%d nota(s) bajo memory/internal omitidas)" % skipped_internal] if skipped_internal else []
    if extra_cites:
        dedup.extend(sorted(extra_cites))
    details = "notas no-vigente/en-retiro con índice máximo: %d findings; %d omitidas por dedup doctor" % (len(findings), skipped_internal)
    return (details, findings, dedup, [])


def cl_04(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """superseded_by/supersedes cuyo wikilink no resuelve (vacío = ausente).
    MACHINE -> FAIL (inexistente); ambiguo -> WARN con candidatos. El check
    mecaniza corpus-wide el algoritmo de hygiene-review."""
    findings: List[Dict[str, Any]] = []
    for rel in ctx.corpus:
        text = ctx.text(rel) or ""
        for field, target in fm_field_links(ctx.fm(rel), SUCCESSION_FIELDS):
            res = ctx.resolve(target, rel)
            line = fm_key_line(text, field)
            if res["status"] == "missing":
                findings.append(finding(
                    "CL-04", "DEPRECATION", "FAIL", "FAIL", rel,
                    "%s -> [[%s]] no resuelve a ninguna nota" % (field, target),
                    "el wikilink de sucesión resuelve por path relativo, basename, casefold único o alias (A9)",
                    "campo %s; target %r; resolución: sin candidatos (corpus físico %d notas)" % (field, target, len(ctx.physical)),
                    "80-agents/skills/_shared/schema-contract.md (canonical_wikilink); %s; %s; 90-system/convenciones.md" % (AUTH_META, AUTH_HYGIENE),
                    "proponer al owner corregir el target o crear la nota canónica (nunca auto-crear); nunca auto-corregido",
                    line=line))
            elif res["status"] == "ambiguous":
                findings.append(finding(
                    "CL-04", "DEPRECATION", "WARN", "FAIL", rel,
                    "%s -> [[%s]] ambiguo: %d candidatos" % (field, target, len(res["candidates"])),
                    "un wikilink de sucesión debe resolver a una única nota canónica",
                    "campo %s; target %r; candidatos: %s" % (field, target, ", ".join(res["candidates"])),
                    "80-agents/skills/_shared/schema-contract.md (canonical_wikilink); %s" % AUTH_HYGIENE,
                    "proponer al owner desambiguar con path completo o renombrar colisiones; nunca auto-corregido",
                    line=line))
    return ("wikilinks de sucesión (supersedes/superseded_by) corpus-wide; existencia cubierta por resolución A9",
            findings, ["hygiene-review:link-check (mecanizado aquí corpus-wide; allí es manual y windowed)"], [])


def cl_05(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """status deprecated/deprecating (permitido por el enum del tipo) sin
    puntero a sucesor: sin superseded_by Y sin wikilink en related/entities.
    HEURISTIC (proxy declarado) -> WARN, nunca FAIL (el callout con link
    cuenta como cumplimiento de 00-RESOURCE-WIKI)."""
    findings: List[Dict[str, Any]] = []
    for rel in ctx.corpus:
        fm = ctx.fm(rel)
        st = str(fm.get("status") or "").strip().lower()
        if st not in EN_RETIRO_ST:
            continue
        state = ctx.life_state(rel)
        if not state["en_retiro"]:
            continue  # el valor no está permitido por el enum del tipo -> lint.py
        if as_list(fm.get("superseded_by")):
            continue
        if fm_field_links(fm, CL05_PROXY_FIELDS):
            continue
        text = ctx.text(rel) or ""
        findings.append(finding(
            "CL-05", "DEPRECATION", "WARN", "WARN", rel,
            "status: %s sin puntero estructurado a sucesor (sin superseded_by ni wikilink en %s)" % (st, "/".join(CL05_PROXY_FIELDS)),
            "una página en retiro enlaza la reemplazante (00-RESOURCE-WIKI); el proxy frontmatter no identifica AL sucesor (WARN, nunca FAIL)",
            "type=%s; status=%s; superseded_by ausente/vacío; %s sin wikilinks (el callout de cuerpo, si existe, no es legible mecánicamente)" % (
                ctx.type_of(rel) or "-", st, " + ".join(CL05_PROXY_FIELDS)),
            AUTH_WIKI + " (\"usa un estado deprecated permitido por su tipo y enlaza la reemplazante\")",
            "proponer al owner añadir superseded_by o un related hacia el sucesor; el callout de cuerpo ya puede cumplir la autoridad; nunca auto-corregido",
            line=fm_key_line(text, "status"), confidence="INFERRED"))
    return ("proxy declarado (modelo sección 4): frontmatter related/entities; el callout con link cuenta como cumplimiento -> nunca FAIL",
            findings, [], [])


STRUCTURAL_BASE_HINTS = {
    "skill": "cada skill vive en <dir>/SKILL.md (doctor/REGISTRY-DISK-PARITY)",
    "00-index": "cada dominio wiki tiene su propio 00-index.md (00-RESOURCE-WIKI)",
    "log": "cada dominio wiki tiene su propia bitácora log.md (00-RESOURCE-WIKI)",
    "index": "registros/templates del sistema",
    "readme": "documentación por directorio",
    "runbook": "template 70-templates/runbook.md + runbooks locales",
}


def cl_06(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Dos notas vivas con basename idéntico casefold (colisión de identidad
    Obsidian). MACHINE -> FAIL. Sin whitelist: los grupos estructurales se
    anotan como mandados por autoridad (ver THRESHOLDS)."""
    findings: List[Dict[str, Any]] = []
    evidence: List[str] = []
    by_cf: Dict[str, List[str]] = {}
    for rel in ctx.corpus:
        base = os.path.splitext(os.path.basename(rel))[0]
        by_cf.setdefault(base.casefold(), []).append(rel)
    groups = 0
    for key in sorted(by_cf):
        rels = sorted(by_cf[key])
        if len(rels) < 2:
            continue
        groups += 1
        structural = STRUCTURAL_BASE_HINTS.get(key)
        evidence.append("%s: %s" % (key, ", ".join(rels)))
        findings.append(finding(
            "CL-06", "CANONICALITY", "FAIL", "FAIL", rels[0],
            "basename %r compartido por %d notas vivas (colisión casefold)" % (key, len(rels)),
            "un basename canónico único por identidad (convenciones: evitar duplicados por mayúsculas/acento/singular-plural)",
            "paths colisionantes: %s%s" % (" | ".join(rels),
                                           ("; nota: colisión estructural mandada por autoridad (%s): el nombre es por-directorio, no de identidad" % structural) if structural else ""),
            "90-system/convenciones.md; %s; %s (Do not create or trust duplicate entity targets)" % (AUTH_HYGIENE, "80-agents/skills/agents-os-context-retrieval/SKILL.md"),
            "proponer al owner nombre canónico único o redirect para las colisiones de identidad; las colisiones estructurales (per-directory) requieren decisión de autoridad; nunca auto-corregido",
            line=None))
    evidence.insert(0, "grupos con colisión casefold: %d sobre %d notas del corpus" % (groups, len(ctx.corpus)))
    return ("colisiones de identidad por basename casefold en el corpus vivo (sin whitelist; grupos estructurales anotados)",
            findings, [], evidence)


def cl_07(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Dos notas vivas con el mismo slug no vacío. MACHINE -> FAIL. lint.py
    sólo valida tipos, no cruza valores entre notas -> net-new."""
    findings: List[Dict[str, Any]] = []
    by_slug: Dict[str, List[str]] = {}
    for rel in ctx.corpus:
        slug = ""
        v = ctx.fm(rel).get("slug")
        if isinstance(v, list):
            v = v[0] if v else ""
        slug = str(v or "").strip().strip("\"'")
        if slug:
            by_slug.setdefault(slug, []).append(rel)
    for slug in sorted(by_slug):
        rels = sorted(by_slug[slug])
        if len(rels) < 2:
            continue
        findings.append(finding(
            "CL-07", "CANONICALITY", "FAIL", "FAIL", rels[0],
            "slug %r compartido por %d notas vivas" % (slug, len(rels)),
            "el slug es el identificador técnico (kebab-case) y debe ser único",
            "paths con el mismo slug: %s" % " | ".join(rels),
            "90-system/convenciones.md (slug = identificador técnico); 80-agents/skills/_shared/note-types.md (automation identifiers belong in slug)",
            "proponer al owner un slug único por nota; nunca auto-corregido",
            line=None))
    return ("slugs duplicados entre notas vivas (lint.py no cruza valores entre notas)",
            findings, ["lint.py:field-types (valida el slug por nota; el cruce entre notas es net-new CL-07)"], [])


def cl_08(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Mismo alias en dos notas vivas S2 o de memoria pública. MACHINE la
    detección; la resolución es HUMAN-REVIEW -> WARN (hygiene-review lo
    declara proposal-only; nunca FAIL)."""
    findings: List[Dict[str, Any]] = []
    s2_types = set(ctx.type_index().keys())
    scope_note = "notas S2 + 80-agents/memory/public"
    by_alias: Dict[str, List[str]] = {}
    for rel in ctx.corpus:
        note_type = ctx.type_of(rel)
        if note_type not in s2_types and not rel.startswith("80-agents/memory/public/"):
            continue
        for alias in as_list(ctx.fm(rel).get("aliases")):
            a = alias.strip()
            if a:
                by_alias.setdefault(a, []).append(rel)
    for alias in sorted(by_alias):
        rels = sorted(by_alias[alias])
        if len(rels) < 2:
            continue
        findings.append(finding(
            "CL-08", "CANONICALITY", "WARN", "WARN", rels[0],
            "alias %r declarado en %d notas vivas" % (alias, len(rels)),
            "las variantes humanas viven en aliases de UNA nota (convenciones); conflicto de navegación proposal-only",
            "paths con el alias: %s" % " | ".join(rels),
            AUTH_HYGIENE + " (Alias check: flag duplicate aliases, proposal-only); 90-system/convenciones.md",
            "proponer al owner qué nota conserva el alias (HUMAN-REVIEW; el linter no propone ganador); nunca auto-corregido",
            line=None))
    return ("aliases duplicados en %s (detección MACHINE, resolución HUMAN-REVIEW)" % scope_note,
            findings, ["hygiene-review:alias-check (manual y windowed allí; corpus-wide aquí)"], [])


def cl_09(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Notas bajo 40-archive/ con load_policy always o indexable true +
    priority critical/high. MACHINE (valores) con severidad atenuada -> WARN
    (landmine si se restaura; invisible para toda la tooling actual)."""
    findings: List[Dict[str, Any]] = []
    scanned = 0
    for rel in sorted(r for r, cls in ctx.physical.items() if cls == "archive_path"):
        scanned += 1
        fm = ctx.fm(rel)
        hits: List[str] = []
        if str(fm.get("load_policy") or "").strip().lower() == "always":
            hits.append("load_policy: always (copia archivada de ex-autoridad; L0 CLOSED-CLUB-ALWAYS excluye 40-archive por diseño)")
        if str(fm.get("indexable") or "").strip().lower() == "true" and \
                str(fm.get("index_priority") or "").strip().lower() in HIGH_PRIORITY:
            hits.append("indexable: true + index_priority: %s (estado de archivo con preferencia de índice máxima)" %
                        str(fm.get("index_priority")).strip().lower())
        if not hits:
            continue
        text = ctx.text(rel) or ""
        line = fm_key_line(text, "load_policy") or fm_key_line(text, "index_priority")
        findings.append(finding(
            "CL-09", "ARCHIVE", "WARN", "WARN", rel,
            "nota bajo 40-archive/ con " + " y ".join(hits),
            "el archivo es retención histórica: sin always ni preferencia de índice (landmine si se restaura a mano)",
            "; ".join(hits),
            "%s (Check 3/1); .graphifyignore; %s (Hard Rules); materialize_schema_note.py FORBIDDEN_TARGET_ROOTS" % (AUTH_DOCTOR, AUTH_BOOT),
            "proponer al owner normalizar la copia archivada (p.ej. load_policy: never); decisión A7 del parent: no se normaliza automáticamente; nunca auto-corregido",
            line=line))
    return ("notas bajo 40-archive/ escaneadas: %d; hallazgos WARN (hoy invisibles para L0/doctor por diseño de sus scopes)" % scanned,
            findings, ["L0:CLOSED-CLUB-ALWAYS (excluye 40-archive por diseño)", "doctor:check_always (scope 80-agents/)"], [])


def cl_10(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Directorios con forma de archive fuera de 40-archive/ y no declarados.
    HEURISTIC (A1: la autoridad no define la lista cerrada) -> WARN
    report-only con inventario. Regla declarada en THRESHOLDS."""
    findings: List[Dict[str, Any]] = []
    evidence: List[str] = []
    dirs: Dict[str, List[str]] = {}
    for rel in ctx.corpus:
        d = os.path.dirname(rel)
        if any(d.startswith(p) or d == p.rstrip("/") for p in CL10_EXCLUDED_PREFIXES):
            continue
        dirs.setdefault(d, []).append(rel)
    for d in sorted(dirs):
        rels = sorted(dirs[d])
        retired = [r for r in rels if (lambda s: s["no_vigente"] or s["en_retiro"])(ctx.life_state(r))]
        name_hit = bool(CL10_NAME_RE.search(os.path.basename(d)))
        ratio_hit = len(rels) >= CL10_MIN_NOTES and (len(retired) / len(rels)) >= CL10_MIN_RATIO
        if not (name_hit or ratio_hit):
            continue
        states = {}
        for r in rels:
            s = ctx.life_state(r)
            key = s["st"] or s["ms"] or "sin-estado"
            states[key] = states.get(key, 0) + 1
        conf = "EXACT" if name_hit else "INFERRED"
        evidence.append("%s: %d nota(s); estados: %s; disparador: %s" % (
            d, len(rels), json.dumps(states, sort_keys=True),
            "nombre del directorio" if name_hit else "proporción de notas en retiro/no-vigente"))
        findings.append(finding(
            "CL-10", "ARCHIVE", "WARN", "WARN", d + "/",
            "directorio con forma de archive fuera de 40-archive/ (%d nota(s); estados %s)" % (
                len(rels), json.dumps(states, sort_keys=True)),
            "la retención histórica vive en 40-archive/ (o raíz declarada por autoridad); hoy entra al corpus Graphify como notas vivas",
            "disparador: %s; notas: %s" % ("nombre" if name_hit else "contenido",
                                           ", ".join(rels[:8]) + ("..." if len(rels) > 8 else "")),
            "80-agents/agents-os/agents-os.md (estructura informativa, sin 40-archive); .graphifyignore (no excluye esta raíz); materialize_schema_note.py (sólo conoce 40-archive)",
            "A1: registrar como hallazgo de sistema; el owner decide migrar a 40-archive/, declarar la raíz o excluirla; nunca auto-corregido",
            line=None, confidence=conf))
    return ("inventario de directorios con forma de archive fuera de 40-archive/ (A1: report-only, sin FAIL posible)",
            findings, [], evidence)


def cl_11(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Wikilinks de campos de routing frontmatter que no resuelven. MACHINE
    -> FAIL (ambiguo -> WARN). Excluye supersedes/superseded_by (CL-04)."""
    findings: List[Dict[str, Any]] = []
    fields = tuple(f for f in ROUTING_FIELDS if f not in SUCCESSION_FIELDS)
    for rel in ctx.corpus:
        text = ctx.text(rel) or ""
        seen: set = set()
        for field, target in fm_field_links(ctx.fm(rel), fields):
            if (field, target) in seen:
                continue
            seen.add((field, target))
            res = ctx.resolve(target, rel)
            if res["status"] == "ok":
                continue
            line = fm_key_line(text, field)
            if res["status"] == "missing":
                findings.append(finding(
                    "CL-11", "REFERENCES", "FAIL", "FAIL", rel,
                    "campo %s -> [[%s]] no resuelve a ninguna nota" % (field, target),
                    "area/project/application/entities/related usan links canónicos que resuelven (convenciones)",
                    "campo %s; target %r; resolución A9: sin candidatos" % (field, target),
                    "90-system/convenciones.md (area, project, application, entities y related deben usar links canónicos); %s; %s" % (AUTH_DOCTOR, AUTH_HYGIENE),
                    "proponer al owner corregir el target al nombre canónico; nunca auto-corregido",
                    line=line))
            else:
                findings.append(finding(
                    "CL-11", "REFERENCES", "WARN", "FAIL", rel,
                    "campo %s -> [[%s]] ambiguo: %d candidatos" % (field, target, len(res["candidates"])),
                    "el link de routing debe apuntar a una única nota canónica",
                    "campo %s; target %r; candidatos: %s" % (field, target, ", ".join(res["candidates"])),
                    "90-system/convenciones.md; %s" % AUTH_HYGIENE,
                    "proponer al owner desambiguar con path completo; nunca auto-corregido",
                    line=line))
    return ("wikilinks de routing frontmatter corpus-wide (vacío el doctor Checks 2 no implementado en script; supersedes/superseded_by van en CL-04)",
            findings, ["CL-04 (campos de sucesión, mismo algoritmo de resolución)"], [])


def cl_12(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Wikilinks de CUERPO que no resuelven. WARN (el FAIL queda reservado a
    routing: CL-11). heading/bloque/label se resuelven por su nota; fenced
    code blocks se excluyen (THRESHOLDS)."""
    findings: List[Dict[str, Any]] = []
    for rel in ctx.corpus:
        text = ctx.text(rel)
        if not text:
            continue
        for line_no, raw, target in parse_links_with_lines(text):
            res = ctx.resolve(target, rel)
            if res["status"] == "ok":
                continue
            if res["status"] == "missing":
                findings.append(finding(
                    "CL-12", "BROKEN LINKS", "WARN", "WARN", rel,
                    "%s no resuelve a ninguna nota" % raw,
                    "el link de cuerpo resuelve por basename/path/alias (A9); no se auto-crea la nota faltante",
                    "target %r; línea %d; resolución A9: sin candidatos" % (target, line_no),
                    AUTH_HYGIENE + " (Report unresolved links; Do not auto-create missing notes); " + AUTH_RELMAINT,
                    "proponer al owner corregir el link o crear la nota canónica (decisión humana); nunca auto-corregido",
                    line=line_no))
            else:
                findings.append(finding(
                    "CL-12", "BROKEN LINKS", "WARN", "WARN", rel,
                    "%s ambiguo: %d candidatos" % (raw, len(res["candidates"])),
                    "un link de cuerpo debe resolver a una única nota",
                    "target %r; línea %d; candidatos: %s" % (target, line_no, ", ".join(res["candidates"])),
                    AUTH_HYGIENE + " (ambiguous basename matches)",
                    "proponer al owner desambiguar (path completo o renombrar); nunca auto-corregido",
                    line=line_no))
    return ("wikilinks de cuerpo corpus-wide (sin fenced code blocks); intención histórica es HUMAN-REVIEW",
            findings, ["hygiene-review:link-check (manual/windowed allí; corpus-wide aquí)", AUTH_RELMAINT], [])


def cl_13(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Notas del corpus vivo que enlazan (cuerpo o frontmatter) a notas
    ARCHIVED (path 40-archive/ o estado archived/superseded). WARN: la
    intención histórica ("unless intentional") es HUMAN-REVIEW."""
    findings: List[Dict[str, Any]] = []
    seen: set = set()
    fields = tuple(ROUTING_FIELDS)
    for rel in ctx.corpus:
        links: List[Tuple[Optional[int], str]] = []
        text = ctx.text(rel)
        if text:
            for line_no, _raw, target in parse_links_with_lines(text):
                links.append((line_no, target))
        for _field, target in fm_field_links(ctx.fm(rel), fields):
            links.append((None, target))
        for line_no, target in links:
            res = ctx.resolve(target, rel)
            if res["status"] != "ok":
                continue  # missing/ambiguous: CL-12/CL-04/CL-11
            target_rel = res["candidates"][0]
            if target_rel == rel:
                continue
            key = (rel, target_rel)
            if key in seen:
                continue
            seen.add(key)
            tstate = ctx.life_state(target_rel)
            cls = ctx.physical.get(target_rel, "")
            archived_by_path = cls == "archive_path"
            if not archived_by_path and not tstate["no_vigente"]:
                continue
            motivo = "path 40-archive/" if archived_by_path else "estado %s" % (tstate["ms"] or tstate["st"])
            ev = "origen %s -> destino %s (%s)" % (rel, target_rel, motivo)
            if tstate["cites"]:
                ev += "; " + "; ".join(tstate["cites"])
            findings.append(finding(
                "CL-13", "REFERENCES", "WARN", "WARN", rel,
                "enlaza a nota ARCHIVED %s ([[%s]])" % (motivo, target_rel),
                "reemplazar links a archivados salvo que el link histórico sea intencional (relation-maintenance paso 7)",
                ev,
                AUTH_RELMAINT + " (Hard Rules + paso 7, cláusula unless intentional); 80-agents/agents-os/agent-constitution.md (regla 10)",
                "proponer al owner confirmar la intención histórica o reemplazar el link; nunca auto-corregido",
                line=line_no))
    return ("links vivos hacia notas archived (path o estado); la intención histórica es HUMAN-REVIEW -> nunca FAIL",
            findings, [AUTH_RELMAINT + " (ejecuta el juicio manualmente)"], [])


def _wiki_index_files(ctx: LintCtx) -> List[str]:
    """00-index.md de dominios wiki activos (type: index, status: active) bajo
    30-resources/ (definición de 00-RESOURCE-WIKI)."""
    out = []
    for rel in ctx.corpus:
        if not rel.startswith("30-resources/") or os.path.basename(rel) != "00-index.md":
            continue
        fm = ctx.fm(rel)
        if str(fm.get("type") or "").strip() == "index" and \
                str(fm.get("status") or "").strip() == "active":
            out.append(rel)
    return sorted(out)


def _index_rows(ctx: LintCtx, rel: str) -> List[Tuple[int, str]]:
    """Filas de tabla del índice (líneas que empiezan con '|' y no son
    separadores) -> (línea, primer target de wikilink)."""
    text = ctx.text(rel) or ""
    rows: List[Tuple[int, str]] = []
    for i, line in enumerate(text.split("\n")):
        if not line.startswith("|"):
            continue
        if re.match(r"^\|[\s:|-]+\|?\s*$", line):
            continue  # separador
        m = WIKILINK_RE.search(line)
        if not m:
            continue
        target = clean_link_target(m.group(1))
        if target:
            rows.append((i + 1, target))
    return rows


def cl_14(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Filas de 00-index.md de dominio activo wiki apuntando a archivo
    inexistente. MACHINE -> FAIL (ambiguo -> WARN). Los 00-index de la wiki
    no tienen cobertura mecánica previa (REGISTRY-DISK-PARITY es sólo INDEX de
    skills) -> net-new."""
    findings: List[Dict[str, Any]] = []
    indexes = _wiki_index_files(ctx)
    checked = 0
    for idx_rel in indexes:
        for line_no, target in _index_rows(ctx, idx_rel):
            checked += 1
            res = ctx.resolve(target, idx_rel)
            if res["status"] == "ok":
                continue
            if res["status"] == "missing":
                findings.append(finding(
                    "CL-14", "ROUTING", "FAIL", "FAIL", idx_rel,
                    "fila del índice -> [[%s]] no resuelve a ninguna nota" % target,
                    "una fila por página vigente: el link del catálogo resuelve (00-RESOURCE-WIKI: un índice desactualizado es deuda)",
                    "target %r; línea %d; resolución A9: sin candidatos" % (target, line_no),
                    AUTH_WIKI + " (00-index catálogo curado, Layer 1 del context-retrieval)",
                    "proponer al owner corregir la fila o restaurar la página; nunca auto-corregido",
                    line=line_no))
            else:
                findings.append(finding(
                    "CL-14", "ROUTING", "WARN", "FAIL", idx_rel,
                    "fila del índice -> [[%s]] ambiguo: %d candidatos" % (target, len(res["candidates"])),
                    "la fila del catálogo apunta a una única página canónica",
                    "target %r; línea %d; candidatos: %s" % (target, line_no, ", ".join(res["candidates"])),
                    AUTH_WIKI + "; " + AUTH_HYGIENE,
                    "proponer al owner desambiguar la fila con path completo; nunca auto-corregido",
                    line=line_no))
    dedup = [
        "L0:REGISTRY-DISK-PARITY + doctor:check_skill_index (cubren SÓLO el INDEX.md de skills; este check es el de los 00-index de la wiki)",
        "L0:DUAL-REGISTRY-DOMAIN-SYNC (A10: la dualidad INDEX<->00-index no se convierte en FAIL)",
    ]
    return ("00-index de dominios wiki activos escaneados: %d; filas con link verificadas: %d" % (len(indexes), checked),
            findings, dedup, ["00-index activos: %s" % ", ".join(indexes)])


def cl_15(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Filas de 00-index.md de dominio activo apuntando a páginas con estado
    no-vigente/en-retiro o bajo 40-archive/. MACHINE -> FAIL. Net-new (ni
    REGISTRY-DISK-PARITY ni CTX-12 miran filas de índices)."""
    findings: List[Dict[str, Any]] = []
    indexes = _wiki_index_files(ctx)
    checked = 0
    extra_cites: set = set()
    for idx_rel in indexes:
        for line_no, target in _index_rows(ctx, idx_rel):
            res = ctx.resolve(target, idx_rel)
            if res["status"] != "ok":
                continue  # inexistente/ambiguo: CL-14
            checked += 1
            target_rel = res["candidates"][0]
            tstate = ctx.life_state(target_rel)
            archived_by_path = ctx.physical.get(target_rel, "") == "archive_path"
            if not (archived_by_path or tstate["no_vigente"] or tstate["en_retiro"]):
                continue
            motivo = "path 40-archive/" if archived_by_path else \
                ("estado %s" % (tstate["ms"] or tstate["st"]))
            ev = "fila -> %s (%s); línea %d" % (target_rel, motivo, line_no)
            for cite in tstate["cites"]:
                extra_cites.add(cite)
                ev += "; " + cite
            findings.append(finding(
                "CL-15", "ROUTING", "FAIL", "FAIL", idx_rel,
                "fila del índice apunta a página no vigente (%s): [[%s]]" % (motivo, target_rel),
                "el índice raíz deja una sola entrada vigente (una fila por página vigente)",
                ev,
                AUTH_WIKI + " (deprecación S2: el índice deja una sola entrada vigente)",
                "proponer al owner retirar la fila o revisar el estado de la página; nunca auto-corregido",
                line=line_no))
    dedup = [
        "context-budget:CTX-12/M16 (mira frontmatter de archivos del set fijo, no filas de índices)",
        "CL-14 (filas inexistentes/ambiguas van allí)",
        "L0:DUAL-REGISTRY-DOMAIN-SYNC (A10)",
    ]
    dedup.extend(sorted(extra_cites))
    return ("00-index de dominios wiki activos: filas con destino resuelto verificadas: %d" % checked,
            findings, dedup, [])


def cl_16(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """INDEX.md (DEFAULT-LOADED) con destino bajo 40-archive/ (FAIL) o con
    estado de vida no-vigente (WARN). La EXISTENCIA de destinos ya la cubren
    L0 REGISTRY-DISK-PARITY y doctor check_skill_index -> dedup, no re-emitir."""
    findings: List[Dict[str, Any]] = []
    evidence: List[str] = []
    index_rel = ctx.rules.SKILLS_INDEX
    text = ctx.text(index_rel)
    if text is None:
        return ("INDEX.md no disponible", findings,
                ["L0:REGISTRY-DISK-PARITY", "doctor:check_skill_index"],
                ["SKIP parcial: %s ausente" % index_rel])
    # (a) cualquier link/backtick-path de INDEX cuyo destino viva bajo 40-archive/
    for i, line in enumerate(text.split("\n")):
        for m in WIKILINK_RE.finditer(line):
            target = clean_link_target(m.group(1))
            if not target:
                continue
            res = ctx.resolve(target, index_rel)
            for cand in res["candidates"]:
                if cand.startswith("40-archive/"):
                    findings.append(finding(
                        "CL-16", "ROUTING", "FAIL", "FAIL", index_rel,
                        "enlace de INDEX.md cuyo destino está bajo 40-archive/: %s" % cand,
                        "el registry default-loaded nunca enruta a retención histórica",
                        "target %r; línea %d; resuelto a %s" % (target, i + 1, cand),
                        AUTH_BOOT + " (paso 3); " + AUTH_WIKI + " (una fila por vigente, análogo)",
                        "proponer al owner retirar el enlace o migrar el destino; nunca auto-corregido",
                        line=i + 1))
        for m in BACKTICK_PATH_RE.finditer(line):
            p = m.group(1).strip()
            if p.startswith("40-archive/"):
                findings.append(finding(
                    "CL-16", "ROUTING", "FAIL", "FAIL", index_rel,
                    "path citado por INDEX.md bajo 40-archive/: %s" % p,
                    "el registry default-loaded nunca cita retención histórica como destino de routing",
                    "path %r; línea %d" % (p, i + 1),
                    AUTH_BOOT + " (paso 3)",
                    "proponer al owner retirar la cita; nunca auto-corregido",
                    line=i + 1))
    # (b) filas core/federadas: estados de vida del destino (existencia -> dedup)
    sections = ctx.harness._parse_index_tables(text)
    row_targets: List[str] = []
    for row in sections.get("core", []) + sections.get("federated", []):
        m = re.search(r"\[\[((?:80-agents/skills|30-resources/agents/skills)/[^/\]|#]+)/SKILL(?:\.md)?[^\]]*\]\]", row)
        if m:
            row_targets.append(m.group(1) + "/SKILL.md")
    seen: set = set()
    missing_existence = 0
    for target in row_targets:
        target = target.replace("//", "/")
        if target in seen:
            continue
        seen.add(target)
        if target not in ctx.physical:
            missing_existence += 1  # REGISTRY-DISK-PARITY/doctor lo emiten: no re-emitir
            continue
        tstate = ctx.life_state(target)
        if not (tstate["no_vigente"] or tstate["en_retiro"]):
            continue
        ev = "fila de INDEX -> %s (estado %s)" % (target, tstate["ms"] or tstate["st"])
        for cite in tstate["cites"]:
            ev += "; " + cite
        findings.append(finding(
            "CL-16", "ROUTING", "WARN", "FAIL", index_rel,
            "destino de fila de INDEX con estado de vida no vigente: %s (%s)" % (target, tstate["ms"] or tstate["st"]),
            "el registry cargado en cold start enruta sólo a skills vigentes (las skills no definen lifecycle: cualquier estado de vida observado es WARN)",
            ev,
            AUTH_BOOT + " (paso 3: how the agent knows which skills exist)",
            "proponer al owner revisar el estado de la skill o la fila; nunca auto-corregido",
            line=None))
    if missing_existence:
        evidence.append("destinos inexistentes: %d (NO re-emitidos: cubiertos por L0 REGISTRY-DISK-PARITY + doctor check_skill_index)" % missing_existence)
    evidence.append("filas core+federadas con destino único: %d" % len(seen))
    dedup = [
        "L0:REGISTRY-DISK-PARITY (existencia de destinos de INDEX)",
        "doctor:check_skill_index (existencia de destinos de INDEX)",
        "L0:DUAL-REGISTRY-DOMAIN-SYNC (A10)",
        "context-budget:CTX-12/M16 (frontmatter del INDEX como archivo, no sus filas)",
    ]
    return ("INDEX.md: destinos archive (FAIL) y estados de vida de filas (WARN); existencia deduplicada",
            findings, dedup, evidence)


def _hot_source_files(ctx: LintCtx) -> List[str]:
    """Archivos DEFAULT-LOADED cuya prosa cita paths/links: bootstrap SKILL,
    constitución, continuidad global, INDEX + perfil resuelto por directorio
    (método del doctor _always_profiles / harness resolve_profile_note)."""
    vault = ctx.harness.Vault(ctx.root, ctx.harness.parse_frontmatter)
    profile = vault.resolve_profile_note()
    files = [
        "80-agents/skills/agents-os-bootstrap/SKILL.md",
        ctx.rules.CONSTITUTION,
        ctx.rules.GLOBAL_INTERNAL,
        ctx.rules.SKILLS_INDEX,
    ]
    if profile:
        files.append(profile)
    return [f for f in files if f in ctx.physical]


def cl_17(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Paths VAULT_ROOT-relativos entre backticks en los archivos
    DEFAULT-LOADED que no resuelven a disco. MACHINE -> FAIL. Extensión
    declarada del patrón del doctor (que cubre SÓLO AGENTS.md)."""
    findings: List[Dict[str, Any]] = []
    files = _hot_source_files(ctx)
    scanned = 0
    for rel in files:
        text = ctx.text(rel)
        if text is None:
            continue
        scanned += 1
        for i, line in enumerate(text.split("\n")):
            for m in BACKTICK_PATH_RE.finditer(line):
                raw = m.group(1).strip()
                if "<" in raw:
                    continue  # placeholder (misma regla del doctor)
                p = raw.rstrip("/") if not raw.endswith("/") else raw
                abspath = os.path.join(ctx.root, raw)
                if raw.endswith("/"):
                    ok = os.path.isdir(abspath)
                else:
                    ok = os.path.isfile(abspath) or os.path.isdir(abspath)
                if ok:
                    continue
                findings.append(finding(
                    "CL-17", "HOT-PATH", "FAIL", "FAIL", rel,
                    "path VAULT_ROOT-relativo citado que no resuelve a disco: %s" % raw,
                    "toda referencia interna del hot path es relativa a VAULT_ROOT y existe (constitución regla 11)",
                    "path %r; línea %d; citador: %s" % (raw, i + 1, rel),
                    "80-agents/agents-os/agent-constitution.md (regla 11); " + AUTH_BOOT + " (pasos 1-5); " + AUTH_DOCTOR + " (Check 1)",
                    "proponer al owner corregir la ruta citada; nunca auto-corregido",
                    line=i + 1))
    dedup = [
        "doctor:check_paths (cubre SÓLO AGENTS.md; este check extiende el mismo patrón a los demás hot-path files)",
        "doctor:check_skill_refs (refs relativas '../' de skills, scope distinto)",
    ]
    return ("archivos DEFAULT-LOADED escaneados: %d (AGENTS.md excluido: dedup doctor)" % scanned,
            findings, dedup, ["citadores: %s" % ", ".join(files)])


def _m16_fixed_set(ctx: LintCtx) -> set:
    """Set fijo de CTX-12/M16 (always + packs + especialistas): su frontmatter
    ya está barrido por context-budget -> CL-18 no lo re-barre."""
    vault = ctx.harness.Vault(ctx.root, ctx.harness.parse_frontmatter)
    profile = vault.resolve_profile_note() or ""
    files = {ctx.rules.CONSTITUTION, profile, ctx.rules.GLOBAL_INTERNAL,
             ctx.rules.SKILLS_INDEX, ctx.rules.ROUTERS["meli"],
             ctx.rules.ROUTERS["aranea"], ctx.rules.ARANEA_MCPS_EXPERT}
    files |= set(ctx.rules.ROUTER_PREFS["meli"]) | set(ctx.rules.ROUTER_PREFS["aranea"])
    for names in ctx.rules.DOMAIN_GATED_SKILLS.values():
        for name in names:
            files.add("30-resources/agents/skills/%s/SKILL.md" % name)
    return {f for f in files if f}


def cl_18(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """Contaminación de DESTINOS de routing desde hot path: Minimal Reads de
    routers/prefs, paths citados en cold steps, con estado no-vigente/en-retiro
    o bajo 40-archive/. MACHINE -> FAIL. El set fijo de archivos (M16) NO se
    re-barre (dedup CTX-12); las filas de INDEX/00-index van en CL-15/CL-16."""
    findings: List[Dict[str, Any]] = []
    evidence: List[str] = []
    m16 = _m16_fixed_set(ctx)
    destinations: List[Tuple[str, str, str]] = []  # (destino, mecanismo, origen)
    # (a) Minimal Reads: links y paths citados en routers + preferencias scoped.
    for rel in [ctx.rules.ROUTERS["meli"], ctx.rules.ROUTERS["aranea"]] + \
            ctx.rules.ROUTER_PREFS["meli"] + ctx.rules.ROUTER_PREFS["aranea"]:
        text = ctx.text(rel)
        if text is None:
            continue
        for line_no, _raw, target in parse_links_with_lines(text):
            res = ctx.resolve(target, rel)
            if res["status"] == "ok":
                destinations.append((res["candidates"][0], "Minimal Read de router/prefs", rel))
        for m in BACKTICK_PATH_RE.finditer(text):
            p = os.path.normpath(m.group(1).strip()).replace(os.sep, "/")
            if p in ctx.physical:
                destinations.append((p, "path citado por router/prefs", rel))
    # (b) cold steps: paths citados en bootstrap/constitución/continuidad/INDEX/perfil.
    for rel in _hot_source_files(ctx):
        text = ctx.text(rel)
        if text is None:
            continue
        for m in BACKTICK_PATH_RE.finditer(text):
            p = os.path.normpath(m.group(1).strip()).replace(os.sep, "/")
            if p in ctx.physical:
                destinations.append((p, "path citado en cold step", rel))
    checked = 0
    skipped_m16 = 0
    seen: set = set()
    for dest, mechanism, origin in destinations:
        key = (dest, mechanism)
        if key in seen:
            continue
        seen.add(key)
        if dest in m16:
            skipped_m16 += 1  # frontmatter ya barrido por CTX-12/M16
            continue
        checked += 1
        tstate = ctx.life_state(dest)
        archived_by_path = ctx.physical.get(dest, "") == "archive_path"
        if not (archived_by_path or tstate["no_vigente"] or tstate["en_retiro"]):
            continue
        motivo = "path 40-archive/" if archived_by_path else \
            ("estado %s" % (tstate["ms"] or tstate["st"]))
        ev = "destino %s (%s) enrutado desde %s via %s" % (dest, motivo, origin, mechanism)
        for cite in tstate["cites"]:
            ev += "; " + cite
        findings.append(finding(
            "CL-18", "HOT-PATH", "FAIL", "FAIL", dest,
            "destino de routing del hot path en estado no vigente (%s): %s" % (motivo, os.path.basename(dest)),
            "never load superseded or archived continuity/content during normal startup or entity retrieval (bootstrap Hard Rules)",
            ev,
            AUTH_BOOT + " (Hard Rules); 80-agents/agents-os/agent-constitution.md (regla 10)",
            "proponer al owner retirar el destino del mecanismo de routing o revisar su estado; nunca auto-corregido",
            line=None))
    skipped_rows = 2  # INDEX rows (CL-16) y 00-index rows (CL-15): scopes propios
    evidence.append("destinos únicos verificados: %d; omitidos por dedup M16: %d; scopes de filas delegados: CL-15/CL-16" % (checked, skipped_m16))
    dedup = [
        "context-budget:CTX-12/M16 (frontmatter de los ARCHIVOS del set fijo: always + packs + especialistas; %d destinos omitidos)" % skipped_m16,
        "CL-15 (filas de 00-index de la wiki) y CL-16 (filas de INDEX.md): las filas son destino en aquellos checks",
        "doctor:check_internal_memory_lifecycle (continuity bajo memory/internal)",
    ]
    return ("destinos resueltos del routing (Minimal Reads + cold steps): %d verificados; %d en set fijo M16 (omitidos)" % (checked, skipped_m16),
            findings, dedup, evidence)


def cl_19(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """type resource/methodology con status: active sin last_verified. WARN
    (nunca FAIL: 00-RESOURCE-WIKI prohíbe la cadencia global; una página sin
    last_verified no está automáticamente inválida)."""
    findings: List[Dict[str, Any]] = []
    for rel in ctx.corpus:
        fm = ctx.fm(rel)
        note_type = ctx.type_of(rel)
        if note_type not in ("resource", "methodology"):
            continue
        spec = ctx.type_index().get(note_type)
        if not spec or "active" not in (spec[1].get("statuses") or []):
            continue
        if str(fm.get("status") or "").strip().lower() != "active":
            continue
        lv = fm.get("last_verified")
        if isinstance(lv, list):
            lv = lv[0] if lv else ""
        if str(lv or "").strip():
            continue
        text = ctx.text(rel) or ""
        findings.append(finding(
            "CL-19", "METADATA", "WARN", "WARN", rel,
            "type: %s con status: active sin last_verified" % note_type,
            "last_verified registra cuándo se contrastaron las afirmaciones (freshness event-driven: su ausencia no invalida la página)",
            "type=%s; status=active; last_verified ausente/vacío (dato de freshness, nunca veredicto de vigencia)" % note_type,
            AUTH_WIKI + " (freshness event-driven; no existe cadencia global inventada); 80-agents/skills/_shared/schema-contract.md (last_verified optional)",
            "proponer al owner contrastar la página con sus fuentes y fijar last_verified; nunca auto-corregido",
            line=fm_key_line(text, "status")))
    return ("notas resource/methodology activas sin last_verified (dato de freshness; WARN prohibido de escalar a FAIL)",
            findings, [AUTH_LINTPY + " (envelope required/created/updated ya exigido por el lint del corpus)"], [])


def cl_20(ctx: LintCtx) -> Tuple[str, List[Dict[str, Any]], List[str], List[str]]:
    """memory_state presente en nota cuyo tipo declarado != agent_memory.
    WARN report-only: uso informal del campo fuera de su tipo de contrato; no
    decide migración (HUMAN-REVIEW)."""
    findings: List[Dict[str, Any]] = []
    for rel in ctx.corpus:
        fm = ctx.fm(rel)
        ms = str(fm.get("memory_state") or "").strip()
        if not ms:
            continue
        note_type = ctx.type_of(rel)
        if not note_type:
            continue  # tipo ausente: lint.py unknown-type
        if note_type == "agent_memory":
            continue
        text = ctx.text(rel) or ""
        findings.append(finding(
            "CL-20", "METADATA", "WARN", "WARN", rel,
            "memory_state: %s en nota de tipo %s (!= agent_memory)" % (ms, note_type),
            "memory_state es campo opcional del tipo agent_memory; no reemplaza el status de entidades Sistema 2",
            "type=%s; memory_state=%s (uso informal del campo fuera de su tipo de contrato)" % (note_type, ms),
            "80-agents/skills/_shared/schema-contract.md (memory_state es opcional de agent_memory); " + AUTH_META,
            "proponer al owner migrar el estado de vida al campo status del tipo o reclasificar la nota (HUMAN-REVIEW); nunca auto-corregido",
            line=fm_key_line(text, "memory_state")))
    return ("memory_state fuera de agent_memory (report-only; lint.py no lo marca: sólo forbidden explícito)",
            findings, [AUTH_LINTPY + " (forbidden-field sólo cubre prohibiciones explícitas del envelope)"], [])


# ---------------------------------------------------------------------------
# Registro y runner
# ---------------------------------------------------------------------------
CHECKS: List[Tuple[str, str, str, Any, Tuple[str, ...]]] = [
    # (id, categoría, severidad máxima, función, dependencias)
    ("CL-01", "STATUS", "FAIL", cl_01, ("contract", "harness")),
    ("CL-02", "DEPRECATION", "FAIL", cl_02, ("contract", "harness")),
    ("CL-03", "STATUS", "WARN", cl_03, ("contract", "harness")),
    ("CL-04", "DEPRECATION", "FAIL", cl_04, ("harness",)),
    ("CL-05", "DEPRECATION", "WARN", cl_05, ("contract", "harness")),
    ("CL-06", "CANONICALITY", "FAIL", cl_06, ("harness",)),
    ("CL-07", "CANONICALITY", "FAIL", cl_07, ("harness",)),
    ("CL-08", "CANONICALITY", "WARN", cl_08, ("contract", "harness")),
    ("CL-09", "ARCHIVE", "WARN", cl_09, ("harness",)),
    ("CL-10", "ARCHIVE", "WARN", cl_10, ("contract", "harness")),
    ("CL-11", "REFERENCES", "FAIL", cl_11, ("harness",)),
    ("CL-12", "BROKEN LINKS", "WARN", cl_12, ("harness",)),
    ("CL-13", "REFERENCES", "WARN", cl_13, ("contract", "harness")),
    ("CL-14", "ROUTING", "FAIL", cl_14, ("harness",)),
    ("CL-15", "ROUTING", "FAIL", cl_15, ("contract", "harness")),
    ("CL-16", "ROUTING", "FAIL", cl_16, ("harness", "rules")),
    ("CL-17", "HOT-PATH", "FAIL", cl_17, ("harness", "rules")),
    ("CL-18", "HOT-PATH", "FAIL", cl_18, ("contract", "harness", "rules")),
    ("CL-19", "METADATA", "WARN", cl_19, ("contract", "harness")),
    ("CL-20", "METADATA", "WARN", cl_20, ("contract", "harness")),
]

CATEGORIES = sorted({c[1] for c in CHECKS})


def build_ctx(vault_root: str) -> Tuple[Optional[LintCtx], Dict[str, str]]:
    """Construye el LintCtx; devuelve también qué dependencias fallaron para
    los SKIP motivados (spec sección 3: nunca traceback)."""
    failures: Dict[str, str] = {}
    harness_mod = rules_mod = None
    contract: Optional[Dict[str, Any]] = None
    try:
        rules_mod, harness_mod = load_harness(vault_root)
    except Exception as exc:
        failures["harness"] = "harness no importable (%s: %s)" % (type(exc).__name__, exc)
        return None, failures
    if rules_mod is None:
        failures["rules"] = "rules.py no importable bajo %s" % HARNESS_REL
    try:
        vsc = load_contract_module(vault_root)
        contract = vsc.load_contract()
    except Exception as exc:
        failures["contract"] = "schema-contract no cargable (%s: %s)" % (type(exc).__name__, exc)
        contract = None
    try:
        ctx = LintCtx(vault_root, harness_mod, rules_mod, contract or {})
    except Exception as exc:
        failures["corpus"] = "corpus no construible (%s: %s)" % (type(exc).__name__, exc)
        return None, failures
    return ctx, failures


def run_checks(ctx: Optional[LintCtx], failures: Dict[str, str],
               only_ids: Optional[List[str]] = None,
               only_categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Corre los checks pedidos. Sin gate entre checks (todos estáticos); los
    checks con dependencias ausentes van a SKIP con motivo."""
    out: List[Dict[str, Any]] = []
    for check_id, category, severity, fn, deps in CHECKS:
        if only_ids and check_id not in only_ids:
            continue
        if only_categories and category not in only_categories:
            continue
        rec = new_check(check_id, category, severity)
        missing = [d for d in deps if d in failures]
        if ctx is None or missing:
            reason = "; ".join(failures[d] for d in missing) if missing else \
                "; ".join(failures.values())
            out.append(skip_check(rec, reason or "dependencias no disponibles"))
            continue
        try:
            details, findings, dedup, evidence = fn(ctx)
        except Exception as exc:  # input malformado u otro: SKIP/WARN motivado, nunca traceback
            out.append(skip_check(rec, "no ejecutable: %s: %s" % (type(exc).__name__, exc)))
            continue
        rec["details"] = details
        rec["dedup_cites"] = dedup
        rec["evidence"] = evidence
        out.append(finish_check(rec, findings))
    return out


def run_suite(vault_root: str, only_ids: Optional[List[str]] = None,
              only_categories: Optional[List[str]] = None,
              write: bool = True, vault_root_arg: Optional[str] = None) -> Dict[str, Any]:
    """Corre la suite y devuelve el record machine-readable (spec sección 6).
    `write=True` es la única escritura permitida: results/run-<timestamp>.json."""
    ctx, failures = build_ctx(vault_root)
    results = run_checks(ctx, failures, only_ids, only_categories)
    findings_total = sum(len(r["findings"]) for r in results)
    counts = {"pass": 0, "fail": 0, "warn": 0, "skip": 0, "findings": findings_total}
    for r in results:
        counts[r["verdict"].lower()] = counts.get(r["verdict"].lower(), 0) + 1
    observations: List[str] = [
        "A8: fixtures sintéticas excluidas explícitamente del corpus (%s); iter_vault_md del harness no las excluye y .graphifyignore tampoco -> diferencia registrada (hallazgo de sistema, no auto-correctible)" % ", ".join(FIXTURE_REL_PREFIXES),
        "política de side-effects: los findings se registran; las correcciones canónicas son propuestas (recommended_action) para el owner; el motor no muta nada fuera de results/",
    ]
    if ctx is not None:
        observations.append("corpus vivo: %d notas (iter_vault_md - fixtures); mapa físico: %d notas .md" % (len(ctx.corpus), len(ctx.physical)))
        observations.append("clase A5 en vigor: no_vigente = memory_state {superseded, archived} U status {archived, superseded} dentro del enum por tipo; en retiro = status {deprecated, deprecating}")
    doc: Dict[str, Any] = {
        "run": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tool": TOOL,
        "git_head": git_head(vault_root) if vault_root else None,
        "vault_root_arg": vault_root_arg,
        "model": {
            "no_vigente": {"memory_state": list(NO_VIGENTE_MS), "status": list(NO_VIGENTE_ST)},
            "en_retiro": {"status": list(EN_RETIRO_ST)},
            "wikilink_resolution": "path-relativo(origen) > path VAULT_ROOT-relativo (regla 11) > basename exacto > casefold unico > alias exacto; ambiguo -> WARN",
            "hot_path_classes": "DEFAULT-LOADED / ROUTABLE / REFERENCED / ARCHIVED-NO-CORPUS (modelo P3-A seccion 3)",
            "semantic_duplication": "no existe como check: solo proxies CL-06/CL-07/CL-08 (modelo seccion 5)",
        },
        "checks": results,
        "counts": counts,
        "observations": observations,
        "ambiguities": list(DECLARED_AMBIGUITIES),
        "thresholds": dict(THRESHOLDS),
    }
    if write:
        os.makedirs(RESULTS_DIR, exist_ok=True)  # única escritura permitida
        ts = time.strftime("%Y%m%d-%H%M%S")
        out_path = os.path.join(RESULTS_DIR, "run-%s.json" % ts)
        n = 1
        while os.path.exists(out_path):
            n += 1
            out_path = os.path.join(RESULTS_DIR, "run-%s-%d.json" % (ts, n))
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
        # Ruta canónica relativa a VAULT_ROOT (regla 11); sólo en stdout.
        doc["results_file"] = "80-agents/tools/canonical-linter/results/" + os.path.basename(out_path)
    return doc


def human_summary(doc: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("=" * 72)
    lines.append("AGENTS-OS CANONICAL LINTER (P3)")
    lines.append("=" * 72)
    lines.append("run %s · vault: %s · git %s" % (
        doc["run"], doc.get("vault_root_arg") or "auto", (doc.get("git_head") or "?")[:9]))
    for r in doc["checks"]:
        n_find = len(r["findings"])
        extra = " (%d findings)" % n_find if n_find else ""
        lines.append("%s %s %s%s" % (r["check_id"].ljust(6, "."), r["category"].ljust(14), r["verdict"], extra))
    c = doc["counts"]
    lines.append("-" * 72)
    lines.append("counts: PASS %d · FAIL %d · WARN %d · SKIP %d · findings %d" % (
        c["pass"], c["fail"], c["warn"], c["skip"], c["findings"]))
    for r in doc["checks"]:
        if r["verdict"] == "FAIL":
            lines.append("FAIL %s: %s" % (r["check_id"], r["details"]))
    lines.append("=" * 72)
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="canonical_linter.py",
        description="AGENTS OS Canonical / Deprecation Linter (P3). Read-only salvo results/.")
    ap.add_argument("--vault-root", help="ruta del vault (default: autodetección por marker)")
    ap.add_argument("--json", action="store_true", help="JSON a stdout y results/run-<timestamp>.json; resumen a stderr")
    ap.add_argument("--check", help="corre un solo check CL por id (run dirigido por el operador)")
    ap.add_argument("--category", help="corre sólo los checks de una categoría (%s)" % ", ".join(CATEGORIES))
    args = ap.parse_args(argv)

    root = resolve_vault_root(args.vault_root)
    if root is None or not os.path.isfile(os.path.join(root, MARKER)):
        print("ERROR: no se pudo resolver VAULT_ROOT (carpeta que contiene %s). Usa --vault-root." % MARKER, file=sys.stderr)
        return 2
    only_ids = None
    if args.check:
        if args.check not in [c[0] for c in CHECKS]:
            print("ERROR: check desconocido: %s (validos: %s)" % (args.check, ", ".join(c[0] for c in CHECKS)), file=sys.stderr)
            return 2
        only_ids = [args.check]
    only_categories = None
    if args.category:
        if args.category not in CATEGORIES:
            print("ERROR: categoria desconocida: %s (validas: %s)" % (args.category, ", ".join(CATEGORIES)), file=sys.stderr)
            return 2
        only_categories = [args.category]

    doc = run_suite(root, only_ids, only_categories, write=True,
                    vault_root_arg=args.vault_root or "auto")
    if args.json:
        json.dump(doc, sys.stdout, indent=2, ensure_ascii=False)
        print()
        if doc.get("results_file"):
            print("[results] %s" % doc["results_file"], file=sys.stderr)
        print(human_summary(doc), file=sys.stderr)
    else:
        print(human_summary(doc))
        if doc.get("results_file"):
            print("[results] %s" % doc["results_file"])
    return 1 if doc["counts"].get("fail", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
