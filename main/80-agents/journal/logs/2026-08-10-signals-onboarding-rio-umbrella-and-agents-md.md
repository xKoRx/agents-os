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
  - "[[Onboarding Signals]]"
  - "[[data-mesh]]"
related:
  - "[[2026-08-10-rio-applications-created]]"
  - "[[2026-08-10-rio-sources-relocated-no-repos-in-vault]]"
  - "[[Fuentes — Workspace de repositorios]]"
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

# Signals onboarding: RIO umbrella, data-mesh y AGENTS.md de fuentes

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `~/fuentes/AGENTS.md` (workspace, fuera del vault) — índice operativo de 10 apps + grafos + comandos Graphify.
  - `30-resources/applications/RIO.md` — entidad paraguas (service) de la plataforma RIO.
  - `30-resources/methodologies/data-mesh.md` — digest del artículo de Zhamak Dehghani/Fowler.
  - `10-projects/Meli/Onboarding Signals/Onboarding Signals.md` — proyecto raíz de onboarding (planificador único).
- **Tipo:** updated
  - `30-resources/storage/fuentes-workspace.md` — puntero a `AGENTS.md`, [[RIO]] y [[data-mesh]].

## Motivo

- Rodrigo se traspasa al equipo **Signals** como Sr SWE y necesita mira global desde el minuto 1 de la plataforma RIO (10 apps JVM/Spring/Fury) y dejar el contexto como memoria durable para sus agentes (AGENTS OS).

## Fuentes usadas

- Repos `~/fuentes/rio-*` (README/build.gradle), grafo `graphify-signals.json`.
- https://martinfowler.com/articles/data-monolith-to-mesh.html
- Notas previas: [[2026-08-10-rio-applications-created]], [[2026-08-10-rio-sources-relocated-no-repos-in-vault]].

## Próximo paso

- Deep-dive de las 10 apps (patrones/deps del grafo) y extracción de contexto desde los 3 canales de Slack.
