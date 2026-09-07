---
type: user_preference
schema_version: 1
scope: user
created: "2026-09-03"
updated: "2026-09-03"
entities:
  - "[[Meli]]"
  - "[[Aranea]]"
  - "[[AGENTS OS]]"
related:
  - "[[rjara-agent-profile]]"
  - "[[rjara-meli-work-preferences]]"
  - "[[rjara-aranea-operations-preferences]]"
aliases:
  - VPN de Meli versus Aranea
  - routing de VPN
  - conectividad GlobalProtect Aranea
confidence: verified
load_policy: contextual
indexable: true
index_priority: high
tags:
  - kind/user-preference
  - priority/high
  - scope/user
---


# rjara — Routing canónico de VPN

## Preferencias de interacción

- Si una operación de red requiere una VPN desconectada o una interacción gráfica que el agente no puede completar, pedir al usuario que conecte la VPN correcta por su nombre. No intentar otra VPN como sustituto.

## Preferencias de trabajo

- `[DURA]` Para proyectos, repositorios y servicios internos de [[Meli]] —incluidos repos `melisource`, GitHub con allowlist y Fury— la VPN requerida es **GlobalProtect**, la VPN corporativa de MELI.
- `[DURA]` Para repositorios propios, servicios privados y el homelab [[Aranea]], la VPN requerida es **Aranea**.
- `[DURA]` GlobalProtect y Aranea pertenecen a dominios distintos y no son intercambiables. Antes de diagnosticar o remediar conectividad, identificar si el recurso es corporativo MELI o personal/homelab.
- Ante un rechazo de GitHub por IP allowlist en un repo `melisource`, verificar GlobalProtect. Ante un recurso privado del homelab inaccesible, verificar Aranea.

## Preferencias de memoria

- Esta nota es la única autoridad sobre qué VPN corresponde a cada dominio. Las preferencias scoped de Meli y Aranea deben enlazarla, no duplicar la matriz.
