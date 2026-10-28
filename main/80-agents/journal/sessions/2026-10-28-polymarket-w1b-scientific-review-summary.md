---
type: session
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
related:
  - "[[Research — Causal Replay Exploratory W1-b 2026-10-28]]"
  - "[[2026-10-28-polymarket-w1b-causal-replay-summary]]"
  - "[[2026-10-27-polymarket-engine-entity-updated]]"
  - "[[2026-10-28-polymarket-w1b-scientific-review-session-feedback]]"
  - "[[2026-10-28-zcode-glm-5.3-flash-polymarket-w1b-scientific-review]]"
aliases: []
confidence: high
source_session: "sess_d49dc6df-339a-4f88-9be1-6de0c4c43a85"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-10-28-polymarket-w1b-scientific-review-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Sesión NUEVA de revisión científica del W1-b ya terminado (sin re-ejecutar replay, sin re-descargar raw, OOS sellado intacto): contrastar A′/B′ con manifests y source-pin, definir exactamente fill y fee conocida, validar la ausencia de ticks de fee, inspeccionar tests de cortes y añadir sintéticos si faltaban, decidir hipótesis (máximo dos o descarte), roadmap corto, y rectificación canónica del informe W1-b, §18, change_log, summary, feedback y agent_run. Estado de cierre: **PARTIAL (revisión completa; ejecución de la suite sintética NOT_RUN por gate; hashing local NOT_RUN por gate)**.

## Contexto cargado

- Bootstrap canónico una vez (constitución, perfil global `rjara-agent-profile`, nota interna global de continuidad, registro de dominio → DEFAULT sin router); lectura de `skills/INDEX.md` denegada por el gate (retrieval degradado, skills cargadas por rutas directas: session-close).
- §18 de [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] (con Updates 1–5 del W1-b) y [[Research — Causal Replay Exploratory W1-b 2026-10-28]] previo a la rectificación.

## Trabajo realizado

- Preflight: `hostname` = `sqx-ulab-hefesto-0` verificado; branch `w0/offline-causal-replay-20261027` @ `09e8c76` y árbol limpio corroborados SOLO por el snapshot del entorno anfitrión (git denegado por el gate); recursos y hashing criptográfico NOT_RUN (denegados); inventario del paquete reconstruido por referencias cruzadas + Read (`ls` del paquete denegado).
- Contraste A′/B′ CONFIRMADO comparable: cores `w1b-replay-20261028T042313Z-a.json` / `…T043738Z-a.json` idénticos línea a línea en lectura completa (803 líneas; consistente con el SHA común `b75f50ee…` declarado; re-hasheo local NOT_RUN), mismos inputs en ambos run manifests stage3 (fixture `3c843b22…`, manifiesto `5e8c171b…`, identidad w1b5 `f64b9391…`, runner self-label «v7», `protocol: w1b-7`), ejecuciones independientes `20261028T112001Z`/`20261028T112104Z`, digest común `f56adf46…`, stage1 determinista en 3 corridas (A/B/C), row-group accounting exacto 10/10, provisional `42189d39…` preservado con su manifest.
- Salvedades de procedencia NUEVAS: (1) el `run_w1b_replay.py` actual en disco NO son los bytes que produjeron A′/B′ (fixture de todas las corridas con token TOR pre-w1b6 `…6206585…`; el archivo actual trae el corregido w1b6 `…538631385…` y su gate interno de identidad fallaría contra `mapping-revision-w1b5.json` → paquete no re-ejecutable tal cual; fix de una línea `IDENTITY_REVISION_PATH → w1b6` pendiente); (2) el digest canónico depende de las etiquetas del fixture w1b5 (`3901947/hex:ee67ddb7…`) → una re-corrida w1b6 daría OTRO digest con datos idénticos; bytes del código productor no preservados como copia nominada; (3) inconsistencia cosmética `protocol` core `w1b-5` vs manifest `w1b-7`; (4) existe stage1 C posterior al cierre (`20261028T113251Z`) que dejó `w1b-current-group.json` en `stage1_done` — paquete en vuelo, no «grupo B complete».
- Semántica exacta fill/fee definida desde el código: «256 fills» = filas `last_trade_price` observadas del feed (trades de terceros; NO fills simulados del engine — `engine_go_harness` NOT_RUN en todos los manifests — ni órdenes propias, que no existen); «fee conocida» = `fee_rate_bps` no-NULL (0/256 unknown; valores NO registrados en el core; tasa NO certificada; discrepancia WS 0 vs CLOB 1000 bps de S02 E2 sin resolver).
- Denominadores recalculados cohort-wide sobre los cores: BBO embebido 41.768 agree / 334 mismatch = 99,2% (99,8% era la cifra de SD; NYM 97,9%); traza BBA 2 mismatches (SF, NYM), 0 en censurados; intervalos 303 exactos / 11 divergentes / 68 censurados de 327; 72/256 trades en la ventana censurada del incidente 22:30–22:40Z (reportada aparte, no oculta); 0 duplicados; ticks cohort en ventana = 0 con row groups de tick examinados (considered 1+1) y 4.312 ticks ajenos en contador agregado.
- Bordes: 0 eventos reales exactamente en bordes de ventana/cortes y 0 late arrivals → semántica de frontera implementada (start inclusivo, end/corte exclusivo — verificada por lectura del código) pero NO demostrada por datos. Tests existentes del engine (`internal/histimport/anchor_test.go`) cubren orden de tick/orden de archivo, no cortes; el runner no tiene tests.
- Suite sintética creada: `validated-baseline/w1-b/tests-synthetic/test_w1b_cut_boundaries-rev1-20261028.py` (9 grupos contra funciones reales del runner sin modificarlo); ejecución DENEGADA por el gate (1 intento, forma de lanzador con guardas ≤2 GiB / CPU 120 s) → **NOT_RUN** con comando documentado.
- Hipótesis: **0 admisibles** — descarte razonado (sin señales/economía en el replay; universo identidad CURRENT no PIT; tick PIT ausente — ticks del cohort = 2026-09-02; muestra de conveniencia 2h×4 mercados pre-elegidos en W0; fee sin certificar). Sin edge inventado; evidencia mínima faltante registrada en §18.
- Rectificación canónica: doc W1-b (párrafo vigente en Propósito + 4 marcadores [HISTORIA SUPERSEDED] + bullet (7)); §18 (bullet (6) + párrafo vigente de «Siguiente paso» con el previo preservado como [HISTORIA]); change_log sección (7) con declaración vieja→nueva y rollback; este summary, feedback y agent_run.

