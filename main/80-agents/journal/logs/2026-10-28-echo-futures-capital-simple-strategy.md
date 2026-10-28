---
type: change_log
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
entities:
  - "[[Echo — I+D de Estrategias]]"
  - "[[Echo I+D — Futures]]"
  - "[[Echo I+D — Cobertura Futures]]"
  - "[[FUT-R01-RESEARCH-MANDATE]]"
related:
  - "[[80-agents/journal/logs/2026-10-27-echo-futures-fut-r01-owner-mandate]]"
aliases: []
confidence: verified
source_session: "Owner — Echo Futures, corrección capital y ficha simple, 2026-10-28 America/Santiago"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# FUT-R01 — Capital confirmado y ficha simple de Strategy

## Cambio

Actualizados programa padre, planner Futures, cobertura y prompt maestro; prompt_version pasa de 1 a 2. Nuevo registro consolidado; se conserva el historial del 2026-10-27.

- Capital vigente: USD 4.000 exclusivo de Futures; aproximadamente USD 2.000 Forex separado; no nuevos aportes previstos. USD 5.000 superseded.
- Embudo compra/pase/funded/cobro confirmado en su sentido general como ideal, sin convertir tasas en estimaciones.
- Primer retiro objetivo USD 3.000, split 90%/80%; bruto/neto permanece abierto.
- Ficha Strategy simplificada por decisión Owner: setup, filtro, RR u objetivo–riesgo técnico. MM por prop/etapa es otra entidad. El prompt elimina la descomposición extensa y se reduce de unas 3.300 a unas 1.700 palabras.
- Reserva, límite de pérdida y desembolsos por etapas se prepararán para decisión antes de compras; no quedan aprobados ni cuantificados aquí.

## Motivo

El Owner corrigió capital/asignación y rechazó complejidad innecesaria en la descripción de estrategias. Se aplica su instrucción actual sobre la propuesta previa, conservando gates y evidencia en las autoridades existentes. La autorización documental sigue vigente.

## Fuentes usadas

- Mensaje Owner del 2026-10-28: USD 4.000 Futures, aproximadamente USD 2.000 Forex, sin más capital; objetivo primer retiro USD 3.000 con split 90%/80%; ficha simple algorítmica por indicadores y separación Strategy/MM.
- Cuatro notas vigentes leídas en `xKoRx/agents-os@4aab5053633d6c4c97a5a4d9d7340918103161c3`; conservaban los blobs publicados en la iteración anterior.
- Autoridades de actualización/contrato documental ya cargadas; materializador y lint canónicos existentes.
- Revisión ONE-SHOT read-only de la representación de decisiones: capital no equivale a gasto autorizado, bruto/neto abierto, aspiración no garantiza rendimiento y distancia de precio no equivale a dinero arriesgado.

## Resolución aplicada

La decisión nueva reemplaza el pendiente 4k/5k y asignación compartida en todas las superficies vigentes. La bitácora anterior permanece como historia fechada. Se respeta que las tasas son un ideal confirmado y que faltan detalles de horizonte/reset. La arquitectura existente no se modifica: tres bloques describen Strategy y el MM de prop/etapa continúa separado. Datos, ejecución, trazas y gates son evidencia, no una ampliación obligatoria de esa ficha.

No se cambia el plan Forex ni se presume que su capital financie Futures. No se selecciona prop, riesgo monetario, tamaño de lote ni compra. Tampoco se resuelve por inferencia si los USD 3.000 son previos o posteriores al split.

## Validación

- Registro materializado con el contrato canónico de change_log, exit 0.
- Lint canónico dirigido a los cinco archivos: exit 0, ERROR=0, WARN=0.
- Master reconciliado en `122b97128a3d03fcd7e200b03b6191ca130d2c52` y, tras avanzar durante la publicación, en `61d66b14441feeb690981f3d5cacfeeea6a20a74`: cuatro documentos sin cambios concurrentes respecto de la lectura inicial y ruta del nuevo registro ausente. Se reconstruye el commit sobre el último árbol, conservando el trabajo concurrente.
- Sólo documentación; sin tests de producto, campañas, acceso físico a Hefesto ni cambios de runtime.
- Publicación prevista directa a master, sólo cinco archivos, fast-forward con lease y sin ramas/PRs.

## Compartibilidad

Scope local. Contiene decisiones de capital del proyecto; sin credenciales, secretos ni envío a terceros.

## Rollback

Corregir sólo estos cambios mediante nuevo commit auditable en master, preservando trabajo concurrente y las decisiones vigentes del Owner. No resetear ni forzar HEAD; no borrar el historial ni tocar resultados técnicos.

