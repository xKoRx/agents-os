---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-16
updated: 2026-09-16
tags:
  - kind/doc
  - tech/polymarket
---
# Polymarket resources — Log

## [2026-09-16] ingest | Cuatro Deep Research aportados por el owner → [[Polymarket — Edge Research Consolidado 2026-09-16]], cuatro source notes y [[polymarket/00-index|índice de dominio]]

- Fuentes R1–R4 identificadas por IDs de attachment, títulos originales, tamaño y SHA-256; originales completos no duplicados en este repo.
- Se unifican 58 formulaciones nominales en 30 hipótesis/familias deduplicadas PE-001…PE-030. No se declara ninguna rentable por el solo research.
- Contradicciones visibles: Sports fees/rebates, FLB en Sports, oracle bonds/settlement, retornos de wallets y estimaciones de fill.
- Documentación oficial parcial consultada; fuentes académicas individuales no auditadas exhaustivamente.

## [2026-09-16] ingest | Reframing proyecto → [[Polymarket Engine — MVP]] y preparación M0 Technical Knowledge Pack

- Autoridad canónica cambia de `Polymarket Arbitrage — MVP` a [[Polymarket Engine — MVP]].
- Distinción frozen: **Engine = MVP durable; Strategies = POCs descartables/promovibles**.
- Engine: Go, modular monolith, strategy-agnostic pero Polymarket-specific, una máquina grande inicialmente.
- NegRisk y Sports pasan a POC-S01/POC-S02, primeros consumidores del engine.
- Próxima ingesta del dominio: `Polymarket — Technical Platform Map — synced YYYY-MM-DD`, basado prioritariamente en documentación oficial, `llms.txt`, OpenAPI/AsyncAPI, changelog, contracts y SDK docs.
- Astra/Fable deben recibir ese knowledge pack preparado y no gastar sus ventanas en descubrir endpoints básicos.
- Workflow de diseño/implementación: `Astra proposal → Fable challenge → Astra reconcile → TOP implementation plan → NORMAL implementation` con autoridad documental concentrada en el único archivo del proyecto.
- Pendiente lint/Graphify desde entorno local; Graphify sigue siendo índice derivado.
