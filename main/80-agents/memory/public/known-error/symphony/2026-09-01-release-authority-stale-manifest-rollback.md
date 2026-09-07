---
type: known_error
schema_version: 1
scope: project
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[Stager]]"
related:
  - "[[2026-09-01-release-version-authority]]"
  - "[[2026-09-01-stager-version-collision-release-not-converged]]"
aliases:
  - AUTO bump 0.2.79
  - manifest rollback 0.2.78
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
---

# 2026-09-01-release-authority-stale-manifest-rollback

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- AUTO de `deploy_release.sh` elige `0.2.79` aunque existan prefixes remotos `0.2.80`–`0.2.83` y una certificación física previa en `0.2.83`.
- El deployer confirma `Manifest publicado` `0.2.79` y minutos después la flota (y el manifest publicado) vuelven a `0.2.78`.

## Causa

- El manifest git-tracked queda congelado en `0.2.78` (`baadc35`). `mc` no está instalado, así que AUTO no lee MinIO y bumpea desde `.version` local.
- AUTO no consulta prefixes remotos `worker/sqx/<semver>/`; la protección de colisión es solo filesystem local `deploy/<version>/`.
- Restaurar `deploy/manifest.json` al blob git `0.2.78` con `deployer-watcher` vivo republica ese manifest (MD5 `d83bc580…`) y degrada la autoridad publicada.

## Impacto

- La flota elegible (Zeus/Hera/Kronos/Windows) queda en `0.2.78` (`vcs.revision=5e93c7cd`) en vez del último certificado `0.2.83`.
- Un prefix `0.2.79` preexistente (2026-08-29) no se re-stagea: el stager hace fail-closed por hash mismatch y nunca activa el artefacto C3.

## Detección

- Comparar `worker/sqx/manifest.json` (etag/mtime/version) contra `REMOTE_MAX` de `0.2.x` y contra `CURRENT` de `/opt/stager` y `C:\ProgramData\Stager`.
- En journal `stager.service`: `installed artifact "bin/symphony" failed integrity verification` seguido de republish `0.2.78`.

## Mitigación

- No reusar `0.2.79`. No borrar prefixes históricos. No republicar `0.2.78` a propósito.
- Fix de `deploy_release.sh`: gate remoto + fail-closed si `published < remote_max(0.2.x)` + no overwrite divergente. Luego release `0.2.84` desde `441ea061` sin restaurar el manifest git stale.

## Evidencia

- Manifest MinIO actual: version `0.2.78`, etag `d83bc58016c61e6bd6d1be3163d797ca`, mtime `2026-09-01T19:14:35Z`, sha256 `c4102e34…` = git HEAD.
- Deployer: `0.2.79` publicado `19:13:13Z`; `0.2.78` republicado `19:14:32Z`.
- Stager Zeus: integrity fail `15:13:41`/`15:14:18`; CURRENT `0.2.78` a `15:15`.
- Linux Zeus/Hera/Kronos: `ACTIVATION.json` `origin=requested` `from=0.2.83` `to=0.2.78` `phase=committed` `rollback_of=null`; symphony activo SHA256 `e15aab9f86d68f9e17b2de8d2f4b510280d6d4564e435b56e52a709652a51292` idéntico; 0.2.79 en disco `692f8c21…` (Aug-29), no C3.
- Windows `C:\ProgramData\Stager`: mismo activate `2b52e8ba…` 19:15:01Z; worker SHA256 `09B0AC09…`; 0.2.79 disco `D8F285F7…` size 36397056. Env máquina: `MINIO_ENDPOINT=http://192.168.31.92:9000` `STAGER_BUCKET=deploy` `STAGER_MANIFEST_KEY=worker/sqx/manifest.json` — mismo store que deployer. RC-E Windows refutado con config, no solo conducta.
