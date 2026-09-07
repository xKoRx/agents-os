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

# 2026-06-29-004 — Retry3 crear LXC ca-aranea (CTID 200, disco 20)

> **Status**: failed · **Risk**: low · **Category**: create-resource
> **Fecha**: 2026-06-29 ~01:15
> **Requester**: hermes
> **Target**: athena / lxc / CTID 200

**Path original**: `/home/hermes/aranea/tickets/2026-06-29-004-create-lxc-ca-retry3.md`

## Resumen (3 líneas)

Retry3 con misma configuración (CTID 200, 20 GB). **Mismo fallo** que retry2. El bug del wrapper requiere intervención en el código del wrapper, no en los parámetros de entrada.

## Detalle

- Plan: idéntico al retry2.
- Output: `400 Parameter verification failed. ostemplate: value may only be 255 characters long`.
- **Esperando**: fix en el wrapper `aranea-pve-create` o alternativa (pct manual con root).

**Tickets relacionados**: [[2026-06-29-001..003-*-create-lxc-ca]], [[2026-06-29-005-install-step-ca]] (final aplicado)

---

## Source files

- `/home/hermes/aranea/tickets/2026-06-29-004-create-lxc-ca-retry3.md`

## Captured

2026-06-29. Tarjeta generada 2026-06-30.
