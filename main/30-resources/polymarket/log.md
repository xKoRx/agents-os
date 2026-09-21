---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-16
updated: 2026-09-21
tags:
  - kind/doc
  - tech/polymarket
---
# Polymarket resources — Log

## [2026-09-21] publish | Master canónico — Five-POC absorbido, M4 recertificado @ 85e27ff

- Default GitHub `master` = `origin/main` = `a770da6`. Código `56e8fac` / integración `85e27ff` fast-forward desde `9ae5dde`. Recibo `testdata/research-master/certificate.json`: `M4_CERTIFIED_NON_LIVE` 27/0/0/5 pineado a `85e27ff` (no se heredó v07).
- Gates físicos en worktree `polymarket-engine-master`: build/vet/test/race PASS. `LIVE_DISABLED`. Sin force-push.
- U-02 `d5ce263` **no** integrado (`PATCH_NOT_ACCEPTED_FOR_V2`); tag `archive/u02-patch-not-accepted-for-v2`; unidad [[u02-v2-cash-confirmed]]. `REAL_FEE_READY=false`.
- Sports E2 ya entregado (`NO_SIGNALS_IN_SAMPLE`), cero código; worktree de integración conservado.
- Continuidad §13, padre, guía. Change log [[2026-09-21-polymarket-master-consolidation]].

## [2026-09-16] ingest | Cuatro Deep Research aportados por el owner → [[Polymarket — Edge Research Consolidado 2026-09-16]], cuatro source notes y [[polymarket/00-index|índice de dominio]]

- Fuentes R1–R4 identificadas por IDs de attachment, títulos originales, tamaño y SHA-256; originales completos no duplicados en este repo.
- Se unifican 58 formulaciones nominales en 30 hipótesis/familias deduplicadas PE-001…PE-030. No se declara ninguna rentable por el solo research.
- Contradicciones visibles: Sports fees/rebates, FLB en Sports, oracle bonds/settlement, retornos de wallets y estimaciones de fill.
- Documentación oficial parcial consultada; fuentes académicas individuales no auditadas exhaustivamente.

## [2026-09-16] ingest | Reframing proyecto → [[Polymarket Engine — MVP]] y preparación M0 Technical Knowledge Pack

- Autoridad canónica cambia de `Polymarket Arbitrage — MVP` a [[Polymarket Engine — MVP]].
- Distinción frozen: **Engine = MVP durable; Strategies = POCs descartables/promovibles**.
- Engine: Go, modular monolith, strategy-agnostic pero Polymarket-specific, una máquina grande inicialmente.
- NegRisk y Sports pasan a POC-S01/POC-S02, primeros consumidores del engine.
- Próxima ingesta del dominio: `Polymarket — Technical Platform Map — synced YYYY-MM-DD`, basado prioritariamente en documentación oficial, `llms.txt`, OpenAPI/AsyncAPI, changelog, contracts y SDK docs.
- Astra/Fable deben recibir ese knowledge pack preparado y no gastar sus ventanas en descubrir endpoints básicos.
- Workflow de diseño/implementación: `Astra proposal → Fable challenge → Astra reconcile → TOP implementation plan → NORMAL implementation` con autoridad documental concentrada en el único archivo del proyecto.
- Pendiente lint/Graphify desde entorno local; Graphify sigue siendo índice derivado.

## [2026-09-17] intake | Technical Platform Map guardado íntegro en Biblioteca; ficha GitHub y enlace al proyecto

- El original del owner `Polymarket — Technical Platform Map — synced 2026-09-17` está preservado **sin editar** en Biblioteca `/Polymarket Engine/Resources/Polymarket — Technical Platform Map — synced 2026-09-17.md`.
- Identidad: `160165` bytes; SHA-256 `78e6506fa67aa12843ba4acb0e4c8271a83c1841432a4a53777c73c4c723c11f`.
- Se crea [[Polymarket — Technical Platform Map — Intake 2026-09-17]] en GitHub y `Research — Technical Platform Map M0.md` en la carpeta del proyecto; el índice enlaza ambos. **Importante: el Markdown íntegro no está todavía en GitHub** porque el conector de escritura utilizado no recibe directamente bytes de adjuntos locales.
- El documento original admite certificación contractual pendiente, siete gaps RG-01…RG-07 y bloqueo de conversión NegRisk Protocol-v2 live sin ABI/ruta verificadas.
- Siguiente agente: conseguir el archivo íntegro, verificar SHA, incorporarlo en `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`, commit sin edición, luego corregir in-place por RG y commits incrementales. No regenerar 160 KB de memoria ni declarar falsamente que se ingirió completo.
- M0 no certificado; diseño Astra/Fable sólo cuando los blockers contractuales relevantes queden cerrados o explícitamente acotados con criterios de seguridad.

