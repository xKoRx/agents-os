---
type: change_log
schema_version: 1
scope: session
created: '2026-10-28'
updated: '2026-10-27'
area: '[[Trading]]'
project: '[[Echo — I+D de Estrategias]]'
entities:
  - '[[Echo — I+D de Estrategias]]'
  - '[[Echo I+D — Futures]]'
  - '[[Estrategias IMOX — Forex y CFD con Echo Forge]]'
related:
  - '[[echo-rnd-two-market-program]]'
  - '[[Echo I+D — Mapa de capacidades]]'
aliases: []
confidence: verified
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - tech/agents-os
  - project/echo-rnd
  - change/organization
---

# Echo I+D — Unificación y continuidad — 2026-10-27

## Cambio

**Fuente y autorización:** mandato directo del Owner del 2026-10-27: unificar la I+D de Echo/trading en un programa permanente con dos líneas, managers, metodología, cobertura Futures y cierre con feedback. Sustituye la instrucción anterior de parar en discovery. No autoriza motores, estrategias/código de producto, cuentas ni producción.

**Baseline:** `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`, tree `f0d64c984c6f1c1e04d1112a45ff35dcd12fa174`. Revisión documental enfocada; superficies físicas no inspeccionadas.

| Antes | Después | Autoridad/evidencia |
|---|---|---|
| Investigación IMOX autónoma y Futures repartida entre producto/lab/fuentes | [[Echo — I+D de Estrategias]] como raíz; IMOX reutilizado como división Forex; [[Echo I+D — Futures]] como nueva división | Mandato Owner; [[echo-rnd-two-market-program]] |
| Sin manager transversal ni manager de ciclo científico Futures | Nuevas skills `echo-rnd-manager` y `echo-futures-research-manager`; `imox-strategy-research` extendida a manager Forex, revisión 2 | INDEX y [[Echo I+D — Mapa de capacidades]] |
| Metodología común implícita | `echo-rnd-cycle-runbook`: registros, source→spec→code, mandatos, retornos, decisiones, aprendizaje y mejora controlada | Contrato documental; no runner ni software nuevo |
| Matriz Futures ausente | [[Echo I+D — Cobertura Futures]] propuesta, NQ inmediato y expansión aparcada | Inventario/code refs declarados; no prueba de alpha |
| Vista Forex decía rescate pendiente | Cobertura y Frente NDX alineados con rescate25-10 y registro26-10; F0→F3 y objetivo táctico diez activos preservados | Proyecto/registro canónicos; no nueva ingesta |
| Optimización bajo producto; investigación soporte dispersa | Optimización, Prop Universe y Prop Economics bajo línea Futures; Regularización IMOX bajo Forex | Parent/frontmatter, links y puente único transferido sin cambiar REVIEW |
| Retester con activación Forex residual y conformidad implícita | Futures-only; conformidad fuente/regla/predicado/fixtures/traza y contexto E2T histórico | Gates, números, recibos y campo heredado `QUARTER_FUNDED` conservados |
| Dos excepciones textuales de baja actividad omitían G2C | Excepciones reconciliadas con cadena propia y guard vigente; sin G2C no quarter | Autoridad retester/qualification guard preexistente; no gate rebajado |
| Ocho pares de runbooks byte-idénticos en core/federados | Ocho autoridades federadas; rutas core como redirecciones fuera de recuperación normal | Igualdad de Git blobs comprobada en baseline; historia preservada |
| Golden E2E antiguo podía seleccionarse como receta vigente | Aviso acotado de aplicabilidad frente al mandato Owner27-10 de Forge | Comandos y cuerpo histórico desde Propósito preservados |
| Índice tenía descripciones antiguas de cierre/feedback | Routing de managers y mapa; cierre por delta y feedback por evento | Skills canónicas vigentes |

También se normalizó metadata heredada sólo en notas tocadas: Trading recibe schema_version1; tags sin namespace y status `complete` se ajustan al contrato; secciones mínimas faltantes se añaden sin reescribir historia. Producto/runtime siguen en sus owners; no se fusionan los dos controles técnicos homónimos de Forge, se enlaza la ruta vigente explícita.

## Validación

- Notas nuevas creadas por `materialize_schema_note.py` con el contrato/template de cada tipo, sin cambios al schema ni templates.
- Lint estricto dirigido a los archivos modificados, parse YAML y revisión de referencias: gate previo a publicación; ver recibo de cierre al finalizar.
- Tres forward-tests de managers en contextos frescos y sin decisiones esperadas filtradas:
  - Global: mantuvo dos preguntas documentales, WIP y Owner; no lanzó campañas para fingir paralelismo.
  - Futures: rechazó quarter/histórico sin G2C, concatenación de dos contratos y E2T como perfil actual; separó stop experimental de fuente.
  - Forex: reconoció rescate completado, F0 pendiente, diez activos≠diez EAs y genética vigente; no inició Random/Builders.
- Activación positiva/negativa/adyacente revisada para managers y skills refinadas. Retester conserva su gate técnico; SQX conserva diseño de presets; tareas de producto derivan al owner técnico.
- Perfil federado de skills: se usa lint Agents-OS y parse YAML. El `quick_validate.py` portable rechaza claves federadas `type/scope/created/updated/tags`; esa incompatibilidad prevista por skill-contract no se resuelve quitando metadata.
- Ocho redirects validados y originales preservados en Git. Golden conserva comandos/historia; no se certifica su ejecución en144.
- Ningún backtest, build de producto, cambio de cuenta, despliegue ni nuevo proceso automático se ejecutó.
- Graphify no está expuesto en esta superficie. Validación remota se hará por Markdown/tree/blobs; no se atribuye un PASS al índice local ni a la réplica de Hefesto/Daedalus.

### Recibo de publicación

Estado previo al write remoto: `LOCAL_VALIDATED_PENDING_REMOTE_VERIFICATION`.
Se completará con el commit publicado, readback y resultado de validaciones al cerrar la sesión. No interpretar este estado provisional como sincronización física de hosts.

## Rollback

Revertir únicamente el delta de esta reorganización mediante un nuevo commit sobre `master`, sin force-push. Restaurar parents, puente e índices conjuntamente si se revierte la estructura; conservar evidencia/campañas y las decisiones Owner. Las copias antiguas de runbooks se recuperan desde el baseline citado si hiciera falta. No resetear trabajo concurrente ni reabrir entregas históricas por un rollback documental.

## Continuidad

- Global: [[Echo — I+D de Estrategias]].
- Forex: planner existente, sección Continuidad y entrada del manager Forex; siguiente preparación EVAL-144/F0.
- Futures: [[Echo I+D — Futures]], FUT-R01 y entrada del próximo chat.
- Nuevas decisiones Owner: perfil económico Futures, primer experimento y presupuesto. Matriz/prioridades propuestas separadas de aceptación.
