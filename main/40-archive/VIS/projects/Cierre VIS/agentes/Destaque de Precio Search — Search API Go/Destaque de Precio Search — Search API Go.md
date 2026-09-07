---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Cierre VIS]]"
sprint:
start: 2026-08-04
due:
progress: 70
repo: search-api-go
jira: VMDEM-22
prs:
aliases:
  - Implementación PRICE_HIGHLIGHT_TIER Search API Go
  - Destaque de Precio Search API
tags:
  - kind/project
  - area/meli
  - app/search-api-go
  - feature/destaques-de-precio
created: 2026-08-04
updated: 2026-08-04
cssclasses:
  - wide
---

# Destaque de Precio Search — Search API Go

%% Naming: plan de implementación de la propagación de PRICE_HIGHLIGHT_TIER en Search API Go. Proyecto de agente bajo [[Cierre VIS]]. %%

> [!info]+ Search API Go — propagación del tier
> **Padre:** [[Cierre VIS]] · **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1
> **Baseline:** develop @ 414d5f3bf4 · **Spec:** [VMDEM-22](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-22)

## 🎯 Objetivo

Conservar PRICE_HIGHLIGHT_TIER desde la lectura de Items hasta el item
cacheado y la respuesta consumida por Search Middleware, sin interpretar el
valor ni crear contratos específicos.

Valores vigentes: VERY_LOW, LOW y NORMAL. Valores futuros deben viajar sin
transformación; la decisión de visibilidad no pertenece a Search API.

## 📊 Estado actual

- Items REST ya solicita attributes e include_attributes=all.
- internal/support/item/core/entity/item_transformation.go aplica la
  allowlist de atributos en Item.SetAttrAndTags.
- PREVIOUS_PRICE y PRICE_HIGHLIGHT_TIER están permitidos antes de construir
  SearchAPI.Attributes; los tiers futuros se conservan sin transformación.
- Process.Execute copia los atributos filtrados a SearchAPI.Attributes y el
  flujo de sincronización existente los escribe en las capas de caché.
- La rama `feature/price-highlight-tier-search-api` agrega `PRICE_HIGHLIGHT_TIER`
  a la allowlist y conserva atributos completos, incluidos tiers futuros.
- La allowlist histórica `process.FilterAttributes` también quedó sincronizada
  con una prueba específica; no se conectó al flujo productivo porque no tiene
  callers en esta baseline.
- POST /consumers/items ya reprocessa items ante actualizaciones; no se
  necesita endpoint, consumer, caché ni topic nuevo.
- Costo esperado: cambio acotado de allowlist, tests y validación operativa.

## 🧭 Alcance

### Incluye

- Permitir PRICE_HIGHLIGHT_TIER en SetAttrAndTags.
- Preservar value_id, value_name, values y value_type sin mutación.
- Tests de allowlist y propagación al modelo SearchAPI.
- Validar el camino de actualización de caché existente.
- Coordinar deploy antes del backfill o definir reprocess explícito.

### Fuera de alcance

- Calcular tiers o validar reglas del Sugeridor.
- Crear un campo dedicado en el response.
- Hacer el atributo filtrable como filtro de búsqueda.
- Cambiar pricing, SalePrice o PREVIOUS_PRICE.
- Agregar consumers, endpoints, KVS, Redis o BigQueue.

## 🏗️ Diseño

~~~text
Items API attributes
  -> item REST mapper
  -> Item.SetAttrAndTags allowlist
  -> SearchAPI.Attributes
  -> synchronize writers
  -> BigCache / Redis / KVS
  -> Search response item.attributes
~~~

Cambio productivo esperado:

~~~go
"PRICE_HIGHLIGHT_TIER": true,
~~~

No crear una constante de dominio si solo sería usada una vez: mantener el
patrón vigente de la allowlist y evitar una abstracción adicional.

## ✅ Tareas

> [!example]- Fuente de tareas — planificador único
> - [x] G1 — Crear branch desde develop y verificar baseline limpia respecto de archivos del feature #owner/agent #type/dev #area/meli #app/search-api-go ✅ 2026-08-04
> - [x] G2 — Agregar PRICE_HIGHLIGHT_TIER a validAt en item_transformation.go #owner/agent #type/dev #area/meli #app/search-api-go ✅ 2026-08-04
> - [x] G3 — Extender TestSetAttrAndTags con VERY_LOW, LOW y NORMAL, validando ID y valor exactos #owner/agent #type/dev #area/meli #app/search-api-go ✅ 2026-08-04
> - [x] G4 — Agregar test de Process.Execute que confirme presencia en SearchAPI.Attributes #owner/agent #type/dev #area/meli #app/search-api-go ✅ 2026-08-04
> - [x] G5 — Verificar que un tier futuro se conserva y no es reinterpretado por Search API #owner/agent #type/dev #area/meli #app/search-api-go ✅ 2026-08-04
> - [x] G6 — Ejecutar gofmt, tests focalizados, go test ./... y lint definido por el repo #owner/agent #type/dev #area/meli #app/search-api-go ✅ 2026-08-04
> - [x] G7 — Dejar diff listo para revisión con evidencia de no cambio de contrato y no regresión de PREVIOUS_PRICE #owner/agent #type/pr-review #area/meli #app/search-api-go ✅ 2026-08-04
> - [ ] G8 — Coordinar deploy antes del backfill; si el atributo ya fue producido, documentar y ejecutar reprocess del universo afectado #owner/agent #type/admin #area/meli #app/search-api-go #waiting
> - [ ] G9 — Validar en respuesta real que item.attributes contiene PRICE_HIGHLIGHT_TIER #owner/agent #type/dev #area/meli #app/search-api-go #waiting

