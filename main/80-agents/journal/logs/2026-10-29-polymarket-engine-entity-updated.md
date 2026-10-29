---
type: change_log
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine]]"
related:
  - "[[Research — First Hypothesis W1-f 2026-10-29]]"
aliases: []
confidence: verified
source_session: sess_4d2d4204-b8bd-4a0f-9ea9-5218ad3d6c24
source_feedbacks:
  - "[[2026-10-29-polymarket-w1f-first-hypothesis-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-29-polymarket-engine-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Preregistration — First Hypothesis W1-f 2026-10-29.md` (nuevo; preregistro congelado antes de medir)
  - `10-projects/Personal/Polymarket Engine/Research — First Hypothesis W1-f 2026-10-29.md` (nuevo; informe canónico del shot)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (actualizado: bullet (18) W1-f, "Siguiente paso concreto" reemplazado con historia preservada, regla de horario 2026-10-29 registrada sin borrar historia)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1f-first-hypothesis-summary.md` (nuevo)
  - `80-agents/journal/feedback/system-1/2026-10-29-polymarket-w1f-first-hypothesis-feedback.md` (nuevo)
  - `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-polymarket-w1f-first-hypothesis.md` (nuevo)
  - este change_log (nuevo)
  - Repo externo (fuera del vault): commit local `853c0e46c9be2de4e84201e240e9cf8366b1036e` en `w0/offline-causal-replay-20261027` — `internal/experiment/w1f_hypothesis_test.go` + `internal/experiment/w1f_hypothesis_integration_test.go` (sólo tests; sin push, sin cambios de producción)
  - OUT (fuera del vault): `validated-baseline/w1-f-first-hypothesis-20261029/` — prereg JSON, 8 evidencias, 12 manifests derivados, `W1-F-MANIFEST.json`, binario `engine`

## Motivo

- Cierre del mandato W1-f (one-shot GLM-5.3-Flash Max): primera hipótesis preregistrada y falsada/confirmada con el Engine real, con diagnóstico de suficiencia de capture-v6 y registros verificables.

## Fuentes usadas

- Continuidad Five-POC §§1–18 (estado vigente W1-e), informes W1-c/W1-d/W1-e, 6 manifests v6, `.private-execution/w1f/inputs.json`, código del checkout @ `7d519eb712a6a4ec9f369c92d9ee2c735454678b`.

## Resolución aplicada

- Hipótesis W1-F-H1 (falsación del gate de calidad prospectiva) elegida por contratos; prereg con P1–P7 y regla de veredicto congelados antes de medir; corrida autoritativa 14:45:03Z con `NO_FALSATION_FIRED_IN_RUN`; veredicto `DATA_SUFFICIENT_FOR_GATE_AVAILABILITY_TRIAL` con ramas stale/tick-change INCONCLUSIVE (déficit cuantificado) y economía no afirmada.

## Validación

- Suite completa del paquete `internal/experiment` PASS (13.875s final; incluye tests previos); BUILD exit 0 (binario reproducible `3d8b83f5…`); 12/12 inputs SHA-verificados in-process 2 veces por corrida; `capture.Verify` íntegro frontier 103; `git diff --check` limpio; árbol limpio tras commit; sin push.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Repo: `git revert 853c0e4` (commit local, sin dependencias; los tests no afectan producción).
- Vault: eliminar las notas nuevas listadas y revertir el bloque (18)/horario en la continuidad (edición textual; historia §§1–17 intacta).
- OUT: directorio `w1-f-first-hypothesis-20261029/` completo es aditivo; puede archivarse sin afectar inputs (los 12 inputs jamás fueron escritos).

---

## 2026-10-29 (W1-g) — preregistro económico PE-005-R1, plan de adquisición y correcciones W1-f

### Cambio

- **Tipo:** updated / created
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29.md` (nuevo; preregistro económico ejecutable, congelado antes de adquirir datos)
  - `10-projects/Personal/Polymarket Engine/Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29.md` (nuevo; diseño de adquisición mínima, NO ejecutado)
  - `10-projects/Personal/Polymarket Engine/Research — Economic Strategy Specification W1-g 2026-10-29.md` (nuevo; contrato vs preregistro, matriz de aptitud, fees citadas, correcciones)
  - `10-projects/Personal/Polymarket Engine/Research — First Hypothesis W1-f 2026-10-29.md` (erratas fechadas a/b/c añadidas; original íntegro)
  - `10-projects/Personal/Polymarket Engine/Preregistration — First Hypothesis W1-f 2026-10-29.md` (nota de alcance añadida; preregistro original íntegro)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (19) W1-g; "Siguiente paso" actualizado con historia W1-f preservada íntegra)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1g-economic-preregistration-summary.md`, `…w1g-economic-preregistration-feedback.md`, `…zcode-glm-5.3-flash-polymarket-w1g-economic-preregistration.md` (nuevos), este change_log (sección añadida)
  - OUT (fuera del vault): `validated-baseline/w1-g-economic-preregistration-20261029/` (copias de especificación + recibos con hashes medidos; sin código)
- **Repo:** sin cambios (HEAD `853c0e4` intacto, árbol limpio, sin commit ni push).

### Motivo

- Mandato W1-g (Metis): cierre TÉCNICO aceptado de W1-f; producir (1) UNA estrategia económica candidata completamente preregistrada y (2) el paquete de adquisición mínima para falsarla, como especificación pendiente de adjudicación.

### Fuentes usadas

- Continuidad §§12–18, W1-f (recibo + evidencias JSON), manifests W1-b/W1-c/W1-d, `.private-execution/w1g/inputs.json`, fuente Go @ `853c0e4` (`internal/strategy/pocs/sports/sports.go`, `cmd/engine/*`, `internal/transport/marketws`, `internal/experiment`), y documentación pública de Polymarket (docs.polymarket.com; repos oficiales go-order-utils/py-clob-client) vía WebFetch HTTPS.

### Resolución aplicada

- PE-005-R1 elegida por contratos (params congelados 2026-09-21 reutilizados sin ajuste; fee ex ante 0–500 bps dominante documentado; θ con p0=0,50; n=90/≥30 episodios; exploratorio 1–60 vs OOS-nuevo sellado). Fees: ecuación taker `C·rate·p·(1−p)` y categorías VERIFICADAs con URL; exponente/mapeo mbf/tbf/fee_rate_bps del trade NOT_VERIFIED → escenarios etiquetados + gate. Correcciones W1-f (a/b/c) documentadas sin re-ejecutar nada; (c) resuelta como unidades distintas con residuo no conciliado nombrado.

### Validación

- Documental: comandos/flags citados verificados por lectura de fuente (no `--help`); sin ejecución de tests/build/captura (no requerida: no hay fuente nueva); 12 inputs no escritos; hashes medidos sólo sobre artefactos OUT propios.

### Rollback

- Vault: eliminar las 3 notas nuevas W1-g, las secciones de erratas añadidas a las 2 notas W1-f y el bullet (19)/"Siguiente paso" de la continuidad (historia W1-f restaurable del propio marcador). OUT W1-g es aditivo.
