---
type: learning
schema_version: 1
scope: project
created: 2026-07-01
updated: 2026-07-01
area: "[[Aranea]]"
project:
application:
entities:
  - "[[Aranea]]"
  - "[[Hermes]]"
  - "[[Traefik]]"
related:
  - "[[../../../30-resources/aranea/02-servicios/dashboard-hermes-agent]]"
  - "[[../../../30-resources/aranea/05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]"
  - "[[../../../80-agents/journal/sessions/2026-07-01-1130-hermes-dashboard-post-update-recovery-summary]]"
aliases:
  - dashboard ws origin
  - origin_mismatch 4403
  - origin rewrite middleware
  - websocket behind traefik
confidence: verified
source_session: 2026-07-01-1130-hermes-dashboard-post-update-recovery
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - tech/hermes
  - topic/dashboard
  - tech/websocket
  - failure/origin-mismatch
  - tech/traefik
  - tech/reverse-proxy
  - area/aranea
  - kind/learning
  - priority/high
  - scope/project
---

# Hermes Dashboard — Reverse Proxy con WebSocket Origin

## Aprendizaje

Para el **Hermes Dashboard** detrás de Traefik usando túnel reverse SSH hacia loopback, **HTTP exitoso no garantiza WebSocket exitoso**. Si el dashboard está bindeado a `127.0.0.1`, el browser envía `Origin` con el dominio público y Hermes puede rechazarlo con `origin_mismatch` (close code 4403). Hay que alinear `Host`/`Origin` con el `bound_host` o configurar Hermes para aceptar el host público si existe soporte oficial.

## Aplicabilidad

- **Cuándo cargarlo:** al desplegar o diagnosticar Hermes Dashboard detrás de Traefik, especialmente cuando HTTP responde pero el chat WebSocket falla.
- **Cuándo no cargarlo:** en servicios sin WebSocket o sin validación de `Origin` en el backend.

## Contexto

Durante el incidente **2026-07-01-014**, el dashboard pasó por tres estados:
1. HTTP 502 (Traefik backend incorrecto) → arreglado por URL + `passHostHeader: false`.
2. HTTP 200, WebSocket 4403 origin_mismatch → arreglado por middleware `hermes-dashboard-origin-rewrite@file` con `headers.customRequestHeaders.Origin: http://127.0.0.1:19119`.
3. Chat JS crash con `paths[0] undefined` → arreglado por env vars en unit drop-in override.

Los 3 fixes requeridos son consecutivos. Un solo fix no alcanza. **El síntoma clave** era que HTTP regresaba 200 pero el chat (WebSocket) se cerraba inmediatamente.

## Detalle técnico

### Por qué `passHostHeader: false` no es suficiente

`passHostHeader: false` en el loadBalancer reescribe el `Host` HTTP al server URL (`http://127.0.0.1:19119`). El browser, al abrir WebSocket, envía `Host: dashboard.lab.aranea` por UPGRADE, y Traefik lo reemplaza por `Host: 127.0.0.1:19119`. **Pero el browser también envía `Origin: https://dashboard.lab.aranea`** por separado, y Traefik NO lo reemplaza automáticamente (es un header CORS, no es el Host).

El código fuente de Hermes (`hermes_cli/web_server.py:12092` en adelante, función `_ws_host_origin_reason`) compara el `Origin` recibido contra el `bound_host` (que es `127.0.0.1`). Si no matchea → close 4403.

### El fix mínimo

Middleware Traefik con `headers.customRequestHeaders`:

```yaml
http:
  middlewares:
    hermes-dashboard-origin-rewrite:
      headers:
        customRequestHeaders:
          Origin: "http://127.0.0.1:19119"
```

Aplicado al router del dashboard. Traefik reescribe `Origin` antes de pasarlo al backend, y el dashboard acepta porque matchea `127.0.0.1`.

### Alternativa oficial (a investigar)

Revisar release notes upstream de Hermes para flags oficiales:
- `dashboard.allowed_hosts` (lista de hosts aceptables)
- `dashboard.public_url` (URL canónica)
- `dashboard.trusted_proxy` (acepta reescritura via reverse proxy)

**Pendiente**: si Hermes soporta esto nativamente, el middleware Traefik puede eliminarse y el dashboard opera con config-side en lugar de proxy-side.

## Patrones relacionados

- [[agents-os/manual-validation-vs-automated-healthcheck-policy]] — el fix fue visualmente "verde" desde la primera iteración (Traefik respondía) pero el chat seguía roto. **Smoke test real** (browser manual) confirmó el origen del bug.
- `passHostHeader: false` es preferible antes que rewrite middleware cuando el alcance es solo Host; pero cuando hay WebSocket, **el `Origin` requiere su propio rewrite**.

## Anti-patrones

- ❌ Declarar "fix completo" cuando `curl -H 'Host:'` da 200: el chat puede seguir roto porque WS tiene gates adicionales.
- ❌ Asumir que `--insecure` puede reintroducir binds a `0.0.0.0` post v0.17.0. **No se puede** — el flag fue eliminado.
- ❌ No buscar el código fuente del dashboard antes de proponer fix. La info vive en `/home/hermes/.hermes/hermes-agent/hermes_cli/web_server.py`.

## Confirmación operativa

Aplicado y verificado el 2026-07-01 16:48 UTC:
- HTTP 200 + `pty accepted peer=127.0.0.1 mode=loopback cred=token` en `gui.log`.
- Owner confirmó en Safari que el chat carga y funciona.

## Evidencia

- Sesión fuente `2026-07-01-1130-hermes-dashboard-post-update-recovery`.
- Ticket y runbook canónicos enlazados en Referencias.

## Referencias

- Ticket [[../../../30-resources/aranea/05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]
- Runbook [[../../../30-resources/aranea/02-servicios/dashboard-hermes-agent]]
- Skill `~/.hermes/profiles/ariadna/skills/devops/hermes-dashboard-recovery/`
