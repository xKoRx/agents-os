---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures — Optimización de Campañas]]", "[[EF-CAMPAIGN-MODES-I0-LOCAL]]", "[[EF-CAMPAIGN-MODES-DESIGN]]", "[[EF-CAMPAIGN-MODES-I0-FINAL-RETURN]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---

# Echo Futures — change log — revisión manager de I0-S3 (2026-10-29)

## Motivo y fuentes

Continuidad del manager tras retorno I0-S3 del ejecutor. Source revisado mediante GitHub: xKoRx/echo `feature/ef-campaign-modes-i0@4ff327247f3c369ce3aded5bc577bcebc64ecc61`; corrección `a98914c7`; SOURCE Go `compose.go`, `platform_campaign.go`, `platform_research.go`, reporter y nuevos tests. Retorno [[EF-CAMPAIGN-MODES-I0-FINAL-RETURN]] ya sincronizado en Agents-OS, aunque el verificador local declaró .git no accesible.

## Decisión

Commit y diff de scope verificados: S3 toca economics_report.py, tests y SDD, no Go/SDK/runtime. Autor reporta 51/51+124/124, 25/25 fixtures, R03 determinista, 408/408 coverage, sentinel no spawn; no reejecutados por manager CLOUD. Código fuente presenta cuatro nuevas barreras focales: (G1) RunID determinista ≠ identidad attempt; igual RunID no prueba revision; (G2) provisional FUNDING_INSTALL_PENDING/CompliantAt no prueban control aplicado, setup fees son setup; (G3) q OBSERVED con q_roots y gaps en la misma cohorte, sin validación temporal; (G4) sums_by_assignment True con declaración parcial. No mezclar con reabrir 11 findings previos.

## Continuidad

Actualizar solo planner, diseño C05 por precisión R1 y paquete I0-LOCAL con mandato I0-S3R1. Cero cambio producto, pruebas físicas, campañas, cash/infra, merge/deploy. S04-F01 fixture Go y S04-F02 guard ausente continúan separados y sin aceptar. Próximo agent GLM LOCAL focal≤90 min; registrar SHA y test. Manager/programa abiertos; PROD FROZEN; PRO_CHAT_POOL_DELTA UNKNOWN.
