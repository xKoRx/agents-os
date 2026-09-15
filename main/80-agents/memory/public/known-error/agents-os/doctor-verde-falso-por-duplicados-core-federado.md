---
type: known_error
schema_version: 1
scope: global
created: "2026-09-14"
updated: "2026-09-14"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-doctor]]"
  - "[[agent-constitution]]"
  - "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
aliases:
  - doctor verde falso duplicados
  - duplicados core federado
  - migracion federada incompleta
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/global
  - project/agentsos
  - tech/agents-os
---

# Doctor verde falso por duplicados core↔federado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `agents-os-doctor` reporta `MEDIUM` con el texto `skill missing from index` para skills que sí están en `INDEX.md`, y el diagnóstico obvio —"falta indexar"— es falso.
- Peor: al corregir sólo esa clase, Doctor queda `HIGH=0/MEDIUM=0` con duplicados divergentes vivos en otra clase de artefacto. El verde no prueba canonicalidad.
- Incluso después del dedup, Doctor puede quedar `0/0/0` mientras el export
  contiene metadata que rutea a un área ausente o templates que reproducen
  paths y tags de un dominio no instalado. La fuente puede ser válida y el
  artefacto DEFAULT estar roto.

## Causa

- Una migración de Sistema 1 hacia el registro federado (`30-resources/agents/skills/`, `30-resources/runbooks/`) copió los artefactos sin borrar el origen en `80-agents/`. `INDEX.md` se repuntó al destino; los archivos quedaron en los dos lados.
- Doctor resuelve la fila del índice por el path del core, así que lee la copia federada como "ausente". Su cobertura abarca skills contra `INDEX.md` y **no** cubre runbooks, de modo que la duplicación en esa clase es invisible para el linter.

## Impacto

- Dos fuentes escribibles por hecho: sólo se edita una y la otra envejece en silencio, que es exactamente lo que la constitución (regla 5) existe para impedir.
- Verificado al 2026-09-14: 13 skills duplicadas (12 idénticas, `signals-code-review` divergente en `updated` y rutas relativas) y 9 runbooks duplicados con **tres divergencias materiales** — `aranea-mcp-capability-plane.md` (172 líneas), `aranea-ssh-mcp.md` (143 líneas) y `signals-code-review.md`, cuya copia federada está `status: superseded` mientras la del core sigue presentándose como vigente.
- `core-export/sources.list` embarca nueve de esas skills leyendo la ruta del core, así que la distribución compartida hereda la copia equivocada apenas una diverja.
- Seis memorias públicas Meli-scoped quedaban seleccionadas por árboles amplios.
  Además, templates distribuidos traían defaults Meli y paths operativos de
  Aranea; cada entidad nueva podía nacer mal ruteada aunque el vault fuente
  resolviera correctamente esas referencias.

## Detección

- `for d in 80-agents/skills/*/; do ls -d 30-resources/agents/skills/$(basename $d) 2>/dev/null; done` y el equivalente entre `80-agents/memory/public/runbook/` y `30-resources/runbooks/`: cualquier nombre presente en ambos lados es el defecto.
- Un `MEDIUM` de Doctor que diga `skill missing from index` sobre una skill que sí aparece en `INDEX.md` es la firma de este error, no un problema de índice.
- `cmp -s` entre las dos copias distingue duplicado inerte de duplicado divergente; el divergente ya causó daño.
- El gate del export debe resolver cada `area` distribuida y revisar metadata
  de todas las notas, además del cuerpo de startup y templates. Un grep verde
  no prueba la consecuencia: materializar cada tipo canónico en un vault
  DEFAULT temporal detecta placeholders que sólo se vuelven inválidos al render.

## Mitigación

- Resolver por nombre, no por clase: barrer skills **y** runbooks en el mismo pase, dejando `30-resources/` como autoridad y borrando la copia del core.
- Repuntar `core-export/sources.list` al path federado y, en el mismo cambio, adaptar `build-core.py`: `filter_skill_index()` matchea `80-agents/skills/([^/]+)/SKILL\.md` y descarta el bloque `## 🌐 Registro federado` completo, así que reapuntar sin tocarlo deja skills copiadas y cero filas en el índice distribuido.
- Convertir la detección en check permanente del provider `Canonical` del canonical-linter. Sin eso el invariante no sobrevive a la siguiente migración.
- Excluir del export la memoria scoped completa, sin falsificar sólo su `area`;
  neutralizar los templates en su autoridad fuente; y hacer que el propio
  builder aborte ante referencias de dominio, áreas no resolubles o entidades
  materializadas inválidas para DEFAULT.

## Evidencia

- `80-agents/skills/agents-os-doctor/scripts/doctor.py` — salida `HIGH=0 MEDIUM=13` al 2026-09-14.
- `30-resources/agents-os/core-export/sources.list` y `build-core.py` — proyección del índice distribuido.
- `30-resources/runbooks/signals-code-review.md` frente a `80-agents/memory/public/runbook/signals-code-review.md` — `superseded` contra vigente.

## Resolución

- Corregido el 2026-09-14 en PHASE 3.5: se retiraron las 13 copias core de skills y las 9 copias core de runbooks, conservando `30-resources/` como autoridad federada.
- `core-export` consume las nueve skills portables desde su ruta canónica,
  proyecta nueve filas descubribles, excluye declarativamente seis memorias
  scoped y valida el artefacto construido completo sobre sus superficies
  ejecutables y metadata de routing.
- Los templates distribuidos quedaron DEFAULT-neutral. El build materializa 44
  tipos canónicos en una instalación temporal y audita también el resultado;
  una prueba adversarial con `area: "[[{{title}}]]"` pasó el pre-render y fue
  rechazada post-render por producir un área inexistente.
- CL-21 mantiene el invariante para skills y runbooks. Evidencia post-fix: cero duplicados por nombre y Doctor `HIGH=0 MEDIUM=0 LOW=0` tanto en fuente como en el export construido.
