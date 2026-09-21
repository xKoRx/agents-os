---
title: "MANDATO 4 — Replicación pool0→pool2 (Etapa C; ventana propia)"
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
tags: [kind/doc, area/aranea, domain/backup-dr]
---

# MANDATO 4 — Replicación pool0→pool2 (1ª transferencia + activación)

**Ejecutor**: Ariadna (Backup/DR) + canal DDP TrueNAS. **SPEC**: [[POOL0-TO-POOL2-REPLICATION-SPEC]] (autoridad técnica). **Etapa C** — ventana propia o tramo exclusivo, JAMÁS simultánea con backups full, restauraciones o migraciones que carguen TrueNAS.

## Propósito

Mandato de ejecución de la réplica pool0→pool2 (Etapa C): primera transferencia y activación del schedule diario.

## Contenido

## Preflight (fail-closed, el día de la ventana)
1. **G-REP-1**: scrub pool2 completado con 0 errores (ventana previa separada; ~7h estimadas; NO el mismo día que la full si el chasis comparte carga — programar scrub → día siguiente réplica).
2. **G-REP-2**: alcance confirmado (todo pool0; excluidos técnicos `.ix-virt`/`.system`; trading_systems/documents y frigate media INCLUIDOS por confirmación explícita del owner).
3. Capacidad: pool2 free zpool ≥ 4,00T (de lo contrario NO_GO con cifras); pool0 saludable (scrub OK, sin errores); espacio pool0 para retención @repl-* 14d (estimar con delta medido).
4. **G-REP-3**: ventana con presupuesto de I/O exclusivo: sin G1B, sin vzdump full, sin migraciones sobre TrueNAS ese día/tramo; Echo cerrado (madrugada sábado-domingo propuesta).
5. Canal de ejecución verificado (SSH ariadna@truenas o consola middleware); **stack nativo desplegado y probado con fixture G-REP-0** (snapshottask+replication creados disabled sobre `pool2/fixrep`, 1 ciclo real + drill dataset/zvol verificado; el script `repl-pool0.sh` del paquete anterior queda DESCARTADO — mecanismo nativo zettarepl LOCAL).

## Operaciones (orden)
1. Crear dataset destino `pool2/pool0-replica` (sin quotas; sin `sync=always`; el readonly final lo aplica la tarea con `readonly:"SET"` — probado en fixture G-REP-0).
2. **1ª transferencia completa**: deshabilitar el schedule y ejecutar `replication.run_onetime` de la tarea validada en fixture (~2,35T; 7-11h estimadas a HDD; monitoreo horario: estado job, tasa, `zpool list` free pool2 ≥1,00T).
3. Al terminar: verificar `zfs list -r pool2/pool0-replica` (datasets hijos + zvols con volsize correcto) + 1 drill de lectura (clonar RO un dataset hijo y un zvol del destino).
4. **G-REP-4**: habilitar la tarea nativa (`replication.update enabled=true` + snapshottask enabled) con horarios 04:45/04:50; retención 14d origen (snapshottask) + destino según fixture; scrub mensual pool2 (`pool.scrub.create` primer domingo 00:00).
5. Registrar serie de crecimiento diario y estado en CAPACITY-FREEZE v2.

## Gates
G-REP-1..4 — todos owner; una aprobación general NO sustituye gates. K2-check del día: si Ceph se degrada (HEALTH_ERR) durante la ventana por causas externas, la réplica NO se aborta (no toca pool1) pero se registra.

## Riesgo / ABORT
Riesgo principal: I/O sostenido sobre TrueNAS ~8-12h (chasis hades: guests de trading quedan en idle nocturno — ventana con Echo cerrado obligatoria). ABORT de la transferencia: free pool2 < 1,00T durante el envío, o errores de checksum/IO, o degradación del chasis (temperatura/errores SMART) → detener send, dejar destino consistente (último snapshot recibido completo), documentar, reprogramar.

## Rollback
Desactivar cron (G-REP-4 no activado hasta validación); destruir `pool2/pool0-replica` = autorización INDEPENDIENTE e irreversible (jamás en la misma operación que otra cosa).

## DoD
1ª réplica completa VERIFIED (listing + drill de lectura); cron activo con 2º ciclo incremental OK al día siguiente; retención viva en ambos lados; estado registrado en la SPEC y bitácora.
