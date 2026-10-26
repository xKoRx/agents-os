---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
related: ["[[IMOX]]"]
aliases: []
tags: ["kind/doc", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
project: "[[Estrategias IMOX — Forex y CFD con Echo Forge]]"
---

# IMOX — Registro de campañas

## Propósito

Definir una ficha canónica por campaña de [[Estrategias IMOX — Forex y CFD con Echo Forge]] y una vista derivada para distinguir lo propuesto, listo, ejecutado y aprendido. Esta nota es el contrato del registro, no un segundo historial de cada campaña.

## Contenido

### Unidad de investigación y de ejecución

- **Celda de cobertura:** carril/producto × activo/instrumento × lógica × dirección × timeframe/horizonte; sesión/régimen son dimensiones adicionales cuando cambian la tesis. El broker/feed es parte de la receta; NDX cash CFD y un futuro NQ no comparten validación por nombre.
- **Hipótesis:** comportamiento falsable que se busca explotar. Puede tener varias recetas/presets y varias campañas.
- **Familia de preset:** selección semántica de bloques, orden, filtros y salidas. La variante fija versión SQX, rangos, símbolo, sesiones y costes.
- **Campaña:** experimento con receta y criterios congelados. Agrupa ejecuciones y conserva cambios de versión como nueva campaña/receta cuando alteran la pregunta.
- **Run:** intento físico identificado por Forge. Retry técnico no es nuevo experimento; registrar el vínculo al original y outcome.
- **Cohort heredado:** material previo aún por inventariar. No fingir conocer la campaña original ni adjudicar fechas/versión/autoría no demostradas.

### Ficha mínima y campos para vistas

Materializar cada ficha como `type: doc` por el contrato del vault, en `campanas/`, con `project: [[Estrategias IMOX — Forex y CFD con Echo Forge]]`, `research_record: campaign`, `campaign_id`, `campaign_state` y rutas a evidencia. No crear un tipo paralelo de frontmatter sin contrato.

| Grupo | Contenido requerido |
|---|---|
| Identidad | ID estable propuesto `IMX-FX-AAAA-NNN`, título, hipótesis y vínculos de deriva/reutilización; reservarlo antes de ejecutarlo. |
| Cobertura | Carril, activo canónico, símbolo broker, producto, lógica, dirección, TF, horizonte y sesión/régimen. No rellenar desconocidos por inferencia. |
| Diseño | Tesis y criterio de descarte previos, receta/preset y revisión, IDs de bloques/roles, compatibilidad SQX/motor y delta respecto de su antecedente. |
| Datos | Dataset/versionado o hash, broker/feed, sesiones, costes, periodos IS/selección/evaluación y registro de qué datos vio el agente. |
| Presupuesto | Tiempo/candidatas/cómputo acordados y condición de parada. |
| Evaluación | Policy/revisión de gates, reglas congeladas, cobertura temporal, contraste de motores y qué constituye un candidato elegible. |
| Ejecución | Config/FlowRun/artefactos reales, fechas y outcome físico; por ahora no inventar un mapping a APIs de Forge. |
| Resultado | Candidatas por etapa, causas de rechazo, coste, errores, decisión y contribución al conjunto. Distinguir fallo operativo de tesis no apoyada. |
| Aprendizaje | Evidencia, límite de generalización y siguiente experimento; indicar si amerita cambiar el procedimiento de la skill. |

### Estados de campaña

`idea` → `designed` → `prepared` → `running` → `evaluating` → `closed`.

- `prepared` requiere paquete compatible y criterios previos completos; una selección de bloques en prosa todavía es `designed`.
- `blocked` puede interrumpir el ciclo con causa y condición de reanudación. `parked` es decisión de priorización.
- Al cerrar, registrar outcome separado: `candidate`, `no_edge_supported`, `inconclusive` o `execution_failed`. No cerrar como «sin edge» un error de datos/motor.
- Después de campaña, cada candidata tiene estado propio de validación/admisión/seguimiento. El estado de campaña no se recicla como estado live de la EA.
- El registro legado permanece `inventory_pending` en su frente, sin crear campañas históricas ficticias.

### Vista de campañas

```dataview
TABLE campaign_id AS ID, campaign_state AS Estado, instrument AS Activo, strategy_family AS Familia, direction AS Dirección, timeframe AS TF, recipe_revision AS Receta
FROM "10-projects/Estrategias IMOX — Forex y CFD con Echo Forge/campanas"
WHERE research_record = "campaign"
SORT campaign_id ASC
```

No hay campañas de este proyecto registradas aún. Las campañas históricas de los proyectos técnicos no se adoptan automáticamente; deben enlazarse cuando se compruebe que corresponden al material que Rodrigo quiere rescatar.

### Reutilización y mejora

Mantener el padre reusable y su variante separados. Cambiar broker obliga a validar producto/costes/feed; cambiar TF obliga a revisar horizonte, frecuencia, rangos y muestra; cambiar long/short obliga a comprobar simetría económica y de bloques. Transferir una hipótesis no transfiere su resultado.

Las mejoras del procedimiento se aplican por delta durable, con fuente/fallo que lo justifique y comprobación en un caso concreto. Guardar `methodology_revision` en las campañas; conservar la evaluación original y reanalizar con una revisión nueva sin sobrescribirla.

## Fuentes

- [[Estrategias IMOX — Forex y CFD con Echo Forge]]; petición expresa de Rodrigo de planificar hasta fin de año y diferir rescate.
- [[IMOX - Building Blocks Skill]] · [[IMOX - Tipos de estrategia en trading algorítmico]] · [[IMOX - SQX automatizado - Hipótesis, sondas y ejecución]].
