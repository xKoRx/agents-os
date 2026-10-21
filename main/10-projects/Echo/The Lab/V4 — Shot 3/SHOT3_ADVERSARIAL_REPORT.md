---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[0 — Submanager State]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-21"
updated: "2026-10-21"
---

# SHOT3_ADVERSARIAL_REPORT

## Propósito

Establecer garantías y defectos del candidato parcial de The LAB V4 y dejar aceptación ejecutable para Shot 4. Ejecutor independiente: **GPT-6.1-Sol / reasoning high**, superficie Codex LOCAL, por sustitución explícita del Owner. No atribuir esta ejecución a GLM. No hubo fixes de producto ni Shot 4.

## Contenido

### Dictamen y alcance efectivo

**AUDIT: BLOCKED. PRODUCT: INCOMPLETE. VERDICT: FAIL_DEFECTS_AND_INCOMPLETE_SCOPE. NEXT: GOD_CRITICAL_VALIDATION.** El trabajo funcional autorizado quedó investigado y entregado; la auditoría original no está completa porque el harness restringió la continuación y excluyó pruebas dinámicas de autenticación, autorización, aislamiento de seguridad y traversal. Esos casos son **NOT_RUN — harness safety restriction**, nunca PASS. No se reintentaron pruebas excluidas. No hay aprobación de Astra.

Corte inmutable auditado: `xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f`, rama entregada `feature/lab-v4-shot2`, base `d74b652500e673fc2bf4289f9f195f11960ba26e`. Cuatro commits entregados; delta de 29 archivos, 4.132 inserciones y 29 eliminaciones. HEAD del implementador coincidía con ese corte y su árbol estaba limpio antes y después de la investigación. Clon propio detached; sólo se agregaron tests de auditoría sin editar implementación. Baseline independiente detached en el SHA base.

Autoridad aplicada: instrucción actual Owner > D09/D10/D11/D16 > aceptación V3 e invariantes > diseño compatible > realidad de source y ejecución. Freeze aceptado `agents-os@eb9ad25e`, blob `cee739a8f8ae7c0bfe2d7e30bc473c88ab608c78`; no se reabrió discovery, freeze ni entrevista. Se leyó el mandato íntegro, la SPEC completa y las fuentes obligatorias. La admisión parcial permite auditar, no aprobar I1 incompleto.

### Entorno y autenticidad

Workspace externo resuelto como el workspace local de este chat; activos entregables en `outputs/SHOT3_AUDIT_EVIDENCE/`. `VAULT_ROOT` resuelto al checkout vigente de `xKoRx/agents-os`, sobre master. Rutas persistidas relativas a esas autoridades. El clon, data-dir, socket y evidencias de trabajo viven fuera del vault.

PG propio: PostgreSQL 16.3, puerto loopback **54339**, usuario efímero local `audit`, bases `echo_labv4_audit`, `echo_labv4_baseline`, `echo_labv4_upgrade`, sin secretos ni credenciales compartidas; data-dir `work/shot3/pgdata`. No se reutilizó puerto 54329 ni data-dir del implementador. Se reutilizaron sólo binarios PostgreSQL disponibles localmente. Go 1.27.1 linux/amd64; kernel Linux 7.0.0-38-generic. Locale C/SQL_ASCII; fixtures ASCII, sin certificación Unicode. No conexiones a infraestructura compartida, seeds, PROD, trading, campañas ni despliegues.

Se inspeccionaron defaults, DSN y efectos antes de ejecutar. `go test ./postgres` se lanzó desde `v3/sdk`, corrigiendo la receta ambigua del handoff. Contratos es un módulo Go anidado; gateway se validó con un go.work externo mínimo que incluye sdk/contracts/sdk/gateway del clon local. Un primer intento GOWORK=off no resolvía contracts; se corrigió el workspace de pruebas sin tocar go.mod de producto.

