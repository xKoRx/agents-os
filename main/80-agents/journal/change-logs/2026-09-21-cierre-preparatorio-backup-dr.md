# 2026-09-21 — Cierre preparatorio Backup/DR (noche-6, mandato owner ONE-SHOT)

## Contexto

Mandato owner: ejecutar el cierre preparatorio de Backup/DR reutilizando íntegramente el estado vigente de Agents-OS (noche-5); no rehacer inventario ni arquitectura; cero cambios productivos; persistir, actualizar continuidad y cerrar sesión. 7 objetivos: T-21b/W-02 listos, P1 ejecutable, ticket 018 congelado por matriz de cobertura, presupuesto por etapas (margen real pool0), `rbd du` completo RO, paquete único 25-26sep.

## Ejecución

- Bootstrap canónico + router aranea; delta desde continuidad noche-5 (lectura única de fuentes canónicas; cero re-derivación).
- **Sonda runtime RO** (canal ariadna demostrado; evidencia en `~/aranea/work/cierre-preparatorio-20260921/raw/sondas-runtime-20260921.md`): PBS 295G/18% ext4; quórum 5/5; 124/125 running; Ceph osd.0/2 86,56/86,60% (22:39; K2 no disparada; ritmo vespertino ≈1,8G/OSD/h → margen backfillfull ≈18-80h → riesgo de disparo K2 antes del viernes); W-01 re-validado live (pool-kronos VFree 733,87G; VM 180 scsi1 serial `pbs-data`); hades local-lvm errata ≈20,5G libres; T-21b verificado sin aplicar; whitelist guest PG `command=` por diseño (canal Echo = W-04/dump).
- **Deltas materiales**: 162 y 170 YA LIBERADAS por el owner (qmdestroy root@pam 20sep 23:58 -03, tasks OK en kronos/zeus; configs y RBDs ausentes) — doc del 21sep las mantenía DEFER; queda sólo 112; huérfana vm-112-disk-0 = 5,9G usados (no ~120G); rbd du completo 48 imágenes: 1.503G prov / 848G usados (alivio real fase 1 W5-post ≈164G; escenario máximo ≈572G); 127/106/141 llenos al prov → prioritarios W5-post.
- **Entregables**: `PAQUETE-EJECUCION-25-26SEP.md` (READY / READY_AFTER_OWNER_GATE / GATED-owner-pendiente / DEFER con dependencias exactas; insumo freeze T-24) + `RBD-DU-RESULTADOS-20260921.md` (baseline por imagen para verificación Fase 2) + `raw/sondas-runtime-20260921.md` + `raw/rbd-du-pool1-20260921.txt` + `raw/rbd-du-classes.json`.
- **Vault**: erratas en [[CAPACITY-AND-RESERVATIONS]] (§3 lecturas Ceph 22:39; §5 hades 20,5G) y [[ANALISIS-DISCO-POR-DISCO]] (alivio real medido; §5 huérfanas con usados reales + errata 162/170); proyecto: bitácora noche-6 + status_detail.

## Alcance y límites

- Cero mutaciones de infraestructura; Echo operando (última evidencia: 1 posición abierta 09:44); tickets 018-021 intactos; R2/timers intactos; ninguna decisión tomada en nombre del owner.
- Sesión-cierra (L0/L1) y congela T-24 siguen pendientes por diseño (T-24 = jueves 24; cierre explícito del owner).
