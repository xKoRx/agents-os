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
| W-PF1 | U01/A01: lineage versión/MM/Q_i emisor→consumidor + delta de captura | worker ONE-SHOT | PENDING | `preflight/wpf1/FINDINGS.md` |
| W-PF2 | U02/A02: hechos/retención/reproducción + U03 tamaños/transporte | worker ONE-SHOT | PENDING | `preflight/wpf2/FINDINGS.md` |
| W-PF3 | U05: inventario naming futures_*/migración consumidores + legacy LAB | worker ONE-SHOT | PENDING | `preflight/wpf3/FINDINGS.md` |
| SM-1 | U04 capacidad/SLOs numéricos + metodología; U06 baseline/entornos | submanager | PENDING | sección del freeze packet |
| SM-2 | Concretar D12–D15 (PG/worker, API v2/CAS, retención inputs, comparación copias) + SPEC ejecutable | submanager | PENDING | `1 — TECHNICAL_FREEZE_PACKET.md` |

**Despacho secuencial obligatorio** (cuota 1310: workers grandes en paralelo mueren por burst). Probe antes del primero.

## Restricciones activas

- Preflight = READ-ONLY sobre repos/infra. PG: solo SELECT (RO PROD vía `aranea-postgres-ro`; DEV `echo-develop` vía `aranea-postgres-rw` con SELECT únicamente). Sin mutaciones ETCD/PROD/workers/flota.
- Forge: sin crear Forge DEV; lectura de su repo y de artefactos ya ingeridos/candidatos aislados autorizados.
- Echo policy: SDD en `specs/<FEAT-ID>/`, Allowed Files, roles; sin force-push; sin promoción a master.
- Agents-OS sobre master, cambios pequeños + change_log.

## Siguiente acción

Despachar probe de cuota → W-PF1 → W-PF2 → W-PF3 (secuencial) → SM-1/SM-2 → devolver `TECHNICAL_FREEZE_READY`.

## Log de avance

- 2026-10-20: bootstrap Agents-OS completo (constitución, perfil, router aranea, Environment Contract §0–§7); 4 autoridades leídas; baselines verificados; workspace dedicado creado; este estado registrado.
