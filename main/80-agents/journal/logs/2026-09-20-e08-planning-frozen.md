# Change Log — 2026-09-20: E-08 planning frozen (Routing, EconomicCommand and Risk Reservation)

## Contexto

Mandato TOP E-08: convertir la fase «Routing, EconomicCommand and Risk Reservation» en un paquete de implementación cerrado y ejecutable por NORMAL, sin esperar certificación física de Forge ni E-06/E-07, sin implementar código y sin reabrir arquitectura frozen. El gate RAW-BEFORE-ROUTE de E-07 (ERRATUM-A §17.4: PublishSync ≠ commit durable PG) debía quedar elevado a boundary estructural del diseño.

## Cambios

- Repo `xKoRx/echo` (fuera del vault): branch nueva `feature/e08-routing-economic-command-risk-reservation` desde `3765f2ba` (HEAD E-07 C3), commit docs-only `fe5c9de0`, push FF verificado (nueva rama en origin). `specs/FEAT-ROUTING-ECONOMIC-COMMAND-RISK-RESERVATION-E8/`: SPEC.md v1.0.0 (gate RG-1…RG-6; universo expected/excluded congelado por decisión; CommandID determinístico por `command_unique_key` UNIQUE + `content_digest` H("echo-command-content.v1",…) con UUIDv7 mint-once — consume defer E-02 §1.0.1; snapshots inmutables content-addressed con contenido embebido; reservas integradas al command con headroom serializado por cuenta y `UNKNOWN_HELD` sin auto-release; outbox monotónico en la fila del comando; errores permanentes/transitorios/desconocidos fail-closed; sweepers SKIP LOCKED; reconciliación sin reenvío como superficie E-09; migración 066 exclusiva; separación clase A vs clase C), PLAN.md (lista cerrada de archivos + tablas 066), TASKS.md (T00–T14), VERIFICATION.md (gates + matriz MT-01…MT-18 + dependencias), NORMAL-PROMPT.md (mandato único autónomo con baseline exacto, STOPs y prohibiciones económicas).
- Vault: nota nueva `10-projects/Echo/agentes/Echo — E-08 Routing EconomicCommand and Risk Reservation.md` materializada vía `materialize_schema_note.py` y llenada (owner agent, parent Live Platform V1); `Echo — Live Platform V1.md` actualizada por delta (estado actual, tabla de entrega con fila E-08, roadmap § E-08 con planning vivo, tarea puente enlazada a la nota, hijas de implementación, Docs/Links, bitácora 2026-09-20, frontmatter updated).
- Registro de ejecución: `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-e08-planning-frozen.md`.

## Verificación

- Baseline resuelto contra repos reales: `origin/master` `5dd998f1` == mandato; `origin/feature/e07-raw-facts-deal-lifecycle` `3765f2ba` == local (C3); `origin/feature/e06-reference-enrollment-binding` `b66dc5ff`; ancestry master→E-07 verificado; migración 066 libre (001–065 ocupadas).
- Interfaces verificadas en source del baseline: S0 `EconomicCommand`/`RuntimeBinding`/`TradingFactV1`, consumer E-07 (transacción única + PROCESSED + `RecoverPendingFact` SKIP LOCKED), `binding_lookup` (razones pin), 029 (`source_event_id` único, `processing_status` CHECK), 064/065 (estados binding, UNIQUE origin/deal key), 062, legacy planner/MM (`GenerateUUIDv7`), catálogo mutable, Live Authority §§7–8 completas, defer E-02 confirmado.
- Ninguna decisión de identidad, riesgo o exactly-once económico delegada a NORMAL; clase C (activación económica) condicionada con prerrequisitos declarados y router default OFF fail-closed.

## No-tocados

- Código de `xKoRx/echo` (sólo docs specs en rama nueva), Forge, master, ramas E-06/E-07, migraciones 001–065, SHARED DEV, PROD, cuentas: sin intervención. E-01…E-07 no reabiertos. Defecto `EchoPersistence.mqh` (defecto #6) intocado — carril del Manager. PHYSICAL/ECONOMIC_ACTIVATION declarados PENDING; FINAL_CLOSED=NO.
