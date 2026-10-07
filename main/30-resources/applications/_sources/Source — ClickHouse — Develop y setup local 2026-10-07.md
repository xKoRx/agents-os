---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url:
repo: melisource/fury_rio-controlplane-clickhouse
path: README.md
author:
published:
captured: "2026-10-07"
license:
checksum:
supersedes:
superseded_by:
aliases: []
tags:
  - kind/source
created: "2026-10-07"
updated: "2026-10-07"
related: ["[[rio-controlplane-clickhouse]]"]
---

# Source — ClickHouse — Develop y setup local 2026-10-07

## Referencia

- Repositorio: `melisource/fury_rio-controlplane-clickhouse`; baseline `develop @ c8b20b6531a73348314587fc14f43e0ad8ce76ae`.
- Archivos: `README.md` (On-Premise), `docker-compose.yml`, `src/main/resources/application-local.yml`, `BigQueueClientFactory`, `LocalFileBigQueueClient` y `DeploymentEventController`.
- Fuente adicional: instrucción explícita del owner de eliminar `feature/new-component-context` y limitar el trabajo a comprender el estado/setup/integración.

## Alcance

- Se ejecutó `git merge --abort`, `git switch develop` y `git branch -D feature/new-component-context`. La rama local fue eliminada; no queda merge pendiente.
- `git status --short --branch`: develop alineado con origin/develop, sin cambios trackeados; `graphify-out/` se preservó sin staging.
- `git ls-remote --heads origin refs/heads/feature/new-component-context` terminó sin referencias: la rama no existe en el remoto consultado.
- El commit de develop es el mismo baseline certificado en [[Source — ClickHouse — Preflight local 2026-10-07]]: 2335 tests verdes, bootJar y ping local. No se repitieron pruebas ni se iniciaron servicios en esta actualización.
- Compose expone 8123/9000 sólo en loopback y requiere `CLICKHOUSE_LOCAL_ADMIN_PASSWORD`. El CP toma usuario `controlplane` por defecto y `CLICKHOUSE_ONPREM_PASSWORD` desde `.env` o entorno; el README define la creación de usuario y grants.
- `SCOPE=local` usa ClickHouse on-premise, estado/locks en memoria, KMS simulado y resultados BigQueue en archivos. No se encontraron listeners ni publishers Kafka ni perfil local-integration en el CP inspeccionado.
- El archivo de resultado usa el wrapper `topic`, `timestamp`, `messageId`, `message`; Kafka de Playmaker espera el payload contenido en `message`, sin ese wrapper.

## Notas de provenance

- La rama antigua quedó descartada por autorización explícita. El foco vigente es el baseline develop y su capacidad local, no el delivery de adopción de inputs.
- El README y Bruno consultados carecen de Context en sus examples de provision; un trigger sin Context es rechazado con FAILED aunque el ACK sea HTTP 200.
- Las signatures públicas de los DTOs trigger/result/context/component/latestVersion/inputs/outputs/relatedComponent se compararon mediante javap entre los jars SDK 1.5.0 y 1.6.1: coinciden. `DeploymentSchemaVersion.CURRENT` es 1 en ambos. Esto es evidencia estática, no una prueba producer-consumer de serialización.
