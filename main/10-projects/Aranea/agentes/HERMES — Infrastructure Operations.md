---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Aranea]]"
parent: "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
sprint:
start: 2026-09-14
due:
progress: 45
repo:
jira:
prs:
slug: hermes-infrastructure-operations
aliases:
  - Hermes Infrastructure Operations
  - Hermes Homelab Administration
  - Hermes Infra Ops
tags:
  - kind/project
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - agent/hermes
  - domain/infrastructure
created: "2026-09-14"
updated: "2026-09-18"
---

# HERMES — Infrastructure Operations

> [!info]+ Infrastructure Operations
> **Padre:** [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1

## 🎯 Objetivo

**Habilitar (enablement) y certificar la capacidad administrativa de Ariadna/Hermes sobre Aranea**: descubrir y reconciliar identidades, certificar acceso/permisos/alcance y rutas de recuperación, documentar herramientas y límites, y preparar procedimientos y contratos operativos que los **proyectos ejecutores** (Backup/DR, y en su momento los demás) consumen sin bootstrap humano rutinario.

**Separación enablement/execution (decisión owner 2026-09-18):** este workstream NO ejecuta backups, restores, lifecycle, provisioning ni ningún cambio operativo en los sistemas de otros proyectos. Ejecutar es del proyecto ejecutor (p.ej. [[BACKUP-DR-OWNER-PROJECT]] para Backup/DR); de aquí salen identidades, matrices de autoridad certificadas, rutas nativas y handoffs listos para consumir. El objetivo final de autonomía operativa del programa se conserva: lo que cambia es **quién ejecuta cada tarea y desde qué proyecto**.

Este workstream define el **management plane nativo** de Hermes. No depende del MCP Access Plane para reparar o administrar el mismo plano MCP ni los servicios subyacentes.

**Objetivo inmediato vigente (mandatos owner 2026-09-18):** `H1 — Backup & Storage Administrative Enablement` CERRADO con `H1 ENABLEMENT PASS`, `H2 — Proxmox Lifecycle Administrative Enablement` CERRADO con `H2 ENABLEMENT PASS`, y `H3 — Guest & Service Administrative Enablement` EJECUTADO el mismo día con veredicto `H3 PARTIAL — LINUX ENABLED / WINDOWS BLOCKED` (Windows sin management nativo; owner bundle W1 pendiente). H0 cerró 2026-09-18 (`h0-20260918-r1`, PASS WITH DEBT); su SPEC queda HISTORICAL. Próximo nivel natural (H4) sin mandato vigente.

## 🧠 Contexto

Hermes será el administrador general del homelab, pero entregar root-equivalent sobre todo Aranea desde el primer día generaría demasiado blast radius y dificultaría saber qué autoridad está realmente certificada.

La estrategia es progresiva:

```text
observe
→ protect storage/backups
→ operate Proxmox lifecycle
→ operate guests/services
→ provision new infrastructure
→ enable high-impact infrastructure
→ integrated autonomy
```

El conocimiento existente de Backup/DR se reutiliza desde [[BACKUP-DR-OWNER-PROJECT]]. Este workstream **no rediseña Backup/DR**; lo usa como primer dominio real para certificar el modelo de autonomía.

## 🏛️ Boundary

### Este workstream SÍ gobierna

- authority/bootstrap de Hermes sobre interfaces administrativas nativas;
- inventario y discovery de infraestructura;
- habilitación y certificación de la administración de Proxmox/TrueNAS/hosts/guests por etapa (H0–H6): este carril clasifica autoridad, contratos y rollback; la ejecución operativa queda en los proyectos ejecutores;
- acceso Linux/Windows para operación;
- Docker/systemd/filesystem/configuración no secreta;
- contratos y habilitación de service lifecycle/recovery (la ejecución es del proyecto de servicio correspondiente);
- habilitación de provisioning (H4): el provisioning mismo lo ejecuta el proyecto consumidor;
- gates, rollback, revoke y evidencia de cada nivel.

### Este workstream NO gobierna

- capabilities MCP entregadas a Echo/Forge/agentes: eso vive en [[HERMES — Agent Access Operations]];
- endpoints/permisos exactos del MCP Access Plane: source of truth [[AGENT-PLATFORM - MCP Access Plane]];
- redefinir la estrategia Backup/DR: source of truth [[BACKUP-DR-OWNER-PROJECT]];
- mutaciones PROD no autorizadas explícitamente.

## 🔐 Matriz de autoridad H1 (2026-09-18, certificación read-only)

Cadena demostrada por familia: `CONNECTIVITY ✓ < AUTHENTICATION ✓ < AUTHORITY ✓ (ejercida sólo en lectura) ≠ OPERATIONAL CERTIFICATION ✗ (ninguna operación de backup/restore ejecutada ni certificada)`.

| Target | Identidad estable | Canal(es) | Autenticación demostrada | Permisos efectivos demostrados (sólo lectura) | Estado | Límites / notas |
|---|---|---|---|---|---|---|
| athena .10 / zeus .100 / hera .110 / kronos .120 / hades .90 | host PVE 8.4.20, clúster `aranea` | SSH + API 8006 | SSH `ariadna` con key `ariadna_pve` (ED25519, `from=192.168.31.122`=hermes-vm); API token `ariadna@pve!backup-dr` (privsep=1, expire=0) | SSH: uid local + `sudo NOPASSWD: ALL` **5/5**; API: `version`+`cluster/resources` **200 en los 5 nodos** (59 guests = 39 qemu+20 lxc, exacto vs H0); local con sudo: `pvecm status` Quorate 5/5, `storage.cfg` 10 storages sin `pbs`, `/cluster/backup` = **[] (0 jobs, `/etc/pve/jobs.cfg` inexistente)**, user/token/ACL leídos (`/vms` AriadnaVMBackup) | VERIFIED · **G1 PASS** | Token API NO cubre `/cluster/status`(403)/`/cluster/backup`(403)/`/storage`(403) — scope `/vms` VM.Audit+VM.Backup; lecturas cluster-level requieren SSH+sudo (disponible). Permisos H2 (lifecycle) clasificados por ACL, NO ejercidos. |
| truenas — VM 145, .91 | TrueNAS SCALE 25.04.1 | SSH + WS `wss://.91/websocket` + UI 443 | SSH `ariadna` key `ariadna_truenas` (sin from-restrict); WS api-key `ariadna-admin-20260918` (id 1, user `ariadna` uid 3005, grupos 544/3002/3008, FULL_ADMIN, password_disabled) | WS: system.info 25.04.1, pool.query (pool0+pool2 ONLINE healthy), zfs.dataset.query 202 (173 FS+29 VOL), zfs.snapshot.query 606, replication.query 0, cronjob.query 0, cloudsync.query 0, service.query (cifs/nfs/iscsitarget/smartd/ssh RUNNING); SSH: uid 3005, `sudo (ALL) NOPASSWD: ALL`, midclt disponible | VERIFIED · **G2 PASS** | ENOMETHOD en `snapshot.query` y `snapshottask.query` (25.04 renombró métodos ZFS a `zfs.*`): snapshot tasks por `task.query`/oneshot **pendiente de verificar** (gap menor, no bloquea R2). Canal de recovery independiente: SSH+sudo. |
| pbs — VM 180 @kronos, .123 | proxmox-backup-server 4.2.6-1 (running 4.2.5), Debian 13.6, kernel 7.0.14-8-pve | SSH + UI :8007 | SSH `ariadna` key `ariadna_pbs` (ED25519, `from=192.168.31.122`); UI unauth responde 401 (wall de auth verificado — jamás se probó login) | SSH: uid 1000 + `sudo NOPASSWD: ALL`; servicios api+proxy activos; `datastore list` = **vacío (0 datastores)**; `user.cfg` solo root@pam; sin remote.cfg/sync jobs — **PBS VIRGEN** (re-confirmado; consistente con R2 discovery de Backup/DR del mismo día) | VERIFIED · **G3 PASS** (con límite) | RBAC/API PBS NO probado con credencial propia (sólo existe root@pam; no se pidió login — quedaría para el ejecutor). Operacional: sin datastores no hay nada que certificar operativamente (correcto pre-R2). |
| hermes-vm (self) | runtime Hermes | `systemd --user` + FS local | identidad propia | recovery 2026-09-16 vigente | VERIFIED | ver [[hermes-linux-update-recovery]] |
| mcps LXC / daedalus | management paths `mcps-ops` / `daedalus-ops` | SSH nativo | key-only | estado previo vigente (G0) | VERIFIED | independiente del MCP — management independence re-verificada en G4 |
| Windows worker-kronos | ssh-mcp viewer/operator | plano MCP | — | estado 2026-09-18 vigente (viewer) | VERIFIED (parcial) | CONSUMER_PLANE_ONLY; sin cambios en H1 |

**Recuperación independiente:** todas las identidades SSH viven en `~/.ssh/` de hermes-vm (`ariadna_pve`, `ariadna_truenas`, `ariadna_pbs`; fingerprints en evidencia) — no dependen del MCP Access Plane. **Revocación observable:** `authorized_keys` por host (option `from=` restringe a hermes-vm en PVE/PBS; TrueNAS sin restrict), token PVE eliminable vía `pveum` (owner), api-key TrueNAS eliminable vía UI/owner. **Expiración:** token `expire=0` (sin expirar; rotación = decisión owner), keys sin fecha de expiración.

## 🔐 Matriz de autoridad H2 (2026-09-18, Proxmox lifecycle — clasificación read-only, sin ejercer mutaciones)

Auditoría en vivo 5/5 nodos (20:41–21:02 UTC): PVE 8.4.20 en todos, quorum 5/5, 59 guests verificados vivos (39 qemu + 20 lxc, exacto vs inventario H0), 10 storages, HA sin recursos, `datacenter.cfg` vacío (defaults), sudoers `90-ariadna-pve` NOPASSWD en 5/5, llave `from=192.168.31.122` presente en todos. Permisos efectivos contrastados usuario↔token por `pveum user/token permissions`: idénticos (`VM.Audit`+`VM.Backup` en `/vms`, propagate). API sondeada con 19 GET declarados como read-intent. **Capacidad del token API (`ariadna@pve!backup-dr`) ≠ capacidad SSH (`ariadna` + sudo root-equivalent):** el token sólo lee per-VM; todo lifecycle existe vía SSH y queda NO EJERCIDO por diseño de este carril.

| Familia | Operaciones clave | Permiso API requerido (según PVE 8.4) | Efectivo demostrado | Alternativa SSH/sudo | Estado habilitación |
|---|---|---|---|---|---|
| A — Descubrimiento/inspección/estado | cluster/resources, version, config+status per-VM, Ceph health, storages, ACL/roles, snapshots existentes | `VM.Audit` (/vms) | 200 reales API + SSH — **EJERCIDO**; node-status 403 y lecturas cluster-level por SSH | `qm/pct list/config/status`, `ceph -s`, `pveum`, `storage.cfg` | AUTHORIZED_AND_VERIFIED (lecturas) |
| B — Power lifecycle | start/stop/shutdown/reboot VM+LXC, consola | `VM.PowerMgmt` | NOT_PROVEN (no ejercido; jamás inferido de VM.Audit) | `qm/pct start|stop|shutdown|reboot` (root-equivalent disponible) | AUTHORIZED_NOT_EXERCISED |
| C — Config/recursos | CD/ISO, CPU/RAM, disco, red, options | `VM.Config.*` | NOT_PROVEN | `qm set/resize` (disponible) | AUTHORIZED_NOT_EXERCISED |
| D — Creación/clonación | create, clone, template | `VM.Allocate`+`Datastore.AllocateSpace`; `VM.Clone` | NOT_PROVEN | `qm create/clone/template` (disponible; pool1 Ceph NEARFULL hoy = precaución de capacity) | AUTHORIZED_NOT_EXERCISED |
| E — Migración/ubicación | migrate, move-disk, affinity | `VM.Migrate` + recursos en ambos nodos | NOT_PROVEN; foto: storages `local-sqx-*`/`local-kronos` LVM shared=0 (migrar = mover discos), pool1 RBD shared; HA vacío | `qm migrate/move-disk`, `ha-manager` (disponible) | AUTHORIZED_NOT_EXERCISED |
| F — Eliminación/teardown | destroy VM/LXC | `VM.Allocate` | NOT_PROVEN y **vetado por contrato**: jamás sobre los 59 guests ni PBS 180; sólo recursos propios del ejecutor con doble target proof | `qm/pct destroy` (sin red de seguridad hoy: 0 backups, 0 snapshots) | OUT_OF_SCOPE salvo owner-gate |
| G — Recovery/rollback | snapshot/rollback, restore, recuperación de acceso | `VM.Snapshot`/`VM.Snapshot.Rollback`; restore requiere Datastore en destino | NOT_PROVEN e **inaplicable hoy**: 0 snapshots verificados (108/111/123/135/145/180) y 0 jobs de backup; acceso: SSH 5/5 **EJERCIDO** | `qm snapshot/rollback`, `qmrestore` (post-R2); break-glass = consola owner | AUTHORIZED_NOT_EXERCISED (acceso: VERIFIED) |

Hallazgo técnico (regla nueva para operadores): PVE **filtra por permiso** en `/storage`, `/nodes/{n}/storage`, `/pools` y `/cluster/tasks` devolviendo **200 con lista vacía** sin `Sys.Audit`/`Datastore.Audit`; mientras `/cluster/status`, `/cluster/backup`, `/cluster/ha` y `/nodes/{n}/status` dan 403 reales. Un 200-filtrado no prueba vacío real ni permiso efectivo. Negativo G4 (21:02 UTC): `POST /nodes/hera/qemu/123/status/start` y `/shutdown` con el token → **403 `VM.PowerMgmt`** (denegación de mutación demostrada por read-intent, sin ejecutar nada).

Discos de los sagrados SQX leídos: `backup=0` explícito en los 4 discos verificados (VM 108/111/123: 50G+600G cada una; worker-kronos 135 sin snapshots). Ceph: HEALTH_WARN (osd.0/osd.2 nearfull; pools pool1 y .mgr nearfull; 129 pgs active+clean; 834 GiB / 2.3 TiB usados).

**Matriz completa (34 filas, por operación, con target/canal/riesgo/precondiciones/validación/rollback/recuperación/evidencia+timestamp):** `~/aranea/work/h2-enablement-20260918/h2_authority_matrix.csv` + probes crudos del mismo directorio. **Contrato del futuro operador:** [[proxmox-lifecycle-operator-contract]] (enablement-only; no autoriza operaciones). **G4 sesión fresca:** hijo aislado resolvió `sqx-hera` desde inventario (VM 123 @ hera, running), verificó estado vivo por API+SSH, clasificó operaciones por canal y demostró management independence sin tocar el guest ni usar secretos en el prompt — read-only completo.

**Recuperación independiente:** SSH+sudo 5/5 (verificado hoy); si la API PVE cae, SSH opera todo; si SSH falla, consola PVE del owner (break-glass); si hermes-vm muere, `from=` de las llaves exige reinstalación por consola física del owner.

## 🔐 Matriz de authority previa (2026-09-17, H0 — HISTORICAL)

La matriz incremental de H0 (wrapper `agent_ro`+`agent-read` 6/6, `mcps-ops` 26 containers, `daedalus-ops` sin sudo, APIs nativas "absent") queda **HISTORICAL**: las APIs nativas dejaron de estar absent con las identidades instaladas 2026-09-18 y certificadas arriba; el wrapper sigue válido como canal alternativo de observación. Detalle completo en la bitácora 2026-09-17 y change log G0.

## 🔐 Principios de autoridad

1. Hermes recibe sólo la autoridad necesaria para el nivel H actualmente certificado.
2. Un operador especializado recibe tools/credentials sólo para su responsibility boundary.
3. Los valores secretos nunca se escriben en Agents-OS; sólo referencias.
4. Antes de cualquier mutación se demuestra target, entorno y blast radius.
5. Toda nueva autoridad debe tener revoke/rollback viable.
6. Un management path no puede depender exclusivamente del servicio/plano que debe recuperar.
7. PROD/high-impact permanece gated hasta decisión explícita del owner.

## 🚦 Roadmap H0 → H6

### H0 — Observe / Inventory

**Objetivo:** Hermes puede reconstruir el estado real de Aranea sin mutar.

- inventario de nodos físicos/virtualizados;
- Proxmox cluster resources;
- TrueNAS/storage topology y health;
- VMs/LXC, host placement y estado;
- services/runtimes relevantes;
- interfaces administrativas disponibles;
- relaciones service → guest → host → storage;
- identificación de gaps de autoridad/credenciales por referencia.

**Gate:** un agente fresco puede diagnosticar dónde vive un servicio y qué management path usar sin preguntar al owner por datos ya documentados.

### H1 — Backup & Storage Administrative Enablement *(redefinido 2026-09-18; el texto anterior que ordenaba ejecutar backups quedó HISTORICAL — ver change log)*

**Objetivo:** Ariadna dispone de identidades, herramientas, permisos efectivos, rutas nativas de administración, recuperación independiente y documentación suficiente para que [[BACKUP-DR-OWNER-PROJECT]] utilice esas capacidades **sin bootstrap humano rutinario**. H1 NO implica que existan backups, jobs, retención o restores certificados: eso es ejecución de Backup/DR (R2+).

Tareas de habilitación (reemplazan las I2.1–I2.5 ejecutoras originales):

- reconciliar los accesos administrativos instalados (PVE/TrueNAS/PBS) con evidencia read-only y matriz de autoridad;
- certificar conectividad, autenticación y autoridad efectiva por familia (G1/G2/G3), distinguiendo `CONNECTIVITY != AUTHENTICATION != AUTHORITY != OPERATIONAL CERTIFICATION`;
- certificar desde sesión fresca que el consumidor real (Ariadna) resuelve canales sin owner ni secretos en el prompt (G4);
- consumir la lista de necesidades administrativas de Backup/DR y producir handoff consumible por R2;
- identificar capacidades realmente faltantes (owner bundle sólo ante bloqueo demostrado) y dependencias futuras.

**Gate:** `H1 ENABLEMENT PASS` — el alcance administrativo demostrado permite a Backup/DR consumirlo sin bootstrap manual rutinario. Variantes honestas: `PASS WITH LIMITATIONS`, `PARTIAL`, `BLOCKED` según impacto demostrado. No se certifica capacidad por inferencia.

### H2 — Proxmox Lifecycle *(enablement-only desde 2026-09-18; EJECUTADO Y CERRADO 2026-09-18)*

**Qué habilitará este workstream:** permisos, herramientas, contratos y certificaciones para que el proyecto ejecutor opere `inspect/config/status`, `start/stop/reboot`, `create/clone` y cambios de resource/config con target proof, validación post-change y rollback. Este carril NO ejecuta lifecycle.

**Gate:** matriz de autoridad H2 demostrada (permisos efectivos clasificados sin ejercerlos) + contratos/rollback disponibles para el ejecutor.

**Resultado (2026-09-18):** `H2 ENABLEMENT PASS` — matriz de 34 operaciones (familias A–G) clasificada sobre auditoría read-only en vivo 5/5 nodos; contrato del operador publicado ([[proxmox-lifecycle-operator-contract]]); G4 de sesión fresca PASS; management independence verificada. `PROXMOX LIFECYCLE OPERATIONAL CERTIFICATION` queda explícitamente FUERA de este hito: la demuestra el proyecto ejecutor operando. Handoff y evidencia: ver matriz H2 y bitácora.

### H3 — Guest & Service Operations *(enablement-only)*

**Qué habilitará:** accesos Linux/Windows management, Docker/Compose, systemd, filesystem y canales de diagnóstico para que el servicio operativo correspondiente repare servicios dentro de guests. Este carril NO ejecuta repairs.

**Gate:** rutas nativas por familia (Linux/Windows) certificadas + contratos de escalation definidos.

### H4 — Provisioning *(enablement-only)*

**Qué habilitará:** autoridad y tooling de provisioning (VM/LXC/containers, OS/bootstrap, instalación/config, onboarding backup/observabilidad) para el proyecto ejecutor. Este carril NO provisiona.

**Gate:** identidad/token con scope de provisioning clasificado + flujo de onboarding documentado, sin ejecutar.

### H5 — High-impact Infrastructure *(enablement-only)*

**Qué habilitará:** certificaciones de autoridad para networking, cluster/storage de mayor blast radius y operaciones host-level críticas, cada familia con recovery demostrado, authority específica y criterios abort/rollback, para uso del ejecutor autorizado.

**Gate:** por familia, autoridad clasificada y recovery path verificado — sólo lectura; la operación queda gated al proyecto ejecutor.

### H6 — Integrated Autonomy *(enablement-only)*

**Qué habilitará:** contratos de coordinación multi-capa (handoffs, matriz de operadores, criterios de incidente) que permitan al programa coordinar incidentes y cambios usando los proyectos ejecutores y operadores especializados.

**Gate:** el conjunto H0–H5 certificado permite tareas multi-capa habituales sin intervención humana excepcional — demostrado por los ejecutores, no por este carril.

## 🤖 Operadores lógicos previstos

La separación exacta se ajustará por evidencia; punto de partida:

- `backup/storage operator`
- `proxmox operator`
- `linux/container operator`
- `windows operator`
- `service operator`

No se crea un framework genérico de operadores por anticipación. Primero se certifican paths reales; después se extraen skills/prompts reutilizables.

## 🧪 Acceptance scenarios

Este workstream debe demostrar progresivamente escenarios reales, no sólo acceso técnico. Escenario habilitado ≠ ejecutado por este carril: cada escenario se certifica como capacidad entregada al proyecto ejecutor correspondiente:

- identificar host/guest de un servicio desde nombre lógico;
- habilitar al ejecutor para detectar backup faltante o job fallido;
- habilitar al ejecutor para validar un backup y restaurar una muestra acotada;
- habilitar al ejecutor para reiniciar de forma segura un servicio DEV/test;
- recuperar un MCP/runtime caído usando el management path nativo;
- habilitar al ejecutor para crear/provisionar un workload no crítico cuando H4 esté habilitado;
- registrar evidencia suficiente para que otro agente continúe.

## 📊 Estado actual

- **H2 ENABLEMENT PASS — 2026-09-18 (mandato owner; cero mutaciones):** capacidad administrativa Proxmox lifecycle clasificada para las familias A–G sobre auditoría read-only en vivo (matriz H2 arriba, 34 operaciones), contrato del futuro operador publicado ([[proxmox-lifecycle-operator-contract]]), consumidor real verificado en sesión fresca (G4: resolución sqx-hera 123@hera API+SSH), management independence re-verificada, handoff entregado. La `PROXMOX LIFECYCLE OPERATIONAL CERTIFICATION` corresponde al proyecto ejecutor futuro. Detalle y evidencia: `80-agents/journal/logs/2026-09-18-h2-proxmox-enablement.md` + `~/aranea/work/h2-enablement-20260918/`.
- **H1 ENABLEMENT PASS — 2026-09-18 (mandato owner; cero mutaciones):** alcance administrativo PVE/TrueNAS/PBS certificado read-only (matriz H1 arriba), consumidor real verificado en sesión fresca (G4), handoff entregado a Backup/DR R2. Detalle, límites y evidencia: `80-agents/journal/logs/2026-09-18-h1-enablement.md`.
- **Workstream:** creado 2026-09-14; **H0 PASS WITH DEBT — 2026-09-18 (run h0-20260918-r1):** G0/G1/G3 heredados del preflight + G2 (5 familias) y G4 (sesiones frescas) certificados en ese run; veredicto completo, deuda y handoff en la bitácora de cierre.
- **Habilitación habilitada por carriles:** H2–H6 quedan enablement-only (clasificación de autoridad/contratos para el ejecutor) — ver roadmap arriba. Backup/DR conserva autoridad de ejecución ([[BACKUP-DR-OWNER-PROJECT]]).
- **Backup/DR:** [[BACKUP-DR-OWNER-PROJECT]] mantiene autoridad de ejecución; R2 discovery PBS ya ejecutado por ese carril el 2026-09-18 (owner action bundle propio en `~/aranea/work/r2-pbs-20260918/`); este carril no toca jobs, tickets ni decisiones.
- **G0:** PASS, bootstrap y `agent-read` 6/6, `mcps-ops`, `daedalus-ops` y authorities; `I0.1–I0.4` cerradas.
- **G1 discovery:** captura 2026-09-17 18:58 UTC 6/6, 59 VMs definidas (42 running / 17 stopped), 10 storages, canon actualizado. Discovery PASS según resumen owner; la cobertura service/guest y G2 no se infieren de este PASS.
- **G3 integration:** batch autorizado en config Hermes (`aranea-ssh` y observability junto con postgres-ro); helper consumer-side PASS (SSH 11 tools, observabilidad 22 tools); pendiente prueba en sesión nueva. El change log `2026-09-17-hermes-infra-preflight-g0` ya registra G3 resuelto; la fotografía previa 'sólo postgres' queda histórica.
- **G2:** parcial, Linux probado; Windows tiene probes previos pero requiere matriz de cobertura y certificación H0 formal; Proxmox/TrueNAS ahora con credenciales nativas certificadas (H1 2026-09-18: SSH `ariadna`+sudo y API/WS propias — ver matrices H1/H2); wrapper `agent_ro` queda como canal alternativo de observación.
- **G4:** pruebas de sesión fresca certificadas por run: H0 (3 escenarios + negativos), H1 (canales PVE/TrueNAS nativos) y H2 (resolución sqx-hera + clasificación por canal + management independence). Pruebas integrales futuras se diseñan por mandato, no por rutina.
- **Management path:** independiente vía `mcps-ops`; nunca tratar el MCP como ruta exclusiva de recovery.
- **Runtime Hermes 2026-09-16:** `v0.21.3 (2026.9.14)`, dashboard 127.0.0.1:9119 HTTP 200, `hermes-gateway-ariadna.service` conectado. Legacy `hermes-gateway.service` permanece disabled para evitar doble polling de Telegram. Recovery en [[hermes-linux-update-recovery]] y [[hermes-agent-operator]].
- **Publicación Agents-OS:** editar `VAULT_ROOT` como fuente canónica; pipeline vault→GitHub corre en otro equipo (~1 min); repo local Hermes es consumidor fast-forward, no productor. Si GitHub diverge, resolver conservando delta del vault y evitar direct push al espejo.
- **Backup/DR:** [[BACKUP-DR-OWNER-PROJECT]] mantiene autoridad; no tocar jobs ni decisions congeladas en H0.

## 🧱 Entrega de desarrollo

_No aplica como repo único. Este workstream puede cambiar configuración ejecutable e infraestructura; antes de cada implementación registrar target, source of truth, baseline, scope, rollback y evidencia. Si aparece código/versioned config, declarar repo, branch, base y SPEC antes de modificar. No inventar repo ni editar el espejo GitHub como si fuera el vault en runtime._

## 🧭 H0 — Plan de ejecución 2026-09-18 · **HISTORICAL SPEC (ejecutado y cerrado 2026-09-18, run `h0-20260918-r1`, veredicto PASS WITH DEBT)**

> [!warning] HISTORICAL — no volver a ejecutar
> Este SPEC se congeló el 2026-09-17 para la jornada H0 del 18 y ya fue ejecutado y cerrado. El roadmap actual es de HABILITACIÓN (ver Objetivo y H1–H6 arriba). Se conserva como registro histórico; el change log de esta sesión documenta la corrección de alcance.

### Misión y definición de resultado

Ventana de **hasta 10 horas desde T0 real de inicio**. Ejecutar H0 hasta su gate máximo demostrable; NO confundir 10 horas con garantía de PASS ni con autorización de mutaciones. Prioridad: 1) verificación desde Hermes; 2) cobertura y mapa de servicios; 3) observación nativa estrictamente necesaria; 4) evidencia y handoff. H0 NO ejecuta lifecycle, provisioning, restores, backups, restart productivo, root/elevación, red, storage mutable ni desarrolla Echo/Forge. Si hay tiempo remanente, adelantar únicamente contratos/handoff read-only para H1; no empezar H1 formal.

