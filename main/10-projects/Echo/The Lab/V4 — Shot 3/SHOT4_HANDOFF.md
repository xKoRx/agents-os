---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[0 — Submanager State]]"
  - "[[SHOT3_ADVERSARIAL_REPORT]]"
  - "[[SHOT4_EXECUTION_PACKAGE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-21"
updated: "2026-10-21"
---

# SHOT4_HANDOFF

## Propósito

Handoff final de Shot 4 (SHOT4_AUTHORIZED_CORRECTIONS_AND_I1_COMPLETION): correcciones S3-F01–F08, capacidades S3-M01–M06, evidencia S3-E01, límites S3-E02 conservados. Ejecutor: Implementation Submanager LOCAL (motor efectivo GLM-5.3-Flash, host-declarado; el perfil GPT-6-Luna del encabezado del mandato no pudo verificarse desde este runtime y se registra la discrepancia). Corte de entrada `xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f`; rama de producto `feature/lab-v4-shot4`; SHA final del candidato `fa24546f` (6 commits, 46 archivos, +6.180/−303). PG descartable propio 54349 (`~/aranea/work/lab-v4-shot4-20261021/pgdata`), sin tocar servicios compartidos ni el clon Shot 2.

## Registro de implementación

| Commit | Paquete | Contenido |
|---|---|---|
| `adfd3be0` | P0–P3 | S3-F01/F03/F06 ingesta exacta; S3-F02/F04 revisiones inmutables + snapshot completo; S3-F05 receipts semánticos; S3-F07 down 067; S3-F08 fixtures + allowlist 001 |
| `04158d51` | P4–P5 | S3-M01 HTTP v2; S3-M02 Q_i causal + economía por Operation (`lab/opfacts`) |
| `99574e0f` | P6 | S3-M03 encolado transaccional + worker + 4 perfiles + métricas B.6.5 |
| `52fe4cb9` | P7 | S3-M04 read models paginados + rutas gateway + tab Vue + metadata Hasura aditiva (archivo) |
| `540e045c` | P8 | S3-M05 composición estática (D11) |
| `fa24546f` | P9 | S3-M06/E01 capacidad medida + binario lab-worker-v4 + orden canónico O(n log n) |

## Matriz S3-F → resolución → evidencia

| ID | Resolución | Evidencia (repro del auditor, PG 54349) |
|---|---|---|
| S3-F01 | Comparación decimal NUMÉRICA (big.Rat, `10`≡`10.000…`); operations PRIMERO y luego cada movement UNA vez | A01/A02 PASS |
| S3-F02 | Revisiones aceptadas INMUTABLES en DB (guards 069: UPDATE/DELETE bloqueados; INSERT sólo en revisión creada en la MISMA tx — xmin); toda corrección/terminalidad publica N+1 vía servicio con snapshot completo y head atómico | A09/A10/A11/A17 PASS (A09 setup adaptado al contrato adjudicado: sello por N+1 del servicio, oráculo de identidad conservado) |
| S3-F03 | Sello terminal completo en INSERT (guard); net check NULL-safe y POR MONEDA (sin FX: moneda ajena impide el sello) | A07/A08 PASS; A18 (+120−3−2−1=114, setup vía N+1) PASS |
| S3-F04 | Sink OBLIGATORIO (sin sink no hay aceptación); artefacto NDJSON con header de snapshot completo (D16/MM/cobertura/versionado); `header_json` por revisión; read model del head actualizado coherentemente en cada N+1 | A03/A05 PASS |
| S3-F05 | Huella del request liga método/recurso/versión/historia/revisión-esperada; replay resuelto DENTRO del advisory lock; UNCHANGED deja receipt durable; colisión = conflicto de negocio (409), jamás unique violation crudo | A13/A14/A15/A21 PASS |
| S3-F06 | Digests ligan contenido completo (SourceRef de movement, MMContext canónico, history_id); timestamps STRICT (inválido = error, jamás NULL); `numeric` sin typmod (sin redondeo oculto) + `MaxDecimalDigitsV2=64` declarado | A06/A12/A19/A23 PASS |
| S3-F07 | Down 067 evalúa TODAS las tablas que elimina (fills/orders/decisions/observations) | M04 PASS; A20 PASS |
| S3-F08 | Fixtures descubren referenciantes FK vía pg_constraint (baseline y candidato); cadena V4 explícita en la lista base; seed identity_bwc aplicado por rebuild; allowlist 001 por IDENTIDAD de error (7+1+1 exactos) | 5 tests comunes baseline PASS en candidato (3 postgres + 2 gateway); TestCertification 18/18 PASS |

## Matriz S3-M/E → estado → evidencia

