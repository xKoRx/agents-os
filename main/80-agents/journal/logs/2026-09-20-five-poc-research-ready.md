---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]"
aliases:
  - "Five-POC research-ready 2026-09-20"
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
  - area/personal
---

# 2026-09-20-five-poc-research-ready

## Cambios

- Entidad [[Polymarket Engine — MVP]]: sección nueva `Five-POC Research-Ready — hardening de investigación (2026-09-20, manager)` tras la de Golden Baseline + entrada de bitácora `FIVE_POC_RESEARCH_READY`. Estado del programa: `FIVE_POC_RESEARCH_READY`, baseline código `c977447`, HEAD `cb549c7` en `feature/five-poc-integration` (sin push). Consume el REFACTOR_CANDIDATE de doble registro de estrategias (ahora `strategyCapabilities` única fuente).
- Recurso [[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]: invocación homogénea ampliada con `engine fixture fivepoc` (paso 0, input determinista) y `engine experiment compare` (comparabilidad BASE/VARIANT); determinismo de stamps por receive timeline documentado; sección nueva `Superficie de configuración por POC` (SAFE_TO_CHANGE / USUALLY_CHANGE / DO_NOT_CHANGE / REQUIRES_RESEARCH para S01–S05); gates F5-G13/G14/G15 agregados; suite 33→34 paquetes; limitación `windows_s` de S05 documentada.

## No cambiado

- Receipt v04 del golden baseline (`037c15d`) se conserva intacto; la recertificación research-ready vive en `testdata/research-v05/certificate-v05.json` (27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 live diferidos).
- Deuda previa sin cambios: PE004 W/SFG-06, fee venue real U-02, weather real, calibración probabilística, live.
