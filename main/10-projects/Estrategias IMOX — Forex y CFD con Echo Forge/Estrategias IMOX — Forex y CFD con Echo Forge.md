---
type: project
schema_version: 1
owner: "me"
root: true
status: "active"
priority: "P1"
area: "[[Trading]]"
sprint:
start: "2026-10-24"
due: "2026-12-31"
progress: 0
repo:
jira:
prs:
aliases: ["Investigación de estrategias IMOX", "Roadmap Forex Forge Q4 2026"]
tags: ["kind/project", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-26"
related: ["[[IMOX]]", "[[Echo Futures]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# Estrategias IMOX — Forex y CFD con Echo Forge

## 🎯 Objetivo

Construir una práctica reproducible de investigación y desarrollo de estrategias con metodología IMOX, SQX y Echo Forge, empezando por NDX y extendiendo cobertura de lógicas, direcciones, temporalidades y mercados según evidencia. Hasta el 31 de diciembre de 2026, demostrar el ciclo completo en una escala manejable: hipótesis → preset compatible → sonda → validación → decisión → seguimiento y reutilización.

El resultado puede ser promover, mantener en evaluación o descartar una hipótesis con evidencia. No hay cuota de EAs rentables ni objetivo de rentabilidad inventado. La amplitud de cobertura es una dirección de largo plazo; no compromete todas las combinaciones para diciembre.

## 📊 Estado actual

**Fase: diseño de metodología y roadmap, sin ejecución nueva.** Rodrigo avanzará en Echo Futures y en Forex/CFD; aquí gobierna la investigación Forex/CFD con Forge. NDX es el primer frente, un índice y producto a resolver, no un par de divisas.

Existe material NDX creado en SQX 142: estrategias, selección y un par de grupos según Rodrigo. Está en las instalaciones 142 de los workers. El rescate se ejecutó el 2026-10-25 ([[IMOX — Rescate 142 en flota Forge (2026-10-25)]]): tres pools 142 inventariados y clasificados — Zeus 727 G1 (Cohort 001, ya en Forge), Hera 555 G2 y Kronos 1091 NDX_W3/G4 (estos dos nunca ingestado, listos para Watcher Import) — preservados con SHA256 verificado en MinIO `sqx-strategies/recovery-imox-142/20261025/`. Derivados intermedios (passed/fail/test ≈ 1.259 archivos) quedan en origen, declarados como no preservados.

SQX actual declarado por Rodrigo: 144. No se usa una guía 145 como contrato de compatibilidad de su instalación. La metodología de referencia y sus límites viven en [[IMOX - Empezar con SQX 144 - Metodología y primera campaña]].

## 🧱 Entrega de desarrollo

_No aplica — proyecto de negocio/investigación, no delivery de software. Los cambios necesarios de código, configuración ejecutable, esquema o infraestructura se derivan al proyecto técnico dueño de Forge/Echo. Una ficha de hipótesis o diseño no implica haber aplicado configuraciones ni ejecutado campañas._

## Modelo operativo

- **Una ficha por campaña:** autoridad de su hipótesis, receta, estado y evidencia. [[IMOX — Registro de campañas]] define el contrato. Repetir una ejecución no crea una metodología nueva.
- **Cobertura por evidencia:** [[IMOX — Cobertura de investigación]] distingue objetivo, preparado, probado, validado y seguimiento. Cantidad de bloques o EAs no equivale a diversidad.
- **Un primer frente:** [[IMOX — NDX - Frente inicial]]. Primero clasificar/revalidar material heredado cuando corresponda, sin considerarlo equivalente a una construcción nueva 144.
- **Trabajo reutilizable:** tesis, familia de preset y receta de evaluación versionadas; variantes por broker/símbolo/TF conservan vínculo y motivo del cambio. No asumir portabilidad por compartir nombre de indicador.
- **WIP y orden del owner (26-10):** certificar primero la cadena completa usando datos de prueba; cerrar después los tres grupos históricos G1/G2/G4; rediseñar familias, grupos y múltiples configs calibradas antes de lanzar Builders nuevos. No usar los pools reales para certificar el pipeline. Conservar proyectos Echo Futures separados.


## Tramo prioritario — Cierre común de BR-G1/G2/G4 y rediseño posterior (2026-10-26)

**Decisión del owner:** se paraliza la idea de replicar G1/G2/G4 sin revisión a nuevos activos. Primero certificar la cadena íntegra de Forge con datos de TEST y entorno descartable, después cerrar los tres pools de NDX H1 LONG, y sólo entonces volver a diseñar familias, grupos y varias configuraciones genéticas calibradas por grupo. El detalle de las tasks, la semántica de sus resultados y la matriz están en [[IMOX — Registro de campañas]]. Este control no inicia builds, test runs, deploy ni promociones.

### Gates secuenciales

| Gate | Resultado exigible | Estado |
|---|---|---|
| F0 — Certificación previa | Pipeline completo con estrategias/datos de prueba, oráculos independientes y E2E físico en SQX 144, MT5, Echo TEST y The Lab de pruebas; ranking por logical type, selección WFM/Apply, lineage, warnings y reintentos demostrados. Los pools históricos no se usan como fixtures. | PENDIENTE. Dynamic Groups Shot 4 con findings y E2E físicos abiertos; frontera Echo todavía pendiente |
| F1 — Cierre G1/G2/G4 | Tres cohortes antiguas NDX H1 LONG procesadas por **tasks completamente nuevas** de SQX 144, usando una receta versionada común; resultado por logical type, Top 5 o UNDERFILLED justificado, warnings, reporte y estado final de Echo/The Lab. | PENDIENTE. Rescate 142 preservado |
| F2 — Revisión de taxonomía | GLM-5.3-Flash Max desafía G1–G6, redundancias y evidencias; el owner aprueba qué familias/grupos existen y por qué se incluyen o descartan, sin obligación de mantener seis. Cada familia puede tener muchos grupos y cada grupo múltiples configs genéticas distintas y calibradas. | PENDIENTE |
| F3 — Minería continua | Campañas nuevas según matriz de cobertura y capacidad real de Zeus, Hera, Kronos y Hefesto; reporte por campaña y mejoras sustentadas en evidencia. | PENDIENTE |

### Único plan de cierre para los tres grupos heredados

| Grupo inmutable | Material preservado 142 | Estado previo | Próximo paso después de F0 PASS |
|---|---:|---|---|
| BR-G1 · compresión y expansión | 727 | Ya ingestado en Forge | Procesar mediante nuevas tasks 144 y registrar todo el funnel |
| BR-G2 · ruptura horizontal | 555 | READY_FOR_IMPORT | Importar, procesar con las mismas tasks 144 y reportar |
| BR-G4 · ruptura con tendencia | 1.091 | READY_FOR_IMPORT | Importar, procesar con las mismas tasks 144 y reportar |

**Pipeline propuesto y compartido:** Retester Light → ranking preliminar → clasificación por logical type → lotes de diez con objetivo Top 5 por tipo → Retester Full → WFM/Optimizer → selección del run IS/Apply con nueva versión de estrategia → Retester Full Precision tick y MT5 sobre el mismo período/artefacto y parámetros efectivos → reconciliación y ranking final de SQX + MT5 → acumulación Top 5 o UNDERFILLED con EOF probado → warnings y reporte → revisión manual de pertenencia a familia asistida por IA → ingesta idempotente en Echo → ACK operativo y métricas de The Lab. Los warnings nacen en cada task; los bloqueantes impiden selección/promoción. El Top 5 no autoriza relajar criterios.

**Configuraciones:** una receta de evaluación SQX 144 por revisión (fuente y efectiva por task, hashes y entradas/outputs), compartida entre los tres grupos; diferencias por instrumento, estrategia y WFM son bindings explícitos e inmutables por ejecución. Los Builders genéticos **futuros** tendrán configs propias por grupo, nunca se reutilizan sus CFX 142 como contrato de procesamiento 144. El descriptor de orquestación WorkflowSpec establece orden y bindings; no reemplaza los CFX/INI ni los criterios de cada task.

**Reporte GLM-5.3-Flash Max:** antes de la campaña producir un brief de intención, hipótesis falsable, familia/grupo/config, exclusiones, régimen y criterios previos; después un reporte de evaluación con cantidades y métricas por etapa y logical type, períodos, fallos, advertencias, contraste de motores, finalistas, diversidad y resolución. Cada dato numérico debe apuntar a evidencia de Forge/Echo/The Lab. La clasificación económica de finalistas es una revisión manual asistida por IA y no cambia silenciosamente un ClassificationSnapshot vigente.

**Hefesto:** físicamente incorporado a Forge y SQX 144 con guard intermitente de recursos; se reserva a Retester/Optimizer de hasta 10 estrategias por tarea, nunca Builders. No subir concurrencia global por contar su poller ni inferir perfil/dataset actualizado de un activo sin preflight. Zeus/Hera/Kronos son los Builders principales de las campañas futuras.

**Decisiones abiertas antes de F0:** ranking/eligibilidad final con métricas SQX+MT5 y tolerancias de concordancia; criterio exacto de selección del run de WFM (el código candidato usa último IS no-future, aún sin aprobación expresa del owner para este plan); límites de tiempo/candidatas y concurrencia; períodos IS/OOS y holdout independiente; autorización y gates para admisión/habilitación en Echo. Una repetición de backtest en el IS seleccionado no constituye prueba OOS.

### Checklist inmediato

- [ ] Cerrar F0 E2E con tests descartables y evidencia, sin estrategias históricas reales.
- [ ] Preparar una sola receta de tasks SQX 144 con configuraciones nuevas por task, incluidas rankeos, clasificación, WFM, tick, MT5, warnings y Echo, más sus bindings y hashes.
- [ ] Congelar las decisiones abiertas que cambian selección y comparabilidad antes de ejecutar.
- [ ] Procesar cada pool preservado G1/G2/G4 cuando F0 esté aprobado, con un informe propio y refs de resultado.
- [ ] Evaluar qué familias, grupos y configs genéticas calibradas sí se investigarán a futuro y cuáles se excluyen, dejando justificación.

## Roadmap hasta el 31 de diciembre de 2026

**Roadmap histórico del 24 de octubre: hoy subordinado a los gates F0→F1→F2→F3 anteriores.** Las fechas son orientativas; no autorizan saltos ni fabricar Top 5. La capacidad semanal y throughput de Forge se deben medir.

| Ventana | Outcome de negocio | Evidencia de salida | Si no se alcanza |
|---|---|---|---|
| 24 oct–1 nov | Metodología, registro y primer alcance NDX definidos. | Contrato de campaña, mapa de cobertura y primera hipótesis delimitada; separación de dato de diseño/selección/evaluación. | Cerrar decisiones pendientes; no preparar una cola masiva. |
| 2–15 nov | Baseline NDX y una sonda compatibles con 144. | Cuando Rodrigo active el rescate: inventario 142 preservado, grupos clasificados, catálogo real 144, receta importable y una sonda con resultado. | Resolver dato/config o dependencia técnica; reducir número de hipótesis. |
| 16–29 nov | Una campaña NDX evaluada de extremo a extremo hasta la frontera demostrada de Forge. | Identidad de artefactos, resultado de robustez/contraste MT5, motivos de selección/rechazo y decisión humana. Un resultado sin candidatos es válido. | Mantener el experimento diagnosticable; no inventar éxito ni ampliar activos. |
| 30 nov–13 dic | Segunda iteración que aporte diversidad o aprendizaje transferible. | Cambiar un eje —lógica, dirección, TF o instrumento— con delta explícito y misma evaluación; comparación con baseline. | Completar NDX o la causa de fallo antes de transferir. |
| 14–27 dic | Consolidar el ciclo de vida y la frontera con Echo. | Informe de cartera de candidatos, limitaciones, plan de observación; admisión/demo solo si hay candidatos elegibles e integración demostrada. | Cerrar el trimestre en pre-Echo con frontera explícita; no bloquear conocimiento por falta de integración. |
| 28–31 dic | Cierre anual y cartera de trabajo Q1 2027. | Cobertura real, coste por aprendizaje/candidata, decisiones, pendientes y backlog priorizado. | Documentar lo aprendido y lo no demostrado, sin completar casillas por calendario. |

El mínimo útil al cierre anual es **un ciclo reproducible NDX y registro íntegro**, no una cartera grande. Si las dependencias consumen el trimestre, el cierre reportará exactamente el tramo demostrado y el siguiente bloqueo.

## Relación con Echo, Forge y Futures

- Este proyecto decide **qué investigar, por qué y cómo interpretar resultados**. La aplicación [[30-resources/applications/echo/echo-forge|Forge]] posee ejecución, configuración efectiva e identidad técnica; los logs del vault enlazan sus refs, no los reemplazan.
- [[Echo Forge — Operación Real V2]] y [[Echo Forge — Robust Run Selection V2]] son dependencias/contexto técnico, no padres de esta investigación. El último control consultado de Robust Run (15 oct) declara resultado **pre-Echo**; no demuestra entrega al runtime Echo ni preparación actual para Random nuevo.
- [[Echo Futures]] es otro carril. Se reutiliza lenguaje de hipótesis, registro y evaluación, no contratos de producto, costes ni evidencia de resultados. Su capacidad compite por el tiempo de Rodrigo y debe ajustarse al revisar el roadmap.
- El resultado puede quedarse en candidato offline validado sin ser admitido ni ejecutado en Echo. `Finalista Forge`, `admitida Echo`, `en demo` y `real` son hitos distintos.

## ✅ Tareas

- [x] Crear proyecto, roadmap provisional, contrato de registro y frente inicial NDX. #owner/me #type/research #area/trading
- [ ] Revisar y priorizar el alcance Q4 frente al trabajo de Echo Futures. #owner/me #type/research #area/trading
- [ ] Elegir primera celda NDX: producto/broker, lógica, dirección y timeframe. #owner/me #type/research #area/trading
- [ ] Fijar política de evaluación y presupuesto de la sonda, antes de mirar nuevas candidatas. #owner/me #type/research #area/trading
- [x] Cuando corresponda, inventariar el material NDX 142 de los workers sin alterar originales. #owner/me #type/research #area/trading — DONE 2026-10-25: 3 pools clasificados (G1/G2/G4) y preservados en MinIO; [[IMOX — Rescate 142 en flota Forge (2026-10-25)]].
- [ ] Verificar catálogo/configuración de SQX 144 y compatibilidad de la primera receta. #owner/me #type/research #area/trading
- [ ] Comprobar la frontera operativa de Forge necesaria para ejecutar la sonda. #owner/me #type/research #area/trading
- [ ] Ejecutar y registrar una primera campaña solo cuando su paquete sea preparado y se dé la instrucción de ejecución. #owner/me #type/research #area/trading
- [ ] Revisar resultados y actualizar cobertura/aprendizajes; elegir siguiente celda sin cambiar varias dimensiones a ciegas. #owner/me #type/research #area/trading

## 📆 Bitácora

- **2026-10-26** — Owner fija certificar primero el E2E con tests, cerrar BR-G1/G2/G4 históricos con todas las tasks nuevas 144, reportar con GLM-5.3-Flash Max y rediseñar familias/grupos/configs antes de reanudar minería genética. Plan documentado sin ejecutarlo.

- **2026-10-25** — Rescate 142 ejecutado sobre la flota (solo lectura + copia conservadora): pools Zeus 727 G1 / Hera 555 G2 / Kronos 1091 G4 identificados, clasificados por bloques de los builders reales, preservados en MinIO `sqx-strategies/recovery-imox-142/20261025/` con SHA256/ETag verificado 15/15 (~1,71 GB) y staging de import para Forge preparado sin despachar. Pools B y C nunca habían pasado por Forge. Detalle: [[IMOX — Rescate 142 en flota Forge (2026-10-25)]]. No se lanzaron builders/retesters/optimizers ni waves; Echo PROD sin promociones Forge (0 promotions, 0 strategy versions, RO 2026-10-25).
- **2026-10-24** — Proyecto creado por solicitud de Rodrigo. Se define planificación Q4; rescate 142 diferido. Sin conexión a workers, ejecución de campaña o cambios de Forge/Echo.

## 🧭 Decisiones

- Owner humano y área Trading; la asistencia del agente se realiza sobre el mismo control sin un subproyecto de desarrollo ficticio.
- NDX primero; universo total y timeframes se incorporan gradualmente. No se despliega el producto cartesiano de todos los ejes en cientos de notas vacías.
- La skill gobierna el procedimiento; las fichas gobiernan el estado y los resultados. Una mejora metodológica conserva versión y evidencia y no cambia retrospectivamente campañas cerradas.

## 🔗 Docs / Links

- [[IMOX — Cobertura de investigación]] · [[IMOX — Registro de campañas]] · [[IMOX — NDX - Frente inicial]].
- [[30-resources/agents/skills/imox-strategy-research/SKILL.md|Skill de investigación y registro IMOX]].
- [[IMOX - Tipos de estrategia en trading algorítmico]] · [[IMOX - IA y Building Blocks - Cambio de enfoque de Aritz]].
- [[IMOX - Building blocks y preparación de campañas Forge]].
