---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-17"
updated: "2026-09-17"
tags:
  - area/aranea
  - tech/etcd
  - kind/workstream
  - priority/high
---

# ETCD — Seguridad y Hardening — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]]. **No es un proyecto paralelo.**
>
> Registro del incidente de escritura accidental en PROD (2026-09-17), del hallazgo de exposición de credenciales, y del workstream de hardening (TLS, auth/RBAC, rotación). El MCP etcd greenfield quedó **NO AUTORIZADO** por el owner (2026-09-17); este workstream cubre la seguridad del cluster, no el access plane.

## Estado

```text
INCIDENTE 2026-09-17:   CONTAINED / ROLLBACK VERIFIED (sin pérdida de datos)
HALLAZGO ETCD-EXP-01:   OPEN — HIGH (cluster sin auth/TLS expuesto a todo el LAN,
                        incl. 63 keys con credenciales en claro)
GREENFIELD ETCD MCP:    NO AUTORIZADO (owner 2026-09-17)
HARDENING (TLS+RBAC):   PENDING / OWNER-GATED (workstream separado)
```

## Cluster afectado (identidad física verificada 2026-09-17)

```text
cluster:  UNO — cluster_id 10805131107728833281, etcd 3.6.4 / etcdcluster 3.6.0, healthy
members:  athena 192.168.31.254 · zeus .250 · hera .251 · kronos .252 · hades .253
          (VMIDs topología: 101/147/154/155/156; los puertos son por IP real, no VMID)
puertos:  :2379 client + :2380 peer — AMBOS abiertos a todo el LAN 192.168.31.0/24
auth:     authRevision=1 → auth DISABLED; sin TLS (plaintext)
SSH:      los LXC no exponen :22 → configuración sólo accesible vía consola PVE (owner)
keys:     985 en 13 prefijos; 63 contienen credenciales en claro (ver § Exposición)
```

## Incidente 2026-09-17 — escritura accidental en PROD

- **Qué:** durante discovery del mandato MCP-trio, un probe pensado como "negativo" (`kv/put` de la key `aranea-test` con valor `x`) fue **aceptado** por el cluster porque auth está deshabilitada. Revisiones: 55031 (pre) → 55032 (post-put).
- **Por qué ocurrió:** se asumió que un servidor rechazaría escrituras anónimas. En un server sin auth no existen probes negativos de escritura: todo `put/delete/txn` es una mutación real. Regla añadida a la skill `mcp-access-plane-operations`: el enforcement se demuestra con un READ (`auth/status`), jamás ejecutando el mutador.
- **Rollback (verificado):** `kv/deleterange` de la key exacta → `deleted:1`, rev 55033; re-read `count=0`; sweep completo de keys → **985 = baseline pre-incidente** (idéntico); `/health` → `true` en los 5 members. Cero keys residuales con `aranea` en el nombre. Nota: la primera tentativa de delete usó base64 con `/` inicial por transcripción (key inexistente, deleted=0); corregido a la key exacta sin slash.
- **Lección durable:** skill actualizada (gotcha "probes negativos en superficies sin enforcement = mutaciones reales") + feedback de sesión (`80-agents/journal/feedback/system-1/2026-09-17-aranea-mcp-trio-session-feedback.md`).

## Exposición de credenciales (ETCD-EXP-01)

Keys que **contienen** credenciales en claro (mapeo por nombre — valores jamás leídos ni impresos por el agente):

- MinIO `access_key`/`secret_key`: `/sqx-worker/{development,f03cert,production}`, `/sqx-watcher/{development,f03cert,production}`, `/sqx-flowkit/{development,production}`, `/sqx-mt5-worker/production`, `/sqx-worker-backup/production`, `/deployer-watcher/{development,production}` (incluye variante malformada `deployer-watcher/productionminio/…`), `/deployer/development`, `/symphony/{development,integration_test,local,production}`, `/minio-example/development`, `/demo/local`
- PostgreSQL `password`: `/echo/{development,production}`, `/sqx-worker/…`, `/sqx-watcher/…`, `/sqx-flowkit/…`, `/symphony/…`, `/demo/local`

