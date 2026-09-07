---
type: known_error
schema_version: 1
scope: application
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
  - "[[Symphony]]"
related:
  - "[[stager-go-requires-current-pending-bridge]]"
  - "[[symphony-deploy-release-go-stager-cutover-gap]]"
aliases:
  - stager staged sin Request
  - state CURRENT no se actualiza
  - MkdirTemp 0700 kor
confidence: verified
source_session: 37e19434-4324-445e-bef5-3aaf7a1e25e8
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - app/stager
  - tech/deployment
---

# stager-staged-without-runtime-request

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `stager` imprime `staged` y deja `releases/<ver>` + raíz `CURRENT`/`PENDING`, pero el proceso worker sigue en la release anterior.
- `lstat .../releases/<ver>/bin: permission denied` si el runtime corre como otro usuario.

## Causa

- `cmd/stager` cableaba `Coordinator.Recover` y no `Coordinator.Request()` tras stage; el runtime lee `state/CURRENT`, no el `CURRENT` de raíz.
- `os.MkdirTemp` deja el árbol en `0700`; `bin/` sí es `0755`.
- `systemctl restart` bloqueaba el oneshot (`TimeoutStopSec=infinity`) y `User=stager` no tenía polkit para `stager-runtime.service`.
- Un `ACTIVATION` committed de una versión vieja con `state/CURRENT` adelantado a mano fallaba Load (`committed activation requires CURRENT target`).

## Impacto

- Un E2E puede completar contra el binario viejo si alguien alinea `state/CURRENT` a mano, o no cortar nunca si nadie lo hace.

## Detección

- Comparar `state/CURRENT` vs raíz `CURRENT` vs `ps` del entrypoint bajo `releases/`.
- Journal de `stager.service`: `staged` seguido de worker sin restart.
- Mode del directorio `releases/<ver>` distinto de `0755`.

## Mitigación

- Tras stage, `Activate` → `Request` bajo lock; `chmod 0755` del release; `systemctl --no-block restart`; pending = exit 0; supervisor adopta `state/CURRENT` en caliente; polkit acotado a `stager-runtime.service`.
- Load permite drift committed/`CURRENT` para no tumbar el oneshot.

## Evidencia

- 2026-08-14/15: `9.9.11` staged, worker en `0.2.42` hasta cutover manual; oneshot `noop` en Zeus/Hera/Kronos Linux y Windows tras el hotfix.