## [2026-09-17] checkpoint | M0 audit: preflight verified, in-place edit/extraction blocked — PARTIAL

- El mapa canónico **sí existe actualmente** en `master`: `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`; blob GitHub `0e6f8856d23695fd28493ec5b861828af461dd1b`, 160164 bytes; branch HEAD observado `8d66274b336a2c39c2aecb3ff5604067e67cd6e5`. Las frases de la entrada histórica anterior que indican que aún faltaba subirlo describen el estado de aquel intake, NO el estado actual.
- Bootstrap Agents-OS resuelto desde `main/AGENTS.md` y `main/80-agents/skills/agents-os-bootstrap/SKILL.md`; área `[[Personal]]` sin router de dominio aplicable. GitHub concedió permiso `push`; la rama canónica es `master`, con sincronización externa automática. No hay inspección válida de cambios locales pendientes: el acceso disponible es GitHub remoto, no el worktree del owner.
- RG-01…RG-07 siguen abiertos según §24 del mapa. No hubo extracción programática completa de los siete OpenAPI ni del AsyncAPI RFQ, comparación mecanizada operación→catálogo, certificación de NegRisk-v2 o auditoría HTTP individual de cada `[Sxx]`. No afirmar que esas verificaciones ocurrieron ni que M0 pasó.
- Bloqueo operativo reproducido: el conector GitHub `update_file` requiere reemplazar el contenido UTF-8 completo del archivo (160164 bytes), sin operación de parche parcial; el entorno de ejecución disponible no resuelve `github.com` por DNS y tampoco logró descargar el mapa. Es inseguro reconstruir/reemplazar el blob largo a partir de respuestas truncadas; por tanto, el mapa canónico queda intacto y no se publican correcciones no verificadas. No hubo órdenes, firmas, allowances ni conversiones.
- Próximo intento: disponer de un worktree autenticado con acceso a GitHub y al mapa completo, verificar `master` HEAD/working tree/blob nuevamente, extraer raws oficiales y parsearlos mecánicamente, parchear únicamente las secciones RG, validar cada etapa, commitear y verificar commits en `master` sin force push. Mientras tanto `M0=PARTIAL`, `DESIGN_READY=FAIL`, `FULL_CONTRACT_CERTIFICATION=FAIL`, y `NO LIVE CONVERSION UNTIL ROUTE VERIFIED` continúa vigente. No habilitar ASTRA-1 por este checkpoint.

## [2026-09-17] gate | M0 DESIGN_READY documental, no live certification

- Evidencia en Technical Platform Map §24: siete RG cerrados **para diseño**; 7/7 OpenAPI con 163 operaciones, RFQ AsyncAPI 13/13, DTOs Data v2; sources críticos validados con un fallo secundario S37 de límite de descarga.
- Conversión NegRisk CTF y v2 sigue deshabilitada live; v2 ABI no verificada. Historical L2 backfill deshabilitado por falta de garantías de replay/retención. RFQ/Combos y modos Builder/deferExec=true fuera de MVP inicial o disabled.
- M0 DESIGN_READY=PASS; FULL_PLATFORM_CONTRACT_CERTIFIED=NO; LIVE_EXECUTION_CERTIFIED=NO. Es cierre del knowledge pack para arquitectura, no diseño aprobado, implementación ni certificación con fondos.
- El manifiesto conserva el baseline histórico (160164 bytes) y actualiza SHA-256 de la concatenación vigente de once partes; proyecto e índice alineados con §24. Siguiente fase: owner/manager revisión conjunta → Astra propuesta → Fable challenge.

## [2026-09-20] checkpoint | Five-POC Research-Ready: 5/5 integradas + gates F5 verdes + M4 recertificado

- Rama `feature/five-poc-integration` @ `037c15d` (base shared `9d0512a`): las cinco POCs registradas (`poc-negrisk`, `poc-sports`, `poc-sports-combinatorial`, `poc-weather`, `poc-maturation`), suite completa 34/34 paquetes ok, race PASS en paquetes tocados, archtests PASS.
- Casos de uso nombrados engine-level: NEG-CASE-01, SPORT-REV-CASE-01 (`d4cf25e`) y gates F5-G01..G12 con vertical S03 + coexistencia de cinco instancias (`037c15d`); causas raíz documentadas (dispatcher usa reloj real para VirtualTime; contract_id weather = `SYN-WX-20260920-HIGH-UTC`).
- M4 recert: `experiment certify --profile no-live --baseline 037c15d` → 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 deferred live ⇒ `M4_CERTIFIED_NON_LIVE`. Evidencia: `10-projects/Personal/Polymarket Engine/agentes/M4-certify-037c15d-2026-09-20.json`.
- Guía operativa canónica: [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]] (HOW TO RUN/INPUT/MODE/OUTPUT por POC, research surfaces, limitaciones). `HYPOTHESIS_VALIDATED=NO` en las cinco (esperado); S05_W `BLOCKED_BY_SFG06`; fee REAL `UNVERIFIED`.

