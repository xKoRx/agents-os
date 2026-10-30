---
type: "doc"
schema_version: 1
status: "active"
area: "[[Trading]]"
related: ["[[IMOX]]"]
aliases: []
tags: ["kind/doc", "area/trading", "topic/imox"]
created: "2026-10-30"
updated: "2026-10-30"
review_started_at: "2026-10-30T15:58:07-03:00"
review_finished_at: "2026-10-30T16:05:31-03:00"
inventory_complete: false
processing_complete: false
---

# IMOX — Revisión 2026-10-30 - Actualización incremental

## Propósito

Actualizar IMOX al estado disponible durante el 2026-10-30, con seguimiento reusable en sesiones nuevas y fuentes web readonly.

## Contenido

Inicio del lote registrado: 15:58:07 -03; consolidación: 2026-10-30T16:04:51-03:00, America/Santiago. Superficie: Codex; host comprobado `sqx-ulab-hefesto-0` (Hefesto); Chrome del owner perfil KoR. No se guardan IDs de browser/tab, cookies o credenciales.

### Recorrido

Feed desde cabecera (post de 19 horas) hasta solapamiento con posts del 23–26 de octubre; se observaron tres publicaciones recientes sin registro previo: IPMI, índice general y sqcli. Cabeceras de Anuncios, SQX, IA, Seguridad y Laboratorio contrastadas; fijados se distinguen de orden cronológico. Cuatro posts de reglas/índice en sus URLs originales reabiertos como cambios, no posts nuevos. El índice de SQX permitió descubrir un post del 21 de septiembre omitido antes. No se acredita paginación/filtro completo por espacio ni universo histórico/exhaustividad del feed.

### Identidades nuevas

- [[IMOX - Fuente - Tailscale sin login - Recuperación por IPMI]] — `processed`, útil; fecha mostrada `19 horas`.
- [[IMOX - Fuente - Índice general de Zona de Aportes]] — `processed`, útil; fecha mostrada `1 día; cuerpo: Actualizado 29 de octubre de 2026`.
- [[IMOX - Fuente - Automatizar SQX con sqcli - Experimento 143]] — `partial`, útil; fecha mostrada `2 días`.
- [[IMOX - Fuente - Panel de EAs - Comparación del custom con MT5]] — `partial`, útil; fecha mostrada `21 sept`.

### Revisitas

