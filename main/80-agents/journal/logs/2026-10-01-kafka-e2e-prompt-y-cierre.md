---
type: change_log
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Meli]]"
project: "[[Kafka — Ambiente local con servicios reales]]"
application: "[[rio-controlplane-kafka]]"
entities: ["[[Kafka — Ambiente local con servicios reales]]"]
related: ["[[Prompt maestro — E2E completo de CP Kafka]]"]
aliases: []
confidence: verified
source_session: "01a0f494-bc08-75d0-8908-85b45ae72c45"
source_feedbacks: ["[[2026-10-01-kafka-local-e2e-session-feedback]]"]
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Kafka — Prompt maestro E2E y cierre AGENTS OS

## Cambio

- **Tipo:** created + updated.
- **Archivo(s):**
  - [[Prompt maestro — E2E completo de CP Kafka]] y proyecto [[Kafka — Ambiente local con servicios reales]].
  - [[2026-10-01-kafka-local-e2e-session-feedback]] y [[2026-10-01-codex-unknown-kafka-local-runtime]].

## Motivo

- El owner pidió un prompt maestro para un agente ejecutor que entregue E2E completos OK/falla, se especialice en Kafka CP, use subagentes, optimice tokens y complete la documentación de ads-signals-knowledge-library. Solicitó además cierre AGENTS OS y feedback.

## Fuentes usadas

- Solicitud del owner, decisión de KVS real Fury Sandbox y fuentes ya persistidas del proyecto.
- [[Kafka local — Historia y prueba de arranque (2026-10-01)]].
- AGENTS.md y routing/context pack de `ads-signals-knowledge-library@de7cde85f7dd83a673c918e22ae9f08a0f7e05bd`, sólo para orientar el encargo; no se realizó la auditoría documental completa.
- Skills canónicas de session-close, session-feedback y agent-run-register.

## Resolución aplicada

- Se materializó un recurso con prompt copiable, cobertura mínima ampliable desde código, baselines a revalidar, estrategia de subagentes, pruebas físicas y criterios de terminado.
- Se actualizó la continuidad del proyecto: prompt entregado y próximo paso de ejecución. La implementación de E2E y los cambios a la library siguen pendientes.
- Se registró la ejecución de depuración/pruebas como Codex × unknown, con evidencia parcial y sin inferir el modelo.
- Se dejó feedback crítico sobre comunicación de alcance, selección de skills y ruido/contexto. No se duplicaron hechos de fuentes/wiki en nuevas memorias públicas ni se crearon raw/summary por ritual.

## Validación

- Lint estricto dirigido de los cinco paths tocados: ERROR=0, WARN=0, notes_scanned=5.
- Graphify recuperó exactamente un recurso por el alias `Prompt Kafka E2E`; el índice derivado se actualizó. El lint global reportó deuda ajena a estos cinco paths y permitió continuar el auto-refresh local; esa deuda no se modificó durante el cierre.
- No se ejecutaron nuevas pruebas de producto durante este cierre. La implementación E2E sigue como próximo trabajo del proyecto.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos, payloads productivos completos, logs masivos ni paths absolutos de máquina. El ID externo vive sólo en source_session.

## Rollback

- Retirar el prompt y revertir los cambios de continuidad de esta iteración mediante un cambio registrado; conservar evidencia de investigación/pruebas previas y el historial de feedback/ejecución.
