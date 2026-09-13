---
type: skill
schema_version: 1
name: meli-agent-dev
description: Router del dominio Meli para trabajo de desarrollo del agente. Cargar al empezar trabajo corporativo Meli (RIO/Signals/Ads, Fury, Spellbook, Zord) para fijar qué skills, preferencias y fuentes de acceso son válidas en este dominio. Nunca aplica al homelab Aranea ni a sistemas personales; las capabilities MCP aranea-* no existen en este dominio.
scope: area
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Meli]]"
entities:
  - "[[Meli]]"
related:
  - "[[rjara-meli-work-preferences]]"
  - "[[rjara-vpn-routing-preferences]]"
  - "[[aranea-agent-dev]]"
aliases:
  - meli agent dev
  - dominio meli
  - meli dev routing
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/meli
  - action/domain-routing
  - tech/agents-os
---

# meli-agent-dev

## Purpose

Dominio exclusivo del trabajo corporativo Meli. Fija el boundary del dominio, carga las preferencias scoped y ruta a la skill especializada correcta. No ejecuta el trabajo itself: cada skill especializada posee su procedimiento.

Trigger boundary:

- **Sí:** cualquier tarea sobre repos, apps, datos, specs, PRs, deploys o infraestructura corporativa Meli (incluye RIO, Signals, Ads, Fury, Spellbook, Zord).
- **No:** homelab Aranea (→ [[aranea-agent-dev]]), sistemas personales, o identidad Meli no demostrable.
- **Handoff:** acceso MCP de Aranea → [[aranea-agent-dev]]; trabajo específico → skill especializada de la tabla de routing.

## Minimal Read

1. Esta skill para fijar dominio y routing.
2. `../../../../80-agents/memory/public/user-preference/rjara-meli-work-preferences.md` — preferencias scoped Meli.
3. `../../../../80-agents/memory/public/user-preference/rjara-vpn-routing-preferences.md` — conectividad por dominio.
4. Sólo la skill especializada elegida en el routing; nunca el catálogo completo.

## Procedure

1. **Confirmar boundary Meli.** Demostrar identidad corporativa (remoto/owner del repo, metadata corporativa o relación canónica del vault); la mención del usuario no basta por sí sola. Si es no Meli o queda incierto, no abrir fuentes corporativas y resolver el dominio real.
2. **Cargar preferencias scoped** (Minimal Read 2–3). Son válidas sólo dentro de este dominio.
3. **Rutear a la skill especializada:**

   | Tarea | Skill |
   |---|---|
   | Code review de branch/PR Meli | [[signals-code-review]] |
   | Spec funcional Signals/Ads | [[signals-func-spec-authoring]] |
   | Spec técnica / design doc RIO | [[signals-tech-spec-authoring]] |
   | Descripción de PR | [[pr-description]] |
   | Comunicación escrita para personas | [[human-first-technical-writing]] |
   | Deploy de librería Java Fury | [[fury-lib-consumer-deploy]] |
   | Sincronizar rama local | [[sync-local-branch]] |

4. **Conectividad:** resolver VPN/proxy por [[rjara-vpn-routing-preferences]] antes del primer acceso corporativo.
5. **Acceso a datos o clusters Meli:** sólo por las herramientas y superficies corporativas autorizadas por la skill especializada elegida; esta skill no habilita superficies propias.

## Output

```text
Dominio:              meli
Boundary demostrado:  <repo/PR/fuente> | NO_DEMOSTRADO
Prefs cargadas:       meli-work | vpn-routing
Skill especializada:  <nombre | ninguna>
Dominio rechazado:    <ninguno | aranea/personal + motivo>
```

## Hard Rules

- Las capabilities MCP `aranea-*` **no existen en este dominio**: nunca usarlas para hosts, datos, repos o infraestructura Meli/corporativa.
- No mezclar dominios: si la tarea cruza a Aranea, cerrar el paquete Meli y hacer swap explícito a [[aranea-agent-dev]].
- Las preferencias Meli son scoped (`when_area_loaded`): no se cargan en cold start ni persisten fuera del dominio.
- No duplicar aquí el contenido de las skills especializadas; esta skill sólo ruta.
- Revisión de código Meli exige Zord vía [[signals-code-review]]: nunca revisar PRs Meli sin esa skill.
