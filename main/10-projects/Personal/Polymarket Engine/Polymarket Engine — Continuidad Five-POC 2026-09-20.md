---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-20
updated: 2026-10-28
aliases:
  - Five-POC continuity
  - Polymarket Engine handoff
  - Retoma Polymarket Engine
tags:
  - kind/doc
  - tech/polymarket
  - topic/research-ops
---

# Polymarket Engine — Continuidad Five-POC (cierre 2026-09-20)

## Propósito

> [!danger] PROJECT_FROZEN_OWNER_2026_09_23 — NO CONTINUAR AUTOMÁTICAMENTE
> El owner congeló Polymarket Engine el 2026-09-23 y prioriza [[Echo Futures]]. El engine queda preservado en `master@09e8c7610f29a35f8080122b7cb4219b9866ebd7` / código `66486ac99a4606d5dc2b44757ac0722a6baa5415`. HCA-1 de Astra no fue implementado; H01–H11 siguen NOT_RUN; OOS sellado; `REAL_FEE_READY=false`; `LIVE_DISABLED`. Esta nota conserva historial, pero ya no define “próxima sesión” activa. Para retomar, leer primero el freeze del padre y [[Polymarket Engine — Historical Causality Architecture Audit]] y exigir mandato explícito del owner. No reactivar POCs, Sports Week, research, compra de datos, backtests ni live por inferencia.

> [!important] PUNTO DE ENTRADA PARA LA PRÓXIMA SESIÓN
> Esta nota es un **handoff de continuidad y tareas**, no una nueva SPEC ni sustituto del proyecto padre. Leer primero [[Polymarket Engine — MVP]], esta nota y [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]. Fuente del cierre: reporte ejecutor del 2026-09-20, registrado en [[2026-09-20-polymarket-fivepoc-final-closure]] y recursos del dominio. Las evidencias ejecutables viven en **el repo local del engine**, no en este vault. Cualquier SHA/resultado se debe volver a verificar al retomar; esta nota no afirma haber corrido comandos en la sesión documental.

**Actualización de autoridad 2026-09-22:** para causalidad histórica consultar §17 y [[Polymarket Engine — Historical Causality Architecture Audit]]. Allí sí se distingue la inspección física de código/tests de esta sesión de los resultados históricos reportados. Los checkpoints siguientes se preservan como historia.

## Contenido

## 1. Estado canónico al cierre

| Dimensión | Estado comunicado y condición |
|---|---|
| Programa | `FIVE_POC_FINAL_CERTIFIED_BASELINE_READY` **offline**, 5/5 estrategias/observador implementados, pipeline y outputs reproducibles; **no** equivale a validación de edge. |
| Engine | Go, monolito modular, Polymarket-specific, engine durable y strategies reemplazables. `TIME_TO_VALIDATED_HYPOTHESIS` sigue siendo el norte. |
| Repo | `~/go/src/github.com/xKoRx/polymarket-engine`; worktree **canónico** `~/go/src/github.com/xKoRx/polymarket-engine-master` en `master`. Worktree de integración `~/go/src/github.com/xKoRx/polymarket-engine-integration` conservado (`feature/five-poc-integration@85e27ff`) para la sesión Sports. |
| Shared base | `9d0512a912fcce4b9aefc152c7a89b090ff8df1d` sobre `feature/research-strategies-v01@f070496` local al inicio del programa. |
| SHA de corrección de código | `56e8fac`: bugs `notional_by_scenario`, `reserve_held` y wiring Catalog O. |
| SHA de evidencia/certificación | `c38f6c4`: evidencia `research-v07` y baseline del recibo M4. Árbol de código idéntico a `56e8fac` según reporte. |
| HEAD final | Canónico `master` @ `a770da6` (recibo M4 de `85e27ff`). Código Go = `56e8fac`; `85e27ff` añade v07; `a770da6` añade `testdata/research-master/`. |
| Calidad | 2026-09-21 sobre `85e27ff`: build/vet/test/race PASS (34 paquetes), certify no-live PASS. |
| M4 | Recertificado **en `85e27ff`**: `M4_CERTIFIED_NON_LIVE` 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 live diferidos. Recibo: `testdata/research-master/certificate.json` (commit `a770da6`). El pin v07 @ `c38f6c4` queda histórico; no certifica `master` por herencia. |
| Git/publicación | **Publicado.** Default GitHub `master` = `origin/main` = `a770da6`. Fast-forward, sin force-push. |
| Datos/hipótesis | Fixtures sintéticos; datasets RS v0.3 (41/41 SHA OK) y pe001 (78/78 SHA OK) intactos; Weather/Catalog **inventariados** 2026-09-21 sin vintages ni cohorte nueva; fee venue **`V2_CASH_CONFIRMED`** (unidad BUY = collateral pUSD; `TAKER_PROCEEDS` = V1 archivado, no el venue de PE-001/weather); `REAL_FEE_READY=NO`; `HYPOTHESIS_VALIDATED=NO` en las cinco. Etapa: `ENGINEERING_STAGE_CLOSED_RESEARCH_REPRODUCIBLE`. |
| Seguridad | `LIVE_DISABLED` / SHADOW virtual; wallet, signing, órdenes y certificación live fuera de alcance. |

**Control de documentación:** las secciones antiguas, `updated` de frontmatter, `progress: 0` en subproyectos o bullets históricos del padre pueden describir checkpoints previos. Para el estado vigente usar *este snapshot + §13 + § Master canónico del padre + recibo `research-master`*, verificando el checkout. No borrar historial ni convertir un estado reportado en evidencia nueva.

## 2. Matriz de cinco POCs — límites del alcance

| POC | ID/identidad | Camino disponible y evidencia comunicada | Lo que NO está demostrado |
|---|---|---|---|
| S01 NegRisk | PE-002, `poc-negrisk` | Fixture → SCREEN → SHADOW virtual → REPLAY RESOLVED → compare; 919 evaluaciones aceptadas, 16 fills de pata, notional corregido `170`; variante min_edge_bps 919→0. | Beneficio con book/fee real, liquidez ejecutable y alpha. |
| S02 Sports Reversion | PE-005-R1, `poc-sports` | Una aceptación/fill en caso sintético; variante `widen_min_bps` rechaza; notional `24.9998`, replay RESOLVED. | Maker calibrado, fill/fee real y edge. NO confundir con Sports Combinatorial. |
| S03 Sports Combinatorial | PE-001, `poc-sports-combinatorial` | Proof `Cover(A,-h) ⇒ Win(A)`, 2 BUY legs, L2 DECLARED, synthetic fee, casos positive/no-edge/shortfall/semantic-reject; E3-RC WNBA 986912 0 ACCEPT; discovery 2026-09-21: 7 pares / 0 semántico∩temporal. | RFQ/Combo nativo; OT/tie WNBA demostrable; par live usable; fee efectiva (5 dp / operador); alpha. |
| S04 Weather | PE-030, `poc-weather` | Offline UNCALIBRATED intacto; inventario 2026-09-21 NYC **KLGA** (1046925/1052139), Tokyo **RJTT** (1046399); `weather_fees` 0.05/1/to rebate 0.25. | Forecast vintages point-in-time; calibración; alpha. Adquisición: `hardening-20260921/weather/ACQUISITION.md`. |
| S05 New Market Maturation O/B | PE-004, `poc-maturation` | Observador durable `FrameObserver`; wiring Catalog O verificado; sync 2026-09-21 de 986912: `first_known_at` ≠ `createdAt`. **No nació mercado nuevo** en la ventana. | Cohorte O/B sobre mercado *nuevo*; W (SFG-06); alpha. Descriptiva: NO forzar fills. |

**Semántica de métricas:** S01 `accepted` = evaluaciones, `baskets_planned` = planes, `simulated_fills` = patas; 16 fills = ocho canastas completadas, 911 residuales en el drill completo. S04 `scorecard.accepted` es total del run; `strategy_metrics` como `fee_bps`/`net` describen **último bucket del último frame** (merge last-wins), no el run entero. No inferir aceptación con net negativo de comparar ambos niveles. Ver explicación y regresiones en `testdata/research-v07/experiment-drills/DRILLS.md` y la guía.

## 3. Correcciones finales v07 — qué cambió y por qué

1. `notional_by_scenario`: el acumulador era `""`, provocaba `ParseDecimal("")` y omitía notional de patas; ahora identidad aditiva `"0"`, corrupción → error invariante. Pruebas no-ops, pata única, basket completo/parcial, rutas mixtas y persistencia. El drill S01 comunica notional `170` que ya constaba en ledger.
2. `reserve_held`: lectura errónea `Balances["held"]`; la fuente es `HeldReserves` viva por namespace. Reporta `"0"` sin reservas. Es reporting-only según auditoría, **no** alimentación de Risk. Precaución: repetir el **mismo** run-id sobre el mismo directorio puede topar con dedup de fill keys y dejar reservas vivas; para repetir experimentos usar dataset/directorio fresco o la receta de idempotencia documentada.
3. Catalog O: `cmd/engine/maturation_catalog.go` integra `CatalogFirstKnownAnchor`/`catalog.Service.InspectEntity` **antes** de congelar manifest, con rechazo fail-closed. `anchor_source=catalog` + `market_id` explícito; prohíbe doble declaración `known_at_ms`, cohorte B+Catalog, ancla ausente y `createdAt` de Gamma como sustituto. Modo fixture sin `anchor_source` preservado. Probado sobre catálogo real de servicio alimentado con fixture, **NO** en Gamma productivo.
4. Evidencia v07: 10 drills BASE/VARIANT regenerados, datasets `dataset_digest` idénticos 10/10, contadores idénticos 10/10 y observaciones S05 idénticas; cambiaron `content_hash`/`virtual_pnl_net` cuando corresponde por notional corregido. Evidencias `research-v01…v06` preservadas. `cuts=5` es el default correcto para reproducir drill histórico; `cuts=4` da digest diferente. La identidad experimental es `dataset_digest`, no hash byte-a-byte de journal (capture_id/boot_id aleatorios).

## 4. Ubicación precisa de fuentes y artifacts

- **Proyecto padre:** [[Polymarket Engine — MVP]] — sección `Five-POC Cierre Definitivo` y su bitácora; el padre conserva historia previa.
- **Guía de ejecución:** [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]] (build, `fixture fivepoc`, `screen-consolidated`, `experiment shadow`, `experiment compare`, `manifest build`, `replay`, HOW TO RUN de S01–S05 y modo Catalog O).
- **Corpus de evidence final del engine:** `testdata/research-v07/experiment-drills/DRILLS.md`, `testdata/research-v07/experiment-drills/S01..S05/{base,variant,compare}.json`, `S05O/base.json`, `testdata/research-v07/certificate-v07.json`.
- **Correcciones en code:** `internal/experiment/experiment.go`, `cmd/engine/maturation_catalog.go`, `internal/strategy/pocs/maturation/catalog_anchor.go`, más tests. Usar `git show 56e8fac` y `git log c915c11..85e27ff --oneline`; no confiar en nombres de commits sin inspección.
- **Notas POC existentes:** [[POC-S03 — Sports Combinatorial]], [[POC-S04 — Weather]], [[POC-S05 — New Market Maturation]]; S01/S02 tienen historial integrado en el padre y el repo, no inventar notas nuevas si no existen.
- **Recibo narrativo final:** `80-agents/journal/logs/2026-09-20-polymarket-fivepoc-final-closure.md`; recursos del dominio `main/30-resources/polymarket/log.md`.
- **Research autoridad:** [[Polymarket — Edge Research Consolidado 2026-09-16]]; plataforma [[Polymarket — Technical Platform Map — synced 2026-09-17]]. No usar papers o snapshots para inferir fee/contratos vivos sin verificación nueva.

## 5. Procedimiento de retoma para cualquier agente nuevo

**Orden:** bootstrap canónico de Agents-OS (`main/AGENTS.md` y skill bootstrap), leer padre → esta continuidad → guía → SPEC de la POC elegida → `DRILLS.md` v07 → código real. No reabrir diseño M0/M1 ni ejecutar un refactor por defecto.

