---
type: known_error
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
aliases: []
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
---

# 2026-09-01-stager-version-collision-release-not-converged

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Un manifest se confirma, pero los nodos conservan un binario anterior; la versión destino ya existía con bytes distintos.

## Causa

- Parcial: el prefix `0.2.79` de 2026-08-29 existía y el stager no re-descarga un `releases/0.2.79` local con hash distinto.
- Completa (esta auditoría): AUTO desde manifest git `0.2.78` + overwrite MinIO de `0.2.79` + republicación del manifest `0.2.78` 79s después. Ver [[2026-09-01-release-authority-stale-manifest-rollback]].

## Impacto

- El código nuevo no queda activo; la certificación física contra ese código debe detenerse.

## Detección

- Comparar proceso activo, `CURRENT`, SHA256 y timestamp en cada nodo; la presencia del directorio no basta.

## Mitigación

- Marcar BLOCKED/CLOSED, preservar evidencia y resolver la asignación de versión por el release canónico. No parchear fuente ni crear fixtures DB manuales durante el bloqueo.
- Mitigación de fuente completada en `xKoRx/symphony` commit `ee61d3d0b3b53416e80b231522342482322e556e`: AUTO fail-closed con remote/local line max y ACK exacto; prefixes ocupados y bytes divergentes nunca se sobreescriben; manifest downgrade falla cerrado.

## Evidencia

- El artefacto local C3 `0.2.79` difirió del remoto preexistente; Linux y Windows quedaron activos en `0.2.78`.