**Producto H0:** un Hermes fresco puede resolver `servicio lógico → guest/VMID y nodo → storage/dependencias cuando estén demostradas → canal disponible y authority → health/logs/métricas permitidas → diagnóstico con evidencia y gaps`, sin hacer cambios. No construir un provider framework, dashboard, DB de capabilities, nuevo MCP ni orquestador.

**No confundir denominadores:** 59 es inventario de guests definidos, no número de SSH targets ni de servicios. Los 17 apagados no fallan por no aceptar SSH; deben figurar como `STOPPED_EXPECTED` salvo otra evidencia. La capacidad de guest-SSH se mide sólo sobre hosts encendidos, de familia pertinente, con identidad autorizada. Coverage de servicios se mide sobre el catálogo in-scope enumerado, no sobre un total inventado. `PASS` de un endpoint no implica permisos para otras máquinas.

### Baseline congelado y delta obligatorio

- Canon: [[HERMES — Infrastructure Operations]], [[HERMES — ARANEA AUTONOMOUS OPERATIONS]], [[AGENT-PLATFORM - MCP Access Plane]], [[BACKUP-DR-OWNER-PROJECT]], `30-resources/aranea/00-index.md`, `01-topologia/fechas-captura.md`, catálogo de servicios, skills `aranea_agent_ro_inventory_refresh` / [[hermes-agent-operator]]. Resolver paths reales desde `VAULT_ROOT`, no fijar paths absolutos.
- Evidencia inicial: change log `2026-09-17-hermes-infra-preflight-g0`, discovery `*_20260917_185839.txt`, `inventory_20260917_185839.json`; 6/6, 59 = 42+17, 10 storages, `mcps-ops` 26 containers; G3 helper PASS.
- T0: bootstrap warm (si aplica); leer delta de esta nota, último change log y el runtime, comprobar hash/mtime de la captura y git/vault freshness. Si hay evidencia posterior, adoptar la más reciente tras reconciliation; no revertir gates demostrados, no volver a generar G0/G1 por rutina.
- La instrucción del owner de adelantar H0 el 2026-09-18 autoriza **únicamente preparación/observación H0** como excepción de prioridad frente a la secuencia histórica padre Access Plane→Echo/Forge→H0. A2–A5, H1–H6 y Backup/DR permanecen en sus propios proyectos.

