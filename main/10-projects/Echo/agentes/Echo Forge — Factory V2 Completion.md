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
repo: xKoRx/symphony
jira:
prs:
aliases:
  - Factory V2 Completion
  - Echo Forge Factory V2
  - F0 F1 D F2 Forge
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-07"
updated: "2026-09-12"
---

# Echo Forge — Factory V2 Completion

%% Naming: Echo Forge — Factory V2 Completion es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — Factory V2 Completion
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Producto Integrado]] · **Repo:** `xKoRx/symphony`
> Subproyecto de agente. Cada fase = una Agent Task `#owner/agent`. F-01 CLOSED: [[Echo Forge — F-01 Canonical generation concurrency]] / [[Echo Forge — F-01 Canonical Generation Concurrency Contract]]. F-02 CLOSED: [[Echo Forge — F-02 Finalist Model V2]] / [[Echo Forge — F-02 Finalist Model V2 Contract]]. F-03 CLOSED: [[Echo Forge — F-03 SQX long-running]] / [[Echo Forge — F-03 SQX Long-Running Contract]]. F-04 C5 CONTRACT CLOSED: [[Echo Forge — F-04 Magic allocation, version seal and handoff]] / [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] — READY FOR NORMAL C5; C4 CLOSED @ `bba833d`; T2.11–T2.13 OPEN; not physical-ready. F-05 pendiente.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre humano tiene la tarea puente `#type/supervision`. Las fases internas no inundan el cockpit.

## 🎯 Objetivo

Completar la factory V2: crear supply, evaluar con robustez, validar físicamente, producir finalistas estructurales, reponer, sellar versiones exactas, emitir handoffs canónicos, recuperar bien, correr cómputos largos SQX, pasar FULL golden real y exponer result surfaces.

Echo SDK gobierna el lenguaje compartido. Forge **no** escribe DB Echo, **no** calcula eligibility/capital/activation, **no** recalcula membership en Echo.

## 📊 Estado actual

- **F-01 CLOSED. F-02 CLOSED. F-03 CLOSED. F-04 C5 CONTRACT CLOSED (2026-09-12) — READY FOR NORMAL C5; C4.1–C4.6 CLOSED @ `bba833d`; T2.11–T2.13 OPEN; not physical-ready.** Manifest identity must not parse CanonicalStrategyID. E-04 join sigue one-shot separado. F-05 pendiente.
- **Cerrado y no reabrir:** B1A PASS/CLOSED `185825c` (ownership global ETCD CAS, reuse durable EX5/HTM). B1B PASS/CLOSED `ef65dd1` (sin wall-clock de negocio; cap Campaign=4 eliminado). B2 PASS/CLOSED `db8a022` (Temporal cancel ≠ pérdida de attempt; singleton/drain/recovery). Slot Pool V2 y fencing V3 frozen. Factory V1 contractual cerrado; **no** equivale a V2.
- **Roadmap vigente:** F-01 CLOSED, F-02 CLOSED, F-03 CLOSED; F-04 WIP (NORMAL C5; not physical-ready); F-05 pendiente.
- **Base observada:** Symphony `master`=`origin/master`=`382f4ba5d417371f778e21619ed9eb72624a23f4`; merge-base previo F-03=`e50cb7e`; worktree CLEAN. SDK Temporal declarado v1.35.0 vs workspace v1.44.1: no confundir pin/build/binario.
- **Dependencia Echo:** F-01/F-02/F-03 independientes de S0. F-04 consume pin [[Echo — Live Platform V1]] E-01. Catálogo CC owner antes de allocation real.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `master` (F-03 integrada); F-04 branch `feature/f04-magic-version-handoff` (HEAD `bba833d`) | `0b9742b09019526a8119f086199d15d1f0d42cb1` | F-04: este padre | F-04: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | **F-01 CLOSED**; **F-02 CLOSED**; **F-03 PASS / CLOSED `382f4ba`**; **F-04 C5 READY FOR NORMAL; C4 CLOSED @ `bba833d`; T2.11–T2.13 OPEN; not physical-ready**; F-05 pendiente |

## 🧩 Subproyectos