Preflight **read-only** del checkout local (no ejecutar en la copia de GitHub si aún no está publicada):

```bash
cd ~/go/src/github.com/xKoRx/polymarket-engine-master
git status --short --branch
git rev-parse HEAD
git worktree list
git log -n 12 --oneline
git merge-base --is-ancestor 85e27ff HEAD && echo CODE_ANCESTRY_OK
ls -l testdata/research-master/certificate.json testdata/research-v07/certificate-v07.json
```

Esperado **tras la consolidación 2026-09-21**: HEAD `a770da6` en `master`, limpio, certificado `research-master` pineado a `85e27ff`. **STOP** si falta la rama/commit, el árbol está dirty o M4 no corresponde a `85e27ff`: diagnosticar primero; NO forzar checkout/reset/push. El remoto canónico es `origin/master`. El worktree `feature/five-poc-integration` permanece en `85e27ff` para Sports; no reconstruir desde un HEAD remoto viejo.

Validar operabilidad después del preflight, en dataset nuevo:

```bash
cd ~/go/src/github.com/xKoRx/polymarket-engine-master
go build -o /tmp/engine ./cmd/engine
go vet ./...
go test ./... -count=1
/tmp/engine fixture fivepoc --kind vertical --out /tmp/pme-resume-s01s02
# Continuar la receta exacta por POC desde la guía operativa; no reutilizar un output dir existente.
```

Para M4, leer flags reales `engine experiment certify --help`, confirmar SHA completo de baseline e invocar perfil `no-live` solo si se requiere certificar **código nuevo**. El recibo v07 histórico sigue válido exclusivamente para el código correspondiente; no heredar M4 por nombre de branch.

## 6. Tareas reales de la próxima sesión — orden de decisión

- [x] **OWNER / P0 — Review humana + publicación** (2026-09-21, mandato de consolidación): Five-POC `85e27ff` absorbido en `master` @ `a770da6`; M4 recertificado en `85e27ff`; remoto publicado; `d5ce263` no mergeado. El agente no se autoaceptó: el mandato owner autorizó la publicación.
- [x] **OWNER / P0 — Publicación engine:** ejecutada. Default `master`. `main` alias FF. Sin force-push.
- [ ] **RESEARCH / P1 — Elegir UNA POC y UN experimento falsable** con criterio de falsación, métrica, sample, dataset y controles; usar mutation drill BASE/VARIANT como harness, no como prueba de alpha. Arranque de menor infraestructura: S01 sensibilidad `min_edge_bps` o S05 B descriptiva sobre fixture; escoger según interés del owner.
- [ ] **DATA / P1 — Plan de paso a datos reales de sólo lectura:** inventariar RS v0.3 certificados y manifest de cierre, integridad, fuente/reglas/fees/as-of y ventanas. No declarar `REAL_DATA_READY` por existencia de carpetas `.rs-v03-*`; obtener recibo verificable y preservar guard.
- [r] **PE-001 / P2 — Contratos de mercado y fees (2026-09-21):** reality check ejecutado sobre HEAD `85e27ff`. Par WNBA 986912 ML/SP identificado; implicación Cover⇒Win **no** demostrada (OT del spread UNKNOWN + cláusula de empate); H1 no falsificada (0 ACCEPT, `RULES_CONTRADICT`); U-02 parcialmente observado (`fd r=0.05 e=1 to=true`) pero `REAL_FEE_READY=NO`; decisión `GO_RESEARCH`. Evidencia `pe001-reality-check-20260921`. No cierra Review humana ni live.
- [x] **PE-001 / P2 — Discovery E3-RC2 (2026-09-21, Grok 4.6):** SCREEN Gamma+Catalog sobre 41 series basketball / 73 eventos / 7 pares ML+SP. Semántico∩temporal = **0**. Familia WNBA (6/6) `RULES_CONTRADICT` (OT SP UNKNOWN + tie clause). Template FIBA 863805 OT INCLUDED ambos lados, kickoff pasado (Gamma accepting stale). 0 oportunidades económicas q=20. U-02 **`U02_PARTIAL`**. Bundle `polymarket-engine-datasets/hardening-20260921/`. Sin SHADOW (no había miembro admisible). Sin órdenes.
- [ ] **PE-001 / P2 — Siguiente par usable:** esperar un ML+SP con OT escrito igual y sin tie, **o** dictamen owner de que la cláusula WNBA es boilerplate inerte; entonces WS + congelar journal **antes** de SHADOW. Sin órdenes.
- [x] **PE-030 / P2 — Inventario de contrato real (2026-09-21):** NYC Sep 21/22 station **KLGA**, Tokyo **RJTT**, NOAA hourly + fallback WU; fee `weather_fees` 0.05/1/to rebate 0.25. **Sin vintages point-in-time** → UNCALIBRATED. Adquisición mínima en `hardening-20260921/weather/ACQUISITION.md`. No se calibró.
- [ ] **PE-030 / P2 — Forecast vintages:** ingestar NWS MOS/NBM issued-at ≤ frame; no latest. Mantener UNCALIBRATED hasta evidencia.
- [x] **PE-004 / P2 — Catalog first_known ≠ createdAt (2026-09-21):** sync Gamma de 986912 en dataset fresco → `first_known_at=2026-09-21T14:33:53Z` vs `createdAt=2026-09-08`. Wiring honesto. **No nació mercado nuevo en la ventana** → cohorte O/B real ausente (no sustituir).
- [ ] **PE-004 / P2 — Cohorte real O/B:** observar un mercado **nuevo** durante captura; `first_known_at` auténtico; W sigue SFG-06.
- [x] **U-02 / P0 — Protocol authority V1/V2 (2026-09-21):** dictamen **`V2_CASH_CONFIRMED`**. PE-001 y weather liquidan en Exchange V2 / NegRisk V2 con BUY fee en pUSD y shares completas. `TAKER_PROCEEDS` @ `d5ce263` modela V1 archivado; no mergear como venue. `REAL_FEE_READY=NO`. Informe `u02-protocol-authority-20260921/REPORT.md`. Change log [[2026-09-21-u02-protocol-authority]]. Código no integrado; v07/v08 preservados.
- [x] **S02 / PE-005-R1 — E2 real sports (2026-09-21):** captura 1800 s de 4 moneylines MLB distintas de 2284198, muestra por kickoff preregistrada. Exit **`NO_SIGNALS_IN_SAMPLE`** (0 señales baseline y `widen_min_bps=25`). 3/4 mercados `SUSPECT` por `fee_source_discrepancy` (WS fee 0 vs Gamma 1000); 4613496 USABLE 1-tick. No es NO_GO global. Bundle `pe005-r1-e2-20260921/`. Change log [[2026-09-21-pe005-r1-e2]]. Sin código, sin live.
- [ ] **BACKLOG no bloqueante / P3:** SFG-06 residual `new_market → Catalog reducer → UniverseChanged → replay` para W; relabel `USDC_CASH`/`TAKER_PROCEEDS` según dictamen V2 (plan listo, no ejecutado); redondeo 5 dp vs `TRUNCATE_6DP`; `capitalLock` legacy BBO hardcodeado `5.1` ≠ notional real (reconfirmado `experiment.go`); tres archivos `cmd/engine` gofmt drift reconfirmados (`five_poc_cases_test.go`, `research_gates_test.go`, `screen.go`); A2 PE-004 serializar corpus 22 fixtures. Priorizar sólo cuando un experimento lo requiera.
- [ ] **CIERRE / P0 al retomar:** actualizar esta nota, padre, nota POC afectada, recurso/guía y journal con resultados de la nueva sesión. `Graphify` y lint sólo marcar PASS si se ejecutaron; no confundir docs con ejecución física.

## 7. Políticas de ejecución y separación de estados

- `IMPLEMENTATION_PASS`, `PIPELINE_PASS`, `RESEARCH_READY_OFFLINE`, `REAL_DATA_READY`, `HYPOTHESIS_VALIDATED`, `LIVE_CERTIFIED` **son seis estados diferentes**. Hoy sólo los tres primeros están reportados afirmativamente para cinco consumidores. Real datos, alpha y live pendientes.
- S05 O/B es **descriptiva**. `0 opportunities / 0 orders / 0 fills` es PASS de diseño; no comparar directamente con PnL de strategies. SFG-06 W no bloquea O/B.
- Dos workstreams aislados como máximo para nuevos coding agents. Manager único escritor de composition/registry/shared; cada POC sólo su paquete/fixtures. Datos originales read-only; fixtures en temp, `dataset.Guard`, no `LIVE`.
- Nuevos cambios de código invalidan recertificación anterior hasta certificar SHA final. Historical evidence v05/v06/v07 no se sobrescribe; nuevo experimento → nuevo run-id, provenance, manifest y artifact versionado.
- Nada de negociación con dinero real, secrets, wallet, signing o permisos live sin mandato/seguridad/aceptación explícitos separados.

## 8. Qué debe responder el primer agente de la próxima sesión

```text
RESUME_STATUS:
  agents_os_bootstrap:
  engine_worktree:
  current_branch:
  current_head:
  clean:
  final_code_sha_present:
  evidence_sha_present:
  certificate_baseline_verified:
  remote_vs_local:
  five_pocs_status:
  datasets_and_capture_safety:
  owner_review_state:
  publication_decision_state:
  chosen_poc_and_first_falsifiable_experiment:
  blockers_requiring_owner:
  next_execution_action:
```

La primera sesión debe **comenzar ejecutando el preflight y un caso de uso real offline**; no gastar horas redescubriendo arquitectura ni afirmar estado remoto/local sin comprobarlo. El cierre documental 2026-09-20 dejó Review/push abiertos; **§13 supersede**: `master` está publicado (`a770da6`).

## 9. Reality check PE-001 — 2026-09-21

Ejecutado sobre worktree integración HEAD `85e27ff` (limpio). Informe: `~/go/src/github.com/xKoRx/polymarket-engine-datasets/pe001-reality-check-20260921/REPORT.md`. Change log [[2026-09-21-pe001-reality-check]].

```text
RESUME_STATUS_20260921:
  agents_os_bootstrap: PASS (DEFAULT Personal)
  engine_worktree: /home/kor/go/src/github.com/xKoRx/polymarket-engine-integration
  current_branch: feature/five-poc-integration
  current_head: 85e27ff85d466c6522455f1426f6e0c8e23fe157
  clean: YES
  final_code_sha_present: 56e8fac (ancestro)
  evidence_sha_present: c38f6c4
  certificate_baseline_verified: YES (v07 pin c38f6c4; no recertificado)
  remote_vs_local: origin 25f578a; HEAD local unpushed
  five_pocs_status: offline certified intacto; PE-001 E3_RC = GO_RESEARCH
  datasets_and_capture_safety: rs-v03 intocado; bundle nuevo pe001-reality-check-20260921
  owner_review_state: OPEN c915c11..85e27ff
  publication_decision_state: UNPUBLISHED
  chosen_poc_and_first_falsifiable_experiment: PE-001 H1 (reglas verbatim ⇒ no ACCEPT) — no falsificada
  blockers_requiring_owner: OT/tie boilerplate WNBA; Review/publicación engine; U-02 rounding 5 vs 6 dp
  next_execution_action: E3-RC2 par con OT explícito emparejado; congelar journal antes de shadow
  decision: GO_RESEARCH (nunca live)
```

## 10. Hardening + U-02 + discovery — 2026-09-21

Informe: `~/go/src/github.com/xKoRx/polymarket-engine-datasets/hardening-20260921/REPORT.md`. Change log [[2026-09-21-polymarket-final-readiness]]. Código del engine **no** modificado; M4 v07 sigue válido para `c38f6c4`.

