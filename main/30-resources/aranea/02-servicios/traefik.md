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

# 🔀 traefik

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> [!info]+ traefik
> **VMID:** 115 · **Nodo:** athena · **Tier:** 0a (infraestructura base)
> **Status:** ✅ Running · **Tipo:** lxc container · **Stack:** Debian + Traefik

## 🎯 Propósito

**Reverse proxy HTTPS interno del cluster Aranea.** Traefik recibe requests HTTP/HTTPS externos o internos, los termina (TLS), aplica middlewares (auth, rate limit, headers), y los enruta a los servicios backend correctos vía Docker labels, file provider o Kubernetes ingress.

**Funciones específicas en Aranea**:
- Terminación TLS para subdominios `*.lab.aranea`
- Emisión automática de certificados vía **step-ca** (ACME-compatible)
- Filtro de acceso **LAN-only** (`lan-only@file`) — rechaza tráfico WAN al dashboard
- Dashboard expuesto vía subdominio con **basic-auth**

**Sin traefik**: ningún servicio interno puede exponerse vía HTTPS unificado. Cada servicio tendría que manejar sus propios certs (manual, propenso a expirar).

Contexto mayor: **Aranea es datacenter para el sistema "echo"**. Traefik es el único punto de entrada HTTPS unificado para argus, dashboards de servicios internos, etc.

## 🌐 Acceso

| Tipo | Valor |
|---|---|
| Host (athena PVE) | `192.168.31.10` |
| IP del container | `> [!note] Pendiente: confirmar IP del LXC` |
| URL dashboard (Traefik) | `https://dashboard.lab.aranea` (vía subdominio propio) |
| Dashboard auth | Basic-auth (credenciales en Secret Zero) |
| Puerto HTTP | 80 (default, redirige a HTTPS) |
| Puerto HTTPS | 443 (default) |
| URL admin API | `http://<IP-LXC>:8080/api/` (default, solo LAN) |
| SSH al container | `pct enter 115` (desde host athena) |

## 💾 Storage

- **Disco container:** 16 GB ext4 (`pve-vm--115--disk--0`) en `local-lvm` de athena
- **Datos persistentes:**
  - `/etc/traefik/` — configuración estática (`traefik.yml`) y dinámica (`config/`)
  - `/var/log/traefik/` — access logs, error logs
  - `/tmp/acme/` — certificados emitidos por step-ca (temporal)
- **Backup policy:** → ver `[[BACKUP-DR-DESIGN]]` § <pendiente>
- **Tags:** `community-script`, `proxy`

## 🔐 Secrets

> [!danger] Regla de hierro
> Esta sección SOLO contiene referencias a Secret Zero. NUNCA valores.

| Secret ID | Uso | Storage |
|---|---|---|
| `traefik-basic-auth-credentials` | Hash bcrypt para basic-auth dashboard | `> [!note] Pendiente confirmar ubicación exacta` |
| `step-ca-EAB-key` (si aplica) | External Account Binding para ACME | `> [!note] Pendiente` |
| `traefik-api-auth` | API admin auth (si habilitado) | `> [!note] Pendiente` |

## 🔧 Operación

### Recursos asignados

| Recurso | Valor |
|---|---|
| vCPUs | 2 |
| RAM | 2 GB |
| Disco | 16 GB |
| NetIn (acumulado) | 18 GB |
| NetOut (acumulado) | 3.2 GB |

### Configuración reciente (referencia histórica)

> [!info] Configurado en ticket `2026-06-29-006`
> - `certificatesResolvers.stepca` configurado (integración con step-ca vm 200)
> - Filtros `lan-only@file` (solo IPs `192.168.31.0/24` aceptadas)
> - Basic-auth para dashboard
> - Dashboard expuesto via `dashboard.lab.aranea`

### Restart

```bash
# Desde el host athena
ssh root@192.168.31.10 "pct reboot 115"

# Dentro del container
pct enter 115
systemctl restart traefik
```

> [!warning] Blast radius
> Reiniciar traefik = pérdida temporal del routing HTTPS. Si los servicios dependen de subdominios `*.lab.aranea`, quedan inalcanzables hasta el restart (~5-10s típico).

### Health check

```bash
# Status del container
pct status 115

# API health
curl -fsS http://<IP-LXC>:8080/api/overview

# Dashboard accesible
curl -kI https://dashboard.lab.aranea
```

### Logs