Hijos: [[Echo Forge — F-01 Canonical generation concurrency]] (CLOSED). [[Echo Forge — F-02 Finalist Model V2]] (CLOSED). [[Echo Forge — F-03 SQX long-running]] (CLOSED). [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (WIP C5). C1/C2 siguen siendo milestones internos de F-02, no proyectos extra.

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> Este board muestra `#owner/agent`. El humano sigue el curro desde [[Echo — Producto Integrado]].

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] [[Echo Forge — F-01 Canonical generation concurrency]] F-01 Canonical generation concurrency #owner/agent #type/dev #area/echo
> - [x] [[Echo Forge — F-02 Finalist Model V2]] F-02 Finalist Model V2 (C1+C2) #owner/agent #type/dev #area/echo
> - [x] [[Echo Forge — F-03 SQX long-running]] F-03 SQX long-running #owner/agent #type/dev #area/echo
> - [/] [[Echo Forge — F-04 Magic allocation, version seal and handoff]] F-04 Magic allocation, version seal and handoff #owner/agent #type/dev #area/echo
> - [ ] F-05 Cohesive release, physical cert and FULL golden #owner/agent #type/dev #area/echo

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

Cada bloque es el contenedor de planificación. No es SPEC. TOP futuro debe fijar baseline, allowed files, tests y stop conditions. Size: S/M/L relativo a este track.

### F-01 Canonical generation concurrency

- **ID / status / size:** F-01 · Done · MEDIUM
- **Implementation project:** [[Echo Forge — F-01 Canonical generation concurrency]]
- **SPEC:** [[Echo Forge — F-01 Canonical Generation Concurrency Contract]]
- **Outcome (2026-09-08):** PASS/CLOSED — commit final `0509342439cfbaa048839088787458dde1ed1b05` en `master` (ff-only); G34 P1–P8 SOURCE/CONTRACT PASS, registry-postgres DEGRADED por entorno. IDs estables desbloquean F-04/F-05.
- **Objective:** Hacer `CanonicalStrategyID` puro **después** de probar un discriminador durable de output de productores concurrentes intra-wave. HOST_KEY resolvió colisiones reales de Builder; no borrarlo a ciegas.
- **Capability unlocked:** generación paralela sin colisión de identidad; IDs adoptados intactos.
- **Product value:** supply concurrente correcto; desbloquea retiro futuro del sufijo host.
- **Why this phase exists:** sin proof intra-wave, “pureza” de ID recrea el bug que HOST_KEY tapó.
- **Frozen input contracts:** [[2026-09-04-echo-forge-campaign-builder-supply-identity]]; identity V2 GENERATED_STRATEGY; [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] §3 identidades. No reabrir StrategyRef UUID.
- **In scope:** proof de unicidad concurrente multiworker/crash; wrapper conocidos; discriminador durable si el proof lo exige; G34.
- **Out of scope:** retirar sufijos adoptados antes del proof; magic allocation; Finalist V2; S0 wire; B1/B2.
- **Dependencies:** ninguna de Echo. Independiente de F-02/F-03.
- **Cross-project:** none.
- **Parallel with:** F-02, F-03, E-01, E-02.
- **Hypotheses:** HOST_KEY no es identidad de negocio; el discriminador durable de logical producer es `ExecutionIntentKey`, no `OutputNamespaceOwnership`.
- **Risks:** colisión intra-wave no reproducida en test débil; retirar sufijo rompe IDs adoptados.
- **Output authority:** CanonicalStrategyID + proof G34. Adopted IDs intactos.
- **Certification:** SOURCE PASS + CONTRACT/concurrency PASS (G34 unit + registry multiworker/crash). No PHYSICAL de flota salvo que la SPEC toque runtime de generación.
- **Done when:** proof intra-wave PASS; no se eliminó HOST_KEY/sufijo sin esa evidencia; IDs históricos no renombrados.
- **Unlocks next:** F-04 puede sellar versiones sobre IDs estables; F-05 golden no depende de retirar sufijo.
- **Accepted debt:** host-suffixed adopted IDs hasta proof.
- **Planning:** TOP corregido in-place 2026-09-07, pendiente manager re-review. **Implementation:** NORMAL no autorizado aún. **GOD REQUIRED NOW:** NONE.

