---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Product Contract — The Lab]]"
  - "[[B — Architecture Decision Report]]"
  - "[[D — Revised Roadmap]]"
tags: [kind/doc, area/echo]
created: "2026-09-22"
updated: "2026-10-26"
---
# F — Decision Register — owner clarifications and D1 decisions

## Propósito

Conservar decisiones ratificadas, su precedencia y gates técnicos de The Lab dentro de Echo. Distinguir autoridad producto vigente de evidencia y contratos históricos.

## Contenido

## Ingestion V2 — Mandato Owner 2026-10-26 (autoridad vigente)

El programa The Lab V4 anterior permanece cerrado con excepciones. Nuevo workstream dentro del mismo proyecto Echo en 10-projects/Echo/Ingestion V2 — Operational Integration/. No reabre Shot4 ni crea otro producto. SPEC [[B — Frozen Architecture]]; baseline/merge [[A — Source Baseline and Branch Integration]]; plan/gates [[C — Implementation Shots and Acceptance Gates]]; prompts [[D — GLM Handoff Packages]].

### D25 — Base The Lab e integración temprana (OWNER_RATIFIED)

**Precedencia explícita sobre D24:** nueva rama propuesta feature/lab-v4-ingestion-v2 DEBE salir del HEAD remoto refrescado de lab-v4/shot4-integration, verificado b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce. Verificar nombre/ownership. Prohibido originarla desde master, feature/ef-runtime-pools, feature/lab-v4-shot4 o backtester. Runtime feature/ef-runtime-pools@0e17c4d3f1179cde709f923c8dd28e8cd853afc9 es referencia de incompatibilidades/ownership, NO base ni destino autorizado. Divergencia125/64 y migración081 distinta requieren conciliación futura separada, sin merges/rebases/resets/cherry-picks ciegos.

Primer incremento Shot2: endpoint V2 persistente. Apenas obtiene **ECHO_INGESTION_V2_ENDPOINT_INTEGRATION_PASS** (C1), integrar inmediatamente sólo commits/migraciones completos de ese incremento en lab-v4/shot4-integration, antes de provisioning/reference/copy/analytics/UI o fin de Shot2. Gate exige router real, PG/artifacts de harness, readback independiente, replay/conflictos/rollback/restart/migraciones/regresiones y cero efectos externos; no readiness/copy/curvas finalizadas. Si baseline ya satisface gate mediante prueba efectiva, no fabricar delta/merge. Registrar SHAs y RESUME_BASE_SHA; continuar desde base sincronizada. Push normal, preservar commits ajenos, ningún force-push.

D25 sustituye cláusulas D24 de rama evolutiva única y resolución sobre runtime. **No sustituye** prohibición de interrumpir extracción/migrar legacy ni autoriza integración posterior a runtime, deploy o cutover. D24 queda abajo como historia, no ejecutar partes incompatibles.

### D26 — Cuatro shots y QA GLM independiente (OWNER_RATIFIED)

| Shot | Modelo/rol obligatorio | Límite |
|---|---|---|
|1 | GOD diseño/source forensics/contratos/freeze | Sólo diseño/persistencia, sin implementación ni QA ejecutado |
|2 | GLM-5.3-Flash Max LOCAL | Implementación/validación funcional/early merge endpoint |
|3 | GLM-5.3-Flash Max LOCAL independiente | Sesión fresca sin autoría implementación; adversarial/E2E/findings |
|4 | GLM-5.3-Flash Max LOCAL | Fixes/regresiones y otra instancia independiente verificando SHA final dentro del mismo shot |

Sustituye en D23 el reparto GOD/Luna/Sol para QA y cualquier GLM-5.3 normal en ejecución. No GOD review por defecto, Shot5 ni subshots indefinidos. Early merge es hito interno Shot2. Persistir diseño no inicia shots posteriores. Independencia final no se simula con auto-revisión.

D09/D10/D11/D16–D22 conservan autoridad compatible: una identidad/ingesta/journal, observación separada de ejecución, economía honesta,4curvas/2rankings V4, cero features especulativas. H01–H49 son49; QA01 separado. H45/QA01/AUTH_FORGE e installer nil conservan atribución: installer nil es delta implementable, no permiso para READY ficticio.

### D27 — Resoluciones del freeze (TECHNICAL_RESOLUTION)

