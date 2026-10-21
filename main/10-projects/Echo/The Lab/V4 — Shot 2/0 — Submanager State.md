# V4 Shot 2 — Submanager State (durable)

**Role:** Implementation Submanager / Technical Integration Lead (mandato maestro 2026-10-20). **Engine:** GLM-5.3-Flash Max LOCAL. **Estado global:** ver [[F — Decision Register]] §V4 y [[Echo — Producto Integrado]].

**Gate vigente:** dictamen Manager 2026-10-21 (V2) `TECHNICAL_FREEZE_REPAIR_REQUIRED_V2` (C01–C06) sobre blob `40c16d50` (rev 2, commit `3baaaf81`). **Respuesta:** paquete REVISIÓN 3 emitido 2026-10-21 con estado pedido `TECHNICAL_FREEZE_READY_V3` — corrige sólo C01–C06 (mecanismo de migración real con `lab_migration_state` auto-registrada y 066 jamás ficticia; receta `definition-v1` con `identity_recipe` sellada, analytic-v1 retirada; QI_SEALED en la primera decisión MM del ciclo; economía por Operation con correlación y movimientos al reconocerse; sin GC concurrente en I1 + cadena única de revisiones; grano de historia intacto con límites 128 MiB/250k ops/1M movements) y el fallback de autoabsorción eliminado (despacho alternativo o escalación). Evidencia actualizada (E05/E08/E09/E12 + tabla correcciones rev 3). Espera la ÚNICA aceptación; sin editar producto.

## Baselines verificados (2026-10-21, daedalus)

| Repo / superficie | Baseline | Verificación |
|---|---|---|
| `xKoRx/echo` origin/master | `d74b6525` (= baseline de diseño; re-verificado fetch 2026-10-21) | fetch + rev-list en clon Shot 2 |
| `xKoRx/echo` rama e04 | `feature/e04-dev-ingest-recovery` @ `4aad647b`: 5 commits exclusivos (seeds+wiring, policy_id, platform+migración 068, guard DeleteVar, renumber); 305 detrás de master | git log/cherry/diff en clon Shot 2 (EV-E01) |
| `xKoRx/echo` stream concurrente | `feature/ef-runtime-pools` @ `112ccccd` (FEFB S01) — dueña del grammar Java; renombres coordinados | NO integrar |
| `xKoRx/symphony` origin/master | `daded14` (release 0.3.2) | clone limpio existente |
| Workspace Shot 2 | `~/aranea/work/lab-v4-shot2-20261020/echo` rama `feature/lab-v4-shot2` @ `d74b6525`, limpio | verificado 2026-10-21 |
| PG DEV `echo-develop` @ .220 | sin `schema_migrations`; efectos 001→065 + CHECK 4 tokens aplicados a mano; `futures_*` ausente; 5 objetos lab legacy admin-owned; REFERENCE 137.276 filas (64,7% risk_money) | SELECT-only 2026-10-21 (EV-E05..E11) |

## Correcciones a la rev 1 (registradas en evidencia)

065 SÍ aplicada en DEV (schema lab_curves v3 presente); distribución journal REAL (p50=19/p75=33/p95=59/p99=24.682/max=56.884 ops por strategy+symbol; 412–421 B/op; max body 23,65 MB); DEV sin tabla de control de migraciones completa; proyector 066 sin actividad observable en Core DEV desplegado.

## Estado del gate

`TECHNICAL_FREEZE_READY_V2` pedido — pendiente de aceptación única. U01–U06 con estados VERIFIED/SPECIFIED_FOR_IMPLEMENTATION/NOT_DEMONSTRATED (EV; sin cierre en bloque; frontera PROD acotada al retiro de 066).

## Restricciones activas

- Read-only en esta reparación: sin migraciones ejecutadas, sin deploy, sin PROD, sin Gateway compartido, sin campañas.
- Despacho de workers SECUENCIAL con probe (cuota 1310); si el harness falla de nuevo: documentar bloqueo y usar despacho alternativo (serial propio) sin absorción tácita ni cambio de modelo.
- Horario owner: 08:00–02:30 CLST; al parar, estado durable aquí; sin presuponer reanudación automática.
- Agents-OS sobre master, cambios pequeños + change_log.

## Siguiente acción

Al aceptarse `TECHNICAL_FREEZE_ACCEPTED_V2`: I1 en orden — i-mig-0 (reconciliación schema_migrations, ejecución con gate) → i-e04 (adopción acotada con tests portados + re-certificación boundary Forge) → fundación/identidad (069) y vertical → proyección 067 → curvas/métricas/dashboard (070) → composición/corte; caso T sin venue/LIVE incluido en matriz G1–G11/T01–T45; paquete Shot 3 al cierre. Sin Shot 3 ni cierre de sesión antes de tiempo.

## Log de avance

- 2026-10-20: bootstrap; 4 autoridades; baselines; workspace; preflight U01–U06 por el submanager; paquete rev 1 (`TECHNICAL_FREEZE_READY`).
- 2026-10-21: dictamen Manager `TECHNICAL_FREEZE_REPAIR_REQUIRED` (R01–R06). Investigación de reparación ejecutada (git e04/máximo detalle, PG DEV read-only, contratos de motor, mediciones de transporte): matriz de adopción e04, orden 067→068→069→070, taxonomía Q_i + QI_SEALED, history_id con producer_writer, receipts tabla nueva, retención write-ahead, recorrido con Ledger autoridad, caso T, 64 MiB=request completo + caps, benchmark congelado con distribución medida. Evidencia publicada en el proyecto; paquete rev 2 emitido (`TECHNICAL_FREEZE_READY_V2`). Sin edición de producto.
