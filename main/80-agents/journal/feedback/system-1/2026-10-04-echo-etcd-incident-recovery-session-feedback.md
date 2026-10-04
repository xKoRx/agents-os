---
type: feedback
schema_version: 1
scope: session
created: "2026-10-04"
updated: "2026-10-04"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run:
session_goal: "Recuperación mínima del incidente ETCD de producción (BT-S03)"
source_session:
confidence: verified
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback — INC-ETCD-20261004 — recuperación y falla de aislamiento

## Context

Cierre del incidente abierto en [[Echo Futures — BT-S03 Adversarial Review]]. Forense read-only (historia MVCC del cluster ETCD vía API HTTP v3, sin etcdctl) demostró que el write masivo fue byte-idéntico al estado vigente salvo `postgres/password`, restaurado por CAS probado con auth física. Reporte completo: `10-projects/Echo Futures/artifacts/incidents/2026-10-04-bt-s03-etcd-production-incident.md`.

## Scores

Startup clarity 5/5; retrieval usefulness 4/5; skill fit 5/5; prevención de efectos externos 1/5 (sigue la deuda del incidente fuente); confianza operativa global 4/5.

## What Complicated The Session Most

El SDK `v3/sdk/etcd` resuelve por defecto al cluster ETCD de producción (`192.168.31.250-254:2379`, mismos endpoints que `deploy-prod.sh`): cualquier proceso Go que importe el SDK sin `ETCD_ENDPOINTS` alcanza producción. Además `TestSeedEchoConfig_{Development,Production}` corren sin build tag ni env guard dentro de `go test ./...`. No hay audit log ETCD para atribuir escritores: los bursts periódicos previos (que re-escriben el namespace con el placeholder) no son atribuibles desde el cluster.

## Most Useful Part Of Sistema 1

La constitución (preservar cambios ajenos, fallar cerrado, no asumir pre-image) y la continuidad global (leer estado durable antes de repetir efectos) encajaron 1:1 con el mandato de no-rollback-cego. El gotcha del MCP etcd fuzzy-read ya registrado evitó confiar en lecturas no exactas.

## Pain Pattern Candidate

Severidad high; recurrencia confirmada (bursts repetidos del seed antes del incidente). Candidato: side-effect tests sin guard + defaults de conexión que apuntan a producción = todo `go test ./...` de SDK es un write a producción latente. La prohibición textual no basta (ya falló en S03): el guard debe vivir en el test (build tag `seeds` + env/endpoint guard), recomendación ya dejada para S04 en el reporte del incidente.

## One Next Improvement

Aplicar en S04 el prevention fix del seed (build tag + guards) y fijar el credential real en la fuente que re-materializa `/echo/production/`; mientras exista el re-materializador, el password restaurado puede volver a ser clobbered en el próximo burst.
