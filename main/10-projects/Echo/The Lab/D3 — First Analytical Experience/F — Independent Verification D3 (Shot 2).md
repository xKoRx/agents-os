---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: []
aliases: []
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d3
created: "2026-09-24"
updated: "2026-09-24"
---

# F — Independent Verification D3 (Shot 2)

**Verificación adversarial independiente del candidate D3, 2026-09-24.** Modalidad fresh context, un shot, sin relación con el implementador. El verificador NO modificó producto: cero cambios en engine, persistencia, migraciones, front, Hasura, worker o tests existentes. Veredicto y hallazgos gobernados por [[A — Product Contract — The Lab]], [[B — Architecture Decision Report]], [[D — Revised Roadmap]], [[E — First Usable Vertical Slice]], [[F — Decision Register]] y el paquete D1; la SPEC D3 de Shot 1 ([[A — Technical SPEC D3]]) se trató como claim a verificar, no como autoridad.

## Veredicto

**`SHOT2_VERIFIED_WITH_FINDINGS`** (nunca `DAY_PASS`; ni Fase 3 ni Shot 3 quedan cerrados).

El candidate implementa realmente la capacidad analítica declarada y la mayoría de sus invariantes resistieron la falsificación: determinismo, exactitud decimal, separación de bases, períodos D1, trazabilidad, atomicidad de publicación, reemplazo/staleness, migración 065 y ausencia de dependencias prohibidas. Los hallazgos F-D3-01…F-D3-07 (ninguno BLOCKER) quedan como input de corrección para Shot 3; el manager congela el alcance.

## Candidate auditado

```text
candidate_sha:        6a111c9ec7c987fed885dfea82951256af12b6e1
parent_sha:           8adce7ec98fc20517950635537e515e07c931144
candidate_parent:     verificado (git show %H %P)
candidate_commit_count: 1 (rev-list parent..candidate)
branch:               origin/feature/d3-lab-v3-first-analytical (tip == candidate; identidad por SHA, no por nombre)
diff:                 36 archivos, +4817/-2
branch excluida:      feature/d3-lab-v3-curve-engine (no auditada, no autoridad)
working_tree:         worktree detached limpio (~aranea/work/d3-shot2-verify-20260924/candidate-wt)
candidate_mutated:    NO (probes desechables eliminados; git status limpio al cierre; HEAD == candidate SHA)
```

## Hallazgos

### F-D3-01 — Publicación cruzada de StrategyVersion en el boundary del servicio · HIGH

- SEVERITY: HIGH
- AREA: `v3/sdk/postgres/lab_curve_service.go` (boundary F4)
- EXPECTED: `RecalculateStrategyVersion(ns, ref, specs)` debe fallar cerrado antes de publicar si algún spec porta identidad distinta al `(namespace, versionRef)` cuya historia se leyó; una curva jamás puede portar identidad distinta al dataset consumido (crítico porque `lab_curves` no tiene FK dura por diseño, migración 065 §1).
- ACTUAL: el servicio resuelve head+operaciones de `(ns, ref)` pero publica cada spec con la identidad que el caller puso en el spec, sin ninguna validación de consistencia. Probe físico: leyó historia de `refA` y publicó fila `lab_curves` bajo `refB` con `history_digest == head(refA)`; publicó también bajo identidad fantasma inexistente (`ns='other-namespace'`, ref inexistente) y bajo mismatch parcial (ns correcto + ref incorrecto). Los tres ataques publicaron.
- EVIDENCE: probe `TestProbeShot2_*H3*` sobre PG desechable (log `shot2-probes-go.log`); ataques 1/2/3 con `published=true`, `history_digest==headA=true`, `rows under ghost identity = 1`.
- REPRODUCER: llamar `svc.RecalculateStrategyVersion(ctx, nsA, refA, []curve.Spec{{RegistryNamespace: nsB, StrategyVersionRef: refB, ...}})`.
- CLASSIFICATION: PERMANENT_REGRESSION (candidato a regresión permanente en Shot 3).
- MINIMAL_CORRECTION: al inicio de `RecalculateStrategyVersion`, para cada spec: `if spec.RegistryNamespace != namespace || spec.StrategyVersionRef != versionRef { return error }` (fail-closed pre-transacción). No requiere DDL.

### F-D3-02 — Dataset vacío rompe la publicación con violación de constraint · MEDIUM