| ID | Resolución | Evidencia | Shot consumidor |
|---|---|---|---|
|IV2-01 | Reusar Gateway/SDK/registry/history/store; corregir validación/digests/artifacts/metadata CAS | A G01–G05; B2–B4 |2 E; QA3/4 |
|IV2-02 | Profile config existente, binding CAS/snapshot; installer real/ACK fenced/lease/lookup | A G06–G08; B5/B6 |2 O; QA3/4 |
|IV2-03 | Source/cycle exactos, un journal owner, no Signal nativa externa; dispatch durable/gates último envío | A G09–G11; B7/B8 |2 J; QA3/4 |
|IV2-04 | Projector asíncrono scoped, N+1 acumulativo/delivered selectivo; LAB sin matemática nueva | A G12–G14; B9 |2 L; QA3/4 |
|IV2-05 | Adapter Forge durable/receipt verificado; AUTH externo separado | A G15/G16; B10 |2 F; QA3/4 |

Sin decisión de producto abierta. Contratos y alternativas descartadas sólo en B; este registro guarda autoridad/trazabilidad.

## V4 — Decisiones Owner 2026-10-22: autoridad compatible; D23/D24 parcialmente sustituidas

**Estado:** OWNER_RATIFIED para requisitos/producto. **No equivale a implementación ni certificación**. Esta sección complementa D09/D10/D11/D16; sustituye interpretaciones anteriores que daban por terminada una integración Forge limitada a ingesta analítica. El siguiente ciclo de cierre tiene **exactamente 4 shots** (diseño, implementación, auditoría adversarial, correcciones); no es permiso para continuar indefinidamente el Shot 4 anterior.

### D17 — Forge canonical ingest → Echo operacional → LAB (OWNER_RATIFIED)

Una estrategia enviada por Forge mediante el **contrato canónico Echo** debe: (1) registrar identidad Strategy/StrategyVersion inmutable y una o varias historias históricas con operaciones, revisiones y provenance; (2) quedar **registrada y habilitable operativamente en Echo** mediante la integración real con `echo.strategy_definitions` y las rutas de señales/políticas/identidades correspondientes; (3) permitir que una señal de cuenta master entrante incluso **un minuto después de la recepción** sea correlacionada a la misma estrategia/version, ingresada en `echo.trade_journal` por su ruta canónica y proyectada como historia Echo/REFERENCE junto a la historia importada de Forge en una **vista continua con selección temporal**, sin mutar ni sumar dos veces las historias; (4) producir curvas, métricas y scores automáticos. Distinguir `INGEST_ACCEPTED`, `ANALYTICS_PENDING` y `ECHO_OPERATIONAL_READY`; una aceptación analítica NO implica preparación operacional. Si faltan políticas de cuenta, mappings, permisos, data o habilitación operativa, respuesta de readiness explícita con motivos; **no ejecutar trading real sin las autorizaciones operacionales aplicables**. Idempotencia/replay, reconciliación, fallo parcial, retry y condición de carrera señal-inmediata son requisitos de aceptación.

Forge puede configurar su propia estrategia en su dominio inmediatamente usando las identidades/receipts devueltos por Echo. Echo NO debe conocer las tablas, clases ni formato interno de Forge; el cliente Forge conoce, valida y traduce al `strategy-ingestion.v2` (versión compatible/aditiva si hace falta). No acoplar provisioning a cálculo de curvas ni obligar al runtime a esperar el worker analítico.

### D18 — Frontera de fuentes y niveles históricos (OWNER_RATIFIED)

La historia normal es la evidencia económica fuente (USD cuando el productor la declara USD; no inferir USD en otras divisas). `History` y revisiones contienen evidencia exacta y cobertura. `Operation` conserva ciclo lógico, movimientos, cuenta, run/rol y enlaces a orders/fills cuando existen; `CLOSED_SUMMARY` es legítimo para legado, no una simulación de fills. Forge aporta histórico antes de Echo; Echo aporta una historia nueva de ejecución/reference desde la operación real. Selección de historia y segmentos previenen solapes/look-ahead, conservan todas las alternativas y distinguen `construction_at`, cutoff, `available_at`, inicio Echo y conocimiento efectivo. Se exige trazabilidad Forge→estrategia habilitada→señal master→journal→proyección LAB→vista histórica.

### D19 — Curvas y scoring son subsistemas independientes (OWNER_RATIFIED)

