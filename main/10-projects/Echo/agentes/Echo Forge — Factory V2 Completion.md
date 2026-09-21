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
updated: "2026-09-21"
---

# Echo Forge — Factory V2 Completion

%% Naming: Echo Forge — Factory V2 Completion es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — Factory V2 Completion
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Producto Integrado]] · **Repo:** `xKoRx/symphony`
> Subproyecto de agente. Cada fase = una Agent Task `#owner/agent`. F-01 CLOSED: [[Echo Forge — F-01 Canonical generation concurrency]] / [[Echo Forge — F-01 Canonical Generation Concurrency Contract]]. F-02 CLOSED: [[Echo Forge — F-02 Finalist Model V2]] / [[Echo Forge — F-02 Finalist Model V2 Contract]]. F-03 CLOSED: [[Echo Forge — F-03 SQX long-running]] / [[Echo Forge — F-03 SQX Long-Running Contract]]. F-04 CLOSED (CERT-F04-01/02 PASS 2026-09-20; CERT-E04-01 + CERT-F04-03 PASS 2026-09-21; T2.11/T2.12/T2.13 satisfechos): [[Echo Forge — F-04 Magic allocation, version seal and handoff]] / [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]. F-05-I IMPLEMENTED / SOURCE VERIFIED (T7-CLOSE `3d0e8c9`): [[Echo Forge — F-05-I Cohesive release and read surfaces]] / [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]. **F-05-C COMPLETADA 2026-09-21: `CERT_F05_01_PASS` + `CERT_F05_02_PASS` + `CERT_F05_03_PASS` → `FACTORY_V2_PHYSICALLY_CERTIFIED` — release cohesiva `0.2.105` @ `745bc8b`, campaña FULL `0ce72173…` con 3 finalistas y HTM byte-verificados; manifest final en `~/aranea/work/cert-f05-20260921/CERT-F05-03-MANIFEST-PASS-20260921.md`.**

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre humano tiene la tarea puente `#type/supervision`. Las fases internas no inundan el cockpit.

## 🎯 Objetivo

Completar la factory V2: crear supply, evaluar con robustez, validar físicamente, producir finalistas estructurales, reponer, sellar versiones exactas, emitir handoffs canónicos, recuperar bien, correr cómputos largos SQX, pasar FULL golden real y exponer result surfaces.

Echo SDK gobierna el lenguaje compartido. Forge **no** escribe DB Echo, **no** calcula eligibility/capital/activation, **no** recalcula membership en Echo.

## 📊 Estado actual

- **F-01 CLOSED. F-02 CLOSED. F-03 CLOSED. F-04 C5.1–C5.6 IMPLEMENTED (2026-09-12) @ `b57bfb2` — release `0.2.98` publicada desde el SHA certificado el 2026-09-13. Corrección de autoridad: Zeus/Hera/Kronos sí ejecutan `/opt/stager/releases/0.2.98/bin/symphony` bajo `stager-runtime.service`; los marcadores `/opt/symphony/*` observados históricamente son legacy/no-authoritative. Windows `mt5-kronos` tiene un **MCP viewer policy gap confirmado tras probes mínimos allowlisted**: sólo identidad de host fue legible; servicio/proceso/path/release/poller siguen sin evidencia, por lo que el rollout global sigue bloqueado; T2.11–T2.13 OPEN; not physical-ready and F-04 not closed.** Manifest identity must not parse CanonicalStrategyID. E-04 join sigue one-shot separado. F-05 pendiente.
- **Cerrado y no reabrir:** B1A PASS/CLOSED `185825c` (ownership global ETCD CAS, reuse durable EX5/HTM). B1B PASS/CLOSED `ef65dd1` (sin wall-clock de negocio; cap Campaign=4 eliminado). B2 PASS/CLOSED `db8a022` (Temporal cancel ≠ pérdida de attempt; singleton/drain/recovery). Slot Pool V2 y fencing V3 frozen. Factory V1 contractual cerrado; **no** equivale a V2.
- **Roadmap vigente:** F-01 CLOSED, F-02 CLOSED, F-03 CLOSED; F-04 `IMPLEMENTED / SOURCE VERIFIED / RELEASED`, no físicamente certificado; F-05 se divide en preparación de implementación y campaña de certificación.
- **Base observada:** Symphony `master`=`origin/master`=`382f4ba5d417371f778e21619ed9eb72624a23f4`; merge-base previo F-03=`e50cb7e`; worktree CLEAN. SDK Temporal declarado v1.35.0 vs workspace v1.44.1: no confundir pin/build/binario.
- **Dependencia Echo:** F-01/F-02/F-03 independientes de S0. F-04 consume pin [[Echo — Live Platform V1]] E-01. Catálogo CC owner antes de allocation real.