### Roles, ownership y paralelización

Un **Hermes manager/integrador** coordina y es único escritor de ESTA nota, gates, config compartida e integración. Ejecutores lógicos A/B/C/D sólo si el runtime real permite aislamiento, credenciales y concurrencia; si no, ejecutarlos secuencialmente. Máximo 4 workers y un integrador, NO crear subagentes/perfiles por reflejo. Antes de delegar, manager entrega worktree/repo/branch/base y `allowed files` exclusivos por tarea; un único integrador une cambios después de pruebas. No compartir sesión SSH MCP entre workers si causa agotamiento: reutilizar `Mcp-Session-Id`, hacer DELETE al finalizar y acotar concurrency. `ssh-mcp` tiene antecedente de pool 64 agotado por init-only; no disparar sondeos masivos.

- **A / inventory & service map (critical path):** consumir el JSON actual, registrar 59 identidades estables (`node + VMID` como localización actual, VMID de clúster como identidad cuando aplique), tipo, state, colocación, storage referido, origen y hora. Reconciliar hosts/nodos, 10 storages, catálogo de servicios y servicios críticos; joins `service→guest→node→storage` con `UNKNOWN` explícito si faltan datos; verificar que migración/cambio IP no fija el target equivocado. No duplicar inventario en otra DB. Documentar cobertura/gaps y proveer casos de prueba al integrador.
- **B / Linux & management boundaries:** certificar desde runtime Hermes `agent-read` 6/6, distinguir operator `mcps-ops` y `daedalus-ops` de viewer wrapper y guest SSH; mapear identities/profile/capabilities por target; smokes inocuos y negativos `POLICY_DENIED` sobre comandos realmente prohibidos. `docker ps` con exit 127 en viewer es CLI inexistente, NO prueba de enforcement. No ampliar sudo, no modificar host-keys ni crear root universal. Preparar onboarding idempotente read-only sólo como SPEC si aparece un guest nuevo sin permiso.
- **C / Windows & service observation:** recuperar evidencias existentes del 17-sep, inspeccionar publisher SYSTEM y perfiles viewer/operator según sources vigentes; validar desde la nueva sesión Hermes al menos identidad, target, lectura de evidencia no secreta, estado/timestamp y rechazo efectivo de mutadores no autorizados. NO otorgar Windows admin/JEA en H0, NO tocar Task Scheduler ni MT5 productivo. Si el MCP ofrece sólo acceso indirecto, marcarlo como `CONSUMER_PLANE_ONLY`, no como recovery nativo.
- **D / Proxmox–TrueNAS read-only:** verificar si `agent-read` existente ya prueba inventario PVE, placement, cluster health, storage health/TrueNAS health necesarios. Emitir matriz `fact → wrapper/API → PASS/MISSING`. Sólo para MISSING genuino preparar API RO owner bundle; no pedir credenciales de H2/H4. Después de autorización, adoptar cliente/API nativo existente y probar lectura y rechazo de mutaciones. Detectar versiones reales antes de escoger transporte (TrueNAS 25.04+ usa JSON-RPC/WebSocket; REST eliminado en 26; verificar release instalada); exigir TLS/verificación cert para keys. Proxmox usar token privilege-separated, scopes efectivos de user∩token y expiración, no full privileges. Ninguna credencial nueva hasta consentimiento explícito.

