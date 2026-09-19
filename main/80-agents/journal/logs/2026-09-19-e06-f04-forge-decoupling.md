---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Aranea]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
related:
  - "[[Echo Forge]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change Log — 2026-09-19 — Desacoplamiento Forge↔E-06 (decisión Manager)

Sesión ZCode/GLM-5.3-Flash, mandato NORMAL de continuidad: eliminar toda subordinación del desarrollo, releases o flota compartida de Forge a E-06. Cambios exclusivamente documentales en el vault; cero código E-06/Forge, cero merges, cero releases, cero deploys, cero instalaciones, cero intervención sobre RERUN-5 o campañas paralelas.

## Cambios

1. **[[Echo — E-06 Reference Enrollment and Binding]] — nuevo bullet de continuidad `E06_FORGE_DESCOPLAMIENTO_REGISTRADO`** al tope de «Estado actual»: decisiones del Manager registradas (no ejecución del paquete release `0.2.103`; sin merge a `master` ni deploy workers/JAR por necesidad exclusiva de E-06; RERUN-5 `c42dd637`/`c06b09a9` intocada por drain; Forge con autoridad plena sobre roadmap, releases y selección de finalistas), G0 PASS y G1 `PROMOTION_SEAL_MISSING` sin cambio, referencia concreta de la ruta de certificación aislada ya documentada (backlog CERT-F04-01 + `OWNER-REQUEST-0.2.103.md` UNA go/no-go + `NEW-RUN-FRESH-IDENTITY-PROMPT.md` `cert-f04-01-rerun6`), advertencia aislamiento Git ≠ aislamiento runtime, y el siguiente evento que permite reanudar T21.
2. **[[Echo Forge — F-04 Magic allocation, version seal and handoff]] — nuevo bullet de continuidad `DESCOPLAMIENTO Forge↔E-06 REGISTRADO`** al tope de «Estado actual»: autoridad de Forge preservada, `OWNER-REQUEST-0.2.103.md` queda como solicitud documental sin go, drain canónico vigente sobre RERUN-5, ruta de certificación SOLO referenciada sin construir infraestructura nueva, y prohibición de fabricar promociones/evaluaciones/seals.
3. **Verificación de no-duplicación:** el único «desacoplamiento» preexistente en ambas notas era la sección «Estado de lifecycle y desacoplamiento de certificación» de F-04 (certificación diferida del 2026-09-13); el desacoplamiento de dependencia Forge↔E-06 del Manager NO constaba. Evidencias técnicas previas (G0 R3, reconciliación de release, fixtures) preservadas sin reescritura.

## Estado resultante

- E-06: G0 **PASS** vigente; G1 `PROMOTION_SEAL_MISSING`; T21 [ ]; T22 PENDING; NO CLOSED. Echo @ `b66dc5ff` (docs-only, sin cambios este mandato); Forge integrada `codex/f05-r3-integration` @ `3f6cd110` == origin, `master` @ `0b9742b0`; release publicada `0.2.102` @ `66faa42`; candidate `0.2.103` sin go.
- RERUN-5 viva sobre `0.2.102`, preservada por drain canónico, sin observación nueva esta sesión (el mandato no la interviene).
- **Siguiente evento para reanudar T21:** existencia durable de una FINALIST_PROMOTION auténtica de `b94f1400` con seal exitoso (`strategy_versions`/`handoffs` no vacíos en el control plane PG live) + designación del entorno de certificación E-04 y terminal reference; producción de esa promoción es decisión exclusiva de Forge.

## No ejecutado (por diseño del mandato)

Release `0.2.103`, merge FF, rollout de flota, instalación JAR R3, corrida `cert-f04-01-rerun6`, cualquier ingesta E-04 u orden económica. `OWNER-REQUEST-0.2.103.md` permanece como solicitud documental sin go; su ejecución futura es go/no-go del owner por la autoridad de Forge, nunca por necesidad de E-06.
