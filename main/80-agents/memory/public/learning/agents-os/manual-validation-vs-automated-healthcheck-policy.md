---
type: learning
scope: project
created: 2026-06-30
updated: 2026-06-30
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Ariadna]]"
related:
  - "[[agents-os]]"
aliases:
  - healthcheck vs alarm policy
  - manual validation antipattern
  - repeated healthcheck noise
  - dont validate sync every write
  - automated healthcheck preference
confidence: verified
source_session: 2026-06-30-ariadna-profile-iteration
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/learning
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/project
  - tech/observability
  - tech/healthchecks
---

# Manual Validation vs Automated Healthcheck

## Aprendizaje

Cuando una validación puede automatizarse como healthcheck periódico,
Ariadna no debe repetirla manualmente en cada flujo. Debe preferir una
alarma, healthcheck o monitor programado, y solo validar manualmente
ante señales de riesgo o antes de operaciones críticas.

## Regla Operativa

- **Sync de vault, backups, servicios y otros componentes** debe
  vigilarse mediante alarmas o healthchecks programados, no con
  validación manual en cada escritura.
- **Ariadna solo valida manualmente** cuando exista una señal
  concreta de problema:
  - Conflicto
  - Corrupción
  - Ausencia de archivos esperados
  - Error de plugin
  - Falla de escritura
  - Antes de una operación masiva o crítica sobre el Second Brain
- **No validar por si acaso** antes de cada acción normal. Genera
  ruido operativo, fricción innecesaria y consume tokens sin valor
  agregado.
- **Si una validación recurrente es valiosa**, debe automatizarse
  como cron job, watchdog systemd, monitor externo o skill invocada
  por schedule.

## Error Que Evita

- Validar manualmente el sync de LiveSync antes de cada escritura
  del vault
- Repetir el mismo check de salud en cada flujo sin evidencia de
  problema
- Asumir que la validación preventiva es gratis — no lo es
- Pedir OK al owner antes de registrar notas operativas normales
  en el vault (eso es fricción inútil; el registro de avance, sesión,
  decisión, aprendizaje o cierre es parte del trabajo de Ariadna)

## Entidades relacionadas

- `[[Ariadna]]` — agente principal que aplica esta política
- `[[AGENTS OS]]` — sistema operativo de agentes que define cuándo
  cargar esta memoria
- `[[Second Brain]]` — vault sobre el cual se aplica la política
- skill `operational-healthcheck-policy` — skill complementaria que
  decide cuándo activar healthchecks programados

## Evidencia

- Fuente: sesión `2026-06-30-ariadna-profile-iteration` — corrección literal del owner: "Ariadna no debe validar LiveSync en cada escritura normal del vault... solo debe verificar estado del vault cuando exista una señal concreta de problema... La salud del sync debe resolverse mediante un healthcheck programado/alarma, no mediante validaciones manuales repetitivas dentro de cada flujo".

## Aplicabilidad

- **Cuándo cargarlo:** cuando Ariadna esté por ejecutar una
  validación recurrente sobre LiveSync, backups, servicios o
  cualquier componente vigilable.
- **Cuándo no cargarlo:** cuando la validación es de un solo uso
  para confirmar un estado concreto que ya requiere evidencia
  puntual, o cuando es una nota operativa normal de registro
  (decisión, aprendizaje, sesión, cierre) que Ariadna puede escribir
  sin pedir OK.
