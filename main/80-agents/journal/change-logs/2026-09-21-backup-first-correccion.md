# Change log — 2026-09-21 noche-5: Mandato correctivo BACKUP FIRST (storage ↔ Backup/DR)

**Ejecutor**: Ariadna · **Mandato**: owner ONE-SHOT "ARANEA · BACKUP FIRST" · **Clase**: documental, cero mutaciones de infra.

## Motivo

El reporte noche-4 conservaba la dependencia `STORAGE_ORGANIZATION_COMPLETE → activar Backup/DR`, revocada por el owner. Además, la clasificación KEEP por workload no satisfacía el análisis disco por disco pedido, y los presupuestos mezclaban fases.

## Cambios

1. **Dependencia eliminada de TODOS los documentos vivos** (grep verificado = 0 residuos como requisito):
   - `STORAGE-ORGANIZATION-FREEZE.md` — gate redefinido (cierra optimización de storage); §2 reescrito ("Qué es y qué NO es"); criterio 2 con criterio de desbloqueo por migración (BACKUP_BASELINE_VERIFIED).
   - `MASTER-PLAN-STORAGE-BACKUP-DR.md` — errata noche-4 corregida + errata noche-5 con la secuencia aprobada y las reglas fijas.
   - `PLACEMENT-DECISIONS-20260920.md` §F — migraciones condicionadas a BACKUP_BASELINE_VERIFIED + gates propios (ya no al gate de organización).
   - `FIRST-MAINTENANCE-WINDOW-20260920.md` §8.2 — paso 8 del DAG redefinido.
   - `ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP.md` — E6 corregido + delta noche-5 completo.
   - `ROADMAP-WP-BACKUP-DR.md` — sección "Corrección noche-5" (secuencias sin el gate como frontera).
   - `BACKUP-DR-OWNER-PROJECT.md` — status_detail (extraído con sed, 2,2k chars) + T-24/T-25/T-26.
   - Workspace: `~/aranea/work/continuity-20260923/TABLA-APROBACION-23SEP.md` + `MANDATO-JUEVES-24.md` — errata noche-5.
2. **ANALISIS-DISCO-POR-DISCO.md (NUEVO)** — 99 discos clasificados con evidencia existente (guest-disk-map.json 59/59 + evidence/05 prov + rbd-du2 used; derivación programática, 0 filas sin clasificar; 38 imágenes RBD mapeadas 1:1 + 5 huérfanas 200G). Totales verificados por script: MIGRATE 21/773G · DEFER 13/340G · RECONFIGURE 1/50G · UNKNOWN 7 · alivio real proyectado 150-350G (thin) vs techo 1363G.
3. **CAPACITY-AND-RESERVATIONS.md §7 (NUEVO)** — presupuestos por fases (baseline / post-vm-backup / post-migraciones); baseline alcanzable completo sin migrar; ahorro contabilizado sólo post-liberación verificada.
4. **Mandatos viernes/sábado** — MANDATO-BACKUP-VMS-SPEC: preflight con estado por bloque (READY_AFTER_OWNER_GATE/BLOCKED/DEFER, objetivo principal Backup/DR, nada se fuerza a PASS); MANDATO-BACKUP-DATOS-SPEC: orden nocturno (T-21b/W-02 primero); MANDATO-MIGRACIONES-SPEC: errata noche-5 (dependencia fuera; vzdump+verify del preflight = verificación del BACKUP_BASELINE).

## No cambiado (explícito)

Diseño F-01..F-14 · notas históricas del journal (operating-state, R0, L1s, change logs previos) · paquete del miércoles W-01..W-04 (salvo erratas a 2 archivos indicadas) · mecánica de gates G-REP-0..5/G-B1/G-NFSVM · cronograma 25-26sep · decisiones D-NEW-01..06.

## Verificación

- `grep -c` noche-5: 11 archivos del proyecto con marcadores.
- `grep STORAGE_ORGANIZATION` en mandatos/SPECs/workspaces: sin residuos como requisito (sólo menciones negadas/depuradas).
- Matriz: 99 filas × 11 columnas, `revisar=0`, `unmatched=[]`.
- Ningún comando contra PVE/PBS/TrueNAS; R2/A1/R1/R1.5 intactos.
