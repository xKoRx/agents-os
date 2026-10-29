---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]]"
  - "[[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]]"
  - "[[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-28"
updated: '2026-10-28'
---

# F — Final Certification

## Propósito

Certificación final del programa `forge-echo-ingestion-task-v2` (task `echo_ingestion_v2`). Este documento separa la evidencia del CORRECTOR (Shot 4, fase 1, dos sesiones 2026-10-28) y el launcher de VERIFICACIÓN INDEPENDIENTE (fase 2, verificador fresco sin autoría). **Estado reportado por el corrector (adjudicación actual en Contenido): SHOT4_BLOCKED (parciales avanzados)** — QA-S3-01..08 CERRADAS con regresiones permanentes; A/B con E2E real completo (Generic, Group, Gateway, readback, replay, subcasos); Gate C ejecutado con oráculo cumplido y estados honestos; Gate D BLOCKED_EXTERNAL re-verificado; el corrector declaró como única brecha del piso Owner **QA-S3-09: cobertura del delta nativo 80,12% < 95% por statements**. No hay autocertificación ni FORGE_ECHO_INGESTION_TASK_VERIFIED.

## Contenido

### Adjudicación gerencial del retorno y destino E2E — 2026-10-28

**SHOT4_BLOCKED; el corrector avanzó, pero el cierre aún no está acreditado.** La recepción CLOUD verificó las refs y leyó fuente en Symphony 0417330a9d1ab9c8639d8f449f6d65548382f0e1 / SDK be85d144b7dfcc8e82941c2ee0de26082de60b85 / Echo 24af786232fa362cc1599df1b9d90b1c8347b557. No ejecutó los tests, perfiles ni el runtime LOCAL. La evidencia runtime de las secciones siguientes conserva autoría del corrector. El cierre ejecutable vigente es [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]], sección «Cierre final e integración E2E».

1. **Cobertura aún abierta:** 1499/1871=80,12% del delta Symphony declarado, bajo el piso. El script/perfiles permanecen referidos al workspace LOCAL, no inspeccionados por CLOUD. Con denominador fijo faltan al menos 279 statements cubiertos para 95%; 372 corresponden al 100%. El scope final debe identificar el código nuevo del programa por repo, incluidos fix SDK, addendum Echo y adaptaciones de integración, sin legado ajeno ni un piso nuevo por archivo.
2. **Verificación sin resultado publicado en esta recepción:** el Owner comunica tercer intento en background; esta F todavía dice NO despachado. Recuperar job/resultado antes de duplicar. El launcher histórico que exige al verificador terminar cobertura queda supersedido: primero corrector listo, después verificador fresco sin autoría. Despacho no equivale a veredicto.
3. **C positivo incompleto:** B§11/14 ya exige cuatro perfiles y dos rankings pertinentes con datos suficientes. Cero targets no prueba ese positivo. Los resultados net=6/PF=2.5 e insuficiencias son útiles; faltan los positivos y readbacks requeridos. A/B/C se mantienen atribuidos por superficie y no se certifican globalmente desde este relato.
4. **QA-S3-02, subcaso reabierto por fuente:** echoSourceInstanceRef fabrica task_output:<task> o FlowRun según selector y el perfil de destino omite source_instance_ref. B§6.1/8.3 exige instancia configurada y sellada. Corregir propagación y demostrar invariancia de identidad al seleccionar la misma evidencia por cuatro modos; no se afirma duplicación persistida observada. La igualdad RunRef=FlowRunRef generalizada necesita acreditación del contrato productor y sus positivos/negativos.
5. **SDK reproducible pendiente:** raíz y sqx declaran c7f11496 con replace local, mientras el fix probado se reporta en be85d144. Sellar módulo/manifest/layout y reconstruir sin checkout accidental; GOWORK=off no anula replace.
6. **Integración E2E nueva y concreta:** cert-replay remoto 36071d819b1532cade14ce06ad691d0d33856772 utiliza dynamic-groups.v1 y un dispatcher compartido sin echo_ingestion_v2. Su ruta no queda probada por el Generic/Group legacy de s4c. Preparar un candidato desde el head fresco E2E, preservar ambas historias y reconciliar dispatcher, dependencias y migraciones. El ledger usa filename completo, no ordinal numérico: conservar nombres históricos y probar upgrades desde ambos linajes.
7. **Echo ya integrado en source:** master 347eee8bdab7f7628629af6383d1e45520815abd contiene 24af7862 y 118 commits posteriores. No reintegrar baseline viejo ni hacer downgrade; validar el Echo efectivo de la combinación final. Source no equivale a runtime desplegado.

**Precisiones:** ancestry correcta 7731cb8→d760dc3→0417330. Kafka -1001 acredita ausencia observable de offset en esa consulta; no prueba universal que nunca se commiteó ni que no hubo efectos. Mantener UNKNOWN histórico y no abrir una auditoría operacional general. D sigue separado por acceso auténtico concreto; aprovechar outputs E2E ya completados mediante lectura autorizada. Release/cambios compartidos siguen fuera de la autorización automática.

**Próxima acción autorizada:** corrector/integrador LOCAL completa los puntos anteriores, publica y prueba la combinación con el linaje E2E; verificador fresco adjudica su evidencia dentro del MISMO Shot 4. Rama de integración propia y participación opt-in con recursos propios; no alterar una corrida ya en vuelo. No nueva decisión Owner para corregir el código, pruebas, coverage o preparar la integración. La promoción con efectos de release/infraestructura compartida requiere su autorización específica.

### Integración E2E del candidato al linaje cert-replay — 2026-10-28 (tercera sesión del corrector)

**Orden ejecutado:** «Cierre final e integración E2E — 2026-10-28» del mandato, desde el commit documental c41d43fac276c6f6c1329d586616cf6cd2eba27e. Integración construida, probada y publicada; verificador fresco pendiente de despacho al candidato final (tras el grind de cobertura). Estado: SHOT4_EN_CIERRE (corrector completo salvo piso de cobertura; verificación independiente no ejecutada todavía).

#### A. Estado de entrada recuperado (mandato §1)

