---
type: doc
scope: global
created: 2026-06-27
updated: 2026-06-27
indexable: true
index_priority: high
load_policy: when_project_loaded
tags:
  - agent/memorysystem
  - kind/doc
  - scope/global
---

# Agent Memory Properties

## Ubicación

```text
80-agents/agents-os/_drafts/Agent Memory Properties.md
```

Este documento queda como documentación de trabajo para construir el sistema. En Fase 1 fue reconciliado con `80-agents/skills/_shared/metadata-schema.md`, que ahora es el contrato beta compacto. Este draft conserva detalle y ejemplos extendidos.

## Propósito

Este documento define las propiedades base que deben usar las memorias, entidades, aprendizajes, sesiones resumidas y documentos operativos creados para el sistema de memoria de agentes del vault.

El objetivo es que las notas sean:

- fáciles de leer por humanos;
    
- consistentes para Obsidian;
    
- útiles para Graphify;
    
- recuperables por agentes;
    
- filtrables por tags;
    
- suficientemente simples para mantenerlas en el tiempo.
    

La regla principal es:

```text
Pocas propiedades, bien usadas.
Tags precisos.
Links explícitos.
Nada de YAML ceremonial.
```

## Decisiones beta relacionadas

- La memoria de agentes vive centralizada bajo `80-agents/memory/`.
- `80-agents/memory/public/` contiene memoria pública indexable.
- `80-agents/memory/internal/` contiene memoria interna del agente, también indexable y con `load_policy: always` cuando corresponda.
- `80-agents/journal/` contiene sesiones y logs operativos; no es la memoria reutilizable principal.
- Las raw sessions viven en `80-agents/journal/sessions/raw/` y se excluyen de Graphify.
- Los logs de modificaciones, eliminaciones y creaciones de memoria pública viven en `80-agents/journal/logs/`.
- Graphify para beta debe usar `graphify-obsidian`; el objetivo posterior es migrar outputs generados al `graphify-out/` del root y controlar exclusiones con `.graphifyignore`.

---

# 1. Principios

## 1.1 No usar `status`

No se usará una propiedad `status`.

Motivo:

Una memoria debe representar conocimiento vigente y útil. Si ya no sirve, se borra o se reemplaza. No interesa mantener memorias obsoletas como parte del contexto normal.

Ejemplo:

```text
Si una app antes usaba jQuery y ahora usa Vue 3, la memoria vigente debe decir Vue 3.
La historia antigua queda en session summaries o raw sessions.
```

Esto evita que el agente cargue conocimiento muerto.

---

## 1.2 No usar `draft` como propiedad base

No se usará `draft: true`.

Si una nota todavía no está lista, debe vivir temporalmente en `00-inbox` o marcarse visualmente en el título o tags de trabajo.

Ejemplo:

```text
00-inbox/LRN-CANDIDATE - Validar overview_json antes de persistir.md
```

Cuando se valida, se mueve a su carpeta definitiva y se normalizan sus tags.

---

## 1.3 `indexable` es convención propia

La propiedad `indexable` no debe asumirse como una feature nativa de Graphify.

Se usará como convención interna del vault para:

- reglas de agentes;
    
- Obsidian Bases;
    
- búsquedas;
    
- validaciones futuras;
    
- posibles scripts propios;
    
- documentación del criterio de indexación.
    

Graphify se controlará principalmente por rutas, carpetas y `.graphifyignore`.

---

## 1.4 `scope` es primario, no múltiple

Una nota debe tener un `scope` principal.

Si aplica a varias entidades, esas entidades se declaran en `entities`.

Ejemplo:

```yaml
scope: integration
entities:
  - "[[SQX Export Plugin]]"
  - "[[Echo Forge Importer]]"
  - "[[overview_json]]"
```

No se recomienda:

```yaml
scope:
  - application
  - integration
  - project
```

Eso ensucia la lógica de carga.

---

# 2. Propiedades base

Las propiedades base recomendadas son:

```yaml
---
type:
scope:
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence:
source_session:
load_policy:
indexable:
index_priority:
tags:
---
```

No todas son obligatorias en todos los tipos de nota.

---

# 3. Propiedades obligatorias mínimas

Toda nota del sistema de memoria debería tener:

```yaml
---
type:
scope:
created:
updated:
tags:
---
```

