---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-01-release-authority-stale-manifest-rollback]]"
  - "[[2026-09-01-release-version-authority]]"
aliases: []
confidence: high
load_policy: when_echo_forge_loaded
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - scope/project
  - project/echo-forge
---

# Continuity — C3 release authority RCA

## Continuidad

- C3-A PASS / CLOSED en `441ea061`. C3-B BLOCKED / CLOSED. No repetir C3-A. No consumir CERT-A/B.
- Autoridad publicada actual: MinIO `deploy/worker/sqx/manifest.json` = `0.2.78` (etag `d83bc580…`, sha256 `c4102e34…` = git). Flota Zeus/Hera/Kronos/Windows CURRENT = `0.2.78`.
- No reusar `0.2.79`. Prefix remoto ya tiene historia divergente (Aug-29 vs C3 overwrite). Stagers conservan el árbol Aug-29 y no re-descargan.
- No restaurar `deploy/manifest.json` git `0.2.78` con deployer-watcher vivo: eso republica y degrada.
- No borrar prefixes `0.2.79`–`0.2.83` ni `9.9.x`.

## Señales de carga

- published `0.2.78` < remote_max `0.2.x` = `0.2.83` ⇒ INCONSISTENT_RELEASE_AUTHORITY. AUTO no debe publicar.
- `mc` ausente en el host de release. `/opt/symphony/CURRENT` es leftover Bash (`9.9.11`), no autoridad.
- Windows stager: `MINIO_ENDPOINT=http://192.168.31.92:9000`, bucket `deploy`, key `worker/sqx/manifest.json` (env de máquina). RC-E cerrado en Windows. Linux `/etc/stager/stager.env` sigue 0640 no leíble; conducta y hashes alineados.
- Activate flota: `origin=requested` 0.2.83→0.2.78, `rollback_of=null`. El stager siguió el manifest publicado, no un rollback etiquetado.

## Próxima acción

- ECHO-FORGE-RELEASE-AUTHORITY-STDOUT-ISOLATION-FIX-NORMAL **PASS / CLOSED**: SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` elimina `RESPUESTAAAA`; Symphony `02fabffe958854ab30e017301a8c30aaada527ac` aísla stdout del CLI y pinnea `v0.0.0-20260902001205-c85594440f67` en root/sqx/deployer; ambos `HEAD == origin/master`.
- Acceptance real read-only pasó sin ACK (exit 1, JSON único, `INCONSISTENT`, candidate `0.2.84`), con ACK exacto (exit 0) y target `0.2.84` (exit 0, `AVAILABLE`); published permanece `0.2.78`, no se publicó release ni se consumieron identities Campaign/CERT.
- NEXT EXACT: `ECHO-FORGE-C3-RELEASE-CONVERGENCE-RECOVERY-NORMAL` desde Symphony `02fabffe958854ab30e017301a8c30aaada527ac` y SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`; no repetir C3-A ni usar test injection.