- **Verificador en background: SIN veredicto y SIN autoría.** El tercer intento creó worktree `verifier-symphony` y rama local `verifier/shot4-verif1` @ 0417330, sin commits, sin push, sin `VERIFIER-REPORT.md`, sin sección en F y con árbol limpio: el proceso murió antes de producir evidencia. No hay correcciones ni tests suyos que registrar. Launcher conservado en `s4c-stack/VERIFIER-LAUNCHER.md`.
- Refs remotas verificadas con `git ls-remote` al inicio: Symphony shot4 0417330, master dd4af7d, cert-replay 36071d8, SDK be85d144/c855944, Echo 24af7862/347eee8b — **todas idénticas al despacho, sin descendientes concurrentes**. La campaña física w12R estaba EN VUELO (0.4.2 desplegada en la flota, watcher certw12 y sqcli activos en sqx-ulab-zeus-0); durante la sesión la flota avanzó por trabajo ajeno a 0.4.3 en kronos (21:29Z). La corrida en vuelo NO fue alterada: cero escrituras fuera de la pila s4c propia.
- Binario 0.4.2 desplegado acreditado por `go version -m` (hash 2b2550d14a93544a…, manifiesto deploy/0.4.2): construido desde 35463d5 con **SDK c7f11496 resuelto limpio** (vcs.modified=false) — confirma que el linaje E2E en vuelo aún no lleva el fix del SDK, exactamente el hueco que esta integración cierra.

#### B. Candidato integrado (mandato §2)

| Superficie | Ref | SHA |
|---|---|---|
| Symphony integración | `origin/shot4/forge-echo-ingestion-e2e-integration` | 8e9ca6e (merge 0417330 sobre 36071d8) → 64b60c9 (dispatcher V2) → 908e4d3 (migraciones+harness flow_run) → c60c1af (source_instance_ref) → 9ad2cce (pin SDK) → 73e4899 (harness Gate C) |
| Echo (linaje del programa) | `origin/shot4/integ-gatec-fixes` | 1376476b1bcb78d3821efe83daaf080a40ad16d7 (24af7862 + 087_lab_v4_integ_metric_values_bundle_index) |
| SDK | `origin/shot4/telemetry-optional-metrics` | be85d144b7dfcc8e82941c2ee0de26082de60b85 pinneado como `v0.0.0-20261028194935-be85d144b7df` |
| Contracts | `v0.0.1-forge-ingestion-task.2` | 7496b05b inmutable; `exclude lab-v4-shot2.1` mantiene MVS |
| shared-analytics | `v0.0.1-lab-v4-shot2.1` | compatible, build verde |

- Worktree de integración propio `~/aranea/work/e2eint-20261028/wt` desde el head acreditado cert-replay; merge `--no-ff` con ambas ancestrias verificadas (`merge-base --is-ancestor` 0417330 ✓ y 36071d8 ✓). Conflictos resueltos uno a uno (runner.go de migraciones, generic_workflow.go, go.mod/go.sum, 2 fixtures generados) — sin resolución "todos de un lado".
- **Dispatcher dinámico integrado:** `sqx/workflows/task_dispatch.go` gana `case echo_ingestion_v2` → `dispatchEchoIngestionTask` (carrier intacto, misma secuencia resolve→batch→finalize, sin SQCLI ni bindings — no se inventó requisito de InputBindings ni capacidad para toda task). Outputs de productores por nombre (`EchoOutputsByName`) alimentados en la secuencia raíz V2 (root_dispatch_v2.go) y en el subflujo de grupos dinámicos (evaluate_strategy_durable.go); modo `task_output` falla cerrado si el output no fue capturado. Compatibilidad legacy Generic/Group V1 preservada (el bookkeeping M02 queda sólo en la shell sin ExecutionContract).
- **Migraciones reconciliadas:** `ordered` = 001–016 + 017/018 cert-replay + 017/018/019 ingesta (ledger por FILENAME completo). Pruebas PG nuevas (`integration_lineages_test.go`, package migrations, PG embebida por test): Fresh idempotente, upgrade desde cert-replay (fila de control preservada), upgrade desde ingesta, **upgrade desde la 018 antigua de 07c9142** (shape viejo demostrado, delta 019 aplicado, unique universal sustituida por la guardia parcial, decision_ref opcional), equivalencia de esquema Fresh↔cada upgrade por huella (columnas+índices+constraints), y boots concurrentes (4 workers, advisory lock) — todas PASS. Sin renumeraciones ni borrones de ledger.
- **Regresiones del package `workflows` mejoraron respecto al baseline:** en 36071d8 fallan 127 tests de la suite completa con el mismo comando (`go test ./...`); en el árbol integrado fallan 117 y, tras reparar el harness heredado (mocks de FlowRunStart/Seal ausentes en AMBOS linajes), la suite E2E JSON pasa 5/6 subtests que en el baseline fallaban 6/6. El conjunto de fallos restante (familia MT5 durable-mocks, magic-readback, Example_Flow_Config) está CONTENIDO en el conjunto del baseline — **cero regresiones nuevas**; las 3 únicas diferencias eran los tests del catálogo de migraciones (19→21, contract intacto, actualizados con justificación).

#### C. Correcciones del integrador (mandato §3)

