---
type: known_error
schema_version: 1
scope: tool
created: 2026-09-14
updated: 2026-09-14
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[local-agents-pipeline-cli]]"
related:
  - "[[signals-code-review]]"
  - "[[signals-code-review-runbook]]"
aliases:
  - Zord false green
  - Zord empty success
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/tool
  - tech/zord
---

# Zord reporta éxito vacío cuando todos los reviewers fallan

## Síntoma

- `zord assemble --output-json` puede terminar con exit code `0` y `{"zords":[]}` aunque todos los reviewers hayan fallado por autenticación, presupuesto o timeout.
- Con `--quiet`, el consumidor puede no ver la causa y confundir ausencia de resultados con una revisión limpia.

## Causa

- El orquestador excluye resultados fallidos del array serializado y la ruta `--output-json` no convierte el fallo total en exit no exitoso ni incluye errores estructurados.

## Impacto

- Un gate automatizado o una revisión humana puede aceptar un falso `PASS` sin que haya corrido ningún reviewer válido.

## Detección

- Exigir al menos un resultado esperado y comprobar que cada reviewer convocado tenga `{ reviewer, findings, summary }`; no usar sólo el exit code.
- Si el array queda vacío, repetir sin `--quiet` únicamente para diagnosticar y revisar mensajes `Agent failed`, `error_max_budget_usd`, auth o exit `124`.

## Mitigación

- Tratar cero resultados válidos como `BLOCKED`, conservar stderr diagnóstico y no sintetizar/publicar un veredicto.
- Antes de ejecutar, validar provider/auth, presupuesto, timeout y que la base del diff coincida con el PR; `origin/HEAD` puede apuntar a una rama de feature.

## Evidencia

- Observado el 2026-09-09 con siete fallos de OAuth y nuevamente el 2026-09-14 con límites de USD 0,50 y dos timeouts del Zord global Codex a 300 s.
- El segundo smoke de 2026-09-14 usó el diff exacto del PR #1126 (1.929 líneas) y aun así devolvió exit `0` con `zords: []` tras exit interno `124`.
