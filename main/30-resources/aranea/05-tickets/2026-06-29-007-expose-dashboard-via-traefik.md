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

# 2026-06-29-007 — Exponer dashboard.lab.aranea via Traefik con TLS step-ca

> **Status**: applied · **Risk**: low · **Category**: deploy-service
> **Fecha**: 2026-06-29 ~04:55
> **Requester**: hermes
> **Target**: Traefik LXC 115 (athena)

**Path original**: `/home/hermes/aranea/tickets/2026-06-29-007-expose-dashboard-via-traefik.md`

## Resumen (3 líneas)

Exponer el dashboard de Hermes (`127.0.0.1:9119`) públicamente como `https://dashboard.lab.aranea` via Traefik, con TLS emitido por step-ca. **Aplicado**. Dashboard accesible vía HTTPS sin warnings de certificado.

## Prerrequisitos verificados

- step-ca corriendo (ticket 005)
- Traefik tiene `certificatesResolvers.stepca` configurado (ticket 006)
- Dashboard de Hermes respondiendo HTTP 200 en `127.0.0.1:9119`

## Cambios aplicados

- Router en Traefik para `dashboard.lab.aranea`
- Backend: `http://127.0.0.1:9119` (loopback)
- TLS via `certResolver=stepca`
- Filtro `lan-only@file` (solo IPs 192.168.31.0/24)
- Basic-auth para acceso

**Tickets relacionados**: [[2026-06-29-006-configure-traefik-stepca]], [[2026-06-29-008-dashboard-no-password-via-reverse-tunnel]] (siguiente)

---

## Source files

- `/home/hermes/aranea/tickets/2026-06-29-007-expose-dashboard-via-traefik.md`

## Captured

2026-06-29. Tarjeta generada 2026-06-30.
