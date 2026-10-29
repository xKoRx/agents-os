# Change Log — 2026-10-29 — Echo campañas I0-S2 (verificación adversarial)

## Contexto

ONE-SHOT I0-S2 (TOP LOCAL, GLM-5.3-Flash/ZCode) sobre `xKoRx/echo@feature/ef-campaign-modes-i0` (base `2baf319d`, candidato `b964e13d`, readback remoto verificado). Mandato: falsificar el reporter económico I0-S1 antes de aceptar su integración; producto READ_ONLY. Bootstrap agents-os ejecutado (constitución, perfil, continuidad, índice de skills); routing: sdd-workflow, echo-retester-master, qualification runbook (reconocido, sin ejecución de cualificación), agent-run-register, session-feedback, session-close.

## Cambios

- CREATE `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-VERIFY-RETURN.md` — retorno canónico: STATUS=FINDINGS (4 P1 + 5 P2 + 1 P3 confirmados; 2 refutados), INDEPENDENT_E2E, REPRO_REFS con hashes, LEGACY_COMPATIBILITY, NO_SPAWN, COVERAGE, S04_REMAINING, NOT_EXECUTED/UNKNOWN, NEXT.
- CREATE `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-campaign-modes-i0-s2.md` — registro atribuible.
- CREATE este change_log.
- Fuera del vault: harness/fixturas persistidos en `~/echo-work/i0-s2-verify/` (workspace propio, fuera del árbol de producto).

## Resolución aplicada

- Verificación adversarial ejecutada: arquitectura PASS (proyección pura, sin spawn/egress demostrado por imports + sentinel + diff, legacy byte-idéntico, scopes separados); E2E real R03 doble corrida byte-idéntica conciliada contra cálculo independiente; 11 falsificadores con 9 confirmados y 2 refutados. Los P1 (residual sin refunds; Q sin linaje pase/activación; funded inflada por review_at/credentials_at pre-activación; cutoff conciliado contra terminal) bloquean VERIFY_PASS; veredicto FINDINGS, sin corrección de producto, manager adjudica y emite I0-S3.
- Falsificadores que demostraron defectos clasificados PERMANENT_REGRESSION_CANDIDATE con fixtures reproducibles; bundles/retries y re-lectura idempotente quedan como comportamiento correcto verificado.

## Validación

- 34/34 tests del autor y 124/124 suites del lab re-ejecutados OK en el candidato (pasan con los defectos presentes ⇒ los contraejemplos no estaban cubiertos).
- E2E: determinismo byte-idéntico, sentinel sin spawn/egress con salida idéntica, inputs sellados byte-intactos (sha256 pre/post), conciliación independiente coincidente.
- Sin campañas/compras/trading/deploy; sin suites Go; S04 sin reapertura (censo V1 reconocido, fixture Go registrado como dependencia); umbral 1/3 THRESHOLD_NOT_ADJUDICATED.

## Compatibilidad

- Scope: local (Hefesto). Sin escrituras fuera del vault propio/harness propio; sin secretos; importes citados pertenecen a receipts ya sellados del proyecto.

## Rollback

- Vault: borrar/revertir los tres archivos creados (no hay commit git disponible en esta superficie; ver fricción). Producto: sin cambios (READ_ONLY).

## Continuidad

- Manager adjudica F1–F11 y emite I0-S3 (corrección sobre el mismo SHA, integrando los falsificadores como regresiones permanentes); S04 permanece abierta en su alcance (equivalencia de intérprete V1 + fixture Go de frontera); PRO_CHAT_POOL_DELTA UNKNOWN.
- Este worker queda CERRADO; el manager de Optimización de Campañas y el programa Echo Futures permanecen abiertos.
