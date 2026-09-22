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
updated: 2026-09-22
cssclasses:
  - wide
---

# Estandarización de Scopes RIO

%% Naming: Estandarización de Scopes RIO es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!danger] REGLA BÁSICA DEL PROYECTO
> **EL `ENVIRONMENT` DEL PIPELINE NO ES LO MISMO QUE EL SCOPE DE FURY.** Fury Routes usa la selección del frontend para dirigir la request, pero Playmaker y cada control plane deducen su lane desde el nombre canónico de su propio scope Fury y publican `scope:<lane>` en BigQueue. El filtro entrante se valida contra esa lane. Nada de esto modifica el `Environment` funcional del pipeline, se persiste en `PipelineExecution`, participa en idempotencia/history ni crea un campo `environment_scope`.

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
- **Capability nueva (2026-08-19):** habilitar **selección independiente del scope de frontend y de backend en runtime**: Nordic/MeliLab determina el frontend y `backend` puede sobreescribir sólo el backend en test, sin acoplar el alta de scopes a un deploy del frontend. El diseño ejecutable vive en [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]].
- **Resultado esperado:** RIO dispone del catálogo funcional `production`, `staging`, `alpha`, `beta` y `gamma`, materializado en runtime con los tokens `prod`, `stage`, `alpha`, `beta` y `gamma`. Cada equipo habilita sólo las lanes y roles que necesita; el backend usa `<lane>-<rol>-<segment>`. Una operación conserva la misma lane Fury a lo largo del flujo sin modificar su pipeline environment.

## 📊 Estado actual

- **Fuente reproducible:** `~/fuentes/rio-inspector/scope_inventory.py` consulta el service graph read-only de Fury, `fury scopes status -j`, `fury describe-infra`, Config Orchestrator y los checkouts registrados; genera `rio-scopes.json`, [[scope-inventory]] y el HTML publicado desde el mismo corte.
- **Auditoría Fury 2026-09-03:** **91 scopes** en 9 aplicaciones con infraestructura: 87 `Active`, 4 `Inactive`; 47 con al menos una instancia `running` y 44 sin instancias observadas. [[rio-sdk-events]] sigue como librería sin runtime Fury.
- **Evidencia operativa:** 51 scopes tienen una route, un binding activo o instancias `running`; 15 no presentan evidencia activa y 25 no son concluyentes. Estas categorías no miden tráfico y nunca autorizan un retiro sin validación del equipo.
- **Reconciliación:** 1 consumer BigQueue pausado de [[rio-controlplane-fury]] quedó sin runtime resoluble en el service graph; se conserva explícitamente como hallazgo y no se asigna por inferencia.
- **SPEC funcional vigente:** [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) usa las etiquetas `production`, `staging`, `alpha`, `beta`, `gamma`; el estándar técnico fija `prod|stage|alpha|beta|gamma` para nombres runtime y filtros. Cada equipo adopta sólo las lanes y roles que necesita.
- **Grid publicado:** el doc Grid `01KZXKPH3YAGGX89P04GTY7B7E` separa la foto Fury del contrato funcional y no agrega instrucciones, targets, routing, filtros, segmentación ni pilotos que no estén definidos por SIG-599. El HTML narrativo quedó integrado al generador.
- **Próxima fase:** ejecutar la Fase 1 de la POC: preparar la Fury Route compartida e implementar [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]] antes de extender el recorrido a eventos, Playmaker y Flink.

## 🧪 POC alpha end-to-end — plan de implementación

### Resultado del programa

La POC debe demostrar un deploy completo en el scope Fury `alpha` y probar que ninguna etapa cruza a producción ni a otra lane. El pipeline environment del deploy permanece intacto. El contrato funcional está en SIG-599; cada repo conserva su propia SPEC técnica y este proyecto mantiene únicamente orden, dependencias, gates y evidencia de cierre.

### Fase 1 — Routing dinámico frontend → Playmaker

**Entregable técnico:** [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]].

**Resultado de fase:** cualquier scope frontend de test puede usar el mismo entrypoint no productivo de Playmaker y seleccionar otro backend de test sin cambios de código por scope; producción permanece aislada y sin selector.

