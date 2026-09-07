# Agent Memory System para Obsidian + Graphify

## Estado

`draft`

## Ubicación recomendada

```text
90-agents/AGENTS.md
```

## Propósito

Este documento define el sistema de memoria técnica para agentes que trabajan sobre este vault de Obsidian.

El objetivo es permitir que agentes desktop, IDEs, herramientas tipo Hermes/OpenClaw/Cursor/Codex/Gemini/Claude Code y futuros flujos locales puedan:

- recuperar contexto relevante sin leer todo el vault;
    
- reducir consumo de tokens;
    
- evitar reexplicar proyectos desde cero;
    
- transformar sesiones en conocimiento reutilizable;
    
- mantener continuidad entre sesiones;
    
- preservar trazabilidad mediante raw sessions;
    
- construir un grafo útil con Graphify;
    
- mantener el vault legible para humanos y útil para agentes.
    

Este sistema no busca crear “memoria infinita”. Busca **continuidad verificable**.

---

# 1. Principio central

La arquitectura se basa en esta separación:

```text
Obsidian = fuente de verdad humana
Graphify = índice derivado para navegación y retrieval
Agente = consumidor/productor controlado de conocimiento
Raw sessions = respaldo retrocompatible
```

Graphify no debe reemplazar el conocimiento en Markdown.

Graphify debe explotar el conocimiento ya modelado en notas limpias, enlazadas, con properties y tags consistentes.

---

# 2. Estructura actual del vault

El sistema debe respetar la estructura existente:

```text
00-inbox/
10-projects/
20-areas/
30-resources/
70-templates/
80-agents/
  AGENTS/
  LLM Wiki/
90-system/
  attachments/
  bases/
  dashboards/
  excalidraw/
  control-panel/
  convenciones/
  obsidian-sync/
95-graphify/
Excalidraw/
```

No se deben crear carpetas nuevas en el root del vault salvo decisión explícita.

---

# 3. Ubicación de cada tipo de artefacto

## 3.1 Convenciones del sistema

```text
90-system/convenciones/
```

Uso:

- definición del modelo;
    
- políticas de memoria;
    
- tipos de notas;
    
- taxonomía de tags;
    
- reglas de Graphify;
    
- reglas de carga de contexto;
    
- criterios de calidad.
    

Documento principal:

```text
90-system/convenciones/agent-memory-system.md
```

Documentos opcionales posteriores:

```text
90-system/convenciones/note-types.md
90-system/convenciones/learning-types.md
90-system/convenciones/load-policies.md
90-system/convenciones/graphify-retrieval-policy.md
90-system/convenciones/tag-taxonomy.md
```

---

## 3.2 Instrucciones operativas para agentes

```text
80-agents/AGENTS/
```

Uso:

- instrucciones que el agente debe leer antes de trabajar;
    
- reglas de cierre de sesión;
    
- cómo consultar Graphify;
    
- cómo escribir resúmenes;
    
- cómo proponer cambios al vault.
    

Documento recomendado:

```text
80-agents/AGENTS/obsidian-memory-agent.md
```

Este documento debe ser breve y operacional.

No debe contener toda la teoría. Para eso está `90-system/convenciones/agent-memory-system.md`.

---

## 3.3 Templates

```text
70-templates/
```

Uso:

- template de raw session;
    
- template de session summary;
    
- template de entidad;
    
- template de aprendizaje;
    
- template de ADR;
    
- template de known error;
    
- template de runbook.
    

Ruta sugerida:

```text
70-templates/agent-memory/
```

Templates recomendados:

```text
70-templates/agent-memory/entity.md
70-templates/agent-memory/learning.md
70-templates/agent-memory/session-summary.md
70-templates/agent-memory/raw-session.md
70-templates/agent-memory/adr.md
70-templates/agent-memory/known-error.md
70-templates/agent-memory/runbook.md
```

---

## 3.4 Graphify

```text
95-graphify/
```

Uso:

- outputs generados por Graphify;
    
- `graph.json`;
    
- `GRAPH_REPORT.md`;
    
- visualizaciones;
    
- reportes;
    
- configuración derivada;
    
- índices temporales o reconstruibles.
    

Graphify es una capa generada. No es la fuente de verdad.

Si algo se pierde en `95-graphify`, debe poder reconstruirse desde las notas Markdown.

