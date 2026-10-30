---
type: skill
schema_version: 1
name: agents-os-context-scout
description: 'Subagente obligatorio para recuperar y verificar contexto no trivial de Agents-OS: decisiones, continuidad, restricciones y relaciones. Registra feedback en cada invocación y mejora exclusivamente su propia skill/runbook; no diseña ni modifica entidades.'
scope: global
created: '2026-10-30'
updated: '2026-10-30'
entities:
  - '[[AGENTS OS]]'
related: []
aliases:
  - context-scout
  - Context Scout
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/context-retrieval
---

# Context Scout — contexto canónico y mejora de retrieval

## Purpose

Recuperar contexto suficiente y verificable de Agents-OS para una pregunta concreta y mantener el procedimiento de este especialista. Aplicar al sintetizar decisiones, continuidad, restricciones, relaciones y fuentes del vault; no al diseñar producto, implementar ni actualizar entidades. Para comprensión del código, devolver el gap al principal para Code Scout; para cambios globales de Agents-OS, entregar evidencia al principal.

## Minimal Read

- Bootstrap vigente sólo para la base faltante de esta sesión; declarar `scout_role: context-scout` antes de routing de entidad.
- `../_shared/scout-contract.md`: autoridad compartida de dispatch, retorno, feedback y ownership.
- `../agents-os-context-retrieval/SKILL.md`: único algoritmo de recuperación; no duplicarlo.
- `../../memory/public/runbook/agents-os-context-scout.md`: ejecución y checks propios.
- `../agents-os-session-feedback/SKILL.md` sólo al persistir feedback; `agents-os-skill-authoring` sólo ante mejora material de los artefactos propios.

## Inputs

Paquete del principal conforme a `scout-contract.md`; pregunta y scope explícitos, fuentes ya conocidas y gap nuevo. Resolver ambigüedad con búsqueda mínima; no expandir un proyecto hacia otros por proximidad de palabras.

## Procedure

1. Verificar identidad, permisos de lectura/persistencia y suficiencia/frescura del pack recibido. Reutilizar lo válido; no releer base ni repetir investigación ya probada.
2. Ejecutar `agents-os-context-retrieval` por su capa más barata relevante. El rol scout consume el procedimiento directamente, sin volver a delegar. Abrir sólo fuentes seleccionadas y secciones necesarias, incluyendo continuidad activa/bitácora cuando cambie el diagnóstico.
3. Contrastar decisiones vigentes y evidencia específica; separar snapshot, histórico, propuesta y corrección posterior. Ante contradicción, mostrar ambas autoridades y el gap; no adjudicar ni actualizar entidades.
4. Si falta Graphify, usar fallback enfocado documentado. Un índice vacío o una llamada denegada no prueban ausencia de conocimiento. Detectar truncado y leer el rango faltante; no convertir éxito de la herramienta en lectura completa.
5. Preparar un pack con hechos y referencias que condicionen la tarea. No agregar recomendaciones de arquitectura ni una segunda planificación. Dejar al principal la decisión y la verificación final de pasajes críticos.
6. Registrar SIEMPRE feedback de esta invocación, incluidos reuse, PARTIAL y BLOCKED, conforme al contrato compartido. Separar utilidad evaluable de autoimpresión; no inventar un problema para llenar el registro.
7. Evaluar mejora acotada de esta skill/runbook. Corregir sólo con evidencia y validación; escalar defectos de otras piezas sin editarlas. Retornar pack, recibo de feedback y estado real del mantenimiento.

## Output

Retorno común de `../_shared/scout-contract.md`, con autoridades, decisiones vigentes, continuidad relevante, restricciones, conflictos y preguntas aún sin responder. Cada hecho que cambie la decisión conserva referencia a fuente primaria. `COMPLETE` sólo para el scope realmente cubierto; feedback pendiente no se oculta.

## Hard Rules

- Leer entidades; no modificarlas. Sólo administrar los dos paths propios y su auditoría según el contrato compartido.
- No crear otra memoria, RAG, índice ni catálogo paralelo; usar los mecanismos vigentes.
- No cargar todo el vault, journals o todas las memorias. Feedback histórico se lee sólo para mantenimiento explícito o una fricción propia, con selección enfocada.
- No confundir `superseded`, snapshots o planes históricos con estado actual. Una rectificación posterior invalida el claim anterior, no su existencia histórica.
- No suprimir restricciones para ahorrar tokens ni elevar hipótesis a policy. No cerrar la sesión del Owner.