**Alcance de lectura:** cualquier host del LAN puede `range` completo sobre `:2379` (verificado desde mcps .219, daedalus .161 y hermes-vm). Con `:2380` abierto además existe superficie de operaciones de membership para quien hable el protocolo peer.

**Servicios que dependen de estos prefijos** (config dinámica en etcd): sqx-worker, sqx-flowkit, symphony, sqx-watcher, deployer-watcher, echo, sqx-mt5-worker, sqx-worker-backup, deployer, demo, minio-example. Cambiar claves/valores o habilitar auth sin migrar estos consumidores los rompe — por eso el hardening es un workstage con migración, no un flip.

## Contención de red propuesta (NO implementada — requiere owner)

Objetivo: dejar `:2379` alcanzable **sólo** desde los hosts que legítimamente lo consumen, sin tocar los LXC (no hay SSH) y sin romper consumidores.

1. **Inventario de consumidores reales (owner, ~15 min):** en cada host que corre los servicios SQX/echo/deployer, identificar el origen de las conexiones a :2379 (`ss -tnp | grep 2379` en Zeus/Hera/Kronos/hades vía agent_ro; los PVE sí tienen canal). Sospechosos legítimos: los propios VMs/LXC que corren los servicios listados arriba y `etcd-keeper` (.148) para la UI.
2. **Reglas OPNsense (reversibles, auditadas):** en el LAN interface, allow `:2379/:2380` sólo hacia `.250-.254` desde la lista de consumidores del paso 1 + mcps (futuro) + etcd-keeper; **deny log** para el resto del LAN. `:2380` debería permitir además tráfico member↔member entre `.250-.254` (los 5 se hablan entre sí por peer port). Estado actual = implícito allow-all; la contención es un cambio de firewall de blast radius medio → **GATED owner**, con ventana y rollback (desactivar reglas).
3. **Verificación post-contención:** probes TCP desde un host no-listed (debe fallar) y desde cada consumidor listado (debe pasar); health de los 5 members; smoke de un servicio SQX de los que lean etcd.
4. **No sustitutivo:** bloquear red NO sustituye auth/TLS (cualquier host permitido sigue pudiendo escribir); es reducción de superficie mientras el hardening se ejecuta.

## Workstream de hardening (propuesto, owner-gated, separado)

Fases sugeridas (cada una con ventana, rollback y verificación propia):

- **F1 — snapshot previo:** UNA snapshot del cluster vía gateway v3 HTTP desde mcps (host de staging `~/aranea/backup-staging`) antes de tocar nada. Precondición de todo lo demás.
- **F2 — TLS:** certificados internos (step-ca ya existe en el homelab) para los 5 members + clientes; reinstalar members con `--trusted-ca-file/--cert-file/--key-file/--client-cert-auth` (requiere recrear los LXC o consola PVE; ventana con quorum: NUNCA <3 members vivos, hacer member por member).
- **F3 — auth/RBAC:** `auth enable` + usuario admin + roles por prefijo (least-privilege: cada servicio con role readonly sobre su prefijo; escritura sólo para el servicio que la posee). Requiere emitir credenciales a cada consumidor (F2 antes).
- **F4 — rotación de credenciales expuestas:** tras F3, rotar las 63 credenciales (MinIO access keys y PostgreSQL passwords) que estuvieron legibles en claro; actualizar consumidores por servicio.
- **F5 — re-evaluación del MCP etcd:** con auth+TLS activos, un `aranea-etcd-ro` con credencial dedicada y allowlist de prefijos vuelve a ser evaluable (greenfield sigue requiring decisión owner; con cluster endurecido el riesgo residual baja).

Fuera de scope de este workstream: membership changes, downgrade/upgrade de versión, re-ubicación de members.

## Evidencia

- Change log del mandato: `80-agents/journal/logs/2026-09-17-mcp-trio-temporal-minio-etcd.md`
- Skill local (gotchas): `mcp-access-plane-operations` § etcd cluster Aranea
- Feedback: `80-agents/journal/feedback/system-1/2026-09-17-aranea-mcp-trio-session-feedback.md`
- Reconciliación MCP-etcd (upstreams descartados): `~/aranea/work/mcp-trio/etcd-reconciliation.md` (hermes-vm)
