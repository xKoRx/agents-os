---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Estandarización de Scopes RIO]]"
  - "[[ads-signals-frontend]]"
  - "[[RIO]]"
aliases:
  - SPEC frontend scopes RIO
  - routing dinámico Playmaker desde ads-signals-frontend
tags:
  - kind/doc
  - area/meli
  - project/scopes-rio
  - tech/nordic
created: "2026-09-16"
updated: "2026-09-16"
---

# Technical Specification — Routing dinámico de backend en `ads-signals-frontend`

**Feature**: `rio-dynamic-backend-scope-routing`
**Owner**: Rodrigo Jara
**Project**: Signals (`ads-signals-frontend`)
**Status**: DRAFT
**Deriva de**: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) y [[Estandarización de Scopes RIO]]
**Baseline revisada**: `develop@7a9296cb`

## Propósito

Desacoplar el scope del frontend Nordic del target físico de Playmaker en ambientes de test. Todo frontend desplegado en un scope Fury de test usa `rio-playmaker-test.melisystems.com`; el BFF envía el scope backend efectivo en `X-Rio-Scope` y Fury Routes selecciona la infraestructura destino. Producción conserva su host dedicado, no acepta overrides y nunca emite el header.

## Contenido

### Contexto

`frontend-config` carga hoy `config/<SCOPE>-production.js`, por lo que `test2`, `test3`, `beta` y `staging` fijan distintos hosts de Playmaker. Nordic ya publica el scope efectivo del frontend en `env.SCOPE`, incluido el scope elegido mediante MeliLab. Las llamadas server-side y las 61 integraciones BFF con Playmaker convergen en `api/lib/playmaker.ts`; no se requiere migrar cada servicio a un cliente nuevo.

El cambio introduce un único entrypoint no productivo. El frontend sólo valida forma y longitud; Fury Routes decide si un scope existe y a qué target no productivo resuelve.

### Arquitectura objetivo

```text
MeliLab / Nordic [UNCHANGED]
  └─▶ env.SCOPE = frontendScope

URL ?backend=<scope> [NEW, test only]
  └─▶ resolveBackendScope(req) [NEW]
       └─▶ playmaker(req) [MODIFIED]
            ├─ test ─▶ Fury Route compartida [NEW] ─▶ target no-prod
            └─ prod ─▶ Playmaker productivo [UNCHANGED]
```

### Contrato de selección

| Runtime | `frontendScope` | Override `backend` | `backendScope` efectivo | Host Playmaker | Header |
|---|---|---|---|---|---|
| Fury test | `env.SCOPE` | ausente | `env.SCOPE` | `http://rio-playmaker-test.melisystems.com` | `X-Rio-Scope: <env.SCOPE>` |
| Fury test | `env.SCOPE` | `?backend=<scope>` | `<scope>` | `http://rio-playmaker-test.melisystems.com` | `X-Rio-Scope: <scope>` |
| Fury production | `env.SCOPE` | cualquiera | no aplica | `http://rio-playmaker-prod.melisystems.com` | ausente |

Precedencia en test:

```text
query.backend válido > override de sesión válido > env.SCOPE
```

`backend=` vacío elimina el override y vuelve a `env.SCOPE`. Un valor explícito usa `^[a-z0-9][a-z0-9-]{0,62}$`; no existe catálogo frontend. Un scope bien formado que Fury no reconoce falla sin retry al default ni a producción.

El override se conserva en la cookie de sesión host-only y `HttpOnly` `rio_backend_scope_override`, con `Secure` y `SameSite=Lax`. `app/server/index.ts` la actualiza antes de SSR; `playmaker(req)` usa `req.query.backend` en el primer request y la cookie en `/api`. Sólo el BFF construye `X-Rio-Scope`.

Después de resolver, el middleware publica el resultado en la cookie host-only `rio_effective_backend_scope`, legible por la UI y no autoritativa. Los stores la usan únicamente para namespacing/reset; el BFF la ignora y siempre recalcula desde query, override de sesión y `env.SCOPE`.

### Frontera test / producción

La activación no usa `NODE_ENV`: los scopes Fury de test ejecutan builds `production`. `test-production.js` declara las claves de routing test, `default-production.js` las de producción y `fury-production.js` importa explícitamente `test-production.js`; `frontend-config` no hereda por `FURY_IS_TEST_SCOPE`. El archivo nuevo proyecta sólo `playmaker_meli_domain` y `playmaker_scope_routing_enabled`, nunca el objeto test completo:

