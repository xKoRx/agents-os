---
type: index
schema_version: 1
status: active
icon: 🔗
slug: aranea-integration
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
created: "2026-09-19"
updated: "2026-09-19"
reviewed: "2026-09-19"
aliases:
  - Aranea integration index
  - H6 integrated capabilities
  - catalogo integrado H6
  - matriz routing H6
cssclasses:
  - wide
tags:
  - kind/index
  - area/aranea
  - domain/aranea
  - action/orchestration
  - project/hermes-aranea-autonomous-operations
---

# 🔗 Aranea — Integración de Capacidades (H6)

> [!info] Índice de integración H6 — enablement-only
> **Mandato:** H6 ONE-SHOT 2026-09-19 · **Veredicto:** `H6 ENABLEMENT PASS — VERIFIED SCOPE` · **Mutaciones de infraestructura: 0**
> Integra las capacidades certificadas en H0–H5: catálogo único, routing por proyecto ejecutor, cadena de orquestación, dependencias multicapa y negativos de decisión. La **ejecución** de operaciones pertenece a los proyectos ejecutores; ningún contenido de este índice autoriza operaciones. `INTEGRATED ENABLEMENT CERTIFIED` ≠ `OPERATIONAL READINESS` ≠ `OPERATIONAL AUTONOMY`.
> Contrato de orquestación: [[integrated-orchestration-contract]] · Evidencia: `~/aranea/work/h6-integration-20260919/`.

## 📊 Catálogo integrado de capacidades

Clasificaciones usadas: `ENABLED` (canal+identidad+lectura demostrados), `ENABLED_WITH_LIMITATIONS` (demostrado con alcance acotado documentado), `AUTHORIZED_NOT_EXERCISED` (ruta existe, no ejercida por diseño enablement), `OPERATIONALLY_CERTIFIED` (ejecutado y verificado por proyecto ejecutor — hoy casi vacío por diseño), `GATED` (requiere owner gate), `BLOCKED`, `NOT_PROVEN`, `OUT_OF_SCOPE`, `NOT_CERTIFIED`. Denominador: 15 capacidades evaluadas (C01–C15).

