---
type: learning
schema_version: 1
scope: application
created: "2026-10-13"
updated: "2026-10-13"
area: "[[Meli]]"
project: "[[RIO E2E local]]"
application: "[[rio-playmaker]]"
entities: ["[[rio-playmaker]]"]
related: ["[[RIO E2E local — Diseño revisado]]"]
aliases: []
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
---

# Playmaker — Publicar ambos ledgers antes de entregar señales

## Aprendizaje

En el launcher local de Playmaker, state.json e identity.json deben quedar iguales y con sus permisos finales antes de entregar SIGINT/SIGTERM/SIGHUP pendientes. Diferir señales sólo en el bootstrap inicial no protege el segundo save, que ocurre después de crear Compose y retener el proceso Playmaker. Una interrupción entre escrituras hace que load rechace el par y bloquea el teardown de recursos propios.

La región protegida debe abarcar ambas escrituras y sus chmod, usando el deferral existente dentro de save. La entrega posterior conserva los guards de ownership y el orden drain→Compose-down. Probar señales reales enviadas por otro proceso en las fronteras tardías y recoger los oráculos antes del cleanup de emergencia; no basta lanzar un InterruptedError antes de save.

## Aplicabilidad

- **Cuándo cargarlo:** al cambiar save, startup, handlers de señales o teardown del orquestador local que mantiene los dos ledgers.
- **Cuándo no cargarlo:** para afirmar atomicidad ante SIGKILL, caída de máquina, error de disco o escritores concurrentes. La máscara corresponde al CLI de un solo hilo; no sustituye los guards ni autoriza teardown desde un ledger parcial.

## Entidades relacionadas

[[rio-playmaker]] y [[RIO E2E local]].

## Evidencia

- [[2026-10-13-rio-e2e-local-pr-comments]] — fuente354f9d RED:8 fallos entre10 TERM/HUP; fix GREEN launcher26tests, child real y frontera Docker controlada, ledger0400/igual y cero marcadores/proceso/state antes de fallback.
- [Comentario4263209136](https://github.com/melisource/fury_rio-playmaker/pull/1286#discussion_r4263209136) y regresión permanente LateLedgerSignalTests en local/tests/test_rio_e2e_launcher.py.
