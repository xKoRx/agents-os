---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Producto Integrado]]"
sprint:
start: 2026-09-07
due:
progress: 0
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo Live Platform V1
  - Echo S0 E0 E1 A0
tags:
  - kind/project
  - area/echo
  - agent/owner
created: 2026-09-07
updated: 2026-09-12
cssclasses:
  - wide
---

# Echo — Live Platform V1

%% Naming: Echo — Live Platform V1 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — Live Platform V1
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Producto Integrado]] · **Repo:** `xKoRx/echo`
> Dueño de Echo SDK (S0) y de la cadena live. No recalcula membership Forge. No asigna magic.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre humano tiene la tarea puente `#type/supervision`.

## 🎯 Objetivo

Consumir handoffs Forge, persistir identidad/versión, enrolar Reference, capturar hechos atribuibles, copiar a Execution con seguridad, medir Execution Fidelity y Strategy Quality, decidir eligibility cuando las reglas lo pidan, construir/aplicar PortfolioVersion determinista, reservar/controlar riesgo, observar/reconciliar estado físico, soportar replacement/rebalance/retirement, y exponer superficies READ/OBSERVE suficientes para el owner.

## 📊 Estado actual

- **PREPARADO + E-01 CLOSED + E-03 CONTRACT_PASS / FINAL CLOSED + E-04 INTEGRATED (SPEC 1.0.2) + E-05 TOP CORRECTION READY.** Roadmap congelado; E2 histórico descompuesto. Progress 0 de plataforma V1. E-04 FINAL CLOSED espera T21 POST-INTEGRATION. E-05 planning v1.0.1 @ `dd1f2da9` en `feature/e05-analytics-convergence-a0` (reserva 063; 062 es E-02); no NORMAL; master intacto `a99f9a63`.
- **E-02 IMPLEMENTATION READY FOR MANAGER SOURCE REVIEW — FOCUSED CORRECTION (2026-09-12):** [[Echo — E-02 Control Safety, Auth and Journal Recovery]] con SPEC/PLAN/TASKS/VERIFICATION v1.0.2 @ `f7ddea18` en `origin/feature/e02-control-safety-journal-recovery` (base `origin/master` `a99f9a63`). Auth hook Hasura = JSON de session variables; READ/CONFIG/CONTROL/webhook requieren tokens distintos y duplicados fallan cerrado 503; literales históricos registrados fueron eliminados en los 17 paths autorizados. Gateway/front/SOURCE/E-04 relevant regression PASS; PHYSICAL_PARTIAL. No verifier, no merge master.
- **Contrato:** [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] B + FR-1…FR-5 en E-01 (`CONTRACT_PASS` `91671f6f`). Live authority [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] ratificado por Fable durability; O1/O3 default técnico; O2 catálogo CC (F-04 Magic Number V1 ya owner-gated).
- **Base observada:** `origin/master` `fac4805185eb586bb73c3df0c0ccc20d1377099c` (E-03 CONTRACT_PASS / FINAL CLOSED; FF desde `c408a12fe36643129a2ae3c3dfa69727b593ba76`, 2026-09-12). E-01 certified S0 permanece `91671f6f`.
- **Ownership SDK:** S0 es de **este** subproyecto. Forge consume el pin. No hay proyecto Integration.
- **E-03:** CONTRACT_PASS / FINAL CLOSED en [[Echo — E-03 Identity and BWC Foundation E0]] @ `fac48051` (integrado FF a `origin/master` 2026-09-12; evidencia en esa nota y en `specs/FEAT-CROSS-IDENTITY-BWC-E0/VERIFICATION.md`).
- **E-04:** SPEC v1.0.2 en [[Echo — E-04 Forge Ingestion E1]]. **INTEGRATED=YES** por fast-forward desde `2f8db345` tras implementation/verifier/E-03/base gates PASS. READY_FOR_INTEGRATION consumido. T21/AC-37 PENDING como gate POST-INTEGRATION; E-04 FINAL CLOSED=NO. Golden no inventado; F-04 no tocado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `master` integrado + feature histórica `feature/e04-forge-ingestion-e1` + feature `feature/e02-control-safety-journal-recovery` + feature `feature/e05-analytics-convergence-a0` | E-01 certified: `91671f6f46ffa889a79aed0979cb3b4e5821ed33` · E-03 CONTRACT_PASS: `fac4805185eb586bb73c3df0c0ccc20d1377099c` · E-04 boundary integrado desde `2f8db345` · E-02 focused correction `f7ddea18` sobre `a99f9a63` · E-05 planning `dd1f2da9` sobre `a99f9a63` | Por Agent Task | E-01: `specs/FEAT-SDK-CANONICAL-CONTRACT/SPEC.md` · E-03: `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md` v1.1.1 · E-04: `specs/FEAT-FORGE-INGESTION-E1/SPEC.md` v1.0.2 · E-02: `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/SPEC.md` v1.0.2 · E-05: `specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md` v1.0.1 | E-01 CLOSED · E-03 CONTRACT_PASS / FINAL CLOSED · E-04 INTEGRATED · READY consumido · T21 POST-INTEGRATION PENDING · FINAL CLOSED=NO · E-02 READY FOR MANAGER SOURCE REVIEW · PHYSICAL_PARTIAL · E-05 TOP CORRECTION READY FOR MANAGER REVIEW |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

