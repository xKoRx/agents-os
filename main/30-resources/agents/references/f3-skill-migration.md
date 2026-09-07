---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[AGENTS OS - Fase 3]]"
aliases: []
tags:
  - kind/doc
created: "2026-08-10"
updated: "2026-08-10"
---

# F3 — Migración de skills

## Propósito

Registrar el move map reproducible de Fase 3. La autoridad de cada skill queda en su destino; este documento sólo conserva evidencia de migración, hashes y rollback.

## Contenido

| Skill | Origen | Destino | SHA-256 antes | Rollback |
|---|---|---|---|---|
| `sync-local-branch` | `30-resources/agents-skills/sync-local-branch/` | `30-resources/agents/skills/sync-local-branch/` | `494c42895c6db6063e3335c71b55113d54f6949eafdcfa92de68b467014e5d4c` | mover el directorio completo al origen y restaurar las referencias exactas listadas abajo |
| `fury-lib-consumer-deploy` | `30-resources/agents-skills/fury-lib-consumer-deploy/` | `30-resources/agents/skills/fury-lib-consumer-deploy/` | `660c842208395cda113d8bdf4a67fd0fb7ecbbb95046bebf770f99cf48431fd1` | mover el directorio completo al origen y restaurar las referencias exactas listadas abajo |
| `sdd-workflow` | `30-resources/agents-skills/sdd-workflow/` | `30-resources/agents/skills/sdd-workflow/` | `f138a9891d1559d26befb311f9b85f5b0b07fea67c216c65613909d25a2d0810` | mover el directorio completo al origen y restaurar las referencias exactas listadas abajo |

Referencias live a actualizar: `80-agents/skills/INDEX.md`, `80-agents/skills/agents-os-doctor/scripts/doctor.py` y `80-agents/memory/internal/agent-memory/2026-07-15-local-branch-sync-continuity.md`. Las ocurrencias en Fase 2, logs, archive y outputs son evidencia histórica o derivada y no se reescriben.

Las skills app-owned `echo-forge-wfm-troubleshooting` y `sqx-temporal-failure-audit` se migraron a `xKoRx/symphony/.agents/skills/` y ya no viven en el vault. Hashes de origen: `e45900da105ca199d4c0965a58bd068063a3bcb86070de956606420bc0c752e0` y `704d7fbcab78e0f85b79b25c77418eae1f6cd96acbee13134592a5699c82284c`. Hashes finales después de adaptar metadata, secciones y referencias al contrato del repo: `4b5c5d4bea45d671248f5f85eb0eb85e8e4154510f69d26759bb57439a8ee954` y `45037f9bae306fd08afdd0e8b44625a5873c683967b2b004140f9a5b3c7c0ccc`; README humana de la auditoría: `35249714d0b807a77ca9bc97d3b9d873a9561b7c7166d13e3529d4947d05286d`. El forward-test también restauró `sqx-plugin-lifecycle` desde el commit `ea03696` porque el checkout activo no contenía el target ya registrado; su `SKILL.md` final es `5d4fea36a8579e260faa2f54007f3baf6e2f2759396c61a81a65d3616f434d5b`. Rollback: mover ambos directorios nuevos de vuelta a `80-agents/skills/`, restaurar las referencias vault-relative del README/SKILL y las filas anteriores del registry; para la piloto, retirar sólo la copia restaurada del checkout activo si el target sigue resolviendo desde la rama autorizada.

## Fuentes

- [[AGENTS OS - Fase 3]]
- [[80-agents/skills/INDEX.md|Índice de skills]]
