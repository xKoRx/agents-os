---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# 06 — Diagramas visuales

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28 vía `agent-read all`
> **Generado**: 2026-06-30

## 📑 Contenido

| Doc | Tipo | Descripción |
|---|---|---|
| [[topologia-completa]] | Mermaid | Diagrama lógico completo del cluster (nodos, Ceph, storage, servicios clave) |

---

## 🎨 Tipos de diagramas en este folder

- **Mermaid**: soportado nativamente por Obsidian ✅
- **SVG handcrafted**: si necesitas alta calidad visual — fuera del scope de esta documentación inicial

## 📐 Diagramas embebidos en otros docs

Para no duplicar, varios docs ya tienen sus propios diagramas mermaid:

| Doc | Diagrama |
|---|---|
| [[../00-index]] | Cluster at-a-glance (status, total cores/RAM) |
| [[../01-topologia/README]] | Diagrama lógico + físico (ASCII) |
| [[../01-topologia/diagrama-red]] | Red: routers, switches, VLANs, subnets |
| [[../02-servicios/README]] | Dependencias cross-service |
| [[../03-storage/README]] | Mapa lógico de storages |

> Para más diagramas específicos (servicios individuales, Ceph detail, network flows), ejecutar Task 2 (auditoría profesional) o pedir a Rodrigo ampliaciones.

## 🛠️ Cómo agregar más diagramas

```bash
# Crear archivo nuevo en /home/hermes/obsidian/SecondBrain/main/30-resources/aranea/06-diagramas/
# Usar bloques mermaid con sintaxis estándar:

\`\`\`mermaid
flowchart TB
    A[athena] -->|Ceph cluster network| B[zeus]
    ...
\`\`\`

# Tipos soportados en Obsidian: flowchart, sequenceDiagram, classDiagram, 
# stateDiagram, erDiagram, gantt, pie, journey
```

---

## Source files

- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260628_211812.txt`
- `/home/hermes/aranea/topology/README.md`
- `/home/hermes/aranea/topology/services.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
