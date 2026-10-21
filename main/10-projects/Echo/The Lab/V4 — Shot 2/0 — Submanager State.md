# V4 Shot 2 — Submanager State (durable)

**Role:** Implementation Submanager / Technical Integration Lead (mandato maestro 2026-10-20). **Engine:** GLM-5.3-Flash Max LOCAL. **Estado global:** ver [[F — Decision Register]] §V4 y [[Echo — Producto Integrado]].

**Gate vigente:** `SHOT1_DESIGN_REVIEWED_WITH_CONDITIONS`; D09/D10/D11/D16 OWNER_RATIFIED; D12–D15 aceptados como dirección para preflight. **Antes de editar código de producto: entregar TECHNICAL_FREEZE_PACKET y obtener UNA aceptación Manager/Owner.** Este estado NO es autorización de implementación.

## Baselines verificados (2026-10-20, daedalus)

| Repo / superficie | Baseline | Verificación |
|---|---|---|
| `xKoRx/echo` origin/master | `d74b6525` (= baseline de diseño, 0 commits de delta) | fetch + rev-list en clon `ef-rp-s03-audit-20261018/echo` |
| `xKoRx/echo` stream concurrente | `feature/ef-runtime-pools` @ `112ccccd`, 34 commits sobre master (toca `v3/sdk/futures`, `v3/core/internal`, `v3/futures-bridge`) — stream FEFB S01 EN CURSO (W2–W4 pendientes) | NO integrar ni descartar; coordinar traslape de naming `execution` con ese stream antes de tocar `v3/sdk/futures` |
| `xKoRx/symphony` origin/master | `daded14` (release 0.3.2; source 619c3b6f) | clone limpio `sqx144-supply-remediation-20261018/symphony` |
| Workspace Shot 2 | `~/aranea/work/lab-v4-shot2-20261020/echo` rama `feature/lab-v4-shot2` @ `d74b6525` (clone dedicado, limpio) | creado por submanager 2026-10-20 |
| Hardware (U04 input) | daedalus: 8 vCPU, 92 GB RAM (76 avail), `/` 30G libres, `/srv/echo-work` 100G libres | df/free 2026-10-20 |

## Trabajos (preflight técnico → freeze packet)

| ID | Paquete | Responsable | Estado | Entregable |
|---|---|---|---|---|
| W-PF1 | U01/A01: lineage versión/MM/Q_i emisor→consumidor + delta de captura | submanager (workers cancelados 2/2 por harness) | DONE 2026-10-20 | `preflight/FINDINGS-U01-U06.md` §U01/A01 |
| W-PF2 | U02/A02: hechos/retención/reproducción + U03 tamaños/transporte | submanager | DONE 2026-10-20 | ídem §U02/U03 |
| W-PF3 | U05: inventario naming futures_*/migración consumidores + legacy LAB | submanager | DONE 2026-10-20 | ídem §U05 |
| SM-1 | U04 capacidad/SLOs numéricos + metodología; U06 baseline/entornos | submanager | DONE 2026-10-20 | ídem §U04/U06 |
| SM-2 | Concretar D12–D15 (PG/worker, API v2/CAS, retención inputs, comparación copias) + SPEC ejecutable | submanager | DONE 2026-10-20 | `1 — TECHNICAL_FREEZE_PACKET.md` |

**Estado del gate:** `TECHNICAL_FREEZE_READY` emitido 2026-10-20 — esperando la ÚNICA aceptación Manager/Owner. Sin editar producto hasta entonces.

**Despacho secuencial obligatorio** (cuota 1310: workers grandes en paralelo mueren por burst). Probe antes del primero.

## Restricciones activas

- Preflight = READ-ONLY sobre repos/infra. PG: solo SELECT (RO PROD vía `aranea-postgres-ro`; DEV `echo-develop` vía `aranea-postgres-rw` con SELECT únicamente). Sin mutaciones ETCD/PROD/workers/flota.
- Forge: sin crear Forge DEV; lectura de su repo y de artefactos ya ingeridos/candidatos aislados autorizados.
- Echo policy: SDD en `specs/<FEAT-ID>/`, Allowed Files, roles; sin force-push; sin promoción a master.
- Agents-OS sobre master, cambios pequeños + change_log.

## Siguiente acción

Esperar aceptación única del freeze. Al aceptarse: implementación I1 en orden (fundación y recorrido vertical → curvas/métricas/dashboard → composición/corte) con workers o en serie, matriz G1–G11/T01–T45, sustitución legacy y paquete Shot 3.

## Log de avance

- 2026-10-20: bootstrap Agents-OS completo (constitución, perfil, router aranea, Environment Contract §0–§7); 4 autoridades leídas; baselines verificados; workspace dedicado creado; este estado registrado.
- 2026-10-20 (noche): preflight U01–U06+A01/A02 ejecutado por el submanager (2 despachos de worker cancelados por el harness; reportado como trabajo propio, sin paralelismo simulado). Hallazgos: rama e04 `4aad647b` certificada NO mergeada a master (adoptar como baseline); 065/066 no aplicadas en DEV; journal con risk_money en 64% REFERENCE; transporte inline 64 MiB suficiente (p95 ≈ 6–9 MB); 066 sin consumidores físicos (ventana de migración limpia). `TECHNICAL_FREEZE_PACKET` emitido — `TECHNICAL_FREEZE_READY`.
