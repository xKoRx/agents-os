---
type: project
schema_version: 1
owner: agent
root: false
status: review
priority: P1
area: "[[Meli]]"
parent: "[[Crear Context]]"
sprint:
start: "2026-08-25"
due:
progress: 100
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs:
aliases:
  - Code Review Context Playmaker
  - Remediacion code review context
  - Context code review
tags:
  - kind/project
  - area/meli
  - project/crear-context
  - application/rio-playmaker
created: "2026-08-25"
updated: "2026-09-03"
---

# Crear Context - Code Review Remediation

> [!info]+ Proyecto agente
> **Área:** [[Meli]] · **Estado:** review · **Prioridad:** P1 · **Parent:** [[Crear Context]]

## 🎯 Objetivo

Dejar `feature/new-component-context` de [[rio-playmaker]] impecable para PR, aplicando las correcciones del code review del 2026-08-25 y las decisiones que el owner tomó sobre ese review. El alcance es **remediación de la implementación existente**, no rediseño del contrato: el contrato v1 del Context queda como está en [[Crear Context]].

Tres ejes: **sacar la sobre-ingeniería** (presupuestos de bytes inventados, flag de outputs, constructores "backward" que solo usan los tests), **corregir lo que está mal** (fallback de ambiente hardcodeado, validaciones duplicadas, métricas que no distinguen causas) y **alinear la documentación** (CHANGELOG a `1.4.0`, SPEC SDD sin DT-27).

## 🚨 Decisiones del owner que gobiernan esta remediación

> [!danger]+ No reabrir
> Estas cuatro las tomó el owner el 2026-08-25 al revisar el code review. No se reabren dentro de este proyecto.

- **Los `outputs` se emiten SIEMPRE.** `rio.context.outputs.enabled` no fue una decisión del owner — lo introdujo un agente. Los valores sensibles ya vienen cifrados desde el control plane, así que Playmaker los reenvía sin gate. Esto **deroga DT-27 y T-18** de SIG-590.
- **El Context nunca se corta por tamaño.** El presupuesto de bytes se va completo. El contrato ya está acotado por records fijos; el único mapa abierto es `outputs`, y truncarlo rompe justo el caso que el Context existe para resolver: provisionar correctamente componentes/servicios en cada CP.
- **`OutputResolver` no lee configuración.** Sin flags, sin límites, sin `@Value`. Resuelve siempre.
- **Fail-open en una sola capa.** El Context es opcional hoy y obligatorio cuando todos los CP estén migrados; la guarda queda en un solo punto para que ese cambio sea de una línea.

## 📊 Estado actual

**Las 18 tareas aplicadas y verificadas (2026-08-25). Listo para revisión humana.**

**Suites:** Playmaker **3181 tests, 0 fallas, 2 skipped**; SDK **701 tests, 0 fallas** con `jacocoTestCoverageVerification` PASS. Cobertura de las clases del Context en Playmaker: `ComponentContextServiceImpl` 99% branch / 100% line, `ContextValueResolver` 100%/100%, `ContextMetrics` 100%/100%.

**Playmaker commiteado y pusheado.** Rama principal en `f49789d2c`; rama test integrada mediante merge en `ca120c20c`, preservando su logging exclusivo. Local y origin coinciden en ambas ramas. `0.0.5-component-context-test`, creada desde el commit test correcto, terminó en Fury con estado `FINISHED`.

**Versiones.** El SDK va en `0.0.6-component-context-null-safe` y Playmaker apunta ahí. La productiva sigue siendo `1.4.0`, que sale desde `master` después del merge del SDK — es lo que nombra el CHANGELOG de Playmaker.

**Falta sincronizar SIG-590 en Spellbook.** La copia SDD del repo está enmendada —DT-31, DT-32, DT-33, PT-11 y la nueva medición de tamaño— pero `.sdd/` está en `.gitignore` (línea 33) y no viaja en el PR.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] | `feature/new-component-context` | `develop` @ `0524ce49e` | `rio-playmaker` → `.sdd/features/new-component-context/1-functional/spec.md` (SIG-573) | `rio-playmaker` → `.sdd/features/new-component-context/2-technical/spec.md` (SIG-590) | Remediación en curso sobre `39f616c46` |
| [[rio-sdk-events]] | `feature/new-component-context` | `master` @ `9d86eb8` | ídem | ídem | **Sin cambios en esta remediación.** El contrato v1 no se toca; solo se lo nombra desde el CHANGELOG de Playmaker |