Cada curva es un **derivado versionado de la historia económica**, no otra fuente ni un algoritmo de ranking. Registro/factory pequeño de implementaciones Go con `profile_id/algorithm_version/config_digest`, requisitos y producción automática para todas las historias elegibles al registrar perfil o actualizar historia. Inicialmente preservar perfiles V4 existentes: `recorded_money.v1`, `r_net_cumulative.v1`, `normalized_10k_open_balance.v1`, `normalized_10k_initial_balance.v1`; visualización inicial prioriza R y 10k, con dinero registrado como fuente. Los puntos/operaciones/movimientos asociados a cada curva conservan el mismo input y pueden consultarse por revisión/fecha. No clonar historia, duplicar costos o falsear Q_i para un perfil insuficiente.

Cada ranking es otra familia de derivados: `ranking_algorithm_id`, versión, configuración sellada, **input_curve_profile_id propio**, ventana/cohorte y un score por estrategia/algoritmo/contexto/revisión con status, explicación/componentes y provenance. **Selector de curva de UI independiente del selector de ranking**: las columnas reflejan la curva visible; el score refleja el algoritmo elegido, aunque se calcule sobre otra curva. Ordenar por score y por columnas, filtros server-side y Hasura (roles/metadata aditiva). Un nuevo algoritmo registrado una vez se aplica automáticamente a todas las estrategias elegibles y se recalcula ante cambios, sin copias de implementación por estrategia.

### D20 — Dos rankings iniciales, motor compartido Forge/Echo (OWNER_RATIFIED)

Usar una **única implementación pura y reutilizable Go** de combinación ponderada con normalización Min-Max y versionado, basada en el ranker REAL de Forge (`xKoRx/symphony/sqx/core/domain/ranking_snapshot_per_type.go`, `weighted_combination_minmax.v1`) y adaptada a métricas de curvas V4. No copiar código en dos lugares; comparar snapshots/golden tests de la implementación Forge y la compartida para garantizar paridad sin acoplar Echo a internals de Forge.

Presets iniciales (dos algoritmos configurados sobre un mismo motor):
1. `edge_duo.v1` / **Edge Dúo**, entradas Ret/DD 50% y Profit Factor 50%. Perfil económico base definido y fijado por contrato del algoritmo, nunca por el selector UI.
2. `forge_quality_four.v1` / **Forge Calidad 4**, Ret/DD 31.25%, Profit Factor 25%, Sharpe 25%, SQN 18.75% (renormalización 5:4:4:3 de los cuatro componentes similares al `risk_adjusted_delta.v1` de Forge; aquel es **comparador de dos curvas** y no debe usarse como score absoluto sin transformación explícita).

Ret/DD/PF/Sharpe/SQN exigen **definiciones, unidades, perfil, calendario, window, mínimo de muestra, política de extremos/undefined y tratamiento de costes declarados y versionados**. Sharpe requiere retornos periódicos y base temporal; SQN requiere distribución por operaciones evaluables bajo regla explícita; no copiar números SQX sin equivalencia de definiciones. Si falta métrica obligatoria, score `INSUFFICIENT_DATA/NOT_COMPARABLE`, nunca cero favorable o renormalización silenciosa de los pesos.

**Advertencia estructural:** Min-Max depende del conjunto elegible. Cambiar una estrategia puede cambiar scores del resto: fijar identidad de **cohorte/snapshot de métricas** y recalcular/publicar rankings completos del grupo afectado con consistencia y desempate determinista. Un score absoluto por estrategia sin cohorte NO es comparable entre universos distintos.

### D21 — Experiencia V4 prioritaria (OWNER_RATIFIED)

La entrada a LAB es un **screener de estrategias reales** (no fixtures ni consola de portfolios/backtest). Selectores independientes `ranking` y `curve`, grilla con métricas de curva seleccionada y score/rank del ranking elegido, filtros y orden server-side con Hasura. Click abre detalle: perfiles R/dinero/10k, métricas correspondientes y score por algoritmo, curva de capital/resultado con su historia exacta, timeline de operaciones parciales/terminales, calendario diario de PnL/resultado bajo la curva y fuente seleccionadas, períodos pre/post/Forge/Echo, identidades y cobertura. Los datos de una generación deben ser coherentes, no mezclar curva N con operaciones de N+1. Fuentes reales de Echo y Forge; sin scores ni trades ficticios.

### D22 — Portfolios dinámicos: cero trabajo funcional ahora (OWNER_RATIFIED)

