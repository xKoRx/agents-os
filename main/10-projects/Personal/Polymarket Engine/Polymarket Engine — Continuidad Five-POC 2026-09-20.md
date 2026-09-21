---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-20
updated: 2026-09-21
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

> [!important] PUNTO DE ENTRADA PARA LA PRÓXIMA SESIÓN
> Esta nota es un **handoff de continuidad y tareas**, no una nueva SPEC ni sustituto del proyecto padre. Leer primero [[Polymarket Engine — MVP]], esta nota y [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]. Fuente del cierre: reporte ejecutor del 2026-09-20, registrado en [[2026-09-20-polymarket-fivepoc-final-closure]] y recursos del dominio. Las evidencias ejecutables viven en **el repo local del engine**, no en este vault. Cualquier SHA/resultado se debe volver a verificar al retomar; esta nota no afirma haber corrido comandos en la sesión documental.

## 1. Estado canónico al cierre

| Dimensión | Estado comunicado y condición |
|---|---|
| Programa | `FIVE_POC_FINAL_CERTIFIED_BASELINE_READY` **offline**, 5/5 estrategias/observador implementados, pipeline y outputs reproducibles; **no** equivale a validación de edge. |
| Engine | Go, monolito modular, Polymarket-specific, engine durable y strategies reemplazables. `TIME_TO_VALIDATED_HYPOTHESIS` sigue siendo el norte. |
| Repo | `~/go/src/github.com/xKoRx/polymarket-engine`; worktree de integración `~/go/src/github.com/xKoRx/polymarket-engine-integration`; branch **LOCAL** `feature/five-poc-integration`. |
| Shared base | `9d0512a912fcce4b9aefc152c7a89b090ff8df1d` sobre `feature/research-strategies-v01@f070496` local al inicio del programa. |
| SHA de corrección de código | `56e8fac`: bugs `notional_by_scenario`, `reserve_held` y wiring Catalog O. |
| SHA de evidencia/certificación | `c38f6c4`: evidencia `research-v07` y baseline del recibo M4. Árbol de código idéntico a `56e8fac` según reporte. |
| HEAD final | `85e27ff`: añade `certificate-v07.json`; delta `56e8fac..85e27ff` reportado **sin cambios de código**, worktree limpio. |
| Calidad | Reporte del ejecutor: build/vet/test/race PASS, archtest 12/12, F5 + SFG-07 PASS, dataset guard y LIVE_DISABLED PASS. |
| M4 | `M4_CERTIFIED_NON_LIVE` **@ c38f6c4**, 27 PASS, 0 FAIL, 0 NOT_RUN in-scope, 5 live diferidos. Receipt: `testdata/research-v07/certificate-v07.json`. No heredar este certificado si cambia código. |
| Git/publicación | **Engine sin push ni merge** a `feature/research-strategies-v01` ni `main`; remoto puede ser históricamente anterior. `OWNER_REVIEW_REQUIRED`, rango `c915c11..85e27ff`. No publicar ni dar por aceptado sin decisión explícita del owner. |
| Datos/hipótesis | Fixtures sintéticos; datasets RS v0.3 (41/41 SHA OK) y pe001 (78/78 SHA OK) intactos; Weather/Catalog **inventariados** 2026-09-21 sin vintages ni cohorte nueva; fee venue **`V2_CASH_CONFIRMED`** (unidad BUY = collateral pUSD; `TAKER_PROCEEDS` = V1 archivado, no el venue de PE-001/weather); `REAL_FEE_READY=NO`; `HYPOTHESIS_VALIDATED=NO` en las cinco. Etapa: `ENGINEERING_STAGE_CLOSED_RESEARCH_REPRODUCIBLE`. |
| Seguridad | `LIVE_DISABLED` / SHADOW virtual; wallet, signing, órdenes y certificación live fuera de alcance. |

**Control de documentación:** las secciones antiguas, `updated` de frontmatter, `progress: 0` en subproyectos o bullets históricos del padre pueden describir checkpoints previos. Para el estado del programa usar *este snapshot + § Five-POC Cierre Definitivo del padre + receipts v07*, verificando el checkout. No borrar historial ni convertir un estado reportado en evidencia nueva.

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
cd ~/go/src/github.com/xKoRx/polymarket-engine-integration
git status --short --branch
git rev-parse HEAD
git worktree list
git log -n 12 --oneline
git merge-base --is-ancestor 56e8fac HEAD && echo CODE_ANCESTRY_OK
git diff --name-status c38f6c4 85e27ff
ls -l testdata/research-v07/certificate-v07.json testdata/research-v07/experiment-drills/DRILLS.md
```

Esperado **al cierre comunicado**, no condición impuesta si ha avanzado el repo: HEAD `85e27ff` limpio, branch `feature/five-poc-integration` y certificado con baseline `c38f6c4` sin delta de código después del pin. **STOP** si falta la rama/commit local, el árbol está dirty o M4 no corresponde al código: diagnosticar primero; NO forzar checkout/reset/push para fingir sincronización. El remoto de engine no contiene necesariamente estos commits. Si checkout está en `feature/research-strategies-v01` o `main`, descubrir la branch local y usar su worktree, NO reconstruir desde HEAD remoto viejo.

Validar operabilidad después del preflight, en dataset nuevo:

```bash
cd ~/go/src/github.com/xKoRx/polymarket-engine-integration
go build -o /tmp/engine ./cmd/engine
go vet ./...
go test ./... -count=1
/tmp/engine fixture fivepoc --kind vertical --out /tmp/pme-resume-s01s02
# Continuar la receta exacta por POC desde la guía operativa; no reutilizar un output dir existente.
```

Para M4, leer flags reales `engine experiment certify --help`, confirmar SHA completo de baseline e invocar perfil `no-live` solo si se requiere certificar **código nuevo**. El recibo v07 histórico sigue válido exclusivamente para el código correspondiente; no heredar M4 por nombre de branch.

## 6. Tareas reales de la próxima sesión — orden de decisión

- [ ] **OWNER / P0 — Review humana** del rango `c915c11..85e27ff`, recibo `certificate-v07.json`, correcciones contables/wiring y datasets intactos. Registrar decisión en padre/bitácora; el agente NO se autoacepta.
- [ ] **OWNER / P0 — Decidir publicación** del engine. Si acepta: estrategia de integración/push de `feature/five-poc-integration` hacia `feature/research-strategies-v01` o branch objetivo que el owner elija; detectar remoto adelantado, revisar diff/conflictos, no force-push; ejecutar suite+M4 sobre SHA realmente integrado. Si no acepta: preservar rama local y estado `UNPUBLISHED`.
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

La primera sesión debe **comenzar ejecutando el preflight y un caso de uso real offline**; no gastar horas redescubriendo arquitectura ni afirmar estado remoto/local sin comprobarlo. Esta continuidad queda cerrada documentalmente, **Review humana y push siguen abiertos**.

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