| Paso | Owner | Estado | Gate de salida |
|---|---|---|---|
| 1.1 Cerrar diseño y revisión | Rodrigo | `DRAFT listo` | SPEC aprobada; ninguna decisión de negocio abierta |
| 1.2 Preparar Fury Route compartida | Rodrigo / Fury | `pending` | satisfacer la dependencia externa definida en la SPEC |
| 1.3 Implementar frontend | Rodrigo | `pending` | PR cumple la SPEC y checks del repo |
| 1.4 Certificar aislamiento | Rodrigo | `pending` | matriz default/override/desconocido/test→prod/prod→test con evidencia |
| 1.5 Rollout controlado | Rodrigo | `pending` | canary test estable y rollback probado |

Dependencia de inicio: cerrar la [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend#Dependencia externa de aprobación]]. El código puede comenzar después de aprobar la SPEC; el gate 1.4 no puede cerrarse sin evidencia real de Fury.

### Fase 2 — Routing KISS por scope en Playmaker

**Entregables:** [[POC KISS — Routing de scopes en Playmaker]] y [[SPEC técnica — Routing KISS por scope en rio-playmaker]].

**Resultado de fase:** Fury Routes selecciona una instancia de Playmaker; Playmaker no lee ni propaga `X-Rio-Scope`. Una instancia canónica resuelve su lane al startup y los dos producers activos de deployment trigger más el result producer publican `scope:<lane>` sin fallback a mensajes sin filtro. El timeout/retry queda deshabilitado en alpha y fuera de la certificación porque la DB compartida no garantiza ownership por lane.

### Fases siguientes

| Orden | Unidad | Repo / superficie | Dependencia de entrada | Gate de salida |
|---|---|---|---|---|
| 2 | Scope Fury runtime y filtros BigQueue | `rio-playmaker` | Fase 1 aprobada + G0 del planner aceptado | G1–G3 del [[POC KISS — Routing de scopes en Playmaker]] aceptados |
| 3 | Continuidad de scope en control planes | `rio-controlplane-flink` como piloto lane-affine | contrato completo de los producers Playmaker + accessor Fury + filtro BigQueue demostrados | [[SPEC técnica — Continuidad de scope en control planes RIO]] aprobada; runtime estricto, guard antes de side effects y result `scope:alpha`; GCP/KVS/PubSub/schedulers fuera |
| 4 | Aprovisionamiento de lane | Fury | Specs 2–3 aprobadas | scopes, config, routes y bindings listos sin tráfico |
| 5 | Integración | todas | gates 1–4 aceptados | golden deploy, negativos, cleanup y rollback completados |

La implementación, los archivos y los contratos de cada unidad viven sólo en su SPEC. El runbook final orquesta rollout, golden deploy, cleanup y rollback sin reescribir esas decisiones.

### Gates del programa

- **G1 Frontend:** Fase 1 aprobada y sin rutas cross-segment.
- **G2 Contratos:** Playmaker y Flink comparten `scope:<environment>` mediante el envelope BigQueue existente; los payloads SDK permanecen sin cambios.
- **G3 Infra:** recursos no productivos listos, sin tráfico y con rollback.
- **G4 E2E:** un golden deploy completa el recorrido, el frontend observa estado terminal y los negativos no producen side effects.
- **G5 Cierre:** recurso descartable eliminado, evidencia enlazada y ruta de rollback ejecutada.

## 🔀 Evidencia de planificación

El discovery de `ads-signals-frontend` que habilita la Fase 1 quedó incorporado en la SPEC técnica: baseline de repo, seam único de Playmaker, carga de configuración Nordic, persistencia y superficies de cache/estado. Este proyecto no replica ese inventario; sólo registra que el diseño está listo para revisión y que Fury sigue siendo la dependencia externa del gate de integración.

## 🚀 Propuesta ejecutiva

- **Propuesta:** estandarizar el nombre base como `<environment>-<role>`, dejar que Fury agregue `-<segment>` y usar `rio-controlplane-kms/test` como primer slice: `alpha-api` → `alpha-api-nonprod`. Si el flujo obligatorio sólo acepta `test-nonprod`, tratarlo como bridge transitorio, no como target state.
- **Qué ganamos:** una ruta explícita para regularizar el incumplimiento del plazo 2026-09-09, salida verificable de `legacy`, nombres predecibles, selección independiente de front/back, menor blast radius y una plantilla reusable para migrar el resto de RIO con canary y rollback.
- **Qué implica:** confirmar con Fury el nombre aceptado y la señal de cumplimiento; desacoplar ambiente/configuración del último token de `SCOPE`; crear el scope segmentado y sus routes; desplegar, probar y mover tráfico gradualmente; mantener el legacy como rollback; luego replicar el patrón con manifiesto, validadores y guardrails.

### Hallazgo de implementación — KMS

`rio-controlplane-kms` calcula `SCOPE_SUFFIX` con el último token de `SCOPE` y activa ese Spring profile. Como Fury agrega siempre `nonprod/nonsite`, tanto `test-nonprod` como `alpha-api-nonprod` intentarían cargar `application-nonprod.yml`, que no existe, en vez del profile lógico. La migración debe reemplazar esa heurística por un mapping explícito `scope Fury materializado → profile/config`, sin relacionarlo con el `Environment` de ningún pipeline.

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
> - [x] **[Diseño de routing de ambientes — discovery]** Auditar Playmaker, rio-sdk-events, mqclient y Fury consumer filters; separar scope Fury, pipeline environment, segmento y tópico/filtro; la decisión vigente de frontend está en [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]] #owner/me #type/research #area/meli ✅ 2026-08-12
> - [x] **[Spec funcional]** Reestructurar [[scope-naming-standard]] como Functional Specification con contrato de datos, user stories, acceptance criteria, E2E, riesgos y rollout #owner/me #type/dev #area/meli ✅ 2026-08-12
> - [x] **[Front/back — verificación de estado]** Confirmar en repos el acople actual (front por `baseURL` de config; Playmaker sin header-routing, solo env `SCOPE` + profiles + topics estáticos; CP por push HTTP + filtro `componentType`) con evidencia file:line #owner/me #type/research #area/meli ✅ 2026-08-19
> - [x] **[Front/back — verificación de filtros BigQueue]** Confirmar en `~/fuentes/vis/vis-items-loader-tagging` que los filtros son tags de valor arbitrarios (`scope:x` viable); corrige reporte previo #owner/me #type/research #area/meli ✅ 2026-08-19
> - [x] **[Grid — reestructura narrativa]** Reordenar el grid como reporte de estado + propuesta doble, con presentación, guía de lectura y decisiones abiertas consolidadas; publicado como v2 del doc Grid #owner/me #type/dev #area/meli ✅ 2026-08-25
> - [r] **[Discovery agente — integraciones y persistencia]** [[Scopes RIO - Discovery de Integraciones y Persistencia]] discovery documentado; revisar matriz, gaps y seams de refactor #owner/me #type/supervision #area/meli
> - [x] **[Grid — reconciliar y publicar]** Revalidar las 10 aplicaciones con Fury CLI, alinear la propuesta sólo con SIG-599, integrar la vista narrativa al generador y publicar el doc Grid #owner/me #type/dev #area/meli ✅ 2026-09-03
> - [ ] **[Grid — compartir con el equipo]** Presentar el Grid a Signals #owner/me #type/admin #area/meli
> - [ ] **[Alineación]** Validar inventario, propósito y ownership con el equipo Signals; resolver scopes huérfanos y excepciones #owner/me #type/research #area/meli
> - [/] **[Naming]** Validar con el equipo el contrato funcional de [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599): scopes de frontend iguales al ambiente y backend limitado a `api`/`consumer`; la materialización Fury y el manifiesto de compatibilidad se definen en el SPEC técnico #owner/me #type/dev #area/meli #blocked
> - [ ] **[Piloto KMS — segmentación obligatoria]** Revalidar el estado de la exigencia vencida, acordar una nueva fecha y confirmar si Fury acepta `alpha-api-nonprod` como remediación de `test` o exige el bridge `test-nonprod`; luego ejecutar scope+routes, canary, verificación de tráfico y rollback #owner/me #type/dev #area/meli #urgent #blocked 📅 2026-09-09
> - [ ] **[Piloto KMS — configuración]** Reemplazar `ScopeUtils` last-token por un mapping explícito de scope Fury/profile compatible con el sufijo `nonprod/nonsite` agregado por Fury #owner/me #type/dev #area/meli #blocked
> - [ ] **[Segmentación/Legacy]** Inventariar recursos live y sus `segment-id` efectivos antes de planificar migración; confirmar con Fury el mecanismo de aislamiento dentro de `nonprod` #owner/me #type/dev #area/meli #waiting
> - [ ] **[Manifest de bindings]** Definir y completar por runtime `application/scope`, lane, role, workload, channel, direction, infra-segment, contract/schema, versión y site/tenant #owner/me #type/dev #area/meli #waiting
> - [ ] **[Estándar]** Definir contrato de configuración: perfiles, segmentos, recursos compartidos/dedicados, secretos, canales, criticidad y ownership #owner/me #type/dev #area/meli #waiting
> - [ ] **[Automatización]** Diseñar validadores de CI/runtime que impidan scopes incompatibles, perfiles ausentes y rutas cross-segment accidentales #owner/me #type/dev #area/meli #waiting
> - [-] **[POC alpha — SPEC técnica SDK]** Cancelada: el contrato existente de `BigQueueMessage.filters`/mqclient ya transporta `scope:alpha`; la POC no agrega campos de scope a los DTOs #owner/me #type/dev #area/meli
> - [x] **[Fase 1 — SPEC técnica Front]** Crear [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]] con entrypoint test compartido, scope backend dinámico, aislamiento test/prod y particionado de estado/cache #owner/me #type/dev #area/meli ✅ 2026-09-16
> - [ ] **[Fase 1 — Fury Route]** Implementar y evidenciar la dependencia externa definida en la [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend#Dependencia externa de aprobación|SPEC]] #owner/me #type/dev #area/meli
> - [ ] **[Fase 1 — implementación Front]** Implementar la SPEC aprobada en `ads-signals-frontend` y completar checks del repo #owner/me #type/dev #area/meli #waiting
> - [ ] **[Fase 1 — certificación]** Ejecutar la matriz default/override/desconocido/test→prod/prod→test, probar rollback y enlazar evidencia #owner/me #type/dev #area/meli #waiting
> - [r] **[POC alpha — SPEC técnica Playmaker]** Corregir y aprobar [[SPEC técnica — Routing KISS por scope en rio-playmaker]]: runtime canónico estricto, ambos trigger producers + result filtrados, cero fallback y timeout/retry deshabilitado en alpha #owner/me #type/dev #area/meli
> - [r] **[[POC KISS — Routing de scopes en Playmaker]]** revisar y supervisar la implementación fase a fase bajo KISS/YAGNI #owner/me #type/supervision #area/meli
> - [r] **[POC alpha — SPEC técnica CPs/Flink]** Revisar y aprobar [[SPEC técnica — Continuidad de scope en control planes RIO]]: lane estricta al startup, guard `incomingLane == runtimeLane`, result siempre filtrado, cero carrier/legacy y GCP durable fuera #owner/me #type/dev #area/meli
> - [ ] **[POC alpha — SPEC técnica Infra Fury]** Crear la SPEC técnica de aprovisionamiento para scopes, Fury Config, routes, consumers y manifiesto de bindings sin crear topics #owner/me #type/dev #area/meli
> - [ ] **[POC alpha — runbook de integración]** Escribir el checklist ejecutable de orden de rollout, golden deploy, aislamiento, cleanup y rollback, sin duplicar las decisiones de las cinco SPECs técnicas #owner/me #type/dev #area/meli
> - [ ] **[POC alpha — implementación]** Implementar las SPECs técnicas aprobadas y ejecutar la vuelta completa de deploy en alpha #owner/me #type/dev #area/meli #waiting
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
- **2026-09-16 (POC alpha planificada)** — La segunda parte del proyecto queda acotada a una vuelta real de deploy `ads-signals-frontend -> rio-playmaker -> rio-controlplane-flink -> rio-playmaker -> frontend`, toda en `alpha`. Se elimina el header custom como requisito de la POC, se toma el filtro BigQueue por tag como capability disponible, se mantienen `rio-deployment-trigger`/`rio-deployment-result`, se dejan Actions y Observability fuera de alcance y se divide el trabajo en cinco futuras SPECs técnicas más un runbook de integración, sin crear esos artefactos en esta sesión.
- **2026-09-16 (Fase 1 replanteada y especificada)** — La primera implementación de la POC pasa a ser el routing dinámico de backend en `ads-signals-frontend`: el plan de ejecución queda en este proyecto y el diseño objetivo en [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]]. Se adopta una entrada test compartida por header, sin catálogo frontend de scopes; producción conserva su entrada aislada y Fury queda como gate externo de no-crossing.
- **2026-09-16 (Fase 2 Playmaker — diseño invalidado)** — La primera versión del planner confundió el scope Fury con estado de `PipelineExecution`; esa resolución queda invalidada.
- **2026-09-17 (Fase 2 corregida; supersedida el 2026-09-21)** — Rodrigo establece la regla `Pipeline Environment ≠ Fury Scope`. La primera corrección propuso propagar `X-Rio-Scope` sólo en memoria; la revisión posterior de la Fase 2 reemplazó ese carrier por derivación desde el scope Fury del runtime. No hay persistencia, migrations, idempotencia/history scope-aware ni cambios SDK.
- **2026-09-21 (Fase 3 CPs diseñada; supersedida el 2026-09-22)** — La primera versión de [[SPEC técnica — Continuidad de scope en control planes RIO]] definió Flink con parser fail-closed, `expectedScope`, carrier in-memory y publicación filtrada. La comparación sobre refs remotas frescas confirmó primitivas reutilizables en `rio-sdk-events` y boundaries comunes; la revisión del día siguiente eliminó la configuración y el carrier duplicados.
- **2026-09-22 (Fase 3 alineada con Playmaker)** — Se corrige la autoridad del routing: cada CP deduce la lane desde su scope Fury canónico y usa el filtro entrante sólo como aserción. Se eliminan `expectedScope` y el carrier in-memory; el publisher vuelve a resolver la lane local. La POC queda gated por confirmar el accessor oficial de Fury, porque `java-toolkit-shared` observado sólo expone helper de segmento. Los reconciliadores siguen requiriendo ownership aislado por lane.
- **2026-09-22 (review independiente aplicado con KISS/YAGNI)** — Se acepta que `unresolved=legacy` era fail-open, que Playmaker tiene dos trigger producers activos y que Flink GCP/Playmaker timeout no son lane-affine. La corrección no agrega classifier de cuatro estados ni persistencia: el artefacto alpha exige scope canónico al startup, no tiene fallback, filtra ingreso/egreso y excluye/deshabilita los paths durables. Fury/BigQueue pasa a gate real de plataforma. La generalización queda postergada hasta un segundo caso.

