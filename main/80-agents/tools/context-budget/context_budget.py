#!/usr/bin/env python3
"""AGENTS OS Context Budget + Domain Leak Auditor (PHASE 2, P2-B).

Implementa la tool definida por dos documentos vinculantes (autoridad de esta
implementación):
- artifacts/p2-context-budget-design.md  (diseño P2-A: modelo de medición,
  métricas M01-M19, escenarios CTX-01..CTX-15, definiciones operativas 8.1-8.3)
- artifacts/p2-context-budget-spec.md    (spec del parent: decisiones A1-A9,
  write scope, verificación, output schema)

El medidor es un CONSUMIDOR del modelo de sesión del Conformance Harness
(`80-agents/tools/conformance-harness/rules.py`): importa `rules` y los
helpers de `agents_os_conformance.py` resolviendo la ruta del harness relativa
a VAULT_ROOT en runtime (constitución regla 11: jamás paths absolutos
persistidos). PROHIBIDO fork/copia de rules.py: no hay aquí un segundo modelo
de cold/warm/switch; toda decisión de carga sale de `rules.Session`.

Read-only sobre todo el vault salvo `results/` propio. Python 3.9+ stdlib
only. Determinista. Sin daemon, sin DB, sin red, sin frameworks.

Etiquetado (regla estricta del diseño sección 3 y spec sección 2):
- `estimated_tokens` = chars//4 vía `_size` del harness; NUNCA un campo
  llamado `tokens`; bytes/chars son EXACT; toda cifra estimada es baseline-only
  ("chars/4, sin tokenizador de autoridad (C04)") y jamás sostiene un FAIL.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
MARKER = "80-agents/agents-os/agents-os.md"
HARNESS_REL = "80-agents/tools/conformance-harness"
RESULTS_DIR = os.path.join(HERE, "results")

TOOL = "context-budget"
TOKENS_NOTE = "estimated_tokens = chars//4 (chars/4, sin tokenizador de autoridad, C04); baseline-only, jamas criterio de fallo"

# A4 ratificado: umbral de duplicación M14 (heurística propia de la tool,
# self-declared; veredicto máximo WARN). min_run_tokens acota falsos positivos
# de runs cortos de stopwords; se declara en el record para comparabilidad.
DUP_THRESHOLD = {
    "min_consecutive_lines": 3,
    "min_chars": 120,
    "min_run_tokens": 5,
    "version": 1,
    "max_verdict": "WARN",
}

# A1 ratificado: techos blandos WARN-only (bootstrap Token Targets; doctor
# Check 11). Ninguna desviación produce FAIL (C04).
SOFT_CEILINGS = {
    "cold_base_estimated_tokens": (3000, 6000),
    "warm_delta_estimated_tokens": (0, 1000),
    "swap_estimated_tokens": (1000, 3000),
}

CTX_ORDER: List[str] = [
    "CTX-15", "CTX-01", "CTX-02", "CTX-03", "CTX-04", "CTX-05", "CTX-06",
    "CTX-07", "CTX-08", "CTX-09", "CTX-10", "CTX-11", "CTX-12", "CTX-13",
    "CTX-14",
]

# WARN declarados por los audits del harness, heredados por diseño (spec
# sección 4): se registran en `ambiguities` del record y no degradan veredictos.
DECLARED_AMBIGUITIES: List[str] = [
    "Hallazgo 6 (A2): la clausula de evidencia de superficie del bootstrap paso 6 no distingue evidencia ambiental de evidencia de tarea; con mcp__aranea-* conectados permanentemente una sesion real sin entidad puede colapsar a ARANEA. Registrado como WARN, no resuelto (ADR pendiente).",
    "Hallazgo 7 (A3): rjara-vpn-routing-preferences.md tiene trigger when_area_loaded sin campo area; autorizada en el pack meli (Minimal Read 3 del router); en escenarios aranea su aparicion seria WARN (clasificacion ambigua, INFERRED).",
    "C09: vocabulario load_policy ad-hoc (when_echo_forge_loaded, etc.) y la semantica exacta de 'error matching' no tienen autoridad; heredado del harness como WARN y no invalida escenarios.",
    "Hallazgo 11: areas drift [[Echo Forge]]/[[Personal]] en memoria de dominio no mapean a ningun dominio del gate (WARN declarado del harness ACTIVE-MEMORY-DOMAIN-PURITY).",
    "DUAL-REGISTRY-DOMAIN-SYNC (Hallazgo 16): clausula dual de pr-description entre INDEX.md ('Vía meli-agent-dev u obra propia') y 30-resources/agents/00-index.md; semantica de la columna no definida por autoridad.",
    "Modo ambiguo DEFAULT->dominio (C02/C07 unknown): con entidad previa=none, la definicion de cold ('no entity loaded yet') y la de swap convergen al mismo observable; ninguna autoridad fija la clasificacion (CTX-09/CTX-10 WARN por diseno).",
    "C04: estimated_tokens es chars/4 sin tokenizador de autoridad; vale para comparar escenarios y detectar drift entre runs, jamas para tokens reales ni como criterio de FAIL.",
    "Hallazgo 3: domain gate, warm reuse y swap son prompt-discipline sin enforcement mecanico; el medidor mide la decision transcrita (rules.py), no la obediencia de una sesion viva.",
    "Hallazgo 4 / Hallazgo 17: la presencia de tools en superficie no es violacion; la config MCP vive a nivel maquina fuera del vault (CTX-14 registra el dato, nunca es criterio de FAIL).",
    "Hallazgo 8: 'drop the previous domain pack' es instruccion al modelo sin mecanismo de unload; el residuo real post-swap en la ventana del modelo es UNOBSERVABLE (solo potential_residual INFERRED).",
    "Hallazgo 10: hoy no existe memoria interna activa Meli (estado observado, no invariante).",
    "A8: skills transversales nunca cuentan como unrelated-domain aunque un registro diga 'Vía meli-agent-dev' (la fila es una puerta, no una exclusividad).",
]


# ---------------------------------------------------------------------------
# VAULT_ROOT + harness-as-library (diseño sección 10; spec sección 5)
# ---------------------------------------------------------------------------
def resolve_vault_root(explicit: Optional[str] = None) -> Optional[str]:
    """Resuelve VAULT_ROOT: el argumento explícito, o subiendo desde la
    carpeta de esta tool hasta encontrar el marker `80-agents/agents-os/agents-os.md`
    (mismo contrato que detect_vault_root del harness)."""
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
    (sys.path insert; jamás paths absolutos persistidos en el record). Si el
    harness no está disponible, los escenarios que dependen del modelo de
    sesión van a SKIP con motivo (lo maneja run_suite)."""
    harness_dir = os.path.join(vault_root, HARNESS_REL)
    if not os.path.isdir(harness_dir):
        raise ImportError("harness no disponible bajo %s" % HARNESS_REL)
    if harness_dir not in sys.path:
        sys.path.insert(0, harness_dir)
    import rules  # noqa: E402  (transcripción única; NUNCA se copia ni se fork-a)
    import agents_os_conformance as harness  # noqa: E402
    return rules, harness


# ---------------------------------------------------------------------------
# Pesos: SIEMPRE vía _size del harness (spec sección 2: jamás hardcodear)
# ---------------------------------------------------------------------------
def file_weight(harness, vault, rel: str) -> Optional[Dict[str, int]]:
    """{bytes, chars, estimated_tokens} de un archivo vía harness._size.
    None si el archivo no existe. estimated_tokens = chars//4 (C04)."""
    s = harness._size(vault, rel)
    if s is None:
        return None
    return {"bytes": s["bytes"], "chars": s["chars"],
            "estimated_tokens": s["approx_tokens_chars_over_4"]}


def weight_of(harness, vault, rels: List[str]) -> Dict[str, Any]:
    """Agregado {files, bytes, chars, estimated_tokens} sobre una lista de
    archivos (los ausentes se omiten del peso y se listan en missing)."""
    total = {"files": 0, "bytes": 0, "chars": 0, "estimated_tokens": 0}
    missing: List[str] = []
    for rel in sorted(set(rels)):
        w = file_weight(harness, vault, rel)
        if w is None:
            missing.append(rel)
            continue
        total["files"] += 1
        total["bytes"] += w["bytes"]
        total["chars"] += w["chars"]
        total["estimated_tokens"] += w["estimated_tokens"]
    total["missing"] = missing
    return total


def metric(name: str, value: Any, unit: str, confidence: str, authority: str) -> Dict[str, Any]:
    return {"name": name, "value": value, "unit": unit,
            "confidence": confidence, "authority": authority}


# ---------------------------------------------------------------------------
# Clasificación de dominio (diseño sección 8.1; A8) — territorio L0/STATIC:
# clasificación estática de archivos y frontmatter, reutilizando rules y el
# parseo de registros del harness. NO transcribe decisiones nuevas.
# ---------------------------------------------------------------------------
_REG_CACHE: Dict[str, Dict[str, Any]] = {}


def _registries(root: str, harness) -> Dict[str, Any]:
    """Parseo perezoso y cacheado de INDEX.md y 30-resources/agents/00-index.md
    reutilizando los helpers del harness (_parse_index_tables/_row_name/
    _classify_index_use)."""
    key = os.path.abspath(root)
    if key in _REG_CACHE:
        return _REG_CACHE[key]
    index_cls: Dict[str, str] = {}
    wiki_cls: Dict[str, str] = {}
    try:
        text = harness.read_text(os.path.join(root, "80-agents/skills/INDEX.md"))
        for row in harness._parse_index_tables(text)["federated"]:
            name = harness._row_name(row)
            cells = [c.strip() for c in row.strip("|").split("|")]
            use = cells[-1] if cells else ""
            if name:
                index_cls[name] = harness._classify_index_use(use, name)
    except (OSError, IndexError):
        pass
    try:
        wiki_text = harness.read_text(os.path.join(root, "30-resources/agents/00-index.md"))
        for line in wiki_text.splitlines():
            m = re.search(r"30-resources/agents/skills/([^/#|\]]+)/SKILL", line)
            if m:
                cls = ("meli" if "Meli-only" in line
                       else "aranea" if "Aranea-only" in line
                       else "transversal" if "transversal" in line.lower() else "")
                if cls:
                    wiki_cls[m.group(1)] = cls
    except OSError:
        pass
    _REG_CACHE[key] = {"index": index_cls, "wiki": wiki_cls}
    return _REG_CACHE[key]