```js
const env = require('frontend-env');
const testConfig = require('./test-production');

module.exports = env.FURY_IS_TEST_SCOPE === 'true'
  ? {
      playmaker_meli_domain: testConfig.playmaker_meli_domain,
      playmaker_scope_routing_enabled: true,
    }
  : {};
```

El orden efectivo es `default` → `default-<env>` → `<env>` → `<platform>` → `<platform>-<env>` → `<scope>` → `<scope>-<env>`. Por eso los archivos de scopes conocidos de test declaran también esas dos claves compartidas; en particular, `staging-production.js` no puede depender de una clasificación aún no verificada de `FURY_IS_TEST_SCOPE`. Para scopes nuevos, `fury-production.js` entrega el default dinámico.

La prohibición de scopes cruzados se aplica en dos capas:

1. El cliente productivo usa sólo `rio-playmaker-prod.melisystems.com`, ignora `backend` y no emite `X-Rio-Scope`.
2. `rio-playmaker-test.melisystems.com` sólo registra targets no productivos; `production` o un scope desconocido fallan cerrado.

`test2-production.js`, `test3-production.js`, `beta-production.js` y `staging-production.js` se conservan. Sólo se desacopla el destino de Playmaker: sus diferencias actuales de templates, Entity Service, Kraken, feature flags y analítica no cambian en esta fase. En `test`, las dos claves de routing pueden mergearse desde `fury-production.js` y luego desde `test-production.js`; el segundo merge es idempotente.

### Resolver y cliente Playmaker

`api/lib/backendScope.ts` concentra `resolveBackendScope(req)`, sintaxis, cookies y decisión test/prod. Devuelve `undefined` cuando `playmaker_scope_routing_enabled` es falso y no conoce hosts, targets ni listas de scopes.

`api/lib/playmaker.ts` conserva su API pública (`playmaker(req).get/post/put/patch/delete`) y agrega el resultado del resolver a todos los verbos. En Fury inicializa RestClient con el `meliDomain` estático `rio-playmaker-test` o `rio-playmaker-prod`; fuera de Fury conserva el `baseURL` actual para no cambiar la resolución a `melioffice.com` ni el flujo local. El header se incorpora únicamente cuando el resolver retorna un scope y ningún caller puede sobreescribirlo. La construcción del cliente conserva `allowRepeatedParams: true`, requisito del filtro repetido `component_template_code`.

El override selecciona el backend Playmaker, no el catálogo configurado en el frontend. `playmaker_component_templates` permanece asociado al scope frontend; la POC sólo certifica pares de scopes de test cuyos IDs/códigos de template sean compatibles. Esa compatibilidad es un gate de prueba o de manifiesto de infraestructura, nunca un enum ni una validación semántica en el frontend.

### Persistencia y aislamiento de estado

Cambiar de backend scope obliga a una navegación completa. El reload hace que SSR, cookie, llamadas BFF y estado hidratado observen el mismo scope antes de emitir requests.

Los datos persistidos o compartidos se aíslan por `backendScope` efectivo:

- `api/teams/grants.ts`: la clave deja de ser sólo `userId` y pasa a `backendScope:userId`.
- `api/pipeline/index.ts`: la clave `history-month` incorpora `backendScope` además de usuario, data product, environment, mes, página y tamaño.
- `src/app/store/page.store.ts`: la versión persistida registra `backendScope`; al hidratar otro scope conserva preferencias visuales y reinicia los slices ligados al backend, incluidos `activeEnvironments`, drafts, pending approvers e import info.
- `src/features/deploy-pipeline/store/deploySessionStore.ts`: el namespace incorpora `backendScope`; una ejecución iniciada en un scope no se retoma ni se pollea desde otro.

### Manejo de errores

| Escenario | Comportamiento |
|---|---|
| `backend` malformado en una página test | `400`; no se actualiza cookie ni se llama Playmaker |
| Cookie de override malformada o manipulada | se elimina, se usa `env.SCOPE` y se registra warning sin el valor crudo |
| Scope bien formado pero inexistente | se propaga el rechazo de Fury/Playmaker mediante el manejo actual; no hay fallback |
| `backend` presente en producción | se ignora, se elimina cualquier cookie de override y se llama al host prod sin header |
| `env.SCOPE` ausente con routing test habilitado | `500` de configuración; no se llama Playmaker |
| Respuesta upstream inválida | conserva el `502` actual de `playmaker.ts` |