### F-02 Finalist Model V2 (C1+C2)

- **ID / status / size:** F-02 · Done · LARGE (una capacidad; milestones internos C1/C2, no tres fases)
- **Implementation project:** [[Echo Forge — F-02 Finalist Model V2]]
- **SPEC:** [[Echo Forge — F-02 Finalist Model V2 Contract]]
- **Outcome (2026-09-08):** PASS/CLOSED — commit final `c3b7ede4da5caa5f3294533b0dcf5e8570369c38` en `master` (ff-only desde `0509342`); T1.1–T1.6 DONE; migration `014_finalist_promotion_v2` en runner; `master` quedó en `e50cb7e` tras rescate documental separado del manifest `0.2.96`. Desbloquea F-04/F-05 membership V2.
- **Objective:** Membresía estructural V2, Promotion V2, warnings, gates estructurales, Campaign BWC, Result Surface V2, finalists nullable/no-rank, compatibilidad historia V1.
- **Capability unlocked:** Finalist ≠ Top N; NOT_COMPARABLE válido puede seguir finalista; mismatch requested symbol/TF bloquea; ranking/warnings aparte.
- **Product value:** supply estructuralmente honesto; UI/result inspectable; no perder candidatos físicos por score.
- **Why:** V1 copia TopProjection; es la semántica WRONG del target. Histórico C1+C2 es **un** modelo.
- **Frozen input:** [[2026-09-06-echo-forge-finalist-model-v2]]; SDK §§ membership/ranking; checkpoint B2. No reabrir B1/B2.
- **In scope:** C1 core/gates/warnings/promotion; C2 Campaign BWC, result v2, nullable rank, V1 replay. Recert física acotada al cambio.
- **Out of scope:** handoff/magic/S0; eligibility Echo; ranking como admisión; nuevo modelo de score.
- **Dependencies:** B2 CLOSED. No S0.
- **Parallel with:** F-01, F-03, E-01.
- **Hypotheses:** membership estructural + result v2 cubre BWC sin reescribir Decisions V1.
- **Risks:** romper Result V1 replay; mezclar rank 0 con no-rank.
- **Output authority:** Decision/Result V2 + replay V1 intacto.
- **Certification:** SOURCE + CONTRACT (G01–03/G11–12/G22) + PHYSICAL recert del path de promotion tocado, no nueva auditoría de ownership.
- **Done when:** V2 estructural PASS; V1 history readable; zero finalists honesto; NOT_COMPARABLE no expulsa por sí solo.
- **Unlocks:** F-04 membership exacta en handoff; F-05 golden nonempty estructural.
- **Accepted debt:** policy 1.0.0 histórica inmutable.
- **Planning:** TOP persistió SPEC + TASKS 2026-09-08. **Implementation:** NORMAL no autorizado. **GOD:** NONE.

### F-03 SQX long-running

- **ID / status / size:** F-03 · CLOSED · MEDIUM
- **Implementation project:** [[Echo Forge — F-03 SQX long-running]]
- **SPEC:** [[Echo Forge — F-03 SQX Long-Running Contract]]
- **Outcome (2026-09-10):** PASS/CLOSED — commit `382f4ba5d417371f778e21619ed9eb72624a23f4` integrado por ff-only a `master` y pushed; SOURCE/CONTRACT PASS y PHYSICAL PASS con job real `14m51.98s` COMPLETED, 3000/3000, 0 errores, heartbeat vivo a T+10m y cancel árbol aislado. `DATABASE MIGRATION: NONE`.
- **Objective:** Elapsed wall-clock ≠ failure en Builder/Optimizer/WFM/etc. Quitar deadlines de negocio arbitrarios preservando liveness/recovery. SQX sigue serial por máquina/databank; no hereda allocator MT5.
- **Capability unlocked:** jobs SQX largos terminan; cancel explícito sigue siendo la muerte cooperativa.
- **Product value:** factory no aborta cómputo sano; simétrico al freeze MT5 B1B.
- **Why:** D quedó cerrado sin confundir elapsed sano con failure de negocio.
- **Frozen input:** mismo principio B1B; [[2026-09-06-echo-forge-mt5-execution-model-v2]] no se copia a SQX slots.
- **In scope:** timeouts de negocio SQX/Temporal de esas etapas; heartbeat/liveness; recovery. Medir duration.
- **Out of scope:** slots MT5; takeover; Finalist; S0; budget de admisión owner (separado); Adaptive DEPRECATED.
- **Dependencies:** ninguna Echo. Independiente de F-01/F-02.
- **Parallel with:** F-01, F-02, E-01.
- **Hypotheses:** techo técnico Temporal + heartbeat basta; el budget de capacidad no debe matar el job.
- **Risks:** confundir liveness con deadline de campaña; tocar databanks SQX con semántica de pool MT5.
- **Output authority:** contratos de activity SQX sin kill por wall-clock de negocio.
- **Certification:** SOURCE/CONTRACT + PHYSICAL SQX PASS (job largo sobre el límite viejo termina; cancel explícito mata sólo su árbol).
- **Done when:** no existe deadline de negocio que mate Builder/Optimizer/WFM sano; liveness real conservada.
- **Unlocks:** F-05 puede incluir cómputos largos en golden.
- **Accepted debt:** serialización SQX one-job-per-machine.

