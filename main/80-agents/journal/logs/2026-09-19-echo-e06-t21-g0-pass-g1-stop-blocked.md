---
type: change_log
schema_version: 1
created: "2026-09-19"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
  - "[[Echo Forge]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
---

# Change Log — 2026-09-19 E-06 T21 BLOCKED (G0 PASS + G1 STOP material)

- **Cambio:** la nota `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` recibe el bullet de estado `E06_T21_BLOCKED_G0_PASS_G1_PROMOTION_MISSING (8ª sesión)` y la actualización de la fila de entrega de `xKoRx/echo` (HEAD `b66dc5ff`); el repo `xKoRx/echo` recibe commit docs-only `b66dc5ff` (TASKS.md: bullet T21 de la 8ª sesión; VERIFICATION.md: sección nueva «G0 RE-EJECUTADO = PASS + G1 SEAL = STOP MATERIAL (2026-09-19, 8ª sesión)» — secciones históricas R2/G0 FAIL/R3 preservadas), push FF `8351ef18..b66dc5ff`, HEAD==origin, worktree limpio.
- **No modificado:** código de echo/forge (cero delta de producción), SPEC v1.2.4, migraciones, Versions históricos, contratos S0/E-03/E-04, branches Forge (`5d55c6b4` intocada), dirty ajeno `codex/f05-release-prep` y `symphony-f04-c9` (`87a3ab9`).
- **Motivo:** mandato maestro T21 (R3 G0 → Forge seal → E-04 → §22). G0 re-ejecutado = PASS con lecturas físicas en vivo (MQ5 R3 `4042db94…` byte-idéntico zeus==Windows; EX5 `34e7fe64…`; compile.log 0/0; XML long + sitios magic; allocation leída EN VIVO de la autoridad primaria PG vía flowkit — cierra la limitación de lectura de la 6ª sesión). G1 = STOP material ordenado por el mandato: la ejecución origen (RERUN-3, FlowRun `b6a1edea`) no tiene FINALIST_PROMOTION auténtica para `b94f1400` (falló en mt5_reconcile antes de promotion; read-back durable en vivo `strategy_versions: []`/`handoffs: []`), la única FINALIST_PROMOTION V2 (RERUN-4) es de otras 4 estrategias con el seal caído por el defecto #4 (fix `87a3ab9` sin release, ausente de la lane R3), y los artefactos R3 viven fuera de la cadena durable de evidencia. G2/G3/G4 no ejecutables. RESULT: `T21_BLOCKED`.
- **Verificación:** hashes/certutil/grep en vivo sobre las rutas certificadas; flowkit SELECT-only contra PG `trading_systems_test`@192.168.31.220 (allocation_ref `sha256:1d44410f…`, assigned_at 2026-09-17T23:36:42.522023Z); `git diff --check` limpio; push FF verificado; cero órdenes/exposición/ingestion; E-06 NO CLOSED.
