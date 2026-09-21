---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P2
area: "[[Echo]]"
parent: "[[Echo Forge — Factory V2 Completion]]"
sprint:
start: 2026-09-21
due:
progress: 0
repo: xKoRx/symphony
jira:
prs:
aliases:
  - Forge Explorer v0
  - Echo Forge Explorer
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-21"
updated: "2026-09-21"
---

# Echo Forge — Forge Explorer v0

%% Naming: Echo Forge — Forge Explorer v0 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — Forge Explorer v0
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P2 · **Parent:** [[Echo Forge — Factory V2 Completion]] · **Repo:** `xKoRx/symphony`
> Visor LOCAL y READ-ONLY de los resultados de Echo Forge: un binario Go nuevo (`sqx/cmd/forge-explorer`) que renderiza HTML server-rendered en loopback consumiendo exclusivamente los seis comandos read de `sqx-flowkit` (contrato F-05-I). Sin SQL propio, sin segunda autoridad, sin escrituras, sin HTTP público, sin certificaciones. SPEC/PLAN/NORMAL-PROMPT frozen en `specs/FEAT-FORGE-EXPLORER-V0/` @ `codex/forge-explorer-v0` `cc36c39` (base `745bc8b` = release `0.2.105`). IMPLEMENTADO 2026-09-21: EX0–EX6 con commits atómicos `01ceaa8`→`648d5e6` (push FF a origin); gates §6 GREEN; smoke real read-only contra production PASS. `PHYSICAL CERTIFICATION NOT RUN`.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre humano tiene la tarea puente `#type/supervision`. Las fases internas no inundan el cockpit.

## 🎯 Objetivo

Dar al operador/owner una superficie de inspección visual de los resultados Forge (campañas, runs, estrategias, release matrix) sin abrir bases a mano y sin tocar el carril de certificación: navegación por refs exactos sobre la read surface F-05-I existente, estados vacíos y errores honestos (ausencia ≠ cero, RUNNING sin finalistas inventados, ranking ausente rotulado), seguridad local (loopback-only, GET-only, cero writes) y cero interferencia con los contratos frozen F-05-I.

## 📊 Estado actual

- **Planificación TOP completa (2026-09-21):** SPEC FROZEN v1.0.0 + PLAN con WPs EX0…EX6 + NORMAL-PROMPT completo, commiteados docs-only en `codex/forge-explorer-v0` `cc36c39` y publicados en origin (branch nueva desde `745bc8b94e1f6148ddc16c02eb86a755088c2666`, la punta verificada de `codex/f05-release-prep` = release `0.2.105`; `origin/master` `0b9742b` ancestro). Worktree independiente: `/home/kor/aranea/work/forge-explorer-20260921/symphony`.
- **Decisiones frozen (SPEC §2):** pieza nueva delimitada (verificado @ `745bc8b`: cero frontend y cero HTTP server en la ruta inspect); frontend = HTML server-rendered (`net/http` + `html/template` + `embed`, sin framework JS ni npm); acceso a datos = exec de `sqx-flowkit` con allowlist cerrada de exactamente los 6 comandos read (`campaign get|list`, `run get|stages`, `strategy get`, `release-matrix`); `push-output` excluido y verificado ausente por guard; mapping exec→render fail-closed (exit 0 + schema verificado → render; error → stderr textual; stdout inválido con exit 0 → error interno, jamás render parcial); bind loopback-only (el binario rechaza otra dirección), GET-only, sin auth/CORS; paquete con dependencias sólo stdlib (⇒ cero drivers DB/DI por construcción, gate `go list -deps`); cursor `next_cursor` opaco en pass-through (charset-check, jamás decodificar).
- **Contratos F-05-I intactos:** `docs/echo-forge/f05-read-surface.md` y todo `sqx/cmd/sqx-flowkit/**`, `sqx/core/**`, `sqx/adapters/**` quedan prohibidos en allowed files (SPEC §5). La campaña CERT-F05-02 en curso (CampaignRef `0ce72173-b629-4ca4-bf4c-e7e586792e72`) se cita sólo como REF de lectura opcional; su verificación pertenece al carril CERT.
- **Pendiente:** despachar NORMAL con `specs/FEAT-FORGE-EXPLORER-V0/NORMAL-PROMPT.md`; implementación EX0→EX6; manager review del delta. PHYSICAL CERTIFICATION NOT RUN para todo el Explorer.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `codex/forge-explorer-v0` (creada desde SHA; publicada en origin 2026-09-21) | `745bc8b94e1f6148ddc16c02eb86a755088c2666` (`codex/f05-release-prep` = release `0.2.105`) | [[Echo Forge — Factory V2 Completion]] (viewer como superficie de lectura post-F-05-I) | `specs/FEAT-FORGE-EXPLORER-V0/SPEC.md` v1.0.0 FROZEN @ `cc36c39` | PLANNING FROZEN — docs-only commiteado y pusheado; implementación NORMAL pendiente; físico NOT RUN |