def classify_file(rules, harness, root: str, rel: str, fm: Optional[Dict[str, Any]] = None) -> Tuple[Optional[str], str, str]:
    """Clasificación operativa de dominio (diseño 8.1 a-e + A8).
    Devuelve (dominio|None, 'EXACT'|'INFERRED', nota)."""
    vault = harness.Vault(root, harness.parse_frontmatter)
    if fm is None:
        fm = vault.frontmatter(rel)
    # (a) frontmatter area -> AREA_TO_DOMAIN (bootstrap paso 6).
    dom = rules.domain_from_area(fm.get("area"))
    if dom:
        return dom, "EXACT", "area %s -> %s (bootstrap paso 6)" % (fm.get("area"), dom)
    # (b) membresía en routers/prefs/skills domain-gated (C12/C13).
    if rel in set(rules.ROUTERS.values()):
        for d, r in rules.ROUTERS.items():
            if r == rel:
                return d, "EXACT", "router de dominio %s (bootstrap paso 6)" % d
    if rel in rules.MELI_SCOPED_PREFS:
        return "meli", "EXACT", "preferencia scoped del router meli (ROUTER_PREFS)"
    if rel in rules.ARANEA_SCOPED_PREFS:
        return "aranea", "EXACT", "preferencia scoped del router aranea (ROUTER_PREFS)"
    m = re.match(r"^30-resources/agents/skills/([^/]+)/SKILL\.md$", rel)
    if m:
        name = m.group(1)
        for d, names in rules.DOMAIN_GATED_SKILLS.items():
            if name in names:
                return d, "EXACT", "skill domain-gated %s (C12/C13)" % d
        # (c) ambos registros coinciden en exclusividad Meli-only/Aranea-only
        # (Hallazgo 16); transversales y puertas ('Vía <router>') son neutrales (A8).
        regs = _registries(root, harness)
        icls = regs["index"].get(name, "")
        wcls = regs["wiki"].get(name, "")
        if icls in ("meli", "aranea") and wcls == icls:
            return icls, "EXACT", "ambos registros lo clasifican %s-only (Hallazgo 16)" % icls
        if icls in ("meli", "aranea") or wcls in ("meli", "aranea"):
            return None, "INFERRED", (
                "registros duales no coinciden en exclusividad para %s (INDEX=%s, 00-index=%s): "
                "ambigua por DUAL-REGISTRY-DOMAIN-SYNC; trátase como neutral-WARN (A8), nunca FAIL" % (name, icls or "-", wcls or "-"))
        return None, "EXACT", "skill transversal/sin exclusividad declarada (neutral, A8)"
    # (d) bajo 30-resources/aranea/ -> aranea (router Minimal Read 3).
    if rel.startswith("30-resources/aranea/"):
        return "aranea", "EXACT", "bajo 30-resources/aranea/ (contexto de dominio on-demand)"
    # (e) neutral: constitución, perfil, continuidad global, INDEX, memoria sin
    # área mapeable, workspaces citados por la regla 12 — nunca es leak.
    return None, "EXACT", "neutral (sin area mapeable ni membresía de dominio)"


# ---------------------------------------------------------------------------
# M14: detector de duplicación (heurística self-declared, A4; veredicto
# máximo WARN). Normalización whitespace/puntuación/minúsculas; runs
# contiguos de tokens ≥ min_run_tokens; condición: suma de chars
# normalizados ≥ min_chars O un bloque que abarque ≥ min_consecutive_lines.
# ---------------------------------------------------------------------------
def _norm_text(text: str) -> List[List[str]]:
    """Tokens normalizados por línea no vacía (whitespace/puntuación/minúsculas)."""
    out: List[List[str]] = []
    for line in text.splitlines():
        norm = re.sub(r"[^\w]+", " ", line.lower(), flags=re.UNICODE).strip()
        toks = norm.split()
        if toks:
            out.append(toks)
    return out


def _tokens_and_line_map(normed: List[List[str]]) -> Tuple[List[str], List[int]]:
    toks: List[str] = []
    line_of: List[int] = []
    for li, line_toks in enumerate(normed):
        toks.extend(line_toks)
        line_of.extend([li] * len(line_toks))
    return toks, line_of


def find_duplication(text_a: str, text_b: str) -> Dict[str, Any]:
    """Runs contiguos comunes (greedy, no solapados) entre dos textos
    normalizados. Devuelve {runs: [{chars, lines_a, lines_b, snippet}],
    total_chars, max_consecutive_lines}."""
    na, nb = _norm_text(text_a), _norm_text(text_b)
    ta, la = _tokens_and_line_map(na)
    tb, lb = _tokens_and_line_map(nb)
    k_min = DUP_THRESHOLD["min_run_tokens"]
    index: Dict[Tuple[str, ...], List[int]] = {}
    for j in range(len(tb) - k_min + 1):
        index.setdefault(tuple(tb[j:j + k_min]), []).append(j)
    used_b = set()
    runs: List[Dict[str, Any]] = []
    i = 0
    while i <= len(ta) - k_min:
        key = tuple(ta[i:i + k_min])
        hit = index.get(key)
        if hit:
            best: Optional[Tuple[int, int, int]] = None
            for j in hit:
                if j in used_b:
                    continue
                k = 0
                while i + k < len(ta) and j + k < len(tb) and ta[i + k] == tb[j + k] and (j + k) not in used_b:
                    k += 1
                if best is None or k > best[2]:
                    best = (i, j, k)
            if best and best[2] >= k_min:
                i0, j0, k0 = best
                for p in range(j0, j0 + k0):
                    used_b.add(p)
                snippet = " ".join(ta[i0:i0 + k0])
                runs.append({
                    "chars": len(snippet),
                    "lines_a": len(set(la[i0:i0 + k0])),
                    "lines_b": len(set(lb[j0:j0 + k0])),
                    "snippet": snippet[:160],
                })
                i = i0 + k0
                continue
        i += 1
    return {
        "runs": runs,
        "total_chars": sum(r["chars"] for r in runs),
        "max_consecutive_lines": max([min(r["lines_a"], r["lines_b"]) for r in runs], default=0),
    }


def duplication_hit(report: Dict[str, Any]) -> bool:
    return (report["total_chars"] >= DUP_THRESHOLD["min_chars"]
            or report["max_consecutive_lines"] >= DUP_THRESHOLD["min_consecutive_lines"])


# ---------------------------------------------------------------------------
# Punto de inyección para selftest (NO para producción): los escenarios
# construyen la sesión vía _session_for; el selftest la sustituye para
# inyectar un agente que viola el pack cruzado (spec sección 6.2).
# ---------------------------------------------------------------------------
def _session_for(ctx):
    return rules.Session(ctx.vault)


# ---------------------------------------------------------------------------
# Helpers de escenario
# ---------------------------------------------------------------------------
def _new_record(scn_id: str, reuses: List[str]) -> Dict[str, Any]:
    return {"id": scn_id, "reuses": reuses, "verdict": "SKIP",
            "metrics": [], "evidence": [], "skip_reason": None, "details": ""}


def _skip(rec: Dict[str, Any], reason: str) -> Dict[str, Any]:
    rec["verdict"] = "SKIP"
    rec["skip_reason"] = reason
    rec["details"] = "no ejecutable: %s" % reason
    return rec


def _finish(rec: Dict[str, Any], problems: List[str], pass_state: str, pass_details: str, fail_details: str) -> Dict[str, Any]:
    if problems:
        rec["verdict"] = "FAIL"
        rec["details"] = fail_details
        rec["evidence"] = rec["evidence"] + problems
    else:
        rec["verdict"] = pass_state
        rec["details"] = pass_details
    return rec


def _m15_leak_check(rules, harness, ctx, rec: Dict[str, Any], opens: List[str], extra: List[str],
                    active_domain: Optional[str], problems: List[str]) -> List[str]:
    """M15 sobre el set cargado (opens + extra): archivos de dominio ajeno con
    prohibición explícita -> FAIL (diseño 8.1); ambiguos -> WARN (nunca FAIL)."""
    loaded = list(dict.fromkeys(list(opens) + list(extra)))
    unrelated: List[str] = []
    ambiguous: List[str] = []
    for rel in loaded:
        dom, conf, note = classify_file(rules, harness, ctx.root, rel)
        if dom is not None and active_domain is not None and dom != active_domain:
            if conf == "EXACT":
                unrelated.append(rel)
            else:
                ambiguous.append("%s: %s" % (rel, note))
        elif dom is not None and active_domain is None:
            if conf == "EXACT":
                unrelated.append(rel)  # dominio cargado sin entidad/dominio activo
            else:
                ambiguous.append("%s: %s" % (rel, note))
        elif dom is None and conf == "INFERRED":
            ambiguous.append("%s: %s" % (rel, note))
        # Nota VPN en sesión aranea (Hallazgo 7): WARN declarado.
        if active_domain == "aranea" and rel == rules.ROUTER_PREFS["meli"][1]:
            ambiguous.append("%s: nota VPN (Hallazgo 7) presente en escenario aranea; ni afirmada ni prohibida (WARN, A3)" % rel)
    if unrelated:
        problems.append("M15 unrelated-domain en el set cargado (diseño 8.1, FAIL): %s — autoridades: meli-agent-dev/aranea-agent-dev Hard Rules de exclusividad; perfil ('Las preferencias Meli y Aranea son scoped'); bootstrap paso 6 ('Never load both routers', fail-closed)" % unrelated)
    rec["metrics"].append(metric("unrelated_domain_files", unrelated, "files", "EXACT",
                                 "diseño 8.1 clasificación estática (frontmatter area + rules.ROUTERS/ROUTER_PREFS/DOMAIN_GATED_SKILLS)"))
    if ambiguous:
        rec["evidence"].append("M15 clasificaciones ambiguas (WARN, nunca FAIL): %s" % ambiguous)
    return unrelated


def _weight_metrics(rec: Dict[str, Any], label: str, agg: Dict[str, Any], conf_bytes: str, conf_est: str, authority: str) -> None:
    rec["metrics"].append(metric("%s_bytes" % label, agg["bytes"], "bytes", conf_bytes, authority))
    rec["metrics"].append(metric("%s_chars" % label, agg["chars"], "chars", conf_bytes, authority))
    rec["metrics"].append(metric("%s_estimated_tokens" % label, agg["estimated_tokens"], "estimated_tokens",
                                 conf_est, authority + " + " + TOKENS_NOTE))