---

## 3.5 Entidades y conocimiento reutilizable

Las entidades canónicas y aprendizajes deben vivir principalmente en:

```text
30-resources/
```

Ruta sugerida para MVP:

```text
30-resources/agent-memory/
```

Subestructura sugerida:

```text
30-resources/agent-memory/entities/
30-resources/agent-memory/learnings/
30-resources/agent-memory/operations/
```

Ejemplo:

```text
30-resources/agent-memory/entities/SQX Export Plugin.md
30-resources/agent-memory/entities/Echo Forge Importer.md
30-resources/agent-memory/entities/StrategyQuant X.md

30-resources/agent-memory/learnings/LRN-001 - No asumir completitud de overview_json.md

30-resources/agent-memory/operations/ERR-001 - SQX export sin indicadores.md
30-resources/agent-memory/operations/RUN-001 - Validar export SQX contra fixture.md
```

Si una entidad pertenece fuertemente a un proyecto, también puede vivir dentro del proyecto correspondiente en `10-projects/`, pero para MVP conviene centralizar las entidades en `30-resources/agent-memory/entities/`.

La carpeta no es lo más importante. Lo importante son:

- `type`;
    
- `scope`;
    
- `project`;
    
- `application`;
    
- `tags`;
    
- links internos;
    
- consistencia de nombres.
    

---

## 3.6 Proyectos

```text
10-projects/
```

Uso:

- project briefs;
    
- estado actual de proyectos;
    
- documentos vivos de proyecto;
    
- sesiones directamente asociadas a un proyecto, si se prefiere mantenerlas ahí.
    

Ejemplo:

```text
10-projects/Echo Forge/Echo Forge.md
10-projects/Echo Forge/sessions/
10-projects/Echo Forge/sessions/raw/
```

Alternativa simple para MVP:

```text
30-resources/agent-memory/sessions/
30-resources/agent-memory/raw-sessions/
```

Decisión recomendada:

- Si la sesión pertenece claramente a un proyecto: guardar bajo `10-projects/<project>/sessions/`.
    
- Si es transversal o exploratoria: guardar bajo `30-resources/agent-memory/sessions/`.
    

---

# 4. Niveles de memoria

El sistema usa niveles conceptuales. Estos niveles no son necesariamente carpetas. Son roles del conocimiento.

```text
L0 = raw session
L1 = session summary
L2 = canonical entities
L3 = operational knowledge / learnings / decisions
L4 = Graphify index
```

---

## 4.1 L0 — Raw Session

Corresponde a la conversación completa de una sesión.

Debe guardarse como Markdown.

No debe incluir logs gigantes, dumps, exports de aplicaciones, JSON masivos ni archivos operacionales.

La raw session sirve para:

- auditoría;
    
- reprocesamiento futuro;
    
- extracción retrocompatible;
    
- reconstrucción de contexto si faltó algo;
    
- trazabilidad.
    

No se indexa con Graphify por defecto.

### Regla

```text
L0 guarda conversación completa, no evidencia operacional cruda.
```

Si una sesión menciona logs, outputs, archivos SQX, dumps o evidencia técnica pesada, Obsidian debe guardar solo referencias.

Ejemplo:

```md
## Evidencia externa

- Export original: `s3://echo-forge/sqx_exports/2026-06-26/...`
- Commit relacionado: `abc123`
- Job ID: `wfm-export-20260626-001`
- Ruta local temporal: `/home/kor/SQX_exports/overview_json`
```

---

## 4.2 L1 — Session Summary

Corresponde al resumen destilado de una sesión.

Debe ser breve, enlazado y útil.

Debe responder:

- qué se intentó resolver;
    
- qué se hizo;
    
- qué se aprendió;
    
- qué decisiones aparecieron;
    
- qué errores fueron detectados;
    
- qué entidades fueron afectadas;
    
- qué debería cargarse en la próxima sesión.
    

Una session summary sí puede ser indexable, pero con prioridad baja o media.

Ejemplo de metadata:

```yaml
---
type: session
scope: project
project: "[[Echo Forge]]"
status: closed
date: 2026-06-26
raw_session: "[[2026-06-26 - raw - SQX export indicators]]"
entities:
  - "[[SQX Export Plugin]]"
  - "[[Echo Forge Importer]]"