- **Access log:** `pct exec 115 -- tail -f /var/log/traefik/access.log`
- **Error log:** `pct exec 115 -- tail -f /var/log/traefik/traefik.log`
- **Systemd journal:** `pct exec 115 -- journalctl -u traefik -f`

### Update

- **Método:** community-script update o `apt upgrade traefik` (si instalado vía apt)
- **Frecuencia:** Trimestral o ante CVE importante
- **Riesgo:** Traefik 2.x → 3.x requiere migración de config (breaking changes). **Testear en staging primero.**

## 📊 Observabilidad

> [!note] Pendiente owner
> - ¿Traefik expone métricas Prometheus en `/metrics`?
> - ¿Hay dashboard Grafana con rate de requests, latency, errores?
> - ¿Argus (vm 160) ingiere logs de traefik?

Por ahora:
- **NetIn 18 GB / NetOut 3.2 GB** sugiere mucho más request de entrada que salida (típico reverse proxy)
- Si requests de error suben → revisar middlewares o backends caídos

## 🚨 Incidentes

### Runbooks

> [!note] Pendiente crear
> Candidatos:
> - `traefik-down.md` — qué hacer si el dashboard no responde
> - `traefik-cert-renew-fail.md` — si step-ca rechaza emisión
> - `traefik-middleware-bypass.md` — si filtro LAN-only bloquea tráfico legítimo
> - `traefik-config-revert.md` — rollback de config rota

### Known errors

> [!note] Pendiente documentar

### SPOF riesgo (alerta estructural)

> [!warning] SPOF compartido
> Traefik corre en athena junto con opnsense y pi-hole. **Si athena cae, los 3 caen juntos** y la red queda aislada (sin DNS + sin firewall + sin proxy HTTPS).
>
> Mitigación NO implementada: traefik secundario en otro nodo con balanceo via DNS round-robin o CARP.
>
> Ver `[[30-resources/aranea/02-servicios/red]]` § alertas.

## 🔗 Cross-refs

### Servicios en el mismo host (athena)

- [[opnsense]] — abre puertos 80/443 hacia traefik
- [[pi-hole]] — DNS para resolver `*.lab.aranea` si interno
- [[etcd-athena]] — puede guardar config de traefik en etcd

### Servicios que usan traefik como entrada

- [[step-ca]] (vm 200, athena) — emite certs que traefik consume
- [[argus]] (vm 160, hades) — dashboards vía traefik (asumido, no confirmado)
- [[etcd-keeper]] (vm 148, hades) — UI expuesta vía traefik (probable)
- [[docker-hasura]] (vm 129, hades) — GraphQL endpoint vía traefik (probable)
- [[homeassistant]] (vm 105, hades) — dashboard típico vía traefik (probable)
- [[docker-frigate.14]] (vm 137, hades) — UI NVR vía traefik (probable)

### Documentación relacionada

- [[SERVICIOS-DOCS-OWNER-PROJECT]] — proyecto padre
- [[BACKUP-DR-OWNER-PROJECT]] — pendiente tier classification
- [[30-resources/aranea/02-servicios/red]] — doc por categoría
- [[30-resources/aranea/01-topologia/nodo-athena]] — info del host
- [[30-resources/aranea/01-topologia/red]] — topología de red

### Tickets relacionados

- `2026-06-29-006` — configure-traefik-stepca (legacy)
- `2026-06-29-007` — expose-dashboard-via-traefik (legacy)

## 📝 Source files

- `/home/hermes/aranea/topology/inventory_2026-07-02.json` → `vms[]` vmid 115
- `/home/hermes/aranea/topology/services.md` → § Servicios de red
- `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt` → captura raw
- `/home/hermes/obsidian/SecondBrain/main/30-resources/aranea/02-servicios/red.md` → doc por categoría

## ✅ Validation checklist

- [x] Frontmatter completo
- [x] Propósito describe el ROL (incluye funciones específicas)
- [ ] Acceso documentado completo (FALTA: IP del LXC)
- [x] Storage con backup policy ref
- [ ] Secrets con referencias (FALTA: confirmar ubicaciones)
- [x] Operación con restart + health check + logs
- [ ] Observabilidad (FALTA: confirmar métricas)
- [x] Cross-refs bidireccionales con servicios que lo usan
- [x] Sin secrets en plaintext

## 📌 Status

**`partial`** — estructura completa. Pendientes:
1. IP del container
2. Ubicación exacta de credenciales en Secret Zero
3. Confirmar qué servicios están realmente detrás de traefik
4. Runbooks específicos
5. Known errors
