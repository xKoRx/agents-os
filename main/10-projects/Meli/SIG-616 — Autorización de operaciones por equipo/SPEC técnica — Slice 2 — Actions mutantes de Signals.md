# SIG-616 — Slice 2: Actions mutantes de Signals

## Metadatos

- Tipo: Technical SPEC
- Estado inicial: Draft
- Requerimiento de origen: [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- Dependencia: Slice 1 aprobado e implementado
- Aplicación: `rio-playmaker`
- Baseline de diseño: `origin/develop@1a4caf093`

## Objetivo

Aplicar la primera restricción funcional nueva de SIG-616 a las Actions mutantes de Signals, usando Tiger para identidad y el autorizador común para ownership + rol ACME, antes de cualquier contexto de deployment, escritura KVS o publicación BigQueue.

El slice protege exclusivamente el par persistido `catalog-signal + start|stop`. Otras tecnologías mantienen su comportamiento. El endpoint precreation sólo incorpora el rechazo mínimo del mismo par para que no exista una ruta alternativa sin componente persistido.

## Decisiones

- Tiger es el único middleware: valida una vez y publica el username en `SecurityContext`. La cadena de Spring Security devuelve `401` en rutas autenticadas sin identidad válida sin interferir con rutas `permitAll`.
- ACME no es middleware ni se precarga sólo con username.
- La identidad autenticada se pasa desde el contexto al caso de uso; `ActionServiceImpl` deja de volver a validar Tiger.
- La whitelist usa `component_type + actionName`, no sólo el nombre de la Action.
- Para component-bound, el `component_type` proviene de `ComponentModel.componentTemplateCode`; nunca del request.
- Sólo `catalog-signal + start` y `catalog-signal + stop` exigen `DEV_AND_UP`.
- Una Action component-bound desconocida sobre `catalog-signal` se rechaza por default deny dentro del alcance.
- Un Signals importado se identifica exclusivamente con `ImportAuthorizationRepository.existsApprovedByImportedComponentId(componentId)` y se rechaza. `sourceComponentId` no decide importación.
- En precreation, el par `catalog-signal + start|stop` se rechaza sin ACME: el dato cliente sólo puede activar DENY, nunca conceder autorización.
- Polling conserva su política y algoritmo; sólo reutiliza la identidad ya validada para evitar una segunda llamada Tiger.

## Alcance

Incluye:

- Corregir el principal de `CustomAuthorizationFilter` para que sea username y nunca Bearer token.
- Configurar un `AuthenticationEntryPoint` explícito que responda `401` para rutas `.authenticated()` sin identidad válida; las rutas `permitAll` continúan pasando sin token.
- Eliminar del filtro las listas duplicadas de rutas públicas y `isPublicPath`; `SecurityConfig` queda como única fuente de verdad para `permitAll` versus `.authenticated()`.
- Pasar el username autenticado desde `ActionController` y `ActionResultController` a `ActionService`.
- Eliminar la dependencia de `TigerTokenService` desde `ActionServiceImpl` si todos sus entrypoints usan el principal.
- Clasificar y autorizar component-bound Signals `start/stop` con `DEV_AND_UP`.
- Rechazar Signals desconocida, importada o con ownership incompleto.
- Rechazar Signals `start/stop` en precreation antes de KVS/BigQueue y sin ACME.
- Probar allow, deny, errores y ausencia de side effects.

No incluye:

- Agregar ACME a Kafka, ClickHouse u otras Actions declaradas de lectura.
- Incorporar Flink u otros tipos que reutilicen `start/stop`.
- Cambiar el long polling, `ActionKvsEntry`, callbacks o visibilidad de resultados.
- Proteger deployments, undeploy, relaciones, pipeline deploy u otras mutaciones.
- Proteger `/services/{serviceId}/actions/code`; es un riesgo residual explícito para una SPEC posterior.
- Cambiar rutas públicas ni callbacks de Control Plane.
- Cache, annotations, AOP o un registry genérico de policies.

## Matriz de política de este slice

### Component-bound

| Tipo persistido | Action | Resultado |
|---|---|---|
| `catalog-signal` | `start` | Tiger + `DEV_AND_UP` |
| `catalog-signal` | `stop` | Tiger + `DEV_AND_UP` |
| `catalog-signal` | cualquier otra | `403` default deny |
| cualquier otro tipo | cualquiera | comportamiento actual, sin ACME nuevo |

`DEV_AND_UP` permite `admin`, `maintainer`, `deployer` y `committer` con grant exacto de team + project.

### Precreation

| Tipo solicitado | Action | Resultado |
|---|---|---|
| `catalog-signal` | `start` o `stop` | `403`, sin ACME ni side effects |
| cualquier otro par | cualquiera | comportamiento actual |

Esta segunda tabla no es una autorización basada en input del cliente. Sólo cierra el bypass de los dos pares mutantes conocidos.

## Flujo objetivo

```text
[MODIFIED] CustomAuthorizationFilter
  -> si hay Bearer, intenta validarlo con Tiger
  -> válido: publica username; inválido: limpia/no establece Authentication

[MODIFIED] SecurityConfig
  -> decide permitAll versus authenticated
  -> sólo una ruta authenticated sin identidad activa el entry point 401

[MODIFIED] ActionController / ActionResultController / ActionService
  -> pasan username autenticado; no revalidan Tiger

[MODIFIED] ActionServiceImpl.triggerAction
  -> resuelve Data Product + componente + environment
  -> usa componentTemplateCode persistido + actionName
  -> si no es catalog-signal: flujo actual
  -> si Signals desconocida: 403
  -> si Signals importada por autorización aprobada: 403
  -> OperationAuthorizationService.require(..., DEV_AND_UP)
  -> sólo después: deployment context -> KVS -> BigQueue

[UNCHANGED] Signals Control Plane
```

### Orden component-bound obligatorio

1. Tiger valida y publica username en la frontera HTTP.
2. `fetchComponentInHierarchy` resuelve DP, componente y environment; inconsistencias mantienen `404`.
3. La policy clasifica con `component.getComponentTemplateCode()` y `actionName`.
4. Para Signals permitido, consulta si existe autorización de importación aprobada y activa.
5. Autoriza con `teamName + projectCode` persistidos y `DEV_AND_UP`.
6. Recién entonces ejecuta `fetchDeploymentContext`, genera dispatch, guarda KVS y publica.

El deny o error en pasos 2–5 debe producir cero llamadas a deployment context, KVS y BigQueue.

### Orden precreation obligatorio

1. Tiger valida y publica username.
2. Se conserva la resolución de Data Product y su `404` actual.
3. Si el input es exactamente `catalog-signal + start|stop`, se rechaza `403`.
4. Sólo otros pares continúan por el flujo existente.

No se consulta importación ni ACME porque no existe componente target persistido.

## Identidad Tiger

Para una ruta protegida, `CustomAuthorizationFilter`:

- Si existe `X-Tiger-Token: Bearer …`, invoca una sola vez `TigerTokenService.getAuthToken(headers)` y exige username no vacío.
- Con Bearer válido, construye `CustomAuthenticationToken` con username como principal.
- Con Bearer presente pero inválido, expirado o con username vacío, limpia/no establece `Authentication` y continúa la cadena.
- Con token ausente o formato no Bearer, también continúa sin `Authentication`.
- `SecurityFilterChain` decide el resultado: una ruta `permitAll` continúa y una ruta `.authenticated()` activa el `AuthenticationEntryPoint` de `401`.
- Nunca registra el token.
- Se eliminan `ANY_METHOD_PUBLIC_PATHS`, `POST_PUBLIC_PATHS`, `GET_PUBLIC_PATHS` e `isPublicPath` del filtro. Las reglas existentes de `SecurityConfig` son la única autoridad de rutas públicas.

`ActionController` y `ActionResultController` obtienen el principal autenticado y pasan su nombre a `ActionService`; no conocen ACME ni roles. `ActionServiceImpl` confía únicamente en ese username proveniente de `Authentication`, nunca en un username/header enviado por el cliente. Los headers siguen disponibles únicamente porque el cliente ACME necesita propagar Tiger.

## Implementación KISS de la whitelist

La clasificación puede permanecer privada en `ActionServiceImpl` mediante una constante de tipo y un `Set<String>` de Actions. No se crea una jerarquía de clasificadores con un único tipo soportado.

Tipo y Action se comparan por igualdad exacta, case-sensitive y sin `trim`, aliases ni normalización. Una variante no exacta bajo `catalog-signal` cae en unknown y se rechaza; la implementación no amplía silenciosamente la whitelist.

La misma función de par conocido se reutiliza así:

- Component-bound: el par conocido habilita la consulta de autorización; un nombre desconocido bajo `catalog-signal` deniega.
- Precreation: el par conocido sólo deniega; nunca habilita.

## Archivos previstos

| Cambio | Archivo |
|---|---|
| Modificado | `filter/CustomAuthorizationFilter.java` |
| Modificado | `filter/CustomAuthenticationToken.java` |
| Modificado | `config/SecurityConfig.java` para el `AuthenticationEntryPoint` explícito |
| Modificado | `controller/ActionController.java` |
| Modificado | `controller/ActionResultController.java` |
| Modificado | `service/ActionService.java` |
| Modificado | `service/impl/ActionServiceImpl.java` |
| Tests | Tests del filtro, controller, service e integración HTTP/side effects |

No se cambia `ActionsTriggerProducer`, `ActionKvsRepository`, eventos ni Control Planes.

## Errores

| Condición | Respuesta |
|---|---|
| Tiger ausente, malformado, inválido o expirado en ruta `.authenticated()` | `401` desde la cadena de seguridad |
| Cualquier estado Tiger en ruta `permitAll` | La ruta continúa; el token opcional no cambia su carácter público |
| DP/componente/environment inexistente o fuera de jerarquía | `404` actual |
| Signals desconocida | `403` |
| Signals importada | `403` |
| username/team/project nulo o blanco | `403` fail-closed; sin llamada ACME |
| grant insuficiente o cruzado | `403` |
| ACME no verificable | `403` fail-closed, distinguible sólo en observabilidad |
| deployment activo inexistente después de autorizar | `409` actual |

Ninguna respuesta revela grants, team members, tokens o detalles internos de ACME.

## Observabilidad

- Eliminar cualquier log del Bearer token.
- Registrar resultados de autorización con causas de baja cardinalidad: `invalid_tiger`, `unknown_signals_action`, `imported_component`, `invalid_scope`, `insufficient_role`, `acme_unavailable`.
- No registrar username, token ni payload de grants en los nuevos logs.
- Mantener logs de dispatch sólo después de una autorización exitosa.

## Pruebas

Pruebas críticas primero y cobertura mínima de 95% del código nuevo:

- Integración HTTP: en rutas autenticadas, token ausente, malformado, inválido y expirado devuelve `401`; el controller no se invoca.
- Filtro/cadena: Tiger válido publica username, no token; rutas `permitAll` continúan sin token, con Bearer válido y con Bearer inválido/expirado.
- `SecurityConfig` es la única fuente de verdad de `permitAll`; el filtro no mantiene ni consulta una lista de paths.
- Action controller/service: no hay segunda llamada Tiger y `triggeredBy` usa username.
- Signals `start/stop`: permiten los cuatro roles `DEV_AND_UP` con team + project exactos.
- Rol insuficiente, grant de otro team/project, scope incompleto y error ACME devuelven `403`.
- `catalog-signal + unknown` devuelve `403` sin ACME ni side effects.
- Importado aprobado/activo devuelve `403`; un `sourceComponentId` de migración sin autorización aprobada no se considera importado.
- Deny/error no llama `fetchDeploymentContext`, no guarda KVS y no publica BigQueue.
- Allow guarda una vez y publica una vez.
- Precreation Signals `start/stop` devuelve `403` sin ACME/KVS/BigQueue; otros pares mantienen sus tests actuales.
- Kafka, ClickHouse, Flink y polling mantienen su comportamiento; ninguno recibe una policy ACME nueva en este slice.

## Gate de datos y rollout

Antes de habilitar el cambio en producción se debe medir cuántos componentes `catalog-signal` apuntan a Data Products sin `teamName` o `projectCode`, y comprobar que el `projectCode` persistido coincide exactamente con la convención real de ACME. El gate es cero registros afectados o una remediación/aceptación explícita antes del rollout; no se convierte en fallback permisivo.

La validación incluye un contract test determinista de `AcmeClientImpl` con un fixture representativo de `owner-project` y un smoke en ambiente no productivo usando un Data Product Signals y grant reales. El smoke se registra como evidencia operativa y no convierte ACME en dependencia de la suite automatizada.

El cambio de principal Tiger afecta transversalmente a rutas protegidas. La implementación debe verificar por búsqueda y pruebas que ningún consumidor productivo dependa de recibir el Bearer token como `Authentication.principal`.

Rollback: revert del slice. No hay migración de datos ni cambio de contrato de eventos.

## Tasks ejecutables

1. Corregir filtro/principal Tiger, eliminar sus allow-lists duplicadas y configurar el entry point `401`, cubriendo rutas autenticadas, `permitAll` y ausencia de token en logs.
2. Pasar username autenticado por `ActionController` y `ActionResultController`, actualizar firmas/Javadocs/`throws` de `ActionService` y controllers, y retirar revalidaciones Tiger sin alterar el algoritmo ni la autorización de polling.
3. Implementar whitelist local `catalog-signal + start|stop` y default deny para otras Actions Signals component-bound.
4. Integrar detección canónica de importados y `OperationAuthorizationService` con `DEV_AND_UP` antes de side effects.
5. Cerrar el bypass precreation para los dos pares conocidos sin consulta ACME.
6. Ejecutar matriz de pruebas, contract test ACME, smoke no productivo, gate de ownership y regresión de tecnologías/rutas excluidas.

## Criterios de aceptación

- Toda ruta Action protegida recibe username validado desde Tiger y nunca expone el Bearer token como principal o log.
- `SecurityConfig` es la única fuente de verdad de rutas públicas; una ruta `permitAll` continúa incluso con Bearer inválido o expirado.
- Signals component-bound `start/stop` sólo continúa con grant exacto y rol `DEV_AND_UP`.
- Signals desconocida, importada o sin scope completo falla cerrado antes de deployment context, KVS y BigQueue.
- Precreation Signals `start/stop` no puede evadir la policy y no consulta ACME.
- Otras tecnologías, polling, callbacks y legacy conservan su comportamiento.
- No se introducen policies genéricas, interfaces, annotations, cache ni lógica en Control Planes.

## Riesgos residuales explícitos

- Deployments, undeploy, relaciones, pipeline deploy y otras mutaciones siguen requiriendo sus propios slices.
- `POST /services/{serviceId}/actions/code` continúa fuera de cobertura y debe tratarse en una SPEC posterior.
- El `403` ante ACME no verificable es compatible pero menos expresivo que `5xx`; cualquier cambio requiere decisión separada.
- `@RequiresCapability` se evaluará sólo al final del proyecto si la repetición real lo justifica.
