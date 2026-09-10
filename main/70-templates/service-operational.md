---
type: service-doc
schema_version: 1
status: template
area: "[[Aranea]]"
aliases:
  - "{{title}}"
tags:
  - service-doc
  - template
  - aranea
  - kind/service-doc
  - area/aranea
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

> [!warning] Template — NO usar como nota final
> Este archivo es un template. Para crear una nota de servicio real:
> 1. Copiar a `30-resources/aranea/02-servicios/<nombre-servicio>.md`
> 2. Rellenar frontmatter (vmid, node, tier)
> 3. Rellenar cada sección con datos reales (NO inventar)
> 4. Cambiar `status: draft` → `status: partial` → `status: active`
> 5. Borrar este bloque de warning

%% Convention: notas de servicio individuales viven en `30-resources/aranea/02-servicios/<servicio>.md`. El catálogo por categoría (`02-servicios/README.md`) sigue siendo truth-of-record paralelo. %%

---

## 📋 Frontmatter reference

```yaml
---
title: "<nombre-servicio>"        # ej: "opnsense", "pi-hole"
type: service-doc
status: draft                     # draft | partial | active
icon: 🛡️                          # opcional: emoji representativo
vmid: <id>                        # VMID en Proxmox
node: <host>                      # athena | hades | zeus | hera | kronos | truenas
tier: 0a                          # 0a | 0b | 0c | 0d
owner: rodrigo
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases:
  - <alias1>
  - <alias2>
tags:
  - service-doc
  - aranea
  - kind/service-doc
  - area/aranea
  - tier/0a
related:
  - "[[SERVICIOS-DOCS-OWNER-PROJECT]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[<servicios-relacionados>]]"
---
```

---

## 📝 Estructura de la nota (referencia)

```markdown
# <Servicio>

> [!info]+ <Servicio>
> **VMID:** <id> · **Nodo:** <host> · **Tier:** 0a/b/c/d
> **Status:** ✅ running | ⏸️ stopped | ❌ failed

## 🎯 Propósito

[Qué hace realmente en el sistema echo. NO el nombre — el rol concreto.
Ejemplo malo: "firewall".
Ejemplo bueno: "gateway/firewall del cluster Aranea — control plane absoluto. Todo el tráfico north-south pasa por acá. Si cae, el cluster queda aislado."]

## 🌐 Acceso

| Tipo | Valor |
|---|---|
| URL admin (LAN:port) | `https://192.168.31.X:PORT` |
| URL vía Traefik | `https://<subdominio>.<dominio>.local` |
| SSH | `ssh root@192.168.31.X` |
| API endpoint | `http://192.168.31.X:PORT/api/v1/...` |
| Dashboard | `https://<subdominio>.<dominio>.local/dashboard` |

> [!warning] Secret Zero discipline
> Si alguna URL lleva credencial embebida (ej: `postgres://user:pass@host`),
> redactar como `postgres://USER:PASS@host → ver Secret Zero → <secret-id>`.
> NUNCA escribir el valor del secret en la nota.

## 💾 Storage

- **Datasets / volúmenes:** (ZFS datasets, LVM volumes, RBD)
- **Mount paths:** (`/mnt/...`, `/var/lib/...`)
- **Backup policy:** → ver `[[BACKUP-DR-DESIGN]]` § <sección>

## 🔐 Secrets

> [!danger] Regla de hierro
> Esta sección SOLO contiene referencias a Secret Zero. Nunca valores.

| Secret ID | Uso | Storage |
|---|---|---|
| `secret-zero → <id>` | <para qué se usa> | `[[20-areas/Aranea#Secret-Zero]]` |

## 🔧 Operación

### Restart

```bash
# Comando exacto (read-only primero)
ssh root@<node> "qm stop <vmid> && qm start <vmid>"
```

### Health check

```bash
# Comando de verificación
curl -fsS http://192.168.31.X:<port>/health || echo "DOWN"
```

### Logs

- **Path:** `/var/log/<servicio>/...`
- **Comando:** `journalctl -u <servicio> -f`

### Update

- **Método:** (apt upgrade / docker pull / custom script)
- **Frecuencia:** (manual / auto / patch tuesday)

## 📊 Observabilidad

- **Métricas Prometheus:** (endpoint scrape, ej: `/metrics`)
- **Alertas Grafana:** (dashboard ID)
- **Dashboards argus:** (si el servicio expone a argus vm 160)

## 🚨 Incidentes

- **Runbook:** → `[[30-resources/aranea/runbooks/<servicio>]]`
- **Known errors:** → `[[80-agents/memory/public/known-errors/<servicio>]]`

## 🔗 Cross-refs

- [[SERVICIOS-DOCS-OWNER-PROJECT]] — proyecto padre
- [[BACKUP-DR-OWNER-PROJECT]] — si el servicio está en tier de backup
- [[BACKUP-DR-DESIGN]] — política de backup del servicio
- [[30-resources/aranea/02-servicios/<categoría>]] — doc por categoría
- [[30-resources/aranea/01-topologia/nodo-<host>]] — info del nodo host
- Servicios relacionados: [[<servicio-1>]], [[<servicio-2>]]

## 📝 Source files

- `<host>:<ruta-de-inventario>/inventory_YYYY-MM-DD.json` — VMID/nodo/status
- `<host>:<ruta-de-inventario>/services.md` — descripción de categoría
- `<host>:<ruta-de-inventario>/discovery/<host>_YYYYMMDD_HHMMSS.txt` — discovery raw

Se registra host + ruta relativa a esa raíz, nunca la ruta absoluta de una máquina.

## ✅ Validation checklist (antes de marcar `status: active`)

- [ ] Frontmatter completo (vmid, node, tier, owner)
- [ ] Propósito describe el ROL, no solo el nombre
- [ ] Acceso documentado (al menos LAN:port + SSH)
- [ ] Storage con datasets/mounts/backup policy
- [ ] Secrets con SOLO referencias (grep debe dar 0 secrets en claro)
- [ ] Operación con restart + health check + logs
- [ ] Cross-refs bidireccionales (esta nota aparece en otras notas relacionadas)
- [ ] Sin secrets en plaintext (verificado con `grep -E '(password|token|api_key)'`)
```

---

## 🎯 Tier definitions (referencia)

| Tier | Definición | Servicios |
|---|---|---|
| **0a** | Infraestructura base — sin estos NADA funciona | opnsense, pi-hole, traefik |
| **0b** | Storage — sostiene todos los servicios | truenas |
| **0c** | Cluster quorum crítico — warning feo si baja de 3 | etcd (5) + kafka (3) |
| **0d** | Sistema echo (trading algorítmico) — el core | mt4 (4) + echo + postgres + mongo + argus + flink + hasura |

---

## 📌 Source files

- `10-projects/Aranea/SERVICIOS-DOCS-OWNER-PROJECT.md` — proyecto padre
- `10-projects/Aranea/agentes/agent-project-09-service-docs-rollout.md` — subproyecto agente
- `30-resources/aranea/02-servicios/README.md` — catálogo por categoría (truth-of-record paralelo)
