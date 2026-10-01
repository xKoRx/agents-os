---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-30
due:
progress: 0
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs:
aliases:
  - "Playmaker — Context en retry, deprovision y desactivación"
  - "Playmaker — Context en retry y deprovision"
  - Context en retry y deprovision
  - Context en reintentos y undeploy
  - Playmaker Context en otros flujos
  - Context en retry, deprovision y desactivación
tags:
  - kind/project
  - area/meli
  - project/playmaker-context-retry-deprovision-desactivacion
created: 2026-09-30
updated: 2026-10-01
slug: playmaker-context-retry-deprovision-desactivacion
application: "[[rio-playmaker]]"
related:
  - "[[Crear Context]]"
  - "[[Adopción de Context en Control Planes]]"
  - "[[rio-sdk-events]]"
  - "[[rio-controlplane-clickhouse]]"
---

# Playmaker — Context en emisores existentes

%% Naming: Playmaker — Context en emisores existentes es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Playmaker — Context en emisores existentes
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> **Fase:** corrección funcional · **Próximo paso:** sincronizar SIG-645 tras renovar la sesión de Spellbook y revisar la descripción de los emisores.

## 🎯 Objetivo

Estandarizar Context como capacidad transversal de RIO y extenderlo a los emisores existentes de Playmaker incluidos: undeploy/deprovision, desactivación y republicación interna de `PROVISION` por timeout elegible. Se preservan `params`, operación, identidades, correlaciones, permisos y elegibilidad.

Los flujos funcionales son undeploy/deprovision y desactivación. La republicación es un mecanismo interno del deployment; esta entrega enriquece su mensaje cuando ya corresponde enviarlo. No crea una API ni una operación de retry.

Secuencia: **SPEC funcional → SPEC técnica → tareas → implementación → validación**. Reutiliza [[Crear Context]] y coordina la validación del consumidor con [[Adopción de Context en Control Planes]].

## 📊 Estado actual

