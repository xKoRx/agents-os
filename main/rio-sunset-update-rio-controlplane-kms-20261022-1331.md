---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-controlplane-kms]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-controlplane-kms

**Desenlace: ACTION_REQUIRED** — El código y los otros scopes ya están corregidos; falta rollout productivo, fuera del deploy permitido por esta skill.

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| com.fasterxml.jackson.core/jackson-databind | 6508087,6508032,6507463 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| com.fasterxml.jackson.core/jackson-core | 6552766 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |

### Scopes afectados

Solo prod conserva Jackson 2.21.5 (artefacto 2026.9.23-rc-2).

### Cambio, PR y validación

- Ruta: El código y los otros scopes ya están corregidos; falta rollout productivo, fuera del deploy permitido por esta skill.
- PR: No corresponde: no se modificó código.
- SHA completo: `1168240a4204c536544c2b36b796171b89233455`.
- Validación nativa: runtimeClasspath de Gradle confirma las versiones efectivas; no se modificó código..
- Build: `202610.6.1-rc-3 (existente; no se creó otro)` — Build existente FINISHED; catálogo confirma Jackson corregido en todos los scopes salvo prod.

### Deploy a test

No corresponde redeploy de test: todos los scopes afectados son productivos. prod requiere una persona; no se pidió scope de test ni se creó build adicional.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-controlplane-kms/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-controlplane-kms` y evidencia Gradle del SHA indicado.