1. **source_instance_ref — instancia del productor CONFIGURADA (QA-S3-02 reabierta):** `echoDestinationProfile` ahora exige `echo/ingest/v2/destinations/<id>/source_instance_ref` (fail-closed en composición, DESTINATION_UNCONFIGURED sin la clave); la instancia viaja en `ResolveRequest.SourceInstanceRef`, se sella en `EchoIngestionSourceSnapshotV1` (Validate la exige), participa del history_id y contrasta en `mapCanonicalHistoryV2` y en `MapItem` (snapshot de otra instancia ⇒ PAYLOAD_SCOPE_MISMATCH antes de Prepare). Eliminada la fabricación `task_output:<task>` y el uso del FlowRunRef del selector. Regresiones nuevas (`qa_source_instance_regression_test.go`): la identidad económica (history_id) es ÚNICA para la misma evaluación/scope seleccionada por los modos, el snapshot sella la instancia configurada en los tres modos resolubles en memoria, payload de otra instancia rechazado con error tipado antes de Prepare, y fail-closed sin instancia. Manifests ya sellados: recovery conserva autoridad/key/body (no se re-escriben).
2. **Run canónico:** el contraste `run_ref` contra FlowRunRef del binding se mantiene como aserción del perfil (no universalizada); positivo/negativos ya congelados en la sesión 2 se conservan (M04 intacto: una operación por trade, precisión del contrato, decimales, typed-null de source_evidence).
3. **SDK reproducible:** pin inmutable `v0.0.0-20261028194935-be85d144b7df` en go.mod raíz y sqx; `SDK-PIN.md` + `scripts/sync-sdk-checkout.sh` (verifica go.mod↔pin, posiciona el checkout hermano en be85d144 fallando ante trabajo local, y coteja el Sum del módulo publicado `h1:zWvLBtT7ZWD+8HXa78wnRAIaiV4vQzH4bkHaxZcpIJI=`). Resolución limpia demostrada SIN sibling ni replace: copia del árbol con replaces del SDK eliminados → `go mod tidy` resuelve el pseudo-version desde el origen, `go.sum` gana las líneas h1, y `go build ./cmd/sqx-worker` produce el binario con `go version -m: dep github.com/xKoRx/sdk v0.0.0-20261028194935-be85d144b7df h1:…`. Contrato de layout (replaces) conservado.

#### D. Matriz funcional y Gate C en s4c con el binario integrado (mandato §5)

- Worker integrado (release 9ee2d7c5b07c140f… e instrumentado 172fe45e1034c6ec…, `go version -m` con SDK be85d144 + contracts .2) desplegado en la pila s4c propia (ETCD 7445, PG 56439/forge_s4c, Mongo 27418, Garage 8345, Kafka 19096, Temporal 7234/ns s4c, Gateway 8125) tras drain del binario anterior. Pila verificada como propiedad de este programa; la sesión del verificador muerto no dejó procesos.
- **E2E legacy + dinámico con 4 perfiles de muestra suficiente:** harness `qatools/integ-gatec` (s4c) siembra 4 estrategias (integ-winner/steady/choppy/loser) con 34 operaciones cerradas cada una en 34 días compartidos (gate ranking_sample_30x30), Q_i por operación, moneda OBSERVED, tiempo DECLARED/INSTANT sin look-ahead; despacha `echo_ingestion_v2` exact_evaluations CANONICAL_HISTORY_V2 por **GenericSQXWorkflow legacy (w5) y por el dispatcher dinámico V2 con `execution_contract=dynamic-groups.v1` (w6)**. Ambas corridas COMPLETED: 8 entregas INGESTED nuevas (19 en el store; las de w4 previas incluidas), receipts estrictos y readback por la ruta integrada.
- **Gate C:** HistoryRevision → outbox → generaciones PUBLISHED (el Lab worker s4c publicó los 4 perfiles nuevos) → curvas/métricas con valores EXACTOS del fixture (profit_factor 12.857=2700/210, 4.646=2300/495, 1.818, 1.091; return_over_dd 83; SQN definidos) → snapshots de los DOS presets congelados (edge_duo.v1 1:1 y forge_quality_four.v1 5:4:4:3) con 6 miembros y exclusiones tipadas declaradas. Se conservan los positivos net=6/PF=2.5 y las insuficiencias honestas de la sesión 2. **Subcaso PARTIAL:** el positivo eligible>0 con orden esperado verificado a mano sigue bloqueado por la ventana sellada del gate de muestra — los miembros carecen de `analysis_generation_profiles` (manifests) para las generaciones nuevas y `pickSealedWindow` sella from=0 ⇒ INSUFFICIENT_DATA. Registrado como **hallazgo F-INTEG-02 (frontera Echo, con reproducción y datos)**; no se fabrica orden esperado observando el resultado.
- **Hallazgo F-INTEG-01 corregido (frontera Echo):** el índice `idx_v4_metric_values_bundle` (083) INCLUDE `reasons` desborda el tuple B-tree (3144>2704) con razones por operación (QI_UNPROVEN:<sha> ×34) — el publish de análisis muere con UNAVAILABLE para CUALQUIER perfil con muestra rica. Corregido en el linaje Echo del programa: rama `shot4/integ-gatec-fixes` con migración 087 (rebuild del índice sin reasons en INCLUDE; el access path del bundle se conserva, las razones van al heap). La ventana gobernada V4 de THE LAB V4 NO fue tocada (manifest propio de ese programa); en el harness s4c el DDL equivalente se aplicó directamente y quedó documentado como reconciliación de harness. Con el índice corregido, los 4 perfiles publicaron PUBLISHED.
- Cleanup honesto: un fixture adversarial del package `cmd/sqx-worker` (despachado a la pila viva por mi propia suite a las 20:56Z) quedó reintentando para siempre; fue cancelado (Temporal s4c). La precisión Kafka de la sesión 2 se mantiene: -1001 = ausencia observable de offset en esa consulta.

#### E. Gate D — BLOCKED_EXTERNAL con recurso/operación/error exactos (mandato §6)

- Fuente auténtica ALCANZADA por canal RO recuperado (reconexión soportada: initialize HTTP + bearer del config — el canal Mongo había expirado con -32003): BD Mongo `forge` contiene las evaluaciones del E2E vigente; p.ej. FlowRun `5cbd4400-15a3-437d-93ca-74f2ef0956b3`, stage_execution `0fce7c4c-85ec-4eae-9c1f-334648146e4d`, stage `mt5_backtesting`, artifacts OUTPUT/INPUT/EVIDENCE con digests. Esa etapa MT5 no tiene contrato de productor soportado ⇒ el resultado CONTRACTUAL correcto para ella es `UNSUPPORTED_SOURCE_CONTRACT` (comportamiento congelado y testeado; jamás conversión silenciosa a SQX).
- Bloqueo externo exacto: (1) PG de campaña `trading_systems_test@192.168.31.220:5432` (config acreditada en ETCD `/sqx-worker/certw12/postgres/*`) — el canal RO postgres fija base `echo` (sin schema sqx) y el cluster no tiene dblink/postgres_fdw; (2) los bytes de artefactos viven en el store del linaje E2E y las claves de credenciales están excluidas de los canales RO (etcd-ro: "secret-named keys are excluded everywhere"). La etapa SQX del flujo no está en la porción alcanzable. D queda **BLOCKED_EXTERNAL (parcial RO)**: metadata auténtica leída y registrada; ingesta opt-in de outputs auténticos requiere un canal RO con cross-DB o un reader autorizado vigente. No se declara FULL_CERTIFIED.

