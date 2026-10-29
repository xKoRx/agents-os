---
type: change_log
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
application:
entities:
  - "[[Echo I+D — Futures]]"
related:
  - "[[FUT-R01-LOTE-COBERTURA-01]]"
  - "[[FUT-R01-I01-SPEC]]"
  - "[[FUT-R01-I01-CONTRATOS]]"
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
  - area/trading
  - project/echo-rnd
---

# Echo Futures — recepción A/B y propuesta de lote por cobertura

## Cambio

- Tipo: creación de artefacto y actualización de continuidad, por solicitud Owner de recomendaciones sobre cobertura, número de estrategias/alternativas e iteraciones cortas.
- Crea [[FUT-R01-LOTE-COBERTURA-01]]: adjudicación A/B, ocho bases/seis preguntas, techo propuesto 24 versiones, primera preparación FBC15/ORB30/MR04, coste progresivo, backlog con disparadores y mandato LC01-PREP preparado.
- Actualiza planner Futures, cobertura e índice; A/B dejan de figurar pendientes de recepción. Conserva ambos originales, DR/RV, evidencia histórica y planner C sin modificaciones.
- A: distinguir veto causal antes de enviar un market de fill ocurrido/tardío. B: cinco estrategias no son cinco cuentas; el conflicto 3/4 NQ requiere atribución de fase. La falta de A reportada por B está resuelta por cronología, no fue un error del worker.
- S04: 26 nativas + 63 SG únicas = 89; recuperar resultados existentes. SOURCE integrado al corte leído, aceptación semántica pendiente, I0 no despachado en C04. No se realiza ni duplica integración.
- 8/24 es recomendación pendiente Owner, no cuota de ganadoras, congelación de recetas, autorización de cómputo ni modificación de WIP/gates.

## Motivo

El Owner pide pasar de investigación amplia a un lote de estrategias con un propósito y una fábrica continua. Una única candidata nueva no debe bloquear todo el inventario; una multiplicación cartesiana tampoco aporta evidencia proporcional a su coste. La comparación por preguntas y la recuperación por identidad permiten avanzar por paquetes cortos, sin prometer throughput que no se ha medido.

## Fuentes usadas

- Instrucción Owner y retornos I01-A/B con sus commits; autoridad vigente de FUT-R01 y skill manager.
- Agents-OS master 5fe399572e640fd632bd8b25d745dbb3f0c2947c; catálogo/runner/R03 de Echo master 2baf319ddcba622d9557bc9f23a13787b44c58a7.
- DR-03/04 con adjudicación RV-01, cobertura, planner Futures y estado C04 del laboratorio.
- Tres workers acotados read-only: A/B, cobertura y catálogo/coste. No escritos externos, motores, acceso físico ni certificados independientes. Root revisó fuentes decisivas y consolidó.
- Verificación primaria focal: paper de persistencia, ayuda específica MFFU Rapid EOD y tabla comercial. Alcance y URLs en el artefacto.

## Resolución aplicada

- Un lote FUT-R01 con ramas y cola; el primer paquete aprovecha apertura/rangos/calendario. Las otras señales se preparan y sus receipts se recuperan sin abrir seis iniciativas activas.
- MR01/MR08 tienen prioridad física menor: diversidad conceptual no basta para asignarles históricos caros. A empieza con una baseline; sus alternativas no se multiplican por horario/RR.
- Strategy, MM, etapa, RuleSet, identidad y evidencia se conservan separados. Payout variable y reinversión 100% siguen vigentes; 1/3 es umbral Owner, no probabilidad asumida.
- C mantiene su manager. Requisitos de investigación: source→receipt, guard de admisión y presupuesto real por tiempo/recursos. max-runs limita lanzamientos; characterize usa resultados existentes; no scanner gratuito ni checkpoint intrabar acreditados.
- Sólo propuestas y preparación documental; la siguiente ejecución exige el alcance y presupuesto correspondientes.

## Validación

- Nuevos artefactos materializados desde las plantillas canónicas doc/change_log.
- Lecturas originales y deltas preparados contra blobs del HEAD observado. Reconciliar HEAD y preservar trabajo concurrente antes de publicar sobre master, sin ramas/PRs.
- Lint estricto de las cinco notas: ERROR=0, WARN=0. Lectura remota posterior requerida antes de declarar publicación verificada.
- No tests de producto, campañas, código, cambios de G0–G5, compras, operaciones, hosts o escritura del frente C. Agent-run omitido por alcance documental; ningún consumo Pro/throughput inventado. Sin indexación o réplica física declarada.

## Compartibilidad

- Scope: local.
- Redacción revisada: sin credenciales ni secretos. Importes/decisiones pertenecen al mandato Owner.

## Rollback

Revertir únicamente este delta documental mediante nuevo commit reconciliado sobre master, preservando cambios concurrentes, originales A/B y DR/RV. No resetear el repositorio ni tocar producto.

## Continuidad

OWNER_ACCEPTANCE=REVIEW para 8/24; LC01-PREP preparado, no despachado. Primero congelar baselines de apertura y reutilización; C devuelve admisión/coste cuando corresponda. El programa y este manager permanecen abiertos; no se ejecutó cierre completo ni feedback de cierre.
