---
type: agent_memory
scope: project
tags:
  - kind/learning
  - project/echo
  - area/trading
created: 2026-08-14
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
---

# Continuidad Cognitiva: Ubicación del repo Echo y fix Daily Ops nativas (2026-08-14)

## Ubicación canónica del código Echo (CORRECCIÓN IMPORTANTE)

- El monorepo de Echo (core, bridge, agent, gateway, clients MT4/MT5, front, etc.) vive en el **GOPATH**, NO en `~/fuentes`: `~/go/src/github.com/xKoRx/echo` (v1/v2/v3 + agent + core + pipe + tools).
- El home difiere por máquina: Mac laboral (epga) → `rjara/go`; Mac personal → `rodrigojara/go`. Resolver siempre vía `~/go`.
- `~/fuentes` es storage de proyectos Meli (rio-*, ads-signals-*, graphify). No buscar Echo ahí. Relacionado: [[Fuentes — Workspace de repositorios]].
- Hasura del front (env `.env` de `v3/front`): `http://192.168.31.75:8080/v1/graphql`; inalcanzable fuera de esa red.

## Bug: operaciones NATIVE cerradas no aparecían en Daily Ops (Watchtower V3)

Causa raíz (confirmada: cero filas `origin='NATIVE'` en `trade_journal` según queries del owner):

1. El EA slave envía opens nativos como `execution_result` **sin campo `broker`** (MT4 y MT5).
2. `ensureJournalParentRows` (sdk/postgres) se saltaba todo el provisioning sin broker → nunca se creaba `strategy_definitions` para `NATIVE`/`magic_N`.
3. INSERT del open caía por `fk_trade_journal_canonical_strategy` → open descartado sin retry → close rechazado por `ErrCloseWithoutOpen` → nunca llega `status='CLOSED'` → fuera de `mv_daily_operations` → invisible en Daily Ops.

Fix aplicado (2026-08-14, working tree sin commit, repo echo):

- `v3/bridge/internal/pipe_handler.go`: backfill `result.Broker = h.broker` en `handleExecutionResult` (simétrico a close).
- `v3/sdk/postgres/trade_journal_repository.go`: `ensureJournalParentRows` provisiona `strategy_definitions` aunque no venga broker (fallback `unknown_broker` para FK de accounts).
- Tests sqlmock actualizados + nuevo `SaveOpen_NativeWithoutBroker_ensuresStrategy`. Build/tests OK (Scratch/Kafka falla preexistente).

## Pendientes

- Deploy de bridge (agent) + core. Las nativas abiertas/cerradas antes del deploy no se recuperan solas; opcional: script de backfill desde historial de deals.
- Debt detectada: tras reinicio del EA con nativa abierta se regenera otro `trade_id` sintético (huérfanas OPEN); `GetEffectiveMagicNumber` convierte manuales (magic 0) en `magic_<DefaultMagicNumber>` en vez de `NATIVE`.

## Actualización 2026-08-20 (corrección de estado)

- El fix YA ESTÁ COMMITEADO como `c8aa59a4` (2026-08-19 22:27) en rama local `hotfix/native-dailyops-broker` (worktree `/private/tmp/echo-native-dailyops-hotfix`, volátil). NO está pusheada ni mergeada a master. "Working tree sin commit" quedó obsoleto.
- Estado consolidado del ecosistema echo: [[Echo - Discovery y Estado]].

## Actualización 2026-08-20 (tarde — resolución)

- **El hotfix SÍ estaba deployado en prod** (core en `192.168.31.71` = build del worktree, deploy 19-08 22:28; md5 verificado). El fix broker FUNCIONA (closes nativos con broker lleno, `unknown_broker` 0 veces).
- Por decisión del owner se consolidó: merge ff a master + push (`c8aa59a4` en origin), rama y worktree eliminados. Prod no fue redeployeado.
- **Nativas siguen sin verse por causas NUEVAS, no por este fix:** (1) opens nativos llegan con `lot_size=0` → core los rechaza (`trade_journal.go:280`; mapeo pendiente EA→bridge); (2) `mv_daily_operations` da 0 filas para TODO hoy (filtro cuenta ACTIVE; 2186 INACTIVE vs 17 ACTIVE). Hasura real: `192.168.31.48:8080` (`.75` obsoleto). Detalle: [[Echo - Discovery y Estado]].