- SEVERITY: MEDIUM
- AREA: engine `money_cumulative` (unit vacía) × migración 065 `chk_lab_curves_unit` × servicio
- EXPECTED: un envelope válido con cero operaciones es un estado legítimo D1 (SPEC D1 §5.1); la curva debe publicarse honesta (READY sin datos inventados o INSUFFICIENT_DATA), jamás romper el recálculo.
- ACTUAL: `money_cumulative` sobre dataset vacío calcula sin error pero `Output.Unit == ""` (nunca se asigna) → el header viola `chk_lab_curves_unit` → la publicación ENTIRA hace rollback: ninguna curva de la versión se publica y el servicio retorna error de DB (`pq: new row for relation "lab_curves" violates check constraint "chk_lab_curves_unit"`). El test de engine de Shot 1 del caso vacío sólo cubre `rmoney_cumulative` (unit `R`), enmascarando el camino MONEY.
- EVIDENCE: probe `TestProbeShot2_*ServiceInsufficientAndEmpty*`: `EMPTY dataset recalc: service ERROR = ... chk_lab_curves_unit`; `no curves published at all = true`.
- CLASSIFICATION: PERMANENT_REGRESSION.
- MINIMAL_CORRECTION: en `moneyCumulativeV1.Validate` devolver `InsufficientError` cuando `len(in.Operations) == 0` (o fallback `res.Unit = desc.Unit` en el engine cuando `out.Unit` quede vacío). Decisión exacta para Shot 3.

### F-D3-03 — `operation_count` persiste basis `MONEY` en curvas READY · MEDIUM

- SEVERITY: MEDIUM (hipótesis manager H1: CONFIRMADA)
- AREA: `v3/sdk/analytics/curve/metrics.go` (`countMetric`)
- EXPECTED: basis factual `CLOSED_OPERATIONS` (constante declarada en el mismo package y usada por los caminos INSUFFICIENT/UNKNOWN del propio candidate).
- ACTUAL: en toda curva READY, `operation_count` se persiste con `basis='MONEY'` (unit `OPERATIONS`), incoherente con el dominio y con los otros dos caminos del mismo archivo. Verificado en PG: fila `operation_count status=READY basis=MONEY`.
- EVIDENCE: probe `TestProbeShot2_*H1*` + lectura `lab_curve_metrics`.
- CLASSIFICATION: PERMANENT_REGRESSION.
- MINIMAL_CORRECTION: `countMetric` usa `Basis: BasisClosedOperations` (1 línea).

### F-D3-04 — Bandas visuales de períodos ausentes: dos líneas A/B no son las tres regiones · MEDIUM

- SEVERITY: MEDIUM (hipótesis manager H2: CONFIRMADA)
- AREA: `v3/front/src/components/lab/v3/CurveV3Chart.vue`
- EXPECTED: representación visual distinguible de TRAINING_DATA / PRE_REAL / REAL (contrato UI congelado; SPEC D3 declara "bandas A/B y períodos").
- ACTUAL: el chart dibuja exactamente 2 annotations verticales (`x` con `x2: null`) en A y B, y la serie es una sola línea de un color; los períodos no existen como regiones distinguibles en el gráfico (los períodos sólo son visibles como badges de color en la tabla de operaciones). El subtítulo del propio componente dice "bandas = …", que es engañoso respecto de lo que renderiza. El test del chart sólo afirma las 2 annotations — el patrón exacto que el protocolo prohibió aceptar como prueba de bandas.
- EVIDENCE: lectura de source (`periodAnnotationAt` con `x2: null`; `colors: ['#34d399']` única) + `CurveV3Chart.spec.js`.
- CLASSIFICATION: HARNESS_TOOLKIT_CANDIDATE (test que exija `x2`/fill de región en las annotations) + corrección front.
- MINIMAL_CORRECTION: convertir las 2 annotations en regiones ApexCharts (`x2` + `fillColor` por banda, o 3 annotations de rango TRAINING/[A,B)/[B,∞)) y corregir el subtítulo.

### F-D3-05 — La UI puede presentar una curva parcial como completa · LOW

