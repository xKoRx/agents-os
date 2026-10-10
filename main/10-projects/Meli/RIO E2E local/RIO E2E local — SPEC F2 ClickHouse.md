# SPEC F2 — ClickHouse físico con transporte Kafka embebido

Estado: **Implementación y E2E backend soportado PASS; C6 API PM y gates externos bloqueados, F4 no ejecutado**. Owner: Rodrigo Jara. Alcance: backend F2 de [[RIO E2E local]]. Esta página reúne la SPEC vigente para revisión; las SPEC funcionales, técnicas y tareas de cada repo enlazadas abajo son la autoridad de implementación y conservan sus deltas y evidencia.

## Resultado requerido

Desde las APIs reales de Playmaker, provisionar, reconciliar y retirar MergeTree y materialized views en un ClickHouse real. Ejecutar list-warehouse y list-database mediante las APIs de actions y su polling autenticado. Los triggers y resultados circulan por Kafka embebido en las aplicaciones, con el mismo harness y contrato F1.

La aceptación requiere concordancia de API, eventos/keys/offsets, terminales y logs de PM, y SQL directo: DDL, columnas, datos, usuarios, grants y acceso real. Cada método crea recursos propios y verifica su retirada. Browser/front corresponde a F4.

## Referencias recuperadas y candidatos

Refs F1 recuperadas por fetch y objetos leídos el 10/10, cotejo de esta reanudación (f1-refs-resume-current.json, objetos recuperados y sin delta):

