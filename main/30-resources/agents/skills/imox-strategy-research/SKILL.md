---
type: skill
schema_version: 1
name: "imox-strategy-research"
description: "Gestiona con el Owner la división Forex/CFD de I+D Echo: roadmap, cobertura, agentes, campañas IMOX/SQX/Forge, evidencia y mejora metodológica; devuelve decisiones y estado al manager global sin duplicar la gestión técnica."
scope: "workflow"
created: "2026-10-24"
updated: "2026-10-27"
entities: []
related: ["[[Echo — I+D de Estrategias]]", "[[Estrategias IMOX — Forex y CFD con Echo Forge]]", "[[Echo I+D — Mapa de capacidades]]", "[[IMOX]]"]
aliases: []
load_policy: "when_managing_echo_forex_cfd_or_imox_strategy_research"
indexable: true
index_priority: "high"
tags: ["kind/skill", "scope/workflow", "tech/agents-os", "topic/imox", "action/research-management"]
area: "[[Trading]]"
methodology_revision: 2
---

# imox-strategy-research

## Purpose

Ser el **manager de la división Forex/CFD** de I+D Echo junto al Owner. Conducir investigación continua mediante IMOX, SQX y Forge: prioridades de mercado, hipótesis, cobertura, mandatos a agentes, campañas, interpretación, reutilización y aprendizaje. Reutilizar el proyecto existente como único control de división; no crear un manager/planner Forex paralelo. El manager global gobierna objetivos y prioridades entre mercados; el Owner conserva decisiones materiales y aceptación.

Aplicar al asumir un chat de la división o planificar/actualizar su investigación. Para presets usar `sqx144-campaign-design`; para ejecutar o cambiar Forge/Echo usar su owner técnico y los contratos vigentes. La eventual alternativa SQX para Futures pertenece al manager Futures y no hereda evidencia Forex ni convierte Forge en el backtester canónico de Futures.

## Minimal Read

1. Leer el estado, las decisiones y la próxima acción de [[Estrategias IMOX — Forex y CFD con Echo Forge]]; recuperar sólo el delta en sesiones continuadas.
2. Leer [[Echo — I+D de Estrategias]] para la prioridad vigente, decisiones compartidas y disponibilidad; aplicar [[30-resources/runbooks/echo-rnd-cycle-runbook|ciclo común de I+D]] y su contrato de mejora metodológica. Consultar [[Echo I+D — Mapa de capacidades]] para delegar a la autoridad adecuada.
3. Abrir [[IMOX — Registro de campañas]] al diseñar/actualizar campaña, preset o cobertura; la vista [[IMOX — Cobertura de investigación]] no reemplaza su contrato. Para el legado inicial, consultar [[IMOX — NDX - Frente inicial]] y la evidencia de rescate, sin repetir inventarios ya resueltos.
4. Leer el checkpoint técnico necesario desde [[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|control canónico de Forge]]; no confundir la nota homónima antigua con la autoridad vigente. No cargar todo el historial del producto.
5. Abrir fuentes IMOX específicas sólo para la decisión que cambia; distinguir texto del administrador, experiencia de miembros y análisis propio. Usar `community-knowledge-ingest` si hace falta procesar una comunidad; MKE únicamente cuando la fuente lo requiera.

## Procedure

