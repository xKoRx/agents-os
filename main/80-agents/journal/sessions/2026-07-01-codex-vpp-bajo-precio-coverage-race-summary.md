---
type: session
scope: session
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Meli]]"
project: "[[Destaques de Precio]]"
application: "[[vpp-backend]]"
entities: ["[[vpp-backend]]"]
related: ["[[Search Middleware - Correccion Bajo de Precio Motors]]"]
aliases: ["bajo de precio motors", "price drop motors", "vpp coverage"]
confidence: high
source_session: "[[2026-07-01-codex-vpp-bajo-precio-coverage-race]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# Codex VPP bajo de precio coverage race summary 2026-07-01

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Resolver baja de coverage del PR de bajo de precio Motors en vpp-backend.
- Revisar reporte race-conditions y aplicar fix acotado, no disruptivo, alineado con patrones VPP.

## Contexto cargado

- AGENTS OS entrypoint y skill agents-os-session-close.
- Reglas del repo: .agentic-rules/java/java-kotlin-security-patterns-rules_v1.md y meli/PATTERNS.md.
- Graphify query sobre VPP/bajo de precio coverage/tests.

## Trabajo realizado

- Se agregaron tests para PriceDeprecatedComponentTask, VipMotorsViewTrackingInfoTask, MaintenanceFeeVISMarshaller Android/iOS y PriceMarshaller.
- Se aplicó fix race-condition evitando mutar VISItemTrackingInfoModel recibido desde Observable.zip.
- Se agregó mapper MapStruct VISItemTrackingInfoModelCopyMapper, siguiendo patrón existente de CopyMapper en VPP.
- Se copió el map de experiments de Motors antes de agregar experimentos de price drop / vehicle reservation.

## Artifacts creados o modificados

- src/main/java/com/mercadolibre/vpp/backend/app/shared/mappers/VISItemTrackingInfoModelCopyMapper.java
- src/main/java/com/mercadolibre/vpp_backend/app/shared/tasks/vip/tracks/VipVISViewTrackingInfoTask.java
- src/main/java/com/mercadolibre/vpp_backend/app/shared/tasks/vip/tracks/VipMotorsViewTrackingInfoTask.java
- Tests asociados en VipVISViewTrackingInfoTaskTest, VipMotorsViewTrackingInfoTaskTest y tests de coverage previos.

## Memoria propuesta o creada

- No se creó L3: lo aprendido es específico de esta implementación y queda resumido en L1.

## Decisiones

- No mover price drop a VISItemTrackingInfoTask para no cambiar el contrato de todos los consumidores.
- Preferir copia local con MapStruct frente a copia manual campo por campo.

## Pendiente

- Revisar diff final antes de commit.
- Si se va a pushear: correr ./gradlew jacocoTestReport y dejar que el pre-push hook ejecute los gates, sin bypass.
