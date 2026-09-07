---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-08-12
due:
progress: 55
repo:
jira:
prs:
aliases:
  - Scopes RIO
  - Estándar de scopes Signals
  - Naming de scopes RIO
tags:
  - kind/project
  - area/meli
  - project/scopes-rio
created: 2026-08-12
updated: 2026-09-03
cssclasses:
  - wide
---

# Estandarización de Scopes RIO

%% Naming: Estandarización de Scopes RIO es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Estandarización de Scopes RIO
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Plataforma:** [[RIO]]
> **Alcance:** (1) listar toda la infra/scopes de RIO, curarla y proponer limpieza + redefinición; (2) backend RIO: [[rio-playmaker]], control planes, [[rio-materializer]] y [[rio-sdk-events]]; (3) **ampliado 2026-08-19:** frontends RIO ([[rio-frontend]], [[ads-signals-frontend]]) y la capability de **selección independiente de scope front vs back en runtime** (MeliLab + queryParam).

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Estandarización de Scopes RIO]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- **Listar, curar y redefinir la infra de scopes de todo RIO.** Enumerar todos los scopes en Fury, curar el inventario (lifecycle/health, segmento, bindings), y proponer una limpieza (retiros) + una **redefinición y estándar** de scopes.
- Diseñar y acordar una **nomenclatura canónica y un estándar operativo de scopes para el backend de [[RIO]]**, de modo que la identidad compuesta `application/scope` exprese lane, rol y workload sin ambigüedad, mientras un manifiesto separado declare canales, segmentos, contratos y compatibilidad entre aplicaciones.
- Partir de una **fuente de verdad verificable del estado actual**: qué scopes existen en Fury, su segmento runtime, lifecycle/health y qué bindings tipados los referencian.
- Convertir el resultado en una propuesta implementable: contrato de naming, reglas de compatibilidad entre Playmaker y control planes, validaciones automáticas, estrategia de migración, ownership y documentación operativa.
- **Capability nueva (2026-08-19):** habilitar **selección independiente del scope de frontend y de backend en runtime** (MeliLab + queryParam), ej. `frontend=alpha` con `backend=beta`, sin acoplarlos a deploy-time. Diseño completo en la sección [🔀 Selección independiente de scope front/back](#🔀-selección-independiente-de-scope-frontback-diseño-objetivo).
- **Resultado esperado:** RIO dispone del catálogo acotado de ambientes lógicos `production`, `staging`, `alpha`, `beta` y `gamma`, pero cada equipo habilita sólo los ambientes y roles que necesita. Los scopes de frontend se llaman únicamente como el ambiente; el backend usa `<environment>-<rol>-<segment>`. Una operación conserva el mismo ambiente de backend a lo largo de todo el flujo.

## 📊 Estado actual

- **Fuente reproducible:** `~/fuentes/rio-inspector/scope_inventory.py` consulta el service graph read-only de Fury, `fury scopes status -j`, `fury describe-infra`, Config Orchestrator y los checkouts registrados; genera `rio-scopes.json`, [[scope-inventory]] y el HTML publicado desde el mismo corte.
- **Auditoría Fury 2026-09-03:** **91 scopes** en 9 aplicaciones con infraestructura: 87 `Active`, 4 `Inactive`; 47 con al menos una instancia `running` y 44 sin instancias observadas. [[rio-sdk-events]] sigue como librería sin runtime Fury.
- **Evidencia operativa:** 51 scopes tienen una route, un binding activo o instancias `running`; 15 no presentan evidencia activa y 25 no son concluyentes. Estas categorías no miden tráfico y nunca autorizan un retiro sin validación del equipo.
- **Reconciliación:** 1 consumer BigQueue pausado de [[rio-controlplane-fury]] quedó sin runtime resoluble en el service graph; se conserva explícitamente como hallazgo y no se asigna por inferencia.
- **SPEC funcional vigente:** [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) define un catálogo acotado de ambientes (`production`, `staging`, `alpha`, `beta`, `gamma`), no una cantidad fija de scopes. Cada equipo adopta sólo los ambientes y roles que necesita; frontend usa `<environment>` y backend usa `<environment>-<rol>-<segment>`.
- **Grid publicado:** el doc Grid `01KZXKPH3YAGGX89P04GTY7B7E` separa la foto Fury del contrato funcional y no agrega instrucciones, targets, routing, filtros, segmentación ni pilotos que no estén definidos por SIG-599. El HTML narrativo quedó integrado al generador.
- **Próxima fase:** la implementación física, el aprovisionamiento, el routing y la migración corresponden a una futura SPEC técnica.

## 🔀 Discovery técnico histórico — fuera de SIG-599

> Evidencia levantada el 2026-08-19 para una futura SPEC técnica. No forma parte del contrato funcional vigente ni se publica en el Grid.

### Selección (dos ejes independientes)
- **Dos query params, se llaman literalmente `frontend` y `backend`** (no otros nombres). Ej: `?frontend=alpha&backend=beta`.
- El **front lee y PERSISTE** ambos query params (obligatorio: un queryParam solo no sobrevive navegación SPA ni se pega a los XHR; persistir en cookie/estado de sesión).
- **MeliLab = cookie.** El front la **lee en código**. Resolución por eje, con override: `scope_eje = queryParam[eje] ?? cookieMeliLab[eje] ?? prod`. Ej: con MeliLab en `gamma` pero `?frontend=alpha&backend=beta`, corre alpha/beta (el queryParam pisa MeliLab, por eje).

### Direccionamiento por capa
- **Front → nginx.** El nginx del front resuelve qué scope/build de front sirve.
- **Back (Playmaker) → Fury routes por HEADER.** El scope **lo manda el request**: el front traduce el `backend` resuelto a un **header de scope** en cada request a Playmaker (el scope NO va en el dominio; se descartó `rio-playmaker-<scope>.melisystems.com` porque obliga a mantener hosts por scope). Las **Fury routes** matchean ese header y rutean al runtime de Playmaker del scope.
- **CP (control planes) → un tópico compartido + filtro por scope.** Playmaker (publisher) adjunta un **tag `scope:<x>`** al mensaje (mecanismo `WithFilters`/`BigQueueFilters` = lista de tags arbitrarios, confirmado en VIS). El **consumer definido en Fury** aplica el filtro por ese tag; el endpoint de la app puede además re-filtrar (defensa en profundidad, como hace VIS en `pkg/middlewares/filter.go`).

### El fork y su resolución
- **Fork:** (A) **filtro por scope en tópico compartido** (favorita) vs (B) **tópico por scope**.
- **Resuelto: (A) filtro.** Confirmado viable con evidencia: los filtros BigQueue son tags de valor arbitrarios (`scope:alpha`), no sólo nombres de campos. La corrección anula el reporte previo que decía "no hay filtro por valor".
- **Matiz de seguridad (opción, no imposición):** si el filtro resultara app-side (el broker entrega todo y el consumer descarta), un consumer no-prod recibiría físicamente mensajes de prod. Blindaje barato: **prod en su propio tópico** y **`alpha/beta/gamma` compartiendo un tópico no-prod + filtro por `scope`**. Calza con "DB solo test+prod" y con el eje `segment` (nonsite=prod, nonprod=test). Si Fury filtra server-side de verdad, no hace falta.

### Estado actual real (lo que hay que cambiar)
- **Front (Nordic 9.12, ambos):** back scope acoplado por `baseURL` de `config/<scope>-<env>.js` (`playmaker_base_url`); sin header de scope; único header custom `X-Tiger-Token`; cliente `nordic/restclient` (`api/lib/playmaker.ts`), sin interceptor central único (cada `call()` arma sus `opts` con `buildContext(req)`); cero MeliLab, cero queryParam de ambiente.
- **Playmaker (Spring Boot, Java 17):** sin ingreso de header de scope; scope propio por env `SCOPE` (`util/ScopeUtils.java`); topics estáticos por profile YAML; sin `environment_scope` en payload; sin validación de coherencia.
- **CP hoy NO se suscriben a BigQueue:** Playmaker les hace **push HTTP** a endpoints REST (`@PostMapping /triggers/deployments`, `/deployments`, `/actions`) y el CP **filtra client-side por `componentType`** (`rio-controlplane-kafka/.../DeploymentTriggerController.java:97-101`, `rio-controlplane-flink/.../DeploymentTriggerController.java:96-99`). El payload (`DeploymentTriggerMessage`/`ActionTriggerMessage`) trae `environmentId`/`environmentName`, **no** scope.
- **SDK (`rio-sdk-events`, librería Java 21):** `BigQueueClient` es publish-only; `BigQueueFilters` = `List<String>` (record, wire `modified_fields`); sin campo scope en el envelope.

### Requisitos duros que agrega esta capability
1. **Front:** leer+persistir `frontend`/`backend`; leer cookie MeliLab; traducir `backend` a header de scope en cada request a Playmaker (introducir el interceptor/override, hoy no existe).
2. **Playmaker:** leer/validar el header de scope en el ingreso; estampar `scope:<x>` como tag en cada publish (y opcionalmente `environment_scope` en el body para auditoría/validación consumer-side); ruteo por Fury routes según header.
3. **CP:** filtrar por el tag `scope:<x>` (server-side en la definición Fury del consumer; y/o extender el filtro client-side `componentType` para incluir scope).
4. **DB:** `test` y `prod` sin cambios. El scope es routing/cómputo, **no frontera de datos**.

### Seguridad (guardrails no negociables)
- **El scope (header a Playmaker y tag en el mensaje) lo estampa SIEMPRE server-side el trusted-ingress**, nunca desde datos del cliente. Si viniera del cliente, se podría spoofear el scope de otro CP (CWE-639 / CWE-862).
- **Validar el queryParam contra un enum allowlist** de scopes válidos (`@meli/input-validation`, `iv.enumeration()`); nunca armar host/routing/tag desde el valor crudo (CWE-918 / CWE-99).
- **Fail-closed:** en prod para usuario real/anónimo → ignorar selectores y forzar `prod`. Override a no-prod sólo para **identidad interna** (gating MeliLab + identidad no manipulable, `@platsec-security/*`).
- **DB no-prod compartida (test):** `alpha/beta/gamma` comparten la DB `test` → **no hay aislamiento de datos entre scopes no-prod**; el filtro de scope es routing, no frontera de datos. Dejarlo escrito.
- No PII en el queryParam (CWE-598). Reusar el header de scope estándar, no inventar variantes por capa.

### Verificaciones de plataforma pendientes (no confirmables desde el código local)
1. **Fury BigQueue:** ¿el filtro por tag se aplica **server-side** en la definición del consumer (entrega sólo lo matcheado) o es app-side? Decide si hace falta separar el tópico de prod. *(La definición Fury del consumer NO está versionada en los repos.)*
2. **Fury routes:** nombre/estructura del header estándar de scope que matchean para rutear Playmaker, y cómo se declara la route por scope.
3. **MeliLab:** nombre/estructura real de la cookie y cómo la leen los fronts (confirmar en algún front que ya la use). *(El RAG interno `ask_knowledge` no respondió esta sesión — timeout.)*
4. **nginx front:** dónde vive la config del direccionamiento de scope de front (nginx propio vs Fury frontend routing).

## 🚀 Propuesta ejecutiva

- **Propuesta:** estandarizar el nombre base como `<environment>-<role>`, dejar que Fury agregue `-<segment>` y usar `rio-controlplane-kms/test` como primer slice: `alpha-api` → `alpha-api-nonprod`. Si el flujo obligatorio sólo acepta `test-nonprod`, tratarlo como bridge transitorio, no como target state.
- **Qué ganamos:** cumplimiento antes del 2026-09-09, salida verificable de `legacy`, nombres predecibles, selección independiente de front/back, menor blast radius y una plantilla reusable para migrar el resto de RIO con canary y rollback.
- **Qué implica:** confirmar con Fury el nombre aceptado y la señal de cumplimiento; desacoplar ambiente/configuración del último token de `SCOPE`; crear el scope segmentado y sus routes; desplegar, probar y mover tráfico gradualmente; mantener el legacy como rollback; luego replicar el patrón con manifiesto, validadores y guardrails.

### Hallazgo de implementación — KMS

`rio-controlplane-kms` calcula `SCOPE_SUFFIX` con el último token de `SCOPE` y activa ese Spring profile. Como Fury agrega siempre `nonprod/nonsite`, tanto `test-nonprod` como `alpha-api-nonprod` intentarían cargar `application-nonprod.yml`, que no existe, en vez del profile lógico. La migración debe reemplazar esa heurística por un mapping explícito `scope materializado → environment_scope → profile/config`, sin usar el segmento físico como ambiente.

### Repos y evidencia (para el handoff)
- Fronts: [[rio-frontend]] (`config/*.js`, `api/lib/playmaker.ts`), [[ads-signals-frontend]] (`config/*.js` incl. `beta-production.js`, `api/lib/playmaker.ts`, `api/lib/rioEntityService.ts`).
- Backend: [[rio-playmaker]] (`util/ScopeUtils.java`, `controller/SignalsController.java:91`, `events/DataProductChangedPublisher.java`, `restclient/impl/BigQueueDataProductChangedProducerImpl.java`, `application-*.yml`), [[rio-sdk-events]] (`bigqueue/BigQueueClient.java`, `bigqueue/BigQueueFilters.java`, `deployment/DeploymentTriggerMessage.java`, `actions/ActionTriggerMessage.java`).
- CP consumers: `rio-controlplane-kafka` y `rio-controlplane-flink` (`controller/DeploymentTriggerController.java`, `ActionTriggerController.java`, `application*.yml`, `config/ClusterRegistry.java`).
- Patrón de filtros BigQueue de referencia: `~/fuentes/vis/vis-items-loader-tagging` (`pkg/services/item_to_publish.go:25`, `pkg/process/vehicle_risk_profile_unified/create.go:191`, `pkg/middlewares/filter.go:25-83`, `docs/guide/processes/re_ranged_attributes_calculation.md:80-116`) + SDK `fury_go-toolkit-bigqueue` (`pkg/bigq/options.go:19-36`, `pkg/bigq/jit.go:97-100`).

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
> - [x] **[Inventario 1]** Enumerar todos los scopes actuales por aplicación reconciliando `fury list-infra` con `fury scopes status -j`, incluyendo tipo, estado, ambiente, versión, criticidad y salud disponible #owner/me #type/research #area/meli ✅ 2026-08-12
> - [x] **[Inventario 2]** Trazar cómo cada repo interpreta `SCOPE` y qué perfil/configuración carga #owner/me #type/research #area/meli ✅ 2026-08-12
> - [-] **[Inventario 3 histórico]** Clasificación genérica de uso descartada por no ser funcional; reemplazada por bindings tipados y estado Fury en [[scope-inventory]] #owner/me #type/research #area/meli
> - [x] **[Inventario 4]** Identificar qué scopes de Playmaker producen/consumen qué canales y qué scope de cada CP los atiende; matriz de routing en [[scope-compatibility-matrix]] (40 consumers BigQueue, canal→segmento→scope; no implica compatibilidad semántica) #owner/me #type/research #area/meli ✅ 2026-08-12
> - [x] **[Reproducibilidad del grid]** Fuente normalizada + generador versionable en `~/fuentes/rio-inspector`; JSON, Markdown y HTML salen del mismo corte con gates de reconciliación #owner/me #type/dev #area/meli ✅ 2026-08-12
> - [x] **[Inventario 5 — routes + config]** Registrar Fury routes Web y resolver por scope profile Spring, archivo dedicado local y artifact Fury sin confundir ausencia de artifact con ausencia de configuración #owner/me #type/research #area/meli ✅ 2026-08-12
> - [x] **[Reporte por aplicación]** Reemplazar conteos opacos por listas de scopes con bindings pausados/ausentes, routes y contraste de config Fury, separando hechos de propuesta #owner/me #type/dev #area/meli ✅ 2026-08-12
> - [x] **[Fury Config real]** Contrastar por scope versión desplegada vs latest `APPROVED` de Config Orchestrator; separar por completo esta evidencia de profiles/archivos del checkout #owner/me #type/research #area/meli ✅ 2026-08-12
> - [x] **[Target state por aplicación]** Registrar en base separada scopes objetivo, origen, grupo/rol/workload, segmento y decisiones pendientes; exponer switch actual/propuesta en cada card #owner/me #type/dev #area/meli ✅ 2026-08-12
> - [x] **[Diff visual de migración]** Derivar desde las bases el listado retirar/mantener/agregar, ordenar retiros primero y luego prod/stage/alpha/beta/gamma, con validación amarilla exclusiva para Streams #owner/me #type/dev #area/meli ✅ 2026-08-12
> - [x] **[Diseño de routing de ambientes]** Auditar Playmaker, rio-sdk-events, mqclient y Fury consumer filters; definir header de ingreso + `environment_scope` + tópico/filtro #owner/me #type/research #area/meli ✅ 2026-08-12
> - [x] **[Spec funcional]** Reestructurar [[scope-naming-standard]] como Functional Specification con contrato de datos, user stories, acceptance criteria, E2E, riesgos y rollout #owner/me #type/dev #area/meli ✅ 2026-08-12
> - [x] **[Front/back — verificación de estado]** Confirmar en repos el acople actual (front por `baseURL` de config; Playmaker sin header-routing, solo env `SCOPE` + profiles + topics estáticos; CP por push HTTP + filtro `componentType`) con evidencia file:line #owner/me #type/research #area/meli ✅ 2026-08-19
> - [x] **[Front/back — verificación de filtros BigQueue]** Confirmar en `~/fuentes/vis/vis-items-loader-tagging` que los filtros son tags de valor arbitrarios (`scope:x` viable); corrige reporte previo #owner/me #type/research #area/meli ✅ 2026-08-19
> - [x] **[Grid — reestructura narrativa]** Reordenar el grid como reporte de estado + propuesta doble, con presentación, guía de lectura y decisiones abiertas consolidadas; publicado como v2 del doc Grid #owner/me #type/dev #area/meli ✅ 2026-08-25
> - [r] **[Discovery agente — integraciones y persistencia]** [[Scopes RIO - Discovery de Integraciones y Persistencia]] discovery documentado; revisar matriz, gaps y seams de refactor #owner/me #type/supervision #area/meli
> - [x] **[Grid — reconciliar y publicar]** Revalidar las 10 aplicaciones con Fury CLI, alinear la propuesta sólo con SIG-599, integrar la vista narrativa al generador y publicar el doc Grid #owner/me #type/dev #area/meli ✅ 2026-09-03
> - [ ] **[Grid — compartir con el equipo]** Presentar el Grid a Signals #owner/me #type/admin #area/meli
> - [ ] **[Alineación]** Validar inventario, propósito y ownership con el equipo Signals; resolver scopes huérfanos y excepciones #owner/me #type/research #area/meli
> - [/] **[Naming]** Validar con el equipo el contrato funcional de [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599): scopes de frontend iguales al ambiente y backend limitado a `api`/`consumer`; la materialización Fury y el manifiesto de compatibilidad se definen en el SPEC técnico #owner/me #type/dev #area/meli #blocked
> - [ ] **[Piloto KMS — segmentación obligatoria]** Confirmar si Fury acepta `alpha-api-nonprod` como remediación de `test` o exige el bridge `test-nonprod`; ejecutar scope+routes, canary, verificación de tráfico y rollback antes del deadline #owner/me #type/dev #area/meli #urgent 📅 2026-09-09
> - [ ] **[Piloto KMS — configuración]** Reemplazar `ScopeUtils` last-token por un mapping explícito de ambiente lógico/profile compatible con el sufijo `nonprod/nonsite` agregado por Fury #owner/me #type/dev #area/meli #blocked
> - [ ] **[Segmentación/Legacy]** Inventariar recursos live y sus `segment-id` efectivos antes de planificar migración; confirmar con Fury el mecanismo de aislamiento dentro de `nonprod` #owner/me #type/dev #area/meli #waiting
> - [ ] **[Manifest de bindings]** Definir y completar por runtime `application/scope`, lane, role, workload, channel, direction, infra-segment, contract/schema, versión y site/tenant #owner/me #type/dev #area/meli #waiting
> - [ ] **[Estándar]** Definir contrato de configuración: perfiles, segmentos, recursos compartidos/dedicados, secretos, canales, criticidad y ownership #owner/me #type/dev #area/meli #waiting
> - [ ] **[Automatización]** Diseñar validadores de CI/runtime que impidan scopes incompatibles, perfiles ausentes y rutas cross-segment accidentales #owner/me #type/dev #area/meli #waiting
> - [ ] **[Implementar routing de ambientes]** Versionar contratos SDK, propagar `environment_scope`/tag `scope:<x>`, crear el ingreso de header en Playmaker y el filtro por scope en consumers, ejecutar con compatibilidad/rollback #owner/me #type/dev #area/meli #waiting
> - [ ] **[Front/back — validar tópicos y filtros]** Confirmar con Fury el contrato de los tópicos `nonsite`/`nonprod` y que el filtro `scope:<environment>` de `nonprod` se aplica antes de entregar cada mensaje #owner/me #type/dev #area/meli #waiting
> - [ ] **[Front/back — verificar plataforma]** Header estándar de Fury routes; cookie MeliLab (nombre/estructura y lectura en front); config de scope de front en nginx #owner/me #type/research #area/meli #waiting
> - [ ] **[Front/back — guardrails de seguridad]** Allowlist enum (`@meli/input-validation`), authz de override (identidad no manipulable), fail-closed a prod, scope estampado server-side, DB compartida = routing no datos #owner/me #type/dev #area/meli #waiting
> - [x] **[Front/back — spec funcional]** Publicar y simplificar [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599): ambientes canónicos, selección independiente, frontend con scope simple, backend `api`/`consumer` y continuidad end-to-end; queda en `draft` para revisión del equipo #owner/me #type/dev #area/meli ✅ 2026-09-01
> - [ ] **[Migración]** Preparar plan incremental de renombre/adopción con compatibilidad, rollback y retiro de scopes obsoletos #owner/me #type/dev #area/meli #waiting
> - [ ] **[Implementación]** Ejecutar los cambios aprobados y extender el estándar al resto del backend RIO #owner/me #type/dev #area/meli #waiting

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

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-08-12** — Proyecto creado como tercera iniciativa raíz de Signals. Baseline desde código + service graph Fury; iteraciones de inventario, reporte por app, Fury Config real, target state segmentado, diff visual y diseño de routing. Fuente reproducible en `~/fuentes/rio-inspector`. [[scope-naming-standard]] pasó a spec funcional; naming `#blocked` hasta ratificación del equipo. Baseline consolidado: 88 scopes, 40 consumers BigQueue, target `prod/stage/alpha`.
- **2026-08-19 (extensión a frontend + selección independiente de scope)** — Rodrigo pide como aporte poder elegir scope de front y back por separado (ej. `frontend=alpha`, `backend=beta`) vía MeliLab + queryParam. Se amplió el alcance del proyecto a frontends y a la capability runtime, y a "listar+curar+limpiar+redefinir" toda la infra. Verificación en repos: (1) header-routing sólo diseñado, no implementado en Playmaker; (2) fronts Nordic acoplan el back scope por `baseURL` de config; (3) CP no se suscriben a BigQueue, reciben push HTTP + filtro `componentType`. **Corrección clave:** los filtros BigQueue son tags de valor arbitrarios (evidencia en `vis-items-loader-tagging`), así que "un tópico + filtro `scope:<x>`" (la favorita) es viable. Diseño final acordado: MeliLab+queryParam (`frontend`/`backend`, queryParam pisa cookie por eje), front→nginx, back→Fury routes por header, CP→tópico+filtro por tag, DB test+prod sin cambios. Pendiente: cerrar fork server-side/app-side con Fury, header de routes, cookie MeliLab, nginx front, y spec funcional.
- **2026-08-19 (persistencia)** — Note reconstruido desde el snapshot de inicio de sesión porque el disco había **regresado** a una versión vieja (progress 25 / 87 scopes) por conflicto de Obsidian Sync. Confirmar convergencia del sync. Handoff completo dejado en este note (sección [🔀 Selección independiente de scope front/back](#🔀-selección-independiente-de-scope-frontback-diseño-objetivo)) para el segundo agente que llevará la propuesta al grid.
- **2026-08-19 (piloto de segmentación KMS)** — Notificación Fury exige segmentar `rio-controlplane-kms/test` antes del 2026-09-09. Se adopta como forcing function del estándar: RIO define `alpha-api`, Fury materializa `alpha-api-nonprod`; `test-nonprod` queda como bridge sólo si la remediación lo exige. Hallazgo: `ScopeUtils` usa el último token del scope como profile y debe desacoplarse del segmento agregado por Fury.
- **2026-08-25 (reestructura del grid para el equipo)** — El grid estaba desordenado: mezclaba KPIs, modelo, situación actual, routing propuesto y detalle sin declarar nunca qué era hecho y qué era propuesta. Se reordenó para separar el reporte de estado de la propuesta.
- **2026-08-25 (discovery agente front/Playmaker/control planes)** — Se cerró [[Scopes RIO - Discovery de Integraciones y Persistencia]] con cortes HEAD, matriz de integraciones, semántica as-is, persistencia/transporte, gaps de plataforma y seams para el refactor. Hallazgo central: no existe carrier transversal; front usa baseURL, Playmaker usa `SCOPE` runtime y los eventos usan ambiente/tipo de componente sin scope. La tarea puente queda en Review para revisar la propuesta y cerrar evidencia de nginx/MeliLab/Fury.
- **2026-08-31 (spec funcional de ambientes)** — Publicada [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) en `draft`. Define MeliLab como ambiente base de frontend/backend, overrides independientes `frontend`/`backend`, default `prod`, dos puntos de entrada de Playmaker, tópicos `nonsite`/`nonprod` con filtro `scope:<environment>`, nomenclatura `<environment>-<role>[-<qualifier>]-<segment>`, un scope por tipo obligatorio en testing y scopes productivos según necesidad. El alta de una lane de testing no requiere código ni configuración por ambiente en nginx, dominios o tópicos.
- **2026-09-01 (simplificación funcional de SIG-599)** — El SPEC se reescribió alrededor de una sola idea: conservar la identidad del ambiente durante todo el flujo. Los nombres canónicos pasan a `production`, `staging`, `alpha`, `beta` y `gamma`; frontend usa únicamente el ambiente y backend usa `<environment>-<rol>-<segment>`. Headers, tópicos y filtros quedan fuera del funcional y se resolverán en el SPEC técnico. El Grid no cambió.
- **2026-09-03 (Grid publicado)** — Auditoría read-only con Fury CLI 5.21.0 sobre las 10 aplicaciones: 91 scopes en 9 apps con runtime y [[rio-sdk-events]] como librería. Se integró la vista narrativa al generador, se eliminó el target físico anterior y se publicó el Grid alineado sólo con SIG-599.
- **2026-09-03 (corrección editorial del Grid)** — Se eliminó la instrucción no respaldada que pedía confirmaciones a cada equipo, se retiró la rotulación pública de versiones y se corrigió el enlace canónico de SIG-599.
- **2026-09-03 (corrección de naming backend)** — Se corrigió el contrato y el Grid: el formato backend es `<environment>-<rol>-<segment>`.
- **2026-09-03 (SIG-599 alineado)** — Se actualizó el SPEC funcional en Spellbook para definir backend con `<environment>-<rol>-<segment>`; `api`, `consumer`, `sink` y `tp` quedan como ejemplos de rol y no como un catálogo limitado a dos tipos.
- **2026-09-03 (render de placeholders)** — Spellbook interpretaba los placeholders con `<…>` como tags HTML y mostraba sólo `--`; las cuatro apariciones del patrón backend quedaron escapadas para renderizar `<environment>-<rol>-<segment>` completo.

## 🧭 Decisiones

- **Ownership y jerarquía:** proyecto humano raíz (`owner: me`, `root: true`) bajo [[Meli]], tercero del dominio Signals. No es subproyecto de onboarding ni de [[Crear Context]].
- **Separación de fases:** el inventario as-is se completa antes de diseñar naming o implementar cambios. La propuesta y la adopción pertenecen a este mismo objetivo, pero quedan gated por evidencia.
- **Definición operativa vigente:** un scope existe si el service graph Fury lo lista; lifecycle, health, segmento y binding se registran como dimensiones independientes.
- **Dimensiones separadas:** el estándar debe distinguir al menos lane/celda, aplicación, rol/workload, ambiente lógico, segmento Fury, canal y contrato/schema.
- **Ambiente lógico vs segmento:** `environment_scope` (`production/staging/alpha/beta/gamma`) decide routing funcional; `metadata.segment` (`legacy/nonprod/nonsite`) describe placement Fury. Ejes independientes.
- **Fuentes:** Fury es autoridad del inventario desplegado; los repos son autoridad de interpretación y comportamiento; el vault conserva el conocimiento durable y las decisiones.
- **Selección front/back:** MeliLab define el ambiente base de ambos ejes; `frontend` y `backend` lo sobrescriben de forma independiente; cada eje sin selección usa `production`. El front lee y persiste la selección.
- **Entrada Web extensible:** nginx sirve el frontend efectivo con una regla genérica y el front deja de seleccionar Playmaker mediante archivos/baseURL por scope. Playmaker mantiene sólo dos puntos de entrada: productivo para `prod` y testing para los ambientes `nonprod`.
- **BigQueue por segmento + filtro:** cada canal mantiene un tópico `nonsite` para `prod` y uno `nonprod` compartido por los ambientes de testing; los mensajes y consumers `nonprod` se asocian mediante `scope:<environment>`.
- **Cantidad y nombres funcionales:** frontend se nombra con `<environment>` y backend con `<environment>-<rol>-<segment>`.
- **Extensibilidad:** agregar una lane de testing consiste en aprovisionar scopes y bindings; no agrega código, reglas nginx por ambiente, subdominios de Playmaker ni tópicos BigQueue.
- **DB sin cambios:** sólo `test` y `prod`; el scope es routing/cómputo, no frontera de datos.
- **Scope estampado server-side:** el header/tag de scope lo fija el trusted-ingress, nunca el cliente.
- **Nombre canónico:** SIG-599 define frontend `<environment>` y backend `<environment>-<rol>-<segment>`.
- **Piloto KMS:** usar la obligación de segmentar `test` como primer slice vertical, con target `alpha-api-nonprod` y bridge `test-nonprod` sólo si Fury lo impone para marcar cumplimiento.

### Preguntas abiertas para el equipo / verificaciones
1. ¿Qué decisiones de negocio y ownership se requieren para proponer retiros sin convertir bindings en una categoría genérica?
2. ¿La unidad de alineación es una lane/celda completa de RIO y qué contrato/schema debe compartir?
3. ¿Qué scopes especiales sobreviven como roles explícitos y cuáles son deuda transitoria?
4. ¿Qué ventana y fallback para mensajes legacy sin `environment_scope` mientras se adopta `prod/stage/alpha`?
5. ¿Qué recursos pueden compartirse entre familias y cuáles deben aislarse por construcción?
6. ¿Qué capability soportada por Fury implementará el aislamiento de lanes dentro de `nonprod`?
7. ¿Dónde se versionará el manifiesto de bindings y el generador reproducible?
8. ¿Qué aplicación será el piloto de migración y quién aprueba cada retiro y cada Stream amarillo?
9. **Front/back:** ¿el filtro por tag BigQueue se aplica server-side antes de la entrega? ¿Qué contrato de Fury routes permite que el punto de entrada de testing seleccione el scope? ¿Nombre/estructura de la cookie MeliLab y cómo la leen los fronts? ¿Qué capacidad de nginx permite una regla genérica sin configuración por ambiente?
10. **Piloto KMS:** ¿la remediación de `test` acepta el target renombrado `alpha-api-nonprod` o exige crear `test-nonprod`? ¿Qué señal del dashboard confirma que la restricción de deploy quedó levantada?

## 🔗 Docs / Links

- Inventario canónico del proyecto: [[scope-inventory]]
- Matriz de routing scope-level (Inventario 4): [[scope-compatibility-matrix]]
- Modelo de segmentación Fury: [[fury-segmentation-model]]
- Propuesta de nomenclatura (borrador): [[scope-naming-standard]]
- Spec funcional de ambientes y scopes: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) · estado `draft`
- Grid visual (generado): `30-resources/grids/rio-scope-inventory.html` · índice [[00-index|grids]]
- Grid publicado para el equipo (reproducible): [RIO · scopes y ambientes](https://grid.adminml.com/d/01KZXKPH3YAGGX89P04GTY7B7E/view) · doc Grid `01KZXKPH3YAGGX89P04GTY7B7E`
- Deuda del grid resuelta: [[2026-08-25-rio-scope-grid-restructure-lives-outside-the-generator]]
- Cambio y continuidad del Grid: [[2026-09-03-rio-scope-grid-v3-reconciliation]]
- Plataforma y aplicaciones: [[RIO]] · [[30-resources/applications/00-index|applications]]
- Flujos e integraciones: [[system-map]] · [[integration-map]] · [[deploy-request-path]]
- Proyectos pares: [[Onboarding Signals]] · [[Crear Context]]
- Workspace de código: [[Fuentes — Workspace de repositorios]]
- Patrón de filtros BigQueue de referencia: `~/fuentes/vis/vis-items-loader-tagging`

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- Generar el inventario y el lint de naming desde una herramienta reproducible en `~/fuentes`, sin guardar dumps de plataforma en el vault.
- Introducir un manifiesto de compatibilidad por familia/celda que permita validar Playmaker, consumidores y CP antes de desplegar.

### Motivos / principios

- Un nombre debe expresar intención estable; tipo de runtime, ambiente, segmento y rol no deben inferirse mediante heurísticas diferentes en cada repo.
- Una excepción permitida debe ser explícita, versionada y validable; no un comentario perdido en un `application-*.yml`.

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** 
- **Memoria interna:** 
- **Motivo:** 