## 🧩 Subproyectos

Sin subproyectos; fases internas = WPs EX0…EX6 abajo.

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> Este board muestra `#owner/agent`. El humano sigue el curro desde [[Echo — Producto Integrado]].

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [ ] EX0 scaffold + seguridad estructural (flags loopback-only, mux GET-only, embed, guards stdlib/allowlist/no-push-output) #owner/agent #type/dev #area/echo
> - [ ] EX1 adaptador sqx-flowkit (exec argv sin shell, stderr `<code>:<kind>:<mensaje>`, verificación de schema, fail-closed, validadores ref/ranking/cursor/limit) #owner/agent #type/dev #area/echo
> - [ ] EX2 HOME (campaign list, paginación next_cursor opaco, apertura por ref exacto) #owner/agent #type/dev #area/echo
> - [ ] EX3 CAMPAIGN (5 estados, target vs observados, waves→RUN, finalists→STRATEGY, bloques stop/failure/cancel) #owner/agent #type/dev #area/echo
> - [ ] EX4 RUN (run get + run stages, ranking por status, promotion, timeline, funnel, formulario ?ranking= en AMBIGUOUS_RESULT) #owner/agent #type/dev #area/echo
> - [ ] EX5 STRATEGY + RELEASE (identidad durable, magic/delivery null rotulados; matriz 17×6 sin inferencia) #owner/agent #type/dev #area/echo
> - [ ] EX6 stub fixtures + README + gates completos + push FF #owner/agent #type/dev #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label] of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"\u2705 Done");render(done);}if(!any){dv.paragraph("_Sin tareas._");}}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## ✅ Completion criteria

Paquete `sqx/cmd/forge-explorer` implementado EX0–EX6 con gates de SPEC §6 verdes (build, tests con fixtures por pantalla y anti-fabricación, vet, gofmt, deps sólo stdlib, regresión sqx-flowkit/forge/releasematrix), navegación completa HOME→CAMPAIGN→RUN/STRATEGY + RELEASE con fixtures, cero cambios fuera de allowed files, push FF, y smoke manual documentado sin certificar nada físico.

## 🛑 Stop conditions

`STOP — MANAGER REVIEW — BASELINE_MOVED`: `origin/codex/f05-release-prep` ≠ `745bc8b…` al arrancar. `STOP — MANAGER REVIEW — FROZEN_CONTRACT_COLLISION`: necesidad de tocar contratos F-05-I, añadir dependencias, auth/CORS, binding no-loopback o escrituras. `release-matrix` que deja de parsear → fail-closed + reporte, sin adaptar parser.

## 📆 Bitácora

- **2026-09-21 — NORMAL ejecutado (ZCode/GLM-5.3-Flash).** EX0 scaffold+seguridad `01ceaa8`; EX1 adaptador fail-closed `ea5159a`; EX2 HOME `29297d1`; EX3 CAMPAIGN `e18558a`; EX4 RUN `b626b14`; EX5 STRATEGY+RELEASE `24b2e3d`; EX6 fixtures+README+hardening `648d5e6` (parseStderr última línea no vacía; ranking_value RawMessage). Smoke real contra production: campaña F05-02 navegable, warnings reales 3× PNL_SIGN_FLIP, matrix 17×6. Un binario accidental fue purgado del historial con filter-branch antes del push (FF cc36c39..648d5e6). F-INT-06 detectado aquí y corregido fuera del visor (SDK `c7f11496b6f6` + symphony `145d6be`).