Hijos de implementación (no Integration, no tercer producto): [[Echo — E-01 Canonical SDK Foundation S0]], [[Echo — E-03 Identity and BWC Foundation E0]], [[Echo — E-04 Forge Ingestion E1]], [[Echo — E-02 Control Safety, Auth and Journal Recovery]], [[Echo — E-05 Analytics Convergence A0]]. S0 permanece ownership de este track.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [r] [[Echo — E-01 Canonical SDK Foundation S0]] E-01 Canonical SDK foundation S0 #owner/agent #type/dev #area/echo
> - [r] [[Echo — E-02 Control Safety, Auth and Journal Recovery]] E-02 Control safety auth and journal recovery #owner/agent #type/dev #area/echo
> - [r] [[Echo — E-03 Identity and BWC Foundation E0]] E-03 Identity and BWC foundation E0 #owner/agent #type/dev #area/echo
> - [r] [[Echo — E-04 Forge Ingestion E1]] E-04 Forge ingestion E1 #owner/agent #type/dev #area/echo
> - [r] [[Echo — E-05 Analytics Convergence A0]] E-05 Analytics convergence A0 #owner/agent #type/dev #area/echo
> - [ ] E-06 Reference enrollment and binding #owner/agent #type/dev #area/echo
> - [ ] E-07 Raw facts DEAL coverage and trade lifecycle #owner/agent #type/dev #area/echo
> - [ ] E-08 Routing EconomicCommand and risk reservation #owner/agent #type/dev #area/echo
> - [ ] E-09 Execution copy reconciliation and Execution Fidelity #owner/agent #type/dev #area/echo
> - [ ] E-10 Strategy Quality and eligibility #owner/agent #type/dev #area/echo
> - [ ] E-11 PortfolioVersion selection allocation shadow #owner/agent #type/dev #area/echo
> - [ ] E-12 Apply rebalance replacement retirement #owner/agent #type/dev #area/echo
> - [ ] E-13 Front observe ops and V1 completion #owner/agent #type/dev #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 🗺️ Roadmap — Agent Tasks

E2 histórico era mega-fase; aquí está partido en verticales ya frozen. No rediseñar semántica. Size relativo a este track.

### E-01 Canonical SDK foundation S0

- **ID / status / size:** E-01 · To Do · MEDIUM
- **Objective:** Materializar el contrato frozen en `v3/sdk/contracts` puro: types, wire, validation, hash recipes, MetricSelector, Scope sin valuation, record_digest, golden corpus, FR-1…FR-5, compatibility.
- **Capability unlocked:** pin de corpus que Forge y Echo pueden consumir en paralelo.
- **Product value:** lenguaje compartido estable; desbloquea F-04 y E-03/E-05.
- **Why:** sin S0 no hay handoff ni analytics canónica nueva.
- **Frozen input:** [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]; [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]] FR-1…FR-5. No reabrir freeze.
- **In scope:** nested módulo stdlib-only; codec/schema; G01–36 corpus; `C()` vs `H()` vs HashIdentity legacy nombrados distintos; fixture write-once conflict.
- **Out of scope:** infra, DB, Gateway, producers reales, migrar Lab big-bang, autoridad de dominio.
- **Dependencies:** none. **Parallel:** F-01, F-02, F-03, E-02.
- **Hypotheses:** FR-1…FR-5 caben en S0 sin TOP nuevo.
- **Risks:** mezclar hash recipes; valuation colarse en Scope.
- **Output authority:** módulo + golden bytes/digests + pin revisable.
- **Certification:** CONTRACT PASS; tests puros sin infra; GOWORK=off; old/new compat.
- **Done when:** pin publicable; consumidores fake compilando; Forge no cambia significado de fixtures unilateralmente.
- **Unlocks:** F-04, E-03, E-05, E-04.
- **Accepted debt:** adapters vendor/legacy.
- **Planning:** TOP (SPEC). **Implementation:** NORMAL. **GOD:** NONE.

