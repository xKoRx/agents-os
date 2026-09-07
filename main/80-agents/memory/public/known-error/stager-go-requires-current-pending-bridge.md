---
type: known_error
scope: application
created: 2026-08-09
updated: 2026-08-15
area: "[[Echo]]"
project: "[[Stager - Symphony Publisher Integration]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
  - "[[echo-forge]]"
related:
  - "[[Stager]]"
aliases:
  - stager go current symlink bridge
  - releases 700 kor worker
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - area/echo
  - app/stager
  - tech/deployment
---

# Stager Go no alimenta solo al worker Bash/systemd

## Síntoma

- Tras un `staged` exitoso del Stager Go bajo `/opt/symphony`, `symphony-worker` queda en `activating` o no arranca.
- El binario vive en `releases/<version>/` pero el unit sigue usando `/opt/symphony/current/bin/...`.
- `PENDING` del worker no aparece en `/var/lib/symphony/PENDING`.

## Causa

- El worker productivo resuelve el entrypoint por el symlink `current` y observa `PENDING_FILE=/var/lib/symphony/PENDING`.
- El Stager Go escribe `releases/<version>`, `CURRENT` y `PENDING` bajo `STAGER_ROOT`, sin mantener el symlink ni el path legacy de PENDING.
- Además crea `releases/<version>` como `0700` owned by `symphony`, mientras el unit corre como `User=kor`.

## Impacto

- Cutover incompleto: staging OK, runtime no actualiza o no puede ejecutar.
- Riesgo de flota en PENDING sin worker sano.

## Detección

- `systemctl is-active symphony-worker` ≠ `active` tras stager.
- `readlink -f /opt/symphony/current` no apunta a `releases/<CURRENT>`.
- `ls` de `releases/<version>/bin` falla con Permission denied para `kor`.

## Mitigación / Fix

- Stager (2026-08-15) hace `chmod 0755` del release y el runtime lee `releases/` + `state/CURRENT` sin symlink `current`. Ver [[stager-staged-without-runtime-request]].
- Histórico: wrapper `/usr/local/sbin/symphony-stager-go` (`ln -sfn`, copia PENDING, `chmod -R a+rX`).

## Prevención

- Toda release nueva debe quedar traversable por el user del runtime (`kor`), o el unit debe correr como el usuario que stagea.