learnings:
  - "[[LRN-001 - No asumir completitud de overview_json]]"
decisions:
  - "[[ADR-004 - Mantener plugin Java para export SQX]]"
known_errors:
  - "[[ERR-001 - SQX export sin indicadores]]"
indexable: true
index_priority: low
tags:
  - kind/session
  - project/echo-forge
  - status/closed
---
```

---

## 4.3 L2 — Canonical Entities

Las entidades canónicas son las notas que representan cosas importantes del ecosistema.

Ejemplos:

- proyecto;
    
- aplicación;
    
- servicio;
    
- herramienta;
    
- tecnología;
    
- integración;
    
- workflow;
    
- storage;
    
- API;
    
- dataset;
    
- concepto;
    
- ambiente;
    
- repositorio;
    
- agente.
    

Las entidades responden:

```text
Qué es esto.
Para qué sirve.
Cómo se conecta.
Cuál es su estado actual.
Qué reglas vigentes aplican.
Qué errores, decisiones y aprendizajes están relacionados.
```

Ejemplo:

```yaml
---
type: application
scope: application
project: "[[Echo Forge]]"
status: active
technologies:
  - "[[Java]]"
  - "[[StrategyQuant X]]"
integrates_with:
  - "[[StrategyQuant X]]"
  - "[[Echo Forge Importer]]"
produces:
  - "[[overview_json]]"
known_errors:
  - "[[ERR-001 - SQX export sin indicadores]]"
decisions:
  - "[[ADR-004 - Mantener plugin Java para export SQX]]"
learnings:
  - "[[LRN-002 - SQX Export Plugin requiere fixtures con indicadores conocidos]]"
indexable: true
index_priority: high
tags:
  - kind/application
  - project/echo-forge
  - app/sqx-export-plugin
  - tech/sqx
  - status/active
---
```

---

## 4.4 L3 — Operational Knowledge

L3 contiene conocimiento reutilizable que guía acciones futuras.

Incluye:

- aprendizajes;
    
- ADRs;
    
- known errors;
    
- runbooks;
    
- comandos validados;
    
- patrones;
    
- anti-patrones;
    
- reglas operativas.
    

L3 responde:

```text
Qué aprendimos.
Por qué decidimos algo.
Qué falló.
Cómo se opera.
Qué no hay que repetir.
Qué procedimiento está validado.
```

---

## 4.5 L4 — Graphify Index

L4 es el índice generado por Graphify.

Graphify debe procesar solo notas útiles para retrieval.

Debe quedar en:

```text
95-graphify/
```

Graphify no debe indexar por defecto:

- raw sessions;
    
- inbox;
    
- drafts;
    
- notas diarias;
    
- scratch;
    
- adjuntos;
    
- evidencia pesada;
    
- archivos generados temporales.
    

Graphify debe priorizar:

- constitución del agente;
    
- preferencias globales;
    
- proyectos;
    
- entidades;
    
- aprendizajes;
    
- ADRs;
    
- known errors;
    
- runbooks;
    
- integraciones;
    
- workflows;
    
- tecnologías;
    
- herramientas;
    
- conceptos.
    

---

# 5. Aprendizajes

No todo es aprendizaje, pero casi todo puede producir uno.

Un aprendizaje es una conclusión reutilizable extraída desde una sesión, error, decisión, experimento o implementación.

El aprendizaje no reemplaza a una entidad, ADR o known error.

Ejemplo:

```text
Entidad:
[[SQX Export Plugin]] = qué es y cómo funciona hoy.

Aprendizaje:
[[LRN-002 - SQX Export Plugin requiere fixtures con indicadores conocidos]] = regla reutilizable aprendida.

ADR:
[[ADR-004 - Mantener plugin Java para export SQX]] = decisión técnica tomada.

Known Error:
[[ERR-001 - SQX export sin indicadores]] = falla conocida, causa, impacto y mitigación.
```

---

## 5.1 Tipos de aprendizajes

Tipos recomendados:

```text
constitutional_learning
user_preference_learning
project_learning
application_learning
integration_learning
technology_learning
operational_learning
error_learning
pattern_learning
anti_pattern_learning
```

---

## 5.2 Constitutional learning

Reglas globales que deben cargarse siempre.

Ubicación recomendada:

```text
90-system/convenciones/agent-constitution.md
```

Ejemplo:

```yaml
---
type: constitution
scope: global
load_policy: always
status: active
indexable: true
index_priority: critical
tags:
  - kind/constitution
  - scope/global
  - agent/always-load