#### F. Cobertura (mandato §4) — en vuelo al corte de esta sección

Medición congelada: `covunion5.py` (scope = delta 36071d8..HEAD no-test sin qatools, NumStmt, unión max-count). Con perfiles unitarios (16 paquetes) + runtime instrumentado (GOCOVERDIR del worker durante w4–w6): **1526/2045 = 74,62%**. El grind de brechas por clusters (map 119, persistence 78, resolver 58, children 42, ingress 62, wiring 26, …) está en ejecución como continuación del corrector con el procedimiento del brief `~/aranea/work/e2eint-20261028/COVERAGE-GRIND-BRIEF.md`; resultado y SHAs en `COVERAGE-GRIND-RESULT.md` (a incorporar en la próxima actualización de esta F). Piso: ≥95% statements del código nuevo del programa (sin diluir con legado).

#### G. Pendientes externos concretos

1. **Grind de cobertura** (en vuelo): al aterrizar, congelar candidato final (build frío + hashes `go version -m`), actualizar esta F con el total y despachar el verificador fresco LOCAL sin autoría.
2. **D**: requiere canal RO cross-DB hacia `trading_systems_test` o reader autorizado para los bytes de artefactos del linaje E2E; acción concreta: habilitar base `trading_systems_test` en el canal postgres-ro o prolongar la sesión mongo/crear reader MinIO RO del linaje.
3. **F-INTEG-01**: la migración 087 del linaje Echo debe entrar a la ventana gobernada V4 de THE LAB V4 por su propio procedimiento (dueño: ese programa).
4. **F-INTEG-02**: decidir si el gate de muestra debe tolerar cohortes con miembros sin manifest (hoy envenena from=0 para todos) — decisión Echo/Lab, con reproducción entregada.
5. Verificador: launcher nuevo con los SHAs de la rama de integración final (a emitir tras el grind).

### Continuación de cierre 2 — 2026-10-28 (segunda sesión del corrector)

**Orden ejecutado:** «Continuación de cierre tras F — 2026-10-28» del mandato. Candidato recuperado, publicado, pila aislada nueva, correcciones pendientes cerradas, E2E/Gate C/subcasos completados, cobertura subida de 56,0% (bloques) a 80,12% (statements del delta nativo) con medición corregida. La sesión termina en checkpoint único: la brecha de cobertura restante es trabajo implementable documentado (§C), no un pedido de permiso.

#### A. Candidato fijado y publicado (paso 1 del mandato)

| Superficie | Ref | SHA completo | Verificación remota |
|---|---|---|---|
| Symphony | `origin/shot4/forge-echo-ingestion-task-v2` | `0417330a9d1ab9c8639d8f449f6d65548382f0e1` | push normal sin force; `git ls-remote` OK |
| Symphony (base de entrada) | ídem | `d760dc36aea211aeb4578d90fae5416af064af96` | descendiente de `7731cb84` verificado (`merge-base --is-ancestor`) |
| SDK | `origin/shot4/telemetry-optional-metrics` | `be85d144b7dfcc8e82941c2ee0de26082de60b85` (base `c7f11496`) | push normal; `ls-remote` OK |
| Echo | `feature/forge-task-contract-v2` | `24af786232fa362cc1599df1b9d90b1c8347b557` | intacto, worktree limpio |
| Contracts | `v0.0.1-forge-ingestion-task.2` | `7496b05b` (tags .1/.2 inmutables) | sin nueva versión (no hubo cambio de contrato) |
| SDK efectivo | `replace ../../sdk` | build frío `GOWORK=off` contra el checkout SDK local con el fix be85d144 | verificado en cada build |

Delta del candidato (commits de esta sesión, todos descendientes de `d760dc3`): `e9300f5` (telemetría opcional + run acreditado QA-S3-02) → `88f6056` (suites workflow/children/wiring) → `dc53a61` (typed null canónico + qavertical5) → `ec2aca4` (brechas cobertura tanda 1) → `0417330` (modos de fuente + receipt adversarial). Los fixtures ajeno `phase4_performance.json` (autoregen de benchmark) se restauraron a HEAD en cada caso.

#### B. Pila aislada s4c y manifest de ownership (pasos 2–3 del mandato)

**Ningún recurso compartido con la otra sesión ni con el corrector anterior.** ETCD 7439 (otra sesión) y 7441 (corrector previo, cliente 7441+peer 7442) intactos — el health-check inicial golpeó el 7442 ajeno y se reasignaron puertos antes de escribir nada.

| Recurso | s4c (esta sesión) | Ownership |
|---|---|---|
| PG | `127.0.0.1:56439/forge_s4c` (initdb propio, auth trust) | datadir `s4c-stack/pg-data`; migraciones 001–019 por el camino normal del producto + catálogo Echo/Lab V4 (pre_001 + applybase 001–086, 048 defer por rol `echo_user` inexistente — grants irrelevantes) |
| Mongo | `127.0.0.1:27418` (mongod propio), db `forge_s4c` | datadir `s4c-stack/mongo-data` |
| S3 (Garage) | `127.0.0.1:8345`, bucket `sqx-strategies-s4c`, key `GK65fce3ddd0732ee9d1b60ff4` | datadir `s4c-stack/garage-data` (sustituto S3 documentado; jamás MinIO real) |
| ETCD | `127.0.0.1:7445` (cliente) / 7446 (peer) | datadir `s4c-stack/etcd-data`; 42 claves sembradas (`/echo/development/*` gateway + `/sqx-worker/development/*` worker) |
| Kafka | KRaft `127.0.0.1:19096` (controller 19097) | datadir `s4c-stack/kafka-data`; cluster UUID propio |
| Temporal | `127.0.0.1:7234`, namespace `s4c`, cola `s4c-ingest` | db `s4c-stack/temporal.db` |
| Gateway | `127.0.0.1:8125` (binario Echo `24af7862`) | ETCD 7445; artifact root `s4c-stack/echo-artifacts`; identidades `producer_ingest` + `lab_readonly` propias |
| Worker | binario del candidato (`0417330`), perfil `data_only`, **metrics/traces DESHABILITADAS** | logs `s4c-stack/logs/worker-s4c.log` |
| Artifacts | `s4c-stack/echo-artifacts`, Lab out `s4c-stack/lab-out` | — |