**NO implementar ni diseñar ahora** scheduler, selector Top N automático, rebalanceo, simulador causal, membresías mutables ni infraestructura de portfolios. Objetivo **solo** que la identidad de versiones, revisiones/snapshots, disponibilidad temporal, provenance, curva y scores sean extensibles mediante tablas/servicios **aditivos** cuando I2 se aborde. Si un bloqueo estructural real en lo que se implementa HOY impediría esa extensión, repararlo mínimamente como parte de Forge/LAB; no abrir trabajo de I2 ni gastar tiempo en él.

### D23 — Programa único de cierre: SOLO CUATRO SHOTS (histórico; reparto sustituido por D26)

**Shot 1:** GOD LOCAL submanager de DISEÑO detallado, coordina Luna/Sol en contexto fresco para investigación técnica y redacción; él decide contradicciones materiales y valida el paquete compacto, NO hace inspección/test masivos personalmente. Ratificar dentro del shot todos los detalles técnicos deducibles, sin devolver entrevistas generales al Owner.
**Shot 2:** GLM LOCAL implementa, integra Echo/Forge/LAB/Hasura en superficies autorizadas y valida con data auténtica aislada.
**Shot 3:** GOD LOCAL submanager de QA adversarial independiente, coordina Luna/Sol (independientes del implementador), valida findings/evidencia compacta; NO es el auditor ejecutor ni consume cuota en suites/logs/source completos.
**Shot 4:** GLM LOCAL corrige TODOS los findings y completa el alcance, con revisión independiente de los cambios finales DENTRO del mismo shot. **No Shot 5, subshots perpetuos ni freeze recurrentes.** Limitar GOD a despacho y validación crítica, evidencias compactas, sin fallback de ejecución premium.

Prioridad: activar correctamente estrategia Forge en Echo, enlazar master/trade_journal e historia LAB, curvas y **dos rankings**, screener/detalle reales y Hasura. No hacer rollout/trading/operaciones destructivas sin permisos específicos; pruebas con cuentas/datos autorizados en entornos aislados. Mantener AGENTS OS master, código por repo/rama autorizada; preservar no-interferencia con el runtime paralelo.

### D24 — Runtime es la única rama evolutiva; backtester legacy se migra después (histórico; rama sustituida por D25)

**Única autoridad de desarrollo del código Echo para el siguiente programa:** `xKoRx/echo`, rama `feature/ef-runtime-pools`. El modelo operacional y el motor evolucionaron en esta rama: Shot 1 debe inspeccionar su HEAD actual y diseñar todas las integraciones Echo/Forge/LAB sobre sus contratos y estructuras **vigentes**, sin tratar dos ramas como fuentes equivalentes ni mantener la rama de backtester como co-baseline. Último HEAD verificado en GitHub el 2026-10-22: `2ee61791deb3139be23e1c9be3708b1d41da8d6b` (referencia móvil; refrescar al ejecutar).

**Ramas históricas:** `feature/lab-v4-shot4`, las ramas previas de backtester y otros cortes antiguos son evidencia histórica, no objetivos de merge, rebase, cherry-pick ni fuentes normativas del modelo actual. Su documentación/resultados pueden orientar criterios ya aceptados, pero ninguna capacidad debe declararse integrada en el runtime por existir en una rama anterior. No exigir reconciliación de ramas legacy como hito; cualquier función nueva o equivalente se diseña/verifica **sobre la rama runtime** y conforme a su modelo, sin trasplantes automáticos.

**Secuencia de producto:** la extracción de estrategias en curso termina primero. **Sólo después**, en un trabajo futuro separado y autorizado por el Owner, se migrarán esas estrategias al nuevo motor runtime. El programa actual no migra backtester/estrategias heredadas, no interrumpe su extracción y no crea workflows de migración, adapters legacy ni compatibilidad especulativa. La integración canónica de Forge, readiness operacional (en entorno aislado), `trade_journal`, curvas, rankings y Hasura se resuelve sobre el runtime vigente sin activar ni migrar por anticipación las estrategias de la campaña actual.

**Precedencia:** D24 corrige expresamente cualquier instrucción anterior que ordene comparar, unir o reconciliar `feature/lab-v4-shot4` con `feature/ef-runtime-pools`, o integrar rutas de backtester obsoletas como requisito del programa. Se mantienen D09–D23 y los cuatro shots, pero se reinterpretan para ejecutar sobre **una única rama Echo**, sin añadir tiempo al backtester legacy.