- [[IMOX - Fuente - Acceso VDS por WireGuard]] — El post ahora muestra cinco comentarios. Se aconseja tener varios dispositivos autorizados para no depender de uno; otro miembro menciona firewall del proveedor para gestionar acceso desde fuera. No se verifica esa configuración ni se amplía acceso. Lectura de comentarios no sustituye una prueba de recuperación.
- [[IMOX - Fuente - Manual de psicología para traders]] — Se revisaron seis comentarios accesibles: las incorporaciones son agradecimientos y experiencias, sin criterio técnico nuevo. Se conserva lectura dirigida del PDF, no se eleva a completa.
- [[IMOX - Fuente - Cartera estable - Ventaja frente a azar y selección]] — Comentarios posteriores proponen un control sintético con ventaja conocida para medir también falsos negativos, no sólo paseos sin ventaja. Xavi dice que lo probará; Ayose cuestiona cómo construir/calibrar un control independiente. Es propuesta y desacuerdo de miembros, no test implementado ni validado. Evitar ajustar el propio test hasta obtener el resultado esperado.
- [[IMOX - Fuente - Mi base de datos para analizar resultados]] — El feed muestra 15 comentarios, frente a 14 observados antes. Se leyeron 13 artículos accesibles; la incorporación más reciente es agradecimiento, sin capacidad técnica nueva. Las respuestas anidadas siguen sin agotarse y no se reconfirman afirmaciones sobre asignaciones Darwinex.
- [[IMOX - Fuente - Seminario 30 de octubre - Repaso 136 a 144]] — El anuncio muestra 19 comentarios y el evento figura finalizado el 30 de octubre. El evento tiene cuatro comentarios accesibles; IMOX confirma que queda grabado, pero no se observó locator de grabación. Sustituye el estado temporal de evento futuro; no acredita revisión de su contenido.
- [[IMOX - Fuente - Reglas del espacio Strategy Quant]] — El post fijado conserva identidad y ahora se titula Índice y qué publicar. Organiza rutas para empezar con 144, construir/filtrar, automatizar, exportar y resolver fallos; enlaza el experimento sqcli y un panel SQX→MT5 antes no registrado. Es curaduría de navegación, no receta oficial de umbrales.
- [[IMOX - Fuente - Reglas del espacio IA]] — El mismo locator ahora presenta Índice y qué publicar: rutas de iniciación IA, construcción en SQX y análisis/automatización; destaca el audio de Aritz y builders acotados. El índice no acredita haber escuchado el audio ni auditado cada destino. Se conserva como norma comunitaria la restricción escrita sobre compartir material en IA externas, sin convertir el contenido del foro en instrucciones del agente.
- [[IMOX - Fuente - Reglas de Seguridad y Servidores]] — El post fijado ahora organiza infraestructura, virtualización y seguridad/backups con enlaces; mantiene dudas diarias en chat. La fecha original mostrada sigue 16 sept; no se inventa timestamp de edición.
- [[IMOX - Fuente - Reglas de Otro Laboratorio]] — El post fijado ahora organiza investigación de estrategias, riesgo/MM y reflexión, con comentarios destacados. Conserva fecha mostrada 16 sept y reglas de publicar investigaciones fuera de las otras categorías. Ranking y resúmenes no prueban las afirmaciones de los destinos.

### Materiales y límites

[[IMOX - Fuente - Evento Repaso 136 a 144 del 30 de octubre]] separa el evento del contador de posts. Finalizado al consultar, grabación prometida sin locator observado. [[IMOX - Fuente adjunta - Documento Automatizar SQX con sqcli]] registra el locator de Academia que exige login; cero lectura del documento y cero archivo descargado acreditado en este lote. [[IMOX — Descargas pendientes]] conserva la URL para descarga manual y carga posterior. Las cuatro imágenes del hallazgo histórico no fueron revisadas; siguen pendientes. Las cinco descargas previas no se duplicaron.

**128 posts únicos: 5 procesados, 13 excluidos con motivo y 110 parciales.** No se avanzan fronteras completas ni se promete detección de todos los cambios de comentarios. Scope: posts y cambios seleccionados, sin chats, presentaciones o material privado inaccesible. Próximo paso: cargar documento sqcli cuando el owner lo descargue; localizar/revisar la grabación cuando exista locator y completar medios de fuentes parciales. No hay monitor ni minados, cambios de riesgo o publicación externa.

### Skill reusable

[[30-resources/agents/skills/imox-update/SKILL.md|imox-update]] queda en registro del bootstrap para una sesión nueva en este vault. Disparador natural «actualiza imox»; gate Codex/Hefesto, Chrome del owner, lista completa de descargas, posterior carga local por pedido y continuidad desde manifiesto/revisiones, sin depender de este chat. Contrato genérico de ingesta enlazado, sin duplicarlo.

## Fuentes

[[IMOX — Registro de publicaciones]] · [[IMOX — Cobertura de revisión]] · [[IMOX — Descargas pendientes]] y las fuentes de este lote.

## Validación final

41 notas canónicas con lint estricto: cero errores y cero advertencias. Bitácora de Agents append-only preservada en su formato previo. Las 42 rutas tocadas tienen enlaces internos resolubles; 128 identidades de post únicas, conteos coherentes y manifiesto con una descarga pendiente sin filename inventado. Skill registrada para cold start, frontmatter YAML válido y prueba real del pedido actual; sin prometer cobertura completa del foro. Fin verificado: 2026-10-30T16:05:31-03:00.