- SEVERITY: LOW
- AREA: `v3/front/src/views/lab/StrategyCurveV3TabContainer.vue` (`loadCurveDetail`)
- EXPECTED: ninguna curva parcial mostrada como completa (protocolo §14).
- ACTUAL: paginación offset (5000/página) hasta `first.total`; si una página intermedia llega vacía antes del total (p.ej. republicación concurrente de la misma curva entre páginas), el loop hace `break` silencioso, renderiza las filas parciales y el header muestra `pointsTotal` completo, sin aviso. Offset pagination bajo republicación concurrente además puede duplicar/saltar puntos silenciosamente.
- EVIDENCE: análisis de source (no reproducible determinísticamente sin concurrencia; ventana real pero estrecha).
- CLASSIFICATION: E2E_CANDIDATE (prueba de republicación concurrente durante paginación front).
- MINIMAL_CORRECTION: keyset por `seq` (`where: {seq: {_gt: $last}}`) + banner/aviso si `rows.length !== pointsTotal`.

### F-D3-06 — El rol `readonly` de Hasura no puede servir la tab (agregados) · LOW

- SEVERITY: LOW
- AREA: `v3/hasura/metadata/tables/lab_curves_v3.yaml` × `strategyCurveV3.js`
- EXPECTED: read model usable por el rol readonly declarado (migración 065 otorga SELECT a `mcp_echo_dev_ro`; el YAML declara `readonly`).
- ACTUAL: `getCurvePoints` usa `echo_lab_curve_points_aggregate` para el total, pero el permiso `readonly` no declara `allow_aggregations: true` ⇒ toda query de total falla bajo ese rol. En DEV-práctica funciona sólo porque el front hornea `x-hasura-admin-secret` (rol admin, §5.7 del contrato de ambientes).
- EVIDENCE: comparación YAML vs query GraphQL del front.
- CLASSIFICATION: corrección de metadata (1 línea por tabla agregada).
- MINIMAL_CORRECTION: `allow_aggregations: true` en el permiso readonly de `lab_curve_points` (y opcionalmente `lab_curves`).

### F-D3-07 — El header no muestra Strategy aunque está físicamente disponible · LOW

- SEVERITY: LOW
- AREA: `v3/front/src/views/lab/StrategyCurveV3TabContainer.vue` (header)
- EXPECTED: "Strategy cuando esté físicamente disponible" (contrato UI congelado).
- ACTUAL: muestra StrategyVersion (ref corto), namespace, instrumento, A/B, estado y datos; NO muestra `canonical_strategy_id`/`strategy_ref` pese a que `strategy_versions` está físicamente disponible y el propio artifact `canonical_history_readonly.yaml` otorga SELECT readonly sobre esas columnas. `timeframe` no existe en el modelo D1/D3 (correctamente omitido, no es brecha).
- EVIDENCE: source del header + YAML.
- CLASSIFICATION: corrección front (agregar query/label) — decisión de alcance Shot 3.
- MINIMAL_CORRECTION: fetch de `strategy_versions` por identidad y render de `canonical_strategy_id` en el header.

## Matriz de gates (G01–G15)

