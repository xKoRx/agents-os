---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application: "[[ads-signals-frontend]]"
entities:
  - "[[Estandarización de Scopes RIO]]"
  - "[[ads-signals-frontend]]"
  - "[[RIO]]"
related:
  - "[[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]]"
aliases:
  - rio frontend scope routing plan and spec
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-16-rio-frontend-scope-routing-plan-and-spec

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated + skill refinement
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing dinámico de backend en ads-signals-frontend.md` — nueva SPEC técnica de la Fase 1.
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md` — plan maestro actualizado para separar ejecución de diseño y adoptar la Fase 1.
  - `30-resources/agents/skills/signals-tech-spec-authoring/SKILL.md` — regla reusable de frontera proyecto vs SPEC técnica.

## Motivo

- Preparar la primera implementación de la POC de scopes RIO con una entrada test compartida de Playmaker, selección backend dinámica y prohibición de cruces test/prod.
- Evitar que el proyecto y la SPEC mantengan copias divergentes del mismo diseño. La skill no definía qué artefacto debía poseer planificación/estado versus arquitectura/contratos.

## Fuentes usadas

- Decisiones explícitas del owner en la sesión: MeliLab/Nordic define el scope frontend y el backend por default; `backend` sobreescribe sólo backend; routing por header únicamente en test; producción no lleva scope; Fury Routes será configurado por el owner; no se permiten cruces test/prod.
- `ads-signals-frontend` `develop@7a9296cb`: `frontend-config`, `frontend-env`, configuraciones production, `app/server/index.ts`, `api/index.ts`, `api/lib/playmaker.ts`, caches y stores persistidos.
- `meli-frontender-web` v2.10.1: detector sobre `.fury` válido (`ads-signals-frontend`) resolvió Odin 9.3.2, Nordic 9 y Andes 9.8.0; referencias Nordic de config, env, Ragnar, RestClient y seguridad.
- `30-resources/agents/skills/signals-tech-spec-authoring/SKILL.md`, `signals-func-spec-authoring/references/que-es-una-spec.md` y SPECs técnicas vivas de SIG-616.
- `80-agents/skills/agents-os-skill-authoring/SKILL.md`, su runbook y `skill-contract.md` para refinar la skill sin introducir un segundo artefacto de policy.

## Resolución aplicada

- El proyecto queda como autoridad del plan: fases, owners, dependencias, gates, tareas, estado y evidencia de cierre.
- La SPEC queda como autoridad del diseño: contratos, arquitectura, decisiones, errores, archivos, tests y rollout.
- La Fase 1 usa el cliente `playmaker(req)` existente como seam, un host test compartido y `X-Rio-Scope`; no incorpora catálogo semántico de scopes en el frontend.
- El cliente usa `meliDomain` estático en Fury y reserva `baseURL` para localhost; el scope nunca se concatena a una URL.
- La skill técnica ahora obliga a enlazar proyecto y SPEC y a eliminar duplicación según la autoridad de cada artefacto.

## Corrección posterior a review

- Se descartó retirar los archivos `test2/test3/beta/staging-production.js`: contienen catálogo de templates y, por herencia, diferencias de Entity Service/Kraken que esta fase no debe cambiar. La configuración compartida proyecta sólo las claves de routing de Playmaker.
- Se explicitó que el override no cambia `playmaker_component_templates` ni `rio_entity_service_base_url`; la compatibilidad de templates entre el frontend y el backend elegido es gate de certificación, no validación semántica del frontend.
- Se mantuvo `meliDomain` para dominios internos en Fury por el contrato Nordic, pero se acotó el cambio: `baseURL` sigue gobernando fuera de Fury/local para evitar el desvío a `melioffice.com`. La seguridad deriva del destino estático, no del nombre de la opción.
- Se conservó el reset de `page.store.ts` porque contiene IDs, drafts y estado de mutación ligados al backend; se eliminó `ui.store.ts` del alcance y se mantuvieron como obligatorios los caches server-side y el namespace de `deploySessionStore`.
- Se agregó el invariante `allowRepeatedParams: true`, el import explícito/proyección de `test-production.js`, la defensa particular de `staging` y el orden de merge de `frontend-config`.
- El proyecto dejó una sola fuente para el contrato Fury, actualizó el catálogo canónico y marcó la remediación KMS como vencida y bloqueada hasta revalidar fecha/estado.

## Validación

- `validate_schema_contract.py --type doc` y `--type change_log`: 0 errores.
- `lint.py --strict` sobre proyecto, SPEC, skill y change log: `ERROR=0 WARN=0`.
- Frontmatter de la skill parseado con Ruby/Psych: PASS; el `quick_validate.py` portable se ejecutó con PyYAML y produjo la incompatibilidad esperada por `skill-contract.md` al rechazar los campos federados `type`, `scope`, lifecycle, routing y tags.
- Regla del lector cero sobre la SPEC: 0 coincidencias; tamaño final dentro de la calibración de un repo.
- Activación de la skill: positiva PASS — redactar SPEC técnica Signals con proyecto asociado; negativa PASS — actualizar sólo progreso/tareas pertenece a entity update; adyacente PASS — requisitos `RF/CA/E2E` pertenecen a `signals-func-spec-authoring`.
- Referencias canónicas `[[Estandarización de Scopes RIO]]`, `[[ads-signals-frontend]]`, `[[RIO]]` y la nueva SPEC resueltas en el vault.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin secretos, tokens, cookies reales ni rutas absolutas persistidas; los paths de repo son relativos.

## Rollback

- Revertir conjuntamente la nueva SPEC, el bloque de Fase 1 del proyecto y la regla de separación de la skill. No hay cambios de código ni infraestructura en esta operación documental.
