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
updated: "2026-10-25"
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
- **WIP propuesto:** una campaña experimental activa; cola corta de diseños listos para la siguiente ejecución. En Echo Futures, registrar capacidad y dependencias aparte, sin mezclar sus resultados con CFDs.

## Roadmap hasta el 31 de diciembre de 2026

Fechas objetivo propuestas, no certificaciones ni compromisos de cantidad. La capacidad semanal de Rodrigo y disponibilidad efectiva de Forge no están medidas; revisar semanalmente el alcance y no los gates para cumplir calendario.

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