```text
RESUME_STATUS_20260921_HARDENING:
  agents_os_bootstrap: PASS (DEFAULT Personal)
  engine_worktree: /home/kor/go/src/github.com/xKoRx/polymarket-engine-integration
  current_branch: feature/five-poc-integration
  current_head: 85e27ff85d466c6522455f1426f6e0c8e23fe157
  clean: YES
  final_code_sha_present: 56e8fac
  evidence_sha_present: c38f6c4
  certificate_baseline_verified: YES (no recertificado; sin código nuevo)
  remote_vs_local: origin 25f578a; HEAD local unpushed
  five_pocs_status: offline certified intacto
  u02_gate: U02_PARTIAL
  pe001_discovery: 41 series / 73 events / 7 pairs / 0 semantic∩temporal / 0 economic
  datasets_and_capture_safety: pe001 78/78 SHA OK; rs-v03 41/41 SHA OK; bundle nuevo hardening-20260921
  owner_review_state: OPEN c915c11..85e27ff
  publication_decision_state: UNPUBLISHED
  chosen_poc_and_first_falsifiable_experiment: PE-001 espera par OT-emparejado o dictamen boilerplate; S04 adquisición NOAA/NWS; S02 segunda ventana
  blockers_requiring_owner: Review/publicación engine; dictamen OT/tie WNBA; autorización de parche Economics BUY-shares si se desea
  next_execution_action: no código; esperar par usable o vintages weather; no live
  decision: ENGINEERING_STAGE_CLOSED_RESEARCH_REPRODUCIBLE (nunca live, nunca alpha)
```

## 11. Protocol authority U-02 — 2026-09-21

Dictamen **`V2_CASH_CONFIRMED`**. Informe: `~/go/src/github.com/xKoRx/polymarket-engine-datasets/u02-protocol-authority-20260921/REPORT.md`. Change log [[2026-09-21-u02-protocol-authority]]. **Cero código nuevo en integración; parche U-02 no mergeado.** v07 y v08 preservados. `REAL_FEE_READY=NO`.

```text
RESUME_STATUS_20260921_U02_AUTHORITY:
  agents_os_bootstrap: PASS (DEFAULT Personal; Graphify degradado — binario ausente)
  engine_worktree: /home/kor/go/src/github.com/xKoRx/polymarket-engine-integration
  current_branch: feature/five-poc-integration
  current_head: 85e27ff85d466c6522455f1426f6e0c8e23fe157
  clean: YES
  u02_worktree: /home/kor/go/src/github.com/xKoRx/polymarket-engine-u02 @ d62768a (código d5ce263, no integrado)
  final_code_sha_present: 56e8fac
  evidence_sha_present: c38f6c4
  certificate_baseline_verified: YES v07 @ c38f6c4; v08 @ d5ce263 (HEAD U-02 = pin d62768a; correspondencia exacta HEAD↔cert NO)
  remote_vs_local: origin 25f578a; HEAD local unpushed
  five_pocs_status: offline certified intacto
  u02_gate: V2_CASH_CONFIRMED (unidad BUY=collateral pUSD); TAKER_PROCEEDS=V1 archivado; REAL_FEE_READY=NO
  pe001_exchange: CTF Exchange V2 0xE111180000d2663C0091e4f400237545B87B996B; collateral pUSD
  pe001_settlement_tx: 0x35f204735b3d0854dc3da5a77a0ff4251cf41ad19a88f4dc569a9b83b7c2de61 (BUY 180.34 shares + 2.239820 pUSD fee)
  weather_exchange: Neg Risk CTF Exchange V2 0xe2222d279d744050d28e00520010520000310F59
  weather_settlement_tx: 0x5a2269f1f9a9325b7874630b3346040ddd7fef18899cca5c22ee3f38685c5fc8
  datasets_and_capture_safety: pe001/rs-v03/v07/v08 intocados; bundle nuevo u02-protocol-authority-20260921
  owner_review_state: OPEN c915c11..85e27ff; d5ce263 NO mergear como venue
  publication_decision_state: UNPUBLISHED
  chosen_poc_and_first_falsifiable_experiment: PE-001 espera par OT-emparejado o dictamen boilerplate; S04 vintages
  blockers_requiring_owner: Review/publicación engine; dictamen OT/tie WNBA; autorización de relabel USDC_CASH/TAKER_PROCEEDS (plan listo, no ejecutar)
  next_execution_action: no código; no integrar d5ce263; no live
  decision: V2_CASH_CONFIRMED (nunca REAL_FEE_READY, nunca live, nunca alpha)
```

## 12. S02 PE-005-R1 E2 — captura real MLB — 2026-09-21

Exit **`NO_SIGNALS_IN_SAMPLE`**. Informe: `~/go/src/github.com/xKoRx/polymarket-engine-datasets/pe005-r1-e2-20260921/REPORT.md`. Change log [[2026-09-21-pe005-r1-e2]]. **Cero código.** Integración HEAD `85e27ff` intacta. U-02 no usado como baseline. rs-v03 intocado. Journal congelado antes de SHADOW. Sesión **no cerrada**.

```text
RESUME_STATUS_20260921_S02_E2:
  agents_os_bootstrap: PASS (DEFAULT Personal; warm turn)
  engine_worktree: /home/kor/go/src/github.com/xKoRx/polymarket-engine-integration
  current_branch: feature/five-poc-integration
  current_head: 85e27ff85d466c6522455f1426f6e0c8e23fe157
  clean: YES
  u02_worktree_used: NO
  final_code_sha_present: 56e8fac
  evidence_sha_present: c38f6c4
  certificate_baseline_verified: YES (v07 pin c38f6c4; no recertificado; sin código nuevo)
  remote_vs_local: origin 25f578a; HEAD local unpushed
  five_pocs_status: offline certified intacto
  s02_e2_exit: NO_SIGNALS_IN_SAMPLE (no global NO_GO)
  sample: 4 MLB moneylines (4584879, 4584889, 4584903, 4613496); excluded 2284198
  capture: 2026-09-21T15:34:02Z/16:04:03Z 1800s; recv 2590 admitted 2411 refused 0 frontier 2430
  quality: 6/8 SUSPECT fee_source_discrepancy; 4613496 YES+NO OBSERVED_USABLE 1-tick
  screen: 30 cuts × 8 instances; 0 opportunities; 0 ineligible (CLI); engine_sha 85e27ff
  replay: digest MATCH e713ebac… records_applied=2430 not_reproducible=0
  shadow: 8 runs × 920 frames; 0 opp/eval/fills; INCONCLUSIVE min_samples 100
  variant: widen_min_bps 50→25 same dataset; 0 vs 0 signals
  economics: NOT_CERTIFIED; maker UNCALIBRATED; quotes/spreads/depth only
  datasets_and_capture_safety: rs-v03 intocado; journal-frozen read-only pin; bundle pe005-r1-e2-20260921
  owner_review_state: OPEN c915c11..85e27ff
  publication_decision_state: UNPUBLISHED
  chosen_poc_and_first_falsifiable_experiment: S02 E2 ejecutado; siguiente = T-90min kickoff esta noche SI USABLE, o runbook 2284198 T-8.5h
  blockers_requiring_owner: Review/publicación engine; U-02 fee_source_discrepancy excluye Detect en books con last_trade fee=0
  next_execution_action: no código; no live; no merge U-02
  decision: NO_SIGNALS_IN_SAMPLE (nunca live, nunca alpha, nunca NO_GO global)
```

## 13. Consolidación `master` — 2026-09-21

Mandato owner one-shot. Change log [[2026-09-21-polymarket-master-consolidation]]. Agent run [[2026-09-21-cursor-grok-4.6-polymarket-master-consolidation]].

```text
RESUME_STATUS_20260921_MASTER:
  agents_os_bootstrap: PASS (DEFAULT Personal)
  engine_worktree: /home/kor/go/src/github.com/xKoRx/polymarket-engine-master
  current_branch: master
  current_head: a770da6648f93127411cac9a844baaacb7a53397
  clean: YES
  integration_sha: 85e27ff85d466c6522455f1426f6e0c8e23fe157
  code_sha: 56e8fac
  m4_baseline: 85e27ff (recertified; v07 c38f6c4 historical)
  certificate: testdata/research-master/certificate.json M4_CERTIFIED_NON_LIVE 27/0/0/5
  remote: origin/master = origin/main = a770da6; default_branch=master
  u02: V2_CASH_CONFIRMED; d5ce263 PATCH_NOT_ACCEPTED_FOR_V2; REAL_FEE_READY=false
  sports: E2 NO_SIGNALS_IN_SAMPLE delivered; zero code; integration worktree kept @ 85e27ff
  live: LIVE_DISABLED
  owner_review_state: publication executed by consolidation mandate
  publication_decision_state: PUBLISHED
  blockers_requiring_owner: OT/tie WNBA boilerplate; autorización de relabel USDC_CASH/TAKER_PROCEEDS (no ejecutado: cambiaría modelo económico)
  next_execution_action: research sobre master; no live; no merge U-02
  decision: MASTER_CANONICAL
```

## 14. PE-005-R1 semana Sports — 2026-09-21

Mandato owner one-shot. Change log [[2026-09-21-pe005-r1-sports-week]]. Agent run [[2026-09-21-cursor-grok-4.7-pe005-r1-sports-week]]. Sesión Agents-OS no cerrada.

```text
RESUME_STATUS_20260921_SPORTS_WEEK:
  agents_os_bootstrap: PASS (sesión previa; esta nota es el delta)
  published: origin/master = origin/main = bfa6eafa57ae17aa92d7e112d41b87cae5b67990
  code_sha: c3b1aa1e01d2444feaf1d0ff7c32fde4b75ceb0d
  certificate: testdata/research-master/certificate.json M4_CERTIFIED_NON_LIVE 27/0/5-deferred-live pineado a c3b1aa1
  binary: vcs.revision bfa6eaf vcs.modified=false
  fee_identities: cap declarado y fee de trade son distintas; trade dentro del cap → INTERVAL [0, cap]; fuera del cap o trades que no convergen → SUSPECT; trade convergente sin cap → POINT de ese trade
  real_fee_ready: false
  live: LIVE_DISABLED
  u02: V2_CASH_CONFIRMED; d5ce263 no integrado
  canary: PASS mercado 4584879 ambos libros OBSERVED_USABLE; trade fee raw "0" @ seq 29 conservada; suspect false; cuarentena 0; replay digest 844a9392eaea0eccf3555d3eb0eda0b329c5d10c3cfecde86e729b47f6ee8e86 MATCH
  campaign_status: ARMED
  started_at: null
  ends_at: null
  next_t90: 2026-09-21T21:05:00Z mercado 4584879 kickoff 2026-09-21T22:35:00Z
  waiting_moneylines: 91
  params_frozen: window_ms=300000 ref_frames=10 widen_min_bps=50 entry_budget=25 min_net_edge_bps=50 taker=true cuts=30
  economics: NOT_CERTIFIED
  service: user sports-week-capture.service active; timers health 5min y analyze 60min enabled
  dataset: sports-week-pe005
  notify_channel: none (alertas durables en el dataset)
  disk_free_ratio_at_arm: 0.189 (pausa de sesiones nuevas bajo 0.15; halt bajo 0.05; no se borra evidencia)
  decision: ARMED_WAITING_NEXT_WINDOW
```

## 15. Histórico M0 — PE-005-R1 — 2026-09-21

**ADDENDUM 2026-09-21 (adquisición y persistencia; diagnóstico L2 supersedido):** `HISTORICAL_DATA_ACQUISITION_RESULT` reportó objetos v3 verificados byte a byte, replay 4/4 reproducido y selección Parquet+DuckDB con equivalencia ClickHouse, sin compra necesaria. Su conclusión de drift BBO 66–85% y fundamento de `L2_SNAPSHOT_ONLY` fueron corregidos por [[Research — Historical L2 Forensic Validation 2026-09-21]]: el reconstructor externo aplicaba mal size/delete. No reutilizar ese drift como diagnóstico vigente. Ver [[Research — Historical Data Acquisition ADDENDUM 2026-09-21]], dataset `hist-acq-20260921` y auditoría §17 para los límites de continuidad y causalidad.

Mandato owner one-shot. Change log [[2026-09-21-historical-research-m0]]. Agent run [[2026-09-21-cursor-grok-4.7-historical-research-m0]]. La campaña Sports Week no se reinició, no se le cambió el binario ni se escribió su dataset. Sesión Agents-OS no cerrada.

