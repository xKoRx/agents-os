---
type: change_log
schema_version: 1
scope: session
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Meli]]"
project: "[[Zords — Human-First Technical Authoring]]"
application:
entities:
  - "[[Zords — Human-First Technical Authoring]]"
  - "[[human-first-technical-writing]]"
related:
  - "[[2026-08-26-zords-human-first-authoring-implemented]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-01-zords-human-first-synthesizer-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Human First en el synthesizer de Zords

## Cambio

- **Tipo:** refined
- **Archivo(s):** `zords/synthesizer.md` y `tests/synthesizer.spec.ts` en `local-agents-pipeline-cli`, branch `feature/zords-technical-authoring`.

## Motivo

- Hacer que el reporte final sintetizado ayude al reviewer a comprender y decidir, sin introducir otro runtime ni alterar el contrato de review.

## Resolución aplicada

- Se agregó una sección Human First al prompt bundled del synthesizer con orientación inicial, causalidad problema → mecanismo → consecuencia, progresión, recognition over recall, certeza epistemológica y siguiente paso humano.
- Se preservaron el retorno de JSON válido, los headings `Findings`/`Notas adicionales` y la ubicación `zords/synthesizer.md` fuera del registry `zords/agents`.
- Se agregaron tests deterministas del contrato editorial y del aislamiento de layout.

## Validación

- `npm test -- --runInBand`: 34 suites y 460 tests passing; cobertura global 95.26% statements y 95.35% lines.
- `npm run build`, `npm run dist` y `git diff --check`: pasan.
- `npm run lint -- --no-warn-ignored`: 0 errores; permanecen 11 warnings preexistentes en `tests/add.spec.ts` y `tests/cli.spec.ts`.
- La skill `release-process` no pudo inicializar su MCP en este entorno; se ejecutaron los checks locales equivalentes y todos pasaron.
- El reindex Graphify quedó bloqueado por el gate global del vault: 25 errores y 6 warnings fuera del alcance de Zords; no se modificó esa deuda.

## Rollback

- Retirar la sección `Redacción Human First` de `zords/synthesizer.md` y `tests/synthesizer.spec.ts`; no requiere migración del runtime ni de los contratos JSON.
