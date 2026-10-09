---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTG-S05-REMEDIATION-AND-RESULTS]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-09"
---

# BTG-PLAN — Estado vigente y continuidad del backtester

## Propósito

Control operativo único del backtester de [[Echo Futures]]. BTG conserva su cierre histórico acotado. La intervención vigente BTX-PERF tiene cuatro shots: diseño, implementación, adversarial independiente ejecutado y corrección/validación final. Objetivo: una trayectoria histórica integrada por modalidad, utilizable por interfaz pública, reproducible y con rendimiento medido, conservando el dominio runtime y módulos Strategy/MM sustituibles. No optimizar ROI ni certificar rentabilidad.

El control anterior completo queda preservado en Git, commit `52d17ce92321fe0673eeaf1ed59d7e8753d47af7`, mismo path. Esta edición reemplaza sus estados de apertura, bloqueo previo a S02, superficie de S02 y reloj operativo; no borra RED, evidencia o deltas concurrentes. La adenda Owner del9oct2026 prevalece sobre instrucciones históricas del diseño o del plan que pidan otro E1/diseño antes de repairs.

## Contenido

### Autoridad vigente — aceptación técnica S01 y autorización acotada S02

```text
PROGRAM = BTX-PERF
PRIMARY_SESSION = OPEN_UNTIL_EXPLICIT_OWNER_CLOSE
S01_TECHNICAL_DESIGN = ACCEPTED_FOR_IMPLEMENTATION_WITH_EXPLICIT_PERF_EXCEPTION
E1 = PARTIAL_WITH_EVIDENCE
S02 = AUTHORIZED_REPAIR_AND_INTEGRATION
PERF_TARGET_FREEZE = REQUIRED_BEFORE_OPTIMIZATIONS
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
CURRENT_ACTION = OWNER_RUN_SINGLE_FRESH_TOP_LOCAL_S02_PROMPT
S02_EXECUTION = NOT_OBSERVED_BY_PRIMARY
S03 = NOT_STARTED_INDEPENDENT_EXECUTED_ADVERSARIAL_PRESERVED
S04 = NOT_STARTED_CORRECTION_AND_FINAL_VALIDATION_PRESERVED
NEW_PRODUCT_CHANGES_BY_PRIMARY = NONE
NEW_PRODUCT_TESTS_PROFILES_RUNS_BY_PRIMARY = NONE
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED_OUT_OF_SCOPE
PROMOTION = NOT_ACCEPTED_NO_MERGE_OR_DEPLOY
```

Owner aprueba arquitectura y contratos técnicos de [[BTX-PERF-DESIGN]] con las precisiones de su adenda «CIERRE TÉCNICO S01 Y AUTORIZACIÓN ACOTADA DE SHOT 2». No aprueba producto, no completa E1 ni crea otro shot. Autoriza un único integrador TOP LOCAL fresh-context ONE-SHOT en Daedalus, con el acceso usado por E1. Primary permanece coordinador CLOUD, sin código de producto/tests/scripts ni integración mecánica; no acepta su propio gate. No insistir en S02 CLOUD sin runner acreditado.

### Secuencia vinculante dentro de S02

1. Recuperar evidencia existente y capturar CPU del baseline usando R sellado, timeout120s y herramientas autorizadas; una corrección mecánica de instrumentación como máximo.
2. Implementar repairs de correctness, entrada integrada y replay.
3. Congelar source/build de control corregida, con integración funcional y sin optimizaciones de rendimiento.
4. Fijar y sellar contrato numérico con evidencia comparable.
5. Aplicar únicamente optimizaciones sustentadas y compararlas contra ese control corregido.

Los objetivos se congelan antes del primer cambio destinado a mejorar rendimiento, no sólo antes de medir el candidato. Esto incluye gzip rápido, valuación incremental, índices, fast paths y paralelismo de preparación usado para acelerar. La interfaz integrada puede disponer de una preparación secuencial correcta en el control; no se introduce otro motor financiero de referencia. No esconder optimizaciones en el commit de repairs ni mover objetivos después de ver resultados.

Sin evidencia suficiente para sostener el contrato completo: entregar repairs/integración/replay verificados y bloqueo preciso de performance dentro del mismo S02, con optimizaciones no iniciadas. No inventar números, optimizar a ciegas, pedir otro GOD/probe exploratorio o declarar listo el objetivo total. Un fallo de profiling no revoca la autorización de repairs.

### Reloj y límites

```text
HISTORICAL_CALENDAR_DEADLINE = 2026-10-09T00:00:00-03:00
HISTORICAL_WINDOW_STATUS = EXPIRED
HISTORICAL_180M_T0 = UNKNOWN
S02_CONTINUATION = EXPLICITLY_AUTHORIZED_BY_OWNER
NEW_TOTAL_OWNER_TIME_BUDGET = NOT_SPECIFIED
CPU_DIAGNOSTIC_TIMEOUT_SECONDS = 120
PROBE_SUGGESTED_4H_BUDGET = NOT_APPROVED
```

