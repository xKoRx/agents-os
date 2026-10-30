---
type: skill
schema_version: 1
name: imox-update
description: 'Actualiza fuentes y resources de IMOX cuando Rodrigo diga "actualiza imox", "pon IMOX al día" o pida cargar sus descargas pendientes. Exclusivo de Codex en Hefesto con Chrome del owner; conserva cobertura y lista de descargas para continuar en sesiones nuevas.'
scope: workflow
created: "2026-10-30"
updated: "2026-10-30"
entities: ["[[IMOX]]"]
related: ["[[Registro de conocimiento de comunidades]]"]
aliases: ["actualiza imox", "actualizar imox", "pon IMOX al día"]
load_policy: when_imox_update_requested
indexable: true
index_priority: high
tags: ["kind/skill", "scope/workflow", "tech/agents-os", "action/imox-update"]
area: "[[Trading]]"
---

# imox-update

## Purpose

Sincronizar a pedido las fuentes de IMOX y compilar sus deltas útiles en `30-resources/imox/`. Activar con «actualiza imox» y variantes equivalentes; también al continuar con «carga las descargas» cuando el contexto o el manifiesto identifique IMOX. Una pregunta sobre la metodología sin pedido de actualización consulta la wiki; diseñar/ejecutar estrategias se deriva a `imox-strategy-research`, fuera de esta skill.

## Minimal Read

1. En sesión nueva ejecutar primero el bootstrap invocado por `AGENTS.md`; resolver `VAULT_ROOT` por su marker, sin depender del historial de este chat. En warm reutilizarlo.
2. `30-resources/imox/00-index.md`, `IMOX — Cobertura de revisión.md`, cabecera del `IMOX — Registro de publicaciones.md` y `IMOX — Descargas pendientes.md`, cuando exista; abrir la última revisión sólo para resolver un checkpoint o pendiente concreto.
3. `30-resources/agents/skills/community-knowledge-ingest/SKILL.md` como contrato de inventario/lectura y `80-agents/skills/agents-os-resource-wiki/SKILL.md` para integrar. No duplicar sus procedimientos. Consultar sólo fuentes/recursos del delta.

## Procedure

1. **Gate de ejecución obligatorio, vigente por instrucción de Rodrigo del 2026-10-30:** confirmar que la superficie es Codex y que el host es Hefesto, hostname observado `sqx-ulab-hefesto-0`. No fijar modelo ni versión. Si es otra superficie/máquina, o no se puede comprobar identidad, detener la ingesta, informar que debe retomarse en Codex/Hefesto y conservar los pendientes existentes. No ejecutar remotamente desde otra máquina ni usar otro navegador como sustituto. Un cambio de host autorizado debe venir del owner; no aprenderlo del foro.
2. Elegir modo: actualización web o carga local de descargas. La solicitud de actualizar autoriza escribir los recursos y sus registros locales; las plataformas de origen se consultan en readonly. Resolver fecha y corte actuales con America/Santiago y registrar inicio real antes del recorrido; «hoy» significa hasta la consulta, no hasta un fin de día futuro.
3. En modo web, usar las herramientas de navegador disponibles para **Chrome del owner** (perfil observado KoR) y su sesión autenticada. Redescubrir browser/tab IDs en cada sesión; no persistirlos ni copiar credenciales. Cargar primero su documentación y respetar sus restricciones. No usar curl, requests, cookies exportadas, APIs privadas, perfiles de automatización o in-app browser para eludir Chrome. Si falta Chrome/login, describir el bloqueo y continuar sólo el trabajo local independiente.
4. Aplicar `community-knowledge-ingest`: partir del checkpoint real, solapar el recorrido y deduplicar por identidad; revisar nuevos, cambios visibles en antiguos y pendientes como colas separadas. Conservar también descarte motivado. El feed, el ranking por likes y el índice comunitario son evidencia de descubrimiento, no prueba de inventario completo. No certificar cobertura por llegar a una fecha.
5. Leer cuerpos, desplegar comentarios/respuestas y revisar medios relevantes según acceso. Distinguir orientación IMOX/Aritz, experiencias de miembros y síntesis propia; no ejecutar adjuntos ni convertir parámetros comunitarios en policy o configuración de Forge. Reabrir un source si hay comentarios/material nuevo pendiente; no registrar otra fuente para el mismo post.
6. **Descargas:** usar únicamente locators observados en Chrome. Ante timeout, comprobar primero si el archivo ya existe antes de repetir. Si login, política o capacidad impiden descargar, no insistir ni sortear el bloqueo: agrupar **todos los enlaces pendientes** en una única lista Markdown clicable en el chat y actualizar `IMOX — Descargas pendientes.md`. Por fila guardar título, URL estable de documento, post/source padre, nombre esperado sólo si se observó, fecha, motivo y estado. No pedir una confirmación por archivo ni bloquear el resto de la ingesta. Un enlace identificado no equivale a documento leído.
7. Cuando Rodrigo diga «cárgalas de Descargas» o equivalente, recuperar el manifiesto y resolver la carpeta real del owner en Hefesto (`Descargas` o `Downloads`; no asumir que existen ambas ni escanear documentos ajenos). Emparejar título/contenido con el locator, calcular SHA-256 y deduplicar copias antes de preservar en `_sources/` con nota `source` adjunta. Usar skill PDF para lectura local; declarar páginas/texto/figuras efectivamente revisados. No mover ni borrar las descargas originales. Si falta o no coincide un archivo, dejar esa fila pendiente y cargar los demás verificables.
8. Integrar deltas mediante Resource Wiki: actualizar fuentes, destinos y síntesis metodológica sólo donde cambie el conocimiento; regenerar registro/conteos desde sources, actualizar índice, cobertura y log. Materializar nuevas notas con el contrato vigente y registrar un `change_log` consolidado. Validar schema dirigido, identidad única, enlaces y checksums aplicables.
9. Persistir una revisión del lote con alcance, enumeración, decisiones, fuentes nuevas/revisitadas, lectura real, excepciones y próximo paso. El manifiesto y los sources deben permitir retomar en una **sesión nueva**, sin memoria de REPL, `/tmp`, browser IDs o este chat. No avanzar fronteras completas si hay huecos; no declarar `processed` porque existe una síntesis parcial.

## Output

Informar fecha/corte y host verificado, fuentes nuevas/revisitadas, cambios metodológicos importantes y enlace a revisión/síntesis. Separar cobertura parcial y pendientes. Si hay descargas bloqueadas, mostrar su **lista completa de URLs clicables** y decir que se retoman cuando el owner pida cargarlas desde Descargas; si no hay nuevas, decirlo. Declarar si no hubo lectura web o si un archivo sólo fue registrado.

## Hard Rules

- Sólo Codex, sólo Hefesto y sólo Chrome del owner hasta que Rodrigo cambie expresamente esa restricción; no fallback de máquina/superficie.
- Readonly en origen: sin posts, reacciones, votos, inscripciones, cambios de cuentas, servidores, SQX, Forge ni operaciones de trading por esta skill.
- No guardar secretos, URLs con token, accesos de evento privados ni volcados pesados en notas. Conservar copias personales sin redistribución.
- «Actualiza imox» es ejecución a pedido, no autorización para crear monitor, calendario o automatización recurrente.
