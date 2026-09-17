---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-17"
updated: "2026-09-17"
aliases:
  - "ETCD — Seguridad y Hardening — workstream del MCP Access Plane"
tags:
  - area/aranea
  - tech/etcd
  - kind/workstream
  - priority/high
---

# ETCD — Seguridad y Hardening — workstream del MCP Access Plane

> Componente de [[AGENT-PLATFORM - MCP Access Plane]], no proyecto paralelo. Gobierna la deuda de seguridad del CLUSTER etcd y un incidente histórico, NO el despliegue del MCP. Reconciliación 2026-09-17: la no-autorización inicial de greenfield fue supersedida por el mandato MCP-trio que autorizó un gateway estrictamente RO y certificó `aranea-etcd-ro :3012`. El **MCP está ACTIVE/CERTIFIED**; TLS/auth/RBAC/rotación del cluster siguen OPEN/OWNER-GATED. No mezclar ambos veredictos. Contrato agent-facing: [[aranea-etcd-mcp]]; matriz Daedalus: [[Daedalus — Development Agents MCP Access & Gaps]].

## Estado vigente

```text
INCIDENTE PUT ACCIDENTAL:   CONTAINED / ROLLBACK VERIFIED / NO DATA LOSS
ETCD-EXP-01:                OPEN HIGH — cluster :2379/:2380 LAN sin TLS/auth
aranea-etcd-ro MCP :3012:  ACTIVE/CERTIFIED — server 13/13 y Cursor consumer PASS
MCP MUTATORS:               NONE (cuatro tools lectura)
CLUSTER HARDENING:          PENDING / OWNER-GATED
ROTACIÓN CREDENCIALES:      PENDING / OWNER-GATED
```

**Discovery físico previo (no re-probado al reconciliar documentos):** un cluster de cinco members etcd 3.6.4/3.6.0, cluster_id `10805131107728833281`: athena `.254`, zeus `.250`, hera `.251`, kronos `.252`, hades `.253`; :2379 client y :2380 peer abiertos a LAN `192.168.31.0/24`; auth DISABLED, sin TLS. LXC sin SSH :22: configuración por consola PVE owner. Baseline 985 keys en 13 prefijos; 63 keys con credenciales en claro. No transcribir valores al vault ni prompts.

## Incidente 2026-09-17 — histórico y mitigado

Probe negativo `kv/put aranea-test=x` resultó ACEPTADO porque auth estaba deshabilitada. Revision 55031 pre → 55032 post. Rollback exacto `kv/deleterange` de esa key `deleted=1`, rev 55033; readback count 0, sweep 985 keys = baseline, health true 5/5 members, cero keys `aranea` residuales. Primer delete usó slash inicial erróneo en preimage base64 (`deleted=0`); segunda ejecución usó key correcta. Regla durable: **no realizar mutadores como pruebas negativas en superficies sin enforcement; verificar por READ auth/status**. Registrado en `mcp-access-plane-operations` y feedback de sesión.

## Exposición ETCD-EXP-01

Por nombres de keys, 63 entradas contienen MinIO `access_key`/`secret_key` y PostgreSQL `password` en ramas `/sqx-worker`, `/sqx-watcher`, `/sqx-flowkit`, `/sqx-mt5-worker`, `/sqx-worker-backup`, `/deployer-watcher`, `/deployer`, `/symphony`, `/echo`, `/demo`, `/minio-example`; incluye branch `/deployer-watcher/development/minio` y variantes malformadas. No se leyeron ni imprimieron los valores en la investigación. Range arbitrario en :2379 era alcanzable desde mcps, Daedalus y Hermes VM; :2380 también es superficie peer. Exposición potencial demostrada, NO asumir exfiltración.

Consumidores de configuración dinámica: sqx-worker, sqx-flowkit, symphony, sqx-watcher, deployer-watcher, echo, sqx-mt5-worker, sqx-worker-backup, deployer, demo/minio-example. Cambiar claves, prefijos, TLS o auth sin migrar consumidores puede romperlos; hardening por etapas con respaldo/quorum, no flip improvisado. La allowlist del MCP RO protege SU consumidor, no corrige el cluster abierto ni autoriza acceso directo.

## Mitigación y hardening propuesto, NO ejecutado

1. Descubrir conexiones efectivas client :2379 y peer :2380 desde hosts y servicios legítimos por management paths autorizados; incluir etcd-keeper sólo con prueba. Registrar servicio/prefijo/host/rollback.
2. Contención red reversible: allow :2379 sólo consumidores reales, :2380 tráfico peer necesario, deny+log resto. Verificar punto de enforcement efectivo (OPNsense LAN puede no ver tráfico L2 intra-LAN; usar PVE/host según topología). Contención no sustituye TLS/auth.
3. Snapshot consistente, restauración comprobada antes de intervenir.
4. TLS por miembro con CA interna, client/peer cert, rolling preservando quorum ≥3; ventana owner + rollback.
5. auth/RBAC con credenciales por servicio y roles por prefix/verbs; identidad MCP RO separada; rollout gradual de consumidores.
6. Rotar credenciales MinIO/PostgreSQL expuestas después de cerrar acceso anónimo, migrar dependencias una a una con verificación.
7. Re-certificar `aranea-etcd-ro` contra cluster autenticado (toolset 4, prefix filters, negatives, server+cliente exacto); no introducir RW automáticamente.

Fuera de scope: member changes, downgrade/upgrade, reubicación de hosts, publicación Internet. Todo cambio exige gate owner/ventana/rollback/health. Coding agents NO reciben root/admin porque ya exista un MCP read-only.

## Evidencia y fuentes

[[aranea-etcd-mcp]] — MCP ACTIVE server+Cursor 2026-09-17 (4 tools, ocho prefixes, secret-names denegados, max 200 keys/4KB); `80-agents/journal/logs/2026-09-17-mcp-trio-temporal-minio-etcd.md` (discovery, incidente e historia inicial); `80-agents/journal/feedback/system-1/2026-09-17-aranea-mcp-trio-session-feedback.md` y skill `mcp-access-plane-operations` (lección probes negativos); `~/aranea/work/mcp-trio/etcd-reconciliation.md` en Hermes VM (upstreams evaluados). Ningún secreto se persiste aquí.