> [!note] Versión del SDK
> El CHANGELOG de Playmaker debe nombrar **`rio-sdk-events:1.4.0`**, que es la versión productiva que sale desde `master` una vez mergeado el PR del SDK. `build.gradle` **se queda en `0.0.4-component-context`** porque `1.4.0` todavía no existe, y porque la constitución (regla 14) y el perfil del owner prohíben fijar una versión productiva limpia desde una rama feature. El bump a `1.4.0` es gate de merge, no trabajo de esta rama.

## ✅ Tareas

> [!example]- Fuente de tareas
> Estados: `[ ]` To Do · `[/]` WIP · `[r]` Review · `[x]` Done · `[-]` Canceled.

- [x] **T-1 · CHANGELOG a `1.4.0`** — reescribir la entrada de `## [Unreleased]` para nombrar `rio-sdk-events:1.4.0`, sacar la mención al flag de outputs (ya no existe) y mover `### Added` antes de `### Changed`/`### Fixed` según Keep a Changelog #owner/agent #type/dev #area/meli
- [x] **T-2 · Sacar `rio.context.outputs.enabled`** — fuera el `@Value` de `OutputResolver`, fuera la clave de `application.yml`, fuera `SuppressionReason.DISABLED`. Los outputs se resuelven siempre #owner/agent #type/dev #area/meli
- [x] **T-3 · Sacar todo el conteo de bytes** — `maxContextBytes`, `fitContext`, `ContextTooLargeException`, `maxKeyBytes`, `maxTotalBytes`, el acumulador `totalBytes` y las cuatro claves de `application.yml`. `OutputResolver` queda con un solo colaborador: `ContextMetrics` #owner/agent #type/dev #area/meli
- [x] **T-4 · Fail-open en una sola capa** — sacar el `catch (Exception)` global de `ComponentContextServiceImpl.build`; `ComponentContextService.build` pasa a devolver `ComponentContext` (sin `Optional`, que hoy no transporta información) y a documentar que propaga; la única guarda queda en `BatchDispatchServiceImpl` #owner/agent #type/dev #area/meli
- [x] **T-5 · Volar el constructor backward de `BatchDispatchServiceImpl`** — con él se va el `@Autowired`, que solo existía para desambiguar entre dos constructores públicos. Actualizar los 5 usos en tests #owner/agent #type/dev #area/meli
- [x] **T-6 · Volar el constructor backward de `DispatchRequest`** — 37 líneas para una firma que solo usan 4 tests #owner/agent #type/dev #area/meli
- [x] **T-7 · `resolveEnvironment` sobre `EnvironmentType`** — reemplazar las constantes `"staging"`/`"test"` y el fallback bidireccional por el tipo canónico normalizado, que ya cubre `Test → Staging` y `Sandbox → Staging` #owner/agent #type/dev #area/meli
- [x] **T-8 · Ampliar el tipado de `SuppressionReason`** — hoy `NOT_AUTHORIZED` cubre tres causas distintas (no autorizado, sin ambiente equivalente, sin slot). Separarlas para que la métrica sirva en producción #owner/agent #type/dev #area/meli
- [x] **T-9 · Sacar validaciones duplicadas** — la exclusión de auto-relaciones que la query ya hace, el chequeo de `componentId == null` que `loadServices` ya filtró, y la guarda `isEmpty()` que el caller ya garantiza #owner/agent #type/dev #area/meli
- [x] **T-10 · Garantizar `type`/`name`/`version` no nulos** — los `@NotBlank` del contrato no los ejecuta ningún validador; que un CP que sí consume Context no reciba un `RelatedComponent` sin `type` #owner/agent #type/dev #area/meli
- [x] **T-11 · `ObjectMapper` inyectado** — `OutputResolver` usa el bean de Spring en vez de instanciarlo a mano #owner/agent #type/dev #area/meli
- [x] **T-12 · Batchear `findByDataProductId`** — hoy es una query por data product dentro de un `forEach`; el resto de la clase batchea todo #owner/agent #type/dev #area/meli
- [x] **T-13 · Tests** — cubrir la guarda de cadena de imports (`original.getSourceComponentId() != null`, hoy sin ningún test), arreglar el test de `OutputResolver` mal nombrado, y ajustar toda la suite a los cambios anteriores. Criterio: primero funcionalidad crítica, después coverage hasta ≥90% #owner/agent #type/dev #area/meli
- [x] **T-14 · SPEC SDD** — derogar DT-27 en `2-technical/spec.md` y T-18 en `3-tasks/tasks.md`; revisar RF-8 del funcional. SIG-590 en Spellbook queda como sincronización pendiente #owner/agent #type/dev #area/meli
- [x] **T-15 · Perfil del owner** — agregar la regla de construcción de tests (funcionalidad crítica primero, coverage ≥90% después) a `rjara-agent-profile.md`, con su `change_log` #owner/agent #type/admin #area/meli
- [x] **T-16 · Verificación final** — suite completa verde, jacoco ≥90% en las clases tocadas, `git status` limpio de daño colateral (`docs/specs/swagger.yaml` se ensucia solo) #owner/agent #type/dev #area/meli
- [x] **T-17 · Poblar `inputs` (T-24 de SIG-590)** — `LastDeployedVersion.inputs` desde `deployment.componentDefinition.parameters` del mismo deployment; `RelatedComponent.inputs` desde `service.componentDefinition.parameters` del mismo slot que aporta los outputs. `OutputResolver` pasa a `ContextValueResolver` con `resolveInputs`/`resolveOutputs` #owner/agent #type/dev #area/meli
- [x] **T-18 · Normalización pareja de contenedores (SDK)** — las cuatro listas/mapas del contrato normalizan ausente a vacío. Antes `inputs` toleraba `null` y `outputs`/`sources`/`destinations` tiraban NPE; el que pagaba era el consumidor, que reventaba al deserializar un payload sin la clave #owner/agent #type/dev #area/meli
- [x] **T-19 · Imports correctos en el camino v1** — hidratar el ambiente stub y cargar originales, ambientes y slots importados en batches, conservando topología con mapas vacíos cuando falta un original o slot #owner/agent #type/dev #area/meli
- [x] **T-20 · Cierre de Zord** — preservar filas legacy con `LEFT JOIN`, mover la métrica de derivación al boundary de construcción, limitar catches de serialización a Jackson y aplicar simplificaciones menores verificadas #owner/agent #type/dev #area/meli

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

