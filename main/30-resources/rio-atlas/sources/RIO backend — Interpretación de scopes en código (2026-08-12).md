---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url:
repo: melisource/rio-backend
path: <repo>/.fury + <repo>/src/main/** + <repo>/src/main/resources/application*.yml
author: Signals
published: 2026-08-12
captured: "2026-08-12"
license:
checksum:
supersedes:
superseded_by:
aliases:
  - rio-backend-scope-code-2026-08-12
  - Código de scopes backend RIO 2026-08-12
tags:
  - kind/source
  - tech/rio
  - project/scopes-rio
created: "2026-08-12"
updated: "2026-08-12"
---

# RIO backend — Interpretación de scopes en código (2026-08-12)

## Referencia

- **Origen resoluble:** repos backend RIO bajo `melisource`, resueltos mediante `~/fuentes/AGENTS.md`; paths relativos indicados en frontmatter.
- **Fecha de captura:** 2026-08-12.

## Alcance

- Implementación que interpreta `SCOPE`/`scope`, calcula perfiles Spring y conecta recursos por ambiente/segmento en [[rio-playmaker]], control planes, [[rio-materializer]] y [[rio-sdk-events]].
- Se revisaron `ScopeUtils`, `EnvironmentPostProcessor`, `application*.yml`, `.fury`, Dockerfiles y tests específicos de resolución de perfiles; documentación y specs se usaron sólo como contexto secundario.

## Notas de provenance

- El código prueba comportamiento soportado por la versión del checkout, no que cada scope desplegado use esa misma revisión. La columna de versión Fury permite detectar esa distancia y debe considerarse antes de afirmar comportamiento runtime exacto.
- Los repos no se copian al vault y no se persisten secretos ni configuraciones inyectadas por la plataforma.

## Lifecycle

- **Supersedes:** —
- **Superseded by:** —
