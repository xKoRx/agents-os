---
type: change_log
schema_version: 1
scope: session
created: "2026-08-11"
updated: "2026-08-11"
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
application:
entities:
  - "[[deploy-request-path]]"
  - "[[system-map]]"
  - "[[rio-playmaker]]"
  - "[[rio-materializer]]"
  - "[[ads-signals-frontend]]"
related:
  - "[[30-resources/rio-atlas/00-index]]"
  - "[[deploy-component]]"
  - "[[signals-context-flow]]"
  - "[[Crear Context]]"
aliases:
  - deploy request path journey
  - corrección transporte trigger BigQueue
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
  - area/meli
  - change/created
  - change/updated
---

# Journey del camino de un request de deploy + corrección de transporte del trigger

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s) creados:**
  - `30-resources/rio-atlas/journeys/deploy-request-path.md` (resource, active) — diagrama de secuencia end-to-end + fork de ruteo a materializer, con provenance file:line.
  - `30-resources/rio-atlas/log.md` (bitácora del dominio Atlas, antes vacía).
- **Archivo(s) actualizados:**
  - `30-resources/rio-atlas/architecture/system-map.md` → resueltas las 2 preguntas abiertas (transporte del trigger y orden del fan-out); `updated`/`last_verified` → 2026-08-11.
  - `30-resources/rio-atlas/00-index.md` → nueva fila, "de un vistazo" (5 vistas), salud (contradicción de transporte reconciliada).
  - `10-projects/Meli/Onboarding Signals/Onboarding Signals.md` → bitácora (8).
  - `10-projects/Meli/Crear Context/Crear Context.md` → bitácora (punto de intervención confirmado).

## Motivo

- Onboarding Signals: entender qué pasa cuando el front manda a deployar a playmaker (servicio, endpoint, qué genera, quién reacciona, si llega a materializer) y dejarlo como contexto durable + diagrama.
- Insumo directo de [[Crear Context]] (dónde intervenir para mover la lógica de contrato del front al backend; futuro CLI dummy).

## Fuentes usadas

- Discovery de primera mano en código local (2026-08-11) de los repos en `~/fuentes`: `rio-playmaker`, `ads-signals-frontend`, `rio-frontend`, `rio-materializer`, CPs y `rio-sdk-events`.
- Evidencia clave: `PipelineDeploymentController.java:88`, `DeploymentServiceImpl.java:691,860,919-937,957`, `DeploymentRoutingConfig.java:50`, `DeploymentTriggerProducerImpl.java:32-45`, `DeploymentResultConsumerController.java:45`, `DeploymentResultHandlerImpl.java:387,389`, `application.yml:162-197`, `application-production.yml:25-27,67,68`; front `useDeployPipeline.ts:441`, `api/pipeline/index.ts:91-130`.

## Resolución aplicada

- **Corrección de modelo (contradicción resuelta):** el trigger de deploy **no** viaja por HTTP POST directo al CP (como decía system-map); se publica a **BigQueue `rio-deployment-trigger`** y la cola entrega por **HTTP push** al controller del CP. Reconciliado: la cola es el transporte, el POST su mecanismo de entrega.
- **Ruteo table-driven:** el "fan-out" es fork por tipo de componente (`routingConfig` en `application.yml`): tipos modernos → BigQueue→CP directo; catch-all `*/*` → `MATERIALIZER_REST` (catalog/signal + no listados) → [[rio-materializer]] (en deprecación).

## Validación

- Nueva página con frontmatter conforme (materializada vía `materialize_schema_note.py`), enlazada desde [[00-index]] y desde las 4 vistas del Atlas.
- Sin huérfanos: enlazada desde índice, system-map, deploy-component, signals-context-flow y ambos proyectos.
- Diagramas Mermaid (sequence + flowchart) con sintaxis válida.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, secretos ni dumps de código; solo firmas/paths y contrato.

## Rollback

- Archivar `deploy-request-path.md`, revertir la sección "Límites" y las fechas de `system-map.md`, quitar la fila de `00-index.md`, revertir las líneas de bitácora en ambos proyectos y la entrada de `log.md`. Conservar este log como auditoría.
