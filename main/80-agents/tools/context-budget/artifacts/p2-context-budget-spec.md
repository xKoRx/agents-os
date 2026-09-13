---
type: doc
schema_version: 1
status: active
scope: project
project: "[[AGENTS OS]]"
area: "[[Personal]]"
created: 2026-09-13
updated: 2026-09-13
description: Spec vinculante del parent para la tool context-budget (PHASE 2) — métricas, escenarios, semántica, paths permitidos y output schema; ratifica el diseño de P2-A resolviendo las ambigüedades A1-A9.
aliases:
  - p2-context-budget-spec
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
---

# P2 — Context Budget + Domain Leak: Spec del Parent (binding para P2-B)

- Entrada: [[80-agents/tools/context-budget/artifacts/p2-context-budget-design.md|p2-context-budget-design]] (P2-A), reconciliado contra el Conformance Harness (`80-agents/tools/conformance-harness/`) sin contradicciones factuales encontradas. Este spec es la única autoridad de implementación; lo que aquí no se fija, lo fija el diseño de P2-A.
- Principios: reuso del harness como librería (importar `rules` + helpers de `agents_os_conformance.py`; prohibido fork/copia de `rules.py`); KISS (stdlib Python 3.9+, determinista, read-only sobre el vault salvo `results/` propio); ninguna medición estimada sostiene FAIL; ningún finding del sistema se auto-corrige.

## 1. Decisiones del parent sobre ambiguities (A1-A9, vinculantes)

- A1 — Soft ceilings (M18): WARN-only. Ratificado: desviación de 3-6k / <1k / 1-3k produce WARN con cifras `estimated_tokens`; no existe autoridad para techo duro con FAIL.
- A2 — DEFAULT y cláusula de superficie: se codifica la lectura literal del harness (`domain_gate` con evidencia de tarea); el colapso ambiental a ARANEA se registra como WARN (Hallazgo 6) remitiendo al ADR pendiente. Prohibido inventar otra semántica.
- A3 — Nota VPN: clasificación ambigua (INFERRED). Autorizada en pack meli (Minimal Read 3); en escenarios aranea su aparición es WARN. No se corrige su frontmatter (sistema bajo prueba).
- A4 — Umbral de duplicación (M14): ratificado ≥3 líneas consecutivas normalizadas o ≥120 chars (normalización whitespace/puntuación/minusculas), declarado como heurística propia de la tool con su versión en el record. Veredicto máximo WARN (nunca FAIL).
- A5 — Superficie MCP (CTX-14/M17): SKIP por defecto. Con flag `--live`, la tool REUTILIZA el código de lectura de configs del harness (misma función; sin reimplementación). Nunca criterio de FAIL.
- A6 — Granularidad: archivo completo como unidad (paridad con harness). Body-only queda explícitamente fuera (YAGNI).
- A7 — `30-resources/aranea/00-index.md` y similares on-demand: no se cobran al pack base; sólo si el escenario los abre.
- A8 — Skills transversales: nunca cuentan como unrelated-domain aunque un registro diga "Vía meli-agent-dev" (la fila es puerta, no exclusividad). Confirmado neutral.
- A9 — Salida humana: una línea por escenario (`<ID> <VERDICT> <detalle corto>`) + una línea de baseline con `estimated_tokens` etiquetado visible + línea de counts. En `--json`, el resumen va a stderr (paridad con harness).

## 2. Métricas ratificadas

Se ratifican M01-M19 del diseño de P2-A con sus clases de confianza y métodos (tabla del diseño, sección 4, es normativa). Reglas duras de emisión:

- Campos de tamaño permitidos: `bytes`, `chars` (EXACT), `estimated_tokens` (chars//4 vía `_size`/`context_baseline` del harness, ESTIMATED). Prohibido emitir cualquier campo llamado `tokens` o afirmar tokens exactos. Toda aparición de `estimated_tokens` debe poder trazarse a la nota "chars/4, sin tokenizador de autoridad (C04)".
- Sets y conteos: EXACT vía transcripción (`rules.Session`, `opens_in_turn(n)` con el turno fijado antes de invocar, convención fix D1).
- Clasificaciones (dominio, duplicación, residuo potencial): EXACT dada la regla; INFERRED cuando la clasificación del archivo sea ambigua, siempre con la regla de interpretación en la evidencia.
- Métricas agregadas por escenario en `totals`: `always_load`, `scope_pack` por dominio, `cold_estimated_tokens`, `warm_delta`, `swap_estimated_tokens`, `unrelated_domain`, `deprecated_hot_path`, `duplicate_hot_path` — cada una con `{files, chars, bytes, estimated_tokens}` y `confidence`.

## 3. Escenarios ratificados

Se ratifican CTX-01..CTX-15 del diseño (sección 6) con ids, `reuses` y métricas tal como están definidos. Orden de ejecución obligatorio: pre-flight `RULES-FIDELITY-ANCHORS` (importado del harness) → CTX-15 baseline → CTX-01/02/03 → CTX-04/05/06 → CTX-07/08/09/10 → CTX-11 → CTX-12 → CTX-13 → CTX-14 (SKIP salvo `--live`). FAIL del pre-flight ⇒ todos los CTX en SKIP con motivo; FAIL de un CTX no corta los demás. Con `--scenario <ID>` el run es dirigido por el operador y NO aplica gate (paridad con harness).

## 4. Semántica de veredictos y confidence

- PASS / FAIL / WARN / SKIP con la semántica textual del README del harness. SKIP siempre con motivo. UNKNOWN nunca se convierte en PASS (queda SKIP o WARN con motivo).
- Un FAIL exige: autoridad inequívoca citada + métrica sustentante EXACT (o INFERRED cuando la prohibición es inequívoca y la única inferencia es la clasificación, dejando la duda como WARN separada). ESTIMATED jamás sostiene FAIL.
- Todos los WARN declarados por los audits del harness (Hallazgos 3, 4, 6, 7, 8, 9, 10, 11, 16, 17; C04, C09; DUAL-REGISTRY-DOMAIN-SYNC; modo ambiguo DEFAULT→dominio) se heredan como WARN por diseño y no degradan el veredicto.

## 5. Write scope de P2-B (paths permitidos, todo lo demás prohibido)

- `80-agents/tools/context-budget/context_budget.py` — entrypoint único (CLI: `--vault-root`, `--json`, `--scenario <ID>`, `--live`, exit code 0/1/2 análogo al harness).
- `80-agents/tools/context-budget/selftest.py` — pruebas de inyección/negativas locales (no toca canonical; fixtures temporales en tmp del sistema, nunca en el vault).
- `80-agents/tools/context-budget/README.md` — qué mide, cómo correrlo, qué NO mide, semántica, cómo agregar un escenario, limitaciones (esqueleto del README del harness).
- `80-agents/tools/context-budget/results/run-<timestamp>.json` — salida de runs.
- `80-agents/tools/context-budget/artifacts/p2-implementation-notes.md` — nota corta de implementación: decisiones tomadas, evidencia de verificación (corridas normal/negativa/malformed/SKIP/repeat), resultados de la suite ejecutada, limitations operativas.
- PROHIBIDO: modificar `rules.py` o cualquier archivo del harness; modificar autoridades, skills, memorias, proyecto, AGENTS.md; crear daemons/DB/dependencias externas; hardcodear cifras de baseline (siempre salen de `_size` en el run); persistir paths absolutos de máquina (resolver relativos a VAULT_ROOT; constitución regla 11).

## 6. Requisitos de verificación (gate antes de entregar)

P2-B debe demostrar con evidencia registrada en `p2-implementation-notes.md`: (1) caso normal — suite completa ejecutada con counts; (2) caso negativo — al menos una inyección controlada que dispare FAIL (p. ej. fixture temporal con pack cruzado) sin dejar rastro en el vault; (3) input malformado — archivo corrupto/faltante produce SKIP o FAIL motivado, nunca traceback abortando; (4) comportamiento SKIP — marker ausente (VAULT_ROOT falso vía `--vault-root`), pre-flight en rojo simulado, CTX-14 sin `--live`; (5) determinismo — dos runs consecutivos producen records idénticos salvo `run`/timestamp; (6) baseline explícito — `git_head` resuelto en VAULT_ROOT; (7) no mutación canónica — `git status` limpio de cambios fuera del write scope al terminar.

## 7. Output schema (machine-readable)

```json
{
  "run": "<timestamp>",
  "tool": "context-budget",
  "git_head": "<sha en VAULT_ROOT>",
  "fidelity_gate": "PASS|FAIL|SKIP",
  "scenarios": [
    {"id": "CTX-01", "reuses": ["COLD-DEFAULT"], "verdict": "PASS|FAIL|WARN|SKIP",
     "metrics": [{"name": "always_load_estimated_tokens", "value": 7108, "unit": "estimated_tokens",
                  "confidence": "ESTIMATED", "authority": "C04 + _size del harness"}],
     "evidence": ["..."], "skip_reason": null}
  ],
  "totals": {"always_load": {"files": 4, "chars": 28436, "bytes": 29990, "estimated_tokens": 7108, "confidence": "ESTIMATED"},
             "scope_pack": {"meli": {"files": 3, "chars": 8148, "bytes": 8471, "estimated_tokens": 2036, "confidence": "ESTIMATED"},
                            "aranea": {"files": 2, "chars": 4821, "bytes": 5040, "estimated_tokens": 1205, "confidence": "ESTIMATED"}}},
  "counts": {"pass": 0, "fail": 0, "warn": 0, "skip": 0},
  "ambiguities": ["A2 ..."],
  "thresholds": {"duplication": {"min_consecutive_lines": 3, "min_chars": 120, "version": 1, "max_verdict": "WARN"}}
}
```

- `totals.scope_pack` es ilustrativo: los valores SIEMPRE salen de `_size` en el run (jamás hardcodeados; drift esperable). `thresholds` queda registrado en cada record para comparabilidad entre versiones de la heurística M14.
- Compatibilidad futura `agents-os doctor`: records con `id`, `verdict`, `metrics[].confidence`, `authority` — suficiente para agregación sin re-parseo; no se crea abstracción compartida ahora (YAGNI).