### Owner Action Bundle — única interrupción agrupada

Antes de T+60 min el manager entrega UN bloque consolidado, sólo si existe gap probado, con tabla para cada autorización: `ID; hecho que falta; target real/versión; canal/identidad actual; mínimo permiso RO; efecto; cómo instala owner de forma segura; verificación positiva y negativa; expiración/revoke; alternativa sin permiso; impacto sobre gate`. Separar **DECISION** (autorizar o rechazar API RO) de **SEED** (owner instala el secreto directo en canal seguro del host); no pedir copiar tokens al chat/vault/GitHub. Validar account/role por read-only inspect, nunca autoelevar. Al responder owner: revalidar sólo los target afectados, continuar workstreams independientes en paralelo. Si owner no responde: registrar `GATED_OWNER`, continuar A/B/C y observación D por wrappers; no insistir ni inventar autorización. H2/H4 requieren otro contrato futuro; token RO NO los desbloquea.

### Evidence contract y matriz G2

Crear únicamente archivos de evidencia no secretos bajo la convención de run actual fuera del vault para artefactos grandes; en esta nota dejar referencias relativas al workspace y síntesis. Campos mínimos por observación: `run_id`, timestamp UTC, source/version, stable target ID, hostname/VMID+node actual si procede, service ID si procede, environment, method/channel, identity profile *sin credencial*, requested operation, effective allow/deny, result code/status, freshness, evidence reference, limitations. Redactar headers, env, payloads sensibles y blobs; no logs masivos en vault.

