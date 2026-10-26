---
type: "doc"
schema_version: 1
status: "active"
area: "[[Trading]]"
related: ["[[IMOX]]"]
aliases: []
tags: ["kind/doc", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-26"
coverage_intervals: []
inventory_complete_through: 
processing_complete_through: 
coverage_state: "partial_inventory_observed"
review_mode: "on_request"
---



# IMOX — Cobertura de revisión

## Propósito

Saber qué intervalo del foro está realmente inventariado y procesado, y qué queda por descubrir o revisar. Impedir que la fecha del post más reciente se use como prueba de que todos los anteriores fueron tratados.

## Contenido

### Actualización incremental — 2026-10-26

[[IMOX — Revisión 2026-10-26 - Actualización de octubre]]: feed recorrido desde novedades del día hasta 29/30 de septiembre; 46 posts de octubre dentro del corpus observados, 28 nuevos y 18 deduplicados. Tres revisitas. No certifica todos los espacios ni detección exhaustiva de cambios; orden/filtros y cobertura por espacio no acreditados. La tabla de abajo corresponde al lote histórico anterior y no a una frontera vigente de octubre. **124 posts únicos: 3 procesados, 13 excluidos con motivo y 108 parciales.**

Cinco PDF conservados con alcance explícito; manual MPPT sólo parcialmente leído. No se cerraron intervalos ni se cambió el modo a pedido. Ver síntesis [[IMOX - Metodología para investigación Forex y CFD]] y pendientes por fuente.

### Estado por espacio — lote histórico 2026-10-25

Lote y evidencia: [[IMOX — Reporte de regularización hasta septiembre 2026]] · [[IMOX — Revisión 2026-10-25 - Histórico hasta septiembre]].78 posts dentro del corte contextual registrados; el diccionario acumulado suma96 con los anteriores. **No hay frontera cronológica global acreditada.**

| Espacio | Posts del lote hasta septiembre | Inventario continuo | Procesamiento continuo |
|---|---:|---|---|
| `anuncios-627857` | 6 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `aportes-ia` | 12 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `aportes-y-recursos` | 12 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `axi-select` | 4 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `catalizadores-mercado` | 2 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `como-funciona-el-club` | 1 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `darwinex-zero` | 2 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `descuentos-690832` | 1 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `errores` | 4 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `laboratorio-a51b70` | 6 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `plugins-627f40` | 7 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `prop-firms` | 3 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `psicotrading` | 5 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `resultados-mensuales` | 2 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `seguridad-y-sevidores-vds` | 11 | Parcial: feed observado, paginación/filtro por espacio pendiente. | No cerrado; ver fuentes. |
| `futuros-088fb8` | Desconocido | Privado; requiere invitación. | Inaccesible. |
| `presentate-d90334` | Excluido | Fuera del alcance pedido. | No aplica. |

Los chats y CLUB no accesible no forman parte del corpus de posts enumerado. No se contabilizan como vacíos ni se asume que el feed los cubra. Fechas día/mes sin año u hora nativos conservan precisión contextual; no cierran intervalos diarios.

### Dos coberturas separadas

1. **Inventario completo de un intervalo:** se enumeraron todos los posts visibles bajo un scope y orden de creación comprobados, se recorrió toda la paginación y se registró evidencia de límites. Puede haber posts pendientes de leer.
2. **Procesamiento completo del intervalo:** cada post del inventario tiene tratamiento terminal dentro de su alcance —extracción integrada o exclusión motivada— y los adjuntos/comentarios necesarios no quedan pendientes. No equivale a haber leído completo lo que se excluyó por alcance; guardar nivel de lectura.

Una exclusión por inaccesibilidad o error no cuenta como descarte por irrelevancia y no cierra un hueco sin dejar una excepción visible. Si el inventario de la plataforma no puede probar exhaustividad, marcar el intervalo como parcial aunque todas las URLs encontradas estén procesadas.

### Checkpoint por intervalo

Registrar en la revisión que lo demuestra: comunidad/espacio, scope de contenido, `from_inclusive`, `to_exclusive`, timezone, orden/filtro usado, inicio/fin de recorrido, cantidad e identidades enumeradas, límite de acceso/paginación, pendientes/excepciones y evidencia de finalización. Usar ISO 8601 con offset; UTC para comparación cuando se conozca y America/Santiago para lectura humana. No inferir horas de lecturas pasadas.

Solo una cadena contigua de intervalos verificados permite declarar una frontera histórica. Un intervalo de septiembre completo no cierra agosto desconocido. No avanzar un contador global porque una lista ordenada por actividad ya llegó a septiembre.

**Ejemplo hipotético del usuario:** si se acredita cobertura hasta el fin de agosto, los nuevos posts comienzan a buscarse desde el 1 de septiembre, con límite exclusivo coherente. Hoy ese checkpoint **no existe** en IMOX.

### Tres colas para sincronizar a pedido

- **Histórico:** espacios/intervalos no enumerados o con huecos; se recorre por creación.
- **Nuevos:** posts creados desde la última frontera verificada, con un pequeño solapamiento configurable y deduplicación por identidad, no por título.
- **Cambios:** posts antiguos editados, respuestas/comentarios nuevos y adjuntos reemplazados. Su cursor de actividad es independiente de creación. Si Circle no ofrece changelog fiable, mantener una revisión periódica de pendientes/hilos relevantes y declarar ese límite; no prometer detección exhaustiva.

Procesar un lote es independiente de activar un monitor. Rodrigo eligió seguimiento cuando lo pida; esta nota no crea una ejecución diaria.

## Fuentes

- [[IMOX — Registro de publicaciones]] · [[Registro de conocimiento de comunidades]] · [[IMOX — Revisión 2026-10-25 - Inicialización del registro]].