### Decisión de continuidad y taxonomía de estado

La certificación física/de infraestructura se retira temporalmente del critical path de desarrollo mientras termina el [[AGENT-PLATFORM - MCP Access Plane]]; se difiere, no se waiva. `IMPLEMENTED != CERTIFIED`. Estados válidos: `PLANNED → IMPLEMENTED → SOURCE VERIFIED → RELEASED → DEPLOYED → PHYSICALLY CERTIFIED → CROSS-LANE CERTIFIED → CLOSED`; un estado posterior no se infiere por el anterior y se conserva la evidencia histórica.

F-04 truth: implementation DONE; contract/source verification DONE; release `0.2.98` publicada desde `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; Linux rollout PASS; Windows runtime certification BLOCKED by Aranea MCP viewer policy; authentic golden and Echo join deferred. Overall: `IMPLEMENTED / NOT CERTIFIED`.

La backlog ordenada y no ejecutada vive en [[Echo + Echo Forge — Deferred Certification Backlog]]. El trigger es capability MCP operacional/certificada más runtimes objetivo observables/operables; no se usa fecha calendario.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `master` (F-03 integrada); F-04 branch `feature/f04-magic-version-handoff` (HEAD `b57bfb2`) | `bba833d7b57c767d6ce5ebfeae7a7b71b5785782` | F-04: este padre | F-04: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | **F-01 CLOSED**; **F-02 CLOSED**; **F-03 PASS / CLOSED `382f4ba`**; **F-04 C5.1–C5.6 IMPLEMENTED `b57bfb2` — READY FOR MANAGER REVIEW; C4 CLOSED @ `bba833d`; T2.11–T2.13 OPEN; not physical-ready/not closed**; F-05 pendiente |

## 🧩 Subproyectos

Hijos: [[Echo Forge — F-01 Canonical generation concurrency]] (CLOSED). [[Echo Forge — F-02 Finalist Model V2]] (CLOSED). [[Echo Forge — F-03 SQX long-running]] (CLOSED). [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (WIP C5; C5.1–C5.6 IMPLEMENTED, manager review pending). [[Echo Forge — F-05-I Cohesive release and read surfaces]] (IMPLEMENTED / SOURCE VERIFIED @ `3d0e8c9`; físico diferido a F-05-C). [[Echo Forge — Forge Explorer v0]] (PLANNING FROZEN 2026-09-21; visor read-only sobre la read surface F-05-I; implementación NORMAL pendiente). C1/C2 siguen siendo milestones internos de F-02, no proyectos extra.

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> Este board muestra `#owner/agent`. El humano sigue el curro desde [[Echo — Producto Integrado]].

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] [[Echo Forge — F-01 Canonical generation concurrency]] F-01 Canonical generation concurrency #owner/agent #type/dev #area/echo
> - [x] [[Echo Forge — F-02 Finalist Model V2]] F-02 Finalist Model V2 (C1+C2) #owner/agent #type/dev #area/echo
> - [x] [[Echo Forge — F-03 SQX long-running]] F-03 SQX long-running #owner/agent #type/dev #area/echo
> - [/] [[Echo Forge — F-04 Magic allocation, version seal and handoff]] F-04 implementation complete; physical/cross-lane certification deferred #owner/agent #type/dev #area/echo
> - [ ] [[Echo Forge — F-05-I Cohesive release and read surfaces]] F-05-I Cohesive release/read-surface preparation #owner/agent #type/dev #area/echo
> - [ ] [[Echo Forge — Forge Explorer v0]] Forge Explorer v0 (visor local read-only; SPEC frozen, implementación NORMAL pendiente) #owner/agent #type/dev #area/echo
> - [ ] F-05-C Release/physical/FULL golden certification campaign #owner/agent #type/admin #area/echo #blocked

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
- **Status:** WIP. C5.1–C5.6 IMPLEMENTED 2026-09-12 @ `b57bfb2` — READY FOR MANAGER REVIEW. C4.1–C4.6 CLOSED @ `bba833d`. SPEC [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]. Hijo [[Echo Forge — F-04 Magic allocation, version seal and handoff]]. Parent bridge remains `[/]`; T2.11–T2.13 OPEN. F-04 not physical-ready/not closed. Migration 015/016; C4/C5 migration NONE.