## 🧭 Decisiones

- **Ownership y jerarquía:** proyecto humano raíz (`owner: me`, `root: true`) bajo [[Meli]], tercero del dominio Signals. No es subproyecto de onboarding ni de [[Crear Context]].
- **Separación de fases:** el inventario as-is se completa antes de diseñar naming o implementar cambios. La propuesta y la adopción pertenecen a este mismo objetivo, pero quedan gated por evidencia.
- **Definición operativa vigente:** un scope existe si el service graph Fury lo lista; lifecycle, health, segmento y binding se registran como dimensiones independientes.
- **Dimensiones separadas:** el estándar debe distinguir al menos lane/celda, aplicación, rol/workload, scope Fury lógico, pipeline environment, segmento Fury, canal y contrato/schema.
- **Tres ejes separados:** pipeline environment es dominio del data product; scope Fury (`prod/stage/alpha/beta/gamma`) identifica la lane de infraestructura; `metadata.segment` (`legacy/nonprod/nonsite`) describe placement físico. Ninguno reemplaza a otro.
- **Fuentes:** Fury es autoridad del inventario desplegado; los repos son autoridad de interpretación y comportamiento; el vault conserva el conocimiento durable y las decisiones.
- **Selección front/back:** Nordic/MeliLab determina el scope frontend efectivo y, por default, el backend; `backend` puede sobreescribir sólo el backend en test. Producción no procesa overrides.
- **Entrada Web de la Fase 1:** todos los scopes frontend de test comparten la entrada de Playmaker y Fury selecciona el target no-prod; contrato y guardrails en [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]].
- **Scopes dinámicos en el front:** `ads-signals-frontend` no mantiene un enum/allowlist de scopes existentes; la existencia y el target son responsabilidad de Fury. El front sólo aplica validación sintáctica.
- **Sin scopes cruzados:** una entrada test nunca resuelve infraestructura productiva y la entrada productiva nunca acepta selección test; este gate es obligatorio aunque el query param intente forzar el cruce.
- **BigQueue por segmento + filtro:** cada canal mantiene un tópico `nonsite` para `prod` y uno `nonprod` compartido por los ambientes de testing; los mensajes y consumers `nonprod` se asocian mediante `scope:<environment>`.
- **Cantidad y nombres funcionales:** frontend se nombra con `<environment>` y backend con `<environment>-<rol>-<segment>`.
- **Extensibilidad:** la Fase 1 debe demostrar que una lane de test nueva no exige un archivo de configuración ni un deploy frontend; las fases posteriores prueban que topics y contratos tampoco se duplican por ambiente.
- **DB sin cambios:** sólo `test` y `prod`; el scope es routing/cómputo, no frontera de datos.
- **Scope Fury runtime → filtro:** Fury Routes usa la selección HTTP antes de entregar la request. Playmaker y los CPs deducen la lane desde el primer token de su scope Fury canónico y publican `scope:<lane>`; no leen el header como dato de dominio ni lo persisten.
- **Sin cambio SDK en la POC:** `DeploymentTriggerMessage` y `DeploymentResultMessage` permanecen iguales; el scope Fury viaja en `BigQueueMessage.filters`/mqclient y cualquier propuesta de agregar un campo reabre explícitamente la decisión.
- **Retry fuera de la POC:** continuidad durable ante timeout/restart exige otro diseño; no se resuelve contaminando `PipelineExecution`.
- **Nombre canónico:** SIG-599 define frontend `<environment>` y backend `<environment>-<rol>-<segment>`.
- **POC end-to-end:** el CP piloto es `rio-controlplane-flink` y la cobertura obligatoria es el deploy completo; Actions, runtime status, Observability, Materializer y KMS quedan fuera.
- **Continuidad del filtro:** el artefacto alpha deriva `runtimeLane=x` al startup, exige exactamente `scope:x` antes de ejecutar y publica siempre `scope:x`. Scope inválido no arranca; missing/mismatch se descartan sin side effects. No existe `expectedScope`, carrier, fallback legacy ni persistencia en la POC.
- **Límite KISS de la garantía:** runtime-derived sin estado sólo aplica a paths lane-affine. Playmaker timeout, Flink GCP y reconciliadores compartidos quedan fuera y deshabilitados/aislados; no se agrega `routingLane` durable hasta que una fase específica lo requiera.
- **Piloto KMS separado:** la remediación de segmentación de KMS conserva su propio objetivo y no certifica la POC end-to-end.

