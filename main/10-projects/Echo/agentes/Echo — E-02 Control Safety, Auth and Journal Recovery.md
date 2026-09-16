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
updated: "2026-09-15"
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
| xKoRx/echo | `feature/e02-control-safety-journal-recovery` | `a99f9a63354bbe72219d1e590bb93757ed08e45e` (origin/master) | Reality Check D-01/D-04 + master §14 + Live Authority V1 (replay facts ≠ commands) | `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/SPEC.md` v1.0.2 @ `f7ddea18`; T01–T10, T12–T15 ejecutados (T11 `[-]` E-08); AC-01…AC-17 PASS con evidencia física; verifier independiente PASS | **E02 CLOSED (software)** — pendiente: CONTROLLED INTEGRATION a master (gate de closure) · AC-18 rotación prod = gate ops owner |

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

Ninguno para DONE de software. Pendientes de closure formal: (1) CONTROLLED INTEGRATION a `master` (ancestry demostrado, sin force-push); (2) AC-18 rotación en prod = gate ops del owner (no cierra software; sin él no se habilita capital). `echo.journal_quarantine` en PROD PG (152) se crea con el deploy del branch (PLAN §3).

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

- **2026-09-16 (sesión 2) — `E02 CLOSED`: AC-11 + AC-12 + AC-01 + verifier independiente PASS.** Runtime topology owner FROZEN: **Daedalus `192.168.31.161` = runtime DEV de Echo/Echo Forge; `.75` = infra soporte (Hasura/Flink), JAMÁS runtime Echo; `.211` = antiguo ubuntu-dev, retirado; DNS canónico `dev.echo.core.lab.aranea → .161` (Pi-hole owner). Regla durable: *Application runtime follows declared topology; infrastructure proximity is never authority to colocate product components.*** Ejecución: `echo-core` @ `f7ddea18` compilado en Daedalus (sha256 `00240dd1d37384d2…`) y servido en `:9090` vía DNS canónico (sin extra_hosts, sin tocar `urlPathTemplate`); Flink StateFun `.75` → core Daedalus → PG `.220/echo-develop`. **AC-12 PASS (kill -9 Core Go, compose StateFun develop + PG real):** Window A (kill -9 post-persistencia: redelivery ⇒ 1 fila/1 id, sin doble fila); Window B (kill -9 pre-persistencia del close: close publicado con core DOWN ~30s, job Flink restart ×2, redelivery ⇒ close aplicado EXACTAMENTE 1 vez, fila CLOSED `2405.75`, cero pérdida); replay de OPEN late → clasificado `OPEN_AFTER_CLOSED` → cuarentena durable (1 fila, unique index funciona) → ACK → loop converge; 0 publishes a `echo.commands.*`. **AC-11 PASS (outage real PG 17.6):** ACCESS EXCLUSIVE lock sobre `echo.trade_journal` (sesión fixture, ~100s) ⇒ INSERTs bloquean ⇒ `canceling statement due to … timeout` ⇒ handler clasifica **TRANSIENT** (5× `persistence_error`, error retornado a StateFun, **0 quarantine, 0 fila parcial**); liberado el lock ⇒ redelivery ⇒ exactamente 1 fila/1 id, sin duplicado. **AC-01 PASS (bundle):** `vite build` real (43 assets, dist agregado sha16 `2747ba2985042409`) + `check-frontend-bundle.sh` PASS + 4 greps independientes (header/var/Bearer/hex-48) limpios + **doble-check con valor REAL del admin secret DEV** (sha16 `8a36217243c11629`, valor jamás impreso, stdin-only mcps→Daedalus). **Verifier independiente PASS (V1–V5, superficie separada, read-only):** identidad source/binario, evidencia PG, bundle, drift; encontró y corrigió 2 residuales (topics fixture `e02cert-gate2{,b}-20260915` borrados; SQL del verifier corregido). **KEEP:** migración 062 `journal_quarantine` aplicada a `.220/echo-develop` como `echo_user` (additive, idempotente, down-migrable; rollback = down migration, ahora vacía). **REMOVE ejecutado:** filas fixture journal/quarantine (0 residuo), core fixture detenido, bearers locales shredded. Nota: `echo.journal_quarantine` NO existe aún en PROD PG (152) — se crea con el deploy del branch (PLAN §3). E-02 desbloquea E-06; AC-18 (rotación secret prod) sigue como gate ops del owner para uso con capital. Evidencia durable: [[Echo — Access & Physical Capability Matrix]] · change_log 2026-09-16-e02-closed.
- **2026-09-16 — E-02 PHYSICAL CERTIFICATION ejecutada (3/3 gates PASS, con clasificación contractual de mutaciones):** Gates físicos contra capabilities certificadas del Access Plane, ejecución vía helper SDK consumer único (`e02-hermes-mcp.py`, bearer por stdin). **Gate 1 Hasura DEV roles/hook PASS 13/13 probes:** runtime DEV arrancaba sin auth hook ni roles (0 permissions, 0 `"role"` en metadata exportada — defecto D-04 aún vivo en runtime); metadata contractual del branch `f7ddea18` (`e02_front_tables.yaml` + 6 archivos, 151 grants) aplicada vía `apply_metadata` (44 permisos `admin` legacy inconsistentes excluidos — Hasura no los permite, admin es implícito); probes: anon/wrong/no-auth → denied fail-closed; READ → SELECT 46 tablas, 0 mutaciones (schema-level "no mutations exist"); CONFIG → SELECT+INSERT/UPDATE sólo en 8 tablas de config, sin delete, journal/identity/promotion inaccesibles; CONTROL/webhook en Hasura → hook 403 fail-closed; hook responde JSON `{"X-Hasura-Role":...}` sin header (AC-04/AC-05 físicos). Auth hook del Gateway demostrado con fixture E-02 @ `f7ddea18` compilado y corrido en Daedalus (READ→200 readonly JSON, CONFIG→200 config_operator, CONTROL/webhook→403, inválido→401, close-positions READ→403). **Clasificación owner (KEEP/REMOVE):** roles+metadata = KEEP contractual (AC-05, estado durable; re-aplicados post-rollback erróneo); `HASURA_GRAPHQL_AUTH_HOOK` = activation step del deploy Gateway (PLAN §3 step 4) — REMOVE hasta entonces, fixture eliminado con rollback byte-identical verificado; fixtures REMOVE: fila `e02cert-*` borrada (DELETE 1), gateway/toolchain/tokens/scripts Daedalus eliminados. **Gate 2 Kafka PublishSync/redelivery PASS:** fixture `e02cert-gate2-*` (topic 1p/RF3 en DEV .44): produce con key `e02-trade-001` + headers dict + payload envelope → consume round-trip con key/headers/payload preservados (header roundtrip explícito `check-header-roundtrip` PASS) → re-consume = mismo registro offset 0 (redelivery visible, sin duplicado lógico) → delete → describe 0 particiones (post-condición). PublishSync (`WaitForAll`) es path de código ya en CONTRACT (T03/T12); el gate físico demuestra el transporte Kafka DEV con semántica idempotente. **Gate 3 Flink restart/recovery PASS:** baseline job `StatefulFunctions` `6bfc59ad` RUNNING, 1524 checkpoints completados, `restored=0`, sin excepciones → `docker restart statefun-worker` (control mínimo, 1 container, .75) → job RUNNING de nuevo, checkpoints `restored=1` / total 1532 (recovery desde checkpoint = evidencia de estado), 0 failed → Kafka post-recovery: groups `echo-statefun-*` sanos, `echo.core-commands.v1` intacto (0 publishes anómalos desde retry). Restart-strategy fixed-delay 3×5s operativa. **T14/T15 parcialmente ejecutados; NO se declara E-02 CLOSED:** falta outage PG real (AC-11), compose kill -9 del binario core (AC-12 completo con core real — este gate usó restart del worker, no kill -9 del proceso Go), bundle/build front (AC-01) y verifier independiente. Blockers históricos resueltos: superficies Hasura/Kafka/Flink DEV operativas. **Deuda operacional P1 del MCP Access Plane registrada (2º caso):** tras churn de sesiones, los proxies nginx-wrapped (hasura/kafka/flink/ssh) entran en modo async-202 sin sid visible que bloquea clientes stateless; recovery = `docker restart` del backend proxy (workaround certificado, no solución durable); pools de sesión/leak = causa raíz a diagnosticar. Evidencia: bitácora de sesión + [[ACCESS-CERTIFICATION]] + [[Echo — Access & Physical Capability Matrix]].
- **2026-09-15b — Access Plane delta (GAP-ECHO-004 CLOSED, sin gates ejecutados):** owner seed instalado en `.71` y viewer `echo-runtime-prod` certificado end-to-end: Gateway RUNNING (`echo-gateway` PID 713), Core RUNNING (`echo-core` PID 110701), `echo-functions` RUNNING, Bridge NOT_DEPLOYED (evidencia, no se levanta); listeners 80/9080/9090/8080/8090; negative `run-command` POLICY_DENIED. La verificación física Gateway de E-02 pasa de BLOCKED-pending a observación SSH directa PASS; control verbs siguen fuera de scope (PROD). `E02_PHYSICAL_CERTIFICATION_BLOCKED` se mantiene por gates propios. Evidencia: [[ACCESS-CERTIFICATION]] § GAP-ECHO-004 CLOSED · [[Echo — Access & Physical Capability Matrix]].
- **2026-09-15 — Access Plane delta (sin gates ejecutados):** reconciliación de gaps stale — Hasura DEV/PROD, Kafka DEV, Flink DEV y observabilidad PROD ya tienen capabilities MCP certificadas y operativas ([[ACCESS-CERTIFICATION]]); el bloqueo "no hay tool" de 2026-09-14 ya no aplica: las verificaciones físicas pendientes de E-02 pueden ejecutarse contra esas superficies. Target Gateway resuelto: `.211` muerto, runtime vivo = PROD `192.168.31.71` (`prod.echo.gateway.lab.aranea`, `/health` 200) observable vía `aranea-observability-ro` (logs/metrics en vivo); SSH viewer `echo-runtime-prod` staged pendiente de única owner action. `E02_PHYSICAL_CERTIFICATION_BLOCKED` se mantiene. Evidencia: [[Echo — Access & Physical Capability Matrix]].
- **2026-09-14 — Access certification delta:** PG17.11 disposable 062 up/down/up `READY`; ARGUS Prometheus/Jaeger/Loki READ `PASS`. Hasura DEV roles/hook, Kafka PublishSync/redelivery, Flink restart/recovery y Gateway físico `BLOCKED` por falta de superficies/tools/target probados; E-02 permanece `PHYSICAL_PARTIAL` y no se reabre para cierre. Evidencia durable: [[Echo — Access & Physical Capability Matrix]]. Sin physical gate E-02 ejecutado.
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

- [[Echo — Access & Physical Capability Matrix]]
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