Para notas que deben ser usadas por agentes, agregar:

```yaml
---
entities:
load_policy:
indexable:
index_priority:
---
```

Para aprendizajes extraídos desde sesiones, agregar:

```yaml
---
confidence:
source_session:
---
```

---

# 4. Definición de propiedades

## 4.1 `type`

Define qué tipo de nota es.

Es la propiedad más importante.

Valores recomendados:

```yaml
type: constitution
type: user_preference
type: project
type: area
type: entity
type: application
type: service
type: technology
type: tool
type: integration
type: workflow
type: storage
type: api
type: concept
type: learning
type: decision
type: known_error
type: runbook
type: command
type: pattern
type: session
type: raw_session
```

Ejemplos:

```yaml
type: learning
```

```yaml
type: application
```

```yaml
type: integration
```

```yaml
type: raw_session
```

Uso esperado:

- `type` permite clasificar la nota.
    
- Ayuda a Graphify a encontrar términos explícitos.
    
- Ayuda a los agentes a saber cómo interpretar el contenido.
    
- Ayuda a Obsidian Bases/Dataview a filtrar.
    

---

## 4.2 `scope`

Define el nivel principal donde aplica la nota.

Valores recomendados:

```yaml
scope: global
scope: user
scope: area
scope: project
scope: application
scope: service
scope: integration
scope: technology
scope: tool
scope: workflow
scope: storage
scope: api
scope: concept
scope: session
```

Ejemplos:

```yaml
scope: global
```

```yaml
scope: project
```

```yaml
scope: application
```

```yaml
scope: integration
```

Regla:

```text
Una nota tiene un scope principal.
Si toca varias cosas, se enlazan en entities.
```

Ejemplo correcto para una integración:

```yaml
type: learning
scope: integration
project: "[[Echo Forge]]"
entities:
  - "[[SQX Export Plugin]]"
  - "[[Echo Forge Importer]]"
  - "[[overview_json]]"
```

Cuándo crear una sola memoria:

```text
Cuando el conocimiento describe una relación entre entidades.
```

Ejemplo:

```text
SQX Export Plugin produce overview_json consumido por Echo Forge Importer.
```

Cuándo crear varias memorias:

```text
Cuando el conocimiento genera obligaciones distintas para cada entidad.
```

Ejemplo:

```text
SQX Export Plugin debe validar indicadores antes de exportar.
Echo Forge Importer debe rechazar overview_json sin indicadores.
```

---

## 4.3 `created`

Fecha de creación de la nota.

Formato recomendado:

```yaml
created: 2026-06-27
```

Uso:

- trazabilidad;
    
- orden cronológico;
    
- auditoría;
    
- filtros en Obsidian.
    

---

## 4.4 `updated`

Fecha de última actualización significativa.

Formato recomendado:

```yaml
updated: 2026-06-27
```

Uso:

- saber si la nota está fresca;
    
- detectar notas viejas;
    
- priorizar revisión;
    
- evitar que agentes tomen como actual conocimiento no revisado hace mucho tiempo.
    

No se debe actualizar por cambios menores de formato.

---

## 4.5 `area`

Área general del second brain.

Ejemplos:

```yaml
area: "[[Trading Algorítmico]]"
```

```yaml
area: "[[Homelab]]"
```

```yaml
area: "[[Second Brain]]"
```

Uso:

- navegación humana;
    
- agrupación por dominio;
    
- filtros de alto nivel.
    

No todas las notas necesitan `area`, pero es recomendable para memorias reutilizables.

---

## 4.6 `project`

Proyecto principal relacionado.

Ejemplo:

```yaml
project: "[[Echo Forge]]"
```

Uso:

- cargar contexto por proyecto;
    
- filtrar memorias;
    
- conectar entidades;
    
- buscar desde Graphify por nombre de proyecto.
    

Si una memoria es global o de usuario, puede omitirse.

---

## 4.7 `application`

Aplicación principal relacionada.

Ejemplo:

```yaml
application: "[[SQX Export Plugin]]"
```

Uso:

- cargar contexto al trabajar sobre una app específica;
    
- encontrar learnings críticos de una aplicación;
    
- evitar leer todo el proyecto.
    

Si una memoria aplica a varias aplicaciones, no usar lista en `application`. En ese caso usar:

```yaml
scope: integration
entities:
  - "[[App X]]"
  - "[[App Y]]"
```

---

## 4.8 `entities`

Lista de entidades relacionadas.

Ejemplo:

```yaml
entities:
  - "[[SQX Export Plugin]]"
  - "[[Echo Forge Importer]]"
  - "[[overview_json]]"
  - "[[Mongo Strategy Store]]"
```

Uso:

- conectar notas en Obsidian;
    
- alimentar Graphify con relaciones explícitas;
    
- ayudar a agentes a navegar nodos relevantes;
    
- evitar duplicar memorias innecesarias.
    

Regla:

```text
entities debe contener las cosas importantes que la nota conecta.
```

Ejemplos de entidades:

```text
Aplicaciones
Servicios
Herramientas
Tecnologías
Integraciones
Workflows
APIs
Storage
Conceptos
Repositorios
Ambientes
```

---

## 4.9 `related`

Lista de notas relacionadas que no necesariamente son entidades.

Ejemplo:

```yaml
related:
  - "[[ERR-001 - SQX export sin indicadores]]"
  - "[[ADR-004 - Mantener plugin Java para export SQX]]"
  - "[[RUN-001 - Validar export SQX contra fixture]]"
```

Diferencia entre `entities` y `related`:

```text
entities = cosas del dominio.
related = documentos relacionados.
```

Ejemplo:

```yaml
entities:
  - "[[SQX Export Plugin]]"
  - "[[overview_json]]"

related:
  - "[[ERR-001 - SQX export sin indicadores]]"
  - "[[LRN-002 - SQX Export Plugin requiere fixtures]]"
```

---

## 4.10 `aliases`

Nombres alternativos de la nota.

Ejemplo:

```yaml
aliases:
  - SQX plugin
  - StrategyQuant exporter
  - export plugin
```

Uso:

- mejorar búsqueda;
    
- ayudar a Graphify;
    
- conectar nombres informales usados por agentes;
    
- evitar duplicados.
    

Recomendado especialmente para:

- aplicaciones;
    
- herramientas;
    
- tecnologías;
    
- conceptos;
    
- servicios con nombres largos.
    

---

## 4.11 `confidence`

Nivel de confianza del conocimiento.

Valores recomendados:

```yaml
confidence: low
confidence: medium
confidence: high
confidence: verified
```

Significado:

```text
low      = inferencia débil o todavía dudosa.
medium   = razonable, pero no validada completamente.
high     = validada en sesión o respaldada por evidencia clara.
verified = confirmada por implementación, test, documentación oficial o producción.
```

Uso:

- agentes pueden tratar con cuidado memorias de baja confianza;
    
- ayuda a priorizar revisión;
    
- evita convertir una inferencia en verdad canónica.
    

Ejemplo:

```yaml
confidence: high
```

No aplica necesariamente a raw sessions.

---

## 4.12 `source_session`

Sesión desde donde salió el conocimiento.

Ejemplo:

```yaml
source_session: "[[2026-06-26 - SQX export indicators]]"
```

Uso:

- trazabilidad;
    
- auditoría;
    
- reprocesamiento;
    
- saber de dónde salió un aprendizaje.
    

Recomendado para:

- aprendizajes;
    
- decisiones;
    
- errores conocidos;
    
- runbooks derivados de una sesión;
    
- cambios relevantes en entidades.
    

No obligatorio para constitución global o preferencias del usuario si fueron escritas manualmente.

---

## 4.13 `load_policy`

Define cuándo debería cargarse la nota como contexto.

Valores recomendados:

```yaml
load_policy: always
load_policy: when_user_loaded
load_policy: when_area_loaded
load_policy: when_project_loaded
load_policy: when_application_loaded
load_policy: when_integration_loaded
load_policy: when_technology_loaded
load_policy: when_workflow_loaded
load_policy: when_error_matches
load_policy: manual
load_policy: never
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

Uso:

- orientar agentes;
    
- reducir tokens;
    
- evitar lectura innecesaria;
    
- definir memoria crítica.
    

Reglas sugeridas:

```text
constitution      -> always
user_preference   -> always o when_user_loaded
project           -> when_project_loaded
application       -> when_application_loaded
integration       -> when_integration_loaded
learning          -> depende del scope
session           -> manual
raw_session       -> never
```

---

## 4.14 `indexable`

Convención interna que indica si la nota debería entrar en el corpus de Graphify.

Valores:

```yaml
indexable: true
indexable: false
```

Importante:

```text
indexable no se asume como feature nativa de Graphify.
Es una convención propia del vault.
```

Uso:

- documentar intención;
    
- filtrar con Obsidian Bases;
    
- permitir validaciones futuras;
    
- ayudar a agentes;
    
- preparar posibles scripts propios.
    

Ejemplos:

```yaml
indexable: true
```

```yaml
indexable: false
```

Reglas sugeridas:

```text
constitution      -> true
user_preference   -> true
project           -> true
application       -> true
integration       -> true
learning          -> true
decision          -> true
known_error       -> true
runbook           -> true
session           -> opcional
raw_session       -> false
```

---

## 4.15 `index_priority`

Convención interna que indica prioridad de indexación/retrieval.

Valores recomendados:

```yaml
index_priority: critical
index_priority: high
index_priority: medium
index_priority: low
index_priority: never
```

Uso:

- orientar al agente;
    
- filtrar búsquedas;
    
- diferenciar contexto crítico de contexto histórico;
    
- apoyar Graphify mediante queries más precisas.
    

Ejemplos:

```yaml
index_priority: critical
```

```yaml
index_priority: high
```

```yaml
index_priority: low
```

```yaml
index_priority: never
```

Reglas sugeridas:

```text
constitution      -> critical
user_preference   -> critical
project           -> high
application       -> high
integration       -> high
learning          -> high
decision          -> high
known_error       -> high
runbook           -> high
session           -> low
raw_session       -> never
```

---

## 4.16 `tags`

Lista de tags normalizados.

Ejemplo:

```yaml
tags:
  - kind/learning
  - scope/application
  - area/trading
  - project/echo-forge
  - app/sqx-export-plugin
  - priority/high
