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

STATE = BLOCKED_EXTERNAL — ORIGINAL_BYTES_TRANSFER_POLICY
WORK_IN_PROGRESS = CLI_F11_EXACT_ONCE_FRESH_REMEDIATION; F08_F09_F10_INDEPENDENTLY_VERIFIED
FUNCTIONAL_CONFIG_AUTHORITY = OWNER_DELEGATED_CONSISTENT_RULES_2026_10_06
SDK_STATE = READY_SDK_PREREQUISITE_REVIEW_ONLY
SECONDARY_STATE = ORIGINAL_TRANSFER_PENDING; FUNCTIONAL_CONFIG_SELECTED; LOCAL_CLI_FINAL_REMEDIATION
REAL_SMOKE = NOT_RUN
LONGITUDINAL_RUN = NOT_RUN
DETERMINISTIC_RERUN = NOT_RUN
ECONOMIC_STAGE_COVERAGE = NOT_DEMONSTRATED
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = NOT_MEASURED

El inventario previo del Primary es preparación documental; no acredita datos físicos ni una corrida. S00–S04 son ACCEPTED_INPUT para capacidades; D6, Generic20/GAU50 y simuladores previos son REFERENCE_ONLY. Otros runs permanecen UNREVIEWED.

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
| BTG-B03 / BLOCKED_EXTERNAL | Corpus físico real con provenance, contratos, orden, timezone y digests | Workspaces históricos seleccionados contienen Polymarket/MLB. Evidencia de feed vivo no acredita corpus multiday. Candidato NinjaTrader no listado: permiso OS denegado bajo perfil RO; ruta/stock quedan no resueltos, no declarados inexistentes. | Antes de DatasetSource; transferir originales ya exportados C:\Temp\history por mecanismo autorizado byte-exact; listado/muestras13files legibles, SFTP policy denegada. No comprar ni tocar el feed/runtime. |

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

### Continuidad y próximo paso

Identidad resuelta por Owner 2026-10-06: S2 actual. Owner ubicó trece exports candles en `C:\Temp\history`; nombres/tamaños/endpoints son legibles, pero la transferencia completa SFTP está denegada por policy viewer. Se pidió ZIP preservando originales, sin ampliar ACL/perfil ni usar una ruta alternativa para sortear la denegación. Owner delegó selección de reglas consistentes para hacer funcionar backtesting; [[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]] fija el baseline funcional sin atribuir reglas a una cuenta física. El lector fix `e44b741e` pasó revisión independiente y está integrado byte-exacto. Driver/venue nativo e2e15a35 y F08 fix171fc712 pasaron revisión independiente acotada; CLI198f29f4 está congelado y su revisión [[BTG-S01-NATIVE-INTEGRATED-FINAL-REVIEW]] requiere F09/F10. Fresh NORMAL corrige desde docs-tip6ef303 en carril propio; nuevo TOP verificará el candidato, sin merges ni cambios shared nuevos. Al disponer de bytes completos y port verificado, este submanager continúa slice real, remediación y longitudinal dentro de S01. S01 no está aceptado ni cerrado; S02 no inició.

REUSABLE_BEHAVIOR_CANDIDATES = NONE adjudicado por root en esta fase; candidatos/fricción propios de workers quedan en sus artefactos, sin editar skills generales.

### Persistencia y verificación documental

Evidencia consolidada en `xKoRx/agents-os`, rama `codex/btg-s01-evidence`, base `bb9fa98`. Importación por contenido de archivos seleccionados; sin merges, rebases ni cherry-picks preventivos. Root comprobó digests de entrada y fuentes del worker TOP. Guards S04 conservados; ninguna modificación a sync o policy/skills generales.

Refresh antes del handoff: Echo master `372af59a`, S04 `cd451972`, D6 `d08a30ce`, source/D6 trees limpios. Agents-OS master avanzó a `a326c237d6a2fdfd6fc9367da927da40328df33b`; diff desde base no afecta Echo Futures ni Agents-OS/skills relevantes. No se integró ese delta ajeno. Documentación nueva y plan con lint dirigido sin findings; nota de proyecto mantiene cinco errores de lint preexistentes (dos tags y tres secciones), idénticos al baseline, sin ampliación.

Refresh final: Agents-OS master `07ea74689eeb56988653cce61cc836be32c0effe`, Echo master `372af59a`, S04 `cd451972`, D6 `d08a30ce`; producto frozen `407e03dd` y D6 locales limpios. SDK/D6 sin intersección material; sin cambios runtime/bridge.