### F-04 Magic allocation, version seal and handoff

- **ID / status / size:** F-04 · WIP (C5 READY FOR NORMAL; not physical-ready) · LARGE (pipeline único; milestones internos allocation→stamp→seal→adapter; no F-04A/F-04B)
- **Objective:** Tras pin S0: allocation durable de magic, stamp/readback, effective inputs exactos, seal de StrategyVersion, productor `HandoffManifestV1`, adapter de aplicación Forge→Echo.
- **Capability unlocked:** paquete exportable que Echo puede ingerir sin latest/folder query.
- **Product value:** puente real Forge→Echo; Forge sigue dueño de magic y membership.
- **Why:** sin seal/handoff, Finalist V2 no sale del recinto Forge.
- **Frozen input:** SDK §§9–13 y FR-1…FR-5 ya en pin S0; live authority §3 StrategyVersion; O2 catálogo CC. HashIdentity legacy newline **distinto** de `H()`.
- **In scope:** registry allocation CAS/no recycle; stamp; compile/readback bytes; seal; manifest write-once; thin client adapter. Fixtures G04–10/G19–25. G22 cero POST indelegable.
- **Out of scope:** escribir DB Echo; eligibility; catálogo CC inventado; retirar HOST_KEY si F-01 no pasó; B1/B2.
- **Dependencies:** **E-01 S0 pin**; F-01 antes de retirar discriminador host; F-02 para membership V2 nueva (V1 smoke posible con fixtures). **Owner CC antes de allocation física.**
- **Parallel with:** E-03 verification, E-04 development (no E-04 master merge), E-05 tras pin.
- **Hypotheses:** allocation-before-Apply + seal-after-bytes es implementable sin nuevo agregado; adapter no hace POST profundo de workflow.
- **Risks:** allocation sin CC; seal antes de bytes; adapter que active Echo.
- **Output authority:** StrategyVersion sealed + HandoffManifest write-once + delivery status.
- **Certification:** SOURCE + CONTRACT (unique/CAS, replay magic, readback, corpus compartido). PHYSICAL de stamping cuando haya catálogo. INTEGRATION con E-04: mismo pin/digest.
- **Done when:** manifest fixture idéntico lo acepta el consumer del mismo release; no side-effects Echo; CC bloquea allocation real si falta.
- **Unlocks:** F-05 golden de handoff; E-04 puede dejar fakes.
- **Accepted debt:** HashIdentity legacy; attach Echo no es de esta fase.
- **Status:** WIP. C5 CONTRACT CLOSED 2026-09-12 — READY FOR NORMAL. C4.1–C4.6 CLOSED @ `bba833d`. SPEC [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]. Hijo [[Echo Forge — F-04 Magic allocation, version seal and handoff]]. T2.11–T2.13 OPEN. Not physical-ready. Migration 015/016; C4/C5 migration NONE.

### F-05 Cohesive release, physical cert and FULL golden

