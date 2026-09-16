---
type: skill
schema_version: 1
name: aranea-agent-dev
description: Router del dominio Aranea (homelab) para trabajo de desarrollo y operación del agente. Cargar al trabajar sobre Echo, Echo Forge, Hermes, el appliance mcps, backups o red del homelab para fijar qué skills y fuentes de acceso son válidas. Todo acceso MCP aranea-* pasa exclusivamente por aranea-mcps-expert; nunca aplica a MELI ni a sistemas corporativos.
scope: area
created: "2026-09-12"
updated: "2026-09-16"
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[hermes-agent-operator]]"
  - "[[rjara-aranea-operations-preferences]]"
  - "[[meli-agent-dev]]"
  - "[[Echo]]"
  - "[[Echo Forge]]"
aliases:
  - aranea agent dev
  - dominio aranea
  - aranea dev routing
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - action/domain-routing
  - tech/agents-os
---

# aranea-agent-dev

## Purpose

Dominio exclusivo del homelab Aranea. Fija el boundary del dominio, carga las preferencias scoped y ruta al acceso MCP y a las skills de dominio. Los servicios MCP de Aranea (SSH, PostgreSQL, MongoDB, Hasura, Kafka y Flink) son exclusivos de este dominio: ninguna otra skill o dominio los activa.

Trigger boundary:

- **Sí:** trabajo sobre hosts/servicios del homelab, Hermes Agent, Echo/Echo Forge (DEV o PROD), el appliance `mcps`, backups/DR, red del homelab, o cualquier uso de una capability MCP `aranea-*`.
- **No:** Meli o sistemas corporativos (→ [[meli-agent-dev]]), trabajo local sin infraestructura Aranea.
- **Handoff:** Hermes como target/runtime → [[hermes-agent-operator]]; elección de ambiente/capability MCP → [[aranea-mcps-expert]]; trabajo Meli → [[meli-agent-dev]]; skills app-owned de `xKoRx/symphony` para SQX/Echo Forge específico.

## Minimal Read

1. Esta skill para fijar dominio y boundary MCP.
2. `../../../../80-agents/memory/public/user-preference/rjara-aranea-operations-preferences.md` — preferencias scoped Aranea.
3. `30-resources/aranea/00-index.md` — wiki curada del dominio (topología, servicios, storage); abrir sólo las páginas que la tarea toque.
4. [[hermes-agent-operator]] sólo cuando Hermes Agent sea el target del incidente/cambio.
5. [[aranea-mcps-expert]] sólo cuando la tarea requiera acceso MCP.

## Procedure

1. **Confirmar boundary Aranea.** Homelab y sus hosts/Hermes/Echo/mcps son este dominio; Meli/corporativo se rechaza y deriva a [[meli-agent-dev]] antes de leer documentación o abrir conexiones.
2. **Cargar preferencias scoped** (Minimal Read 2).
3. **Contexto de dominio:** elegir la página desde `30-resources/aranea/00-index.md`; no escanear la carpeta.
4. **Hermes como target:** activar [[hermes-agent-operator]] para instalación, perfiles, dashboard/serve, gateways, systemd user, updates y recovery del propio runtime Hermes. Si Hermes sólo opera otro target, no cargarla.
5. **Acceso MCP:** activar [[aranea-mcps-expert]] y seguir su contrato: ambiente (PROD/DEV/runtime) antes que autoridad, autoridad mínima, runbook de la familia. Esta skill nunca conecta `aranea-*` por su cuenta.
6. **Skills app-owned:** para plugins SQX o troubleshooting Echo Forge/WFM, usar las skills en `xKoRx/symphony/.agents/skills/` (repo owner); ellas delegan el acceso MCP aquí.

## Output

```text
Dominio:              aranea
Boundary:             <host/servicio/app> | NO_DEMOSTRADO
Prefs cargadas:       aranea-operations
Hermes target:         <sí → hermes-agent-operator | no>
MCP requerido:        <sí → aranea-mcps-expert | no>
Skill de dominio:     <hermes-agent-operator | aranea-mcps-expert | app-owned symphony | ninguna>
Dominio rechazado:    <ninguno | meli/local + motivo>
```

## Hard Rules

- El acceso MCP `aranea-*` es **exclusivo de este dominio** y pasa siempre por [[aranea-mcps-expert]]; ninguna otra skill abre esas conexiones ni duplica endpoints, permisos o semántica MCP.
- Hermes como runtime/target pasa por [[hermes-agent-operator]]; no usarla sólo porque Hermes sea el actor que opera otro servicio.
- **MUST NOT** para MELI o sistemas corporativos: es dominio de [[meli-agent-dev]].
- Elegir ambiente antes que autoridad; PROD de datos/control plane es read-only (contrato de [[aranea-mcps-expert]]).
- No mezclar dominios: si la tarea cruza a Meli, cerrar el paquete Aranea y hacer swap explícito.
- No copiar esta skill ni las skills expert/operator a `80-agents/skills/` ni a repos de cliente; el vault cura, el repo owner posee lo suyo.