| Gate | Estado | Evidencia (una frase) |
|---|---|---|
| G01 small/extensible Curve Engine | PASS | Registry por (id,versión)+config con interfaz pública `Algorithm`; probe registró `shot2_double@v1` desde fuera del core y calculó sin tocar nada del engine. |
| G02 >=1 algoritmo funcional | PASS | `rmoney_cumulative` y `money_cumulative` verificados matemáticamente con dataset controlado (+100/−50, riesgo 100/25); `rpips_cumulative` honesto INSUFFICIENT_DATA. |
| G03 persistencia reproducible | PASS | Harness d3_curves sobre PG real: up/down/up, segunda pasada idempotente, probe de ROLLBACK sin residuo, recálculo idéntico sin duplicados (suite 10/10). |
| G04 métricas mínimas + semántica explícita | PASS con F-D3-02/03 | 9 métricas con formula/basis/unit/window/estado, NULL≠0 verificado en PG (INSUFFICIENT persiste NULL), exactitud half-even 12dp (`1/3 → 0.333333333333`); defectos: basis de operation_count y crash de dataset vacío. |
| G05 read model estable/usable | PASS con F-D3-06 | YAMLs válidos y consumibles por el mecanismo del repo (proyecto hasura CLI `config.yaml`+`metadata/`), solo-lectura, `by_pk` consistente con PK real (061/064); brecha `allow_aggregations` readonly; NO aplicado a DEV Hasura (fuera del claim del candidate). |
| G06 screen V3 muestra StrategyVersion | PASS con F-D3-07 | Tab `Curve Lab V3` con selector versión/curva, ref, namespace, instrumento, A/B, estado y datos; falta Strategy disponible físicamente. |
| G07 curva usa tiempo real | PASS | `EventAt = closed_at` real, eje datetime en el chart, test y probe (`no ordinal`) confirman. |
| G08 A/B + tres períodos representados visualmente | FAIL (F-D3-04) | Sólo 2 líneas verticales A/B; las 3 regiones no son distinguibles en el chart (badges de tabla no equivalen a bandas). |
| G09 point → operation trace | PASS | `(source, source_trade_id)` persistido; probe de trazabilidad resuelve la operación canónica; front maneja honestamente el punto stale ("dataset puede haber sido reemplazado"). |
| G10 mismo input semántico ⇒ determinista | PASS | Mismo result_digest en recálculos repetidos (suite + probe), orden canónico, permutación de input irrelevante, nil/empty config y orden de mapa sin colisiones falsas; `result_digest` reacciona a identidad/dataset/estado. |
| G11 dataset cambiado invalida/recalcula | PASS | Probe: cambio A/B ⇒ `history_digest` y `result_digest` cambian con `dataset_digest` estable; cambio de contenido ⇒ `dataset_digest` cambia; sin recálculo el header conserva digest viejo (stale detectable); replacement D1 no bloqueado por derivados (36 regresiones D1 verdes con 065 aplicada). |
| G12 sin dependencia Forge | PASS | Diff sin imports/referencias efectivas a Forge (sólo strings de no-goals y fixtures con namespace `forge-live`, nombre de registro, no dependencia). |
| G13 sin escrituras trade_journal | PASS | Ningún DML/DDL hacia journal en el diff; worker legacy (recompute/canonical_a0/materialize) intocado. |
| G14 sin segundo canonical | PASS | Sólo lecturas de `canonical_operations`; `lab_curves*` son derivados puros con upsert por identidad y sin historial. |
| G15 tests críticos afectados en verde | PASS | Reproducido desde worktree fresco: engine 100%, harness d3_curves 10/10, regresión D1 sdk/postgres 36/36, analytics+contracts+lab-worker verdes, front vitest 22/22. |

## Hipótesis del manager

```text
H1_OPERATION_COUNT_BASIS = CONFIRMED  (READY persiste basis=MONEY; CLOSED_OPERATIONS es la basis factual declarada; evidencia PG en probe H1)
H2_VISUAL_PERIOD_BANDS = CONFIRMED    (2 annotations-lineales A/B sin regiones; subtítulo "bandas" engañoso; serie monocolor)
H3_CROSS_VERSION_SPEC_PUBLICATION = CONFIRMED (3 ataques publicaron: refB con dataset de refA, identidad fantasma inexistente, mismatch parcial; boundary sin validación)
H4_SOURCE_VS_OPEN_DATE_PERIODIZATION = REJECTED (classifyPeriod = conjunción source+opened_at exactamente según SPEC D1 §3: SQX<A, MT5∈[A,B), REFERENCE≥B con B requerida; 11 casos adversariales INCLUDING exactamente-A, exactamente-B y B-NULL fallan cerrados a ERROR, jamás reclasifica; P03 se satisface porque en dataset coherente las ventanas por fuente son disjuntas y opened_at contra A/B determina la pertenencia)
```

## Invariantes congeladas

```text
FORGE_DEPENDENCY = NONE (verificado por grep del diff; sin imports/efectos)
FORGE_DUAL_HISTORY_INTEGRATION = PENDING (sin cambios; correcto)
TRADE_JOURNAL_WRITES = NONE (verificado)
SECOND_CANONICAL = NONE (verificado; lab_curves* derivados only)
```

## Evidencia de ejecución (superficies)

- SOURCE: lectura íntegra del diff (36 archivos) + contratos D1 (`HistoryDatasetDigest`, `HashTagged`, ref S0, advisory lock `hashtext(ns),hashtext(ref)` igual al replacement D1, `historyInsertChunkSize=250`, `ListOperations` 5000/cap 50000 intacto).
- FIXTURE: fixture determinista de Shot 1 verificado como introducido por mecanismos correctos (PUT D1 `ReplaceHistory` para SQX/MT5; REFERENCE por SQL declarado con provenance fixture — coherente con el alcance, no certifica autenticidad).
- DISPOSABLE_PG: PostgreSQL 17 desechable (puerto 16001 harness / 16002 probes), schema hasta 065 reconstruido; logs en workspace externo `~/aranea/work/d3-shot2-verify-20260924/evidence/` (`shot2-probes-go.log`, `d1-regression.log`).
- FRONT: `npm ci` + vitest 22/22; H2 y paginación juzgados por source (el stub de apexcharts en tests no renderiza raster: los tests no prueban bandas).
- HASURA: export de metadata DEV (RO) — `lab_curves*` ausentes del metadata vigente de DEV ⇒ artifact source-only, sin claim de aplicación; PROD RO (`mcp_echo_prod_ro`): ninguna tabla 061/064/065 existe ⇒ sin despliegue no autorizado. E2E Hasura real: UNVERIFIED_EXTERNAL (no se levantó Hasura local; no se tocó DEV compartido).
- BASELINE_COMPARISON: no se requirió para ningún hallazgo — F-D3-01…07 son introducidos por el diff del candidate (el baseline no contiene curve engine; el guard del `d1_foundation/run.sh` es vacuamente equivalente en el baseline, donde no existen migraciones >064). Ningún fallo reproducido resultó PREEXISTING_BASELINE_DEFECT.

