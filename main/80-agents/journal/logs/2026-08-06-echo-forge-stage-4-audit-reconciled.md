---
type: change_log
scope: session
created: 2026-08-06
updated: 2026-08-06
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
related: []
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
  - area/echo
  - project/echo-forge
---

# Echo Forge — reconciliación de auditoría de Etapa 4

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/Echo Forge.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md`
- **Antes:** EF-G29 estaba deprecado y EF-G31 diferido; el roadmap sólo exigía EF-G30, EF-G32 y un smoke.
- **Después:** EF-G29 y EF-G31 vuelven al camino bloqueante. EF-G30 y EF-G32 se mantienen en progreso porque sus cambios no están integrados ni desplegados. Se añadió la recuperación de evidencia runtime antes del smoke y la cuarentena histórica.

## Motivo

- La identidad declarada de la wave procesada es `NDX/H1`, mientras sus cuatro templates `.cfx` contienen `XAUUSD_darwinex`; el re-retest también contiene un chart D1.
- El código no contiene `PatchChartIdentity` ni `IDENTITY_MISMATCH`.
- El fail-closed de TradeList, timezone, mapeo de variant y ruta de salida están sólo como modificaciones locales; `HEAD` sigue en `8e2f2dd`.

## Fuentes usadas

- Informe de auditoría entregado por el usuario el 2026-08-06.
- `symphony/input/processed/20260805_231914_*` y sus XML internos.
- `symphony/specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.5–10.9.
- `git status`, `git log`, búsqueda de símbolos y `git diff --check` en `symphony`.

## Resolución aplicada

- **Conflicto:** hecho canónico obsoleto entre la decisión operativa de 2026-08-04 y la evidencia del input procesado posterior.
- **Resolución:** la evidencia directa del artefacto ejecutable prevalece para el cierre de Etapa 4; el proyecto no puede tratar los fixtures como inocuos mientras una wave los publica bajo identidad NDX.
- La igualdad entre `retester_test.cfx` y `reretester_test.cfx` queda registrada como observación, no como gap nuevo: la diferenciación relevante es la estrategia de entrada después de Robust Run y debe verificarse en el output SQX.

## Validación

- Hashes y XML de los cuatro `.cfx` contrastados; `retester_test.cfx` y `reretester_test.cfx` tienen el mismo SHA-256.
- `git diff --check` pasó para los cambios locales de TradeList.
- `go vet ./activities/worker/... ./core/runtime/...` pasó.
- `go test -race -cover` y `go test -cover` no pudieron compilar por un problema local de Go: faltan paquetes `testmain` en `runtime/coverage`; no se interpreta como test verde.
- No se modificó el repositorio `symphony`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, credenciales, paths locales ni memoria interna.

## Rollback

- Revertir únicamente las dos notas de proyecto y este log si una ejecución posterior demuestra, con `.sqx` y trazas runtime, que la identidad efectiva no provino de esos `.cfx`.
