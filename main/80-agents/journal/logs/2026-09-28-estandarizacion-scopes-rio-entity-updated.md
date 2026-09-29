---
type: change_log
schema_version: 1
scope: session
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application: "[[ads-signals-frontend]]"
entities:
  - "[[Estandarización de Scopes RIO]]"
related:
  - "[[Descripción PR — adminfrontend-rules]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/scopes-rio
---

# Cambio de ingreso Signals alpha-nonprod

## Cambio

- **Tipo:** updated
- **Archivo(s):** `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md`; `10-projects/Meli/Estandarización de Scopes RIO/Descripción PR — adminfrontend-rules.md`; repo `melisource/adminfrontend-rules` (`subdomains/frontend.conf`, `test/cases.sh`); draft PR [#11182](https://github.com/melisource/adminfrontend-rules/pull/11182).

## Motivo

- El usuario pidió que `signals.adminml.com` enrute `meliLab=alpha-nonprod` al scope frontend alpha como parte de la iniciativa de estandarización de scopes RIO.

## Fuentes usadas

- Solicitud del usuario y captura del bloque `Signals Admin`.
- Código base en `subdomains/frontend.conf` y casos hermanos de Signals en `test/cases.sh`.
- Nota del proyecto y evidencia registrada el 2026-09-25 sobre el scope `alpha-nonprod` y el ingreso actual.
- Checks de PR #11182: `continuous-integration`, `workflow` y `Nginx Rule Check` pasaron; `Edge Authentication Workflow` devolvió `NOT_READY` por Deny by Default.

## Resolución aplicada

- Se agregó una condición exacta para `meliLab=alpha-nonprod` hacia `alpha-nonprod.ads-signals-frontend.melifrontends.com`, junto con un test `all_fe` que sigue los casos actuales de Signals.
- Se abrió el PR #11182 desde `feature/signals-alpha-nonprod-ingress` a `master` en estado draft, con la descripción guardada junto al proyecto.
- El gate Edge Authentication queda pendiente: el workflow clasifica la nueva URL como pública aunque el guard `X-Public` está a nivel `server`, fuera del `location` que inspecciona. El validador devuelve `NOT_READY` para tráfico público. Shield 4357 es el ticket para aplicar un esquema Edge AuthN si ese tráfico debe aceptarse; su necesidad para esta ruta privada sigue por confirmar.

## Validación

- `git diff --check` pasó al tratar CRLF como fin de línea en el archivo Nginx.
- `continuous-integration`, `workflow` y `Nginx Rule Check` de GitHub Actions: PASS.
- `Edge Authentication Workflow`: FAIL (`NOT_READY`, `Pool has Deny by Default schema - rejects public traffic`); el workflow indica que el merge está bloqueado.
- `make test` no se ejecutó localmente; el flujo de acceso autenticado por `signals.adminml.com` sigue sin validar.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos.

## Rollback

- Revertir el commit `ae67565` elimina la condición alpha-nonprod y el caso de regresión; el PR puede cerrarse sin merge.
