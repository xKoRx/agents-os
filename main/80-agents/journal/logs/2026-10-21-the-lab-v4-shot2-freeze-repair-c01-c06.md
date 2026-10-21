---
type: change_log
schema_version: 1
scope: session
created: 2026-10-21
updated: 2026-10-21
project: "[[Echo — Producto Integrado]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/the-lab-v4
---

# 2026-10-21 — The Lab V4 Shot 2: paquete de freeze revisión 3 (corrige C01–C06)

- **Qué cambió:** en `10-projects/Echo/The Lab/V4 — Shot 2/`, `1 — TECHNICAL_FREEZE_PACKET.md` pasa a REVISIÓN 3 (estado pedido `TECHNICAL_FREEZE_READY_V3`) corrigiendo sólo C01–C06 del dictamen `TECHNICAL_FREEZE_REPAIR_REQUIRED_V2` (blob `40c16d50`), y `2 — Preflight Evidence (U01–U06).md` se corrige en E05/E08/E09/E12 más una tabla de correcciones rev 3; `0 — Submanager State.md` actualizado.
- **Decisiones aplicadas:** (C01) mecanismo de migración real reconocido — toolkit `apply-migration` = `db.Exec` de un archivo, sin golang-migrate ni tracking (afirmación de rev 2 corregida); adopción mínima con `echo.lab_migration_state` auto-registrada por cada archivo V4 dentro de su transacción implícita, cero delta de tooling; 066 jamás se registra como aplicada (efectos ausentes en DEV); 070 derivados aditivos separada de 071 retiro gated con retirement ledger (skip = BLOCKED_SKIP, no eliminación). (C02) receta `analytic-v1` retirada; extensión mínima del registro con `identity_recipe` sellada por fila (`sqx-v1` intacta para MT; `native-v1` con slots naturales; `definition-v1` con `strategy_definition_sha256` y slots de ejecutable NULL); modo LIVE/BACKTEST/REPLAY no crea versiones; caso de aceptación: misma definición + otro perfil ⇒ versión inmutable, revisión y derivados nuevos. (C03) sello QI_SEALED movido a la primera decisión MM del ciclo (materialización `engine.go:1051` precede a `invokeMM` `:1113`; `MMDecision` con DecisionIDs); SL×cantidad no es presupuesto por defecto; CYCLE_BUDGET exige método+evidencia; caso multi-entrada con primera entrada ≠ presupuesto. (C04) economía por Operation con identificación específica correlacionada (caso A/B: B=5), Ledger como autoridad de cuenta con conciliación publicada; movimientos publicados al reconocerse (parciales/costes de ciclo abierto); CLOSED_SUMMARY sin movements legítimo; modo/rol separados; backtester existente dentro de I1 por el mismo servicio y caso T sobre esa ruta. (C05) I1 sin GC automático concurrente (store append-only + protocolo de limpieza con quiesce); "commit sin artefacto imposible" corregido; cadena única de revisiones (head + revision_no) sustituye al superseded_by por movimiento. (C06) grano de historia intacto (sin división por símbolo; caso 132.805 ops preservado); límites 128 MiB request / 250k ops / 1M movements / 8 historias; tamaños V1 reclasificados como referencia y benchmark certifica envelope V2. Organización en la propuesta: fallback de ejecución propia eliminado (despacho alternativo de implementador o escalación explícita de cambio de rol).
- **Dónde:** repo vault (commits de este change_log); repos producto SIN cambios por esta reparación (SPEC only, read-only).
- **Por qué:** dictamen del Primary Manager 2026-10-21 (V2) exige corregir C01–C06 sin reabrir lo aceptado; los contratos a implementar no deben contradecir el producto ni el código base.
- **Sin cambios en:** decisiones ratificadas D09/D10/D11/D16, direcciones aceptadas de la rev 2, producto, PROD, Gateway, skills/constitución globales.

## Aceptación posterior del Primary Manager — 2026-10-21

