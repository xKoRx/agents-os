#!/usr/bin/env python3
"""Selftest de context-budget (P2-B): pruebas de inyección y negativas.

Spec vinculante: artifacts/p2-context-budget-spec.md sección 6 (requisitos de
verificación 2-5) y diseño P2-A sección 10. NUNCA toca el vault canónico:
todos los fixtures se construyen en tempfile del sistema; las dos autoridades
de anchors (bootstrap/doctor SKILL.md) se COPIAN read-only desde el vault real
cuando el test necesita un pre-flight en verde. Escrituras de resultados de
main() se redirigen a un results/ temporal.

Cobertura:
- T1 inyección: un agente saboteador que carga el pack cruzado dispara FAIL
  en CTX-02 (sin dejar rastro en el vault).
- T2 input malformado (binario basura / frontmatter roto / perfil ausente)
  produce SKIP/FAIL motivado, nunca traceback abortando.
- T3 pre-flight en rojo (autoridad truncada) -> todos los CTX en SKIP motivado.
- T4 marker ausente -> todos los CTX en SKIP con motivo.
- T5 determinismo: dos runs completos sobre el vault real (read-only, sin
  escribir resultados) producen records idénticos salvo `run`/timestamp.
- T6 etiquetado: prohibido un campo llamado `tokens`; la nota chars/4 es
  visible; `estimated_tokens` presente.
- T7 exit codes: escenario desconocido -> 2; suite sin FAIL -> 0.

Python 3.9+ stdlib only. Imprime PASS/FAIL por test y exit code.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True  # sin __pycache__ fuera del write scope
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import context_budget as cb  # noqa: E402

VAULT = cb.resolve_vault_root()
if VAULT is None:
    print("FAIL selftest-bootstrap: no se pudo resolver VAULT_ROOT")
    sys.exit(1)

RESULTS = []  # [(nombre, ok, detalle)]


def report(name: str, ok: bool, detail: str) -> None:
    RESULTS.append((name, ok, detail))
    print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))


# ---------------------------------------------------------------------------
# Fixtures temporales (fuera del vault; nunca se toca el canónico)
# ---------------------------------------------------------------------------
PROFILE_REL = "80-agents/memory/public/user-preference/rjara-agent-profile.md"
MELI_PREF_REL = "80-agents/memory/public/user-preference/rjara-meli-work-preferences.md"
VPN_REL = "80-agents/memory/public/user-preference/rjara-vpn-routing-preferences.md"
ARANEA_PREF_REL = "80-agents/memory/public/user-preference/rjara-aranea-operations-preferences.md"
GLOBAL_REL = "80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md"
ARCHIVE_REL = GLOBAL_REL.replace(".md", "-archive.md")
FURY_REL = "80-agents/memory/public/known-error/rio/2026-08-19-rio-fury-note.md"
PLAYMAKER_REL = "80-agents/memory/public/decision/rio/2026-08-25-playmaker-note.md"
MT5_REL = "80-agents/memory/internal/agent-memory/2026-09-04-echo-forge-mt5-note.md"
RIO_REL = "30-resources/applications/RIO.md"
ECHO_REL = "10-projects/Echo Forge/Echo Forge.md"
MELI_ROUTER_REL = "30-resources/agents/skills/meli-agent-dev/SKILL.md"
ARANEA_ROUTER_REL = "30-resources/agents/skills/aranea-agent-dev/SKILL.md"
SIGNALS_REL = "30-resources/agents/skills/signals-code-review/SKILL.md"
BOOTSTRAP_AUTH = "80-agents/skills/agents-os-bootstrap/SKILL.md"
DOCTOR_AUTH = "80-agents/skills/agents-os-doctor/SKILL.md"


def _write(root: str, rel: str, text: str) -> None:
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _copy_from_vault(rel: str, root: str) -> None:
    """Copia read-only de una autoridad del vault real al fixture temporal."""
    src = os.path.join(VAULT, rel)
    dst = os.path.join(root, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(text)


def build_temp_vault(variant: str = "full") -> str:
    """Construye un vault mínimo temporal. Variantes: full (preflight verde),
    corrupt (perfil binario), missing-profile, red (bootstrap truncado),
    empty (sin marker). Para las variantes con marker, el harness se enlaza
    por symlink (resolve relativo a VAULT_ROOT en runtime: el vault temporal
    finge ser un VAULT_ROOT y trae su harness instalado, como el real)."""
    root = tempfile.mkdtemp(prefix="ctx-budget-selftest-")
    if variant == "empty":
        os.makedirs(os.path.join(root, "80-agents/agents-os"), exist_ok=True)
        return root  # sin marker: las reglas de AGENTS OS no aplican
    os.makedirs(os.path.join(root, "80-agents/agents-os"), exist_ok=True)
    _write(root, "80-agents/agents-os/agents-os.md", "# map\n")
    harness_target = os.path.join(root, "80-agents/tools/conformance-harness")
    os.makedirs(os.path.dirname(harness_target), exist_ok=True)
    os.symlink(os.path.join(VAULT, "80-agents/tools/conformance-harness"), harness_target)
    _copy_from_vault(BOOTSTRAP_AUTH, root)
    _copy_from_vault(DOCTOR_AUTH, root)
    _write(root, "80-agents/agents-os/agent-constitution.md",
           "---\ntype: doc\narea: \"[[Personal]]\"\nload_policy: always\n---\n\n5. Una fuente canónica por hecho; enlazar en vez de repetir.\n")
    _write(root, "80-agents/skills/INDEX.md", "# Índice de skills\n\n| Skill | Una línea | Dominio / uso |\n")
    _write(root, GLOBAL_REL,
           "---\ntype: agent_memory\narea: \"[[Personal]]\"\nmemory_state: active\ncontinuity_key: global/test\nload_policy: always\n---\n\nContinuidad global de prueba.\n")
    _write(root, ARCHIVE_REL,
           "---\ntype: agent_memory\narea: \"[[Personal]]\"\nmemory_state: superseded\ncontinuity_key: global/test\nload_policy: manual\nindex_priority: low\nsuperseded_by: \"[[agents-os-operating-continuity]]\"\n---\n\nArchive de prueba.\n")
    if variant == "corrupt":
        path = os.path.join(root, PROFILE_REL)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(b"\xff\xfe\x00\x01binary garbage \x00\x9c not markdown")
    elif variant == "missing-profile":
        pass  # el perfil no se crea
    else:
        _write(root, PROFILE_REL,
               "---\ntype: user_preference\nscope: user\nload_policy: always\nentities:\n  - \"[[AGENTS OS]]\"\n---\n\nPerfil global de prueba.\n")
    _write(root, MELI_PREF_REL,
           "---\ntype: user_preference\nscope: area\narea: \"[[Meli]]\"\n---\n\nPreferencias Meli de prueba.\n")
    _write(root, VPN_REL,
           "---\ntype: user_preference\nscope: user\nload_policy: when_area_loaded\n---\n\nVPN de prueba (Hallazgo 7: sin campo area).\n")
    _write(root, ARANEA_PREF_REL,
           "---\ntype: user_preference\nscope: area\narea: \"[[Aranea]]\"\n---\n\nPreferencias Aranea de prueba.\n")
    _write(root, RIO_REL,
           "---\ntype: service\nstatus: active\narea: \"[[Meli]]\"\nslug: rio\naliases:\n  - RIO\n---\n\nRIO de prueba.\n")
    _write(root, ECHO_REL,
           "---\ntype: project\nstatus: active\narea: \"[[Echo]]\"\n---\n\nEcho Forge de prueba.\n")
    _write(root, MELI_ROUTER_REL, "---\ntype: skill\n---\n\n# meli-agent-dev\nRouter de prueba.\n")
    _write(root, ARANEA_ROUTER_REL, "---\ntype: skill\n---\n\n# aranea-agent-dev\nRouter de prueba.\n")
    _write(root, SIGNALS_REL, "---\ntype: skill\n---\n\n# signals-code-review\nSkill de prueba.\n")
    _write(root, FURY_REL,
           "---\ntype: known_error\narea: \"[[Meli]]\"\nload_policy: when_error_matches\nentities:\n  - \"[[RIO]]\"\n---\n\nKnown error de prueba.\n")
    _write(root, PLAYMAKER_REL,
           "---\ntype: decision\narea: \"[[Meli]]\"\nload_policy: when_application_loaded\napplication: \"[[rio-playmaker]]\"\n---\n\nDecisión de prueba.\n")
    _write(root, MT5_REL,
           "---\ntype: agent_memory\nmemory_state: active\nload_policy: when_echo_forge_loaded\ncontinuity_key: echo-forge/test\n---\n\nContinuidad MT5 de prueba.\n")
    return root


def _ctx_for(root: str):
    rules, harness = cb.load_harness(VAULT)
    ctx = harness.Ctx(root, no_live=True)
    return rules, harness, ctx


# ---------------------------------------------------------------------------
# T1 — inyección: pack cruzado dispara FAIL (spec sección 6.2)
# ---------------------------------------------------------------------------
def t1_injection_cross_pack() -> None:
    rules, harness, ctx = _ctx_for(build_temp_vault("full"))
    # Control: sin inyección, CTX-02 pasa.
    control = cb.ctx_02_meli_cold(ctx, rules, harness)
    report("T1a.control-ctx02-sin-inyeccion", control["verdict"] == "PASS",
           "CTX-02 sobre fixture temporal sin inyección -> %s" % control["verdict"])
    original = cb._session_for

    class CrossPackSession(rules.Session):
        """Agente saboteador: tras el cold start meli carga además el pack
        aranea (violación del Hard Rule 'Never load both routers')."""

        def cold_start(self, request):
            missing = super().cold_start(request)
            if self.active_domain == "meli":
                for rel in [rules.ROUTERS["aranea"]] + rules.ROUTER_PREFS["aranea"]:
                    self.open(rel, "inyeccion selftest: pack cruzado")
                    self.pack_files.append(rel)
            return missing

    try:
        cb._session_for = lambda c: CrossPackSession(c.vault)
        sabotaged = cb.ctx_02_meli_cold(ctx, rules, harness)
        joined = json.dumps(sabotaged, ensure_ascii=False)
        ok = sabotaged["verdict"] == "FAIL" and "aranea-agent-dev" in joined and "carga prohibida" in joined
        report("T1b.inyeccion-pack-cruzado-dispara-FAIL", ok,
               "sesión saboteada -> %s con evidencia del pack cruzado" % sabotaged["verdict"])
    finally:
        cb._session_for = original  # restauración: el vault real nunca se toca
    control2 = cb.ctx_02_meli_cold(ctx, rules, harness)
    report("T1c.restauracion-sin-efecto-residual", control2["verdict"] == "PASS",
           "tras restaurar _session_for, CTX-02 vuelve a %s (sin residuo de la inyección)" % control2["verdict"])


# ---------------------------------------------------------------------------
# T2 — input malformado: SKIP/FAIL motivado, nunca traceback
# ---------------------------------------------------------------------------
def t2_malformed_input() -> None:
    for variant, desc in (("corrupt", "perfil con bytes binarios ilegibles"),
                          ("missing-profile", "perfil always ausente")):
        root = build_temp_vault(variant)
        try:
            doc = cb.run_suite(root, write=False)
            states = {r["verdict"] for r in doc["scenarios"]}
            skips = [r for r in doc["scenarios"] if r["verdict"] == "SKIP"]
            motivated = all(r.get("skip_reason") for r in skips)
            ok = states <= {"PASS", "FAIL", "WARN", "SKIP"} and skips and motivated
            report("T2.%s" % variant, bool(ok),
                   "%s -> estados %s; %d SKIP todos con motivo (sin traceback)" % (desc, sorted(states), len(skips)))
        except Exception as exc:  # un traceback aquí sería el fallo del test
            report("T2.%s" % variant, False, "excepción no contenida: %s: %s" % (type(exc).__name__, exc))
        finally:
            shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------
# T3 — pre-flight en rojo: todos los CTX en SKIP motivado
# ---------------------------------------------------------------------------
def t3_preflight_red() -> None:
    root = build_temp_vault("red")
    try:
        # Trunca la autoridad bootstrap: las anclas de fidelidad desaparecen.
        path = os.path.join(root, BOOTSTRAP_AUTH)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# bootstrap truncado\n\nContenido sin las citas transcritas.\n")
        doc = cb.run_suite(root, write=False)
        gate = doc["fidelity_gate"]
        all_skip = all(r["verdict"] == "SKIP" for r in doc["scenarios"]) and doc["scenarios"]
        motivated = all("gate" in (r.get("skip_reason") or "") for r in doc["scenarios"])
        report("T3.preflight-rojo-todos-skip", gate == "FAIL" and bool(all_skip) and motivated,
               "fidelity_gate=%s; %d/%d CTX en SKIP con motivo de gate (transcripción obsoleta)" % (
                   gate, sum(1 for r in doc["scenarios"] if r["verdict"] == "SKIP"), len(doc["scenarios"])))
    finally:
        shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------
# T4 — marker ausente: todos los CTX en SKIP con motivo
# ---------------------------------------------------------------------------
def t4_marker_missing() -> None:
    root = build_temp_vault("empty")
    try:
        doc = cb.run_suite(root, write=False)
        all_skip = all(r["verdict"] == "SKIP" for r in doc["scenarios"]) and doc["scenarios"]
        motivated = all("marker" in (r.get("skip_reason") or "") for r in doc["scenarios"])
        report("T4.marker-ausente-todos-skip", bool(all_skip) and motivated and doc["fidelity_gate"] == "SKIP",
               "%d CTX en SKIP citando el marker ausente" % len(doc["scenarios"]))
    finally:
        shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------
# T5 — determinismo: dos runs completos idénticos salvo run/timestamp
# ---------------------------------------------------------------------------
def _normalize(doc):
    d = json.loads(json.dumps(doc))
    d.pop("run", None)
    d.pop("results_file", None)
    return d


def t5_determinism() -> None:
    doc1 = cb.run_suite(VAULT, write=False)
    doc2 = cb.run_suite(VAULT, write=False)
    same = _normalize(doc1) == _normalize(doc2)
    report("T5.determinismo-dos-runs", same,
           "dos runs completos sobre el vault real: records %s salvo run/timestamp" % ("idénticos" if same else "DIFERENTES"))
    if not same:
        n1, n2 = _normalize(doc1), _normalize(doc2)
        for sid in n1["scenarios"]:
            other = [r for r in n2["scenarios"] if r["id"] == sid["id"]][0]
            if sid != other:
                print("  diff en %s" % sid["id"])
                break


# ---------------------------------------------------------------------------
# T6 — etiquetado: prohibido campo `tokens`; nota chars/4 visible
# ---------------------------------------------------------------------------
def _all_keys(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            acc.add(k)
            _all_keys(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            _all_keys(v, acc)


def t6_labeling() -> None:
    doc = cb.run_suite(VAULT, write=False)
    keys = set()
    _all_keys(doc, keys)
    no_tokens_field = "tokens" not in keys
    has_estimated = "estimated_tokens" in keys
    text = json.dumps(doc, ensure_ascii=False)
    note_visible = "chars/4" in text and "C04" in text
    report("T6.etiquetado", no_tokens_field and has_estimated and note_visible,
           "campo `tokens` ausente: %s; `estimated_tokens` presente: %s; nota chars/4+C04 visible: %s" % (
               no_tokens_field, has_estimated, note_visible))


# ---------------------------------------------------------------------------
# T7 — exit codes (spec sección 5: 0/1/2)
# ---------------------------------------------------------------------------
def t7_exit_codes() -> None:
    original_results = cb.RESULTS_DIR
    tmp_results = tempfile.mkdtemp(prefix="ctx-budget-selftest-results-")
    cb.RESULTS_DIR = tmp_results  # main() escribe sus runs fuera del vault
    try:
        code_unknown = cb.main(["--scenario", "NO-EXISTE"])
        report("T7a.escenario-desconocido-exit-2", code_unknown == 2, "exit=%d" % code_unknown)
        root = build_temp_vault("full")
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
                code_clean = cb.main(["--vault-root", root, "--json"])
            report("T7b.suite-temporal-sin-FAIL-exit-0", code_clean == 0, "exit=%d (suite completa sobre fixture temporal con harness enlazado)" % code_clean)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    finally:
        cb.RESULTS_DIR = original_results
        shutil.rmtree(tmp_results, ignore_errors=True)


def main() -> int:
    print("selftest context-budget (fixtures temporales; vault canónico: %s)" % VAULT)
    t1_injection_cross_pack()
    t2_malformed_input()
    t3_preflight_red()
    t4_marker_missing()
    t5_determinism()
    t6_labeling()
    t7_exit_codes()
    failures = [name for name, ok, _ in RESULTS if not ok]
    print("-" * 72)
    print("selftest: %d/%d PASS%s" % (len(RESULTS) - len(failures), len(RESULTS),
                                      ("; FALLAN: %s" % ", ".join(failures)) if failures else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
