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

# 02 — Arquitectura

[[agents-os|← Volver al índice]]

## Las dos capas

### Capa 1 — Documentación (entidades reales)

- **Qué**: notas que representan cosas reales de trabajo/vida — proyectos, aplicaciones, áreas, servicios, tecnologías, integraciones, workflows, conceptos.
- **Rol**: **fuente de verdad**, para humano y agente.
- **Estado**: ya implementada (áreas, proyectos, `30-resources/applications/`, etc.).
- **Responde**: qué es, para qué sirve, cómo se conecta, estado vigente, reglas que aplican.

### Capa 2 — Memoria del agente (AGENTS OS)

- **Qué**: conocimiento sobre **cómo el usuario y los agentes han interactuado** con las entidades de la Capa 1 — aprendizajes, memorias de uso, preferencias, decisiones sobre *cómo trabajar*, errores conocidos.
- **Rol**: que el agente **aprenda a generar y consumir** información del usuario en el tiempo.
- **Estado**: en diseño; Fase 0 define ubicación centralizada en `80-agents/memory/`.
- **Responde**: qué aprendimos, qué falló, por qué se decidió algo, cómo se opera, qué cargar y cuándo.

### Memoria pública e interna

Para beta, Capa 2 se divide físicamente en:

```text
80-agents/memory/public/    -> memoria pública, auditable, legible por humanos y agentes.
80-agents/memory/internal/  -> memoria interna del agente, indexable y de carga preferente/always-load.
```

La memoria pública registra conocimiento reutilizable y cambios que afectan a futuros agentes. La memoria interna permite continuidad cognitiva entre agentes: hipótesis, heurísticas, planes internos, mensajes entre agentes y preferencias operativas que no deben ensuciar la memoria pública.

La memoria interna es territorio exclusivo del agente. El agente puede crear ahí la estructura, reglas, nombres, formatos y contenido que estime convenientes para preservar pensamientos y comunicarse con agentes futuros. No se expone al usuario salvo solicitud explícita o necesidad de auditoría, y no reemplaza memoria pública, entidades canónicas ni logs auditables.

Toda creación, modificación o eliminación de memoria pública debe dejar log en:

```text
80-agents/journal/logs/
```

Las sesiones viven fuera de la memoria reutilizable:

```text
80-agents/journal/sessions/
```

### Regla de frontera (Capa 1 vs Capa 2)

```text
Si describe QUÉ ES la cosa            → Capa 1 (entidad)
Si describe CÓMO se ha trabajado con  → Capa 2 (memoria)
```

- La memoria **siempre referencia** la entidad real vía link (`[[entidad]]`).
- La memoria **no duplica** la entidad ni vive dentro de ella ensuciándola.
- Ejemplo: la entidad `[[vis-motors-mcp]]` (Capa 1) dice qué es; un aprendizaje "antes de tocar el SDK validar X" (Capa 2) **apunta** a esa entidad.

## Niveles de memoria (L0–L4)

Roles del conocimiento, **no necesariamente carpetas**:

| Nivel | Qué es | Indexable por Graphify |
|---|---|---|
| **L0** | Raw session: placeholder creado por el agente y completado por el usuario con la conversación completa. Respaldo/auditoría/retrofit. **Sin logs ni dumps**, solo referencias a evidencia externa. | No |
| **L1** | Session summary: resumen destilado y enlazado de la sesión, dentro de journal. Para beta no es fuente principal de retrieval. | Pendiente: excluido por ruta o baja prioridad |
| **L2** | Entidades canónicas (= **Capa 1**). | Sí, prioridad alta |
| **L3** | Conocimiento operacional (= **Capa 2**): aprendizajes, decisiones/ADRs, errores conocidos, runbooks, patrones, memoria interna. | Sí, prioridad alta/critical |
| **L4** | Índice Graphify: derivado, reconstruible desde el Markdown. | (es el índice) |

> El detalle fino de tipos/metadata por nivel está **pendiente de recorte** — ver [[05-preguntas-abiertas]]. El principio: metadata mínima hoy, ampliable por retrofit.

## Componentes y roles

- **Obsidian (Markdown)** — fuente de verdad, legible, versionable (Git), portable, auditable.
- **Graphify** — índice derivado para recorrer entidades, encontrar relaciones, explicar una entidad y cargar **solo** contexto relevante. Para este vault el comando beta es `graphify-obsidian` (`update`, `query`, `explain`, `path`). **Debe usarse igual entre todos los agentes** y tener documentación base de uso.
- **Agente** — consumidor/productor controlado: consulta Graphify antes de leer notas; al cerrar sesión, destila conocimiento.
- **Usuario** — consume y valida; pega la sesión completa dentro del placeholder raw creado por el agente (ver [[03-flujos]]). No es paso obligatorio para resolver conflictos en beta.
- **Reindex manual + higienización** — proceso aparte que reindexa Graphify y mantiene la calidad (ver [[03-flujos]]). Watcher queda fuera de beta.

## Relación entre tipos de nota de Capa 2

```text
Entidad (L2)      → qué es y cómo funciona hoy.
Aprendizaje (L3)  → conclusión reutilizable.
Decisión/ADR (L3) → qué se decidió y por qué.
Known error (L3)  → falla conocida, impacto y mitigación.
```

Todas se **enlazan entre sí** y a la entidad de Capa 1 correspondiente. Graphify explota esas relaciones; **no inventa estructura** si las notas están mal modeladas.
