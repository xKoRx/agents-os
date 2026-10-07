---
type: source
schema_version: 1
status: superseded
area: "[[Meli]]"
source_url:
repo: melisource/fury_rio-playmaker
path: src/main/resources/application-local-integration.yml
author:
published:
captured: "2026-10-07"
license:
checksum:
supersedes:
superseded_by: "[[Source — Playmaker — Kafka local 2026-10-07]]"
aliases: []
tags:
  - kind/source
created: "2026-10-07"
updated: "2026-10-07"
related: ["[[rio-playmaker]]", "[[rio-controlplane-clickhouse]]"]
---

# Source — Playmaker — Transporte local 2026-10-07

## Referencia

- Repositorio: `melisource/fury_rio-playmaker`.
- Checkout inspeccionado: `release/202610.5.0 @ 5abe5c26a0e52a689001dd43ee3f4e84aa76960d`. No se sincronizó, cambió ni ejecutó Playmaker.
- Archivos: `build.gradle`, `src/main/resources/application-local.yml`, `src/main/resources/application-local-integration.yml`, `docker-compose.yaml`, `local/01-mysql.sh`, `LocalDeploymentTriggerLoopback`, `LocalKafkaDeploymentTriggerProducer`, `LocalKafkaDeploymentResultListener`, `DeploymentResultConsumerController` y `service/pipeline/ComponentContextService.java`.

## Alcance

- El perfil local configura puerto 9090, MySQL, usuario `playmakeruser`, contraseña por `PLAYMAKER_DB_PASSWORD` y base `rioplaymakerdb`. La existencia de un MySQL en 3306 no demuestra que tenga esa base, usuario o migraciones.
- El loopback local puede producir STARTED/COMPLETED/FAILED simulados; no invoca físicamente un control plane.
- El perfil conjunto `local,local-integration` desactiva ese loopback y usa Kafka: `rio-deployment-trigger-local`, `rio-deployment-result-local`, `rio-deployment-result-local-dlt`; bootstrap loopback en puerto 39092 por defecto.
- Los triggers Kafka contienen el payload SDK plano. El listener de resultados usa `DeploymentResultConsumerService` real.
- Playmaker también recibe envelopes BigQueue de resultados mediante `POST /events/deployment/result`.
- Dependency declarada `rio-sdk-events:1.5.0`; se debe comprobar compatibilidad wire con `1.6.1` del CP, sin inferirla sólo del número de versión.
- `resolveLatestVersion` deriva inputs/outputs de la definición asociada al último deployment. No demuestra requested inputs del deployment nuevo.

## Notas de provenance

- Inspección de código únicamente: no es prueba E2E ni verificación de la referencia remota más reciente.
- El CP local publica archivos; Playmaker local-integration espera Kafka. Se requiere un adapter de transporte o un bridge explícito que conserve el payload y permita verificar correlación, estado final y outputs.