### E-02 Control safety auth and journal recovery

- **ID / status / size:** E-02 · IMPLEMENTATION READY FOR MANAGER SOURCE REVIEW (focused correction v1.0.2; PHYSICAL_PARTIAL) · MEDIUM
- **Objective:** Cerrar exposición de control (admin secret fuera del cliente; auth proxy+roles) y journal ACK/recovery (hechos no se pierden ni se doble-efectúan). H1 del Reality Check; D-04/D-01.
- **Capability unlocked:** el owner puede confiar que una falla se ve y se recupera; control no queda abierto en red.
- **Product value:** TIME_TO_USABLE sin capturar meses sobre un journal que traga errores.
- **Why:** P0 actual; no esperar portfolio.
- **Frozen input:** Reality Check §3 D-01/D-04; master security §14. No nuevo control-plane genérico.
- **In scope:** retirar admin del bundle; auth de mutaciones; persistencia/ack journal; cuarentena de conflictos; replay de facts ≠ replay de órdenes.
- **Out of scope:** rewrite UI; tenancy; DR multi-región; eligibility; CommandID determinístico / EconomicCommand (E-08).
- **Dependencies:** none. **Parallel:** E-01 y Forge interno. Debe anteceder captura canónica E-06.
- **Hypotheses:** Gateway endurecido basta vs servicio nuevo.
- **Risks:** rotación incompleta de secret; ack que dispara órdenes.
- **Output authority:** control autenticado + journal recuperable.
- **Certification:** SOURCE + PRODUCT (GET bundle sin secreto; outage DB/retry/CLOSE-before-OPEN sin pérdida/doble efecto). PHYSICAL de red interna.
- **Done when:** D-04/D-01 del scope habilitado PASS.
- **Unlocks:** E-06 captura confiable; E-13 ops.
- **Accepted debt:** journal mínimo no es ledger institucional.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.
- **Planning vivo:** SPEC/PLAN/TASKS/VERIFICATION v1.0.2 en `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/` @ `f7ddea18` ([[Echo — E-02 Control Safety, Auth and Journal Recovery]]): auth = actores READ/CONFIG/CONTROL/webhook con Bearer presentado y hook Hasura por JSON de session variables (A03-A, sin BFF, sin runtime-config de tokens); unicidad de tokens fail-closed; journal = transientes al retry del ingress journal + cuarentena 062 + `v3/tools/journalctl` PG→PG (A01-A); CommandID UUIDv5 diferido a E-08 (fan-out Kafka paralelo); migración única additive; PHYSICAL_PARTIAL por infraestructura ausente.

### E-03 Identity and BWC foundation E0

- **ID / status / size:** E-03 · To Do · MEDIUM
- **Objective:** Persistence/protocol groundwork: StrategyVersion, PromotionRecord, wide IDs, magic int64, legacy dispatch, immutability, schema protection, BWC.
- **Capability unlocked:** Echo puede guardar identidad/versión sin truncar ni competir con Forge.
- **Why:** ingestión sin esto fabrica identidades Echo.
- **Frozen input:** SDK identity; live authority §§2–3, 9. Magic Forge-owned.
- **In scope:** widen canonical/IDs; EA variable-length/migración; G19–21; layouts old/new; fail-closed unsupported.
- **Out of scope:** allocator magic; ingestion handler; live facts; JS float loss sin test.
- **Dependencies:** E-01. **Parallel:** F-04, E-05.
- **Hypotheses:** PromotionRecord + binding cubre versión sin version-service.
- **Risks:** truncar >64 canonical; crash widen in-place (D-31).
- **Output authority:** schema protegido + adapters BWC.
- **Certification:** SOURCE + MIGRATION (backup/atomic/restart; >int32; >2^53 wire).
- **Done when:** no truncate; old maps preserved; no magic Echo competidor.
- **Unlocks:** E-04 development (implementation closed); E-04 integration espera CONTRACT_PASS.
- **Accepted debt:** aliases `magic_*` por scope.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-04 Forge ingestion E1

