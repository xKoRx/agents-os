---
type: session
scope: session
created: 2026-07-22
updated: 2026-07-22
area: "[[Personal]]"
project: "[[Symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-07-22-symphony-worker-permissions-raw]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - project/symphony
---

# Symphony Worker Permissions — Session Summary

> [!info]+ Session summary L1
> Resumen operativo. Excluido del corpus normal de Graphify.

## Objetivo

- Diagnosticar el fallo de permisos de `apply_selected_run`, homologar Hera y Kronos con Zeus y dejar el procedimiento documentado.

## Contexto cargado

- Skills `worker-ssh`, `worker-troubleshooting`, `agents-os-bootstrap` y `agents-os-session-close`.
- Código de `apply_selected_run`, unidades systemd y logs de los tres workers.

## Trabajo realizado

- Confirmada la causa raíz: ruta relativa `input/` combinada con `WorkingDirectory=/opt/symphony/current/bin` en Hera/Kronos.
- Copiada íntegramente la unidad de Zeus a Hera y Kronos, con respaldo previo, `daemon-reload` y reinicio.
- Verificados en los tres hosts: mismo SHA-256 de unidad, versión `0.1.130`, servicio activo, cwd `/var/lib/symphony` y escritura exitosa en `input/`.

## Artifacts creados o modificados

- `.agents/skills/worker-troubleshooting/SKILL.md` actualizado a `1.1.0` con diagnóstico, solución y validación.
- Nota de continuidad interna actualizada.

## Memoria propuesta o creada

- No se creó L3 pública separada: la skill de troubleshooting es la fuente operativa canónica para este incidente.

## Decisiones

- Mantener `/opt/symphony/current/bin` inmutable; no relajar permisos del release.
- Usar `/var/lib/symphony` como directorio de trabajo escribible en todos los workers.

## Pendiente

- Sin pendientes por este incidente: el intento 9 superó `apply_selected_run` y el workflow avanzó a tres actividades `mt5_exporter` iniciadas.
