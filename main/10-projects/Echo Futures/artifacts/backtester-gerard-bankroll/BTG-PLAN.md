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

Control operativo vigente del programa de cinco shots: motor de backtesting fiel al dominio compartido de Echo Futures, con BASIC y CAMPAIGN, Strategy/MM sustituibles, evidencia reproducible y límites explícitos. El entregable es corrección del motor, no una estrategia ganadora. ROI, barridos de targets y holdout para escoger rentabilidad fueron retirados expresamente del alcance por Owner; no reabrirlos desde el plan inicial.

Esta edición concentra el estado actual para no obligar al siguiente agente a reconciliar varias secciones históricas llamadas «vigentes». El plan previo completo queda preservado en [Git, corte anterior al cierre Primary](https://github.com/xKoRx/agents-os/blob/91219e102d9ceb20807fa0e6c1b4b7e0eb5983ff/main/10-projects/Echo%20Futures/artifacts/backtester-gerard-bankroll/BTG-PLAN.md). Diseños, RED, decisiones y evidencia detallada no se eliminan: permanecen en sus artefactos y versiones.

## Contenido

### Estado vigente — cierre Primary solicitado por Owner, 2026-10-08

```text
PRIMARY_FINAL_REVIEW = PASS_BOUNDED_OFFLINE_SOFTWARE
S05_ENGINEERING_REVIEW = CLOSED_VERIFIED_SCOPE
PRIMARY_SESSION = CLOSED_BY_EXPLICIT_OWNER_REQUEST
PRODUCT_CODE_SHA = d1b1446d401f88cfa42dee2eb959120305f5a372
DOCUMENTATION_SHA = 50250a2b0df6106943108bf6bfe57552409f3d13
CURRENT_D1B_REAL_RUNS = BASIC_AND_CAMPAIGN_COMPLETE_WITH_EXACT_FRESH_REPLAYS
S04_FINDINGS = 16_CLOSED_WITH_INDEPENDENT_EVIDENCE
ID_INVARIANCE_FINDING = FIXED_REVIEWED_AND_REAL_RERUN_COMPLETE
FULL_2023_2026_CONTINUITY = NOT_CERTIFIED
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED
PROMOTION = NOT_ACCEPTED_NO_MERGE_OR_DEPLOY
NEXT = FRESH_ONE_SHOT_READ_ONLY_ALL_YEARS_USAGE_AND_FEEDBACK
```

El cierre técnico es acotado a la versión, capacidades, modelos y escenarios con evidencia disponible. No afirma corrección universal, rentabilidad, ejecución física ni continuidad de todos los años. La revisión Primary se apoya en lectura de source/deltas y evidencia independiente LOCAL; Primary no reejecutó los binarios ni reconstruyó todos los assets privados. La aceptación/promotion del producto completo y la habilitación LIVE no se conceden por esta nota.

**La reejecución final d1b ya está terminada. No volver a solicitarla como pendiente.** La entrega actual de [[BTG-S05-REMEDIATION-AND-RESULTS]] contiene los cuatro procesos y su verificación. Los estados `PRIMARY_FINAL_REVIEW=PENDING`/`NEW_REAL_RUNS_D1B=NOT_RUN` de handoffs anteriores describen sus cortes históricos; para continuidad del manager los supersede este control. S01/S03 fueron baselines acotados, S04 encontró defectos, S05 los corrigió con sus regresiones y corrigió además el desempate por IDs. No S06 ni nueva ronda de diseño por el cierre.

Plazo original: 7 de octubre de 2026 America/Santiago; entrega final y cierre ocurrieron el 8 de octubre. Incumplimiento temporal explícito, no fecha retroactiva ni reducción silenciosa de requisitos.

### Documentación canónica del producto

[Echo Backtester — README canónico](https://github.com/xKoRx/echo/blob/50250a2b0df6106943108bf6bfe57552409f3d13/v3/backtester/README.md), enlazado desde [AGENTS.md del repo](https://github.com/xKoRx/echo/blob/50250a2b0df6106943108bf6bfe57552409f3d13/AGENTS.md).

Fuente documentada d1b; commits40f19620/50250a2b cambian exclusivamente README/AGENTS. No cambian código, tests, datos, builds ni evidencia de ejecución. Publicados sobre la rama de producto existente `codex/btg-s05-id-invariance`; sin merge/deploy. Agents-OS permanece exclusivamente en master.

La guía contiene arquitectura, responsabilidades, paridad y límites, factories/warmup, BASIC/CAMPAIGN, velas/ticks/MIXED, fases causales y matching, dinero/retención, CLI/configuración, fuentes/gaps/rollover, errores, evidencia/replay, rendimiento/concurrencia y protocolo de uso ONE-SHOT con nota y feedback. Un agente usuario debe empezar ahí, no en transcripciones de cinco shots. Toda modificación técnica futura autorizada debe actualizar esa guía.

### Resultados finales verificados d1b

CLI SHA256 `520d5343a1171796b67daa43875ac71ebeb9ce2c5ad39f84737c7adba44a84f1`; build limpia/VCS exacto según evidencia LOCAL. Datos NQZ3; warmup `2023-10-15T22:00:00Z`; trading `2023-10-29T22:00:00Z`; fin exclusivo `2023-11-23T03:29:00Z`; S2/GerardMM CONFIGURED y OHLC_CAUSAL_PATH_V2.

| Resultado | BASIC | CAMPAIGN |
|---|---:|---:|
| Fills | 116 | 22 |
| PnL bruto USD | -34900 | -5305 agregado |
| Fees USD | 8505.84 | 846.60 |
| PnL neto USD | -43405.84 | -6151.60 agregado |
| Saldo nominal / caja personal USD | 56594.16 | 4640 |
| Compras / reemplazos / cobros | no aplica | 3 / 2 / 0 |
| Wall first / replay | 826.715 / 911.089 s | 751.442 / 721.335 s |
| Replay fresco | exacto | exacto, incluido export |

La caja cumple `5000−3×120+0=4640`; no carga otra vez pérdidas nominales. Cuentas1/2 quemadas y3 activa; saldos97996.16/97851.24/98001; inventario final flat. Los tiempos se midieron con carga concurrente y no acreditan un benchmark universal. La cobertura modificada95.66% corresponde al corte fuente/metodología de1ab; d1b tiene evidencia del delta, no se inventa un nuevo porcentaje global.

Release: [btg-s05-id-invariance-d1b1446d](https://github.com/xKoRx/echo/releases/tag/btg-s05-id-invariance-d1b1446d). Paquete final de reejecución `BTG-S05-FINAL-RERUN-d1b1446d.tar.gz`,112640203bytes,SHA256 `e95b178e61240ca39200f8da6be23c9c62554b2661b9821d7fe1f249062fa907`;102archivos según recibo. Leer README suplementario y fases actuales, no atribuir el informe base1ab a d1b. Scripts independientes originales conservan rutas absolutas históricas: localización scratch permitida por receta, sin cambiar asserts/dinero ni usar provenance antigua para otra ejecución.

### Restricciones que sobreviven al cierre

- Un dominio compartido Strategy/MM/Operation/Provider/accounting. Módulos sustituibles por composición; no variantes de negocio live/backtest, no postprocesamiento que reemplace decisiones. KISS/YAGNI, sin plugins dinámicos, DSL, optimizer ni otro motor.
- BASIC100000 continuo sin compras/retiros/lifecycle prop. CAMPAIGN5000, compra120 ON_DEMAND, una cuenta activa, máximo cuatro COBROS efectivos, reinversión y caja separada. Perfil económico FUNCTIONAL_ASSUMPTIONS, no reglas de una prop verificadas. Un cierre por pérdida no vuelve a debitar caja.
- Base1m; S2 usa5m/H4 cerradas. MM/protección reaccionan intrabar. OHLC es modelado, ticks observados conservan secuencia y MIXED selecciona una autoridad completa por minuto. LIVE stale jamás genera mercado sintético.
- Causalidad, cantidad protectora, claims hasta finality, dedup, no fills retrospectivos y prioridad/orden de aceptación son invariantes. No cambiar parámetros para restaurar un PnL histórico después de un fix.
- Un escritor por trayectoria dependiente; paralelismo limitado entre experimentos independientes. No partir días/cuentas/expiries de una campaña para sumar resultados.
- Toda certificación está ligada a SHA/build/config/corpus/fidelidad y evidencia. Replay idéntico no demuestra por sí solo seguridad; paridad usa además oráculos independientes. Economía inyectada en runtime no prueba productor financiero físico independiente.
- D6 sigue ENVIRONMENTAL_BLOCKED en otra build; adapter Ninja no acredita snapshot completo de cuenta requerido. Nuevo riesgo permanece fail-closed sin esa autoridad. Sin órdenes físicas, merge, deploy, PROD/ETCD ni ampliación de permisos desde este cierre.

### Todo el histórico: siguiente uso, no nueva implementación

Los13exports cubren extremos2023–2026 pero contienen gaps; falta autoridad histórica completa de calendario/schedule. El hueco al extender la ventana verificada empieza `[2023-11-23T03:29Z,03:30Z)`. No inventar feriados, rellenar precios o liquidar sin fuente. Los originales ya están en `daedalus:/home/hermes-ops/echo-dev/history/nq/`; el README da localizadores alternativos/receipts. No pedir otra exportación Windows.

**Capacidad del núcleo no equivale a interfaz lista para cualquier uso:** `prepare-functional-nt` y `campaign` del CLI admiten un stream físico NT; Campaign CLI no expone composición multicontrato/MIXED genérica. El núcleo tiene catálogo/schedule y APIs públicas, pero el agente read-only no puede fabricar un runner ni inventar el schedule faltante. Debe intentar el horizonte completo por interfaces/autoridades existentes, reportar resultados realmente disponibles y distinguir bloqueo de datos, interfaz, documentación y producto. Los tramos independientes no se suman como una cuenta/caja continua.

Limitación documental detectada en el preparador: su metadata externa sigue rotuladaV1/NO_ADDS incluso pidiendoV2/CONFIGURED; RunSpec/config/resultado sellados son autoridad efectiva. Quedó visible en README; no hubo patch de producto ni se usa para esconder el error.

### Próximo despacho — independiente, fresco y ONE-SHOT

Owner reiteró que no quiere volver a las mismas conversaciones para cada corrección/uso. El próximo agente es usuario/evaluador, **sesión nueva ONE-SHOT**, no implementador. Recibe sólo el README canónico y la tarea: usar BASIC/CAMPAIGN sobre todos los años NQ disponibles, sin modificar producto/tests/estrategia/MM/originales; crear sólo inputs/artifacts externos permitidos, entregar resultado/reproducción/cobertura/bloqueos, nota1–7 de uso y feedback. No tuning ROI, fixes, wrappers de producto, commits, PRs, permisos o infraestructura. Sus permisos no se amplían por un procedimiento de cierre.

No agregar otra etapa al programa de desarrollo. El intento completo multi-año es validación de uso/cobertura, no requisito retroactivamente declarado cumplido. Si encuentra una carencia, entrega evidencia y propuesta mínima sin implementarla; una reparación posterior requiere una decisión nueva, no un ciclo ilimitado en la misma conversación.

Para futuras tareas complejas autorizadas: GOD decide/orquesta, cero código; TOP GPT-6.1 Sol implementa o revisa con independencia; Luna ejecuta mecánica delimitada. Cada especialista ONE-SHOT con ownership/pruebas/handoff. Ahorrar por asignación/contexto, no por quitar safety. No inferir modelos/tokens/costos no expuestos.

### Cierre de esta sesión

Primary cierra por instrucción explícita Owner. Persistencia: esta nota como única continuidad operativa del manager, documentación de producto y feedback/change_log del cierre. No transcript grande ni checkpoint interno duplicado. Feedback: [[2026-10-08-echo-backtester-primary-session-feedback]]. Registro de cambio: [[2026-10-08-echo-backtester-primary-close]].

Validación del cierre: escritura/readback de las rutas afectadas y compare de producto que acredita únicamente dos archivos Markdown. No ejecuciones de backtest, suite física, Graphify ni lint global en esta superficie. La ejecución canónica de materializador/validador de los tipos nuevos se realiza sobre copia documental local; se declara el alcance sin trasladarlo al vault físico.

## Fuentes

- Owner: cierre explícito, documentación completa en repo y nuevo usuario ONE-SHOT read-only, 2026-10-08.
- [[BTG-S05-REMEDIATION-AND-RESULTS]], corte final d1b con reejecución independiente y fases de publicación.
- [[BTG-S04-GOD-ADVERSARIAL]], RED/evidencia originales; [[BTG-S02-DESIGN]] y mandatos Owner posteriores para restricciones aplicables.
- [Producto d1b](https://github.com/xKoRx/echo/commit/d1b1446d401f88cfa42dee2eb959120305f5a372) y documentación50​250a2b (SHA exacto en estado; no confundir con build de producto).
- [Plan histórico preservado](https://github.com/xKoRx/agents-os/blob/91219e102d9ceb20807fa0e6c1b4b7e0eb5983ff/main/10-projects/Echo%20Futures/artifacts/backtester-gerard-bankroll/BTG-PLAN.md).
