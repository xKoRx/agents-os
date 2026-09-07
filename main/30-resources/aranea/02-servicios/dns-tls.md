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

# DNS & TLS

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28 + tickets 2026-06-29

## DNS — Pi-hole (lxc/149)

Ver [[red]] § Pi-hole para detalle.

- **VMID**: 149
- **Nodo**: athena
- **Estado**: ✅ Running

## TLS — step-ca (CA interna)

> [!note] step-ca instalado y operativo
> step-ca corre en un LXC en athena (CTID 200 según ticket 005). Configurado y emitiendo certificados para Traefik.

### Línea de tiempo relevante

| Ticket | Estado | Qué hizo |
|---|---|---|
| `2026-06-29-001` | failed | Crear LXC ca-aranea (CTID 112) — falló por bug del wrapper |
| `2026-06-29-002` | failed | Retry post-fix wrapper |
| `2026-06-29-003` | failed | Retry2 con CTID 200, 20G disk |
| `2026-06-29-004` | failed | Retry3 |
| `2026-06-29-005` | applied | Instalar step-ca en LXC CTID 200 ✅ |
| `2026-06-29-006` | applied | Configurar Traefik con `certificatesResolvers.stepca` ✅ |
| `2026-06-29-007` | applied | Exponer `dashboard.lab.aranea` via Traefik con TLS step-ca ✅ |
| `2026-06-29-008` | applied | Eliminar doble auth dashboard — túnel SSH reverso Hermes→Traefik ✅ |

### step-ca server

- **FQDN**: `ca.lab.aranea`
- **IP**: `192.168.31.12/24`
- **OS**: Debian 12 (LXC)
- **CTID**: 200

> Ver `~/aranea/tickets/2026-06-29-005-install-step-ca.md` para detalle.

### Certificados emitidos

- `dashboard.lab.aranea` (expuesto vía Traefik con certResolver stepca)
- Wildcard `*.lab.aranea` configurado

## DNS wildcard `*.lab.aranea`

- Funcional y validado en tickets `2026-06-29-001..007`
- Resolución apuntando a Pi-hole o similar

## Stack final de TLS

```
step-ca (CTID 200, athena)              ← CA interna
       ↓ emite cert
Traefik (lxc/115, athena)               ← reverse proxy
       ↓ publica con HTTPS
dashboard.lab.aranea                    ← servicio del usuario
```

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟡 | step-ca SPOF en athena — si athena cae, no se emiten nuevos certs |
| 2 | 🟡 | Renovación automática de certificados no documentada explícitamente |
| 3 | 🟡 | Sin backup de la CA (claves privadas, BD de step-ca) — **Task 2 debería cubrirlo** |

---

**Source files**: `/home/hermes/aranea/tickets/2026-06-29-005..008-*.md`

**Captured**: 2026-06-28 21:18 UTC + tickets 2026-06-29. Doc generado 2026-06-30.
