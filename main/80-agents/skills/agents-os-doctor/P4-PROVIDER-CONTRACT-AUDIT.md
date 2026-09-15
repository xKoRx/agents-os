---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
aliases:
  - phase 4 provider contract audit
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
created: "2026-09-14"
updated: "2026-09-14"
---

# PHASE 4 — Provider Contract Audit

## Propósito

Fijar el contrato real de integración de los cuatro providers antes de modificar el runtime de `agents-os-doctor`.

## Contenido

## Contratos observados

| Provider | CLI actual | JSON | Exit codes observados | Escritura actual | Runtime real 2026-09-14 |
|---|---|---|---|---|---|
| Structural | `--strict` | no | `0` sano; `1` HIGH o MEDIUM con strict | ninguna | <1 s |
| Conformance | `--layer`, `--scenario`, `--json`, `--vault-root`, `--no-live` | `scenarios[].state`, counts uppercase, baseline/context_baseline | `0` sin FAIL; `1` con FAIL; `2` input/root inválido | siempre escribe `results/` | 1.78 s |
| Context | `--vault-root`, `--json`, `--scenario`, `--live`, `--conformance-json` | `scenarios[].verdict`, counts lowercase, totals | `0` sin FAIL; `1` FAIL/fidelity FAIL; `2` input/root inválido | siempre escribe `results/` | 1.04 s |
| Canonical | `--vault-root`, `--json`, `--check`, `--category` | `checks[].verdict`, findings, counts lowercase | `0` sin FAIL; `1` con FAIL; `2` input/root inválido | siempre escribe `results/` | 1.26 s |

Los tres providers externos usan Python 3.9+ stdlib, imprimen JSON a stdout y resumen a stderr con `--json`. Conformance posee el único modelo de sesión (`rules.py`); Context y Canonical lo consumen y no deben forkearlo.

## Adapter mínimo autorizado

- Mantener `doctor.py` como único entrypoint y como autoridad de checks estructurales; exponer un runner estructural machine-readable dentro del mismo módulo, sin copiar checks.
- Agregar `--no-write` a Conformance, Context y Canonical. El agregador los invoca como subprocess secuencial con `--json --no-write`; así conserva aislamiento sin llenar `results/` en cada health check.
- Mapear el default no-live del Doctor a `--no-live` en Conformance; `--live` omite ese flag y se propaga sólo a Context. Canonical no recibe un flag inventado.
- Propagar `--vault-root` a todos. El provider estructural reconfigura su root antes de correr; los externos ya soportan el argumento.
- Timeout fijo de 30 segundos por provider: es >16× el runtime más lento observado y evita un subsistema de configuración. Timeout, JSON inválido, executable ausente o exit `2` se normalizan como `execution_status=ERROR` sin detener providers posteriores.
- Exit `1` con JSON válido significa `execution_status=OK` y un FAIL real del sistema. El agregador no interpreta stderr ni reescribe findings.
- La distribución debe incluir los cuatro archivos runtime externos (`agents_os_conformance.py`, `rules.py`, `context_budget.py`, `canonical_linter.py`); no incluye selftests, artifacts ni results.
- El registro federado vacío es una configuración válida del artefacto DEFAULT:
  ningún módulo puede indexar routers conocidos al importar; baselines enumeran
  sólo packs registrados y escenarios con fixtures ausentes declaran SKIP.

## Normalización mínima

- Structural: HIGH→FAIL, MEDIUM→WARN, LOW→INFO; LOW queda visible pero no cambia verdict ni `--strict`, preservando la política previa sin etiquetar un finding como PASS.
- Conformance: `state`; Context/Canonical: `verdict`. Se conservan los records crudos bajo `records` y sólo se proyectan counts, findings acotados y métricas de contexto.
- Context emite su pre-flight `RULES-FIDELITY-ANCHORS` como record y count normales. El agregador no inspecciona `fidelity_gate` para fabricar semántica.
- Overall: ERROR si algún provider no ejecuta; si todos ejecutan, FAIL > WARN > PASS > SKIP. `--strict` cambia sólo exit code y nunca el verdict emitido.
- Baseline Git se captura al inicio y al final desde el vault. Si no existe Git, ambos quedan `null` y `baseline_stable` queda `null`, nunca `true` inventado.

## Ownership y solapes

- Structural conserva paths/portabilidad, closed club always, skill registry/frontmatter/refs, secretos internos, continuidad y budget del startup.
- Conformance conserva cold/warm/switch/isolation y gating interno L0→L1/L2.
- Context conserva métricas estimadas e isolation; `estimated_tokens` no se renombra.
- Canonical conserva canonicalidad/deprecation/routing y CL-21. No hay deduplicación semántica cross-provider en V1.

## Fuentes

- `80-agents/skills/agents-os-doctor/PHASE-4-AGGREGATION-SPEC.md`.
- Los cuatro entrypoints ejecutados con `--help` y `--json` sobre el vault real el 2026-09-14.
