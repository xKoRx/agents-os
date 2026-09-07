---
type: raw_session
scope: session
created: "2026-07-05"
updated: "2026-07-05"
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[sqx-worker]]"
entities:
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: verified
source_session: "241add91-8048-41f7-b2cd-87470b589ef0"
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# Echo Forge: Unificación de Carpeta Custom en Flujos y Subflujos - Raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Antigravity
- Proyecto o entidad: [[Echo Forge]]
- Objetivo de la sesión: Modificar la config para normalizar el uso de la carpeta `custom` en flujos y subflujos paralelos por tipo lógico en Zeus, configurar grupos de a 1 con límite total de 2 retesteadas y documentar la convención en el repo.

## Transcript

- Se detectó que previamente el worker de Zeus contenía proyectos creados con nombres dinámicos de tipos lógicos y stages (ej. `02_retester_full_EMA...`), causando sobrecarga y polución en los directorios de trabajo.
- Se vaciaron por completo las tablas `databank_metadata`, `type_rankings` y `export_runs` de la base de datos `forge` mediante un script ad-hoc.
- Se actualizó `input/example/config.json` para direccionar todas las tareas de ejecución de StrategyQuant a la carpeta `"custom"` en Zeus, con `batch_size: 1` y parada temprana `top_n_per_logical_type: 2`.
- Se copió el archivo de configuración a la carpeta `input/` de Symphony para gatillar la ejecución del watcher.
- Se observó a través del journal del worker que las subtareas se ejecutaron secuencialmente e independientes sobre el proyecto `custom` en Zeus.
- Se verificó que todas las actividades del pipeline finalizaron de forma 100% exitosa y se poblaron las tablas de MongoDB sin generar colisiones ni crear directorios de proyectos adicionales con nombres de agrupaciones.
- Se actualizó la documentación de `sqx/README.md` y `.agents/skills/echo-forge-testing/SKILL.md` para evitar repetir este antipatrón en el futuro.