### F-05 Cohesive release, physical cert and FULL golden

- **ID / status / size:** F-05 · split: implementation `PLANNED (SPEC frozen)`; certification `DEFERRED / BLOCKED BY INFRASTRUCTURE` · MEDIUM
- **Implementation project:** [[Echo Forge — F-05-I Cohesive release and read surfaces]]
- **SPEC:** [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]
- **Objective:** Un release cohesivo de lo implementado, matriz determinística, certificación física MT5 de superficies tocadas, conformidad de handoff, BWC, FULL golden **real** y result surfaces inspectables. Source merge ≠ product completion.
- **Capability unlocked:** factory V2 operable: supply queryable, costo/latencia observables, al menos un finalista estructural con artifacts verificados cuando el cómputo lo permita.
- **Product value:** owner lanza campaign, deja calcular, inspecciona funnel/warnings y obtiene/razona finalistas (H2).
- **Why:** cert física y golden no caben dentro de cada slice sin crear releases-por-fix ni un catch-all de implementación.
- **Frozen input:** cert V2 mínima del master arquitectura §5; C3 0.2.96 no se extiende a V2; no tercer FULL bajo timeout viejo.
- **In scope implementation:** matriz determinística del release, preparación de result/read surfaces y conformance checklist para outputs ya existentes, sin nuevo contrato ni sustitución de golden.
- **In scope certification:** release único del burn-down F-01…F-04 (o el subconjunto mergeado); three-slot/cancel/retry/drain recert **de lo cambiado** (B1/B2 no se reimplementan); FULL real; handoff conformance contra pin S0.
- **Out of scope:** reabrir ownership; yield económico; eligibility Echo; recertificar Slot Pool desde cero sin delta.
- **Dependencies:** F-01, F-02, F-03; F-04 para golden de handoff. E-04 para smoke ingestión real (fixtures primero).
- **Parallel with:** cadena live Echo post E-04.
- **Hypotheses:** un release + matriz física cierra V2 factory; zero-supply sigue siendo resultado válido.
- **Risks:** declarar PRODUCT PASS con mocks; mezclar deploy viejo con HEAD nuevo.
- **Output authority:** release pin + cert manifest + golden refs.
- **Certification:** la preparación puede avanzar ahora; RELEASE + PHYSICAL + PRODUCT CAPABILITY requieren la campaña [[Echo + Echo Forge — Deferred Certification Backlog]]. INTEGRATION PASS handoff→receipt requiere E-04/T21 y golden auténtico.
- **Done when:** criterios de completion abajo. Zero finalists honesto no falla el software.
- **Unlocks:** Echo enrollment con candidata real; no bloquea diseño Echo previo.
- **Accepted debt:** cert singleton Windows residual documentada si sigue pendiente de Kronos, explicitada en el manifest, no escondida.
- **Planning:** TOP F-05-I cerró SPEC + tareas F05I-T1…T7 el 2026-09-13 (README del proyecto hijo). **Implementation:** NORMAL para F-05-I tras manager review; **certification:** diferida hasta trigger de infraestructura. **GOD:** NONE.

#### F-05 split operativo

- **F-05-I — CAN CONTINUE NOW:** preparar release matrix, result/read surface y checklist de conformance usando sólo outputs/fixtures existentes; no marca ningún gate físico.
- **F-05-C — DEFERRED:** ejecutar CERT-F05-01…03 sólo después de CERT-F04-01…03 y de que el Access Plane habilite observación/operación real.

### Dependency classification

