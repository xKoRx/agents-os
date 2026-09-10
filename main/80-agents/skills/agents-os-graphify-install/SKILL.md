---
type: skill
name: agents-os-graphify-install
scope: global
created: 2026-07-05
updated: 2026-09-03
index_priority: high
indexable: true
load_policy: manual
schema_version: 1
description: Install or repair graphify-obsidian on one machine. Use when the command is missing, fails with exit 42, the isolated venv is broken, or a fresh machine needs a local retrieval index. Installs from a machine-local wheel or source checkout and keeps all generated state outside the vault.
aliases:
  - agents-os-graphify-install
tags:
  - kind/skill
  - action/install
  - tech/agents-os
  - tech/graphify
  - scope/global
---

# AGENTS OS Graphify Install

## Purpose

Dejar `graphify-obsidian` operativo con binario, wheel e índice locales a cada
máquina. Lazy-load: invocar solo cuando falta/está roto el comando o en máquina nueva.

## Minimal Read

1. `../../memory/public/runbook/graphify-obsidian-install.md` — el procedimiento ejecutable (fuente única).
2. `../_shared/graphify-contract.md` — solo si hay dudas de salida/paths/reindex.

No repetir aquí los pasos: viven en el runbook. Esta skill decide *cuándo* y ejecuta ese runbook.

## Procedure

1. **Detectar necesidad**: `which graphify-obsidian` vacío, o `graphify-obsidian --help` falla,
   o aborta con exit 42 (venv aislado ausente), o máquina nueva.
2. **Confirmar fuente local**: wheel bajo `~/.local/share/graphify-obsidian/dist/`
   o checkout configurado por `AGENTS_OS_GRAPHIFY_SOURCE`. El vault no distribuye binarios.
3. **Ejecutar el runbook** `graphify-obsidian-install.md` paso a paso (instalar wheel en venv aislado,
   instalar wrapper en `~/bin`, PATH, ajustar `VAULT_PATH` si el vault no está en la ruta canónica).
4. **Validar** con la sección Validación del runbook: `--help`, `cache-path`,
   `status` y una query que active auto-refresh si corresponde.
5. Si tras instalar el retrieval sigue fallando, derivar a `agents-os-graphify-maintenance`.

## Output

```text
Estado previo:        (missing | exit 42 | venv roto | máquina nueva | ok)
Compilado usado:      <wheel o checkout local>
Wrapper instalado:    ~/bin/graphify-obsidian (sí|no)
VAULT_PATH ajustado:  (no aplica | ruta)
Validación:           auto-refresh ok | explain ok | estado fuera del vault (sí|no)
Próximo paso:         (reindex | maintenance | listo)
```

## Hard Rules

- No duplicar los pasos del runbook: esta skill los referencia y los ejecuta.
- Binario, wheels, logs, índice y temporales son locales a la máquina y nunca se guardan en el vault.
- El wrapper canónico vive en `scripts/graphify-obsidian`; sólo ese archivo pequeño se sincroniza.
- Las queries refrescan automáticamente el índice cuando detectan cambios.
- No instalar el fork en el `graphify`/`graphify-personal` compartido: usa su venv aislado.
