---
type: feedback
schema_version: 1
scope: session
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-30-zcode-glm-5-3-flash-result-surface-v1]]"
  - "[[symphony-prod-probe]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-RESULT-SURFACE-V1-NORMAL
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# 2026-08-30-echo-forge-result-surface-session-feedback

%% Feedback solicitado explícitamente por el owner al cierre de la sesión. %%

## Contexto

- Sesión de implementación de la result surface CLI read-only sobre `xKoRx/symphony`; resultado PASS/CLOSED con golden query física. Fricciones reales de la superficie CLI/SDK.

## Fricción

- El SDK (`xKoRx/sdk`) escribe diagnóstico de inicialización/shutdown (telemetría zerolog, debug de etcd `RESPUESTAAAA`) directamente a **stdout** en cada comando CLI, contaminando la salida machine-readable; la única solución local fue silenciar fd 1 con `dup`/`close` POSIX durante el ciclo de vida de los clientes, y las líneas impresas en fase `init()` de paquetes (`internal/config` "BasePath", "Connecting to the server...") quedan imposibles de silenciar desde el comando. Un fix raíz pertenece al SDK (logs a stderr por defecto).
- El árbol de configuración de etcd está namespaced por aplicación/entorno y no existe documentación del contrato: `di.InitSelective("symphony-cli", …production)` falla con "clave requerida faltante: telemetry/otlp/traces/endpoint" porque la config productiva vive bajo `sqx-worker`. El nombre de app es una clave de lookup oculta, no un label.
- `postgrestest.OpenDB` intenta descargar binarios embedded desde Maven en cada host sin cache (DNS bloqueado) y los tests de registry-postgres fallan con timeouts de 30s en vez de saltarse con mensaje claro; el workaround canónico (PG manual desde `.txz` + `TEST_POSTGRES_DSN` + DB virgen) está solo en memoria del vault, no en el README del paquete.

## Pain Pattern Candidate

- Salidas y configuración con side-effects globales implícitos (stdout compartido entre logs y resultado; app-name como clave de config): cada comando nuevo paga el mismo descubrimiento. Candidato a runbook: "contrato de un comando CLI symphony" (DI app-name, stdout limpio, exit codes).
