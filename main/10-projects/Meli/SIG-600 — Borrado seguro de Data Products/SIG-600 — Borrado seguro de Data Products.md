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
start: 2026-09-28
due:
progress: 0
repo:
jira:
prs:
aliases:
  - SIG-600
  - Delete Data Products
  - Borrado de Data Products
  - SIG-643
entities:
  - "[[rio-playmaker]]"
  - "[[ads-signals-frontend]]"
related:
  - "[[RIO]]"
tags:
  - kind/project
  - area/meli
  - project/sig-600
created: "2026-09-28"
updated: "2026-10-01"
---

# SIG-600 — Borrado seguro de Data Products

%% Naming: SIG-600 — Borrado seguro de Data Products es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ SIG-600 — Borrado seguro de Data Products
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[SIG-600 — Borrado seguro de Data Products]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Implementar el borrado seguro de Data Products de [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600): bloquearlo ante componentes activos en producción, importaciones pendientes o vigentes, y despliegues o infraestructura activa; mostrar una causa específica en el listado y en el detalle.
- Usar [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) como diseño técnico. Playmaker valida dentro del `DELETE`; el frontend comparte modal y mensajes entre ambas entradas. La ejecución y el avance viven en este proyecto; los contratos viven en las SPECs.

## 📊 Estado actual

