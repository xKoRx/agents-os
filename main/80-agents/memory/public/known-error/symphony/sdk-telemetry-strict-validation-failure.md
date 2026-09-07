---
type: known_error
scope: project
created: 2026-07-02
updated: 2026-07-02
area: "[[Personal]]"
project: "[[symphony]]"
application: "[[sdk]]"
entities:
  - "[[symphony]]"
  - "[[sdk]]"
related: []
aliases:
  - telemetry strict validation error
  - telemetry-init-error
  - error cargando configuracion desde etcd telemetry
confidence: verified
source_session: 6c3cabba-7d32-4efb-8783-ae64c5f6f72d
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - project/symphony
  - tech/telemetry
  - error/telemetry-init
---

# SDK Telemetry Strict Validation Failure in Integration Tests

## Síntoma

- Las pruebas de integración fallan repentinamente con un error del tipo:
  `error cargando configuración desde ETCD (symphony/local): clave requerida faltante o vacía: telemetry/otlp/traces/insecure`
  o `versión requerida: ninguna de las claves de versión encontrada: [version]`, o `telemetry/traces/enabled debe ser 'true' o 'false'`.

## Causa

- El cliente de telemetría del SDK (`sdkTelemetry.Init`) realiza validaciones estrictas y fast-fail en las configuraciones cargadas de ETCD.
- Si se inicializan clientes de pruebas conectados a un prefijo de ETCD (como `symphony/local` o `symphony/development`) que no tiene poblados todos los parámetros estrictos de telemetría, la inicialización aborta el proceso de test.

## Impacto

- Aborta la inicialización de los clientes reales de MinIO, PostgreSQL, etc., bloqueando la ejecución completa del conjunto de pruebas que hagan uso de la telemetría del SDK.

## Detección

- Buscar en los logs de la ejecución de pruebas: `error cargando configuración desde ETCD (<app>/<env>): clave requerida faltante o vacía: telemetry/...` o `ninguna de las claves de versión encontrada: [version]`.

## Mitigación

- Poblar manualmente las claves de configuración de telemetría requeridas en el `etcdCache` del test ANTES de instanciar o inicializar el cliente de telemetría con `sdkTelemetry.Init`:
  ```go
  _ = etcdCache.SetVar(ctx, "telemetry/otlp/traces/endpoint", "http://192.168.31.45:4317")
  _ = etcdCache.SetVar(ctx, "telemetry/otlp/traces/insecure", "true")
  _ = etcdCache.SetVar(ctx, "telemetry/otlp/metrics/endpoint", "http://192.168.31.45:4317")
  _ = etcdCache.SetVar(ctx, "telemetry/otlp/metrics/insecure", "true")
  _ = etcdCache.SetVar(ctx, "telemetry/metrics/enabled", "true")
  _ = etcdCache.SetVar(ctx, "telemetry/metrics/interval", "10s")
  _ = etcdCache.SetVar(ctx, "telemetry/traces/enabled", "true")
  _ = etcdCache.SetVar(ctx, "telemetry/traces/sample_rate", "1.0")
  _ = etcdCache.SetVar(ctx, "telemetry/log/level", "info")
  _ = etcdCache.SetVar(ctx, "version", "1.0.0")
  ```

## Evidencia

- Repo `github.com/xKoRx/symphony`, path `integration/project_listing_test.go`.
- Repo `github.com/xKoRx/symphony`, path `internal/tasks/project_listing_integration_test.go`.