Config efectiva del worker/Gateway registrada en ETCD 7445 (inspectable con `etcdctl --endpoints=127.0.0.1:7445 get "" --prefix`). Cero operaciones sobre flota/PROD/PG del incidente.

**Kafka DEV compartido — comprobación RO acotada (2026-10-28, canal `aranea-kafka-dev-admin`):** grupo `echo-gateway-v3-automation` STABLE con miembro ÚNICO `echo-gateway-v3-automation-consumer-daedalus` host `/192.168.31.161` (gateway DEV de producción, no del harness); topic `echo.automation-actions.v1` p0: `committed_offset=-1001` (sentinela: sin offset comprometido observable en esta consulta; no acredita historial completo), `high_watermark=low_watermark=8`, lag 0. **Acreditado:** no hay offset comprometido observable en la consulta; eso no prueba ausencia de commits históricos; no queda miembro del harness en el grupo. **UNKNOWN explícito:** si el consumer transitorio consumió sin commitear durante la ventana; qué automatizaciones (si alguna) se ejecutaron; el historial de mensajes previo a offset 8 (recortado por retención — la auditoría a nivel de mensaje es imposible desde este canal). Sin resets, replays, ni reconexión de consumers.

#### C. Correcciones cerradas en esta sesión

1. **Métricas/tracer deshabilitados (cierre del sorteo del panic `t.Activity=nil`).** Causa raíz en el SDK: `Client.TemporalMetrics()` devuelve nil con métricas deshabilitadas y `pkg/shared/temporal/interceptor.go` desreferenciaba sin guard. Fix en dos capas — SDK `be85d144`: guards en el interceptor + métodos nil-safe del bundle (`TestInterceptor_MetricsDisabled_NoPanic` ejercita el interceptor REAL vía `TestActivityEnvironment` y `TestTemporalMetrics_NilBundleNoOp`; baseline preexistente de `pkg/shared/telemetry` intacto, 5 FAILs + panic idénticos con y sin el fix). Symphony `e9300f5`: guards `GetGlobalSQXMetrics()` en quiesce-etcd/quiesce-file/watcher-steps. **Validación runtime:** el worker s4c corrió TODO el ciclo E2E con `telemetry/metrics/enabled=false` y `telemetry/traces/enabled=false` sin panic (antes de la corrección el arranque del sorteo panicaba).
2. **QA-S3-02 run acreditado (B§6.3).** `mapCanonicalHistoryV2` contrasta ahora `payload.run_ref` PRESENTE contra el `FlowRunRef` del binding (miembro; la autoridad del productor es la evidencia de evaluación). Run ajeno de la MISMA instancia ⇒ `PAYLOAD_SCOPE_MISMATCH` antes de Prepare/POST. Ausencia declarada por el productor (`RunAbsenceReason`) aceptada sin igualdad impuesta; `RunRef` vacío sin ausencia ⇒ rechazo tipado del decoder. Positivos legítimos conservados (fixture con run acreditado `flow-1`). No se impone `run_ref == EvaluationRef` universal (la igualdad existe sólo en la identidad propia B§6.2 del task_output).
3. **Typed null en el wire canónico (defecto NUEVO reproducido en runtime).** El branch CANONICAL del mapper acumulaba historias pero no acreditaba el TradeSet de cuyo artifact llegó el payload, y el cierre `len==0 ⇒ nil` serializaba `source_evidence.sources[].trade_sets: null` ⇒ el Gateway real respondía **400 INVALID_WIRE** (reproducido y diagnosticado: `DecodeStrategyIngestionV2` estricto). Corregido en `dc53a61`: el perfil canónico registra el TradeSet acreditado y el nil-ing se elimina (`TestShot4CanonicalSourceEvidenceNeverTypedNull`). Este defecto explica el rechazo del primer intento positivo y quedaba latente para TODO productor canónico.
4. **Hardening fail-closed del resolver** (`0417330`): `ResolveSource` valida deps nil con error tipado (jamás panic ni cohorte vacía).
5. **QA-S3-01..08 (sesión anterior)** permanecen cerradas con sus regresiones; los oráculos M04 se conservan.

#### D. Runtime E2E real sobre la pila s4c (Gate A/B)

Evidencia completa en `s4c-stack/logs/worker-s4c.log`, `gateway.log`, job JSONs `s4c-stack/job-s4c*.json`, y PG `forge_s4c` (inspectable):

- **Generic COMPLETED** (`sqx-main-v1-e8888888-8888-4888-8888-888888888802`, refs `flow f888…801`/`token e888…802`): flow_run_start → begin_workflow_span → resolve (snapshot sellado + stages técnicos source/finalize COMPLETED en PG) → batch (map → Prepare write-once → BindSourceBinding → POST Gateway real → receipt validado → INGESTED) → finalize (TaskResult PERSISTED) → seal → COMPLETED. Delivery `sqx.handoff_deliveries_v2`: INGESTED, post_attempts=1, receipt `ddad18d1-7fc1-46b3-a8df-6372d266527a` con 1 historia de 2 operaciones.
- **Readback:** `GET /api/v2/strategy-ingestions/by-key/<key>` HTTP 200 con el MISMO receipt (acceptance, namespace/writer, versión, operaciones, source_evidence).
- **Replay de la misma intención** (nueva corrida, mismos bindings ⇒ mismas keys): COMPLETED y converge al receipt durable **sin re-POST** (post_attempts permanece 1; una sola fila por key). El ID de workflow está contractualmente atado al flow_intent_token (`sqx-main-v1-<token>`, fail-closed verificado con IDs dispares).
- **Group COMPLETED** (`sqx-main-v1-…806`) con payload `sub_tasks`.
- **Positivo canónico COMPLETED** (`sqx-main-v1-…812`): CANONICAL_HISTORY_V2 con 3 operaciones (timestamps DECLARED, Q_i sellado, moneda OBSERVED, nets 10/−4/0) — tras el fix del typed null.
- **Ingesta con métricas deshabilitadas:** todo el ciclo arriba corrió sin métricas ni tracer (validación del cierre del panic).

