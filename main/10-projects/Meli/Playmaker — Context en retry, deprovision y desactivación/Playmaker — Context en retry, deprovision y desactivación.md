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
updated: 2026-09-30
slug: playmaker-context-retry-deprovision-desactivacion
application: "[[rio-playmaker]]"
related:
  - "[[Crear Context]]"
  - "[[Adopción de Context en Control Planes]]"
  - "[[rio-sdk-events]]"
  - "[[rio-controlplane-clickhouse]]"
---

# Playmaker — Context en retry, deprovision y desactivación

%% Naming: Playmaker — Context en retry, deprovision y desactivación es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Playmaker — Context en retry, deprovision y desactivación
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> **Fase:** preparación de SPECs · **Próximo paso:** SPEC funcional en Spellbook.

## 🎯 Objetivo

Extender la publicación de `DeploymentTriggerMessage.context` en Playmaker a los tres flujos declarados por Bren: retry por timeout, undeploy/deprovision y desactivación de componente, manteniendo la configuración de la operación en `params`, las identidades y correlaciones existentes, y la derivación de Context como información opcional que no bloquea el envío.

La secuencia de trabajo es **SPEC funcional → SPEC técnica → tareas → implementación → validación**. Este proyecto es una nueva entrega de cambio; reutiliza el contrato de [[Crear Context]] y coordina la prueba del consumidor con [[Adopción de Context en Control Planes]].

## 📊 Estado actual

- **Fase:** preparación de SPECs. La evaluación inicial está completa; las SPECs, las tareas técnicas y la implementación aún no comienzan. `progress: 0` corresponde a la entrega pendiente.
- **Próximo paso:** redactar la SPEC funcional en Spellbook para los tres flujos incluidos y definir criterios de aceptación antes de diseñar la solución técnica. El owner ya cerró el alcance: lo declarado por Bren ahora; los hallazgos adicionales quedan para después.
- **Base inspeccionada:** `rio-playmaker @ c4ac43da4a1c7222e4cdbceaff666978c96e0811`; comparación read-only con `develop @ 6e37608bca25cc15c8c413b55d6dd91e5b2e831d` el 2026-09-30. Los emisores y el builder revisados no cambiaron entre esos commits. Revalidar la base al comenzar las SPECs y la implementación.
- **Resultado de la evaluación:** cambio acotado en Playmaker, con riesgo medio en retry y en la selección de la versión de deprovision. El SDK 1.5.0 ya está disponible y consumido por Playmaker; el alcance aditivo no requiere cambiar el contrato ni migrar datos.
- **Origen y alcance confirmado:** conversación aportada por el owner con Bren Kikuta y aclaración del owner el 2026-09-30. Se incluyen retry, deprovision y desactivación, aunque esta última no sea habitual en ClickHouse. Deploy individual y correcciones adicionales detectadas durante la evaluación quedan fuera de esta entrega.
- No se modificó código de aplicaciones ni se ejecutaron pruebas durante la evaluación. Falta validar recepción y consumo en la versión concreta de ClickHouse que participará en la prueba.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] / `fury_rio-playmaker` | Pendiente de definir y verificar al iniciar implementación | `develop`; referencia evaluada `6e37608b`, revalidar antes de trabajar | Pendiente de crear en Spellbook y enlazar | Pendiente de crear en Spellbook y enlazar | Preparación; implementación pendiente de SPECs, tareas y branch/base verificadas |

`rio-sdk-events:1.5.0` es una dependencia existente; no hay entrega nueva de SDK planificada. ClickHouse participa como consumidor de validación: cualquier modificación de su código debe definirse como alcance propio y tener sus SPECs y branch/base.

## 🧭 Alcance confirmado

| Flujo | Situación verificada | Alcance confirmado para la SPEC |
|---|---|---|
| Deploy del pipeline por batches | `DispatchRequestFactory` deriva Context y `BigQueueDispatchAdapter` lo publica | Referencia de comportamiento y regresión |
| Retry por timeout | `DeploymentTimeoutJob.retry` usa el constructor sin Context | Incluir en la primera entrega |
| Deprovision genérico | `UndeployServiceImpl.publishGenericBigQueueDeprovisionTrigger` usa el constructor sin Context | Incluir en la primera entrega |
| Deprovision Fury→Kafka y Kafka→Fury | `publishDeprovisionTrigger` y `publishKafkaFuryStreamsDeprovisionTrigger` tampoco agregan Context | Incluir para no dejar deprovision parcialmente cubierto |
| Desactivación de componente | `ComponentInactivationServiceImpl.buildDeprovisionMessage` envía `DEPROVISION` sin Context | Incluir en esta entrega: tercer flujo declarado por Bren |
| Deploy individual | `DeploymentServiceImpl` construye otro trigger `PROVISION` sin Context | Fuera de alcance; hallazgo adicional diferido por el owner |

