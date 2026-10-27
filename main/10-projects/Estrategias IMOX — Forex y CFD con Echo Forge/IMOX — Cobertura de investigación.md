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

# IMOX — Cobertura de investigación

## Propósito

Mostrar huecos, trabajo preparado y evidencia disponible para [[Estrategias IMOX — Forex y CFD con Echo Forge]], sin equiparar tener un preset con haber cubierto una estrategia.

## Contenido

### Ejes y estados de cobertura

Universo de activos y temporalidades: todavía por delimitar. Primer activo: NDX en el carril Forex/CFD; producto exacto pendiente. La cobertura de [[Echo Futures]] se consulta en su propio control y no se suma a esta matriz como si fueran resultados comparables.

Para cada celda distinguir: `unscoped` (sin compromiso), `targeted` (objetivo elegido), `designed` (hipótesis), `prepared` (receta compatible), `tested` (ejecución válida), `validated` (gates acordados), `observing` (seguimiento) y `retired`. Un fallo y una celda desconocida no son lo mismo.

### Catálogo de lógicas

Referencia semántica: [[IMOX - Tipos de estrategia en trading algorítmico]]. Punto inicial para priorizar: breakout/ruptura de canal, expansión de rango, momentum/trend, pullback, mean reversion, false breakout/fade, giros/patrones, squeeze, sesión/ORB/gaps y calendario. No deben tratarse como familias mutuamente excluyentes ni como ventajas demostradas.

Los bloques se clasifican por papel —estado, evento, valor numérico, nivel/margen y salida—, no solo por indicador. Horizonte y dirección pueden modificar la hipótesis aun conservando bloques.

### Frente inicial

| Frente | Producto | Lógicas | Dirección/TF | Estado real | Próxima decisión |
|---|---|---|---|---|---|
| [[IMOX — NDX - Frente inicial]] | NDX broker/feed por confirmar | Grupos 142 sin clasificar; nuevas familias por priorizar | Desconocidos para el legado; nuevos por elegir | `targeted`; legado `inventory_pending`, rescate diferido | Diseñar metodología primero; luego seleccionar primera celda y auditar inventario. |
| Otros índices/CFD | Sin universo aprobado | Según huecos observados | Por delimitar | `unscoped` | Elegir una transferencia tras baseline NDX. |
| Pares Forex | Sin universo aprobado | Según propiedades/datos del par | Por delimitar | `unscoped` | Priorizar un instrumento con criterio, no minar todos simultáneamente. |

H1/H4 pueden ser candidatos de discusión, pero no se registran como selección aprobada ni se atribuyen al material 142 de Rodrigo. El mapa se amplía por celdas priorizadas; no se crean miles de combinaciones vacías.

### Cómo leer la salud del trabajo

- Cobertura objetivo: celdas comprometidas y motivo. Denominador todavía no definido; no publicar un porcentaje ficticio de cobertura total.
- Cobertura de evidencia: celdas probadas con ejecución válida y qué policy las evaluó.
- Diversidad útil: lógicas/exposiciones/horizontes y contribución al conjunto, no cantidad de EAs.
- Flujo: campañas por estado y bloqueos; las campañas son autoridad del dato, la tabla de consulta solo proyecta.
- Coste/aprendizaje: tiempo por experimento, descartes por causa y decisión reutilizable.

No hay métricas de producción calculables todavía. El legado desconocido no se contabiliza como cero estrategias.

## Fuentes

- [[IMOX — Registro de campañas]] · [[Estrategias IMOX — Forex y CFD con Echo Forge]] · [[IMOX - Tipos de estrategia en trading algorítmico]].
