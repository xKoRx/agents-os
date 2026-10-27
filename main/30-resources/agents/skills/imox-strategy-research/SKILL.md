---
type: skill
schema_version: 1
name: "imox-strategy-research"
description: "Planifica y mantiene investigación de estrategias IMOX en el vault: roadmap, cobertura, campañas, reutilización y aprendizaje con evidencia; deriva presets SQX y operación técnica a sus procedimientos."
scope: "workflow"
created: "2026-10-24"
updated: "2026-10-24"
entities: []
related: ["[[Estrategias IMOX — Forex y CFD con Echo Forge]]", "[[IMOX]]"]
aliases: []
load_policy: "when_managing_imox_strategy_research"
indexable: true
index_priority: "high"
tags: ["kind/skill", "scope/workflow", "tech/agents-os", "topic/imox", "action/research-management"]
area: "[[Trading]]"
methodology_revision: 1
---

# imox-strategy-research

## Purpose

Conducir proyectos de investigación de estrategias IMOX: roadmap, cobertura, campañas, reutilización y aprendizaje verificable. Aplicar al planificar o actualizar el trabajo de estrategias en el vault. Para preparar presets SQX, usar `sqx144-campaign-design`; para ejecutar/cambiar Forge, Echo o Futures, usar el procedimiento de su owner técnico.

## Minimal Read

1. Resolver el proyecto activo y leer su estado, decisiones y próxima acción; no cargar todos sus registros.
2. Abrir su contrato de campañas y cobertura solo al crear/actualizar esos registros.
3. Abrir fuentes IMOX específicas únicamente para la decisión metodológica que cambia; distinguir texto del administrador, experiencia de miembros y análisis propio.

## Procedure

1. Resolver si se pide planificación, diseño, registro de resultado o ejecución. Respetar fases diferidas; no convertir un plan en autorización de acceder a workers o lanzar campañas.
2. Comparar el roadmap con capacidad humana/técnica disponible. Mantener un WIP explícito y reducir alcance antes de bajar gates por calendario. No prometer cantidad de estrategias ni rentabilidad.
3. Antes de proponer nuevos minados, consultar inventario/procedencia de lo existente. Si el rescate está diferido, registrar desconocidos y planear sin inventar cobertura del legado.
4. Definir la celda de investigación por producto/instrumento, lógica, dirección, TF/horizonte y sesión/régimen cuando importen. Separar hipótesis, preset reusable, variante, campaña, run y candidata.
5. Usar el contrato del registro del proyecto al materializar fichas mediante templates del vault. Una ficha es autoridad; índices/tablas son vistas. Mantener estados de preparación/ejecución/evaluación separados y exigir evidencia para promoverlos.
6. Para diseñar bloques, invocar `sqx144-campaign-design` con versión, catálogo real y criterio de evaluación. Reutilizar una tesis con delta de receta explícito; no transferir resultados entre CFD y futuros, brokers o TF sin contrastarlos.
7. Registrar input congelado, policy/revisión, referencias de ejecución y resultado. No-resultado por infraestructura y resultado negativo de tesis reciben outcomes distintos. Conservar los datos de evaluación vistos por agentes para detectar contaminación de holdout.
8. Al cerrar o bloquear un experimento, extraer la decisión reutilizable y actualizar estado, cobertura y próxima acción. No copiar logs grandes ni credenciales al vault.
9. Mejorar el procedimiento solo ante delta durable: fallo reproducido, nueva fuente contrastada o aprendizaje que cambie decisiones futuras. Separar actualización del estado de campaña de cambio metodológico. Si cambia la skill, registrar motivo/evidencia, cambio acotado, caso de aplicación y change_log; conservar la revisión usada por campañas previas.
10. Antes de ampliar símbolos/TF, comprobar coste y valor de la siguiente celda. Revisar reutilización, diferencias de producto y frontera de integración. No declarar Echo admitido/demo/live a partir de finalista Forge o certificación pre-Echo.

## Output

Entregar objetivo y horizonte; estado real/cobertura/desconocidos; siguiente experimento y dependencias; qué se reutiliza y qué debe revalidarse; fichas e índices tocados; evidencia de cambios de estado; aprendizaje y revisión metodológica si corresponde. Declarar qué no se ejecutó.

## Hard Rules

- Guardar conocimiento y resultado en sus entidades canónicas, no en el cuerpo de esta skill.
- No crear un universo de campañas vacías para cada combinación; materializar solo trabajo priorizado.
- No «auto-mejorar» bajando gates, cambiando objetivos de riesgo o reinterpretando resultados antiguos silenciosamente. Una revisión nueva conserva la anterior y su procedencia.
- No considerar auto-mejora la edición automática en cada uso: sin aprendizaje durable, no tocar la skill.
- Este workflow no modifica software ni concede ejecución de campañas; las autorizaciones concretas pertenecen al pedido y a los owners aplicables.
