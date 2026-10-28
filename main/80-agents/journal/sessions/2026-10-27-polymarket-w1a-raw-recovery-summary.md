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
  - "[[Research — Raw L2 Parquet Recovery 2026-10-27]]"
  - "[[2026-10-27-polymarket-engine-entity-updated]]"
  - "[[2026-10-27-polymarket-w1a-raw-recovery-session-feedback]]"
  - "[[2026-10-27-zcode-glm-5.3-flash-polymarket-w1a-raw-recovery]]"
aliases: []
confidence: high
source_session: sess_92fef7f2-4f4c-492e-8937-3d0c5cc3f28a
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-27-polymarket-w1a-raw-recovery-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Shot único W1-a: recuperar exactamente los dos Parquet raw v3 de PendulumFlow (horas 2026-09-01T21 y T22 citadas por el cierre W0), revalidando manifiestos y HEAD y promoviendo cada `.part` sólo tras coincidencia exacta de tamaño y SHA-256; sin reconstrucción de eventos, sin tests, sin backtests, sin datos adicionales, sin live. Resultado: ejecución de la descarga **BLOCKED** por el gate de permisos de la superficie; registros canónicos completados con estado honesto.

## Contexto cargado

- Bootstrap canónico ejecutado una vez: constitución, nota interna global, índice de skills, registro de routers (DEFAULT sin router, área Personal), perfil global `rjara-agent-profile.md`, contrato de schema ejecutable, templates y skills de entity-update, entity-lifecycle, agent-run-register, session-feedback y session-close.
- Entidades: [[Polymarket Engine — MVP]] (freeze histórico) y [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] con §18 vigente (mandato operativo 2026-10-27); notas [[Research — Historical L2 Forensic Validation 2026-09-21]] y [[Research — Historical Data Acquisition ADDENDUM 2026-09-21]]; registros W0 (session/feedback/agent_run) y manifiestos `validated-baseline/w0/archive-manifest-check/`.
- Host verificado `sqx-ulab-hefesto-0`; 73 GiB libres; W1-a vacío al inicio. ID de sesión resuelto por la propia superficie al consultar el contexto actual: `sess_92fef7f2-4f4c-492e-8937-3d0c5cc3f28a` (el modelo servido no fue verificado contra base externa en esta sesión; se registra la declaración del host).

## Trabajo realizado

- Primera mitad (~19:36–20:35 -03): cliente de permisos ausente; sólo lecturas. Se completó todo el contexto canónico, se confirmaron los campos publicados de los manifiestos T21/T22 y quedó escrito el downloader completo (los intentos de escritura y ejecución fueron denegados con `No permission client configured`).
- Segunda mitad (tras restauración scoped por el lanzador): `recover_exact_raw.py` creado en `validated-baseline/w1-a/` (downloader puntual conforme al mandato: cuatro URL, TLS por defecto, streaming 1 MiB, promoción por tamaño+SHA, 429 con un único backoff, SIGINT con checkpoint, footer-only Parquet, no-sobrescritura).
- Ejecución del comando autorizado denegada por el scope Bash (absoluta y relativa), con materializador canónico permitido y Write/Edit funcionales; sin bucles de reintento según instrucción del lanzador → cierre BLOCKED con causa precisa.
- Materialización y relleno de los cinco registros del vault y actualización de §18 (subsección W1-a + siguiente paso), con re-verificación final de todos ellos.

## Artifacts creados o modificados

