---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-06"
---

# BTG-S01-REAL-GERARD-RESULT

## Propósito

Conseguir el baseline histórico REAL de la Strategy Gerard exacta y GerardMM compartido, corregir defectos demostrados y entregar evidencia al Primary Manager para revisión. El submanager conserva continuidad; no acepta el gate Owner ni inicia S02.

## Contenido

### Resultado real consolidado — 2026-10-06

**El backtester completó y reprodujo el tramo probado; esta configuración perdió.** No se afirma cobertura continua de los tres años ni rollover histórico validado. El submanager permanece abierto y entrega el baseline acotado al Primary Manager; aceptación Owner y gate integral pendientes.

| Evidencia | Smoke RAW corregido | Longitudinal DERIVED corregido |
| --- | --- | --- |
| Warmup UTC | 2023-10-15T22:00Z | 2023-10-15T22:00Z |
| TradeStart → EndExclusive UTC | 2023-10-29T22:00Z → 2023-11-03T21:00Z | 2023-10-29T22:00Z → 2023-11-23T03:29Z |
| Contrato físico | NQ 12-23 / NQZ3 | NQ 12-23 / NQZ3 |
| Estado / fresh reproduce | COMPLETE / IDENTICAL | COMPLETE / IDENTICAL |
| Señales / operaciones materializadas / operaciones con fills / fills únicos | 60 / 30 / 12 / 24 | 225 / 113 / 39 / 78 |
| Balance inicial → final USD | 100000 → 90029.30 | 100000 → 65706.68 |
| Gross / costes / net USD | −8900 / 1070.70 / −9970.70 | −27650 / 6643.32 / −34293.32 |
| Max drawdown USD | 9970.70 | 35225.55 |
| SOURCE_CLOSE físicos / records / root inputs | 20700 / 136932 / 45656 | 38909 / 270781 / 85824 |
| Wall proceso run / reproduce | 2m36.06s / 2m40.04s | 6m47.02s / 7m41.56s |
| MaxRSS run / reproduce KiB | 301204 / 283248 | 539916 / 543384 |

Longitudinal RunID `bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f`. Resultado y reproducción tienen SHA256 idéntico `b11bd4e7776762523f29c9dda8e264c98818f5e209c7b051e72e6e671222a637`, 12668478 bytes. Produce ~95.60 barras físicas/s y ~665.28 records/s medidos sobre el proceso completo, sin race, namespace sin red. Son dos procesos frescos equivalentes, sin sumar cuentas reinicializadas. Último fill/posición flat aNov23T03:06Z; unrealized0 y cashflows0. Una Operation ACTIVE flat permanece declarada bajo REPORT_RESIDUALS: flat no sustituye el intent de terminación del dominio compartido; no se oculta ni se fuerza cierre.

Producción ejecutada `d69d03eceeac1495522473a95baf08087f5c28b3`, binary SHA256 `79bd5f2aab74c242dbece8ebd274975c94d37100d18af80103e3c44d62e69839`; tip publicado `77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626` sólo corrige un oráculo nuevo y VERIFICATION, Go producción idéntico a d69. S2 `S2_H4_TREND_BB_PULLBACK_V1` y GerardMM/Provider/Operation/accounting compartidos. Perfil `BTG_FUNCTIONAL_NQ_EVAL_V1`: SIM/GENERIC100K, EVALUATION fijo2000SL/1500TP USD por account-day explícito, fee2.49USD/contrato/lado y1tick slippage. NO_ADDS_FUNCTIONAL_BASELINE_V1, OHLC_1M_MODEL_V1 / SL_FIRST_NEXT_OPEN_V1; trayectoria intrabar modelada, no ticks/quotes observados ni LIVE_EQUIVALENT. No ajuste de S2/MM para mejorar pérdidas.

RunSpec físico SHA256 `c8fa6cbba91fda93b25528a0303392a06314269ef319924eda69ae13635357ef`; dataset lógico `sha256:dea223977939067746d5cd8e4c54e2f6bcf01dae80475e7eb55ec9d8ed5b5c84`; profile `sha256:a43787c9db8fee824fec4d3bf051de8623b549ddcd8192f6c1d70ec868f7f79f`; Calendar `sha256:b092415709ffc9cdd9990cf1194e3b7939d1f94197f488d635b7916d2913981f`; execution `sha256:bbf9f57480b6b974b3685d06460119825a8389da40048ad7e0041e1ce8b71520`. Manifest conserva config antes de resolución y artifact conserva config normalizada/resuelta: digests de objetos distintos, no comparados como si fueran el mismo objeto.

Corpus13files leído íntegramente: 57457558bytes/1096336rows, manifest SHA256 `226f37dd77e9daabc7fe7e985ae1ce11e72f3ecb7fbbd8c54e62fc329f509326`. Derivación exact byte subsequence: 226rows fuera del Calendar configurado excluidas, 1096110retenidas; originals intactos. NQ12-23 derivado SHA256 `85d88ed0b2df3ab6435546676ba49549cfce5cec75495552a28edd13860e7750`, sólo6exclusiones. Manifest exclusiones `318eb05eee54db7e4eed220f157e584eea3b81dc848330d2de745a54811a7d26`; verificación `a67aab5fc67d35b507fc1da0af504198d8cc4ed518babd32976eed6d87e29258`. Los24831 minutos ausentes son respecto al Calendar semanal sin overrides: causaUNKNOWN, no prueba de horario histórico oficial CME ni pérdida del proveedor. No se rellenaron gaps.

**Frontera pendiente:** la corrida continua solicitada de los13exports no está completada. FAIL_VISIBLE_GAPS_V1 detiene en missing-open; el primer gap2023Oct10 está físicamente probado y el longitudinal termina antes del siguienteNov23T03:29. Todos los13derivados tienen segmentos con warmup suficiente, pero esas ventanas no equivalen a una cuenta continua ni acreditan rollover. Primera divergencia fuera de sesión correcta fue sourceOct15[04:32,04:33)Chicago sábado23:32, no una vela viernes21:01; quedan supersedidas las atribuciones preliminares. Primary debe adjudicar cobertura/calendario/recuperación explícita de gaps para el horizonte integral; no se inventa ese contrato en S01.