**Referencias históricas anteriores a D24 (NO baselines para integración):** xKoRx/echo `feature/lab-v4-shot4@10a4eddd540de69370408c60a7a9c159b97e6a38`; xKoRx/echo `feature/ef-runtime-pools@960bf60ae0832570ca3b97aba0e7badea486bb00`; xKoRx/symphony `master@daded14cbe0bc85f6fafda8d079e94036f715b47` según último acceso; refrescar en Shot 1. El loader Echo REFERENCE es **parcial**, el endpoint V2 está verificado localmente, no lo suficiente para disponibilidad operacional/Forge E2E. G11 y seguridad dinámica aún no certificados. **Continuidad:** el siguiente manager debe arrancar en esta sección y el `SHOT4_HANDOFF` final, sin repetir los diseños V4 aprobados.

## V4 — Owner ratifications 2026-10-20 (current product authority)

**Project:** [[Echo — Producto Integrado]] / The LAB V4. **Design evidence:** [[THE_LAB_V4_Diseno_para_revision]] (Shot 1 GOD, 2026-10-20; source artifact preserved). **Authority:** Owner's explicit confirmation on 2026-10-20. These four decisions **supersede conflicting V3 specifications** below; prior ratifications remain historical evidence, not instructions to implement V3 over V4.

| ID | Status | Ratified decision | Required interpretation |
|---|---|---|---|
| D09 | **OWNER_RATIFIED** | Virtual initial capital **10,000** and **1%** risk preset, **configurable**. | `normalized_10k_open_balance.v1`: each operation's virtual risk budget is sealed at opening from the realized virtual balance causally known at that time; no future PnL for sizing. The 1% preset is **not** an operational Echo account/prop risk rule, nor an aggregate exposure cap. Explicitly version the separate initial-balance profile. |
| D10 | **OWNER_RATIFIED** | **Cycle's risk budget proven and sealed when the Operation opens** is the R denominator. | `Q_i > 0` must be source-supported, scoped to the **whole logical cycle**, including possible later adds. Do not infer it from the first entry SL, final SL, realized loss or contemporary MM config; if absent or unsuitable, R and risk-normalized curves are `INSUFFICIENT_DATA`. Do not silently recompute Q_i when exposure changes; any later breach or change in actual risk does not retroactively rewrite its initial normalization basis. |
| D11 | **OWNER_RATIFIED** | **Separate capital per portfolio member**, fixed initial weights, and **flat start**. | No shared financing, loans, margin simulation or implicit rebalance in I1. Initial capital apportioned by member weight; weight sum <= 1, remainder cash. Entries before `composition_start_at` do not earn in a newly flat-initialized portfolio. |
| D16 | **OWNER_RATIFIED** | **Real strategy-version construction date `construction_at`** determines the pre/post construction boundary. | Preserve `construction_data_cutoff` separately as evidence of the last training-data date; do not use it as a substitute for `construction_at`. Preserve `available_at` and `echo_reference_started_at` as distinct time dimensions; never infer unknown timestamps from receipt/import date. |

### V4 authority and conflicts with V3

- **V3 P02/P04 / Echo Integrated Product old "A" boundary**: its cutoff at end of training dataset was the V3 period classifier. **SUPERSEDED for V4 classification** by D16. Training cutoff remains metadata, not the boundary.
- **V3 D1-M01/M07/M08/M09**: one closed trade = one row, no partial fills/OPEN cycles and mandatory TP were V3-scoped constraints. **SUPERSEDED as V4 schema restrictions**. The new model accepts multi-order/partial-fill/movement evidence, open/terminal cycles and different granularity. A CLOSED_SUMMARY remains valid when detailed evidence is absent, but is never added again to its movements.
- **V3 D1-M04/M11**: Echo owns canonical history/identity; Forge supplies a normalized input without writing directly to Echo PG. **RETAIN compatible authority boundary**; V4 extends it to multiple histories, origins and contexts.
- **D09 + D10**: the virtual 1% budget and the Operation's historical `Q_i` have different purposes. The former sizes an *analytical normalized curve*, the latter normalizes the actual cycle's result. Neither authorizes trading or silently enforces prop risk.
- **D11**: static portfolio is retrospective analysis, **not** causal portfolio-selection backtesting, shared capital simulation or live allocation.

### Gate técnico vigente — Runtime Integration, 2026-10-22

