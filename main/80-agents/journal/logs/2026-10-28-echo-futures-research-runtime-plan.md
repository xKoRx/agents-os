---
type: change_log
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Echo]]"
project: "[[Echo I+D — Futures]]"
application:
entities:
  - "[[Echo Futures]]"
  - "[[Echo I+D — Futures]]"
related:
  - "[[FUT-R01-RESEARCH-MANDATE]]"
  - "[[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Futures — prompt de investigación y diseño de integración

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - Echo I+D — Futures.md y Echo I+D — Cobertura Futures.md.
  - FUT-R01-RESEARCH-MANDATE.md, versión 3.
  - Echo Futures.md y artifacts/runtime/EF-BACKTEST-RUNTIME-INTEGRATION-PLAN.md.

## Motivo

- Owner confirma USD 4.000 Futures / aproximadamente USD 2.000 Forex separados, ficha simple Strategy y superposición libre entre 5 challenge y 5 funded. Solicita el prompt completo corregido del frente 2 y avanzar planificación/diseño del frente 1 para integrar Backtester con el nuevo runtime y reproducir sesiones.
- Se conserva el contexto Owner de pruebas PROD; la última evidencia documental recuperada acredita una ventana DEV RO anterior. No se reemplaza una declaración por otra ni se adjudica readiness física.

## Fuentes usadas

- Mensaje Owner del 2026-10-28 y decisiones vigentes de FUT-R01.
- Agents-OS/master f844162d3305e6ce9441dd11598aa1a69e753164, reconciliado antes de publicación con 6dbd64d12a4818fe62f8bf947692bcc74cd8e0c6; autoridades R6, GOD-05, WINDOW-CARD-PRD6 y planner Lab.
- Echo Lab ae1b09bc10370806f7648f076c5fa0825c9efa4e y runtime bcffcf310c5825cd7b1c434158ee160a93b45c47; ancestro d74b652500e673fc2bf4289f9f195f11960ba26e. Fuentes concretas y alcance en el nuevo plan.
- Workers acotados de lectura fuente, autoridad y diseño de investigación; revisión documental técnica y de gobierno. No pruebas físicas; consumo Pro no comprobado = UNKNOWN.

## Resolución aplicada

- Prompt v3 autocontenido y orientado a evidencia externa: tres módulos, ficha Strategy de tres bloques, MM separado, ambos escenarios del payout USD 3.000 y límites de ejecución. Deep Research completo preparado, no ejecutado.
- Superposición 5+5 deja de ser pendiente. Retorno interno/read-only se separa del encargo externo.
- Plan candidato de integración bajo Echo Futures, sin nuevo planner ni reactivación de S05. Diferencia lógica compartida, replay de decisiones, reconstrucción contable y simulación de fills; identifica módulos/MM/policies, divergencia de ramas, caja histórica y simultaneidad no demostrada.
- Revisión independiente incorporada: evitar circularidad al usar revisiones contables como input y resultado; no atribuir al venue un modelo de latencia no acreditado.
- Se prepara mandato read-only de Hefesto y secuencia de hitos. No ejecución, implementación, compras, despliegue ni cierre formal.

## Validación

- Creación desde plantillas canónicas mediante materialize_schema_note.py; lint estricto de los seis documentos: ERROR=0, WARN=0, notes_scanned=6.
- Revisión de fuentes y de coherencia del plan. No se corrieron pruebas de producto, backtests, campañas ni replay.
- Publicación atómica en Agents-OS/master condicionada a reconciliar HEAD y verificar contenido remoto; no ramas/PRs ni force.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** documentación interna del proyecto, sin credenciales ni secretos. El prompt externo contiene únicamente la cápsula de contexto necesaria.

## Rollback

- Revertir sólo este cambio documental mediante un commit posterior sobre master, preservando trabajo concurrente. No modifica source, binarios, datos, cuentas ni resultados previos.

## Addendum — frente 2, campañas prop y mandatos separados

### Fuente y alcance del delta

