---
type: known_error
schema_version: 1
scope: application
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Meli]]"
project: "[[Vulnerabilidades WebSec — RIO Foundation]]"
application:
entities:
  - "[[RIO]]"
related:
  - "[[2026-09-03-sigfoun-websec-vuln-intake-rio-foundation]]"
aliases:
  - dónde están las vulnerabilidades de RIO
  - SIGFOUN
  - WebSec Signals
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - topic/security
  - tech/rio
---

# 2026-09-03-vulnes-signals-no-salen-por-fury-cli

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Se buscan las vulnerabilidades de una aplicación de RIO/Signals por las vías obvias y **todas devuelven vacío o algo distinto**: `fury actionables list` sólo trae rightsizing y migraciones de runtime, `fury platsec` expone políticas y no hallazgos, `fury dla` es licenciamiento y no CVEs, GitHub Code Scanning responde `[]` y Dependabot está deshabilitado en los repos `melisource`. Se concluye erróneamente que no hay vulnerabilidades.

## Causa

- El programa de vulnerabilidades de aplicaciones no vive en Fury ni en GitHub: es **WebSec**, que abre un ticket Jira por hallazgo en el proyecto del equipo (`SIGFOUN` para Signals) y publica un mensaje por ticket en el canal Slack del equipo mediante un bot. Fury nunca ve ese dato.
- El nombre del canal puede confundirse con una app o un proyecto de Fury. `ads-signals-foundation` **es un canal de Slack** (`C08RWQ5P3TM`), no existe como aplicación ni como proyecto en Fury.

## Impacto

- Se pierde tiempo recorriendo herramientas que por diseño no tienen el dato, y se puede reportar "no hay vulnerabilidades" cuando en realidad hay decenas abiertas con SLA corriendo.

## Detección

- `fury actionables list --project <p> --status all` devuelve sólo `Execute scope rightsizing`, `Enable scale to zero` y migraciones de runtime.
- `gh api /repos/melisource/<repo>/code-scanning/alerts` devuelve `[]` y `/dependabot/alerts` responde `403 Dependabot alerts are disabled`.

## Mitigación

- Ir al **canal Slack del equipo** y leer los mensajes del bot de WebSec: traen severidad, dependencia, aplicación y el enlace al ticket. Para Signals es `#ads-signals-foundation`; el canal de soporte transversal es `#tech-websec`.
- Para el detalle de cada ticket (CVE, versión segura, estado) la vía canónica es el MCP **`oraculo-websec-mcp`** (`https://oracle-websec-mcp-mcp.melioffice.com/mcp`). Requiere VPN corporativa GlobalProtect **y** el access group `mcp_consumer_bu_all`, que se pide por autoservicio en MeliHelp (application `traffic-catalog`, read+write). Sin ese grupo responde `403 OFFSEC-AUT-6 / NO_ACCESS_GROUP_MATCHED` aunque la autenticación sea correcta.
- **No usar** `https://mcp.melioffice.com/namespaces/application-security/mcp`: ese endpoint de las guías de setup está obsoleto, el host resuelve a `documentation-mcp-server-py` y devuelve 404 en todos sus namespaces.
- Para cerrar un hallazgo, el flujo de WebSec es transicionar el ticket a `Pending` y completar el campo `solución`; eso detiene el SLA del equipo y lo manda a validación.

## Evidencia

- Fuente: [[2026-09-03-sigfoun-websec-vuln-intake-rio-foundation]] — recorrido completo de las vías fallidas y respuesta literal del proxy al llamar `oraculo-websec-mcp`.
 
