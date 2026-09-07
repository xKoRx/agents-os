---
type: project
schema_version: 1
owner: me
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo - Discovery y Estado]]"
sprint:
start: 2026-08-21
due:
progress: 0
repo: xKoRx/echo (~/go/src/github.com/xKoRx/echo)
jira:
prs:
aliases:
  - echo lab clean cierre
  - echo journal cleanup
  - cierre del lab
tags:
  - project/echo
  - kind/project
  - area/echo
created: 2026-08-21
updated: 2026-08-24
cssclasses:
  - wide
---

# Echo - Cierre del Lab y Limpieza del Journal

%% Naming: Echo - Cierre del Lab y Limpieza del Journal es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo - Cierre del Lab y Limpieza del Journal
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> **Repo:** `xKoRx/echo` (`~/go/src/github.com/xKoRx/echo`) · **Inicio:** 2026-08-21
> Proyecto de **ejecución** (delivery): terminar la limpieza de `trade_journal` y cerrar Lab Clean según lo planificado (RFC-009). Nace del discovery consolidado en [[Echo - Discovery y Estado]]; el estado validado completo y la evidencia viven en [[Echo - Reporte de Estado Lab y Journal 2026-08-21]].

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Echo - Cierre del Lab y Limpieza del Journal]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Terminar **Lab Clean** tal como estaba planificado (RFC-009 rev.8): llevar el gate oficial `lab_clean_readiness_check.sql` a **GO** documentado y completar la **Etapa 10 (legacy removal)** que quedó parcial.
- Sanear `trade_journal` según el contrato final: eliminar la columna prohibida `origin` (reintroducida por la migración 056) consolidando la clasificación en `source_type`, sin perder la funcionalidad de Daily Ops que hoy la lee.
- Restaurar la calidad de datos del path NATIVE: EAs actuales en terminales (opens completos), investigación del timestamp sintético y visibilidad DQ de los trades sin R.
- Alcance explícito: **sin features nuevas** — solo cierre de lo planificado, limpieza, gate y robustez documentada. Todo cambio de producto (p.ej. Daily Ops con cuentas no-ACTIVE) pasa primero por decisión del owner.

## 📊 Estado actual

