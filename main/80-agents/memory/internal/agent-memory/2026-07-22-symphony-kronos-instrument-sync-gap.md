---
type: agent_memory
scope: agent-internal
created: "2026-07-22"
updated: 2026-09-09
memory_state: archived
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
application: "[[StrategyQuant X]]"
entities:
  - "[[sqx-instrument-sync]]"
related: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/internal
  - scope/agent
  - project/symphony
---

# Continuidad para el próximo agente — Kronos instrumentos SQX

## TL;DR / Señal crítica

La skill `sqx-instrument-sync` (en el repo Symphony
`.agents/skills/sqx-instrument-sync/`) **NO detecta divergencias de
instrumentos/datasources/symbols fuera de `History/`**. Un caso real
el 2026-07-22: Kronos falló en `classify_and_rank` con
`ErrMetadataMissing`, yo (Claude Code) diagnosticé BUG-001 (`run_id`),
el usuario me corrigió — la causa raíz era que faltaba el instrumento
`XAUUSD_darwinex` en Kronos, visible en la UI de SQX pero invisible
para el sync actual.

## Si en la próxima sesión tocas Kronos/Hera/Zeus

- **Antes** de concluir "BUG-001 run_id" o cualquier teoría de código,
  verifica estado de datos: instrumentos, symbols, databanks. La
  UI de SQX en el worker afectado muestra "unresolved resources" si
  falta un símbolo.
- Hay un **prompt maestro** pendiente de ejecutar (entregado al
  usuario al final de la sesión anterior) para reescribir
  `sqx-instrument-sync` con verificación bit-a-bit sobre TODO
  `~/sqx/user/data` (no solo `History/`). Si el usuario ya lo corrió,
  la skill debería verse muy distinta. Si no, sigue siendo la versión
  frágil.
- **Zeus es siempre la fuente**. Hera y Kronos deben quedar idénticos
  bit-a-bit (salvo DBs H2 vivas y locks).
- Existe script en `~/sync_user_data_zeus.sh` en Zeus, versionado en
  `.agents/skills/sqx-instrument-sync/scripts/sync_user_data_zeus.sh`.
- Las 3 IPs y credenciales de los workers (Zeus/Hera/Kronos) fueron
  **redactadas el 2026-07-25** por violar el mandamiento 13 de la
  constitución. Vivían en texto plano en una memoria marcada `always`,
  así que se cargaban en toda sesión. Si necesitas esos datos,
  consúltalos fuera del vault (gestor de contraseñas o el propio entorno
  Symphony). Ver log `2026-07-25-hot-path-p0-credential-redaction.md`.

## Si vuelves a caer en la trampa del run_id

Recordatorio amargo: `ErrMetadataMissing` en `classify_and_rank`
aparece cuando `LoadAllStrategyMetrics(ctx, waveKey)` devuelve 0 docs.
Eso puede ser:

1. BUG-001 (`run_id` asimétrico) — posible, documentado.
2. **El builder nunca escribió nada** porque SQX abortó por dependencias
   de proyecto (instrumentos/databanks no resueltos). **ESTO FUE LO
   QUE PASÓ EL 2026-07-22 TARDE**. Siempre mira primero el log crudo
   del builder en el worker afectado antes de culpar a run_id.

## Pendientes del usuario

1. Reescribir `sqx-instrument-sync` con el prompt maestro entregado.
2. (Sesión previa, sigue abierto): corregir
   `sqx/exporter-plugin/test-support/custom_project_config/CustomAnalysis-Task1.xml:38`
   (`databank="null"` → `databank="Existing portfolio"`).
3. (Sesión previa, sigue abierto): post-install del worker que haga
  `chmod 0664 $JAR && mkdir -p internal/tmp/compiled && unzip`.

## Memoria generada esta sesión

- L0 raw (este linaje): `journal/sessions/raw/2026-07-22-2022-...-raw.md`
- L3 known-error (nuevo): `sqx-instrument-sync-history-only-verification-gap`
- L1 summary NO se genera — sesión tactical (cierre corto).
- Feedback de sesión y de Graphify en `journal/feedback/`.

## No tocar

- Código de Symphony (esta sesión solo diagnosticó + entregó prompt).
- Estado de los workers (el usuario decidió seguir con otra IA para
  aplicar el fix).