Nueva instrucción Owner del 28-10-2026: la operativa Futures se evalúa como campañas prop, no como rentabilidad convencional de una cuenta propia. No imponer esperanza positiva por trade ni preservar cada evaluación como requisito universal. Investigar matemáticamente políticas agresivas y resolución rápida pase/pérdida, con posterior simulación autorizada. Persistir el informe exploratorio y entregar prompts ONE-SHOT por especialidad para consolidación posterior del submanager.

Este addendum documenta sólo el delta del frente 2. Las fuentes, workers y validación de seis documentos descritos en las secciones históricas anteriores no son ejecución ni validación de los encargos DR-01–04 aquí preparados.

### Cambios publicados

- `10-projects/Echo I+D/artifacts/FUT-R01-RESEARCH-MANDATE.md` actualizado a v4 en commit `09e0f1e2cb1d61547d23221ef8284bddbbac93c8`, blob `fe4559b73e64e644aa373d7608a0304d2207d3ad`. Contiene edición documental del informe previo, rectificación explícita, límites de trazabilidad y cuatro prompts autocontenidos más revisión independiente.
- `10-projects/Echo I+D/Echo I+D — Futures.md` actualizado en commit `72bd062fd96ee9ecdf5df978a62c88d0f73472bb`, blob `3ed64a190c474d1c08ed1768ba4cb626d8d83f7f`. Estado, mandato económico, tareas y entrada del próximo chat reflejan la corrección. Se preservan historia y autoridades técnicas del frente 1.
- Este registro existente se amplía de forma consolidada; no se crea una segunda nota de sesión, feedback o autoridad de investigación.

### Resolución

La decisión se sitúa en señal × MM × RuleSet × campaña × caja. Expectativa por trade, win rate, profit factor y Sharpe son descriptores, no filtros económicos universales. La agresividad no se rechaza por defecto ni se declara óptima. La referencia Owner USD 400/funded se conserva como supuesto por contrastar con coste agregado de adquisición. No se fija una reserva ni se autoriza gasto.

El informe anterior queda como antecedente exploratorio. Sus cifras y elegibilidades comerciales requieren revalidación first-party en DR-02; no se certifican búsquedas previas, lectura íntegra de PDFs ni revisiones independientes no acreditadas. Las hipótesis de bandas y ruptura fallida son ilustrativas, no selección aceptada.

Mandatos: DR-01 matemática de campañas y MM; DR-02 contratos, automatización y costes; DR-03 mecanismos/cobertura NQ; DR-04 indicadores/reglas/validación. Primero recomendado DR-01. Los otros pueden investigar en paralelo con supuestos e interfaces explícitos. RV-01 exige los cuatro retornos y revisión efectivamente independiente; el submanager consolida después de recibirlos, no por votación.

### Verificación y límites del delta

Se usaron escrituras UTF-8 sobre `master` con SHA vigente por archivo; sin ramas, PRs ni force. Se comprobó mediante lectura remota la versión 4 y su blob después de publicación. La API devolvió commit/blob del planner actualizado; la verificación final debe cotejar también su estado remoto. No se acredita sincronización física de clones locales del Owner.

Actualización de notas ya existentes: no se crearon tipos ni notas canónicas nuevas. Se realizó revisión documental de alcance, reglas e interfaces; no se ejecutó el lint completo del vault en este delta. El resultado de lint de la sección histórica no se reutiliza como prueba de esta actualización.

Estado DR-01–04: PREPARADOS, NO EJECUTADOS. RV-01: ESPERANDO RETORNOS, NO EJECUTADO. No hubo código de producto, backtests, Monte Carlo, compras, órdenes, contactos con firmas, cambios de cuentas, modificación de G0–G5 ni cierre formal de sesión.

### Continuidad

Ejecutar DR-01 en una sesión de investigación externa con su cápsula autocontenida. Recibir y verificar los retornos completos, ejecutar revisión independiente y consolidar una decisión investigable y su alternativa. No asumir que la preparación de prompts implica dispatch ni resultados. Revertir sólo este delta documental con un commit posterior sobre master si corresponde, preservando trabajo concurrente.
