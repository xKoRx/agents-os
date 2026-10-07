---
type: change_log
schema_version: 1
scope: session
created: "2026-10-07"
updated: "2026-10-07"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities: []
related:
  - "[[2026-10-07-codex-gpt-6-playmaker-pr1275-routing-review]]"
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
---

# Playmaker — Routing y descripción PR #1275

## Cambio

- **Tipo:** updated / conflict-resolution.
- **Archivos:** ConnectorActionData y dos suites, runner de contrato, manifiesto, arquitectura/escenarios, cuerpo GitHub y nota canónica. Merge conserva los archivos upstream #1270.

## Motivo

- El usuario pidió explicación ejecutiva, cuerpo de PR claro y atención de comentarios nuevos. El P2 detecta resolución innecesaria de Kafka para pause/resume; el bot repite D27, que se conserva por decisión del usuario. Develop avanzó durante la verificación y generó otro conflicto.

## Fuentes usadas

- PR #1275 comentarios 4209736054 y 4209562841, source de Playmaker/CP, base a4e2829ad y evidencia local reproducible.

## Resolución aplicada

- Fix 0a5a01f76: extraer sólo routing persistido y luego resolver referencias, manteniendo binding del target autorizado. HTTP/H2 demuestra 202 con referencia ajena no running y 409 cuando la referencia faltante es requerida por routing. Runner ejecuta siempre tests productores para materializar fixtures propios.
- Merge 526c1115c: unir escenarios del manifiesto, conservar 93 selectores y adoptar #1270 sin ampliar el diff del PR. Los 21 archivos de código/config/script del PR quedan idénticos al fix validado.
- Descripción ejecutiva publicada y verificada; scope Fury/ACME/lifecycle separado de ClickHouse adicional, Swagger y runner de pruebas. Import timeout explícitamente fuera de lo resuelto. Replies nuevas publicadas y verificadas.

## Validación

- 93 selectores y full 4.703 tests PASS; cero fallas/errores, dos skips; JaCoCo 97,24%, helper strict-local 97,01%. Contrato fresco: 36 HTTP/H2 + seis handlers reales, cleanup certificado. Hooks y validadores PASS; GitHub MERGEABLE. CI #6029: cinco checks SUCCESS; PR coverage 97,72%, helper 97,01% y overall MeliCov 94,92%.
- Stack MySQL falló; cleanup de rio-playmaker-agentic-34015 y rio-playmaker-agentic-48924 certificado, sin recursos propios remanentes. Loopback/Kafka, L1 y F1 pendientes. Versión previa no incluye los fixes.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** evidencia sanitizada, sin payloads reales, credenciales ni secretos.

## Rollback

- Revert del fix 0a5a01f76; si se requiere retirar la integración, revert del merge 526c1115c contra su primer padre. Sin force-push ni cleanup de recursos ajenos.

- Code Reviewer terminó NEUTRAL y repitió D27 en comentario 4210366310; respondido con la política acordada y link al reply anterior: [4210381147](https://github.com/melisource/fury_rio-playmaker/pull/1275#discussion_r4210381147). No nuevo comentario humano ni cambio de código.
