---
type: session
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
related:
  - "[[Research — Causal Replay Exploratory W1-b 2026-10-28]]"
  - "[[Research — Raw L2 Parquet Recovery 2026-10-27]]"
  - "[[2026-10-27-polymarket-engine-entity-updated]]"
  - "[[2026-10-28-polymarket-w1b-causal-replay-session-feedback]]"
  - "[[2026-10-28-zcode-glm-5.3-flash-polymarket-w1b-causal-replay]]"
aliases: []
confidence: high
source_session: "no verificable desde el modelo en este segmento (consulta de contexto de sesión fuera del scope del gate); atribución final corresponde al lanzador — la parada prematura previa de esta misma sesión quedó registrada por el lanzador con exit130"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-28-polymarket-w1b-causal-replay-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Shot W1-b: replay causal exploratorio offline del cohort MLB (SD 3901945, NYM 3901951, TOR 3901947, SF 3901949; ventana de recepción `[21:10Z, 22:40Z)` del 2026-09-01) sobre los Parquet raw T21/T22 de W1-a, con manifiesto exploratorio pre-registrado, script conforme al hook, doble ejecución comparable, OOS sellado y cierre canónico. Resultado honesto: **ejecución BLOCKED por el gate** (comando exacto denegado) y dependencia pyarrow **BLOCKED** (venv falla por `python3.14-venv` ausente; forma pip denegada); manifiesto y script quedaron materializados; ningún evento fue leído; OOS intacto.

## Contexto cargado

- Bootstrap canónico una vez (constitución, perfil global `rjara-agent-profile`, nota interna global de continuidad, índice de skills); routing manual a la entidad sin Graphify (paths enumerados por el mandato).
- §18 de [[Polymarket Engine — Continuidad Five-POC 2026-09-20]]; [[Research — Raw L2 Parquet Recovery 2026-10-27]]; `w1-a/recovery-manifest.json` + `recovery-exit.json`; [[Research — Historical L2 Forensic Validation 2026-09-21]] y [[Research — Historical Data Acquisition ADDENDUM 2026-09-21]]; registros W1-a (summary, feedback, agent_run, change_log).
- Grounding de engine por lectura: manifiestos T21/T22 del paquete W1-a (esquema, row groups por producto, columna `market`), `internal/histimport/anchor_test.go`, `cmd/engine/experiment.go`. `testdata/research-master/certificate.json` fue leído en el segmento prematuro previo a la interrupción: clasificado por verificación scoped como artefacto técnico M4 no-live (generador `internal/experiment/certify.go`; CLI `runCertify`), sin exposición OOS; no se usa como evidencia W1-b y la parada se preserva con su `exit130` registrado, sin PASS retroactivo.

## Trabajo realizado

- Bootstrap y lectura de continuidad; corrección de la explicación falsa W1-a sobre el hook (ver Decisiones) en los cinco registros pertinentes.
- Creación de `validated-baseline/w1-b/exploratory-manifest.json` (pre-registrado antes de cualquier lectura de eventos): scope cohort + exclusión OOS sellada, ventana µs, mapeo identificación-primero, protocolo OOS (nunca seleccionada/contada/hasheada/persistida; row groups mixtos enmascarados pre-observación), upsert + orden venue-ms con empates marcados, cortes negativos 21:40/22:10/22:30Z, guardas RSS ≤2 GiB y lotes ≤25000, protocolo de doble ejecución con digests deterministas, y estado de dependencia registrado como riesgo.
- Escritura de `validated-baseline/w1-b/run_w1b_replay.py` (~14k caracteres): imports sólo de la lista permitida; sin `open`/`eval`/`exec`/`compile`/`getattr`/`setattr` ni import dinámico; ambos raw paths, hashes, IDs cohort/OOS y ventana exactos; `iter_batches` con poda por estadísticas de `market`; contadores cohort y agregado único para "otros"; hashes de fila; reconstrucción upsert por asset con validación por snapshot y doble BBO; cortes con digests; salidas numeradas idempotentes.
- Sondeos de dependencia documentados sin bucles: `python3 -m venv <w1-b>/.venv` (forma autorizada) pasó el gate y falló a nivel OS dos veces (`ensurepip is not available`; falta `python3.14-venv`); forma pip autorizada denegada por el gate (forma exacta una vez por segmento; además una única variante `--only-binary` denegada en el segmento previo: tres denegaciones pip en total); comando exacto de replay denegado una vez — sin reintentos ni alternativas, según mandato.
- Closeout canónico: este resumen, feedback, agent_run, doc W1-b, actualización de §18 y del change_log existente; re-lectura de verificación al cierre.
- **Actualización 2026-10-28 — recuperación del entorno y ejecución real (segmento posterior, misma sesión):** el auxiliar del lanzador preparó el venv con `--without-pip` + wheels oficiales offline `pip 26.0.1`/`pyarrow==26.0.0` (SHA publicados verificados por el auxiliar; procedencia en `/home/kor/Documents/Codex/2026-10-27/task-2/.private-execution/w0/dependency-wheels`, rutas no relacionadas no leídas) y el hook pasó el comando exacto con marcadores SÓLO para el SHA256 del runner `2cce3e49…` (sin editar el script). Dos ejecuciones reales en primer plano (02:22:47Z y 02:23:56Z): integridad de ambos raw revalidada in-run dos veces (SHA-256 completos = publicados; RSS pico ≤2 GiB; manifest v1 SHA `87e8dbb6…` registrado) y fallo cerrado por prerrequisito semántico pre-registrado: `timestamp_received` no es entero-µs sino tipo timestamp en el Parquet físico; `num_rows` y `num_row_groups` (311/210) coincidieron antes del corte. Cero eventos leídos; OOS intacto; segunda corrida idéntica (fallo determinista). Quirk observado: la numeración de corridas depende del output que sólo se escribe en PASS, así que la segunda sobrescribió `w1b-run-manifest-run1.json` (que se preserva intacto desde entonces).
- **Actualización 2026-10-28 (2) — reparación v2 materializada y denegada por el gate:** conforme a la nota de recuperación (bug reparable), esta sesión materializó `exploratory-manifest.json` v2 (`w1b-2`: schema real antes de supuesto, timestamps Arrow con aritmética entera exacta y supuesto naive-UTC registrado, columnas requeridas y mapeo validados antes del recorrido, chequeos de borde ventana/corte, run IDs únicos e inmutables incluso en fallo, IDs cohort e ISO boundaries literales, procedencia corregida) y `run_w1b_replay.py` v2 (~19k caracteres, mismas restricciones). La ejecución del comando exacto con fuente v2 fue denegada por el gate (un único intento): la acomodación de marcadores existe sólo para el SHA v1 y el hook no puede ser modificado por esta superficie — impedimento de permisos diagnósticado, terminal para este segmento según mandato. Re-ejecutar v1 habría sobrescrito evidencia preservada: no se hizo.