```text
HISTORICAL_RESEARCH_M0_RESULT: HISTORICAL_DATA_PARTIAL
  sports_week: INTACT
    service: sports-week-capture.service active since 2026-09-21 14:15:20 -03
    binary: sports-week-pe005/bin/engine-bfa6eafa57ae17aa92d7e112d41b87cae5b67990
    campaign_status: ARMED
    started_at: null
    capture_mode: NO_GAMES_SCHEDULED
  published: origin/master = origin/main = de33d7d4efbcb085cca46dc8f3e2fbe2b2335d97
  code_sha: 56195c945eae59feb8aeefe849d887ed81776494
  certificate: testdata/research-master/certificate.json M4_CERTIFIED_NON_LIVE 27/0/5-deferred-live pineado a 56195c9
  binary_of_pilot: vcs.revision 56195c9 vcs.modified=false
  live: LIVE_DISABLED
  real_fee_ready: false
  economics: ECONOMICS_UNCERTIFIED
  not_claimed: BACKTEST_PASS OOS_PASS HYPOTHESIS_VALIDATED
  source: PendulumFlow v3 hours 2026-09-01T21 and T22, remote predicate, full parquet not stored
  publisher_sha256_not_recomputed_locally: 21=ee4c5add7d23cda375beaeafa0833969059e3d7ad0c5bf246d20b4eb9316c4d3 22=5cd4e6b10bba51f9d54d6ac16637a1009b7ef824c4ed21b4fdaadf8787925dd9
  kickoff_authority: SCHEDULE_CORROBORATED_POSTHOC (MLB statsapi + Gamma gameStartTime, both retrieved 2026-09-21)
  exploratory_kickoff: 2026-09-01T22:40:00Z receive window [21:10Z, 22:40Z)
  markets: SD 3901945, NYM 3901951, TOR 3901947, SF 3901949
  oos_sealed_not_analyzed: ATL 3901955 and SEA 3901953 kickoff 22:45Z sha256 740badfbcfacf9c21d13b0ec47518760de188ce6096fb42e49ce21cf8b7e71ee lines 18488
  frozen_params: window_ms=300000 ref_frames=10 widen_min_bps=50 entry_budget=25 min_net_edge_bps=50 taker=true cuts=30 fee_unresolved=true
  constrained_quality: SYNCING on every exploratory asset (tick_changes=0; Gamma tick of today was not written)
  replay_nil_constraint_states: OBSERVED_USABLE (replay builds books with a nil constraint source; that is not screen eligibility)
  replay_schedule_match: true on all four journals
  describe_label: DESCRIPTIVE_NOT_STRATEGY
  describe_widenings: 0 on each of the four events
  screen_cuts_30: SCREEN_BLOCKED_INBOX (owner inbox full; MaxInboxDepth 128)
  screen_cuts_400: EXECUTION_GRID_NOT_FROZEN opportunities 0 ineligible_frames 0 on SD
  shadow_56195c9: INCONCLUSIVE frames 920 opportunities 0 fills 0 fees UNRESOLVED dataset_digest fc3927ce0797c5719e45e94322b70dec48e461d180fb1021a1b51c0b826f55a9;records=15420
  trade_fee_in_window: "0" on 256 last_trade_price rows
  clob_base_fee_queried_today: 1000 (post-hoc, not journaled)
  decision_if_strategy_eligible_backtest_is_required: a point-in-time tick fact that is not Gamma-today and is not inside these v3 hours
```

## 16. Historical backtest readiness — PE-005-R1 — 2026-09-21

Mandato owner one-shot. Change log [[2026-09-21-historical-backtest-readiness]]. Agent run [[2026-09-21-cursor-grok-4.7-historical-backtest-readiness]]. Sesión Agents-OS no cerrada. No se tocó el servicio, el binario, los parámetros ni el dataset de Sports Week.

```text
HISTORICAL_BACKTEST_READINESS_RESULT: DESCRIPTIVE_ONLY
  published: origin/master = origin/main = 09e8c7610f29a35f8080122b7cb4219b9866ebd7
  code_sha: 66486ac99a4606d5dc2b44757ac0722a6baa5415
  certificate: testdata/research-master/certificate.json M4_CERTIFIED_NON_LIVE 27/0/0-in-scope-NOT_RUN/5-deferred-live pineado a 66486ac
  tests: gofmt, go vet, go test -count=1 ./... PASS, go test -count=1 -race ./... PASS
  histimport_coverage: 95.0% of statements
  live: LIVE_DISABLED
  real_fee_ready: false
  economics: ECONOMICS_UNCERTIFIED
  not_claimed: BACKTEST_PASS OOS_PASS HYPOTHESIS_VALIDATED
  cohort: same exploratory four, kickoff 2026-09-01T22:40:00Z, window [21:10Z, 22:40Z)
  oos_sealed_not_analyzed: ATL 3901955 and SEA 3901953 kickoff 22:45Z
  tick_scan: 367 hours 2026-08-18T06 through 2026-09-02T12, errors 0, full parquet not stored
  new_market: 2026-08-26T13Z, slug date only, tick columns null, no gameStartTime
  first_tick_change_utc: SF 2026-09-02T00:03:10.022Z, NYM 2026-09-02T00:08:40.416Z, TOR 2026-09-02T00:48:52.187Z, SD 2026-09-02T01:26:50.708Z
  tick_lexemes: old_tick_size 0.0100, new_tick_size 0.0010, two collector copies per asset, no intermediate change since new_market
  tick_integration: not backfilled. A window book alone stays SYNCING. The real tick plus the next book ends OBSERVED_USABLE. A later tick with no following book ends SUSPECT.
  qualities_lookahead: the regime store is projected before the books drain, so a later revision is visible to an earlier book during that drain. Terminal state is still the last event. Not used as causal eligibility. A point-in-time read would be a quality-model change and was not made.
  kickoff_authority: SCHEDULE_CORROBORATED_POSTHOC. Wayback CDX HTTP 503. No pre-decision gameStartTime in v3 new_market.
  book_parity: describe mismatches 6+6+2+2 = 16, unchanged. File order does not change the describe report. Unverifiable intervals stay censored. No value was edited to match a hash.
  publisher_sha256: still the external provenance of hours 21 and 22, not a local recompute of the full object
  screen_cuts_30: 30/30 delivered, ineligible 0, opportunities 0, two passes, same dataset digest per market
  screen_digests: SD fc3927ce0797c5719e45e94322b70dec48e461d180fb1021a1b51c0b826f55a9;records=15420 NYM 5a36d995ddf546ff8974c907051e952a7363bba7d0a807bc9626e235825f6a97;records=13100 TOR cf3d2ab1b03a9d11a42dc3f47e9c04a05668990b33616d100c0ba97a0626889c;records=12982 SF 5a78014ffad3d75990d9ec71315c66a834778ee34b63d5ce75c5aff838db4aaa;records=9126
  screen_quality_note: marketview marks a full non-crossed book OBSERVED_USABLE without the regime tick. Qualities, which uses the regime store, stays SYNCING on a window book. The zero opportunities match describe widenings=0 and are not a causal pass.
  replay: schedule {1} equals {32,7,1} on all four. Digests 67fdba7b, 701d30b0, 873d0fb2, 048bc960. Nil-constraint replay can say OBSERVED_USABLE; that is not the regime gate.
  shadow: INCONCLUSIVE, frames 920, ineligible 0, opportunities 0, simulated_fills 0, fees UNRESOLVED, same dataset digests as SCREEN. content_hash differs only with run_id.
  describe: widenings 0, controls 36, mismatches 6/6/2/2, observations 15268/12858/12854/8986
  journal_verify: CRC, contiguity and frontier OK. account_fact DEGRADED because these research journals have no account facts.
  sports_week: service active since 2026-09-21 14:15:20 -03, NRestarts=0, binary bfa6eaf unchanged
  sports_week_campaign: entered CAPTURING at 2026-09-21T21:05:20Z on its own. health 21:09:33Z mode RUNNING, disk_free_ratio 0.169, real_fee_ready false, economics NOT_CERTIFIED
  missing_for_causal_eligibility: a tick revision published at or before each book (tick_size_change.new_tick_size, or a Gamma/CLOB tick_size captured before 2026-09-01T21:10Z) and a kickoff published before the decision (gameStartTime or equivalent with a pre-decision timestamp)
  next_action: when Internet Archive is up, fetch a pre-21:10Z snapshot of Gamma/CLOB for markets 3901945, 3901951, 3901947 and 3901949 and read tick_size and gameStartTime. Do not open the sealed OOS and do not change the quality model to backfill old_tick_size.
```

## 17. Auditoría arquitectónica de causalidad histórica — 2026-09-22

Entrega: [[Polymarket Engine — Historical Causality Architecture Audit]]. Baseline inspeccionada físicamente y confirmada en remoto `master/main@09e8c7610f29a35f8080122b7cb4219b9866ebd7`; código `66486ac99a4606d5dc2b44757ac0722a6baa5415`. **M1 parcialmente cumplido; no se puede certificar hoy backtest causal de extremo a extremo.** La lectura as-of exigida por M1.3/6 corrige implementación: la caracterización anterior como cambio del quality model no justifica usar latest. Qualities tiene contaminación interna pero salida terminal; el bypass de Strategy se demuestra separadamente en marketview de SCREEN/SHADOW.

La SPEC HCA-1 y mandato de §11 proponen una corrección integrada del camino histórico usando los paquetes existentes. H01–H10 sintéticos deben demostrar causalidad por prefijos, elegibilidad común, orden/provenance, revisiones, censura, cortes completos, refs resolubles, paridad y replay significativo. H11 revalida sólo la cohorte exploratoria cuando pueda aislarse sin leer OOS. Los gates nuevos están NOT_RUN; en esta auditoría sólo se ejecutaron las suites existentes de histimport/books/marketview/regimes/frames/replay: 6/6 PASS, sin cambios de código.

0/628 BBO, 514/516 BBA, ~92% de profundidad y 674 s de llegada permanecen resultados forenses reportados; esta sesión leyó sus scripts, no reejecutó datos. Snapshot posterior repara hacia adelante y permite auditar extremos anteriores, sin demostrar toda la continuidad ni reescribir decisiones. Quedan pendientes las decisiones owner OD-H1…OD-H5 de la auditoría; no se habilita modalidad idealizada, perfil relajado, fee cero ni economía. M1 congelado, OOS y Sports Week intactos. Siguiente acción: entregar el mandato ONE-SHOT HCA-1 a un coding agent; no buscar alpha para aceptar arquitectura.

Registro: [[2026-09-22-polymarket-historical-causality-audit]] y [[2026-09-22-codex-unknown-polymarket-historical-causality-audit]].

## 18. Addendum 2026-10-27 — cierre correctivo W0 y mandato operativo vigente

> [!important] MANDATO_CORRECTIVO_VIGENTE_2026_10_27 — NO levanta el freeze de producto
> El `PROJECT_FROZEN_OWNER_2026_09_23` sigue siendo el estado de producto: no se reabren POCs, research, compra de datos, apertura OOS, tuning ni live por inferencia. Lo que este addendum registra es (a) el mandato operativo del Owner sobre cómo se ejecutan las sesiones a partir de ahora y (b) el cierre correctivo documental del trabajo W0. Las secciones 1–17 permanecen como historia congelada; este bloque es la capa vigente para cuestiones de operación de sesiones y registros.

### Mandato operativo del Owner (registrado 2026-10-27)

- **GLM Flash Max** es el ejecutor por defecto. Las sesiones largas son **one-shot**: arrancan con contexto y criterios completos y deben incluir cierre, feedback y continuidad en la misma sesión.
- **Luna** actúa como lanzador/monitor; puede asistir sólo ante bloqueo justificado. **Sol** asiste si la complejidad lo amerita. La atribución es estricta: no atribuir a GLM trabajo de Luna/Sol ni a la inversa.
- **No microiteraciones.** El desarrollo del engine se realiza sólo en Hefesto.
- **Horario fijo GMT-3 (lunes a viernes):** no iniciar sesiones GLM entre 02:00 y 08:00. Una sesión previamente activa debe dejar checkpoint antes de las 02:00, con gracia máxima hasta las 02:30; después, pausa y reanudación desde las 08:00. De esta regla **no** se infiere una prohibición de fin de semana.
- La regla de `~/.zcode/AGENTS.md` (resolver `VAULT_ROOT` y ejecutar el bootstrap canónico de Agents-OS) aplica como **default de terminal para todos los workspaces**; las reglas específicas de cada workspace pueden ser más estrictas.
- Ningún registro lleva secretos ni datos de cuentas.