---
```

Contenido típico:

```md
# Agent Constitution

## Reglas permanentes

- Ser práctico antes que teórico.
- No leer todo el vault si existe índice Graphify.
- No pedir contexto que ya está documentado.
- No modificar conocimiento canónico sin proponer cambios.
- No guardar logs operacionales en Obsidian.
- No convertir el vault en un basural.
- Declarar incertidumbre técnica cuando exista.
- Preferir cambios revisables y versionables.
```

---

## 5.3 User preference learning

Preferencias estables del usuario.

Ubicación recomendada:

```text
90-system/convenciones/user-preferences.md
```

Ejemplo:

```yaml
---
type: user_preference
scope: global
load_policy: always
status: active
indexable: true
index_priority: critical
tags:
  - kind/user-preference
  - scope/global
  - agent/always-load
---
```

Contenido típico:

```md
# User Preferences

## Forma de trabajo

- Priorizar soluciones prácticas.
- Evitar complejidad innecesaria.
- Proponer objeciones cuando algo esté mal planteado.
- Mantener continuidad entre sesiones.
- Optimizar consumo de tokens.
- Preferir tooling local cuando sea razonable.
- Mantener control humano mediante diffs o propuestas.
```

---

## 5.4 Project learning

Aprendizajes aplicables a un proyecto completo.

Ejemplo:

```yaml
---
type: learning
learning_type: project_learning
scope: project
project: "[[Echo Forge]]"
status: active
priority: high
load_policy: when_project_loaded
source_session: "[[2026-06-26 - SQX export indicators]]"
indexable: true
index_priority: high
tags:
  - kind/learning
  - learning/project
  - project/echo-forge
  - status/active
---
```

---

## 5.5 Application learning

Aprendizajes aplicables a una aplicación específica.

Ejemplo:

```yaml
---
type: learning
learning_type: application_learning
scope: application
project: "[[Echo Forge]]"
application: "[[SQX Export Plugin]]"
status: active
priority: critical
load_policy: when_application_loaded
source_session: "[[2026-06-26 - SQX export indicators]]"
indexable: true
index_priority: high
tags:
  - kind/learning
  - learning/application
  - project/echo-forge
  - app/sqx-export-plugin
  - priority/critical