### Seguridad

`backend` no forma una URL ni selecciona un dominio: el destino de red es un `meliDomain` estático y el valor sólo viaja en el header aprobado `X-Rio-Scope`. El regex es una whitelist sintáctica resistente a ReDoS; la whitelist de targets no productivos vive en Fury. Producción ignora el selector, el browser nunca envía el header al upstream y logs/errores no incluyen query completa, cookies ni tokens. La persistencia usa cookies de sesión porque el repo no tiene Ragnar Session configurado; agregarlo exigiría Secret+KVS sólo para un valor no sensible que ya es visible en la URL.

### Design Decisions

#### DD-1: Reutilizar `playmaker(req)` como cliente scope-aware

**Decisión**: extender el cliente BFF existente y mantener su API pública.

**Fundamentación**: todos los verbos y consumidores convergen en ese seam. Un cliente paralelo o headers por router producirían cobertura parcial entre GET, mutaciones y SSR.

#### DD-2: Usar el scope Nordic como default y `backend` sólo como override

**Decisión**: `env.SCOPE` representa la selección MeliLab ya materializada para el frontend; `backend` altera únicamente el backend.

**Fundamentación**: evita interpretar una cookie privada o duplicar Nordic. El repo no contiene un contrato MeliLab de dos ejes; el valor estable es el runtime efectivo.

#### DD-3: Una entrada test por header y una entrada prod sin multiplexación

**Decisión**: test usa `rio-playmaker-test.melisystems.com` + `X-Rio-Scope`; producción usa `rio-playmaker-prod.melisystems.com` sin header.

**Fundamentación**: la topología impide cruces sin que el frontend conozca todos los scopes. Construir `rio-playmaker-${scope}` mantendría el acoplamiento y abriría routing por input. `meliDomain` cumple el contrato Nordic para dominios internos en Fury; la seguridad depende de que el destino sea estático, no de cambiar `baseURL` por sí mismo.

#### DD-4: Fury valida existencia; el frontend sólo valida sintaxis

**Decisión**: no incorporar enum, allowlist ni archivo por scope.

**Fundamentación**: el alta de una lane debe ser una operación de infraestructura. Una allowlist frontend convertiría cada scope nuevo en un deploy de UI y generaría dos autoridades de existencia.

#### DD-5: Persistir sólo el override y forzar reload al cambiarlo

**Decisión**: la cookie conserva la intención explícita del usuario; el default continúa siendo `env.SCOPE`, y todo cambio se aplica mediante navegación completa.

**Fundamentación**: MeliLab sigue definiendo ambos ejes sin override y el reload evita que SSR y XHR consulten backends distintos; `sessionStorage` no cubre SSR.

### Archivos afectados

#### Archivos nuevos

| Archivo | Propósito |
|---|---|
| `config/fury-production.js` | Importar `test-production.js` y proyectar sólo las claves compartidas de routing cuando `FURY_IS_TEST_SCOPE=true` |
| `api/lib/backendScope.ts` | Resolver y validar el scope backend efectivo y administrar el contrato de cookies |
| `src/lib/backendScope.ts` | Leer el scope efectivo sólo para namespacing/reset de estado browser |
| Tests unitarios de resolver/config/cliente | Cubrir precedencia, producción y headers por verbo |

#### Archivos modificados

| Archivo | Cambio |
|---|---|
| `config/default.js` y `config/default-development.js` | Mantener `baseURL` para ejecución no Fury/local y separar el `meliDomain` usado en Fury |
| `config/test-production.js` | Declarar `rio-playmaker-test` y habilitar routing por scope |
| `config/default-production.js` | Declarar `rio-playmaker-prod` y routing deshabilitado |
| `config/test2-production.js`, `config/test3-production.js`, `config/beta-production.js` y `config/staging-production.js` | Reutilizar las dos claves de routing test sin alterar templates, Entity Service, Kraken, flags ni analítica propios |
| `types/config.d.ts` | Tipar `playmaker_meli_domain` y `playmaker_scope_routing_enabled` |
| `app/server/index.ts` | Capturar/limpiar el override, publicar el scope backend efectivo para los stores y forzar navegación coherente |
| `app/nordic-pages/data-products/[name]/index.tsx` | Admitir `backend` en el schema estricto de query de la página SSR |
| `api/lib/playmaker.ts` | Adjuntar `X-Rio-Scope` en test para todos los verbos y conservar `allowRepeatedParams: true` |
| `api/teams/grants.ts` | Particionar cache por scope |
| `api/pipeline/index.ts` | Particionar request coalescing por scope |
| `src/app/store/page.store.ts` | Versionar y resetear estado dependiente del backend al cambiar scope |
| `src/features/deploy-pipeline/store/deploySessionStore.ts` | Namespacing de ejecuciones por backend scope |

