---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: '[[Trading]]'
start: '2026-10-27'
progress: 0
repo: xKoRx/agents-os
aliases:
  - Echo I+D
  - I+D Echo
  - Programa de investigación Echo
  - Echo Strategy R&D
tags:
  - kind/project
  - area/trading
  - project/echo-rnd
created: '2026-10-28'
updated: '2026-10-28'
related:
  - '[[Echo Futures]]'
  - '[[Estrategias IMOX — Forex y CFD con Echo Forge]]'
  - '[[Echo I+D — Futures]]'
---

# Echo — I+D de Estrategias

## 🎯 Objetivo

Mantener una capacidad permanente de investigación y desarrollo de estrategias algorítmicas para Echo que produzca conocimiento reproducible y candidatos evaluables para pasar challenges, sobrevivir en funded y retirar dinero neto. Priorizar la economía del ciclo completo, la corrección de la estrategia y la diversidad demostrada. Una hipótesis refutada con evidencia es un resultado útil.

**Owner / stakeholder:** Rodrigo. **Gestión global:** Owner + manager de este programa. **Dos líneas permanentes:** Forex/CFD y Futures, con managers, matrices y mecanismos técnicos distintos. El programa no tiene fecha de término ni una cuota de estrategias rentables.

El resultado de negocio es extender y mejorar el trading efectivo del Owner: convertir los sistemas y automatizaciones existentes en operación y retiros sostenibles, con decisiones respaldadas por evidencia. Producir más sistemas o documentación no constituye por sí mismo ese resultado.

Unificar misión, gobierno, contratos de investigación, aprendizaje y continuidad. Cada mercado conserva sus autoridades técnicas. I+D Futures posee requisitos funcionales/prioridad económica de las capacidades Backtester que necesita y gestiona su desarrollo con el planner técnico existente; no se limita a consumir el motor disponible. Echo Futures/Runtime Pools conservan arquitectura, implementación y gates; la ampliación no reemplaza Echo Forge ni la división Forex.

## 📊 Estado actual

**2026-10-28 — delta Owner Futures posterior a RV-01:** integración S04/variantes a master en curso según Owner, sin certificación por esta nota. [[Echo I+D — Futures]] incorpora como responsabilidad funcional el desarrollo de campañas CHALLENGE, FUNDED y SIMULATION del Backtester, coordinado con producto y el planner técnico existente. Retiro variable, reinversión total del cash recibido, USD 4.000 de compras y umbral challenge 1/3 sustituyen las preguntas económicas anteriores. Mandato/prompt: [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]. A/B pendientes de retorno; no hay campañas/gasto ni código nuevos por esta actualización.

**2026-10-28 — Futures entrega RV-01 y consolida el expediente FUT-R01.** [[FUT-R01-RV-01-CONSOLIDADO]] declara `NO_APTO_AUN` por integridad de entradas e interfaces contractual/datos/selección; no exige rentabilidad demostrada antes de investigar. [[FUT-R01-INDICE]] reúne retornos disponibles y mandato. La sesión documental está cerrada con feedback; Futures continúa pendiente de decisiones y dependencias, sin campañas ni cambios de producto. La independencia histórica de la revisión no es acreditable.

| Línea permanente | Planner único de mercado | Último estado confirmado | Siguiente trabajo |
|---|---|---|---|
| Forex/CFD | [[Estrategias IMOX — Forex y CFD con Echo Forge]] | Iniciativa existente incorporada. F0→F1→F2→F3 sigue vigente; no confundir material 142 recuperado con validación 144 ni admisión Echo. | Manager Forex recupera el receipt F0 y las dependencias actuales; prepara el cierre EVAL-144 de G1/G2/G4 bajo las decisiones vigentes. |
| Futures | [[Echo I+D — Futures]] | FUT-R01 en curso; RV-01 NO_APTO_AUN, A/B pendientes. S04 en integración informada; tres campañas requeridas y economía Owner actualizadas. | Adjudicar A/B y preparar diseño C01/entrega técnica incremental mediante el planner existente. Señal PERSIST/cierre o alternativa MR06 siguen bajo revisión; no repetir los DR ni ejecutar por recepción. |