- **ID / status / size:** E-04 · READY_FOR_INTEGRATION (SPEC 1.0.2) · MEDIUM
- **Objective:** Gateway individual autenticado; validación; copia verificada de artefacto operativo; tx identity/version/promotion; replay/idempotency; **cero** provision/activation/capital.
- **Capability unlocked:** INGESTED = receipt, no live.
- **Why:** D-13; puente H3.
- **Frozen input:** SDK §12; live authority §4. IngestionReceipt = respuesta del PromotionRecord. Join: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]].
- **In scope:** endpoint; auth; verified copy; G01–25/G31/G35 (SYNTHETIC); race/crash/restore; producer fake suficiente para CONTRACT.
- **Out of scope:** batch; attach EA; eligibility; escribir Forge DB; latest lookup.
- **Development dependency:** E-01 + E-03 IMPLEMENTATION CLOSED @ `c408a12f`. `FORGE_GOLDEN_FIXTURE_PENDING` no bloquea development.
- **Golden dependency:** fixture Forge auténtica versionada. Hoy pending. Bloquea CROSS_LANE GOLDEN PASS / E-04 FINAL CLOSED (gate POST-INTEGRATION). No bloquea READY_FOR_INTEGRATION ni merge. No espera E-03 CONTRACT_PASS.
- **Integration dependency:** E-03 CONTRACT_PASS MET @ `fac48051` + implementation PASS + independent verifier PASS + base reconciliada gates PASS. T21/AC-37 no era prerrequisito del merge; E-04 ya está integrado por FF.
- **Parallel:** F-04 tras pin; verification E-03 (development only).
- **Hypotheses:** key+digest idempotente; conflicto write-once.
- **Risks:** timeout post-commit; side effects.
- **Output authority:** PromotionRecord INGESTED.
- **Certification:** SOURCE + CONTRACT + PG + PHYSICAL HTTP+PG. SYNTHETIC ≠ CROSS_LANE GOLDEN. CROSS_LANE GOLDEN pending authentic Forge fixture (POST-INTEGRATION). CONTROLLED INTEGRATION habilitada por E-03 CONTRACT_PASS + implementation/verifier/base; T21 no bloquea merge. FINAL CLOSED espera T21 PASS.
- **Done when:** matriz duplicate/conflict/partial PASS **e** integración FF ejecutada; FINAL CLOSED adicionalmente T21 PASS.
- **Unlocks:** E-06; join con F-04/F-05 (tras merge E-04; T21 certifica el join).
- **Accepted debt:** artefactos grandes quedan en Forge por refs.
- **Planning:** TOP v1.0.2 ([[Echo — E-04 Forge Ingestion E1]]). **Implementation:** T01–T20 `[x]`. **GOD:** NONE.

### E-05 Analytics convergence A0

- **ID / status / size:** E-05 · TOP PLANNING READY FOR MANAGER REVIEW · MEDIUM
- **Objective:** Operaciones/scopes/sets/metrics canónicos en **paths nuevos**. Lab legacy vía adapters/proyecciones. No big bang.
- **Capability unlocked:** métricas nuevas con key+basis+unit+formula.
- **Why:** mismo nombre ≠ misma semántica.
- **Frozen input:** SDK §§4–8, FR-2/FR-3; Lab R AUTO no prueba base única.
- **In scope:** MetricSet/Scope/R explícito; G16–18/G26–29/G32–33/G36 por borde; adapters Forge/Echo.
- **Out of scope:** recompute histórico masivo; UI nueva como autoridad; ML.
- **Dependencies:** E-01. No exige E-01+E-04 para todos los bordes.
- **Parallel:** E-03/E-04.
- **Hypotheses:** projections legacy identificadas bastan.
- **Risks:** win_rate % vs ratio; R pips vs money silencioso.
- **Output authority:** writers nuevos canónicos; readers legacy adaptados.
- **Certification:** CONTRACT/SOURCE con datasets sintéticos; no analizar profit histórico como prueba.
- **Done when:** new writes canónicos; legacy no se presenta como autoridad.
- **Unlocks:** E-10.
- **Accepted debt:** snapshots Lab como read model.
- **Planning:** TOP v1.0.1 ([[Echo — E-05 Analytics Convergence A0]]). **Implementation:** NORMAL (no lanzado). **GOD:** NONE.
- **Planning vivo:** SPEC/PLAN/TASKS/VERIFICATION v1.0.1 en `specs/FEAT-ANALYTICS-CONVERGENCE-A0/` @ `dd1f2da9` sobre `a99f9a63`. Persistencia 063 additive (exclusiva E-05); `062_journal_quarantine` reserva E-02; 064+ fuera de scope. Calculator Go; Lab dual-run; Hasura SELECT; sin FK a 061; sin SQ/EF. E-02 no bloquea development/implementation/verification. Merge/deploy de 063 espera 062 en `master`.

### E-06 Reference enrollment and binding

