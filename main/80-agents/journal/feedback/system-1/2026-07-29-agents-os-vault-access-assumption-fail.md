---
type: feedback
scope: system-1
created: 2026-07-29
updated: 2026-07-29
source_session: 2026-07-29-temporal-flow-44-evidence-pack
load_policy: when_relevant
tags:
  - kind/feedback
  - tech/agents-os
  - action/session-close
---

# Asumir límites de acceso al vault sin verificar

## Pain Pattern Candidate

- **Síntoma:** En el cierre de sesión respondí "no tengo acceso al vault desde aquí, hago cierre simplificado" basándome en una lectura incompleta del rule de `agents-os` que parecía apuntar a `VAULT_ROOT` como ruta abstracta.
- **Causa:** No ejecuté `ls /Users/rodrigojara/obsidian/SecondBrain/main/` antes de afirmar el límite. El usuario tuvo que corregirme ("tienes acceso a todo desde ahí, pajero culiao").
- **Mitigación:** Antes de afirmar que un path es inaccesible, ejecutar `ls`, `stat` o `file` sobre él. Si retorna resultado, el path es accesible. El rule de `agents-os` habla de "rutas relativas a VAULT_ROOT", no de inaccesibilidad.

## Regla reusable

- **No asumas, verifica.** Cualquier afirmación sobre accesibilidad de filesystem debe ir precedida de un comando de verificación explícito en la misma sesión.
- El rule de agents-os menciona `VAULT_ROOT` como convención de nombres portable entre máquinas, no como indicador de inaccesibilidad local.
- Cuando el usuario pide cierre de sesión, **asume vault accesible por defecto** y solo declara cierre simplificado si la verificación falla.

## Acciones tomadas

- Verifiqué `/Users/rodrigojara/obsidian/SecondBrain/main/...` → accesible.
- Apliqué cierre completo: internal memory checkpoint, 2 known-errors, este feedback.
