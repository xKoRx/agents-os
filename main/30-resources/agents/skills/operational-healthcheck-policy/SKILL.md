---
type: skill
name: operational-healthcheck-policy
scope: global
description: Decide cuándo validar manualmente el estado de componentes vigilables (sync, backups, servicios) del Second Brain vs. confiar en el sistema automático. Usar ante una señal concreta de problema (conflicto, corrupción, falla de escritura, archivos ausentes) o antes de una acción masiva/crítica sobre el vault; evita el anti-pattern de validaciones manuales recurrentes en cada flujo.
aliases:
  - operational-healthcheck-policy
created: 2026-06-30
updated: 2026-08-08
index_priority: high
indexable: true
load_policy: manual
schema_version: 1
tags:
  - kind/skill
  - tech/observability
  - tech/healthchecks
  - tech/obsidian
  - tech/livesync
  - scope/global
---

# operational-healthcheck-policy

## Purpose

Diferenciar cuando Ariadna debe validar manualmente el estado de
componentes vigilables (sync, backups, servicios) vs. cuando debe
confiar en el sistema automático. Resuelve el anti-pattern de
validaciones manuales recurrentes dentro de cada flujo.

## Routing

- **Trigger normal (sin check):** Ariadna va a escribir/leer en el
  vault o ejecutar una acción de mantenimiento. Proceder sin
  validar.
- **Trigger de validación manual:** existe una señal concreta de
  problema (ver lista abajo). Activar la skill.

## Cuando Cargar Esta Skill

Cargarla cuando Ariadna esté por:

- Operar después de detectar: conflicto, corrupción, error de
  plugin, falla de escritura, ausencia de archivos esperados
- Operar antes de una acción masiva o crítica sobre el Second Brain
  (ej. reindex Graphify global, refactor estructural del vault,
  restore desde backup)
- Considerar si una validación recurrente debe automatizarse
  (output: cron job, watchdog, monitor)

## Cuando NO Cargarla

- En cada escritura normal del vault (ruido innecesario)
- Solo por si acaso sin evidencia de problema
- Cuando la validación ya está cubierta por un healthcheck
  programado
- Cuando la nota a escribir es operativa normal (decisión,
  aprendizaje, sesión, cierre) — eso es trabajo de Ariadna sin
  pedir OK

## Procedure

### 1. Detectar Trigger

Preguntarse explicitamente:

- ¿Hay senal concreta de problema?
  - Conflicto reportado
  - Corrupcion de archivo
  - Error en logs del plugin LiveSync
  - Archivo esperado ausente
  - Falla de escritura reciente
- ¿Voy a hacer una operacion masiva o critica sobre el vault?

Si la respuesta es NO a todas -> proceder sin check.

### 2. Si Hay Trigger, Validar

```bash
# Vault local
VAULT_ROOT="${AGENTS_OS_VAULT:-$PWD}"
ls -la "$VAULT_ROOT/.obsidian/plugins/obsidian-livesync/data.json"

# Tamano del vault
du -sh "$VAULT_ROOT"

# Conteo de archivos .md
find "$VAULT_ROOT" -type f -name "*.md" -not -path "*/.obsidian/*" | wc -l
```

Comparar contra el estado esperado (carpetas principales presentes,
cantidad razonable, sin errores de sync).

### 3. Reportar y Decidir

- Si todo OK: reportar brevemente y continuar
- Si hay problemas: abrir un ticket o notificar según severidad
- Si es operacion masiva y sync esta en duda: abortar hasta
  resolver

### 4. Si la Validacion Sera Recurrente

Promover a healthcheck programado. Formato sugerido:

```bash
# Cron job
*/15 * * * * "$HOME/bin/check-obsidian-vault-sync"

# O watchdog systemd
# /etc/systemd/system/vault-healthcheck.service
```

Documentar la promocion en el vault (tema ADR) y archivar la
validacion manual como referencia historica.

## Politica Relacionada

- Ver learning
  `manual-validation-vs-automated-healthcheck-policy`
  en `80-agents/memory/public/learning/agents-os/`

## Hard Rules

- Validar el sync antes de cada escritura
- Repetir el mismo check de salud en cada flujo
- Confundir validacion de un solo uso con healthcheck
- Pedir OK al owner antes de registrar notas operativas normales en
  el vault