- **Autorización Playmaker en [PR #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228): `d6a72a7e1` publicado, develop `dc38ad5a9` integrado, MERGEABLE y los cinco checks de Fury SUCCESS, incluido CI #5758 sobre el mismo SHA.** Se conserva el lock de ownership y Kraken OR membresía del owner para DELETE; la identidad viene del principal autenticado. El guard independiente de cascade heredado de PR #1182 exige el grant del owner cuando el ownership está completo, incluso para equipo plataforma. Update y updateStatus conservan el mismo lock y transacción, con 403 para el owner previo, 404 después del borrado y 410 para DELETE repetido autorizado. Escenarios de esta rama AT-010-S18/S17, sin colisiones con develop. Regresión: 4.383 tests, 0 fallas/errores y 2 skips preexistentes; 83 selectores y los tres checks LOCAL_STACK PASS. Cleanup de MySQL, loopback y Kafka certificado. Review humana pendiente. La [descripción canónica](<Descripción PR — rio-playmaker.md>) conserva las variantes mock y capturas. Acceso Fury a Kraken, revisión especializada de dependencia, coordinación de blockers concurrentes y BFF/UI pendientes; iniciativa activa y SPECs sin cambios.
- SIG-600 CA-1 aún pide prevalidar antes del `DELETE`; SIG-643 valida dentro. También queda pendiente coordinar las rutas de deploy concurrentes y las demás reglas de bloqueo antes de considerar lista la iniciativa completa.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] | `feature/sig-600-delete-auth` · `/Users/rjara/fuentes/rio-playmaker-sig-600-delete-auth` | `develop@dc38ad5a9` | [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) | [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) | [PR #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228), HEAD `d6a72a7e1`, MERGEABLE; CI #5758 y los cinco checks de Fury SUCCESS; 4.383 tests sin fallas, 83 selectores y tres checks LOCAL_STACK PASS; cleanup certificado; lock de ownership y guard de cascade conservados; aprobación humana requerida; acceso Fury y BFF/UI pendientes |
| [[ads-signals-frontend]] | Pendiente de crear | `origin/master@791f79dd8` (baseline leído para SIG-643; base de trabajo por definir) | [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) | [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643) | Retirar guard duplicado del proxy; CA-1 abierto; sin implementación |

## 🧪 Variantes temporales de autorización en test3

| Escenario | Branch | Versión TEST | HEAD | Estado |
|---|---|---|---|---|
| Sin ACME ni Kraken | `feature/sig-600-delete-auth-mock-denied-test3` | [0.0.5-test-sig600-denied](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.5-test-sig600-denied) | `4633cee05` | FINISHED, tests habilitados |
| Solo ACME | `feature/sig-600-delete-auth-mock-acme-test3` | [0.0.3-test-sig600-acme](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.3-test-sig600-acme) | `ebe2807e3` | FINISHED, tests habilitados |
| Solo Kraken | `feature/sig-600-delete-auth-mock-kraken-test3` | [0.0.4-test-sig600-kraken](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.4-test-sig600-kraken) | `252b2324c` | FINISHED, tests habilitados |

- Base funcional: PR #1228 `73fabcfb9`. Worktrees bajo `/Users/rjara/fuentes/rio-playmaker-sig-600-delete-auth-mock-*`.
- Solo DELETE usa respuestas sintéticas de providers; Tiger y blockers existentes siguen activos. ACME_ONLY simula membresía del equipo actual del DP sin modificar DB. Los clients globales no se reemplazan. Ningún perfil distinto de test3 activa los mocks; también se excluyen perfiles production/staging combinados con test3.
- Con deployments activos: NONE devuelve 403 `DP_DELETE_FORBIDDEN` antes de consultar blockers; ACME_ONLY y KRAKEN_ONLY llegan al bloqueo existente 409. Probar directamente en Playmaker, porque el BFF conserva su guard ACME real.
- Cada variante pasó 4.056 tests locales, 0 fallas, 2 skips preexistentes. Gate focalizado y validadores pasan; LOCAL_STACK bloqueado por Docker apagado. Se corrigió un test de fecha que fallaba al cruzar un segundo: ahora exige que deletedAt esté dentro del intervalo real del DELETE.
- [Runbook](</Users/rjara/fuentes/rio-playmaker-sig-600-delete-auth-mock-test3/docs/runbook-sig600-delete-auth-mock-test3.md>). La versión inicial `0.0.2-test-sig600-denied` queda reemplazada por `0.0.5-test-sig600-denied`, que incluye la corrección del test temporal. El usuario aportó capturas de validación manual en el PR. El agente no realizó deploys ni DELETEs remotos. Los mocks no forman parte del PR funcional ni completan las reglas nuevas de SIG-600.

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
> - [ ] Resolver la discrepancia de CA-1 entre SIG-600 y SIG-643 antes de implementar #owner/me #type/admin #area/meli
> - [x] Confirmar SDK o API Java de Kraken para consultar `delete-data-products` con identidad Tiger #owner/me #type/research #area/meli ✅ 2026-09-29
> - [ ] Habilitar tráfico Fury de rio-playmaker a Kraken (`kraken_for_applications_external-kraken-all`) y revisar nueva dependencia con el MCP de seguridad #owner/me #type/admin #area/meli
> - [r] Implementar autorización Kraken OR ACME en Playmaker; [PR #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228) en revisión y CI #owner/me #type/dev #area/meli
> - [x] Fijar precedencia de bloqueos, producción por `EnvironmentModel.type` y HTTP 409 con códigos #owner/me #type/admin #area/meli ✅ 2026-09-28
> - [ ] Relevar rutas de deploy que crean blockers, cerrar su protocolo transaccional y llevar SIG-643 a review #owner/me #type/research #area/meli
> - [/] Elegir branch y base actualizadas para Playmaker y frontend; Playmaker en `develop`, frontend pendiente #owner/me #type/dev #area/meli
> - [ ] Implementar en Playmaker los tres bloqueos, coordinar importaciones y rutas de deploy, y emitir códigos estables #owner/me #type/dev #area/meli
> - [ ] Propagar códigos en el BFF y compartir modal/flujo entre listado y detalle con resultado incierto separado de éxito #owner/me #type/dev #area/meli
> - [ ] Verificar los CA de SIG-600, el `DELETE` directo, permisos y ambas órdenes de carrera; preparar PRs #owner/me #type/dev #area/meli
> - [x] Crear ramas y versiones TEST3 con mocks NONE/ACME_ONLY/KRAKEN_ONLY; builds FINISHED y regresión local verde #owner/me #type/dev #area/meli ✅ 2026-09-30

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

- **2026-10-01 — Nueva iniciativa en develop** — PR #1182 avanzó la base a `dc38ad5a9`. Se conservaron ambas capas de autorización y el lock, se resolvieron los cuatro conflictos y la nueva colisión del catálogo con AT-010-S18/S17. El nuevo setup Mockito delega la lectura bloqueada; se adaptó el stub con doReturn sin debilitar el verify de una sola lectura y ningún save. Regresión de 4.383 tests, 0 fallas/errores, 2 skips; 83 selectores y tres LOCAL_STACK PASS. Cleanup de los tres proyectos del run certificado. Merge `d6a72a7e1` publicado y MERGEABLE frente al último develop; CI #5758 y los cinco checks de Fury SUCCESS en el SHA exacto. Cobertura global 94,84% y del PR 94,02%; static-analyzer sin issues nuevos. Dependencies SUCCESS con aviso LOW por autobulk heredado de develop. Code Scanning de GitHub conserva startup_failure previo sin jobs; no es un check de Fury. Checkout limpio. Sesión AGENTS OS cerrada por pedido explícito; feedback registrado en [[2026-10-01-rio-playmaker-pr-1228-session-feedback]]. La iniciativa sigue activa; review humana pendiente.

- **2026-10-01 — Sincronización posterior y cierre solicitado** — Develop avanzó a `45c92f5ad` con autorización de componentes/pipelines. Se resolvieron conflictos de servicio, tests, manifiesto y testing.md conservando ambas capas de autorización, el principal autenticado y el lock. Se renumeraron AT-010-S16/S17. Regresión de 4.216 tests, 0 fallas/errores, 2 skips; 74 selectores y los tres LOCAL_STACK PASS, con cleanup certificado. Merge `90f7ecebb` publicado y MERGEABLE; CI #5755 SUCCESS. El usuario pidió feedback y cierre de AGENTS OS al completar la validación remota.

- **2026-10-01 — Ownership concurrente** — Se corrigió el hallazgo del bot: DELETE usa la lectura bloqueada que incluye soft-deleted, mientras update y updateStatus adquieren el mismo lock para filas activas. Tres tests con transacciones H2 reales detectan las lecturas sin lock y pasan con la corrección. Commit `d97a5500f` publicado; disparó CI #5726. Develop avanzó a `54c788ba3` con SDKs actualizados, generó un conflicto en build.gradle y se resolvió localmente conservando ambas necesidades. Regresión posterior al merge: 4.166 tests, 0 fallas/errores, 2 skips; 58 selectores aprobados. Merge commit `3a9542cdf` publicado, MERGEABLE y CI #5729 SUCCESS. Develop avanzó después a `dc56a3de4` con aislamiento de recursos de tests; se resolvió el nuevo conflicto del manifiesto conservando ambos grupos de pruebas, el aislamiento y el heap de 2 GB. Segunda regresión: 4.166 tests sin fallas/errores y 2 skips; 61 selectores aprobados. Merge `635f0f2c4` publicado, MERGEABLE; CI #5744 SUCCESS. LOCAL_STACK falla en la migración previa, con cleanup Docker verificado; no hubo F1 ni deploy. Review humana pendiente.

- **2026-10-01** — Se corrigieron los conflictos del PR #1228 mediante merge de `develop@f087e4b7c`; el manifiesto conserva los escenarios, tests y checks de ambas ramas. Se reprodujo `OutOfMemoryError: Java heap space` con el executor de 512 MiB y se configuró el heap de tests en 2 GiB. Regresión: 4.163 tests, 0 fallas/errores y 2 skips preexistentes; 50 selectores aprobados y validadores verdes. LOCAL_STACK falla en la migración preexistente de `component_type`, idéntica a develop; los checks dependientes no llegaron a ejecutarse y cleanup Docker quedó verificado. Commit `bec2648b7` subido y MERGEABLE; CI #5697, workflow, cobertura, dependencies y static-analyzer SUCCESS verificados en el mismo SHA. Cobertura global 94,75% y del PR 91,17%. GitHub conserva REVIEW_REQUIRED; dependencies aprueba con avisos de deprecación, el más próximo a 27 días. Sin merge del PR ni deploy; review de ownership pendiente.

- **2026-09-30 — Cierre de sesión** — Acceso GitHub recuperado; ambos comentarios respondidos y verificados por API. Punto 2 corregido en b0c5bf952; punto 1 tiene propuesta y sigue pendiente. Último HEAD Ready/MERGEABLE, workflow SUCCESS y CI IN_PROGRESS. Feedback y agent_run registrados; iniciativa continúa activa.


%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-28** — Proyecto creado a partir de SIG-600 y SIG-643. Se actualizó SIG-643 con precedencia de bloqueos, HTTP 409, resultado incierto de UI y coordinación de importaciones. Una edición no solicitada de SIG-600 fue revertida y se verificó que su contenido volvió a coincidir exactamente con la versión anterior. Sigue abierta la discrepancia entre ambas SPECs y el protocolo de las rutas de deploy. No se creó branch ni se modificó código.
- **2026-09-28** — SIG-643 actualizada: Playmaker autoriza el borrado con permiso Kraken o membresía ACME, tras Tiger y antes de los bloqueos; falta de permiso devuelve 403. El guard ACME duplicado del proxy BFF debe retirarse para admitir Kraken. SIG-600 no se editó. Quedan abiertos CA-1, la integración Java de Kraken y la concurrencia de deploys.
- **2026-09-29** — Se creó un worktree aislado de Playmaker y se implementó la autorización del `DELETE` con el SDK Java oficial de Kraken 5.0.0 o grants ACME del equipo dueño. Se configuró sandbox para test/test2/test3/local y producción por defecto; `compileJava` y `compileTestJava` pasaron sin ejecutar tests. Pendiente habilitar acceso de tráfico Fury, revisar la dependencia con el MCP de seguridad y alinear BFF/UI. SIG-600 no se editó.
- **2026-09-29** — La rama se rebasó sobre `develop` y se abrió el [PR draft #1228](https://github.com/melisource/fury_rio-playmaker/pull/1228). Pasaron 4.037 tests locales, los cinco tests focalizados y ambos validadores de contrato; el health check LOCAL_STACK no pudo arrancar por falta de Docker. El primer intento contra `master` fue rechazado por el workflow de Fury y se corrigió la base a `develop`. CI quedó verde y Fury terminó la [versión TEST `0.0.1-test-sig600-delete-auth`](https://web.furycloud.io/engineering/applications/rio-playmaker/versions/detail/0.0.1-test-sig600-delete-auth) del commit `73fabcfb9`; aún no se desplegó.

- **2026-09-30** — Se crearon tres ramas test3 derivadas del PR #1228 para NONE/ACME_ONLY/KRAKEN_ONLY. Regresión verde en cada una (4.056 tests, 0 fallas, 2 skips); test temporal estabilizado sin cambiar la lógica de borrado. Versiones finales verificadas en Fury como FINISHED, con tests habilitados y commit igual al HEAD remoto de cada rama; sin deploy. SIG-600 y SIG-643 no se editaron.

- **2026-09-30** — Se mejoró y publicó la descripción del PR #1228 usando human-first-technical-writing y el template del repo: tabla con tres versiones/capturas y pasos de prueba. Se resolvió el conflicto del manifiesto al sincronizar develop, se portó el arreglo del test temporal y se publicaron 4.093 tests locales sin fallas. Los cinco checks del HEAD 37dc1f2d3 pasaron; PR marcado Ready for review y MERGEABLE, con review humana pendiente. El stack MySQL local falló en una migración previa y se verificó cleanup. Texto canónico: [[Descripción PR — rio-playmaker]].

- **2026-09-30** — Descripción del PR #1228 traducida al español y reducida 53%, conservando las tres versiones/capturas y colapsando checklists. Comentario de ownership confirmado: DELETE autoriza un snapshot sin lock y UPDATE puede cambiar de equipo; corrección de concurrencia pendiente antes del merge. Sin cambios de código ni respuesta publicada al reviewer; Ready y cinco checks SUCCESS verificados en el mismo HEAD.

- **2026-09-30** — Se contrastaron los dos comentarios del PR #1228 contra HEAD 37dc1f2d3: carrera de ownership confirmada y falta de mock Kraken en integración confirmada. El verde previo no garantiza aislamiento; un test anterior deja grants ACME en el mock compartido sin reset, posible dependencia del orden. Pendientes coordinar ownership y aislar los providers con fixtures explícitos. Sin cambios de código ni comentarios publicados.

- **2026-09-30** — Punto 2 del review corregido y subido en b0c5bf952: SDK Kraken mock en integración, reset automático de ACME/Kraken y permisos explícitos por caso. Cinco DELETE pasan aislados, 78 tests en la clase completa y 4.098 de regresión sin fallas (2 skips); once selectores focalizados aprobados. Stack local bloqueado por migración previa, cleanup verificado. Resultado final del CI pendiente de verificación: GitHub bloquea la IP por allow list de melisource; último snapshot con workflow SUCCESS y CI IN_PROGRESS. Para el punto 1 se propuso coordinar locks de DELETE/ownership conservando 410; no se implementó.

## 🧭 Decisiones

- Playmaker es la autoridad de las reglas de borrado en el `DELETE`; no se diseña un endpoint `delete-validation`. Los blockers responden HTTP 409 con código específico y prevalece producción sobre infraestructura activa cuando aplican ambas. Fuente: [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643).
- Playmaker también es la autoridad de permisos para el borrado: Kraken `delete-data-products` o membresía ACME; 401 sin autenticación, 403 sin autorización, 503 cuando no se puede verificar. Fuente: [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643).
- Esta es una iniciativa humana (`owner: me`, `root: true`) de dos repos. La rama Playmaker parte de `origin/develop@c4ac43da4`; la rama frontend sigue pendiente.

## 🔗 Docs / Links

- [SIG-600 — funcional](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) · [SIG-643 — técnica](https://spellbook.adminml.com/projects/SIG/specs/SIG-643)
- Aplicaciones: [[rio-playmaker]], [[ads-signals-frontend]]; plataforma: [[RIO]].

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

_Sin ideas registradas._

### Motivos / principios

_Sin motivos adicionales._

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
_No aplica para esta iniciativa._