- **Autoridad y motivo:** el Owner devuelve la revisión 3 y exige continuar los cuatro shots originales, sin más ciclos preparatorios de Shot 2. Metis acepta el contrato para implementación tras leer el paquete en el corte entregado; no certifica producto todavía no construido.
- **Paquete aceptado:** `xKoRx/agents-os@eb9ad25e`, `main/10-projects/Echo/The Lab/V4 — Shot 2/1 — TECHNICAL_FREEZE_PACKET.md`, blob `cee739a8f8ae7c0bfe2d7e30bc473c88ab608c78` (paquete también publicado en `5d6cae71`).
- **Estado nuevo:** `TECHNICAL_FREEZE_ACCEPTED_V3 / IMPLEMENTATION_AUTHORIZED`. Actualizado el planificador `0 — Submanager State.md` en commit `f747a05852d4939d44291e75df9a6a3d8bffd637`, blob `2cde9980f82506f2438c3dbd68e4417a147802c8`. Sustituye las esperas y dictámenes de reparación anteriores para este corte.
- **Cambio de ejecución:** no otra revisión general de freeze ni nueva entrevista. Precisiones de ingeniería y fallos ordinarios se resuelven con implementación/pruebas en Shot 2; se mantienen todos los invariantes, G1–G11/T01–T45 y casos C01–C06. Una entrada fijada por un resultado no puede mutar bajo la misma identidad reproducible.
- **Excepción explícita y acotada:** workers secuenciales preferidos; si el harness vuelve a fallar, el submanager queda autorizado por el Primary Manager a actuar como implementador/integrador serial con GLM-5.3-Flash Max en este mismo Shot 2, atribuyendo el trabajo como propio. No cambia de modelo/proveedor/cuota automáticamente y no reemplaza la independencia de Shot 3.
- **Límites:** autorización de source, integración en rama y pruebas locales/descartables autorizadas. No deploy/reinicio compartido, migración de base compartida, PROD, trading, campañas, merge de producto a master ni retiro destructivo sin autorización específica. Un bloqueo detiene solo la acción dependiente mientras pueda avanzar trabajo independiente.
- **Validación y alcance real:** se leyó el paquete V3 y el estado de master mediante GitHub; no se reejecutaron SQL, benchmarks ni tests de producto. La aceptación y esta actualización son documentación, no evidencia de implementación completada.
- **Próximo entregable:** código integrado y probado, evidencia de gates y paquete para Shot 3, o un bloqueo real que requiera autoridad nueva. No generar otro paquete de freeze. El submanager no cierra Agents-OS ni inicia Shot 3 por esta aceptación.
- **Rollback documental:** si el Owner modifica la dirección, actualizar el gate y registrar el delta; el historial de Git conserva las propuestas y los dictámenes previos. No se alteró el artefacto de diseño aceptado.

## Cambio de fase solicitado por el Owner — Shot 3 sobre candidato parcial, 2026-10-21

- **Fuente:** mensaje actual del Owner: dispone de GOD LOCAL y solicita continuar Shot 3/Shot 4; handoff adjunto del bloque 1 informa fundación, cuatro commits y pendientes I1 explícitos. No es una declaración de implementación completa.
- **Decisión:** `SHOT3_AUTHORIZED_ON_PARTIAL_CANDIDATE`; GOD LOCAL independiente audita el corte real reportado `61ac1f72` (resolver SHA completo localmente). No repetir freeze, no certificar capacidades inexistentes y no iniciar un quinto shot. Las restricciones anteriores que prohibían iniciar Shot 3 quedan sustituidas únicamente para esta admisión excepcional.
- **Actualización:** `10-projects/Echo/The Lab/V4 — Shot 2/0 — Submanager State.md` en commit `4cc51cc82364aba14180c516aa0f077443f76336`, blob `62c0b28433b5c89b3443e79e37009177c8e169db`. Conserva ratificaciones, diseño aceptado e historial; explicita `SHOT2_PARTIAL_DELIVERED` y la siguiente acción vigente.
- **Shot 4:** correcciones más cumplimiento de los faltantes del alcance I1 aprobado identificados por el auditor; el delta implementado después del corte tendrá pruebas y revisión independiente en contexto fresco como parte del gate final de Shot 4. No autoriza I2 ni bajar criterios.
- **Aislamiento:** se solicita pausar nuevas escrituras/despachos del implementador y fijar el corte; no se afirma que ya ocurrió. Auditor en worktree y PG descartable propios; prohibido limpiar/resetear el árbol ajeno. El incidente de pérdida de untracked se trata como riesgo de coordinación/evidencia, no como prueba automática de defecto del producto.
- **Validación y límites:** se leyó el handoff completo y el estado actual mediante GitHub. No se reejecutaron los 7 tests ni SQL. GitHub no resolvió `61ac1f72`; el acceso/commit local debe comprobarlo GOD, sin exigir publicación remota para auditar. No se modificó código, bases ni infraestructura y no se inició ningún agente por esta actualización.
- **Sin cierre:** no se cierra sesión, programa o gate final; no deploy, PROD, trading, merge de producto ni migración compartida autorizados. Rollback documental por nuevo delta Owner, preservando la historia Git.