`progress: 0` no mide el porcentaje de un programa infinito. Cada entrega acotada conserva su progreso y aceptación; aquí importa el estado de las líneas, los bloqueos y las decisiones.

### Entrada rápida para cualquier chat

1. Leer esta nota y la última bitácora.
2. Seleccionar el manager en [[Echo I+D — Mapa de capacidades]].
3. Abrir únicamente el planner del mercado y sus autoridades necesarias para la decisión actual.
4. Leer estado/decisiones/recibos actuales antes de escribir. Un resumen de chat no sustituye la nota vigente.
5. Mantener explícitos `ACCEPTED_BY_OWNER`, propuesta, evidencia y pendiente; no convertir una recomendación en decisión.

La superficie de conversación es el proyecto **Trading de ChatGPT**. Los chats de manager global y managers de mercado comparten Agents-OS como verdad durable; no se depende de memoria implícita entre chats. Crear esta organización no crea chats ni un servicio autónomo en segundo plano.

## 🧱 Entrega de desarrollo

_No aplica a esta iniciativa de gestión e investigación. Toda entrega de código, configuración ejecutable, schema o infraestructura necesita su proyecto técnico, branch/base y SPECs canónicas antes de implementación. Este programa conserva las dependencias y consume su evidencia._

## 🧩 Subproyectos y fronteras

- **División Forex/CFD:** [[Estrategias IMOX — Forex y CFD con Echo Forge]]. Reutiliza su proyecto y skill; no existe otro planner Forex paralelo.
- **División Futures:** [[Echo I+D — Futures]]. Coordina estrategias, fuentes, cualificación y economía; su producto sigue siendo [[Echo Futures]].
- **Fuentes de Forex:** [[IMOX — Regularización histórica hasta septiembre 2026]], subordinada a la división Forex; conserva su alcance documental.
- **Laboratorio y optimización Futures:** [[Echo Futures — Optimización de Campañas]], subordinado a la división Futures; conserva su alcance, gates, presupuesto y estado de revisión.
- **Catálogo de props y economía histórica:** [[Echo Futures — Futures Prop Universe]] y [[Echo Futures — Prop Economics Experiment]], bajo Futures como evidencia y soporte, sin reabrir entregas cerradas.
- **Dependencias técnicas:** [[Echo Futures]], [[Echo Futures — Runtime Pools]], [[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]], [[Echo Forge — Robust Run Selection V2]], MKE y contratos app-owned. No son proyectos nuevos de alpha ni reciben un segundo dueño técnico.

La unificación es de propiedad, navegación y metodología. Las rutas históricas se conservan para no romper enlaces ni reescribir procedencia.

## Operating model

### Un responsable por hecho

| Superficie | Qué conserva |
|---|---|
| Este programa | Misión, decisiones comunes, prioridades entre mercados, capacidad, bloqueos transversales y revisión de metodología. |
| Planner de mercado | Cobertura, backlog, selección de investigaciones y estado de sus iniciativas. |
| Proyecto acotado o ficha de campaña | Hipótesis/celdas, alcance autorizado, tareas, versiones, evidencia, decisión y próximo paso. |
| Skill | Conducta reusable del agente y elección del procedimiento. |
| Runbook / repo técnico | Secuencia operativa, comandos, validación, fallos y recuperación. |
| Repositorios y almacenes de evidencia | Código, datos, planes efectivos, builds, órdenes/fills y artefactos voluminosos; el vault enlaza identidad y procedencia. |

Cada investigación declara la celda o celdas a las que aporta evidencia. El trabajo habilitante —datos, catálogo, conformidad, laboratorio— declara qué celdas desbloquea; no se disfraza como nueva estrategia. Una celda no exige un proyecto separado y un proyecto puede estudiar varias celdas con resultados separables.

### Equipo y superficies

El manager global decide con el Owner qué pregunta merece recursos y resuelve conflictos entre líneas. Cada manager de mercado organiza su búsqueda y consume la evidencia técnica aplicable. Un submanager sólo se crea para una pregunta acotada que necesite aislar contexto o coordinar especialistas.