#### E. Gate C — Lab E2E con positivos e insuficiencias honestas

- Outbox: `echo.history_dirty_outbox` DELIVERED vía `RelayDirtyOutbox` (labv4-worker del candidato Echo `24af7862`).
- **Generación PUBLISHED con oráculo cumplido:** `realized_net.v1 = DEFINED 6` (nets 10, −4, 0 contribuyen una vez y suman 6), `profit_factor.v1 = 2.5`, `expectancy.v1 = 2`, `max_drawdown.v1 = 4`; `sqn.v1 = INSUFFICIENT_DATA` y `NO_OBSERVATIONS` en perfiles/cortes sin evidencia — estados honestos, jamás ceros inventados.
- **Fixture insuficiente (Exposure UNKNOWN, sin Q_i):** generación PUBLISHED con `realized_net NO_OBSERVATIONS`, `terminal_count 0`, `win_rate/profit_factor NO_OBSERVATIONS` — insuficiencia visible, no ficticia.
- **Screener:** `POST /api/v2/lab/read-bundles` (rol `lab_readonly`) HTTP 200, `row_count=2` — ambas estrategias visibles con generation/history/profile `r_net_cumulative.v1`.
- **Rankings:** sin targets de ranking sembrados ⇒ cero entradas (honesto; el camino `RunRankingOnce` corre sin targets). Pendiente del verificador si el Owner exige cohortes de ranking: sembrar composición/selección y re-observar.
- Cero historias y COMPLETE/PARTIAL/GAP: la availability del fixture insuficiente es PARTIAL con reason codes; la elección de evidencia y NO_HISTORY vs HISTORY_NOT_REQUESTED quedan cubiertos por las suites O-cases de Shot 3 preservadas (EC-05/O23 con test IDs propios en `core/forge`).

#### F. Subcasos A/B pendientes — cerrados en runtime

1. **Dos workers concurrentes:** segunda instancia del binario (HOST_KEY distinto) en la misma cola; corrida `…814` COMPLETED con UNA fila de delivery nueva y post_attempts=1 — el write-once PG deduplica; sin doble POST.
2. **Crash -9 mid-run + boot fail-closed con Mongo caído:** corrida `…818` interrumpida con SIGKILL a ambos workers; el reinicio con Mongo caído abortó el boot con «bootstrap durable falló (migraciones/Foundation obligatorias)» (fail-closed correcto); restaurado Mongo y reiniciado el worker, la corrida **CONVERGIÓ a COMPLETED** (estado durable en Temporal; actividades re-ejecutadas; un solo `WorkflowTaskTimedOut` registrado). post_attempts=1.
3. **Mongo caído tras Prepare ⇒ REPORT_PENDING:** corrida `…81a` con Mongo detenido inmediatamente después del commit del delivery (polling de `handoff_deliveries_v2`); el finalize falló y Temporal lo reintentó; restaurado Mongo, la corrida **COMPLETED con `report_state: PERSISTED`** y `post_attempts=1` (sin re-ingesta ni re-selección).
4. **Receipts adversariales** (suite permanente, `qa4_ingress_gaps_test.go`): receipt malformado ⇒ UNKNOWN; receipt ajeno ⇒ REJECTED; 401/403 ⇒ UNKNOWN con un solo POST; 409/422/400 ⇒ REJECTED con cuerpo preservado; 5xx ⇒ UNKNOWN + reconciliación GET-by-key que entrega sin segundo POST; 404 en reconcile ⇒ UNKNOWN; recovery sin manifest local ⇒ fail-closed sin red.
5. **Goldens cruzados y techo SQX:** goldens de key/digest (B§9.2) y techo canónico 262144/262145 cubiertos por las suites Shot 3 promovidas (`core/forge`, `echo-handoff`, `magic-readback` — readback.go al 100% del delta).

#### G. Gate D — BLOCKED_EXTERNAL re-verificado (2026-10-28, canales RO vigentes)

- ETCD PROD (`aranea-etcd-ro`): `/sqx-worker/certw12/` = 86 claves, sólo shape legacy (`feature/metadata_export`, `maintenance/*`, `log/*`) — sin `worker/profile`, sin `echo/ingest/v2/*`.
- PG PROD (`aranea-postgres-ro`): schema `echo` sin tablas V2 del store nativo (sólo `trade_journal_v2_legacy_backup`); sin `handoff_*` ni `strategy_ingestion*`.
- Mongo RO (`aranea-mongo-forge-ro`): **error exacto** `JSON-RPC -32003 "session not found"` (sesión expirada). SSH MCP: expirado (clase igual a la sesión anterior).
- Conclusión: despliegue observado = legacy; el dataset Forge auténtico (evaluaciones/lineage Mongo + artifacts) sigue **inaccesible por recurso/operación concretos**. D permanece BLOCKED_EXTERNAL demostrado; A/B/C completan con fixtures identificados. Sin despliegues ni mutaciones PROD.

#### H. QA-S3-09 — cobertura por statements (medición corregida) y brecha vigente

**Método (reproducible):** unión por bloques con max-count sobre perfiles `-coverpkg=./...` por paquete + perfil de **runtime instrumentado** (`go build -cover`, GOCOVERDIR, boot + ciclo E2E completo + SIGTERM); denominador = statements (NumStmt) del **delta nativo** `22f337ca..HEAD` (archivos nuevos completos + bloques que intersectan líneas añadidas en archivos existentes), excluyendo `qatools/**` (harness, informado aparte). Herramienta: `s4c-stack/covunion4.py`; perfiles crudos: `s4c-stack/coverage/cov4_*.out` + `cov4_runtime_boot.out`; resultados: `coverage/COVERAGE-S4C.txt` (candidato `0417330`; hash agregado de perfiles `4dd4ab4b9ca3631b`).

