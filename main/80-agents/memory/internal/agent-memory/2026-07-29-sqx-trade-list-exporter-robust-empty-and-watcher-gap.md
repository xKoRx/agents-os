---
type: doc
status: active
created: 2026-07-29
updated: 2026-07-29
project: "[[Echo Forge]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[EchoForgeTradeListExporter]]"
  - "[[sqx-watcher]]"
  - "[[deployer-screen]]"
load_policy: when_error_matches
tags:
  - kind/continuity
  - tech/sqx
  - tech/watcher
  - area/echo-forge
---

# Echo Forge — Trade List Exporter robusto vacío + gap de watcher en Hera/Kronos

## Resumen de la sesión

- Workflow Temporal `sqx-main-00_configs-v1-NDX-H1-L-1785373312` (RunID `019fb08a-c4b1-7743-949a-9bfbe0770c22`) falló en `ActivityType trade_list_exporter`, Attempt 6, mismo error en los 3 workers (Zeus, Hera, Kronos).
- El exporter Java `EchoForgeTradeListExporter v1.2.0` corrió 36+ veces entre 28-29 julio; todos los intentos terminan con `Artifacts written: 0, Strategies seen: 1, errors: 1` y `source_order_count=0, sample_byte=0`.
- Causa raíz Java: `TradeExtractionException` en `TradeExtractionService.java:189` — el `.sqx` "robusto" seleccionado (`NDX_L_H1_example_flow_44_v1_Strategy_6.1.14.h0_robust.sqx`, 283 KB) no contiene trades OOS/FULL materializados.

## Estado de los workers verificado por SSH (2026-07-29 21:43 local)

- `/opt/symphony/CURRENT` = `0.2.6` en los 3 nodos.
- Binario `symphony` con md5 idéntico `f385073b779786ed0cca1b8867345d28` en los 3.
- **Hera y Kronos NO tienen `sqx-watcher` en `/opt/symphony/current/bin/`.** Solo Zeus lo tiene (md5 `ff4293e58a0cbf0aa146b7faa9e33330`).
- `systemctl status symphony-watcher.service`:
  - Zeus: `active (running) since Wed 2026-07-29 20:53:09`.
  - Hera: `Unit symphony-watcher.service could not be found.`
  - Kronos: `Unit symphony-watcher.service could not be found.`
- `/var/lib/symphony/input/`:
  - Zeus: 26 archivos `.sqx` sueltos en root + `00_configs/` (4 `.cfx`) + `example/` + `processed/`.
  - Hera/Kronos: directorio completamente vacío.
- Stager dice `ya en versión 0.2.6; nada que hacer` en los 3.

## Artefactos preparados para diagnóstico externo

Reporte detallado (H1–H7 + Q1–Q5) entregado al usuario para que lo pase a otra IA.
Conclusión principal: el gap H2 (watcher ausente en Hera/Kronos) es un bug de despliegue, no diseño. El binario está en MinIO pero el stager no lo materializa y/o el unit no se instala.

## Próximo paso humano

- Pasar reporte de evidencia a IA externa para diagnóstico de H1 (causa raíz Java) y H2 (gap de stager/unit en Hera/Kronos).
- Decidir si se hace fix de H4 (`validate_configs` ignora `spec.ConfigFolder` en `sqx/activities/watcher/steps.go:184-200`).