| ID | Capacidad | Resuelve | Proyecto ejecutor responsable | Targets | Canal / identidad | Estado enablement | Certificación operacional | Contrato canónico | Gate |
|---|---|---|---|---|---|---|---|---|---|
| C01 | Inventario y diagnóstico | Reconstruir estado real de hosts/guests/servicios sin mutar | Infrastructure Operations (este carril) | 5 PVE + TrueNAS + PBS + 59 guests (H0) | SSH `ariadna_*` +sudo; API token `/vms`; WS TrueNAS; `qm guest cmd` | ENABLED (H0–H5, ejercicio continuo) | OPERATIONALLY_CERTIFIED (lectura, uso repetido) | Matrices H0/H5 + [[integrated-orchestration-contract]] | ninguno (lectura) |
| C02 | Administración Proxmox (lifecycle) | Inspeccionar/operar VMs y LXC en el clúster | Proyecto ejecutor Proxmox (por crear) | 5 nodos PVE 8.4.20; 59 guests | SSH `ariadna`+sudo (root-equivalent); token API NO-servible | ENABLED (clasificado H2; mutación AUTHORIZED_NOT_EXERCISED) | NOT_CERTIFIED (ejecutor) | [[proxmox-lifecycle-operator-contract]] | CLASS 2/3 según op |
| C03 | Administración Linux/LXC | Operar guests Linux (systemd, FS, usuarios) | Proyecto ejecutor del servicio correspondiente | guests Linux; LXC 113 mcps | SSH nativo / `mcps-ops` / `qm guest cmd` | ENABLED (H3) | NOT_CERTIFIED (ejecutor) | [[linux-container-operator-contract]] | CLASS 1/2 |
| C04 | Administración Windows | Administrar Windows nativo | Proyecto ejecutor del servicio correspondiente | SOLO worker-kronos VM 135 | SSH `ariadna_win` (from=.122) | ENABLED_WITH_LIMITATIONS (W1; sólo VM 135) | NOT_CERTIFIED (ejecutor) | [[windows-operator-contract]] | CLASS 1/2; fuera de 135 = NOT_CERTIFIED |
| C05 | Lifecycle de servicios | Diagnosticar/preparar recuperación de un servicio | Proyecto ejecutor del servicio (Echo/Forge/otro) | servicios del catálogo H0 (58) | nativo por guest; MCP = consumer plane | ENABLED (H3) | NOT_CERTIFIED (ejecutor) | [[service-lifecycle-operator-contract]] | CLASS 2 en PROD |
| C06 | Docker/Compose | Administrar contenedores | Agent Access Operations (mcps) / ejecutor del servicio | 26 contenedores mcps (LXC 113); daedalus 141 | `sudo docker` vía `mcps-ops` (nativo) | ENABLED (H0/H3) | NOT_CERTIFIED (ejecutor) | [[linux-container-operator-contract]] + skill `mcp-access-plane-operations` | CLASS 1/2 |
| C07 | Provisioning VM Linux | Crear VM nueva | Proyecto consumidor/ejecutor (por crear) | clon 117/120 o ISO @nfs-storage | SSH+sudo (AUTHORIZED_NOT_EXERCISED) | ENABLED (H4; sin ejercicio) | NOT_CERTIFIED (ejecutor) | [[provisioning-operator-contract]] | capacidad por storage + backup/observability gates |
| C08 | Provisioning LXC | Crear LXC nuevo | Proyecto consumidor/ejecutor (por crear) | `pct create` debian-13 vztmpl | SSH+sudo (AUTHORIZED_NOT_EXERCISED) | ENABLED (H4; sin ejercicio) | NOT_CERTIFIED (ejecutor) | [[provisioning-operator-contract]] | ídem C07 |
| C09 | Provisioning Windows | Crear VM Windows | — | template 109 / ISO | — | NOT_PROVEN (W1 ≠ creación) | NOT_PROVEN | — (sin ruta habilitada) | EXECUTOR_NOT_DEFINED + NOT_PROVEN |
| C10 | Backup/DR (protección, jobs, restores, drills) | Proteger workloads; verificar restores | [[BACKUP-DR-OWNER-PROJECT]] (R0–R8) | PBS 180 + R1 staging + timers | SSH `ariadna_pbs`/`ariadna_pve`; plano R2 propio | ENABLED (H1) + ejecución R1/R1.5/R2 del proyecto | OPERATIONALLY_CERTIFIED (parcial: R1/R1.5 + fail-closed R2; piloto 7d ACTIVE, falta 7/7 días) | [[BACKUP-DR-OWNER-PROJECT]] + BACKUP-DR-RUNBOOK | owner tickets 018/019; D tras piloto |
| C11 | Networking/DNS/DHCP | Operar gateway/DNS/resolución | Proyecto de networking (por crear) | OPNsense 130, Pi-hole 149, Tailscale 119 | host-mediated (qm/pct); config interna NO legible | ENABLED_WITH_LIMITATIONS (H5 A/B: sólo lectura externa) | NOT_CERTIFIED; recovery NOT_CERTIFIED | [[high-impact-networking-dns-contract]] | CLASS 3 owner-gated |
| C12 | Cluster maintenance / quorum | Mantenimiento de nodos, quorum, HA | Proyecto de cluster-maintenance (por crear) | 5 nodos, corosync LAN-only | SSH+sudo 5/5 (ejercido lectura) | ENABLED (H5 C/J) | NOT_CERTIFIED; node-loss NOT demostrado | [[cluster-node-maintenance-contract]] | CLASS 3 (node ops) |
| C13 | Ceph / storage distribuido | Operar OSD/MON/pools; resolver nearfull | Proyecto Ceph (por crear) | pool1 (87.29% 2026-09-19), 4 OSD, 3 MON | SSH+sudo desde zeus/hera/kronos (athena sin conf) | ENABLED (H5 D; VERIFIED_READ) | NOT_CERTIFIED; NO_GO provisioning vigente | [[ceph-storage-operations-contract]] | CLASS 3 owner-gated |
| C14 | TrueNAS (admin storage compartido) | Pools/datasets/shares/snapshots | [[BACKUP-DR-OWNER-PROJECT]] / ejecutor storage | VM 145 @hades | SSH+WS FULL_ADMIN (H1) | ENABLED (H1, revalidado H5) | NOT_CERTIFIED (mutaciones); SSH ejercido | Matriz H1 ([[HERMES — Infrastructure Operations]]) | CLASS 2/3 |
| C15 | Recovery del management plane | Recuperar acceso/administración cuando falla una capa | Infrastructure Operations (self) + owner break-glass | hermes-vm 118, mcps LXC, keys | self systemd; `mcps-ops`; consola owner | ENABLED (recovery hermes-vm demostrado 2026-09-16) | OPERATIONALLY_CERTIFIED (hermes-vm); resto parcial | [[hermes-linux-update-recovery]] + [[integrated-orchestration-contract]] | CLASS 2 |

