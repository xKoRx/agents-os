---
type: action
schema_version: 1
project:
status: done
created: 2026-08-10
updated: 2026-08-10
tags:
  - kind/action
  - area/aranea
---

## Descripción

Registro histórico de ejecución para [[Aranea]].

## Checklist

- [x] Resultado histórico preservado

# 2026-06-29-005 — Instalar step-ca en LXC ca-aranea (CTID 200)

> **Status**: applied · **Risk**: low · **Category**: deploy-service
> **Fecha**: 2026-06-29 ~01:35
> **Requester**: hermes
> **Target**: athena / lxc / CTID 200

**Path original**: `/home/hermes/aranea/tickets/2026-06-29-005-install-step-ca.md`

## Resumen (3 líneas)

Instalar y configurar `step-ca` (CA interna basada en `step`) en el LXC CTID 200. **Aplicado exitosamente**. step-ca quedó corriendo y emitiendo certificados.

## Configuración del LXC

| Item | Valor |
|---|---|
| Hostname | `ca` |
| FQDN | `ca.lab.aranea` |
| IP | `192.168.31.12/24` |
| OS | Debian 12 |

## Lo que se instaló

- `step-ca` (servidor de CA)
- `step` (cliente CLI)
- Configuración inicial de la CA
- Claves y provisioner password

**Tickets relacionados**: [[2026-06-29-001..004]] (failed creates previos), [[2026-06-29-006-configure-traefik-stepca]] (siguiente paso)

---

## Source files

- `/home/hermes/aranea/tickets/2026-06-29-005-install-step-ca.md`

## Captured

2026-06-29. Tarjeta generada 2026-06-30.
