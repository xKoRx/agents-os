---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — BT-S03 Adversarial Review]]"
aliases: []
tags:
  - kind/doc
  - kind/incident
created: "2026-10-04"
updated: "2026-10-04"
---

# Echo Futures — INC-ETCD-20261004: BT-S03 write a /echo/production/ ETCD — forense y recuperación mínima

## Veredicto

```text
ETCD_INCIDENT_RECOVERY_PASS
```

El incidente **NO alteró ningún valor** del namespace `/echo/production/`: las 32 keys escritas por `TestSeedEchoConfig_Production` a las 14:19:46–48 America/Santiago (revisiones ETCD **59356–59387**, bloque contiguo exacto de 32 escrituras) tenían **valores byte-idénticos** al estado materializado vigente (comprobado contra el historial MVCC completo del cluster: 31/32 keys con un único valor distinto en toda su historia desde la siembra original, revisiones 50000–50030). La única excepción real es `postgres/password`, cuya contaminación (placeholder `test-postgres-password`, 22 chars) **preexistía** al incidente (vigente desde la revisión 56082, re-aplicada por bursts anteriores del mismo seed): el incidente re-aplicó el mismo valor contaminado. Se restauró el credential operativo (10 chars, digest `8a36217243c1…`, presente en la historia desde la siembra original 50030 y re-aplicado manualmente 3×: 58427, 58791, 58875) mediante compare-and-swap probado contra autenticación física de PostgreSQL. Sin secretos expuestos en este documento ni en logs.

## Incident scope

- **Comando:** `go test ./...` desde `v3/sdk` (workspace externo `bt-s03-20261004/echo`, branch `codex/bt-s03-adversarial-review`, base f41da25c). Fuente responsable: `v3/sdk/etcd/echo_seed_test.go::TestSeedEchoConfig_Production` (+ `TestSeedEchoConfig_Development`, corrida en la misma ejecución).
- **Ventana:** 2026-10-04 14:19:46–14:19:48 America/Santiago.
- **Cluster afectado:** ETCD de producción `192.168.31.250..254:2379` (cluster_id `10805131107728833281`) — los endpoints por defecto del SDK (`ETCD_ENDPOINTS` no seteado en el entorno del test) son **exactamente** los mismos que fija `deploy-prod.sh` para los servicios productivos. Namespace `/echo/production/` (prefijo `/<app>/<env>/`).
- **Mecanismo de escritura:** el seed itera un mapa hardcodeado de 32 keys (`productionEchoConfig()`) con `SetVar`. La corrida de ese `go test ./...` escribió **ambos namespaces**: dev (revisiones 59328–59349, también valores idénticos al estado vigente) y producción (59356–59387).
- **Key 32ª reconstruida:** el resumen S03 capturó 31 nombres; la faltante es `telemetry/metrics/enabled` (presente en 59361, valor igual al mapa del test). 32/32 reconciliadas.

## Key reconciliation

Método: lectura MVCC histórica por key (rango con `revision` descendente) contra el cluster, sin `etcdctl` (API HTTP v3). 37 keys en `/echo/production/`.

| Grupo | Cantidad | Estado |
| --- | --- | --- |
| Tocadas por el incidente | 32 | — |
| → UNCHANGED_OR_ALREADY_CORRECT (valor único en toda la historia, igual al escrito) | 31 | sin acción |
| → Restauradas (contaminación probada + reemplazo demostrado) | 1 (`postgres/password`) | CAS 59386→59390 |
| → LEGITIMATELY_CHANGED_AFTER_INCIDENT | 0 | — |
| → AMBIGUOUS | 0 | — |
| No tocadas (tokens `gateway/auth/*` ×4 + `gateway/cors_allowed_origins`, mods 59077–59086, previas al incidente; el seed no las escribe ni borra keys) | 5 | intactas |
| `bridge/reference_accounts` / `bridge/execution_accounts` | — | nunca existieron en producción (coherente con el readback fallido del test; no son omisión del incidente) |

Patrón histórico relevante (contexto, no acción): el namespace producción viene siendo reescrito periódicamente con los valores del seed en bursts contiguos de 32 revisiones (bloque A: 59275–59306, intercalado con el staging D6 59217–59309; y anteriores hasta ≈56275). Tras cada burst, `postgres/password` fue corregido manualmente como escritura single-key (58427, 58791, 58875 — mismo digest `8a36217243c1…`). Desde el burst 59129 el placeholder quedó vigente sin corrección posterior hasta esta restauración. El autor de los bursts y de las correcciones manuales no es atribuible desde ETCD (sin audit log); el Owner puede correlacionar con logs de sesión.

### postgres/password — receipt sanitizado

