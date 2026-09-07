---
type: change_log
scope: public
created: 2026-08-07
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Fase 2]]"
  - "[[agents-os-doctor]]"
confidence: verified
load_policy: manual
indexable: false
tags:
  - kind/changelog
  - action/refactor
  - project/agents-os
  - scope/public
---

# Change log — AGENTS OS Fase 2 · Cierre de los 2 gaps de G2

Sesión de proceso fresco (superficie Claude Code) para cerrar los 2 gaps que
dejaron G2 en review y dejarlo listo para aceptación del owner. **No** se inició
Fase 3 y **no** se auto-aceptó el gate. Doctor estricto verde al cierre
(`HIGH=0 MEDIUM=0 LOW=0`, startup ≈4979, exit 0).

## Gap 2 — repo owner Echo Forge/SQX: HALLADO + piloto migrada

- **Repo owner hallado:** `~/go/src/github.com/xKoRx/symphony` (remote
  `xKoRx/symphony`). Confirmado por marcadores que las 3 skills app-owned
  referencian: `AGENTS.md`, `CONSTITUTION.md`, `deploy/manifest.json`, `sqx/`,
  `specs/`, `scratch/`, y la skill `worker-ssh` — todos presentes en
  `.agents/skills/` (home canónica nativa de skills de la app; discovery nativo
  declarado para Cursor y Antigravity en su `.agents/README.md`). No estaba en
  `~/fuentes/` (por eso el bloqueo previo), sino en el GOPATH.
- **Piloto migrada (sin copia):** `sqx-plugin-lifecycle` movida de
  `VAULT_ROOT/80-agents/skills/sqx-plugin-lifecycle/` →
  `xKoRx/symphony` `.agents/skills/sqx-plugin-lifecycle/`. Método: `cp -R` +
  verificación de checksums (4 archivos: `SKILL.md`, `agents/openai.yaml`,
  `references/deployment-checklist.md`, `references/echo-forge-build142.md`,
  shasum idénticos) + `rm -rf` del origen. No queda copia en el vault.
  En el repo aparece como untracked; **no** se commiteó ni pusheó (decisión del
  owner).
- **Piloto elegida:** la más representativa (única con `references/` +
  `agents/openai.yaml` de surface-metadata) y la de menor blast radius: sin refs
  vivas por wikilink en memoria/proyectos (solo el INDEX y journals, que no se
  reescriben) y sin colisión de nombre. Descartadas:
  `echo-forge-wfm-troubleshooting` (colisiona con el proyecto de agente homónimo)
  y `sqx-temporal-failure-audit` (referida por una known-error viva).
- **INDEX actualizado:** sección app-owned reescrita (`repo + path relativo`,
  invariante 11): repo owner hallado; `sqx-plugin-lifecycle` marcada ✅ migrada;
  las otras 2 pasan de "bloqueado/repo no hallado" a "migración pendiente (repo
  hallado)"; `operational-healthcheck-policy` aclarada como core vault-ops.

## Gap 1 — forward-test multisuperficie (superficie Claude Code)

Dos mecanismos de discovery observados en esta superficie:

1. **Registro nativo de skills de Claude Code** (herramienta `Skill`): solo
   expone `agents-os-bootstrap` como entrypoint AGENTS OS. `agents-os-doctor`,
   `sync-local-branch` y `fury-lib-consumer-deploy` **no** aparecen → MISS por
   este mecanismo. Es **por diseño** (skill-contract: no copiar/symlinkar skills
   a carpetas de cliente; el cliente rutea a `80-agents/skills/`). El único shim
   nativo es el entrypoint bootstrap.
2. **Registry federado** (`INDEX.md` → pointer → `SKILL.md` vía file-tools; el
   mecanismo al que rutea bootstrap): resolución medida, todos HIT:

   | Skill | Clase | Path resuelto | Éxito | Tamaño | Latencia |
   |---|---|---|---|---|---|
   | `agents-os-doctor` | core | `80-agents/skills/agents-os-doctor/SKILL.md` | HIT válida | ~1161 tok | 0.30 ms |
   | `sync-local-branch` | federada transversal | `30-resources/agents-skills/sync-local-branch/SKILL.md` | HIT válida | ~873 tok | 0.26 ms |
   | `fury-lib-consumer-deploy` | federada transversal | `30-resources/agents-skills/fury-lib-consumer-deploy/SKILL.md` | HIT válida | ~2148 tok | 0.33 ms |
   | `sqx-plugin-lifecycle` (piloto migrada) | app-owned | — (removida del vault) | **MISS en vault (correcto)** / HIT en repo (`.agents/skills/`, 9059 B) | — | 0.10 ms |

- **Resultado:** en la superficie Claude Code, un proceso fresco descubre tanto
  la skill core como la federada transversal por el mecanismo nativo AGENTS OS
  (registry federado). La piloto migrada ya no resuelve desde el vault (correcto)
  y sí desde su repo owner por discovery nativo de `.agents/skills/`.
- **Limitación de superficie registrada:** el registro nativo de skills de
  Claude Code no auto-expone las skills del vault (solo bootstrap); el discovery
  real es vía registry federado leído con file-tools. Consistente con el
  skill-contract (matriz de compatibilidad, no segunda fuente física).
- **≥2 superficies:** ejecutado end-to-end en 1 superficie (Claude Code) con 2
  mecanismos comparados. La réplica en Codex/Cursor queda para el owner; el
  `.agents/README.md` del repo declara discovery nativo de la piloto en Cursor y
  Antigravity (documentado, no ejecutado aquí).

## Higiene colateral (no era del trabajo de G2)

- El doctor arrancó la sesión en `MEDIUM=1` (startup ≈5012 > 5k soft), **no**
  causado por este trabajo (mis ediciones fueron a `INDEX.md` `load_policy:
  manual` y a la remoción de la piloto — ninguno cuenta en el set always-load).
  Causa: la nota interna global `agents-os-operating-continuity.md` creció
  +241 chars (1360→1601) en una sesión previa de hoy, duplicando el estado de
  G2 que ya vive en el planner. Compactada a un puntero (autorizado por la
  constitución para memoria interna; sirve al assert doctor-verde y a "una
  fuente por hecho"). Resultado: startup 5012→4979, `MEDIUM=0`.

## Verificación

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py --strict
# AGENTS OS doctor: HIGH=0 MEDIUM=0 LOW=0 startup_tokens≈4979  (exit 0)
graphify-obsidian update
# Rebuilt: 5272 nodes, 6041 edges, 512 communities (exit 0)
```

## Archivos tocados

- move: `80-agents/skills/sqx-plugin-lifecycle/` → `xKoRx/symphony`
  `.agents/skills/sqx-plugin-lifecycle/` (4 archivos, checksums verificados).
- modify: `80-agents/skills/INDEX.md` (sección app-owned + fecha).
- modify: `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
  (compactación del puntero al planner).
- modify: `10-projects/AGENTS OS/agentes/AGENTS OS - Fase 2.md` (estado, matriz,
  gates, tareas, bitácora).
- derived: `95-graphify/` reindexado.

## Pendiente (post-aceptación del owner)

- Migrar las 2 skills app-owned restantes (`echo-forge-wfm-troubleshooting`,
  `sqx-temporal-failure-audit`) al repo owner cuando el owner lo autorice.
- Commit/push de la piloto en `xKoRx/symphony` (decisión del owner).
- Réplica del forward-test en Codex/Cursor (segunda superficie real).
- G2 lo acepta el owner; el agente no auto-acepta ni inicia Fase 3.