### Preguntas abiertas para el equipo / verificaciones
1. ¿Qué decisiones de negocio y ownership se requieren para proponer retiros sin convertir bindings en una categoría genérica?
2. ¿La unidad de alineación es una lane/celda completa de RIO y qué contrato/schema debe compartir?
3. ¿Qué scopes especiales sobreviven como roles explícitos y cuáles son deuda transitoria?
4. ¿Qué path lane-affine concreto usará el golden deploy Flink y qué configuración demuestra que GCP/KVS/PubSub/schedulers no participan?
5. ¿Qué recursos pueden compartirse entre familias y cuáles deben aislarse por construcción?
6. ¿Qué capability soportada por Fury implementará el aislamiento de lanes dentro de `nonprod`?
7. ¿Dónde se versionará el manifiesto de bindings y el generador reproducible?
8. ¿Qué aplicación será el piloto de migración y quién aprueba cada retiro y cada Stream amarillo?
9. **Piloto KMS:** ¿la remediación de `test` acepta el target renombrado `alpha-api-nonprod` o exige crear `test-nonprod`? ¿Qué señal del dashboard confirma que la restricción de deploy quedó levantada y cuál es la nueva fecha acordada?

## 🔗 Docs / Links

- Inventario canónico del proyecto: [[scope-inventory]]
- Matriz de routing scope-level (Inventario 4): [[scope-compatibility-matrix]]
- Modelo de segmentación Fury: [[fury-segmentation-model]]
- Propuesta de nomenclatura (borrador): [[scope-naming-standard]]
- Spec funcional de ambientes y scopes: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) · estado `draft`
- SPEC técnica Fase 1: [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]] · estado `DRAFT`
- Planner y SPEC técnica Fase 2: [[POC KISS — Routing de scopes en Playmaker]] · [[SPEC técnica — Routing KISS por scope en rio-playmaker]] · estado `DRAFT listo para revisión independiente`
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