| Task | Class | Current truth |
|---|---|---|
| F-04 T2.11/T2.12/T2.13 | C — HARD BLOCKED | Requiere físico, golden auténtico y/o join real; OPEN, no waived. |
| F-05-I | A — CAN CONTINUE NOW | Preparación de release/read-surface sin dependencia semántica de evidencia física. |
| F-05-C | B — CAN IMPLEMENT BUT CANNOT CERTIFY | La preparación documental/tooling puede avanzar; PASS/CLOSED depende de campaña física. |
| E-04 T21/AC-37 | C — HARD BLOCKED | Requiere golden auténtico de Forge y runtime Echo real; synthetic ≠ PASS. |
| E-05 | B — CAN IMPLEMENT BUT CANNOT CERTIFY | No depende de T2.11–T2.13; conserva sus blockers propios de S0/Hasura/verificación. |
| E-06…E-13 | A/B según task | El DAG permite trabajo con fixtures/shadow; las certificaciones físicas/product capability quedan posteriores. |

### Next development task

**(Actualizado 2026-09-21T13:40Z.)** **CERT-F05-01 PASS** (2026-09-21T13:05Z): release cohesiva `0.2.105` @ `codex/f05-release-prep` `745bc8b` (master `0b9742b` + F-04 + F-05-I + fixes C1…C13 + `a2321cc` F-INT-01/02 + `1056b30` F-INT-03 + refresh frozen release matrix `745bc8b`); rollout Stager 4/4 con SHA instalado == manifest EXACT; `vcs.revision=745bc8b` en binarios. Release test gate 6182 obligatorio 53/53 PASS/0 skips; registry-postgres GREEN (4 FAILs del baseline corregidos test-only, `1056b30`); workflows 21 fallos idénticos al baseline por nombre (twin worktree `25a5122`); anti-masking aditivo. Release matrix refrescada por mandato §7: filas F-04 físico + cross-lane DONE con certification_record/cross_lane_receipt; `f05i-read-surface.released` DONE; pipeline conserva DEFERRED CERT-F05-01/02. **CERT-F05-02 EN EJECUCIÓN** (13:22:40Z): campaña FULL `cert-f05-02-20260921T131850Z-fcc90342` sobre `0.2.105` — CampaignRef `0ce72173-b629-4ca4-bf4c-e7e586792e72`, workflows `sqx-forge-campaign-v1-87a7bb80…`/`01a0c422-0935…` + `sqx-main-v1-52fc8a15…`, receta RERUN-6 con diff de exactamente 4 paths (identidades todas nuevas), CFX byte-exactos fd5ffebe/121ec05e/1a993957, preimage SHA `50e51a34…`, dispatch único 6/6 pasos. Siguiente: observación hasta terminalización + result surfaces + CERT-F05-03.

## Definition of Done — Factory V2

Factory puede crear supply, evaluar robusto, validar físicamente, producir finalistas estructurales, replenish, sellar versiones exactas, emitir handoffs canónicos, recuperar, correr cómputos largos, pasar FULL golden real y exponer result surfaces. No promete yield rentable ni eligibility Echo.

## 📆 Bitácora