- **ID / status / size:** E-06 · To Do · MEDIUM
- **Objective:** RuntimeBinding: una enrollment canónica por Version; cuenta+broker+magic mapping observado; ACK/read-back; coverage start barrier. Attach manual verificado permitido V1.
- **Capability unlocked:** reloj forward atribuible. Ingestion ≠ observing.
- **Why:** sin enrollment no hay Quality canónica.
- **Frozen input:** live authority §§5–6; O1/O3 default técnico Fable; pin Version al OPEN.
- **In scope:** observed fact; duplicate collector reject; no observation on DB-only; shadow vs canonical; no same-account overlap de versiones.
- **Out of scope:** generic provisioning; auto-takeover; editor.
- **Dependencies:** E-04; E-02 para confiar captura. Supply Forge ayuda, no bloquea diseño.
- **Parallel:** F-05 si hay candidata.
- **Hypotheses:** accounts/policies + facts de binding bastan (no tabla deployments anticipada).
- **Risks:** overlap magic/cuenta; ACK operator sin read-back.
- **Output authority:** RuntimeBinding + coverage watermark inicial.
- **Certification:** PHYSICAL (read-back, duplicate collector, no trading on DB-only). Mocks ≠ OBSERVING.
- **Done when:** primera observación atribuible o UNKNOWN explícito.
- **Unlocks:** E-07.
- **Accepted debt:** attach manual.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-07 Raw facts, DEAL, coverage and trade lifecycle

- **ID / status / size:** E-07 · To Do · MEDIUM
- **Objective:** Raw immutable antes de routing; DEAL irreducible; OPEN/MODIFY/CLOSE clocks/costs; coverage como evidencia de observación, no “no hubo trades”.
- **Capability unlocked:** hechos recuperables; UNKNOWN ≠ cero.
- **Why:** Quality/Fidelity mienten sin esto.
- **Frozen input:** SDK TradingFact/Coverage; live authority §6; FR-5 record_digest.
- **In scope:** durable raw; deal dedupe; late CLOSE; partial fills; initial-risk unknown; outage coverage U; replay no despacha.
- **Out of scope:** netting; MAE/MFE institucionales; pre-broker signal.
- **Dependencies:** E-06, E-03.
- **Parallel:** diseño E-08.
- **Hypotheses:** journal proyecta; raw es autoridad de fills que el journal no tiene.
- **Risks:** CLOSE usa current_version; recorded vs event-time (Lab recorded se conserva).
- **Output authority:** TradingFact ledger + Coverage.
- **Certification:** PHYSICAL (offline/restart/partial/late cost). SOURCE fixtures primero.
- **Done when:** lookup por trade_id; coverage U visible.
- **Unlocks:** E-08/E-09.
- **Accepted debt:** legacy journal rows.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-08 Routing, EconomicCommand and risk reservation

- **ID / status / size:** E-08 · To Do · MEDIUM
- **Objective:** Universo expected/excluded congelado; EconomicCommand durable con policy/risk snapshot y reservation 1:N deals; UNKNOWN no resend ciego.
- **Capability unlocked:** routing denominator + comando económico recuperable.
- **Why:** Fidelity y apply necesitan expected universe, no INNER JOIN.
- **Frozen input:** live authority §§7–8; SDK Routing/EconomicCommand.
- **In scope:** planner snapshot; command uniqueness/outbox; reservation headroom por cuenta; crash PENDING; policy mutation no cambia command histórico.
- **Out of scope:** optimizer de routing; multi-broker abstracto; netting.
- **Dependencies:** E-07 identidad raw.
- **Parallel:** guards de E-12 en shadow.
- **Hypotheses:** reserva integrada en command, no servicio de riesgo distribuido.
- **Risks:** dos opens concurrentes; UNKNOWN libera presupuesto.
- **Output authority:** Routing result + EconomicCommand.
- **Certification:** SOURCE + PHYSICAL (empty vs unknown, exclusions, MM crash PENDING).
- **Done when:** expected recipients persistidos; reserva sobrevive crash.
- **Unlocks:** E-09, E-12.
- **Accepted debt:** hedging-only V1.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-09 Execution copy, reconciliation and Execution Fidelity

