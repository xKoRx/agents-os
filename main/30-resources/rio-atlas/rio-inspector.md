---
type: tool
schema_version: 1
status: active
scope: tool
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
source_url:
command: cd ~/fuentes/rio-inspector && python3 inspect.py
entities:
  - "[[rio-inspector]]"
related:
  - "[[RIO]]"
  - "[[integration-map]]"
  - "[[system-map]]"
aliases:
  - rio-inspector
  - rio inspector
  - rio-map
tags:
  - kind/tool
  - scope/tool
  - priority/high
created: 2026-08-10
updated: 2026-08-10
cssclasses:
  - wide
---

# rio-inspector

> [!info]+ rio-inspector
> **Tipo:** tool · **Estado:** active · **Dueño de contexto:** [[Onboarding Signals]] · **Genera:** [[integration-map]] / [[system-map]] del [[00-index|RIO Atlas]].

## Descripcion

- Herramienta (script Python stdlib) que **genera un modelo navegable del acoplamiento de [[RIO]] desde código/config**, en vez de mantenerlo a mano. Nace porque el grafo AST de Graphify da 0 aristas cross-repo: el acoplamiento real de RIO es de runtime (BigQueue/HTTP/REST/Fury Streams) y hay que reconstruirlo desde configs y clases.
- **Ubicación:** `~/fuentes/rio-inspector/inspect.py` (fuera del vault, invariante 12: el código derivado vive en [[Fuentes — Workspace de repositorios]], no en `VAULT_ROOT`).

## Uso principal

- Recorre los 10 repos RIO en `~/fuentes` y descubre por repo: topics BigQueue en `application*.yml` (rol trigger/result/status), clases `*Publisher`/`*Consumer`/`*TriggerController`, controllers y clientes REST, y la dependencia de contratos `rio-sdk-events`.
- Empareja producer→consumer por canal lógico (normaliza variantes por scope: `-test`/`-prod`/`--nonprod`/`rio-actions-`→`rio-action-`) y clasifica transporte: `*-trigger` = HTTP POST (fallback BigQueue), `*-result`/`*-status` = BigQueue async; añade aristas REST/stream conocidas con evidencia.

## Operaciones / comandos

- Regenerar el modelo:

```bash
cd ~/fuentes/rio-inspector && python3 inspect.py
```

## Entradas y salidas

- **Input:** `~/fuentes/rio-*/src/main/**` (config `application*.yml` + código Java/Kotlin) y `build.gradle*`.
- **Output crudo (fuera del vault):** `~/fuentes/rio-inspector/rio-integrations.json` (modelo) y `.mmd` (Mermaid).
- **Output canónico:** escribe **directo** la nota `resource` conforme [[integration-map]] en el vault (idempotente, preserva `created`, pasa `lint --strict`). Ruta overridable por `argv[1]`; default `…/rio-atlas/architecture/integration-map.md`.

## Integraciones

- Alimenta el **RIO Atlas** ([[00-index]]): [[integration-map]] (tabla/grafo) y [[system-map]] (vista de 30 s).
- Complementa a Graphify (`~/fuentes/graphify-signals.json`), que NO captura el acoplamiento cross-servicio.

## Reglas de uso

- **No editar [[integration-map]] a mano:** es generada; el generador la reescribe de forma idempotente con frontmatter contractual (`resource`). Editar el generador, no la nota.
- Salida `medium` de confianza en las aristas REST/stream de `rio-materializer`; validar con el tracer bullet.
- Mejora sistémica de fondo (shift-left del gate en flujos que generan Markdown): [[AGENTS OS - Fase 3]].

## Links

- Plataforma [[RIO]] · Atlas [[00-index]] · Vistas [[system-map]] · [[integration-map]] · Proyecto [[Onboarding Signals]]
