---
type: change_log
schema_version: 1
scope: session
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-23 — Echo Futures seven-day research horizon

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Convertir el discovery operativo en un horizonte máximo de siete días gestionado por `technical-project-manager`, con research acotado y gates de producto diarios.

## Fuentes usadas

- Decisión explícita del owner: velocidad máxima de una semana, tres referentes y curso privado de Gerard disponible para entrevista.
- `technical-project-manager` como procedimiento de management activo.

## Resolución aplicada

- Tres research one-shot paralelos bajo contrato común; Gerard combina entrevista del owner + research público. D2 síntesis, D3 mecanización, D4 backtest/replay, D5 prop simulation, D6 robustness y D7 `GO | ITERATE | NO_GO`. El piloto aproximado de 20×10K queda como hipótesis ilustrativa hasta D7.

## Validación

- Proyecto re-leído desde `master` tras el update; sprint y horizonte persistidos. No se autorizó implementación ni compra de cuentas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir commit del horizonte y volver al plan G0/G1 previo si el owner decide cambiar la cadencia.