**Resultado: 1499/1871 = 80,12% del delta nativo — BAJO el piso 95% (QA-S3-09 sigue ABIERTA).** Tabla por archivo (delta stmts/cubiertos): workflow `echo_ingestion_workflow.go` 72/72 (100%), readback 35/35 (100%), steps 16/16, evidence 3/3, persistence 5/5 (100%); activity 168/150 (89,3%); domain 36/33; children 80/66 (82,5%); wiring 138/111 (80,4%); sink 88/71 (80,7%); http_ingress 189/162 (85,7%); task config 110/85 (77,3%); forge resolver 277/218 (78,7%); **mapper 471/350 (74,3%)** — mayor brecha (ramas de error del mapeo económico); native 75/54; definition 34/24; stage_execution delta 11/7; generic_workflow delta 37/29; quiesce guards 6+6/0 (sólo disparan con eventos de quiesce); main delta 7/3 (boot); capabilities 1/0; mt5 delta 6/5. Harness qatools (5 tools, 0%) fuera del piso por adjudicación (harness, no producto).

**Brecha restante: 372 statements**, concentrados en: ramas de error del mapper (~120: corruption/decode/límites por registro), http_ingress (~27 restantes), forge resolver (~59), wiring boot (~27: rutas os.Exit no testables en-proceso), task config (~25), native (~21), activity (~18), sink (~17), children (~14: decodes de documentos malformados), definition (10), quiesce (12), y colas menores. **Acción pendiente concreta:** extender las tandas `qa_shot4_coverage_gaps*_test.go` (patrón ya establecido: fakes + httptest + error tipado esperado) hasta el piso; los bloques de wiring/main restantes son rutas `os.Exit` del boot → cubrir con runtime instrumentado adicional o documentar como no-unit-testeables con justificación.

#### I. Registro de capacidad de despacho (verificador)

Dos intentos de despacho del worker de cobertura fallaron por infraestructura (`Connect Timeout Error` / `project_token_request_failed`, sin producir trabajo — worktree `s4c-cov` limpio). El corrector asumió el cierre manual. El launcher del verificador (§J) está listo; si el despacho directo vuelve a fallar, queda como prompt exacto para otra sesión.

### Sesión anterior del corrector (2026-10-28, preservada)

### 1. Identidad del corrector y candidato

**Corrector:** GLM-5.3-Flash Max LOCAL/ZCode, sesiones 2026-10-28 (dos), rol TOP LOCAL por el mandato Shot 4. Bootstrap Agents-OS ejecutado una vez por sesión. Autoridad documental leída desde el commit `512771211af96da134187b3b32706422db8f4355` (xKoRx/agents-os), preservando cambios ajenos.

Worktrees del programa en `~/aranea/work/forge-echo-task-v2-20261027/`. Evidencia Shot 3 preservada ANTES de corregir: commits `d70c171a` (qa-symphony, rama `qa/shot3-adversarial`) y `8270676b` (qa-echo, rama `qa/shot3-adversarial-echo`), manifest `QA-SHOT4-PRESERVATION-MANIFEST.txt`. Pila QA previa (56438/27417/8344/7441/7233/8124) queda INTACTA y fuera de uso.

### 2. Correcciones adjudicadas por QA-S3-ID (consolidado a dos sesiones)

| ID | Corrección | Regresión permanente | Estado |
|---|---|---|---|
| QA-S3-05 | `migrations.ordered` con 017/018/019; `019_…_reconcile.up.sql` aditivo con guardia de shape; data_only pasa por `wireDurablePersistence` antes de publicar | `TestShot4FreshChainIncludesV2Store`, `TestShot4UpgradeFromLegacy018Reconciles`, `TestShot4ConcurrentBootAppliesOnce` + Fresh/upgrade demostrados en PG s4c (migraciones 016–019 aplicadas por la ruta normal) | CERRADA |
| QA-S3-06 | `SaveManifest` persiste `decision_ref NULL`; sin `decision:<key>` sintético | `TestShot4ManifestWithoutDecisionPersistsNULL` | CERRADA |
| QA-S3-08 | data_only registra spans + flow_run_start/seal; sink con StageExecution técnico real (CAS con row_version); requests echo con TelemetryCarrier; nil-guard SpanID | Suite runtime real (§D) + tests worker | CERRADA (runtime real Generic/Group en s4c) |
| QA-S3-07 | Versión por item con `VERSION_SOURCE_MISMATCH`; SEALED_REF/SQX_DEFINITION/DEFINITION_REF sin primer-gana | `TestShot4ConflictingVersionBindingsRejected`, `TestShot4VersionJoinIsByEvaluationMembership`, `TestShot4SQXDefinitionMembersMustAgree` + brechas (sello ajeno/ausente, versión derivada≠congelada) | CERRADA |
| QA-S3-04 | Key = `HashTaggedV2("forge-echo-delivery.v1", 7 argumentos)` con golden; versión congelada antes de work-item refs | `TestShot4IdempotencyKeyGoldenB92`, `TestShot4BindingDigestDistinguishesExpectedVersion`, `TestShot4DerivedModeFreezesVersionBeforeWorkItems`, `TestShot4MapItemVerifiesFrozenVersion` | CERRADA (runtime: key `sha256:f828…` congelada con la versión antes del batch) |
| QA-S3-02 | Contraste `source_instance_ref` + **run acreditado** (B§6.3, esta sesión) antes de Prepare/POST | `TestShot4CanonicalForeignIdentityRejected`, `TestShot4CanonicalForeignRunSameInstanceRejected`, `TestShot4CanonicalRunAbsenceDeclaredAccepted`, `TestShot4CanonicalRunRefEmptyUndeclaredRejected`, `TestShot4CanonicalOwnIdentityAcceptedPreservesData` | CERRADA |
| QA-S3-03 | Gate de moneda sólo cuando la fuente no acredita; OBSERVED/DECLARED preservados | `TestShot4CanonicalSelfCurrencyNeedsNoDeclaration`, `TestShot4CanonicalContradictoryDeclarationRejected`, `TestShot4TradeListDeclarationStillRequiredWithoutSourceCurrency` | CERRADA |
| QA-S3-01 | Positivo canónico y negativo separados; `Validate` intacto | `TestEchoTaskResultValidateAndSort` (rc=0) | CERRADA |
| QA-S3-09 | Medición por statements con unión y runtime instrumentado; 4 tandas de suites de brechas | Perfiles reproducibles (§H) | **ABIERTA: 1499/1871 = 80,12% < 95%** |

