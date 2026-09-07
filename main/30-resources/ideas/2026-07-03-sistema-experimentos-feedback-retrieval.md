---
type: idea
status: seed
priority: P3
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[token-economy-indexing-architecture]]"
  - "[[graphify]]"
visibility: public
governed_by: user
promotion_target:
source:
aliases:
  - sistema de experimentos de retrieval
  - experiments + feedback loop
tags:
  - kind/idea
  - area/personal
  - project/agents-os
  - idea/research
  - size/large
created: 2026-07-03
updated: 2026-07-03
---

# 💡 Sistema de experimentos + feedback para el retrieval

> [!tip]+ Sistema de experimentos + feedback
> _Idea en bruto. NO implementar aún — el owner lo dejó explícitamente como idea para
> no irse por la tangente del proyecto principal (arquitectura de indexación)._

## 🧠 La idea

- Un sistema completo donde se puedan **agregar notas de experimentos** (probar una
  forma de indexar/consultar), que esas notas **se integren al funcionamiento del
  agente** (el agente corre el experimento), y que luego el **agente entregue feedback
  en base al resultado** (qué tokens gastó, si acertó el retrieval, qué sobró/faltó).
- Cierra el loop: experimento → ejecución del agente → medición → feedback → ajuste de
  las capas de indexación.

## 🎯 Motivo / por qué

- Darle **rigor medible** al proyecto de economía de tokens: no "creo que ahorra", sino
  "mido que ahorra". Base natural: `graphify benchmark` + conteo de tokens por query +
  el sistema de `journal/feedback/` y `agents-os-kaizen-memory` que ya existen.

## 🧭 Routing

- **Área:** [[Personal]]
- **Proyecto:** [[AGENTS OS]]
- **Entidades:** [[AGENTS OS]]

## 🏷️ Clasificación

- **Tamaño:** large
- **Tipo:** research
- **Prioridad:** P3
- **Estado:** seed
- **Visibilidad:** public
- **Gobernada por:** user
- **Criterio de promoción:** promover a proyecto solo cuando la arquitectura de
  indexación (ver [[token-economy-indexing-architecture]]) esté estable y validada.

## 🔗 Relacionado

- [[token-economy-indexing-architecture]] — el proyecto principal que esto mediría.

## 🌱 Próximo paso

- [ ] No accionar todavía; revisitar cuando el sistema de indexación esté armado #owner/me #type/research #area/personal