- **2026-09-21 — TOP Forge Explorer v0 planning frozen (sin tocar source ni el carril CERT).** Visor LOCAL read-only de resultados Forge como pieza nueva delimitada: package `sqx/cmd/forge-explorer` (sólo stdlib) que renderiza HTML en loopback consumiendo exclusivamente los 6 comandos read de `sqx-flowkit` (contrato F-05-I intacto; `push-output` excluido por guard; cero SQL/DI/drivers; loopback-only; GET-only; fail-closed). Baseline `codex/f05-release-prep` @ `745bc8b` (release `0.2.105`) verificado contra origin; branch `codex/forge-explorer-v0` + worktree independientes; SPEC/PLAN/NORMAL-PROMPT frozen en `specs/FEAT-FORGE-EXPLORER-V0/` @ `cc36c39` publicados en origin. Detalle e historial en [[Echo Forge — Forge Explorer v0]]. Implementación NORMAL pendiente de despacho; PHYSICAL CERTIFICATION NOT RUN.
- **2026-09-21 — CERT-F05-01 PASS + CERT-F05-02 despachada (misión F05 FINAL COMPLETION).** G0 baseline `F05_SOURCE_AND_RUNTIME_BASELINE_PASS` (master ancestro del release branch; flota 0.2.104 4/4; `codex/f05-r3-integration` = lane E-06 no integrada). G1: FF `a2321cc`; fix F-INT-03 `1056b30` (DB compartido sin reset por test + invariante V1-origin en autocommit; suite registry-postgres GREEN; test-only); refresh frozen `745bc8b` de la release matrix (F-04 físico/cross-lane DONE con records; allowlist del guard ampliada acotadamente; F-04 PASS vs matriz DEFERRED resuelto). G2 PASS sin regresiones. Release `0.2.105` publicada y desplegada 4/4 (Zeus 2856509 / Hera 1440696 / Kronos 1400507 / Windows 16192; SHA == manifest EXACT; rollback 0.2.104 operativo). Campaña FULL F05-02 dispatch única 13:22:40Z sobre `0.2.105` con identidades todas nuevas; read surface F-05-I verificada viva (`campaign list` ve la campaña RUNNING). Evidencia: `~/aranea/work/cert-f05-20260921/`; delta en el Backlog.
- **2026-09-21 — CERT-F04-03 PASS (HTTPIngress aislado, golden auténtico, sin workers).** 5 receipts INGESTED en Echo DEV `3d260e81`; `sqx.handoff_deliveries` no mutado. F-INT-03 abierto en backlog propio. Siguiente: CERT-F05-01. Evidencia: `~/aranea/work/cert-e04-01/`.
- **2026-09-21 — Deploy Echo Gateway DEV + ingestión funcional (lane Echo; HTTPIngress Forge `a2321cc` aislado, sin workers).** Gateway `2360369c` en Daedalus; 201 INGESTED DEV; **`CERT_F04_03_BLOCKED`** por golden. Evidencia: `~/aranea/work/echo-dev-ingest-close-20260921/FINDINGS-INGEST-CLOSE-20260921.md`.
- **2026-09-21 — Recert CERT-F04-03 / CERT-E04-01 (Daedalus, sin redeploy).** Runtime Echo DEV reconfirmado healthy; Gateway ingest 503 misconfigured; `/symphony/development/echo/ingest/*` ausente; golden corpus revalidate+recompute 5/5 PASS pero bodies GOLDEN_AUTHORITY_BLOCKED; F-INT-01/02/03 STILL_REPRODUCIBLE. Veredicto **`CERT_F04_03_BLOCKED`**. Sin POST auténtico, sin workers, sin PROD.
- **2026-09-20 — Misión FORGE-F04-CONTINUITY/F05-NEXT (lane Forge only; sin efectos laterales).** Reconciliación documental: esta nota quedó desactualizada respecto a F-05-I — el cierre declarativo T7-CLOSE `3d0e8c9` (2026-09-16) ya había dejado F-05-I `IMPLEMENTED / SOURCE VERIFIED` en la SPEC y en el proyecto hijo; verificado en git (`3d0e8c9`/`0ddd4db` en la genealogía de HEAD `25a5122`) y corregido el info box de esta nota. G4 del mandato: **ninguna tarea de ejecución Forge desbloqueada** — F-05-I cerrada; la preparación de CERT-F05-01 (matriz + read surface + checklist + manifest template) ya fue entregada por F-05-I; CERT-F05-01…03 permanecen tras CERT-F04-01…03 por orden frozen; el único gate siguiente es **CERT-E04-01 (T21, lane Echo — dependencia externa, ownership Echo)**. Hallazgo registrado para manager (**FROZEN_CONTRACT_COLLISION potencial**, condición STOP prevista por la SPEC F-05-I): la fila de la release matrix para `f04-magic-allocation`/`f04-strategy-version-seal` declara `physically_certified DEFERRED {CERT-F04-01, CERT-F04-02}`, gates hoy PASS (CERT-F04-01 PHYSICALLY CERTIFIED, CERT-F04-02 PASS/T2.11) — actualizarlas a DONE exigiría ampliar la allowlist histórica física del guard del artefacto (cambio frozen, requiere manager review; NO ejecutado en esta sesión). Continuidad F04-03: frontera A/B/C fijada y paquete `F04-03-FORGE-CONTINUITY.md` creado en el corpus; validador del corpus re-ejecutado PASS; suites herméticas del productor re-evidenciadas @ `25a5122` (PASS + `-race` + vet). Cero campañas/backtests/POST/releases/deploys; producción y Echo intactos; dirty operacional ajeno preservado. Control: delta FORGE-F04-CONTINUITY en [[Echo + Echo Forge — Deferred Certification Backlog]]; agent-run `2026-09-20-zcode-glm-5.3-flash-forge-f04-continuity-f05-next`.

