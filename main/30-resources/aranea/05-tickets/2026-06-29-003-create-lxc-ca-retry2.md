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

# 2026-06-29-003 — Retry2 crear LXC ca-aranea (CTID 200, 20G disk)

> **Status**: failed · **Risk**: low · **Category**: create-resource
> **Fecha**: 2026-06-29 ~01:00
> **Requester**: hermes
> **Target**: athena / lxc / CTID 200

**Path original**: `/home/hermes/aranea/tickets/2026-06-29-003-create-lxc-ca-retry2.md`

## Resumen (3 líneas)

Retry2: cambio de CTID a 200 (de 112) y disco a 20G. **Mismo fallo**: el parámetro `ostemplate` aún excede 255 chars. Bug del wrapper persiste.

## Detalle

- Plan: crear LXC con CTID 200, hostname `ca`, 20 GB disco en `local-lvm`.
- Output: `400 Parameter verification failed. ostemplate: value may only be 255 characters long`.
- Cambiar CTID y tamaño no resolvió el problema porque la limitación está en el path completo del template.

**Tickets relacionados**: [[2026-06-29-001-create-lxc-ca]], [[2026-06-29-002-create-lxc-ca-retry]], [[2026-06-29-004-create-lxc-ca-retry3]]

---

## Source files

- `/home/hermes/aranea/tickets/2026-06-29-003-create-lxc-ca-retry2.md`

## Captured

2026-06-29. Tarjeta generada 2026-06-30.
