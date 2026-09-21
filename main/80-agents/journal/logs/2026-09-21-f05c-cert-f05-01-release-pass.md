---
type: change_log
schema_version: 1
created: 2026-09-21
updated: 2026-09-21
area: "[[Echo]]"
project: "[[Echo Forge — Factory V2 Completion]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo — Producto Integrado]]"
tags:
  - kind/change-log
  - area/echo
  - project/echo-forge
---

# 2026-09-21 — CERT-F05-01 PASS (release cohesiva 0.2.105) y arranque CERT-F05-02

- **Qué cambió:** (1) Backlog `[[Echo + Echo Forge — Deferred Certification Backlog]]`: nuevo delta "release cohesiva CERT-F05-01" (G0–G2 + veredicto) y marcado `CERT_F05_01_PASS` en la fila CERT-F05-01. (2) `[[Echo Forge — Factory V2 Completion]]`: Next development task y Bitácora actualizados (F05-01 PASS, F05-02 en ejecución con identidades).
- **Fuera del vault (xKoRx/symphony @ `codex/f05-release-prep`):** FF `a2321cc` (F-INT-01/02); `1056b30` fix F-INT-03 test-only (reset por test en `newControlPlane` + V1 coexistence con membership de origen en tx; suite completa registry-postgres GREEN); `745bc8b` refresh frozen de `sqx/core/releasematrix/release-matrix.json` + guards (físico/cross-lane F-04 DONE con records; allowlist ampliada exactamente a esas 3 filas; f05i released DONE; pipeline conserva DEFERRED). Release `0.2.105` publicada desde `745bc8b` y desplegada 4/4.
- **Autoridad:** mandato maestro F05 FINAL COMPLETION del owner (§7 autoriza el delta frozen acotado de la matriz; §9 autoriza la publicación).
- **Evidencia:** `~/aranea/work/cert-f05-20260921/` (G0 baseline, G2 test gates, CERT-F05-01 PASS, logs de build).
- **No cambió:** ningún contrato frozen de producto; sin migraciones; sin DEFERRED de pipeline alterados; deployed rows siguen OPEN hasta el refresh post-campaña.
