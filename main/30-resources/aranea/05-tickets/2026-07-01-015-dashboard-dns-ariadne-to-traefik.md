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

---
id: 2026-07-01-015
title: "DNS dashboard.lab.aranea apunta a Hermes (122) en vez de Traefik (11)"
type: action
schema_version: 1
status: todo
status_detail: "Detectado 2026-07-01 04:39 UTC. `dashboard.lab.aranea` resuelve a `192.168.31.122` (Hermes directo) en lugar de `192.168.31.11` (Traefik). Safari desde LAN funciona porque Traefik escucha en :443 y responde al host header; otros escenarios pueden fallar. Requiere revisar zona DNS."
severity: low
icon: 🎫
slug: 2026-07-01-015-dashboard-dns-ariadne-to-traefik
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
owner: me
aliases:
  - ticket 015
  - dashboard dns
tags:
  - kind/action
  - area/personal
  - project/agents-os
  - action/ticket
related:
  - "[[2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]"
  - "[[../02-servicios/dashboard-hermes-agent]]"
  - "[[../02-servicios/dns-tls]]"
---

# 2026-07-01-015 — DNS dashboard.lab.aranea

## Descripción

Corregir el registro DNS de `dashboard.lab.aranea` para que apunte a Traefik en vez de Hermes directamente.

## Checklist

- [ ] Ejecutar la acción y verificar la evidencia y los riesgos documentados.

## Contexto

Detectado durante el ticket 014: el FQDN `dashboard.lab.aranea` resuelve a `192.168.31.122` (Hermes VM), no a `192.168.31.11` (Traefik).

### Evidencia

```bash
$ getent hosts dashboard.lab.aranea
192.168.31.122  dashboard.lab.aranea

$ nslookup dashboard.lab.aranea
Server:        127.0.0.53
Address:       127.0.0.53#53
Name:          dashboard.lab.aranea
Address:       192.168.31.122
```

## Por qué funciona hoy igual

Safari desde LAN logra el flujo correcto porque:

1. Safari hace DNS query → `192.168.31.122`
2. Hermes VM (192.168.31.122) tiene SSH daemon escuchando en :22 pero **NO en :443** (verificado: `ss -tlnp | grep :443` vacío en Hermes).
3. Resultado: Safari recibe `connection refused` en :443.

Pero el síntoma que reporta el owner fue **502 Bad Gateway**, no `connection refused`. ¿Cómo es posible?

**Hipótesis**: Safari en realidad **NO usa** el DNS local directo. O hay un override de DNS en macOS, o el browser está usando un DNS upstream que resuelve diferente. **Esto no está confirmado** y requiere reproducir el escenario para descartarlo.

**Workaround funcional hoy**: acceder vía `https://192.168.31.11/api/status` con `-H 'Host: dashboard.lab.aranea'` (lo verifiqué durante el fix). Pero para usuarios del dashboard, eso no es viable.

## Acción

1. Localizar la zona DNS donde está registrado `dashboard.lab.aranea`:
   - Probablemente Pi-hole en `athena` (192.168.31.10). Confirmar con `dns-tls.md`.
   - Verificar `/etc/pihole/custom.list` o equivalente.
2. Cambiar el registro de `192.168.31.122` → `192.168.31.11`.
3. Validar con `getent hosts dashboard.lab.aranea` desde un cliente LAN.
4. Documentar el cambio en `dns-tls.md`.

## Riesgos

- Si el cambio de DNS afecta otros servicios que esperen `dashboard.lab.aranea` apuntando a Hermes directo (no esperado pero posible): podría romper algo. **Mitigación**: backup del archivo DNS antes de cambiar.
- El TLS del cert step-ca está emitido para `dashboard.lab.aranea` con SAN. Si la IP canónica del cert no afecta el contenido del cert mismo (y no debería), no hay riesgo de TLS.

## Pendiente

- Owner decide cómo abordar la zona DNS en sesión dedicada.
- Validar que el cert step-ca sigue válido tras el cambio (no debería invalidarse).