## Artifacts creados o modificados

- `validated-baseline/w1-b/exploratory-manifest.json` (creado) y `validated-baseline/w1-b/run_w1b_replay.py` (creado, nunca ejecutado); `.venv/` parcial creado por el comando venv autorizado (sin pip, sin pyarrow).
- `10-projects/Personal/Polymarket Engine/Research — Causal Replay Exploratory W1-b 2026-10-28.md` (creado).
- `80-agents/journal/sessions/2026-10-28-polymarket-w1b-causal-replay-summary.md` (esta nota), `80-agents/journal/feedback/system-1/2026-10-28-polymarket-w1b-causal-replay-session-feedback.md`, `80-agents/journal/agent-runs/2026-10-28-zcode-glm-5.3-flash-polymarket-w1b-causal-replay.md` (creados).
- `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (§18: subsección W1-b + corrección fechada de la explicación del hook; §§1–17 intactas) y `80-agents/journal/logs/2026-10-27-polymarket-engine-entity-updated.md` (sección datada W1-b).
- Correcciones fechadas en registros W1-a: [[Research — Raw L2 Parquet Recovery 2026-10-27]], [[2026-10-27-polymarket-w1a-raw-recovery-summary]], [[2026-10-27-polymarket-w1a-raw-recovery-session-feedback]], [[2026-10-27-zcode-glm-5.3-flash-polymarket-w1a-raw-recovery]].
- Checkout engine y `validated-baseline/w0`, `w1-a` intactos (sólo lectura).

## Memoria propuesta o creada

- Ninguna L3 nueva; el delta de estado quedó en §18, en el doc W1-b y en el change_log. Pain pattern vigente (gate con mensajes sin causa y allowlist incompleta en one-shots) actualizado en el feedback, sin promoción (defer al hygiene cycle junto a los feedbacks W0/W1-a).

## Decisiones

- Cierre BLOCKED honesto por pieza: manifiesto y script PASS como artefactos; venv BLOCKED (OS); pyarrow BLOCKED (gate); replay y doble ejecución NOT_RUN con causa; footer y revalidación in-run NOT_RUN (dependían del script); harness Go NOT_RUN pre-registrado (sin forma autorizada); sin fabricar ningún resultado.
- Corrección W1-a aplicada con historia preservada: la explicación «el hook sólo aceptó `run_in_background:true`» era falsa — un preflight del hook a un runner inexistente dio ALLOW en foreground; el source inicial fue denegado por imports/markers y longitud (>32000); la variante compacta foreground también obtenía ALLOW; las llamadas GLM posteriores usaron background por elección. Causa observada: validación de source y formas de comando no registradas, con mensaje genérico que no revela la regla; método futuro: preflight real de forma+fuente antes de afirmar reglas.
- Un único intento del comando exacto de replay y ningún loop de permisos (instrucción explícita del mandato).
- Atribución: todo el trabajo de este segmento = ZCode × account:zai-individual-coding-plan/GLM-5.3-Flash; la parada prematura previa de la misma sesión quedó registrada por el lanzador (exit130) y no se reclama PASS retroactivo.

## Pendiente

- (Actualizado 2026-10-28 tras la reparación v2) El lanzador debe preflight-registry la fuente v2 del runner (nuevo SHA con la acomodación de marcadores, o publicar los marcadores exigidos junto al mandato) y re-despachar; runner v2 y manifiesto v2 (`w1b-2`) ya están conformes por construcción y listos para la doble corrida comparable con run IDs únicos e inmutables. El supuesto de esquema ya está corregido en ambos (timestamp Arrow con conversión entera exacta).
- Tras la re-ejecución: doble corrida comparable (digests idénticos), validación BBO por snapshot, cortes negativos y ventana de incidente 22:30–22:40Z censurada; después, elección de como máximo dos hipótesis (gate humano).
- `rs-v03`/`pe001` y el mapeo de `hist-acq-20260921` siguen sin evidencia de recuperación.
- Sin sync/publicación: todo local; elegibilidad/cuenta/fondos/riesgo/arming/live siguen cerrados.
