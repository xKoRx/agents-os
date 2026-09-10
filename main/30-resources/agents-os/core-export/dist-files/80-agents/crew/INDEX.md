---
type: index
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases:
  - crew
  - registro de superficies
tags:
  - kind/index
created: 2026-09-09
updated: 2026-09-09
---

# Registro de la Tripulación (Crew Dashboard)

## Propósito

Registro canónico de las superficies de agente autorizadas para trabajar sobre este vault, y dashboard de performance por superficie × modelo.

## 📊 De un vistazo

- **Superficies registradas:** 0. El registro se puebla durante la instalación.

## Contenido

Una **superficie** es una entidad estable (el cliente o IDE desde el que trabaja un agente). El **modelo** es un atributo exacto y mutable de cada ejecución: no es una entidad ni un valor base del perfil.

### Contrato de identidad

- **Superficies registradas:** ninguna todavía. `agents-os-install` da de alta las que el usuario declare, usando `70-templates/`.
- **Identidad atribuible:** cuando un schema admita `agent_surface`/`agent_model`, usar el perfil canónico de la superficie y el modelo exacto reportado para ese trabajo. No agregar esos campos a tipos que no los soportan.
- **Registro de ejecución:** `80-agents/journal/agent-runs/` mediante `agents-os-agent-run-register`.
- **Clave de comparación:** `agent_surface × agent_model`. Un cambio de cualquiera de los dos crea otro run atribuible.
- **Modelo:** identificador exacto reportado por el host o por el usuario. `unknown` si no existe evidencia, nunca inferido.
- **Evidencia primaria:** outcome, verificación y rework del usuario. Los scores 1–5 son secundarios y siempre declaran su evaluator.
- **Historial:** los valores legacy en texto libre no se migran por heurística.

## 📂 Catálogo

| Superficie | Especialidad | Estado |
|---|---|---|
| _vacío_ | — | pendiente de instalación |

## Límite conocido

Un tercio de las ejecuciones registradas en el vault de origen quedó con `agent_model: unknown` porque la superficie no expone el modelo. Es deuda declarada, no un dato que se pueda inferir.
