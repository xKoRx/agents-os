# Applications — Bitácora (Resource Wiki)

Append-only, cronológico. Prefijo: `## [YYYY-MM-DD] <op> | <detalle>` con `<op>` ∈ `ingest | query | lint`. Últimas ops: `grep "^## \[" log.md | tail -5`.

## [2026-07-02] ingest | Bootstrap del índice — piloto Resource Wiki
- Creado `00-index.md` con las 11 apps existentes (echo-forge + 10 de Meli/VIS).
- Resúmenes de una línea derivados de la sección "Descripción" real de cada página. Cero contenido inventado.
- No se tocó ninguna página canónica de app.
- Flagueado `commons-middleend` como concepto sin página (candidato a ingest futuro).
- Pendiente: correr `resource-wiki-lint-reindex` una vez Graphify quede depurado (trash/json/outputs fuera del corpus).

## [2026-07-03] ingest | Echo Core + changelog
- Ingestadas `echo-core` y `echo-core-changelog` → índice pasa a 12 apps.
- Fila y "una línea" agregadas al catálogo; `updated` del índice = 2026-07-03.
- Entrada de log backfilleada 2026-07-04 durante la higienización (el ingest quedó sin log en su momento).

## [2026-07-17] ingest | vis-credits-consumer
- Creada [[vis-credits-consumer]] desde el repositorio local `~/fuentes/vis-credits-consumer`.
- Verificado el flujo `item-financeable`: consulta Segments Wrapper y actualiza `IS_FINANCEABLE`, `FINANCEABLE_BY` y `IS_FINANCEABLE_VEHICLE_RISK_PROFILE` para `MLB-CARS_AND_VANS`.
- Relacionada con [[vis-items-loader-tagging]], que publica el ítem al flujo de Credits para el caso B2C.

## [2026-08-08] ingest | Stager application
- Creada [[stager-app]] desde el template vigente para el repo/módulo independiente `github.com/xKoRx/stager`.
- Relacionada con [[Stager]], [[Echo Forge]], [[echo-forge]] y la decisión arquitectónica del MVP.
- Índice reconciliado a 17 applications reales; se agregaron también las filas antiguas omitidas de [[vis-credits-segment-wrapper]] y [[vis-sdk-go]].

## [2026-08-10] ingest | Aplicaciones RIO
- Creadas las aplicaciones [[rio-playmaker]], [[rio-controlplane-clickhouse]], [[rio-controlplane-fury]], [[rio-controlplane-flink]], [[rio-controlplane-kafka]], [[rio-controlplane-signals]], [[rio-controlplane-kms]], [[rio-controlplane-observability]], [[rio-sdk-events]] y [[rio-materializer]] desde `70-templates/application.md`.
- Los nombres canónicos y checkouts locales usan el prefijo solicitado `rio-*`; cada nota conserva el remote real solo como referencia de procedencia.
- El índice queda reconciliado a 27 aplicaciones reales.

## [2026-08-10] ingest | Deep-dive LLM Wiki de las 10 apps RIO (desde código)
- Reescritas las 10 páginas rio-* con el corte estable/volátil (responsabilidad vs implementación con `last_verified`), evidencia leída del código real (README/build/graph/src) y provenance por repo+path. Consolidación de 10 subagentes en paralelo.
- Deps corregidas contra código: [[rio-controlplane-clickhouse]] depende de [[rio-materializer]] (no de playmaker); [[rio-controlplane-kafka]] reemplaza comportamiento legacy de [[rio-materializer]]; [[rio-playmaker]] orquesta control planes vía BigQueue.
- `lang` corregido: [[rio-controlplane-fury]] es **Kotlin** (no Java).
- Contradicciones doc↔código anotadas: [[rio-controlplane-signals]] sigue en scaffold inicial (`.fury` = `template-java-graddle-web`, sin dominio Signals) → `confidence: medium`; [[rio-sdk-events]] documenta "2 dominios" pero el código ya tiene `actions/`, `state/`, `discovery/` → `confidence: medium`; varios README en scaffold con versiones distintas al `build.gradle` (playmaker, observability, kms).
- Convención estable/volátil promovida a Sistema 1 (templates `application.md`/`service.md` + `00-RESOURCE-WIKI.md`).

## [2026-08-10] ingest | Corrección de nombres RIO/Signals
- Aclarado (por el usuario, del equipo): **RIO = Real time Input Output**; **Signals es el otro nombre de RIO** (equipo Signals = equipo RIO = equipo ADS), no un sub-dominio. El dominio del equipo Signals son las 10 apps RIO.
- Corregidas [[RIO]] (aliases + nota de nombres) y [[rio-controlplane-signals]]: verificado en disco que es un **scaffold Fury vacío** (`.fury` = `template-java-graddle-web`, "Initial commit"), placeholder sin propósito ni relaciones reales; se removió el framing erróneo de "control plane del dominio Signals" y las deps especulativas.

## [2026-08-11] ingest | Frontends y catálogo Signals ADS
- Se incorporaron [[ads-signals-frontend]], [[rio-frontend]] y [[ads-signals-catalog]]; el índice quedó reconciliado a 16 aplicaciones vigentes y enlaza también el servicio [[RIO]] y [[echo-core-changelog]].

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4
- Cobertura del índice completa tras incorporar los dos artefactos auxiliares; lifecycle `deprecating` validado por contrato; Graphify limpio y actualizado.

## [2026-09-06] ingest | Source Echo + Echo Forge → auditoría maestra de producto 2026

