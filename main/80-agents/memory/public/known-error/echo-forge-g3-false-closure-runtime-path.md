---
type: known_error
scope: project
created: 2026-07-26
updated: 2026-07-26
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge - Cierre de Etapa 4]]"
aliases:
  - g3 false closure
  - trade list double gunzip
confidence: verified
source_session: cursor-echo-forge-f3-g3-close-2026-07-26
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - project/echo-forge
  - area/echo
  - scope/project
---

# Echo Forge G3 — cierre falso sin path runtime

## Síntoma

- Un agente reporta Fase 3 / G3 “7/7 end-to-end” con unit tests verdes, pero el owner encuentra blockers runtime al revalidar.
- Ocurrió dos veces (iter-1 y iter-2) antes del cierre real con T3.8.

## Causa

- Validar solo contratos de capa (caps nil, validate ref) sin ejercitar la cadena `DownloadNDJSON → decode`.
- Código de índice correcto en un método (`TradeListRepository.EnsureIndexes`) que el boot nunca llama; el boot usa otra definición legacy.
- Overclaim de cobertura §8.4 y conteo `ahead` stale.

## Impacto

- G3 no aceptable: import falla siempre (double-gunzip) y Mongo crea índice único incompleto.
- Pérdida de confianza en handoffs “cerrados”.

## Detección

- Leer `import_trade_list` + contrato de `DownloadNDJSON` (¿plano o gzip?).
- Verificar qué `EnsureIndexes` invoca `cmd/sqx-worker/main.go`.
- Exigir test E2E mínimo de step import con reader fake que escribe plano.
- Contrastar SHAs/`ahead` del mensaje contra `git rev-list --count origin/master..HEAD`.

## Mitigación

- Para trade lists: `DecodeNDJSON` tras download descomprimido; `uniq_scope_natural_v1` en `adapter.EnsureIndexes` + repo.
- Regla de gate: no marcar §8.4.d/c OK sin evidencia del path de boot y del decode post-download.

## Evidencia

- Rechazos 2026-07-26 11:33 y 12:00 en [[Echo Forge - Cierre de Etapa 4]].
- Fix T3.8 commit Symphony `99736de`.