**Síntesis del denominador:** ENABLED u operación equivalente = 12/15 (C01–C08, C10, C14, C15, con C04 acotada); `NOT_PROVEN`/sin ruta = C09; `ENABLED_WITH_LIMITATIONS` = C04/C11. `OPERATIONALLY_CERTIFIED` sólo donde un proyecto ejecutor demostró la operación (C01 lectura, C10 parcial R1/R2, C15 hermes-vm). **ENABLEMENT PASS ≠ OPERATIONAL AUTONOMY.**

## 🧭 Matriz de ownership y routing (NEED → ejecutor)

Regla dura: **no existe proyecto ejecutor ⇒ `EXECUTOR_NOT_DEFINED`** — no se asigna silenciosamente a Infrastructure Operations. Infrastructure Operations habilita, certifica accesos y coordina; no ejecuta operaciones de otros dominios. Nota de navegación: los contratos de operador citados en esta matriz viven en `30-resources/runbooks/` (enlazados abajo y en el índice de runbooks). Las fichas de proyecto propuestas, si el owner aprueba crearlas, se materializan como notas `type: project` en `10-projects/Aranea/agentes/` desde `70-templates/` mediante el contrato ejecutable (`materialize_schema_note.py`, constitución regla 13) — no se crean por iniciativa del carril.

| Necesidad (ejemplos reales) | Dominio | Proyecto ejecutor | Capacidades | Autoridad/gate | Contrato | Handoff hacia |
|---|---|---|---|---|---|---|
| Nuevo servicio DEV en VM/LXC | provisioning | Proyecto consumidor (por crear) | C07/C08 + C10 onboarding + observability | capacidad storage (pool1 NO_GO) + backup gate | [[provisioning-operator-contract]] | ficha de proyecto propuesta |
| Servicio dejó de responder (diagnóstico/recuperación) | guest/service | Proyecto del servicio (Echo/Forge/otro) | C01→C03/C05 | CLASS 2 en PROD; target proof | [[service-lifecycle-operator-contract]] | proyecto del servicio |
| Nuevo workload necesita protección | Backup/DR | [[BACKUP-DR-OWNER-PROJECT]] | C10 (+C07 si requiere guest) | tickets 018/019; D post-piloto | [[BACKUP-DR-OWNER-PROJECT]] | R2+/R3 del proyecto |
| Ceph nearfull / operación OSD-pool | storage distribuido | Proyecto Ceph (por crear) | C13 | CLASS 3 owner gate | [[ceph-storage-operations-contract]] | ficha de proyecto propuesta |
| Mantenimiento de nodo / quorum | cluster | Proyecto cluster-maintenance (por crear) | C12 | CLASS 3 + ventana owner | [[cluster-node-maintenance-contract]] | ficha de proyecto propuesta |
| Gateway/DNS caído o por operar | networking | Proyecto de networking (por crear) | C11 | CLASS 3 owner gate | [[high-impact-networking-dns-contract]] | ficha de proyecto propuesta |
| Capacidad MCP nueva / repair | agent access | [[HERMES — Agent Access Operations]] | C06 + familia A0–A5 | A2–A5 gates propios | skill `mcp-access-plane-operations` | su cola de blockers |
| Admin TrueNAS (shares/snapshots) | storage compartido | Backup/DR o ejecutor storage | C14 | CLASS 2/3 | matriz H1 | proyecto storage |
| Falta de acceso/identidad nueva | enablement | Infrastructure Operations (este carril) | C01/C15 | decisión owner si amplía autoridad | este índice + [[integrated-orchestration-contract]] | owner action bundle |