| ID | Estado | Evidencia |
|---|---|---|
| S3-M01 | COMPLETADO (G11 acotado) | Rutas reales POST/GET/PUT + receipt lookup + catálogo; 128 MiB/413/409/412 probadas; recorrido request→receipt→historia→lectura→PUT→N+1 en HTTP real+PG (`TestStrategyHistoryV2_FullVertical`). **G11 Forge auténtico: PENDING_AUTHENTIC_ARTIFACT** (fallback del mandato: fixtures sintéticos prueban contrato; sin artefacto auténtico accesible) |
| S3-M02 | COMPLETADO | QI_SEALED una sola vez en la primera decisión que abre riesgo (gerardmm sella en MMState `cycle_budget_*`/`entry_risk_*`; engine sella tras admitir órdenes; sello tardío rechazado como observación, jamás como decisión); `lab/opfacts`: identificación específica (A/B lógico 5 vs FIFO cuenta 15, delta visible), parciales 0.8R−0.3R−0.1R=0.4R una operación terminal, costes publicados en ciclo abierto, terminalidad concilia net=Σ; publisher → MISMO servicio común (modo BACKTEST probado sin venue) |
| S3-M03 | COMPLETADO | Encolado transaccional en la tx del head + coalescing de objetivos superados (QUEUED→STALE); claim SKIP LOCKED + lease + fencing (=attempt); publicación atómica CAS contra manifiesto completo; worker obsoleto NO publica sobre head nuevo; oráculos: +114 una vez, 10.100 simultáneo, 10.098 secuencial; N reproducible tras N+1; INSUFFICIENT_DATA/CAPITAL_EXHAUSTED honestos |
| S3-M04 | COMPLETADO (metadata PREPARADA, no aplicada) | Catálogo paginado con cursor estable; perfiles unidos SÓLO a la revisión del head (una generación coherente); STALE visible mientras se calcula; faltantes explícitos (missing ≠ cero); detalle D16/MM + operaciones paginadas; tab Vue read-only (sin recálculo financiero en front); metadata Hasura aditiva read-only en repo — **NO aplicada a ningún Hasura compartido** (requiere ownership) |
| S3-M05 | COMPLETADO | 60/40 ⇒ allocations 6000/4000, cash explícito, pesos ≤1 (sin préstamos), flat start excluye historial previo reportándolo, contribución = capital_i×(V/V_base−1) (jamás suma dos curvas de 10k), insuficiencia propagada, resultado etiquetado RETROSPECTIVO; servicio PG valida D11 transaccionalmente |
| S3-M06 | PARCIAL — inventario y sustitución segura (ver abajo) | Cutover/retiro real requiere permisos de ownership (071 BLOCKED_SKIP se mantiene honesto) |
| S3-E01 | CERRADO | Allowlist 001 por identidad; orden canónico O(n log n) con equivalencia probada (digest independiente del orden); **capacidad medida**: 132.805 ops íntegras en UNA historia vía servicio común = 2m40s (828 ops/s, receipt rev1, 4 jobs encolados); catálogo 20k sembrado, página 1 y página 2 por cursor con límite 50 |
| S3-E02 | CONSERVADO | T33/T36 y pruebas dinámicas de seguridad: NOT_RUN — harness safety restriction; sin reintento, sin renombrado, sin PASS por omisión |

## Inventario de sustitución CURRENT→TARGET (S3-M06)

| Superficie CURRENT | TARGET | Clase | Estado |
|---|---|---|---|
| Servicio historia V1 (D1 `strategy_history.go`) | Servicio común V2 (`strategy_history_ingestion_v2.go`) | ADAPT (convive hasta migrar consumidores) | V4 activo; V1 intacto (sin tocar consumers ajenos) |
| Proyector/journal/runtime legacy | `lab/opfacts` publisher + execution.* V4 (067) | REUSE (motor y aritmética) / ADAPT | Adapter publisher probado; wiring runtime→producer queda en integración operacional (sin modificar decisiones de trading) |
| `echo.lab_curves`/`echo.lab_curve_metrics` D3 (065) + `LabCurveRepository` | `lab.curves`/`lab.curve_points`/`lab.metric_results` V4 (070) | REPLACE (código nuevo conectado); DELETE diferido | V4 publicado por worker; D3 sigue vivo para sus consumidores; retiro real = 071 gated (BLOCKED_SKIP honesto, no equivale a borrado) |
| Front legacy (StrategyLabClean/CurveV3/AccountLab/Portfolios) | Tab LAB V4 read-only | ADAPT (una experiencia Lab, V4 primero) | Tab registrado en la lens; retiro de tabs legacy tras verificación de consumidores por entorno |
| Worker legacy (lab-canonical-a0/lab-materialize-pg) | `lab-worker-v4` | REPLACE | Binario nuevo disponible; el legacy sigue operando su ciclo vigente |
| Nombres genéricos | `lab.*`/`execution.*` genéricos; adapters específicos preservados | REUSE | Cumplido por diseño V4; sin facade perpetua (el V4 es la ruta canónica nueva) |

**Sin tocar**: journals, recovery, configuración ajena, seeds, event triggers Hasura, permisos existentes. Retiro destructivo: REQUIERE permisos específicos por entorno y consumidor — fuera del alcance de Shot 4.