## Artifacts creados o modificados

- Vault: doc W1-b, continuidad §18, `80-agents/journal/logs/2026-10-27-polymarket-engine-entity-updated.md` (sección (7)), este summary, feedback y agent_run (frontmatter escrito a mano por gate — desviación documentada en el change_log).
- Paquete W1-b: `tests-synthetic/test_w1b_cut_boundaries-rev1-20261028.py` (creado, NOT_RUN). NINGÚN archivo preexistente del paquete modificado; raw inmutable; OOS intacto; sin jobs huérfanos (nada se lanzó en background).

## Decisiones

- No derivar PASS desde labels: la pareja A′/B′ se confirmó leyendo cores+manifests, no aceptando el rótulo «PASS».
- Preservación estricta: los textos obsoletos («BLOCKED», «nunca ejecutado», «grupo B complete») quedaron marcados como historia superseded, sin borrar ni reescribir el registro cronológico.
- Hipótesis: descarte en vez de invención; la unidad experimental y el preregistro quedan como requisito para datos futuros, no como afirmación sobre los datos actuales.
- Denegaciones del gate: sin reintentos ni alternativas (1 intento por forma); cada denegación documentada con comando/target/razón y su pieza marcada NOT_RUN.

## Pendiente

- **Actualización 2026-10-28 — segmento 2 (misma sesión, mandato integrado de reanudación): ingeniería w1b8 COMPLETADA.** Divergencia mapping/runner/manifest resuelta con el paquete versionado `validated-baseline/w1-b/pkg-w1b8/` (código congelado `1d3e3c25…` verificado por el propio runner en cada arranque; identidad cargada desde snapshot pinneado w1b6 `5049acf1…` con corroboración decimal/hex — etiqueta oficial `3901947:TOR` confirmada contra bytes de datos; manifiesto pineado `5e8c171b…`; puntero del grupo C preservado verbatim en copia y en `prior_pointer_preserved` del stage1-D, sin completarlo). Suite sintética EJECUTADA (comando exacto autorizado): **50 checks ALL_PASS, exit 0**, con 4 detecciones de mutación controlada y restauración (outcome exacto en `pkg-w1b8/tests-synthetic-outcome.md`; 5 defectos ordinarios del fixture corregidos en sesión). **Doble corrida nueva comparable: grupos D (`20261028T123826Z`) y E (`20261028T125105Z`), tres etapas cada uno, digests D=E=`2e3830baa38ef4b04d096223808157d1480bbc6749d5588b7f3440c4be134783`, cores byte-idénticos `092de56a…`, RSS ≤2 GiB**; `f56adf46…` queda como registro histórico canónico de A′/B′ bajo fixture w1b5 (no es el digest esperado bajo w1b8 por etiquetas+protocolo; contadores idénticos). Verificación criptográfica de la revisión completada (A′=B′ `b75f50ee…` medido; `b9f498e7…` y w1b5/w1b6 medidos). Fees: documentación docs.polymarket.com RECIBIDA del auxiliar (WebFetch denegado, 1 intento); describe CURRENT/2026, no certifica fee/tick del 2026-09-01. Corrección de atribución: prerequisitos técnicos PIT = tareas del agente (plan prospectivo propuesto y NO iniciado); Owner sólo decisiones críticas. Stage2 en background supervisado hasta exit por tope foreground 600 s; sin huérfanos. Cambios de estado de agente pendientes tras w1b8: ninguna acción automática; el resultado técnico queda validado con estrategia bloqueada por datos.
- Lanzador: nada pendiente obligatorio de w1b8; si se quisiera completar el grupo C bajo identidad w1b6, crear cadena nueva (nuevo freeze), nunca edición in-place.
- Owner: sólo decisiones críticas de cuenta/elegibilidad/fondos/riesgo/activación real; sin exigencia de rentabilidad para cerrar.
- `rs-v03`/`pe001` y el mapeo de `hist-acq-20260921` siguen sin evidencia de recuperación; elegibilidad/cuenta/fondos/riesgo/arming/live siguen cerrados (freeze de producto vigente).
