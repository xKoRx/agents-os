---
type: skill
schema_version: 1
name: echo-futures-research-manager
description: 'Gestiona la línea permanente de investigación Futures de Echo: cobertura por hipótesis, discovery multifuente,
  especificación, mandatos a Hefesto, revisión económica challenge/funded y aprendizaje. Usar para seleccionar, diseñar o
  revisar investigaciones Futures; echo-retester-master conserva desarrollo/cualificación G0–G5 y la ejecución requiere mandato
  propio.'
scope: project
created: '2026-10-27'
updated: '2026-10-27'
entities:
  - '[[Echo I+D — Futures]]'
related:
  - '[[Echo — I+D de Estrategias]]'
  - '[[30-resources/agents/skills/echo-retester-master/SKILL]]'
  - '[[Echo Futures — Optimización de Campañas]]'
aliases:
  - manager Futures I+D
  - echo-futures-strategy-rnd
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

# echo-futures-research-manager

## Purpose

Conducir [[Echo I+D — Futures]] con el Owner dentro del programa Echo I+D. Seleccionar y formular preguntas de investigación, preparar especificaciones y mandatos, revisar evidencia y actualizar la siguiente investigación.

Activar para discovery, cobertura, priorización, source-to-spec, diseño experimental y evaluación de resultados Futures. No sustituir `echo-retester-master`, el planner del laboratorio ni el owner runtime. Para Forex/CFD, derivar a `imox-strategy-research`; para prioridades entre líneas, a `echo-rnd-manager`.

## Minimal Read

1. Planner Futures: estado, decisiones, siguiente trabajo y límite de instrumentos.
2. [[Echo I+D — Cobertura Futures]] sólo para las celdas afectadas.
3. `30-resources/runbooks/echo-rnd-cycle-runbook.md` para registro, handoff y mejora.
4. `echo-retester-master` y qualification runbook antes de preparar desarrollo o pruebas.
5. Sólo catálogo/recibos del lab, fuente original, perfil económico o autoridad de producto que pueda cambiar la decisión. Para ClutiFX, resolver qué artefacto supersede al anterior; no reconstruir todo el caso por defecto.

## Procedure

1. Clasificar el trabajo como investigación, conformidad, defecto, dato, economía o dependencia técnica. Recuperar identidad/ref de la evidencia existente. No tratar una campaña terminada como una estrategia aceptada.
2. Resolver alcance Owner: instrumento, fuente, fase económica y presupuesto. No inferir un proveedor vigente a partir de un perfil histórico. En el arranque actual, NQ es el único instrumento autorizado para la futura ejecución; ampliar datos/instrumentos requiere decisión aplicable.
3. Mapear la pregunta a mecanismo/tesis, instrumento, contexto/horizonte y fase económica. Consultar estrategias y recibos existentes antes de proponer desarrollo. Distinguir familia, tesis, estrategia, variante, configuración, MM y campaña según el contrato común.
4. Formular hipótesis falsable, alternativa/control comparable, observación que la refutaría, incertidumbre y coste de resolverla. Separar señal, gestión y restricciones de cuenta. No exigir toda la historia para aprender ni usar un diagnóstico como vía para saltar gates.
5. Elegir ruta de fuente:
   - hipótesis propia: observación y transformaciones reproducibles; causalidad económica propuesta separada de hecho observado;
   - paper/documento: afirmación, alcance, datos y limitaciones contrastados;
   - curso/audio/video: usar MKE/Whisper en Daedalus cuando aporte evidencia necesaria; activar extraction/worker y pedir reparación focal;
   - señal/estrategia existente: fuente, spec, código y evidencia actual, sin heredar conclusiones de versiones anteriores.
6. Preparar especificación determinista con fuente o hipótesis por regla, obligatoriedad/opcionalidad, información disponible al decision_time, entradas, invalidación, salidas, sesión y dependencia de datos. Marcar SOURCE / OP / HIP / UNRESOLVED; no atribuir MM experimental a la fuente. Ambigüedad material bloquea implementación, no la rellena el implementador.
7. Delegar a Hefesto el desarrollo y la cualificación bajo `echo-retester-master`, con branch/base, SPECs, identidad y presupuesto. Solicitar evidencia de configuración→predicado efectivo, positivos/contraejemplos y trazas revisables de entradas/no-entradas y operaciones completas. El manager revisa resultados; la verificación física independiente ocurre donde pueda ejecutarse.
8. Aplicar la secuencia G0–G5 vigente por identidad y su alcance de datos. Una revisión de “tres meses” no reemplaza G1/G2 ni habilita concatenar contratos. Un G4 PASS sólo habilita el siguiente cómputo; no prueba robustez, retiro ni aprobación Owner.
9. Revisar economía por fase y perfil: compras/pases/pérdidas/pendientes, costes, frecuencia y sequías, geometría y admisión, supervivencia funded, retiros/cash neto y sensibilidad. Verificar qué fue medido, proyectado o no implementado. Exigir trazabilidad y no inventar funded results a partir de challenge results.
10. Distinguir defecto, ambigüedad de fuente, datos insuficientes, incompatibilidad de sesión, muestra inconclusa y resultado económico negativo. Preservar intentos y negativos. Reutilizar recibos vigentes; una nueva identidad no borra los anteriores.
11. Registrar decisión, límites y disparador de reapertura. Mantener la próxima pregunta y una alternativa que pueda aportar diversidad, sin cuota de familias ni candidatos. ClutiFX no bloquea la cola de otras fuentes.
12. Actualizar planner/cobertura y devolver al manager global sólo delta, bloqueo material, recursos y siguiente decisión. Aplicar mejora controlada con evidencia; ejecutar cierre completo sólo por solicitud.

## Output

```text
RESEARCH_QUESTION: <celda(s) / tesis / fase / objetivo económico>
CURRENT_EVIDENCE: <source/ref / spec / identidad / receipt / vigencia>
SOURCE_UNCERTAINTY: <SOURCE / OP / HIP / UNRESOLVED>
EXPERIMENT: <refutador / control / datos / selección-vs-evaluación / presupuesto>
HANDOFF: <responsable / superficie / contrato / gates / parada | ninguno>
CONFORMANCE: <regla→gate→fixture→traza / gaps>
ECONOMICS: <challenge / funded / retiros / costes / limitaciones>
DECISION: <continuar / corregir / aparcar / rechazar / candidata para revisión>
OWNER_ACCEPTANCE: <pendiente o referencia a aceptación expresa>
COVERAGE_DELTA: <evidencia nueva, no nombres/variantes>
NEXT_RESEARCH: <siguiente pregunta y alternativa / dependencia>
METHOD_DELTA: <evidencia + revisión | NO_DELTA>
CONTINUITY: <planner y refs publicados/verificados>
```

## Hard Rules

- Strategy / MM / Provider permanecen separados; ningún cambio de uno conserva silenciosamente la misma identidad/evidencia.
- No modificar G0–G5 ni heredar PASS entre variantes. Una identidad sin operación completa propia no avanza por “rareza”.
- No llamar OOS a datos que ya influyeron en selección, incluidas decisiones de agentes y ajustes manuales.
- No deducir equivalencia o independencia por nombre; demostrar señales y exposición.
- No convertir OHLCV 1m en prueba de microestructura, cola o fill intrabar de una tesis que exige otros datos.
- No instalar otra plataforma de backtest, scheduler, DSL o base de datos para resolver organización.
- SQX-Futures es una opción de investigación futura, no compatibilidad, integración o autorización existente.
- No congelar requisitos materiales sin Owner ni promover a producción desde esta skill.
