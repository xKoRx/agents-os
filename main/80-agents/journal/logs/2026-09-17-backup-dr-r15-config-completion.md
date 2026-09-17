---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
  - "[[agent-project-01-critical-config-backup]]"
tags:
  - kind/change-log
  - area/aranea
  - project/backup-dr
  - domain/backup-dr
---

# 2026-09-17 — Backup/DR R1.5: corrección D0 + completación config + automatización

## Mandato

Owner one-shot (mensaje único = autorización explícita): corregir dos residuos documentales D0, resolver unidades config pendientes por canales autorizados, backups reales, restores/drills a scratch, automatizar schedules frozen de backup-policy.yaml. Sin session close.

## Parte 1 — Correcciones D0 (§1)

- **RC-20260917-001**: contradictorio "requiere aprobación owner aparte" (change log D0, sección Nuevo) vs "APROBADO y aplicado" (verificación final). Corregido: sección Nuevo reescrita (estado final APPROVED + APPLIED, explicando que la aprobación vino con el paquete D0 v2); REQUEST-CHANGES.md alineado (`owner_decision` ya no "pendiente", footer ya no "vacío al cierre"). Evidencia y decisiones intactas.
- **Session-close no autorizado**: D0 dejó L0 `sessions/raw/2026-09-17-backup-dr-d0-doc-consistency-raw`, L1 `sessions/2026-09-17-backup-dr-d0-doc-consistency-summary`, feedback y L3 continuity (mecánica de cierre sin session close). Reclasificación mínima: L0/L1 conservados con callout de clasificación (evidencia del workload D0 completado, proyecto sigue ACTIVE); L3 conservada como delta note y actualizada; feedback conservado. Ningún artefacto borrado; ninguna señal autoritativa de "session closed" queda sin corregir.
- Validación: cero contradicciones RC (grep), proyecto Backup/DR ACTIVE en owner project y agent-project-01, D0 continúa PASS.

## Parte 2 — Access Plane: capacidades reales medidas (§4)

- **etcd :2379 es alcanzable desde hermes-vm** (corrección de R1, que lo registró "filtrado desde LAN"): los 5 members responden `GET /version` (server 3.6.4, storage 3.6.0). R1 no lo probó desde hermes. No se abrió ningún puerto ni se tocó el cluster.
- **pi-hole .149 está muerto a nivel L2**: ARP `FAILED` visto desde athena (su propio hipervisor); sin ICMP/22/53/80/443 ni desde hermes ni desde mcps. DNS del LAN hoy resuelve via 192.168.31.31 (no .149). Coherente con que pvesh lo muestre running: contenedor vivo pero sin respuesta de red. Hallazgo operativo para el owner (posible fw/ct no arrancado).
- **agent_ro funciona en los 5 nodos PVE** (wrapper `/usr/local/sbin/agent-read` idéntico, md5 592422e6d24d0acb13f04dba5af9b0fd, secciones node/network/storage/proxmox/ceph/services; sin sección `config`); `/usr/local/sbin` NO escribible para agent_ro → la extensión del wrapper requiere root (no auto-instalable). Root SSH sigue fail-closed (probe con agent_ro, agent_pve_create_athena y agent_ca_root: Permission denied — correcto).
- `agent_ca_root` es una llave ed25519 scoped al LXC ca (bootstrap step-ca, hoy stopped), no una CA de host SSH.
- pvesh sin credenciales no sirve (ipcc errors); configs node-local (`/etc/network/interfaces`, hosts, hostname) SÍ legibles por agent_ro en los 5 nodos.

## Parte 3 — Unidades (§3)

### etcd-snapshot: BACKUP + RESTORE VERIFIED, AUTOMATED

- Tooling: `~/aranea/bin/etcd-tools/{etcdctl,etcdutl}` v3.6.4 instalado en Hermes desde release oficial etcd-io (== server 3.6.4, doc oficial aplicable; no abre puertos, no toca el server). apt ofrece 3.4.x (incompatible) — descartado.
- Pre-checks del run: `endpoint health` 5/5, `endpoint status` (quorum íntegro, leader .254, rev 55740), `endpoint hashkv` idéntico en los 5 members (459293923 / rev 55033).
- Snapshot del cluster (1 archivo, member .254): `etcd-cluster-snapshot.db` 5.1MB, etcdutl verify: rev 55033, 985 keys, hash b9c58878. sha256 registrado. Nada fue escrito en el cluster (snapshot save es lectura).
- Drill: `etcdutl snapshot restore` a data-dir temporal (nunca miembro), status del db restaurado rev 55033/985 keys; scratch eliminado. Evidencia: `restore-drill.json` en runs 20260917-153323 (primero) y 20260917-153932 (del timer).

### pve-config: node-local BACKUP + RESTORE VERIFIED (5/5), AUTOMATED; pmxcfs GATED

- Por nodo (agent_ro, read-only): tar de `/etc/network/interfaces + /etc/hosts + /etc/hostname`; drill de restore con sha256 restaurado == vivo en los 5/5 nodos (run 20260917-153934).
- pmxcfs (`/etc/pve`): ilegible sin root (dirs 750 root:www-data; agent_ro sin grupo) y sin canal para instalar la extensión `agent-read config` — GATED owner (bundle §4). El script `r15-pve-config.sh` ya lleva el contrato: cuando el owner instale la sección `config` (tar.gz por stdout), la captura y el manifest cambian a CAPTURED sin nuevas ediciones.