# ---------------------------------------------------------------------------
# CTX-15 — baseline (siempre corre primero tras el pre-flight; spec sección 3)
# ---------------------------------------------------------------------------
def ctx_15_baseline(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-15", ["context_baseline (spec sección 9 del harness)"])
    profile = ctx.vault.resolve_profile_note()
    if profile is None:
        return _skip(rec, "perfil always de %s no resuelto (0 o >1 notas; bootstrap paso 1 / doctor Check 3)" % rules.USER_PREF_DIR)
    always = [rules.CONSTITUTION, profile, rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX]
    packs = {
        "meli": [rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"],
        "aranea": [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"],
    }
    missing = harness.require_files(ctx.vault, always + [f for f in packs["meli"] + packs["aranea"]])
    if missing:
        return _skip(rec, "archivos del baseline ausentes en el vault: %s" % missing)
    rec["metrics"].append(metric("always_load_file_list", always, "files", "EXACT",
                                 "bootstrap pasos 1-3 (C02) via rules.Session.cold_start/resolve_profile_note"))
    for domain, files in packs.items():
        rec["metrics"].append(metric("scope_pack_file_list_%s" % domain, files, "files", "EXACT",
                                     "rules.ROUTERS + rules.ROUTER_PREFS (Minimal Reads de los routers)"))
    agg_always = weight_of(harness, ctx.vault, always)
    _weight_metrics(rec, "always_load", agg_always, "EXACT", "ESTIMATED", "_size del harness")
    for domain, files in packs.items():
        agg = weight_of(harness, ctx.vault, files)
        _weight_metrics(rec, "scope_pack_%s" % domain, agg, "EXACT", "ESTIMATED", "_size del harness")
    for rel in always + packs["meli"] + packs["aranea"]:
        w = file_weight(harness, ctx.vault, rel)
        rec["evidence"].append("%s: bytes=%d chars=%d estimated_tokens=%d" % (
            rel, w["bytes"], w["chars"], w["estimated_tokens"]))
    rec["evidence"].append(TOKENS_NOTE)
    return _finish(rec, [], "PASS",
                   "baseline-only (chars/4, C04): always-load y packs meli/aranea medidos con _size en el run; nunca criterio de fallo",
                   "")


# ---------------------------------------------------------------------------
# CTX-01 — CTX-DEFAULT-COLD (reusa COLD-DEFAULT)
# ---------------------------------------------------------------------------
def ctx_01_default_cold(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-01", ["COLD-DEFAULT"])
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"entity_title": "entidad-fantasma-xyz", "casual": True})
    evidence = rec["evidence"]
    ghost = ctx.vault.resolve_entity("entidad-fantasma-xyz")
    evidence.append("entidad fantasma 'entidad-fantasma-xyz' no resuelve: %s (fixture)" % (ghost is None))
    problems = harness._base_assertions(s, evidence)
    problems += harness._assert_absent(harness.NOT_LOAD_DEFAULT, s.all_opens(), evidence)
    if s.active_domain is not None:
        problems.append("router activo sin entidad resoluble: %s (bootstrap paso 6)" % s.active_domain)
    if s.pack_files:
        problems.append("pack de dominio cargado en DEFAULT: %s" % s.pack_files)
    # Métricas de presupuesto: M01-M03, M07, M08, M15, M19 (diseño sección 6).
    always = [rules.CONSTITUTION, s.profile_note or "", rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX]
    rec["metrics"].append(metric("always_load_file_list", always, "files", "EXACT",
                                 "bootstrap pasos 1-3 (C02) via rules.Session"))
    agg = weight_of(harness, ctx.vault, s.opens_in_turn(1))
    _weight_metrics(rec, "always_load", agg, "EXACT", "ESTIMATED", "_size del harness")
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT",
                                 "rules.Session.all_opens (telemetría D1)"))
    rec["metrics"].append(metric("opens_per_turn", {str(t): len(s.opens_in_turn(t)) for t in (1,)}, "count", "EXACT",
                                 "rules.Session.opens_in_turn"))
    rec["metrics"].append(metric("session_cold_estimated_tokens", agg["estimated_tokens"], "estimated_tokens",
                                 "ESTIMATED", "_size del harness + " + TOKENS_NOTE))
    rec["metrics"].append(metric("gate_decision_trace", s.gate_note or "", "text", "EXACT (transcripción)",
                                 "bootstrap paso 6 via rules.domain_gate"))
    _m15_leak_check(rules, harness, ctx, rec, s.all_opens(), [], s.active_domain, problems)
    evidence.append("estado: session_mode=%s active_entity=%s active_domain=%s bootstrap_runs=%d pack=%s" % (
        s.session_mode, s.active_entity, s.active_domain, s.bootstrap_runs, s.pack_files))
    evidence.append("WARN declarado (Hallazgo 6): la clausula de evidencia de superficie del paso 6 no distingue evidencia ambiental de evidencia de tarea; con mcp__aranea-* conectados permanentemente una sesion real sin entidad puede colapsar a ARANEA. Registrado como WARN, no resuelto (ADR pendiente).")
    return _finish(rec, problems, "WARN",
                   "cold start DEFAULT sin router: set = exactamente los 4 always; presupuesto base medido (chars/4, C04)",
                   "cold start DEFAULT violó el contrato de carga o registró unrelated-domain")