- **2026-09-03 (2)** — Remediación final commiteada y pusheada en `feature/new-component-context @ f49789d2c`; mergeada y pusheada a `feature/new-component-context-test @ ca120c20c`. La rama test preserva el full-trigger logging y pasó `clean test jacocoTestCoverageVerification jacocoTestReport`: 3574 tests, 0 fallas, 2 skipped. El bloqueo anterior correspondía a la VPN corporativa GlobalProtect de MELI, no a `Aranea`; una vez disponible, ambos pushes quedaron verificados comparando HEAD local con `ls-remote`. Fury creó `0.0.5-component-context-test` desde `ca120c20c` y terminó en estado `FINISHED`.
- **2026-09-03** — Revalidación después del smoke funcional y de una auditoría Luna High de los 12 comentarios de David. Apareció un gap material en `createSingle`: el `EnvironmentModel` llegaba sólo con id, por lo que el Context importado podía resolver el nombre como null; ahora se hidrata desde repository. La carga de imports se convirtió en tres consultas batch —originales, ambientes y slots— con `LEFT JOIN FETCH`, y se cubrieron original ausente, ambiente equivalente ausente, varios imports y fila legacy sin `component_id`. Zord ejecutó siete revisores con Claude sobre el estado efectivo: **security sin findings**, sin revisión humana requerida, critical ni high. Queda como deuda el N+1 entre componentes del mismo batch; es anterior como patrón en los resolvers de placeholders y el Context agregó su propia capa desde el 2026-08-19. La solución correcta es un snapshot/DataLoader por batch y no se incorpora en esta remediación. Gate final: 3574 tests, 0 fallas, 0 errores, 2 skipped, JaCoCo PASS; `ComponentContextService` 99,6% line / 96,2% branch. El delta queda local, sin commit ni push.