### traefik-config: cobertura ampliada, BACKUP + RESTORE VERIFIED, AUTOMATED

- Nuevo en el wrapper: drop-in systemd `traefik.service.d/` (incluye `cloudns.conf`, 644 en el LXC, con las env del proveedor DNS del dnsChallenge letsencrypt) — indispensable para re-emitir `acme.json`; guardado 600.
- Drill: 11/11 archivos restaurados con sha256 == fuente viva del LXC (incluye cloudns.conf; valores de env nunca cruzaron el canal).
- Análisis recovery: dynamic configs no referencian certificados externos; los únicos secretos TLS son `ssl/acme.json` (re-emisible con el drop-in: NO recovery-critical) y `ssl/acme-stepca.json` (CA en lxc-200 STOPPED: NO re-emisible hoy → recovery-critical, gated owner). `secrets/` sin referencias desde configs → no copiado por costumbre.

### pi-hole: NO resuelto — OWNER GATE REAL (doble causa)

- Agotado el Access Plane (§4): sin HTTP desde hermes/mcps/athena, L2-dead desde su propio hipervisor, sin SSH (22 filtered/no-route), sin api_token FTL en ningún canal autorizado. Además el propio servicio está caído en red: ni un export con token sería posible hoy. GATED owner: requeriría root/consola en LXC 149 (o restaurar su red) + api_token para Teleporter v6.

### second-brain y hermes-state

- Sin repetición de drills (evidencia R1 válida, sin modificaciones que los afecten). Sanity en el run nuevo: config.yaml YAML válido, unit túnel con ExecStart, manifests con sha256 completos (fix del bug cosmetic: los 3 artefactos hermes-state registraban sha256 null en R1; ahora el fallback lee hermes-state.sha256).

## Parte 4 — Automatización (§8, schedules frozen literal)

- Unidades instaladas en hermes-vm (sudo NOPASSWD verificado; `systemctl enable --now`, Persistent=true):
  - `aranea-backup-r1.timer` → `*-*-* 04:00:00` (jobs.traefik_config_backup DAILY 04:00; second-brain/hermes-state viajan en el mismo run, documentado en la unidad).
  - `aranea-etcd-snapshot.timer` → `*-*-* 05:00:00` (jobs.etcd_snapshot DAILY 05:00).
  - `aranea-pve-config.timer` → `Sat *-*-* 08:30:00` (jobs.etc_pve_backup WEEKLY SAT 08:30).
- Semántica verificada con `systemd-analyze calendar` (next elapse 2026-09-18 04:00/05:00, 2026-09-19 08:30 -03). Horarios intactos; backup-policy.yaml intacto.
- Prueba real SIN esperar días: cada unidad ejecutada manualmente vía `systemctl start <service>` (la unidad exacta del timer), exit 0, journal consultable (`journalctl -u ...`). Scripts: `~/aranea/bin/r1-backup.sh` (ampliado), `r15-etcd-snapshot.sh` (nuevo, con pre-checks quorum/hashkv y fallback de member), `r15-pve-config.sh` (nuevo, nodo-local + contrato pmxcfs).
- Registro consolidado append-only sin secretos: `manifest-etcd.jsonl`, `manifest-pve.jsonl` + `manifest.json`/`restore-drill.json` por run.
- Second-brain/hermes-state/pi-hole: `SCHEDULE_NOT_FROZEN` (sin frecuencia frozen propia; viajan en el run 04:00 los dos primeros — justificado en la unidad del timer, sin cambiar el significado de la policy).

## Parte 5 — Drills y staging

- Drills ejecutados a scratch, cero toques a producción: traefik 11/11 (run 20260917-154236), pve node-local 5/5 (153934), etcd rev 55033 (153932 + 153323), sanity hermes-state (154236). Scratch eliminado post-evidencia en todos.
- Staging: `~/aranea/backup-staging/` 194MB (16GB libres en /, uso 44%). Sin pruning (§9: staging explícitamente temporal, R2 lo sustituye; NO es deuda documental).

## GATES OWNER VIGENTES (consolidados, §12/§15)

1. **pmxcfs `/etc/pve`**: instalar sección `config` (tar.gz por stdout) en `/usr/local/sbin/agent-read` de los 5 nodos — requiere root; el pipeline de captura ya está armado.
2. **traefik `ssl/acme-stepca.json`** (+ revisión de `secrets/`): canal root a LXC 115.
3. **pi-hole**: doble causa — servicio muerto en red (hallazgo operativo) + api_token FTL/canal root a LXC 149.

Correcciones de drift documental (R1 → medido hoy): ":2379 filtrado desde LAN" (falso para hermes), "pi-hole sin ping/HTTP" (ahora con causa L2 demostrada desde athena), "pi-hole DNS en 149" (hoy el LAN resuelve via .31).

## No hecho (explícito)

- Sin cambios a CONTRACT/policy/F-*; sin R2/PBS; sin vzdump/dumps DB; sin Ceph/storage mutation; sin Echo; sin session close. Tickets 018-021 intactos.
