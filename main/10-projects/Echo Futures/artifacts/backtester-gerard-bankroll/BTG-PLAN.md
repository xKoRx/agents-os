---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-S02-DESIGN]]"
  - "[[BTG-S04-GOD-ADVERSARIAL]]"
  - "[[BTG-S05-REMEDIATION-AND-RESULTS]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-08"
---

# BTG-PLAN — Estado vigente y continuidad del backtester

## Propósito

Control operativo único del backtester de [[Echo Futures]]. El programa BTG de cinco shots conserva su cierre histórico acotado; la intervención vigente es **BTX-PERF**, autorizada por Owner el 8 de octubre de 2026, con cuatro shots: diseño, implementación, adversarial ejecutado y corrección/validación final. El objetivo es un experimento histórico integrado por modalidad, sustancialmente más rápido, reproducible y utilizable desde una interfaz pública, con el mismo dominio runtime. No optimizar ROI ni convertir una estrategia ganadora en criterio de correctness.

El contenido anterior completo se preserva en [BTG-PLAN antes de BTX-PERF, corte dc8961fb](https://github.com/xKoRx/agents-os/blob/dc8961fb6d55cb33d233b392e72c2b2baefdd8bd/main/10-projects/Echo%20Futures/artifacts/backtester-gerard-bankroll/BTG-PLAN.md). No se reescriben RED ni artefactos históricos como PASS. Los estados de aquel cierre y el callout anterior del proyecto padre no son el estado operativo de esta intervención.

## Contenido

### Estado vigente — BTX-PERF, apertura Primary CLOUD

```text
PROGRAM = BTX-PERF
PRIMARY_SESSION = OPEN_UNTIL_EXPLICIT_OWNER_CLOSE
PROGRAM_STATUS = PREFLIGHT_WITH_EXECUTION_ACCESS_GAP
CURRENT_ACTION = OWNER_RUN_FRESH_CLOUD_SHOT_1_PROMPT
SHOT_1_STATUS = PROMPT_READY_NOT_EXECUTED
SHOTS_2_3_4 = NOT_STARTED
OWNER_ACCEPTANCE = NOT_REQUESTED_NOT_GRANTED
NEW_PRODUCT_CHANGES = NONE
NEW_BACKTESTS_PROFILES_TESTS = NOT_RUN_BY_MANAGER
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED_OUT_OF_SCOPE
PROMOTION = NOT_ACCEPTED_NO_MERGE_OR_DEPLOY
```

Mandato vigente: adjunto Owner «PRIMARY MANAGER GOD CLOUD — RENDIMIENTO, EXPERIMENTO INTEGRADO Y CORRECTNESS», PROMPT_VERSION 1, fecha 2026-10-08; SHA256 del adjunto `6beac22dd02e0b4d8220f5b77f4b36832ae9b51d22cab2d155a8362bbacb5e63`. Reemplaza `BTG-PERFORMANCE-CONTINUIDAD-3H-ONESHOT.md` y su despacho GOD LOCAL; no ejecutar ese prompt anterior.

Para esta intervención se reemplaza la regla anterior de adversarial GOD LOCAL por **GOD CLOUD independiente con TOP independiente que escribe/ejecuta falsificadores**. GOD no escribe producto, tests, scripts, parches ni hace integración mecánica. El permiso de dirigir repairs no autoriza promoción, merge/rebase preventivo, despliegue, órdenes, PROD/ETCD, broker, cuentas ni ampliación de permisos. El read-only del antiguo evaluador no bloquea la implementación que recibirán Shots 2 y 4. El nombre histórico s06 de su carpeta no numera este programa.

### Reloj y consumo

Primera observación de reloj registrada al arrancar este manager: **2026-10-08T21:16:02-03:00**, America/Santiago. No se equipara al T0 original de los 180 minutos.

```text
OWNER_WINDOW_T0 = UNKNOWN
OWNER_DEADLINE_180M = UNKNOWN
OWNER_REMAINING_180M = UNKNOWN
OWNER_CALENDAR_LIMIT_EXCLUSIVE = 2026-10-09T00:00:00-03:00
```

El prompt anterior, recuperado en Library, establece 180 minutos desde su inicio efectivo, pero no contiene recibo de ejecución/T0. Su creación/upload no demuestra ese inicio. No hay extensión autorizada ni tres horas nuevas por sesión. El techo calendario no prueba el remanente de los 180 minutos. Recuperar sólo un recibo verificable o una última ventana expresamente autorizada; conservar UNKNOWN mientras falte y declarar desfase si se cruza la fecha.

Distribución inicial orientativa del remanente real: 20% diseño/preflight, 35% implementación, 20% adversarial y 25% corrección/validación. No son estimaciones garantizadas ni permiso para extender deadline. Identidad ejecutada/modelos de workers/tokens/consumo de pool no expuestos: UNKNOWN. No cargar un despacho planeado ni inferir +1; contador global leído, sin modificación por consumo no confirmado.

### Baseline y disponibilidad comprobada por el manager

Agents-OS master inicial observado: `dc8961fb6d55cb33d233b392e72c2b2baefdd8bd`. Echo `codex/btg-s05-id-invariance` HEAD observado: `50250a2b0df6106943108bf6bfe57552409f3d13`. Compare autenticado desde código `d1b1446d401f88cfa42dee2eb959120305f5a372`: dos commits, sólo `AGENTS.md` y `v3/backtester/README.md` modificados. Separar source, commits documentales y ejecutable medido.

GitHub autenticado de lectura comprobado; esta actualización usa escritura documental sobre master con blob SHA y readback. La superficie dispone de shell sandbox, pero repo, corpus y artefactos físicos de evaluación no están montados. No se acreditó SSH/MCP Daedalus, runner conectado utilizable ni despacho directo de especialistas. La consulta de integración no acreditó un runner existente; no se instaló/conectó infraestructura. No hubo compilaciones, perfiles, tests ni backtests por este manager.

Se recuperó el relato completo de evaluación en Library `Texto pegado(20261008-200718).txt`, backing file `file_00000000c7c0820e98cf3e7915293478`. Esto confirma lo que el evaluador reportó, no sus ejecuciones físicas. Los dos informes originales, inputs/outputs/recibos físicos nuevos y datos siguen pendientes de acceso. La metadata del release S05 está disponible; no se descargó/reconstruyó el bundle entero ni se lo confundió con la evaluación posterior.

**Única transferencia si no hay runner existente con acceso:** cápsula privada `BTX-PERF-INPUT-CAPSULE`, fuera del vault, manifiesto/hash/rutas relativas, con informes y descriptores realmente consumidos, 13 derivados autorizados y recibos de exclusiones/gaps, evidencia causal mínima NQZ5/replay pass-funded/reemplazo, comandos/mediciones/build pertinentes. Si el destino ya tiene corpus por hash, transferir sólo recibos/delta. No otra exportación NinjaTrader, otro clon por worker, `.env`, credenciales ni ACL. La cápsula está **requerida/no creada por este manager**. Sus localizadores se resuelven desde los recibos existentes; el mandato de despacho conserva los localizadores externos aportados por Owner sin convertirlos en paths universales.

### Evidencia nueva — obligaciones abiertas, no diagnósticos inventados

Clasificación: OWNER_REPORTED, recuperada del texto del evaluador; raw original pendiente. No anular estos hallazgos por falta de un recibo ni dar por demostrada la causa raíz.

- Corpus reportado: 13 contratos, extremos 2023–2026, 1.096.110 filas retenidas = 1.096.336 originales − 226 exclusiones. Segmentos aproximadamente 124 días-equivalentes/15,6%, no trayectoria continua. Labels del calendario derivado no prueban por sí solos autoridad histórica del exchange.
- Full-extent rechazado por `SOURCE_COVERAGE_INCOMPLETE`. Hubo 14 BASIC con retry/replays, cuatro campañas/segundas ejecuciones e intentos adicionales; 13–14 procesos, inputs stale y rutas guessed. NQU6 BASIC ~88 min y CAMPAIGN ~67 min bajo concurrencia no son baseline aislado ni diagnóstico de CPU/I/O.
- NQZ5 CAMPAIGN: `LEDGER_HISTORY_RELEASE_FAILED: recorded revision 4870 is not current authority 4872`, después de burn/reemplazo y una frontera de contexto; BASIC del tramo termina. «Reset» sigue siendo hipótesis. Reconstruir revisiones, reentrancia y ownership.
- Replay de campaña: `KIND_MISMATCH`, expected ACCOUNT_REPLACEMENT / actual OPERATION_APPLY; readmisión pass-funded sin typed payload. Dos fallos idénticos no son replay exitoso.
- Pases de la evaluación multianual: **UNRESOLVED**. El resumen declara cero, pero el relato menciona control pass-funded de cuenta 2; conciliar solicitud, aplicación y traza antes de publicar una cifra. No confundirlo con el resultado histórico S05.
- Preparador/campaign monostream, help incompleto y stdout sin ruta causal: carencia de producto/usabilidad, no sólo datos externos. Baseline de hardware reportado 24 cores/64 GB disponibles/6 GB libres en raíz no acredita recursos actuales; medir cuotas/carga/espacio efectivo.

### Cuatro shots — registro único del manager

| Shot | Owner funcional / modelo solicitado / superficie | inputSHA | Estado | Evidencia / salida |
|---|---|---|---|---|
| 1 | Arquitecto GOD GPT-6 Astra CLOUD, distinto del manager | source d1b1446d; docs 50250a2b; mandato 6beac22d… | PROMPT_READY_NOT_EXECUTED; acceso/profiling pendientes | Prompt externo 4c39d4e1…; esperado `BTX-PERF-DESIGN.md`, aún no creado |
| 2 | Integrador TOP GPT-6.1 Sol CLOUD con runner autorizado | PENDING_ACCEPTED_DESIGN | NOT_STARTED | Esperado `BTX-PERF-IMPLEMENTATION.md`, aún no creado |
| 3 | GOD GPT-6 Astra CLOUD independiente + TOP falsificador independiente del autor | PENDING_IMPLEMENTATION | NOT_STARTED | Esperado `BTX-PERF-ADVERSARIAL.md`, aún no creado; no sustituir pruebas por source review |
| 4 | TOP GPT-6.1 Sol CLOUD fresco + comprobación TOP independiente acotada | PENDING_ADJUDICATED_FINDINGS | NOT_STARTED | Esperado `BTX-PERF-FINAL.md`, aún no creado |

Todos los artefactos esperados pertenecen a este mismo directorio. No crear otro control paralelo, árbol de submanagers o quinto shot. Revisión final TOP acotada dentro de Shot 4 no es otra auditoría general. Sólo el Owner acepta el objetivo; manager permanece abierto.

### Objetivo integrado y criterios de adjudicación

BASIC USD100000 continuo, todas las oportunidades admisibles, sin lifecycle prop. CAMPAIGN caja5000, compra ON_DEMAND120, una cuenta operando, máximo cuatro cobros efectivos por cuenta y reinversión. Pérdida nominal no vuelve a cargarse a caja. Strategy/MM por composición compartida; S2/GerardMM y parámetros actuales son prueba congelada, no objetivo de optimización ROI. Perfil FUNCTIONAL_ASSUMPTIONS, no reglas de prop externamente verificadas.

Shot 1 decide partición/concurrencia con evidencia: comparar preparación/cálculo independiente por contrato y unificación frente a otras particiones, conservando dependencias de Strategy, cuenta/riesgo, MM, órdenes, día contable y lifecycle/caja. Ni un hilo para todo como dogma ni trece simulaciones reiniciadas sumadas. Contraejemplo A→B obligatorio, workers/orden de entrega adversos y equivalencia demostrada. Estar flat o hacer rollover no prueba independencia.

Debe decidir hot path/fidelidad, entrada multicontrato para ambos modos, rollover/warmup/gaps, repairs de historial/reemplazo/replay y una interfaz pública con una especificación y primera causa real. No if Gerard, precios/fills inventados, guardas relajadas, dinero flotante, desactivación de recorder ni comparación permisiva. Módulo genérico desconocido conserva fallback correcto. No cambiar Strategy/MM para acelerar.

`MAX_WALL_PER_MODE`, `MIN_SPEEDUP_TARGET`, objetivo throughput y RSS: **NOT_FIXED**, responsabilidad Shot 1 antes de implementar, fundamentados en baseline aislado/workload activo/recursos reales. No adoptar 88 min bajo contención ni inventar target. Sin evidencia material, diseño candidato bloqueado; no aceptar criterios pendientes ni cambiarlos para pasar. Outputs y replay cuentan en el presupuesto.

Gates iniciales del objetivo BTX-PERF: **Correctness FAIL** por fallos nuevos reportados (raw/reproducción manager no realizados); **Performance NOT_DEMONSTRATED** sin contrato numérico comparable; **Usabilidad integrada FAIL** por limitación documentada/reportada; **Cobertura FAIL** porque el horizonte continuo solicitado no fue entregado. Son evaluación inicial del objetivo, no resultados de tests ejecutados por este manager. No READY_FOR_OWNER_ACCEPTANCE hasta resolver obligaciones materiales con evidencia nueva. PHYSICAL_RUNTIME_READINESS permanece fuera de alcance.

### Despacho exacto y persistencia

Prompt completo fresh-context: Library `/BTX-PERF-S01-GOD-CLOUD-PROMPT.md`, `library_file_id=libfile_864dc5b619548191bab98b8956408203`, backing `file_00000000d9c0820eb990a83b2bce4685`; SHA256 `4c39d4e1c0d893ceac2b70dd15f37ad6464bec8ab1d767bed82ddbce6a6f6885`. Es artefacto de transporte, no diseño ejecutado ni nota canónica duplicada. El Owner lo transporta a una nueva sesión GOD CLOUD y devuelve su artefacto; no diseña tareas ni reconstruye historia.

Control actualizado sobre la nota existente, schema_version1. No se crearon notas canónicas nuevas con frontmatter manual. **CHANGE_LOG_PENDING_WRITER:** materializar conforme al contrato vigente un registro consolidado de apertura BTX-PERF en `80-agents/journal/logs/` dentro de la siguiente persistencia documental autorizada, sin otro shot. Contenido del delta: autoridad Owner nueva, overrides CLOUD/cuatro shots, HEADs verificados, hallazgos reportados frente a raw pendiente, reloj UNKNOWN sin extensión, prompt Library/hash, cero cambios/ejecución de producto y sesión manager abierta. La auditoría inmediata queda en este commit; no se afirma que el change_log canónico ya exista ni que el vault físico esté sincronizado. Nuevos artefactos de especialistas deben materializarse/validarse mediante contrato y readback o devolverse como PENDING_WRITER; no inventar commits.

## Baseline histórico BTG-S05 — preservado, no extendido a BTX-PERF

El Primary anterior cerró por Owner el 8 de octubre de 2026 con `PASS_BOUNDED_OFFLINE_SOFTWARE`, 16 findings S04 cerrados y fix de invariancia de IDs verificado. Producto `d1b1446d401f88cfa42dee2eb959120305f5a372`; docs `50250a2b0df6106943108bf6bfe57552409f3d13`; CLI SHA256 `520d5343a1171796b67daa43875ac71ebeb9ce2c5ad39f84737c7adba44a84f1`. **La reejecución final d1b terminó: no volver a pedirla como pendiente.** Ventana NQZ3 warmup2023-10-15T22:00Z, trading2023-10-29T22:00Z, fin exclusivo2023-11-23T03:29Z, CONFIGURED/OHLC_CAUSAL_PATH_V2.

BASIC histórico: 116fills, bruto−34900, fees8505.84, neto−43405.84, saldo56594.16USD. CAMPAIGN histórica: 22fills, neto−6151.60 agregado, caja4640USD, 3compras/2reemplazos/0cobros, cuentas1/2 quemadas y3activa; saldo final nominal de cuentas97996.16/97851.24/98001, inventario flat. Caja5000−3×120=4640. Wall first/replay: BASIC826.715/911.089s; CAMPAIGN751.442/721.335s, con concurrencia; no benchmark aislado. Replays frescos exactos según evidencia independiente LOCAL, no reejecutados por este manager.

Release [btg-s05-id-invariance-d1b1446d](https://github.com/xKoRx/echo/releases/tag/btg-s05-id-invariance-d1b1446d), paquete `BTG-S05-FINAL-RERUN-d1b1446d.tar.gz`,112640203bytes,SHA256 `e95b178e61240ca39200f8da6be23c9c62554b2661b9821d7fe1f249062fa907`;102archivos según recibo. No atribuir informe base1ab a d1b ni porcentajes de cobertura anteriores a una nueva build. Scripts originales/RED/evidencia inmutables conservados; adaptación de localizadores no cambia oráculos/dinero ni habilita producto físico.

El plazo original BTG fue 7 de octubre; cierre el8, incumplimiento temporal preservado. FULL_2023_2026_CONTINUITY no certificado, promoción no aceptada, D6 ENVIRONMENTAL_BLOCKED en otra build. Nuevo riesgo físico sigue fail-closed sin snapshot completo/autoridad necesaria; backtest no demuestra ese productor ni conectividad/broker.

## Fuentes

- Mandato Owner BTX-PERF adjunto del8oct2026, hash y alcance arriba; supersede el despacho GOD LOCAL anterior.
- Relato de evaluación aportado por Owner y recuperado en Library `Texto pegado(20261008-200718).txt`; raw físico nuevo aún no inspeccionado por manager.
- [README canónico del producto](https://github.com/xKoRx/echo/blob/50250a2b0df6106943108bf6bfe57552409f3d13/v3/backtester/README.md) y compare autenticado d1b→5025, sólo documentos.
- [[BTG-S05-REMEDIATION-AND-RESULTS]], [[BTG-S04-GOD-ADVERSARIAL]] y [[BTG-S02-DESIGN]]: baseline/regresiones y restricciones no reemplazadas por el mandato nuevo.
- [Control anterior completo preservado](https://github.com/xKoRx/agents-os/blob/dc8961fb6d55cb33d233b392e72c2b2baefdd8bd/main/10-projects/Echo%20Futures/artifacts/backtester-gerard-bankroll/BTG-PLAN.md). Cierre/feedback históricos: [[2026-10-08-echo-backtester-primary-close]], [[2026-10-08-echo-backtester-primary-session-feedback]].