Los agentes de fuentes, hipótesis, especificación, implementación, backtest, análisis económico y verificación se instancian según el mandato. **Muchos agentes no requieren una skill distinta por instancia.** Cada función debe tener un contrato y una autoridad clara en el mapa de capacidades.

- **Cloud:** dirección, investigación documental accesible, diseño, análisis y revisión conceptual. Usar herramientas realmente disponibles; no inventar acceso ni resultados físicos.
- **Daedalus:** procesamiento local de fuentes cuando Whisper/MKE o bibliotecas lo requieran. No es paso obligatorio de toda estrategia.
- **Hefesto:** código y pruebas físicas de Futures, Backtester, replay, órdenes/fills, reconciliación y cualificación.
- **Forex:** Forge/SQX/MT5 y su flota según el contrato técnico vigente. La compartición de Hefesto no concede capacidad adicional: antes de una ejecución se coordina disponibilidad entre owners.

No hay un recorrido obligatorio Cloud→Daedalus→Hefesto. Un paper o hipótesis propia puede ir directamente desde investigación a especificación y ejecución autorizada en Hefesto.

### WIP y recursos

**Default operativo v1, ajustable por el Owner:** una pregunta primaria en ejecución por mercado; varios workers pueden resolver partes independientes de esa pregunta. Preparar la siguiente pregunta no autoriza una segunda campaña simultánea. Si la capacidad real obliga a detener una línea, dejar bloqueo, responsable y acción de desbloqueo visibles; no fingir ejecución para cumplir el paralelismo.

El mandato Owner posterior habilita diseñar campañas multietapa y posteriormente multi-Strategy/multi-prop; desarrollo habilitante puede avanzar coordinado con la investigación. Esa capacidad no autoriza automáticamente más campañas activas ni cambia límites de recursos.

Cada mandato fija presupuesto de datos, cómputo, motores/jobs, intentos, tiempo o dinero según corresponda. Si falta un límite material, se prepara el mandato y se obtiene la decisión antes de ejecutar. Reutilizar límites existentes; no copiar el límite de motores Futures a la flota Forex.

No hay cron, polling permanente ni compra de recursos implícitos. Automatizar una tarea repetitiva requiere propuesta concreta, autorización aplicable y validación; el agente puede ejecutarla manualmente dentro del mandato mientras tanto.

## Roadmap evergreen

| Tramo | Resultado y criterio de salida | Continuación |
|---|---|---|
| Organización actual | Un programa, dos planners, managers, mapa de autoridades y ciclo de trabajo verificables. Entrega documental en revisión. | Abrir ambos chats de mercado desde sus puntos de entrada. |
| Arranque Forex | Recuperar el estado F0 vigente; cerrar decisiones de receta/comparabilidad y dependencias técnicas. | Seguir F0→F1→F2→F3 del planner Forex, sin reiniciar el rescate ni crear otra certificación. |
| FUT-R01 | Inventario NQ por identidad y celda; vigencia de recibos; perfil económico por decidir; primer mandato y alternativa con mecanismo distinto. | Decidir con el Owner perfil, pregunta y presupuesto. |
| Investigación por celda | Fuente/observación → hipótesis falsable → especificación → pruebas → evaluación → decisión. | Continuar, corregir, aparcar o rechazar con evidencia y disparador de reapertura. |
| Candidatos y adopción | Evaluación económica de challenge y funded, límites de generalización y requisitos de integración. | Entregar a los gates técnicos/de producción; ninguna promoción por mera aprobación de un backtest. |
| Aprendizaje y siguiente investigación | Actualizar cobertura, negativas, coste de aprendizaje, diversidad y delta metodológico. | Elegir la siguiente celda por valor de información y objetivo económico; repetir mientras el Owner mantenga el programa. |

El programa permanente no tiene una cuota universal ni una fecha de término. Las metas tácticas siguientes son objetivos de gestión sujetos a evidencia, capacidad y decisiones; no rebajan gates ni garantizan resultados.

### Hito táctico al 31-12-2026 — actualización Owner