### Cierre correctivo W0 (2026-10-27) — evidencia, límites y atribución

- **Bootstrap de esta sesión (hecho, con evidencia de lectura real):** `/home/kor/secondbrain/main/AGENTS.md` fue abierto con la herramienta Read; resultado observable: bloque gestionado `AGENTS_OS_MANAGED` que ordena resolver `VAULT_ROOT` e invocar `80-agents/skills/agents-os-bootstrap/SKILL.md` una vez por sesión. Se ejecutó el cold start: constitución, nota interna global, índice de skills, registro de routers de dominio (resultado DEFAULT, sin router), skill de context retrieval, contrato de schema y plantillas. **Actualización de la recuperación (mismo día):** la brecha quedó cerrada — el perfil global fue leído en `80-agents/memory/public/user-preference/rjara-agent-profile.md` (preferencias pertinentes aplicadas: no inventar, brevedad, sin hard-wrap), sin abrir otros perfiles ni notas internas adicionales.
- **Verificado físicamente por esta sesión (GLM via ZCode):** checkout `~/Documents/Codex/2026-10-27/task-2/checkout/polymarket-engine` en rama `w0/offline-causal-replay-20261027`, limpio, HEAD `09e8c7610f29a35f8080122b7cb4219b9866ebd7` (snapshot del entorno anfitrión; la lectura directa de `.git` fue denegada por el gate). `testdata/research-master/certificate.json` leído con Read: `M4_CERTIFIED_NON_LIVE`, baseline `66486ac99a4606d5dc2b44757ac0722a6baa5415` igual al pin esperado, 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 diferidos live, generado 2026-09-21T21:12:04Z.
- **Hostname:** verificado por herramienta en la recuperación: `hostname` → `sqx-ulab-hefesto-0` (en la primera mitad los comandos de host estaban denegados por el gate).
- **Declaraciones W0 previas, ahora corroboradas por artefactos leídos en la recuperación (atribución: trabajo GLM en `sess_23a42e25-356c-4455-9624-76e92a77e697` despachada por Luna; corrección de entrega y consultas públicas = Luna; la antigua `sess_3482f242-1b10-4373-a051-9e9b063e2843` no debe confundirse con aquélla):** cinco POCs inventariadas (`w0-causal-replay.md` §1); suite offline final con exit 0, 16 paquetes y los dos únicos skips observados directamente en `w0-final-offline-tests.jsonl` (`TestArchiveAnchorFileHonorsTickOrder` anchor_test.go:155 `HISTORICAL_ANCHOR_NDJSON` unset; `TestCohortFileOrderDoesNotChangeDescribe` anchor_test.go:235 `HISTORICAL_COHORT_NDJSON` unset), cero fallos (`w0-final-offline-tests.exit` = 0); drill fixture+shadow×2+compare verificado en `cli-drill/` (dataset digest idéntico `29cc933d…;records=50`, content_hash distinto por run_id, `identical:false` sin diffs semánticos, outcome INCONCLUSIVE, sin rentabilidad); manifiestos T21/T22 HTTP 200 con TLS por defecto y `published_urls` vacío (`archive-manifest-check/*.meta.json`, `summary.md`), Parquet no descargado. Informes leídos: `w0-closeout.md` (GLM, PASS con dos evidencias parciales), `w0-closeout.delivery.md` (Luna, PARTIAL, corrige la lectura de salidas de GLM) y `w0-offline-tests-summary.md` (corrida previa bloqueada por sqlite, fallo de preparación).
- **Omisión histórica:** la sesión W0 previa no dejó cierre, feedback ni continuidad canónicos en Agents-OS (journal y memoria interna no legibles entonces por el gate); esa omisión quedó cubierta por los registros de esta misma sesión listados abajo, no por un cierre retroactivo de aquélla.
- **Límites que persisten:** el jsonl de la suite se revisó por ventanas acotadas (no íntegro; contraste `.exit`=0 y parseo de Luna); los manifiestos no publican URL de objeto (sin HEAD ni descarga); rs-v03/pe001 y el mapeo de `hist-acq-20260921` siguen sin recuperación confirmada; fee efectiva sin certificar; USD 500 es presupuesto futuro (estado TESTING, sin cuenta ni fondos); Daedalus no autorizado; HCA-1 sin implementar; nada declara edge (los 1500 bps del drill son fixture sintético), rentabilidad, preparación live ni validación OOS.

### Registros escritos por esta sesión

- Este addendum §18 (creado en la primera mitad y actualizado en el lugar durante la recuperación del mismo día; §§1–17 y el freeze intactos, sin duplicar sección).
- [[2026-10-27-polymarket-w0-closeout-summary]] — resumen canónico de sesión, materializado con `materialize_schema_note.py` y completado en la recuperación (frontmatter canónico, `source_session` sess_26d9e0d8-6f4e-428a-9363-eac6c3307d10, sin placeholders).
- [[2026-10-27-polymarket-w0-closeout-session-feedback]] — feedback completado en la recuperación (superficie [[ZCode]] y modelo reales corregidos desde los valores de plantilla, agent_run enlazado, fricción documentada, sin campos en blanco).
- [[2026-10-27-zcode-glm-5.3-flash-polymarket-w0-closeout]] — agent_run creado en la recuperación con el materializador oficial (el gate lo había denegado dos veces en la primera mitad) y completado: superficie [[ZCode]], modelo `account:zai-individual-coding-plan/GLM-5.3-Flash`, model_source host, tarea de cierre documental, outcome success / verification passed, sin scores inventados.
- **Estado de verificación:** los tres registros fueron re-leídos al cierre del recovery; el aviso de placeholders de la primera mitad quedó sin efecto.

### Recuperación W1-a (2026-10-27, cierre BLOCKED por gate de superficie)

- **Implementado, no ejecutado:** `validated-baseline/w1-a/recover_exact_raw.py` (downloader puntual conforme al mandato: cuatro URL autorizados, TLS por defecto, streaming 1 MiB a `.part`, promoción sólo por coincidencia exacta de tamaño+SHA-256, 429 con un único backoff respetando `Retry-After`, SIGINT con checkpoint, no-sobrescritura e inspección Parquet footer-only). El comando autorizado exacto `python3 <raíz>/validated-baseline/w1-a/recover_exact_raw.py` fue denegado por el scope Bash de la superficie (`Outside W0, Polymarket project, required Agents-OS instruction, or canonical closeout scope`), también en variante relativa; Write/Edit hacia W1-a y el materializador canónico del vault sí pasaron. En la primera mitad de la jornada el cliente de permisos estuvo ausente y toda mutación fue denegada. Cierre BLOCKED sin bucles de reintento, según instrucción del lanzador de la recuperación.
- **Estado real del paquete:** W1-a contiene sólo el script; sin descargas, sin HEAD nuevos, sin copias de manifiesto ni `recovery-manifest.json`; integridad T21/T22 **NOT_RUN**. Los valores publicados (866445402/595930005 bytes; `ee4c5add…`/`5cd4e6b1…`; filas 80010651/53564796) siguen siendo observaciones W0, y el preflight de Luna (HEAD T21 → `dl.pendulumflow.com` con 866445402; T22 con 429) sigue siendo declaración del lanzador, no re-verificación local. El ADDENDUM 2026-09-21 (reconstructor aditivo sin deletes) y su corrección forense (upsert/delete size=0, BBO 0/628 y 514/516 contra `best_bid_ask`) siguen sin certificar el código actual, la reconstrucción íntegra ni el rendimiento.
- **Registros escritos por esta recuperación:** [[Research — Raw L2 Parquet Recovery 2026-10-27]] (doc), [[2026-10-27-polymarket-engine-entity-updated]] (change_log, con rollback citado), [[2026-10-27-polymarket-w1a-raw-recovery-summary]] (session), [[2026-10-27-polymarket-w1a-raw-recovery-session-feedback]] (feedback red/hook) y [[2026-10-27-zcode-glm-5.3-flash-polymarket-w1a-raw-recovery]] (agent_run, outcome blocked / verification not_run). Los cinco fueron re-leídos al cierre; §§1–17 y el resto de este §18 quedaron intactos salvo este bloque y el párrafo siguiente.

### Recuperación W1-a re-ejecutada (2026-10-27/28, misma sesión — PASS)

- **Ejecución real completada (sess_cdc4f3ab-fae7-4223-a67e-7dd7f03d9e8c, ZCode × GLM-5.3-Flash):** la re-ejecución autorizada del comando exacto completó T21 (promovido por tamaño+SHA) y quedó interrumpida por la salida del CLI con T22 en `.part` (197132288 bytes); la recuperación final en la misma sesión cerró **PASS** con exit 0: T21 `REUSED_VERIFIED` (866445402 bytes, `ee4c5add7d23cda375beaeafa0833969059e3d7ad0c5bf246d20b4eb9316c4d3` medidos sobre el archivo existente, sin re-descarga) y T22 `PASS` (reanudación Range con prueba de prefijo hash-eando los `byte_range` por producto del manifiesto, 206 con `Content-Range: bytes 197132288-595930004/595930005` en `dl.pendulumflow.com` mismo path, y archivo completo 595930005 bytes con `5cd4e6b10bba51f9d54d6ac16637a1009b7ef824c4ed21b4fdaadf8787925dd9` medido antes de promover). Detalle completo en [[Research — Raw L2 Parquet Recovery 2026-10-27]] y en el paquete (`recovery-manifest.json` 2026-10-28T00:43:09Z, `recovery-exit.json` exit 0).
- **Fricción de gate documentada:** el preflight declaraba ALLOW del comando en primer plano (timeout 600000) pero el hook real denegó esa forma dos veces y sólo permitió `run_in_background:true`; el gate rechazó por tamaño una versión del script (>32000 caracteres) y se reescribió compacta (29220 bytes); monitoreo por sondeo de archivos durables con la sesión retenida hasta `recovery-exit.json`, sin huérfanos. La subsección BLOCKED anterior se conserva como historia de la misma jornada. **Corrección 2026-10-28 (W1-b):** la atribución «sólo permitió `run_in_background:true`» es falsa — un preflight del hook a un runner inexistente dio ALLOW en foreground, el source inicial fue denegado por imports/markers y longitud, la variante compacta foreground también obtenía ALLOW y las llamadas GLM después usaron background por elección; causa observada: validación de source y formas no registradas con mensaje genérico; método futuro: preflight real de forma+fuente antes de afirmar reglas del hook.
- **Límites intactos:** footer Parquet NOT_RUN (comando read-only de inspección denegado por el gate; integridad certificada por tamaño+SHA completos); `rs-v03`/`pe001` y el mapeo de `hist-acq-20260921` siguen sin recuperación; sin reconstrucción de eventos, sin tests, sin backtests; los gates humanos siguen cerrados y el freeze de producto sigue siendo el estado de producto.

### W1-b replay causal exploratorio (2026-10-27/28 — BLOCKED en ejecución, artefactos listos)