No reiniciar180min, no adoptar4h del probe ni convertir el timeout CPU en presupuesto total. Registrar inicio/límites reales del harness como límites de ejecución, no autorización Owner inventada. La fecha vencida no bloquea el alcance que Owner acaba de autorizar. Ningún proceso propio queda corriendo para otra sesión.

### Entradas fijadas y evidencia disponible

| Entrada | Identidad y alcance |
|---|---|
| Echo source/documentación | `50250a2b0df6106943108bf6bfe57552409f3d13`; HEAD remoto de `codex/btg-s05-id-invariance` confirmado sin cambio en este turno |
| Código histórico | `d1b1446d401f88cfa42dee2eb959120305f5a372`; dos commits documentales hasta50250a2b, no nueva build atribuida por Primary |
| Binario E1 | SHA256 `66657a99384ff6e622da15cd6953ea34621edc35100b536f118d1ff3918a89fb` |
| Diseño vigente | `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTX-PERF-DESIGN.md`; materializado en Agents-OS master, commit `8942ee2f236d2c84b9c83cc95334588977f0bdac`, con aceptación/adenda delante de la entrega histórica |
| Original de transporte S01 | Library `BTX-PERF-DESIGN.md`, backing `file_000000009700820e8a3386507c9564dc`, versión1; SHA256 leído `a792532bdaead5589aa05721369f5861c1807c7989dc4b048e5b59664bde9262`; no es el hash de la nota canónica |
| Registro E1 | commit `52d17ce92321fe0673eeaf1ed59d7e8753d47af7`, `80-agents/journal/logs/2026-10-08-btx-perf-s01-e1-local-probe.md` relativo a VAULT_ROOT |
| Cápsula E1 | Ya existente localmente según Owner y registro remoto; el commit NO contiene la cápsula íntegra. Verificar hashes y consumirla en Daedalus, no regenerarla |
| Evaluación anterior | Informes/inputs/prepared/outputs/replay/logs referenciados por E1; nombre histórico s06 no numera este programa |

Localizadores externos de Daedalus, aportados por Owner, se conservan en el prompt de transporte S02 y en el registro E1. No son rutas de VAULT_ROOT ni montaje acreditado en CLOUD. E1 root reportado `aranea/work/btx-perf-s01-e1-20261008/` relativo al home del usuario autorizado; contiene `BTX-PERF-E1-EVIDENCE.md` y `BTX-PERF-INPUT-CAPSULE/manifest.json`. Evaluación previa bajo `aranea/work/btg-s06-user-oneshot-20261008/`. Resolver las rutas precisas desde esos recibos; no exportar NinjaTrader otra vez, clonar por worker, ampliar ACL o reconstruir paquetes grandes.

Primary leyó el diseño completo y el registro remoto E1; no inspeccionó bytes de la cápsula física ni ejecutó el probe. Acceso LOCAL usado por E1 queda aceptado como entrada del despacho, sujeto a comprobar identidad/hashes al ejecutar, no a otra investigación de conexiones.

E1 reportó R BASIC89,64s/73,3MiB y CAMPAIGN90,04s/73,5MiB. Registro remoto: NQU6, warmup2026-07-05T22:01Z hasta fin exclusivo2026-07-19T23:00Z, exposición/SL ejercitados; CPU163,5s/167,9s y campaña caja4880. Son prefijos con warmup, no horizonte completo ni speedup. CPU/allocs no capturados; H no medido. E1 conserva PARTIAL_WITH_EVIDENCE aunque S02 capture CPU después.

### Contratos congelados y precisiones Owner

**Experimento:** BASIC nominal100000 continuo sin lifecycle prop; CAMPAIGN caja5000, compra ON_DEMAND120, una cuenta operando, máximo cuatro cobros efectivos y reinversión. No sumar campañas reiniciadas ni cargar otra vez una pérdida nominal a caja. Mantener configuración funcional y dominio compartido; S2/GerardMM son módulos de prueba, no lógica del driver ni objetivo ROI.

**Paralelismo:** preparación/lectura por stream, buffers acotados y merge estable antes del dominio. Finalización de workers no ordena dinero. Strategy/MM/riesgo/cuenta/caja conservan dependencias. Diseño: C financiero1, pool preparación hasta2 sujeto a recursos, chunks acotados256registros/1MiB serializado según diseño; esa cota no demuestra RSS. Sin otro motor de indicadores ni partición financiera por contrato. Contraejemplo A→B y workers/orden adverso son obligaciones de prueba, no arquitectura por rediseñar.