- **ID / status / size:** F-05 · To Do · MEDIUM
- **Objective:** Un release cohesivo de lo implementado, matriz determinística, certificación física MT5 de superficies tocadas, conformidad de handoff, BWC, FULL golden **real** y result surfaces inspectables. Source merge ≠ product completion.
- **Capability unlocked:** factory V2 operable: supply queryable, costo/latencia observables, al menos un finalista estructural con artifacts verificados cuando el cómputo lo permita.
- **Product value:** owner lanza campaign, deja calcular, inspecciona funnel/warnings y obtiene/razona finalistas (H2).
- **Why:** cert física y golden no caben dentro de cada slice sin crear releases-por-fix ni un catch-all de implementación.
- **Frozen input:** cert V2 mínima del master arquitectura §5; C3 0.2.96 no se extiende a V2; no tercer FULL bajo timeout viejo.
- **In scope:** release único del burn-down F-01…F-04 (o el subconjunto mergeado); three-slot/cancel/retry/drain recert **de lo cambiado** (B1/B2 no se reimplementan); FULL real; result read surface; handoff conformance contra pin S0.
- **Out of scope:** reabrir ownership; yield económico; eligibility Echo; recertificar Slot Pool desde cero sin delta.
- **Dependencies:** F-01, F-02, F-03; F-04 para golden de handoff. E-04 para smoke ingestión real (fixtures primero).
- **Parallel with:** cadena live Echo post E-04.
- **Hypotheses:** un release + matriz física cierra V2 factory; zero-supply sigue siendo resultado válido.
- **Risks:** declarar PRODUCT PASS con mocks; mezclar deploy viejo con HEAD nuevo.
- **Output authority:** release pin + cert manifest + golden refs.
- **Certification:** RELEASE + PHYSICAL + PRODUCT CAPABILITY (factory usable). INTEGRATION PASS handoff→receipt si E-04 listo; si no, CONTRACT PASS de fixtures y PHYSICAL factory igual.
- **Done when:** criterios de completion abajo. Zero finalists honesto no falla el software.
- **Unlocks:** Echo enrollment con candidata real; no bloquea diseño Echo previo.
- **Accepted debt:** cert singleton Windows residual documentada si sigue pendiente de Kronos, explicitada en el manifest, no escondida.
- **Planning:** TOP (plan de cert/release). **Implementation:** NORMAL. **GOD:** NONE.

## Definition of Done — Factory V2

Factory puede crear supply, evaluar robusto, validar físicamente, producir finalistas estructurales, replenish, sellar versiones exactas, emitir handoffs canónicos, recuperar, correr cómputos largos, pasar FULL golden real y exponer result surfaces. No promete yield rentable ni eligibility Echo.

## 📆 Bitácora