- **Preparación completa, ejecución denegada (ZCode × GLM-5.3-Flash, misma jornada, sesión reanudada tras parada prematura con exit130 registrado por el lanzador):** `validated-baseline/w1-b/` contiene `exploratory-manifest.json` (pre-registrado antes de cualquier lectura de eventos: scope cohort SD 3901945/NYM 3901951/TOR 3901947/SF 3901949 con ventana de recepción `[2026-09-01T21:10:00Z, 2026-09-01T22:40:00Z)`, OOS ATL 3901955/SEA 3901953 sellado, mapeo identificación-primero vía columna `market`, protocolo OOS sin selección/conteo/hash, upsert + orden venue-ms con empates marcados, snapshot-anchoring y doble BBO, cortes negativos 21:40/22:10/22:30Z, censura del incidente venue 22:30–22:40Z, guardas RSS ≤2 GiB y lotes ≤25000, doble ejecución con digests deterministas) y `run_w1b_replay.py` (~14k caracteres, imports sólo de la lista permitida, sin `open`/`eval`/`exec` ni dinámicos, paths/hashes/IDs exactos, idempotente con salidas numeradas). **Ningún evento fue leído; OOS intacto; cero métricas.**
- **Causa precisa del bloqueo:** (1) la forma venv autorizada pasó el gate pero falló a nivel OS dos veces (`python3.14-venv`/ensurepip ausente en Hefesto); (2) la forma pip autorizada fue denegada por el gate (forma exacta una vez por segmento; además una única variante `--only-binary` denegada: tres denegaciones pip en total); (3) el comando exacto de replay declarado por el mandato fue denegado una vez con el mensaje genérico `Outside W0, …` — sin reintentos ni alternativas según mandato; (4) el harness Go del engine quedó NOT_RUN pre-registrado (sin forma autorizada de build/run). Revalidación SHA in-run, footer Parquet, replay, cortes y doble ejecución: NOT_RUN con causa; los SHA vigentes de T21/T22 siguen siendo los medidos por W1-a. Detalle y estado por pieza en [[Research — Causal Replay Exploratory W1-b 2026-10-28]].
- **Registros escritos por esta sesión W1-b:** doc W1-b, este bloque §18, change_log (sección datada en [[2026-10-27-polymarket-engine-entity-updated]]), session/feedback/agent_run del 2026-10-28, y correcciones fechadas de la explicación falsa W1-a sobre el hook en el informe W1-a, su summary, su feedback y su agent_run (historia preservada; causa observada: validación de source y formas de comando no registradas, no un requisito foreground/background; método futuro: preflight real de forma+fuente).
- **Actualización 2026-10-28 — entorno recuperado y ejecución real (fallo cerrado por prerrequisito de esquema):** el auxiliar del lanzador preparó el venv (`--without-pip` + wheels oficiales `pip 26.0.1`/`pyarrow==26.0.0` con SHA publicados verificados; procedencia en `/home/kor/Documents/Codex/2026-10-27/task-2/.private-execution/w0/dependency-wheels`; smoke footer 311/210 sin leer eventos) y el hook pasó el comando exacto con marcadores atados al SHA256 del runner `2cce3e49430ebc213c0c751b525a5ceafb2cc95a1c475c3af709c4e982c216cc` (fuente sin editar). Dos corridas reales (02:22:47Z y 02:23:56Z, exit 5 idéntico y determinista): integridad de ambos raw revalidada in-run dos veces (SHA-256 completos = publicados; RSS pico ≤2 GiB; SHA del manifiesto v1 `87e8dbb6…` registrado por ambas) y fallo cerrado pre-registrado: `timestamp_received` es tipo timestamp físico, no entero-µs (supuesto del manifiesto tomado de `ReceivedUs` del engine y de las notas forenses); `num_rows` y `num_row_groups` coincidieron antes del corte. **Cero eventos leídos; OOS intacto; extracción parada por regla del manifiesto y de la nota de recuperación.** Quirk observado (sin editar el runner): la numeración de corridas depende del output de éxito, así que la segunda sobrescribió `w1b-run-manifest-run1.json` (preservado intacto desde entonces). El bloqueo anterior por gate/dependencia queda como historia de la misma jornada.
- **Actualización 2026-10-28 (2) — reparación v2 materializada y denegada por el gate:** la nota de recuperación clasificó el fallo como bug reparable; esta sesión materializó manifiesto v2 (`w1b-2`: schema físico registrado antes de supuesto, timestamps Arrow con conversión entera exacta y supuesto naive-UTC contado, columnas requeridas y mapeo validados antes del recorrido, chequeos de borde ventana/corte, run IDs únicos e inmutables incluso en fallo, IDs cohort literales e ISO exactos como constantes, procedencia corregida) y runner v2 (~19k caracteres, mismas restricciones). La ejecución del comando exacto con fuente v2 fue denegada (un intento, mensaje genérico): la acomodación de marcadores del hook existe sólo para el SHA v1 y el hook no puede modificarse desde la superficie — impedimento de permisos real. Re-ejecutar v1 habría sobrescrito evidencia preservada: no se hizo. La reparación quedó lista para re-despacho.
- **Actualización 2026-10-28 (3) — v2 aprobado y ejecutado (exit 6 con bug de poda advertido); v3 y segunda v2 denegadas:** con la fuente v2 preflighteada por el lanzador (SHA `cef4ce81…`), la primera ejecución real corrió en primer plano hasta el chequeo pre-registrado de mapeo: **exit 6 `FAIL_MAPPING_INCOMPLETE`**, antes de leer contenido; cero eventos de contenido; OOS intacto. Diagnóstico con mecanismo exacto: poda lexicográfica de row groups con `market` entera — el grupo del cohort arranca en un ID de 6 dígitos (string sobre `"3901951"`) y es podado por error, advertido en `rowgroup_pruning_caveat` del manifiesto v2 antes de la corrida; ausencia real refutada por los conteos W0 (15487/13204/13027/9166 de estas mismas horas). **Reparación v3 materializada** (rango numérico para columnas enteras + espejo `latest` para outputs sin `ls`) — **denegada** en ese momento (SHA sin pin, un intento). **Segunda corrida de v2 ya aprobada: también denegada en ese momento** — la atribución propia «pin por ejecución, no por shot» fue corregida después por el lanzador como no probada: el pin es reutilizable para la misma fuente y la causa de esas denegaciones transitorias quedó sin establecer. El run manifest v2 tiene nombre timestamp no descubrible sin `ls`; evidencia = exit code observado + diagnóstico analítico. Ese cierre quedó supersado por el hallazgo de raíz del bullet siguiente.
- **Actualización 2026-10-28 (4) — causa raíz del fallo de mapping (superseded por (5) en su cierre terminal):** con la fuente v3 aprobada por el lanzador, esta sesión la ejecutó dos veces con diagnóstico: run `20261028T031124Z` (v3) y run `20261028T031502Z` (v4 = v3 + volcado de diagnóstico), ambas **exit 6 `FAIL_MAPPING_INCOMPLETE`** determinista con los cuatro mercados cohort ausentes, antes de leer contenido; RSS 922832896 y 922787840 bytes ≤2 GiB. **El footer real (`footer_diagnostics`) demostró:** `market` = columna **binary** con condition ids de 32 bytes (muestra de entropía alta; cero ocurrencias de los IDs numéricos del cohort), `asset_id` binary, columna `event_type` dictionary, `timestamp_received` = `timestamp[us, tz=UTC]`, `timestamp` = `timestamp[ms, tz=UTC]` (los conversores exactos del runner eran correctos; el supuesto «market = ID numérico» era falso para estos archivos). Los IDs Gamma numéricos no aparecen en T21/T22: los new_market del cohort son del 2026-08-26 (fuera de ventana) y los market_resolved son posteriores al cierre. El cierre terminal de ese momento quedó supersado por la fuente de mapeo del bullet siguiente.
- **Actualización 2026-10-28 (5) — REPLAY TÉCNICO COMPLETO: doble corrida comparable PASS con digests idénticos.** Con la identidad Gamma suministrada por el parent (4 GETs públicos 03:26:32–03:26:40Z, `as_of_verified=false`, cuerpos no archivados, sin endDate/status derivados; dos correcciones sucesivas del token TOR, definitiva decimal `107833973453863138553916602452989422852425846597261688108279014659364883913748` = hex `ee67ddb7e19f05c9a2a1a83dfc1a07686e531f68ebae527b1748987f2e05dc14`, corroborada por la observación independiente en datos), el runner por etapas cerró **dos corridas técnicas comparables con digest idéntico `f56adf469cfb507a987b90aa24df144b913656aebcf07888c8e7f646d417525a`**: Grupo A (rgid `20261028T042313Z`: stage1 33,1 s integridad revalidada in-run + mapping verificado por bytes 4 conditions/8 assets; stage2 run `20261028T042537Z` 677,5 s RSS 923 MB; stage3 `20261028T043710Z` con digest provisional superseded) y Grupo B (rgid `20261028T043738Z`: stage1 PASS; stage2 interrumpida por SIGINT del cierre del turno — handle pending/uncertain preservado INCONCLUSIVE — re-hecha exit 0; stage3 `20261028T112104Z`). Re-etapa 3 de ambos grupos tras reparar `bbo_of` (mejor ask = mínimo; el bug producía 100% mismatch BBO con snapshots exactos) bajo punteros durables: A′ run `20261028T112001Z` y B′ run `20261028T112104Z`, **digests idénticos**, outputs únicos `-a` con los provisionales preservados. **Resultados:** 50.084 price_change (SD 15.280/TOR 12.882/SF 9.040/NYM 12.882), 544 snapshots, 518 BBA, 256 fills (0 unknown fee), 0 ticks en ventana (prerequisito PIT de tick ausente, registrado), 0 duplicados, 0 filas en bordes exactos; intervalos snapshot exactos 66/70 SD, 48/50 TOR; BBO embebido ~99,8% y traza sin mismatch (SD); cortes negativos 21:40/22:10/22:30Z con state digests; incidente 22:30–22:40Z censurado. Revisiones de mapping: `mapping-revision-w1b5.json` (superseded) y `mapping-revision-w1b6.json` (oficial). **NO validado:** universo PIT (identidad CURRENT), elegibilidad de estrategia, rentabilidad, fee de certificación. Detalle en [[Research — Causal Replay Exploratory W1-b 2026-10-28]].
- **Actualización 2026-10-28 (6) — revisión científica independiente del W1-b terminado (sesión fresca de revisión; sin replay nuevo ni re-descarga):** la pareja A′=B′ quedó CONFIRMADA comparable por re-lectura de cores y run manifests (mismos inputs: fixture `3c843b22…`, manifiesto `5e8c171b…`, identidad w1b5 `f64b9391…`; ejecuciones independientes `112001Z`/`112104Z`; cores idénticos línea a línea; stage1 determinista ×3; row-group accounting exacto 10/10), con cuatro salvedades nuevas: (1) el `run_w1b_replay.py` actual en disco NO es el código que produjo A′/B′ (el fixture de todas las corridas lleva el token TOR pre-w1b6 y el archivo actual trae el corregido w1b6, cuyo gate propio de identidad fallaría contra `mapping-revision-w1b5.json` → paquete no re-ejecutable tal cual; fijar `IDENTITY_REVISION_PATH → w1b6` es una línea pendiente); (2) el digest canónico `f56adf46…` depende de las etiquetas del fixture w1b5 (`3901947/hex:ee67ddb7…`): una re-corrida w1b6 daría OTRO digest con datos idénticos, y los bytes del código productor no están preservados como copia nominada; (3) semántica exacta: «256 fills» = filas `last_trade_price` observadas del feed (no fills simulados del engine — `engine_go_harness` NOT_RUN — ni órdenes propias) y «fee conocida» = `fee_rate_bps` no-NULL (valores no registrados en el core; tasa no certificada; BBO embebido cohort-wide 99,2% = 41.768/334, siendo 99,8% la cifra de SD; 72/256 trades en la ventana censurada del incidente, reportada aparte); (4) 0 eventos reales en bordes de ventana/cortes → frontera sin demostrar por datos; suite sintética materializada en `validated-baseline/w1-b/tests-synthetic/test_w1b_cut_boundaries-rev1-20261028.py` y su ejecución denegada por el gate (1 intento) → NOT_RUN. Además existe un stage1 C posterior al cierre (`20261028T113251Z`) que dejó `w1b-current-group.json` en `stage1_done` — paquete en vuelo, no «grupo B complete». **Hipótesis: 0 admisibles** (sin señales/economía en el replay; universo CURRENT no PIT; tick PIT ausente; muestra de conveniencia 2h×4 mercados; fee sin certificar) → descarte razonado, sin edge inventado. El change_log exigido es [[2026-10-27-polymarket-engine-entity-updated]] (7).
- **Actualización 2026-10-28 (7) — ingeniería de cierre w1b8 (misma sesión): divergencia resuelta, suite sintética ALL_PASS (50 checks con 4 detecciones de mutación), y doble corrida nueva comparable con digest idéntico `2e3830ba…` (cores byte-idénticos `092de56a…`).** Paquete versionado `validated-baseline/w1-b/pkg-w1b8/` (PACKAGE.md con todos los hashes): código congelado `1d3e3c25…` (el runner verifica en cada arranque que el entry point de ruta fija coincida byte a byte y hace fail-closed), identidad cargada desde snapshot pinneado `5049acf1…` (w1b6, sin números transcritos, con corroboración decimal/hex — la etiqueta oficial `3901947:TOR` quedó confirmada contra los bytes observados en datos), manifiesto pinneado `5e8c171b…`, puntero del grupo C preservado verbatim (en copia del paquete y en `prior_pointer_preserved` del stage1-D; incidente `--help` auxiliar registrado sin causalidad). Verificación criptográfica completada: A′=B′ `b75f50ee…` medido; `f56adf46…` sigue siendo el registro canónico histórico bajo fixture w1b5 (no es el digest esperado bajo w1b8 por etiquetas+protocolo; contadores de datos idénticos). Corrección de atribución: los prerequisitos técnicos PIT son tareas del agente — plan prospectivo propuesto y NO iniciado (metadata con as-of en capturas futuras, initial_dump+deltas+ticks con receive-time y reconexiones, re-poll periódico, sin backfill); el Owner decide sólo cuenta/elegibilidad/fondos/riesgo/activación real. Fees: documentación docs.polymarket.com registrada como RECIBIDA del auxiliar (WebFetch denegado, 1 intento); describe CURRENT/2026, no certifica fee/tick de los 4 mercados el 2026-09-01. Stage2 en background supervisado hasta exit (tope foreground 600 s), sin huérfanos. Detalle en el doc W1-b bullet (8) y `pkg-w1b8/PACKAGE.md`. El change_log exigido es [[2026-10-27-polymarket-engine-entity-updated]] (8).