## Matriz G1–G11 / T / C (estado Shot 4)

| Gate | Estado | Nota |
|---|---|---|
| G1 | PASS funcional | handler real + receipts semánticos + CAS; seguridad dinámica NOT_RUN (E02) |
| G2 | PASS funcional | grano dual + Q_i causal + economía por Operation |
| G3 | PASS funcional | 4 perfiles + métricas B.6.5 + estados honestos |
| G4 | PASS funcional | metadata D16/MM en snapshot+read model; selección principal = tabla 069 (lifecycle de selección para UI queda en I2) |
| G5 | PASS funcional | cadena única inmutable + receipts + worker CAS/fencing |
| G6 | PASS funcional | read models + tab V4 + metadata preparada (no aplicada) |
| G7 | PASS funcional | composición estática D11 |
| G8 | PARCIAL | adapters al servicio común probados; copia/comparación declarativa en I2 |
| G9 | PARCIAL | retiro real gated (071 BLOCKED_SKIP); inventario arriba |
| G10 | PARCIAL | capacidad medida (132.805 + 20k); SLOs de producción requieren ventana compartida |
| G11 | PENDIENTE | PENDING_AUTHENTIC_FORGE_ARTIFACT (fixtures no satisfacen G11) |
| T01–T32, T34–T35, T37–T45 | CUBIERTOS por los tests nombrados arriba | ver commits; T34 M01–M04 PASS |
| T33/T36 | NOT_RUN — harness safety restriction | S3-E02 vigente |
| C01–C06 | CERRADOS con las correcciones adjudicadas | C06 caps+medición incluidos |

## Verificación ejecutada (una pasada, PG 54349)

- `go vet` postgres/contracts/gateway/lab/opfacts/futures: LIMPIO.
- postgres: `TestLabV4*` 7/7, `TestShot3Functional` 23/23, `TestShot3MigrationsWithData` 4/4, worker 4/4, read models, portfolio PG, capacidad (sort+20k+132k) — `ok`.
- lab/*: analyze (incl. portfolio), opfacts, curves, metrics, riskpolicy, segments, dataquality, ids, formulas — `ok`.
- futures: gerardmm (incl. QI budget tests), operation, domain — `ok`.
- gateway/internal: suite completa `ok` (go.work del repo; con GOWORK=off no resuelve contracts — misma receta del auditor).
- Front: `vite build` OK con el tab LAB V4.
- PREEXISTING (no regresión): `TestTGFilterSharedTypedLiveBacktestFactoryParity` falla idéntico en la base `61ac1f72` (wiring de analytics view, ambiental).

## Adaptaciones de repros documentadas

A09/A18 sellaban terminalidad por UPDATE SQL directo (contrato freeze §4 original). El mandato adjudicó el contrato de revisiones inmutables (terminalidad publica N+1). Los setups se adaptaron al contrato corregido y los ORÁCULOS se conservaron: A09 identidad de input fijado bajo referencia sintética `lab.curves` (ahora sobre la revisión sellada del head); A18 conservación exacta +114 (ahora vía PUT N+1, comparación numérica exacta). Ninguna aserción económica debilitada.

## SHARED_ENVIRONMENTS

Sin cambios. PG descartable propio (54349) ya detenido al cierre; sin PROD, trading, campañas, migraciones en compartidas, merges, deploys ni aplicado de metadata Hasura.

## RESIDUALS

1. **G11**: integración con artefacto auténtico de Forge (requiere artefacto autorizado accesible).
2. **S3-E02**: cobertura dinámica de seguridad sigue NOT_RUN (restricción del harness); ningún PASS de seguridad declarado.
3. **Metadata Hasura**: preparada en repo (`v3/hasura/metadata/tables/lab_v4_derived.yaml`), aplicación real requiere ownership.
4. **Cutover/retiro legacy** (071): gated por ownership+consumidores por entorno.
5. **Selección principal/alternativas UI** (tabla 069 existe; lifecycle de selección para dashboard en I2).
6. **SLOs operacionales**: la medición de capacidad es de desarrollo (disposable local); SLOs de producción requieren ventana compartida autorizada.
7. **Engine efectivo**: GLM-5.3-Flash (host); discrepancia con GPT-6-Luna del encabezado registrada, sin atribuir trabajo a otro motor.

## NEXT

PRIMARY_MANAGER_FINAL_REVIEW. Revisión independiente del delta en contexto fresco ejecutada dentro de Shot 4 (ver sección correspondiente del planificador). Sin quinto shot; sin cierre de proyecto ni sesión salvo pedido del Owner.

## Fuentes

[[SHOT4_EXECUTION_PACKAGE]], [[SHOT3_ADVERSARIAL_REPORT]], [[SHOT3_COVERAGE_MATRIX]], [[0 — Submanager State]], `xKoRx/echo@feature/lab-v4-shot4` (61ac1f72..fa24546f), paquete de repros `outputs/SHOT3_AUDIT_EVIDENCE/`.