- **2026-09-13 — TOP F-05-I PLANNING COMPLETE.** Recon read-only @ `b57bfb2` confirmó: read models V2 sin callers productivos (`forge.Service`, `LoadForgeCampaignResult`), cero HTTP/API/GraphQL, inspección vía `sqx/tools` informales. SPEC frozen [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]: read surface CLI JSON determinística sobre ports narrow + release matrix declarativa (`deploy/release-matrix.json` + validador `sqx/core/releasematrix`) + funnel proyección pura por `stage_key`; `DATABASE MIGRATION: NONE`; sin HTTP; sin writes; `fixture != authentic physical golden`. Proyecto hijo con F05I-T1…T7, allowed files exactos y matriz de tests congelada. NORMAL pendiente manager review. Ningún gate físico marcado.

- **2026-09-13 — NORMAL F-04 Windows viewer policy proof.** `mt5-kronos` admitió `hostname` y `whoami`; las formas mínimas únicas para `StagerRuntime`, `sqx-mt5-worker`, `C:\\ProgramData\\Stager`, executable y poller fueron rechazadas con `POLICY_DENIED`. Se confirma `PHYSICAL BLOCKED — ARANEA MCP POLICY GAP — MT5 VIEWER`; no operator, no IDs, no LICENSE/T2.12/T2.11. Evidencia detallada en [[2026-09-13-f04-mt5-viewer-policy-gap-summary]].

- **2026-09-13 02:17** — Corrección de autoridad F-04: el intento anterior no probó la ausencia de `0.2.98`, porque usó marcadores legacy `/opt/symphony/*`. La inspección canónica de `stager-runtime.service` prueba `0.2.98` activo en Zeus/Hera/Kronos vía `/opt/stager/releases/0.2.98/bin/symphony`, con activación committed, `CURRENT/PENDING` Stager y pollers `sqx-main-queue`. `mt5-kronos` viewer rechazó toda lectura con `POLICY_DENIED`; no se escaló a operator sólo para inspección. Rollout global `INCONCLUSIVE`, primer stage no probado = autoridad runtime Windows; no se generaron IDs ni se ejecutó licencia/workflow. T2.11/T2.12/T2.13 siguen OPEN. La historia previa se conserva y queda marcada como interpretación corregida.

- **2026-09-13** — F-04 one-shot físico: baseline/release publicados PASS y MCP SSH recuperado; rollout bloqueado por environment porque Zeus/Hera/Kronos no tienen `/opt/symphony/releases/0.2.98`, `PENDING=0.2.40` y `current -> 0.2.40` (el archivo `CURRENT` además contiene `9.9.11`). No se ejecutó flow ni se creó golden. T2.11/T2.12/T2.13 permanecen OPEN; F-04 sigue no cerrado. Evidencia: [[2026-09-13-f04-physical-certification-blocked-summary]].

- **2026-09-12** — NORMAL F-04 C5.1–C5.6 implemented @ `b57bfb2` from exact baseline `bba833d` and pushed fast-forward. Durable `sqx.strategies` row is manifest identity authority; canonical carrier is opaque consistency-only; LONG/SHORT map through Magic V1 and BOTH/unknown/empty fail closed; WorkflowSpec direction is an exact case-sensitive gate; legacy parser removed. Focused race/build/vet pass; worker red set matches baseline; registry full suite timed out in embedded-postgres with no new targeted failure. Parent bridge remains `[/]`; F-04 NOT CLOSED; T2.11–T2.13 OPEN.
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
- [[Echo Forge — F-05-I Cohesive release and read surfaces]]
- [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]
- [[Echo Forge — Forge Explorer v0]]
- [[Echo — Live Platform V1]]
- [[Echo + Echo Forge — Deferred Certification Backlog]]
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