Refresh directo previo al gate integrado final2026-10-06: Agents-OS master07ea74689eeb56988653cce61cc836be32c0effe, Echo master372af59a7b83604781346613da01e3d510ea1360, S04cd451972b242c8933321e03001decd4b6d778c61, D6d08a30ce9815f820fda7132e20dc42cc345eb8e8, sin avance respecto al corte previo. D6 checkout limpio; delta desde commonbase7fbd7e99 sólo v3/futures-bridge, sin intersección material SDK/Core con este carril. F09/F10 permitido sólo cmd/backtester, sin nuevos cambios shared.

ROOT_AGENT_RUN = SKIPPED: coordinación, revisión de evidencia y documentación; los segmentos de implementación/tests están atribuidos en los registros ONE-SHOT respectivos. ROOT_SESSION_CLOSE = NOT_REQUESTED.

### Handoff compacto

```text
SUBTASK = BTG-S01
STATE = BLOCKED_EXTERNAL
SDK_STATE = READY_SDK_PREREQUISITE_REVIEW_ONLY; PRODUCT_407e03dd
INPUT_STATE = E44b741e_BOUNDED_LOCAL_VERIFIED; REAL_RERUN_PENDING
NATIVE_DRIVER_STATE = FROZEN_e2e15a3559034a3ed08c04f247baf4919e20b2ff; F08_FIX_171fc712_INDEPENDENTLY_VERIFIED; CLI_e6325487_F09_F10_INDEPENDENT_PASS; F11_LOW_FRESH_REMEDIATION
BASELINE_SHA = cd451972b242c8933321e03001decd4b6d778c61
DATASET = NT_EXPORT_HISTORY_13_FILES_LISTED_AND_ENDPOINTS_READ; ORIGINALS_NOT_ACQUIRED; FULL_MANIFEST_DIGEST_NOT_AVAILABLE
GERARD_STRATEGY_AUTHORITY = OWNER_2026_10_06_S2_H4_TREND_BB_PULLBACK_V1; SHARED_DEFAULTS_SELECTED_FOR_FUNCTIONAL_RUN
GERARD_MM_AUTHORITY = D4-B2 + shared gerardmm; day1/2 SL2000/TP1500; runtime config NOT_RECOVERED; FUNCTIONAL_PROFILE_NOW_SELECTED_BY_OWNER_DELEGATION
REAL_SMOKE = NOT_RUN
LONGITUDINAL_RUN = NOT_RUN
DETERMINISTIC_RERUN = NOT_RUN
ECONOMIC_STAGE_COVERAGE = NONE_DEMONSTRATED
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = NOT_MEASURED
OPEN_MATERIAL_FINDINGS = BT2-F01_F02_F03_FIX_REGRESSION_VERIFIED_REAL_RERUN_PENDING; BT2-F04_F05_FIX_REGRESSION_VERIFIED_REAL_RERUN_PENDING; BT2-F06_F07_FIX_REGRESSION_INDEPENDENTLY_VERIFIED_REAL_RERUN_PENDING; BT2-F08_FIX_REGRESSION_INDEPENDENTLY_VERIFIED_REAL_RERUN_PENDING; BT2-F09_F10_FIX_REGRESSION_INDEPENDENTLY_VERIFIED_REAL_RERUN_PENDING; BT2-F11_LOW_REPRODUCED_FRESH_REMEDIATION_ACTIVE; B01_RESOLVED_BY_OWNER; B02_FUNCTIONAL_PROFILE_SELECTED_BY_OWNER_DELEGATION; ORIGINAL_TRANSFER_AND_NATIVE_DRIVER_PENDING
ARTIFACT = BTG-S01-REAL-GERARD-RESULT + BTG-S01-FINDINGS + identity/config + dataset inventory + NT acquisition + source SDK/remediation/final-review
PRODUCT_PR = https://github.com/xKoRx/echo/pull/2; DRAFT_AGAINST_S04
AGENTS_OS_COMMIT = final consolidated commit supplied in chat/PR handoff
GAPS_FOR_S02 = remaining config + historical corpus + horizon rows/stages + economic units/rules/fees/settlement
NEXT_PRIMARY_MANAGER_ACTION = byte-preserving authorized transfer of existing C:\Temp\history files; functional profile selected; fresh CLI F11 exact-once correction and independent gate; real slice then deterministic rerun within S01
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
