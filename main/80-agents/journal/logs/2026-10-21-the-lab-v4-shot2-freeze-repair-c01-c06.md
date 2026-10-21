---
type: change_log
schema_version: 1
created: 2026-10-21
project: "[[The Lab]]"
tags:
  - kind/change-log
  - project/the-lab-v4
---

# 2026-10-21 — The Lab V4 Shot 2: paquete de freeze revisión 3 (corrige C01–C06)

- **Qué cambió:** en `10-projects/Echo/The Lab/V4 — Shot 2/`, `1 — TECHNICAL_FREEZE_PACKET.md` pasa a REVISIÓN 3 (estado pedido `TECHNICAL_FREEZE_READY_V3`) corrigiendo sólo C01–C06 del dictamen `TECHNICAL_FREEZE_REPAIR_REQUIRED_V2` (blob `40c16d50`), y `2 — Preflight Evidence (U01–U06).md` se corrige en E05/E08/E09/E12 más una tabla de correcciones rev 3; `0 — Submanager State.md` actualizado.
- **Decisiones aplicadas:** (C01) mecanismo de migración real reconocido — toolkit `apply-migration` = `db.Exec` de un archivo, sin golang-migrate ni tracking (afirmación de rev 2 corregida); adopción mínima con `echo.lab_migration_state` auto-registrada por cada archivo V4 dentro de su transacción implícita, cero delta de tooling; 066 jamás se registra como aplicada (efectos ausentes en DEV); 070 derivados aditivos separada de 071 retiro gated con retirement ledger (skip = BLOCKED_SKIP, no eliminación). (C02) receta `analytic-v1` retirada; extensión mínima del registro con `identity_recipe` sellada por fila (`sqx-v1` intacta para MT; `native-v1` con slots naturales; `definition-v1` con `strategy_definition_sha256` y slots de ejecutable NULL); modo LIVE/BACKTEST/REPLAY no crea StrategyVersion; caso de aceptación: misma definición + otro perfil ⇒ versión inmutable, revisión y derivados nuevos. (C03) sello QI_SEALED movido a la primera decisión MM del ciclo (materialización `engine.go:1051` precede a `invokeMM` `:1113`; `MMDecision` con DecisionIDs); SL×cantidad no es presupuesto por defecto; CYCLE_BUDGET exige método+evidencia; caso multi-entrada con primera entrada ≠ presupuesto. (C04) economía por Operation con identificación específica correlacionada (caso A/B: B=5), Ledger como autoridad de cuenta con conciliación publicada; movimientos publicados al reconocerse (parciales/costes de ciclo abierto); CLOSED_SUMMARY sin movements legítimo; modo/rol separados; backtester existente dentro de I1 por el mismo servicio y caso T sobre esa ruta. (C05) I1 sin GC automático concurrente (store append-only + protocolo de limpieza con quiesce); "commit sin artefacto imposible" corregido; cadena única de revisiones (head + revision_no) sustituye al superseded_by por movimiento. (C06) grano de historia intacto (sin división por símbolo; caso 132.805 ops preservado); límites 128 MiB request / 250k ops / 1M movements / 8 historias; tamaños V1 reclasificados como referencia y benchmark certifica envelope V2. Organización: fallback de ejecución propia eliminado (despacho alternativo de implementador o escalación explícita de cambio de rol).
- **Dónde:** repo vault (commits de este change_log); repos producto SIN cambios (SPEC only, read-only).
- **Por qué:** dictamen del Primary Manager 2026-10-21 (V2) exige corregir C01–C06 sin reabrir lo aceptado; los contratos a implementar no deben contradecir el producto ni el código base.
- **Sin cambios en:** decisiones ratificadas D09/D10/D11/D16, direcciones aceptadas de la rev 2, producto, PROD, Gateway, skills/constitución globales.