| Repo | Referencia publicada | Base remota recuperada | Candidato local F2 |
|---|---|---|---|
| Playmaker | [PR 1286](https://github.com/melisource/fury_rio-playmaker/pull/1286), c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f | develop 1ba12db957576db04eca686c16e6afac7564edd1 | feature/rio-e2e-local-clickhouse; HEAD f0cac94ffadd1b55d136d22ab38b437dad8e19e5 limpio |
| CP Kafka | [PR 86](https://github.com/melisource/fury_rio-controlplane-kafka/pull/86), 90710a590794e8a35b39f420013b24e2367ea4c1 | develop 6a91937c0664d83f907dec222af8a96b4042c6ae | feature/rio-e2e-local-clickhouse-regression; f8fe76718cea6aae2f03b436e9cfbee7285fa446 limpio |
| CP ClickHouse | Repo real fury_rio-controlplane-clickhouse | develop cf17797ef9bc1eb9b9bdb3329e6c70bfc8231386 | feature/rio-e2e-local-clickhouse; 61b638084d0462bbc93b5c2605463df5aa436c29 limpio |

Los originales sucios e históricos se conservan. El fix DEPROVISION b6030980501139723338390a70458f111e5d2a7f ya es ancestro de PM. Code Scanning de PM conserva startup_failure publicado; los resultados locales no cambian ese estado remoto.

## Contrato funcional por caso

Rutas vigentes: `{slot}` es `/data-products/{dpId}/components/{componentId}/environments/{environmentId}`. PROVISION usa `POST {slot}/deployments` con `{"definition_id": id}`; undeploy usa `DELETE {slot}/deployments/{deploymentId}`. Las actions usan `POST /data-products/{dpId}/actions/{action}?component_type=clickhouse-mergetree` con body `{"data": params}` y respuesta HTTP202 con `action_id`; polling autenticado `GET /v2/actions/{actionId}`. Params productivos: `teamId`/`environmentId` para list-warehouse y `warehouseName` para list-database. El contexto SDK y sus campos desconocidos se conservan en el wire.

| Caso | Entrada y resultado esperado | Oráculo físico y de transporte |
|---|---|---|
| C1 MergeTree | POST {slot}/deployments con definition_id válido; PROVISION real, STARTED → IN_PROGRESS ×3 → COMPLETED | SDK/context/key; PM terminal/logs; DB, tabla, DDL/columnas, usuarios ro/rw, grants y acceso real mínimo. El contrato vigente tiene tres progress. |
| C2 cambio MergeTree | Redeploy real de PM emite PROVISION reconciliado | ALTER observado, filas preservadas, nueva correlación y terminal PM. UPDATE literal se prueba separado en CP. |
| C3 baja | DELETE {slot}/deployments/{id} y camino inactivate pertinente | Operación nueva, ComponentRuns anteriores intactos; tabla/usuarios propios ausentes y recursos ajenos/sistema conservados. |
| C4 materialized view | PROVISION y DEPROVISION por PM | DDL/dependencia/datos/usuario/grants reales y posterior ausencia física. |
| C5 context | Rechazo PM antes del wire, o FAILED real CP cuando un trigger válido en estructura llega sin contexto válido | Sin STARTED en el FAILED correspondiente, sin efecto físico, validación intacta. |
| C6 MV UPDATE | UPDATE literal CP conserva FAILED de negocio no soportado; PM redeploy vigente emite PROVISION y reconcilia | Razón productiva y vista/usuarios/datos sin cambios en UPDATE; reconcile PM probado aparte. **Subgate PM FAILED por UPDATE literal: BLOCKED**, porque no hay API vigente que emita esa operación. No se agrega semántica de oficio. |
| A1 actions | /data-products/{id}/actions/list-warehouse o list-database, component_type=clickhouse-mergetree; polling /v2/actions/{id} | Auth/action_id/correlación; warehouse del catálogo productivo filtrado; databases de system.databases real. Negativos de params/motor/publicación, locks/CAS/TTL por owner y restore de credencial propia. |
| X1–X4 | Dos CPs juntos, foreign type, poison deployments/actions/results y restart CH owned | Sólo CP correcto procesa; DLT conserva bytes/key y barrier de offsets; restart cambia miembro, conserva offsets/PM/identidad SQL y evita replay de trabajo aceptado. |

Se conservan la matriz backend Kafka F1, PEEK, guards de actions/history, afterCommit, claims e idempotencia productivos. El publisher-loss gap y GCP provider unmapped mantienen sus resultados y límites. Los duplicados/tardíos se prueban contra el upsert real de PM y las claims actuales de CH; no se promete exactly-once.

## PLAN técnico y ownership

1. **Intake CH compartido mínimo.** Controller MVC y listener usan el intake estructural común, preservando binding/validación/routing/advice, métricas/MDC/context y dispatch productivo. Paridad con filtros/controller reales. El runtime invoca código in-process; REST/SQL nativo del motor es la frontera física.
2. **Publisher productivo, transporte local.** Bean Kafka BigQueueClient bajo el publisher existente; JSON SDK crudo snake_case, campos desconocidos/context preservados, sin envelope msg. Keys deployment_id/action_id. Beans y destrucción única probados; assets/dependencias locales fuera del jar productivo.
3. **Spring Kafka del contrato F1.** RECORD, raw bytes, auto commit/topic creation apagados; acks=all e idempotencia. ACK fuente tras aceptación o DLT confirmada, fallo DLT retiene fuente. Backoff 1000 ms ×2/reset=false; poison sin retry y FAILED de negocio normal. UTF8/trailing/envelope/límite256KiB por bytes y lifecycle/rebalance/commit/shutdown tienen gates propios.
4. **Topología N CPs por configuración PM.** Un broker/red rio-local del Compose Kafka. PM host; CH/motor en Compose propio unido a red externa. RIO_LOCAL_TOPICS suministra topología. Groups y DLTs distintas; observer assign sin group.id. Readiness comprueba padres/hijos/assignment y accepted_work pendiente. Se conserva CLI standalone/defaults F1.
5. **Motor concreto.** ClickHouse 25.8.33.6, compatibilidad SQL acreditada por cliente real; paridad de versión on-prem no acreditada. MergeTree/MV single-node. KMS local reversible, ownership local no-op y KVS/locks memoria por JVM son fronteras explícitas, sin coordinación/persistencia cross-process.
6. **Runtime único.** Contexto explícito colima-rio-kafka-e2e-01a0f8e0 con lease root; baseline y presupuestos se revalidan antes de arrancar. Ledger/nonce/labels/PID birth+PGID+argv y señales protegidas; rechazo íntegro de estado ajeno. Drain → CH/motor → MySQL → Kafka/broker/red, después ausencia de IDs/procesos/credenciales y baseline exacto. Port settlement60s más fresh-start real. VM original offline36868 queda intocada y su cleanup NO_CERTIFICADO.

## TASKS READY por repo

| Repo/owner | Trabajo y gates | Documentos de ejecución |
|---|---|---|
| PM / runner e integración | Configuración N CPs; fixtures y clientes SQL; C1–C6/A1/X/F1; capabilities/contratos/catálogo; regresión/cobertura; lifecycle, freeze y reproducción | [Funcional](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md), [PLAN](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md), [TASKS](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |
| ClickHouse / CP | Intake/paridad, adapter/publisher Kafka, Compose/motor real, lifecycle/actions, guards y SQL compatibility, full regression/cobertura/inventario | [Funcional](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md), [PLAN](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md), [TASKS](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |
| Kafka / F1 regresión | Mantener broker/red y transporte F1; contratos raw SDK, regressions y standalone del jar actual; aislamiento multi-CP | [Funcional](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md), [PLAN](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md), [TASKS](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |

## Gate de entrega y estado real

IMPLEMENT → VERIFY por agente independiente sobre candidato congelado → CORRECT/final gate. Cambios invalidan los gates afectados. Regresión productiva completa, contratos/capabilities, cobertura ≥95% líneas **y** ramas whole crítico/main modificado, IDs de clases/exec/jars exactos y aislamiento productivo. Suites seriales dos veces en stack vivo, recreación vacía y repetición; reproducción independiente desde commits limpios/cwd arbitrario/paths con espacios. Catálogo por identidades y receipts no vacíos, E2E cero failures/errors/skips. Normal conserva presupuestos productivos; gaps destructivos separados con presupuesto explícito y repetidos.

Estado de ejecución al 10/10, candidato actual:

- Java de PM, CP Kafka y CP ClickHouse: regresión y verificación independiente acreditadas para los hashes de jars y clases inventariados en VERIFICATION.
- Runner PM14: full175/0FES y cobertura whole R97.545% líneas/95.808% ramas, helper99.306%/96.983%, sin exclusiones. R0cd6b5bc/helperf53bb75a; VERIFY independiente20+batch PASS, ALL3912PID/762PGID inclZ ausentes,0SIG. Históricos PM13/RED/ERROR_PROBE conservados en journal/VERIFICATION.
- Contrato root87a5185f: comando0,23selectors/5capabilities y ocho matrices físicas104 casos0FES; PMfull4862 con dos skips heredados. Collector privado FAIL ParseError de redacción XML preservado; aceptación independiente7e5e830a desde originales válidos y hashes anteriores a redacción. Standalone Kafka25×2, fault9/native52 PASS. Critical7:513/514 líneas y268/274 ramas, IDs/exec completos; Request/Topology sin ramas=N/A, collector privado KeyError preservado y reconciliación independiente a3e81cec PASS.
- Cleanup root12 imágenes/21rmi exactos --no-prune sinforce,24fullmetadata/RootFS iguales,0containers/volumes,3nets y22puertos libres;2720PID/554PGID inclZ ausentes sinseñales. No se inventa RootFS de baseline histórico que no lo capturó.
- Primer clean bootstrap660431b713e7 desde clones/cwd externo/paths con espacios: FAIL unhealthy de motor CH antes de PM/tests; causa NO_CAUSA_AISLADA, cleanup propio certificado y corroboración externa332PID/167PGID ausentes. Jar limpio CH9166ad56 difiere de ab9156 sólo en20 descripciones de metadata Spring;897 otras entradas ZIP byteexact. Receipts nuevos usan su hash real.
- Corrección8ab2961d: Dockerfile.local añade stage engine fijado25.8.33.6 con init público y Compose elige target, eliminando bind del init; CPstage final/default y todos los guards/lifecycle intactos. VERIFY estático independiente PASS con10 probes negativos. Java/jars/productregression/cobertura conservan identidad; gates físicos afectados se repiten íntegros por verificador exclusivo: normal23×4/gap15tres×4 en cuatro stacks fresh, cleanup de nuevas imágenes atribuidas y baseline exacto. Reproducción completa PASS: cuatro normales×23 y cuatro gaps×3/15s, cuatro stacks nuevos,104ejecuciones exactas/0FES/comandos0. Fuente runtime PMc5cc53e0/CH8ab2961d/Kafka28428ff4; entrega documental f0cac94f/61b63808/f8fe7671 yclones exactos limpios; delta sólo ocho archivos existentes. Manifest ebb133f2 inmutable3136files; matrices56993045/motores-cleanup45fbb366/externalsb151d252 PASS, baseline root6430d371 y SOURCE_RELEASE aditivo. ALL2808PID/1116PGID+observadores ausentes inclZ/0SIG; cleanup14IDs/23rmi exactos,24baselinefullRootFS/3redes intactos/0containersvolumes/puertos libres/statecredsausentes. Tres verificaciones históricas L3/COV-M1 siguen FAIL sustituidos; corrección documental adicional1espacio, ninguna fuente/jar cambió. C6PMliteralUPDATE/capabilities externas/CodeQL remoto/F4 siguen sin certificación.
- C6 PM literal y Code Scanning remoto permanecen bloqueados; AOC/security/SDD canónicas necesarias ausentes se registran. F4 y el proyecto de cinco apps quedan fuera de esta certificación.

Los comandos, freezes, fallos previos, cobertura cruda, inventario de seis jars, estados por caso y cleanup están en [VERIFICATION F2](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/4-implementation/VERIFICATION.md). El histórico permanece allí y en los reportes de cada candidato.

Entrega: ramas/commits reviewables, matriz por caso PASS/FAIL/BLOCKED/NO_EJECUTADO, comandos/refs/hashes/oráculos/limitaciones/cleanup y próximo paso concreto. Artefactos clasificados PERMANENT_REGRESSION, E2E_CANDIDATE, HARNESS_TOOLKIT_CANDIDATE o DISPOSABLE_REPRODUCER. PR, merge y deploy requieren pedido específico; AGENTS OS permanece abierta.

Evidencia viva: [VERIFICATION F2](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/4-implementation/VERIFICATION.md).