Harness entregado verificado desde el commit: `migrations_labv4_harness_test.go` SHA256 `6afe60ed85837febabee1adbb9cd3ddddca0bb10da0ca387b0244866bc2cd502`; `strategy_history_ingestion_v2_test.go` SHA256 `08a7bd86a0e7c363e19b323096468da7184d0657d22f7ea7cc906d9456cecff9`. El incidente histórico de pérdida untracked no se da por reparado por un árbol limpio: aquí se verificó el contenido realmente entregado y se observaron sus huecos.

### Resultados ejecutados

| Grupo | Casos distintos | PASS_EXECUTED | FAIL_EXECUTED | Evidencia |
|---|---:|---:|---:|---|
| Siete TestLabV4 entregados | 7 | 7 | 0 | evidence/reported-seven.json |
| Nuevos funcionales A01–A23 | 23 | 6 | 17 | evidence/functional.json |
| Migraciones con datos M01–M04 | 4 | 3 | 1 | evidence/migrations-data.json |
| Regresión funcional postgres candidata | 5 | 1 | 4 | evidence/candidate-functional-regression.json |
| Regresión funcional gateway candidata | 2 | 0 | 2 | evidence/candidate-gateway-functional.json |
| **Candidato, casos distintos** | **41** | **17** | **24** | Sin contar wrappers ni repeticiones |
| Contraste baseline, casos comunes | 5 | 5 | 0 | baseline-functional-regression.json y baseline-gateway-functional.json |
| Oráculos racionales independientes | 11 | 11 | 0 | independent-oracles.json; no son producto |

Repeticiones dirigidas adicionales: A13/A14 con `-race -cover` (CAS PASS, replay FAIL; sin data race reportada, coverage parcial 7,1% de postgres), A09 con referencia sintética retenida en `lab.curves` (FAIL) y una ejecución individual del test legacy (FAIL). No inflan los 41 casos distintos. No se ejecutó la suite completa del monorepo ni las suites completas postgres/gateway porque contienen casos excluidos y diagnósticos contra servicios compartidos. No hubo skips entre los 41 casos seleccionados. Los NOT_RUN y faltantes están explicitados en la matriz, no convertidos a PASS. `go vet` de postgres, contracts y gateway/internal PASS. staticcheck no estaba disponible; NOT_RUN. No se certifica coverage 95%.

**Garantías demostradas acotadas:** replay secuencial y CAS existentes; CAS verdaderamente concurrente con una aceptación y una precondición fallida; rechazo transaccional multihistoria sin aceptación parcial; fallo de sink sin escritura durable; neto +114 por SQL una sola vez; rechazo de down 069 con datos; upgrade sin aplicar ni registrar 066, preservando versión e historia V1; fallo real a mitad de 069 con rollback; down/up preservando datos fuente legacy; retirement sin armar conserva objetos y marca BLOCKED_SKIP. Esquemas, DTOs y comentarios no demuestran adapters, worker ni producto visible.

### Findings

Todos los paths y líneas siguientes corresponden al SHA completo auditado. Los repros A y M están en `repros/`; sus fallos son aserciones del comportamiento esperado, no tests modificados para quedar verdes.

#### S3-F01 — La ingesta válida por movimientos no funciona en dos caminos básicos

**Tipo CODE_DEFECT; P1/alta. Contrato:** G1/G2, T01–T04, C04. **Source:** `v3/sdk/postgres/strategy_history_ingestion_v2.go:370–405, 613–625, 728–735`. **Repro:** A01 envía una operación terminal válida cuyo neto y único movimiento son `10`; A02 envía dos operaciones abiertas válidas con un movimiento cada una. **Esperado:** aceptación exacta y atómica. **Observado:** `10 != 10.000000000000000000`; en A02 FK `strategy_history_movements_op_fk` porque el bucle interior recorre TODAS las operaciones mientras la exterior todavía no las insertó todas. Con otro orden también puede intentar duplicar movimientos. **Impacto:** bloquea historias terminales válidas y cargas multioperación, aunque 7/7 originales pasen. **Mínimo:** comparar importes numéricamente bajo precisión canónica; insertar cada movimiento una vez después de su operación, o insertar todas las operaciones antes de todos sus movimientos. **Aceptación:** A01/A02 verdes con los mismos oráculos; 132.805 operaciones íntegramente procesadas, sin multiplicación de filas. No rellenar el neto con ceros decimales prohibidos por wire para rodear el fallo.

