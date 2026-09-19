---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: run
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-09-19-zcode-glm-research-data-unblock-v02

## Trabajo

- **Objetivo:** mandato RESEARCH DATA UNBLOCK v0.2 — preservar la evidencia real de v0.1, desbloquear los datos que dejaron la capa real en `DATA_BLOCKED` (constraints fuera del techo offset≤2000 de Gamma, exhaustividad NegRisk no verificable, kickoff Sports sin contrato) y reejecutar las POCs preregistradas sin modificar hipótesis. Baseline `0d6a635`, branch `feature/research-strategies-v01`, sin push, LIVE_DISABLED.
- **Fase A (`54b68b7`):** bundle persistente del journal real v0.1 en `~/go/src/github.com/xKoRx/polymarket-engine-datasets/rs-v01/` (15 archivos, SHA-256 por archivo, manifiesto con clasificación/retención/referencias copiado en `testdata/research-v02/rs-v01-bundle-manifest.json`); verificación física: `journal verify` sobre la copia (frontier 941, sin holes), replay con digest `5a5bb186…` idéntico al comprometido en ambos schedules, originales intactos por `diff -r`. Erratum declarado: el manifest_id citado en EVIDENCE.md v0.1 (`4196186e…`) no coincide con el artefacto comprometido (`ac9e2858…`). Matriz de identidades NegRisk 30829 + Sports en `testdata/research-v02/IDENTITIES.md` con clasificación NOT_OBSERVED/UNKNOWN/OBSERVED_LIVE_ONLY.
- **Fase B (`d9fab99`):** B1 — flag `catalog sync --id` (el filtro documentado `id=` ya existía en `CatalogFilter`/`gamma.Query`); sync dirigido real del evento 30829: 1 request → 129 entidades (1 evento + 128 mercados), relaciones `neg_risk_membership`/`containment`/`complement` VERIFIED ×128 contra el contexto `0x2c3d…4700`, constraints de régimen OBSERVED (tick 0.001, min_size 5, fees 1000 bps — el bloqueo exacto de v0.1 resuelto), idempotencia verificada. B2 — contrato keyset demostrado contra el wire (envelope `{$schema,items,next_cursor}`, terminación null, clamp limit≤100, cursor inválido 422 definitivo, reinicio silencioso ante cambio de cohort) + adapter mínimo en ownership (gamma transporte, `protocol.ParseGammaKeyset{Events,Markets}` con kinds nuevos y fixtures versionadas de envelope; walk driver declarado fuera de alcance). B3 — `EvaluateExhaustiveness` en negrisk: prueba explícita que combina estructura/relaciones/Other/placeholders/reglas-payout documentadas/conjunto de resultados; demostrada sobre el hermano resuelto 903193 (17 mercados, exactamente un YES ⇒ VERIFIED); 30829 clasificado `EXHAUSTIVENESS_UNKNOWN` con evidencia faltante exacta (`getQuestionCount` on-chain o resultados propios). B4 — kickoff verificado: `gameStartTime` == `event.startTime` en eventos en vivo Y futuros (kickoff conocido 2 semanas antes), `startDate` rechazado como editorial; `gameStartTime`+`sportsMarketType` ahora se parsean en protocol y se proyectan en el contenido del catálogo.
- **Fase C (`e1134f1`):** canal canónico `catalog emit-params` (deriva los params de las POCs desde Catalog/Regimes por interfaces públicas: assets YES, membresía, veredicto de exhaustividad, fee interval, kickoff; params estadísticos viajan preregistrados como flags). Hallazgo material del canal: el mercado 559779 "Will another person win…" del evento 30829 declara `negRiskOther=true` (mercado Other en el conjunto — contradice la narración de v0.1 a nivel evento) ⇒ estructura aumentada ⇒ inelegible por semántica mutable preregistrada. Corrección por ownership (books, S06): el segundo `record` sobre el mismo data dir fallaba con regresión de cursor por asset; `books.Drain` ahora testifica `max(almacenado, replayed)` con test de regresión; el primitivo frozen `persist.AdvanceCursor` queda intacto. Runs reales: NegRisk SCREEN 2 sets/2 REJECT `EXHAUSTIVENESS_UNSUPPORTED_STRUCTURE`, REPLAY digest `b24982b0…` idéntico en {1} y {32,7,1} (manifest `a67f2b10…`, cutoff 1074), SHADOW 50 evals/50 REJECT/INCONCLUSIVE con denominadores honestos; Sports (moneyline 4734898, kickoff verificado desde catálogo) SCREEN 6 cortes/0 oportunidades (libro pre-match tranquilo), REPLAY determinista, SHADOW INCONCLUSIVE con requisito de muestra documentado exacto. Extensión de vocabulario: `exhaustiveness=UNSUPPORTED` aceptado por la POC (rechazo estructural `EXHAUSTIVENESS_UNSUPPORTED_STRUCTURE` en vez de launder a UNKNOWN).

## Verificación

- Regresión completa: build/vet/test/race (el suite race completo mostró un flake preexistente de cancelación en catalog bajo carga paralela; el paquete en aislamiento con -race pasó 2/2), tidy sin diff, diff-check limpio en cada checkpoint.
- Cobertura (denominador tests-propios, atomic): protocol 96.3, gamma 96.6, books 98.4, negrisk 95.3 ≥ piso; cmd/engine 94.4% — residuo ~14 statements `DEFENSIVE_FAULT_GUARD` (fallos de store/cursor-snapshot y render residual no alcanzables por CLI) clasificado como excepción técnica declarada pendiente de owner, mismo mecanismo que la excepción de M2-S03.
- Certificación: `engine experiment certify --repo-root . --baseline <SHA>` → `M4_CERTIFIED_NON_LIVE` 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 diferidos live en `e1134f1` y re-pineado en el árbol final; un pin con SHA corto devolvió correctamente `M4_STALE_CERTIFICATION`. LIVE_DISABLED intacto (gates live diferidos NOT_RUN por diseño).
- Verificación física de datos: syncs y records reales contra Gamma/CLOB WS read-only; outputs commiteados en `testdata/research-v02/`.

## Rework

- Intra-sesión: bug off-by-one propio en el fixture de test del filtro `id`; separador de fee en emit-params (coma → `;`); detección de lado YES en moneylines de equipos (fallback al outcome canónico 0); aserción de cohort en el test keyset. Sin rework del owner.

## Estado

- Gates `DATA_A_PASS` (54b68b7), `DATA_B_PASS` (d9fab99), Fase C ejecutada (e1134f1); certificado en árbol final (7bd264d). Resultado global `RS_V02_PARTIAL_DATA`: capa de datos desbloqueada y demostrada extremo a extremo; NegRisk `INCONCLUSIVE` por estructura (Other presente + exhaustividad no demostrable pre-resolución, con la evidencia faltante nombrada exactamente); Sports `INCONCLUSIVE` por muestra insuficiente con requisito de captura documentado. Conversión NegRisk DISABLED; sin órdenes; sin push.
