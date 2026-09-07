---
type: doc
status: draft
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
created: 2026-06-27
updated: 2026-06-27
---

# 01 — Problema y visión

[[agents-os|← Volver al índice]]

## El problema

Al trabajar con agentes de IA en sesiones largas o separadas se repite el mismo patrón:

- cada sesión pierde contexto;
- el usuario debe re-explicar proyectos, decisiones, errores y arquitectura;
- se gastan tokens releyendo o re-explicando información;
- los aprendizajes importantes quedan atrapados en una conversación;
- no hay forma consistente de convertir sesiones en conocimiento reutilizable;
- los agentes no tienen una memoria técnica verificable entre sesiones.

El objetivo **no** es "memoria infinita", sino una memoria **operativa, local, versionable y consultable**, útil para el usuario y para agentes desktop / IDEs / herramientas (Codex, Claude, Cursor, Antigravity, MiniMax, Gemini, etc.).

## La visión

Un **sistema operativo de agentes (AGENTS OS)** que le dice al agente **cómo almacenar información sobre lo que hace el usuario en todos sus ámbitos** (hoy más orientado a TI, pero no limitado) y **cómo persistir memoria a lo largo del tiempo**.

La hipótesis central:

> Mientras más se usen los agentes bajo este SO, **más útiles se vuelven**, porque con el tiempo el sistema llega a entender lo que el usuario hace, sus necesidades, prioridades y problemas.

Es la generalización de la "memoria personal" que un asistente podría tener del usuario, llevada a **todo ámbito** (trabajo, vida, proyectos) y **compartida entre agentes**.

## Qué NO es

- No es una vector DB como base (ver [[04-principios-y-decisiones]]).
- No es un chatbot semántico mágico sobre el vault.
- No es un índice paralelo mantenido a mano (context packs).
- No reemplaza la documentación humana: la **extiende** con memoria de cómo se ha trabajado.

## Resultado esperado

```text
Sesiones → conocimiento.
Conocimiento → grafo (Graphify).
Grafo → contexto barato.
Contexto barato → mejores sesiones.
```

Concretamente: abrir una sesión nueva sobre una entidad (app, proyecto, tecnología), que el agente **recupere el contexto relevante vía Graphify** sin leer todo el vault, y que el usuario **no tenga que re-explicar** lo ya conocido — manteniendo el vault legible para humanos.