- **Fase:** corrección funcional. [[SPEC Funcional — Context transversal en RIO]] describe dos flujos funcionales y un punto interno de envío; el ajuste local está preparado. SIG-645 tuvo estado `review` en la última lectura válida del 2026-09-30; el 2026-10-01 la CLI devuelve `Session expired` y no permite verificar ni publicar la corrección.
- **Próximo paso:** renovar la sesión, releer SIG-645 para preservar cambios ajenos y publicar título/contenido corregidos; continuar la revisión antes de crear la SPEC técnica. No se inicia implementación.
- **Base verificada:** `develop @ f087e4b7cc185d93618de4bdeaeb76b53486ac47`, resuelta por GitHub el 2026-10-01 y leída por commit sin cambiar la rama local. Comparación con `6e37608b` sin cambios en los emisores evaluados.
- **Resultado del audit:** undeploy y desactivación tienen endpoints y envían `DEPROVISION`. `DeploymentTimeoutJob` es invocado por scheduling y por historia; puede publicar `PROVISION` sólo para un deployment activo `DEPLOY/REQUESTED` elegible. El contrato SDK no define `RETRY`.
- **Límite de evidencia:** el código base configura dos intentos y una ventana de diez minutos; `local` configura cero intentos. Se verificó implementación y configuración versionada, no una release ni la configuración efectiva de producción. No afirmar un flujo operativo general de retry en producción.
- **Alcance:** mismos emisores señalados por Bren; deploy individual, cambios de política de timeouts y corrección de params quedan diferidos. `progress: 0`; SPEC técnica, tareas técnicas e implementación pendientes.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] / `fury_rio-playmaker` | Pendiente de definir antes de implementar | `develop`; referencia auditada `f087e4b7`, revalidar | [SIG-645](https://spellbook.adminml.com/projects/SIG/specs/SIG-645); corrección local en [[SPEC Funcional — Context transversal en RIO]] | Pendiente | Corrección/revisión funcional; sincronización remota bloqueada por sesión expirada |

`rio-sdk-events:1.5.0` es dependencia existente. La adopción o modificación del consumidor tiene alcance propio. No se hicieron cambios en código de aplicaciones.

## 🧭 Alcance confirmado

| Ruta | Evidencia | Alcance |
|---|---|---|
| Undeploy/deprovision | API DELETE → `ComponentDeploymentServiceImpl` → `UndeployServiceImpl`; `DEPROVISION` en BigQueue | Context en emisores genérico, Fury→Kafka y Kafka→Fury. Materializer REST y finalización sin envío no se convierten en mensajes BigQueue. |
| Desactivación | API POST inactivate → `ComponentInactivationServiceImpl`; `DEPROVISION` después del commit | Context conservando ejecución, correlación y action lock. |
| Republicación interna de deployment | `checkTimeouts` / `resolveTimeoutsForExecution` → `processTimeout` → `retry`; operación `PROVISION` | Context sólo en el envío que permite la política existente. No flujo funcional, endpoint ni operación `RETRY`. |
| Deploy por batches | Derivación y guard existentes | Referencia de comportamiento y regresión. |
| Deploy individual y otros emisores | Hallazgos adicionales | Diferidos por el owner. |

La clasificación de rutas de código no equivale a tres flujos funcionales. La existencia del timeout job está respaldada por invocaciones y publicación; su uso efectivo en una release de producción no fue verificado.

## ⚠️ Impacto y riesgos

- **Elegibilidad del envío interno:** sólo `DEPLOY/REQUESTED`, activo, timeout vencido, dentro de la antigüedad e intentos configurados, `BIG_QUEUE` y servicio/grupo/ejecución resolubles. `STARTED` y `UNDEPLOY` no se republican. Context no modifica estos guards.
- **Configuración:** la ventana base de diez minutos puede agotar la elegibilidad antes del timeout de algunos tipos; `local` deshabilita intentos. La prueba requiere un escenario/configuración admitidos, sin cambiar configuración productiva ni prometer retries generales.
- **Limitación heredada:** el envío interno usa `params = Map.of()`. Context no recupera esos parámetros ni reemplaza la configuración solicitada. Su corrección queda diferida.
- **Semántica temporal:** definición asociada al deployment, estado consultado al envío y versión histórica del mismo servicio/ambiente. No snapshot idéntico al primer mensaje.
- **Retiro:** obtener el último `deploy_completed` y sus outputs antes de la transición a `undeploy_requested`; no inventar historia si no existe.
- **Compatibilidad:** preservar params específicos de Fury, identidades, correlaciones y fronteras transaccionales. Desactivación publica después del commit y correlaciona por execution ID.
- **Disponibilidad:** reutilizar derivación parcial, fallback y límite de 200 KiB del mensaje completo. Medir duración, tamaño y descartes sin valores sensibles ni nuevos thresholds.

## ✅ Criterios para validar la entrega

- Context coherente en los emisores de deprovision y desactivación; en la republicación interna, únicamente cuando la ruta existente decide emitir `PROVISION`.
- Casos no elegibles y finalizaciones sin mensaje no generan publicaciones adicionales por incorporar Context.
- Fallo de construcción, medición o exceso de tamaño: mensaje sin Context y otros campos preservados. Límite exacto conservado.
- Versión y outputs de retiro del recurso objetivo; ausencia histórica y relaciones vacías conservan el contrato parcial.
- Preservación de parámetros Fury, correlación, persistencia, publicación después de commit y action lock; regresión de batches.
- Validación del consumidor en un entorno que soporte cada operación. No declarar validación productiva por inspeccionar código o mocks.

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

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [r] Revisar [[SPEC Funcional — Context transversal en RIO|SIG-645]]: dos flujos funcionales y un envío interno de PROVISION; publicar la corrección tras renovar sesión #owner/me #type/dev #area/meli
> - [ ] Crear y revisar la SPEC técnica desde los emisores y guards verificados; mantener la política de timeouts #owner/me #type/dev #area/meli
> - [ ] Desglosar tareas técnicas desde las SPECs y enlazar IDs de Spellbook #owner/me #type/dev #area/meli
> - [ ] Registrar y verificar branch y base de Playmaker antes de implementar #owner/me #type/dev #area/meli
> - [ ] Implementar Context en los emisores incluidos según las SPECs cerradas #owner/me #type/dev #area/meli
> - [ ] Validar caminos críticos, elegibilidad, fallback, tamaño y regresiones; comprobar coverage requerido #owner/me #type/dev #area/meli
> - [ ] Coordinar con Bren la prueba del consumidor en escenarios existentes admitidos #owner/me #type/dev #area/meli
> - [ ] Preparar PR con evidencia, completar review y registrar rollout #owner/me #type/pr-review #area/meli

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

- **2026-10-01 — Sesión cerrada por pedido del owner:** feedback en [[2026-10-01-playmaker-context-flow-verification-session-feedback]] y aprendizaje [[verificar-invocaciones-antes-de-describir-flujos-de-playmaker]]. Corrección local lista; sincronización de SIG-645 pendiente de renovar la sesión de Spellbook. Próximo paso: releer, publicar y verificar antes de avanzar a la SPEC técnica.
- **2026-10-01 — Corrección de clasificación:** el owner reporta que se cuestionó la existencia de retry. Se auditan endpoints, scheduling, historia, guards, configuración y productores en `develop @ f087e4b7`. Se distingue undeploy/desactivación de la republicación interna de `PROVISION`; se elimina la descripción de un tercer flujo funcional de retry, se renombra el proyecto conservando aliases y se prepara SIG-645 corregida. Publicación pendiente por `Session expired`.
- **2026-09-30 — Ajuste visual y aclaración E2E:** el owner reporta que Spellbook no muestra el diagrama y solicita una visual en texto. La copia local reemplaza Mermaid por un diagrama de texto e identifica E2E-4 como política común de degradación de RF-6/RF-7, sin agregar flujos. La lectura inicial confirma SIG-645 en `review`; la edición y las lecturas siguientes devuelven `Authentication failed`. La publicación del ajuste queda pendiente de renovar la sesión de CLI.
- **2026-09-30 — SPEC funcional creada:** el owner aprueba el motivo de capacidad transversal y estandarización y solicita crear la SPEC. Se guarda [SIG-645](https://spellbook.adminml.com/projects/SIG/specs/SIG-645) en Spellbook, tipo funcional y estado `draft`, con tres historias, nueve requisitos, nueve criterios de aceptación y cuatro escenarios E2E. El contenido guardado se verifica contra el borrador local. La revisión funcional queda pendiente; no se crean la SPEC técnica, tareas técnicas ni cambios de código.
- **2026-09-30 — Ajuste de alcance:** el owner confirma que quiere abordar ahora los tres flujos declarados por Bren y dejar cualquier hallazgo adicional para después. Se incluye desactivación, se excluyen deploy individual y corrección de params del retry, y se renombra el proyecto conservando el título anterior como alias. Se actualizan objetivo, alcance, tareas y criterios de validación; las SPECs e implementación siguen pendientes.
- **2026-09-30** — El owner solicita una iniciativa nueva para extender Context, con SPECs antes de implementación. Se materializa el proyecto con evaluación read-only, alcance inicial de retry y tres variantes de deprovision, extensiones pendientes de decidir, riesgos, criterios de validación y checklist secuencial. No se crean SPECs, ramas ni cambios de código en esta etapa.

## 🧭 Decisiones

- Context es una capacidad transversal y opcional; esta entrega sólo enriquece mensajes de los emisores existentes incluidos.
- Dos flujos funcionales: undeploy/deprovision y desactivación. El punto de republicación interna pertenece al deployment y conserva `PROVISION` y sus guards.
- No crear endpoint/operación de retry, cambiar intentos/timeouts ni habilitar envíos nuevos. No equiparar código en develop con uso productivo verificado.
- Seguir SPEC funcional → técnica → tareas → implementación; corregir/sincronizar SIG-645 antes de avanzar.
- Deploy individual, otras operaciones y la corrección de params vacíos quedan para después. Sin nueva versión de SDK ni migración de consumidores.
- El nombre anterior se conserva como alias; el slug/tag técnico continúa estable para no romper routing histórico.

## 🔗 Docs / Links

- [[SPEC Funcional — Context transversal en RIO]] — corrección local de [SIG-645](https://spellbook.adminml.com/projects/SIG/specs/SIG-645), UUID `b3b0fb05-d64f-4119-b98e-6aac9b36ca3c`; sincronización pendiente de sesión válida.
- [[rio-playmaker]], [[rio-sdk-events]], [[rio-controlplane-clickhouse]], [[Crear Context]] y [[Adopción de Context en Control Planes]].
- [Invocación/guards del timeout job](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/DeploymentTimeoutJob.java#L124-L285), [PROVISION y publicación](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/DeploymentTimeoutJob.java#L311-L360), [invocación desde historia](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/impl/PipelineHistoryServiceImpl.java#L87-L104), [scheduling](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/config/ExecutorConfig.java#L23-L26).
- [API undeploy](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/controller/ComponentDeploymentController.java#L158-L175), [emisores deprovision](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/impl/UndeployServiceImpl.java#L562-L673), [API inactivate](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/controller/ComponentInactivationController.java#L54-L79), [emisión de desactivación](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/impl/ComponentInactivationServiceImpl.java#L383-L471).
- [Política base](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/resources/application.yml#L264-L294) y [local: cero intentos](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/resources/application-local.yml#L68-L82).
- [[2026-10-01-playmaker-context-flows-corrected]] — resolución de la clasificación y evidencia del audit.
- [[verificar-invocaciones-antes-de-describir-flujos-de-playmaker]] — criterio para verificar rutas existentes antes de describirlas en una SPEC.

## 💡 Ideas

- Evaluar en la SPEC técnica un colaborador pequeño para derivación y enriquecimiento del trigger que pueda usarse desde ambos producers, sin unificar el lifecycle de los flujos.
- **Para después:** agregar Context al deploy individual y evaluar la corrección de `params` vacío en retry. Son hallazgos diferidos, sin tareas de implementación ni gates de cierre en esta entrega.