## Clasificación de assets reutilizables (para Shot 3, NO promovidos)

- PERMANENT_REGRESSION (candidatos fuertes): F-D3-01 (cross-version publication), F-D3-02 (empty dataset publication), F-D3-03 (operation_count basis), probe de períodos adversariales (11 casos), probe de paginación 0/1/10000/10001/25001 con `opened_at` duplicado, probe de atomicidad con triggers en points/metrics + seam after_curve multi-spec.
- E2E_CANDIDATE: republicación concurrente durante paginación front (F-D3-05).
- HARNESS_TOOLKIT_CANDIDATE: test de chart que exija regiones (`x2`+fill) y no sólo annotations; test de permisos Hasura (`allow_aggregations`).
- Todos los probes se ejecutaron como archivo desechable `lab_curve_shot2_probe_test.go` (package postgres, para acceder al seam `publishFault`), ELIMINADO al cierre; no se promovió nada al candidate.

## Alcance restante / externo no verificado

- Experiencia física E2E en DEV (Hasura aplicado + front servido + browser): UNVERIFIED_EXTERNAL — requiere aplicar metadata 065/Hasura y desplegable de datos en DEV compartido; decisión de ventana del manager.
- Historia auténtica Forge: fuera por diseño (`FORGE_DUAL_HISTORY_INTEGRATION = PENDING`); toda la certificación del candidate es fixture-only, tal como declaró Shot 1.
- `pg_advisory_xact_lock(hashtext(ns),hashtext(ref))`: keying idéntico al replacement D1 (consistente), hereda la probabilidad teórica de colisión de `hashtext` de 32 bits — observación, no defecto nuevo.

## Input para Shot 3 (el manager congela alcance)

1. Correcciones mínimas propuestas: F-D3-01 (guard de identidad en boundary, fail-closed pre-tx), F-D3-02 (INSUFFICIENT o unit fallback para dataset vacío), F-D3-03 (basis 1 línea), F-D3-04 (regiones ApexCharts + subtítulo), F-D3-06 (`allow_aggregations`), opcionales F-D3-05/F-D3-07.
2. Regresiones que deberían quedar permanentes: cross-version publication, empty-dataset, metric basis, períodos adversariales, paginación de stream, atomicidad por triggers.
3. Comandos de gate final: `bash v3/sdk/postgres/tests/d3_curves/run_tests.sh` (incluye rebuild D1+065 y suite `TestLabCurve*`), `go test ./analytics/curve/`, suites `TestStrategyHistory|TestIngest|...` contra PG desechable, vitest de `v3/front` para los 4 specs D3.
4. Decisiones para el manager: (a) si G08 bandas se corrige en Shot 3 o se re-negocia el contrato UI; (b) ventana/autorización para validar E2E Hasura+front en DEV; (c) confirmar que la corrección F-D3-01 no exige DDL (no lo exige).

## Fuentes

- [[A — Product Contract — The Lab]] · [[B — Architecture Decision Report]] · [[D — Revised Roadmap]] · [[E — First Usable Vertical Slice]] · [[F — Decision Register]]
- Paquete D1: [[A — Technical SPEC D1]] (§3 períodos, §5–§9 contrato, §6 digests, §8 replacement)
- Shot 1: [[A — Technical SPEC D3]] (claim verificado), [[B — Implementation Record D3 (Shot 1)]], [[C — Evidence D3 (Shot 1)]], [[D — Debt Ledger D3]], [[E — F4 Handoff D3]]
- Workspace externo de verificación (fuera del vault): `~/aranea/work/d3-shot2-verify-20260924/` (worktree detached + evidence logs)
