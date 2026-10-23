---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo — Producto Integrado]]", "[[0 — Shot 1 Gate and Baseline]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-23"
updated: "2026-10-23"
---

# SHOT3_ADVERSARIAL_REPORT

## Propósito

Dictamen independiente definitivo del candidato integrado de THE_LAB_V4_RUNTIME_FORGE_INTEGRATION. GOD actuó en dos fases sustantivas: despacho y revisión/adjudicación. Seis especialistas ONE-SHOT con contexto fresco, clones propios y ownership disjunto; ningún fix implementado. Los documentos históricos homónimos de V4 — Shot3 permanecen intactos.

## Contenido

**SHOT3_ADVERSARIAL_COMPLETE / SHOT4_FIX_PACKAGE_READY.** El candidato no es aceptable como producto completo; los defectos no bloquean esta entrega de auditoría. Shot4 es el único shot restante y todavía no se inicia. Sesión abierta, sin `/close`.

53 findings adjudicados: 23 P0, 29 P1 y 1 P2. H01–H49: 1 PASS, 41 FAIL, 7 NOT_RUN, 0 BLOCKED_EXTERNAL principales.

### Cortes y autenticidad del baseline

| Repositorio | SHA fijo | Tree verificado |
|---|---|---|
| xKoRx/echo, procedencia feature/ef-runtime-pools | 3b3ae81eb0905286324c899e122737f98dd45303 | c0f5a369f5122ed094a9a11424b07a99742828ec |
| xKoRx/symphony, procedencia master | dd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19 | 380b595e7329a6da31070e4266d90a7d95d12757 |

Doce clones detached independientes, sin adoptar HEAD posterior. El checkout original Symphony tenía go.work.sum modificado; quedó intacto y ese delta no se copió. D24 excluye ramas históricas Echo. Autoridades congeladas y hashes: `work/shot3/contract-manifest.json`; baseline: `work/shot3/baseline.json`.

### Dictamen de evidencia y contradicciones

- Los 57 registros originales se consolidan en 52 findings de especialistas: F-03→A-08, F-04→C-09, F-05→E-11, F-06→E-06, F-07→F-01. QA-01 agrega la brecha de cobertura basada en sus perfiles: total53. E-10 se limita a API/UX; C-11/C-14 conservan motor D11/selección temporal.
- P0 significa bloqueo de aceptación del candidato por pérdida/invención de hechos, identidad, autoridad runtime, aislamiento o integridad de publicación; no afirma un incidente desplegado. P1 cubre funcionalidad/analítica/QA obligatoria pendiente; P2 identifica trazabilidad incompleta sin pérdida demostrada adicional.
- A/F propusieron severidades distintas para readiness/fencing. Se adopta P0 porque A/C reproducen pérdida de hechos o estado y las rutas pueden aceptar/publicar sin la autoridad vigente. F aporta corroboración, no otro finding.
- H06 cambia NOT_RUN→FAIL por A-05/A-08; H13 por C-14/E-10 y H25 por E-10. La capacidad obligatoria ausente falla aunque el oráculo físico completo no haya corrido. Los otros siete NOT_RUN se conservan; no son blockers externos inventados.
- El score sí nace de ranking_entries bajo published_snapshot_ref (D). E demuestra que luego se pierde en la página durable o se combina con métricas/pins incorrectos. No se adjudica un kernel de scoring duplicado/ad hoc.
- H44 conserva FAIL principal por cota numérica C-13, además del FAIL previo de Shot2 como antecedente. El intento íntegro nuevo llegó a900.06s sin commit. No se adjudica pérdida durable, causa única de publicación ni consumo del worker a partir de ese timeout. Sys no es peakRSS. F heredó esa etiqueta del handoff; prevalece la medición y limitación de C.
- La distribución prerelease H33 existe y coincide en checksum. Fallan toolchain contractual y resolución del consumidor sqx; la paridad integral H27 quedó NOT_RUN por dependencia local SDK ausente. No se recodifica ese setup incompleto como BLOCKED_EXTERNAL.
- 075 requiere compatibilidad aditiva. Se rechaza “consolidar en070” si altera bytes ya registrados. No cambiar decisiones Owner ni reducir criterios para obtener PASS.
- La presencia de endpoints remotos en config no demuestra una solicitud. La primera prueba Vite de E no permite certificar cero conexiones; no hubo mutación remota observada/ejecutada. F-07 no se acepta como obligación de bloquear remotos en todo producto: su alcance válido es el launcher QA.

### Hallazgos adjudicados

Los detalles esperados/observados, ruta exacta, repro, corrección y regresión de cada ID están en [[10-projects/Echo/The Lab/V4 — Runtime Integration/SHOT4_FIX_PACKAGE|SHOT4_FIX_PACKAGE]] y en `work/shot3/adjudicated-findings.json`. La evidencia técnica se conserva en el idioma original del especialista. No se atribuye evidencia física a una lectura de source.

| ID | Severidad | Tipo | Hallazgo | Casos |
|---|---|---|---|---|
| A-01 | P0 | bug | JOURNALED receipt and outbox exist without a canonical journal write | H07,H10,H11 |
| A-02 | P0 | bug | Pending reconciliation irreversibly deletes observations without journalization | H08,H10 |
| A-03 | P0 | bug | Journal adapter reverses signed commission and swap | H11 |
| A-04 | P0 | bug | Journal history invents metadata and cannot preserve source scope | H11 |
| A-05 | P0 | functional_missing | Master bridge and native causal Qi integration are absent from production flow | H07,H09,H10,H11,H49 |
| A-06 | P0 | bug | Replay loses original receipt and trade lifecycle collides with event dedupe | H07,H10 |
| A-08 | P0 | bug | Readiness cannot invalidate stale consumer incarnation immediately | H09 |
| B-01 | P0 | bug | App role can forge Magic allocation events and manufacture a successful replay | H35 |
| B-02 | P0 | bug | Ingestion auto-aliases external identities onto a canonical strategy | H01 |
| B-05 | P0 | functional_missing | H12 fact persistence has no writer and grants UPDATE over source facts | H12,H35 |
| B-06 | P0 | bug | History PUT drops correction/retraction temporal evidence | H14 |
| B-07 | P0 | bug | 075 master intake is unusable by echo_user and is exposed as a normal migration despite harness-only status | H35 |
| C-05 | P0 | bug | Normalizados sin Q_i se publican READY vacíos | H16 |
| C-06 | P0 | bug | NO_FX ignora moneda de Q_i y mezcla netos de movimientos | H19 |
| C-07 | P0 | bug | Loader de historia elimina CLOSED_SUMMARY de la curva | H15,H17 |
| C-09 | P0 | bug | Fallo tardío de token viejo borra lease del nuevo; permanent reintentable | H34 |
| C-10 | P0 | bug | Publicador no valida vector de heads ni renueva heartbeat | H34,H44 |
| D-04 | P0 | bug | Stale cohort can be promoted after source advances | H29,H32 |
| D-05 | P0 | bug | Publication error swallowed then dirty state cleared | H32 |
| E-03 | P0 | bug | Read bundle binds another strategy history and mixes generations | H36,H37,H39,H40 |
| E-08 | P0 | bug | Direct economic children lack bundle owner scope | H36,H41 |
| E-11 | P0 | bug | V4 frontend retains admin-secret and legacy session fallback | H41,H43 |
| F-02 | P0 | bug | The documented rebase.sh stop path signals unowned pgboot processes and then restarts the database | H48 |
| A-07 | P1 | test_gap | Claimed t+60 test changes a field instead of emitting after a minute | H07 |
| B-03 | P1 | bug | Parallel POST with the same idempotency key returns a unique violation instead of its receipt | H02 |
| B-04 | P1 | functional_missing | Multi-instrument identity is truncated to the first instrument | H01 |
| C-01 | P1 | bug | SQN y Sharpe pierden el signo de la media | H21,H22 |
| C-02 | P1 | bug | DailyBins omite días COMPLETE vacíos y desconoce GAP | H22 |
| C-03 | P1 | bug | Current drawdown CURVE_RUNNING devuelve máximo histórico de ventana | H21 |
| C-04 | P1 | bug | Batch sin causalidad total crea puntos intermedios y DD ficticio | H17,H21 |
| C-08 | P1 | bug | Métricas del worker usan B inicial constante y exigen Q para money | H16,H21 |
| C-11 | P1 | functional_missing | Composición estática D11 carece de motor/servicio/ruta | H24 |
| C-12 | P1 | functional_missing | Límites de admisión/backpressure/deadlines no implementados | H46 |
| C-13 | P1 | bug | Cota fixed24 no propaga error de capital/presupuesto y queda por debajo del error real | H26,H44 |
| C-14 | P1 | functional_missing | Selección temporal AS_KNOWN no tiene servicio ni ejecución analítica | H20 |
| D-01 | P1 | bug | Invalid metric parse can manufacture zero input | H30 |
| D-02 | P1 | bug | Kernel accepts values outside required ranking range | H30 |
| D-03 | P1 | functional_missing | Eligibility ignores sealed 30x30 sample/window | H31 |
| D-07 | P1 | functional_missing | Echo consumers violate Go 1.24 cold-build contract | H33 |
| D-08 | P1 | bug | Symphony sqx effective consumer fails cold module resolution | H33 |
| E-01 | P1 | bug | Gateway executable never supplies V4 configuration | H36,H37,H41,H43 |
| E-02 | P1 | bug | Mounted Hasura hook rejects scoped LAB sessions; helper accepts empty identity | H41,H43 |
| E-04 | P1 | bug | Durable page drops score/rank and economic columns consumed by UI | H37,H38,H39 |
| E-05 | P1 | bug | Search and filters ignored; UI descending sort parsed as ascending | H37,H42 |
| E-06 | P1 | bug | REST page path broken; Hasura accepts invalid/foreign cursors | H41,H42 |
| E-07 | P1 | functional_missing | Hasura action transport and response cannot satisfy frontend contract | H37,H41,H42 |
| E-09 | P1 | bug | Curve/ranking selectors relabel unchanged data | H38 |
| E-10 | P1 | functional_missing | Mandatory detail/selection/composition API and UI surfaces missing | H36,H37,H39,H40 |
| E-12 | P1 | bug | V2 read parser accepts unknown fields; unsupported encoding wrong status | H43 |
| E-13 | P1 | bug | Freshness/error/navigation and detail paging incomplete | H39,H40 |
| F-01 | P1 | bug | H47 guard allows a declared port already owned by another loopback process | H47 |
| QA-01 | P1 | test_gap | Cobertura de código nuevo y caminos críticos sin certificación | H§10/transversal |
| D-06 | P2 | functional_missing | Published membership omits required provenance vector | H32 |

### Límites de certificación

No hay certificación AUTH_FORGE ni AUTHENTIC_END_TO_END_VERIFIED. A/E ejecutaron servicios reales del candidato sobre PostgreSQL18.3 propio con esquemas mínimos sintéticos declarados; demuestran los efectos descritos, no equivalencia de migraciones/Hasura. B ejecutó SQL aislado y métodos reales para identidad; C ejecutó NUM y PG propio con catálogo reconstruido y stubs inventariados; D verificó kernel/módulos y rutas fuente; F usó sentinel y espías locales. UI Vitest usa el composable real con transporte simulado; el browser real sólo llegó a carga/error, no a una experiencia funcional certificada.

Hasura físico: intento comprobado sin socket Docker ni graphql-engine disponible en E, sin fallback compartido. Subgate BLOCKED_EXTERNAL/X_RUNTIME_CAPABILITY; implementación faltante sigue FAIL. AUTH_FORGE: no se incorporó un artefacto económico autenticado con manifest; el impedimento consta en Shot2, no se redescubrió buscando campañas activas. Su disponibilidad local independiente sigue NOT_RUN; antes del gate auténtico debe aportarse copia autorizada e inmutable o documentarse el impedimento exacto. Nunca es permiso para lanzar campañas.

Capacidad: H44 intentado con SCALE132805 intacto; C fija4CPU para el test pero el host tiene8CPU/92GiB, sin límite16GiB. Timeout durante cierre COPY/FK; tuplas procesadas132805, bytes151955720, excluidas0, sin receipt/commit confirmado. PeakRSS del proceso de prueba durante ingest2,558,144KiB (~2.44GiB), worker no iniciado. H45 catálogo20k y la saturación física H46 no se certificaron. El paquete exige repetir presupuestos originales en harness declarado y estable sin reducir dataset, granularidad o cardinalidad.

### Cobertura

95% del código nuevo/cambiado **no acreditado**. A: execution0%, accounting79.5%, combinado seleccionado50.7%; C: analyze434/517=83.9%, accounting79.5%. E: gateway387/1871=20.7%, prueba sort SDK7/3810=0.2%. Son denominadores de paquetes/pruebas seleccionadas distintos, no una cifra agregable ni el delta completo. Los defectos críticos se sostienen por repros o rutas fuente, aunque suites existentes pasen. QA-01 exige mapa de delta y cobertura por paquete, agregado ponderado y checklist crítico antes de certificar Shot4.

### No interferencia y teardown

Los seis auditores verificaron SHAs/trees y clones limpios al terminar. PostgreSQL A55461/B55471/C55481/E55501, Vite E55502, browser E y sentinel F quedaron drenados según evidencias propias; D no inició servicios. C conserva pgdata inerte (~1.4GiB) y los demás repros/logs/caches declarados; no son servicios vivos. No producto editado, fixes, merge/rebase/cherry-pick, trading, deploy, ETCD compartido, campañas Forge ni backtester legacy intervenidos.

Límite explícito: primer Vite E sin overrides heredó endpoints compartidos; lo detuvo y repitió con loopback. Las llamadas observadas se interrumpieron en prompt de token antes de fetch, pero faltó captura global de requests: **cero conexiones externas no certificado**. No mutaciones remotas observadas o ejecutadas. `work/shot3/E/logs/browser-evidence.txt` conserva el detalle seguro. La siguiente ejecución debe pasar el guard browser/env antes de arrancar.

D observó un pgboot-bin residual del harness Shot2 sin listener54359 y procesos de sesiones ajenas; contradice el claim amplio de teardown previo, sin demostrar actividad DB de ese proceso. Se preservaron intactos. F probó por espías que `rebase.sh stop` selecciona por nombre y reinicia: no reutilizar ese helper antes de corregirlo. La ausencia de listener sola no acredita drenaje físico.

### Paquete y siguiente paso

Primary Manager recibe este dictamen y [[10-projects/Echo/The Lab/V4 — Runtime Integration/SHOT4_FIX_PACKAGE|SHOT4_FIX_PACKAGE]] para GLM LOCAL. Corregir todos los findings y completar gates pendientes, con revisión independiente final dentro de Shot4. Sin otro freeze, entrevistas, rescate de ramas históricas ni Shot5. [[10-projects/Echo/The Lab/V4 — Runtime Integration/SHOT3_COVERAGE_MATRIX|SHOT3_COVERAGE_MATRIX]] mantiene exactamente49 filas principales.

Evidencia grande fuera del vault, raíz lógica workspace `the-lab-v4-shot-3-god`: `work/shot3/{A,B,C,D,E,F}`. Índice verificable `outputs/SHOT3_EVIDENCE_MANIFEST.json`; los169 hashes de manifests originales fueron comprobados sin discrepancias. Los archivos raw de especialistas quedan inmutables; adjudicaciones prevalecen sobre sus propuestas. No se almacenan datasets ni secretos en el vault.

## Fuentes

[[F — Decision Register]] D09/D10/D11/D16–D24; [[0 — Shot 1 Gate and Baseline]]; contratos A–J de Runtime Integration; [[S2 — Shot 2 Delivery Status]]; [[Echo + Echo Forge — Environment Contract]]; reportes y manifests independientes A–F referidos arriba. Handoff Shot2 es claim a contrastar, no certificado.
