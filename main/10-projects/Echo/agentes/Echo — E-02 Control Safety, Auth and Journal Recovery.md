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
progress: 10
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

- **TOP PLANNING READY FOR MANAGER REVIEW (2026-09-12).** SPEC/PLAN/TASKS/VERIFICATION v1.0.0 de `FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2` @ `ac7b4e14fa971738b4a6cbb88fc8f672bbd57d40` pusheados a `origin/feature/e02-control-safety-journal-recovery` (un commit docs sobre `origin/master` `a99f9a63354bbe72219d1e590bb93757ed08e45e`; master intacto; sin source productivo). NORMAL no arranca hasta manager review.
- **Baseline verificado:** `origin/master` = `a99f9a63354bbe72219d1e590bb93757ed08e45e` (E-04 integrado), igual al esperado al inicio de la sesión. E-04 T21/AC-37 POST-INTEGRATION **no** bloquea E-02; F-04 y E-05 tampoco. E-02 no depende de código nuevo de otro carril.
- **Source revalidado en `a99f9a63`** (no sólo heredado del Reality Check): gateway sin auth en control/webhooks tras CORS `*`; `close-positions` publica CloseCommands físicos sin credencial; admin secret en `front/.env*` + `client.js` + `v3/hasura/config.yaml` (literal); metadata Hasura sólo con rol `admin`; `TradeJournalFn.Invoke` retorna `nil` siempre (fallos de persistencia y conflictos absorbidos); sin cuarentena/DLQ/replay tools; `CommandID` UUIDv7 aleatorio por invocación (replay de fact puede duplicar orden); Flink AT_LEAST_ONCE 60s + restart fixed-delay 5×10s (el retry runtime existe y está sin usar). Detalle: SPEC §3.
- **Autoridades:** Reality Check D-01/D-04 (certificación requerida y alternativas A01-A/A03-A), master §14, evidencia R02/R03/R06/R09. Ningún AUTHORITY_CONFLICT encontrado: el defecto observado en source coincide con el frozen input.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e02-control-safety-journal-recovery` | `a99f9a63354bbe72219d1e590bb93757ed08e45e` (origin/master) | Reality Check D-01/D-04 + master §14 + Live Authority V1 (replay facts ≠ commands) | `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/SPEC.md` v1.0.0 @ `ac7b4e14`; TASKS T01–T15 `[ ]` | TOP planning READY FOR MANAGER REVIEW · No implementing · No CLOSED |

## 🗺️ Arquitectura frozen (resumen; contrato completo en SPEC)

- **Auth:** middleware Gateway por clase (`control_operator`, `service_hasura_webhook`, `forge_ingest` existente, auth hook Hasura) con Bearer opaco constant-time; 401/403/503 fail-closed. Hasura: roles `readonly` (select) y `config_operator` (config writes, sin delete ni identity/journal) vía auth hook `/api/v1/auth/hasura`; admin secret queda server-side y se rota (runbook). Front sin secret en bundle; tokens runtime. Tokens en etcd/env. CORS allowlist complementa, no sustituye.
- **Journal:** taxonomía TRANSIENT (error ⇒ retry Flink existente ⇒ convergencia o fallo visible) / DETERMINISTIC_REJECT (cuarentena durable `echo.journal_quarantine`, migración 062 additive) / DUPLICATE (merge no-op). CLOSE-before-OPEN ⇒ cuarentena + replay PG→PG vía `tools/journalctl` (sin Kafka, sin commands). Síntesis NATIVE (BWC) intacta. Webhooks y trade-facts del bridge a `PublishSync` (`WaitForAll`).
- **Replay:** FACTS = `journalctl replay-facts` (PG→PG, guard estructural sin messaging); COMMANDS = no existe en E-02 (E-08). Fact replay no duplica efecto: `CommandID` fact-triggered pasa a UUIDv5 determinístico sobre `kind|trade_id|accountID`; operator emergency close sigue UUIDv7; EA sin cambios MQL.

## 📦 Work packages (TASKS T01–T15)

- **WP-A Gateway auth** T01–T04: middleware core, CONTROL, WEBHOOK+PublishSync, auth hook Hasura.
- **WP-B Front/secrets** T05–T06: bundle sin admin secret, runtime tokens, CORS allowlist, limpieza repo (`hasura/config.yaml`).
- **WP-C Journal recovery** T07–T10: migración 062, quarantine repo, taxonomía+cuarentena en `TradeJournalFn`, `tools/journalctl`.
- **WP-D Fact replay safety** T11–T12: command identity UUIDv5, bridge trade-facts sync.
- **WP-E Hasura roles** T13: metadata readonly/config_operator (enumeración mecánica del front).
- **WP-F Cert** T14–T15: pack físico (compose StateFun kill/restart, replay doble con spy topic, outage PG real, bundle real, Hasura develop), SOURCE greps, runbook rotación.

## TOP / NORMAL boundaries

- TOP: SPEC/PLAN/TASKS/VERIFICATION, esta nota, linkage padre, gobernanza. Sin source Go/SQL/JS productivo (cumplido: commit docs-only).
- NORMAL: T01–T15 mecánicamente contra SPEC/PLAN. No inventa roles, clases de auth, semántica de cuarentena ni formato de command_id. Stop conditions: PLAN §8 (schema no-additive ⇒ AUTHORITY_CONFLICT; dedupe EA insuficiente ⇒ BWC_GAP; compose indisponible ⇒ PHYSICAL_PARTIAL documentado, jamás mock como PASS).
- GOD: NONE.

## Migrations

**062_journal_quarantine** (única, additive, down migrable; verificar número libre al ejecutar — 061 es la última en master). 060/061 intocables. Ningún cambio al schema de `echo.trade_journal`.

## Certification gates (NORMAL)

Ver VERIFICATION.md. Clases: SOURCE (greps secret/auth/messaging, contracts diff 0), CONTRACT (matriz auth + matriz journal contra PG 17 real), MIGRATION (062 up/down), PHYSICAL (compose StateFun kill/restart, replay doble sin doble efecto con spy topic, outage PG real, `vite build` + bundle grep, HTTP real Gateway, Hasura develop roles/hook). DoD E-02 (roadmap): admin secret fuera del cliente; control fail-closed; outage no pierde facts; retries convergen; conflictos visibles; CLOSE-before-OPEN recuperable; restart no pierde durable; fact replay sin ejecución; BWC preservada; verifier PASS; integración controlada. AC-18 (rotación en prod) es gate ops del owner.

## Branch strategy

- Branch única `feature/e02-control-safety-journal-recovery` desde `a99f9a63` (ya creada, planning `ac7b4e14` pusheado).
- Master push prohibido para NORMAL. Integración controlada posterior (ancestry demostrado, sin force-push).
- Ramas ajenas (E-04/F-04/E-05/E-03) intocables.

## Blockers

Ninguno para planning ni para NORMAL tras manager review. `NOT_OBSERVED` declarado (no bloquea implement, se verifica en VERIFY/owner): etcd/tokens reales de prod, deploy Hasura prod (auth hook env), bundle actualmente servido (evidencia vigente = R03 @ 2026-09-06).

## Closure conditions

T01–T15 `[x]`; AC-01…AC-17 PASS con evidencia física; verifier independiente PASS; integración controlada a master; E-06 desbloqueado. E-02 no se declara CLOSED en planning.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-02; no crea hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [ ] WP-A Gateway auth (T01–T04) #owner/agent #type/dev #area/echo
> - [ ] WP-B Front sin admin secret + limpieza repo (T05–T06) #owner/agent #type/dev #area/echo
> - [ ] WP-C Journal recovery: 062 + quarantine + taxonomía + journalctl (T07–T10) #owner/agent #type/dev #area/echo
> - [ ] WP-D Fact replay safety: command_id determinístico + bridge sync (T11–T12) #owner/agent #type/dev #area/echo
> - [ ] WP-E Hasura roles metadata (T13) #owner/agent #type/dev #area/echo
> - [ ] WP-F Pack físico + SOURCE + runbook rotación (T14–T15) #owner/agent #type/dev #area/echo

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

- **2026-09-12 (TOP one-shot)** — Recovery de estado y planning completo E-02. Baseline confirmado `origin/master` `a99f9a63` (igual al esperado; E-04 integrado encima). Source revalidado físicamente en el baseline: defectos D-04 (CORS `*` sin auth en control/webhooks; secret admin en `.env`/`client.js`/`hasura/config.yaml`; metadata sólo rol `admin`) y D-01 (`Invoke` retorna `nil` siempre; sin cuarentena/replay; CommandID UUIDv7 no replay-stable; Flink restart existe sin usarse). Decisiones frozen en SPEC v1.0.0: A03-A (roles Gateway/Hasura fail-closed, sin BFF) + A01-A (transientes al retry runtime + cuarentena durable) + command_id UUIDv5 determinístico fact-triggered + `journalctl` PG→PG (replay facts ≠ commands) + PublishSync para facts/webhooks. SPEC/PLAN/TASKS/VERIFICATION @ `ac7b4e14` pusheados a la feature; catálogo SPECS.md actualizado; master intacto. Sin implementación; no NORMAL; no CLOSED. Detalle de fricción en feedback de sesión.

## 🧭 Decisiones

- Extender Gateway existente; no BFF ni reverse-proxy auth nuevo (A03-A por etapas).
- Retry owner del journal = restart-strategy Flink existente (retornar error en transientes); nada de colas nuevas.
- Cuarentena durable en tabla nueva 062; conflicto ≠ duplicado; resolución operatoria, no automática.
- CommandID fact-triggered determinístico (UUIDv5); operator close sigue UUIDv7; E-08 lo sustituye por EconomicCommand.
- Replay de facts PG→PG sólo (`journalctl`); replay de commands explícitamente fuera (E-08).
- Rotación del secret expuesto: código + runbook en E-02; ejecución prod = gate del owner (AC-18).

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]]
- [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]]
- [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] (§14)
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- SPEC: `xKoRx/echo` `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/SPEC.md` (PLAN/TASKS/VERIFICATION en la misma carpeta)
- Branch: `feature/e02-control-safety-journal-recovery` @ `ac7b4e14`

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