- **2026-09-21 — TOP planning frozen (sesión TOP, read-only sobre source).** Baseline resuelto contra repos reales: `git fetch` + `rev-parse` confirman `origin/codex/f05-release-prep` == `745bc8b94e1f6148ddc16c02eb86a755088c2666` (release `0.2.105`, CERT-F05-01 PASS según bitácora del padre) y `origin/master` `0b9742b` ancestro (verificado con `merge-base --is-ancestor`). Recon source @ `745bc8b`: sin frontend ni assets web en el repo y cero HTTP server en la ruta inspect (matches previos eran falsos positivos de regex); superficie F-05-I confirmada en source (`sqx/cmd/sqx-flowkit/inspect.go` + `main.go`: 6 comandos read + push-output brownfield excluido, exit codes 0/2/4/10/50, stderr `<code>:<kind>:<mensaje>`, boot PG+etcd con ENV heredado, `release-matrix` cero DI, refs UUID validadas pre-boot por `domain.Parse*Ref`); release matrix vigente con 17 capabilities × 6 dimensiones (veredictos CERT-F04-01/02/03 y CERT-E04-01 ya registrados por `745bc8b`). Decisiones: visor SSR local que exec `sqx-flowkit` (el CLI sigue siendo la única autoridad de composición; el explorador añade cero SQL/DI/drivers), loopback-only, allowlist cerrada de 6 comandos, fail-closed en toda violación de contrato. Entregado: branch `codex/forge-explorer-v0` + worktree `/home/kor/aranea/work/forge-explorer-20260921/symphony`; SPEC.md v1.0.0 FROZEN + PLAN.md (EX0…EX6) + NORMAL-PROMPT.md en `specs/FEAT-FORGE-EXPLORER-V0/`; commit docs-only `cc36c39` (3 archivos, 229 inserciones), push FF verificado (branch nueva en origin). Vault: nota de proyecto materializada (esta nota) + delta en el padre. Sin código, sin certificaciones, sin tocar la campaña CERT-F05-02 en curso. Evidencia: agent-run `2026-09-21-zcode-glm-5.3-flash-forge-explorer-v0-planning`.

## 🧭 Decisiones

- Arquitectura visor = exec de `sqx-flowkit` + HTML server-rendered en loopback; sin JSON API adicional, sin framework JS, sin npm (el JSON versionado F-05-I ya es el contrato; una capa más sería una segunda superficie que reinterpretar).
- `push-output` jamás se expone: el visor es read-only por construcción y por guard (allowlist exacta + ausencia del token en el paquete + GET-only).
- Cursor `next_cursor` opaco end-to-end: el visor valida charset y lo reenvía; jamás decodifica (contrato F05I-PAGINATION-C1 preservado).
- Los estados vacíos son ciudadanos de primera clase: ausencia ≠ cero en todas las pantallas (magic null, delivery null, RUNNING sin finalistas, ranking ausente rotulado).
- Viewer SQX GUI y front de métricas quedan para v1 posterior (backlog del padre); esta SPEC no los cubre.

## 🔗 Docs / Links

- `specs/FEAT-FORGE-EXPLORER-V0/{SPEC.md,PLAN.md,NORMAL-PROMPT.md}` @ `codex/forge-explorer-v0` `cc36c39`
- [[Echo Forge — F-05-I Cohesive release and read surfaces]] · [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]
- `docs/echo-forge/f05-read-surface.md` @ baseline (contrato consumido)
- [[Echo Forge — Factory V2 Completion]] (padre/roadmap) · [[Echo + Echo Forge — Deferred Certification Backlog]] (carril CERT, intocado)

## 💡 Ideas

### Backlog de ideas

- v1: viewer SQX GUI; JSON API opcional que envuelva los mismos read services si aparece un segundo consumidor; deep-links desde campañas CERT hacia el visor.

### Motivos / principios

- projection ≠ authority; membership ≠ rank; ausencia ≠ cero; el visor muestra, nunca calcula.

### Memoria pública / interna

- **Memoria pública:** SPEC/PLAN/NORMAL-PROMPT en el repo.
- **Memoria interna:** ninguna nueva (sin delta operativo más allá del proyecto).
- **Motivo:** el estado y la historia viven en el proyecto y en la SPEC del repo.