- Creado [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] como Resource canónico autocontenido, con dos notas source y entrada de catálogo. Source remoto contrastado, decisiones frozen preservadas, segunda pasada adversarial integrada; no implementación ni production writes.
- Evidencia física previa explícitamente fechada/reportada; producción actual no recertificada. Checkout Echo habitual stale frente a master remoto; el master Resource usa 04c16bd.
- Trazabilidad y validación: [[2026-09-06-echo-forge-auditoria-producto-2026]].

## [2026-09-06] ingest | Revisión independiente Echo + Forge

[[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]] → [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] y correcciones materiales de [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]]. Triage y roadmap por uso; V3 takeover/B1; evidencia productiva read-only y forward recuperable sin certificación inventada. Catálogo actualizado. Change log [[2026-09-06-echo-forge-independent-reality-review]].

## [2026-09-06] ingest | Forge → Echo boundary y live authority

Creado [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]; enlazado desde master, companion y ambas fuentes. Errata material de B1/B2 source y Temporal declared/resolved; secuencia version-seal corregida. Nuevas decisiones siguen I con O1–O3, no freeze owner ni implementación. Lint dirigido y closure registrados en [[2026-09-06-echo-forge-live-authority-contract]].

## [2026-09-07] ingest | Revisión de durabilidad arquitectónica Echo + Forge (Fable 5.1)

Creado [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]]; enlazado desde master, Independent Reality Check y contrato Live Authority. Decisión B: grafo ratificado, siete correcciones acotadas, O1/O3 default técnico, O2 sólo catálogo CC, ningún TOP. Hallazgo S nuevo: `CanonicalStrategyID` lee `HOST_KEY`. Change log [[2026-09-07-echo-forge-architecture-durability-review]].


## [2026-09-07] ingest | Echo SDK canonical integration and analytics contract V1

[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]: 22 outputs, 36 casos golden definidos, B con correcciones acotadas, SDK Echo como autoridad y ningún TOP. Preparados [[Echo Forge — Factory V2 Completion]] y [[Echo — Live Platform V1]]; supersession puntual de SDK externo/unknown-field rejection y precisión R/HOST_KEY. Change log [[2026-09-07-echo-sdk-canonical-contract-close]]. Índice Markdown actualizado; Graphify externo no se modifica por restricción owner read-only fuera del vault. Validación dirigida registrada en cierre.

## [2026-09-07] ingest | Freeze review final del contrato Echo SDK (Fable 5.1)

Creado [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]; enlazado desde el contrato Astra, la revisión de durabilidad Fable y ambos proyectos. Decisión B: cinco correcciones FR-1…FR-5 incorporables en S0, ningún TOP. Hallazgo S: `HashIdentity` vigente en Forge es newline-join, distinto del `H()` JSON array del contrato; refs S de MetricSet/TradeSet ya derivan identidad de inputs, no de payload. Change log [[2026-09-07-echo-sdk-contract-freeze-review]]. Graphify externo no se refresca (read-only fuera del vault).

## [2026-09-07] ingest | Echo Forge F-01 Canonical generation concurrency contract

Creado [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] y subproyecto [[Echo Forge — F-01 Canonical generation concurrency]] hijo de [[Echo Forge — Factory V2 Completion]]. Change log [[2026-09-07-echo-forge-f01-canonical-generation-concurrency-spec]]. Graphify externo no se refresca.

## [2026-09-07] ingest | Echo Forge F-01 correction — ExecutionIntentKey discriminator

Corrección in-place de [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] e hijo [[Echo Forge — F-01 Canonical generation concurrency]]: logical producer = Builder StageExecution; discriminator = `ExecutionIntentKey`; `OutputNamespaceOwnership` insuficiente (T7). Change log [[2026-09-07-echo-forge-f01-canonical-generation-concurrency-correction]]. Graphify externo no se refresca.

## [2026-09-07] ingest | Echo Forge F-01 correction 02 — filename budget

Corrección in-place: published GENERATED compacto 91 chars (`Base64URL` EIK + stem); Campaign `FilenameToken` no se proyecta en nombres nuevos. Change log [[2026-09-07-echo-forge-f01-filename-budget-correction]]. Graphify externo no se refresca.

## [2026-09-08] ingest | Echo Forge F-02 Finalist Model V2 contract

Creado [[Echo Forge — F-02 Finalist Model V2 Contract]] y subproyecto [[Echo Forge — F-02 Finalist Model V2]] hijo de [[Echo Forge — Factory V2 Completion]]. Change log [[2026-09-08-echo-forge-f02-finalist-model-v2-spec]]. Graphify externo no se refresca.

## [2026-09-08] ingest | Echo Forge F-03 SQX Long-Running Contract

Creado [[Echo Forge — F-03 SQX Long-Running Contract]] y subproyecto [[Echo Forge — F-03 SQX long-running]] hijo de [[Echo Forge — Factory V2 Completion]]. Change log [[2026-09-08-echo-forge-f03-sqx-long-running-spec]]. Graphify externo no se refresca.

## [2026-09-08] ingest | Echo Forge F-03 TOP correction C1–C3

Corrección in-place: ceiling `MaxInt64ns−1s` como platform safety; Adaptive `INACTIVE/DEPRECATED — NO CHANGE`; process-tree parent+child+grandchild y `Canceled`≠Timeout. Change log [[2026-09-08-echo-forge-f03-top-correction]]. Graphify externo no se refresca.