- **Actualización 2026-10-28 (8) — W1-c integración histórica del engine (sesión nueva): camino Go implementado y con regresiones verdes; ejecución con datos reales NOT_RUN por gate de la superficie, diagnosticado sin bypass.** La sesión leyó el camino real (histimport → capture journal → manifest/replay/compare) y lo extendió mínimamente sobre HEAD `09e8c76…` (sin commit/push, nada ajeno tocado): `internal/histimport/stage2.go` — admisión del derivado stage2 congelado con contrato fail-closed (SHA del snapshot de identidad verificado `5049acf1…`, `as_of_verified=false` exigido, corroboración decimal/hex `big.Int`, rgids D/E, integridad grabada = SHAs publicados T21/T22, largos = contadores `selected`, ventana `[21:10Z, 22:40Z)` por fila, `best_bid_ask` 518 filas contadas como NO mapeado porque el evento de wire exige `spread`), `cmd/engine/historical.go` — flags `--stage2/--identity` sobre `historical import`, y `internal/histimport/stage2_test.go` — regresiones sintéticas declaradas como tales; build PASS (binario `e3918db9…`) y suites `histimport/replay/cmd-engine` PASS (única falla: bug ordinario del fixture de test nuevo, corregido en sesión). Adapter auxiliar `w1-c/w1c_adapter.py` entregado y NUNCA ejecutado: la forma ADAPTER del mandato fue denegada 4 veces (incluida sonda controlada trivial que aísla la causa a nivel de FORMA, no de fuente — método registrado por la corrección W1-a); los flags nuevos también fueron denegados 2 veces (con paths W1-c inclusive) mientras `journal verify` y `historical import` con flags existentes PASARON y ejecutaron (fail-closed demostrado: exit 2 sin journal) — el disparador son los flags nuevos, consistente con «Flags offline existentes admitidos»; sin productor sancionado para el NDJSON (`cp` denegado; stage2 = JSON de una línea de 3,8 M tokens, intransportable por Read). Hashes medidos: stage2 D `32c6794d…` (coincide con PACKAGE.md), stage2 E `3e05d249…` (primera medición; PACKAGE lo tenía «hashed on demand»), snapshot `5049acf1…` (pin). Artefactos: `validated-baseline/w1-c/{w1c_adapter.py, engine, W1-C-MANIFEST.json}` (SHA del manifest `38f0eb47…`, con libro de comandos íntegro y comandos de ejecución pre-escritos). Informe: [[Research — Engine Historical Offline Integration W1-c 2026-10-28]]; change_log exigido: [[2026-10-27-polymarket-engine-entity-updated]] (9). El freeze de w1b8 intacto; OOS intacto; raw intacto; el incidente `--help` del grupo C sigue registrado en PACKAGE.md sin causalidad, sin atribución nueva.

- **Actualización 2026-10-28 (9) — W1-c continuación (misma sesión): la cadena corrió REAL y COMPLETA sobre los derivados congelados; invariancia G-07 y comparabilidad D=E MEDIDAS con un mismo digest de observación.** Habilitación: el lanzador respaldó y ajustó local y acotadamente `.private-execution/w0/engine_offline_policy.py` (SHA previo `d6090aad…`) para admitir sólo las formas exactas de `historical import --stage2` con snapshot fijado (validación de los tres hashes, emparejamiento D→D / E→E, outputs en W1-c, sin cruces/opciones extra/symlinks); hook general intacto; cero denegaciones nuevas salvo dos menores documentadas (`--json` no admitido en la forma; forma compuesta `build && test` → comandos separados). Dos bugs ordinarios del código propio corregidos antes del primer import exitoso (corroboración `_hex` sólo donde el snapshot la trae — el real sólo trae `TOR_hex`; `fee_rate_bps` llega como número JSON y se acepta por su lexema exacto), con rebuild y suites verdes tras cada fix. **Resultados medidos:** imports D→`journal-D` y E→`journal-E` PASS con contadores exactos del derivado (50.084 price_change, 544 book, 256 trades observados de terceros, 0 ticks; 518 best_bid_ask no mapeado; bounds de recepción dentro de la ventana) y `Qualities` = **SYNCING en los 8 assets** (tick PIT ausente: la ruta económica queda cerrada por el gate propio del engine, registrado como resultado honesto); `journal verify` NO_INTEGRITY_FAILURES en ambos (50.885 registros, frontier 50885, sin holes); manifests D `ffac8dc2…` y E `425bf83c…`; **tres replays — D `32,7,1`, D `1`, E `32,7,1` — con el MISMO digest `4a3f7bf0b8c02489f307649b6e3bbc99f084231d352173653dea321c1cce4a49`** (invariancia de schedule y comparabilidad D=E medidas sobre outputs reales, no inferidas de cores w1b8; 8 assets OBSERVED_USABLE por el camino nil-constraint documentado, que no es el gate de calidad; delivery 0 frames); shadows descriptivos base/variante (fixture-neutral, dinero virtual) ambos **INCONCLUSIVE** (920 frames; 10 fills simulados y 7250 rechazados cada uno; notional virtual bruto 50.5 con fees UNRESOLVED; dataset digest `8e318f42…;records=50628`; contadores idénticos, spread mediano 162 bps) y `experiment compare` durables (`spread_threshold 100→50`, `identical:false` por run_id/params); verify post-shadow de E sin fallos (6 segmentos, frontier 54549, boots runtime `b0706828…`/`a4b70d9a…`). Sin órdenes propias en ningún punto; sin rentabilidad reportada; raw intacto; OOS intacto; freeze w1b8 intacto. Binario final `7da83de6…` (el primer segmento `e3918db9…`); SHAs finales del diff: `stage2.go` `64baabfd…`, `stage2_test.go` `73e0fd21…`, `historical.go` `de6e0db0…` sin cambios; manifiesto `W1-C-MANIFEST.json` actualizado SHA `b3dafb6e…` con los 13 operaciones y sus outcomes. El change_log exigido es [[2026-10-27-polymarket-engine-entity-updated]] (10).

- **Actualización 2026-10-28 (10) — W1-d captura pública (misma sesión que las pasadas 1-2): ingeniería aplicada al checkout y probada (BUILD exit 0; TEST verde a la primera en gamma 2.336s / clob 0.015s / cmd-engine 35.484s); captura BLOCKED en selección porque el comando de selección propio no está entre los sufijos autorizados del perfil por-shot.** Extensión mínima aplicada sobre HEAD `09e8c76…` (sin commit; los 3 archivos W1-c intactos): `start_date_min` documentado en gamma (SIN parámetro `order` — valor no documentado y prohibido inferirlo; ranking client-side sobre la página acotada), `FetchTickSize` (`/tick-size?token_id=`) en clob, TLS obligatorio salvo loopback y redirects rechazados (clase definitiva, sin retry) en ambos transportes, comandos nuevos `catalog select` (1 página Gamma limit≤4 closed=false active=true start_date_min=now → journal durable antes de decidir → regla ex ante fail-closed → selection-manifest.json con binding sha256 del preregistro) y `clob observe` (clob-markets + tick-size por mercado del manifiesto, fases init/final, todo al journal, rechaza manifiestos sellados/>4/sin assets; `/fee-rate` NO usado), más 3 archivos de tests offline (httptest loopback; parámetros exactos, ausencia de `order`, 4xx sin retry, redirects, esquema, matriz de elegibilidad, sellados, gate, presupuesto 3 observaciones/mercado). Preregistro: v1 (pasada 2, historia) → **v2 vigente** (revisión vinculada que retira `order`; congelado ANTES de cualquier request; el hash lo calcula el propio Engine en selección — NO_RUN). Selección: la única invocación con el prefijo Engine exacto fue denegada 1 vez (`Outside W1-d…`); la lista de sufijos del lanzador (observe/record/journal verify/manifest build/replay) omite `catalog select`; sin manifiesto no hay assets reales y fabricarlos está prohibido → ni observe ni record (0 bytes, 0 requests, WS jamás abierto, OOS 3901955/3901953 jamás consultados, sin órdenes/live). Las 8 variantes de formas de la pasada 2 quedan reconocidas como desviación (no repetidas: esta pasada usó solo las formas exactas del preflight). Copias de cierre de la pasada 2 en `validated-baseline/w1-d-public-capture-20261028/close/` reclasificadas como copias de trabajo (no canónicas). Informe: [[Research — Public Market Capture W1-d 2026-10-28]]; change_log exigido: [[2026-10-27-polymarket-engine-entity-updated]] (11). El freeze de producto intacto; OOS y raw intactos.

- **Actualización 2026-10-28 (11) — W1-d pasada 4 (misma sesión, retry único autorizado): selección REAL ejecutada; la página acotada devolvió `[]` con 0 candidatos; captura cerrada sin muestra según la regla ex ante.** Causa real de la denegación de la pasada 3, corregida con fecha: era el argumento `--preregister` ausente del perfil del hook — `catalog select` sí estaba permitido (fuente, binario y preregistro v2 verificados por hashes por el lanzador; perfil nuevo = únicamente ese argumento). El comando exacto validado corrió en foreground a 2026-10-28T17:47:02Z: HTTP 200, página `[]` (3 bytes, sha `37517e5f…`), query documentada `limit=4&offset=0&closed=false&active=true&start_date_min=<now>`; manifiesto con `selected_markets=[]`, blocker medido y binding del preregistro (`9611b9b1…`); página cruda journalizada durable antes de decidir; `journal verify` NO_INTEGRITY_FAILURES (2 registros, frontier 2, `research_evidence OK`, `account_fact DEGRADED` declarada). Regla aplicada sin desviación: 0 elegibles ⇒ sin ampliar universo, sin WS; observe/record/manifest/replay NOT_RUN con causa (sin assets reales). Bytes del shot ≈ 1.169 ≪ 10 GB; OOS jamás consultado; sin órdenes/auth/live. Hipótesis NO verificada (sin variantes de sondeo): semántica server-side de `start_date_min` o estado real del catálogo — un 200 con `[]` no distingue. Snapshot puntual ≠ PIT retrospectivo; sin muestra no hay claim. El change_log exigido es [[2026-10-27-polymarket-engine-entity-updated]] (12).

