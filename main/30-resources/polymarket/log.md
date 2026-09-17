---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-16
updated: 2026-09-17
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

## [2026-09-17] intake | Technical Platform Map guardado íntegro en Biblioteca; ficha GitHub y enlace al proyecto

- El original del owner `Polymarket — Technical Platform Map — synced 2026-09-17` está preservado **sin editar** en Biblioteca `/Polymarket Engine/Resources/Polymarket — Technical Platform Map — synced 2026-09-17.md`.
- Identidad: `160165` bytes; SHA-256 `78e6506fa67aa12843ba4acb0e4c8271a83c1841432a4a53777c73c4c723c11f`.
- Se crea [[Polymarket — Technical Platform Map — Intake 2026-09-17]] en GitHub y `Research — Technical Platform Map M0.md` en la carpeta del proyecto; el índice enlaza ambos. **Importante: el Markdown íntegro no está todavía en GitHub** porque el conector de escritura utilizado no recibe directamente bytes de adjuntos locales.
- El documento original admite certificación contractual pendiente, siete gaps RG-01…RG-07 y bloqueo de conversión NegRisk Protocol-v2 live sin ABI/ruta verificadas.
- Siguiente agente: conseguir el archivo íntegro, verificar SHA, incorporarlo en `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`, commit sin edición, luego corregir in-place por RG y commits incrementales. No regenerar 160 KB de memoria ni declarar falsamente que se ingirió completo.
- M0 no certificado; diseño Astra/Fable sólo cuando los blockers contractuales relevantes queden cerrados o explícitamente acotados con criterios de seguridad.
