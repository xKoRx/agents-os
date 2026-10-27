---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
related: ["[[Echo — I+D de Estrategias]]", "[[IMOX]]"]
aliases: []
tags: ["kind/doc", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-27"
project: "[[Estrategias IMOX — Forex y CFD con Echo Forge]]"
---

# IMOX — Cobertura de investigación

## Propósito

Mostrar huecos, trabajo preparado y evidencia disponible de la división [[Estrategias IMOX — Forex y CFD con Echo Forge]] dentro de [[Echo — I+D de Estrategias]], sin equiparar tener un preset con haber cubierto una estrategia. **Esta nota es una vista resumida**: el contrato y la matriz detallada vigentes viven en [[IMOX — Registro de campañas]], sección «Matriz de cobertura v0.1 — 2026-10-26»; las campañas conservan sus evidencias. No mantener aquí un segundo registro de resultados.

## Contenido

### Ejes y estados de cobertura

La celda se identifica por producto efectivo, activo, timeframe, dirección, familia y grupo; sus variantes conservan feed, datos, build, costes, sesiones/DST y receta. `logical_type` es una clasificación observada dentro de las campañas, no sinónimo de familia o grupo. La cobertura de [[Echo I+D — Futures]] se consulta en su propio control: NDX CFD y NQ futuro no comparten validación por nombre.

Separar el avance de investigación —objetivo, diseño, preparación, prueba, validación y seguimiento— del procesamiento físico y del resultado económico. Los estados de matriz `NR`, `DESIGN`, `H142(n)`, `IMPORTED`, `READY_IMPORT`, `TOP5` y `UNDERFILLED(n/5)` se interpretan según el Registro. Un fallo operativo, una hipótesis no apoyada y una celda desconocida no son lo mismo. Un trabajo que habilita muchas celdas declara esa capacidad y sus consumidores; no llena una celda de estrategia por certificar infraestructura.

### Catálogo de lógicas

Referencia semántica: [[IMOX - Tipos de estrategia en trading algorítmico]]. Punto inicial para priorizar: breakout/ruptura de canal, expansión de rango, momentum/trend, pullback, mean reversion, false breakout/fade, giros/patrones, squeeze, sesión/ORB/gaps y calendario. No deben tratarse como familias mutuamente excluyentes ni como ventajas demostradas.

Los bloques se clasifican por papel —estado, evento, valor numérico, nivel/margen y salida—, no solo por indicador. Horizonte y dirección pueden modificar la hipótesis aun conservando bloques.

### Corte de cobertura — 2026-10-27

El rescate 142 se ejecutó el **25-10**; las entradas de esta vista del 24-10 que lo daban por diferido quedan superadas por [[IMOX — Rescate 142 en flota Forge (2026-10-25)]] y el Registro del 26-10. No se ejecutó una campaña nueva al actualizar esta vista.

| Frente | Cobertura identificada | Evidencia disponible | Estado y siguiente paso |
|---|---|---|---|
| [[IMOX — NDX - Frente inicial]] | NDX CFD heredado `USATECHIDXUSD_darwinex`, H1, LONG, BR-G1/G2/G4 | SQX 142.2399: G1 727 archivos IMPORTED; G2 555 y G4 1.091 READY_IMPORT, preservados con hashes | Revalidación 144 pendiente. F0 certificado antes de F1; confirmar perfil y bindings efectivos. Los conteos son archivos heredados, no finalistas ni estrategias independientes. |
| NDX BR-G3/G5/G6 | Diseño histórico de breakout; H1 LONG | Definición de grupos; sin pool materializado reconocido en el registro | DESIGN; F2 revisará redundancias y utilidad antes de replicarlos o minar nuevos grupos. |
| DAX, USDJPY, XAUUSD, GBPJPY y EURUSD | Activos objetivo del catálogo Owner 26-10 | Objetivo registrado; producto/feed/TF/dirección y campañas por delimitar | NR para combinaciones sin evidencia. Seleccionar transferencias después de los gates vigentes. |
| A07–A10 | Cuatro slots del objetivo táctico | Sin activo asignado | No cuentan como activos estudiados ni celdas procesadas. |

**Hito Owner preservado:** registrar y estudiar al menos diez activos al 31-12-2026. Es una meta táctica revisable frente a capacidad, no el cierre del programa ni permiso para completar una matriz cartesiana. No compromete diez activos operativos ni todas las combinaciones. H1/LONG está comprobado como identidad del legado; M15/H4 y otras direcciones conservan su estado no probado hasta aportar evidencia.

**Orden de avance:** F0 certificación con TEST → F1 cierre EVAL-144 de G1/G2/G4 → F2 revisión de familias/grupos/configs → F3 minería continua. Los detalles y el próximo mandato se gestionan sólo en el proyecto de división. El corte técnico del 27-10 mantiene F0 pendiente; consultar [[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|control canónico de Forge]].

### Cómo leer la salud del trabajo

- Cobertura objetivo: activos registrados, celdas comprometidas y motivo. Diez activos objetivo no definen el denominador de todas las combinaciones; no publicar un porcentaje ficticio de cobertura total.
- Cobertura de evidencia: celdas probadas con ejecución válida y qué policy las evaluó.
- Diversidad útil: lógicas/exposiciones/horizontes y contribución al conjunto, no cantidad de EAs.
- Flujo: campañas por estado y bloqueos; las campañas son autoridad del dato, la tabla de consulta solo proyecta.
- Coste/aprendizaje: tiempo por experimento, descartes por causa y decisión reutilizable.

No se declara ninguna estrategia admitida u operando en Echo a partir de los pools heredados. El registro distingue finalista, ingestado, operativo, demo/real y métricas The Lab listas; una etapa no demuestra las siguientes.

## Fuentes

- [[IMOX — Registro de campañas]] · [[Estrategias IMOX — Forex y CFD con Echo Forge]] · [[IMOX - Tipos de estrategia en trading algorítmico]].