Matriz de targets: una fila por guest (59) y una por host/servicio pertinente con estado `INVENTORIED`, `OBSERVED`, `STOPPED_EXPECTED`, `UNREACHABLE`, `AUTH_DENIED`, `NOT_AUTHORIZED`, `UNKNOWN`, `STALE`, `CONFLICT`, según evidencia; permisos por canal y fecha. Mantener inventario≠reachability≠authority≠health; no colapsar estados ni inferir diagnósticos. Para VM offline, inventario y placement pueden PASS, guest-access es N/A. Para `PBS VM 180` respetar inaccesibilidad documentada y dependencia Backup/DR: registrar bloqueo, no escanear ni reparar por H0.

G2 family certifications:
- **Linux:** 6/6 control-plane wrapper (reprobe si stale); muestra representativa de guest Linux sólo si hay identidad ya autorizada; distinción viewer/operator y negativos.
- **Windows:** target `worker-kronos` y casos documentados; viewer/operator de alcance probado, evidencia publisher fresca, negativos seguros; no extrapolar a todas las Windows.
- **Proxmox:** inventario cluster/VMID, placement, state, storage por wrapper o API RO, source proof y exact permissions; clasificar API directa separadamente.
- **TrueNAS:** pools/datasets/health/topology por wrapper o API RO, auth y source proof; no mutaciones.
- **Observability:** Grafana/Jaeger/Loki datasource health y consulta acotada con target correlation, no confundir MCP tool list con observación real.

Un family gate es `PASS` sólo si todos sus MUST dentro del scope observado pasan; de otro modo `PASS_WITH_LIMITATIONS` (limitaciones no críticas y documentadas), `BLOCKED` (autoridad/target crítico) o `FAIL` (regresión real). No declarar un PASS universal a partir de una muestra. Reportar denominadores exactos por familia.

### Golden G4 — prueba desde sesión Hermes nueva

1. Nueva sesión real: comprobar que config carga `aranea-ssh`, observability y postgres-ro; mínimo session initialize+tools/list, health observable y cero secretos. Comprobar que no se levanta gateway legacy duplicado.
2. Elegir por inventory service catalog **tres escenarios** si hay evidencia: Linux/servicio en nodo, Windows MT5 vía publisher, infraestructura/storage TrueNAS/Proxmox. Al menos uno debe partir de nombre lógico de servicio, no host/IP anticipado. Usar diferentes targets, sin inventar estado saludable.
3. Para cada escenario, resolver: nombre lógico → identidad unívoca/guest/VMID/ubicación → source y timestamp → canal autorizado → lectura de estado/log/metric según exista → síntesis y evidencia. Contrastar dos fuentes cuando sea posible; contradicción = CONFLICT, no adivinar.
4. Negativos obligatorios: nombre inexistente o ambiguo devuelve NOT_FOUND/AMBIGUOUS sin ejecutar acciones; viewer mutator devuelve POLICY_DENIED verificable; endpoint auth sin secreto devuelve 401/403 sólo si prueba segura preexistente; caído/no autorizado se clasifica sin reintentos ilimitados. No ejecutar un mutador real para probar un DENY si el policy layer no garantiza bloqueo antes del target.
5. Recoverability: probar por lectura que `mcps-ops` sigue disponible independentemente del MCP y que existen runbooks vigentes. No apagar servicios para simular incidentes.
6. Un agente fresco (contexto sólo skill/proyecto y sources indicadas) reproduce al menos un lookup de servicio sin owner knowledge. Si no existe ruta runtime directa, declarar PARTIAL y especificar blocker verificable.

**G4 PASS** requiere G2 con cobertura MUST suficiente, sesión nueva PASS, ≥3 escenarios si están autorizados (de lo contrario justificar menor alcance y no declarar integral), negativos, management independence, cero mutaciones y evidencia reproducible. No usar HTTP 200, tool count o mocks como sustituto de consumer real.

### Cadencia de 10 horas, presupuesto y stop rules

| Ventana relativa | Manager / workers | Output no opcional |
|---|---|---|
| T+0–0:30 | cold/warm delta, baseline runtime y distribución de archivos | manifiesto + alcance + fuentes; no repetir G0/G1 |
| T+0:30–1:00 | A/B/C/D inspect paralelo; D detecta RO gaps; manager consolida bundle owner | owner action bundle único si procede, deps claros |
| T+1:00–5:00 | A inventory/service map; B Linux; C Windows; D wrapper/API RO | entregas independientes y evidencias parciales |
| T+5:00–7:00 | manager integra; se corrigen conflictos/bugs; D aprovecha auth aprobada | matriz coverage normalizada y rutas runtime |
| T+7:00–8:30 | G2 por familia; regresión y negativos | PASS/PARTIAL/BLOCKED honesto |
| T+8:30–9:30 | nueva sesión Hermes + G4 golden | ejecución E2E reproducible |
| T+9:30–10:00 | freeze cambios, verify, notas, handoff | estado del proyecto actualizado, changelog, pendientes |

