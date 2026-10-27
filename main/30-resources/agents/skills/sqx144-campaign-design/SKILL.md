---
type: skill
schema_version: 1
name: "sqx144-campaign-design"
description: "Diseña hipótesis, presets de bloques y sondas para campañas en SQX 144 basadas en IMOX; úsala al preparar minados y configuraciones Builder, con catálogo real para generar archivos importables."
scope: "tool"
created: "2026-10-24"
updated: "2026-10-27"
entities: []
related: ["[[Echo — I+D de Estrategias]]", "[[Estrategias IMOX — Forex y CFD con Echo Forge]]", "[[IMOX]]", "[[IMOX - Empezar con SQX 144 - Metodología y primera campaña]]"]
aliases: []
load_policy: "when_preparing_sqx144_campaign"
indexable: true
index_priority: "high"
tags: ["kind/skill", "scope/tool", "tech/agents-os", "tech/sqx", "action/campaign-design"]
area: "[[Trading]]"
---

# sqx144-campaign-design

## Purpose

Preparar hipótesis y configuraciones de Builder para campañas SQX 144 según evidencia de IMOX, y definir una primera sonda verificable. Aplicar al diseñar minados, elegir familias o transformar una idea en preset. Para explicar una fórmula aislada, responder desde su fuente sin activar el workflow completo. Para operar Forge o ejecutar una campaña, hacer handoff al procedimiento técnico vigente de esa aplicación.

## Minimal Read

1. Resolver el mandato del manager de mercado y su política vigente. Para Forex/CFD, leer las decisiones de [[Estrategias IMOX — Forex y CFD con Echo Forge]] y el contrato de presets de [[IMOX — Registro de campañas]]; después [[IMOX - Empezar con SQX 144 - Metodología y primera campaña]] para la referencia de fuentes.
2. Para elegir lógica, consultar solo las familias pertinentes de [[IMOX - Tipos de estrategia en trading algorítmico]].
3. Para materializar presets, leer [[IMOX - Building Blocks Skill]] y el catálogo/export real entregado. Consultar la guía 145 solo para bloques seleccionados, sin asumir compatibilidad con 144.

## Inputs

Obtener los que cambien la decisión: build SQX, motor destino, instrumento/broker/servidor, dirección, timeframe, hipótesis, rangos y sesiones, periodos de diseño/selección/evaluación, presupuesto y criterios. Para archivos importables, requerir `.sqb` de la instalación objetivo; para configuración completa o restricciones no expresables en `.sqb`, requerir `.cfx`/plantilla compatible. No bloquear investigación que no depende de esos archivos.

## Procedure

1. Clasificar la petición: puesta al día, diseño de hipótesis, preparación de preset o ejecución. Reutilizar el contexto ya verificado y recuperar solo el delta.
2. Separar la recomendación escrita de IMOX de experiencias de miembros y de decisiones Owner. La división Forex/CFD tiene como política vigente del 26-10 **genética IMOX**, con F0→F1→F2 antes de Builders nuevos y múltiples configs calibradas por grupo. Random es una alternativa explícita descrita por fuentes; no es el default de este proyecto ni sustituye silenciosamente la política acordada. No fijar números universales del foro. Una futura propuesta SQX para Futures requiere mandato, compatibilidad y validación propios de esa división.
3. Definir la tesis falsable y sus roles: lógica, dirección, régimen, orden, disparador, filtro, horizonte y salidas. Distinguir diversificación de firma de indicadores y diversificación de exposición/riesgo.
4. Verificar que la base de datos/instrumento tiene evidencia suficiente. Si falta comprobar point value, costes, sesiones o compatibilidad, emitir el control pendiente; no inventar una especificación del broker.
5. Con export real, seleccionar únicamente IDs y rangos permitidos, preservando estructura. Revisar shifts, comodines, opuestos para cortos y tipo de orden. Si un signo o restricción no se puede fijar en `.sqb`, pedir la plantilla necesaria y declarar qué queda sin garantizar. Sin export, entregar diseño y faltantes, no un archivo supuestamente importable.
6. Formular sonda con límite de recursos, criterios previos y artefactos a conservar. Proponer importación, revisión, ejemplo exportable/compilable y medición antes de aumentar presupuesto. No ejecutar esos pasos por el solo hecho de producir el plan.
7. Separar el dato usado para adaptar hipótesis del utilizado para evaluar el proceso. Si se pide un cambio tras mirar un holdout, reclasificar ese periodo como selección y advertir la pérdida de independencia.
8. Registrar la propuesta y resultados reales en su recurso/proyecto mediante los contratos del vault. Conservar catálogo maestro `.sqb` y preset `family/group/config/revision`, sus hashes/referencias privadas, relación con Builder `.cfx` y campaña, y límites no expresables en el preset. La revisión empleada en una campaña es inmutable; cualquier cambio motivado crea otra revisión.
9. Si falla importación o coherencia, preservar el fallo y devolverlo al manager de mercado; no esconderlo cambiando filtros hasta que aparezca una candidata. La mejora de la skill sigue [[30-resources/runbooks/echo-rnd-cycle-runbook|el ciclo común de I+D]]: evidencia, delta acotado, revisión y comprobación en un caso. Escalar al Owner cambios materiales de política/gates/automatización; no editar por obligación en cada uso.

## Output

Entregar: hipótesis y justificación con fuentes; configuración elegida y alternativas; artefactos disponibles/faltantes; restricciones que el preset sí/no representa; plan de sonda y criterio de descarte; estado separado de diseño, importación, exportación/compilación, ejecución y evaluación. Si no hubo pruebas, indicarlo expresamente. En preparación para Forge, dejar un contrato de campaña para verificar en el owner técnico, sin afirmar integración implementada.

## Hard Rules

- La lista real de bloques/versión manda sobre nombres sugeridos por el modelo o un PDF de otra versión.
- No convertir cifras de miembros, muestras de backtest ni recomendaciones de Aritz en rentabilidad demostrada o defaults universales.
- No entregar indicadores Java nuevos como si fueran presets `.sqb`; distinguir selección de bloques existentes, plantilla de estrategia y desarrollo de plugin.
- No relajar criterios ni reutilizar evaluación oculta sin registrar que cambió el experimento.
- No afirmar importación o ejecución a partir de XML válido o de un proceso vivo. Exigir evidencia en SQX/MT del artefacto correcto.
- Esta skill no autoriza campañas, cambios de producción, instalación de parches ni operaciones de cuenta.

## Sources

- [Origen metodológico en Circle](https://comunidad.imoxtrading.com/c/aportes-ia/ia-building-blocks).
- Las notas de Minimal Read conservan provenance por publicación; no duplicar sus manuales en esta skill.