`SHOT1_DESIGN_COMPLETE / SHOT2_IMPLEMENTATION_READY` por GOD para THE_LAB_V4_RUNTIME_FORGE_INTEGRATION. [[0 — Shot 1 Gate and Baseline]] fija evidencia runtime y adjudicaciones; [[J — Shot 2 Implementation Package]] es entrada de GLM Shot2. No es nueva ratificación Owner ni altera D09/D10/D11/D16/D17–D24. Las condiciones técnicas de 2026-10-20 siguientes y el freeze V3 aceptado son antecedentes resueltos o requisitos compatibles; no otro gate previo pendiente. Diseño completo no equivale a implementación/E2E/deploy certificado, y no autoriza recursos compartidos.

### Manager review / freeze gate — histórico 2026-10-20, sustituido para diseño vigente

- `OWNER_PRODUCT_DECISIONS_D09_D10_D11_D16 = FROZEN` as of 2026-10-20.
- `SHOT1_DESIGN = REVIEWED_WITH_CONDITIONS`; **not** `FROZEN` or `READY_FOR_UNRESTRICTED_IMPLEMENTATION` yet. The Shot 1 source explicitly requires resolution/verification of G.2 technical facts before freezing an implementation-ready contract.
- `D12–D15 = MANAGER_TECHNICAL_DIRECTION_ACCEPTED_FOR_PREFLIGHT`, **not Owner ratifications nor final technical freeze**: PostgreSQL+bounded worker; versioned API/CAS; input-retention and exact revision manifests; explicit-evidence copy comparisons.
- `TECHNICAL_PREFLIGHT_OPEN = U01–U06 + A01/A02`: emitted strategy-version/MM/risk lineage; complete historical retention/rebuild; real history size and delivery shape; numeric SLOs/hardware; consumers of generic naming and migration constraints; real deployment/test posture, source artefact preservation.
- **Gate:** request bounded LOCAL preflight and record evidence plus revised complete SPEC; manager/Owner accept scope and technical freeze before editing dependent production code. No new Owner product interview is required unless a verified material contradiction arises.
- **Source-of-truth status:** original V4 design artifact is kept unchanged as proposed design; this decision register is the ratified Owner delta. Do not mistake the source artifact's `READY_FOR_OWNER_REVIEW` label for freeze approval.

---

## CLOSED — producto confirmado por Rodrigo el 22-09
| ID | Decisión | Alcance |
|---|---|---|
| P01 | The Lab V3 será sección Echo; base única durable de operaciones y N curvas derivadas + métricas/dashboard/screener; luego money management/portfolios | Ratificado; precisión de ownership en D1-M04 |
| P02 | Tres periodos EXACTOS: TRAINING_DATA SQX, PRE_REAL MT5, REAL Echo Reference; DOS fechas configurables en importación Forge→Echo | Ratificado |
| P03 | Clasificar pertenencia exclusivamente por `opened_at` probado. Cierre posiciona realización del resultado, nunca pertenencia | Ratificado; resuelve contradicción A vs D/E/F anterior |
| P04 | Fecha A es última fecha usada por dataset de entrenamiento Forge, NO selección/promotion; si es día civil, include día y convertir al primer instante posterior | Ratificado semánticamente; precisión/timezone en SPEC diaria |
| P05 | Forge inserta/entrega operaciones SQX+MT5 como base histórica; Echo normaliza/persiste/calcula; journal es autoridad FULL ECHO, solo leído por Lab | Ratificado; D1-M04 precisa ingestión como recurso Echo, sin API de escritura Lab |
| P06 | Histórica una sola base oficial; reimport manual destruye/reemplaza dataset analítico tras validación atómica, sin conservar cadena permanente de HistoryRevision/Publication. No borrar originales Forge ni journal | Ratificado; D1-M04 precisa ownership de la base en Echo |
| P07 | Preferencia modelo minimalista canonical operations + curves. TradeSet/HistoryRevision/HistoryPublication NO nuevos objetos de producto obligatorios; evitar dos autoridades persistentes | Ratificado como arquitectura conceptual; D1-M04 desplaza operaciones a Echo y E05 deja de gobernar el nuevo modelo |
| P08 | No BWC ni paridad V1/V2 como razón para conservar legacy; cleanup incluye tablas, código, jobs, vistas y front; journal/runtime intocables | Ratificado |
| P09 | Jornada 23–27: planificación técnica profunda al empezar cada día, luego desarrollo/pruebas/corrección a gate; dashboard auténtico viernes, REAL job sábado, screener E2E domingo | Ratificado como objetivos; no garantías de certificación |
| P10 | N algoritmos Go para curvas y bases R_PIPS/R_MONEY/pips/money según evidencia; detalles de algoritmos a iterar. Riesgo sizing separado de señal entry/SL/TP; candle/intrabar futuro | Ratificado |
| P11 | Uso futuro: money management múltiple, portfolios research y ejecución/asignaciones, dashboard y limpieza legacy explícita en roadmap general | Ratificado |

