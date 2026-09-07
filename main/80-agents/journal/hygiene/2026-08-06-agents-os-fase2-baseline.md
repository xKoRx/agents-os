---
type: log
scope: baseline
created: 2026-08-06
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
  - kind/log
  - action/baseline
  - project/agents-os
  - scope/hygiene
---

# AGENTS OS Fase 2 — Baseline (Fase 0)

Fotografía reproducible del sistema **antes** de modificar autoridades, paths o
topología. Medición pura (T0.5); no es fuente canónica ni corpus Graphify
(excluido vía `80-agents/journal/**` en `.graphifyignore`). Vault respaldado a
nivel de infraestructura.

- **Fecha:** 2026-08-06
- **Comando raíz:** `python3 80-agents/skills/agents-os-doctor/scripts/doctor.py [--strict]`
- **Ejecutado desde:** `VAULT_ROOT` (`.../SecondBrain/main`)

## 1. Doctor output

Resumen ejecutable: `HIGH=3 MEDIUM=1 LOW=0 startup_tokens≈4948`

| Sev | check | archivo | issue |
|---|---|---|---|
| HIGH | portability | `80-agents/agents-os/agent-memory/2026-07-28-echo-forge-tradelist-java-snippets-stale.md` | path absoluto machine-specific en core |
| HIGH | portability | `80-agents/skills/sqx-temporal-failure-audit/SKILL.md` | path absoluto machine-specific en core |
| HIGH | skill-ref | `80-agents/skills/sqx-temporal-failure-audit/SKILL.md` | ref relativa rota: `../../agents-os-context-retrieval/SKILL.md` |
| MEDIUM | graphifyignore | `.graphifyignore` | falta exclusión `.obsidian/` |

- **Modo normal:** exit 0.
- **Modo `--strict`:** exit 1 (mismos hallazgos; strict falla el gate ante
  cualquier HIGH/MEDIUM).

Nota: el proyecto anticipaba estos hallazgos como trabajo de **Fase 1** (dos
portability + ref SQX + `.obsidian/`). El baseline los confirma sin actuar
sobre ellos. Los dos "falsos positivos de portabilidad" mencionados en el
proyecto corresponden a estos dos hits sobre paths remotos válidos, a
reclasificar por el doctor refinado en F1 (paso T1.3).

## 2. Skills

- **SKILL.md en disco:** 32 (bajo `80-agents/skills/`).
- **Notas con `type: skill`:** 57 (incluye docs/`_shared`/copias que no son
  SKILL.md; el delta 57→32 es señal para el inventario de ownership de F2).
- Inventario de directorios de skills:

```text
agents-os-agent-project-workflow      agents-os-behavior-config
agents-os-bootstrap                   agents-os-conflict-resolution
agents-os-context-retrieval           agents-os-doctor
agents-os-entity-lifecycle            agents-os-entity-update
agents-os-graphify-install            agents-os-graphify-maintenance
agents-os-hygiene-cycle               agents-os-hygiene-review
agents-os-implementation-planning     agents-os-install
agents-os-kaizen-memory               agents-os-memory-distillation
agents-os-note-capture                agents-os-relation-maintenance
agents-os-requirement-interview       agents-os-resource-wiki
agents-os-retrofit-raw-session        agents-os-session-close
agents-os-session-feedback            agents-os-skill-authoring
agents-os-tagging-system              agents-os-vault-refactor
echo-forge-wfm-troubleshooting        fury-lib-consumer-deploy
operational-healthcheck-policy        sqx-plugin-lifecycle
sqx-temporal-failure-audit            sync-local-branch
```

Clasificación preliminar (para F2, no ejecutada aquí): 26 `agents-os-*` core;
app/domain-owned candidatas → `echo-forge-wfm-troubleshooting`,
`fury-lib-consumer-deploy`, `operational-healthcheck-policy`,
`sqx-plugin-lifecycle`, `sqx-temporal-failure-audit`, `sync-local-branch`.

## 3. Notas por tipo (frontmatter `type:`)

- **Total notas `.md`** (excl. `.trash/`, `.obsidian/`): **1311**
- **Sin `type` / sin YAML:** 141
- **Variantes distintas de `type`:** **63** (evidencia dura de R7 — drift de schema)

Top tipos: change_log 196 · feedback 173 · raw_session 163 · session 123 ·
agent_memory 73 · skill 57 · project 56 · known_error 42 · learning 27 ·
doc 25 · decision 22 · application 18 · internal_memory 17 · runbook 14 ·
index 14 · area 13 · agent-project 10.

Ejemplos de drift (mismo concepto, distinto casing/separador):

- `agent_memory` (73) / `agent-memory` (3) / `memory` (2) / `internal_memory` (17)
- `raw_session` (163) / `session_raw` (2) / `session-raw` (2) / `raw-session` (1)
- `known_error` (42) / `known-error` (2)
- `session/summary`, `session/raw`, `feedback/system-1` (variantes con slash)

## 4. Graphify

- **Estado:** `95-graphify/` presente. Dominios activos: `obsidian`, `personal`,
  `work` (+ `dist/` derivado). Salidas en `graphify-out/`.
- **`.graphifyignore`:** excluye `outputs/`, `95-graphify/`, `graphify-out/`,
  `trash/`, `00-inbox/`, `40-archive/`, `80-agents/journal/**`, raw sessions,
  chatgpt-pack y `**/*.json`. **Falta `.obsidian/`** (hallazgo MEDIUM del
  doctor; se corrige en F1).
- El corpus de retrieval no incluye este log (journal excluido).

## 5. Startup cold — forma y tokens

- **Tokens de startup (doctor):** ≈ **4948** (dentro del benchmark blando cold
  3–5k, extremo alto).
- **Archivos leídos en cold** (hook + closed club always-load):

| Archivo | words | chars |
|---|---|---|
| `AGENTS.md` (hook) | 153 | 1110 |
| `80-agents/agents-os/agent-constitution.md` | 588 | 4301 |
| `80-agents/memory/public/user-preference/rjara-agent-profile.md` | 291 | 2153 |
| `80-agents/skills/agents-os-bootstrap/SKILL.md` | 798 | 5594 |
| `80-agents/skills/agents-os-context-retrieval/SKILL.md` | 966 | 6548 |
| `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` | 177 | 1360 |
| **Total** | **2973** | **21066** |

## 6. Reproducibilidad

Comandos ejecutados desde `VAULT_ROOT`:

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py          # normal, exit 0
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py --strict # exit 1 (HIGH/MEDIUM presentes)
find 80-agents/skills -name SKILL.md | wc -l                         # 32
find . -name "*.md" -not -path "./.trash/*" -not -path "./.obsidian/*" | wc -l  # 1311
```

## 7. Conclusión / Handoff a Fase 1

Baseline capturado y reproducible. Estado del sistema sano para arrancar F1:
- Startup ≈4948 tokens (referencia para no aumentar en F1).
- Doctor: 3 HIGH + 1 MEDIUM, todos ya previstos como trabajo de F1.
- Schema drift cuantificado (63 variantes de `type`, 141 sin type) → insumo F3.
- Ownership de skills con delta 57→32 → insumo F2.

Gate **G0 → review**. Prohibido iniciar F1 hasta aceptación del owner.
