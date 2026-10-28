---
type: change_log
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
entities:
  - "[[Echo — I+D de Estrategias]]"
  - "[[Echo I+D — Futures]]"
  - "[[Echo I+D — Cobertura Futures]]"
  - "[[FUT-R01-RESEARCH-MANDATE]]"
related:
  - "[[30-resources/agents/skills/echo-futures-research-manager/SKILL]]"
aliases: []
confidence: verified
source_session: "Conversación Owner — Echo Futures Research Director, primera ronda, 2026-10-27 America/Santiago"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# FUT-R01 — Mandato Owner, cobertura y bases de investigación

## Cambio

- **Tipo:** updated + created + conflict-resolution.
- Actualizados [[Echo — I+D de Estrategias]], [[Echo I+D — Futures]] y [[Echo I+D — Cobertura Futures]]; creados [[FUT-R01-RESEARCH-MANDATE]] y este registro.
- Se conserva un programa, dos divisiones y el planner Futures existente. FUT-R01 pasa de READY_FOR_MANAGER a recuperación documental/entrevista en curso.
- Registradas metas y preferencias Owner, preguntas abiertas, evidencia R03 reutilizable y correcciones de mapeo de código. Preparado un prompt ONE-SHOT para fundamentos, cobertura y economía, más plantilla de recuperación física read-only.

## Motivo

El Owner pidió documentar el proyecto para continuar, orientar el trabajo por cobertura y preparar bases de anatomía de estrategias, indicadores, métricas, familias y RR. Precisó el objetivo de trading efectivo y el hito al 31-12-2026 de cinco estrategias challenge y cinco funded retirando, en al menos dos props simultáneamente. Esta autorización cubre los cambios documentales presentes; no compras, campañas, código de producto, producción ni cierre formal.

## Fuentes usadas

- Instrucciones iniciales y primera ronda del Owner del 2026-10-27 America/Santiago; ejecución de lectura/escritura en UTC 2026-10-28. No se cambia la fecha de referencia comercial del mandato.
- Autoridades canónicas ya cargadas: bootstrap/core aplicable, manager Futures, ciclo I+D, retester y cualificación. Para la escritura: agents-os-entity-update, conflicto, note-types, metadata-schema y contrato ejecutable de schemas.
- Agents-OS leído inicialmente en `5418dbfbaba7524a3aa6a09c35f4cf1ff5716017`; la publicación requiere reconciliar el HEAD y las notas afectadas antes de actualizar master.
- Código de `xKoRx/echo@ae1b09bc10370806f7648f076c5fa0825c9efa4e`: TG, FBC, ORB, MR variants.go, variants2.go y mr.go; R03-STATUS y R03-DECISION-STRATEGIES. Enlaces exactos en matriz y planner.
- Fuentes primarias localizadas para el mandato: Bailey et al., referencia institucional de Gao et al. y documentación oficial Topstep API/live; alcance de lectura y enlaces en el prompt. No se ha completado una comparación comercial ni seleccionado prop.
- Workers Cloud acotados y read-only: anatomía/cobertura, economía/denominadores y diseño de investigación; revisión independiente enfocada antes de publicación. La escritura permanece en un único integrador.

## Resolución aplicada

| Tema | Antes / fuente | Resolución actual y alcance |
|---|---|---|
| Propósito operativo | Investigación continua para challenge/retiros | Owner explicita trading efectivo y autosostenimiento como resultado; se mantiene programa permanente, sin apropiarse de Forex o producto. |
| Objetivo táctico | Sin objetivo numérico vigente en el planner recién organizado | Registrar 5 challenge + 5 funded con retiros, mínimo dos props simultáneas, al 31-12-2026. Meta aceptada; factibilidad, superposición y sostenibilidad no demostradas. |
| Capital | Nueva intervención menciona USD 5.000 y cerca de USD 4.000 | Ambigüedad conservada. No inventar techo autorizado, asignación a Futures ni política de compras. |
| Tasas 1/10 y 1/3 | Aspiraciones Owner sin denominador/horizonte completo | Registrar objetivos; proponer cohortes, cadena de cobro y ledger. Matemática condicional ilustrativa no convertida en estimación. |
| ClutiFX | Planner decía línea secundaria | Instrucción expresa Owner prevalece: histórico, sin nuevas investigaciones salvo decisión expresa. No borrar evidencia ni reabrir entrega. |
| Cobertura | MR10 omitida; MR08 situada en persistencia sin matiz | MR10 incorporada y MR08 descrita como reversión local condicionada por tendencia H1 según predicados leídos. Clasificación propuesta; no conformance ni independencia acreditada. |
| FBC y unidades | Riesgo de confundir sigla, TF, filtros/MM y familias | Mantener primera vela/color; no failed breakout. Separar identidad de estrategia, variante, configuración, MM, programa y reglas. |
| R03 | Evidencia heredada de campañas y shortlist | Recuperar receipt válido sin rerun; simulación histórica, REVIEW, confirmación retrospectiva y muestras limitadas. No funded real ni autorización runtime. |
| Deep Research | Owner propone investigar bases | Prompt concreto preparado para una o tres IAs y revisión integrada; no investigación exhaustiva fingida ni roadmap definitivo. |
| Autorización | Documentar y preparar siguiente trabajo | Sólo notas canónicas y herramientas documentales existentes. No nuevos gates, skills, managers, programas o procesos autónomos. |

## Validación

- Nuevas notas materializadas con el script canónico `materialize_schema_note.py`, tipos prompt y change_log, ambos exit 0; no se escribió un frontmatter nuevo saltando el contrato.
- Conservadas identidades, relaciones y autoridades de los documentos existentes; revisadas diferencias semánticas y límites de atribución.
- Lint canónico dirigido de los cinco archivos: exit 0, ERROR=0, WARN=0, cinco notas verificadas; sin validación masiva del vault.
- Revisión independiente económica: corregida la condición de la expectativa de cobros entre treinta cuentas; probabilidad marginal hipotética explícita y ausencia de garantía. Sin otros defectos materiales en el alcance revisado.
- Reconciliación: master avanzó de `5418dbfbaba7524a3aa6a09c35f4cf1ff5716017` a `cf459cf6dd5f775d87b1fe543d6252d1fbba3b8a`; las tres notas existentes conservaban exactamente contenido/blob originales y las dos rutas nuevas no existían. Publicación preparada sobre el árbol vigente, sólo cinco archivos, con avance fast-forward y lease; sin rama/PR ni force.
- La verificación física de Hefesto, cualificación G0–G5 y rentabilidad no forman parte de esta validación documental.

## Compartibilidad

- **Scope:** local; registro técnico de continuidad del Owner.
- **Redacción revisada:** sin credenciales ni secretos; incluye decisiones de capital del proyecto y referencias a repositorios autorizados. No enviar ni compartir externamente como efecto de esta publicación.

## Rollback

Revertir únicamente este conjunto documental mediante un nuevo commit auditable sobre master, reconciliando cambios concurrentes. No resetear/forzar HEAD, no tocar artefactos históricos de laboratorio ni revertir trabajo de otros owners. Las decisiones Owner seguirán requiriendo registro correcto aunque se corrija la representación documental.