Hallazgos nuevos corregidos (dos sesiones): TelemetryCarrier ausente en requests echo; deref de SpanID nil; sink fabricaba StageExecutionRef no-UUID; desalineación deriver/mapper en versión congelada; mapper sin bloques `[]`; **typed null en source_evidence canónica (Gateway 400 real)**; **panic t.Activity con métricas deshabilitadas (SDK+symphony)**; resolver sin guard de deps nil.

### 3. Gates tras la continuación

- **A funcional** — PASS en superficies probadas: build/vet rc=0; suites forge/domain/runtime/sqx-definition/echo-handoff/metadata-mongo/workflows(echo)/capabilities rc=0; fallos residuales = MT5/ambientales PREEXISTENTES idénticos a la base 22f337ca (`TestDurableSelect_GenericRootUsesDurableRequest` y clase MT5 verificadas rojas en la base — atribución con comando/fixture equivalente) y el gate honesto `SQX_AUTHENTIC_FIXTURE` de readback (fixture auténtico RERUN-5 no disponible en el workspace).
- **B ingestion E2E** — PASS con Gateway real de la pila s4c: receipt `ddad18d1…`, readback 200, replay sin re-POST, conflicto de misma intención cubierto en suite (digest distinto ⇒ conflicto local; server 409/422 ⇒ REJECTED con cuerpo preservado), receipts adversariales (§F.4).
- **C Lab E2E** — PASS con límites documentados (§E): generación PUBLISHED con oráculo neto=6, insuficiencias honestas, screener con 2 filas; rankings sin targets ⇒ vacío honesto.
- **D fuente auténtica** — BLOCKED_EXTERNAL re-verificado (§G).
- **E release** — NOT_AUTHORIZED (sin cambios).

### 4. Bloqueos declarados (SHOT4_BLOCKED — causa, alcance, acción)

1. **QA-S3-09 cobertura bajo el piso (ÚNICO bloqueo vigente).** Causa/alcance/acción: §H. No hay otra decisión Owner pendiente; el trabajo es implementable con el patrón de fakes ya establecido.
2. **Gate D** — BLOCKED_EXTERNAL demostrado (§G); no bloquea A/B/C ni la preparación de revisión gerencial con límites; impide FULL_CERTIFIED.
3. **Concurrencia de sesión:** sin interferencias en esta sesión (ETCD 7439/7441 intactos; recursos s4c exclusivos). La detección de la sesión anterior (§4.4 previa) queda documentada como historia.

### 5. Launcher histórico del corrector — supersedido por el cierre final e integración

**El corrector NO despachó aún el verificador** (dos intentos fallidos por infraestructura de despacho, §I) y NO declara verificación ejecutada. Launcher exacto:

- **Entrada:** Agents-OS master (commit de publicación de esta F); mandato `SHOT4 — Correction and Final Verification Mandate` §8; candidato Symphony `origin/shot4/forge-echo-ingestion-task-v2 @ 0417330a9d1ab9c8639d8f449f6d65548382f0e1` (worktree `~/aranea/work/forge-echo-task-v2-20261027/shot4-symphony`); SDK `origin/shot4/telemetry-optional-metrics @ be85d144` (base `c7f11496`); Echo `24af7862`; contracts `.2` inmutable.
- **Pasos obligatorios:** (1) reconstruir sin heredar checkout/PID (build frío `GOWORK=off`, hash del binario); (2) repetir los nueve criterios con expected propio (los tests `TestShot4*/TestGap*/TestGap2*` son del corrector — escribir los propios); (3) repetir el ciclo E2E con seed `sqx/qatools/qavertical5` (subject seed propio ⇒ refs propias) sobre la pila s4c o una pila propia equivalente (puertos libres siguientes; NO tocar 7439/7441/7442/56438/27417/8344/19092/7233/8124); (4) revalidar la cobertura con SU propia medición (covunion4.py como referencia, perfiles propios) y **continuar el cierre hasta ≥95%** con el patrón de las tandas de brechas; (5) re-verificar Gate D con canales RO vigentes; (6) agregar a esta F la sección «Verificación independiente» con evidencia atribuible, separada de las afirmaciones del corrector.
- **Salida esperada:** READY_FOR_MANAGER_REVIEW o SHOT4_BLOCKED con causa/alcance/acción. La adjudicación `FORGE_ECHO_INGESTION_TASK_VERIFIED` corresponde al Manager, no al corrector ni al verificador.

### 6. Límites y precisión

Las lecturas PROD de Gate D son read-only por canales soportados. Garage/Kafka local son sustitutos documentados del harness. «Sin operaciones sobre PROD» = sin mutaciones. El verificador no hereda este relato como certificación. Agents-OS permanece abierto, sin feedback/L0/L1. Registry namespace `forge` y writer `2c8d1f4a-6e3b-4d97-8f51-9b4a6c2e7d30` son IDENTIDADES DEL HARNESS s4c (no de producción).

## Fuentes

- [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]], [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]].
- Evidencia ejecutable: `~/aranea/work/forge-echo-task-v2-20261027/s4c-stack/` (boot-stack.sh, seed-etcd.sh, coverage/COVERAGE-S4C.txt + perfiles cov4_*, logs worker/gateway, job-s4c*.json, sqx-worker-s4c/labv4-worker-s4c/lab-worker-s4c) y `qa-evidence-shot4/` (sesión anterior).
- Candidatos: Symphony `shot4/forge-echo-ingestion-task-v2 @ 0417330` (+ history e9300f5/88f6056/dc53a61/ec2aca4), SDK `shot4/telemetry-optional-metrics @ be85d144`, Echo `24af7862`, contracts `.2` (`7496b05b`).