- **Punto de partida (validado contra prod y repo el 2026-08-21, read-only):** gate oficial corrige a `summary|1|1|NO_GO` — único blocker: columna `origin` presente (prohibida por el contrato, reintroducida por 056 para que `mv_daily_operations` la exponga); único warn: `policy_row_coverage_pct = 0%` (las 351 policies viven en `strategy_id` tipo `magic_*` que no calzan con ningún trade REFERENCE CLOSED). El script del gate está roto tal cual commiteado: **4 CTEs tipados** (líneas 13/57/194/389) son sintaxis inválida en PostgreSQL; requiere parche local para correr.
- **Pipeline Lab operativo:** worker cada 5 min (64.897 job runs, últimas runs hoy SUCCEEDED), `lab_canonical_trades` 2611, outcomes 2287 (100% REFERENCE vía source_type ECHO), curvas 4529, snapshots 9284 frescos. Etapas 1-9 de RFC-009 construidas y corriendo; **Etapa 10 parcial** (052 dropeó parte del legacy; quedan `lab_out_*` vivas, front dual-stack y tablas RFC-003 dormantes).
- **Salud de datos:** journal 2664 filas (2287 REFERENCE CLOSED + 306 EXECUTION CLOSED + 51 FAILED + 2 OPEN + 18 NATIVE CLOSED); 63 CLOSED sin `r_multiple` (45 ECHO + 18 NATIVE con `risk_pips` NULL); drift event↔recorded ~3.1 h (reloj broker); `mv_daily_operations` en 0 filas es **comportamiento esperado de ventana** (reset HWM diario 22:00–23:00 UTC + filtro ACTIVE que oculta ~82% de la actividad de hoy en cuentas INACTIVE).
- **Detalle completo con evidencia y semáforos:** [[Echo - Reporte de Estado Lab y Journal 2026-08-21]].

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

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> **Fase 0 — Decisiones de diseño (bloquean el resto)**
> - [ ] **D1 · Decisión `origin` vs `source_type`**: eliminar `origin` del journal (recomendado; es el contrato rev.8 y el único blocker del gate) o legitimarlo actualizando el gate. Eliminar implica tocar: migración nueva (rewrite de `mv_daily_operations` con `source_type` + DROP columna), `sdk/postgres/trade_journal_open.go` (insertOpenRowTx/updateOpenRowTx), `trade_journal_repository.go` (SaveClose), campo `Origin` del dominio, telemetría core y queries GraphQL del front. `comment` (también de 056) NO está prohibida por el gate — decidir si se queda como fact legítimo #owner/me #type/research #area/echo
> - [ ] **D2 · Decisión síntesis NATIVE** (`synthesizeNativeOpenFromClose`, `e25165ba`): mantenerla como red de seguridad hasta que los EAs actuales estén en todos los terminales (debería volverse inerte), con revisión posterior para retirarla, o acotar su alcance ya #owner/me #type/research #area/echo
> - [ ] **D3 · Decisión producto Daily Ops**: (1) el "0 filas" del 20/21-08 quedó explicado: la matview muestra "operaciones desde el último reset diario HWM" y el `daily_hwm_reset_at` rueda 22:00–23:00 UTC, después del último close (viernes 17:59 UTC) — vaciamiento vespertino esperado, no fallo; decidir si esa semántica de ventana es la deseada para el tab. (2) El filtro `status='ACTIVE'` oculta 102 de los 124 trades de hoy (~82%, en cuentas INACTIVE; universo real 48 cuentas: 17 ACTIVE / 20 ARCHIVED / 11 INACTIVE — el "~2186 INACTIVE" del discovery era falso); decidir si Daily Ops muestra cuentas no-ACTIVE o si se corrige el estado de las cuentas activas en trading #owner/me #type/research #area/echo
> - [ ] **D4 · Decisión stash 2026-05-20**: 52 archivos, ~98% junk de node_modules + 7 de código real (gateways v2/v3, README clients, **047 ya aplicada** — pop riesgoso, LabClean UI). Extraer los 7 a rama de evaluación y dropear el resto, o descartar todo #owner/me #type/dev #area/echo
>
> **Fase 1 — Cerrar el gate (GO)** — depende de D1
> - [ ] **G1 · Commitear fix del script del gate**: corregir los 4 CTEs tipados de `v3/sdk/postgres/scripts/lab_clean_readiness_check.sql` (líneas 13, 57, 194, 389 — quitar la anotación de tipo de la lista de columnas). Es un fix de sintaxis puro, independiente de D1 #owner/me #type/dev #area/echo
> - [ ] **G2 · Migración de salida de `origin`** (si D1 = eliminar): nueva migración que reescriba `mv_daily_operations` usando `source_type`, dropee la columna y actualice sdk/core/front; con tests de repositorio y verificación de Daily Ops post-deploy #owner/me #type/dev #area/echo #blocked
> - [ ] **G3 · Investigar `policy_row_coverage_pct = 0%`**: 351 policies (25 cuentas, 136 `strategy_id` tipo `magic_*`) sin ningún match con los pares (account, strategy) de los 2287 trades REFERENCE CLOSED. Determinar si es dato stalkeado de provisioning, ids que no corresponden o diseño a cambiar; resolver o reclasificar el warn con criterio #owner/me #type/research #area/echo
> - [ ] **G4 · Re-correr el gate y documentar GO**: ejecutar el script corregido contra prod tras G2/G3 y registrar el veredicto en `v3/docs/lab/00-trade-journal-readiness.md` (hoy dice BLOCKED de mayo) #owner/me #type/dev #area/echo
>
> **Fase 2 — Completar Etapa 10 (legacy removal)**
> - [ ] **E1 · Inventario final pre-borrado**: completar el reconstruction report pendiente (§49-59 del handoff) con lo que falte del reporte del 21-08: flows runtime por path (Reference/Execution/Native: quién aporta cada fact) y writer/reader de cada tabla lab_* #owner/me #type/research #area/echo
> - [ ] **E2 · Archivar/eliminar RFC-003 dormante**: `raw_trade_imports` y `canonical_trades` (8437 filas, congeladas desde 05-04), `raw_trade_events` (0), `execution_trade_pairs` (0), `analytics_job_runs` (13) + funciones `job_backfill_*`/`job_build_*` de 029. Verificado: cero writers Go vivos. Backup antes de DROP #owner/me #type/dev #area/echo
> - [ ] **E3 · Archivar `stage0_audit.sql` + docs Stage 0**: audita el spec vNext/042 muerto y ya no corre limpio contra post-043; mover a archivo histórico y dejar el readiness check como único gate #owner/me #type/admin #area/echo
> - [ ] **E4 · Unificar el front del Lab**: conviven `strategyLensProvider`+`journal.js` (legacy: `mv_strategy_overview` **dropeada por 052** → queries rotas; `fn_strategy_kpis` y familia siguen vivas) y `strategyLabCleanProvider`+`strategyLabClean.js` (clean). Migrar lo que siga útil (account selector usa `getExecutionAccountsRanking` de journal.js), decidir destino del tab legacy y remover el stack muerto #owner/me #type/dev #area/echo
> - [ ] **E5 · Cerrar destino de `lab_out_*` restantes**: 052 dropeó solo 4 de las ~17; las demás siguen en prod sin consumidor identificado en el stack clean. Confirmar lectores (incluida metadata Hasura live) y dropear o declarar legacy-active #owner/me #type/dev #area/echo
>
> **Fase 3 — Calidad de datos del path NATIVE**
> - [ ] **N1 · Redeployar EAs actuales en terminales MT4/MT5**: los terminales corren builds pre-`0abdf720` (05-07) y los opens nativos llegan incompletos (por eso existe la síntesis). Confirmar primero qué EA emite el open nativo (`execution_agent_v3` según el discovery vs `reference_v3` según la inspección de repo del 21-08 — evidencia mixta), compilar con MetaEditor e instalar en cada terminal; verificar primera NATIVE con `risk_pips` y duración reales #owner/me #type/dev #area/echo
> - [ ] **N2 · Investigar `opened_at_ms` sintético del path NATIVE**: las 18 NATIVE tienen duraciones ≈3h exactas (10798–10800 s) y drift event>recorded; decidir corrección en EA/bridge/core #owner/me #type/research #area/echo
> - [ ] **N3 · Backfill opcional del hueco NATIVE 1-jun→20-08**: reconstruible parcialmente desde logs de core (profit_gross/commission/close_price); evaluar valor vs esfuerzo #owner/me #type/research #area/echo
> - [ ] **N4 · Visibilidad DQ de los 63 CLOSED sin R** (45 ECHO/REFERENCE + 18 NATIVE sin `risk_pips`): el modelo canónico no tiene flags; exponerlos vía DQ del Lab (RFC-009: `missing_initial_risk_count`, `excluded_trades_pct`) para que no sean invisibles #owner/me #type/dev #area/echo
>
> **Fase 4 — Contrato y robustez**
> - [ ] **C1 · Test real de repositorio del UPSERT**: OPEN incompleto → OPEN completo mismo trade → 1 fila con valores llenos → CLOSE → facts sellados intactos (pendiente del review de mayo) #owner/me #type/dev #area/echo
> - [ ] **C2 · Retry/DLQ para execution** (pendiente del review de mayo) #owner/me #type/dev #area/echo
> - [ ] **C3 · Poner los RFCs en línea con la realidad**: RFC-009 sigue "Propuesta rev.8" y RFC-010 "Draft" pese a estar mayormente implementados (043/045/046/047/052/056-060); promocionar estados y **ratificar la extensión no-planeada del contrato**: status `FAILED` + `error_code`/`error_message` (migración 060) y las columnas 056 (`origin`/`comment`) — hoy el contrato escrito y el schema real divergen en esos puntos #owner/me #type/admin #area/echo
>
> **Fase 5 — Seguridad y ops (transversal)**
> - [ ] **S1 · Rotar el password único reutilizado** (ssh con sudo / Postgres / Hasura) y sacar el secret de Hasura del `.env` público del front #owner/me #type/dev #area/echo
> - [ ] **S2 · Alinear metadata Hasura**: la del repo no trackea `mv_daily_operations` ni `v_trade_stream` (drift con la instancia live); trackear o documentar por qué no #owner/me #type/dev #area/echo
> - [ ] **S3 · Docs de raíz desactualizadas**: Makefile raíz y `ESTRUCTURA_PROYECTO.md` describen v1; el pipeline real es `build_v3.sh` + `deploy-prod.sh`. Además: `deploy-prod.sh` no deploya el bridge (manual no trazable) — documentar runbook #owner/me #type/admin #area/echo

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

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-08-23** — Segunda revisión adversarial completada: auditoría exhaustiva POC/identidad sobre echo+symphony con 116 hallazgos registrados (magic 888111 compartido por wave, canonical_strategy_id sensible a $HOST_KEY, overwrite MinIO sin run-segment, autoprovision de catálogo, NATIVE/GOLD, drift RFCs↔código). Impacto directo acá: G3 se reinterpreta (el gate mide mal el join de coverage), `comment` es columna muerta (cae junto a origin), y el roadmap suma F0 (registro de MagicNumber en Forge) antes del Golden Path. Detalle completo: [[Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23]].
- **2026-08-21** — Proyecto creado por pedido del owner ("arma un proyecto con tareas para el roadmap de limpieza"). Base: discovery consolidado + doble validación read-only del día (repo y prod, subagentes) integrada en [[Echo - Reporte de Estado Lab y Journal 2026-08-21]]. Hallazgos que moldearon el roadmap: gate `summary|1|1|NO_GO` (blocker `origin` de 056 + warn policies 0%), script del gate con 4 CTEs tipados rotos, 51 filas FAILED (migración 060 no registrada en el vault), universo de cuentas corregido a 48, y causa del vacío de Daily Ops cerrada (ventana HWM + filtro ACTIVE).