## CLOSED — decisiones owner D1 23-09, entrevista modelo
| ID | Decisión ratificada | Consecuencia obligatoria |
|---|---|---|
| D1-M01 | Una fila por trade completo (alternativa A), no una fila por deal ni realización parcial | Diseñar identidad de trade estable; si la fuente ofrece deals, agregarlos sólo con evidencia completa y sin PnL duplicado. Política exacta de cierres parciales aún es detalle técnico de SPEC, no licencia para inventarlos. |
| D1-M02 | Dos estrategias distintas son dos historias distintas. En REAL procesar exclusivamente trades REFERENCE; operaciones de cuentas/copy EXECUTION quedan fuera de D1–D4 y servirán después para slippage/fidelidad | Sin merge entre cuentas/copies ni inferir estrategia por cambio de cuenta; identidad StrategyVersion explícita. |
| D1-M03 | Ingesta estricta: trade con error o campos requeridos ausentes falla; no aceptar operaciones degradadas para fabricar curvas. Header de curva debe tener estado ante error | Definir conjunto mínimo de campos efectivamente requeridos según uso. No exigir ni crear columnas especulativas; fuentes incompletas no obtienen PASS; curvas no se calculan sobre input inválido. |
| D1-M04 | Operaciones canónicas y estrategia/historia pertenecen a Echo; The Lab es subproducto consumidor con ownership exclusivo de curvas/derivados | Forge inyecta estrategia con historia mediante servicio Echo, jamás escribe Lab ni PostgreSQL directamente. El nombre lógico `lab_operations` de A/B/D anteriores queda SUPERSEDED: proponer `echo.canonical_operations` o equivalente en SPEC. Una sola autoridad durable de operaciones, no segunda escritura E05 TradeSet. Echo journal continúa autoridad operacional y fuente de Reference. |
| D1-M05 | Modelo canónico S0 debe modificarse/definirse completo desde necesidades de todos los productores (Forge, journal y futuros), sin diseñar alrededor de E05 actual | E05 no gobierna modelo V3 ni se conserva por obligación; preservar sólo datos y consumidores realmente necesarios mientras se hace convergencia segura. S0 se extiende o sustituye versionadamente según contrato aprobado. |
| D1-M06 | KISS: columnas y tablas sólo para atributos realmente usados; provenance/trazabilidad/calidad no son subsistemas por defecto. Modelo consultado y actualizado con frecuencia y volumen creciente | Evitar JSONB como almacenamiento central de campos consultables, evitar tablas de import/calidad/revisiones sin necesidad demostrada; DDL e índices se ratifican en la SPEC. |
| D1-M07 | La base canónica persiste sólo trades CERRADOS (alternativa A). No se almacenan operaciones abiertas en canonical_operations | El worker REAL incorpora Reference sólo después del cierre. No hace falta state/lifecycle en la fila canónica D1. |
| D1-M08 | Cierres parciales no forman parte del modelo V3 inicial (alternativa A): 1 operación = 1 cierre = 1 trade = 1 row | Si una fuente representa un trade mediante más de una realización/fila y no puede producir inequívocamente un único trade cerrado, el ingreso falla. No se agrega tabla de deals ni legs. Curvas no deben calcularse sobre ese input; su header debe reflejar ERROR/INVALID_INPUT. TP y SL forman parte obligatoria del trade canónico. |
| D1-M09 | En V3 inicial `take_profit` es obligatorio aunque el dominio futuro pueda admitir estrategias sin TP | `take_profit NOT NULL` en el contrato/DDL inicial. Si más adelante se habilitan estrategias legítimas sin TP, se versiona el contrato; NULL no se usa como sinónimo de dato faltante. Nota técnica: el cálculo de R depende del riesgo inicial/SL y del resultado realizado, no matemáticamente del TP; TP se conserva porque es parte de la señal y del contrato actual de estrategia. |
| D1-M10 | Echo conoce sólo símbolos canónicos; canonical_operations y Lab heredan esa autoridad | El flujo de ingestión debe resolver/solicitar el símbolo canónico al inicio y persistir sólo ese identificador. No se guardan aliases/broker symbols en canonical_operations ni se crea instrument mapping dentro de Lab. Un símbolo no canónico/no resoluble falla antes de persistir trades. |
| D1-M11 | Forge adapta sus fuentes al contrato canónico de Echo; Echo valida y persiste. Echo NO conoce formatos SQX/MT5 | El SDK/contrato compartido expone el DTO de operación/historia requerido por Echo. Cada productor resuelve internamente cómo obtenerlo. No entran parsers SQX/MT5 al dominio Echo. |
| D1-M12 | D1 es Echo-first. Forge continúa por carril de desarrollo independiente y consume las definiciones publicadas por Echo | El gate D1 no depende de inspeccionar ni corregir implementación Forge. Echo entrega modelo base, contrato, servicio de integración, persistencia y tests de contrato. La certificación física Forge→Echo ocurre al converger ambos carriles, sin trasladar deuda Forge a Echo. |

