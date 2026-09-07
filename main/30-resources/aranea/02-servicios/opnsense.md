---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# 🛡️ opnsense

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> [!info]+ opnsense
> **VMID:** 130 · **Nodo:** athena · **Tier:** 0a (infraestructura base)
> **Status:** ✅ Running · **Tipo:** qemu VM · **Stack:** FreeBSD / OPNsense

## 🎯 Propósito

**Gateway/firewall del cluster Aranea — control plane absoluto de red.** Todo el tráfico north-south (WAN ↔ LAN) del cluster pasa por acá. Es el **único punto** donde se aplican reglas de firewall, NAT y segmentación.

**Sin opnsense**: el cluster queda sin acceso a internet, sin segmentación de red, sin protección perimetral. **Es el SPOF #1 de Aranea** (corre como VM dentro del host athena, que también es SPOF — si athena cae, opnsense cae con él).

Contexto mayor: **Aranea NO es un homelab hobby — es un datacenter para el sistema de trading algorítmico "echo"**. Opnsense es la frontera que protege echo del mundo externo.

## 🌐 Acceso

| Tipo | Valor |
|---|---|
| Host (athena PVE) | `192.168.31.10` |
| Gateway WAN | `192.168.31.1` |
| VM gateway interno | `> [!note] Pendiente: confirmar IP LAN de la VM opnsense` |
| URL admin (LAN:port) | `> [!note] Pendiente: confirmar puerto admin (típico 8443 HTTPS)` |
| SSH (FreeBSD) | `> [!note] Pendiente: confirmar si SSH está habilitado y bajo qué puerto` |
| Dashboard web | `> [!note] Pendiente: URL exacta del dashboard` |

> [!warning] Secret Zero discipline
> Si la URL lleva credenciales embebidas (ej: `https://user:pass@...`), redactar como `USER:PASS → ver Secret Zero → opnsense-admin`. **Nunca** escribir el valor del secret en esta nota.

## 💾 Storage

- **Disco VM:** 64 GB (`pve-vm--130--disk--0`, 4 MB efivars) en `local-lvm` de athena
- **Tipo:** qemu virtual disk
- **Backup policy:** → ver `[[BACKUP-DR-DESIGN]]` § <sección a definir> (actualmente PENDING — depende de OWNER-TASK-CRITICAL-VMS ticket 018)
- **Configuración persistida:** FreeBSD root filesystem (dentro del disco de 64 GB)

## 🔐 Secrets

> [!danger] Regla de hierro
> Esta sección SOLO contiene referencias a Secret Zero. NUNCA valores.

| Secret ID | Uso | Storage |
|---|---|---|
| `opnsense-admin-password` | Login admin web | `> [!note] Pendiente confirmar ubicación exacta en Secret Zero` |
| `opnsense-api-key` | API REST (si aplica) | `> [!note] Pendiente` |

## 🔧 Operación

### Recursos asignados

| Recurso | Valor |
|---|---|
| vCPUs | 8 |
| RAM | 8 GB |
| Disco | 64 GB |
| NetIn (acumulado) | 1.72 TB |
| NetOut (acumulado) | **6.20 TB** ← todo el tráfico WAN del cluster |

### Restart

```bash
# Desde el host athena (vía agent-read, no directo)
ssh root@192.168.31.10 "qm stop 130 && qm start 130"
```

> [!warning] Blast radius
> Reiniciar opnsense = **toda la red Aranea cae durante el reboot** (~30-60s típico OPNsense). Solo hacerlo en ventana de mantenimiento o emergencia justificada.

### Health check

```bash
# Ping al gateway (verifica que la VM responde)
ping -c 3 192.168.31.1

# Verificar reglas NAT/firewall activas
# (vía dashboard web, no CLI directo)
```

### Logs

- **OPNsense GUI:** System → Log Files (todos los subsistemas)
- **FreeBSD:** `/var/log/` (system, security, filter)
- **Comando desde la VM:** `clog /var/log/filter.log` (mostrar log de firewall en tiempo real)

### Update

- **Método:** OPNsense GUI → Firmware → Updates (con confirm)
- **Frecuencia:** Mensual (releases menores OPNsense)
- **Riesgo:** Update con cambio mayor puede romper NAT/VLAN. **Testear en ventana de mantenimiento.**

## 📊 Observabilidad

> [!note] Pendiente owner
> - ¿Hay métricas Prometheus exportadas desde OPNsense? (vía telegraf + opnsense_exporter)
> - ¿Hay alertas Grafana configuradas para opnsense?
> - ¿Argus (vm 160) ingiere logs de firewall?