Esta entrega cubre los tres flujos declarados por Bren. Las variantes genérica y Fury forman parte de un mismo flujo de deprovision. El deploy por batches sólo participa como regresión; no se busca cobertura universal de todos los triggers ni se incorporan otros hallazgos a las SPECs o tareas de esta entrega.

## ⚠️ Impacto y riesgos

- **Limitación heredada del retry:** hoy envía `params = Map.of()`. Se registra como riesgo de validación, pero su corrección queda diferida por la instrucción del owner de abordar sólo la ausencia de Context declarada por Bren. Agregar Context no recupera por sí solo los params solicitados; `latestVersion` describe un deployment completado anterior y puede faltar en un primer deployment. No atribuir a esta entrega una corrección de la equivalencia del retry.
- **Semántica temporal del retry:** el Context existente es efímero y se deriva desde estado consultado al enviarlo. Definir qué identidad, versión, ambiente y usuario conserva el reintento y reconocer que recalcular Context no reproduce un snapshot idéntico al original.
- **Versión de deprovision:** `ComponentContextService.build` busca el último deployment no eliminado con estado `deploy_completed`. Construir Context antes de cambiar el deployment a `undeploy_requested`; validar también que la versión y los outputs seleccionados correspondan al recurso objetivo.
- **Compatibilidad:** conservar `params`, operación, campos planos de identidad y correlación. En Fury se deben preservar `mappingId` y los descriptores `source`/`destination` que necesita deprovision.
- **Disponibilidad y payload:** reutilizar la derivación tolerante a fallas y el límite existente de 200 KiB sobre el mensaje completo. Si la derivación o medición falla, o el candidato excede el límite, publicar el trigger sin Context y registrar la causa.
- **Coste operacional:** más consultas y serialización por retry, deprovision y desactivación; el timeout job mantiene el deployment bloqueado durante su procesamiento. Medir duración de derivación, tamaño y descartes, sin inventar thresholds nuevos.
- **Fronteras de publicación:** los flujos usan dos interfaces de producer y distintas reglas transaccionales. Compartir enriquecimiento y protección de Context sin trasladarles efectos de `BigQueueDispatchAdapter` que cambien correlación, timeout o persistencia. En desactivación, preservar su publicación después del commit, la correlación por execution ID y el ciclo del action lock.
- **Datos sensibles:** no registrar valores crudos de `params` o Context. Mantener la responsabilidad vigente del CP sobre la protección de outputs.

## ✅ Criterios para validar la entrega

- Context presente en los tres flujos declarados por Bren: retry, deprovision (emisores genérico y de Fury) y desactivación. Verificar componente, definición, servicio, ambiente y usuario correctos.
- Fallo de derivación, medición o exceso de tamaño: trigger publicado sin Context, preservando sus otros campos y las métricas de causa.
- En deprovision, la última versión y sus outputs siguen disponibles al construir el mensaje; cubrir también ausencia de versión histórica y referencias que ya no puedan resolverse.
- Preservar `params`, operación, correlaciones y efectos de persistencia/publicación; probar especialmente los parámetros específicos de Fury y la política vigente de elegibilidad del retry.
- Desactivación: verificar Context derivado desde el service y su definición, publicación después del commit, correlación por execution ID y preservación del ciclo del action lock. Validar este flujo en un entorno de prueba aunque ClickHouse no lo use habitualmente.
- Regresión del deploy por batches y prueba E2E de retry/deprovision con ClickHouse correlacionada por `deploymentId`, verificando recepción, uso esperado y resultado de la operación.
- Verificar primero los caminos críticos y después el piso de coverage vigente del equipo. Publicar cualquier versión de prueba con sufijo; la release productiva sigue la policy del repositorio.

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
> - [ ] Crear y revisar la SPEC funcional en Spellbook para retry, deprovision y desactivación: semántica de Context y criterios de aceptación #owner/me #type/dev #area/meli
> - [ ] Crear y revisar la SPEC técnica en Spellbook: integración de los tres flujos, derivación compartida, guard de tamaño, versión de deprovision, publicación/correlación de desactivación, métricas y plan de pruebas #owner/me #type/dev #area/meli
> - [ ] Desglosar las tareas técnicas desde las SPECs y enlazar sus IDs de Spellbook en el proyecto #owner/me #type/dev #area/meli
> - [ ] Registrar y verificar branch y base de Playmaker antes de implementar #owner/me #type/dev #area/meli
> - [ ] Implementar Context en retry, deprovision (genérico y variantes Fury) y desactivación según las SPECs cerradas #owner/me #type/dev #area/meli
> - [ ] Validar caminos críticos, fallback, tamaño y regresiones; comprobar el coverage requerido #owner/me #type/dev #area/meli
> - [ ] Coordinar con Bren la prueba de la versión de test y verificar el flujo E2E en ClickHouse #owner/me #type/dev #area/meli
> - [ ] Preparar la descripción de PR con evidencia, completar el review y registrar el resultado del rollout #owner/me #type/pr-review #area/meli

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

