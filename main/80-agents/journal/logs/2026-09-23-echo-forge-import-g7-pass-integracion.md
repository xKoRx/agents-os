# change_log — 2026-09-23 · Echo Forge IMPORT V1: G7 físico PASS, integración en master y limpieza

**Entidad:** [[Echo Forge — Import Task V1]] · repo `xKoRx/symphony`

## Cambio

Cierre del mandato IMPORT V1 tras CONFIRMED del owner sobre RT-1 v5 (@ `a2b4bbd`): ejecución física de G7 en VM 111 Kronos, corrección en ventana de 7 defectos materiales de integración (todos fail-closed, cada uno con red→green y re-pin documentado en la RT-1), campaña certificadora `g7r7` COMPLETED end-to-end, integración FF de la rama a `master` (`745bc8b..9a69243`, 35 commits) y limpieza (branch remota/local y worktree eliminados; remoto queda sólo `master`).

- Nota de proyecto actualizada: `10-projects/Echo Forge/Echo Forge — Import Task V1.md` (nuevo estado + fila de entrega).
- Memoria del agente actualizada (`echo-import-task-v1-state`).

## Evidencia física (resumen)

- FlowRun `7e2f4c05` COMPLETED; workflow `sqx-main-v1-5f6a0a08` COMPLETED; StageExecution `import@sqx-import.v1` COMPLETED.
- 8 evaluaciones `import@sqx-import.v1` `IMPORTED_HISTORICAL_RESULT` (provenance `minio_package`, keys+SHA256 exactos); snapshots 1 classification → 3 ranking → 1 selection con 6 finalists; sin TaskSpec type=import.
- Read-back MinIO 8/8 byte-exact vs manifest congelado `import_freeze_manifest_g7r7.json`.
- Drill: resume de crash pre-publish (mismo FlowRun) + sondas EXTRA/MISSING/MUTATED fail-closed.
- Negativos: flota PID 1400507/binario intactos; `passed` 200/0-nuevos/bytes exactos; ETCD production 110 claves sin cambios; 0 pollers `sqx-main-queue`; Echo 0 POST.
- Teardown: procesos detenidos; prefixes ETCD candidatos (34+26) eliminados y verificados; proyecto efímero + databank `input` eliminados; watch_dir/MinIO/PG/Mongo conservados como evidencia.

## Desviaciones documentadas

- SQX candidate-local (copia del install de `kor` bajo `/home/echo-dev/import-cert-v1/sqx`) por permisos del operador `echo-dev`; el install de flota queda byte-intacto (refuerza el negativo).
- Ventana de 2h excedida por la corrección en ventana de los 7 defectos (cada uno documentado en la RT-1 con re-pins).
- Delete de la fila `output_namespace_ownership` del propio wave (3 veces, post-campañas fallidas de la ventana) como limpieza del scratch propio del candidato, con verificación previa de ownership.

## Nota de seguimiento

Campaña B (SELECTED COHORT → SQX TICK RETEST → MT5) se especifica aparte. Adopción formal de `usatechidxusd` en el catálogo Echo queda como decisión del owner (el alias de CanonicalSymbol ya la enruta).