**Fichas de proyecto ejecutor propuestas (NO creadas ni iniciadas por H6):** (1) *Proyecto Proxmox Lifecycle* — consumiría C02/C07/C08, hereda [[proxmox-lifecycle-operator-contract]] + [[provisioning-operator-contract]]; (2) *Proyecto Ceph Storage* — consumiría C13, [[ceph-storage-operations-contract]], primera tarea = resolver nearfull con owner gate; (3) *Proyecto Networking/DNS* — consumiría C11, [[high-impact-networking-dns-contract]], primero cerrar recovery OPNsense; (4) *Proyecto Cluster Maintenance* — consumiría C12, [[cluster-node-maintenance-contract]]. La decisión de crearlos es del owner.

## ⚖️ Autoridad multicapa (transiciones entre sistemas)

Las credenciales de un sistema NO se propagan a otro. Cada transición exige su propio proyecto/autoridad/identidad/canal/gate. Ejemplos concretos vigentes:

| Transición | Lo que NO implica | Gate independiente requerido |
|---|---|---|
| root Proxmox (SSH+sudo nodos) → operación dentro de un guest MT5 | autorización sobre MT5/Echo | proyecto del workload + CLASS según superficie (MT5 = trading execution, siempre gated) |
| admin TrueNAS FULL → cambiar protección Backup/DR | autoridad sobre jobs/retención PBS | proyecto Backup/DR (sus tickets/decisión owner) |
| W1 nativo VM 135 → cualquier otra Windows | flota Windows habilitada | enablement por VM (NOT_CERTIFIED fuera de 135) |
| poder crear VM (C07/C08) → poner el servicio en producción | autorización de go-live | gates de onboarding: backup demostrado + observability + health (si falta backup ⇒ GO-LIVE BLOCKED) |
| contrato Ceph → reparar nearfull | autorización de ejecución | proyecto ejecutor + owner gate CLASS 3 |
| token `ariadna@pve!backup-dr` → gestión/lifecycle | permisos de mutación | sólo SSH/sudo certificado; token queda read-only `/vms` |

CLASS 1 = baja (DEV/test, reversible trivialmente) · CLASS 2 = media (PROD/servicios, ventana+evidencia) · CLASS 3 = alta (networking/cluster/Ceph/host/UPS: irreversibilidad o corte masivo) — CLASS 3 owner-gated sin excepción; H6 no propone autorización global permanente.

## ⛓️ Dependencias del management plane y recovery decision tree

Grafo vigente (corroborado H5 2026-09-19; revalidar antes de operar tras cambios):

```text
Ariadna/Hermes (hermes-vm VM 118 @kronos, .122)
  ├─ host: kronos (PVE) ─ quorum 5/5 LAN (corosync SIN red dedicada)
  ├─ red: LAN 192.168.31.0/24 ← OPNsense VM 130 @athena (SPOF: athena+130)
  ├─ DNS: .31 Pi-hole (LXC 149 @athena) → upstream .1 (router ISP)
  ├─ storage guests: pool1 Ceph (NO_GO nearfull) / local-lvm / nfs-storage (TrueNAS VM 145 @hades, turtles)
  ├─ management: SSH keys ariadna_pve×5 / truenas / pbs / ariadna_win — sin dependencia del MCP
  └─ herramientas: hermes CLI (self), mcps-ops → LXC 113 @hades (26 conts), consola PVE owner = break-glass universal
```

Single points of failure y pérdida simultánea: athena (gateway+DNS+CA+tailscale) degrada LAN, quorum corosync y MONs Ceph a la vez; kronos cae ⇒ hermes-vm + PBS + sqx-kronos caen juntos; `from=.122` de las keys ⇒ hermes-vm muerto/cambiado de IP = acceso nativo exige consola owner.

Decision tree (basado en evidencia; ningún caso provocado):