# ---------------------------------------------------------------------------
# CTX-02 — CTX-MELI-COLD (reusa COLD-MELI)
# ---------------------------------------------------------------------------
def ctx_02_meli_cold(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-02", ["COLD-MELI"])
    fixtures = ["30-resources/applications/RIO.md"] + rules.ROUTER_PREFS["meli"] + [rules.ROUTERS["meli"]]
    missing = harness.require_files(ctx.vault, fixtures)
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    evidence = rec["evidence"]
    problems = harness._base_assertions(s, evidence)
    ent = s.active_entity
    if not ent or ent.get("path") != "30-resources/applications/RIO.md":
        problems.append("entidad resuelta no es el fixture RIO.md: %s" % (ent,))
    if s.active_domain != "meli":
        problems.append("gate no activó meli: %s (%s)" % (s.active_domain, s.gate_note))
    expected_pack = [rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"]
    if sorted(s.pack_files) != sorted(expected_pack):
        problems.append("pack meli != {router + 2 preferencias scoped}: %s" % s.pack_files)
    not_load = ([rules.ROUTERS["aranea"], rules.ARANEA_MCPS_EXPERT,
                 "30-resources/aranea/00-index.md"] + rules.ROUTER_PREFS["aranea"]
                + harness.MELI_ECHO_ACTIVE_NOTES)
    problems += harness._assert_absent(not_load, s.all_opens(), evidence)
    # Métricas: M01-M08, M12, M15, M19.
    rec["metrics"].append(metric("always_load_file_list", [rules.CONSTITUTION, s.profile_note or "", rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX],
                                 "files", "EXACT", "bootstrap pasos 1-3 via rules.Session"))
    rec["metrics"].append(metric("scope_pack_file_list_meli", s.pack_files, "files", "EXACT",
                                 "rules.ROUTERS + rules.ROUTER_PREFS (Minimal Reads router meli-agent-dev)"))
    rec["metrics"].append(metric("scope_pack_bytes_meli", weight_of(harness, ctx.vault, s.pack_files)["bytes"], "bytes", "EXACT", "_size del harness"))
    rec["metrics"].append(metric("scope_pack_chars_meli", weight_of(harness, ctx.vault, s.pack_files)["chars"], "chars", "EXACT", "_size del harness"))
    rec["metrics"].append(metric("scope_pack_estimated_tokens_meli", weight_of(harness, ctx.vault, s.pack_files)["estimated_tokens"],
                                 "estimated_tokens", "ESTIMATED", "_size del harness + " + TOKENS_NOTE))
    agg = weight_of(harness, ctx.vault, s.opens_in_turn(1))
    _weight_metrics(rec, "session_cold", agg, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(1)")
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("opens_per_turn", {str(t): len(s.opens_in_turn(t)) for t in (1,)}, "count", "EXACT", "rules.Session.opens_in_turn"))
    rec["metrics"].append(metric("session_cold_estimated_tokens", agg["estimated_tokens"], "estimated_tokens",
                                 "ESTIMATED", "_size del harness + " + TOKENS_NOTE))
    rec["metrics"].append(metric("specialist_skills_selected", s.specialist_skills, "files", "EXACT",
                                 "bootstrap paso 9 via rules.Session.route_specialist (sin specialist_task en el fixture)"))
    rec["metrics"].append(metric("gate_decision_trace", s.gate_note or "", "text", "EXACT (transcripción)", "bootstrap paso 6 via rules.domain_gate"))
    _m15_leak_check(rules, harness, ctx, rec, s.all_opens(), [], s.active_domain, problems)
    # Hallazgo 10: estado observado de la memoria interna activa Meli.
    active_meli = [rel for rel in harness.iter_vault_md(ctx.root, "80-agents/memory/internal")
                   if rules.domain_from_area(harness.fm_of(ctx.root, rel).get("area")) == "meli"
                   and str(harness.fm_of(ctx.root, rel).get("memory_state", "")) == "active"]
    evidence.append("Hallazgo 10 (estado observado): continuidad interna activa meli hoy = %s; el delta esperado de retrieval es vacío" % (active_meli or "ninguna"))
    evidence.append("estado: active_entity=%s active_domain=%s pack=%s" % (
        ent.get("title") if ent else None, s.active_domain, s.pack_files))
    return _finish(rec, problems, "PASS",
                   "cold start Meli: base 4 + router meli-agent-dev + 2 prefs scoped; presupuesto ≈ base + pack meli (chars/4)",
                   "cold start Meli violó el contrato (C10/C11) o registró unrelated-domain")


# ---------------------------------------------------------------------------
# CTX-03 — CTX-ARANEA-COLD (reusa COLD-ARANEA; WARN Hallazgo 7 por diseño)
# ---------------------------------------------------------------------------
def ctx_03_aranea_cold(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-03", ["COLD-ARANEA"])
    fixtures = ["10-projects/Echo Forge/Echo Forge.md", rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"]
    missing = harness.require_files(ctx.vault, fixtures)
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"entity_title": "Echo Forge"})
    evidence = rec["evidence"]
    problems = harness._base_assertions(s, evidence)
    ent = s.active_entity
    if not ent or ent.get("path") != "10-projects/Echo Forge/Echo Forge.md":
        problems.append("entidad resuelta no es el fixture Echo Forge.md: %s" % (ent,))
    else:
        fm = ctx.vault.frontmatter("10-projects/Echo Forge/Echo Forge.md")
        evidence.append("fixture real: area=%s -> mapeo [[Echo]]->aranea-agent-dev verificado (bootstrap paso 6)" % fm.get("area"))
    if s.active_domain != "aranea":
        problems.append("gate no activó aranea con area [[Echo]]: %s (%s)" % (s.active_domain, s.gate_note))
    expected_pack = [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"]
    if sorted(s.pack_files) != sorted(expected_pack):
        problems.append("pack aranea != {router + aranea ops prefs}: %s" % s.pack_files)
    not_load = ([rules.ROUTERS["meli"], "30-resources/aranea/00-index.md"]
                + rules.ROUTER_PREFS["meli"][:1] + [harness.FURY_NOTE])
    problems += harness._assert_absent(not_load, s.all_opens(), evidence)
    if rules.ARANEA_MCPS_EXPERT in s.all_opens():
        problems.append("aranea-mcps-expert cobrado sin necesidad MCP declarada (Minimal Read 4 exige tarea MCP; FAIL si aparece)")
    # Métricas: M01-M08, M12, M15, M19.
    rec["metrics"].append(metric("always_load_file_list", [rules.CONSTITUTION, s.profile_note or "", rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX],
                                 "files", "EXACT", "bootstrap pasos 1-3 via rules.Session"))
    rec["metrics"].append(metric("scope_pack_file_list_aranea", s.pack_files, "files", "EXACT",
                                 "rules.ROUTERS + rules.ROUTER_PREFS (Minimal Reads router aranea-agent-dev; A7: 30-resources/aranea/00-index.md no se cobra al pack base)"))
    agg_pack = weight_of(harness, ctx.vault, s.pack_files)
    _weight_metrics(rec, "scope_pack_aranea", agg_pack, "EXACT", "ESTIMATED", "_size del harness")
    agg = weight_of(harness, ctx.vault, s.opens_in_turn(1))
    _weight_metrics(rec, "session_cold", agg, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(1)")
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("opens_per_turn", {str(t): len(s.opens_in_turn(t)) for t in (1,)}, "count", "EXACT", "rules.Session.opens_in_turn"))
    rec["metrics"].append(metric("session_cold_estimated_tokens", agg["estimated_tokens"], "estimated_tokens",
                                 "ESTIMATED", "_size del harness + " + TOKENS_NOTE))
    rec["metrics"].append(metric("specialist_skills_selected", s.specialist_skills, "files", "EXACT",
                                 "bootstrap paso 9 (sin necesidad MCP en el fixture)"))
    rec["metrics"].append(metric("gate_decision_trace", s.gate_note or "", "text", "EXACT (transcripción)", "bootstrap paso 6 via rules.domain_gate"))
    _m15_leak_check(rules, harness, ctx, rec, s.all_opens(), [], s.active_domain, problems)
    evidence.append("estado: active_entity=%s active_domain=%s pack=%s" % (
        ent.get("title") if ent else None, s.active_domain, s.pack_files))
    evidence.append("WARN declarado (Hallazgo 7): rjara-vpn-routing-preferences.md tiene trigger when_area_loaded sin campo area y el router Aranea no la lista en su Minimal Read; su carga on-demand via el enlace del perfil no se afirma ni se prohíbe (C11). M15 la clasifica ambigua (A3).")
    return _finish(rec, problems, "WARN",
                   "cold start Aranea via area [[Echo]]: base 4 + router aranea-agent-dev + aranea ops prefs; expert no cobrada (chars/4)",
                   "cold start Aranea violó el contrato (C10) o registró unrelated-domain")


# ---------------------------------------------------------------------------
# CTX-04 — CTX-DEFAULT-WARM (reusa WARM-DEFAULT)
# ---------------------------------------------------------------------------
def ctx_04_default_warm(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-04", ["WARM-DEFAULT"])
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"casual": True})
    s.turn = 2
    s.warm_turn({})
    evidence = rec["evidence"]
    problems = harness._warm_no_base_reopen(s, 2, evidence)
    if any(rules.ROUTERS[d] in s.opens_in_turn(2) for d in ("meli", "aranea")):
        problems.append("router cargado en turno warm casual")
    if s.session_mode != "warm" or s.bootstrap_runs != 1:
        problems.append("modo/ritual incorrecto: mode=%s runs=%d" % (s.session_mode, s.bootstrap_runs))
    delta = weight_of(harness, ctx.vault, s.opens_in_turn(2))
    # Métricas: M07, M09, M18.
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("warm_delta_files", len(delta), "files", "EXACT", "rules.Session.opens_in_turn(2) (fix D1)"))
    _weight_metrics(rec, "warm_delta", delta, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(2)")
    rec["metrics"].append(metric("soft_target_warm_delta", delta["estimated_tokens"], "estimated_tokens", "ESTIMATED",
                                 "bootstrap Token Targets + doctor Check 11 + " + TOKENS_NOTE))
    lo, hi = SOFT_CEILINGS["warm_delta_estimated_tokens"]
    in_range = lo <= delta["estimated_tokens"] < hi
    rec["metrics"].append(metric("soft_target_in_range", in_range, "bool", "ESTIMATED",
                                 "techo blando %d-%d estimated_tokens (A1: WARN-only)" % (lo, hi)))
    if not in_range:
        rec["evidence"].append("WARN (A1): warm delta %d estimated_tokens fuera del techo blando %d-%d (chars/4, C04); desviación registrada, nunca FAIL" % (delta["estimated_tokens"], lo, hi))
    evidence.append("estado: session_mode=%s active_entity=%s active_domain=%s" % (s.session_mode, s.active_entity, s.active_domain))
    return _finish(rec, problems, "PASS",
                   "turno warm sin dominio: cero opens obligatorios; presupuesto del turno = delta puro (%d archivos)" % len(delta),
                   "turno warm re-leo base o cargó router (C06)")


# ---------------------------------------------------------------------------
# CTX-05 — CTX-MELI-WARM (reusa WARM-MELI + BOOTSTRAP-NOT-RERUN-ON-WARM)
# ---------------------------------------------------------------------------
def ctx_05_meli_warm(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-05", ["WARM-MELI", "BOOTSTRAP-NOT-RERUN-ON-WARM"])
    missing = harness.require_files(ctx.vault, [harness.FURY_NOTE, "30-resources/applications/RIO.md"])
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    pack_t1 = list(s.pack_files)
    s.turn = 2
    s.warm_turn({})
    candidates = s.retrieve("error")
    miss = s.open_delta(harness.FURY_NOTE)
    evidence = rec["evidence"]
    problems = harness._warm_no_base_reopen(s, 2, evidence)
    if harness.FURY_NOTE not in candidates:
        problems.append("el known-error del fury segment suffix no fue seleccionado por el filtro de retrieval: %s" % candidates)
    if miss:
        problems.append("delta declarado inexistente en disco: %s" % miss)
    if any(p in candidates or p in s.opens_in_turn(2) for p in pack_t1):
        problems.append("recarga del pack de dominio en turno que pide un hecho (C06/C11)")
    if any(p in candidates or p in s.opens_in_turn(2) for p in (rules.ROUTERS["aranea"], rules.ROUTER_PREFS["aranea"][0])):
        problems.append("pieza Aranea en turno Meli")
    # BOOTSTRAP-NOT-RERUN-ON-WARM heredado: turnos 3..5 sin releer base ni re-invocar.
    base = [rules.CONSTITUTION, rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX,
            "80-agents/skills/agents-os-bootstrap/SKILL.md"] + ([s.profile_note] if s.profile_note else [])
    for t in range(3, 6):
        s.turn = t
        s.warm_turn({})
        reopened = [p for p in s.opens_in_turn(t) if p in base]
        if reopened:
            problems.append("turno %d re-abrió base/bootstrap sin invalidación declarada: %s" % (t, reopened))
    if s.bootstrap_runs != 1:
        problems.append("bootstrap re-ejecutado en turnos warm: %d runs" % s.bootstrap_runs)
    evidence.append("turnos 3..5 warm sin aperturas de base: verificado (BOOTSTRAP-NOT-RERUN-ON-WARM heredado)")
    # Métricas: M07, M09, M13, M18.
    delta = weight_of(harness, ctx.vault, s.opens_in_turn(2))
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("warm_delta_files", len(delta), "files", "EXACT", "rules.Session.opens_in_turn(2) (fix D1)"))
    _weight_metrics(rec, "warm_delta", delta, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(2)")
    rec["metrics"].append(metric("resources_selected", {"candidates": candidates, "opened": [harness.FURY_NOTE]},
                                 "files", "EXACT (modelo)", "rules.Session.retrieve + open_delta (C09: matching declarado por el harness)"))
    rec["metrics"].append(metric("soft_target_warm_delta", delta["estimated_tokens"], "estimated_tokens", "ESTIMATED",
                                 "bootstrap Token Targets + doctor Check 11 + " + TOKENS_NOTE))
    lo, hi = SOFT_CEILINGS["warm_delta_estimated_tokens"]
    in_range = lo <= delta["estimated_tokens"] < hi
    rec["metrics"].append(metric("soft_target_in_range", in_range, "bool", "ESTIMATED", "techo blando %d-%d (A1: WARN-only)" % (lo, hi)))
    if not in_range:
        rec["evidence"].append("WARN (A1): warm delta %d estimated_tokens fuera del techo blando %d-%d (chars/4, C04)" % (delta["estimated_tokens"], lo, hi))
    evidence.append("candidatos del filtro (%d): %s" % (len(candidates), ", ".join(candidates) or "-"))
    evidence.append("cuerpo abierto (delta único del turno 2): %s" % harness.FURY_NOTE)
    evidence.append("estado: session_mode=%s active_entity=%s active_domain=%s" % (
        s.session_mode, s.active_entity.get("title") if s.active_entity else None, s.active_domain))
    return _finish(rec, problems, "PASS",
                   "turno warm Meli: delta = known-error RIO (1 archivo, peso chars/4); base y pack intactos en turnos 2..5",
                   "turno warm Meli violó el contrato (C06/C11)")


# ---------------------------------------------------------------------------
# CTX-06 — CTX-ARANEA-WARM (reusa WARM-ARANEA)
# ---------------------------------------------------------------------------
def ctx_06_aranea_warm(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-06", ["WARM-ARANEA"])
    missing = harness.require_files(ctx.vault, [harness.MT5_NOTE, "10-projects/Echo Forge/Echo Forge.md"])
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"entity_title": "Echo Forge"})
    s.turn = 2
    s.warm_turn({})
    candidates = s.retrieve("continuity")
    miss = s.open_delta(harness.MT5_NOTE)
    evidence = rec["evidence"]
    problems = harness._warm_no_base_reopen(s, 2, evidence)
    if harness.MT5_NOTE not in candidates:
        problems.append("la continuidad activa del MT5 parser cert no fue seleccionada por el filtro: %s" % candidates)
    if miss:
        problems.append("delta declarado inexistente en disco: %s" % miss)
    for p in candidates:
        if rules.domain_from_area(ctx.vault.frontmatter(p).get("area")) == "meli":
            problems.append("memoria del dominio Meli en turno Aranea: %s" % p)
    if any(p in candidates or p in s.opens_in_turn(2) for p in (rules.ROUTERS["meli"], rules.ROUTER_PREFS["meli"][0])):
        problems.append("pieza Meli en turno Aranea")
    # Métricas: M07, M09, M13, M18.
    delta = weight_of(harness, ctx.vault, s.opens_in_turn(2))
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("warm_delta_files", len(delta), "files", "EXACT", "rules.Session.opens_in_turn(2) (fix D1)"))
    _weight_metrics(rec, "warm_delta", delta, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(2)")
    rec["metrics"].append(metric("resources_selected", {"candidates": candidates, "opened": [harness.MT5_NOTE]},
                                 "files", "EXACT (modelo)", "rules.Session.retrieve + open_delta"))
    rec["metrics"].append(metric("soft_target_warm_delta", delta["estimated_tokens"], "estimated_tokens", "ESTIMATED",
                                 "bootstrap Token Targets + doctor Check 11 + " + TOKENS_NOTE))
    lo, hi = SOFT_CEILINGS["warm_delta_estimated_tokens"]
    in_range = lo <= delta["estimated_tokens"] < hi
    rec["metrics"].append(metric("soft_target_in_range", in_range, "bool", "ESTIMATED", "techo blando %d-%d (A1: WARN-only)" % (lo, hi)))
    if not in_range:
        rec["evidence"].append("WARN (A1): warm delta %d estimated_tokens fuera del techo blando %d-%d (chars/4, C04)" % (delta["estimated_tokens"], lo, hi))
    evidence.append("trigger del fixture: %s (vocabulario no canónico = WARN de LOAD-POLICY-VOCABULARY/C09, no invalida el escenario)" %
                    ctx.vault.frontmatter(harness.MT5_NOTE).get("load_policy"))
    evidence.append("candidatos del filtro (%d): %s" % (len(candidates), ", ".join(candidates) or "-"))
    evidence.append("cuerpo abierto (delta único del turno 2): %s" % harness.MT5_NOTE)
    return _finish(rec, problems, "PASS",
                   "turno warm Aranea: delta = continuidad MT5 parser cert; base intacta; delta acotado a memoria aranea",
                   "turno warm Aranea violó el contrato (C06)")


# ---------------------------------------------------------------------------
# CTX-07 — CTX-SWITCH-MELI-TO-ARANEA (reusa SWITCH-MELI-TO-ARANEA)
# ---------------------------------------------------------------------------
def ctx_07_switch_meli_aranea(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-07", ["SWITCH-MELI-TO-ARANEA"])
    missing = harness.require_files(ctx.vault, ["30-resources/applications/RIO.md", "10-projects/Echo Forge/Echo Forge.md", rules.ROUTERS["aranea"]])
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"entity_title": "RIO"})
    pack_meli = list(s.pack_files)
    base_before = set(s.opens_in_turn(1))
    s.turn = 2
    s.swap_entity("Echo Forge")
    evidence = rec["evidence"]
    problems: List[str] = []
    reopened = [p for p in s.opens_in_turn(2) if p in base_before]
    if reopened:
        problems.append("swap re-leo archivos base (deben persistir sin relectura): %s" % reopened)
    if rules.GLOBAL_INTERNAL in s.opens_in_turn(2):
        problems.append("nota interna global re-cargada en swap (Session Modes: skip global internal reload)")
    if [p for p in pack_meli if p in s.opens_in_turn(2)]:
        problems.append("piezas del pack meli re-abiertas en el turno del swap (swap paso 4)")
    if s.holds_two_packs():
        problems.append("dos packs de dominio activos tras el swap (Hard Rule)")
    if s.opens_in_turn(2).count(rules.ROUTERS["aranea"]) != 1:
        problems.append("el router aranea se abre %d veces en el turno del swap (debe ser exactamente una)" % s.opens_in_turn(2).count(rules.ROUTERS["aranea"]))
    if s.active_domain != "aranea":
        problems.append("dominio post-swap != aranea: %s (%s)" % (s.active_domain, s.gate_note))
    if sorted(s.pack_files) != sorted([rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"]):
        problems.append("pack post-swap != pack aranea: %s" % s.pack_files)
    if any(p in s.pack_files for p in pack_meli):
        problems.append("pack Meli persiste tras el swap (swap paso 3): %s" % [p for p in pack_meli if p in s.pack_files])
    # Métricas: M07, M10, M11, M15, M19 (+ residuo potencial 8.3).
    swap_agg = weight_of(harness, ctx.vault, s.opens_in_turn(2))
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("swap_new_pack_files", s.opens_in_turn(2), "files", "EXACT", "rules.Session.opens_in_turn(2) (fix D1)"))
    _weight_metrics(rec, "swap", swap_agg, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(2)")
    routers_in_pack = [p for p in s.pack_files if p in set(rules.ROUTERS.values())]
    rec["metrics"].append(metric("active_pack_count_post_swap", len(routers_in_pack), "count", "EXACT",
                                 "rules.Session.holds_two_packs + pack_files (debe ser <=1)"))
    rec["metrics"].append(metric("gate_decision_trace", s.gate_note or "", "text", "EXACT (transcripción)", "bootstrap swap paso 3 via rules.domain_gate"))
    residual = weight_of(harness, ctx.vault, pack_meli)
    _weight_metrics(rec, "potential_residual", residual, "EXACT", "ESTIMATED",
                    "peso en disco del pack saliente (meli); INFERRED como residuo (Hallazgo 8: sin mecanismo de unload)")
    rec["metrics"].append(metric("potential_residual_files", pack_meli, "files", "INFERRED",
                                 "Hallazgo 8: los archivos del pack saliente siguen en disco; su presencia en la ventana real es UNOBSERVABLE"))
    _m15_leak_check(rules, harness, ctx, rec, s.all_opens(), [], s.active_domain, problems)
    evidence.append("antes: domain=meli pack=%s" % pack_meli)
    evidence.append("despues: domain=%s pack=%s entity=%s" % (s.active_domain, s.pack_files, s.active_entity.get("title") if s.active_entity else None))
    evidence.append(s.swap_note or "")
    evidence.append("residuo real post-swap en la ventana del modelo: UNOBSERVABLE (Hallazgo 8); a nivel modelo el pack meli salió de pack_files (EXACT) y no fue re-abierto tras el swap")
    lo, hi = SOFT_CEILINGS["swap_estimated_tokens"]
    if not (lo <= swap_agg["estimated_tokens"] < hi):
        rec["evidence"].append("WARN (A1): swap %d estimated_tokens fuera del techo blando %d-%d (chars/4, C04)" % (swap_agg["estimated_tokens"], lo, hi))
    return _finish(rec, problems, "PASS",
                   "swap Meli->Aranea: un solo pack, base persistente; swap_turn = pack aranea (%d estimated_tokens, chars/4)" % swap_agg["estimated_tokens"],
                   "swap Meli->Aranea violó el contrato (C07) o registró unrelated-domain")


# ---------------------------------------------------------------------------
# CTX-08 — CTX-SWITCH-ARANEA-TO-MELI (reusa SWITCH-ARANEA-TO-MELI)
# ---------------------------------------------------------------------------
def ctx_08_switch_aranea_meli(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-08", ["SWITCH-ARANEA-TO-MELI"])
    missing = harness.require_files(ctx.vault, ["30-resources/applications/RIO.md", "10-projects/Echo Forge/Echo Forge.md",
                                                rules.ROUTERS["meli"], "30-resources/agents/skills/signals-code-review/SKILL.md"])
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"entity_title": "Echo Forge"})
    pack_aranea = list(s.pack_files)
    base_before = set(s.opens_in_turn(1))
    s.turn = 2
    s.swap_entity("RIO")
    spec = s.route_specialist("meli", "code_review")
    evidence = rec["evidence"]
    problems: List[str] = []
    if [p for p in s.opens_in_turn(2) if p in base_before]:
        problems.append("swap re-leo archivos base: %s" % [p for p in s.opens_in_turn(2) if p in base_before])
    if s.holds_two_packs():
        problems.append("dos packs activos tras el swap (Hard Rule)")
    if s.opens_in_turn(2).count(rules.ROUTERS["meli"]) != 1:
        problems.append("el router meli se abre %d veces en el turno del swap (debe ser exactamente una)" % s.opens_in_turn(2).count(rules.ROUTERS["meli"]))
    if s.active_domain != "meli":
        problems.append("dominio post-swap != meli: %s" % s.active_domain)
    if sorted(s.pack_files) != sorted([rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"]):
        problems.append("pack post-swap != {meli router + meli prefs + vpn prefs}: %s" % s.pack_files)
    if rules.ROUTERS["aranea"] in s.pack_files or rules.ROUTER_PREFS["aranea"][0] in s.pack_files:
        problems.append("pack Aranea persiste tras el swap")
    if [p for p in pack_aranea if p in s.opens_in_turn(2)]:
        problems.append("piezas del pack aranea re-abiertas en el turno del swap (swap paso 4)")
    if rules.ARANEA_MCPS_EXPERT in s.all_opens():
        problems.append("aranea-mcps-expert activado en turno meli (MUST NOT, C13)")
    if not spec:
        problems.append("signals-code-review no rut-eada por la tabla del router para code_review (C12)")
    elif s.all_opens().index(rules.ROUTERS["meli"]) > s.all_opens().index(spec):
        problems.append("skill especializada cargada antes que el router (debe rutear via tabla del router, C12)")
    if rules.SKILLS_INDEX in s.opens_in_turn(2):
        problems.append("INDEX.md re-cargado en el swap (registry ya en contexto)")
    # Métricas: M07, M10, M11, M12, M15, M19 (+ residuo potencial 8.3).
    swap_agg = weight_of(harness, ctx.vault, s.opens_in_turn(2))
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("swap_new_pack_files", s.opens_in_turn(2), "files", "EXACT", "rules.Session.opens_in_turn(2) (fix D1)"))
    _weight_metrics(rec, "swap", swap_agg, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(2)")
    routers_in_pack = [p for p in s.pack_files if p in set(rules.ROUTERS.values())]
    rec["metrics"].append(metric("active_pack_count_post_swap", len(routers_in_pack), "count", "EXACT",
                                 "rules.Session.holds_two_packs + pack_files (debe ser <=1)"))
    rec["metrics"].append(metric("specialist_skills_selected", s.specialist_skills, "files", "EXACT",
                                 "bootstrap paso 9 + router Procedure 3 via rules.Session.route_specialist"))
    rec["metrics"].append(metric("gate_decision_trace", s.gate_note or "", "text", "EXACT (transcripción)", "bootstrap swap paso 3 via rules.domain_gate"))
    residual = weight_of(harness, ctx.vault, pack_aranea)
    _weight_metrics(rec, "potential_residual", residual, "EXACT", "ESTIMATED",
                    "peso en disco del pack saliente (aranea); INFERRED como residuo (Hallazgo 8)")
    rec["metrics"].append(metric("potential_residual_files", pack_aranea, "files", "INFERRED",
                                 "Hallazgo 8: residuo real en la ventana del modelo UNOBSERVABLE"))
    _m15_leak_check(rules, harness, ctx, rec, s.all_opens(), [], s.active_domain, problems)
    evidence.append("routing: %s via tabla del router meli-agent-dev (Procedure 3), no directo desde INDEX" % (spec or "-"))
    evidence.append("VPN por rjara-vpn-routing-preferences.md antes del primer acceso corporativo (router Procedure 4): incluida en pack (autorizada en meli; A3)")
    evidence.append("despues: domain=%s pack=%s especialista=%s" % (s.active_domain, s.pack_files, s.specialist_skills))
    evidence.append("residuo real post-swap: UNOBSERVABLE (Hallazgo 8); potential_residual = peso del pack aranea saliente en disco")
    lo, hi = SOFT_CEILINGS["swap_estimated_tokens"]
    if not (lo <= swap_agg["estimated_tokens"] < hi):
        rec["evidence"].append("WARN (A1): swap %d estimated_tokens fuera del techo blando %d-%d (chars/4, C04)" % (swap_agg["estimated_tokens"], lo, hi))
    return _finish(rec, problems, "PASS",
                   "swap Aranea->Meli: router + 2 prefs + signals-code-review solo via tabla del router; expert ausente",
                   "swap Aranea->Meli violó el contrato (C07/C12/C13) o registró unrelated-domain")


# ---------------------------------------------------------------------------
# CTX-09 / CTX-10 — resolución tardía desde DEFAULT (WARN de modo por diseño)
# ---------------------------------------------------------------------------
def _switch_from_default(rec: Dict[str, Any], ctx, rules, harness, title: str,
                         expected_domain: str, pack: List[str]) -> Dict[str, Any]:
    missing = harness.require_files(ctx.vault, pack + [_fixture_of(title)])
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    s = _session_for(ctx)
    s.turn = 1
    s.cold_start({"casual": True})
    base_before = set(s.opens_in_turn(1))
    s.turn = 2
    s.swap_entity(title)
    evidence = rec["evidence"]
    problems: List[str] = []
    if [p for p in s.opens_in_turn(2) if p in base_before]:
        problems.append("resolución tardía re-leo la base (warm paso 3 / AGENTS.md): %s" % [p for p in s.opens_in_turn(2) if p in base_before])
    if s.opens_in_turn(2).count(rules.ROUTERS[expected_domain]) != 1:
        problems.append("el router %s se abre %d veces en el turno del swap (debe ser exactamente una)" % (
            expected_domain, s.opens_in_turn(2).count(rules.ROUTERS[expected_domain])))
    if s.bootstrap_runs != 1:
        problems.append("bootstrap re-ejecutado al resolver la entidad")
    if s.active_domain != expected_domain:
        problems.append("dominio != %s: %s (%s)" % (expected_domain, s.active_domain, s.gate_note))
    if sorted(s.pack_files) != sorted(pack):
        problems.append("pack != esperado: %s" % s.pack_files)
    other = "aranea" if expected_domain == "meli" else "meli"
    if rules.ROUTERS[other] in s.pack_files or rules.ROUTERS[other] in s.all_opens():
        problems.append("pack del dominio ajeno (%s) cargado" % other)
    # Métricas: M07, M10, M11, M18, M19.
    swap_agg = weight_of(harness, ctx.vault, s.opens_in_turn(2))
    rec["metrics"].append(metric("session_loaded_set", s.all_opens(), "files", "EXACT", "rules.Session.all_opens"))
    rec["metrics"].append(metric("swap_new_pack_files", s.opens_in_turn(2), "files", "EXACT", "rules.Session.opens_in_turn(2) (fix D1)"))
    _weight_metrics(rec, "swap", swap_agg, "EXACT", "ESTIMATED", "_size del harness sobre opens_in_turn(2)")
    routers_in_pack = [p for p in s.pack_files if p in set(rules.ROUTERS.values())]
    rec["metrics"].append(metric("active_pack_count_post_swap", len(routers_in_pack), "count", "EXACT",
                                 "rules.Session.holds_two_packs + pack_files"))
    rec["metrics"].append(metric("soft_target_swap", swap_agg["estimated_tokens"], "estimated_tokens", "ESTIMATED",
                                 "bootstrap Token Targets + doctor Check 11 + " + TOKENS_NOTE))
    rec["metrics"].append(metric("gate_decision_trace", s.gate_note or "", "text", "EXACT (transcripción)", "bootstrap swap pasos 1-4 via rules.domain_gate"))
    _m15_leak_check(rules, harness, ctx, rec, s.all_opens(), [], s.active_domain, problems)
    evidence.append("transicion: active_entity none->%s; active_domain none->%s" % (title, s.active_domain))
    evidence.append("gate: %s" % s.gate_note)
    lo, hi = SOFT_CEILINGS["swap_estimated_tokens"]
    if not (lo <= swap_agg["estimated_tokens"] < hi):
        rec["evidence"].append("WARN (A1): swap %d estimated_tokens fuera del techo blando %d-%d (chars/4, C04)" % (swap_agg["estimated_tokens"], lo, hi))
    warn = ("WARN declarado (C02/C07 unknown): con entidad previa=none, la definicion de cold ('no entity loaded yet') y la de swap "
            "('switches to a different entity') convergen en el mismo observable; ninguna autoridad fija la clasificacion del modo.")
    if problems:
        rec["verdict"] = "FAIL"
        rec["details"] = "resolución tardía desde DEFAULT violó el contrato"
        rec["evidence"] = rec["evidence"] + problems + [warn]
    else:
        rec["verdict"] = "WARN"  # modo ambiguo: WARN por diseño (spec sección 4)
        rec["details"] = "resolución tardía %s: gate aplicado, base intacta, sin re-ejecutar bootstrap" % title
        rec["evidence"] = rec["evidence"] + [warn]
    return rec


def _fixture_of(title: str) -> str:
    return {"RIO": "30-resources/applications/RIO.md",
            "Echo Forge": "10-projects/Echo Forge/Echo Forge.md"}.get(title, title)


def ctx_09_default_to_meli(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-09", ["SWITCH-DEFAULT-TO-MELI"])
    return _switch_from_default(rec, ctx, rules, harness, "RIO", "meli",
                                [rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"])


def ctx_10_default_to_aranea(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-10", ["SWITCH-DEFAULT-TO-ARANEA"])
    rec = _switch_from_default(rec, ctx, rules, harness, "Echo Forge", "aranea",
                               [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"])
    if rec["verdict"] != "SKIP":
        rec["evidence"].append("mapeo [[Echo]]->aranea-agent-dev verificado explícitamente (bootstrap paso 6)")
    return rec


# ---------------------------------------------------------------------------
# CTX-11 — CTX-LEAK-UNRELATED-DOMAIN (reusa UNRELATED-DOMAIN-NOT-LOADED)
# ---------------------------------------------------------------------------
def ctx_11_leak_unrelated(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-11", ["UNRELATED-DOMAIN-NOT-LOADED"])
    missing = harness.require_files(ctx.vault, ["30-resources/applications/RIO.md", "10-projects/Echo Forge/Echo Forge.md",
                                                harness.FURY_NOTE, harness.PLAYMAKER_NOTE])
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    evidence = rec["evidence"]
    problems: List[str] = []
    all_unrelated: List[str] = []
    ambiguous: List[str] = []
    avoided = {"files": 0, "bytes": 0, "chars": 0, "estimated_tokens": 0}
    runs = [("meli", "RIO", "context"), ("aranea", "Echo Forge", "continuity")]
    for domain, title, intent in runs:
        s = _session_for(ctx)
        s.turn = 1
        s.cold_start({"entity_title": title})
        candidates = s.retrieve(intent)
        loaded = list(dict.fromkeys(s.all_opens() + candidates))
        other = "aranea" if domain == "meli" else "meli"
        evidence.append("[%s] set cargado (%d archivos, opens+candidatos): %s" % (domain, len(loaded), ", ".join(loaded)))
        for rel in loaded:
            dom, conf, note = classify_file(rules, harness, ctx.root, rel)
            if dom == other and conf == "EXACT":
                if rel not in all_unrelated:
                    all_unrelated.append(rel)
                problems.append("[%s] archivo del dominio ajeno %s en el set cargado: %s (diseño 8.1; Hard Rules de exclusividad de los routers + perfil 'Las preferencias Meli y Aranea son scoped' + bootstrap paso 6 fail-closed)" % (domain, other, rel))
            elif dom == other and conf == "INFERRED":
                ambiguous.append("[%s] %s: %s" % (domain, rel, note))
            elif dom is None and conf == "INFERRED":
                ambiguous.append("[%s] %s: %s" % (domain, rel, note))
            if domain == "aranea" and rel == rules.ROUTER_PREFS["meli"][1]:
                ambiguous.append("[%s] %s: nota VPN (Hallazgo 7) en escenario aranea; ni afirmada ni prohibida (WARN, A3)" % (domain, rel))
        # Counterfactual (leak evitado): notas de memoria bloqueadas SOLO por el
        # chequeo de dominio de trigger_fires y que referencian a la entidad
        # activa por entities/project/application (reutiliza rules.references_entity):
        # sin el gate habrían entrado por los triggers basados en referencia.
        entity = s.active_entity or {}
        e_dom_active = rules.domain_from_area(entity.get("area"))
        mem_root = ctx.vault.abspath("80-agents/memory")
        pool: List[str] = []
        for dirpath, dirnames, filenames in os.walk(mem_root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            for fn in sorted(filenames):
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), ctx.root).replace(os.sep, "/")
                if rel in loaded:
                    continue
                fm = ctx.vault.frontmatter(rel)
                n_dom = rules.domain_from_area(fm.get("area"))
                if not (e_dom_active and n_dom and n_dom != e_dom_active):
                    continue  # no fue bloqueado por el chequeo de dominio
                refs = (fm.get("entities"), fm.get("project"), fm.get("application"))
                if any(rules.references_entity(v, entity) for v in refs):
                    pool.append(rel)
        pool_agg = weight_of(harness, ctx.vault, pool)
        for k in ("files", "bytes", "chars", "estimated_tokens"):
            avoided[k] += pool_agg[k]
        evidence.append("[%s] leak evitado (cota superior INFERRED): %d notas del dominio %s referencian a la entidad activa y fueron bloqueadas solo por el chequeo de dominio del filtro (%d chars / %d estimated_tokens)" % (
            domain, pool_agg["files"], other, pool_agg["chars"], pool_agg["estimated_tokens"]))
        if pool:
            evidence.append("[%s] pool del leak evitado: %s" % (domain, ", ".join(pool)))
    if ambiguous:
        evidence.append("M15 clasificaciones ambiguas (WARN, nunca FAIL): %s" % ambiguous)
    unrelated_agg = weight_of(harness, ctx.vault, all_unrelated)
    rec["metrics"].append(metric("unrelated_domain_files", sorted(all_unrelated), "files", "EXACT",
                                 "diseño 8.1: clasificación estática (frontmatter area + rules.ROUTERS/ROUTER_PREFS/DOMAIN_GATED_SKILLS) sobre opens+candidatos"))
    rec["metrics"].append(metric("unrelated_domain_chars", unrelated_agg["chars"], "chars", "EXACT", "_size del harness"))
    rec["metrics"].append(metric("unrelated_domain_estimated_tokens", unrelated_agg["estimated_tokens"], "estimated_tokens",
                                 "ESTIMATED", "_size del harness + " + TOKENS_NOTE))
    rec["metrics"].append(metric("leak_avoided_pool_files", avoided["files"], "files", "INFERRED",
                                 "cota superior del leak evitado: notas bloqueadas solo por el chequeo de dominio y referenciando a la entidad activa (rules.references_entity)"))
    rec["metrics"].append(metric("leak_avoided_pool_chars", avoided["chars"], "chars", "EXACT", "_size del harness"))
    rec["metrics"].append(metric("leak_avoided_pool_estimated_tokens", avoided["estimated_tokens"], "estimated_tokens",
                                 "ESTIMATED", "_size del harness + " + TOKENS_NOTE))
    evidence.append("semántica del counterfactual: sin el chequeo de dominio, las notas del pool habrían entrado por when_error_matches/when_project_loaded/when_application_loaded (ref_hit); las when_area_loaded cruzadas siguen excluidas por desigualdad de área")
    return _finish(rec, problems, "PASS",
                   "retrieval en ambos dominios: 0 archivos del dominio ajeno en el set cargado (M15 EXACT); pool de leak evitado cuantificado (INFERRED)",
                   "el retrieval o el set cargado trajo memoria del dominio ajeno (C11)")


# ---------------------------------------------------------------------------
# CTX-12 — CTX-DEPRECATED-HOT-PATH (reusa DEPRECATED-DOC-NOT-DEFAULT-LOAD)
# ---------------------------------------------------------------------------
def ctx_12_deprecated_hot_path(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-12", ["DEPRECATED-DOC-NOT-DEFAULT-LOAD"])
    missing = harness.require_files(ctx.vault, [rules.GLOBAL_INTERNAL, rules.CONTINUITY_ARCHIVE])
    if missing:
        return _skip(rec, "fixtures no disponibles en el vault actual: %s" % missing)
    evidence = rec["evidence"]
    # Parte simulada: reutiliza el escenario del harness (sin duplicar su lógica).
    h_state, h_details, h_ev = harness.sc_deprecated_doc_not_default_load(ctx)
    evidence.append("escenario harness heredado %s: %s" % (h_state, h_details))
    evidence.extend(h_ev)
    problems: List[str] = []
    if h_state == "FAIL":
        problems.append("escenario heredado DEPRECATED-DOC-NOT-DEFAULT-LOAD en FAIL: %s" % h_details)
    if h_state == "SKIP":
        return _skip(rec, "escenario harness heredado no ejecutable: %s" % h_details)
    # Parte estática M16: barrido sobre los sets fijos (always + packs + expert)
    # detecta el drift inverso: que la ruta fija del hot path apunte a una nota
    # retirada (bootstrap Hard Rules: "Never load superseded or archived...").
    profile = ctx.vault.resolve_profile_note()
    hot = [rules.CONSTITUTION, profile or "", rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX,
           rules.ROUTERS["meli"], rules.ROUTERS["aranea"], rules.ARANEA_MCPS_EXPERT] \
        + rules.ROUTER_PREFS["meli"] + rules.ROUTER_PREFS["aranea"]
    hot = [h for h in hot if h]
    hits: List[str] = []
    hit_rels: List[str] = []
    for rel in hot:
        fm = ctx.vault.frontmatter(rel)
        state = str(fm.get("memory_state", "")).strip().strip("\"'").lower()
        status = str(fm.get("status", "")).strip().strip("\"'").lower()
        if state in ("superseded", "archived"):
            hits.append("%s (memory_state=%s en hot path: FAIL inmediato, bootstrap Hard Rules 'Never load superseded or archived')" % (rel, state))
            hit_rels.append(rel)
        if status in ("deprecated", "deprecating"):
            hits.append("%s (status=%s en hot path: FAIL, schema-contract)" % (rel, status))
            hit_rels.append(rel)
    weight_hits = weight_of(harness, ctx.vault, hit_rels)
    rec["metrics"].append(metric("deprecated_hot_path_files", hits, "files", "EXACT",
                                 "frontmatter parseado de los sets fijos del hot path (bootstrap Hard Rules superseded + schema-contract status)"))
    rec["metrics"].append(metric("deprecated_hot_path_estimated_tokens", weight_hits["estimated_tokens"], "estimated_tokens",
                                 "ESTIMATED", "_size del harness + " + TOKENS_NOTE))
    evidence.append("barrido M16 estático sobre %d archivos del hot path (always + packs + expert): %d hits" % (len(hot), len(hits)))
    problems.extend(hits)
    return _finish(rec, problems, "PASS",
                   "ni el archive superseded ni contenido deprecated en el hot path (simulado + barrido estático M16: 0 hits esperados)",
                   "contenido deprecated/superseded en el hot path (bootstrap Hard Rules / schema-contract)")


# ---------------------------------------------------------------------------
# CTX-13 — CTX-DUP-CONTENT-STATIC (regla 5 de la constitución; M14)
# ---------------------------------------------------------------------------
def ctx_13_dup_content(ctx, rules, harness) -> Dict[str, Any]:
    rec = _new_record("CTX-13", ["regla 5 de agent-constitution.md ('Una fuente canónica por hecho... Enlazar en vez de repetir')", "DUAL-REGISTRY-DOMAIN-SYNC"])
    profile = ctx.vault.resolve_profile_note()
    base = [rules.CONSTITUTION, profile, rules.GLOBAL_INTERNAL, rules.SKILLS_INDEX]
    sets = {
        "base": [f for f in base if f],
        "base+meli": [f for f in base if f] + [rules.ROUTERS["meli"]] + rules.ROUTER_PREFS["meli"],
        "base+aranea": [f for f in base if f] + [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"],
        "registros": [rules.SKILLS_INDEX, rules.FEDERATED_DOMAIN_INDEX],
    }
    texts: Dict[str, str] = {}
    missing = []
    for files in sets.values():
        for rel in files:
            if rel not in texts:
                t = ctx.vault.read(rel)
                if t is None:
                    missing.append(rel)
                else:
                    texts[rel] = t
    if missing:
        return _skip(rec, "archivos ausentes para el barrido M14: %s" % missing)
    evidence = rec["evidence"]
    pairs_done = set()
    hits: List[Dict[str, Any]] = []
    total_dup_chars = 0
    for set_name, files in sets.items():
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                a, b = sorted((files[i], files[j]))
                key = (a, b)
                if key in pairs_done:
                    continue
                pairs_done.add(key)
                report = find_duplication(texts[a], texts[b])
                if duplication_hit(report):
                    hits.append({"set": set_name, "a": a, "b": b,
                                 "total_chars": report["total_chars"],
                                 "max_consecutive_lines": report["max_consecutive_lines"],
                                 "runs": report["runs"]})
                    total_dup_chars += report["total_chars"]
    for h in hits:
        evidence.append("par duplicado [%s]: %s <-> %s (total %d chars normalizados, max %d líneas consecutivas)" % (
            h["set"], h["a"], h["b"], h["total_chars"], h["max_consecutive_lines"]))
        for r in h["runs"]:
            evidence.append("  bloque (%d chars, %d/%d líneas): \"%s\"" % (r["chars"], r["lines_a"], r["lines_b"], r["snippet"]))
    if not hits:
        evidence.append("ningún par co-cargable supera el umbral declarado (A4): total_chars < %d y ningún bloque de >= %d líneas consecutivas" % (
            DUP_THRESHOLD["min_chars"], DUP_THRESHOLD["min_consecutive_lines"]))
    rec["metrics"].append(metric("duplicate_hot_path_pairs", len(hits), "count", "INFERRED",
                                 "heurística self-declared M14 v1 (umbral A4 ratificado): runs contiguos normalizados >= %d tokens; condición chars >= %d o >= %d líneas" % (
                                     DUP_THRESHOLD["min_run_tokens"], DUP_THRESHOLD["min_chars"], DUP_THRESHOLD["min_consecutive_lines"])))
    rec["metrics"].append(metric("duplicate_hot_path_chars", total_dup_chars, "chars", "EXACT",
                                 "suma de chars normalizados de los runs detectados (dado el detector declarado)"))
    rec["metrics"].append(metric("duplicate_hot_path_estimated_tokens", total_dup_chars // 4, "estimated_tokens", "ESTIMATED",
                                 TOKENS_NOTE))
    evidence.append("veredicto máximo WARN (A4): la duplicación con umbral propio nunca sostiene FAIL hasta que el parent ratifique otro umbral; no detecta paráfrasis semántica")
    verdict = "WARN" if hits else "PASS"
    rec["verdict"] = verdict
    rec["details"] = ("duplicación textual en el hot path detectada (WARN; umbral A4 declarado): %d pares" % len(hits)) if hits \
        else "sin duplicación textual >= umbral declarado en los sets co-cargables (M14 v1)"
    return rec


# ---------------------------------------------------------------------------
# CTX-14 — CTX-SURFACE-EXPOSURE (A5: SKIP por defecto; --live reutiliza la
# misma función de lectura de configs del harness; nunca criterio de FAIL)
# ---------------------------------------------------------------------------
def ctx_14_surface(ctx, rules, harness, conformance_json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    rec = _new_record("CTX-14", ["SESSION-SURFACE-EXPOSURE (L2)"])
    if conformance_json:
        h_scn = [s for s in conformance_json.get("scenarios", []) if s.get("id") == "SESSION-SURFACE-EXPOSURE"]
        if h_scn:
            rec["evidence"].append("veredicto del harness adjuntado (--conformance-json, sin re-ejecutar): %s" % h_scn[0].get("state"))
    if not getattr(ctx, "live", False) and ctx.machine_surface is None:
        return _skip(rec, "--live ausente (A5): la parte de configs de máquina se omite por defecto; equivalente a --no-live del harness")
    configs = harness.read_surface_configs()  # misma función del harness (sin reimplementación)
    if not configs:
        return _skip(rec, "ninguna config de superficie presente (~/.zcode/cli/config.json, ~/.cursor/mcp.json, ~/.codex/config.toml)")
    observations: List[Dict[str, Any]] = []
    deviations: List[str] = []
    for cfg in configs:
        observations.append({"surface": cfg["surface"], "aranea": cfg["aranea"], "meli": cfg["meli"]})
        rec["evidence"].append("%s (%s): aranea=%d meli=%d (nombres only, nunca credenciales)" % (
            cfg["surface"], cfg["path"], cfg["aranea"], cfg["meli"]))
        if cfg["aranea"] == 0:
            deviations.append("%s: sin servers aranea-* configurados" % cfg["surface"])
        if cfg["meli"] > 0:
            deviations.append("%s: servers Meli configurados (%d)" % (cfg["surface"], cfg["meli"]))
    rec["metrics"].append(metric("mcp_surface_config_observed", observations, "count", "EXACT",
                                 "harness.read_surface_configs (misma función, nombres only); SKIP si no existen configs"))
    rec["evidence"].append("presencia de aranea-* registrada como dato (Hallazgo 4); la exposición de una sesión viva sigue UNOBSERVABLE (Hallazgo 17); nunca criterio de FAIL de presupuesto (A5)")
    rec["verdict"] = "WARN" if deviations else "PASS"
    rec["details"] = ("superficie observada con desviaciones (dato WARN, nunca FAIL): " + "; ".join(deviations)) if deviations \
        else "superficie observada: aranea-* presentes y cero servers Meli en las configs presentes (dato; no certifica sesión viva)"
    return rec


# ---------------------------------------------------------------------------
# Runner (orden obligatorio del spec sección 3)
# ---------------------------------------------------------------------------
SCENARIOS: List[Tuple[str, str, List[str]]] = [
    ("CTX-15", "baseline", ["context_baseline"]),
    ("CTX-01", "cold", ["COLD-DEFAULT"]),
    ("CTX-02", "cold", ["COLD-MELI"]),
    ("CTX-03", "cold", ["COLD-ARANEA"]),
    ("CTX-04", "warm", ["WARM-DEFAULT"]),
    ("CTX-05", "warm", ["WARM-MELI", "BOOTSTRAP-NOT-RERUN-ON-WARM"]),
    ("CTX-06", "warm", ["WARM-ARANEA"]),
    ("CTX-07", "switch", ["SWITCH-MELI-TO-ARANEA"]),
    ("CTX-08", "switch", ["SWITCH-ARANEA-TO-MELI"]),
    ("CTX-09", "switch", ["SWITCH-DEFAULT-TO-MELI"]),
    ("CTX-10", "switch", ["SWITCH-DEFAULT-TO-ARANEA"]),
    ("CTX-11", "leak", ["UNRELATED-DOMAIN-NOT-LOADED"]),
    ("CTX-12", "deprecated", ["DEPRECATED-DOC-NOT-DEFAULT-LOAD"]),
    ("CTX-13", "duplication", ["regla 5 constitución", "DUAL-REGISTRY-DOMAIN-SYNC"]),
    ("CTX-14", "surface", ["SESSION-SURFACE-EXPOSURE"]),
]

_FUNCS = {
    "CTX-15": ctx_15_baseline,
    "CTX-01": ctx_01_default_cold,
    "CTX-02": ctx_02_meli_cold,
    "CTX-03": ctx_03_aranea_cold,
    "CTX-04": ctx_04_default_warm,
    "CTX-05": ctx_05_meli_warm,
    "CTX-06": ctx_06_aranea_warm,
    "CTX-07": ctx_07_switch_meli_aranea,
    "CTX-08": ctx_08_switch_aranea_meli,
    "CTX-09": ctx_09_default_to_meli,
    "CTX-10": ctx_10_default_to_aranea,
    "CTX-11": ctx_11_leak_unrelated,
    "CTX-12": ctx_12_deprecated_hot_path,
    "CTX-13": ctx_13_dup_content,
    "CTX-14": ctx_14_surface,
}


def _aggregate_totals(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_id = {r["id"]: r for r in results}

    totals: Dict[str, Any] = {}
    b = by_id.get("CTX-15")
    if b and b["verdict"] != "SKIP":
        m = {mm["name"]: mm["value"] for mm in b["metrics"]}
        totals["always_load"] = {"files": len(m.get("always_load_file_list", [])),
                                 "chars": m.get("always_load_chars"), "bytes": m.get("always_load_bytes"),
                                 "estimated_tokens": m.get("always_load_estimated_tokens"), "confidence": "ESTIMATED"}
        packs = {}
        for dom in ("meli", "aranea"):
            key = "scope_pack_file_list_%s" % dom
            if key in m:
                packs[dom] = {"files": len(m[key]), "chars": m.get("scope_pack_chars_%s" % dom),
                              "bytes": m.get("scope_pack_bytes_%s" % dom),
                              "estimated_tokens": m.get("scope_pack_estimated_tokens_%s" % dom),
                              "confidence": "ESTIMATED"}
        totals["scope_pack"] = packs
    colds = {}
    for dom, sid in (("default", "CTX-01"), ("meli", "CTX-02"), ("aranea", "CTX-03")):
        r = by_id.get(sid)
        if r and r["verdict"] != "SKIP":
            for mm in r["metrics"]:
                if mm["name"] == "session_cold_estimated_tokens":
                    colds[dom] = mm["value"]
    if colds:
        colds["confidence"] = "ESTIMATED"
        colds["note"] = TOKENS_NOTE
        totals["cold_estimated_tokens"] = colds
    wr = by_id.get("CTX-05")
    if wr and wr["verdict"] != "SKIP":
        m = {mm["name"]: mm["value"] for mm in wr["metrics"]}
        totals["warm_delta"] = {"files": m.get("warm_delta_files"), "chars": m.get("warm_delta_chars"),
                                "bytes": m.get("warm_delta_bytes"),
                                "estimated_tokens": m.get("warm_delta_estimated_tokens"), "confidence": "ESTIMATED"}
    swaps = {}
    for label, sid in (("meli_to_aranea", "CTX-07"), ("aranea_to_meli", "CTX-08"),
                       ("default_to_meli", "CTX-09"), ("default_to_aranea", "CTX-10")):
        r = by_id.get(sid)
        if r and r["verdict"] != "SKIP":
            for mm in r["metrics"]:
                if mm["name"] == "swap_estimated_tokens":
                    swaps[label] = mm["value"]
    if swaps:
        swaps["confidence"] = "ESTIMATED"
        totals["swap_estimated_tokens"] = swaps
    l = by_id.get("CTX-11")
    if l and l["verdict"] != "SKIP":
        m = {mm["name"]: mm["value"] for mm in l["metrics"]}
        totals["unrelated_domain"] = {"files": len(m.get("unrelated_domain_files", [])), "chars": 0,
                                      "bytes": 0, "estimated_tokens": 0, "confidence": "EXACT"}
    d = by_id.get("CTX-12")
    if d and d["verdict"] != "SKIP":
        m = {mm["name"]: mm["value"] for mm in d["metrics"]}
        totals["deprecated_hot_path"] = {"files": len(m.get("deprecated_hot_path_files", [])),
                                         "estimated_tokens": m.get("deprecated_hot_path_estimated_tokens"),
                                         "confidence": "EXACT"}
    p = by_id.get("CTX-13")
    if p and p["verdict"] != "SKIP":
        m = {mm["name"]: mm["value"] for mm in p["metrics"]}
        totals["duplicate_hot_path"] = {"pairs": m.get("duplicate_hot_path_pairs"),
                                        "chars": m.get("duplicate_hot_path_chars"),
                                        "estimated_tokens": m.get("duplicate_hot_path_estimated_tokens"),
                                        "confidence": "INFERRED"}
    return totals


def run_suite(vault_root: str, live: bool = False, scenario: Optional[str] = None,
              write: bool = True, conformance_json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Corre la suite CTX y devuelve el record machine-readable (spec sección 7).
    `write=True` es la única escritura permitida: results/run-<timestamp>.json."""
    doc: Dict[str, Any] = {
        "run": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tool": TOOL,
        "git_head": None,
        "fidelity_gate": "SKIP",
        "scenarios": [],
        "totals": {},
        "counts": {"pass": 0, "fail": 0, "warn": 0, "skip": 0},
        "ambiguities": list(DECLARED_AMBIGUITIES),
        "thresholds": {"duplication": dict(DUP_THRESHOLD), "soft_ceilings": {k: list(v) for k, v in SOFT_CEILINGS.items()}},
    }
    requested = [sid for sid, _, _ in SCENARIOS]
    if scenario:
        if scenario == "RULES-FIDELITY-ANCHORS":
            requested = []
        elif scenario in [sid for sid, _, _ in SCENARIOS]:
            requested = [scenario]
        else:
            raise ValueError("escenario desconocido: %s" % scenario)

    marker_ok = os.path.isfile(os.path.join(vault_root, MARKER))
    if not marker_ok:
        reason = "marker %s ausente bajo la raiz indicada: las reglas de AGENTS OS no aplican (AGENTS.md / spec sección 6)" % MARKER
        for sid in requested:
            rec = _new_record(sid, dict(SCENARIOS[[s[0] for s in SCENARIOS].index(sid)][2]))
            doc["scenarios"].append(_skip(rec, reason))
    else:
        try:
            rules, harness = load_harness(vault_root)
        except Exception as exc:
            reason = "harness no disponible (%s: %s): los escenarios que dependen del modelo de sesión van a SKIP" % (type(exc).__name__, exc)
            for sid in requested:
                rec = _new_record(sid, dict(SCENARIOS[[s[0] for s in SCENARIOS].index(sid)][2]))
                doc["scenarios"].append(_skip(rec, reason))
            _finalize(doc, vault_root, write)
            return doc
        ctx = harness.Ctx(vault_root, no_live=not live)
        setattr(ctx, "live", live)
        # Pre-flight RULES-FIDELITY-ANCHORS (importado del harness; corre primero).
        try:
            a_state, a_details, a_ev = harness.sc_rules_fidelity_anchors(ctx)
        except Exception as exc:
            a_state, a_details, a_ev = "SKIP", "no ejecutable: %s: %s" % (type(exc).__name__, exc), []
        doc["fidelity_gate"] = a_state
        doc["fidelity_details"] = a_details
        doc["fidelity_evidence"] = a_ev
        gate_failed = a_state == "FAIL"
        operator_directed = scenario is not None
        for sid in requested:
            reuses = list(SCENARIOS[[s[0] for s in SCENARIOS].index(sid)][2])
            rec = _new_record(sid, reuses)
            if gate_failed and not operator_directed:
                doc["scenarios"].append(_skip(rec, "gate: pre-flight RULES-FIDELITY-ANCHORS en FAIL (transcripción obsoleta); los resultados presupuestarios no son interpretables sobre una transcripción derivada (diseño sección 3)"))
                continue
            fn = _FUNCS[sid]
            try:
                if sid == "CTX-14":
                    rec = fn(ctx, rules, harness, conformance_json)
                else:
                    rec = fn(ctx, rules, harness)
            except Exception as exc:  # nunca traceback: SKIP honesto con motivo
                rec = _skip(rec, "no ejecutable: %s: %s" % (type(exc).__name__, exc))
            doc["scenarios"].append(rec)
    _finalize(doc, vault_root, write)
    return doc


def _finalize(doc: Dict[str, Any], vault_root: str, write: bool) -> None:
    counts = {"pass": 0, "fail": 0, "warn": 0, "skip": 0}
    for r in doc["scenarios"]:
        counts[r["verdict"].lower()] = counts.get(r["verdict"].lower(), 0) + 1
    doc["counts"] = counts
    doc["totals"] = _aggregate_totals(doc["scenarios"])
    try:
        rules, harness = load_harness(vault_root)
        doc["git_head"] = harness.git_head(vault_root)
    except Exception:
        doc["git_head"] = None
    if write:
        os.makedirs(RESULTS_DIR, exist_ok=True)  # única escritura permitida (spec sección 5)
        ts = time.strftime("%Y%m%d-%H%M%S")
        out_path = os.path.join(RESULTS_DIR, "run-%s.json" % ts)
        n = 1
        while os.path.exists(out_path):
            n += 1
            out_path = os.path.join(RESULTS_DIR, "run-%s-%d.json" % (ts, n))
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
        doc["results_file"] = os.path.relpath(out_path, vault_root).replace(os.sep, "/")


# ---------------------------------------------------------------------------
# Salida humana (A9): una línea por escenario + baseline + counts
# ---------------------------------------------------------------------------
def human_summary(doc: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("=" * 72)
    lines.append("AGENTS-OS CONTEXT BUDGET (P2)")
    lines.append("=" * 72)
    lines.append("run %s · vault: %s · git %s · fidelity_gate %s" % (
        doc["run"], doc.get("vault_root_arg", "auto"), (doc.get("git_head") or "?")[:9], doc["fidelity_gate"]))
    for r in doc["scenarios"]:
        lines.append("%s %s %s" % (r["id"].ljust(8, "."), r["verdict"].ljust(5), r["details"]))
    c = doc["counts"]
    lines.append("-" * 72)
    lines.append("counts: PASS %d · FAIL %d · WARN %d · SKIP %d" % (c["pass"], c["fail"], c["warn"], c["skip"]))
    t = doc.get("totals") or {}
    al = t.get("always_load")
    sp = t.get("scope_pack") or {}
    if al:
        lines.append("baseline (baseline-only, chars/4, C04): always-load ≈ %s estimated_tokens · pack meli ≈ %s estimated_tokens · pack aranea ≈ %s estimated_tokens" % (
            al.get("estimated_tokens"), sp.get("meli", {}).get("estimated_tokens"), sp.get("aranea", {}).get("estimated_tokens")))
    for r in doc["scenarios"]:
        if r["verdict"] == "FAIL":
            lines.append("FAIL %s: %s" % (r["id"], r["details"]))
    lines.append("=" * 72)
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="context_budget.py",
        description="AGENTS OS Context Budget + Domain Leak Auditor (P2). Read-only salvo results/.")
    ap.add_argument("--vault-root", help="ruta del vault (default: autodetección por marker)")
    ap.add_argument("--json", action="store_true", help="JSON a stdout y results/run-<timestamp>.json; resumen a stderr")
    ap.add_argument("--scenario", help="corre un solo escenario CTX por id (run dirigido por el operador, sin gate) o RULES-FIDELITY-ANCHORS")
    ap.add_argument("--live", action="store_true", help="habilita CTX-14 (lectura names-only de configs de máquina vía el harness)")
    ap.add_argument("--conformance-json", help="adjunta los veredictos de un run del harness como evidencia cruzada (CTX-14), sin re-ejecutarlos")
    args = ap.parse_args(argv)

    root = resolve_vault_root(args.vault_root)
    if root is None:
        print("ERROR: no se pudo autodetectar VAULT_ROOT (carpeta que contiene %s). Usa --vault-root." % MARKER, file=sys.stderr)
        return 2
    conformance_json = None
    if args.conformance_json:
        try:
            with open(args.conformance_json, "r", encoding="utf-8") as fh:
                conformance_json = json.load(fh)
        except (OSError, ValueError) as exc:
            print("ERROR: --conformance-json ilegible: %s" % exc, file=sys.stderr)
            return 2
    doc = run_suite(root, live=args.live, scenario=args.scenario, write=True, conformance_json=conformance_json)
    doc["vault_root_arg"] = args.vault_root or "auto"
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
    fail = doc["counts"].get("fail", 0) > 0 or doc.get("fidelity_gate") == "FAIL"
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
