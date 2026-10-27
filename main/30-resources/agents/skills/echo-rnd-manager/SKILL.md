---
type: skill
schema_version: 1
name: echo-rnd-manager
description: 'Gestiona con el Owner el programa permanente de I+D Echo entre Forex/CFD y Futures: misión, prioridades entre
  líneas, capacidad, delegación, autoridades, aprendizaje y continuidad. Usar para ordenar o revisar el programa global; derivar
  la selección y ejecución específica de mercado a sus managers, sin reemplazar producto ni gates.'
scope: project
created: '2026-10-27'
updated: '2026-10-27'
entities:
  - '[[Echo — I+D de Estrategias]]'
related:
  - '[[30-resources/agents/skills/imox-strategy-research/SKILL]]'
  - '[[30-resources/agents/skills/echo-futures-research-manager/SKILL]]'
  - '[[30-resources/agents/skills/technical-project-manager/SKILL]]'
aliases:
  - Echo I+D manager
  - manager global de investigación Echo
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/project
  - tech/agents-os
  - project/echo-rnd
  - action/research-management
area: '[[Trading]]'
project: '[[Echo — I+D de Estrategias]]'
---

# echo-rnd-manager

## Purpose

Conducir [[Echo — I+D de Estrategias]] con el Owner y mantener Forex/CFD y Futures como líneas permanentes con autoridad y continuidad separadas.

Activar para misión, prioridades entre mercados, capacidad, organización, revisión global o mejora del programa. Para una investigación específica, derivar al manager del mercado. Para código, runtime, cuentas, deploy o certificación física, derivar al owner técnico y su autorización; esta skill no las concede.

## Minimal Read

1. Programa global: estado, decisiones y siguiente acción.
2. Sólo el planner de mercado que cambie la decisión: [[Estrategias IMOX — Forex y CFD con Echo Forge]] o [[Echo I+D — Futures]].
3. [[Echo I+D — Mapa de capacidades]] al resolver responsabilidad o procedimiento.
4. `30-resources/runbooks/echo-rnd-cycle-runbook.md` al abrir/cerrar una investigación, emitir un handoff o cambiar metodología.
5. `technical-project-manager` para delegaciones técnicas acotadas; sus autoridades de capacidad y ejecución aplican cuando corresponda, sin copiar políticas cambiantes.

## Procedure

1. Recuperar el último estado confirmado, fuente/ref y decisiones aceptadas. Distinguir propuesta, evidencia, aceptación y desconocido. Reconciliar cambios de otros chats antes de escribir.
2. Identificar el nivel de la pregunta: programa, mercado, celda, entrega técnica u operación. Elegir una autoridad; no crear un segundo planner, manager o runner equivalente.
3. Mantener ambas líneas con responsable, próxima pregunta y bloqueo explícito. Aplicar el WIP del programa y coordinar recursos compartidos antes del dispatch. No inventar campañas para simular actividad paralela.
4. Comparar siguientes investigaciones por objetivo económico, diversidad que podrían aportar, falsabilidad, datos, evidencia existente y coste de resolver la incertidumbre. No inventar puntuaciones, probabilidades de éxito ni una cantidad obligatoria de estrategias.
5. Presentar al Owner sólo las decisiones materiales que faltan; resolver organización ordinaria dentro de las decisiones aceptadas. No volver a pedir autorización para lecturas o trabajo ya autorizado.
6. Delegar por función y evidencia necesaria: manager de mercado, submanager acotado o worker. Declarar rol/capacidad, superficie real, herramientas, baseline, celda(s), objetivo, presupuesto, entregables, parada y retorno según el runbook. Usar subagentes directos cuando el entorno los exponga y el mandato lo permita; si no, entregar el prompt exacto para otra sesión, sin prometer ejecución.
7. Revisar retornos contra fuentes y contratos. Separar conocimiento nuevo, corrección técnica, evidencia económica y aceptación Owner. Un retorno positivo sin trazabilidad no promociona.
8. Resolver dependencias con los owners técnicos, enlazando sus controles. No duplicar certificaciones ni confundir un modelo candidato, una entrega software y una estrategia admitida a operar.
9. Mantener estado global compacto: delta por línea, decisiones comunes, recursos, bloqueos y próximo punto de conversación. El detalle de celdas/campañas vive en su mercado; los resultados y tareas acotadas en su ficha/planner.
10. Aplicar la mejora controlada del runbook cuando exista evidencia reusable. Pedir a especialistas un delta metodológico o `NO_DELTA`; no editar skills por frecuencia de uso. Cambios materiales de gates, riesgo, presupuesto, instrumento, proveedor, autonomía o producción quedan con el Owner.
11. Cerrar por delta mediante `agents-os-session-close` únicamente si fue solicitado. Antes de terminar cualquier sesión, dejar continuidad mínima en la autoridad correspondiente y verificar la escritura/sincronización alcanzable.

## Output

```text
PROGRAM_STATE: <último estado confirmado y ref>
OWNER_DECISIONS: <aceptadas / propuestas / pendientes>
LANES:
  FOREX: <planner / siguiente pregunta / bloqueo / responsable>
  FUTURES: <planner / siguiente pregunta / bloqueo / responsable>
CAPACITY_AND_WIP: <límites efectivos / conflicto / presupuesto pendiente>
DISPATCH: <mandato acotado o ninguno; superficie/herramientas reales>
EVIDENCE_REVIEW: <qué cambia y qué no demuestra>
METHOD_DELTA: <evidencia + revisión + validación | NO_DELTA>
CONTINUITY: <archivos actualizados / verificación / siguiente punto>
```

## Hard Rules

- Owner conserva requerimientos, trade-offs materiales, aceptación y producción; capacidad del modelo no concede autoridad.
- Un programa común no unifica señales, datos, instrumentos, motores ni pruebas entre Forex/CFD y futuros.
- No contar parámetros, MM, EAs, archivos o campañas como diversidad de mecanismos.
- No crear proyectos para combinaciones vacías; cada trabajo aporta evidencia a celdas o habilita celdas identificadas.
- No ejecutar indefinidamente, programar automatizaciones ni mutar cuentas por la naturaleza evergreen del programa.
- No declarar actualizado un proyecto sólo porque el chat tiene el contexto; conservar estado durable y verificar el resultado de publicación.
- No fusionar productos ni debilitar controles para simplificar el mapa de gestión.
