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

# 🕳️ pi-hole

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> [!info]+ pi-hole
> **VMID:** 149 · **Nodo:** athena · **Tier:** 0a (infraestructura base)
> **Status:** ✅ Running · **Tipo:** lxc container · **Stack:** Debian + Pi-hole

## 🎯 Propósito

**DNS sinkhole + ad-blocking para toda la LAN Aranea.** Pi-hole intercepta todas las consultas DNS de la red local (192.168.31.0/24) y bloquea dominios de publicidad, tracking y malware conocidos antes de que resuelvan. También actúa como **DNS recursivo/forwarder** para clientes que no configuran DNS externo.

**Sin pi-hole**: la LAN pierde DNS local (si está configurado como DNS principal de los nodos). Si opnsense lo usa como upstream, la cadena DNS completa cae. **Comparte el SPOF con opnsense y traefik en athena**.

Contexto mayor: **Aranea es datacenter para el sistema de trading algorítmico "echo"**. DNS funcional es crítico para que echo resuelva endpoints externos (feeds de mercado, APIs, brokers).

## 🌐 Acceso

| Tipo | Valor |
|---|---|
| Host (athena PVE) | `192.168.31.10` |
| IP del container | `> [!note] Pendiente: confirmar IP del LXC (típico 192.168.31.X del rango DHCP estático)` |
| URL admin (LAN:port) | `http://<IP-LXC>/admin/` (default Pi-hole) |
| Puerto admin web | 80 (default, HTTP) — puede estar detrás de traefik con HTTPS |
| URL vía Traefik | `> [!note] Pendiente: ¿expuesto vía dashboard.lab.aranea/pihole?` |
| SSH al container | `pct enter 149` (desde host athena) |
| Puerto DNS | 53 (default) |

## 💾 Storage

- **Disco container:** 10 GB ext4 (`pve-vm--149--disk--0`) en `local-lvm` de athena
- **Datos persistentes:**
  - `/etc/pihole/` — config (adlists, dnsmasq.d, pihole-FTL.db)
  - `/var/log/pihole/` — logs
- **Backup policy:** → ver `[[BACKUP-DR-DESIGN]]` § <pendiente> (ticket 018 gating tier classification)
- **Customización:** `> [!note] Pendiente: ¿hay listas de bloqueo custom más allá de las defaults?`

## 🔐 Secrets

> [!danger] Regla de hierro
> Esta sección SOLO contiene referencias a Secret Zero. NUNCA valores.

| Secret ID | Uso | Storage |
|---|---|---|
| `pihole-webpassword` | Login admin web (establecida en setup inicial) | `> [!note] Pendiente confirmar ubicación exacta` |

## 🔧 Operación

### Recursos asignados

| Recurso | Valor |
|---|---|
| vCPUs | 2 |
| RAM | 1 GB |
| Disco | 10 GB |
| NetIn (acumulado) | 128 GB |
| NetOut (acumulado) | 2.6 GB |
| Tags | `adblock`, `community-script` |

### Restart

```bash
# Desde el host athena
ssh root@192.168.31.10 "pct reboot 149"

# O desde dentro del container
pct enter 149
pihole restartdns
```

> [!warning] Blast radius
> Reiniciar pi-hole = DNS cae durante el reboot. Si opnsense está configurado para usar pi-hole como upstream DNS, TODO el cluster pierde resolución DNS hasta que vuelva. **Solo hacerlo en ventana corta o si hay DNS secundario configurado en opnsense.**

### Health check

```bash
# Test DNS desde otro nodo
dig @192.168.31.<IP-PIHOLE> google.com

# Status del container desde el host
pct status 149
pct exec 149 -- pihole status
```

### Logs

- **Pi-hole GUI:** Settings → System (tail logs in GUI)
- **dnsmasq log:** `pct exec 149 -- pihole -t` (tail en tiempo real)
- **FTL log:** `/var/log/pihole-FTL.log` dentro del container

### Update

- **Método:** `pihole -up` (dentro del container) o GUI → Tools → Update
- **Frecuencia:** Semanal para gravity (listas de bloqueo), mensual para Pi-hole core
- **Riesgo:** Update de core puede romper config custom. **Testear post-update.**

## 📊 Observabilidad

> [!note] Pendiente owner
> - ¿Pi-hole expone métricas vía telegraf?
> - ¿Hay dashboard Grafana con queries/día, dominios bloqueados, top clientes?
> - ¿Argus (vm 160) ingiere logs?

Por ahora:
- **NetOut 2.6 GB** es bajo → tráfico DNS típico, OK
- Si NetOut sube mucho → posible loop DNS o amplificación

## 🚨 Incidentes

### Runbooks

> [!note] Pendiente crear
> Candidatos:
> - `pi-hole-dns-down.md` — qué hacer si DNS no resuelve
> - `pi-hole-gravity-fail.md` — si la actualización de listas falla
> - `pi-hole-failover.md` — solo si se implementa Pi-hole secundario

### Known errors

> [!note] Pendiente documentar

### SPOF riesgo (alerta estructural)

> [!warning] SPOF compartido
> Pi-hole corre en athena junto con opnsense y traefik. **Si athena cae, los 3 servicios caen juntos** y la red queda completamente aislada (sin DNS + sin firewall + sin proxy).
>
> Mitigación discutida pero NO implementada: Pi-hole secundario en otro nodo (sincronización de listas vía gravity-sync).
>
> Ver `[[30-resources/aranea/02-servicios/red]]` § alertas.

## 🔗 Cross-refs

### Servicios en el mismo host (athena)

- [[opnsense]] — usa pi-hole como DNS upstream (típico)
- [[traefik]] — puede estar integrado vía DNS challenge si usa certs wildcard
- [[etcd-athena]] — usa pi-hole como DNS

### Dependencias del cluster

- **Todos los nodos Proxmox** que tengan `192.168.31.X` como DNS en `/etc/resolv.conf` dependen de pi-hole
- **Echo trading system** necesita DNS para resolver feeds externos
- **Argus (vm 160)** puede depender de DNS para resolver endpoints de scraping

### Documentación relacionada

- [[SERVICIOS-DOCS-OWNER-PROJECT]] — proyecto padre
- [[30-resources/aranea/02-servicios/red]] — doc por categoría
- [[30-resources/aranea/01-topologia/nodo-athena]] — info del host
- [[30-resources/aranea/01-topologia/red]] — topología de red

### Tickets relacionados

- (ninguno específico de pi-hole)

## 📝 Source files

- `/home/hermes/aranea/topology/inventory_2026-07-02.json` → `vms[]` vmid 149
- `/home/hermes/aranea/topology/services.md` → § Servicios de red
- `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt` → captura raw
- `/home/hermes/obsidian/SecondBrain/main/30-resources/aranea/02-servicios/red.md` → doc por categoría

## ✅ Validation checklist

- [x] Frontmatter completo
- [x] Propósito describe el ROL
- [ ] Acceso documentado completo (FALTA: IP del LXC, URL Traefik)
- [x] Storage con backup policy ref
- [ ] Secrets con referencias (FALTA: confirmar ubicación)
- [x] Operación con restart + health check + logs
- [ ] Observabilidad (FALTA: confirmar dashboards)
- [x] Cross-refs bidireccionales
- [x] Sin secrets en plaintext

## 📌 Status

**`partial`** — estructura completa, datos conocidos. Pendientes:
1. IP del container
2. URL admin concreta + integración con Traefik
3. Listas custom de bloqueo (si existen)
4. Ubicación de webpassword en Secret Zero
5. Runbooks + known errors
