---
type: change_log
schema_version: 1
scope: session
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Evaluación y Adopción]]"
  - "[[2026-09-09-agents-os-hygiene-cycle]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
  - change/distribution
---

# Core compartible regenerado y Grid actualizado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created (build reproducible) + updated (fuentes canónicas y entregable remoto) + deleted (artefactos generados superseded)
- **Archivo(s):**
  - `30-resources/agents-os/core-export/` — `sources.list`, `build-core.py`, `dist-files/` y `README.md`, nuevos.
  - `30-resources/agents-os/README.md` — sección del core compartible.
  - `80-agents/skills/agents-os-bootstrap/SKILL.md`, `agents-os-behavior-config/SKILL.md`, `agents-os-install/SKILL.md`, `80-agents/agents-os/agents-os.md`, `80-agents/memory/public/decision/agents-os/public-vs-internal-memory.md` — el perfil global se resuelve por directorio y el proyecto de instalación por búsqueda.
  - `80-agents/skills/agents-os-doctor/scripts/doctor.py` y su `SKILL.md` — resolución portable del perfil always-load y exclusiones genéricas de `.graphifyignore`.
  - `70-templates/service-operational.md` — el bloque de fuentes dejó de traer rutas absolutas de una máquina.
  - `.graphifyignore` — exclusión del staging de `core-export/`.
  - `10-projects/Economía de Tokens/agentes/AGENTS OS - Evaluación y Adopción/` — `agents-os-grid.source.json` y `build-grid.py` nuevos, `agents-os-grid.html` generado, nota de proyecto actualizada; se eliminaron `agents-os-evaluacion-grid.html` y `agents-os-evaluacion-grid.source.json`.

## Motivo

- El core compartible tenía casi dos meses y no reflejaba el sistema vigente. El owner pidió reemplazarlo por el estado actual, con prompt de instalación para Codex y Claude, y actualizar el entregable remoto para que transparente promesa contra realidad en vez de venderse.

## Fuentes usadas

- Las fuentes canónicas del vault como origen del core; el pack de ChatGPT como referencia del contrato de empaquetado.
- El reporte Kaizen y el reporte de higiene del 2026-09-09 como base factual del entregable remoto.
- La skill oficial de Grid en su versión vigente para el contrato de publicación.

## Resolución aplicada

- El export dejó de ser una copia manual y pasó a ser un build declarativo: selección en `sources.list`, material autoral en `dist-files/`, verificación SHA-256 por archivo y guardas que abortan si memoria interna o journal alcanzan la salida.
- Se corrigieron cuatro defectos de portabilidad que sólo se ven al instalar en otra máquina: el nombre del archivo de perfil estaba hardcodeado en cuatro fuentes canónicas y en el doctor; el doctor exigía subrutas de empaquetado propias de este vault; una skill referenciaba por ruta fija un proyecto que no existe en una instalación nueva; y un template llevaba rutas absolutas de una máquina como ejemplo.
- El core ya no viaja con binarios de índice, notas de aplicaciones reales, superficies del owner ni la página de recursos que persiste paths locales. El registro de superficies y el catálogo de aplicaciones viajan vacíos con su contrato.
- El entregable remoto cambió de forma: en vez de un score global, siete promesas con veredicto, evidencia y salvedad. El builder anterior dependía de un generador externo ausente del vault, así que era irreproducible; el nuevo es autocontenido y separa datos de presentación.

## Validación

- Build: 191 archivos canónicos + 13 autorales, 39 skills, 3 filas de índice descartadas por skill no embarcada, igualdad SHA-256 en todos los archivos.
- Sobre el destino: `doctor --strict` `HIGH=0 MEDIUM=0 LOW=0` con startup ≈4466 tokens; `lint --check` `0 ERROR / 0 WARN` sobre 88 notas; contrato de schema `0 errores`.
- Auditoría del destino: cero apariciones de identidad del owner y cero rutas absolutas de máquina.
- Sobre el vault de origen tras los cambios: `doctor --strict` limpio y `lint --gate` en `GO`.
- Grid: versión 4 publicada con control de concurrencia (`if_version=3`). El payload JSON descargado desde el documento remoto es idéntico byte a byte al local; la diferencia de tamaño corresponde sólo a la inyección estándar del runtime de Grid.

## Compartibilidad

- **Scope:** team — el build, las correcciones de portabilidad y el contrato del entregable son agnósticos de persona, modelo y máquina.
- **Redacción revisada:** sin identidad, sin paths locales, sin memoria interna, sin secretos.

## Rollback

- El core se reconstruye con `python3 30-resources/agents-os/core-export/build-core.py`; el destino es material derivado y no contiene nada que no esté en el vault.
- Las correcciones de portabilidad son ediciones puntuales reversibles una por una.
- El Grid conserva su historial de versiones: la versión 3 se restaura con `POST /documents/{doc_id}/rollback`.

## Pendiente para el owner

- El documento de Grid está compartido con una persona además del owner, así que la versión 4 ya cambió lo que esa persona ve.
- El metadato `entry_point` del documento remoto conserva el nombre de archivo de la versión 1. La descarga y la vista sirven el contenido nuevo, así que no bloquea nada; corregirlo requiere un PATCH aparte.

## Addendum — 2026-09-09, corrección de conteo y README para lectores nuevos

- **Conteo de skills corregido.** `build-core.py` derivaba el total desde segmentos de ruta, así que contaba `_shared` e `INDEX.md` como skills y reportaba 39. El total real es **37 embarcadas** de **40 canónicas** en el vault. Se corrigió el script para contar `SKILL.md`, y se corrigieron las tres cifras afectadas en el Grid, publicado como versión 5. La afirmación "36 sin entrada nativa" seguía siendo correcta: cambió el denominador (40, no 39), verificado contra los routers reales del cliente.
- **Baseline del lint de la distribución.** El paquete embarcaba el baseline del vault de origen, así que una instalación nueva heredaba nueve deudas ajenas y el gate reportaba `resolved=13`. Ahora `dist-files/` provee un baseline vacío: una instalación limpia sale `ERROR=0 WARN=0 baseline_ERROR=0`.
- **README reescrito** para una persona que nunca vio el sistema, con la skill `human-first-technical-writing`. Se agregaron introducción, ejemplo del problema, glosario en primer uso, taxonomía explícita de evidencia (observado / autoevaluación del agente / no medido) y sección de contribución. Se corrigieron dos afirmaciones imprecisas: el perfil no viene "en blanco" sino con reglas semilla por confirmar, y `share_scope` no es obligatorio en toda nota sino sólo en los registros de cambio.
- **Se documentó una limitación que antes no estaba declarada:** 48 de 170 archivos Markdown del paquete conservan nombres de proyectos, servicios o herramientas del entorno de origen, casi siempre como ejemplos en plantillas o citas de evidencia en learnings. Identidad de personas, credenciales y rutas absolutas de máquina siguen en cero, verificado. La limpieza de ejemplos queda pendiente y ahora está declarada en el README en vez de omitida.
