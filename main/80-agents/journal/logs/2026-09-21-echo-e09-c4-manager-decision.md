# Echo E-09 C4 — decisión del manager · 2026-09-21

## Resumen ejecutivo

`SOURCE_DELTA_REVIEWED · E09_HARNESS_SAFETY_SOURCE_APPROVED (REGRESSIONS REPORTED) · E09_COVERAGE_PARTIAL=88.6% · COVERAGE_GATE_PENDING · PHYSICAL_PENDING · INTEGRATION_PENDING · FINAL_CLOSED=NO`.

Un único carril de Echo y una sola feature remota activa. No se ordena repetir C1/C2 de E-09, ni repetir cobertura E-08, ni crear ramas nuevas, ni seguir generando tests de cobertura sin decisión de alcance. El siguiente trabajo útil independiente es **planificar E-10 Strategy Quality** según el DAG congelado; E-10 depende de E-05/E-06/E-07, NO del gate porcentual de E-09. E-10 todavía no tiene SPEC/PLAN congelados; preparar sólo documentación en Agents-OS, sin implementación ni merge a master.

## Autoridad y evidencia verificada

- GitHub `xKoRx/echo`: feature `feature/e09-execution-copy-reconciliation-fidelity` @ `d69e1ee35d95f84ddaec812a956f5837d799fbe3`; `master` @ `5dd998f16aea7b2821f460188718d7a6d279829c`. Comparación con `097e39eb767319801130be772de524e7e846e968`: `ahead_by=3`, `behind_by=0`, 11 archivos cambiados EXCLUSIVAMENTE de tests, scripts y `VERIFICATION.md`; sin source productivo/migraciones/S0. Dos refs `rescue/*` intactos.
- Revisión de source publicada: `v3/sdk/postgres/tests/execution_fidelity_e9/boot_disposable_pg.sh` verifica `data_directory` y puerto contra la instancia local antes de DDL/DML; `run.sh` comprueba nombre `echo_e9_harness`, marcador de archivo y marcador SQL `echo_harness.e9_harness_marker` ANTES de `DROP SCHEMA`; `e9_disposable_guard_test.go` verifica DB/rol/archivo/tabla; identidad E-09 separada de E-08. Hay regresión de colisión de puertos publicada. `HARNESS_SAFETY_SOURCE_APPROVED` se refiere a ese control revisado; resultados 4/4 de regresión y harness 067 PASS son reportes de agente, NO ejecuciones nuevas del manager.
- El agente reporta con perfiles cross-package merged: cobertura combinada 1130/1276 statements = 88.6% (`postgres` nuevo 431/499=86.4%, `execfid` 589/658=89.5%, `domain/execution_fidelity.go` 110/119=92.4%). Los tests race, build, vet y harnesses E-08/E-09 figuran reportados PASS. El manager NO volvió a correrlos.

## Decisión sobre residuo de 146 statements

NO se acepta `COVERAGE_GATE_PASS`, ni `CLOSED_WITH_RESIDUAL`, ni cambio de umbral. SPEC E-09 §8 exige ≥95% sobre críticos primero y VERIFICATION §1 conserva un gate contractual de ≥95% en archivos nuevos. Esta sesión reporta 88.6%, no PASS. Los 146 restantes se clasifican en §6.1 sólo por familias: errores del driver, revocaciones bloqueadas por JOIN previo, carreras dobles, wrappers sin llamador. El listado integral supuestamente está sólo en `/tmp/cover-e9-final.out`, NO incorporado en el repo; el agente declara datadirs efímeros eliminados. A falta de inventario durable no es posible juzgar excepción statement por statement ni afirmar que TODOS sean inalcanzables de forma legítima.

NO autorizar mocks de driver para maquillar el %; NO redefinir el denominador unilateralmente; NO ordenar otra ronda de 146 microtests sin riesgo prioritario concreto. Registrar la deuda exacta `E09-COVERAGE-146-EVIDENCE` como pendiente. Para resolverla en una futura ventana de cierre de E-09: regenerar perfiles y enumeración en artefacto persistente con SHA/digest, clasificar rutas críticas vs error/defensa según SPEC, y elevar al manager SOLO caminos críticos materiales o una propuesta explícita de excepción. Nunca etiquetar PASS por una descripción resumida.

E-09 clase A source CONTRACT/PG se conserva como avance; `E09_COVERAGE_GATE_PENDING` no autoriza clase B, certificación física, despliegue, activación económica, release o cierre final. Los prerrequisitos reales E-08 clase C, E-07 PHYSICAL, E-06 G1/T21, MQL compile, EchoPersistence y E-02 AC-18 siguen independientes. La nota VERIFICATION todavía incluye en su sección histórica E-08 C3 como pendiente, ya satisfecho a nivel source tras integración; el siguiente delta documental debe corregir este stale sin modificar contratos.

## Siguiente acción única

TOP documental prepara E-10 en Agents-OS contra el SHA actual `d69e1ee3` como baseline READ ONLY, leyendo autoridades E-05/E-06/E-07 y roadmap. Debe definir SPEC, PLAN, WPs, contrato Reference-only, quality/eligibility con UNKNOWN e INSUFFICIENT, calendario y reseteo por StrategyVersion, gates y prompt NORMAL. Cero source, cero nueva rama, cero E-11/E-12 implementation, cero certificados físicos; no confundir Strategy Quality con E-09 Execution Fidelity. No hay otros agentes Echo que coordinar. El manager revisará el handoff E-10 antes de enviar NORMAL.