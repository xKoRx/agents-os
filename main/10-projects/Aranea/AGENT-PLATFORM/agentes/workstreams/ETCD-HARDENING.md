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

> Componente de [[AGENT-PLATFORM - MCP Access Plane]], NO proyecto paralelo. Esta nota gobierna la deuda de seguridad del CLUSTER etcd y el incidente previo, no el estado de deployment del MCP. **Reconciliación temporal 2026-09-17:** la decisión inicial de NO autorizar greenfield fue supersedida posteriormente por el mandato del MCP-trio que autorizó un gateway estrictamente RO y la certificación `aranea-etcd-ro :3012`. El deployment MCP está ACTIVE/CERTIFIED; TLS/auth/RBAC y rotación del cluster siguen ABIERTOS y OWNER-GATED. No mezclar los dos veredictos. Contrato client-facing en [[aranea-etcd-mcp]] y matriz [[Daedalus — Development Agents MCP Access & Gaps]].

## Estado vigente (corte 2026-09-17)

```text
INCIDENTE PUT ACCIDENTAL:   CONTAINED / ROLLBACK VERIFIED / NO DATA LOSS
ETCD-EXP-01:                OPEN HIGH — cluster :2379/:2380 LAN, sin TLS/auth
aranea-etcd-ro MCP :3012:  ACTIVE/CERTIFIED — server 13/13 y Cursor consumer PASS
MCP MUTATORS:               NONE (cuatro tools exclusivamente de lectura)
CLUSTER HARDENING:          PENDING / OWNER-GATED
ROTACIÓN CREDENCIALES:      PENDING / OWNER-GATED según inventario
```

**Hechos físicos de cluster verificados en discovery (NO re-probados en esta reconciliación documental):** un cluster de 5 members etcd 3.6.4/3.6.0, cluster_id `10805131107728833281`, athena `.254`, zeus `.250`, hera `.251`, kronos `.252`, hades `.253`; :2379 client y :2380 peer abiertos al LAN `192.168.31.0/24`, `authRevision=1` con auth DISABLED, sin TLS. SSH no expuesto en LXCs; configuración vía consola PVE owner. Inventario baseline 985 keys en 13 prefijos; 63 keys con nombres y contenido de credenciales en claro. No transcribir valores al vault ni a prompts.

## Incidente 2026-09-17 — escritura accidental PROD (histórico, mitigado)

Probe planificado como negativo `kv/put` de `aranea-test=x` fue aceptado porque el cluster no tenía auth. Revisiones 55031 antes → 55032 después. Rollback exacto `kv/deleterange` de esa key ⇒ `deleted:1`, rev 55033; readback count 0, sweep 985 keys igual al baseline, health true en los cinco members, sin keys aranea residuales. Primera tentativa de delete usó equivocadamente slash inicial en la key base64, `deleted=0`; luego key exacta y éxito. Regla durable: **en servicio sin enforcement, nunca usar mutador como prueba negativa; verificar auth/status por READ**. Skill `mcp-access-plane-operations` y feedback de sesión registraron la lección.

## Exposición ETCD-EXP-01 — alcance documentado, no redistribuir valores

La investigación identificó 63 claves con nombres de credenciales (no se extrajeron ni imprimieron sus valores): MinIO `access_key`/`secret_key` y PostgreSQL `password` en ramas como `/sqx-worker`, `/sqx-watcher`, `/sqx-flowkit`, `/sqx-mt5-worker`, `/sqx-worker-backup`, `/deployer-watcher`, `/deployer`, `/symphony`, `/echo`, `/demo` y `/minio-example`. La rama `/deployer-watcher/development/minio` y variantes malformadas también fueron identificadas. El servicio responde range de claves desde hosts del LAN, demostrado desde `mcps`, Daedalus y Hermes VM; :2380 abre además superficie peer. Esto no implica afirmar exfiltración; sí exposición potencial demostrada. La allowlist/redacción del MCP RO limita a **agentes consumidores del MCP**, no corrige el cluster abierto ni autoriza acceso directo.

Los consumidores dependen de la configuración dinámica en esos prefijos: sqx-worker, sqx-flowkit, symphony, sqx-watcher, deployer-watcher, echo, sqx-mt5-worker, sqx-worker-backup, deployer y fixtures demo/minio-example. Rotar, cambiar rutas o habilitar auth de golpe puede romperlos: hardening es migración por etapas, nunca un flip improvisado.

## Mitigación y hardening (propuesta, NO ejecutada)

1. **Inventario previo de consumidores legítimos:** conexiones efectivas a :2379 desde hosts SQX/Echo/deployer y miembros, por management paths autorizados; incluir `etcd-keeper` si realmente usado. Registrar origen, servicio, dependencia, prefijo y rollback.
2. **Contención de red reversible:** allow client :2379 sólo desde consumidores verificados y administración, deny+log del resto; peer :2380 únicamente membresía `.250-.254` y peers necesarios. Verificar según topología PVE/OPNsense real: un firewall LAN que no ve tráfico L2 intra-LAN no garantiza contención; usar el punto de enforcement efectivo. Esto NO sustituye TLS/auth y no es un cambio automático del MCP.
3. **Snapshot consistente previo** del cluster, verificada restaurabilidad, antes de tocar TLS/auth.
4. **TLS por member:** CA interna, cert/key/CA client+peer, roll uno por uno preservando quorum >=3; owner/consola PVE y rollback probado.
5. **auth/RBAC con identidades por servicio:** cada consumidor sólo prefijos/verbos propios; credencial MCP RO separada; migrar consumidores secuencialmente, no bloquear todos a la vez.
6. **Rotar credenciales comprometidas/expuestas** MinIO/PostgreSQL tras cerrar acceso anónimo y actualizar servicios con gates individuales.
7. **Re-certificar `aranea-etcd-ro`** después del hardening con identidad autenticada dedicada, tools 4/4, allowlist/negative probes, server+Cursor/ZCode/Codex según necesidad; no crear write capability por defecto.

Fuera de scope: cambios de membership, downgrade/upgrade, reubicación de members, exposición por Internet. Cada cambio exige owner gate, ventana, backup/rollback y health + consumidor smoke. No atribuir estas tareas al coding agent por tener una capability RO.

## Fuentes / evidencia

- [[aranea-etcd-mcp]] — MCP ACTIVE server+Cursor 2026-09-17, cuatro tools RO, ocho prefijos allowlisted, secret-names excluidos, 200 keys/4KB, sin write/watch.
- `80-agents/journal/logs/2026-09-17-mcp-trio-temporal-minio-etcd.md` — discovery/incident/historia inicial.
- `80-agents/journal/feedback/system-1/2026-09-17-aranea-mcp-trio-session-feedback.md` — lección sobre probes negativos.
- Skill `mcp-access-plane-operations` — safety de operación etcd.
- `~/aranea/work/mcp-trio/etcd-reconciliation.md` en Hermes VM — upstream evaluation previa. No almacenar secretos en estas notas.
