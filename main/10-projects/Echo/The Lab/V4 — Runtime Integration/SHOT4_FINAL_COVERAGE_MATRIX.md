---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo — Producto Integrado]]", "[[SHOT3_COVERAGE_MATRIX]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-25"
updated: "2026-10-25"
---

# SHOT4_FINAL_COVERAGE_MATRIX

## Propósito

Exactamente H01–H49 con un veredicto principal por ID al cierre del Shot 4, más QA-01 transversal. Veredictos en tres fases: auditoría W6 (congelado 757b927a) → revalidación (055cd69c) → cierre (b2b3ebfe). Oráculos: contrato H — Test Matrix Independent Oracles.

## Contenido

**Cierre Shot 4: 47 PASS / 2 FAIL** (H45 sub-invariante de presupuesto prepare con piso contractual medido; QA-01 transversal 85,8%/85,2% vs ≥95%). Cero BLOCKED_EXTERNAL principales; cero NOT_RUN (los 7 NOT_RUN de Shot3 ejecutados íntegros).

| Caso | W6 | Reval | Cierre | Oráculo (síntesis) | Evidencia |
|---|---|---|---|---|---|
| H01 | FAIL | PASS | **PASS** | HTTP real sobre echo-gateway-harness: crosswalk B§3 (creación Magic, replay misma ref, ref adicional mapping íntegro, contradictorios display/timeframe/instrume |  |
| H02 | PASS | PASS | **PASS** | Race 20 AcceptIngestionV2 concurrentes misma (ns,writer,key,body) a nivel servicio + HTTP: 409 same-key-diff-body, GET-by-key, replay 200, snapshot inmutable, r |  |
| H03 | FAIL | PASS | **PASS** | PUT races N→N+2 (2 PUT concurrentes mismo expected N), 428 sin precondición, 412 stale, If-Match header ≠ body, replay ganador tras N+2, integridad de revisione |  |
| H04 | FAIL | PASS | **PASS** | 8 historias válidas; 9ª inválida en mismo envelope; >8 historias; >128MiB; SIGKILL mid-COPY (orquestación interna Go, crashchild + pg_stat_activity) con readbac |  |
| H05 | FAIL | PASS | **PASS** | REGISTER_ONLY + readback strategy_definitions/runtime_strategy_links/crosswalk; PROVISION_REFERENCE: sin profile, profile no autorizado (con y sin allowed_profi |  |
| H06 | FAIL | PASS | **PASS** | D17/B07 config aplicada: driver propio oracles/ (h06.go) contra production CreateBinding/RuntimeConfigSupervisor/RuntimeACKRepository; readiness por SQL readbac |  |
| H07 | PASS | PASS | **PASS** | D17/B08 master t+60s con reloj REAL del server: driver h07.go vía ingress REAL (MasterObservationFn.Invoke desde copia byte-idéntica diff -r verificada; transpo |  |
| H08 | PASS | PASS | **PASS** | D17/B09 master pre-ready/bulk: driver h08.go: binding en vigencia + readiness PENDIENTE; OPEN/CLOSE pre-ready; ghost CLOSE; crash durable; reconcile por ingress |  |
| H09 | PASS | PASS | **PASS** | D17/A-B recovery fencing: driver h09.go con gate REAL postgres.NewRuntimeReadinessGate en engine nativo + bridge; restart real de encarnaciones; readback SQL |  |
| H10 | FAIL | PASS | **PASS** | D17/18/B10 crash points: driver h10.go en DOS procesos (arm con os.Exit(9) real tras commit; recover contra el durable), repro por punto; replay/conflicto A-06; |  |
| H11 | PASS | PASS | **PASS** | D17/18/B11/12 source ownership: driver h11.go vía ingress real; dos cuentas/versiones; readback durable echo.history_operations + strategy_history_revisions.cov |  |
| H12 | PASS | PASS | **PASS** | ExecutionFactStoreSQL (writer único Go): APPLIED/DUPLICATE/CONFLICT_QUARANTINED; cuarentena con payload previo; fill tardío + ListUnresolvedConflicts; same-seq  |  |
| H13 | FAIL | FAIL | **PASS** | Físico íntegro: writer real (AcceptIngestionV2) 2 historias Forge/Echo con dos representaciones del mismo hecho (carry 11:50→12:10, Echo start 12:00) + crosswal |  |
| H14 | PASS | PASS | **PASS** | POST N(+40) → PUT N+1 CORRECTION(+30, effective/known RFC3339Nano) → PUT N+2 RETRACTION(0); readback canonical_operation por revisión; history_change_entries ef |  |
| H15 | PASS | PASS | **PASS** | Físico: writer real + worker real sobre PG propia; 3 representaciones (CLOSED_SUMMARY 114 con descomposición gross120/−4/−2; grano movements +120/−4/−2; summary |  |
| H16 | FAIL | PASS | **PASS** | Físico: writer real + worker real; ciclo válido Q100/net50 (sello CYCLE_BUDGET previo), parcial OPEN +40/−2, y 4 mutaciones de sello (TICKET_INITIAL_RISK 20, FI |  |
| H17 | FAIL | PASS | **PASS** | Físico: 4 targets por writer/worker reales — sucesivos (días), simultáneos sin orden (streams distintos), mismo timestamp con orden causal TOTAL (un stream seq  |  |
| H18 | PASS | PASS | **PASS** | NOT_RUN Shot3 → físico ÍNTEGRO: writer real (2 ciclos owner B cierra primero +5, A luego +20, multiplier 1) → pipeline real completo (relay→claim lease60s/heart |  |
| H19 | FAIL | PASS | **PASS** | Físico: 3 ciclos (EUR100/QEUR100, USD100/QUSD100, EUR100/QUSD100) por writer+worker reales; readback de series money del motor, estados, razones y terminales R |  |
| H20 | PASS | PASS | **PASS** | Físico: PUT real N (rev1) y N+1=80 (rev2 vía PutHistoryV2 CAS); received_at REALES de la BD con corte ENTRE ambos (el backdate está denegado físicamente: trigge |  |
| H21 | PASS | PASS | **PASS** | Motor real ComputeMetrics sobre fixtures contractuales; expectativas exactas del oráculo independiente Python (Fraction/Decimal 80+): terminales [−1,2,−1/2,0];  |  |
| H22 | PASS | PASS | **PASS** | Físico (writer+worker: carry-in +40 antes de ventana, +60 cierra dentro, OPEN −20) + motor real DailyBinsCovered/SharpeRealized sobre perfil normalizado 10000→1 |  |
| H23 | PASS | PASS | **PASS** | NOT_RUN Shot3 → físico ÍNTEGRO: writer+worker reales; ciclo X Q=10 B=100 sellado a C=10000 con −1100 (−110R) y luego +200 (+20R); nueva OPEN (op-new) emitida co |  |
| H24 | PASS | PASS | **PASS** | Físico: PutStaticComposition real (CAS) + worker STATIC_COMPOSITION real; miembros A (.6, +2R/−1R secuenciales, ciclo pre-origen) y B (.4, −1R); subcasos .6/.3  |  |
| H25 | FAIL | PASS | **PASS** | Búsqueda de superficie + código: rg 'expected_qty/refVWAP/adverse/slippage' en v3/{lab-worker,gateway,front/src,sdk/lab,sdk/postgres}; lectura del handler real  |  |
| H26 | PASS | PASS | **PASS** | Físico (d=1,Q=3,C0=10000,r=.01 por writer+worker reales) + motor real (FromRat/Display12/cotas) contrastado con oráculo independiente Python Fraction/Decimal y  |  |
| H27 | PASS | — | **PASS** | Oráculo independiente propio (Python stdlib Fraction + binary64 en orden canónico E§3, tools/w6d_oracle.py) comparado a nivel de BITS contra tres vertientes eje |  |
| H28 | PASS | — | **PASS** | Mismo oráculo independiente propio + permutaciones (6 órdenes de entrada, Edge y Quality) + goldens G01-G06 congelados del módulo (TestG01..TestG06, TestH28Perm |  |
| H29 | PASS | — | **PASS** | Kernel: oráculo propio G03 + TestG03OutlierRecalculatesAll + TestH29RemovingOutlierRestoresOriginalScores. Cohorte/publicación: probe adversarial PROPIO TestW6d |  |
| H30 | PASS | — | **PASS** | Adaptador Echo (wmetric.ParseMetricInput, ruta efectiva del worker) + kernel fuente congelado + kernel RESUELTO publicado (v0.0.1), singleton y cohorte, con orá |  |
| H31 | PASS | — | **PASS** | E2E contra PG propia 55511: suite congelada TestD03SampleGate30x30 + gate unitario (TestPickSealedWindowDeterministic, TestApplySampleGateTypedReasons) + probe  |  |
| H32 | PASS | — | **PASS** | PG propia 55511: suites congeladas D-05 (sqlmock 7/7 puntos de escritura + PG física: fallo mantiene pointer/dirty, replay avanza pointer, CONTRACT_CONFLICT sin |  |
| H33 | PASS | — | **PASS** | Builds fríos ejecutados por el auditor con toolchain go1.24.1 (GOTOOLCHAIN=go1.24.1, GOWORK=off, GOMAXPROCS=2, GOPROXY=https://proxy.golang.org,direct, GOMODCAC |  |
| H34 | PASS | PASS | **PASS** | Auditoría independiente propia (audit/audit-bin, módulo con replaces al worktree congelado; conduce Claim/Fail/Renew/Publish/Relay/Retry de RuntimeBindingReposi |  |
| H35 | FAIL | PASS | **PASS** | SQL físico como echo_user (SET ROLE): forja INSERT/UPDATE events; fn_v4_assign_magic_allocation (primera asignación atómica, replay idéntico/conflictivo, terna  |  |
| H36 | PASS | PASS | **PASS** | Pin N/N+1: bundle preparado pre-PUT (bundleN0), PUT CAS revisión N+1 (412/428 clase verificada en H43), prepare post-PUT (bundleStale), children detail/points/o |  |
| H37 | FAIL | PASS | **PASS** | Screener server-side: prepare con sorts/filtros, paginación 1/50/200 concatenada, q literal y metacaracteres, filtros allowlist e imposibles, comparación contra |  |
| H38 | PASS | PASS | **PASS** | 4 curvas × 2 rankings server-side (REST+GraphQL), hijos de curva por perfil, URL state en browser real + reload, Vitest 75/75 |  |
| H39 | FAIL | FAIL | **PASS** | Detalle con pin exacto + calendar/distribution/operaciones/movements server-side con verificación NUM independiente + drill en browser real |  |
| H40 | FAIL | PASS | **PASS** | Estados en catálogo completo (68 filas) + keysets con tie-breakers sobre 201 operaciones y 202 movimientos misma marca temporal + estados en browser |  |
| H41 | PASS | PASS | **PASS** | Hook REST + scoping REST/GraphQL/action/WS físico + DML + login least-privilege + clases 401/403/404 + mutaciones de negocio por rol |  |
| H42 | PASS | PASS | **PASS** | 61 filas own 50+11; cursors tampered/no-base64/truncado; contexto distinto (bundle/sort); foreign bundle y cursor; límites 0/1/200/201/-1/abc/1junk/999999; bund |  |
| H43 | PASS | PASS | **PASS** | Negatives de wire/auth/CAS sobre ingesta y control + sin efectos laterales + errores sin internals + bundle front con env admin/control + engine log del browser |  |
| H44 | PASS | PASS | **PASS** | TestH44ScaleHistory132805 committed (workerstest/scale_h44_test.go) re-ejecutado por el auditor sobre PG fresca, afinidad 4 vCPU, con monitor externo /proc+disc |  |
| H45 | FAIL | FAIL | **FAIL** — presupuesto prepare p95 ≤2s a 20k permanece falsificado: mejora 40% (EXPLAIN 6,9→4,0s; índice 083 + plan query) pero el COPY del payload contractual (~38MB/bund | TestH45Catalog20k committed + oráculo propio completo (audit-bin h45: seed 20k + detalle 2400 ciclos + drain + 2 cohortes + SLOs + walks 1/50/200 + corrección 1 |  |
| H46 | PASS | PASS | **PASS** | Saturación HTTP física contra el gateway REAL (echo-gateway-harness, wiring de producción, loopback 55565; saturate_h46.py con body goteando) + 3 tests committe |  |
| H47 | FAIL | PASS | **PASS** | Oráculo propio del auditor sobre Guard.Allow/Load (suite independiente sandbox/guard-audit/w6g_h47_oracle_test.go, GOWORK=off GOMAXPROCS=2): sentinel loopback c |  |
| H48 | PASS | PASS | **PASS** | Oráculo físico propio sobre rebase.sh sellado (sha256 cf0e01f7…, jamás editado; instrumentación por entorno: función zsh kill + espías PATH rm/setsid/pgrep/pkil |  |
| H49 | PASS | PASS | **PASS** | A/runtime nativo: driver h49.go con operation.NewEngine + MM REAL gerardmm.Manager (plan EVALUATION day1, Scaling real) + gate REAL de readiness; recovery vía c |  |
| QA-01 (transversal) | FAIL | FAIL | **FAIL** (85,8/85,2 < 95; críticos cubiertos; residuos estructurales) | unión de perfiles -coverpkg cruzado, denominadores file-level y hunk-level del delta ac0621a1..cierre, metodología W6h/reval-h | evidence/w6/w6h · evidence/reval/reval-h · evidence/fix3-c |

## Notas de cierre

- H13: criterio definitivo de dedupe = tokens cruzados mutuos; oráculo del auditor re-construido contra el cierre: 6 PASS / 1 INFO / 0 FAIL.
- H39: import del screener reparado; vite build OK en el cierre; server-side ya PASS en reval.
- H45: única invariante falsificada = prepare p95 ≤2s a 20k (piso medido del COPY contractual ~38MB = 3,0–3,5s; índice 083 y plan query aplicados, −40% EXPLAIN; mejor caso 8,4–10,0s). Los otros 22 checks del oráculo H45 pasan.
- QA-01: críticos cubiertos a nivel comportamiento (mutaciones demostradas); gap a 95% = clases estructurales (interceptor de driver a volumen, etcd real, entropía, wiring).
- AUTH_FORGE: BLOCKED_EXTERNAL/X_AUTH_ARTIFACT (sin copia autorizada; NUM/SCALE/NEGATIVE etiquetados; nunca se lanzaron campañas).

## Fuentes

SHOT4_FIX_PACKAGE; H — Test Matrix Independent Oracles; SHOT3_COVERAGE_MATRIX; evidence/w6, evidence/reval, evidence/fix2-*, evidence/fix3-*, evidence/final-verify; SHOT4_INDEPENDENT_FINAL_REVIEW; SHOT4_FINAL_IMPLEMENTATION_REPORT.