**Estado de la sesión:** M01–M12 ratificadas y registradas. NO constituyen aprobación del DDL, contrato wire completo, implementación, pruebas o gate D1. La entrevista del modelo sigue abierta. El contenido previo de A/B/D/E que sitúe `lab_operations` bajo Lab o haga de E05 prioridad de reutilización queda superado por D1-M04/M05; actualizar esos documentos al concluir planificación aprobada, no presentarlos como autoridad vigente sobre ownership.

## TECH — concretar en SPEC diaria, no bloquear roadmap completo
| ID | Decisión pendiente puntual | Fecha/hito responsable |
|---|---|---|
| T01 | DDL de `echo.canonical_operations` (nombre sujeto a SPEC), PK/unique, metadata A/B y vínculo a StrategyVersion, tipos mínimos, reemplazo atómico, tratamiento de correcciones journal, disposición de PG063/consumidores E10 sin dual-write; no crear import/quality tables por inercia | D1 23/09 |
| T02 | Input A/B exacto, timezone y evidencia UTC; campos realmente requeridos para trade COMPLETO y curvas previstas; cierres parciales que origen entregue, cruces y comportamiento fail-closed | D1/D2 |
| T03 | Contrato público Echo para historia TRAINING/PRE_REAL: DTO, A/B, counts/digest de dataset, idempotencia/reemplazo y estados de respuesta. Forge implementa su productor en carril independiente; evidencia física SQX/MT5 se exige en el gate de integración, no para cerrar foundation Echo | D1 contrato / D2 integración |
| T04 | Header de curva con estado de error, CurveAlgorithm descriptor/basis, puntos, fingerprint, invalidación y primeras fórmulas demostrables | D3; estado obligatorio D1-M03 |
| T05 | Journal READ ONLY, Reference/version, watermark/correcciones/timer/freshness, sin copies ni mutation | D4 |
| T06 | Screener: misma basis/currency/ventana/fórmula; DQ de conjuntos; gate final E2E y mapa consumidores legacy | D5 |
| T07 | Destrucción legacy: clasificar objetos LAB_ONLY, SHARED, UNKNOWN, DROP autorizado tras V3 usable; no tocar journal/Core | Inventario D1–D5; ejecución L-CLEAN post D5 |

## Evidencia que aún NO está certificada
- La conformidad física de Forge con el nuevo contrato Echo (TRAINING/PRE_REAL auténticos) aún no está certificada. Es riesgo de integración, no bloqueo para diseñar/implementar la foundation Echo.
- No hay nuevo DDL, job V3, curva V3 ni UI V3 implementados o probados por esta sesión.
- E05 PG063 y consumidores E10 deben localizarse antes de retirar datos que pudieran ser su única copia, pero no tienen derecho de veto arquitectónico ni se mantienen como segunda autoridad.
- Branches locales/worktrees y operaciones físicas del candidato aún no verificados.

## Gate
Planificación D1 en curso, decisiones M01–M12 cerradas. `D1_PASS` exige SPEC/contrato Echo aprobados, migración DEV, servicio de ingestión Echo, persistencia/readback mediante tests de contrato y ausencia de impacto trading. La operación auténtica Forge queda para el gate de integración D2; no se usa un productor incompleto para deformar el modelo Echo. Ninguna actividad de código, migración, PROD o trading autorizada durante la entrevista. No cerrar sesión Agents-OS antes del cierre explícito solicitado al terminar planificación aprobada. Roadmap operativo [[D — Revised Roadmap]] sujeto a las precisiones D1 ratificadas.
