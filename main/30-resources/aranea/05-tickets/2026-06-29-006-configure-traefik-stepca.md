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

# 2026-06-29-006 — Configurar Traefik con certResolver stepca

> **Status**: applied · **Risk**: low · **Category**: modify-config
> **Fecha**: 2026-06-29 ~04:30
> **Requester**: hermes
> **Target**: Traefik LXC 115 (athena)

**Path original**: `/home/hermes/aranea/tickets/2026-06-29-006-configure-traefik-stepca.md`

## Resumen (3 líneas)

Configurar Traefik (lxc/115 en athena) para usar step-ca como `certificatesResolvers.stepca`. **Aplicado**. Traefik ahora emite certificados TLS automáticamente desde la CA interna para los servicios expuestos.

## Contexto

- step-ca instalado y funcionando (ticket 005)
- Traefik NO estaba todavía configurado para usarlo

## Cambios aplicados

- `certificatesResolvers.stepca` configurado en `traefik.yml`
- Endpoint ACME (`stepca.acme`) apunta a `ca.lab.aranea`
- Verificación HTTP-01 (challenge) funcionando
- Cert wildcard `*.lab.aranea` emisibles

**Tickets relacionados**: [[2026-06-29-005-install-step-ca]], [[2026-06-29-007-expose-dashboard-via-traefik]]

---

## Source files

- `/home/hermes/aranea/tickets/2026-06-29-006-configure-traefik-stepca.md`

## Captured

2026-06-29. Tarjeta generada 2026-06-30.
