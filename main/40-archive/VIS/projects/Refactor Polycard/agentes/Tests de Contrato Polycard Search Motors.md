---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Refactor Polycard]]"
sprint: "[[A26Q2S7]]"
start: 2026-07-10
due:
progress: 80
repo: search-middleware, java-polycard-sdk
jira:
prs:
aliases:
  - feature/mot-perform-polycard-contract-tests
  - Motors Polycard contract tests
tags:
  - project
  - area/meli
  - feature/refactor-polycard
  - app/search-middleware
  - app/java-polycard-sdk
created: "2026-07-10"
updated: "2026-07-10"
---

# Tests de Contrato Polycard Search Motors

%% Proyecto de agente para asegurar el contrato visual/estructural de las cards Motors de Search y mantener alineados los escenarios de la SDK. %%

> [!info]+ Tests de Contrato Polycard Search Motors
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> **Parent:** [[Refactor Polycard]] · **Repos:** [[search-middleware]] · [[java-polycard-sdk]]
> **Rama Search:** `feature/mot-perform-polycard-contract-tests`

## 🎯 Objetivo

- Asegurar que las cards Motors de Search mantengan orden, presencia, contenido y payload de componentes Polycard para los caminos orgánico y Ads/VIS, incluyendo B2C y B2C verificado.
- Mantener los tests adaptados a los contratos vigentes de `develop` sin modificar código productivo.

## 📊 Estado actual

- La rama se sincronizó con `develop` y el merge quedó sin conflictos.
- Se actualizaron los tests al contrato `AdvertisingPadsModel`/`advertisingPads` y a la carga multi-site de `StateAbbreviationService`.
- Validación completa de Search: 2.188 suites, 34.552 tests, 46 ignorados, 0 fallos y 0 errores.
- El caso B2C de referencia queda cubierto con golden JSON, `approved_credit`, labels, ubicación, título/subtítulo/precio; B2C verificado agrega `float_highlight` de vehículo verificado.

## ✅ Tareas

- [x] Sincronizar `develop` local con `git pull` y hacer merge simple en la feature #owner/agent #type/dev #area/meli ✅ 2026-07-10
- [x] Actualizar tests y fixtures de contratos Motors Search tras los cambios de `develop` #owner/agent #type/dev #area/meli ✅ 2026-07-10
- [x] Ejecutar tests focales de Organic, Ads/VIS y wiring Motors #owner/agent #type/dev #area/meli ✅ 2026-07-10
- [x] Ejecutar suite completa de tests de Search #owner/agent #type/dev #area/meli ✅ 2026-07-10
- [ ] Extender los escenarios equivalentes a los DDT (Data-Driven Tests) de `java-polycard-sdk` y validarlos en DDT Studio, su frontend local de inspección visual #owner/agent #type/dev #area/meli #waiting

## 📆 Bitácora

- **2026-07-10** — Proyecto creado y asociado a [[Refactor Polycard]] para registrar la feature `feature/mot-perform-polycard-contract-tests`.
- **2026-07-10** — Merge de `develop` sin conflictos; tests adaptados a `AdvertisingPadsModel` y `StateAbbreviationService.loadAllSiteFiles(...)`. Suite completa en verde.
- **2026-07-10** — Confirmado que la tarea pendiente de SDK corresponde a DDT y su frontend local DDT Studio.

## 🧭 Decisiones

- Las pruebas validan el contrato observable de la card (orden, componentes, textos, valores y golden JSON); no se altera código productivo para hacerlas pasar.
- La tarea de SDK queda separada porque requiere trabajar en `java-polycard-sdk` y validar los escenarios DDT/visualización en DDT Studio.

## 🔗 Docs / Links

- [[Refactor Polycard]]
- [[search-middleware]]
- [[java-polycard-sdk]]
- `docs/guide/testing/ddt.md` en `java-polycard-sdk`
- `README.md` — sección DDT Studio en `java-polycard-sdk`
