---
type: session
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
  - "[[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]]"
  - "[[Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29]]"
  - "[[Research — Economic Strategy Specification W1-g 2026-10-29]]"
  - "[[2026-10-29-polymarket-engine-entity-updated]]"
aliases: []
confidence: high
source_session: "W1-g one-shot ZCode × GLM-5.3-Flash Max (sess id no expuesta por el perfil del shot)"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-29-polymarket-w1g-economic-preregistration-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- W1-g (mandato Metis tras el cierre TÉCNICO de W1-f): terminar dos entregables sustantivos sin repetir gates/tests/replay/captura — (1) UNA estrategia económica candidata completamente preregistrada y ejecutable por especificación; (2) el paquete de adquisición mínima para falsarla, DISEÑO solamente pendiente adjudicación Metis. Además: correcciones documentales W1-f (a/b/c) e investigación de fees en fuentes primarias públicas.

## Contexto cargado

- Bootstrap Agents-OS (constitución, perfil global `rjara-agent-profile.md`, nota interna global, índice de skills, registro de routers: DEFAULT sin router). Continuidad Five-POC íntegra (§§1–18). Canónicos W1-f. 12 inputs hashes verificados por lectura. Manifests autorizados W1-b/W1-c/W1-d/W1-f. Fuente Go del checkout @ `853c0e4` (HEAD y rama `w0/offline-causal-replay-20261027` confirmados limpios).

## Trabajo realizado

- Contrato original PE-005-R1 verificado en fuente (`internal/strategy/pocs/sports/sports.go`) y distinguido del preregistro nuevo; candidata elegida sin esquivar dificultad.
- Fees investigadas con WebFetch sólo en dominios autorizados: ecuación taker `fee=C·rate·p·(1−p)`, tabla por categorías, changelog (V2 2026-03-30; deportes 0,03→0,05 el 2026-07-10; `feeSchedule` 2026-03-31; CLOB V2 sin `feeRateBps` 2026-04-17), `mbf/tbf`/`fd` de `/clob-markets`, go-order-utils y py-clob-client; NOT_VERIFIED registrados sin URLs inventadas.
- Matriz de aptitud de datos exploratorios por manifests+contratos (sin procesar raw): causas exactas por dataset; ninguno apto hoy para falsar E1.
- PREREG económico completo (algoritmo ejecutable: universo, señal, fee escenarios, entrada/salida, exposición virtual, abstenciones, latencia/stale/empates, censura 02–08, n=90/≥30 episodios, split exploratorio/OOS-nuevo, suficiencia/abandono).
- PLAN de adquisición mínima (comandos reales con flags de fuente; receta por lote; piloto 3 episodios + campaña; volumen 0,24–1,6 GB/ventana vs techo 10 GB; flag propuesto NO existente marcado).
- Correcciones W1-f (a) orden prereg→medición, (b) P1–P7 regresiones técnicas, (c) 74 vs 8+73 unidades distintas con residuo no conciliado nombrado — sin re-ejecutar nada y preservando historia.

## Artifacts creados o modificados

- Vault: 3 notas nuevas (PREREG/PLAN/INFORME W1-g), erratas en 2 notas W1-f, continuidad (bullet 19 + siguiente paso con historia preservada), change_log (sección W1-g), session/feedback/agent_run.
- OUT: `validated-baseline/w1-g-economic-preregistration-20261029/` (copias MD/JSON + recibos con hashes medidos por `sha256sum`).
- Repo: SIN cambios (HEAD `853c0e4` intacto, sin commit/push; no había fuente nueva).

## Memoria propuesta o creada

- Ninguna nueva; el estado vive en las entidades/canónicos del proyecto (constitución: estado en Sistema 2).

## Decisiones

- PE-005-R1-E1 como primera falsación económica; params ex ante = conjunto congelado 2026-09-21 + fee 0–500 bps (domina la fórmula documentada; alternativa 1000 descartada); p0=0,50; ventana [K−90m,K) con re-polls ≤15 min vía re-invocación de `clob observe` (sin código nuevo); exploratorio=episodios 1–60 vs OOS-nuevo sellado; censura 02:00–08:00 GMT-3.

## Pendiente

- Adjudicación Metis del paquete (perfil por-shot de la receta de lote + preregistro de máquina del piloto); después piloto 3 episodios → campaña a suficiencia. Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real. Freeze de producto intacto; live cerrado; tests NOT_RUN (no requeridos: cero código nuevo).