Tiempos son **timeboxes**, no promesas. Si los workers no pueden correr concurrentemente, manager ordena por A→B→C→D e integra temprano. Limitar probes y contextos, reutilizar resultados frescos; no dejar tareas abiertas con shell sessions sin cerrar. A T+8:30 prohibido empezar funcionalidad nueva; a T+9:30 solo certificar, restaurar cambios reversibles pendientes y documentar. Ante riesgo de secretos, error de identidad, target equivocado o potencial mutación PROD: ABORT inmediato de esa tarea y pedir gate. Owner offline no bloquea A/B/C.

### Definición de cierre y handoff

- `H0 PASS`: inventario actual de 59 identidades reconciliado con source proof, 6 nodos, 10 storages, service map de alcance explicitado y sin conflictos críticos; familias G2 MUST probadas por canal real y con límites explícitos; G4 de sesión fresca PASS y negativos válidos; acceso de recuperación independiente; cero mutaciones; evidencia y proyecto autocontenidos.
- `H0 PASS WITH DEBT`: sólo deuda no bloqueante como API directa innecesaria para datos H0, más mitigación y owner action futura; no llamar H2/H4 READY. Si faltan datos críticos de PVE/TrueNAS, service map decisivo o E2E, usar `H0 PARTIAL/BLOCKED` aunque otras familias estén PASS.
- Entrega durable: actualizar I1 checkboxes durante la ejecución `[ ]→[/]→[x]`, status/progress y esta sección de estado; bitácora con source/time, evidencia, commits y next exact; 1 change log consolidado para las entidades modificadas; matriz de 59 y coverage por familia fuera del vault (referenciada); owner bundle residual sin secretos; lista de decisiones H1 sólo como handoff, sin diseñar H1 ni ejecutarlo.
- Único manager edita proyecto; workers reportan pruebas y commits por scope. En el padre, tarea puente Infra pasa `[ ]→[/]` al comenzar ejecución; solamente `[r]` al quedar para Review y NUNCA `[x]` por el agente. Cierre completo de sesión Agents-OS sólo por pedido explícito del owner.

## ✅ Tareas

### I0 — Bootstrap del management plane

- [x] I0.1 Inventariar interfaces administrativas realmente disponibles para Hermes #owner/agent #type/research #area/aranea — verificado 2026-09-17
- [x] I0.2 Clasificar authority actual por target: observe / operate / provision / absent #owner/agent #type/admin #area/aranea — matriz 2026-09-17
- [x] I0.3 Definir referencias de credenciales y boundaries sin persistir secretos #owner/agent #type/admin #area/aranea
- [x] I0.4 Certificar que Hermes conserva recovery path independiente del MCP Access Plane #owner/agent #type/admin #area/aranea

### I1 — H0 Observe (única cola ejecutable 2026-09-18)

- [x] I1.0 Verificar G0, G1 discovery y G3 helper ya hechos; NO repetir salvo drift — evidencia change log `2026-09-17-hermes-infra-preflight-g0`, owner recap #owner/agent #type/admin #area/aranea
- [x] I1.1 Reconciliar inventario real nodes/hosts/59 VMs/LXC/10 storages **y catálogo de servicios**; baseline 59 confirmado, service map pendiente #owner/agent #type/admin #area/aranea — DONE run h0-20260918-r1 WS A: inventory_59.json 59=42+17 verificado 1:1, service_map 58 servicios (38 completos/17 parciales/3 unknown), 7 testcases G4, discrepancies.md (step-ca 200 stopped vs doc activa; renombres SQX 108/111/112/123; 121/122 eliminados; PBS 180 nuevo)
- [x] I1.2 Construir y probar service → guest → host → storage/dependencies (si demostrado) → management path; resolver unknown/ambiguous/drift #owner/agent #type/admin #area/aranea — DONE WS A: service_map 58 servicios (38 completos/17 parciales/3 unknown), 2 ambiguos y 1 inexistente como testcases G4
- [x] I1.3 Congelar evidence contract/matriz G2 por máquina/familia; distinguir 17 offline de acceso fallido #owner/agent #type/admin #area/aranea — DONE: integration/g2_matrix.csv 70 filas + evidence_records.jsonl (contrato de campos); 17 stopped = STOPPED_EXPECTED, 0 contados como fallo
- [x] I1.4 Preparar owner bundle API RO SOLO ante gap de fact; obtener decisión owner sin exponer tokens, revalidar D #owner/agent #type/admin #area/aranea — RESUELTO SIN BUNDLE: D certificó 0 gaps críticos (9 COVERED/4 PARTIAL/1 MISSING=backup jobs material H1, obtenible extendiendo wrapper); D/owner_bundle_draft.md declara NO SE REQUIERE BUNDLE
- [x] I1.5 Certificar Linux y Windows desde sesión Hermes, positivos/negativos y permisos efectivos #owner/agent #type/admin #area/aranea — DONE WS B+C: Linux PASS (wrapper 6/6, mcps-ops/daedalus-ops, ssh-mcp 16+/4-), Windows PASS_WITH_LIMITATIONS (worker-kronos viewer+operator, publisher FRESH, negativos 4/5 + drift netstat registrado)
- [x] I1.6 Certificar Proxmox/TrueNAS/observabilidad por wrapper o API native RO, sin sobredimensionar permisos #owner/agent #type/admin #area/aranea — DONE WS D + manager probes: facts críticos COVERED por wrapper (nodos/quorum/59 VMs/10 storages/Ceph/pools TrueNAS/versiones/PBS), observabilidad-ro y postgres-ro con lectura real correlacionada y 401 sin bearer
- [x] I1.7 Ejecutar golden G4 desde sesión nueva con escenarios cross-layer y safety negatives #owner/agent #type/admin #area/aranea — DONE: G4 PASS (sesiones frescas CLI): G4.0 carga 3/3 MCPs (50 tools); G4.1 Linux PASS (postgresql→VM152@hades desde nombre lógico, estado vivo PG 17.6 `mcp_echo_prod_ro@echo`, sin contexto privado); G4.2 Windows ejecución PASS (publisher vivo vía mt5-kronos-operator: FRESH 7.2min/SYSTEM/PID 5496/0.2.100+SHA; clasificación del agente corregida por integrador a CONSUMER_PLANE_ONLY); G4.3 TrueNAS PASS (25.04.1, pools ONLINE 0 errores, secciones citadas); G4.4 negativos 3/3 (NOT_FOUND, AMBIGUOUS 114/125, POLICY_DENIED con sessions=0); management independence (`mcps-ops` durante 503 del plano), gateway legacy disabled
- [x] I1.8 Auditar zero mutation/secrets, reconciliar canon, reportar H0 PASS/PASS WITH DEBT/PARTIAL/BLOCKED con evidencias + handoff H1 #owner/agent #type/admin #area/aranea — DONE: leak check CLEAN (sin valores de secretos en evidencia/vault); 3 mutaciones AUTO registradas fielmente por orden owner (config perfil, restart ssh-mcp, parche helper) — veredicto **H0 PASS WITH DEBT** (deuda no bloqueante, detalle en bitácora); handoff H1 en bitácora

### I2 — H1 Backup & Storage Administrative Enablement (mandato 2026-09-18; reemplaza las I2.1–I2.5 ejecutoras del plan original, ahora HISTORICAL — ver change log)

- [x] I2.1 Cargar y reconciliar [[BACKUP-DR-OWNER-PROJECT]] como consumidor (no rediseñarlo); consumir su lista de necesidades administrativas #owner/agent #type/admin #area/aranea — contrato/ownerships reconciliados; R2 discovery PBS ya ejecutado por ese carril hoy (referencia, no duplicación)
- [x] I2.2 Reconciliar accesos instalados por target (5 PVE + TrueNAS + PBS): identidad, canal, auth, permisos efectivos — 7/7 targets con matriz completa; sin exposición de secretos #owner/agent #type/admin #area/aranea
- [x] I2.3 Certificación read-only por familia G1/G2/G3 (PVE API+SSH, TrueNAS WS+SSH, PBS SSH+UI) con límites explícitos y cero mutaciones #owner/agent #type/admin #area/aranea — matriz de autoridad en `## 🔐 Matriz de autoridad H1 (2026-09-18)`
- [x] I2.4 G4 sesión fresca Ariadna: canales cargados, resolución por inventario, consultas read-only por familia, independencia del MCP #owner/agent #type/admin #area/aranea — G4.0/G4.1/G4.3 PASS; G4.2 PARTIAL (ver matriz)
- [x] I2.5 Handoff H1 → Backup/DR R2 + clasificación de gaps (owner bundle sólo ante bloqueo demostrado) + veredicto del gate #owner/agent #type/admin #area/aranea — handoff en `80-agents/journal/logs/2026-09-18-h1-enablement.md`; veredicto: **H1 ENABLEMENT PASS (con límites explícitos)**

