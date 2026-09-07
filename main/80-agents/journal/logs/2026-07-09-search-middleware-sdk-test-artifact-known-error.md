---
type: change_log
scope: integration
created: 2026-07-09
updated: 2026-07-09
entities:
  - "[[search-middleware]]"
  - "[[java-polycard-sdk]]"
related:
  - "[[2026-07-09-search-middleware-sdk-test-artifact-not-published]]"
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - app/search-middleware
  - integration/maven
---

# Change log — SDK de prueba no publicada

- Change type: created
- Changed file: `80-agents/memory/public/known-error/search-middleware/2026-07-09-search-middleware-sdk-test-artifact-not-published.md`
- Evidence: `compileJava` no resolvió `0.0.1-new-title-motors`; publicación local y tests focales sí pasaron.
- Duplicate check: revisadas memorias internas de migración Single View y conocidos errores existentes; no había nota equivalente para este artefacto.
- Reason: futuros agentes deben diagnosticar primero disponibilidad Maven/Fury antes de depurar código Java.