- **ID / status / size:** E-09 · To Do · MEDIUM
- **Objective:** Copiar Reference→Execution con correlación/reconciliación; EF desde early trades: missing/extra/duplicate/reject/delay distintos. SQ ≠ EF ≠ Forge fidelity.
- **Capability unlocked:** owner ve si la copia es fiel, no sólo si la estrategia “funciona”.
- **Why:** H4; D-21.
- **Frozen input:** SDK purposes; master §8; Reality Check fidelity mínimo.
- **In scope:** ACK/deals/positions; reconcile FULL universo expected; vector pequeño por operación.
- **Out of scope:** percentiles institucionales; DEMO→REAL sin evidencia; score broker sofisticado.
- **Dependencies:** E-08. E-02 recovery.
- **Hypotheses:** expected+outcomes bastan para V1 útil.
- **Risks:** INNER JOIN como EF; 2505 unpaired como pérdidas.
- **Output authority:** Execution Fidelity MetricSet/diagnósticos.
- **Certification:** PHYSICAL (Reference mala/copia fiel y viceversa). No mocks como PHYSICAL PASS.
- **Done when:** missing/reject/duplicate visibles; no-trade ≠ outage.
- **Unlocks:** E-10 interpretación conjunta; E-12 safety.
- **Accepted debt:** p50/p95 POST.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-10 Strategy Quality and eligibility

- **ID / status / size:** E-10 · To Do · MEDIUM
- **Objective:** Quality sobre observaciones forward de Version+Expectation; coverage primero; INSUFFICIENT/UNKNOWN separados de FAIL; eligibility sólo con policy validada. Abstención es resultado válido.
- **Capability unlocked:** owner entiende calidad y candidatos explícitos; CASH si no hay evidencia.
- **Why:** no fingir elegibilidad para diciembre.
- **Frozen input:** master §9; Reality Check quality mínimo; Expectation portable acotada (no catálogo exhaustivo).
- **In scope:** baseline Forge/expectation; Reference-only; warnings/incertidumbre; Decision eligibility si product rules lo piden; degradación/régimen **sólo si ya aprobado** (shadow simple SHOULD).
- **Out of scope:** ML; MAE/MFE must; meta-score; bajar umbral en secreto.
- **Dependencies:** E-06/E-07; E-05 writers; calendario irreductible.
- **Parallel:** E-11 con fixtures.
- **Hypotheses:** baseline pequeña + coverage desbloquea captura sin seasonality.
- **Risks:** LIVE default; EdgeScore=coverage; reciclar evidencia de otra versión.
- **Output authority:** Quality read models + Eligibility Decision o INSUFFICIENT.
- **Certification:** PRODUCT (negative-PnL alta DQ no elegible por ese score; new version reset). Calendar Gate no se omite.
- **Done when:** UNKNOWN visible; eligibility no se infiere de días de calendario solos.
- **Unlocks:** E-11 candidatos reales; E-13 explicación.
- **Accepted debt:** historical recover R-33 timebox paralelo.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-11 PortfolioVersion selection allocation shadow

- **ID / status / size:** E-11 · To Do · MEDIUM
- **Objective:** Candidatos versionados + límites + equal-risk determinista + CASH + PortfolioVersion published inmutable. Shadow antes de efectos. Una PortfolioVersion = selection+allocation.
- **Capability unlocked:** propuesta reproducible sin babysitting de Excel.
- **Why:** H5; D-20/D-22.
- **Frozen input:** SDK/master portfolio; no framework Decision-por-verbo.
- **In scope:** draft vs published; no eligible→CASH; familias/concentración conservadora; curvas agregadas o no publicar DD inventado.
- **Out of scope:** ML optimizer; apply/ACK (E-12); grupos de cuentas como allocation.
- **Dependencies:** interfaces E-10; shadow con fixtures ahora.
- **Parallel:** E-10 real y E-08 guards.
- **Hypotheses:** equal-risk + límites V1 útiles.
- **Risks:** UPDATE published; promedio de DD individuales.
- **Output authority:** PortfolioVersion inmutable.
- **Certification:** SOURCE determinista + replay; PRODUCT shadow. No PHYSICAL de dinero.
- **Done when:** published inmutable también vía API/admin; CASH representable.
- **Unlocks:** E-12.
- **Accepted debt:** correlación unknown handling conservador.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-12 Apply, rebalance, replacement and retirement

- **ID / status / size:** E-12 · To Do · MEDIUM
- **Objective:** Aplicar PortfolioVersion con ACK; pause/reduce/replace/rebalance/retire o CASH; risk reservation/control; cero unknown exposure al habilitar opens. Auto DEMO tras gates; REAL sólo aprobación owner.
- **Capability unlocked:** loop DEMO operable (H6); no autonomía económica amplia.
- **Why:** decide sin apply no es producto usable.
- **Frozen input:** INGESTION≠ACTIVATION; D-06/07/09/24/25/32; O-04/O-05.
- **In scope:** effect ledger; partial apply; crash mid-transition; kill pre-send; version drain; no overlap ambiguo.
- **Out of scope:** auto-replace amplio V1; REAL sin gates; generic event sourcing.
- **Dependencies:** E-11, E-08, E-09, E-02.
- **Hypotheses:** auto-protección y cash por defecto.
- **Risks:** replay de facts como replay de órdenes; pause que cierra todo implícito.
- **Output authority:** applied N/N+1 + effect ledger.
- **Certification:** PHYSICAL DEMO (partial/crash/ACK lost/two opens). REAL es PRODUCT DECISION aparte.
- **Done when:** N→N+1 y pause/recovery sin opens/duplicates inesperados.
- **Unlocks:** E-13 firma de scope.
- **Accepted debt:** attach manual residual documentado.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-13 Front observe, ops and V1 completion