### I3 — Expansión H2→H6 (habilitación only; ningún nivel autoriza operaciones desde este carril)

- [x] I3.1 H2: matriz de autoridad Proxmox lifecycle (clasificar sin ejercer) + contratos/rollback para el ejecutor #owner/agent #type/admin #area/aranea — DONE 2026-09-18: 34 operaciones A–G (9 VERIFIED / 24 NOT_EXERCISED / 1 OUT_OF_SCOPE), contrato [[proxmox-lifecycle-operator-contract]], G4 fresco PASS, hallazgo 200-filtrado; evidencia `~/aranea/work/h2-enablement-20260918/`; veredicto H2 ENABLEMENT PASS — change log `2026-09-18-h2-proxmox-enablement`
- [ ] I3.2 H3: rutas nativas Linux/Windows management certificadas + contratos de escalation #owner/agent #type/admin #area/aranea
- [ ] I3.3 H4: identidad/scope de provisioning clasificado + flujo de onboarding backup/observabilidad documentado #owner/agent #type/admin #area/aranea
- [ ] I3.4 H5: mantener high-impact gated hasta aprobación explícita del owner; sólo clasificación de autoridad por familia #owner/agent #type/admin #area/aranea
- [ ] I3.5 H6: definir criterio medible de integración sólo después de escenarios reales repetidos por los ejecutores #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-18 — H2 ENABLEMENT ejecutado y certificado (mandato owner; ZERO MUTACIONES):** auditoría read-only en vivo 5/5 nodos (PVE 8.4.20, quorum 5/5, 59 guests verificados 39+20 exactos, 10 storages, HA vacío, sudoers/`from=` verificados); permisos efectivos contrastados usuario↔token (idénticos: `VM.Audit`+`VM.Backup` en `/vms`); API sondeada con 19 GET de read-intent — clasificación 200 reales vs 403 reales vs 200-filtrado-vacío (`/storage`, `/pools`, `/cluster/tasks`: hallazgo nuevo — filtrado por permiso, NO vacío real); Ceph HEALTH_WARN nearfull (osd.0/osd.2; pool1); 0 snapshots en guests protegidos verificados; discos SQX con `backup=0` leídos en config. Matriz H2 de 34 operaciones A–G (9 AUTHORIZED_AND_VERIFIED / 24 AUTHORIZED_NOT_EXERCISED / 1 OUT_OF_SCOPE = destroy owner-gated) en `~/aranea/work/h2-enablement-20260918/h2_authority_matrix.csv`; contrato del futuro operador creado en `30-resources/runbooks/proxmox-lifecycle-operator-contract.md` (índice+log actualizados, 22 curados); fila de captura añadida a fechas-captura; G4 sesión fresca PASS (hijo aislado: sqx-hera=VM123@hera running verificado API+SSH, clasificación por canal, independence del plano MCP — que al inicio del mandato respondía 401 auth, ya sin el 503 de H1, sin intervención de este carril). Separación API-TOKEN vs SSH-ROOT-EQUIVALENT explícita en toda la matriz. Sin owner action bundle: la autoridad existente alcanza para el objetivo enablement. Cambios: nota del proyecto (matriz H2, gate H2, I3.1, Estado, Bitácora), runbook nuevo, índice/log de runbooks, fechas-captura, change log `2026-09-18-h2-proxmox-enablement`. Veredicto: **H2 ENABLEMENT PASS** — `PROXMOX LIFECYCLE OPERATIONAL CERTIFICATION` queda para el proyecto ejecutor.
- **2026-09-18 — H1 ENABLEMENT ejecutado y certificado (mandato owner; separación enablement/execution incorporada; ZERO MUTACIONES):** alcance redefinido — H1 ya no ordena ejecutar backups (gate `H1 ENABLEMENT PASS`); H2–H6 enablement-only; SPEC H0 marcado HISTORICAL. Reconciliación de accesos instalados por el owner (llaves `ariadna_pve`/`ariadna_truenas`/`ariadna_pbs` + token PVE `ariadna@pve!backup-dr` + api-key TrueNAS): **G1 PVE PASS** (SSH `ariadna`+sudo NOPASSWD 5/5; API 200 en 5/5 nodos con 59 guests exactos; jobs de backup = 0 verificado vivo — cierra fact 12 MISSING de H0; token scope `/vms` confirmado, 403 en cluster/storage = comportamiento correcto); **G2 TrueNAS PASS** (WS `/websocket` FULL_ADMIN: 25.04.1, pools ONLINE, 202 datasets, 606 snapshots, replication/cloudsync/cron 0; SSH+sudo; gap menor: método snapshot-tasks por verificar); **G3 PBS PASS con límite** (4.2.6-1 viva en .123, admin por SSH+sudo, 0 datastores/root@pam-only = VIRGEN, consistente con R2 de Backup/DR; RBAC/API PBS sin credencial propia — sólo root@pam, no se pidió). **G4 sesión fresca:** G4.0 PASS (3/3 MCPs), G4.1 PASS (ssh ariadna@kronos sin secretos ni owner), G4.3 PASS (TrueNAS WS pool.query), G4.2 PARTIAL (management path resuelto y usado; captura MCP en g4_output no disponible en ese flujo), G4.5 PASS (`mcps-ops` hostname). Handoff H1→R2 y matriz de autoridad: ver change log `80-agents/journal/logs/2026-09-18-h1-enablement.md`; evidencia cruda en `~/aranea/work/h1-enablement-20260918/`. NINGUNA mutación de infraestructura; endpoints PVE mutantes sólo tocados como 403 read-intent; sin snapshots/creaciones/logins UI.
- **2026-09-18 — H0 CIERRE run `h0-20260918-r1` · veredicto: PASS WITH DEBT (T+~3h de 10, deuda no bloqueante):** **G2 por familia:** Linux PASS (wrapper 6/6 sha16, mcps-ops 26 containers, daedalus-ops + sudo-DENIED, ssh-mcp 7/7 perfiles, 16+/4-); Windows PASS_WITH_LIMITATIONS (worker-kronos: viewer 4/5 negativos + DEVIATION netstat ALLOWED 2/2, operator, publisher FRESH, CONSUMER_PLANE_ONLY, self-hash ausente del payload); Proxmox PASS vía wrapper (0 gaps críticos, 9/14 COVERED); TrueNAS PASS vía wrapper (25.04.1, pools ONLINE); Observabilidad PASS (22 tools, correlación echo-core, 401 sin bearer); anexo postgres-ro (mcp_echo_prod_ro@echo, PG 17.6). Matriz 70 filas en `~/aranea/work/h0-20260918/integration/` (fuera del vault por diseño). **G4 PASS en sesiones frescas:** carga 3/3 (50 tools), Linux/TrueNAS/Windows resueltos desde nombre lógico, negativos 3/3 con POLICY_DENIED probado (sessions=0), management independence demostrada durante 503 real del plano. **Deuda registrada (no bloqueante, candidata handoff):** (a) drift clasificador viewer Windows: `netstat -ano` ALLOWED donde el mapa 17-sep esperaba denegación — read-only, requiere parche ssh-mcp owner-gated; (b) ambigüedad terminológica runbook aranea-ssh-mcp: el camino "agent-facing certificado" del publisher se presta a leerse como recovery nativo — es plano MCP (CONSUMER_PLANE_ONLY); corregir redacción en próxima edición del runbook; (c) self-hash ausente del payload publicado de worker-kronos (contrato runbook dice self-hash; payload no lo trae) — diagnosticar publisher con authority existente; (d) drift documental 02-servicios: step-ca (VM 200) stopped vs doc activa — reparación = lifecycle GATED (decisión owner pendiente; bloquea renovación TLS `*.lab.aranea`); renombres SQX 108/111/112/123 y eliminados 121/122; (e) helper session-steps-client corregido (DELETE) — extender disciplina de cierre de sesión a consumidores del plano; (f) config base `~/.hermes/config.yaml` conserva el batch G3 duplicado (inofensivo para perfil default; reconciliar cuando se toque ese archivo). **Mutaciones de la jornada (AUTO, registradas por orden owner):** config perfil Ariadna (G3 fix, con backups+sha), `docker restart ssh-mcp` (503 pool-64, pre-checks runbook), parche helper con DELETE de sesión. **Handoff H1 (no iniciado):** (1) arrancar por [[BACKUP-DR-OWNER-PROJECT]]: cargar diseño vigente, reconciliar jobs (D: MISSING=jobs de backup, obtenible extendiendo wrapper con /etc/pve/jobs.cfg); (2) decidir destino del hallazgo step-ca 200 (owner-gated: lifecycle); (3) closures documentales menores: runbook aranea-ssh-mcp (terminología CONSUMER_PLANE_ONLY + nota bookkeeping `[connected]` ya agregada al skill), fechas-captura/02-servicios por delta A; (4) H2/H4 siguen gated: token API RO NO los habilita.
- **2026-09-18 — H0 mutaciones registradas (clase AUTO, NO read-only — orden owner de registro fiel):** (1) **Corrección config perfil Ariadna:** el batch G3 del 17-sep escribió `mcp_servers` + bearers en `~/.hermes/config.yaml` (perfil default), pero las sesiones Ariadna leen `profiles/ariadna/config.yaml` → los 3 MCPs nunca cargaron en sesión nueva (causa raíz del fallo G3 "efectivo próxima sesión"). Fix: mismo batch autorizado por owner aplicado en el archivo correcto (`profiles/ariadna/config.yaml` + `profiles/ariadna/.env` con refs `${VAR}`); backup pre + sha256 en `~/aranea/work/h0-20260918/integration/` (`config.yaml.pre-mcp-*`, `dotenv.pre-mcp-*`, `pre_shas_*`); rollback = restaurar backups. Validado: sesión fresca CLI ve 3/3 capabilities (postgres-ro 13, ssh 13, observability-ro 24 tools). (2) **Restart `ssh-mcp` en mcps:** :3000 en HTTP 503 por pool-64 agotado (leak de sesiones init-only de helpers sin DELETE); recovery según runbook (health + `/status` + logs ANTES de restart), `docker restart ssh-mcp` vía `mcps-ops`, healthy ~12 s, initialize fresco 200. Sin cambio de config. (3) **Parche del helper propio** `mcp-access-plane-operations/templates/session-steps-client.py` (código de Ariadna, NO del plano): captura del `Mcp-Session-Id` por event-hook + DELETE al salir para no re-agotar el pool; probado contra :3001 y :3000 (steps PASS + `session released`). Estas tres mutaciones quedan registradas como mutaciones, no como observación; el resto de H0 (A/B/C/D, G2) fue estrictamente read-only.
- **2026-09-18 — H0 ejecución iniciada (run `h0-20260918-r1`):** T0 2026-09-17T23:30:36Z (20:30 CLT), ventana ≤10 h. Preflight reconciliación GitHub→vault RESUELTO SIN CAMBIOS: `9bc3d58` ya está en `origin/master` y el vault byte-a-byte idéntico en planner + change log (diff vacío; ediciones posteriores del owner preservadas); repo local `~/workspace/agents-os-repo` confirmado consumidor. Delta runtime verificado: 3 MCPs en config (`aranea-postgres-ro` :3001, `aranea-ssh` :3000, `aranea-observability-ro` :3009), bearers por referencia en `~/.hermes/.env` (600), gateway legacy `disabled` y Ariadna activo, hermes CLI v0.21.3 disponible para G4. Evidencia G1 (`*_20260917_185839`) fresca: NO se regenera G0/G1. Workspace run: `~/aranea/work/h0-20260918/` (evidencia fuera del vault). Organización: workers secuenciales A→B→C→D (runtime permite 1 hijo concurrente; B/C comparten plano ssh-mcp — secuencial evita agotar pool 64). Tarea activa: I1.1 (WS A inventory/service map). Siguiente exacta: al cierre de A → B Linux → C Windows → D Proxmox/TrueNAS → integración → G2 → G4 sesión nueva → reporte.
- **2026-09-17 — SPEC H0 freeze para 2026-09-18:** owner solicita plan detallado y mandato de ejecución en ventana hasta 10 horas. Se crea plan único EN ESTA nota con A/B/C/D, owner bundle T+60, G2/G4, cobertura honesta 59/42/17, timeboxes, stop rules, evidencia/handoff y boundary H1–H6. G0/G1/G3 reconocidos sin reejecución. Cambio documental, no se ejecuta H0 ni se conceden permisos nuevos por esta edición.
- **2026-09-17 — G3 runtime integration post-preflight:** `config.yaml` autorizado, `aranea-ssh` 11 tools + observability 22 tools junto postgres-ro; helper consumer-side PASS, datasource Jaeger/Loki health OK; efectivo próxima sesión. Publicación vault→GitHub en otra máquina verificada. En la sesión nueva todavía falta smoke de carga.
- **2026-09-17 — Preflight G0 mandato Infrastructure Enablement:** `agent-read` 6/6 PASS, discovery 6/6 (`*_20260917_185839.txt`, `inventory_20260917_185839.json`: 59 VMs / 42 running / 17 stopped / 10 storages), smokes `mcps-ops` (26 containers) y `daedalus-ops` PASS. Index/nodo-docs/área corregidos por delta. El hallazgo inicial de sincronización y gap de MCPs de este instante se resolvió luego en G3; ver entrada superior.
- **2026-09-16** — Recovery real del runtime Hermes tras `hermes update`: dashboard + Ariadna `systemd --user`, duplicate legacy gateway deshabilitado, `fleet_restart_pending` reconciliado; skill+runbook federados.
- **2026-09-14** — Workstream creado; H0→H6 y separación management/MCP; Backup/DR reutilizado, no duplicado.

