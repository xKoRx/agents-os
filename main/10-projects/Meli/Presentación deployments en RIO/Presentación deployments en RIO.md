---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-01
due: 2026-09-08
progress: 98
repo: ads-signals-knowledge-library
jira:
prs:
aliases:
  - Presentación RIO deployments
  - Deployments en RIO
tags:
  - kind/project
  - area/meli
  - project/presentacion-deployments-rio
created: "2026-09-01"
updated: "2026-10-01"
---

# Presentación deployments en RIO

> [!info]+ Presentación deployments en RIO
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Entrega:** 2026-09-08
> **Knowledge vigente:** [[ads-signals-knowledge-library]] · **Plataforma:** [[RIO]]

## 🎯 Objetivo

- Explicar en la meet el recorrido completo del deployment dentro de Playmaker: por dónde pasa, qué entidades crea y cuándo, qué decisiones condicionan el envío y cómo procesa resultados y avanza batches.
- Mantener un relato acotado con seis paradas en código, siguiendo un mismo caso y desde el request de front hasta el polling, con Grid técnico como apoyo.

## 📊 Estado actual

- Guion y nueva propuesta Grid siguen seis capítulos: request/delta, entidades y creación del Deployment, dispatch, resultado, continuación/cierre y polling/UI. Se sigue el mismo ejemplo de topic y engine.
- Recorrido contrastado con `rio-playmaker origin/master` local `3cd0daf6e17841ab79381f1eb5e2bd014ad68bd1` el 2026-10-01; producción y routing vivo no verificados.
- Corregidas dos distinciones para la exposición: DeploymentGroup contiene la orquestación y los batches se determinan por `ComponentRun.runOrder`; los nuevos Deployments ya nacen con un deadline de dispatch.
- El usuario rechazó la primera propuesta de Grid por su densidad de texto. Se rediseñaron las seis escenas con diagramas causales, iconos, estados y etiquetas cortas; topic y engine mantienen identidad visual. El detalle técnico queda en el guion y en enlaces a código.
- Preview corregida tras detectar que el iframe fijo de 1280 px se recortaba dentro del panel real de 610 px. Ahora escala manteniendo proporción, con navegación compacta y pantalla completa; se revisaron las seis escenas en el panel real y la vista ampliada de 1800 px. Se igualaron columnas y se alinearon conexiones.
- Rediseño local revisado en canvas 1280×720: `30-resources/grids/rio-deployments-story/index.html`. Actualización del [Grid existente](https://grid.adminml.com/d/01M3VWJ9GQ1FHABT2GJZEN1VPA/view) pendiente por falta de conexión a la API; allí sigue la versión de texto.
- Request, BFF, normalización y polling contrastados con `ads-signals-frontend origin/master` local `791f79dd8050e1432bdc5c936539b22dbaa4e35d`.
- Pendiente ensayar el recorrido y ajustar el tiempo definitivo; el guion conserva un presupuesto orientativo de 20–25 minutos.

## 🧱 Entrega de desarrollo

_No aplica — proyecto de comprensión y presentación; no modifica código ni configuración ejecutable de RIO._

## 🧩 Subproyectos

_Sin subproyectos._

## ✅ Tareas

- [x] Reemplazar `signals-knowledge` por [[ads-signals-knowledge-library]] en el vault #owner/me #type/admin #area/meli
- [x] Revisar estructura, contratos, flujos, servicios, troubleshooting, catálogo, gobierno y evaluaciones de la knowledge library #owner/me #type/research #area/meli
- [x] Contrastar las afirmaciones materiales con `origin/master` de los repos RIO #owner/me #type/research #area/meli
- [x] Crear [[Deployments en RIO — flujo completo]] #owner/me #type/research #area/meli
- [x] Crear [[Revisión de ads-signals-knowledge-library]] #owner/me #type/research #area/meli
- [x] Reestructurar [[Deployments en RIO — flujo completo]] como guion técnico con tecnologías, puntos críticos, recuperación y deuda #owner/me #type/research #area/meli
- [x] Crear [[Guion presentación — Deployments en RIO]] y Grid visual local #owner/me #type/research #area/meli
- [x] Reencuadrar el Grid para revisión entre expertos, reducirlo a seis slides y agregar el modelo de datos visual #owner/me #type/research #area/meli
- [x] Reenfocar el guion a seis paradas verificadas en código de Playmaker, con entidades y decisiones en su momento del flujo #owner/me #type/research #area/meli
- [x] Crear propuesta Grid técnica de seis capítulos desde el request de front hasta la vuelta del polling #owner/me #type/research #area/meli
- [x] Rediseñar las seis slides como relato visual de bajo costo de lectura, conservando el detalle en el guion/código #owner/me #type/research #area/meli
- [ ] Subir y revisar el rediseño visual en Grid cuando vuelva la conexión a la API #owner/me #type/admin #area/meli #waiting
- [ ] Ensayar el recorrido por código y ajustar profundidad al tiempo disponible #owner/me #type/research #area/meli
- [ ] Confirmar configuración viva de routing y suscripciones para distinguir código base de tráfico real #owner/me #type/research #area/meli #waiting

## 📆 Bitácora

- **2026-10-01** — Por aclaración del usuario, la meet se centra en profundizar el flujo de Playmaker dentro de un recorrido acotado con código. Se reemplazó el guion por seis paradas verificadas contra `origin/master` local y se corrigieron group versus batch y deadline inicial; se creó una propuesta Grid Dark Theme de seis slides y se verificó también el front/BFF/polling.

- **2026-09-08** — Segunda revisión visual: se ubicó la creación del Deployment explícitamente en el dispatch del batch, se reemplazaron A–D por tres marcadores de familias de corte, se rehízo la slide 3 como diagrama entidad–relación, se explicitó que Materializer termina mediante otro POST HTTP y se simplificó la slide 5 eliminando las cuatro cajas de mecanismos. Fury CP y `timeout_at` quedaron explicados dentro de la propia slide.
- **2026-09-14** — Se expandió el Grid local de seis a doce slides para una revisión más específica: el recorrido distingue qué entidad crea Playmaker en cada momento, las dos transacciones de dispatch, el contrato e identidades del trigger, la aceptación y efecto de cada CP, la publicación y consolidación de resultados, y la continuación del batch. La evidencia sigue limitada a código/documentación local; routing vivo e incidencia real permanecen pendientes.
- **2026-09-08** — Se rearmó la presentación a seis slides y se eliminó el framing de venta o propuesta. El foco vuelve a ser el flujo vigente; las fallas aparecen como segunda lectura. Se agregó un diagrama visual del modelo de datos, DeltaComputationService, los seis CPs y su uso de KVS, el ciclo REST asíncrono de Materializer y la muerte súbita tanto de Playmaker como de un CP. `gcp-kafka-topic` quedó marcado como routing pendiente de validar en configuración viva.
- **2026-09-08** — Se creó un Grid local de ocho slides y un speech de 10 a 12 minutos. La presentación abre con arquitectura, ownership, tecnologías y las dos rutas completas; el análisis de detenciones comienza recién en la segunda mitad e incluye la muerte súbita de un CP después del ACK, el timeout inicial inexistente, locks sin replay y terminales KVS que pueden bloquear recuperación.
- **2026-09-07** — Se revalidó el flujo con refs locales más recientes y se reestructuró la guía para presentar en dos pasadas. Se corrigió la lectura de Materializer: es owner explícito de `s3-bucket` y `gcs-bucket`, pero el catch-all de Playmaker también absorbe tipos no migrados; `gcp-kafka-topic` es el caso verificado. Se documentaron nueve puntos críticos y nueve deudas técnicas con criterio de aceptación.
- **2026-09-01** — Proyecto creado. Se reemplazó la knowledge anterior, se auditó íntegramente la librería nueva y se contrastó el deployment flow con el código actual de los repos. La librería es estructuralmente buena, pero su validación falla con 17 errores y varias afirmaciones materiales quedaron atrás de `master`; la documentación para mañana usa el código como autoridad.

## 🧭 Decisiones

- Para comportamiento vigente, `origin/master` del servicio dueño prevalece sobre la knowledge library; la librería sirve como mapa y provenance, no como sustituto de verificación.
- El guion contiene el recorrido vigente para la meet; la investigación de septiembre y la auditoría de la knowledge conservan sus fuentes y fechas de verificación como referencia.
- Actions y runtime status se explican como protocolos adyacentes, no como estados del deployment, para no mezclar máquinas de estado distintas.
- La pantalla muestra escenas, relaciones y estados; el presentador explica el detalle técnico y abre código en los puntos de decisión. Evitar párrafos y grandes bloques de código dentro de las slides.
- El recorrido sigue una solicitud completa por Playmaker; las entidades y decisiones se explican cuando aparecen en el código. Los detalles internos de CPs y el backlog de recuperación quedan para preguntas posteriores.
- Materializer se presenta en el punto de routing como camino REST con vuelta por callback y normalización al bus de resultados. El YAML local no prueba routing vivo.

## 🔗 Docs / Links

- [[Deployments en RIO — flujo completo]] — investigación de septiembre; consultar el guion para el recorrido verificado en octubre.
- [[Guion presentación — Deployments en RIO]] — recorrido actual por código, entidades por momento y decisiones importantes.
- [Propuesta Grid — request a polling](https://grid.adminml.com/d/01M3VWJ9GQ1FHABT2GJZEN1VPA/view) — seis capítulos; rediseño visual pendiente de subir. HTML, preview y manifest en `30-resources/grids/rio-deployments-story/`.
- `30-resources/grids/rio-deployments-critical-flow.html` — Grid anterior de septiembre.
- [[Revisión de ads-signals-knowledge-library]] — auditoría de cobertura, integridad y frescura.
- [[ads-signals-knowledge-library]] · [[RIO]] · [[rio-playmaker]] · [[rio-sdk-events]]

## 💡 Ideas

- Usar un mismo caso ilustrativo para seguir el nacimiento de entidades, la salida del trigger, la vuelta de outputs y la habilitación del próximo batch.