- **ID / status / size:** E-13 · To Do · MEDIUM
- **Objective:** Superficies READ/OBSERVE (runs, funnels, strategies, metrics, warnings, rankings, finalists, campaigns, Reference/Execution/live, portfolio/control) con watermarks/UNKNOWN. Ops: freshness, backup/restore drill, alertas accionables. Certificar V1 de plataforma, no maquillar cartera financiada.
- **Capability unlocked:** owner explica cada estado desde UI+ledger (H7 software).
- **Why:** sin read surface el sistema no es usable; sin restore no hay REAL.
- **Frozen input:** front READ first; viewer SQX SHOULD; no editor.
- **In scope:** read models/API; auth ya de E-02; restore aislado del scope; certification manifest; declared supported scope.
- **Out of scope:** rewrite UI; reexecution GUI; tenancy; SRE universal.
- **Dependencies:** E-12 para loop; read models pueden adelantarse con fixtures.
- **Hypotheses:** vistas pequeñas por capacidad > UI nueva.
- **Risks:** reader stale como autoridad; declarar Product Complete con eligible=0 **está permitido** para software, no para dinero.
- **Output authority:** control/read surfaces + cert manifest.
- **Certification:** PRODUCT CAPABILITY PASS. Restore PHYSICAL. Viewer SQX no bloquea.
- **Done when:** DoD plataforma del padre; O-01 dinero separado.
- **Unlocks:** operación owner; no más fases V1 de este subproyecto.
- **Accepted debt:** Lab legacy views vía adapter.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

## Definition of Done — Live Platform V1

Consumir handoffs; persistir identity/version; bind Reference; facts atribuibles; copy Execution segura; medir EF y SQ; eligibility cuando las reglas lo requieren; PortfolioVersion determinista; risk reserve/control; observe/reconcile; replacement/rebalance/retirement; front/ops suficientes. CASH/INSUFFICIENT es éxito de software. REAL financiado es gate owner.

## 📆 Bitácora