- **2026-08-25 (3)** — **Normalización pareja de contenedores en el contrato del SDK (DT-33).** El owner detectó la asimetría: `inputs` toleraba `null` y lo normalizaba a `{}`, mientras `outputs`, `sources` y `destinations` tiraban `NullPointerException` vía `Objects.requireNonNull`. Era un accidente de dos pasadas de escritura, no una decisión. **Dónde dolía:** no en Playmaker —el fail-open del borde de dispatch absorbe la excepción y el deploy sigue— sino **en el consumidor**: un CP que recibiera un `RelatedComponent` sin la clave `outputs` reventaba dentro del constructor del record, al deserializar, antes de llegar a su propio código. Justo el escenario del rollout, con mensajes viajando mientras los CP se suman de a poco. Ahora los cuatro contenedores hacen `x == null ? vacío : copyOf(x)`. Los `@NotNull` de listas y mapas se conservan: documentan el contrato de wire y el constructor los garantiza, así que no pueden fallar. **Lo que sigue rechazando `null` a propósito:** un elemento null dentro de una lista —`List.copyOf` lo rechaza— porque eso es un payload corrupto y no un campo ausente; y `ComponentContext.dataProduct`/`.component`, que no tienen valor vacío razonable y los atrapa el `Validator` de Playmaker antes de publicar. SDK en `0.0.6-component-context-null-safe`; 701 tests y gate de cobertura PASS.
- **2026-08-25 (4)** — **Verificado a pedido del owner: el Context se genera en todos los batches, no sólo en el primero.** `safelyBuildContext` vive dentro de `dispatchItem`, que corre por cada ítem de cada llamada a `dispatchBatch`, y `dispatchBatch` es el único punto de entrada de los tres caminos de dispatch: primer batch (`DeploymentGroupServiceImpl:108`), batches siguientes (`OrchestrationServiceImpl:110`) y el camino v1 de componente único (`:156`). `DeploymentOrchestrationIntegrationTest` lo prueba sobre el **segundo** batch —`component1` tiene `runOrder(1)` y lo despacha `checkPrerequisites`—, que es el caso más fuerte. Consecuencia de diseño que conviene tener presente: el batch N recibe un Context **más rico** que el batch N−1, porque para cuando se despacha, los componentes del batch anterior ya desplegaron y el CP escribió sus outputs. Es la "Dependencia de orden" que ya documenta [[Crear Context]], y es deseable, no un efecto colateral.

- **2026-08-25 (2)** — **`inputs` separado de `outputs`, implementado en Playmaker (T-24 de SIG-590).** El owner amplió el contrato del SDK: `LastDeployedVersion` y `RelatedComponent` llevan ahora `inputs` —configuración del usuario, desde `component_definition.parameters`— además de `outputs` —resultados del CP, desde `_values`—. Tres decisiones de implementación: **(1)** `OutputResolver` pasó a `ContextValueResolver` con `resolveInputs`/`resolveOutputs`, porque la única diferencia entre los dos es desenvolver o no el envelope `{type,value,sensitive}` y duplicar 35 líneas de parseo para cambiar una condición no compra nada (DT-31); **(2)** `resolveSlot` devuelve el `ServiceModel` y los dos mapas salen de ahí, así que la estructura —y no una convención— garantiza que nunca se publique la configuración de una entidad junto a los resultados de otra (DT-32); **(3)** los inputs **no** desenvuelven el envelope: una clave de configuración con un campo `value` es data del usuario y colapsarla borraría sus hermanos. **Hallazgo:** `build.gradle` apuntaba a una versión de SDK inexistente (`0.0.5-component-context` en vez de `0.0.5-component-context-inputs`), corregido. **Revisión de sensibilidad de DT-30:** no hay ninguna clave sensible declarada en código ni fixtures, pero `parameters` es JSON libre del usuario, así que es un negativo débil y quedó escrito como tal en la spec. **Nueva medición de tamaño:** el payload duplica —2,9 KB el caso típico, 17,5 KB un pipeline de 8+8 vecinos—; sigue marginal, y el tope real de BigQueue quedó como PT-11.

