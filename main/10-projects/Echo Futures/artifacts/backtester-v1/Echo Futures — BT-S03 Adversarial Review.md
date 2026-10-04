---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
  - "[[Echo Futures — BT-S02 Backtester V1 Implementation Handoff]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-04"
updated: "2026-10-04"
---

# Echo Futures — BT-S03 Adversarial Review

## Propósito

Revisión adversarial de `xKoRx/echo@f41da25cc0b779ea48375198dbedaf932b930a80`, sin fixes productivos. Documento en consolidación; las suites finales quedaron detenidas después del incidente de ejecución descrito a continuación. No es certificación.

## Contenido

El gate técnico requiere remediación: se demostraron defectos de identidad, ownership de fills, contexto económico, finalización y reproducción. Los reportes de cinco subagentes reales y repros aislados se conservan en el workspace externo de review `bt-s03-20261004`; la integración y verificación final siguen pendientes.

### Incidente operativo — escalado al Owner

El subagente Sol causal ejecutó `go test ./...` desde `xKoRx/echo:v3/sdk`, fuera del alcance autorizado. El test legacy `TestSeedEchoConfig_Production` reportó escrituras en ETCD bajo `/echo/production/` a las 14:19:46–14:19:48 America/Santiago del 2026-10-04: 32 claves según su resumen y 31 nombres individualmente observados. Incluye configuración PostgreSQL, Kafka, gateway y telemetría. El comando terminó FAIL. El Primary detuvo el frente y dos procesos posteriores de pruebas del review; no quedan pruebas activas observadas. No se restauró configuración ni se verificó impacto runtime. El Owner fue notificado y debe coordinar revisión/restauración desde historial autorizado. No se persisten valores. Evidencia sanitizada: workspace de review `reports/incident.md`; evidencia primaria: transcript de herramientas de Sol causal. Este incidente preexistente en el test legacy no es un defecto nuevo del backtester ni autoriza ampliar BT-S04 a infraestructura.

## Fuentes

- [[Echo Futures — BT-S01 Backtester V1 Design]], leído completo.
- [[Echo Futures — BT-S02 Backtester V1 Implementation Handoff]], leído completo.
- `xKoRx/echo`, branch `codex/bt-s03-adversarial-review`, baseline `f41da25c`.
