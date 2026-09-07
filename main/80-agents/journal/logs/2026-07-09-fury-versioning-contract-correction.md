---
type: change_log
scope: agents_os
created: 2026-07-09
updated: 2026-07-09
entities:
  - "[[AGENTS OS]]"
  - "[[fury-lib-consumer-deploy]]"
related:
  - "[[java-polycard-sdk]]"
  - "[[search-middleware]]"
confidence: verified
indexable: false
tags:
  - agent/log
  - area/meli
  - kind/change-log
  - tech/fury
---

# Change Log — Contrato de versionado Fury libreria → consumidor

## Motivo

Se detectó una interpretación incorrecta: cambiar `build.gradle` no crea una version en Meli/FURY.

## Cambio

- La libreria Java debe tener la version declarada en `build.gradle`, con el cambio commiteado/pusheado, y crearla con `fury create-version --no-tests` sin argumento de version.
- El consumidor sólo puede importar la version después de que FURY confirme que existe.
- El consumidor crea su propia version explícita de rama, por ejemplo `fury create-version 0.0.1-nombre-rama --no-tests`.

## Validación

Skill actualizada en `80-agents/skills/fury-lib-consumer-deploy/SKILL.md`.
