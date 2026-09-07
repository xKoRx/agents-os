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

# 03 — Flujos

[[agents-os|← Volver al índice]]

## Flujo conceptual general

```text
Sesión con agente
  ↓
Placeholder raw creado por agente y completado por usuario (L0 / journal)
  ↓
Resumen de sesión si corresponde (L1 / journal)
  ↓
Extracción de aprendizajes, entidades, decisiones y errores (L3 / updates a L2)
  ↓
Actualización del second brain + log auditable
  ↓
Graphify indexa el conocimiento relevante (L4)
  ↓
Próxima sesión recupera contexto usando Graphify
```

## Cierre de sesión ("cierra sesión")

Disparador: el usuario le pide al agente **"cierra sesión"**.

Reparto de trabajo acordado:

- **El agente crea el placeholder raw (L0) en journal y el usuario pega ahí la sesión completa.** (Resuelve la duda de si el agente puede volcar todo el chat: lo aporta el usuario, pero el agente prepara el archivo/lugar.)
- **El agente genera los demás componentes** a partir de su contexto:
  - session summary (L1);
  - aprendizajes;
  - ADRs;
  - errores conocidos;
  - actualizaciones a entidades (Capa 1) — edición directa cuando corresponde;
  - recomendación de qué debería indexar Graphify;
  - log de creaciones, modificaciones y eliminaciones de memoria pública o entidades canónicas.

Regla de oro al insertar conocimiento:

> Si un aprendizaje/conocimiento nuevo **se contrapone** con uno anterior, el agente **resuelve la contradicción con contexto enriquecido**, edita lo necesario y deja log auditable.

Premisa que lo habilita: el agente trabaja con **contexto enriquecido** (ya cargó el conocimiento relevante de la entidad al inicio), por lo que **detecta** la contradicción cuando aparece conocimiento nuevo (p. ej. errores de análisis/diseño previo).

## Inicio de sesión / retrieval

```text
1. Identificar entidad principal (proyecto, app, tecnología, integración, workflow).
2. Cargar reglas del agente (constitución / preferencias) y memoria interna always-load.
3. Consultar Graphify con `graphify-obsidian` (no leer todo el vault).
4. Abrir solo las notas fuente que Graphify indique como necesarias.
5. Trabajar con contexto enriquecido.
```

- Uso de Graphify **uniforme entre agentes** (mismo modo para Codex/Claude/Antigravity/etc.), apoyado en una **documentación base** de cómo consultar.
- Las consultas deben ser **precisas** (entidad + tipo de conocimiento + tema), no abstractas.
- Si el índice falta o está obsoleto, el agente debe generarlo/reindexarlo antes de degradar a búsqueda manual.

## Conflicto de conocimiento

```text
1. El agente ya tiene contexto enriquecido de la entidad.
2. Aparece conocimiento nuevo que contradice lo previo.
3. El agente NO deja inconsistencias conviviendo.
4. Resuelve con la evidencia disponible y actualiza memoria/entidades.
5. Registra la resolución en journal, incluyendo fuentes, cambio aplicado y motivo.
```

## Reindex manual beta

- Graphify debe **reindexar** cada vez que se modifica memoria pública/interna o entidades relevantes.
- Para beta, el reindex es manual/documentado con `graphify-obsidian update`.
- Watcher queda fuera de beta y se evaluará post-beta si el reindex manual genera fricción real.
- Objetivo: que el agente no consulte un grafo obsoleto.

## Higienización (proceso aparte)

- **Manual, una vez al finalizar el día.**
- Se ejecuta como **proceso/sistema extra** (no parte del cierre de sesión normal).
- En base a **nuevas sesiones, logs y archivos modificados por fecha**, debe: validar, corregir y reportar (p. ej. inconsistencias, notas sin metadata, memorias duplicadas u obsoletas).
- Objetivo: que el usuario **no tenga carga de gestión**; idealmente lo corre un agente con reglas definidas.
- Reglas, cadencia y formato de reporte quedaron definidos en `80-agents/skills/agents-os-hygiene-review/SKILL.md`.
- Los reportes viven en `80-agents/journal/hygiene/` usando `80-agents/templates/hygiene-report.md`; son artifacts operativos, no memoria publica indexable.