- Pre-escritura: `mod_revision=59386`, `len=22`, `sha256_12=13b1fa3ec5cf` (placeholder del test).
- Fuente del reemplazo: historia MVCC del cluster, valor en revisión 58875 (última corrección manual; mismo digest que la siembra original 50030).
- Prueba de contaminación: `echo_user` @ `192.168.31.220:5432` rechaza el placeholder (fallo físico observado en `TestScratch_QueryDB` durante la corrida del incidente; credenciales hardcoded del test, ETCD-independiente).
- Prueba del reemplazo: sondeo de autenticación read-only (`SELECT 1`) contra la PG de producción con el valor recuperado → `AUTH_OK`; placeholder → `auth_fail`.
- Escritura: txn CAS `compare mod_revision==59386 → put`; `succeeded=true`, `put_revision=59390`. Post-lectura: `mod_revision=59390`, `len=10`, `sha256_12=8a36217243c1`. Probe end-to-end con el valor vigente en ETCD → `AUTH_OK`.

## Verification (read-only)

| Superficie | Resultado |
| --- | --- |
| ETCD `/echo/production/` (37 keys, listing completo post-restore) | Sólo `postgres/password` cambió (59390); resto en revisiones del incidente con valores byte-idénticos al pre-incidente; tokens/cors intactos |
| ETCD `/echo/` post-incidente | Cero keys con `mod_revision ≥ 59388` en todo `/echo/` salvo la restauración (59390) |
| PostgreSQL auth | `AUTH_OK` con el valor restaurado, contra `echo` (producción) en `.220` |
| Kafka | Los 3 brokers de `kafka/brokers` (`.247/.248/.249:9092`) REACHABLE (config vigente = infraestructura viva) |
| Telemetry endpoints | `.60:14317` y `.60:4317` REACHABLE |
| Jaeger dev (`192.168.31.45`) | Preexistente caído/inalcanzable — fallo del probe SDK es ETCD-independiente (endpoints hardcoded) y NO fue causado por el incidente |
| Consumidores en `.71` (unidades systemd core/gateway) | **No verificado** — perfil SSH viewer sin `read-command` operativo (roto) ni `run-command` (policy). Limitación aceptada: el único valor que consumiría en un restart es el ya probado por auth física |
| Órdenes / execution egress / NinjaTrader / D6 gate | No tocados (fuera de alcance por mandato) |

## D6 concurrency

- HEAD inicial y final (fetch antes y después): `origin/feature/d6-shot1-execution-vertical` = `d08a30ce9815f820fda7132e20dc42cc345eb8e8` (commit 14:31:12 -03, 12 min después del incidente). Carril Backtester: `origin/feature/backtester-v1-s02` = `f41da25cc0b779ea48375198dbedaf932b930a80` (13:17:33 -03). Sin movimientos.
- Keys D6 `/echo/development/futures-bridge/*` (staging 59217–59309): intactas; el seed no escribe ese prefijo y ningún burst las tocó. El bloque A de producción (59275–306) quedó intercalado con el staging D6 sin colisión de keys.
- Única mutación del mandato: `/echo/production/postgres/password` (CAS probado). Ningún merge/cherry-pick. Cambios legítimos posteriores al incidente que preservar: ninguno detectado en `/echo/`.

## Prevention (recomendaciones, test-safety puro)

1. **Build tag** en `v3/sdk/etcd/echo_seed_test.go` (y homólogos v1/v2), p.ej. `//go:build seeds`: excluye ambos seeds de `go test ./...` sin bandera explícita. Cambio mínimo, exclusivamente test-safety → dejarlo para el mandato S04.
2. **Env guard** dentro del seed: abortar salvo `ECHO_SEED_ALLOW=production` explícito; **endpoint guard**: negarse si el endpoint resuelto es el cluster `.250-.254` sin override.
3. **Agentes:** mantener la regla ya aplicada en S03 (listas de paquetes explícitas + aislamiento de red `unshare --net` con sólo loopback en suites de agentes); añadir `v3/sdk` a la lista de módulos vetados para `go test ./...` por el gerente de shots.
4. **Dato para el Owner:** existe un re-materializador periódico (o corridas repetidas del seed) que escribe `/echo/production/` con el placeholder; mientras no se corrija la fuente (1), el password puede volver a ser clobbered en el próximo burst. La corrección manual single-key (patrón 58427/58791/58875) debería reemplazarse por fijar el credential real en esa fuente.

## Fuentes

- S03: `bt-s03-20261004/reports/incident.md` (workspace externo), [[Echo Futures — BT-S03 Adversarial Review]] §Incidente.
- Source: `xKoRx/echo` `v3/sdk/etcd/echo_seed_test.go`, `v3/sdk/etcd/client.go` (endpoints/prefijo), `v3/sdk/postgres/scratch_query_test.go`, `v3/sdk/telemetry/dev_jaeger_probe_test.go`, `deploy-prod.sh`.
- ETCD producción: historial MVCC vía API HTTP v3 (`.250/.251/.252:2379`), revisiones 50000–59390.
- Git: `origin/feature/backtester-v1-s02@f41da25c`, `origin/feature/d6-shot1-execution-vertical@d08a30ce`.