```

Uso:

- navegación humana;
    
- búsqueda;
    
- filtros;
    
- Obsidian Bases;
    
- soporte para Graphify;
    
- routing mental de agentes.
    

Regla:

```text
Los tags no reemplazan properties.
Los tags ayudan a filtrar y navegar.
```

Tags recomendados:

```text
kind/*
scope/*
area/*
project/*
app/*
tech/*
learning/*
priority/*
agent/*
```

Ejemplos:

```yaml
tags:
  - kind/application
  - scope/application
  - project/echo-forge
  - app/sqx-export-plugin
  - tech/sqx
```

```yaml
tags:
  - kind/learning
  - scope/integration
  - project/echo-forge
  - app/sqx-export-plugin
  - priority/high
```

```yaml
tags:
  - kind/raw-session
  - scope/session
  - project/echo-forge
```

Evitar tags vagos:

```text
#importante
#cosas
#varios
#ia
#pendiente
#proyecto
```

Esos tags no ayudan a recuperar contexto.

## 4.17 IDs semánticos

Para beta se recomienda preferir IDs semánticos sobre correlativos globales.

Idea base:

```text
learning/search-middleware/polycard-price-drop
decision/vpp-backend/tracking-visibility
known-error/java-polycard-sdk/decorator-null-context
runbook/vis-octopus-lib/release-validation
```

Uso recomendado:

- El filename debe ser humano y estable.
- El slug semántico puede vivir en `aliases` o en un campo futuro si Fase 1 lo necesita.
- Los tags ayudan a navegación (`kind/*`, `project/*`, `app/*`, `priority/*`), pero no deberían ser el único identificador.
- Evitar IDs correlativos globales (`LRN-001`) salvo que Fase 1 demuestre que simplifican automatización.

---

# 5. Metadata recomendada por tipo

## 5.1 Constitution

```yaml
---
type: constitution
scope: global
created:
updated:
entities: []
related: []
aliases:
  - agent constitution
  - reglas globales del agente
confidence: verified
load_policy: always
indexable: true
index_priority: critical
tags:
  - kind/constitution
  - scope/global
  - agent/always-load
  - priority/critical
---
```

---

## 5.2 User preference

```yaml
---
type: user_preference
scope: user
created:
updated:
entities: []
related: []
aliases:
  - user model
  - preferencias del usuario
confidence: verified
load_policy: always
indexable: true
index_priority: critical
tags:
  - kind/user-preference
  - scope/user
  - agent/always-load
  - priority/critical
---
```

---

## 5.3 Project

```yaml
---
type: project
scope: project
created:
updated:
area:
project:
entities:
related:
aliases:
confidence: high
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/project
  - scope/project
---
```

---

## 5.4 Application

```yaml
---
type: application
scope: application
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence: high
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/application
  - scope/application
---
```

---

## 5.5 Integration

```yaml
---
type: integration
scope: integration
created:
updated:
area:
project:
entities:
related:
aliases:
confidence: high
load_policy: when_integration_loaded
indexable: true
index_priority: high
tags:
  - kind/integration
  - scope/integration
---
```

---

## 5.6 Learning

```yaml
---
type: learning
scope:
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence:
source_session:
load_policy:
indexable: true
index_priority: high
tags:
  - kind/learning
---
```

Ejemplo de learning de aplicación:

```yaml
---
type: learning
scope: application
created: 2026-06-27
updated: 2026-06-27
area: "[[Trading Algorítmico]]"
project: "[[Echo Forge]]"
application: "[[SQX Export Plugin]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[overview_json]]"
  - "[[Echo Forge Importer]]"
related:
  - "[[ERR-001 - SQX export sin indicadores]]"
confidence: high
source_session: "[[2026-06-26 - SQX export indicators]]"
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
  - area/trading
  - project/echo-forge
  - app/sqx-export-plugin
  - priority/high
---
```

---

## 5.7 Decision / ADR

```yaml
---
type: decision
scope:
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence: verified
source_session:
load_policy:
indexable: true
index_priority: high
tags:
  - kind/decision
---
```

Nota:

```text
Una decisión debe describir por qué se decidió algo.
La entidad relacionada debe reflejar solo el estado vigente.
```

---

## 5.8 Known error

```yaml
---
type: known_error
scope:
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence:
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
---
```

Nota:

```text
No usar status/open/resolved como propiedad base.
Si el error ya no aplica y no sirve para contexto, se borra o se conserva solo en sesiones históricas.
```

---

## 5.9 Runbook

```yaml
---
type: runbook
scope:
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence:
source_session:
load_policy:
indexable: true
index_priority: high
tags:
  - kind/runbook
---
```

---

## 5.10 Session summary

```yaml
---
type: session
scope: session
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/session
  - scope/session
---
```

Nota:

```text
La session summary puede ser indexable con prioridad baja si Fase 1 decide incluir summaries en el corpus.
Para beta, journal se excluye por defecto de Graphify y el retrieval debe apoyarse en memoria pública/interna.
Si se habilita la indexación de summaries, nunca debería ganarle a entidades, aprendizajes, decisiones o runbooks.
```

---

## 5.11 Raw session

```yaml
---
type: raw_session
scope: session
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---
```

Regla:

```text
Raw session es respaldo retrocompatible.
No se carga como contexto normal.
No se indexa por defecto.
No debe contener logs operacionales gigantes.
```

---

# 6. Graphify y estas propiedades

## 6.1 Qué se puede asumir

Se puede asumir que Graphify funciona mejor si las notas tienen:

- nombres claros;
    
- links explícitos;
    
- entidades repetidas consistentemente;
    
- tags precisos;
    
- propiedades legibles;
    
- relaciones visibles en el cuerpo de la nota.
    

## 6.2 Qué no se debe asumir

No se debe asumir que Graphify respeta automáticamente:

```yaml
indexable: false
```

Tampoco se debe asumir que `index_priority` cambia nativamente su ranking.

Ambas son convenciones del vault.

## 6.3 Control real de indexación

El control real de qué entra a Graphify debe hacerse por:

```text
1. Ruta/carpeta usada como input.
2. .graphifyignore.
3. Estructura limpia del vault.
4. Eventuales scripts propios futuros.
```

## 6.4 Estrategia recomendada para beta

Ejecutar Graphify sobre el corpus del vault con `graphify-obsidian` y usar `.graphifyignore` para excluir lo que no debe entrar.

Ejemplo conceptual:

```gitignore
# Memoria reutilizable de agentes: incluida
!80-agents/memory/
!80-agents/memory/**

# Journal: excluido por defecto para no contaminar retrieval operativo
80-agents/journal/
80-agents/journal/**

# Raw sessions: excluidas siempre
80-agents/journal/sessions/raw/
80-agents/journal/sessions/raw/**
**/*raw-session*.md

