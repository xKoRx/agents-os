---
type: session
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities: []
related:
  - "[[Research — W1-j Causal Gate Diagnosis 2026-10-30]]"
  - "[[2026-10-30-zcode-glm-5.3-flash-polymarket-w1k-conformance]]"
  - "[[2026-10-30-polymarket-w1k-conformance-feedback]]"
  - "[[2026-10-29-polymarket-engine-entity-updated]]"
aliases: []
confidence: high
source_session: sess_no-legible-desde-superficie-w1k-conformance
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - topic/research-ops
---

# 2026-10-30-polymarket-w1k-conformance-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Shot W1-k CONFORMIDAD (ZCode × `account:zai-individual-coding-plan/GLM-5.3-Flash`, host `sqx-ulab-hefesto-0`, hook fijado `90bdb0284012d344ab0db7bb59dba4beadb9fc23bc1d751b67117eeb39c4f2af`): corregir DOS problemas materiales del informe [[Research — W1-j Causal Gate Diagnosis 2026-10-30]] preservando historia como errata y sin inventar causalidad; auditar directamente el preregistro aplicable v2 contra el código congelado (`Detect`/`Evaluate`/`referenceLevel`, tests, orden de llamadas); decidir si `bestAsk < L` es condición ya necesaria del gate. Sólo lectura de fuentes y edición canónica: cero extractor/tests/build/replay, cero código producto, sin red/captura/raw/engine.db/OOS/cuentas/órdenes/push.

## Contexto cargado

- Bootstrap AGENTS OS acotado una vez (constitución, continuidad global always-load, índice de skills). **Bloqueo registrado sin variantes:** el perfil público global (`80-agents/memory/public/user-preference/`) no fue legible — todas las formas probadas (nombres plausibles del archivo y `ls`) denegadas por el guard de superficie.
- Delta: informe W1-j Causal Gate Diagnosis, `recovery-v2/verified-diagnostics.json` (`a1fc1d73…`), preregs v2/v1 (W1-h/W1-g), Research Corrections W1-h, informe piloto W1-j, continuidad §18 (31)-(32), y fuente congelada @ `c0c35e7`: `internal/strategy/pocs/sports/{sports.go, sports_test.go, w1k_synthetic_counterexample_test.go}`, `cmd/researchpilot/{economics.go, supervisor.go}`.

## Trabajo realizado

- **Problema 1 (bid-led → observación estricta):** retirado el salto causal «widenings liderados por caída del bid» / «el origen bid-led queda probado en el episodio» — `ask > L` + widening observan la posición del ask y el tamaño del ensanche, no el lado que lo causó; mecanismo histórico NO IDENTIFICADO (bid/mid de referencia ausentes de la fuente; sólo derivados etiquetados). El patrón bid-led queda probado sólo en el sintético (control del test `c0c35e7`). Historia preservada como ERRATA nueva en el informe.
- **Problema 1 (ejemplos):** sección «Ejemplos» actualizada a los representantes EJECUTADOS de `verified-diagnostics.json` — min gross −1.1028 (asset `612966…`, seq 4420), mediana −0.56805 (asset `503062…`, seq 2386), max −0.1838 (asset `503062…`, seq 4423), con assets completos, timestamps de señal, widening, profundidad de entrada y netos reales; los 2383/4420 previos (borrador `a966b1ff…` no acreditado) quedan superseded. Los agregados ya coincidían y no cambian.
- **Problema 2 (auditoría prereg v2 vs código):** sección nueva «Auditoría de conformidad con el preregistro aplicable» con citas textuales: v2 §5 («Sin datos futuros: … sólo frames recibidos ≤ instante de decisión») y v2 Propósito (reemplaza en alcance a la v1); cláusula v1 §4 («El frame actual jamás entra a su propia referencia») ambigua sobre si cubre `L`. Código: `ref` se computa pre-append (`sports.go:262` vs `:282`) y excluye el frame; `L` se lee en `Evaluate` post-append (`:514`, `referenceLevel` `:335-346`) y lo incluye; réplica de la revisión con el mismo orden (`economics.go:1249-1257`, `:1366-1371`, `replication_match` `:1446`, 36/36); `TestNoLookAheadInReference` cubre sólo `ref_bps`. **Veredicto: SIN desviación del preregistro aplicable** — incluir el frame de señal en `L` no es lookahead temporal (no se lee ningún frame posterior al instante de decisión); la tensión literal sería sólo con la v1, historia. Orden de llamadas y comportamiento ante llamadas documentados (exactly-once por frame; `Evaluate` recomputa `L` desde el anillo vivo, invocado una vez por señal sobre el frame de señal; guarda anti-auto-medición `:291-315`). Ejemplo mínimo razonado incluido (sin reejecutar ni re-referenciar el episodio).
- **Problema 3 (`bestAsk < L`):** determinado en el informe (punto 6 de la auditoría): condición YA necesaria de todo ACCEPT con fees no negativas y `entryVWAP ≥ bestAsk` (`netAtRef = (L−VWAP)·size − fees > 0` ⇒ `L > VWAP ≥ bestAsk`); multi-nivel endurece a `entryVWAP < L`; no dice nada de la profundidad de salida (ausente en la fuente). No se adopta como detector ni margen (cambiaría el conjunto de señales: decisión Owner/Metis); el «≥12%» previo queda SIN EFECTO como umbral (historia preservada); no resuelve fees reales, salidas ejecutables ni rentabilidad.
- **Registros:** informe corregido; continuidad bullet (33) + «Siguiente paso» actualizado; change_log (sección W1-k CONFORMIDAD); estas tres notas materializadas con `materialize_schema_note.py` (rutas relativas) y completadas con Edit contra el contrato.

## Artifacts creados o modificados

- Vault: `Research — W1-j Causal Gate Diagnosis 2026-10-30.md` (editado), `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (33)), `80-agents/journal/logs/2026-10-29-polymarket-engine-entity-updated.md` (sección nueva), las 3 notas nuevas de este cierre.
- Repo: SIN cambios (HEAD `c0c35e7…` intacto, árbol limpio, sin commit/push). Preregs y hashes: intactos. El informe piloto W1-j no se tocó (no arrastra las afirmaciones afectadas).

## Memoria propuesta o creada

- Ninguna memoria interna nueva: el delta es estado de proyecto (informe + continuidad + journal), no comportamiento transferible.

## Decisiones

- **Sin desviación del preregistro aplicable (v2):** la referencia conforma; recomendación de definir explícitamente en el próximo preregistro si `L` incluye o excluye el frame de señal (elimina la ambigüedad v1).
- **`bestAsk < L` documentado como condición aritmética ya necesaria del gate** (re-score offline), NO adoptado como detector ni mejora económica; adopción futura = cambio de estrategia (Owner/Metis con enmienda de prereg).
- Datos faltantes (bid/ask/mid de referencia, profundidad de salida) sólo vía esquema de captura futura preregistrado; jamás releyendo frames sellados.

## Pendiente

- Decisión Metis/Owner sobre la revisión económica especificada (sigue especificada, no implementada; sin captura autorizada).
- Registro por el lanzador del patrón de lectura del perfil público global si se desea cerrar el gap de bootstrap.