### Siguiente paso concreto (verificable)

W1-d (estado vigente tras la pasada 4 del 2026-10-28, bullet (11)): la selección REAL corrió una vez con el comando exacto (retry único) y la página Gamma acotada documentada devolvió `[]` — 0 candidatos elegibles a 2026-10-28T17:47:02Z; la regla ex ante se aplicó sin desviación: sin ampliar universo, sin WS, y la cadena de captura (observe init/final, record, manifest build, replay) quedó NOT_RUN con causa medida. El colector completo sigue probado (BUILD exit 0; TEST verde gamma/clob/engine), la página está durable en el journal (frontier 2, NO_INTEGRITY_FAILURES) y el manifiesto lleva el binding del preregistro v2 (`9611b9b1…`) y de la página (`37517e5f…`). Siguiente decisión (lanzador/Owner, una pieza): resolver la regla ex ante — re-verificar contra la doc autorizada la semántica de `start_date_min` (la página vino vacía con 200, no 422; la causa real es hipótesis, no hecho) y, si procede, materializar preregistro v3 con nueva congelación ANTES de cualquier request y re-despachar con el mismo comando validado. No sondear variantes en red sin nuevo preregistro. Sin claims: una página puntual no observa nada ni prueba estabilidad ni PIT. Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real. Nada de esto reabre el freeze de producto; live sigue cerrado.

> [HISTORIA — párrafo vigente tras la pasada 3 de W1-d, superseded por la pasada 4 (2026-10-28); se preserva íntegro:]

W1-d (estado vigente tras la pasada 3 del 2026-10-28, bullet (10)): el colector W1-d quedó implementado, compilado y probado en el checkout (BUILD exacta exit 0; TEST exacta verde en `internal/transport/gamma`, `internal/transport/clob` y `cmd/engine`; preregistro v2 congelado antes de red con revisión vinculada de la v1). La captura misma quedó BLOCKED en su primer paso: `engine catalog select` (prefijo exacto) fue denegado 1 vez porque el sufijo no está en la lista autorizada del perfil por-shot (observe/record/journal verify/manifest build/replay); sin manifiesto de selección no hay `--assets` reales para `record` ni manifiesto para `observe`, y fabricarlos está prohibido — 0 bytes, 0 requests, WS jamás abierto, OOS jamás consultado. Siguiente tarea de lanzador (una sola pieza): autorizar el sufijo `catalog select` con sus flags (`--data-dir`, `--out`, `--preregister`, `--base-url https://gamma-api.polymarket.com`) en el perfil por-shot y re-despachar; la cadena restante está pre-escrita en el doc W1-d (selección 1 request → `clob observe --phase init` → `record` 5 m de humo con stop-file y reconexión, tope 90 m → `clob observe --phase final` → `journal verify` → `manifest build` → `replay`), con el binario y el preregistro ya listos; el hook de grabación exige el manifiesto válido (≤4 mercados, asset_ids, sin 3901955/3901953). Sin claims de rentabilidad/edge/PIT: nada fue observado en red. Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real. Nada de esto reabre el freeze de producto; live sigue cerrado.

> [HISTORIA — párrafo vigente tras la continuación W1-c, superseded como «siguiente paso» por W1-d (2026-10-28); se preserva íntegro:]

W1-c (estado vigente tras la continuación 2026-10-28, bullet (9)): la integración histórica del engine quedó demostrada de extremo a extremo con los derivados congelados — import fail-closed con contadores exactos, journals con integridad verificada, replay reproducible con digest único medido en tres corridas (schedules distintos y grupos D/E independientes) y shadow descriptivo honesto INCONCLUSIVE con fees UNRESOLVED. Lo que la cadena NO cierra y sigue abierto: (1) **tick PIT** — con 0 ticks en ventana, `Qualities` = SYNCING mantiene la ruta económica cerrada por el propio modelo de calidad; el desbloqueo exige un hecho PIT real de tick (diseño de adquisición prospectiva ya propuesto en el informe W1-c y NO iniciado: metadata con as-of + re-poll, initial_dump+deltas+ticks con receive-clock y reconexiones, cadena de hashes, criterios de suficiencia; distinguiendo tiempo de observación de prueba de estabilidad entre polls, y sin que la coherencia con el fee del feed certifique la tasa), (2) **fee de certificación** — el `fee_rate_bps=0` observado y la metadata CURRENT no certifican la tasa histórica de los 4 mercados el 2026-09-01, (3) **universo PIT** — la identidad es CURRENT (`as_of_verified=false`). Siguiente tarea técnica de agente: nada pendiente de esta cadena (su re-ejecución es mecánica con las formas ya admitidas); el trabajo nuevo empieza por el diseño prospectivo cuando haya ventana autorizada. Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real. Nada de esto reabre el freeze de producto; live sigue cerrado.

> [HISTORIA — párrafo vigente tras el primer segmento de W1-c, superseded por la continuación del 2026-10-28; se preserva íntegro:]

W1-c (estado vigente 2026-10-28, bullet (8) de la subsección W1-b): la integración del engine con los derivados w1b8 está implementada, compilada y con regresiones verdes; su ejecución quedó NOT_RUN por gate. Siguiente trabajo de lanzador (una sola pieza): registrar en el allowlist UNA de las dos formas diagnosticadas — el comando ADAPTER exacto del mandato (inoperante: 4 denegaciones, sonda controlada incluida) o los flags `--stage2/--identity` de `historical import` (2 denegaciones; binario y subcomando ya pasan el gate) — y re-despachar: los comandos exactos de la cadena completa (import D/E → journal verify → manifest build → replay con invariancia de schedule G-07 y comparabilidad D=E → shadow base/variante + compare descriptivo) están pre-escritos en `validated-baseline/w1-c/W1-C-MANIFEST.json`. Al correr, la semántica esperada ya está fijada: 544 snapshots reconstruyen los libros (replay), los 256 `last_trade_price` son trades observados de terceros (no fills propios) y los fills simulados sólo existen en shadow virtual (0 esperado, fees UNRESOLVED); con 0 ticks en ventana, `Qualities` reportará SYNCING — la ruta económica sigue cerrada por datos (tick PIT ausente, fee sin certificar), por el gate propio del engine y no por afirmación externa. El diseño de adquisición prospectiva (metadata con as-of + re-poll, initial_dump+deltas+ticks con receive-clock y reconexiones, cadena de hashes, criterios de suficiencia) quedó propuesto en el informe W1-c y NO iniciado; su ejecución requiere ventana futura autorizada. Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real. Nada de esto reabre el freeze de producto; live sigue cerrado.

> [HISTORIA — párrafo vigente tras la ingeniería w1b8, superseded como «siguiente paso» por W1-c (2026-10-28); se preserva íntegro:]

W1-b (estado vigente tras la ingeniería w1b8, 2026-10-28, bullet (7)): la cadena w1b8 quedó reproducible (D=E digest `2e3830ba…`, cores byte-idénticos) y el paquete `pkg-w1b8` fija bytes/identidad/manifiesto con preservación del grupo C. Siguiente trabajo de agente (no Owner): (1) plan prospectivo de captura PIT propuesto y NO iniciado (metadata con as-of + feeSchedule/orderPriceMinTickSize versionados por receive-time, initial_dump + deltas + ticks + reconexiones, re-poll periódico de metadata, sin backfill de ventanas viejas) — su ejecución requiere una ventana futura autorizada de captura, no datos nuevos históricos; (2) cuando exista fuente PIT real para tick/fee de los 4 mercados el 2026-09-01, re-evaluar elegibilidad con el modelo de calidad del engine (sigue sin backfill); (3) si se quisiera extender la cadena w1b8 (p.ej. completar el grupo C bajo identidad w1b6), crear cadena nueva con nuevo freeze — nunca editar in-place. Owner sólo si hay decisión de cuenta/elegibilidad/fondos/riesgo/activación real; el resultado técnico actual queda validado con la estrategia bloqueada por datos (sin exigencia de rentabilidad). Nada de esto reabre el freeze de producto; live sigue cerrado.

> [HISTORIA — párrafo vigente de la revisión científica, superseded como «siguiente paso» por la ingeniería w1b8 del 2026-10-28; se preserva íntegro:]

W1-b (estado vigente tras la revisión científica 2026-10-28, bullet (6)): el replay técnico completado queda CONFIRMADO comparable con salvedades; el camino corto y verificable es: (1) lanzador — preservar los bytes exactos del código que produjo A′/B′ con SHA registrado (copia nominada), fijar `IDENTITY_REVISION_PATH → mapping-revision-w1b6.json` en el runner y decidir completar o retirar el grupo C (puntero en `stage1_done`; su digest, si se completa bajo identidad w1b6, diferirá del canónico sólo por etiquetas de asset); (2) lanzador — pin de la suite sintética de cortes (`tests-synthetic/test_w1b_cut_boundaries-rev1-20261028.py`, NOT_RUN por gate) para ejecutarla contra el runner sin modificarlo; (3) owner — prerequisitos PIT (tick pre-21:10Z vía snapshot público, fee de certificación, universo PIT) y la elección de como máximo dos hipótesis, que hoy sigue sin base admisible (0 hipótesis; descarte razonado por ausencia de señales/economía, muestra de conveniencia y fee/tick sin certificar). Nada de esto reabre el freeze de producto; elegibilidad/cuenta/fondos/riesgo/arming/live siguen siendo gate humano.

> [HISTORIA — párrafo previo, superseded como «siguiente paso» por la revisión científica 2026-10-28; se preserva íntegro:]

W1-b (estado 2026-10-28, replay técnico COMPLETADO): doble corrida comparable PASS con digests idénticos `f56adf469cfb507a987b90aa24df144b913656aebcf07888c8e7f646d417525a` (grupos A rgid `20261028T042313Z` y B rgid `20261028T043738Z`, tres etapas cada uno con manifiestos durables únicos; re-etapa 3 tras el fix de `bbo_of` bajo punteros durables, outputs `-a`, provisionales preservados). Queda owner-side: (1) identidad de mapping CURRENT con `as_of_verified=false` — universo PIT SIN VALIDAR; (2) prerequisito PIT de tick ausente en la ventana (ticks del cohort = 2026-09-02); (3) fee de certificación económica (256 fills observados con fee 0: dato, no certificación); (4) elegir como máximo dos hipótesis sobre este replay (gate humano). `rs-v03`/`pe001` siguen sin evidencia de recuperación (el mapeo del cohort quedó cubierto por la identidad Gamma del parent). El change_log exigido por esta edición es [[2026-10-27-polymarket-engine-entity-updated]]. Nada de esto autoriza reabrir el freeze de producto; elegibilidad/cuenta/fondos/riesgo/arming/live siguen siendo gate humano. (Texto intermedio ya cumplido y superseded — cubierto por la identidad Gamma del parent;) pendiente de esa fuente de mapeo (acción owner/lanzador): `exploratory-manifest.json` v2 (`w1b-2`) ya corregieron el supuesto de esquema (timestamps Arrow con conversión entera exacta) y están conformes por construcción, con run IDs únicos e inmutables (corrección de poda v3), y la doble corrida comparable (digests idénticos), mapping verificado antes del recorrido, extracción cohort con OOS sellado, replay upsert por asset con validación por snapshot y BBO, chequeos de borde, cortes negativos y ventana de incidente 22:30–22:40Z censurada, y doble corrida comparable (digests idénticos); después, elección de como máximo dos hipótesis (gate humano). `rs-v03`/`pe001` y el mapeo de `hist-acq-20260921` siguen sin evidencia de recuperación. El change_log exigido por esta edición es [[2026-10-27-polymarket-engine-entity-updated]]. Nada de esto autoriza reabrir el freeze de producto; elegibilidad/cuenta/fondos/riesgo/arming/live siguen siendo gate humano.
