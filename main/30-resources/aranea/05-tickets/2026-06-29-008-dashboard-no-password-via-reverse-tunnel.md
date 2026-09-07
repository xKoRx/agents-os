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

# 2026-06-29-008 — Eliminar doble auth dashboard — túnel SSH reverso

> **Status**: applied · **Risk**: medium · **Category**: modify-config
> **Fecha**: 2026-06-29 ~07:15
> **Requester**: hermes
> **Target**: Traefik LXC 115 (athena) ↔ Hermes VM

**Path original**: `/home/hermes/aranea/tickets/2026-06-29-008-dashboard-no-password-via-reverse-tunnel.md`

## Resumen (3 líneas)

Eliminar la doble autenticación del dashboard (Traefik basic-auth + token de Hermes). Reemplazar con un túnel SSH reverso Hermes→Traefik que autentica la conexión a nivel SSH, manteniendo el filtro IP de Traefik (`lan-only@file`). **Aplicado**.

## Cambios aplicados

- Túnel SSH reverso desde Hermes VM hacia Traefik (lxc/115)
- Traefik ahora consume el dashboard desde el túnel, no desde localhost
- Basic-auth removido del frontend (sigue activo el filtro `lan-only@file`)
- Autenticación ocurre a nivel SSH (más fuerte, no visible al cliente HTTP)

## Justificación

El segundo auth es fricción innecesaria. El dashboard ya está protegido por:
- Traefik `lan-only@file` (filtra por IP 192.168.31.0/24)
- Traefik basic-auth (lo que queremos mantener) ← finalmente se removió el basic-auth y se quedó con el túnel SSH

**Tickets relacionados**: [[2026-06-29-007-expose-dashboard-via-traefik]]

---

## Source files

- `/home/hermes/aranea/tickets/2026-06-29-008-dashboard-no-password-via-reverse-tunnel.md`

## Captured

2026-06-29. Tarjeta generada 2026-06-30.
