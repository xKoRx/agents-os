---
type: learning
scope: project
created: 2026-07-02
updated: 2026-07-02
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
  - Cuando se refactoriza un documento histórico con múltiples iteraciones obsoletas en un homelab / sistema grande, congelar el resultado como "design-frozen" + cerrar sesión + entregar tickets next-step.
entities:
  - "[[Aranea]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[../../../30-resources/aranea/03-storage/backup-dr/00-index]]"
  - "[[../../../30-resources/aranea/03-storage/backup-dr/BACKUP-DR-DESIGN]]"
  - "[[../../../30-resources/aranea/03-storage/backup-dr/DIFF-CONCEPTUAL]]"
  - "[[../../../30-resources/aranea/03-storage/backup-dr/REQUEST-CHANGES]]"
  - "[[../../../30-resources/aranea/03-storage/backup-dr/backup-policy]]"
aliases:
  - design-frozen workflow
  - homelab refactor pattern
  - closeout handover pattern
confidence: verified
source_session: 2026-07-02-backup-dr-cerrar-warnings-admin
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - homelab
  - aranea
  - refactor
  - design-frozen
  - workflow
  - policy
  - runbook
  - kind/learning
  - priority/high
  - project/agents-os
---

# 🎓 Design-Frozen Pattern for Homelab Refactors

## Aprendizaje (resumen ejecutivo)

Para refactorizar documentos de diseño en un homelab / sistema grande con **múltiples iteraciones obsoletas** y **contradicciones activas**, el patrón óptimo es:

```
[estado 1] iteraciones históricas con contradicciones
   ↓ (auditoría + racionalización)
[estado 2] DESIGN-FROZEN con 16 archivos ordenados
   ↓ (NO implementación)
[estado 3] tickets next-step + esperar owner gate
```

El "design-frozen" no es excusa para no implementar: **es la barrera formal para no implementar**. Su función es cerrar la sesión con diseño utilizable, sin ejecutar cambios, y dejar next-steps en tickets separados.

---

## Contexto de aplicación

Caso real: `03-storage/backup-dr/` refactor del 2026-07-01.

**Antes**: 4+ iteraciones de propuestas (DESIGN-PROPOSAL iter 1-4, PROPUESTA-COMPLETA-ITER4, BACKUP-SYSTEM, AUDIT, TOPOLOGY-AUDIT) con contradicciones activas:
- `sdf` mencionado como spare (realidad: está en pool0 mirror-0).
- `local-sqx-hera` como destino zfs-recv (realidad: sagrado SQX).
- `pool2` confundido con backup real.
- Tier cloud sin segregación (pcloud = bulk en alguna versión, critical en otras).

**Iteración usada**: iter 5 → 16 archivos congelados → 18 archivos tras warnings admin.

---

## Patrón (5 fases)

### Fase A — Detección del bucle de iteraciones

Síntomas que indican que el refactor anterior entró en bucle:

1. **El ticket original acumula iter 1, 2, 3, 4** sin decisión final.
2. **Hay propuestas "DEPRECATED"** pero referenciadas desde docs activos.
3. **Los "decisiones congeladas" del doc abierto contradicen otros docs**.
4. **El owner responde "ya trabajamos esto"** sin poder identificar la versión canónica en memoria agent.

**Diagnóstico**: `grep -rE "DEPRECATED|superseded" --include="*.md" <vault>`. Una vez N iteraciones detectadas, parar y refactorizar.

### Fase B — Auditoría basada en contradicciones

Construir `DIFF-CONCEPTUAL.md` que liste **cada contradicción** entre documentos:
- `sdf` como spare ↔ `sdf en pool0 mirror-0`.
- `local-sqx-hera` como destino ↔ `local-sqx-*` sagrado.
- …

Cada contradicción recibe una decisión (mantener / cambiar / descartar) y un RC-number asociado si la decisión cambia comportamiento.

### Fase C — Redacción del design final congelado

`BACKUP-DR-DESIGN.md` con:

1. **Decisiones congeladas** enumeradas (`F-01` ... `F-14`) con:
   - Descripción corta.
   - Evidencia (qué prueba la decisión).
   - Prohibición explícita ("NO cambiar sin Request Change").
2. **Capas funcionales** (A-G) con responsables, comandos permitidos y prohibidos.
3. **Recursos protegidos** (VGs, paths, IPs que NO TOCAR).
4. **`dangerous_commands`** rotuladas (DANGEROUS = requiere owner approval).

### Fase D — Subdivisión en subproyectos agente + proyecto owner

Owner project + N agent-projects:
- Cada agent-project tiene **objetivo / scope / inputs / permisos / secrets / ventanas / dependencies / risks / safety-gates / implementation-plan / validation-plan / rollback-plan / evidence**.
- Owner project lista tareas con `type, reason, required_by, blocks, acceptance_criteria`.

### Fase E — Closeout handover

Al cerrar la sesión de diseño, NO implementar. Entregar:

1. `index` con tabla de docs por rol.
2. Cada `status: design-frozen` (no `in-progress`, no `done`).
3. Cada `agent-project-XX` con `status: ready` (no `in-progress`).
4. Owner-tasks como tickets formales (no solo checkboxes).
5. `REQUEST-CHANGES.md` como workflow vivo.
6. `DIFF-CONCEPTUAL.md` (a veces pasa a `awaiting-owner-approval` para recordar que NO fue aprobado).

---

## Lo que NO es "design-frozen"

- "design-frozen" no es doc muerto. Es el **estado que precede** al owner gate formal.
- "design-frozen" no es excusa para skips en implementación. **Cada agencia de campo** debe generar ticket(s) implementation-fase-1 (vzdump, PBS install, Restic push, etc.) — ver `homelab-storage-backup-design` skill y `agent-project-04...07`.
- "design-frozen" no exime de backups: la **documentación** debe respaldarse (commit Obsidian git, snapshot Vault).

---

## Anti-patrones a evitar

1. **"Listo, lo escribimos" sin smoke test de uso del design**: el design es utilizable solo si el agente puede leerlo y ejecutar pasos sin ambigüedad.
2. **Tickets con "closed" cuando solo está "design-frozen"**: status confunde implementación vs diseño.
3. **Agent-projects con status `in-progress` cuando solo se terminó el paper design**: confunde el sprint.
4. **Olvidar owner-tasks bloqueantes**: sin owner-gate explícito, `design-frozen` puede convertirse en "olvidado para siempre".
5. **No tener REQUEST-CHANGES.md workflow**: cualquier cambio material al design congelado debe pasar por ahí, no edición silenciosa.

---

## Recursos para profundizar

- `homelab-storage-backup-design` skill (cómo construir propuestas basadas en inventory real, no en assumptions).
- `aranea_agent_ro_inventory_refresh` skill (snapshots raw que alimentan el design).
- `BACKUP-DR-DESIGN.md` §15 (Cómo usar este set desde otra sesión).
- `BACKUP-DR-DESIGN.md` §16 (Lecciones del refactor).

---

## Confirmación operativa

Aplicado en `03-storage/backup-dr/` el 2026-07-02:
- 18 archivos totales.
- 9 subproyectos agent + 1 owner project.
- 14 decisiones congeladas con RC-numbered mutations vía REQUEST-CHANGES.md.
- 16 alertas con thresholds definidos.
- 6 restore drills con criterios PASS/FAIL.
- 0 secretos, 0 tokens, 0 hashes publicados en docs.
- 1 iter de validación auditor (PASS_WITH_WARNINGS 9/9 constraints duras + 0 contradicciones activas).

## Referencias

- `BACKUP-DR-OWNER-PROJECT.md`
- `00-index.md` del set
- Ticket 013 (superseded): `[2026-06-30-013-storage-redesign-backup-design]`
- Skill: `homelab-storage-backup-design`
- Skill: `aranea_agent_ro_inventory_refresh`
- Skill: `request-change-workflow` (mencionado en `BACKUP-DR-OWNER-PROJECT.md`)