## 🧭 Decisiones

- **2026-08-21** — Scope del proyecto: **solo cierre de lo planificado** (gate GO, Etapa 10, calidad de datos nativos, robustez, seguridad). Sin features nuevas; todo cambio de producto pasa por decisión explícita del owner (D1-D4).
- **2026-08-21** — Este proyecto es de **ejecución** y vive separado del discovery ([[Echo - Discovery y Estado]]), según la regla de no mezclar comprensión con cambio. Las tareas de ejecución que estaban en el discovery quedan consolidadas acá como fuente única.

## 🔗 Docs / Links

- [[Echo - Reporte de Estado Lab y Journal 2026-08-21]] — reporte completo validado (para evaluar con otra IA)
- [[Echo - Discovery y Estado]] — discovery del ecosistema (norte, historia, contrato final)
- [[Echo]] (área) · [[echo-core]] (aplicación) · Repo: `xKoRx/echo` → `~/go/src/github.com/xKoRx/echo`
- Gate oficial: `v3/sdk/postgres/scripts/lab_clean_readiness_check.sql` · doc de veredicto: `v3/docs/lab/00-trade-journal-readiness.md`
- RFCs: `v3/docs/rfcs/RFC-009-analytics-v3-strategy-lab-v3-clean.md` (rev.8) · `v3/docs/rfcs/RFC-010-trade-journal-open-close-ea-persistence.md`

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- 

### Motivos / principios

- 

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** 
- **Memoria interna:** 
- **Motivo:** 