## 🧭 Decisiones

- **I-D01:** management path nativo es obligatorio para recovery del MCP Access Plane y servicios administrados.
- **I-D02:** autoridad progresiva por nivel; no root-equivalent global inicial.
- **I-D03:** storage/backups es el primer dominio operativo por prioridad y porque permite certificar el patrón de seguridad/recovery antes de Proxmox completo.
- **I-D04:** operadores especializados son boundaries de autoridad; su implementación concreta se difiere hasta ver las interfaces reales.
- **I-D05:** gateway operativo `hermes-gateway-ariadna.service`; default legacy permanece disabled mientras comparta identidad Telegram con Ariadna.
- **I-D06 (2026-09-17):** owner adelanta exclusivamente H0 el 2026-09-18 para aprovechar ventana de agentes. Es prioridad de ejecución, no alteración de authority ni habilitación anticipada de H1/H2/H4. Token API RO acredita sólo observación, jamás lifecycle/provisioning.

## 🔗 Docs / Links

- [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] — programa padre.
- [[BACKUP-DR-OWNER-PROJECT]] — source of truth de Backup/DR.
- [[HERMES — Agent Access Operations]] — workstream paralelo del capability plane.
- [[AGENT-PLATFORM - MCP Access Plane]] — plano que Infrastructure Operations debe poder recuperar sin depender de él.
- [[hermes-agent-operator]] — skill agent-facing para operar el runtime Hermes.
- [[hermes-linux-update-recovery]] — runbook mecánico de update/recovery.
- `80-agents/journal/logs/2026-09-17-hermes-infra-preflight-g0.md` — evidencia G0/G1/G3.

## 💡 Ideas

### Backlog de ideas

- Detectar cuáles operators merecen perfil/agent separado después del primer ciclo H0/H1.
- Incorporar drills periódicos de recovery cuando el management plane sea estable.

### Motivos / principios

- La autonomía vale sólo si Hermes puede recuperarse de la falla de las superficies que administra.
- El blast radius debe aumentar más lento que la evidencia de operación segura.