**Historial:** mecanismo localizado por E1 y precisado por Owner: SetAccountContext(k), CloseStage(k+1), OpenStage(k+2), luego recordEconomics(k) y release contra autoridad k+2. Conservar todas las revisiones comprometidas, publicar autoridad final coherente y liberar sólo evidencia poseída del ledger correcto. Mantener guard corriente. Prohibidos LatestRevision como descarte de intermedias, guard<= e ignorar error. Cubrir día, reemplazo, referencias prestadas, reentrancia y writer/Close fallidos. La primera nueva ejecución histórica NQZ5 comprueba la reparación; no redescubre la causa.

**Controles:** congelar cuerpo tipado/digest al admitir, independientemente de APPLIED/REJECTED/CONFLICT/pendiente; aplicación fallida no pierde su cuerpo. Mantener idempotencia y conflictos sin sobrescribir primera admisión. **Replay:** reconstruir modalidad completa y controlador CAMPAIGN; contrastar reemplazos, controles, compras, cobros y caja. Original esperaba ACCOUNT_REPLACEMENT; reproducción produjo OPERATION_APPLY. No invertir causalidad ni borrar records. No readmitir externamente controles regenerados por el controlador.

**Multicontrato:** petición común, catálogo físico completo, schedule prospectivo y warmup por requisitos; obligaciones del contrato retirado sobreviven. Una selección futura no es por sí sola deuda corriente. No copiar año/mes del inicial al seleccionado ni usar siempre catalog[0] como sesión. Política funcional de rollover del diseño necesita identidad/calendario declarados que resuelvan instantes; no inventar fechas, feriados, precios/fills ni continuidad sobre gaps desconocidos. Un bloqueo de datos no se usa como excusa para CLI/replay defectuosos.

**Equivalencia:** dinero exacto, composición sustituible, callbacks/protección/reservas/claims/finality conservados. Sin if Gerard, ajustes de SL/TP/sizing/adds/señales o recorder descartado. Diferencias entre builds/horizontes sólo tipadas y justificadas; mapeos de IDs uno-a-uno con referencias preservadas. Nunca eliminar genéricamente hashes/IDs/timestamps/kinds. Comparar control corregido con optimizado en idéntica semántica/workload; campaña vieja abortada no sirve de denominador.

**Lifecycle:** reconciliar separadamente PASS latched, solicitud, admisión y aplicación FUNDED, estado activo y cobros. No repetir0pases sin resolver estas disposiciones. Cuarto solicitado pendiente no equivale a cuarto cobrado; residual forfeited no es caja. Compra aplicada no equivale a activación y no se inventa refund.

### Contrato de performance — obligatorio antes de optimizar, no antes de reparar

Valores actuales MAX_WALL_PER_MODE/MIN_SPEEDUP_TARGET/MAX_RSS/throughput: **NOT_FROZEN**. S02 fija el contrato completo después del control corregido y antes del primer cambio de rendimiento. Debe incluir horizonte completo solicitado por modalidad, recursos/actividad/workload comparables, C financiero fijada, ejecución y outputs/Close, replay y comparación; separar mediciones de objetivos proyectados con supuestos y sensibilidad. Conservar bytes/hash del bloque congelado y evidencia del orden control→sello→optimización.

No adoptar53,5µs/root-input para todos los años,180/220s de NQU6 como horizonte integral,2× como mejora demostrada o512MiB como máximo multianual verificado. Aborto más rápido no es mejora del objetivo. Un horizonte limitado por datos no sustituye al solicitado. No extrapolar88/67min bajo13–14procesos como benchmark aislado ni volver a lanzar ese lote.

Captura CPU primero sobre R sellado, timeout120s; no repeticiones/escaneos/ritual documental antes. Una corrección mecánica instrumental máxima. No servicios nuevos, cambios de permisos, recorder/factories desactivados ni alteración de fidelidad. Instrumentado no equivale a tiempo normal; pasos despachados no equivalen a omitidos. Volumen/actividad/bytes y límites efectivos se obtienen del material existente; coste dominante no se presupone.

### Registro de cuatro shots

| Shot | Responsable / superficie | Input y estado | Salida |
|---|---|---|---|
| S01 | GOD CLOUD especialista | Diseño aceptado por Owner con excepción explícita; E1 PARTIAL_WITH_EVIDENCE | BTX-PERF-DESIGN materializado, commit8942ee2f; E1 registro52d17ce9 |
| S02 | Un TOP GPT-6.1 Sol LOCAL, fresh-context ONE-SHOT | AUTHORIZED_REPAIR_AND_INTEGRATION; prompt emitido, ejecución no observada por Primary | BTX-PERF-IMPLEMENTATION, aún no recibido |
| S03 | GOD CLOUD independiente + TOP falsificador independiente con ejecución acreditada | Preservado, no iniciado; no sustituir ejecución por source review | BTX-PERF-ADVERSARIAL |
| S04 | TOP fresco y comprobación independiente acotada conforme al mandato vigente | Preservado, no iniciado; correcciones y validación final | BTX-PERF-FINAL |

