---
type: area
schema_version: 1
status: active
icon: 📈
slug: trading
banner: "[[banner-trading.png]]"
desc: Operativa, prop firms, journal y riesgo
tags:
  - area/trading
  - kind/area
review: weekly
created: 2026-06-23
updated: "2026-10-27"
aliases:
  - trading
---

![[banner-trading.png]]

> [!abstract]+ 📈 Trading
> Mi operativa y aprendizaje en trading: estrategias, journal, recursos y seguimiento.

## 🎯 Objetivo

Mantener la operativa, aprendizaje, control de riesgo y desarrollo de estrategias de trading con evidencia. La investigación de Echo se coordina desde [[Echo — I+D de Estrategias]], con líneas Forex/CFD y Futures.


## 📊 Estado actual

Programa único de I+D Echo organizado desde el 2026-10-27. Los planners de cada mercado conservan cobertura, estado y próximos trabajos; esta área sólo los enlaza.


## 🟢 Proyectos de esta área

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Proyectos
    order:
      - file.name
      - note.status
```

## 📚 Recursos de esta área

```base
filters:
  and:
    - 'type == "resource"'
    - 'file.hasLink(this.file)'
views:
  - type: table
    name: Recursos
    order:
      - file.name
      - note.status
```

## ✅ Tareas abiertas

```tasks
sort by priority
not done
tags include #area/trading
short mode
hide task count
```

## 🧭 Decisiones relevantes

- [[Echo — I+D de Estrategias]] concentra el gobierno de investigación; los proyectos de producto/infraestructura mantienen sus owners y gates.


## 🔗 Links

- [[Echo — I+D de Estrategias]] — entrada global.
- [[Estrategias IMOX — Forex y CFD con Echo Forge]] / [[Echo I+D — Futures]] — managers de mercado.
- [[Echo I+D — Mapa de capacidades]] — skills, agentes y runbooks por responsabilidad.