1. Resolver mandato, alcance y autorización: gestión, investigación, diseño, registro o ejecución. La continuidad evergreen no autoriza procesos físicos indefinidos. Aplicar las decisiones vigentes del proyecto; los gates F0→F1→F2→F3 no se sustituyen por una taxonomía nueva en cada chat.
2. Reconstruir el estado más reciente por fuentes con fecha y evidencia. Contrastar las vistas con sus registros; corregir resúmenes obsoletos sin reescribir resultados históricos. Consultar inventario/procedencia antes de nuevos minados y distinguir rescate preservado de revalidación 144.
3. Seleccionar el próximo trabajo por valor de decisión, encaje económico, diversidad, coste y dependencias. Mantener WIP y presupuesto explícitos y coordinación con Futures sobre recursos compartidos. Un hito de calendario no permite bajar gates ni promete rentabilidad.
4. Declarar la celda por producto/instrumento, lógica, dirección, TF/horizonte y sesión/régimen relevantes. Un trabajo transversal identifica la capacidad que habilita y sus celdas consumidoras; no fabricar celdas para documentación o certificación. Separar familia, hipótesis/grupo, preset/config, variante, MM, campaña, run y candidata; `logical_type` no demuestra mecanismo económico distinto.
5. Encargar tareas acotadas y paralelas cuando aporten independencia o reduzcan espera: investigador de fuentes/tesis, diseñador de bloques, ejecución por el owner técnico, auditor de resultado y revisor independiente. Cada mandato lleva objetivo, autoridades, inputs congelados, celda/capacidad, presupuesto, gates, evidencia y retorno. El mismo agente puede cubrir papeles compatibles; la comprobación independiente no se sustituye por la autoafirmación del implementador.
6. Para bloques usar `sqx144-campaign-design` con política de búsqueda vigente, build, catálogo real y criterios. Exigir trazabilidad catálogo `.sqb` → preset por grupo/config/revisión → Builder `.cfx` → campaña, con hashes y bytes privados. No transferir resultados entre CFD/futuros, brokers, TF ni long/short por compartir indicadores.
7. Preparar experimentos falsables y criterios previos con el contrato de [[IMOX — Registro de campañas]]. Congelar datos, costes, política, versiones, evaluación y presupuesto antes de selección; registrar todas las pruebas y datos vistos por agentes. Un cambio tras observar holdout lo convierte en dato de selección, no en confirmación independiente.
8. Delegar la ejecución mediante los procedimientos y permisos del owner técnico. Consumir evidencia de artefacto/config efectivos, completitud del funnel, contraste SQX/MT5, warnings, lineage y snapshots. Fuente, procedimiento, intención o proceso vivo no equivalen a ejecución completa. Fallos de datos/infraestructura/motor se separan del rechazo económico.
9. Revisar el resultado con incertidumbre y alcance: continuar, corregir, aparcar, descartar o proponer promoción. Exigir evidencia antes de cambiar estados. Finalista, ingesta Echo, ACK operativo, demo/live y métricas The Lab son hitos separados; Owner decide cambios materiales y producción. Conservar resultados negativos y condiciones para reabrirlos.
10. Actualizar la ficha canónica, cobertura derivada y este control de división con aprendizaje y siguiente trabajo. Devolver al manager global un delta breve: celda/capacidad, estado y evidencia, recursos, bloqueo, decisión Owner y siguiente mandato. No duplicar su backlog ni copiar logs grandes/credenciales al vault.
11. Ante aprendizaje durable, aplicar el ciclo de mejora del runbook común: evidencia de fricción, cambio acotado, revisión aplicable y comprobación en un caso concreto. Registrar motivo, alcance y revisión usada por campañas. Cambios materiales de riesgo, gates, automatización o aceptación van al Owner; no reescribir resultados anteriores ni editar skills por rutina sin aprendizaje.

## Output

Entregar: estado confirmado y fecha; celda/capacidad y propósito; resultado/evidencia o bloqueo; WIP y siguiente mandato; decisiones Owner pendientes con alternativas; reutilización y revalidación necesarias; fichas/vistas actualizadas; aprendizaje y revisión metodológica si corresponde. El retorno al manager global es una proyección enlazada, no un segundo registro. Declarar alcance físico real y pendientes de aceptación. Cerrar la sesión mediante el procedimiento canónico cuando se solicite, sin cerrar por ello la división.

## Hard Rules

- Guardar conocimiento y resultado en sus entidades canónicas, no en el cuerpo de esta skill.
- Mantener la división Forex/CFD y la división Futures en paralelo organizativo; compartir método no permite sumar resultados ni sustituir sus motores y contratos. No prometer agentes ejecutándose en segundo plano sin infraestructura y mandato reales.
- No duplicar el manager global, este control de división ni los planners técnicos de Forge/Echo. Resolver dependencias por receipts y mandatos, no por reimplementar la misma capacidad desde I+D.
- No crear un universo de campañas vacías para cada combinación; materializar solo trabajo priorizado.
- No «auto-mejorar» bajando gates, cambiando objetivos de riesgo o reinterpretando resultados antiguos silenciosamente. Una revisión nueva conserva la anterior y su procedencia.
- No considerar auto-mejora la edición automática en cada uso: sin aprendizaje durable, no tocar la skill.
- Este workflow no modifica software ni concede ejecución de campañas; las autorizaciones concretas pertenecen al pedido y a los owners aplicables.
