---
type: change_log
scope: session
created: 2026-07-11
updated: 2026-07-11
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Economía de Tokens]]"
related:
  - "[[agents-os]]"
  - "[[context-router]]"
aliases:
  - AGENTS OS ChatGPT pack creation
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
---

# AGENTS OS ChatGPT pack creado

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `70-templates/ai-context-pack.md`
  - `10-projects/AGENTS OS/chatgpt-pack/`
  - `README.md`
  - `10-projects/AGENTS OS/AGENTS OS.md`
  - `.graphifyignore`
  - `outputs/agents-os-chatgpt/` y `outputs/agents-os-chatgpt.zip` derivados

## Motivo

- Transportar a ChatGPT los componentes base reales de AGENTS OS, junto con
  estado general y reglas de iteración, sin entregar el vault completo ni la
  memoria interna privada.
- Evitar un resumen sustituto: las fuentes se copian verbatim y su procedencia
  se conserva en un manifiesto verificable.

## Fuentes usadas

- [[AGENTS OS]]
- [[Economía de Tokens]]
- [[AGENTS OS - Evaluación y Adopción]]
- [[agents-os]]
- [[context-router]]
- [[token-economy-indexing-architecture]]
- Constitución, contratos, skills, templates y memoria pública AGENTS OS.

## Resolución aplicada

- Se creó un builder reproducible con selección declarativa de fuentes.
- El pack preserva rutas relativas y verifica igualdad SHA-256 fuente/copia.
- Se agregó un consolidado de componentes base para carga liviana.
- Se excluyeron memoria interna, journal, archivos históricos y outputs de
  Graphify.
- Se excluyeron de Graphify tanto las fuentes auxiliares del pack como las
  copias generadas para evitar duplicar el corpus.
- El README raíz quedó como portal, no como segunda fuente completa.

## Validación

- Builder ejecutado desde la raíz del vault.
- Hash SHA-256 fuente/copia validado por archivo.
- ZIP validado con `unzip -t`.
- Verificado que el manifiesto no incluya `memory/internal` ni `journal`.
- Graphify reindexado después de los cambios canónicos.