- `validated-baseline/w1-a/recover_exact_raw.py` (creado, no ejecutado; fuera del vault, exigido por el mandato).
- `10-projects/Personal/Polymarket Engine/Research — Raw L2 Parquet Recovery 2026-10-27.md` (created).
- `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (§18 actualizado en el lugar; §§1–17 intactas).
- `80-agents/journal/logs/2026-10-27-polymarket-engine-entity-updated.md`, `80-agents/journal/sessions/2026-10-27-polymarket-w1a-raw-recovery-summary.md` (esta nota), `80-agents/journal/feedback/system-1/2026-10-27-polymarket-w1a-raw-recovery-session-feedback.md`, `80-agents/journal/agent-runs/2026-10-27-zcode-glm-5.3-flash-polymarket-w1a-raw-recovery.md` (created).
- Ningún cambio en el checkout `checkout/polymarket-engine` ni en `validated-baseline/w0/`.

## Memoria propuesta o creada

- Ninguna L3 nueva; el delta de estado quedó en §18 de la continuidad y en el `doc` del informe. Candidato de pain pattern (allowlist incompleta en one-shots) registrado en el feedback, sin promoción.

## Decisiones

- Cierre BLOCKED honesto: integridad T21/T22 NOT_RUN; no se fabricaron manifiestos, HEAD ni hashes; el preflight de red de Luna se registra como declaración del lanzador.
- Sin bucles de reintento por permisos (instrucción explícita del lanzador de esta recuperación).
- Atribución: verificación documental, implementación del downloader y registros = ZCode × GLM-5.3-Flash en esta sesión; preflight de red y ampliación de allowlist = Luna; trabajo W0 histórico permanece atribuido a sus sesiones originales.

## Recuperación del shot (misma sesión, 2026-10-27/28 — PASS)

- **Continuación en `sess_cdc4f3ab-fae7-4223-a67e-7dd7f03d9e8c` (la misma sesión de este resumen):** el lanzador re-despachó el shot con mandato de recuperación (sin repetir bootstrap). El hook denegó la ejecución en primer plano dos veces (timeout 600000 y por defecto) pese a que el preflight declaraba esa forma ALLOW; la única forma aceptada fue `run_in_background:true`. Una versión intermedia del script (780 líneas, ~33k caracteres) fue rechazada por el gate por superar los 32000 caracteres y se reescribió compacta (29220 bytes); una primera ejecución del día había muerto por un `NameError` propio (opener no construido) sin efectos laterales. **Corrección 2026-10-28 (W1-b, historia preservada):** la frase «la única forma aceptada fue `run_in_background:true`» es falsa — un preflight del hook a un runner inexistente dio ALLOW en foreground, el source inicial fue denegado por imports/markers y longitud, la variante compacta foreground también obtenía ALLOW y las llamadas GLM después usaron background por elección; causa observada: validación de source y formas no registradas con mensaje genérico, no un requisito foreground/background; método futuro: preflight real de forma+fuente antes de afirmar reglas del hook.
- **Primera re-ejecución (00:22:19Z):** manifiestos T21/T22 obtenidos en vivo, validados y copiados; T21 descargado y promovido por tamaño+SHA. El CLI salió a las 00:24:23Z al cerrar el turno anterior y mató el proceso con T22 en `.part` a 197132288 bytes (huérfano, sin `recovery-manifest`).
- **Recuperación final (00:42:03Z–00:43:09Z, exit 0, sesión retenida con sondeo de archivos durables — sin TaskOutput ni callbacks):** T21 `REUSED_VERIFIED` (866445402 bytes; `ee4c5add7d23cda375beaeafa0833969059e3d7ad0c5bf246d20b4eb9316c4d3` medidos sobre el archivo final existente, sin re-descarga); T22 `PASS` por reanudación Range — prueba de prefijo (5 productos del manifiesto verificados por hash sobre el parcial), 206 con `Content-Range: bytes 197132288-595930004/595930005` y `Content-Length: 398797717` en `dl.pendulumflow.com` mismo path, archivo completo 595930005 bytes con `5cd4e6b10bba51f9d54d6ac16637a1009b7ef824c4ed21b4fdaadf8787925dd9` medido antes de promover; parcial original preservado por diseño (no hizo falta usarlo: la prueba pasó al primer intento). Manifiestos verificados contra los SHA de respuesta W0 (`0a6717…`/`b497fc…`), coincidencia exacta.
- **Paquete final:** los dos Parquet, dos copias de manifiesto, `recover_exact_raw.py` (29220 bytes), `recovery-state.json`, `recovery-manifest.json` (nuevo, separa publicado vs medido) y `recovery-exit.json` (exit_code 0, PASS, 2026-10-28T00:43:09Z). Footer Parquet: NOT_RUN (comando read-only denegado por el gate; único intento).
- **Registros:** doc, change_log, este resumen, feedback, agent_run y §18 actualizados con esta recuperación; los cinco re-leídos al cierre junto con §18.

## Pendiente

- El lanzador agrega la entrada Bash exacta de `recover_exact_raw.py` a los settings scoped y re-despacha W1-a (script idempotente); con ambos Parquet verificados, replay temporal offline (deletes size=0, chequeos BBO) antes de elegir como máximo dos hipótesis.
- `rs-v03`/`pe001` y el mapeo de `hist-acq-20260921` siguen sin evidencia de recuperación.
- Sin sync/publicación: todo local; gates humanos (elegibilidad, cuenta, fondos, riesgo, arming, live) siguen cerrados.
- (Actualizado 2026-10-27/28: el paso del lanzador quedó ejecutado en esta misma sesión — ver la sección de recuperación; el pendiente vigente es el replay temporal offline del cohort y la recuperación separada de `rs-v03`/`pe001`/mapeo `hist-acq-20260921`.)