- **2026-09-12** — TOP F-04 C5 CONTRACT CLOSED: identidad del HandoffManifestV1 desde `sqx.strategies`; CanonicalStrategyID opaco; BOTH fail closed; migration NONE. C4 permanece CLOSED @ `bba833d`. Tarea puente F-04 sigue `[/]` (not physical-ready). T2.11–T2.13 OPEN.
- **2026-09-12** — NORMAL C4.1–C4.6 implementados sobre `d645ed6` → commit `bba833d` pushed a `feature/f04-magic-version-handoff`: allocation desde `sqx.strategies`, `MagicV1DirectionFromStrategy`, replay/conflict vía `DecodeMagicV1`, TaskSpec magic no requested, migration NONE. Sets rojos pre-existentes idénticos a baseline. Residual de seal/handoff lo posee C5. **C4 CLOSED.**
- **2026-09-12** — TOP F-04 C4 CONTRACT CLOSED: Magic V1 no parsea CanonicalStrategyID; instrument/direction = `sqx.strategies`; TaskSpec `magic_number` no es requested. NORMAL C4 pendiente. Tarea puente F-04 `[r]→[/]`. T2.13 E-04 runtime queda one-shot separado.
- **2026-09-11** — E-04 TOP: [[Echo — E-04 Forge Ingestion E1]] congela HTTP/S0/receipt para que F-04/F-05 avancen contra contrato estable. INTEGRATION/CROSS_LANE de handoff sigue gated por E-03 CONTRACT_PASS; development E-04 paralelo autorizado. Join Forge no se marca closed.
- **2026-09-07** — TOP F-01 persistió SPEC [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] e hijo [[Echo Forge — F-01 Canonical generation concurrency]]. NORMAL no autorizado.
- **2026-09-07** — Corrección F-01 in-place: discriminator = `ExecutionIntentKey`; FlowRun/NS ownership insuficiente. NORMAL no autorizado.
- **2026-09-07** — F-01 corrección 02: filename budget; Campaign `FilenameToken` no se proyecta en GENERATED nuevos. NORMAL no autorizado.
- **2026-09-08** — **F-01 PASS/CLOSED.** Implementación ZCode `0509342` integrada a `master` por fast-forward only y pushed; gate G1 cerrado por orden del manager. G34 P1–P8 PASS; registry-postgres DEGRADED por entorno (preexistente). F-02–F-05 siguen To Do, no despachados.
- **2026-09-08** — TOP F-02 persistió SPEC [[Echo Forge — F-02 Finalist Model V2 Contract]] e hijo [[Echo Forge — F-02 Finalist Model V2]]. Baseline symphony `0509342`. Migration `014_finalist_promotion_v2`. NORMAL no autorizado.
- **2026-09-08** — **F-02 PASS/CLOSED.** Implementación Codex `c3b7ede` integrada a `master` por fast-forward only y pushed; G1 cerrado por orden del manager. Limpieza del dirty tree local: 5 archivos restaurados (config ejemplo, fixtures regenerables de specs cerradas, índice SPECS.md, workspace editorial), 4 RCA/CHANGE de la campaña C3 eliminados (materializados en Agents OS/source o superseded por frozen V2: registro Adaptive ya removido, `ParseCFXConfiguredPeriod` en source, orphan MT5 en B2/V3, execution model V1 superseded por Slot Pool V2), y `deploy/manifest.json 0.2.96` rescatado como commit separado `e50cb7e`. Backup safety temporal en `/tmp`, no autoridad. F-03–F-05 siguen To Do, no despachados.
- **2026-09-08** — TOP F-03 persistió SPEC [[Echo Forge — F-03 SQX Long-Running Contract]] e hijo [[Echo Forge — F-03 SQX long-running]]. Baseline symphony `e50cb7e`. `DATABASE MIGRATION: NONE`. NORMAL no autorizado.
- **2026-09-08** — TOP CORRECTION F-03 C1–C3: ceiling `MaxInt64ns−1s`; Adaptive DEPRECATED no-touch; process-tree obligatorio. NORMAL sigue no autorizado.
- **2026-09-10** — TOP F-04 persistió SPEC [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] e hijo [[Echo Forge — F-04 Magic allocation, version seal and handoff]]. Baseline `382f4ba`. S0 `91671f6f`. CC_MISSING_OWNER_GATE. Migration 015. NORMAL no autorizado.

## 🧭 Decisiones

- No crear fases C1, C2 y F1 separadas.
- D es fase propia.
- F2 espera pin S0; F0/F1 no.

## 🔗 Docs / Links

- [[Echo — Producto Integrado]]
- [[Echo Forge — F-01 Canonical generation concurrency]]
- [[Echo Forge — F-01 Canonical Generation Concurrency Contract]]
- [[Echo Forge — F-02 Finalist Model V2]]
- [[Echo Forge — F-02 Finalist Model V2 Contract]]
- [[Echo Forge — F-03 SQX long-running]]
- [[Echo Forge — F-03 SQX Long-Running Contract]]
- [[Echo Forge — F-04 Magic allocation, version seal and handoff]]
- [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]
- [[Echo — Live Platform V1]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]
- [[Echo Forge]]
- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
- [[2026-09-06-echo-forge-finalist-model-v2]]
- [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]]
- [[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]]

## 💡 Ideas

### Backlog de ideas

- Viewer SQX: SHOULD del padre, no fase Forge V2.

### Motivos / principios

- Elapsed wall-clock ≠ failure. Membership ≠ rank.

### Memoria pública / interna

- **Memoria pública:** Decisions MT5/Finalist enlazadas.
- **Memoria interna:** no duplicar checkpoint B2 aquí.
- **Motivo:** control histórico sigue en el proyecto de persistencia.