- **2026-09-12** — E-05 TOP CORRECTION v1.0.1 ([[Echo — E-05 Analytics Convergence A0]]): reserva de migración @ `dd1f2da9`. E-02 owner de `062_journal_quarantine`; E-05 cambia a `063_analytics_convergence_a0`; 064+ fuera de scope. E-02 no bloquea development/implementation/verification. Merge/deploy de 063 serializa tras 062 en `master`. Docs-only; master intacto `a99f9a63`. Puente E-05 permanece Review.
- **2026-09-12** — E-05 TOP planning one-shot ([[Echo — E-05 Analytics Convergence A0]]): SPEC/PLAN/TASKS/VERIFICATION v1.0.0 @ `be87f11e` pusheados a `origin/feature/e05-analytics-convergence-a0` desde `a99f9a63` (docs-only; master intacto). Persistencia mínima 062; adapters Lab; calculator Go; Hasura SELECT. E-02/E-04/F-04 no tocados. Puente E-05 → Review.
- **2026-09-12** — E-02 focused source-review correction v1.0.2 ([[Echo — E-02 Control Safety, Auth and Journal Recovery]]): SPEC/PLAN/TASKS/VERIFICATION @ `f7ddea18` sobre HEAD inicial `df99084b`. Auth hook entrega JSON Hasura, tokens duplicados fallan cerrado, 17 paths históricos autorizados limpiados; Gateway/front/SOURCE y regresión E-04 relevante PASS; PHYSICAL_PARTIAL, no verifier, master intacto. Puente E-02 permanece Review.
- **2026-09-12** — E-02 TOP planning one-shot ([[Echo — E-02 Control Safety, Auth and Journal Recovery]]): subproyecto materializado; SPEC/PLAN/TASKS/VERIFICATION v1.0.0 @ `ac7b4e14` pusheados a `origin/feature/e02-control-safety-journal-recovery` desde `a99f9a63` (docs-only; master intacto). Source D-04/D-01 revalidado en el baseline. Corregido el mismo día en v1.0.1.
- **2026-09-12** — E-04 CONTROLLED INTEGRATION one-shot PASS: fetch/race y ancestry confirmados; gates mínimos PASS; `master` avanzó por fast-forward desde `fac48051` hasta el boundary E-04 `2f8db345`, sin reescritura ni force-push. Push normal verificado: `origin/master` final=`a99f9a63354bbe72219d1e590bb93757ed08e45e`; feature intacta=`2f8db345`. E-04 INTEGRATED=YES, READY consumido, T21/AC-37 PENDING POST-INTEGRATION y FINAL CLOSED=NO. Evidencia en E-04 `VERIFICATION.md`; F-04 no tocado.
- **2026-09-12** — E-04 TOP CORRECTION 1.0.2 ([[Echo — E-04 Forge Ingestion E1]]): circular golden gate roto. T21/AC-37 ya no bloquea READY_FOR_INTEGRATION/merge; pasa a POST-INTEGRATION. READY_FOR_INTEGRATION=YES. FINAL CLOSED espera T21 PASS. Merge no ejecutado. Master intacto `fac48051`.
- **2026-09-12** — E-03 CONTRACT_PASS / FINAL CLOSED ([[Echo — E-03 Identity and BWC Foundation E0]]): manager certificó en `fac48051` y se integró FF a `origin/master` (`c408a12f..fac48051`, sin merge commit/rebase/force). Gate `E03_CONTRACT_PASS_REQUIRED_FOR_INTEGRATION` de E-04 queda satisfecho; E-04 y Forge no tocados en esta integración. Puente E-03 permanece Review.
- **2026-09-11** — E-04 planning v1.0.1 ([[Echo — E-04 Forge Ingestion E1]] @ `c8e68538`): CROSS_LANE GOLDEN exige fixture Forge auténtica (`FORGE_GOLDEN_FIXTURE_PENDING`); synthetic S0 ≠ golden; CROSS_LANE development no espera E-03 CONTRACT_PASS; merge/close sí. Master no se toca. Puente E-04 permanece Review.
- **2026-09-11** — Enlace al subproyecto [[Echo — E-04 Forge Ingestion E1]]. Development may start en `feature/e04-forge-ingestion-e1` desde `c408a12f` en paralelo con verification E-03. Integration gated by E-03 CONTRACT_PASS. Master no se toca. Puente E-04 → Review.
- **2026-09-10** — Enlace mínimo al subproyecto de implementación [[Echo — E-03 Identity and BWC Foundation E0]]. Baseline E-03 = E-01 certified `91671f6f`. No se reescribió el roadmap.
- **2026-09-10** — E-03 relational integrity `576bf1f4` (parent `45a59fca`) listo para revisión manager. UNIQUE + composite FK Mapping→Version→Promotion. Puente permanece Review. Sin implementación.
- **2026-09-10** — E-03 S0 module consumption `233ec89c` (parent `576bf1f4`) FF a `origin/master`. `require v0.0.0` + `replace => ./contracts`. `go.sum` no delta. Puente permanece Review. Implementación dirty no committed. MT4 PHYSICAL blocker.
- **2026-09-07** — Reparentado a [[Echo — Producto Integrado]], `owner: agent`. E2 partido en E-06…E-09. E-02 extraído como H1. Tareas `#owner/me` de 4 ítems supersedidas. S0 permanece aquí.
- **2026-09-07** — Enlace mínimo al subproyecto de implementación [[Echo — E-01 Canonical SDK Foundation S0]]. Baseline E-01 fijado `04c16bd2`. No se reescribió el roadmap.

## 🧭 Decisiones

- S0 es de Echo, no Integration.
- E2 no es una Agent Task.
- Front V1 es READ/OBSERVE.

## 🔗 Docs / Links

- [[Echo — E-01 Canonical SDK Foundation S0]]
- [[Echo — E-02 Control Safety, Auth and Journal Recovery]]
- [[Echo — E-03 Identity and BWC Foundation E0]]
- [[Echo — E-04 Forge Ingestion E1]]
- [[Echo — E-05 Analytics Convergence A0]]
- [[Echo — Producto Integrado]]
- [[Echo Forge — Factory V2 Completion]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]]
- [[Echo - Discovery y Estado]]
- [[echo-core]]

## 💡 Ideas

### Backlog de ideas

- Viewer SQX pool: SHOULD, no fase bloqueante.
- Recuperación histórica R-33: timebox, no fase V1 de factory.

### Motivos / principios

- Ingestion no inicia el reloj. Coverage no es edge/alpha.

### Memoria pública / interna

- **Memoria pública:** contratos enlazados.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** Discovery conserva historia, no el roadmap.