El Owner quiere ambos mercados operando con props de forma relevante y sostenible. Para Futures fijó al menos cinco estrategias para challenge y cinco estrategias produciendo retiros funded, en al menos dos prop firms a la vez, con un sistema modular y escalable. El alcance, las métricas y las cuestiones abiertas viven en [[Echo I+D — Futures]]; esta meta no convierte variantes/MM en estrategias independientes ni acredita resultados actuales.

**Capital confirmado por el Owner el 2026-10-28:** USD 4.000 iniciales exclusivos de Futures y aproximadamente USD 2.000 separados para Forex. La referencia anterior a USD 5.000 queda superseded. No hay aportes adicionales previstos; no planificar transferencias entre mercados ni reposiciones implícitas. El capital disponible no autoriza gastarlo completo ni comprar cuentas: reserva, pérdida máxima y desembolsos por etapas siguen por decidir. La disponibilidad declarada del Owner es lunes a domingo, 08:00–23:30 en su horario local; no demuestra capacidad técnica de Hefesto ni disponibilidad exclusiva del cómputo.

La meta táctica Forex heredada de estudiar al menos diez activos hasta el 31-12-2026 permanece en su registro como decisión revisable. Su manager conserva la traducción de la nueva visión a su propia operativa; el manager Futures no cambia el plan Forex ni asume su producto.

## Métricas de eficacia

Registrar únicamente cuando exista evidencia:

- Preguntas resueltas y cambios de decisión producidos; distinguir hallazgo negativo, inconcluso y defecto técnico.
- Cobertura de celdas comprometidas y evidencia por estado; no un porcentaje del universo infinito.
- Coste/tiempo por decisión útil y bloqueos recurrentes; presupuesto consumido frente al autorizado.
- Reutilización de conocimiento y recibos válidos; duplicados detectados, trabajo repetido evitado y reglas ambiguas resueltas.
- Diversidad observada de mecanismos, señales, exposiciones y pérdidas; no cantidad de indicadores, configuraciones o EAs.
- En candidatos: compras, pases, supervivencia funded, retiros y cash neto, costes, drawdown, sequías, tiempo y sensibilidad al perfil. El denominador y la fase deben ser explícitos.

No optimizar el programa para producir siempre resultados positivos ni usar una tasa de aprobación aislada como sustituto de economía completa.

## ✅ Tareas

- [r] Revisar organización, managers y metodología v1 materializados bajo este mandato. #owner/me #type/research #area/trading
- [ ] Abrir manager Forex desde el planner existente y recuperar su próximo paso F0/F1. #owner/me #type/research #area/trading
- [x] Abrir manager Futures e iniciar recuperación documental y entrevista de FUT-R01; sin aceptación implícita de entregas del laboratorio. #owner/me #type/research #area/trading
- [ ] Decidir el perfil económico actual de Futures y presupuesto del primer experimento después del análisis de FUT-R01. #owner/me #type/research #area/trading
- [ ] Revisar capacidad compartida y WIP al autorizar ejecuciones concurrentes. #owner/me #type/supervision #area/trading

## 📆 Bitácora

- **2026-10-28 — Futures: tipos de campaña y economía actualizadas.** Se incorpora el frente C de Backtester a la responsabilidad funcional de I+D, con entrega técnica en planner existente. Decisiones/estado/navegación reconciliados; no código, campañas, gasto ni cierre de sesión. [[2026-10-28-echo-futures-campaign-types|Registro]].

- **2026-10-28 — precisión Owner** — Capital: Futures USD 4.000 y Forex aproximadamente USD 2.000, separados y sin nuevos aportes previstos. USD 5.000 deja de ser cifra vigente. La investigación Futures usará ficha simple de setup, filtro y RR/objetivo–riesgo técnico; MM por prop/etapa permanece como entidad separada. Objetivo de primer retiro USD 3.000 con split 90%/80%, bruto/neto por aclarar en el planner Futures. [[80-agents/journal/logs/2026-10-28-echo-futures-capital-simple-strategy|Registro de la corrección]].

