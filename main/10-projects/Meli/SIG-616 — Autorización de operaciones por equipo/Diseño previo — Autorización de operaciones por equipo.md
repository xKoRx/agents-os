---
type: doc
schema_version: 1
status: archived
area: "[[Meli]]"
related:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
aliases:
  - Diseño autorización por equipo
  - Diseño previo SIG-616
tags:
  - kind/doc
  - project/sig-616
created: "2026-09-14"
updated: "2026-09-21"
---

# Diseño previo: autorización de operaciones por equipo

**Estado:** archivado y reemplazado · **Proyecto:** [[SIG-616 — Autorización de operaciones por equipo]] · **SPEC vigente:** [[SPEC técnica — Slice 2 — Actions mutantes de Signals]]

> [!danger] Documento histórico; no usar para implementación
> Este diseño contiene hipótesis descartadas, incluidas reglas para imports, precreation y default-deny. La fuente de verdad vigente es [[SIG-616 — Autorización de operaciones por equipo]] y la SPEC publicada [SIG-623](https://spellbook.adminml.com/projects/SIG/specs/SIG-623): la autorización es aditiva y un par no configurado conserva su comportamiento previo.

## 1. Resultado de diseño actual

La autorización de operaciones se construirá como una capacidad server-side de `rio-playmaker`, con Tiger como fuente de identidad, `DataProduct.teamName` como ownership persistido y ACME como fuente de roles. Playmaker será el enforcement point antes de cualquier side effect; los Control Planes no resolverán Tiger ni ACME.

La solución se desarrollará de manera incremental. El único cambio funcional de la primera entrega será proteger las Actions mutantes de Signals sobre componentes existentes: `catalog-signal + start` y `catalog-signal + stop`. Como trabajo fundacional sin cambio funcional, la autorización de delete/inactivate ya mergeada se migrará al mismo autorizador y será el primer consumidor de regresión. Kafka, Flink, ClickHouse, endpoints legacy, Actions de precreación, polling, deployments y otras mutaciones quedan sin cambios.

La primera etapa conservará un único middleware HTTP: `TigerAuthenticationFilter`, responsable de validar Tiger una sola vez y publicar el username en el `SecurityContext`.

ACME no se implementará como middleware. Después de resolver el recurso persistido, cada caso de uso invocará un autorizador concreto y reutilizable indicando `username`, `teamName`, `projectCode` y nivel requerido. Ese componente encapsulará el cliente ACME, la lista de roles y la traducción de errores. Los handlers no conocerán la autorización y los services consumidores no implementarán llamadas ni reglas ACME por su cuenta. `ActionServiceImpl` ejecutará esta única validación antes de cualquier side effect.

No se introducirá en esta etapa una jerarquía de interfaces, un catálogo abierto de capabilities, un Aspect ni `@RequiresCapability`. Sólo existirán los tres niveles funcionales cerrados: `READ`, `DEV_AND_UP` y `DEPLOYER_AND_UP`. La annotation se evaluará al final del proyecto, cuando existan varios casos implementados y se pueda abstraer sobre repetición real.

## 2. Problema funcional transversal

Playmaker expone operaciones que crean, modifican, despliegan, inactivan o eliminan recursos. La autenticación Tiger existente prueba quién realiza la solicitud, pero no garantiza por sí sola que esa persona tenga permiso para operar recursos cuyo dueño es otro equipo.

La política funcional transversal descrita por SIG-616 se apoya en tres datos:

- Identidad validada mediante Tiger.
- Equipo dueño obtenido de estado persistido en Playmaker, principalmente `DataProduct.teamName`.
- Rol o grant obtenido desde ACME para la identidad y el equipo dueño.

El objetivo no es que cada flujo implemente su propia integración con Tiger y ACME. El objetivo es tener una frontera de seguridad consistente, extensible por etapas y aplicada antes de locks, persistencia, publicación de eventos o llamadas a Control Planes.

## 3. Principios de diseño

- **KISS.** La primera entrega agrega sólo lo necesario para proteger `catalog-signal + start/stop`.
- **YAGNI.** No se implementan legacy, otros tipos, un motor de políticas, annotations ni generalizaciones sin consumidores actuales.
- **SOLID pragmático.** Autenticación, decisión de aplicabilidad y verificación ACME tienen responsabilidades distintas, pero no se crean interfaces o capas sin una segunda implementación real.
- **Default deny dentro del alcance protegido.** Una Action desconocida sobre `catalog-signal` se rechaza; nunca se presume que es de lectura.
- **Estado persistido sobre input del cliente.** En Actions sobre un componente existente, el tipo y el equipo salen del componente y Data Product persistidos.
- **Autorización antes de efectos.** Una solicitud rechazada no crea una entrada KVS, no toma locks, no publica BigQueue y no invoca un Control Plane.
- **Evolución por verticales.** Cada dominio adopta la capacidad mediante su propia SPEC técnica después de que su comportamiento funcional esté cerrado.

## 4. Alcance por etapas

| Etapa | Alcance | Estado de diseño |
|---|---|---|
| 1 | Fundación: middleware Tiger, extracción del autorizador ACME, migración sin cambio funcional de delete/inactivate e integración con `catalog-signal + start/stop` | Primera SPEC técnica a crear; delta funcional sólo en Signals |
| 2 | Deployments y demás mutaciones de componentes | Futuro; requiere análisis y SPEC técnica propia |
| 3 | Relaciones y pipelines | Futuro; requiere resolver casos cross-DP y legacy |
| 4 | Actions de otras tecnologías y endpoints legacy | Futuro; se incorporan sólo mediante whitelist y SPEC aprobada |
| Final | Evaluar `@RequiresCapability` sobre casos de uso ya consolidados | Evolución documentada; fuera del alcance inicial |

La arquitectura puede escalar a legacy, pero legacy no se contempla en el diseño técnico ni en las tasks de la primera entrega.

### 4.1 Niveles de acceso definitivos

| Nivel | Roles | Uso |
|---|---|---|
| `READ` | Cualquier identidad Tiger válida | Actions declaradas de lectura; no consulta ACME |
| `DEV_AND_UP` | `admin`, `maintainer`, `deployer`, `committer` | Escrituras y mutaciones definidas por SIG-616, incluidas Actions mutantes de Signals |
| `DEPLOYER_AND_UP` | `admin`, `maintainer`, `deployer` | Delete e inactivate cubiertos por el PR 1126 |

No existe contradicción entre SIG-616 y el PR 1126: son dos políticas para sensibilidades distintas. No se agregarán más niveles sin un caso funcional nuevo.

## 5. Reglas funcionales preservadas

### 5.1 Actions de lectura

La SPEC declara que Kafka y otras read Actions requieren una identidad Tiger válida, no autorización ACME por equipo. Esta implementación no cambia esa regla ni introduce restricciones adicionales.

Las read Actions de Kafka o ClickHouse están fuera de la primera entrega y continúan con el comportamiento actual. La observación de que algunas pueden devolver datos sensibles es válida como riesgo de seguridad, pero modificar su acceso sería un requerimiento funcional nuevo y debe discutirse fuera de esta implementación.

### 5.2 Actions mutantes

Para la primera entrega sólo se reconocen como Actions protegidas:

| `component_type` persistido | `actionName` | Clasificación | Requisito |
|---|---|---|---|
| `catalog-signal` | `start` | Mutación operacional | Tiger válido + rol ACME permitido en el equipo dueño |
| `catalog-signal` | `stop` | Mutación operacional | Tiger válido + rol ACME permitido en el equipo dueño |

Signals `start/stop` requiere `DEV_AND_UP`: `admin`, `maintainer`, `deployer` o `committer` en el scope dueño persistido.

Una combinación desconocida para `catalog-signal` se rechaza. Una Action de otra tecnología queda fuera de la validación ACME y mantiene su comportamiento actual hasta que una SPEC posterior la incorpore.

### 5.3 Componentes importados

Un componente con `sourceComponentId` no nulo es una copia importada. La importación no transfiere ownership ni permiso para ejecutar una mutación operacional. `start/stop` sobre un `catalog-signal` importado se rechaza antes de consultar ACME y antes de cualquier side effect.

### 5.4 Precreación

Las Actions mutantes de Signals requieren un componente persistido y una relación comprobable con el Data Product. El endpoint de precreación no forma parte de la primera entrega. Si recibe `catalog-signal + start/stop`, el comportamiento definitivo debe ser rechazo explícito; no se habilitará como efecto colateral de esta implementación.

### 5.5 Polling

SIG-616 no define una política nueva de visibilidad para resultados. No se agregará `resultVisibility`, no se modificará `ActionKvsEntry` y no se reclasificarán permisos durante el polling.

Antes de cerrar la SPEC técnica se verificará si alguna read Action asíncrona depende de `GET /v2/actions/{actionId}` y si el control actual de `ActionServiceImpl.authorizeActionResultAccess` contradice la regla funcional de Tiger-only. Si no existe contradicción en los flujos reales, polling queda completamente fuera de alcance. Si existe, se documentará como problema separado y no se resolverá mediante una política genérica de resultados dentro de la vertical Signals.

## 6. Estado técnico actual de Tiger

`CustomAuthorizationFilter` ya intercepta las rutas protegidas y llama a `TigerTokenService.getAuthToken(headers)`. Ese método usa `TigerTokenValidation.getClaims(headers)` y devuelve el username validado.

El filtro actual descarta el username y guarda el Tiger token crudo como principal en `CustomAuthenticationToken`. Controllers y services vuelven a llamar `tigerTokenService.getAuthToken(headers)` para recuperar la identidad. El relevamiento encontró 67 call sites en código de producción; Actions vuelve a hacerlo en los caminos component-bound, precreation y polling.

Problemas observados:

- La identidad se valida o parsea repetidamente.
- El `SecurityContext` contiene el token crudo en lugar del username.
- La responsabilidad de autenticación aparece en controllers y services.
- El filtro puede registrar el token crudo en un error.
- Una excepción Tiger originada dentro del filtro no pasa por el `ControllerExceptionHandler`; debe garantizarse explícitamente que termina en `401` y no en un error genérico.
- Las rutas públicas están declaradas tanto en `SecurityConfig` como en `CustomAuthorizationFilter`; cualquier cambio debe evitar agregar una tercera fuente de configuración.

### 6.1 Estado objetivo incremental

El filtro conservará el username que ya obtuvo y construirá un `Authentication` cuyo principal sea ese username. El token no se expondrá como principal ni se registrará en logs.

```java
String username = tigerTokenService.getAuthToken(headers);
SecurityContextHolder.getContext().setAuthentication(new CustomAuthenticationToken(username));
```

Actions comenzará a consumir `authentication.getName()` o el principal equivalente. No se migrarán en masa los demás call sites de Tiger dentro de la primera entrega; cada flujo se migrará al adoptar la nueva autorización o mediante una iniciativa específica.

## 7. Autorización ACME después de resolver el target

Tiger y ACME no son dos middlewares simétricos:

- Tiger responde una pregunta independiente del dominio: quién es el caller.
- ACME sólo permite decidir si el caller puede operar cuando ya se conocen el equipo y proyecto dueños.

El cliente ofrece `getUserGrants(username, headers)`, pero el commit `7737f053d` documenta que `/grants/user-grants/{username}` no incluye los roles de `OwnerProjectGrant`. La consulta precisa disponible es `getOwnerProjectGrants(username, teamName, headers)`; `projectCode` no se envía a ACME y se compara localmente contra el resultado.

Por esta limitación, ACME no se implementará como middleware ni se precargará en el contexto HTTP. La unidad reutilizable será un autorizador concreto, sin interfaz adicional en esta etapa, que recibe el caller, el scope persistido y el nivel requerido.

### 7.1 Ruta incorporada en la primera vertical

La primera integración se aplicará dentro del caso de uso servido por:

```text
POST /data-products/{dataProductId}/components/{componentId}/environments/{environmentId}/actions/{actionName}
```

No se incorporará ACME en:

- `POST /data-products/{dataProductId}/actions/{actionName}` de precreación.
- `GET /v2/actions/{actionId}` de polling.
- `/services/{serviceId}/actions/**` legacy.
- `/signals/**`, que corresponde a APIs públicas de productores y no al dispatch genérico de Actions.

### 7.2 Algoritmo de la primera integración

1. Tiger valida la request una sola vez y publica el username en `SecurityContext`.
2. `ActionServiceImpl` resuelve Data Product, componente y environment persistidos como parte de su flujo normal.
3. Si el `componentTemplateCode` no es `catalog-signal`, continúa sin alterar el comportamiento actual.
4. Si es `catalog-signal` y `actionName` no pertenece a `start/stop`, rechaza.
5. Si `sourceComponentId` no es nulo, rechaza por ser componente importado.
6. Antes de cargar contexto de deployment, escribir KVS o publicar BigQueue, invoca una única validación reutilizable con `username`, `teamName`, `projectCode`, headers Tiger y `DEV_AND_UP`.
7. El autorizador llama `getOwnerProjectGrants(username, teamName, headers)`, exige match exacto de `teamName + projectCode` y evalúa el nivel.
8. Sólo después de allow continúan los side effects.

El service consumidor conoce que su operación requiere autorización y aporta el target ya resuelto, pero no contiene listas de roles, parsing de grants, endpoints ACME ni traducción de errores.

### 7.3 Dónde se obtiene el scope

El ownership no vive en `ServiceModel`: vive en el `DataProductModel`. Los distintos flujos llegan al mismo scope navegando desde su recurso objetivo hacia el Data Product dueño.

En la primera vertical, la ruta component-bound contiene `dataProductId`, `componentId` y `environmentId`. `ActionServiceImpl.fetchComponentInHierarchy` ya comprueba que los tres recursos pertenezcan al mismo Data Product. De ese `DataProductModel` salen `teamName` y `projectCode`; del componente salen `componentTemplateCode` y `sourceComponentId`.

Para Data Products modernos bajo la política SIG-616, `teamName` y `projectCode` forman el scope obligatorio. Ambos campos pueden faltar en datos históricos. En una operación protegida, scope incompleto implica rechazo fail-closed. Los caminos legacy quedan excluidos por entrypoint en la primera etapa, no mediante un fallback permisivo cuando falte ownership.

### 7.4 Errores

- Tiger ausente o inválido: `401` desde la frontera HTTP.
- Recurso persistido inexistente o inconsistente: `404` o error funcional equivalente antes de ACME.
- Scope dueño incompleto en una operación protegida: rechazo fail-closed.
- ACME disponible pero rol insuficiente para `teamName + projectCode`: `403`.
- ACME no disponible o no verificable: `503`.

### 7.5 Invariante del caso de uso

La autorización vive en la frontera del caso de uso, no exclusivamente en el controller. Así, cualquier llamador futuro de `ActionService.triggerAction` atraviesa la misma validación. La prueba relevante debe demostrar que ninguna ejecución protegida alcanza KVS o BigQueue sin pasar por el autorizador.

## 8. Integración con PR 1126

El [PR 1126 de rio-playmaker](https://github.com/melisource/fury_rio-playmaker/pull/1126) ya está mergeado en `origin/develop` mediante `1a4caf093`. Agrega autorización ACME para inactivate/delete y es la base técnica de esta iniciativa.

### 8.1 Elementos reutilizables

- `AcmeClient.getOwnerProjectGrants(username, teamName, headers)` consulta los grants del usuario acotados al equipo dueño.
- La implementación pagina respuestas, normaliza roles conocidos y selecciona el rol de mayor privilegio.
- La política actual reconoce `admin`, `maintainer` y `deployer` para operaciones destructivas.
- La versión final valida además que el grant corresponda al `projectCode` persistido del Data Product.
- La verificación se ejecuta antes de locks y side effects.
- Las pruebas cubren roles insuficientes, grants de otro equipo, roles faltantes y errores de ACME.

### 8.2 Refactor requerido

No se adoptará como API transversal `PipelineAuthorizationService.assertAdminAccess`, porque está acoplada a pipelines, mezcla Data Product, headers, caller y texto de acción, y su nombre no representa que `deployer` también está autorizado.

Tampoco se mantendrá la política definitiva dentro de métodos estáticos de `AuthorizationUtils`. Lo implementado en el PR se refactorizará gradualmente para que Tiger, consulta ACME, política de roles y adaptación de errores tengan un único ownership técnico reutilizable por los casos que se vayan incorporando.

Ese refactor no significa construir desde ahora un framework genérico. La unidad común será un scope persistido `teamName + projectCode` y uno de los dos niveles ACME (`DEV_AND_UP` o `DEPLOYER_AND_UP`). Primero se extraerá el comportamiento existente de `PipelineAuthorizationService.assertAdminAccess` y `AuthorizationUtils.requireDeployerOrAbove` hacia una única clase concreta. `PipelineComponentDeleteServiceImpl` y `ComponentInactivationServiceImpl` pasarán a consumirla conservando `DEPLOYER_AND_UP`; luego `ActionServiceImpl` será el primer consumidor funcional nuevo con `DEV_AND_UP`.

### 8.3 Diferenciación de errores

El PR convierte tanto falta de permisos como caída de ACME en `SecurityException`. La solución final debe conservar fail-closed, pero distinguir:

| Condición | Respuesta esperada |
|---|---|
| Tiger ausente o inválido | `401 Unauthorized` |
| Recurso persistido inexistente | `404 Not Found` |
| Identidad válida sin rol suficiente | `403 Forbidden` |
| Action Signals desconocida o importada | `403 Forbidden` o error funcional equivalente definido por la SPEC |
| ACME no disponible o no verificable | `503 Service Unavailable` |

En cualquier error no se ejecuta el controller ni existen side effects. Los mensajes no exponen miembros del equipo, grants, tokens o detalles sensibles de ACME.

## 9. Flujo objetivo de la primera vertical

```text
[MODIFIED] SecurityConfig / CustomAuthorizationFilter
    |
    | valida Tiger una vez
    | principal = username
    v
[UNCHANGED] ActionController
    v
[MODIFIED] ActionServiceImpl
    |
    | resuelve DP + componente persistidos
    | whitelist catalog-signal + start/stop
    | rechaza importados
    v
[NEW] OperationAuthorizationService (clase concreta)
    |
    | getOwnerProjectGrants(username, teamName, headers)
    | valida projectCode + DEV_AND_UP
    | retorna antes de cualquier efecto
    v
[MODIFIED] ActionServiceImpl
    |
    | sólo después guarda KVS y publica
    v
[UNCHANGED] Control Plane de Signals
```

Los cambios exactos de clases, paquetes y métodos se fijarán en la SPEC técnica después de validar el diseño contra la branch base limpia y contra el estado final del PR 1126.

## 10. Casos que deben analizarse antes de congelar el diseño

### 10.1 Identidad y transporte

- Confirmar el comportamiento HTTP real del filtro ante Tiger ausente, inválido y expirado.
- Confirmar que las rutas de Actions component-bound no están dentro de ningún matcher público.
- Confirmar que el username de Tiger es el mismo identificador esperado por `getOwnerProjectGrants`.
- Confirmar cómo se propaga el Tiger token hacia ACME sin volver a validarlo.
- Confirmar que ninguna información del token se registra en logs o errores.

### 10.2 Ownership y recurso

- Confirmar la query canónica para obtener un componente dentro de un Data Product.
- Confirmar que `DataProduct.teamName` y `DataProduct.projectCode` están completos en los componentes Signals modernos vigentes.
- Confirmar `DataProduct.projectCode` como segunda dimensión obligatoria del scope, alineada con el código mergeado del PR 1126.
- Definir el error cuando `teamName` es nulo o vacío.
- Confirmar que `systemId` no es requisito artificial si la consulta ACME utiliza `teamName`.
- Confirmar el tratamiento de un componente importado y la semántica exacta de `sourceComponentId`.
- Mantener la autorización dentro del caso de uso y antes del primer efecto para minimizar el intervalo entre lectura del ownership y ejecución.

### 10.3 Actions de Signals

- Confirmar con el Control Plane que los únicos nombres vigentes son `start` y `stop`.
- Confirmar que `catalog-signal` es el único component template soportado.
- Confirmar que ambas son siempre mutaciones y nunca tienen variante de lectura.
- Confirmar que no existe uso legítimo de `start/stop` mediante precreación.
- Confirmar que no existe otro llamador productivo de `ActionService.triggerAction` fuera de `ActionController`.
- Confirmar los roles ACME exactos: `admin`, `maintainer`, `deployer` u otro conjunto.

### 10.4 Compatibilidad

- Verificar que tecnologías distintas de Signals atraviesan el mismo caso de uso sin cambios funcionales ni llamadas ACME.
- Verificar que read Actions continúan requiriendo sólo Tiger donde la SPEC lo declara.
- Verificar que polling no cambia y documentar cualquier contradicción preexistente por separado.
- Verificar que callbacks `/events/actions/**` continúan públicos y fuera de Tiger/ACME.
- Verificar el comportamiento durante el despliegue si existen instancias con versiones distintas; no debe existir un intervalo default-allow para Signals.
- No usar `getUserGrants(username, headers)` para resolver roles `OwnerProjectGrant`: el historial del cliente documenta que ese endpoint no entrega el rol necesario. Reutilizar la consulta precisa del PR 1126 una vez resuelto el team.
- Incorporar `POST /data-products/{name}/environments/{envName}/pipeline/deploy` al inventario de mutaciones aunque haya sido omitido en la lista de rutas de la SPEC original.
- Identificar como legacy las rutas expuestas por controllers `@Deprecated` y reemplazadas explícitamente por RFC-002; excluirlas mediante allow-list de rutas modernas, no mediante inferencia por nombre.
- Tratar cualquier ruta legacy que permita la misma mutación como bypass potencial antes del rollout: debe existir evidencia de retiro, ausencia de tráfico o una decisión explícita de protección posterior.

### 10.5 Operación

- Definir métricas de allow/deny/error ACME por operación sin cardinalidad insegura.
- Definir timeout y tratamiento de errores usando el cliente ACME del PR 1126.
- Confirmar si se necesita un feature flag de rollout; si existe, apagado no puede significar bypass silencioso una vez activada la política en producción.
- Confirmar que un rechazo no crea KVS ni publica BigQueue mediante pruebas de integración.

## 11. Estrategia SDD

### 11.1 SPEC funcional

La SPEC SIG-616 actual contiene objetivo, reglas de negocio, matriz de operaciones y criterios de aceptación propios de una SPEC funcional, aunque en Spellbook figura como `technical`. Antes de implementar se debe decidir una de estas rutas:

1. Reclasificar SIG-616 como funcional y crear una técnica hija para Actions Signals.
2. Crear una SPEC funcional padre nueva y relacionar SIG-616 correctamente, si Spellbook no permite o no conviene reclasificarla.

La funcional debe ser dueña de:

- Qué operaciones son read y cuáles son mutaciones.
- Qué roles habilitan cada mutación.
- Qué sucede con componentes importados.
- Qué caminos y tecnologías están incluidos.
- Criterios de aceptación y escenarios E2E.

### 11.2 Primera SPEC técnica

Se creará una SPEC técnica hija con alcance exclusivo: **autorizar `catalog-signal + start/stop` en el endpoint component-bound de Actions de Playmaker**.

Debe contener:

- Estado objetivo y fuera de alcance.
- Diagrama `[NEW]`, `[MODIFIED]`, `[UNCHANGED]`.
- Contrato del principal Tiger en `SecurityContext`.
- Configuración exacta del endpoint protegido.
- Whitelist de Signals y default deny dentro de ese tipo.
- Resolución persistida de componente, Data Product, owner team e importación.
- Uso del cliente ACME proveniente del PR 1126 y refactor requerido.
- Orden obligatorio antes de KVS/BigQueue.
- Modelo de errores `401/403/404/503`.
- Observabilidad sin datos sensibles.
- Archivos afectados.
- Tests unitarios, de integración, regresión y ausencia de side effects.
- Decisiones `DD-N` de esta nota.

### 11.3 SPECs posteriores

Después de validar la primera vertical se crearán, una por vez y sólo cuando entren en planificación, SPECs técnicas para:

- Refactor de delete/inactivate desde PR 1126 hacia el mecanismo consolidado.
- Deployments y otras mutaciones de componentes.
- Relaciones y pipelines, incluyendo cross-DP y datos legacy.
- Nuevas familias de Actions y, si se decide, endpoints legacy.

No se crearán ahora documentos técnicos vacíos para esas etapas.

## 12. Derivación de tasks

Las tasks se crean solamente después de aprobar la SPEC técnica correspondiente. Para la primera vertical, el corte esperado es:

| Orden | Task conceptual | Gate de término |
|---|---|---|
| T-01 | Corregir el principal Tiger y su respuesta `401` | El filtro publica username, no registra token y los tests de seguridad pasan |
| T-02 | Extraer el autorizador ACME concreto desde la implementación mergeada y migrar delete/inactivate | Una sola implementación recibe `username + teamName`, exige `projectCode`; ambos flujos conservan `DEPLOYER_AND_UP` y sus tests |
| T-03 | Implementar whitelist y validación reutilizable de Signals dentro del caso de uso | Sólo `catalog-signal + start/stop` consulta `DEV_AND_UP`; unknown/imported se rechaza |
| T-04 | Migrar Actions a consumir identidad Tiger y el autorizador común | Actions no llama `TigerTokenService` ni `AcmeClient` directamente y valida antes de efectos |
| T-05 | Verificar exclusiones de alcance | Precreation, polling, legacy y callbacks quedan fuera; otras tecnologías no consultan ACME |
| T-06 | Verificar orden y ausencia de side effects | Deny/error no guarda KVS ni publica BigQueue |
| T-07 | Regresión de tecnologías fuera de alcance | Kafka, Flink y ClickHouse conservan el comportamiento previo |
| T-08 | Observabilidad y documentación operativa | Métricas y logs no exponen token, grants o payloads sensibles |

Esta tabla es una descomposición preliminar para validar el diseño. Los IDs y el contenido definitivo se generan en Spellbook desde la SPEC técnica aprobada.

## 13. Estrategia de pruebas

Primero se implementan los caminos críticos; después se completa al menos 95% de cobertura para código nuevo.

### 13.1 Tiger

- Token válido publica el username correcto.
- Token ausente, inválido o expirado corta con `401`.
- El token no queda como principal ni aparece en logs.
- Una ruta pública preserva su comportamiento.

### 13.2 Autorización de Signals

- `catalog-signal + start` con rol permitido continúa.
- `catalog-signal + stop` con rol permitido continúa.
- `catalog-signal` con Action desconocida rechaza.
- Signals importado rechaza sin consultar ACME.
- Rol insuficiente devuelve `403`.
- Grant correspondiente a otro equipo no habilita.
- ACME no disponible devuelve `503`.
- Data Product, componente o ownership inválido falla cerrado.

### 13.3 Regresión del primer consumidor

- Delete e inactivate usan el autorizador común con `DEPLOYER_AND_UP`.
- `admin`, `maintainer` y `deployer` conservan acceso.
- `committer` y roles inferiores continúan rechazados.
- Un grant de otro proyecto o equipo no habilita.
- No quedan llamadas productivas a `AuthorizationUtils.requireDeployerOrAbove`.

### 13.4 Side effects e integración

- Un rechazo no guarda `ActionKvsEntry`.
- Un rechazo no invoca `producer.publish`.
- Un allow guarda y publica exactamente una vez.
- El component template del mensaje es el persistido.
- Flink, Kafka y ClickHouse no consultan ACME en esta etapa.
- Precreation, polling, callbacks y legacy mantienen su comportamiento.

## 14. Decisiones de diseño

- **DD-1 — Tiger se resuelve una vez en la frontera HTTP.** `CustomAuthorizationFilter` valida el token y publica username como principal; Actions no vuelve a llamar Tiger.
- **DD-2 — ACME no es middleware.** La consulta exacta ocurre dentro de un autorizador reutilizable cuando el caso de uso ya resolvió `teamName + projectCode`.
- **DD-3 — La primera whitelist es un par tipo + Action.** Sólo `catalog-signal + start` y `catalog-signal + stop` quedan protegidas; una Action Signals desconocida se rechaza.
- **DD-4 — La fuente de verdad es persistida.** `componentTemplateCode`, pertenencia al Data Product, `teamName` y `sourceComponentId` salen de Playmaker, no del cliente.
- **DD-5 — El caso de uso aplica la autorización.** La validación no depende de que el llamador sea HTTP y se ejecuta después de resolver el target y antes del primer efecto.
- **DD-6 — Los services consumen un autorizador concreto.** Resuelven su recurso y realizan una sola llamada con caller, scope y nivel; no contienen parsing de grants, endpoints ACME ni nombres de roles.
- **DD-7 — PR 1126 mergeado es base técnica, no diseño transversal final.** Se reutiliza `getOwnerProjectGrants`; `PipelineAuthorizationService.assertAdminAccess` y la política estática se refactorizan al incorporar nuevos casos.
- **DD-8 — Polling no cambia.** Cualquier contradicción con read Actions se registra y resuelve como alcance separado.
- **DD-9 — Legacy no se contempla aún.** La arquitectura puede extenderse, pero no se agregan rutas, adaptadores ni tests legacy en esta entrega.
- **DD-10 — Sin annotation en la implementación inicial.** `@RequiresCapability` se documenta como posible evolución al final del proyecto y sólo se evalúa sobre repetición comprobada.
- **DD-11 — SDD es el gate de ejecución.** No hay branch de implementación ni código antes de aprobar la SPEC funcional, la SPEC técnica y sus tasks.
- **DD-12 — Tres niveles y nada más.** `READ` usa Tiger; `DEV_AND_UP` acepta committer o superior; `DEPLOYER_AND_UP` acepta deployer o superior para delete/inactivate.
- **DD-13 — Pipeline deploy está incluido.** La omisión de su ruta en la SPEC original se considera un error documental, no una exclusión funcional.
- **DD-14 — Legacy se identifica explícitamente.** Controllers/rutas marcados `@Deprecated` y reemplazados por RFC-002 quedan fuera de la primera migración; las rutas modernas se seleccionan mediante allow-list.
- **DD-15 — Una implementación, tres consumidores iniciales.** El autorizador es una clase concreta sin interfaz: delete e inactivate prueban la migración sin cambio funcional; Actions Signals incorpora el nuevo nivel `DEV_AND_UP`.

## 15. Evolución final: `@RequiresCapability`

Cuando Signals, delete, inactivate, deployments y otras mutaciones estén resueltos mediante casos reales, se evaluará si existe una forma estable de expresar capacidades:

```java
@RequiresCapability(DELETE_COMPONENT)
public void deleteComponent(...) {
  // caso de uso
}
```

Si se adopta, la annotation se aplicará en services o fronteras de casos de uso, no en controllers. Debe poder resolver ownership sin duplicar queries, ejecutarse antes de efectos, cubrir invocaciones no HTTP y mantener errores observables. Si requiere parámetros mágicos, SpEL, múltiples resolvers o lógica escondida en Aspects, se descartará en favor de llamadas explícitas.

Esta evaluación pertenece al cierre arquitectónico del proyecto y debe figurar en la presentación o SPEC técnica final como evolución, no como compromiso de la primera entrega.

## 16. Alternativas descartadas o postergadas

- Un `AuthorizationService` genérico con interfaz y múltiples capabilities desde la primera entrega: postergado por YAGNI.
- Resolver todos los grants ACME en cada request protegida: descartado por costo, falta de team conocido y llamadas innecesarias para lecturas.
- Aplicar ACME a todo el endpoint genérico de Actions: descartado porque mezcla read y mutation Actions y afectaría tecnologías fuera de alcance.
- Confiar en `component_type` enviado por el cliente para componentes existentes: descartado; prevalece el estado persistido.
- Considerar una Action desconocida como lectura: descartado por riesgo de bypass.
- Agregar política de visibilidad a polling: descartado del alcance actual porque SIG-616 busca autorizar mutaciones.
- Migrar endpoints legacy junto con Signals: postergado hasta que exista decisión funcional y SPEC propia.
- Incorporar `@RequiresCapability` ahora: postergado hasta observar repetición real y una resolución estable de ownership.

## 17. Gates pendientes

- [ ] Confirmar clasificación o relación funcional/técnica de SIG-616 en Spellbook.
- [x] Confirmar `catalog-signal`, `start` y `stop` contra el contrato vigente del Control Plane.
- [x] Confirmar roles ACME permitidos para mutaciones de Signals: `DEV_AND_UP`.
- [ ] Confirmar tratamiento funcional de componentes importados.
- [ ] Confirmar que precreation de Signals no tiene un uso válido.
- [ ] Verificar comportamiento real de polling para read Actions sin incorporarlo al alcance Signals.
- [x] Verificar que PR 1126 está mergeado en `origin/develop`; base observada `1a4caf093`.
- [x] Validar la consulta ACME contra el contrato final: `username + teamName + headers`, con `projectCode` filtrado localmente.
- [ ] Resolver error mapping de Tiger y ACME antes de congelar la SPEC técnica.
- [ ] Definir branch y base limpias después de aprobar SPEC y tasks.
