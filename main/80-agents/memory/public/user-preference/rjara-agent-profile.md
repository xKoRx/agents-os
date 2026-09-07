---
type: user_preference
schema_version: 1
scope: user
created: 2026-06-27
updated: 2026-09-03
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[human-first-technical-writing]]"
  - "[[rjara-meli-work-preferences]]"
  - "[[rjara-aranea-operations-preferences]]"
  - "[[rjara-vpn-routing-preferences]]"
aliases:
  - perfil de usuario rjara
  - preferencias del usuario
  - user model rjara
confidence: verified
load_policy: always
indexable: true
index_priority: critical
tags:
  - agent/alwaysload
  - kind/user-preference
  - priority/critical
  - project/agentsos
  - scope/user
---

# rjara Agent Profile

- **installation_status:** complete
- **Nombre:** Rodrigo Jara (`rjara`)
- **Idioma:** español de Chile
- **Rol:** Sr Software Engineer, equipo **Signals** (dentro de **ADS / Advertising**, MercadoLibre). Signals es dueño de la plataforma [[RIO]] (10 apps). Equipo anterior: VIS.

## Preferencias de interacción

- `[DURA]` Responder en español chileno cuando el usuario escriba en español,
  salvo que pida otro idioma.
- `[DURA]` Ser directo, colaborativo y preciso; preferir KISS/YAGNI, early
  return, SOLID y clean code cuando aplique.
- `[DURA]` **Todo comentario de GitHub escrito en nombre de Rodrigo debe ser preciso, conciso, clarificador, cordial, amigable y profesional, y debe redactarse aplicando [[human-first-technical-writing]].** Antes de publicarlo, hacer una auditoría explícita de tono y eliminar lenguaje confrontacional, defensivo, despectivo o excesivamente coloquial. En desacuerdos, reconocer el punto de forma constructiva, indicar la decisión y su evidencia, explicar el alcance brevemente y separar pendientes de manera neutral. Nunca usar fórmulas como “te lo voy a decir directo”, “no lo voy a hacer” o equivalentes. Esta directiva es crítica porque una mala redacción puede afectar laboralmente al usuario.

## Preferencias de trabajo

- `[DURA]` No inventar ante una duda material. Investigar o preguntar; si es un
  detalle técnico no bloqueante, dejarlo como supuesto o pendiente explícito.
- `[FUERTE]` Avanzar de forma autónoma cuando el siguiente paso sea claro y
  entregar resultados pequeños, verificables y retomables.
- `[FUERTE]` Evitar updates innecesarios; comunicar degradaciones, decisiones y
  resultado final con brevedad.
- `[DURA]` No cargar flujos o skills que el usuario excluya.
- `[DURA]` No ejecutar cierre completo ni crear L0/L1/feedback salvo pedido
  explícito. Al terminar trabajo normal, responder sin ritual.
- `[FUERTE]` Actualizar el documento de control activo cuando cambie su estado
  real.
- `[DURA]` Código: [[agents-os-agent-run-register]].
- `[DURA]` Conectividad por dominio: [[rjara-vpn-routing-preferences]].
- `[DURA]` **Tests: funcionalidad crítica primero, coverage después.** Los tests existen para asegurar las funcionalidades críticas de un desarrollo, no para llenar un número. El orden es: identificar y cubrir primero los caminos críticos —lo que rompe producción si falla, los bordes de seguridad y autorización, la degradación silenciosa—, y recién entonces complementar con casos hasta llegar al piso. **Todo desarrollo nuevo debe alcanzar al menos 95% de coverage**, pero un 95% conseguido sin cubrir lo crítico no cumple la regla: un test que no atrapa nada no vale por existir. Si una rama no se puede alcanzar con ninguna entrada real, no se le escribe un test — se borra la rama.
- `[DURA]` En repos de desarrollo, jamás crear, fijar ni publicar una versión productiva limpia `X.Y.Z` desde una rama feature; usar una versión de prueba con sufijo y hacer el release productivo exclusivamente desde la rama principal autorizada después del merge (`master` en Meli/Fury).
- `[DURA]` **No mezclar proyectos ni iniciativas.** Separar **comprensión** (onboarding/research: entender un sistema) de **cambio** (delivery: meter una modificación). El discovery y el entendimiento del sistema viven en el proyecto de comprensión; un proyecto de cambio **no lidera ni carga** ese discovery y solo arranca cuando el entendimiento necesario está completo. Ante duda de a qué proyecto pertenece algo, preguntar en vez de asumir.
- `[DURA]` Marcar como ilustrativa toda cifra o regla que el usuario declare de
  ejemplo; nunca convertirla en definitiva por inferencia.
- `[FUERTE]` En documentos secuenciales, ordenar por el flujo real de hitos.
- `[DURA]` No guardar secretos ni dumps pesados; cambios canónicos dejan log
  auditable.
- `[DURA]` Usar Graphify o búsqueda enfocada como retrieval primario y abrir
  Markdown solo para validar fuentes seleccionadas.
- `[FUERTE]` Toda documentación de entidad (app, servicio, área, concepto) se hace con el mecanismo **LLM Wiki** (skill `agents-os-resource-wiki`) sobre `30-resources/`: integrar en la página canónica, actualizar `00-index.md` y `log.md`, y **separar lo estable** (responsabilidad, rol, contratos) **de lo volátil** (stack, librerías, versiones; con `last_verified`). Ver [[30-resources/00-RESOURCE-WIKI|Resource Wiki]].
- `[DURA]` **Prohibido el hard-wrap.** Nunca insertar saltos de línea manuales dentro de un párrafo o de un ítem de lista en Markdown. Cada párrafo y cada bullet va en **una sola línea continua**; el ajuste de línea se deja al render (soft-wrap). Solo hay salto real entre bloques distintos (párrafo↔párrafo, ítem↔ítem, encabezados, tablas). No aplica dentro de bloques de código. Esto rige para todo lo que el agente escriba (vault, código, docs, mensajes).

Las preferencias Meli y Aranea son scoped; se cargan solo con esas entidades.