#### S3-F02 — El contrato de append dentro de revisión contradice su identidad reproducible

**Tipo DESIGN_DEFECT con defecto de código demostrado; P1/alta. Contrato:** invariante de input fijado, C05, G5/T13/T42, freeze §4. **Source:** freeze §4 permite append en la revisión activa y terminalización in-place; SQL `069...up.sql:474–550`. **Contraejemplo/repro:** A09 sella neto 10, retiene una referencia sintética `lab.curves` a revisión 1 y agrega coste −2; commit aceptado, mismo head/digest y suma ahora 8. A17 agrega a SUPERSEDED; A10 cambia instrumento/lado/precio de OPEN; A11 borra un resumen sin cambiar revisión. **Esperado:** una revisión fijada significa un único input exacto. **Observado:** filas y economía cambian bajo la misma identidad; el trigger de suma sólo dispara al escribir operations y el guard omite columnas/DELETE. La referencia de curva fue sintética, no salida de un worker existente. **Impacto:** resultados históricos y actuales pueden consumir distintos inputs con el mismo manifiesto; una conciliación terminal puede quedar falsa. **Solución mínima:** toda aceptación de nuevos hechos, costes, correcciones o terminalidad publica nueva revisión/snapshot/digest/artefacto y mueve head en una transacción; mantener las revisiones aceptadas inmutables. No crear otra cadena por movimiento. **Superficies:** servicio v2, DDL/guards, adapters futuros, lectura de worker/manifiestos y retención. **Aceptación:** resultado fijado en N se reproduce byte/económicamente igual después de append, terminalidad y corrección en N+1; UPDATE/DELETE/INSERT sobre N aceptada se rechazan; head nuevo invalida/encola lo dependiente.

#### S3-F03 — Terminalidad SQL admite dinero incompleto y suma monedas incompatibles

**Tipo CODE_DEFECT; P1/alta. Contrato:** dinero exacto, no FX inventado, T26/T39/C04. **Source:** `069...up.sql:331–348, 515–550`. **Repro:** A07 INSERT terminal con movimiento 10 pero neto/moneda/terminal_at NULL; A08 OPEN con +10 USD y −1 EUR, después UPDATE terminal a 9 USD. **Esperado:** rechazo del sello incompleto y de la suma sin FX demostrado. **Observado:** ambos commits aceptados; `NULL <> suma` no entra al IF y SUM no valida moneda. **Impacto:** resultado terminal indefinido o conversión monetaria ficticia. **Mínimo:** CHECK/trigger exige campos terminales en INSERT y UPDATE, comparación NULL-safe y moneda uniforme compatible con el neto; conservar por moneda lo que no se puede agregar. **Aceptación:** A07/A08 fallan con error de contrato, +120−3−2−1 USD sigue 114; abonos positivos legítimos no se rechazan por su signo.

#### S3-F04 — La revisión no conserva sus metadatos completos y el sink es opcional

