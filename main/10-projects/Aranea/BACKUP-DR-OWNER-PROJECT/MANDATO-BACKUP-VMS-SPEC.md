---
title: "MANDATO 2 — Backups de VM (Mecanismo A: B1 producción + capa pool1→pool0)"
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
tags: [kind/doc, area/aranea, domain/backup-dr]
---

# MANDATO 2 — Backups de VM (Mecanismo A)

**Ejecutor**: Ariadna (Backup/DR). **Dependencias**: MANDATO 1 (diffs listos); decisión D-piloto; ticket 018; ventana 019. **I/O**: vzdump T0 full inicial concentra I/O — JAMÁS simultáneo con la 1ª réplica a pool2 ni G1B.

## Propósito

Mandato de ejecución del Mecanismo A: producción vzdump (B1) y capa nfs-vmbackup pool1→pool0.

## Contenido

## Objetivo
Cobertura imagen-level de VM/LXC según [[TWO-LAYER-BACKUP-SPEC]] §1: (a) B1 producción en PBS; (b) 2ª copia local en `nfs-vmbackup` (pool0) de las unidades con discos en pool1.

## Operaciones (orden)
1. **Preflight fail-closed**: datastore PBS <70%; verify main TASK OK; `pvesm` verde 5/5; Ceph sin HEALTH_ERR (los guests a respaldar corren en pool1 — vzdump es lectura, NO escritura: NO_GO de escritura se respeta); sin sesión Echo activa en la ventana para guests T0d; 018 con lista final.
2. **B1 producción**: activar jobs vzdump diarios 02:00 (T0) / semanal (T1/T2) con retención según D; exclusiones = ledger de la SPEC. El horario lo fija el owner en D/019 (S-07: nunca dentro de sesión de mercado).
3. **Capa pool1→pool0 (G-NFSVM)**: dataset `pool0/vm-backup` + export + storage `nfs-vmbackup` (diff MANDATO 1) + job vzdump semanal snapshot-mode de las unidades del anexo (140, 152, 153, 157, 133/134/144, 124, CTs 126/129/141/128/127, etcd×5, 116/113/103/137) retención keep-weekly=4.
4. **Validación**: 1er ciclo completo + verify PBS TASK OK; 1 restore drill de 1 CT T0 a scratch + 1 VM completa a scratch (primer drill de VM completa del sistema — [[MANDATO-CERTIFICACION-SPEC]]); `pvesm list nfs-storage` intacto (baseline).

## Gates
**G-B1** = D + 018 + 019. **G-NFSVM** = alta storage/dataset + schedule semanal (autorización específica). Una aprobación general NO sustituye gates.

## Riesgo / I/O
vzdump sobre MT4/echo nocturno = UNKNOWN (S-07); limitar bandwidth si el owner lo pide. NFS pool0 soporta la capa semanal (rootfs ≈140G brutos, write-mostly idle).

## Rollback
Desactivar jobs nuevos (timers/jobs.cfg diff guardado); restaurar storage.cfg sin el bloque `nfs-vmbackup` (sin volúmenes recibidos = trivial; con volúmenes, retirar tras conservar vzdump equivalente en PBS).

## ABORT
Fallo de verify 2× sobre la misma unidad → excluir esa unidad del job y reportar; HEALTH_ERR Ceph → pausar jobs nuevos; posición Echo abierta → no tocar guests T0d.

## DoD
B1 activo con N unidades de 018 y verify diario OK; capa semanal `nfs-vmbackup` con 1er ciclo OK; drills CT+VM PASS documentados; MATRIZ actualizada (estado vzdump por guest).