- **2026-10-27 — entrevista Futures, primera ronda** — Owner prioriza trading efectivo y retiros, ambos mercados operativos hacia fin de año y, para Futures, cinco estrategias challenge más cinco funded con retiros y al menos dos props simultáneas. Capital inicial y denominadores por precisar; disponibilidad personal amplia, capacidad técnica no confirmada. Se documenta en el planner existente y se prepara un mandato acotado de investigación; no se autoriza producción ni se cierra la sesión. Registro: [[80-agents/journal/logs/2026-10-27-echo-futures-fut-r01-owner-mandate]].

- **2026-10-27** — Owner autoriza programa único de I+D Echo con dos líneas permanentes y gestión conjunta; prioridad Futures challenge+retiros, ejecución inmediata sólo NQ, cuentas E2T anteriores no vigentes ni operadas. Organización/documentación realizada sin nuevos motores ni código de producto. Baseline de discovery: agents-os `81d4d6b00205855d223914f2c6d7ac70aebc5fa1`. Continuidad lista en ambos planners; aceptación de candidatos y gates técnicos no cambia.

## 🧭 Decisiones

**Aceptadas por el Owner el 2026-10-27:**

- Un único programa de I+D Echo, con Forex/CFD y Futures como líneas paralelas permanentes.
- Owner conserva las decisiones materiales; manager global y managers de mercado gestionan con él.
- Forex usa su mecanismo SQX/Forge/EA. Futures usa Echo Backtester; SQX sería sólo una alternativa futura, no requisito ni integración ya existente.
- Priorizar estrategias Futures por capacidad de pasar challenges y retirar en funded.
- Ejecutar Futures sólo en NQ por ahora; diseñar extensibilidad sin abrir otros mercados.
- Viejas cuentas E2T no representan cuentas vigentes ni operativa real.
- Metodología rigurosa, agentes especializados, mejora continua de skills y automatización acordada.
- Organizar, materializar y cerrar con continuidad; los dos chats nuevos se abrirán por el Owner.

**Actualización aceptada en la entrevista Futures del 2026-10-27:** priorizar operación y dinero efectivamente retirado; hito táctico Futures 5 challenge + 5 funded con retiros y mínimo dos props simultáneas; preferir diversidad demostrada y buenas condiciones de automatización, idealmente sin consistencia. ClutiFX queda como conocimiento histórico, sin nuevas investigaciones salvo decisión expresa. Detalle, pendientes y siguientes mandatos en [[Echo I+D — Futures]].

**Actualización aceptada el 2026-10-28:** capital separado USD 4.000 Futures / aproximadamente USD 2.000 Forex, sin aportes adicionales previstos. La preservación de caja condiciona el plan; no equivale a garantía de resultados ni autorización de gasto. Para Futures, el Owner exige descripción algorítmica simple por indicadores y separación de la entidad Strategy respecto de MM asociado a prop/etapa.

**Decisiones operativas v1 dentro del encargo:** conservar rutas; reutilizar manager Forex; crear sólo global y Futures; usar un runbook común de gestión y los runbooks técnicos existentes. Rationale en [[echo-rnd-two-market-program]].

**Pendientes:** proveedor/programa vigente, riesgos/MM y presupuestos nuevos, primer experimento Futures, ampliación de símbolos/datos, integración SQX-Futures y cualquier promoción. La matriz inicial Futures es propuesta de cobertura, no shortlist aceptada.

## 🔗 Docs / Links

- [[Echo I+D — Mapa de capacidades]] — quién hace qué y con qué autoridad.
- [[30-resources/agents/skills/echo-rnd-manager/SKILL|echo-rnd-manager]] — gestión global.
- [[30-resources/runbooks/echo-rnd-cycle-runbook|Ciclo común de investigación y mejora]].
- [[Echo I+D — Cobertura Futures]] — propuesta de cobertura y trazabilidad.
- [[IMOX — Registro de campañas]] — contrato y matriz vigente Forex.
- [[80-agents/journal/logs/2026-10-27-echo-rnd-unification|Registro de esta reorganización]].

## 💡 Ideas

Fuentes nuevas, instrumentos futuros, SQX como generación adicional para Futures y automatización incremental entran al backlog del mercado con hipótesis y coste. Ninguna idea crea ejecución permanente por sí misma.