- **2026-08-25** — **Remediación completa, suite verde, lista para revisión.** Las 16 tareas aplicadas en una pasada. Lo que se fue: el flag `rio.context.outputs.enabled`, los cuatro presupuestos de bytes con sus tres constantes inventadas, `fitContext` y su `ContextTooLargeException`, los dos constructores "backward" que sólo usaban los tests (con el `@Autowired` que uno de ellos había forzado), tres validaciones que el camino ya garantizaba y dos guardas null inalcanzables en `resolveValue`. Lo que entró: validación real del contrato con un `Validator` —las anotaciones `@NotBlank` del SDK eran decorativas—, `SuppressionReason` con `NO_ENVIRONMENT` separado de `NOT_AUTHORIZED` y `NO_SLOT`, `EnvironmentType` como única fuente de equivalencia de ambientes, y `findByDataProductIdIn` para matar el N+1. **Dos hallazgos nuevos durante la implementación:** (1) `DeploymentGroupServiceImpl.createSingle` arma un `EnvironmentModel` stub con sólo el `id`, así que el `name` y el `type` del ambiente destino llegan en null por el camino v1 de dispatch — el matching de ambiente ahora lee la fila por id (Q8) en vez de confiar en el objeto del caller; (2) ese mismo stub hace que `DispatchRequest.environmentName` viaje null por ese camino, lo cual es **preexistente y ajeno al Context**, queda anotado sin tocar. `.sdd/` está gitignoreado, así que las enmiendas a SIG-590 son locales: sincronizarlas en Spellbook queda pendiente.

- **2026-08-25** — Proyecto creado. Origen: code review completo de `feature/new-component-context` pedido por el owner, con suites corridas (3176 tests / 0 fallas) y jacoco medido. El review salió **BLOQUEADO** por un solo motivo real —el SDK `0.0.4-component-context` no resolvía desde Fury— que resultó ser falta de VPN, no un problema de la rama. De los 13 findings, el owner aceptó 12, **corrigió uno mío** (el unwrap de `{value: …}` en `OutputResolver` es correcto y deliberado: el wrapper `{type,value,sensitive}` sí existe en `service.values` y desenvolverlo replica `ParameterParseServiceImpl:280-281`) y **amplió dos** hacia decisiones de diseño que el review no había propuesto: sacar el flag de outputs y sacar el presupuesto de bytes completo. Las cuatro decisiones del owner quedan arriba.

## 🧭 Decisiones

- **`build()` propaga en vez de devolver `Optional`.** Al mover el fail-open al borde del dispatch, el `Optional` dejó de transportar información: todos los caminos de éxito devolvían un valor presente y el único `empty()` era el de fallo. El contrato quedó "devuelve el Context o tira", y la política de si un deploy puede seguir sin Context vive completa en `BatchDispatchServiceImpl.safelyBuildContext`.
- **Los `@NotBlank` se ejecutan, no se replican.** En vez de agregar guardas ad-hoc para `type`, `name` y `version`, se valida el objeto derivado con un `Validator`, siguiendo el precedente que ya existe en `ComponentRuntimeStatusConsumerServiceImpl`. Una violación es un fallo de derivación y cae en el mismo fail-open. El mensaje sólo lleva el path y el template de la violación, nunca el valor.
- **La degradación por vecino se conserva.** Es una política distinta del fail-open global: que un `_values` corrupto de un vecino borre la topología de todos los demás sería peor que publicar ese vecino con `outputs` vacío. Una capa de fail-open global, más una degradación parcial por vecino que el contrato ya documenta.

- **El presupuesto de bytes no tenía respaldo.** Grepeé `262144`, `65536`, `4096` y `max-bytes` en toda la carpeta `.sdd/` de la feature: cero apariciones. No salían de SIG-590 ni de un límite de plataforma. Eran tres potencias de dos elegidas a ojo por la implementación.
- **El impacto de tamaño no justifica un cap.** Medición de la serialización real del contrato: topología sola (2+2 vecinos, sin outputs) 576 B; típico (2+2 vecinos, 4 outputs de 40 B) 1,7 KB; pipeline grande (8+8 vecinos, 6 outputs de 60 B) 9,5 KB. Contra un mensaje que ya carga `params` completo, es marginal. **Pendiente de confirmar:** el tope real de mensaje de BigQueue en la plataforma; no fue verificable en la sesión del review.
- **`Optional` en `build()` no transporta información.** Todos los caminos de éxito devuelven un `Optional` presente; el único `empty()` es el de fallo. Al mover el fail-open al caller, `Optional` deja de tener sentido y el contrato se vuelve "devuelve el Context o tira".
- **El `@Autowired` era un síntoma.** Spring auto-cablea el constructor cuando hay uno solo; el segundo constructor público obligó a desambiguar. Se va con él.

## 🔗 Docs / Links

- [[Crear Context]] — proyecto padre: contrato v1 vigente, specs, orden de merge y estado de las dos ramas.
- [[signals-code-review]] — protocolo con el que se hizo el review que originó este proyecto.
- [[rio-playmaker]] · [[rio-sdk-events]]