## [2026-09-20] aceptación final | Five-POC Final Acceptance: O/B demostradas, contadores auditados, M4 recert @ 1bcae43

- `FIVE_POC_FINAL_ACCEPTANCE_READY` — `feature/five-poc-integration` código `1bcae43` (HEAD `c915c11` = receipt `certificate-v06.json` pineado a `1bcae43`); delta sobre `cb549c7` = adapter A3 PE-004 (`CatalogFirstKnownAnchor` read-only as-of sobre `InspectEntity`), regresiones de semántica S01/S04 + DRILLS.md, corrección de determinismo en DRILLS (identidad de investigación `dataset_digest` determinista; contenedor con `capture_id`/`boot_id` aleatorios).
- PE-004: A2 `OPTIONAL_IMPROVEMENT` (22 fixtures corren como tests; falta serialización testdata/pe004); A3 `MISSING_REQUIRED_FUNCTIONALITY`→corregido; cohortes O (exige `known_at_ms`) y B (lo prohíbe) demostradas por CLI con observaciones durables y replay ×2; W sigue `BLOCKED_BY_SFG06`; `REAL_DATA_READY=NO`.
- Contadores NegRisk/Weather auditados sin bug: unidades distintas (evaluaciones/planes/fills nivel pata; 16 fills = 8 canastas COMPLETED, 911 RESIDUAL_HELD) y `strategy_metrics` frame-scoped last-wins; documentado en DRILLS.md §"Semántica de los contadores" y en la guía.
- 5/5 smokes operacionales de punta a punta (fixture→screen→shadow→replay RESOLVED→variante→compare), mutaciones nombradas exactas, `CORE_CHANGES_REQUIRED=NONE`; 34/34 build/vet/test/race/archtest; **M4 RECERTIFICADO @ `1bcae43` 27/0/0/5**; negativo `M4_STALE_CERTIFICATION` re-verificado.
- Guía [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]] actualizada al SHA final (spec S03 `max_book_age_ms=60000`, interpretación de contadores, cohorte O con adapter, estado del programa). Revisión humana `cb549c7..c915c11` y merge/push pendientes del owner.

## 2026-09-20 — `FIVE_POC_FINAL_CERTIFIED_BASELINE_READY` — cierre definitivo de las cinco POCs

- Branch `feature/five-poc-integration`: código final `56e8fac` (fix `notional_by_scenario` + fix `reserve_held` en `1f924d3`, wiring Catalog O `eaa8154`), evidencia `testdata/research-v07/` en `c38f6c4`, HEAD `85e27ff` = receipt `certificate-v07.json` pineado a `c38f6c4`; delta `56e8fac..85e27ff` sin cambios de código; sin push.
- Correcciones económicas: `notional_by_scenario` arranca en identidad aditiva `"0"` (antes `""` → `ParseDecimal("")` fallaba y la rama de patas perdía el notional en silencio); `reserve_held` = suma decimal de `HeldReserves` (reservas vivas del namespace; antes leía `Balances["held"]`, clave inexistente, siempre `""`) — reporting-only verificado; se liberan 1:1 con la observación `FinalFill`.
- Wiring PE-004 cohorte O: modo `anchor_source=catalog` en `engine experiment shadow` resuelve el ancla antes de congelar el manifest vía `CatalogFirstKnownAnchor` sobre `InspectEntity` real (sink de rechazo read-only); fail-closed (entidad ausente, doble declaración, cohorte B, `createdAt`); provenance persistido; modo fixture intacto. `CATALOG_WIRING_VERIFIED=YES`, `REAL_CATALOG_DATA_READY=NO`.
- Evidencia v07: 10 drills regenerados con receta idéntica (cuts 5 default CLI; digests v05 reproducen byte-idénticos en `c977447`): `dataset_digest` idéntico 10/10, contadores idénticos, obs digests byte-idénticos, `content_hash` cambia sólo por campos corregidos (BEFORE/AFTER en DRILLS.md v07; v05 intacto) + drill S05O catalog-mode.
- Quality: build/vet/test/race PASS, archtest 12/12, F5 gates + SFG-07 + LIVE_DISABLED PASS, **M4 `M4_CERTIFIED_NON_LIVE` @ `c38f6c4` 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 live diferidos**.
- Owner review pendiente: rango `c915c11..85e27ff`; decisión merge/push.

## [2026-09-21] experiment | PE-001 Sports Combinatorial reality check — `GO_RESEARCH`