# Excluir adjuntos y basura operacional
90-system/attachments/
90-system/attachments/**
**/*.log
**/*.tmp
**/*.zip
**/*.tar
**/*.gz
```

Nota:

```text
Este archivo es un ejemplo. Debe ajustarse a la estructura real del vault y a cómo Graphify implemente .graphifyignore.
```

---

# 7. Criterios para crear una memoria

Crear una memoria cuando el conocimiento sea:

```text
Reutilizable.
Vigente.
Aplicable a sesiones futuras.
Relacionable con entidades.
Útil para reducir tokens.
Útil para evitar errores repetidos.
```

No crear una memoria cuando sea:

```text
Conversación casual.
Detalle temporal.
Información obsoleta.
Log operacional.
Output gigante.
Idea no validada.
Algo que solo importa dentro de la sesión actual.
```

---

# 8. Criterios para borrar una memoria

Borrar una memoria cuando:

```text
Ya no representa el estado actual.
Está duplicada.
Fue reemplazada por una versión mejor.
No aporta a contexto futuro.
Confunde más de lo que ayuda.
```

Si se necesita historia, buscar en:

```text
session summaries
raw sessions
git history
```

No mantener memorias muertas “por si acaso”.

---

# 9. Ejemplos completos

## 9.1 Learning de aplicación

```yaml
---
type: learning
scope: application
created: 2026-06-27
updated: 2026-06-27
area: "[[Trading Algorítmico]]"
project: "[[Echo Forge]]"
application: "[[SQX Export Plugin]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[overview_json]]"
  - "[[Echo Forge Importer]]"
  - "[[Mongo Strategy Store]]"
related:
  - "[[ERR-001 - SQX export sin indicadores]]"
  - "[[ADR-004 - Mantener plugin Java para export SQX]]"
aliases:
  - SQX indicators learning
  - export indicators rule
confidence: high
source_session: "[[2026-06-26 - SQX export indicators]]"
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
  - area/trading
  - project/echo-forge
  - app/sqx-export-plugin
  - priority/high
---
```

---

## 9.2 Integration memory

```yaml
---
type: integration
scope: integration
created: 2026-06-27
updated: 2026-06-27
area: "[[Trading Algorítmico]]"
project: "[[Echo Forge]]"
entities:
  - "[[SQX Export Plugin]]"
  - "[[overview_json]]"
  - "[[Echo Forge Importer]]"
  - "[[Mongo Strategy Store]]"
related:
  - "[[LRN-001 - No asumir completitud de overview_json]]"
aliases:
  - SQX to Echo Forge export
  - SQX overview_json integration
confidence: high
source_session: "[[2026-06-26 - SQX export indicators]]"
load_policy: when_integration_loaded
indexable: true
index_priority: high
tags:
  - kind/integration
  - scope/integration
  - area/trading
  - project/echo-forge
  - app/sqx-export-plugin
  - priority/high
---
```

---

## 9.3 Raw session

```yaml
---
type: raw_session
scope: session
created: 2026-06-27
updated: 2026-06-27
area: "[[Trading Algorítmico]]"
project: "[[Echo Forge]]"
application: "[[SQX Export Plugin]]"
entities:
  - "[[SQX Export Plugin]]"
  - "[[Echo Forge Importer]]"
related:
  - "[[2026-06-27 - SQX export indicators summary]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
  - area/trading
  - project/echo-forge
  - app/sqx-export-plugin
---
```

---

# 10. Resumen final

Metadata base recomendada:

```yaml
---
type:
scope:
created:
updated:
area:
project:
application:
entities:
related:
aliases:
confidence:
source_session:
load_policy:
indexable:
index_priority:
tags:
---
```

Campos eliminados del modelo base:

```yaml
status:
draft:
```

Decisiones clave:

```text
scope es primario.
entities conecta múltiples entidades.
status no se usa; memoria obsoleta se borra.
draft no se usa como propiedad base.
indexable e index_priority son convenciones propias.
Graphify se controla realmente por rutas y .graphifyignore.
```

Regla final:

```text
Una memoria útil debe decir qué se sabe, a qué aplica, con qué entidades se relaciona, cuándo cargarla y qué confianza tiene.
```
