---
type: change_log
scope: public
created: 2026-08-06
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Fase 2]]"
  - "[[agents-os-doctor]]"
  - "[[context-router]]"
confidence: verified
load_policy: manual
indexable: false
tags:
  - kind/changelog
  - action/refactor
  - project/agents-os
  - scope/public
---

# Change log — AGENTS OS Fase 2 · F1 Autoridades y doctor

Patch atómico de Fase 1 (T1.1–T1.4). Objetivo: eliminar duplicación procedural
y hacer que el doctor represente el contrato vigente. Doctor estricto queda
verde (`HIGH=0 MEDIUM=0 LOW=0`, exit 0); startup sin aumentar (≈4948).

## Cambios

1. **`AGENTS.md` (T1.1)** — adelgazado a *resolver root + invocar bootstrap*.
   Se removieron el detalle cold/warm, la regla de Graphify, la regla de cierre
   y la instrucción sobre ubicación/copia de skills. Alineado a la matriz de
   autoridad objetivo (AGENTS.md no contiene cold/warm, Graphify, cierre ni
   lista de skills). Una sola receta ejecutable de startup vive en bootstrap.

2. **`80-agents/agents-os/context-router.md` (T1.2)** — compactado a doc humano
   (qué es, por qué importa, idea central, ejemplo, relaciones). Se eliminó el
   algoritmo duplicado (tabla de rutas por intención con presupuestos, detalle
   de las 4 capas, principios-como-reglas-duras, contrato de salida "context
   pack" y procedimiento paso a paso). El algoritmo ejecutable permanece único
   en la skill `agents-os-context-retrieval` (D3). Callout agregado apuntando a
   esa autoridad.

3. **`80-agents/skills/sqx-temporal-failure-audit/SKILL.md` (T1.3)** — reparada
   la referencia relativa rota `../../agents-os-context-retrieval/SKILL.md` →
   `../agents-os-context-retrieval/SKILL.md` (skills son hermanas bajo
   `80-agents/skills/`).

4. **`.graphifyignore` (T1.3)** — agregada la exclusión `.obsidian/` (+ `**`).
   Estado de cliente/config de Obsidian no es corpus de retrieval.

5. **Nota rogue reubicada (T1.3)** — `80-agents/agents-os/agent-memory/2026-07-28-echo-forge-tradelist-java-snippets-stale.md`
   (sin frontmatter, en ubicación rogue dentro de core) →
   `80-agents/memory/public/known-error/2026-07-28-echo-forge-snippets-runtime-recompile-shadows-jar.md`
   con frontmatter canónico `type: known_error`. Directorio vacío
   `80-agents/agents-os/agent-memory/` eliminado. Links de frontmatter limitados
   a targets resolubles para no introducir drift nuevo.

6. **`80-agents/skills/agents-os-doctor/scripts/doctor.py` (T1.3, paso 7)** —
   refinado el check de portability: escaneo por línea con exención de comandos
   de acceso remoto (`ssh`/`scp`/`rsync`/`sftp`). Los paths `/home/kor/sqx/...`
   dentro de `ssh kor@worker.<host> '...'` son evidencia operacional remota
   legítima, no paths locales no portables del vault. La detección de paths
   locales del vault (`/Users/...`, `/home/...` en prosa/config) se mantiene.

## Verificación

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py --strict
# → AGENTS OS doctor: HIGH=0 MEDIUM=0 LOW=0 startup_tokens≈4948 ; exit 0
```

- Cero refs rotas core; `.obsidian/` excluido.
- Doctor sin falso positivo para paths remotos conocidos (SQX).
- Startup estimado no aumentó (≈4948, sin tocar el always-load set).
- Una sola receta de startup (AGENTS.md → bootstrap).

## Diff de autoridad (antes → después)

| Fuente | Antes | Después |
|---|---|---|
| `AGENTS.md` | hook + cold/warm + Graphify + cierre + regla de skills | resolver root + invocar bootstrap |
| `context-router.md` | concepto **+ algoritmo completo** (rutas, capas, budgets, pack, pasos) | concepto/valor/ejemplo + puntero a la skill |
| retrieval skill | algoritmo | algoritmo (única autoridad ejecutable) |
| doctor portability | flag global de `/Users\|/home/` | flag local; exención de comandos remotos |
