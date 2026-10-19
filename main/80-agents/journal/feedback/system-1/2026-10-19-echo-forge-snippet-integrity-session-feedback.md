---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
confidence: verified
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
  - area/echo
---

# Feedback — Echo Forge / integridad de snippets / cierre

## Pain Pattern Candidate

- **Deploy con éxito falso:** `set -e` no abortó al fallar `cp` en `cp && mv`; un sello del bundle no reemplaza verificar el **source live**. Resultado: JAR S02 + snippet viejo, y SQX recompiló el viejo. Regla transversal de QA: preflight del directorio destino, abort explícito por operación, readback byte-exacto de cada superficie y prueba negativa de permisos; no declarar `DEPLOY OK` antes de eso.
- **Clase efectiva ≠ clase instalada en JAR:** SQX 144 headless recompila snippets; exigir autoridad source↔clases internas↔JARs↔cache y gate antes de despachar. El gate tiene que estar conectado a la operación real, no sólo existir como script.
- **Deriva de enfoque del Manager:** no mezclar certificación técnica Forge con rentabilidad/trades de CFX de prueba. Evitar nuevos E2E/auditorías generales cuando el fallo ya tiene RCA reproducida; registrar deuda de performance separadamente.

## Lo que funcionó

- Sellos `before/after`, forensic de ownership y `ctime`, reproducción candidate-local sin SQX activo, comparación de Zeus/Kronos/Hera y resguardo de campañas largas.
- Evidencia canónica en `artifacts/ECHO-FORGE-SNIPPET-INTEGRITY-P0/`.

## Mejora sugerida

- Reforzar la checklist de plugin: deploy sólo con verificación live completa + gate de identidad versionado + rollback probado con los permisos reales, sin tocar campañas activas.
