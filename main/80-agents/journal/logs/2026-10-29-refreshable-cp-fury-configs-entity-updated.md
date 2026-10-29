---
type: change_log
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Meli]]"
project: "[[Import de Refreshable Materialized Views externas]]"
application:
entities: ["[[Import de Refreshable Materialized Views externas]]", "[[RIO E2E local]]"]
related: []
aliases: []
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
---

# Refreshable import — configuración de arranque y sincronización con develop

## Cambio

- **Tipo:** updated.
- **Entidades:** [[Import de Refreshable Materialized Views externas]] y [[RIO E2E local]]. Actualización de ramas, nueva versión del CP y diagnóstico del fallo de arranque en `test2-consumer-nonprod`.
- **Estado anterior:** versiones de prueba del 28 de octubre: CP `0.0.4-import-ref-view-ch`, PM `0.0.3-import-ref-view-ch`, front `0.0.4-import-ref-view-ch`, sincronizadas con develop de esa fecha.
- **Estado nuevo:** Playmaker y front siguen con cero commits detrás de develop. CP integra y publica `5c469575` mediante merge `9b9f677c`, con el lector de Fury Configs de #363/SIG-686 que entró a develop el 29 de octubre. Fury confirmó `0.0.5-import-ref-view-ch` desde ese commit en FINISHED, con CI PASS y registry disponible en us-east-1.aws/us-east4.gcp (build576).

## Motivo

- El owner pidió revisar la sincronización y diagnosticar un arranque fallido del CP en `test2-consumer-nonprod`. Esta es evidencia del despliegue del owner; el agente no realizó despliegues ni modificó configuración remota.

## Fuentes usadas

- Stacktrace proporcionado: creación de `KvsConfig.kvsOwnershipService` falla por `kvs.ownership-container-name must not be null or blank`.
- Fuente e historia: la validación obligatoria de ownership llegó a develop en `a53c645b` el 19 de octubre; el feature mantiene esa validación. El tag `0.0.4-import-ref-view-ch` carece de `FuryConfig` y de su registro de arranque.
- `ScopeUtils.calculateScopeSuffix` deriva `test2-consumer` del scope señalado. No existe YAML empaquetado con ese sufijo y el normalizador no reconoce `test2` como token `test`; `application.yml` define TTLs y límites KVS, pero no el contenedor de ownership. El valor faltante debe provenir del perfil Fury o de una propiedad explícita equivalente en ese scope.
- La relación Graphify `KvsConfig` → `KvsProperties` y `requireOwnershipContainer` se confirmó contra la fuente. Se consultó el índice existente sin regenerarlo, preservando los tres archivos ajenos exigidos por el owner.
- CLI de KVS: `deploy-state-test-nonprod` existe y está aprobado. Esto no acredita su asignación al scope ni el segmento efectivo.

## Resolución aplicada

- Fetch de los tres origins. PM `fd4b1dac0` incluye develop `c7d894aad`; front `e0f07541b` incluye `c4c09b0bb`. CP quedó en `9b9f677ce2071456ca56a816f6b8fae9b513d259`, con develop `5c469575717293f45cd6fa1241283b16b29b633a`. Las tres ramas están publicadas y con cero commits detrás de develop observado.
- Merge del CP preparado en checkout temporal propio y aplicado preservando los bytes de Graphify del owner. Checkout temporal retirado. No se alteró el guard de ownership ni se agregó un fallback que lo omita.
- El nuevo lector usa el perfil `configs` YAML montado en `/configs/latest`, antes de bindear las propiedades. Conserva prioridades de argumentos/JVM/entorno y valida checksum. El despliegue de la nueva versión reinicia las instancias; el loader no ofrece hot reload.
- Las lecturas de instancia fallaron por HTTP 404 en el proxy de comandos de Fury. El resultado no prueba que falten archivos o claves en el perfil remoto. Se solicitó al owner sólo el bloque KVS no sensible para confirmar la configuración asignada; no se descargó, guardó ni imprimió un perfil completo.

## Validación

- CP: 469 suites, 5123 tests, 0 fallas/errores, 1 omitido. Incluye FuryConfigTest 59, KvsConfigTest 34 y normalizador de perfiles 7, todos PASS.
- PM/front: sin cambios desde las versiones ya verificadas el 28 de octubre; no se repitieron suites innecesariamente.
- La nueva versión del CP tiene tests de Fury habilitados, `productive=false` y commit exacto `9b9f677c`. CI informa `test_passed=true`; estado FINISHED y registry AWS/GCP verificados mediante consultas independientes de Fury.
- El diagnóstico de valor efectivo vacío está acreditado por el stacktrace. La presencia exacta de la clave en el perfil remoto y el arranque real con la nueva versión siguen sin verificar.
- PA-1 a PA-5 no se resolvieron ni se cambió lógica del import en esta ronda.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos, contenido de perfiles, credenciales ni payloads completos del owner.

## Rollback

- No hubo despliegues ni cambios remotos de configuración por parte del agente. Si el owner elige una versión anterior, se mantiene la limitación de lectura de Fury Configs descrita. No deshabilitar ownership para conseguir el arranque.