---
```

---

# 6. Load policies

Cada nota importante debe declarar cuándo debe cargarse.

Valores recomendados:

```text
always
when_user_profile_loaded
when_project_loaded
when_application_loaded
when_technology_loaded
when_integration_loaded
when_error_matches
manual
never
```

Ejemplos:

```yaml
load_policy: always
```

```yaml
load_policy: when_application_loaded
```

```yaml
load_policy: never
```

Raw sessions deben usar:

```yaml
load_policy: never
indexable: false
```

---

# 7. Indexabilidad

Cada nota relevante debe declarar si entra al índice.

```yaml
indexable: true
index_priority: high
```

Prioridades recomendadas:

```text
critical
high
medium
low
never
```

Reglas:

```text
constitution      = critical
user_preference   = critical
project           = high
application       = high
integration       = high
learning          = high
decision          = high
known_error       = high
runbook           = high
session           = low
raw_session       = never
scratch           = never
draft             = never
```

---

# 8. Tags

Los tags deben ser pocos, consistentes y útiles.

La semántica fuerte vive en properties.

Los tags sirven para búsqueda humana, filtros, navegación y soporte a Graphify.

Taxonomía mínima:

```text
kind/*
scope/*
project/*
area/*
app/*
tech/*
learning/*
status/*
priority/*
agent/*
```

Ejemplos:

```yaml
tags:
  - kind/learning
  - learning/application
  - project/echo-forge
  - app/sqx-export-plugin
  - status/active
  - priority/critical
```

```yaml
tags:
  - kind/application
  - project/echo-forge
  - app/sqx-export-plugin
  - tech/sqx
  - status/active
```

```yaml
tags:
  - kind/known-error
  - project/echo-forge
  - app/sqx-export-plugin
  - status/open
  - priority/high
```

Evitar:

```text
#cosas
#importante
#varios
#pendiente
#ia
#proyecto
```

Esos tags no ayudan. Son ruido con pinta de orden.

---

# 9. Relaciones

Las relaciones deben estar explícitas mediante links y properties.

Relaciones recomendadas:

```text
part_of
depends_on
integrates_with
produces
consumes
stores_in
runs_on
implemented_by
documented_by
decided_by
affected_by
fixed_by
related_to
learned_from
source_session
```

Ejemplo:

```yaml
project: "[[Echo Forge]]"
application: "[[SQX Export Plugin]]"
integrates_with:
  - "[[Echo Forge Importer]]"
produces:
  - "[[overview_json]]"
known_errors:
  - "[[ERR-001 - SQX export sin indicadores]]"
decisions:
  - "[[ADR-004 - Mantener plugin Java para export SQX]]"
learnings:
  - "[[LRN-002 - SQX Export Plugin requiere fixtures con indicadores conocidos]]"
```

En el cuerpo de la nota también deben existir links.

Graphify funciona mejor cuando hay entidades explícitas, nombres consistentes y relaciones visibles.

---

# 10. Graphify retrieval policy

Graphify debe usarse como índice estructural.

No debe tratarse como un chatbot semántico universal.

El agente debe consultar Graphify antes de abrir notas fuente.

## 10.1 Comandos recomendados

Para entender una entidad:

```bash
graphify explain "SQX Export Plugin"
```

Para buscar conocimiento alrededor de una entidad:

```bash
graphify query "SQX Export Plugin learning critical" --budget 1000
```

Para buscar errores conocidos:

```bash
graphify query "SQX Export Plugin known_error active indicators export" --budget 1000
```

Para buscar decisiones:

```bash
graphify query "SQX Export Plugin ADR active plugin Java" --budget 1000
```

Para entender una integración:

```bash
graphify path "SQX Export Plugin" "Mongo Strategy Store"
```

## 10.2 Patrón de búsqueda

Usar este patrón:

```text
<entidad> + <tipo de conocimiento> + <tema>
```

Ejemplos:

```bash
graphify query "Echo Forge SQX Export Plugin learning indicators" --budget 1000
graphify query "Echo Forge overview_json entry exit indicators" --budget 1500
graphify query "Temporal WFM Workflow runbook active" --budget 1000
graphify query "MinIO Strategy Artifacts integration Echo Forge" --budget 1000
```

## 10.3 Evitar queries abstractas

Evitar:

```bash
graphify query "qué debo saber antes de trabajar"
graphify query "dame contexto importante"
graphify query "qué cosas debo recordar"
```

Preferir:

```bash
graphify query "SQX Export Plugin learning critical" --budget 1000
graphify query "SQX Export Plugin known_error active" --budget 1000
graphify query "SQX Export Plugin ADR active" --budget 1000
```

La consulta buena no es mágica. Es precisa.

---

# 11. Flujo de inicio de sesión

Cuando un agente inicia una sesión:

```text
1. Identificar proyecto principal.
2. Identificar entidad principal: app, servicio, tecnología, integración o workflow.
3. Leer instrucciones de agente en 80-agents/AGENTS/.
4. Consultar Graphify.
5. Leer solo notas fuente que Graphify indique como necesarias.
6. Trabajar.
```

Ejemplo para una sesión sobre `SQX Export Plugin`:

```bash
graphify explain "SQX Export Plugin"
graphify query "SQX Export Plugin learning critical" --budget 1000
graphify query "SQX Export Plugin known_error active" --budget 1000
graphify query "SQX Export Plugin ADR active" --budget 1000
graphify query "SQX Export Plugin integration overview_json Echo Forge Importer" --budget 1500
```

El agente no debe partir leyendo todo `10-projects/Echo Forge`.

Eso es quemar tokens como si fueran boletas de luz con calefactor eléctrico. Mala práctica.

---

# 12. Flujo de cierre de sesión

Al cerrar una sesión, el agente debe generar:

```text
1. Raw session completa.
2. Session summary.
3. Candidate learnings.
4. Candidate ADRs.
5. Candidate known errors.
6. Candidate entity updates.
7. Recomendación de qué debería indexar Graphify.
```

El agente no debe sobrescribir conocimiento canónico sin dejar claro:

```text
qué cambió;
por qué cambió;
desde qué sesión viene;
nivel de confianza;
impacto;
entidades afectadas.
```

## 12.1 Raw session

Debe guardarse completa.

No se indexa.

Metadata sugerida:

```yaml
---
type: raw_session
scope: project
project: "[[Echo Forge]]"
date: 2026-06-26
status: archived
indexable: false
load_policy: never
tags:
  - kind/raw-session
  - project/echo-forge
  - status/archived
---
```

## 12.2 Session summary

Debe enlazar lo importante.

Metadata sugerida:

```yaml
---
type: session
scope: project
project: "[[Echo Forge]]"
date: 2026-06-26
status: closed
raw_session: "[[2026-06-26 - raw - SQX export indicators]]"
entities:
  - "[[SQX Export Plugin]]"
learnings:
  - "[[LRN-001 - No asumir completitud de overview_json]]"
indexable: true
index_priority: low
load_policy: manual
tags:
  - kind/session
  - project/echo-forge
  - status/closed
---
```

---

# 13. Templates mínimos

## 13.1 Entity template

```md
---
type: application
scope: application
project: ""
status: active
indexable: true
index_priority: high
load_policy: when_application_loaded
tags:
  - kind/application
  - status/active
---

# {{title}}

## Qué es

## Para qué sirve

## Responsabilidades

## Integraciones

## Reglas vigentes

## Aprendizajes relacionados

## Decisiones relacionadas

## Errores conocidos

## Runbooks relacionados

## Fuentes / sesiones relacionadas
```

---

## 13.2 Learning template

```md
---
type: learning
learning_type: application_learning
scope: application
project: ""
application: ""
status: active
priority: high
confidence: medium
source_session: ""
indexable: true
index_priority: high
load_policy: when_application_loaded
tags:
  - kind/learning
  - status/active
---

# LRN-XXX - {{title}}

## Aprendizaje

## Contexto

## Regla práctica

## Entidades relacionadas

## Impacto

## Cuándo cargar este aprendizaje

## Fuente
```

---

## 13.3 ADR template

```md
---
type: decision
decision_type: ADR
scope: project
project: ""
status: accepted
date: ""
indexable: true
index_priority: high
load_policy: when_project_loaded
tags:
  - kind/decision
  - status/accepted
---

# ADR-XXX - {{title}}

## Contexto

## Decisión

## Alternativas consideradas

## Motivos

## Consecuencias positivas

## Consecuencias negativas

## Entidades afectadas

## Aprendizajes relacionados

## Fuente
```

---

## 13.4 Known error template

```md
---
type: known_error
scope: application
project: ""
application: ""
status: open
severity: medium
indexable: true
index_priority: high
load_policy: when_error_matches
tags:
  - kind/known-error
  - status/open
---

# ERR-XXX - {{title}}

## Síntoma

## Causa conocida o probable

## Impacto

## Cómo detectarlo

## Mitigación

## Solución definitiva

## Entidades afectadas

## Runbooks relacionados

## Fuente
```

---

# 14. Qué debe procesar Graphify

Graphify debe procesar:

```text
type: constitution
type: user_preference
type: project
type: area
type: application
type: service
type: integration
type: workflow
type: technology
type: tool
type: storage
type: api
type: concept
type: learning
type: decision
type: known_error
type: runbook
type: command
type: pattern
```

Graphify puede procesar con prioridad baja:

```text
type: session
```

Graphify no debe procesar por defecto:

```text
type: raw_session
type: scratch
type: draft
type: inbox
type: attachment
```

Regla:

```text
Si indexable=false, Graphify debe ignorarlo.
```

---

# 15. Qué debe hacer el agente cuando falta contexto

Si Graphify devuelve poco contexto o contexto ambiguo:

```text
1. No inventar.
2. Abrir las notas fuente sugeridas por Graphify.
3. Si sigue faltando información, pedir aclaración.
4. Si aparece conocimiento nuevo, registrarlo al cierre.
```

Si encuentra contradicciones:

```text
1. No sobrescribir silenciosamente.
2. Crear una nota o sección de conflicto.
3. Citar las notas contradictorias.
4. Proponer resolución.
```

Ejemplo:

```md
# Conflict - overview_json completeness

## Nota anterior
`overview_json` contiene toda la metadata de estrategia.

## Evidencia nueva
Una sesión detectó estrategias persistidas sin indicadores.

## Resolución propuesta
Actualizar entidades relacionadas para indicar que `overview_json` no debe considerarse completo hasta validación explícita.
```

---

# 16. Approach descartado: vector DB como base principal

No se usará vector DB como fuente principal en el MVP.

Motivos:

- reduce control humano;
    
- agrega infraestructura;
    
- dificulta auditoría;
    
- no reemplaza relaciones explícitas;
    
- no modela vigencia de decisiones;
    
- no resuelve contradicciones;
    
- no es tan portable como Markdown + Git.
    

Embeddings pueden agregarse después como acelerador, pero no como base de conocimiento.

Diseño recomendado:

```text
Markdown + links + properties + tags + Graphify
```

Más adelante:

```text
Graphify + embeddings auxiliares
```

Pero no antes de validar el MVP.

---

# 17. Approach descartado: context packs manuales persistentes

No se crearán context packs manuales como índice paralelo en el MVP.

Motivo:

Graphify debe cumplir el rol de índice.

Crear context packs manuales duplicaría información y aumentaría deuda documental.

Lo aceptable es tener una nota breve de instrucciones para agentes, por ejemplo:

```text
80-agents/AGENTS/obsidian-memory-agent.md
```

Pero no mantener índices paralelos a mano.

---

# 18. Approach descartado: guardar logs en Obsidian

No se deben guardar logs de aplicación, dumps masivos ni evidencia pesada en Obsidian.

Motivos:

- ensucia el vault;
    
- empeora navegación;
    
- empeora Graphify;
    
- aumenta ruido;
    
- rompe la idea de second brain;
    
- mezcla conocimiento con evidencia operacional cruda.
    

Obsidian debe guardar referencias a evidencia externa, no la evidencia completa.

---

# 19. Approach aceptado: raw session completa

Sí se debe guardar la conversación completa como Markdown.

Motivos:

- permite auditoría;
    
- permite reprocesamiento;
    
- permite extraer aprendizajes futuros;
    
- mantiene trazabilidad;
    
- permite reconstrucción si el resumen fue malo.
    

Pero:

```text
raw_session no se indexa por defecto.
raw_session no se carga como contexto normal.
raw_session no reemplaza session_summary.
```

---

# 20. Criterios de éxito del MVP

El sistema se considera exitoso si cumple:

```text
1. Una sesión nueva puede partir leyendo Graphify, no el vault completo.
2. El agente puede identificar proyecto, app, learnings, ADRs y errores relevantes.
3. El contexto inicial cabe idealmente en menos de 3.000 tokens.
4. Cada sesión importante genera raw session y summary.
5. Los aprendizajes relevantes terminan como notas explícitas.
6. Las decisiones técnicas relevantes terminan como ADRs.
7. Los errores repetibles terminan como known errors.
8. Graphify puede recorrer relaciones entre entidades.
9. El usuario deja de reexplicar el mismo proyecto en cada sesión.
10. El vault sigue siendo legible para humanos.
```

---

# 21. Métricas recomendadas

```text
context_initial_tokens_target: < 3000
raw_sessions_saved: > 90%
session_summaries_created: > 90%
learnings_created_per_relevant_session: 1..5
decisions_without_adr: 0
known_errors_without_status: 0
raw_sessions_indexed_by_graphify: 0
agent_repeated_context_questions: tendencia a 0
graphify_queries_before_source_reads: > 80%
```

---

# 22. Aprendizajes derivados del diseño

## 22.1 Graphify no reemplaza una buena ontología

Graphify será tan útil como lo sean las notas que procese.

Si las notas tienen nombres malos, pocos links, tags inconsistentes y properties vagas, Graphify no va a hacer magia.

Regla:

```text
El grafo explota estructura. No inventa estructura confiable.
```

---

## 22.2 La memoria no debe ser un basural

Guardar todo parece seguro, pero destruye utilidad.

El sistema debe separar:

```text
conversación completa;
resumen útil;
entidad canónica;
aprendizaje;
decisión;
error conocido;
evidencia externa.
```

Cada cosa tiene un rol.

---

## 22.3 Las decisiones no son lo mismo que conocimiento canónico

Una entidad dice qué es verdad hoy.

Una ADR dice por qué se decidió algo.

Ambas deben enlazarse, pero no mezclarse.

Ejemplo:

```text
Entidad:
El mecanismo vigente de exportación SQX es el plugin Java.

ADR:
Se decidió mantener plugin Java en vez de external script por menor riesgo inicial.
```

---

## 22.4 Los aprendizajes necesitan scope

Un aprendizaje sin scope no sirve para cargar contexto.

Cada aprendizaje debe declarar:

```text
scope;
load_policy;
project;
application o tecnología, si aplica;
priority;
confidence;
source_session.
```

---

## 22.5 Raw session es respaldo, no contexto

La conversación completa debe existir para trazabilidad.

Pero no debe cargarse normalmente en sesiones futuras.

Cargar raw sessions por defecto es volver al problema original de consumo excesivo de tokens.

---

## 22.6 Tags precisos ganan más que carpetas complejas

La estructura debe mantenerse simple.

La inteligencia debe estar en:

```text
properties;
links;
tags;
Graphify;
nombres consistentes.
```

No en una taxonomía de carpetas imposible de mantener.

---

# 23. Implementación MVP sugerida

## Fase 1 — Convención base

Crear:

```text
90-system/convenciones/agent-memory-system.md
80-agents/AGENTS/obsidian-memory-agent.md
70-templates/agent-memory/
```

## Fase 2 — Templates

Crear templates:

```text
entity.md
learning.md
session-summary.md
raw-session.md
adr.md
known-error.md
runbook.md
```

## Fase 3 — Primeras entidades

Crear entidades base:

```text
30-resources/agent-memory/entities/Echo Forge.md
30-resources/agent-memory/entities/SQX Export Plugin.md
30-resources/agent-memory/entities/Echo Forge Importer.md
30-resources/agent-memory/entities/StrategyQuant X.md
30-resources/agent-memory/entities/Mongo Strategy Store.md
30-resources/agent-memory/entities/overview_json.md
```

## Fase 4 — Primeros aprendizajes

Crear:

```text
30-resources/agent-memory/learnings/LRN-001 - No asumir completitud de overview_json.md
30-resources/agent-memory/learnings/LRN-002 - SQX Export Plugin requiere fixtures con indicadores conocidos.md
```

## Fase 5 — Primeros L3

Crear:

```text
30-resources/agent-memory/operations/ADR-004 - Mantener plugin Java para export SQX.md
30-resources/agent-memory/operations/ERR-001 - SQX export sin indicadores.md
30-resources/agent-memory/operations/RUN-001 - Validar export SQX contra fixture.md
```

## Fase 6 — Graphify

Configurar Graphify para procesar solo notas indexables.

Output:

```text
95-graphify/
```

Validar búsquedas:

```bash
graphify explain "SQX Export Plugin"
graphify query "SQX Export Plugin learning critical" --budget 1000
graphify query "SQX Export Plugin known_error active" --budget 1000
graphify path "SQX Export Plugin" "Mongo Strategy Store"
```

---

# 24. Regla final

Este sistema debe optimizar continuidad, no acumular decoración documental.

Cada nota debe justificar su existencia.

Una buena nota debe responder al menos una de estas preguntas:

```text
¿Qué es esto?
¿Cómo se conecta?
¿Qué aprendimos?
¿Qué decidimos?
¿Qué falló?
¿Cómo se opera?
¿Cuándo debe cargarse?
```

Si una nota no responde ninguna, probablemente es ruido.

---

# 25. Resumen ejecutivo

El sistema queda definido así:

```text
L0 Raw Session
Conversación completa. No indexable. Retrocompatibilidad y auditoría.

L1 Session Summary
Resumen destilado. Enlazado. Indexable con baja prioridad.

L2 Canonical Entities
Proyectos, apps, servicios, tecnologías, integraciones, workflows y conceptos. Fuente de verdad actual.

L3 Operational Knowledge
Aprendizajes, ADRs, known errors, runbooks, patrones y anti-patrones.

L4 Graphify
Índice derivado. Se usa para retrieval y navegación. No reemplaza Markdown.
```

La frase guía:

```text
Obsidian guarda la verdad.
Graphify encuentra la verdad.
El agente consulta Graphify antes de gastar tokens.
La sesión cierra convirtiendo conversación en conocimiento reutilizable.
```