**Tipo CODE_DEFECT; P1/alta. Contrato:** D16, C05, G4/G5, E.1/E.2. **Source:** `strategy_history_ingestion_v2.go:223–237, 347–366, 445–455, 502–505, 694–723`. **Repro:** A03 acepta sin sink y graba artefacto NULL; A05 cambia construction_at en PUT y se acepta revisión 2, pero la historia sigue con la fecha anterior; los bytes del artefacto son iguales para ambas fechas. **Esperado:** input exacto retenido, metadatos actuales coherentes y revisión anterior reproducible. **Observado:** el artefacto sólo contiene contract/history/run_mode/count + operaciones; omite MM, cobertura, referencia y fechas; PUT sólo cambia head/digest/updated_at. **Impacto:** clasificación pre/post y contexto pueden diferir del digest aceptado; datos no recuperables desde el artefacto retenido. **Mínimo:** sink obligatorio en servicio real, rechazo antes de aceptar si falta/falla; snapshot canónico completo de historia y metadata versionada, con head/read model coherente. **Aceptación:** A03 rechazado y A05 conserva ambos metadatos exactos, digests/artefactos distintos y readback correcto; falla entre store y commit no publica filas, y artefactos huérfanos quedan para mantenimiento sin borrado concurrente. A04 prueba fallo de sink; A22 sólo prueba conflicto posterior a store, no crash físico ni fsync.

#### S3-F05 — Receipts no cubren todas las carreras ni la identidad del recurso

**Tipo CODE_DEFECT; P2/media. Contrato:** T10/T11/T12, E.2. **Source:** `strategy_history_ingestion_v2.go:135–161, 193–196, 245–249, 287–299, 411–435, 484–485`. **Repro:** A14 sincroniza dos requests idénticos antes del lock mediante sink barrera; uno acepta y otro devuelve unique violation. A15 acepta PUT UNCHANGED sin receipt, luego otra revisión hace que su replay devuelva 412. A21 reutiliza la misma clave/body para el mismo history_id en otra versión del mismo writer; devuelve éxito de la primera aunque el segundo head no cambió. **Esperado:** mismos recurso+contenido convergen al receipt; otra identidad entra en conflicto. **Observado:** precheck fuera del lock, early return sin receipt y digest PUT sin version_ref/path. **Impacto:** reintentos ambiguos y éxito durable referido a otro recurso. **Mínimo:** incluir identidad de método/recurso/version/historia en la huella, resolver receipt dentro del protocolo serializado y persistir también UNCHANGED. **Aceptación:** A14/A15/A21 verdes, dos requests concurrentes con contenido diferente producen un commit y conflicto de negocio, nunca error SQL genérico. No se trata de una prueba de autorización.

#### S3-F06 — Validación permite pérdidas de significado y precisión

**Tipo CODE_DEFECT; P2/media. Contrato:** inputs exactos, G2/G4/G5, C04/D16. **Source:** `contracts/strategy_history_v2.go:320–407, 438–480`; `strategy_history_ingestion_v2.go:599–607, 663–672`; `069...up.sql:282–327, 378`. **Repro:** A06 cambia MMContextJSON sin alterar su digest declarado y conserva digest de revisión; A19 cambia SourceRef del movimiento sin cambiar digest operativo, porque el digest de movimiento no se recalcula; A12 transforma timestamps inválidos conocidos en NULL; A23 acepta `0.1234567890123456789` y PG guarda `0.123456789012345679`. **Esperado:** semántica/digest canónico ligado a todo el contenido, error explícito ante datos inválidos o fuera de precisión soportada. **Observado:** contexto confiado, fuente no ligada al digest, fechas descartadas y redondeo silencioso. **Impacto:** linaje, clasificación y dinero divergen de lo aceptado. **Mínimo:** canonicalizar y recalcular contenido completo; validar fechas/orden temporal y escala antes de persistir; rechazar precisión no soportada o ampliar representación explícita. **Aceptación:** estos cuatro repros verdes sin sustituir missing por valores inventados; corregir contenido cambia revisión y artefacto.

#### S3-F07 — Down 067 puede destruir fills sin marcar entorno destructible