No quinto shot, nuevo diseño/E1 ni reactivación de workers cerrados. Fuente/modelos/consumos reales o UNKNOWN; no atribuir cuota a un despacho planeado o a una sesión LOCAL. La aceptación técnica S01 no convierte los cuatro gates del programa en PASS. Correctness, performance, usabilidad integrada y cobertura conservan FAIL/NOT_DEMONSTRATED donde corresponda hasta evidencia nueva. No PASS por rc0, source review, aborto idéntico o conciliación aislada. PHYSICAL_RUNTIME_READINESS fuera; sin D6, broker, cuentas, ETCD/PROD, órdenes, permisos, merge o deploy.

### Despacho único S02 y persistencia

Prompt completo fresh-context: Library `/BTX-PERF-S02-TOP-LOCAL-PROMPT.md`, `library_file_id=libfile_ddc9a3c286c48191ad89688c82bca501`, backing `file_00000000802c820e8cf5d11c444bef7d`; SHA256 `eef0f184136e24dd71f2f48541248a695c45a52515b8e55debea28c2a7c4acaf`. Es transporte del mandato, no resultado de implementación. Se entrega al Owner para una sesión TOP LOCAL; no hay despacho directo ni ejecución ficticia por Primary.

S02 entrega source/builds exactas, repairs/regresiones ejecutadas, contrato o límite preciso, comparación causal/métricas/artefactos transportables, README con comandos realmente ejecutados y delta del control. Worker deja feedback, agent-run atribuible y cierra sólo su sesión con procesos propios terminados; no cierra Primary. Si falla persistencia, devuelve delta/evidencia sin inventar commit. Agents-OS sólo master y readback; preservar cambios concurrentes.

Registro documental consolidado de esta adenda y materialización: [[2026-10-09-btx-perf-s02-owner-amendment]]. Incluye el delta de apertura que seguía pendiente de change_log, sin recrear sesiones ni modificar el registro E1. Materialización mediante scripts/templates originales verificados en copia documental sandbox, con proyección de tipo doc/change_log del contrato vigente; no lint global, ejecución de producto o sincronización física de Daedalus.

## Baseline histórico BTG-S05 — referencia, no certificación BTX-PERF

Cierre anterior por Owner8oct2026: PASS_BOUNDED_OFFLINE_SOFTWARE sobre d1b1446d,16findings S04 cerrados e invariancia de IDs verificada. La reejecución final d1b terminó; no volver a pedirla como pendiente. Ventana NQZ3 warmup2023-10-15T22:00Z, trading2023-10-29T22:00Z, fin exclusivo2023-11-23T03:29Z; CONFIGURED/OHLC_CAUSAL_PATH_V2. Binario histórico S05 `520d5343a1171796b67daa43875ac71ebeb9ce2c5ad39f84737c7adba44a84f1`, distinto de E1.

Resultados históricos: BASIC116fills, neto−43405.84USD, saldo56594.16; CAMPAIGN22fills, neto agregado−6151.60, caja4640,3compras/2reemplazos/0cobros. First/replay BASIC826.715/911.089s y CAMPAIGN751.442/721.335s bajo concurrencia, no benchmark aislado. Evidencia detallada en [[BTG-S05-REMEDIATION-AND-RESULTS]] y release `btg-s05-id-invariance-d1b1446d`; paquete final112640203bytes, SHA256 `e95b178e61240ca39200f8da6be23c9c62554b2661b9821d7fe1f249062fa907`. No trasladar estos resultados/cobertura/build al candidato nuevo.

El objetivo BTG original vencía7oct y se cerró8oct: incumplimiento histórico preservado. Cobertura multianual completa y readiness física nunca se demostraron por ese cierre. D6 sigue separado, en otra build, y no se autoriza nuevo riesgo físico desde este programa.

## Fuentes

- Adenda Owner9oct2026 en esta sesión: aceptación técnica S01, E1 parcial, S02 LOCAL, secuencia de control/freeze/optimización y ventana histórica vencida.
- [[BTX-PERF-DESIGN]], entrega original recibida más precisiones vigentes; source/documentación50250a2b.
- E1 registro remoto52d17ce92321fe0673eeaf1ed59d7e8753d47af7; cápsula física consumible por integrador, no alojada en ese commit.
- Control anterior completo en52d17ce9, mismo path; [[BTG-S05-REMEDIATION-AND-RESULTS]] para baseline acotado.
