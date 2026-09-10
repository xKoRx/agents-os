---
type: agent_memory
scope: project
tags:
  - kind/learning
  - project/echo
  - area/replication
created: 2026-07-16
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
---

# Continuidad Cognitiva: Diagnóstico de Detención de Replicación en Echo V3

En esta sesión se investigó la causa raíz de por qué no se copian operaciones en Echo desde hace ~2 semanas, descartando el warning menor de Kache y localizando la desconexión del estado de configuración en Flink.

## Diagnóstico y Causa Raíz

1. **Warning de Cuentas (Kache)**:
   - El log `echo.config_flow: kache skipping invalid direct ClientConfig JSON...` con la key `"default"` y `value_bytes: 4` (`"null"`) es inofensivo. Es un descarte controlado de deserialización segura en `account_configs.go` y no afecta a las cuentas de ejecución numéricas reales.

2. **Causa de la Detención de Replicación**:
   - Hace 2-3 semanas (commit `f721f4dd` el 24 de junio de 2026) se implementó la nueva caché local de estrategias (`StrategyCache` en `kache` Go) en Flink/Core.
   - Esta migración eliminó el polling periódico de base de datos (`ExecutionPoliciesLoader` en `echo-core`) y lo reemplazó por el consumo en background del topic compactado `echo.execution-policies.v1`.
   - **El error de configuración en Kafka**: El topic `echo.execution-policies.v1` (y potencialmente `echo.account-configs.v1`) fue configurado con `cleanup.policy = compact,delete` y un `retention.ms` de 7 días. En Kafka, esto significa que los mensajes se borran por completo pasados los 7 días, incluso si son el último valor para una clave. Como Flink y el Bridge leen desde `earliest` al iniciar para poblar el caché en memoria, las políticas antiguas borradas por retención desaparecieron, dejando al replicador con caché vacío y rechazando señales con `NO_EXECUTION_POLICIES`.
   - Para resolver esto, se debe cambiar la política de limpieza a únicamente `compact` (sin `delete`) y eliminar la retención por tiempo, para luego invocar el endpoint administrativo `/api/v1/admin/republish` para repoblar Kafka.

3. **Cuentas sin Símbolos Permitidos**:
   - Se observó además que varias cuentas activas nuevas (`Orion NEWGEN!`, `Orion LOVE!`, `Orion 250%Refund`, `WSF 2X1`, `Orion XAU!`) tienen la columna `client_allowed_symbols` como un array vacío (`[]`). Esto impedirá la copia o la suscripción de símbolos en el EA de Metatrader si no se les configuran explícitamente los símbolos autorizados.