**Tipo CODE_DEFECT; P1/alta. Contrato:** C01, migración/rollback seguro. **Source:** `067_execution_projection_v4.down.sql:8–23`. **Repro:** M04 inserta un fill válido con operations vacía y ejecuta down sin bandera destructible. **Esperado:** rechazo por datos en cualquiera de las tablas afectadas. **Observado:** down aceptado, tabla poblada de fills eliminada; el guard sólo inspecciona execution_operations. **Impacto:** pérdida de evidencia de ejecución durante rollback. **Mínimo:** evaluar datos en cada tabla que se va a borrar y rechazar sin autorización correspondiente. **Aceptación:** filas aisladas de fills/orders/decisions/observations sobreviven a down no autorizado; rollback explícitamente destructible sólo en descartable y con resultado registrado.

#### S3-F08 — Los fixtures existentes no son compatibles con el esquema integrado V4

**Tipo CODE_DEFECT del harness; P2/media. Contrato:** reproducción de suites pertinentes y autenticidad de evidencia. **Source:** `strategy_identity_repository_test.go:34–39`; `gateway/internal/forge_ingest_handler_test.go:62–66`; nuevas FK en `069...up.sql:207–212`. **Repro:** TestIdentity_Insert65And1024, TestIngest_G01_201, TestIngest_ExactReplay_200_NoArtifact y dos tests POST gateway. **Esperado:** fixture prepara el esquema vigente y ejercita la aserción. **Observado:** baseline 5/5 PASS y candidato 5/5 FAIL por TRUNCATE incompleto ante nuevas FK; TestIngest_AuthenticForgePolicyID, nuevo, falla por la misma causa. **Impacto:** el verde completo reportado no se reproduce tras aplicar 069; muchos tests no alcanzan comportamiento. Es regresión integrada del harness, no prueba de fallo económico de esas rutas legacy. **Mínimo:** cleanup transaccional en descartable que incluya todas las tablas dependientes, sin desactivar FK/guards ni alterar oráculos. **Aceptación:** suites funcionales existentes alcanzan sus aserciones después del bootstrap V4; los tests excluidos mantienen su estado NOT_RUN hasta levantarse la restricción.

#### S3-M01 — Falta la entrada vertical I1 y la integración auténtica Forge

**Tipo MISSING_IMPLEMENTATION; P1/alta. Contrato:** G1/G6/G11, T08, E.1/E.2. **Evidencia:** búsqueda source y delta al SHA: el servicio v2 sólo se construye desde tests; no handler/rutas v2, consultas de receipt/historia, perfiles solicitados ni adapter Forge auténtico v2. **Esperado/observado:** productor→endpoint→historia→LAB→PUT usable versus biblioteca sin consumidor real. **Impacto:** no hay producto vertical. **Mínimo/superficies:** gateway, wiring, contracts y productor Forge existente; 128 MiB/413 y límite de memoria real. **Aceptación:** artefacto auténtico aislado, readback, actualización y conciliación original; fixtures sintéticos no satisfacen G11.

#### S3-M02 — Falta captura causal Q_i, atribución por Operation y adapters comunes

**Tipo MISSING_IMPLEMENTATION; P1/alta. Contrato:** D10, C03/C04, G2/G8, T02–T09/T20/T27/T28/T45. **Evidencia:** no emisor QI_SEALED ni topic `echo.execution.operation-facts.v2`, adapter journal/runtime/backtester v2, store/proyector v4 funcional o conciliación de cuenta. 067 define tablas/comentarios, no writer; el runtime y FIFO existentes siguen iguales al baseline. **Impacto:** no se demuestra presupuesto ni PnL lógico; un DTO con CYCLE_BUDGET no lo acredita. **Mínimo/superficies:** primera MMDecision, correlación OrderID→OperationID, aritmética de ledger reutilizada, publishers/adapters y servicio común. **Aceptación:** B abre110/cierra115=5 mientras FIFO físico=15; dos resultados conciliados sin igualarlos artificialmente; parciales/costes OPEN y entrada backtester→mismo servicio; dos entradas con riesgo de primera entrada distinto de presupuesto del ciclo.

