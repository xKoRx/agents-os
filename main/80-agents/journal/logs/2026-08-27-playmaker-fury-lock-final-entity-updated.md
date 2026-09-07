---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
related:
  - "[[Descripción PR — rio-playmaker — Hotfix doble dispatch]]"
  - "[[2026-08-27-playmaker-fury-lock-orchestration-session-feedback]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-27-playmaker-fury-lock-orchestration-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Playmaker Fury Lock — actualización final de entidad

## Cambio

- **Tipo:** updated.
- **Archivo:** `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`.

## Resolución

- Se reemplazó la barrera del avance por Fury Lock en `684138b623fa4a33ca2856faae30e217f18217da`; `565059ed49a0dfe5f9b0578674004cd7fb7240b8` agrega la cobertura dirigida exigida por el gate remoto. Ambos están pusheados en la rama del PR #1079.
- El TTL se restringió a 1–7 segundos, sin renovación, por decisión explícita del owner.
- Las pruebas obligatorias verifican 2 dispatches sin exclusión y 1 con lock compartido. La suite final y `check` locales pasan; el body nuevo se publicó en GitHub.

## Blocker externo

- El check remoto `dependencies` bloquea `com.mercadolibre:lockclient:3.0.1` por deprecación. Esa es la versión exigida por la referencia controlada; no se crea `0.0.11-listener-lock` ni se cambia compatibilidad sin autorización o decisión técnica explícita.

## Validación

- `./gradlew test jacocoTestReport --no-daemon`: 3.237 tests, 0 fallas, 0 errores, 2 skipped.
- `./gradlew check --no-daemon`: PASS.
- CI de Java y code coverage: PASS; `dependencies`: FAIL por el bloqueo descrito.
- `graphify-obsidian update`: no reindexó por 13 errores y 6 advertencias de frontmatter fuera de este proyecto; no se corrigieron fuera de alcance.