Por ahora:
- **NetOut 6.20 TB** es la métrica informal más útil (todo el tráfico WAN)
- Si NetOut cae a 0 → probablemente opnsense está caído o particionado

## 🚨 Incidentes

### Runbooks

> [!note] Pendiente crear
> No existe runbook específico para opnsense en `30-resources/aranea/runbooks/`. Candidatos:
> - `opnsense-down.md` — qué hacer si la VM no responde
> - `opnsense-failover.md` — solo relevante si se implementa HA con CARP
> - `opnsense-rule-conflict.md` — troubleshooting de reglas que rompen tráfico legítimo

### Known errors

> [!note] Pendiente documentar
> Sin known errors registrados aún.

### SPOF riesgo (alerta estructural)

> [!danger] SPOF documentado en múltiples notas
> **athena → opnsense** es el SPOF #1 de Aranea. Si athena cae:
> - opnsense cae
> - DNS cae (pi-hole en athena)
> - Reverse proxy cae (traefik en athena)
> - Toda la red queda aislada
>
> Mitigaciones discutidas pero NO implementadas:
> - HA con CARP (2 opnsense en nodos distintos)
> - Migración de opnsense a hardware dedicado
> - Backup mínimo: OPNsense config export + restore proced documented
>
> Ver `[[00-index]]` § Top 5 alertas, alerta #1.

## 🔗 Cross-refs

### Servicios en el mismo host (athena)

- [[pi-hole]] — DNS, también en athena (SPOF compartido)
- [[traefik]] — reverse proxy, también en athena (SPOF compartido)
- [[etcd-athena]] — etcd member, también en athena (etcd cluster tiene quórum distribuido, no es SPOF)

### Dependencias del cluster

- **Todos los nodos Proxmox** dependen del routing vía opnsense para tráfico WAN
- **etcd cluster** usa opnsense solo para DNS externo (si lo hay)
- **Echo trading system** (vm 140, 124, 133, 134, 144) usa opnsense para feeds de mercado externos

### Documentación relacionada

- [[SERVICIOS-DOCS-OWNER-PROJECT]] — proyecto padre de esta nota
- [[BACKUP-DR-OWNER-PROJECT]] — pendiente clasificación tier 0 (ticket 018)
- [[30-resources/aranea/02-servicios/red]] — doc por categoría (referencia)
- [[30-resources/aranea/01-topologia/nodo-athena]] — info del host
- [[30-resources/aranea/01-topologia/red]] — topología de red
- [[30-resources/aranea/00-index]] § Top 5 alertas — alerta #1 (opnsense SPOF)

### Tickets relacionados

- (ninguno específico de opnsense en `10-projects/Aranea/05-tickets/`)
- `2026-06-29-006` y `2026-06-29-007` (tickets legacy, configuración traefik+stepca)

## 📝 Source files

- `/home/hermes/aranea/topology/inventory_2026-07-02.json` → `vms[]` vmid 130
- `/home/hermes/aranea/topology/services.md` → § Servicios de red
- `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt` → captura raw
- `/home/hermes/obsidian/SecondBrain/main/30-resources/aranea/02-servicios/red.md` → doc por categoría
- `/home/hermes/obsidian/SecondBrain/main/30-resources/aranea/01-topologia/nodo-athena.md` → info del host

## ✅ Validation checklist

- [x] Frontmatter completo (vmid, node, tier, owner)
- [x] Propósito describe el ROL, no solo el nombre
- [ ] Acceso documentado completo (FALTA: URL admin, puerto, SSH)
- [x] Storage con datasets/mounts/backup policy ref
- [ ] Secrets con referencias (FALTA: confirmar ubicación exacta)
- [x] Operación con restart + health check + logs
- [ ] Observabilidad (FALTA: confirmar si hay Prometheus/argus)
- [x] Cross-refs bidireccionales con servicios del mismo host
- [x] Sin secrets en plaintext (verificado)

## 📌 Status

**`partial`** — la nota tiene la estructura y datos conocidos, pero faltan:
1. URL admin concreta + puerto
2. SSH habilitado / puerto
3. Confirmar ubicación de secrets en Secret Zero
4. Runbooks específicos (no existen)
5. Known errors (no hay registro)
6. Observabilidad (no confirmada)

**Próximo paso**: owner completa los `> [!note] Pendiente` con datos reales (puede ser en este chat o editando la nota directamente en Obsidian).
