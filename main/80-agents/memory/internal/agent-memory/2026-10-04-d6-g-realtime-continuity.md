---
type: agent_memory
schema_version: 1
scope: domain
created: 2026-10-04
updated: 2026-10-04
area: "[[Echo Futures]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures]]"
aliases: []
confidence: verified
memory_state: active
continuity_key: domain/echo-futures-d6-g-realtime
supersedes: ""
load_policy: manual
indexable: true
index_priority: medium
tags:
  - agent/internal
  - kind/agent-memory
  - project/echo-futures
  - scope/domain
---

# D6 G-REALTIME — continuidad (2026-10-04)

## Estado al cierre

- `D6_G_REALTIME = PASS` @ `d08a30ce9815f820fda7132e20dc42cc345eb8e8` (C0–H congelado intacto, cero commits/mutaciones, 0 órdenes, G-EGRESS-0 PASS). Artefacto: `10-projects/Echo Futures/artifacts/d6-g-realtime-20261004/D6-G-REALTIME-CERTIFICATION.md` (+ evidence).
- Feed-only: AddOns/feed/relay NUNCA tocados; la única "espera" fue física (reopen CME). MAX event_ts age 0.18 s << bound 30 s sobre 5 muestras; 22,494 eventos QUOTE+TRADE en ventana formal de 18 min.
- Windows/CTL: NT PID 1476, relay PID 1388002 (release `170a4581`), sesiones `5b70e536…` (feed 1.0.0) y `348f52ba…` (exec 2.0.0, account-only, sin ntx).

## Frictions / lecciones transferibles

- El tick de pre-apertura (16:05 CT domingo) engaña en AMBAS direcciones: ni el calendario del artifact (17:00 CT) ni el primer tick son el open real — el stream sostenido con TRADEs es la única prueba; el gate exige movimiento físico, no wall-clock.
- El replay del boot existe SIEMPRE: al reconectar el AddOn republica ~3-7 eventos con event_ts VIEJO (p.ej. viernes 21:38:25.95Z). Excluirlos por event_ts, jamás por receive_ts/offset.
- `consume_messages` del MCP Kafka con `offset_spec=latest` devuelve el último mensaje EXISTENTE (no espera nuevos): probe determinista perfecto para freshness (`event_ts` vs reloj local); `high_watermark` vía `get_consumer_group_offsets` sirve para contar mensajes de un topic (0 = topic vacío).
- ETCD crudo: endpoint en `~/opt/echo-dev/etc/echo-futures-bridge.env` (192.168.31.250-254:2379), `/v3/kv/range` con key base64; el MCP RO lista NOMBRES de claves de forma confiable pero get_value es fuzzy en claves ausentes.
- `pkill/pgrep -f <patrón>` se auto-matches con el propio shell del harness (zsh -c contiene el literal): matar por PID del proceso objetivo, verificar por efecto (log congelado), no por pgrep.
- El project note `Echo Futures.md` (>256 KB) rompe el tool Read incluso con offset: append/patch por bash heredoc.
- Perfil SSH `dev-win` (viewer) rechaza hasta comandos safe; `dev-win-operator` + `run-command` funciona para lecturas (Get-Process OK).

## Siguiente acción (manager)

Ladder físico congelado en **lun 2026-10-05 00:00–15:50 CT** (o evening 17:10–23:59 CT): armar `futures-bridge/accounts=E2T-GAU50-01` + arrancar unidad → barrier venue real → run config → G-STOP → G-ID-Retention → G-HORIZON → G-E2E (+drill) → G-PERF. OD-D6-1 AUTHORIZED sin consumir. No re-ejecutar G-REALTIME salvo anomalía. No emitir `EF_D6_E2E_PASS` hasta ladder completo.