BT2-F01–F11 revisados previamente conservan regresión específica y ahora tienen rerun integrado real, con alcance de ramas declarado en la matriz; BT2-F12–F14 corregidos con regresión y rerun real; [[BTG-S01-REAL-GAP-FORENSICS]] conserva RED/GREEN, fallos, tiempos y censo pre/post. PR producto [borrador4](https://github.com/xKoRx/echo/pull/4), apilado en fb210ac4/PR3; no merge/despliegue. D6 refrescado nuevamente d08a30ce, limpio, intersección SDK/Core vacía; shareddelta final sólo getter Ledger.FillCount readonly y test nuevo. Agents-OS master observado `2e6c75e8f425be43fedbfe76d280dd92f38b76ed`, sin delta de autoridades Echo/bootstrap/skill aplicables desdea2fb9254. Registros y artifacts ONE-SHOT importados por bytes, root conserva continuidad.

### Comando mínimo y evidencia final

Comandos existentes ejecutados offline; el helper prepara el RunSpec sellado y el reproduce verifica resultado/records según contrato. Los outputs pesados permanecen en workspace Aranea. Se puede elegir otro directorio de salida sin alterar la identidad de inputs.

```sh
btg_bin=/home/kor/aranea/work/btg-s01-20261006/reports/real-gap-forensics/echo-backtest-counters
btg_work=/home/kor/aranea/work/btg-s01-20261006/reports/real-history-execution
unshare --user --map-root-user --net "$btg_bin" prepare-functional-nt --input "$btg_work/input-longitudinal-nqz3-derived-candidate.json" --out "$btg_work/prepared-longitudinal-nqz3-derived-candidate"
unshare --user --map-root-user --net "$btg_bin" run --spec "$btg_work/prepared-longitudinal-nqz3-derived-candidate/runspec.json" --nt-source-config "$btg_work/source-derived.json" --out "$btg_work/longitudinal-nqz3-derived-candidate"
unshare --user --map-root-user --net "$btg_bin" reproduce --result "$btg_work/longitudinal-nqz3-derived-candidate/bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f/result.json.gz" --nt-source-config "$btg_work/source-derived.json" --out "$btg_work/reproduce-longitudinal-nqz3-derived-candidate"
```

Detalle machine-readable de runs/fallos/comandos/digests: `/home/kor/aranea/work/btg-s01-20261006/reports/historical-smoke/historical-smoke-evidence.json`, SHA256 `9d231434ece6bdfec0cedc20f36445f8f23c0b9f8c0299785ce0c5288a1a1445`, 14621bytes. [[BTG-S01-NQZ3-REAL-HISTORICAL-EXECUTION]] importado de worker d92a53ad; root normalizó area/links y primera causa de fallo, con hashes original/normalizado explícitos. [[BTG-S01 Final Operation Residual Classification]] importado exacto de worker53d8f35f, docSHA `9e65000026b29c26abe062b88300d7ab41d113cc76509f86bccecb43a2683923`; autoridad D2-04 I5/TERM-02 y records270594/270610/270612 demuestran residual legítimo sin termination intent. No se clasifica como nuevo defecto material.

Workers historical_smoke y final_operation_residual ONE-SHOT cerrados, registros attribuibles Codex/Luna y Codex/Sol importados. Feedback NORMAL NONE; feedback TOP sólo doctor global con errores ajenos al delta, sin modificar skills ni repetir global suites. Lint final14paths PASS0errors/0warnings tras normalización de enum/sección de un agent_run; proyecto conserva sus cinco errores preexistentes. Root no ejecuta session-close propio ni marca aceptación Owner. El intento de despachar un worker adicional de auditoría de prerequisitos fue rechazado por límite de threads del harness: no se afirma ejecución ni modelo adicional. Root efectuó la revisión de conservación de fixes y alcance de la matriz sin producto nuevo.

### Reanudación Owner — 2026-10-06

[[BTG-S01-OWNER-S2-BARS-AUTHORITY]] fija S2 actual (`S2_H4_TREND_BB_PULLBACK_V1`) + GerardMM actual, NQ Last 1m principal y SL-first si una vela toca SL y TP. B01 alias se resuelve por instrucción directa; el resto del informe anterior conserva su corte histórico. No se afirmó una corrida ni se completaron rows económicas por inferencia.

Dos especialistas fresh-context cerraron sus encargos: TOP forensics del seam OHLC/causal bars/ejecución y NORMAL inventario físico Windows de minute/tick y exports. [[BTG-S01-S2-1M-FORENSICS]] pasó diez tests existentes offline y delimitó un ingreso nativo de barras al SDK. [[BTG-S01-NQ-1M-DATASET]] confirma AccessDenied sobre Documents/db/minute, Downloads y Public; ningún byte recuperado. NORMAL implementó el ingreso compartido de barras y su agregación; driver y ejecución OHLC siguen pendientes. Preguntas de trayectoria MM intrabar y configuración se delimitan por evidencia.

Delta implementación: NORMAL cerró candidate `27cb4ceaf62151a042494022cad08e47672a06f2`, [[BTG-S01-SOURCE-BAR-SDK-IMPLEMENTATION]], documentos `612d24b37e2db5d004896a70170921de2c7b3084`. Paquetes bars/analytics/S2 y vet offline PASS; no aceptación. TOP independiente confirmó tres findings en [[BTG-S01-FINDINGS]]: bytes legacy Builder/OwnerState modificados, rechazo de modo después de mutar otro builder y gate de coverage no demostrado con exclusiones de ramas alcanzables. Remediación fresh NORMAL propia desde ese SHA; candidate previo preservado. La importación root normaliza párrafos y distingue instrucción del submanager de decisión Owner, sin alterar pruebas ni resultados.

### Delta verificado — prerequisito SDK, no histórico

Remediación producto congelada y publicada `407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef`, [[BTG-S01-SOURCE-BAR-SDK-REMEDIATION]]. Nuevo TOP LOCAL fresh-context concluye READY_SDK_PREREQUISITE_REVIEW_ONLY en [[BTG-S01-SOURCE-BAR-SDK-FINAL-REVIEW]]: once oráculos de bytes legacy iguales a baseline en proceso fresco; rechazo mixto atómico; restore OHLC tras eviction/discard mantiene modo y high-water; QUOTE válido compatible. Race suites explícitas bars/analytics/S2 y vet PASS dentro de namespace sin red. Source raw 129/135=95.56%; applySourceBar raw 38/41, applicable 38/38 con tres guards redundantes demostrados, sin excluir errores de input alcanzables.

[PR producto borrador #2](https://github.com/xKoRx/echo/pull/2) contra `feature/backtester-v1-s04-remediation`, head `407e03dd`, adjunto a este task. Sin merge/despliegue, S2/MM/accounting intactos. [[BTG-S01-FINDINGS]] conserva BT2-F01..F03 abiertos: fix/regression verificados, real_rerun NOT_RUN. El gate SDK no prueba señales, fills ni rentabilidad de mercado.

La investigación física concluye que la identidad autorizada `echo-dev` no puede leer la carpeta del usuario KoR. C:\Temp sí es legible y no presentó export histórico en su nivel superior. El Owner no necesita ubicar la caché: mínima acción física es `Tools → Historical Data → Export`, `Minute / Last` por contrato, hacia `C:\Temp\BTG-NQ-1m`. Ese destino sólo fue propuesto, no creado ni acreditado. GUI NinjaTrader no expuesta; no se amplió ACL ni se eludió un rechazo. Hasta recibir bytes se conserva BLOCKED_EXTERNAL para la corrida real, con contexto MM/account/provider aún pendiente.

### Nuevo export físico Owner — C:/Temp/history

El Owner confirmó archivos de velas en C:\Temp\history. Root y NORMAL comprobaron trece NQ Last.txt legibles por listado y muestras allowlisted de primera/última fila, [[BTG-S01-NT-CANDLES-ACQUISITION]], commit `9df2c94bf736b709dfca725da4368da0ba05c66c`. Extremos observados desde `20231001 220100` en NQ12-23 hasta `20261006 035000` en NQ12-26; no equivalen a validación continua de tres años. Formato de muestra headerless `YYYYMMDD HHMMSS;O;H;L;C;V`; primeras ocho filas de12-23 avanzan cada minuto. La convención UTC/end-of-bar está documentada por NT, pero no se auditó todo el export.

El bloqueo anterior de ubicación/caché dejó de ser la acción vigente. SFTP dev-win respondió POLICY_DENIED por clase safe en profile read-only; cat simple de muestras sí permite lectura, sin cambio de identidad ni privilegio. Originales completos locales, SHA256, conteos/duplicados/gaps exhaustivos siguen pendientes. Root comprobó ambos SHA256 documentales del worker y releyó la última fila12-23: close16053.5. Una transcripción temprana del handoff indicó16054; el artifact exacto y la instrucción al parser fueron contrastados/corregidos, sin cambiar el original.

Continúa trabajo independiente autorizado: NORMAL construye el DatasetSource NT minute y el contrato nativo en carril `codex/btg-s01-ntminute-ingress` desde407e03dd, con SDD y AllowedFiles por tarea. TOP delimita native driver/venue y MarketContext modelado, conservando S2/MM/provider/accounting. Parser fixture de una fila real no es corpus adquirido ni corrida histórica. Referencia/perfil real de cuenta/programa, costes y scaling se preguntaron al Owner mientras avanza el lector.

### Owner delega reglas consistentes para el baseline funcional

La respuesta Owner posterior a la pregunta de perfil autoriza elegir reglas consistentes ahora e iterarlas después. [[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]] fija el paquete funcional SIM/GENERIC100K, USD100000 inicial, MM2000/1500 uniformes por account-day, costes modelados explícitos y scaling omitido explícitamente. S2 y fórmulas GerardMM quedan compartidas/intactas; esta prueba no afirma scaling ni reglas de una prop. B02 deja de bloquear la selección de configuración funcional: no se sigue exigiendo config física recuperada para este baseline. Funded/campaña/S02 continúan fuera del mandato.

TOP cerró [[BTG-S01-OHLC-RUN-CONTRACT]], docs `549506b9`, artifact digest comprobado por root. Su bloqueo de perfil es el corte anterior, supersedido por autoridad nueva Owner. SOURCE→Mark y diferencias QUOTE/ACCOUNT_ECONOMICS están probadas en source; C debe usar MarketContext nativo modelado sin quotes inventadas. Root define SDD del driver sólo para la configuración NO_ADDS explícita, con rechazo de scaling no soportado, SL-first y fases/attribution declaradas; fresh TOP LOCAL recibe implementación cross-domain después del freeze B. No claim de run ni de SDK price trigger/scaling completo.

### Estado observado

STATE = REAL_BASELINE_COMPLETE_BOUNDED; FULL_13_CONTRACT_CONTINUITY_BLOCKED_DECISION
WORK_IN_PROGRESS = CONSOLIDATION_AND_PRIMARY_MANAGER_REVIEW; NO_HISTORICAL_PID_ACTIVE
FUNCTIONAL_CONFIG_AUTHORITY = OWNER_DELEGATED_CONSISTENT_RULES_2026_10_06
REAL_SMOKE = COMPLETE_RAW_5_DAYS_CORRECTED
LONGITUDINAL_RUN = COMPLETE_DERIVED_NQZ3_OCT29_NOV23
DETERMINISTIC_RERUN = BOTH_FRESH_IDENTICAL
ECONOMIC_STAGE_COVERAGE = EVALUATION_FUNCTIONAL_NO_ADDS_ONLY
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = 225 / 113 / 78 / MINUS_34293_32_USD

El inventario previo del Primary es preparación documental; no acredita datos físicos ni una corrida. S00–S04 son ACCEPTED_INPUT para capacidades; D6, Generic20/GAU50 y simuladores previos son REFERENCE_ONLY. Otros runs permanecen UNREVIEWED.

### Continuación ejecutiva — originales trasladados a Daedalus

Mandato Owner vigente: completar el programa de cinco shots el 6–7 de octubre de 2026, America/Santiago. S01 continúa con S2 compartida, GerardMM y `BTG_FUNCTIONAL_NQ_EVAL_V1`; `NO_ADDS` aceptado sólo para este baseline funcional. Los parámetros no se optimizan. El destino exacto comunicado es `daedalus:/home/hermes-ops/echo-dev/history/nq/`, con trece exports NQ Last 1m esperados. El bloqueo SFTP Windows queda como antecedente y deja de ser la causa vigente.

Comprobación local 2026-10-06 18:26 UTC: `hostname` devuelve `daedalus`; `id` identifica uid1000 `kor`, sin grupo `hermes-ops`. `ls -ld /home/hermes-ops/echo-dev/history/nq` devuelve Permission denied. `namei -l` localiza la primera denegación al atravesar `/home/hermes-ops`, modo `0750`, owner/grupo `hermes-ops`. `getfacl -p /home/hermes-ops` confirma `user::rwx`, `group::r-x`, `other::---`, sin entrada para `kor`. No se pudo verificar existencia, tamaños ni hashes de los trece archivos; su traslado es autoridad Owner, no lectura física acreditada.

El inventario vivo `aranea-ssh.list_connections` expone nueve perfiles, ninguno para Daedalus o `hermes-ops`. No se recurrió a sudo, contenedores, perfiles root de otros hosts, cambios de identidad ni ACL/policy. La prohibición expresa del mandato impide eludir esta denegación. Mínima acción solicitada: una copia intacta accesible a `kor` en `/home/kor/aranea/work/btg-s01-20261006/history/nq/`; no nueva exportación ni ZIP. Al recibirla se comprobarán todos los bytes y digests, sin atribuir una verificación del origen inaccesible.

Especialista fresh ONE-SHOT NORMAL LOCAL `gpt-6-luna`, `real_history_execution`, despachado desde el candidato integrado `fb210ac4afeab2315aaa3c424f287c2d9db5a7b3` para el run real y su reproducción. Confirmó independientemente la denegación y continúa build offline del CLI existente y preparación del comando concreto. Ningún PID de backtest histórico ha arrancado; REAL_SMOKE, LONGITUDINAL y RERUN siguen NOT_RUN. El submanager permanece abierto, S02–S05 no iniciados.

Refresh de continuidad: Agents-OS master `a2fb92548475f6865c972de70e31db466e7ca13e`; diff relevante desde `07ea7468` sólo journals ajenos, sin delta en autoridades Echo/skills. Echo master `372af59a`, S04 `cd451972`, D6 `d08a30ce`, candidato `fb210ac4`, sin avance. D6 checkout y candidato limpios. Sin merges ni intervención runtime.

### Resolución física Owner y arranque real — corte posterior

El Owner confirmó la copia solicitada. Root encontró trece archivos en `/home/kor/aranea/work/btg-s01-20261006/history/nq/nq/` (carpeta anidada conservada), comprobó sus tamaños y leyó todos los bytes con `sha256sum`, sin errores. Los trece tamaños coinciden con el inventario Windows previo. NQ12-23 SHA256 `caead986337256d77011d58cb49d4d4b20393b1261c0f1ef4c494cd0397c6c94`; NQ12-26 `2176dce88405aee7fe5383cf1244330ad83fe0b0f1105abe9c7b198a30555141`. La provenance es export NinjaTrader Owner + traslado/copia confirmado por Owner; los hashes físicos de la ruta home/hermes original siguen sin verificarse, y no se inventa esa comparación.

La denegación anterior queda histórica: ya no bloquea ejecutar sobre las copias legibles. Worker previo `real_history_execution` cerró ONE-SHOT antes de la confirmación con CLI build PASS y feedback NONE; [[BTG-S01 Real History Execution]] y su agent_run se importaron por contenido desde `2c58eeec`, sin merge. Root verificó README SHA256 `a78fb52a58303708aae6095aba1a99e72163897ca3bd8fa1352b8ef6a3692cb9` y binary `5a20ed5c34fa6bfb0e898aa1e39021bd2dcf1865a8fc93ef394964d538c2e945`, candidato limpio.

Fresh NORMAL LOCAL `gpt-6-luna`, `historical_smoke`, recibió mandato completo para usar ese binary y completar smoke auténtico, ampliar sólo el horizonte ante cero trades, corregir fallos ordinarios, medir rendimiento, longitudinal y fresh rerun. Manifiesto exhaustivo y primer RunID aún en preparación: no se afirma PID histórico ni PASS antes de su ejecución. No se reabre identidad, perfil, costes ni aprobación de horizonte. S01 permanece en curso dentro de la ventana Owner; S02–S05 no iniciados.

### Primer run auténtico — fallo visible de cobertura

`prepare-functional-nt` completó usando NQZ3/NQ12-23 real y perfil congelado. RunID `bt-862144ea58fd404b04cc65eb254516f4ec6d5edf811bcc12c28ecacb78f4d97c`; commit `fb210ac4`, binary `5a20ed5c`, inputs digest `sha256:862144ea58fd404b04cc65eb254516f4ec6d5edf811bcc12c28ecacb78f4d97c`. Ventana operada solicitada 2023-10-15T22:00Z → 2023-10-22T22:00Z, warmup previo desde primera disponibilidad del export; ejecución offline en namespace sin red, sin race. PID458702 terminó; ningún proceso activo se afirma en este corte.

Resultado sellado `execution_state=FAILED`, CLI exit0: `SOURCE_COVERAGE_INCOMPLETE` en 2023-10-10T00:16Z, antes de operar. Primer expected interval `[00:16,00:17)`; originales no contienen cierres00:17/00:18 y siguiente cierre00:19. Se preservan original, configuración y fallo; no se fabrica la cobertura. Source consumido8415 filas, root inputs18561, records52238; operaciones0/fills0, balance/equity100000USD, gross/cost/net0. Es un fallo técnico de corrida, no baseline rentable ni smoke funcional terminado.

Tiempo medido33.23s wall (67.59s user,3.17s system), maxRSS124980KiB; ~253.2 source filas/s hasta primera interrupción, ~1572.0 output records/s. El tiempo incluye la ejecución fallida y sellado; no extrapolar como rendimiento longitudinal certificado. Log/result en workspace externo `reports/real-history-execution/smoke-20231015.log` y `smoke-20231015/<RunID>/result.json.gz`; result SHA256 `07d5ab7b97c880beed18a22731d0e757e6048e2494f93d0efecbc7e25983ca72`, contrastado en salida CLI.

NORMAL continúa reproducir en proceso fresco y seleccionar tramo suficiente por cobertura/calidad, sin selección por PnL. Fresh TOP LOCAL `gpt-6.1-sol`, `real_gap_forensics`, inspecciona contrato/discontinuidades/ventanas de los13exports y cualquier divergencia material de reporte. No nueva ceremonia de diseño/adversarial: sólo diagnóstico de este recorrido real y ownership del fix si hay bug probado. Gaps no se interpolan ni se disfrazan como sesiones cerradas. Findings previos siguen pendientes de rerun exitoso; S02 no iniciado.

### Ejecución vigente y diagnóstico precisado — 18:47 UTC

Primer fracaso de gap reproducido en proceso fresco: IDENTICAL,44.23s; no acredita un smoke exitoso. Intentos posteriores encontraron una vela fuera del calendario semanal declarado (viernes2023-10-13 cierre21:01Z, intervaloChicago16:00–16:01). Guard correcto. El error aparecía retrofechado al warmup por diagnóstico del driver/summary; TOP verificó BT2-F12, root asignó fix sólo `driver.go`/`finish.go` y nueva regresión, sin alterar caller frontier, scheduler, timers ni datos/calendario. RED confirmado, patch mínimo y GREEN en curso en carril aislado `codex/btg-s01-real-diagnostics`; el candidatefb permanece intacto.

Inventory TOP encontró segmento limpio NQZ3 de warmup2023-10-15T22Z a2023-11-03T21Z,90H4 completos, readinessOct26T10Z. Selección por calidad/cobertura, nunca por PnL. Smoke actual: warmupOct15T22Z, tradeOct29T22Z → Nov3T21Z (cinco account-days); PID464239, wrapper464204. A18:47:03UTC seguía activo102s, CPU acumulado4m10s y RSS214992KiB. RunID aún no materializado; estado RUNNING, nunca PASS. Comando exacto en log externo `/home/kor/aranea/work/btg-s01-20261006/reports/real-history-execution/smoke-clean-long-20231029.log`: binaryecho-backtest `run --spec .../prepared-smoke-clean-long-20231029/runspec.json --nt-source-config .../source.json --out .../smoke-clean-long-20231029`, bajo namespace offline y time rusage.

TOP determina causa de omisiones intrasesión UNKNOWN (no-trade vs pérdida de datos no demostrado); no se rellena ni relaja policy `FAIL_VISIBLE_GAPS_V1`. Inventario inicial identifica tres contratos sin segmento suficiente para51H4 entre gaps/outside rows (03-25 max48H4,09-25 max49,12-25 max34), pendiente paquete preciso. Estos límites no se adjudican como bugs ni full13COMPLETE; no se suman cuentas reseteadas. Longitudinal/rerun exitosos pendientes del primer smoke funcional y remedioF12.

### Baseline real previo al fix de resumen y longitudinal vigente

Smoke `bt-0049ea259d5b853e3ef4504f6330790048e5401c966d98d8a191b9b5b1ad5fb0` terminó COMPLETE, warmupOct15T22Z / tradeOct29T22Z → Nov3T21Z. Fuente NQ12-23 original, codefb210ac4, misma S2/MM/perfil. Resultado6,588,615bytes, SHA256 `cdbab77738600019410a6d754a73b9992b168da3ee2b79d5e70a78df8fffc19f`. Records136932, root inputs45656; SOURCE_CLOSE20700 (rootordinal NO es conteo physicalbars).150.36s/maxRSS274940KiB:137.67physicalbars/s,910.7records/s,303.64rootinputs/s. Fresh reproduce IDENTICAL con mismoRunID/records,177.40s/maxRSS272868KiB. REPRODUCIBLE para ese escenario; no LIVE_EQUIVALENT.

Eventos compartidos reconciliados:60 señales (30OPEN/30CLOSE_ALL),30decisionesProviderALLOW,30operaciones materializadas/terminales (12con fills),24fills con24provider_execution_id únicos,430contract-sides;34órdenes observadas y10cancels confirmados. Coste430×2.49=1070.70USD. Cuenta inicial100000USD, balance/equity final90029.30USD, gross−8900USD, net−9970.70USD, unrealized0/exposición0; maxDD9970.70USD. Cinco account-day PnL netos−1999.30/−1979.78/−1994.26/−1998.40/−1998.96. Esta configuración perdió en este período; no se optimizó. No se infieren cuentas quemadas ni resultados de prop/funded.

Encontrados BT2-F13: resumen reporta fills0/operations0 pese a los eventos/census anteriores; BT2-F14: residual operation abierto pese a latest shared snapshot TERMINAL/MM_NO_ACTION, CurrentOperationID retenido intencionalmente. Account-day/stage residuals sí legítimos bajo REPORT_RESIDUALS. TOP prueba RED y corrige finish/getter SDK readonly FillCount sin mutar economía, scheduler ni política. D6 refrescado antes sharedgetter: d08a30ce/master372af59a, limpio, delta bridge-only/no SDK-Coreintersección. BT2-F12 ya tiene fix970f1d52 + regresión y dos failedrealreruns/freshreproIDENTICAL con reached-time/source-ref precisos; estado de cierre en [[BTG-S01-FINDINGS]].

Manifiesto corpus raw13files `reports/historical-smoke/corpus-manifest.json`, SHA256 `226f37dd77e9daabc7fe7e985ae1ce11e72f3ecb7fbbd8c54e62fc329f509326`:57457558bytes/1096336filas,0malformed/order/duplicates/tickmisaligned/OHLC/negativevolume. Inventory usa aliasesNQZ23 etc.; RunSpec NQZ3 identifica misma combinación year2023/month12/externalNTref y hash, sin equivalencia implícita de streamIDs.

Preparación derivada autorizada: exact byte subsequence de NT,226filas fuera de regiones del calendario compartido excluidas con ref/interval/rawlineSHA/reason;1096110retained. Sólo6exclusiones en NQ12-23 (68771retained). Originales inalterados; intrasesiongaps íntegros/failvisible. Scope explicitado en `reports/real-gap-forensics/derived-nt-weekly-v1` manifest. Tras excluir fuera-sesión los13contratos sí tienen segmentos≥51H4, por lo que conclusión RAW anterior de tres sinwarmup ya no aplica a DERIVED. Full13span sigue limitado por gaps auténticos/causaUNKNOWN, sin policy de recuperación inventada.

Longitudinal raw más amplio falló correctamente al encontrar otras filas fuera sesión; no se interpreta como éxito. Longitudinal DERIVED actual RunID `bt-ac706c414d88dfbb1d4057c56dee113a4bee92fdc4a22435cd9968b89756b5c5`, PID475832/time475797: warmupOct15T22Z, tradeOct29T22Z, finNov23T03:29Z (último observedclose pre-intragap). Reejecuta íntegro prefix desde cuenta100k en UN run, no suma smoke/resetaccounts. Al último check seguía activo109s/RSS~222MB, codefb pre-counterfix; finalpostfix/repro pendientes. Logs/spec/source derivados conservados en `reports/real-history-execution/longitudinal-nqz3-derived`. No PID futuro ni PASS se promete.

### Autoridad recuperada y aislamiento

El paquete solicitado procede de `xKoRx/agents-os`, commit de rama documental `a16f4bb25cfb6882146f437f5913302a191313c2`, segundo padre del merge existente `d67319f0878610c786b94aa2ad31e5e4503e7efa`. La rama remota ya no aparece en `ls-remote`; su contenido existe en el checkout vigente. Esta sesión no ejecutó ni exigió el merge, ni alteró master. Evidencia nueva en rama `codex/btg-s01-evidence`; especialistas con ramas documentales propias y ownership disjunto. Sin intervención D6 ni cambios de infraestructura.

HEADs refrescados directamente por `git ls-remote` al inicio (2026-10-06 UTC, fecha local 2026-10-05):

| Autoridad | HEAD observado | Estado local |
| --- | --- | --- |
| Agents-OS master | `bb9fa98be22057e8468e83f72cb53fd147accc09` | limpio |
| Echo master | `372af59a7b83604781346613da01e3d510ea1360` | referencia remota |
| Backtester certificado | `cd451972b242c8933321e03001decd4b6d778c61` | worktree certificado limpio |
| D6 | `d08a30ce9815f820fda7132e20dc42cc345eb8e8` | referencia remota; intocado |

### Delegaciones y revisión

- TOP LOCAL `gpt-6.1-sol`, ONE-SHOT: autoridad/configuración inspeccionada; [[BTG-S01-IDENTITY-CONFIG]] en commit `08b79f27bb0b951af3a305f49a3201dfce6823ca`. Root comprobó los 11 digests de fuentes y los tres digests de evidencia externa: cero mismatches. Cuatro tests existentes PASS offline; cierre/run/log completados, feedback NONE.
- NORMAL LOCAL `gpt-6-luna`, ONE-SHOT: [[BTG-S01-DATASET-INVENTORY]] cerrado en commit `9bc160a8b7466c5dd399711bc35e8fc9242b5d8f`. Revisión root corrigió la afirmación inicial sobre inexistencia de Downloads/Documents; el barrido corregido no halló candidatos. El nombre de capability MinIO RW no se trató como prohibición automática de sus métodos RO; metadata de 12 buckets inspeccionada sin mutaciones. Cierre/feedback completados; run-register skipped por lookup/documentación. Root reparó sólo el delimiter de cierre del frontmatter del feedback importado; su digest de contenido cambia, no sus observaciones.
- TOP LOCAL `gpt-6.1-sol`, ONE-SHOT: [[BTG-S01-NINJATRADER-ACQUISITION]] cerrado en commit `1adec4f09f9b12e91aab0a20d76589a76928f659`. Exportador oficial identificado; corpus NOT_ACQUIRED. Sin repetir probes denegadas ni alterar D6. Cierre/log completados; feedback NONE y run-register skipped por lookup/documentación.

El harness expone ambos modelos. No expone una ejecución CLOUD Pro autónoma; las delegaciones presentes requieren inspección física LOCAL. Consumo confirmado Chat Pro = 0 (Codex). Cada worker ejecutó su cierre ONE-SHOT y persistencia por delta; registro sólo donde hubo pruebas de código. Root no se autocierra.

### Fuente del histórico — steering Owner

El Owner confirmó durante el inventario: “la idea es sacar todo desde ninjatrader”. NinjaTrader pasa a ser la fuente seleccionada para adquisición, sin presumir que ya existe un export durable. El inventario continúa sólo por rutas de lectura/extracción autorizadas de esa fuente; no se solicita otro proveedor ni se captura el feed D6 para reemplazar el histórico. El permiso de lectura del archivo/carpeta o una exportación fuera del carril operativo siguen sin demostrarse.

### Bloqueos evidenciados

| ID / clase | Expected | Actual / evidencia | First divergence / owner / mínima acción |
| --- | --- | --- | --- |
| BTG-B01 / RESOLVED_BY_OWNER | Vínculo canónico entre el nombre Owner Gerard y Strategy/version | Owner 2026-10-06 seleccionó S2 actual, SpecID `S2_H4_TREND_BB_PULLBACK_V1`. La inspección previa sin alias conserva su corte histórico, pero ya no bloquea la selección. | Autoridad directa en [[BTG-S01-OWNER-S2-BARS-AUTHORITY]]; configuración restante evaluada como B02. |
| BTG-B02 / RESOLVED_FUNCTIONAL_SELECTION_BY_OWNER | Config MM real y contexto account/provider para el horizonte | D4 sí define EVALUATION account-days 1–2 SL USD 2.000 / TP USD 1.500. Rows posteriores y FUNDED encontradas sólo como fixtures/modeling; no configuración Owner vigente. | Preflight/config, ningún historical run. Owner delegó reglas funcionales consistentes; perfil explícito en BTG-S01-FUNCTIONAL-BASELINE-PROFILE. Original config física no recuperada y no se afirma, pero ya no bloquea este baseline. |
| BTG-B03 / RESOLVED_LOCAL_COPY_ACCESS | Corpus físico real con provenance, contratos, orden, timezone y digests | Owner trasladó originales a Daedalus y luego copió trece exports al workspace legible. Root leyó todos los bytes y hashes de las copias; tamaños coinciden con inventario previo. La ruta home/hermes original conserva su denegación y sus hashes no se atribuyen a lectura directa. | Acceso resuelto por acción física Owner; continuar descriptor/manifiesto y run real con las copias. No se hizo workaround de privilegios ni intervención runtime. |

BT2-F01..F03 materiales registrados en [[BTG-S01-FINDINGS]], hallados en el prerequisito SDK con probes REFERENCE_ONLY y ningún cierre. Ninguna corrida histórica real ocurrió: real_rerun NOT_RUN para todos. Los bloqueos B02/B03 son de configuración/datos; no se maquillan como defectos corregidos ni como ausencia global.

### Evidencia independiente obtenida

El worker TOP observó Core DEV binario source `372af59a`, `vcs.modified=false`; ese commit no contiene `v3/sdk/futures`, `futuresruntime` ni `futuresvertical`. El symlink de release no prueba el source del proceso vivo. No se desplegó otro Core: el mandato es offline y esa instalación no acredita Gerard Futures vigente.

Cuatro tests existentes GerardMM pasaron bajo namespace sin red externa: day1/2, day3 sin resolver, FUNDED ausente/configurado y scaling explícito. Sirven como evidencia de fail-closed y capacidades compartidas; REAL_SMOKE sigue NOT_RUN. Config instalada y fixtures permanecen separados. Logs completos y comandos en [[BTG-S01-IDENTITY-CONFIG]].

En el inventario inicial originales y producto no fueron modificados; no hubo suite amplia, seeds, trading, runtime restart ni configuración de infraestructura. La reanudación tiene un carril producto propio desde S04, `codex/btg-s01-source-bars`, para el prerequisito SDK definido en `specs/btg-s01-source-bars/`; su candidate anterior fue rechazado y la remediación `407e03dd` pasó revisión SDK independiente, sin corrida real. El aislamiento `unshare --user --map-root-user --net` funciona. Toolchain observado Go 1.27.1 linux/amd64; no claim de determinismo entre builds.

### No interferencia D6

D6 refrescado desde remoto y worktree limpio: `d08a30ce`. Base común con S04 `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6`; commits exclusivos D6 desde esa base afectan sólo `v3/futures-bridge/` (adapter, AddOn y harnesses). Ningún delta exclusivo D6 en SDK/Core. Antes de autorizar el prerequisito shared SDK se refrescaron nuevamente Echo master, S04 y D6 sin cambios; carril producto aislado desde S04, sin intervención D6. El tree Git no acredita por sí solo el estado físico del runtime.

### Adquisición NinjaTrader verificada como mecanismo, no como corpus

El especialista TOP confirmó un mecanismo GUI oficial `Tools → Historical Data → Export` para generar TXT UTC por contrato/intervalo/data type desde datos disponibles. Falta validar cobertura del caché y original exportado. El harness no expone GUI nativa NinjaTrader; SSH autorizado no lee la carpeta fuente. La mera existencia del exportador no satisface adquisición ni fidelidad. Detalle oficial, formato, límites y acción mínima en [[BTG-S01-NINJATRADER-ACQUISITION]].

Acción física propuesta en el corte anterior, supersedida por exports existentes `C:\Temp\history` y transferencia pendiente: exportar desde la GUI la caché existente `Minute / Last` por contratos físicos a una carpeta legible por el acceso autorizado, conservando TXT y registro de opciones sin editar. Export `Tick / Last` sólo para los contratos/rangos disponibles, como validación posterior. El submanager comprobará cobertura y provenance antes de convertir. No descargar, reconectar ni cambiar Merge Policy en la instancia D6 activa. Si la caché no alcanza, adquisición posterior requiere un contexto NinjaTrader independiente autorizado y entitlement real; no se afirmó que exista.

Stage comprobado por root mediante lecturas RO `ls C:/` y `ls C:/Temp`, perfil `dev-win`: C:\Temp legible, sin export histórico en su nivel superior. Destino propuesto al Owner `C:\Temp\BTG-NQ-1m`; no se creó carpeta ni se leyó contenido de bundles/configs D6. Permite exportar sin descubrir la ubicación interna de caché.

BBO es un gap técnico condicionado al corpus: el NDJSON actual asigna a ambos lados un único timestamp/ref; combinar exports Bid/Ask independientes como QUOTE simultánea alteraría age lateral. La representación derivada debe conservar timestamps/refs por lado detrás del DatasetSource existente. Se registró compatibilidad pendiente, sin implementar adapter ni cerrar un finding de run no ejecutado. TRADE_MODEL también necesita costos/offsets explícitos; no se seleccionó por inferencia.

### Lector NT nativo — candidato congelado

Worker NORMAL LOCAL `gpt-6-luna` publicó código `933b40d65d7fe0946bb5b75038f6c4858d9912ea`, rama `codex/btg-s01-ntminute-ingress`; tip `54698cb0bbd870c942e3ccc010f1a12127684c01` añade sólo VERIFICATION y SPEC/PLAN/TASKS. DatasetSource streaming procesa TXT NT con schema UTC/end-of-bar, ticks exactos, OHLC/volume/order, manifests lógicos, receipts físicos y discontinuidades crudas; no rellena gaps. La unión SourceBar/legacy y políticas de modelo forman identidad explícita. Suite offline dirigida del worker pasó, adapter244/256 sentencias95.3%, oracle legacy exacto. Revisión TOP LOCAL independiente demostró BT2-F04/F05: cursor podía exponer bytes mutados antes del check EOF y múltiples aliases del mismo archivo físico se vinculaban a streams distintos. Remediación NORMAL fresca en carril separado activa, regresiones/snapshot verificado antes de exposición; candidato no aceptado. Matriz restante identity/model/union/legacy dirigida pasa, sin gate histórico ni económico satisfecho por estos tests. Artefacto [[BTG-S01-NTMINUTE-INGRESS-IMPLEMENTATION]] importado desde Agents-OS `3e391ea06440886a93fd84457b36bc0f1665b644` y digest comprobado; run/feedback/session ONE-SHOT también conservados. Worker cerró su sesión, root permanece abierto. Pro Chat pool0.

### Revisión del lector y remediación causal en progreso

TOP fresh-context publicó revisión `f416c952cc7824e947fb8fe8ffb02e35f701bc91`, [[BTG-S01-NTMINUTE-INGRESS-REVIEW]], importada byte-exacta y SHA25619b6f598e93c6a14946e1105be366f37cdaf043c262b9423fcdb2e1f7346ab5b comprobado. NO_ACCEPT por BT2-F04/F05. Lo restante pasa matriz independiente parsing/union/model/digests y baseline407 legacy byte-idéntico oracleSHA25617d598692c372efbc30099369e9191bcc28d878e7a41013f6ff1ca6d6856e23f; nueva lógica302/31197.106% sin exclusiones. Nota de evidencia: regex del implementer citaba TestS03_Astra_TimeBoundsParticipateInIdentity sin buildtag s03review; no fue ejecutado ni se cuenta como PASS. Oráculos independientes sí ejercieron identidad directamente.

Fix NORMAL fresco `e44b741e0a6c32d39326b46738dc70565db4759c` captura snapshots privados verificados antes de entregar filas y preflight SameFile de bindings. El test recién añadido por B esperaba el timing defectuoso EOF; Coordinator aprobó TEST_CHANGE_REQUEST bajo reglas09§3/10§2, cambiando sólo ese bloque a rechazo en Open y conservando cada aserción de selección/closed-state. La suite completa/race/vet pasa después del cambio; sourceSHA publicado/limpio e integrado byte-exacto por C. Revisión independiente final [[BTG-S01-NTMINUTE-FINAL-REVIEW]], commit documental07143d56, confirmó mismos probes red933→PASSfix; originalraw286/29895.973% y final290/29897.315% sin exclusiones, PASS_BOUNDED_LOCAL. F04/F05 FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED con realrerun pendiente. El claim cambiado56/56 excluía handlers OS no demostrados inalcanzables; no se adjudica. El artifact del implementer declara changed56/63≈88.9% y la revisión delimita sus propios rangos. Fallos de permisos OS pueden impedir unlink; se devuelve error y se cierra el handle, sin afirmar cleanup universal frente a denegación filesystem. No se excluyó el test ni se cambió un oracle S04.

Primer test integrado C usa corpus sintético y ejercita S2→GerardMM→Operation→Provider→venue/economics; SL primero, TP en siguienteOpen y High futuro no altera prefix previo a availability. REFERENCE_ONLY; no es smoke histórico. Test de closed input sequence fija consumo sólo SourceClose, distinguiendo reserva interna en Open. Native CLI se diseña como port delgado para preparar configuración explícita, ejecutar y reproducir artifacts, pendiente del freeze C.

### Primer bottleneck demostrado — BT2-F06

Prueba C completa native1m/51-H4 bajo race agota600s; stack runnable en nextTimer, sin deadlock/assertionfailure. El driver conserva timers fired/replaced y cada1m los recorre/reemplaza; crecimiento histórico produce coste cuadrático. Root registró BT2-F06 y autorizó en SDD C compaction estable native-only de Fired al inicio de nextRoot, antes de seleccionar cualquier índice. Timers live, generations, requests/history records, expiries y legacy paths se preservan. Se exige igualdad de trace/result pequeño antes/después, almacenamiento acotado por live timers y medición sobre el mismo fixture/flags, seguido de E2E/race/regresiones. No proyección de throughput sintético como rendimiento de corpus real. Compaction implementada; comparación nonrace del mismo fixture40.48s→42.46s, sin claim de speedup; records699dc77... y Resultf74d35... exactos antes/después según worker. CPUprofileafter42.45s/87.05CPU-s: GC47.4%, Builder.findSource8.95%, completeNativeBar4.82%; nextTimer deja de ser hotspot. F06 atribución de coste dominante no confirmada; storage/scans se acotan, sin tuning especulativo de SDK/caches. Freeze/revisión de C pendientes en este corte.

### Driver OHLC congelado — gate local pendiente

Producto C `e2e15a3559034a3ed08c04f247baf4919e20b2ff` publicado/limpio, sin nuevos writes del implementer. Suite ordinaria domain/future-extrema/legacy Driver PASS258.765s; los cuatro casos S2/GerardMM long/short SL/TP PASS171.45s, datos sintéticos REFERENCE_ONLY. Race dirigido de causalidad/horizonte/control PASS31.642s, H4/selección timers PASS1.110s; cobertura final y race domain completo siguen pendientes en el corte de freeze. F06 regresión almacenamiento/identidad y F07 late controls/horizonte están implementer-verified, pendientes revisión independiente y realrerun. Un oracle nuevo short-stop se corrigió contra cálculo MM independiente: qty30, remainingSL1475.3USD, distancia2.25, stop104.25, fill104.50; MM no cambió.

Fresh TOP LOCAL revisa SHA congelado en worktree aislado; NORMAL LOCAL implementa CLI source/preparación/reproducción en `codex/btg-s01-native-cli` desde ese mismo SHA. Calentamiento, fills, cierres y contabilidad locales aún no acreditan el corpus real. Histórico sigue NOT_RUN y el submanager no adjudica aceptación.

Revisión independiente C detectó BT2-F08: reset17h Chicago y WarmupStart15:59 crean un día inicial con la fecha civil del warmup y vuelven a abrir igual ID al reset17h, ACCOUNT_DAY_FAILED. Reproducción pequeña respeta el break16–17, sin gaps inventados. Defecto heredado expuesto por el perfil real de reloj, material para backtesting; requiere fresh corrective worker y misma reproducción. No se cambia el warmup caller ni el reset para ocultarlo; C candidate aún no pasa gate local.

Worker C cerró con sourcee2e15a35 intocado/docsd9a4c571; importación root4notes SHA artifact3c62e1c2 y strictPASS. Extendedrace se interrumpió trasfindingmaterialF08 a624.35s/exit143, stopsubcase completado y TP iniciado; no wholePASS, perfil parcial fuera del union. TOPreviewer cerró docs83a71f1a: artifact762d48e3 importado byte-exacto junto a run/log, strictPASS3. Coverage525/55295.1087% adjudicado independientemente con10 invariantes de composición, bruto525/56293.4164%; F06/F07 fix/regressionindependentlyverified, realrerunNOTRUN. Fresh NORMAL remedia F08 inicialización en carril propio; CLI integra ese fix futuro sólo byteexacto desdeSHA congelado bajo deltaSDD, luego freshTOP LOCAL revisa integración. No nuevas writes en candidatos C/B congelados.

### Gate integrado local — F08 verificado, F09/F10 en corrección

F08 fix171fc712 y su integración byteexacta en CLI198f29f4 pasaron TOP independiente: mismo break Chicago17h nativo/legacy, calendarios23/25h DST, EndExclusive y oráculos legacy byteiguales; coverage10/10 bruto. [[BTG-S01-ACCOUNT-DAY-REMEDIATION]] importado byteexacto desde docs280f8993, strictPASS3. F08 queda OPEN_REAL_RERUN_REQUIRED.

CLI worker cerró source198f29f44bc6e58dd445c9a9b5ee1adfdade2ae9 / docs-onlytip6ef303f57739f0b2a44288f387b377d145eeceac, [[BTG-S01-NATIVE-CLI-IMPLEMENTATION]] docs25c89818. TOP independiente pasó fresh-process S2/GerardMM long SL-first en129.517s aislados:30 contratos, entry102.5/protective exit99.5, gross-1800/cost149.4/net-1949.4, COMPLETE y sealed reproduce IDENTICAL sin spec hermano. Son inputs sintéticos REFERENCE_ONLY, no métricas del histórico. Coverage CLI186/19296.875% bruto y CLI+F08196/20297.0297%, sin exclusiones.

Revisión material mantiene gate local REMEDIATION_REQUIRED: F09 cursor nativo permanece abierto ante SpoolDir error público run/reproduce; snapshots ya desvinculados, sin claim de archivo persistente nombrado. F10 Scope debe declarar preparación no adjudica autenticidad, FidelityOHLC correcto. Root despachó fresh NORMAL desde6ef303, AllowedFiles sólo cleanup CLI y Scope + nueva regresión; candidato previo intacto. Constructor leak no demostrado y marshal-error guard alcanzable/correcto, sin refactor NewRun/ResultWriter ni shared SDK. [[BTG-S01-NATIVE-INTEGRATED-FINAL-REVIEW]] cerrado en docs3b7b6eb6 e importado byteexacto; Root verificó SHA del artifactf6d0fcc1 y capsule+6 hashes, strictPASS3. Capsule/logs en reports/native-integrated-final-review. Correctivo congeladoe63254875b84b9ebe91b26ca138bb5c19843113a, source limpio/publicado; productor prueba RED→PASS público,42/42 cambios cubiertos sin exclusiones, race/vet/F08 dirigidos PASS. E2E completo GOGCoff agotó10min en failureRepro, NO_PASS; una repetición GC normal en curso, sin speedclaim ni refactor. Fresh TOP independiente e632 ya revisa ownership/Scope/compatibilidad con gates cortos para evitar pipeline grande duplicado antes de PR nativo; [[BTG-S01-FINDINGS]] registra expected/actual/owner/evidencia.

### Ownership final — F09/F10 verificados; F11 LOW acotado

TOP fresh terminó [[BTG-S01-NATIVE-CLI-FINAL-REMEDIATION-REVIEW]], docsab67f7c9/sourcee632 limpio: F09/F10 PASS,42/42 bruto/aplicable sin exclusiones, race/vet/build/F08 y freshfailure/repro+legacy byteigual. Nuevo BT2-F11 LOW alcanza Close2 al EOF seguido por error de re-admisión; native Close idempotente, sin fuga/diferencia económica observada, exact-oncegate aún exige corrección. Root conservóe632 y despachó freshNORMAL run.go wrapper only +regresión en codex/btg-s01-cli-cursor-once, sin APIs nuevas/shared. Reviewer exactmodelruntime/tokenreceipt no expuesto: solicitado gpt-6.1-sol/high vía harness, registro distingue configuración y runtimeunknown; Codex fuera poolChatPro.

Producer e632 largeE2E: GOGCoff TIMEOUT10m, defaultGC100 ~8m24 pasa complete/repro/failure/repro/identity pero falla después compilando baselinelegacy por GOWORK custom que no incluye módulo extraído. No wholePASS ni atribución causal de performance. No más heavyretries: prueba legacy independiente e632 ya PASS; fricción real harness se persiste por worker. Source/datos/domain no se alteran por este problema de toolchain. Gate final requiere freshTOP del wrapper F11; histórico sigue NOT_RUN.

### Gate local nativo final — evidencia acotada independiente

F11 source15422c2329164a33a76bf63912491168227660b7 pasó freshTOP: mismo EOF/publicsealedscript override Close2→1 con Peek3/Next1 intactos y error original preservado. Race8.070s/F081.171s/vet/build, cachedfirstCloseerror concurrent128/sequential y F09publicFDsinresidual PASS. Changedproductionblocks3/3 bruto/aplicable, exclusiones0. ShortfreshfailureSOURCE_COVERAGE_INCOMPLETE/reproIDENTICAL y legacy e632→15422 byteiguales d5325ae6cf99725a9e7e23dab1951b1e8fb60468f29a41179a636f5b504c5ad7. READY_LOCAL_NATIVE_BASELINE_REVIEW_ONLY; no claim de fullheavyE2E ni histórico. PriorsharedS2/GerardMMcomplete/repro129.517s pertenece a198f y inputs sintéticos; producer e632largeE2Epartial FAILED_HARNESS permanece explícito.

F09/F10 productor cerró sourcee632/docstip a8e85129 y vaultdocs5e629319, [[BTG-S01-NATIVE-CLI-FINAL-REMEDIATION]]. F11 productor source15422/docstipe320fef9 y docs4d5612b9, [[BTG-S01-CLI-CURSOR-ONCE-REMEDIATION]]. Root importó notas byteexactas; dos artifacts producer carecían de frontmatter. Root añadió envoltura canónica con metadata/Propósito/Contenido/Fuentes conservando íntegro el informe original: originalSHA cabd2386/ee5a7a56, normalizedSHA659795f6/139e5576; strict5notesPASS tras normalización. Sin alterar pruebas/source/conclusiones. F09verification integrada sólo documento exacto SHA91a9c52d95d6c0565fa44b98a9f13c51e9d8eba28e128a498c68ccf642ca1b8b; Go source inmutable. FinalTOP cerró docs cffcf2a2cc0ecbff15cc05dee3795455bc40c157, [[BTG-S01-CLI-CURSOR-ONCE-FINAL-REVIEW]] SHA86bfe8eabf347fdbec37848e22046712a62e0d90f2798a41dfb85034e962edc9. Tip verificadofb210ac4afeab2315aaa3c424f287c2d9db5a7b3 en codex/btg-s01-cli-cursor-once-reviewed añade sólo SDD VERIFICATION; Go bytes iguales15422, limpio/publicado. [PR nativo borrador3](https://github.com/xKoRx/echo/pull/3) contra prerequisitoSDK407 ([PR2](https://github.com/xKoRx/echo/pull/2)), adjunto; no merge/despliegue ni aceptaciónOwner/S02.

Refs refrescadas nuevamente antes del gatefinal: AgentsOSmaster07ea74689eeb56988653cce61cc836be32c0effe, Echo master372af59a7b83604781346613da01e3d510ea1360, S04cd451972b242c8933321e03001decd4b6d778c61, D6d08a30ce9815f820fda7132e20dc42cc345eb8e8; D6limpio. Source15422 no modificaSDK/Core/bridge contra407; sin intervención física. BT2-F01..F11 tienen fixes/regresión verificados en alcances respectivos y TODOS realrerunNOT_RUN; cero remediaciones locales pendientes.

### Continuidad y próximo paso

Identidad/configuración funcional resueltas; candidato integrado y CLI compilado. Owner entregó copia local accesible y sus trece archivos fueron leídos/hasheados íntegramente; las denegaciones originales pertenecen al corte anterior. El submanager continúa provenance/digests y manifest físico, slice real con warmup51H4/20x5m y varios account-days, primerdivergence→fix→regression→mismodata, longitudinal y freshdeterministicrerun. Roll/holiday/gaps se fijan por evidencia del corpus, sin interpolar ni tratar jumpcontrato comoPnL. S01 no aceptado ni cerrado, S02 no iniciado.

REUSABLE_BEHAVIOR_CANDIDATES = NONE adjudicado por root en esta fase; candidatos/fricción propios de workers quedan en sus artefactos, sin editar skills generales.

### Comandos mínimos reproducibles

[[BTG-S01-NATIVE-CLI-FINAL-REMEDIATION]] y SDD VERIFICATION contienen build offline y templates prepare-functional-nt→run --spec --nt-source-config→reproduce --result --nt-source-config. Build/contrato/descriptor/horizonte son inputs explícitos que se adjudican sobre originales; no defaults de expiry ni comandos o RunIDs históricos inventados. Ejecución offline aislada, sin flags publish.

### Persistencia y verificación documental

Evidencia consolidada en `xKoRx/agents-os`, rama `codex/btg-s01-evidence`, base `bb9fa98`. Importación por contenido de archivos seleccionados; sin merges, rebases ni cherry-picks preventivos. Root comprobó digests de entrada y fuentes del worker TOP. Guards S04 conservados; ninguna modificación a sync o policy/skills generales.

Refresh antes del handoff: Echo master `372af59a`, S04 `cd451972`, D6 `d08a30ce`, source/D6 trees limpios. Agents-OS master avanzó a `a326c237d6a2fdfd6fc9367da927da40328df33b`; diff desde base no afecta Echo Futures ni Agents-OS/skills relevantes. No se integró ese delta ajeno. Documentación nueva y plan con lint dirigido sin findings; nota de proyecto mantiene cinco errores de lint preexistentes (dos tags y tres secciones), idénticos al baseline, sin ampliación.

Refresh final: Agents-OS master `07ea74689eeb56988653cce61cc836be32c0effe`, Echo master `372af59a`, S04 `cd451972`, D6 `d08a30ce`; producto frozen `407e03dd` y D6 locales limpios. SDK/D6 sin intersección material; sin cambios runtime/bridge.

Refresh directo previo al gate integrado final2026-10-06: Agents-OS master07ea74689eeb56988653cce61cc836be32c0effe, Echo master372af59a7b83604781346613da01e3d510ea1360, S04cd451972b242c8933321e03001decd4b6d778c61, D6d08a30ce9815f820fda7132e20dc42cc345eb8e8, sin avance respecto al corte previo. D6 checkout limpio; delta desde commonbase7fbd7e99 sólo v3/futures-bridge, sin intersección material SDK/Core con este carril. F09/F10 permitido sólo cmd/backtester, sin nuevos cambios shared.

Root verificó19digests externos del último revisor, capsule/manifest y SDDdoc exactos; normalización documental indicada conserva cuerpos fuente. Final notes/registros y plan se lintan por paths explícitos; reporte pesado y binaries permanecen fuera del vault.

ROOT_AGENT_RUN = SKIPPED: coordinación, revisión de evidencia y documentación; los segmentos de implementación/tests están atribuidos en los registros ONE-SHOT respectivos. ROOT_SESSION_CLOSE = NOT_REQUESTED.

### Handoff compacto

```text
SUBTASK = BTG-S01
STATE = BLOCKED_DECISION; REAL_BOUNDED_BASELINE_READY_FOR_PRIMARY_MANAGER_REVIEW
BASELINE_SHA = d69d03eceeac1495522473a95baf08087f5c28b3; published_tip77e188bc_test_docs_only
DATASET = 13_OWNER_NT_EXPORTS_FULLY_HASHED; COMPLETED_RUN_NQZ3_DERIVED_ONLY; corpus226f37dd; derived85d88ed0
GERARD_STRATEGY_AUTHORITY = OWNER_2026_10_06_S2_H4_TREND_BB_PULLBACK_V1_SHARED_DEFAULTS
GERARD_MM_AUTHORITY = D4-B2_SHARED_GERARDMM; OWNER_FUNCTIONAL_PROFILE_BTG_FUNCTIONAL_NQ_EVAL_V1
REAL_SMOKE = COMPLETE_RAW_OCT29_NOV3; 30_operations_24_fills
LONGITUDINAL_RUN = COMPLETE_DERIVED_OCT29_NOV23; bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f
DETERMINISTIC_RERUN = IDENTICAL_FRESH_PROCESS; result_SHA_b11bd4e7776762523f29c9dda8e264c98818f5e209c7b051e72e6e671222a637
ECONOMIC_STAGE_COVERAGE = EVALUATION_NO_ADDS_FUNCTIONAL_ONLY; NO_FUNDED_CAMPAIGN
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = 225 / 113_materialized_39_filled / 78_unique / -34293.32_USD
OPEN_MATERIAL_FINDINGS = NONE_CONFIRMED_OPEN_F01_TO_F14; FULL13_GAPS_AND_REAL_ROLLOVER_ARE_UNRESOLVED_COVERAGE_CONTRACT
ARTIFACT = BTG-S01-REAL-GERARD-RESULT; BTG-S01-FINDINGS; BTG-S01-REAL-GAP-FORENSICS; worker historical execution report; external sealed runs/manifests
PRODUCT_PR = https://github.com/xKoRx/echo/pull/4; DRAFT_STACKED_ON_PR3; NO_MERGE
AGENTS_OS_COMMIT = consolidated commit supplied in PR/chat; no self-referential SHA fabricated
GAPS_FOR_S02 = explicit historical Calendar/gap recovery and real rollover coverage; adds/scaling; funded/prop costs; economic units; 4 withdrawals/reinvestment/bankroll
NEXT_PRIMARY_MANAGER_ACTION = review completed bounded baseline and adjudicate full13coverage contract before S02; no sixth shot; window Oct6_7_America_Santiago
OWNER_ACCEPTANCE = NOT_ADJUDICATED
SUBMANAGER_SESSION = OPEN
PRO_CHAT_POOL_DELTA = 0
```

### Gaps para S02

Pendientes de inventario, sin inferencias económicas nuevas: unidad de `5k / 120k`; programa/prop/fees/settlement; stage config vigente; cuatro retiros netos cobrados y reinversión; preservar una cuenta operando a la vez salvo fuente posterior. S02 no iniciado.

## Fuentes

- [[BTG-PLAN]] y [[BTG-S01-SUBMANAGER-PROMPT]], commit de origen identificado arriba.
- [[Echo Futures]], autoridades master vigentes.
- [[Echo Futures — BT-S01 Backtester V1 Design]], enmiendas frozen.
- [[Echo Futures — BT-S04 Final Remediation and Certification]].
- [[Echo + Echo Forge — Environment Contract]], bootstrap y technical-project-manager.
