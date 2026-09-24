---
type: change_log
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
related:
  - "[[Descripción PR — rio-playmaker — Slice 5]]"
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
---

# Nueva variante deployer de F5 — SIG-616

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/Descripción PR — rio-playmaker — Slice 5.md`

## Motivo

- Las notas de F5 sólo registraban las versiones mock committer y viewer, pese a que inactivar requiere `DEPLOYER_AND_UP`.

## Fuentes usadas

- `feature/sig-616-auth-p5-deployer-test3-v27@d5ef6d48c` incorpora la variante test3 de rol deployer; Fury terminó exitosamente `0.1.23-p5-deployer-allowed` (#1743) en `FINISHED`.

## Resolución aplicada

- Se agregó la versión especializada al estado del proyecto y a su descripción local de PR. El mock queda restringido al profile `test3`; no cambia la autorización productiva ni se desplegó.

## Validación

- Evidencia: commit y rama local/remota, código `ComponentInactivationServiceImpl` que exige `DEPLOYER_AND_UP`, resultado exitoso de `fury create-version`, watcher y `fury list-versions`. Build #1743 `FINISHED`; sin deploy ni smoke remoto.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir únicamente las notas del proyecto y retirar este change log si se revierte la documentación. No borrar ni deshabilitar la versión Fury desde este registro.