- **2026-09-30 — Ajuste de alcance:** el owner confirma que quiere abordar ahora los tres flujos declarados por Bren y dejar cualquier hallazgo adicional para después. Se incluye desactivación, se excluyen deploy individual y corrección de params del retry, y se renombra el proyecto conservando el título anterior como alias. Se actualizan objetivo, alcance, tareas y criterios de validación; las SPECs e implementación siguen pendientes.
- **2026-09-30** — El owner solicita una iniciativa nueva para extender Context, con SPECs antes de implementación. Se materializa el proyecto con evaluación read-only, alcance inicial de retry y tres variantes de deprovision, extensiones pendientes de decidir, riesgos, criterios de validación y checklist secuencial. No se crean SPECs, ramas ni cambios de código en esta etapa.

## 🧭 Decisiones

- Crear una iniciativa propia de [[Meli]], `owner: me` y `root: true`, sin reabrir [[Crear Context]] ni convertir este proyecto en el owner de la adopción del consumidor.
- Seguir Spellbook/SDD: SPEC funcional, SPEC técnica, tareas e implementación. La próxima etapa es la SPEC funcional; las SPECs aún no existen.
- **Alcance cerrado por el owner el 2026-09-30:** incluir únicamente los tres flujos declarados por Bren: retry por timeout, undeploy/deprovision y desactivación de componente. Deprovision incluye sus emisores genérico y específicos de Fury. Deploy individual y cualquier hallazgo adicional se postergan; no abrir tareas para resolverlos en esta entrega.
- Mantener Context como campo opcional y aditivo, con `params` como configuración de la operación. No retirar `params`, persistir snapshots de Context, modificar operaciones ni introducir una nueva versión del SDK como parte del alcance inicial.
- Reutilizar builder, métricas y protección de tamaño existentes. El diseño concreto se cerrará en la SPEC técnica.
- Preservar los `params` actuales. La corrección del `params` vacío del retry queda para después; documentar la limitación sin convertirla en un cambio de esta entrega.

## 🔗 Docs / Links

- [[rio-playmaker]], [[rio-sdk-events]] y [[rio-controlplane-clickhouse]].
- [[Crear Context]] — contrato iteración 1.5 y entrega previa; evitar usar sus secciones históricas como diseño vigente.
- [[Adopción de Context en Control Planes]] — iniciativa relacionada del consumidor; su estado histórico no reemplaza la verificación de código actual.
- SPEC funcional, SPEC técnica y tareas: pendientes de creación en Spellbook; agregar enlaces e IDs reales cuando existan.
- [Retry por timeout — constructor sin Context y params vacío](https://github.com/melisource/fury_rio-playmaker/blob/c4ac43da4a1c7222e4cdbceaff666978c96e0811/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/DeploymentTimeoutJob.java#L333-L360).
- [Deprovision — los tres emisores](https://github.com/melisource/fury_rio-playmaker/blob/c4ac43da4a1c7222e4cdbceaff666978c96e0811/src/main/java/com/mercadolibre/rio/playmaker/service/impl/UndeployServiceImpl.java#L562-L673).
- [Selección de última versión completada en ComponentContextService](https://github.com/melisource/fury_rio-playmaker/blob/c4ac43da4a1c7222e4cdbceaff666978c96e0811/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/ComponentContextService.java#L79-L118).
- [Derivación tolerante a fallas en DispatchRequestFactory](https://github.com/melisource/fury_rio-playmaker/blob/c4ac43da4a1c7222e4cdbceaff666978c96e0811/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/DispatchRequestFactory.java#L97-L140).
- [Protección de tamaño del mensaje completo en BigQueueDispatchAdapter](https://github.com/melisource/fury_rio-playmaker/blob/c4ac43da4a1c7222e4cdbceaff666978c96e0811/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/BigQueueDispatchAdapter.java#L114-L148).
- [Desactivación — publicación y constructor](https://github.com/melisource/fury_rio-playmaker/blob/c4ac43da4a1c7222e4cdbceaff666978c96e0811/src/main/java/com/mercadolibre/rio/playmaker/service/impl/ComponentInactivationServiceImpl.java#L383-L471).
- [Deploy individual — constructor sin Context](https://github.com/melisource/fury_rio-playmaker/blob/c4ac43da4a1c7222e4cdbceaff666978c96e0811/src/main/java/com/mercadolibre/rio/playmaker/service/impl/DeploymentServiceImpl.java#L1016-L1031).
- [Comparación del commit citado con develop evaluado](https://github.com/melisource/fury_rio-playmaker/compare/c4ac43da4a1c7222e4cdbceaff666978c96e0811...6e37608bca25cc15c8c413b55d6dd91e5b2e831d).

## 💡 Ideas

- Evaluar en la SPEC técnica un colaborador pequeño para derivación y enriquecimiento del trigger que pueda usarse desde ambos producers, sin unificar el lifecycle de los flujos.
- **Para después:** agregar Context al deploy individual y evaluar la corrección de `params` vacío en retry. Son hallazgos diferidos, sin tareas de implementación ni gates de cierre en esta entrega.