#### S3-M03 — Faltan worker, cuatro perfiles, métricas y publicación coherente

**Tipo MISSING_IMPLEMENTATION; P1/alta. Contrato:** G3/G5/G10, D09, F.2, B.6. **Evidencia:** 070 sólo tablas; servicio no crea jobs/curvas pendientes ni invalida dependientes. No worker que consuma lab.jobs, algoritmos V4, métricas B.6.5, manifiesto completo, leases/fencing/CAS o coalescing. **Impacto:** ni curvas ni estados analíticos de I1 funcionan. **Mínimo/superficies:** sdk puro, servicio transaccional y lab-worker. **Aceptación:** 10.100 simultáneo/10.098 secuencial; cuatro perfiles, insuficiencia honesta, parciales en tiempo económico; carreras sobre historia+selección+portfolio; worker viejo no publica y último head acaba visible.

#### S3-M04 — Faltan selección, dashboard, metadata y lectura coherente

**Tipo MISSING_IMPLEMENTATION; P1/alta. Contrato:** G4/G6/G8, T16–T19/T29/T32/T43–T45, E.3. **Evidencia:** sin delta front/Hasura, selección principal sólo tabla; no mutación/read model V4 ni vistas temporal/cohorte/pre-post, cobertura/frescura o comparabilidad/copias explícitas. **Impacto:** datos no visibles como producto y sin garantías de interpretación. **Mínimo/superficies:** servicio de selección, consultas paginadas, metadata aditiva y Vue. **Aceptación:** una generación completa, stale visible, cortes D16, principal/alternativas y faltantes explícitos; copia ausente no es cero.

#### S3-M05 — Falta composición estática y conservación de capital

**Tipo MISSING_IMPLEMENTATION; P1/alta. Contrato:** D11/G7/T30/T31/T41, E.4. **Evidencia:** portfolios/members sólo DDL, sin servicio, cálculo, selección/revisión fijada, start flat ni validación de suma de pesos. **Impacto:** no se puede demostrar 6k/4k ni impedir beneficio anterior al capital. **Mínimo/superficies:** servicio Lab/composición, worker y UI existentes. **Aceptación:** 10k 60/40 conserva 6k+4k, cash remanente, sin operaciones abiertas antes del start, sin reinversión/financiación entre miembros; insuficiencia se propaga y se etiqueta retrospectivo.

#### S3-M06 — Falta sustitución completa y cutover genérico

**Tipo MISSING_IMPLEMENTATION; P1/alta. Contrato:** G9/T34, D08/C01. **Evidencia:** runtime/topic/proyector antiguos y front legacy siguen; no consumidores reales de las tablas genéricas. 071 sin armar deja BLOCKED_SKIP, correctamente, sin demostrar retiro completado. **Impacto:** sigue vigente la experiencia previa y la autoridad compartida debe preservarse al cortar. **Mínimo/superficies:** inventario CURRENT→TARGET, adapters/core/projector/worker/front/Hasura y plan de migración existente. **Aceptación:** cero consumidores exclusivos legacy, historia conciliada y huecos declarados; una sola experiencia Lab, journal/recovery intactos; retiro real requiere permiso/ownership específico.

#### S3-E01 — Cobertura y capacidad no demostradas