### Observabilidad

`playmaker.ts` registra `routing_mode`, `scope_source` y status, sin token ni query completa. Ninguna métrica usa el scope dinámico como tag; los contadores distinguen `default`, `override`, `invalid` y `route_rejected`. La POC verifica que prod nunca emita `X-Rio-Scope`.

### Estrategia de tests

- Resolver unitario: precedencia query→cookie→`env.SCOPE`, clear con `backend=`, sintaxis, cookie manipulada, scope ausente y producción.
- Config unitario: cualquier `SCOPE` con `FURY_IS_TEST_SCOPE=true` usa `rio-playmaker-test`; scopes test conocidos conservan el routing compartido aun si una clasificación difiere; producción usa `rio-playmaker-prod`; fuera de Fury/local se conserva `baseURL` y el routing no depende de `NODE_ENV`.
- Cliente unitario: GET/POST/PUT/PATCH/DELETE incluyen header sólo en test; un caller no puede inyectarlo en prod y dos o más `component_template_code` llegan como parámetros repetidos.
- Middleware/SSR: el primer request con `?backend=beta` pasa los schemas de página, consulta beta, persiste el override y los XHR posteriores resuelven el mismo scope; `backend=` vuelve al scope Nordic.
- Aislamiento: grants, history coalescing, page store y deploy sessions no reutilizan entradas entre `test2` y `test3`.
- Integración Fury: matriz `test2→test2`, `test2→test3`, scope inexistente, `test→production`, `prod→test` y prod con query. Los pares test sólo se certifican si comparten contrato de templates; los cruces fallan o se ignoran según la frontera de origen.

### Rollout y rollback

La secuencia y sus gates viven en [[Estandarización de Scopes RIO#Fase 1 — Routing dinámico frontend → Playmaker]]. El rollout técnico exige route test sin targets productivos antes del frontend, canary con default+override y monitoreo de rechazos y ausencia del header en prod.

Rollback: desactivar `playmaker_scope_routing_enabled` y volver a usar los `playmaker_base_url` que los archivos por scope conservaron. La route compartida puede quedar sin tráfico; producción no requiere rollback porque su host y contrato no cambian.

### Fuera de alcance

- Crear o modificar las Fury Routes y sus targets; esa configuración la implementa el owner de infraestructura.
- Cambiar Playmaker, eventos de deployment, BigQueue, control planes o bases de datos.
- Cambiar dinámicamente `playmaker_component_templates`; el catálogo sigue perteneciendo al scope frontend y la compatibilidad entre pares test es un prerrequisito de certificación.
- Enrutar `rio_entity_service_base_url` mediante el override; Entity Service conserva la configuración del scope frontend.
- Agregar un selector visual de scope en la UI; MeliLab y el query param son las entradas de esta fase.
- Validar semánticamente la existencia o el rol de un scope en el frontend.
- Permitir routing productivo por header o cruces entre segmentos.

### Dependencia externa de aprobación

Fury debe confirmar que `X-Rio-Scope` puede usarse como clave exacta de route en `rio-playmaker-test`, que una clave sin target falla sin fallback y que la route test no puede referenciar targets productivos. La implementación frontend puede avanzar con tests unitarios, pero el gate de integración exige evidencia de esas tres propiedades.

## Fuentes

- `ads-signals-frontend` `develop@7a9296cb`: `frontend-config`, configuraciones, servidor Ragnar, cliente Playmaker, caches y stores persistidos.
- `frontend-env/types/index.d.ts`: `SCOPE` y `FURY_IS_TEST_SCOPE` disponibles en runtime Nordic/Fury.
- `meli-frontender-web` v2.10.1: Nordic/Odin 9 detectado; `nordic/config`, `nordic/env`, `nordic/ragnar`, `nordic/restclient` y guía de seguridad.
- [[Estandarización de Scopes RIO]] y [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599): selección independiente frontend/backend y continuidad del ambiente.
