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
updated: 2026-09-10
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

- **PREPARADO + E-01 CLOSED + E-03 TOP listo.** Roadmap congelado; E2 histórico descompuesto. Progress 0 de plataforma V1.
- **Contrato:** [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] B + FR-1…FR-5 en E-01 (`CONTRACT_PASS` `91671f6f`). Live authority [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] ratificado por Fable durability; O1/O3 default técnico; O2 catálogo CC.
- **Base observada:** `origin/master` revalidado `91671f6f46ffa889a79aed0979cb3b4e5821ed33`. Lab/journal/copia existen; ingestión Gateway ausente; P0 auth (admin secret en bundle) y journal ACK.
- **Ownership SDK:** S0 es de **este** subproyecto. Forge consume el pin. No hay proyecto Integration.
- **E-03:** planning TOP en [[Echo — E-03 Identity and BWC Foundation E0]]; SPEC repo `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `master` | Revalidar por fase. E-01 certified: `91671f6f46ffa889a79aed0979cb3b4e5821ed33` | Por Agent Task | E-01: `specs/FEAT-SDK-CANONICAL-CONTRACT/SPEC.md` · E-03: `specs/FEAT-CROSS-IDENTITY-BWC-E0/SPEC.md` | E-01 CLOSED · E-03 TOP listo |

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

Hijos de implementación (no Integration, no tercer producto): [[Echo — E-01 Canonical SDK Foundation S0]], [[Echo — E-03 Identity and BWC Foundation E0]]. S0 permanece ownership de este track.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [r] [[Echo — E-01 Canonical SDK Foundation S0]] E-01 Canonical SDK foundation S0 #owner/agent #type/dev #area/echo
> - [ ] E-02 Control safety auth and journal recovery #owner/agent #type/dev #area/echo
> - [/] [[Echo — E-03 Identity and BWC Foundation E0]] E-03 Identity and BWC foundation E0 #owner/agent #type/dev #area/echo
> - [ ] E-04 Forge ingestion E1 #owner/agent #type/dev #area/echo
> - [ ] E-05 Analytics convergence A0 #owner/agent #type/dev #area/echo
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

- **ID / status / size:** E-02 · To Do · MEDIUM
- **Objective:** Cerrar exposición de control (admin secret fuera del cliente; auth proxy+roles) y journal ACK/recovery (hechos no se pierden ni se doble-efectúan). H1 del Reality Check; D-04/D-01.
- **Capability unlocked:** el owner puede confiar que una falla se ve y se recupera; control no queda abierto en red.
- **Product value:** TIME_TO_USABLE sin capturar meses sobre un journal que traga errores.
- **Why:** P0 actual; no esperar portfolio.
- **Frozen input:** Reality Check §3 D-01/D-04; master security §14. No nuevo control-plane genérico.
- **In scope:** retirar admin del bundle; auth de mutaciones; persistencia/ack journal; cuarentena de conflictos; replay de facts ≠ replay de órdenes.
- **Out of scope:** rewrite UI; tenancy; DR multi-región; eligibility.
- **Dependencies:** none. **Parallel:** E-01 y Forge interno. Debe anteceder captura canónica E-06.
- **Hypotheses:** Gateway endurecido basta vs servicio nuevo.
- **Risks:** rotación incompleta de secret; ack que dispara órdenes.
- **Output authority:** control autenticado + journal recuperable.
- **Certification:** SOURCE + PRODUCT (GET bundle sin secreto; outage DB/retry/CLOSE-before-OPEN sin pérdida/doble efecto). PHYSICAL de red interna.
- **Done when:** D-04/D-01 del scope habilitado PASS.
- **Unlocks:** E-06 captura confiable; E-13 ops.
- **Accepted debt:** journal mínimo no es ledger institucional.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

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
- **Unlocks:** E-04.
- **Accepted debt:** aliases `magic_*` por scope.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-04 Forge ingestion E1

- **ID / status / size:** E-04 · To Do · MEDIUM
- **Objective:** Gateway individual autenticado; validación; copia verificada de artefacto operativo; tx identity/version/promotion; replay/idempotency; **cero** provision/activation/capital.
- **Capability unlocked:** INGESTED = receipt, no live.
- **Why:** D-13; puente H3.
- **Frozen input:** SDK §12; live authority §4. IngestionReceipt = respuesta del PromotionRecord.
- **In scope:** endpoint; auth; verified copy; G01–25/G31/G35; race/crash/restore; producer fake suficiente.
- **Out of scope:** batch; attach EA; eligibility; escribir Forge DB; latest lookup.
- **Dependencies:** E-01+E-03. F-04 real opcional; fixtures primero.
- **Parallel:** F-04 tras pin.
- **Hypotheses:** key+digest idempotente; conflicto write-once.
- **Risks:** timeout post-commit; side effects.
- **Output authority:** PromotionRecord INGESTED.
- **Certification:** SOURCE + INTEGRATION (replay mismo resultado; copy fail no commit; zero non-effects). PHYSICAL después, no mocks como live.
- **Done when:** matriz duplicate/conflict/partial PASS.
- **Unlocks:** E-06; join con F-04/F-05.
- **Accepted debt:** artefactos grandes quedan en Forge por refs.
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

### E-05 Analytics convergence A0

- **ID / status / size:** E-05 · To Do · MEDIUM
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
- **Planning:** TOP. **Implementation:** NORMAL. **GOD:** NONE.

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

- **2026-09-10** — Enlace mínimo al subproyecto de implementación [[Echo — E-03 Identity and BWC Foundation E0]]. Baseline E-03 = E-01 certified `91671f6f`. No se reescribió el roadmap.
- **2026-09-07** — Reparentado a [[Echo — Producto Integrado]], `owner: agent`. E2 partido en E-06…E-09. E-02 extraído como H1. Tareas `#owner/me` de 4 ítems supersedidas. S0 permanece aquí.
- **2026-09-07** — Enlace mínimo al subproyecto de implementación [[Echo — E-01 Canonical SDK Foundation S0]]. Baseline E-01 fijado `04c16bd2`. No se reescribió el roadmap.

## 🧭 Decisiones

- S0 es de Echo, no Integration.
- E2 no es una Agent Task.
- Front V1 es READ/OBSERVE.

## 🔗 Docs / Links

- [[Echo — E-01 Canonical SDK Foundation S0]]
- [[Echo — E-03 Identity and BWC Foundation E0]]
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