**Tipo EVIDENCE_GAP; P2/media. Contrato:** G10/C06 y umbral de coverage. **Evidencia:** no benchmark V2/20k/SLO numérico ejecutado ni informe de memoria/backlog; digest de historia usa insertion sort en `contracts/strategy_history_v2.go:463–468`, coste cuadrático de peor caso frente al cap 250k. No se ejecutó benchmark ni se atribuye una latencia inventada. Bootstrap 001 verifica sólo cantidad=9 de errores, no sus identidades; en esta ejecución fueron siete update_updated_at_column, uno update_active_positions_timestamp y uno notify_risk_policy_changed ausentes. Atomicidad por db.Exec simple sí reproducida; la prueba original era un script toy y M01 añadió fallo dentro de 069 real. **Mínimo:** whitelist precisa de errores conocidos, fallar ante cualquier error distinto; ordenar O(n log n), medir envelope real y carga completa preservando grano; fijar evidencia numérica operativa dentro de Shot 4, sin otro freeze. **Aceptación:** benchmark repetible con hardware/dataset/distribución/concurrencia/tiempos/memoria, 132.805 ops en una historia y catálogo20k; coverage crítico ≥95% con caminos semánticos, no este 7,1% parcial.

#### S3-E02 — Límite del harness impide completar la auditoría original

**Tipo ENVIRONMENT_LIMITATION; P1 para certificación, sin atribuir defecto al producto. Contrato:** alcance original A/F, T33/T36. **Evidencia:** instrucción de continuación del coordinador restringe pruebas dinámicas de autenticación/autorización, aislamiento de seguridad y traversal tras alerta automática del harness. **Esperado/observado:** auditoría completa versus alcance funcional permitido. **Impacto:** AUDIT BLOCKED; ninguna garantía de seguridad queda certificada. **Mínimo:** mantener NOT_RUN y entregar evidencia actual; resolver externamente el alcance permitido antes de declarar gate completo. **Aceptación:** verificación independiente autorizada de esos casos dentro de Shot 4; no se propone otro modelo/proveedor, subagente, quinto shot ni bypass del harness.

### Límites adicionales y procesos

No se ejecutaron casos dinámicos excluidos de E-04, traversal, namespace/writer ajeno, mutación de recetas como ataque ni receipts ajenos. Se leyó su source y se registra EVIDENCE_GAP/NOT_RUN. Los cambios selectivos E-04 y guards de seeds no fueron revertidos; el guard nuevo de TestScratch_QueryDB evita el DSN fijo, pero los diagnósticos Kafka/ETCD restantes siguen apuntando servicios compartidos en source, iguales al baseline: PREEXISTING, no ejecutados. No llamar PASS a su exclusión.

Los tests originales de movimientos no prueban ingestión terminal: insertan OPEN y hacen UPDATE por SQL; no contradicen A01. El sink nil del fixture tampoco prueba retención. A13 concurrente se ejecutó con dos goroutines reales, sin certificar concurrencia sólo con tests secuenciales. La reproducción A09 fija una referencia derivada sintética para probar estabilidad de input; no inventa un worker implementado.

No hay presupuesto semántico Q_i demostrado por fuente real, integración Forge auténtica, crash físico del store, GC, leases, dashboard, portfolio o benchmark ejecutado. Son faltantes/evidencia abierta concretos. Al finalizar se detuvo el PostgreSQL propio, conservando datos/logs para reproducibilidad; no se limpiaron árboles ni procesos ajenos. Los workspaces separados impidieron repetir el incidente untracked; ésa es la mejora de proceso demostrada.

## Fuentes

- [[F — Decision Register]], [[THE_LAB_V4_Diseno_para_revision]], [[1 — TECHNICAL_FREEZE_PACKET]], [[2 — Preflight Evidence (U01–U06)]], [[0 — Submanager State]], [[Echo — Producto Integrado]], [[Echo + Echo Forge — Environment Contract]].
- `xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f` y baseline `d74b652500e673fc2bf4289f9f195f11960ba26e`; source paths/lineas arriba. Evidencia externa: workspace Codex de este encargo, `outputs/SHOT3_AUDIT_EVIDENCE/`, MANIFEST.sha256.
- [[SHOT3_COVERAGE_MATRIX]], [[SHOT4_EXECUTION_PACKAGE]], [[GOD_REVIEW_BRIEF]], [[SHOT3_DIRECTED_EXTRACTS]].
