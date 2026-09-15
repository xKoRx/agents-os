---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
related:
  - "[[agents-os-doctor]]"
aliases:
  - Phase 4 adversarial handoff
tags:
  - kind/doc
created: "2026-09-14"
updated: "2026-09-14"
---

# PHASE 4 — Handoff de verificación adversarial

## Propósito

Permitir que un agente fresco intente invalidar la implementación del Doctor
unificado. No aceptar este reporte por autoridad: ejecutar los comandos y leer
los contratos reales.

## Contenido

## Alcance implementado

- Entry point único: `80-agents/skills/agents-os-doctor/scripts/doctor.py`.
- Agregación delgada: `scripts/aggregate.py`; Structural queda in-process y los
  otros tres providers corren como subprocess secuenciales.
- Adapters `--no-write` en Conformance, Context y Canonical; comportamiento
  default de cada provider preservado cuando se ejecuta por separado.
- Envelope con ejes separados `execution_status` y `verdict`; exit global
  `0/1/2`; `--strict` no muta records.
- Resumen humano acotado a cinco findings y detalle completo con `--json`.
- Distribución de los cuatro runtimes externos mediante `sources.list`.
- Registro federado vacío soportado: baseline sólo DEFAULT y escenarios scoped
  Meli/Aranea en SKIP motivado, sin exportar sus paquetes.

## Evidencia reproducida por el implementador

```text
Doctor selftest:       14/14 PASS
Context selftest:      21/21 PASS
Canonical selftest:     9/9 PASS
Registry selftest:      0/1/>1 PASS
aggregate.py coverage: 91.0%
source Doctor:          execution OK / verdict FAIL / exit 1
built DEFAULT Doctor:   execution OK / verdict FAIL / exit 1
source mutation:        Markdown y provider results sin cambios
core build:             196 canonical / 15 authored / 37 skills /
                        7 exclusions / 44 materialized / validation passed
```

Los `FAIL` reales no son un fallo de la implementación: fuente y export tienen
findings Conformance/Canonical que el Doctor debe preservar. El criterio es que
sean `execution_status: OK`, no volverlos verdes.

| Entorno | Structural | Conformance | Context | Canonical |
|---|---|---|---|---|
| Fuente | PASS `1/0/0/0` | FAIL `5/3/1/17` | WARN `8/0/7/1` | FAIL `8/5/8/0`, 1295 findings |
| Core DEFAULT | PASS `1/0/0/0` | FAIL `5/1/1/19` | WARN `2/0/1/13` | FAIL `15/2/3/1`, 201 findings |

Cada tupla es `pass/fail/warn/skip`. En ambos casos el overall esperado es
`execution_status: OK`, `verdict: FAIL`, exit `1`.

## Ataques obligatorios

1. Buscar business logic de providers copiada dentro de `aggregate.py`.
2. Forzar FAIL y ERROR tempranos; confirmar que providers posteriores corren.
3. Inyectar JSON inválido, timeout, exit 2 y exit/count contradictorio; deben ser
   `execution_status: ERROR`, verdict no fabricado y exit global 2.
4. Confirmar que `SKIP`/ausencia de dominio nunca se transforma en PASS.
5. Comparar records crudos con la proyección normalizada y buscar pérdida de
   PASS/FAIL/WARN/SKIP, evidence o confidence.
6. Generar más de 1000 findings; el texto debe mostrar cinco como máximo y JSON
   debe conservar el detalle.
7. Ejecutar normal/strict/component/live; strict sólo cambia exit code y live
   no debe escribir Markdown ni `results/`.
8. Mover el Git HEAD entre baseline start/end en un fixture y exigir
   `baseline_stable: false`; sin Git debe ser `null`.
9. Comparar todos los checks estructurales previos con `run_structural()` para
   detectar capacidades perdidas.
10. Construir un core limpio con registro vacío y correr allí el Doctor. Ningún
    provider puede importar paquetes Meli/Aranea ni terminar ERROR.
11. Registrar un dominio sintético único y otro ambiguo; validar routing
    `0 → DEFAULT`, `1 → router`, `>1 → fail-closed` sin hardcodes nuevos.
12. Verificar que `--no-write` sea opt-in: providers solos aún escriben por
    defecto y el Doctor nunca lo hace.

## Findings del primer challenge y resolución

- **LOW etiquetado PASS:** corregido a `status: INFO`. Sigue en records,
  `finding_count`, métrica y contador humano; no es accionable ni bloquea
  `--strict`, preservando la semántica anterior explícitamente.
- **Fidelity gate duplicado en el agregador:** eliminado. Context emite
  `RULES-FIDELITY-ANCHORS` como primer record y lo cuenta exactamente una vez;
  el Doctor ya no lee `fidelity_gate`.
- **Primer Doctor del core en FAIL:** decisión explícita del slice. Se preserva
  `SCHEMA-VALIDATOR-GREEN` como finding real del artefacto; PHASE 4 no lo corrige
  ni lo silencia. La remediación de onboarding queda fuera de esta aceptación.

## Comandos mínimos

```bash
python3 80-agents/skills/agents-os-doctor/scripts/selftest.py
python3 80-agents/tools/conformance-harness/registry_selftest.py
python3 80-agents/tools/context-budget/selftest.py
python3 80-agents/tools/canonical-linter/selftest.py
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py --json
python3 30-resources/agents-os/core-export/build-core.py /tmp/agents-os-p4-review
python3 /tmp/agents-os-p4-review/80-agents/skills/agents-os-doctor/scripts/doctor.py --json --vault-root /tmp/agents-os-p4-review
```

## Hallazgo corregido durante P4-C

El primer build DEFAULT falló con `KeyError: 'meli'` al importar Conformance:
`NOT_LOAD_DEFAULT` y los baselines indexaban routers Meli/Aranea al cargar el
módulo. Se corrigió con packs dinámicos y requirements por escenario. El test
`test_portable_default_providers_skip_absent_domains_without_error` debe fallar
si reaparece esa dependencia.

## Criterio de cierre

P4-D sólo pasa si el verifier reproduce los resultados o entrega findings
accionables con archivo/línea y prueba negativa. No auto-corregir durante el
challenge; devolver veredicto `READY`, `READY_WITH_FINDINGS` o `NOT_READY`.

## Veredicto final

**`READY` — 2026-09-14.** El verifier reprodujo ambos fixes de la primera
ronda: LOW conserva severidad y se normaliza como `INFO` sin alterar verdict ni
strict, y el fidelity gate pertenece exclusivamente a Context y aparece una
sola vez. También reprodujo Doctor 14/14, Context 21/21, Canonical 9/9,
registry 0/1/>1, build `196/15/37/7/44`, cuatro providers en
`execution_status: OK` tanto en fuente como en core DEFAULT y ausencia de
mutaciones por hash. P4-D queda cerrado sin findings abiertos.

## Fuentes

- `PHASE-4-AGGREGATION-SPEC.md`.
- `P4-PROVIDER-CONTRACT-AUDIT.md`.
- `scripts/aggregate.py`, `scripts/doctor.py`, `scripts/selftest.py`.
- Entry points de Conformance, Context y Canonical.