## 🧪 Criterios de aceptación

- VERY_LOW, LOW y NORMAL sobreviven SetAttrAndTags sin transformación.
- Un valor futuro también viaja; Search API no decide visibilidad.
- El atributo queda disponible en SearchAPI.Attributes y en la respuesta.
- PREVIOUS_PRICE y la allowlist existente no cambian.
- No hay nuevos endpoints, contratos, llamadas o infraestructura.
- El cache no queda parcialmente poblado: deploy antes del backfill o reprocess verificado.

## ⚠️ Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| El productor publique antes del deploy y la caché guarde el item sin tier | desplegar primero o reprocessar los items afectados |
| El test cubra solo la allowlist y no el modelo cacheable | agregar cobertura explícita sobre Process.Execute |
| Se agregue interpretación del enum en Search API | conservar contrato genérico y testear valor futuro |

## 🔗 Dependencias

- Productor de PRICE_HIGHLIGHT_TIER en vis-items-loader-tagging.
- [[Destaque de Precio Search — Java Polycard SDK]].
- [[Destaque de Precio Search — Search Middleware]].

## 📆 Bitácora

- **2026-08-04** — Se sincronizó `feature/price-highlight-tier-search-api` con `origin/develop`; se resolvió el conflicto conservando `PRESCRIPTION_TYPE` y `PRICE_HIGHLIGHT_TIER`. El merge commit `3d432c4f16` fue pusheado a origin. `go test ./...` pasa.
- **2026-08-04** — Implementación en rama `feature/price-highlight-tier-search-api`: allowlist actualizada, pruebas de `VERY_LOW`, `LOW`, `NORMAL` y valor futuro, y prueba de propagación a `SearchAPI.Attributes`. Tests focalizados de `entity` y `usecase` pasan.
- **2026-08-04** — A partir de la revisión de `SHORT_VERSION`, se replica el cambio en `process/transformations.go` y `transformations_test.go`. `FilterAttributes` no tiene callers productivos en la baseline; se mantiene alineado sin alterar el flujo.
- **2026-08-04** — Revisión final de los cuatro puntos de allowlist: `go test ./internal/support/item/core/entity ./internal/support/item/core/usecase ./internal/support/item/core/usecase/process` y `go test ./...` pasan.
- **2026-08-04** — Se generó `descripcion_pr.md` respetando el template del repositorio, con flujo, validaciones, curl seguro para test y pendientes operativos de deploy/backfill.
- **2026-08-04** — Validación final: `go test ./...` pasa y `git diff --check` no reporta errores. `golangci-lint` no está instalado (`command not found`), por lo que queda como pendiente del entorno/CI. Diff limitado a allowlist y tests; no se cambió el contrato de `PREVIOUS_PRICE` ni se creó infraestructura nueva.
- **2026-08-04** — Graphify reindexado y la consulta canónica relaciona `search-api-go` con este proyecto y [[Cierre VIS]]. La consulta por el alias de repositorio queda limitada a la búsqueda textual del frontmatter.
- **2026-08-04** — Se retoma el proyecto: se ubicó `~/fuentes/search-api-go`, `develop` está en `414d5f3bf4` con archivos locales no trackeados preservados, y se registró la aplicación en el vault.
- **2026-08-04** — Proyecto creado desde el scan de develop. Se confirma que el cambio mínimo es la allowlist de SetAttrAndTags; el consumer y las capas de caché existentes se reutilizan.

## 🧭 Decisiones

- Search API transporta el atributo sin interpretarlo.
- El deploy debe preceder al backfill; si no, el reprocess es parte obligatoria del rollout.
- No se incorpora filtrabilidad en este alcance.

## 🔗 Docs / Links

- [Spec técnica VMDEM-22](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-22)
- [Spec funcional VMDEM-21](https://spellbook.adminml.com/projects/VMDEM/specs/VMDEM-21)
- [[Cierre VIS]]
- [[Destaque de Precio Search — Java Polycard SDK]]
- [[Destaque de Precio Search — Search Middleware]]