```text
FALLA X → ¿el canal de administración de X sigue disponible?
├─ MCP Access Plane caído (contenedor/proxy en mcps)
│    → usar management path nativo certificado (SSH mcps-ops / keys propias). NO simular que el plano consume está vivo. [demostrado H0/G4; lección reutilizada]
├─ un servicio/guest caído
│    → C01 diagnóstico por canal nativo → proyecto del servicio ejecuta recuperación (C05) con preflight/rollback del handoff
├─ hermes-vm (VM 118) caída
│    → OWNER_OR_EXTERNAL_RECOVERY_REQUIRED: Ariadna NO puede asumirse capaz de auto-recuperarse;
│      rutas reales: consola PVE del owner (break-glass) o re-IP + reinstalación de authorized_keys (from=.122). [ninguna alternativa autónoma demostrada]
├─ red de gestión caída (OPNsense/LAN)
│    → NO asumir SSH disponible; acceso físico/consola owner; recovery NOT_CERTIFIED (recovery decision tree de OPNsense no existe)
├─ storage de un guest degradado (Ceph nearfull/latencia)
│    → NO asumir que un reinicio resuelve el incidente; C13 read-only + handoff a proyecto Ceph; NO_GO provisioning vigente
├─ Ceph degradado seriamente (quorum MONs perdido)
│    → recovery NOT_CERTIFIED: ninguna recuperación automática sin contrato y gate operativo; owner gate CLASS 3
├─ PBS/backup pipeline degradado
│    → NO simular protección disponible; estado real en [[BACKUP-DR-OWNER-PROJECT]]; fail-closed ya demostrado evita escrituras huérfanas
└─ nodo PVE caído (node-loss)
     → recovery NOT demostrado; quorum 5/5 sobrevive pérdida de 1; procedimiento [[cluster-node-maintenance-contract]]; ejecución = proyecto + ventana owner
```

Recuperaciones demostradas vs no demostradas: DEMOSTRADO = hermes-vm update/recovery (2026-09-16), PBS reboot+fail-closed (R2, 2026-09-19), restore drills R1/R1.5 (traefik/etcd/second-brain/hermes-state), MCP ssh-mcp restart por mcps-ops. NO DEMOSTRADO (NOT_CERTIFIED) = OPNsense, step-ca, UPS (sin superficie), node-loss, recuperación Ceph, quorum-rebuild.

## 🔍 Negativos H6 (decisiones sin ejecutar operaciones)

| ID | Situación | Clasificación correcta | Nota |
|---|---|---|---|
| N1 | Solicitud ambigua (sin environment/need/target) | AMBIGUOUS — no ejecutar; pedir precisión | entrevistable, no inferible |
| N2 | Capacidad administrativa disponible pero proyecto sin autorización | GATED | credenciales ≠ permiso |
| N3 | Operación CLASS 3 sin aprobación | OWNER_GATE_REQUIRED | sin excepción |
| N4 | Provisioning sobre pool1 nearfull (87.29% vivo 2026-09-19) | NO_GO (capacidad, estado vivo) | [[provisioning-operator-contract]] |
| N5 | Workload con backup obligatorio no demostrado pide go-live | GO_LIVE_BLOCKED | gates de onboarding H4 |
| N6 | Solicitud Windows fuera de VM 135 | NOT_CERTIFIED | alcance W1 |
| N7 | MCP indisponible | usar canal nativo si existe (sin provocar la falla) | independencia demostrada |
| N8 | Hermes VM caída | OWNER_OR_EXTERNAL_RECOVERY_REQUIRED | sin alternativa autónoma demostrada |
| N9 | Operación sin proyecto ejecutor | EXECUTOR_NOT_DEFINED | no reasignar silenciosamente |
| N10 | Fuentes contradictorias o captura antigua | CONFLICT / STALE — revalidar en vivo; no adivinar | frescura < 7 días para decisión crítica |

## 🔗 Links

- [[integrated-orchestration-contract]] — cadena REQUEST→AGENTS-OS UPDATE y contrato de estados.
- [[HERMES — Infrastructure Operations]] — matrices de autoridad H1–H5 (autoridad por target/canal).
- [[30-resources/aranea/06-high-impact/00-index|06-high-impact]] — blast radius CLASS 1–3 y brechas de recovery.
- [[BACKUP-DR-OWNER-PROJECT]] — estado vivo de protección (fuente del estado, no este índice).
- [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] — programa padre.
- [[30-resources/aranea/01-topologia/fechas-captura|fechas-captura]] — fecha de cada captura.
