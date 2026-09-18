---
type: feedback
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
  - "[[Echo Forge]]"
related:
  - "[[aranea-minio-mcp]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: account:zai-individual-coding-plan/GLM-5.3-Flash
agent_run: "[[2026-09-18-zcode-glm-5.3-flash-e06-t21-sqx-object-owner-action]]"
session_goal: Identificar el objeto SQX real de T21 con provenance durable y preparar la solicitud owner-gated
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/echo
---

# Session Feedback - 2026-09-18 - e06-t21-sqx-provenance-digest

## Context

- Agent surface: [[ZCode]] · model host-reported `account:zai-individual-coding-plan/GLM-5.3-Flash`
- Session goal: identificar el objeto SQX real (key exacta, provenance, permiso vigente), agotar rutas autorizadas, preparar solicitud owner para T21
- Artifacts changed: repo xKoRx/echo docs (`9f3ccc2b`, push FF), owner-action en `~/aranea/work/e06-t21-owner-action/`, entidad E-06, agent_run, change_log, este feedback

## What Complicated The Session Most

- Causa: imprecisión de provenance heredada — los registros C5/C6 del backlog y los bullets del vault citaban el MQ5 de RERUN-3 como «282575 B `sha256:f8968dba…`», pero `f8968dba…` es el segmento del key (digest de la fuente de export); el record durable del propio uploader (`mt5_exporter`, resultado de actividad en Temporal) registra el SHA256 de los bytes como `6c598d79…`.
- Impacto: la identidad byte exacta del objeto requerido por la solicitud owner quedó ambigua hasta re-derivar la provenance desde la evidencia durable (scratch Temporal); el fetch definitivo es el único resolutor (verificación SHA256 obligatoria antes de uso).
- Mejora concreta: al citar artefactos durables, tomar el digest desde el record del uploader/actividad (resultado de actividad en el workflow history), no desde el segmento `sha256:…` del key — el key puede codificar el digest de otra entidad (fuente, no objeto). Corregido en VERIFICATION «T21 PRERREQUISITO», nota E-06 y owner-action.

## Secondary Friction

- Causa: la réplica Mongo Forge RO está vacía para `strategy_state`/`strategy_metadata`/`ea_exports` (coherente con el `-32003` ya documentado en el backlog) y no existe copia residual de los artefactos del funnel en los hosts SQX (workspaces limpiados por el pipeline).
- Impacto: toda la provenance del objeto se tuvo que re-derivar del historial Temporal (`/tmp/thist`, canal CLI pre-autorizado por R1).
- Mejora concreta: considerar registrar en el runbook MinIO/access la receta de provenance de artefactos (resultados de actividad del funnel en ns `sqx-prop`) como ruta canónica de metadata cuando las superficies de lectura de bytes están owner-gated.
