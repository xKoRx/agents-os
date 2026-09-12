---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
sprint:
start: 2026-09-12
due:
progress: 70
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-02
  - Control safety E2
  - E-02 E2
  - FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-12"
updated: "2026-09-12"
cssclasses:
  - wide
---

# Echo — E-02 Control Safety, Auth and Journal Recovery

%% Naming: Echo — E-02 Control Safety, Auth and Journal Recovery es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-02 Control Safety, Auth and Journal Recovery
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-02 (H1 del Reality Check: D-01 journal ack/recovery + D-04 control exposure). El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES. Debe DONE antes de que E-06 confíe captura canónica.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí con la tarea puente. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Cerrar los dos P0 actuales con evidencia física: (A) control autenticado fail-closed con el admin secret fuera del cliente/repo y roles mínimos en el Gateway/Hasura existentes; (B) journal donde hechos aceptados no se pierden silenciosamente, retries convergen, conflictos quedan en cuarentena durable y replay de FACTS nunca re-envía órdenes al broker. KISS: extender Gateway y Flink/PG existentes (A01-A + A03-A); sin control-plane genérico.

## 📊 Estado actual

- **IMPLEMENTATION READY FOR MANAGER SOURCE REVIEW — FOCUSED CORRECTION (2026-09-12).** Commit final `f7ddea18` en `origin/feature/e02-control-safety-journal-recovery`, master intacto. Hasura auth hook corregido a JSON de session variables; `AuthConfig` rechaza tokens duplicados entre READ/CONFIG/CONTROL/webhook con 503 fail-closed; 17 paths históricos autorizados fueron limpiados sin imprimir valores. Gateway `-race`, front tests/build/bundle scan, SOURCE y regresión E-04 relevantes PASS; PG/Kafka/Flink/Hasura físico `PHYSICAL_PARTIAL`. No verifier, no E-02 CLOSED.
- **Baseline verificado:** `origin/master` = `a99f9a63354bbe72219d1e590bb93757ed08e45e` (E-04 integrado), igual al esperado al inicio de la sesión. E-04 T21/AC-37 POST-INTEGRATION **no** bloquea E-02; F-04 y E-05 tampoco. E-02 no depende de código nuevo de otro carril.
- **Source revalidado en `a99f9a63`** (no sólo heredado del Reality Check): gateway sin auth en control/webhooks tras CORS `*`; `close-positions` publica CloseCommands físicos sin credencial; admin secret en `v3/front/.env*` + `client.js` + `v3/hasura/config.yaml` (literal); metadata Hasura sólo con rol `admin`; `TradeJournalFn.Invoke` retorna `nil` siempre (fallos de persistencia y conflictos absorbidos); sin cuarentena/DLQ/replay tools; Flink AT_LEAST_ONCE 60s + restart fixed-delay 5×10s (el retry runtime existe y está sin usar). Fan-out Kafka: journal **independiente** del planner/close_handler (consumer groups distintos; `TradeJournalFn` sink). `CommandID` UUIDv7 observado en fábricas de dominio llamadas por MM/close_handler: **no es defecto D-01 de E-02**. Detalle: SPEC §3.
- **Autoridades:** Reality Check D-01/D-04 (certificación requerida y alternativas A01-A/A03-A), master §14, evidencia R02/R03/R06/R09. Ningún AUTHORITY_CONFLICT encontrado: el defecto observado en source coincide con el frozen input.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e02-control-safety-journal-recovery` | `a99f9a63354bbe72219d1e590bb93757ed08e45e` (origin/master) | Reality Check D-01/D-04 + master §14 + Live Authority V1 (replay facts ≠ commands) | `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/SPEC.md` v1.0.2 @ `f7ddea18`; TASKS T01–T10, T12–T15 with focused source-review correction evidence and physical partials; T11 `[-]` E-08 | IMPLEMENTATION READY FOR MANAGER SOURCE REVIEW · no verifier · no CLOSED |

## 🗺️ Arquitectura frozen (resumen; contrato completo en SPEC)

- **Auth (KISS, sin OAuth/IAM, sin LAN-as-auth, sin admin secret en cliente):** cuatro Bearers opacos distintos, patrón E-04, fail-closed 401/403/503. **usuario READ** (`front_read` → Hasura `readonly`): el humano pega el token; `sessionStorage`; SELECT-only. **operador CONFIG** (`config_operator`): token distinto; SELECT + writes de config; nunca CONTROL/webhook. **operador CONTROL** (`control_operator`): token distinto; solo Gateway close/republish; nunca auth hook Hasura. **servicio Hasura webhook** (`service_hasura_webhook`): header del event trigger, solo server-side. Prohibido servir `front_read` (ni ningún Bearer) vía runtime config/nginx/VITE: eso no es autenticación. CORS/LAN complementan, no sustituyen. Admin secret server-side + runbook de rotación.
- **Journal:** taxonomía TRANSIENT (error ⇒ retry Flink del **ingress journal** ⇒ convergencia o fallo visible) / DETERMINISTIC_REJECT (cuarentena durable `echo.journal_quarantine`, migración `v3/sdk/postgres/migrations/062_*` additive) / DUPLICATE (merge no-op). CLOSE-before-OPEN ⇒ cuarentena + replay PG→PG vía `v3/tools/journalctl` (sin Kafka, sin commands). Síntesis NATIVE (BWC) intacta. Webhooks y trade-facts del bridge a `PublishSync` (`WaitForAll`).
- **Replay:** FACTS = `journalctl replay-facts` (PG→PG, guard sin `github.com/xKoRx/echo/v3/sdk/messaging`); COMMANDS = no existe en E-02 (E-08). Fan-out Kafka físico: journal y planner/close_handler son consumer groups independientes; `TradeJournalFn` es sink (0 `ctx.Send`). Retry/replay de journal **no** re-planifica. `CommandID` UUIDv7 intacto; UUIDv5 diferido a E-08. Planner/MM/MQL intocables.

## 📦 Work packages (TASKS T01–T15)

- **WP-A Gateway auth** T01–T04: middleware core, CONTROL, WEBHOOK+PublishSync, auth hook Hasura (READ/CONFIG presentados; CONTROL/webhook 403 en el hook).
- **WP-B Front/secrets** T05–T06: bundle sin admin secret ni tokens; `session_tokens.js` (prompt + sessionStorage por actor); CORS allowlist; limpieza `v3/hasura/config.yaml`.
- **WP-C Journal recovery** T07–T10: migración 062, quarantine repo, taxonomía+cuarentena en `TradeJournalFn`, `v3/tools/journalctl`.
- **WP-D Bridge fact durability** T12: trade-facts `PublishSync`. T11 `[-]` CommandID → E-08.
- **WP-E Hasura roles** T13: metadata readonly/config_operator (enumeración mecánica de `v3/front/src/services/graphql/*.js`).
- **WP-F Cert** T14–T15: pack físico (compose StateFun kill/restart **journal**, 0 publishes a `echo.commands.*` desde journalctl/retry, outage PG real, bundle real, Hasura develop con token presentado), SOURCE greps, runbook rotación.

## TOP / NORMAL boundaries

- TOP: SPEC/PLAN/TASKS/VERIFICATION, esta nota, linkage padre y gobernanza; la focused correction conserva el diseño E-02 y no agrega scope de producto.
- NORMAL: T01–T10 y T12–T15 mecánicamente contra SPEC/PLAN v1.0.2. T11 permanece `[-]`. No inventa actores, clases de auth ni semántica de cuarentena. No reabre CommandID. Stop conditions: PLAN §8 (schema no-additive ⇒ AUTHORITY_CONFLICT; reabrir CommandID/planner/MM ⇒ SCOPE_CONFLICT; compose indisponible ⇒ PHYSICAL_PARTIAL documentado, jamás mock como PASS).
- GOD: NONE.

## Migrations

**062_journal_quarantine** (única, additive, down migrable; verificar número libre al ejecutar — 061 es la última en master). 060/061 intocables. Ningún cambio al schema de `echo.trade_journal`.

## Certification gates (NORMAL)

Ver VERIFICATION.md. Clases: SOURCE (greps secret/auth/messaging, contracts + domain CommandID diff 0), CONTRACT (matriz auth **por actor** + matriz journal contra PG 17 real), MIGRATION (062 up/down), PHYSICAL (compose StateFun kill/restart journal, 0 commands desde journalctl/retry, outage PG real, `vite build` + bundle grep, HTTP real Gateway, Hasura develop roles/hook con token presentado). DoD E-02 (roadmap): admin secret fuera del cliente; control fail-closed; outage no pierde facts; retries convergen; conflictos visibles; CLOSE-before-OPEN recuperable; restart no pierde durable journal; fact replay sin ejecución; BWC preservada; verifier PASS; integración controlada. AC-18 (rotación en prod) es gate ops del owner.

## Branch strategy

- Branch única `feature/e02-control-safety-journal-recovery` desde `a99f9a63` (planning v1.0.0 `ac7b4e14`; TOP correction v1.0.1 `151e0bc5`; focused source-review correction v1.0.2 `f7ddea18` pusheada).
- Master push prohibido para NORMAL. Integración controlada posterior (ancestry demostrado, sin force-push).
- Ramas ajenas (E-04/F-04/E-05/E-03) intocables.

## Blockers

`PHYSICAL_PARTIAL`: no hay psql, Kafka, compose Flink/StateFun ni sesión Hasura develop en esta ejecución. `NOT_OBSERVED`: etcd/tokens reales de prod, deploy Hasura prod, bundle servido y rotación AC-18.

## Closure conditions

T01–T10 y T12–T15 `[x]`; T11 `[-]` (E-08); AC-01…AC-17 PASS con evidencia física; verifier independiente PASS; integración controlada a master; E-06 desbloqueado. E-02 no se declara CLOSED en planning.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-02; no crea hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [x] WP-A Gateway auth (T01–T04) #owner/agent #type/dev #area/echo
> - [x] WP-B Front sin admin secret + tokens presentados + limpieza repo (T05–T06) #owner/agent #type/dev #area/echo
> - [x] WP-C Journal recovery: 062 + quarantine + taxonomía + journalctl (T07–T10) #owner/agent #type/dev #area/echo
> - [x] WP-D Bridge trade-facts PublishSync (T12); T11 CommandID diferido E-08 #owner/agent #type/dev #area/echo
> - [x] WP-E Hasura roles metadata (T13) #owner/agent #type/dev #area/echo
> - [r] WP-F Pack físico + SOURCE + runbook rotación (T14–T15) #owner/agent #type/dev #area/echo

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

## 📆 Bitácora

- **2026-09-12 (focused source-review correction)** — Sobre HEAD inicial `df99084b`, se corrigió el contrato Hasura a JSON de session variables y se añadió validación explícita de unicidad entre tokens READ/CONFIG/CONTROL/webhook con 503 fail-closed. Se registraron primero y limpiaron después los 17 paths históricos autorizados. Gateway `-race`, front tests/build/bundle scan, SOURCE, tooling compile y regresión E-04 relevantes PASS; PHYSICAL sigue parcial. Commit final `f7ddea18`, push sólo a feature; master intacto. Puente permanece Review.

- **2026-09-12 (TOP correction)** — SPEC/PLAN/TASKS/VERIFICATION v1.0.1 @ `151e0bc5`. Auth: READ/CONFIG/CONTROL/webhook son credenciales distintas; el humano presenta tokens (prompt/sessionStorage); webhook solo server-side; prohibido runtime-config de Bearers. CommandID: traza física fact→Kafka fan-out paralelo (journal sink vs planner/close_handler); journal/retry no duplica efecto económico ⇒ UUIDv5 **fuera** (E-08); T11 `[-]`; planner/MM/MQL intocables. Paths: Allowed Files exactos `v3/...` (no existe `sdk/` raíz). Sin source productivo. Puente sigue Review.
- **2026-09-12 (TOP one-shot)** — Recovery de estado y planning completo E-02. Baseline confirmado `origin/master` `a99f9a63` (igual al esperado; E-04 integrado encima). Source revalidado físicamente en el baseline: defectos D-04 (CORS `*` sin auth en control/webhooks; secret admin en `.env`/`client.js`/`hasura/config.yaml`; metadata sólo rol `admin`) y D-01 (`Invoke` retorna `nil` siempre; sin cuarentena/replay; Flink restart existe sin usarse). Decisiones frozen en SPEC v1.0.0 (superseded en auth-discovery y CommandID por v1.0.1). SPEC/PLAN/TASKS/VERIFICATION @ `ac7b4e14` pusheados a la feature; catálogo SPECS.md actualizado; master intacto. Sin implementación; no NORMAL; no CLOSED.
- **2026-09-12 (NORMAL implementation)** — Implementados auth por actor + Hasura hook + CORS allowlist, front sin admin secret, metadata mínima, quarantine 062/repository/journalctl, taxonomía retry/quarantine y facts bridge/webhooks con `PublishSync`. Cinco commits funcionales más cierre de evidencia; HEAD `df99084b` pusheado sólo a feature. Unit/contract y `-race` pasan; build/scan front pasan; physical gates quedan parciales por servicios no disponibles. Recomendación: manager source review y luego repetir pack físico antes de verifier.

## 🧭 Decisiones

- Extender Gateway existente; no BFF ni reverse-proxy auth nuevo (A03-A por etapas).
- Auth humana = Bearer **presentado** por actor (READ ≠ CONFIG ≠ CONTROL); webhook = servicio Hasura server-side. No admin secret en cliente. No OAuth/IAM. No LAN-as-auth. No Bearer compartido auto-descubrible.
- Retry owner del journal = restart-strategy Flink del **ingress journal** (retornar error en transientes); nada de colas nuevas.
- Cuarentena durable en tabla nueva 062; conflicto ≠ duplicado; resolución operatoria, no automática.
- CommandID fact-triggered UUIDv5 **no** entra en E-02: el journal no re-planifica (fan-out paralelo). E-08 EconomicCommand/outbox.
- Replay de facts PG→PG sólo (`v3/tools/journalctl`); replay de commands explícitamente fuera (E-08).
- Rotación del secret expuesto: código + runbook en E-02; ejecución prod = gate del owner (AC-18).

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]]
- [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]]
- [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] (§14)
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- SPEC: `xKoRx/echo` `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/SPEC.md` (PLAN/TASKS/VERIFICATION en la misma carpeta)
- Branch: `feature/e02-control-safety-journal-recovery` @ `f7ddea18` (v1.0.2 focused source-review correction; parent histórico `ac7b4e14`)

## 💡 Ideas

### Backlog de ideas

- Watcher de cuarentena con alerta accionable: E-13 ops, no aquí.
- Kafka rewind/offset tooling para replay completo de topics: E-08.

### Motivos / principios

- Una fuente por hecho: SPEC = contrato; esta nota = ejecución; TASKS = checklist.
- Journal mínimo confiable ≠ ledger institucional; fail closed y visible > sofisticado y silencioso.

### Memoria pública / interna

- **Memoria pública:** autoridades enlazadas.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** no duplicar D-01/D-04 ni rediseñar decisiones frozen.
