---
type: change_log
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
application: "[[RIO]]"
entities:
  - "[[RIO]]"
  - "[[agent-constitution]]"
  - "[[rjara-agent-profile]]"
related:
  - "[[2026-08-10-signals-onboarding-rio-umbrella-and-agents-md]]"
  - "[[30-resources/00-RESOURCE-WIKI|Resource Wiki]]"
aliases: []
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
---

# RIO: deep-dive de 10 apps + corte estable/volátil en LLM Wiki

## Cambio

- **Tipo:** updated (Sistema 2 — ingest wiki)
  - `30-resources/applications/rio-*.md` (las 10) reescritas con el corte estable/volátil, evidencia de código y provenance (`last_verified`, `confidence`). Ejecutado por 10 subagentes en paralelo, consolidado por el agente principal.
  - `30-resources/applications/RIO.md` — nota paraguas actualizada al mismo corte.
  - `30-resources/applications/00-index.md` y `log.md` — catálogo y bitácora al día.
- **Tipo:** updated (Sistema 1 — convención LLM Wiki)
  - `70-templates/application.md` y `70-templates/service.md` — ahora nacen con secciones estable vs volátil + campos `last_verified`/`confidence`.
  - `30-resources/00-RESOURCE-WIKI.md` — regla dura del corte estable/volátil.
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md` — directiva `[FUERTE]`: toda documentación pasa por `agents-os-resource-wiki`.

## Motivo

- Onboarding Signals: dejar las 10 apps RIO documentadas con mira global y contexto durable para agentes, sin exceso de tokens. El usuario pidió el mecanismo LLM Wiki siempre y distinguir información persistente de temporal ("playmaker ES orquestador" vs "usa X librería").

## Hallazgos relevantes

- [[rio-controlplane-signals]]: scaffold inicial (`.fury` = `template-java-graddle-web`).
- [[rio-controlplane-fury]]: Kotlin (no Java); reconciler tipo k8s-controller.
- [[rio-materializer]]: motor real de materialización multi-infra (CQRS legacy + DDD/sagas).
- Deps corregidas contra código (clickhouse→materializer; kafka reemplaza legacy de materializer).
- Drift doc↔código en varios README (scaffold vs build.gradle) y en [[rio-sdk-events]] (2 dominios vs paquetes reales).

## Próximo paso

- Analizar el grafo mergeado `graphify-signals.json` (deps cross-app) y extraer contexto de los 3 canales de Slack (ver [[Onboarding Signals]]).
