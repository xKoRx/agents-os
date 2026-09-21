# Echo — Decisión manager: C4-S doble despacho, reconciliación y siguiente E-09

**Fecha:** 2026-09-21. **Owner de dirección:** manager único Echo. **Resultado:** `DUPLICATE_DISPATCH_RECONCILED · E08_C4S_SOURCE_APPROVED · E08_COVERAGE_GATE_PASS_REPORTED · PHYSICAL_PENDING · ECONOMIC_ACTIVATION_PENDING · E08_FINAL_CLOSED=NO`.

## Autoridad Git y elección canónica

- Repo `xKoRx/echo`; única feature remota activa `feature/e09-execution-copy-reconciliation-fidelity` @ `097e39eb767319801130be772de524e7e846e968` (verificada en GitHub). `origin/master` @ `5dd998f16aea7b2821f460188718d7a6d279829c` intacto. Los dos `rescue/*` permanecen; no son features activas.
- El owner envió involuntariamente el mismo mandato de cierre E-08 C4-S-R1/R2 dos veces. El primer ejecutor publicó mediante FF `7c843e9c..097e39eb` un commit que cambia sólo `boot_disposable_pg.sh`, `boot_disposable_pg_collision_test.sh`, `e8_stores_infra_test.go`, `e8_harness_guard_test.go` y `VERIFICATION.md` §14.6. El segundo ejecutor trabajó desde el mismo baseline en un workspace distinto; al detectar HEAD remoto avanzado, abortó push/rebase y verificó independientemente la corrección publicada. Sus commits `8d47d573`, `89e3077c`, `d70cf1b0`, `b3b7756f` son evidencia local redundante, no autoridad, no deben integrarse, cherry-pickearse, rebasearse ni publicarse. No eliminar su último worktree/ref de recuperación sin revisar si hay contenido exclusivo que preservar; no es una tarea prioritaria.

## Review source R1/R2

- **R1 PASS source**: `boot_disposable_pg.sh` verifica `SHOW data_directory` y `SHOW port` del servidor en el puerto contra el datadir propio canónico y el puerto solicitado *antes de CREATE DATABASE y escribir marcadores*, rechazando cluster ajeno/puerto ocupado. Corregida interpolación de `:'token'`: SQL por stdin, no `psql -c`. Regresión `boot_disposable_pg_collision_test.sh` con dos instancias efímeras verifica colisión y reuso.
- **R2 PASS source**: `infSeedBindingIdent` delega a `e8infPredeleteBinding`; los dos `DISABLE TRIGGER`, DELETEs y dos ENABLEs se ejecutan dentro de una sola transacción con rollback al fallar y commit comprobado; regresión `TestHarness_PredeleteSetupFailureRestoresBindings` prueba error de FK interna a mitad del setup, invariancia de triggers/filas y happy path.
- Compare `7c843e9c..097e39eb`: un commit FF, cinco archivos, cero archivos productivos/migraciones/contratos/flags.

## Evidencia de tests y límites

Ejecutor canónico reporta PostgreSQL 17.11 descartable exclusivo, harness 066 PASS; E-09 harness 067 PASS en esa instancia; suites `-race` econroute, domain y execfid OK; postgres sobre 066 falla únicamente por los 22 tests E-09 que requieren 067, failing set sin nuevos; sobre 067 cero fallos; vet/build/gofmt/diff-check PASS; preimage/postimage esquema intacto y datos fuera de fixtures intactos. El segundo ejecutor reporta verificación independiente con dos datadirs propios. El manager revisó Git/source pero NO re-ejecutó suites localmente. Cobertura reportada: econroute 95.6%; gate 98.0%; reservas 98.2%; command store 98.4%; routing store 97.9%; snapshot store 98.9%; residuos driver/estructural documentados en E-08 VERIFICATION §14.3; no perseguir 100%.

**Decisión:** cierre de `E08_COVERAGE_GATE` software aprobado con residuo no crítico declarado. `E08_FINAL_CLOSED=NO`; `PHYSICAL_PENDING` y `ECONOMIC_ACTIVATION_PENDING`, sin merge a master ni habilitar flags. No reabrir C1–C4-S salvo nueva evidencia concreta.

## NEXT EXACT — E-09 en rama única

Un único NORMAL, en `feature/e09-execution-copy-reconciliation-fidelity @ 097e39eb`, worktree limpio y FF verificado, implementa primero protección fail-closed de `v3/sdk/postgres/tests/execution_fidelity_e9/run.sh` *antes de cualquier DROP/CREATE/ALTER* contra PG exclusivo verificable. Reutilizar patrón R1/Go del harness E-08 sin copiar una verificación parcial ni asumir que loopback o DATABASE_URL bastan. Validar dos clusters propios, colisión sin mutación, happy path, preimage/postimage. Solo entonces continuar con COVERAGE_GATE E-09 VERIFICATION §6 (objetivo ≥95% contractual de paths nuevos), tests reales y fail-closed; jamás borrar defensas o inventar cobertura; si no se alcanza, residuo por bloque y manager decide. No PROD/SHARED, activación económica, físico ni merge. Antes de nuevas pruebas destructivas, asegurar que run.sh E-09 está gateado.

**Regla operativa:** una tarea implementadora a la vez salvo paralelismo explícito del manager; dos envíos del mismo mandato no equivalen a dos líneas de desarrollo. Mantener una sola feature remota activa y una sola versión canónica.