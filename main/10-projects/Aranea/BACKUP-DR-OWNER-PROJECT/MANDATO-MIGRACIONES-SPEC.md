---
title: "MANDATO 5 — Migraciones justificadas (recalificación W1-W5 tras D-NEW)"
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
tags: [kind/doc, area/aranea, domain/backup-dr]
---

# MANDATO 5 — Migraciones justificadas

**Ejecutor**: Ariadna (placement) + carril Ceph/Storage cuando toque pool1. **Base**: [[PLACEMENT-DECISIONS-20260920]] §D. **Principio**: el objetivo es el placement correcto, NO llenar la ventana — ninguna migración sin destino y mecanismo de recuperación certificados; sin causalidad, no se mueve nada.

## Propósito

Mandato de migraciones justificadas tras la redirección: W1/W2 canceladas, W3/W4 por decisión, W5 reevaluada por VM.

## Contenido

## Alcance tras D-NEW

> [!warning] Errata 21sep noche-3 (revisión "Placement Freeze antes de Backup/DR") — la fila W1/W2 conservaba redacción en imperativo ("reubicar…", "Alta del storage nfs-pool2"), contradictoria con su propio estado CANCELADAS. Corrección: la operación es NINGUNA y el alta `nfs-pool2` queda OBSOLETA (sin consumidor tras D-NEW-01). Clasificación canónica: [[PLACEMENT-DECISIONS-20260920]] §F.

> [!warning] Errata 21sep noche-5 (mandato BACKUP FIRST) — dependencia y precondiciones corregidas
> **STORAGE_ORGANIZATION_COMPLETE no es prerequisito de este mandato** (dependencia revocada). **BACKUP_BASELINE_VERIFIED por unidad SÍ es el requisito de cada MIGRATION_READY**: el paso 1 del preflight (vzdump + verify) se convierte en la verificación de ese baseline; ninguna migración se ejecuta antes de que la unidad tenga su protección recuperable demostrada. Análisis disco por disco (99 discos, priorización y ahorro real): [[ANALISIS-DISCO-POR-DISCO]].

| Ítem | Estado | Operación |
|---|---|---|
| W1/W2 edge → pool2 | CANCELADAS (D-NEW-01) | ~~reubicar los 4 CTs + traefik a nfs-pool2~~ · ~~alta del storage nfs-pool2~~ → **NINGUNA**: edge queda como está (correcto hoy); `nfs-pool2` OBSOLETO (sin consumidor tras la cancelación) |
| W3 pi-hole 149 | DEFER → D5 | si owner elige reactivar: mandato separado de diagnóstico RO (logs CT, config FTL, red/L2 en athena) + vzdump + protección; retiro = decomisión formal. Fuera de ventanas de backup |
| W4 kafka 128 | KEEP hasta causalidad | P1-4 diagnóstico RO del brote primero; migración sólo si el diagnóstico la justifica (destino corregido: athena) |
| W5 down-tier SOs | REEVALUACIÓN POR VM | por cada VM (140, 152, 153, 157, 133/134/144): beneficio/rendimiento/disponibilidad/capacidad/destino/dominio de falla/restore/alivio real. Destinos VÁLIDOS: zeus local-lvm (77,5G), hera (91,7G), `nfs-vmbackup` pool0, hades 33,4G SÓLO si la VM ≤25G y deja ≥8G. Tamaños reales en preflight (`qm config`+`pvesm`), no estimaciones |

## Operaciones (si el owner aprueba alguna W5-VM o W4)
1. Preflight por VM: tamaño real de rootfs; destino con espacio; vzdump fresco + verify TASK OK (mecanismo B1 ya activo o one-shot); sin slow ops BlueStore activas; condición de alerta K2 no disparada; Echo 140 sólo con cierre operativo verificado y como primera.
2. Ejecución: stop → restore del rootfs al destino (o `pct move-volume` si aplica; `--delete` jamás por defecto) → arranque → verificación app (PG: `SELECT 1`+servicio; Mongo: ping; Echo: freshness métricas; MT4: arranque terminal) → medir `ceph osd df` delta.
3. Escalonado: 15-30 min/VM, 2-3 ventanas; una VM a la vez; jamás simultáneo con réplica-pool2-full, B1-fulls o G1B.

## Gates
Cada W5-VM/W4 = gate owner explícito con su ficha reevaluada (D1+018+019 donde aplique); sin gates no hay movimiento. pool1: NADA escribe (sólo se lee vía vzdump).

## Rollback
Re-restore del snapshot PBS previo al backend original pool1 (sigue existiendo) — <30 min/VM. El disco de origen NO se borra jamás hasta evidencia de restauración validada + autorización específica.

## ABORT
2 fallos consecutivos del mismo restore → rollback de esa VM + DEFER del resto; HEALTH_ERR Ceph → pausa total del carril.

## DoD
Por VM movida: servicio verificado en destino + delta Ceph medido + rollback probado (o documentado como no-ejecutado) + MATRIZ actualizada. Las no-aprobadas quedan como decisión documentada, no como deuda silenciosa.
