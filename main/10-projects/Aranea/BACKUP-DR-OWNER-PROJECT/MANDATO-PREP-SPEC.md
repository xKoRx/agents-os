---
title: "MANDATO 1 — Preparación y capacidad (Etapa A; ejecutable durante semana de mercado, documental/RO)"
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
tags: [kind/doc, area/aranea, domain/backup-dr]
---

# MANDATO 1 — Preparación y capacidad

**Momento**: Etapa A — durante la semana (mercado abierto); RO + documental + scripts sin ejecutar en producción. **Ejecutor**: Ariadna. **Ejecución de mutaciones**: NO en este mandato.

## Propósito

Mandato de preparación (Etapa A): scripts, diffs, re-medición de capacidad y preflights sin tocar producción.

## Contenido

## Objetivo
Dejar todo listo para que los mandatos 2-6 sean ejecutables en sus ventanas: scripts preparados, capacidad re-medida, preflights empaquetados.

## Tareas
1. **Script de replicación** (`~/aranea/work/replicacion-pool0-pool2/repl-pool0.sh`): lógica §3 de [[POOL0-TO-POOL2-REPLICATION-SPEC]] (flock, último común, NO-SEND por umbral, log local TrueNAS, alerta). Probar con **fixtures aislados** (pools de archivo `zpool file` en VM de prueba o describir prueba simulada) — JAMÁS contra pool0/pool2 reales fuera de ventana.
2. **Script vzdump semanal `nfs-vmbackup`** + alta de storage preparada como diff (`/etc/pve/storage.cfg` +5 nodos, un bloque nuevo; `nfs-storage` INTOCADO — diff en raw/).
3. **Re-medición de capacidad** (preflight de cada gate): pool2 free zpool, pool0 used, crecimiento diario (serie 7d con lectura diaria RO vía API), PBS datastore, VGs kronos.
4. **Lista 018 propuesta actualizada**: matriz 59/59 + exclusión ledger de [[TWO-LAYER-BACKUP-SPEC]] §1 como anexo del formulario del ticket 018 (para el owner).
5. **Preflight T-25 extendido**: añadir a W-04 los checks de la réplica (G-REP-1..4) y de `nfs-vmbackup`.

## Gates
Ninguno para la preparación documental (clase AUTO). Las ejecuciones de los scripts = gates de sus mandatos (2-4).

## ABORT / rollback
N/A (no muta). Los diffs preparados se aplican sólo con su gate; rollback = no aplicar.

## DoD
Scripts con prueba de fixture documentada; diffs preparados; CAPACITY-FREEZE v2 con serie 7d; anexo 018 listo. Todo en workspace + referencias en la SPEC correspondiente.