- Worktree `feature/five-poc-integration@85e27ff` limpio; certificado v07 intacto; sin push; `LIVE_DISABLED`; rs-v03 intocado.
- Par real WNBA event 986912 (ATL vs NYL), ML 4358151 + spread ATL −1.5 4778073. Implicación Cover⇒Win no demostrada (OT del spread no escrito; clause de empate). H1 no falsificada: 0 ACCEPT, SCREEN `RULES_CONTRADICT`, SHADOW 54 semantic_reject.
- Fees: CLOB `fd {r:0.05,e:1,to:true}` en ambas patas; `/fee-rate` legado `{base_fee:1000}`; factory engine `SYNTHETIC_FIXTURE`; U-02 no cerrado.
- REST q=20 VWAP 0.56+0.48=1.04 (no midpoint); worst net sintético negativo. WS 45 s, durable_seq 184, replay digest idéntico en dos schedules.
- Bundle: `polymarket-engine-datasets/pe001-reality-check-20260921/`. Notas: [[POC-S03 — Sports Combinatorial]], continuidad §9, [[2026-09-21-pe001-reality-check]].
- Siguiente mandato mínimo: par basketball con OT explícito emparejado, journal congelado antes de SHADOW. No live.

## [2026-09-21] hardening | U-02 + discovery + readiness — `ENGINEERING_STAGE_CLOSED_RESEARCH_REPRODUCIBLE`

- Worktree `feature/five-poc-integration@85e27ff` limpio; **cero código**; M4 v07 @ `c38f6c4` no recertificado; sin push; `LIVE_DISABLED`; datasets pe001 78/78 y rs-v03 41/41 SHA OK.
- U-02 **`U02_PARTIAL`**: CLOB `fd {r:0.05,e:1,to:true}` = docs/SDK USDC; BUY en shares y `TRUNCATE_6DP` vs 5 dp no pareados; `/fee-rate` 1000 ≠ `fd.r`; rebate sports 15% vs weather 25%; delay `seconds_delay=1`. Vectores `hardening-20260921/u02/`. Factory sigue `SYNTHETIC_FIXTURE`.
- Discovery: 41 series / 73 eventos / 7 pares / 0 semántico∩temporal / 0 oportunidades q=20. WNBA familia `RULES_CONTRADICT`. FIBA 863805 template OT OK, PAST_KICKOFF. Sin SHADOW (no miembro admisible).
- S04: contratos KLGA/RJTT inventariados; sin vintages PIT. S05: `first_known_at` ≠ `createdAt` en 986912; ningún mercado nuevo en la ventana. S01 663 INCONCLUSIVE no promovidos. S02 0 señales locales ≠ NO_GO global.
- Bundle `polymarket-engine-datasets/hardening-20260921/`. Continuidad §10. Change log [[2026-09-21-polymarket-final-readiness]]. No alpha, no live.

## [2026-09-21] experiment | S02 PE-005-R1 E2 — `NO_SIGNALS_IN_SAMPLE`

- Integración `85e27ff` intacta; U-02 no baseline; cero código; sin push; `LIVE_DISABLED`; journal congelado antes de SHADOW.
- Muestra preregistrada por kickoff: 4 MLB moneylines (4584879, 4584889, 4584903, 4613496); 2284198 excluido. Captura 1800 s, 2590/2411/0, frontier 2430.
- SCREEN 0 opp (base y `widen_min_bps=25`); REPLAY MATCH `e713ebac…`; SHADOW 0 opp `INCONCLUSIVE` min_samples. 6/8 assets `SUSPECT` (`fee_source_discrepancy`); 4613496 USABLE 1-tick.
- No es NO_GO global ni alpha. Economía no certificada. Informe `pe005-r1-e2-20260921/REPORT.md`. Continuidad §12. Change log [[2026-09-21-pe005-r1-e2]].

## [2026-09-21] audit | U-02 protocol authority — `V2_CASH_CONFIRMED`

- Integración `85e27ff` intacta; worktree U-02 `d62768a`/`d5ce263` no mergeado; v07/v08 preservados; sin push; `LIVE_DISABLED`; `REAL_FEE_READY=NO`.
- PE-001 liquida en CTF Exchange V2 `0xE11118…` / pUSD. Tx BUY `0x35f20473…`: 180.34 shares completas + 2.239820 pUSD fee (notional+fee = cash 85.196220).
- Weather NYC liquida en Neg Risk V2 `0xe2222d27…`. Tx BUY `0x5a2269f1…`: 483.9 shares + 0.047040 pUSD fee. Misma unidad.
- `TAKER_PROCEEDS` = V1 `CalculatorHelper` (repo archivado). Help Center Maker Rebates (shares on BUY) es lenguaje V1; el FAQ de upgrade + contrato V2 + txs coinciden en collateral.
- Plan de relabel preparado, no ejecutado. Informe `u02-protocol-authority-20260921/REPORT.md`. Continuidad §11. Change log [[2026-09-21-u02-protocol-authority]].

