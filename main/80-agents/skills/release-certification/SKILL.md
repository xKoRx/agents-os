---
type: skill
schema_version: 1
name: release-certification
description: Certifica que un artefacto/release/binario corresponde realmente al código fuente autorizado esperado; usar ante "¿este binario es el commit X?", "certificar la release", "baseline gate", "gate de source integrity", verificación de pins de SDK, vcs.revision, blob equality o SHA256 de artefactos desplegados.
scope: global
created: "2026-08-29"
updated: "2026-08-29"
entities: []
related:
  - "[[symphony-release-certification]]"
  - "[[e2e-gated-validation]]"
aliases:
  - certificación de release
  - baseline gate
  - source integrity gate
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/go
  - action/verify
---

# release-certification

## Purpose

Responder con evidencia la pregunta "¿lo que estoy probando corresponde realmente al código/release esperado?". Evita el falso PASS clásico de confiar en el directorio local, en un tag o en "acabo de compilar". Produce un veredicto `PASS / FAIL / INCONCLUSIVE` con evidencia reproducible.

## Minimal Read

Read only:
1. El runbook del sistema para comandos exactos (ej. [[symphony-release-certification]]).

## Procedure

1. **Baseline gate:** fetch del remote; verificar `HEAD == origin/<main>` contra el baseline autorizado esperado; verificar que el commit de referencia certificado es ancestro (`git merge-base --is-ancestor <ref> HEAD`, exit 0); inventariar el dirty del worktree, clasificarlo en propio vs extranjero y preservarlo sin stage/commit/clean.
2. **Source integrity gate:** si master avanzó desde el commit certificado, comparar cada commit nuevo contra los archivos load-bearing de la feature; sólo chores/docs/artifacts ⇒ documentar rebaseline operacional y continuar; cualquier cambio funcional ⇒ FAIL/BLOCKED. Verificar igualdad por blob (`git rev-parse <ref>:<path>` vs `HEAD:<path>`) de los archivos congelados y el last-commit de cada carrier (debe ser el commit certificado de su slice).
3. **Release integrity gate:** si existe release construida, demostrar su contenido: en Go, `go version -m <binario>` debe mostrar `vcs.revision` == HEAD autorizado y los `dep` de módulos pinned == los pins esperados (un `vcs.modified=true` exige explicar qué archivos no-Go lo causan); verificar SHA256/size de los binarios contra el manifest o descriptor publicado.
4. Emitir veredicto por gate y consolidado, con los comandos exactos ejecutados y sus salidas clave (hashes, refs) como evidencia.

## Output

```text
BASELINE_GATE: PASS/FAIL/INCONCLUSIVE — <HEAD, origin, ancestro, dirty>
SOURCE_INTEGRITY: PASS/FAIL/INCONCLUSIVE — <blobs verificados, last-commits, rebaseline si aplica>
RELEASE_INTEGRITY: PASS/FAIL/INCONCLUSIVE — <vcs.revision, pins, sha256s>
```

## Hard Rules

- El veredicto se basa en contenido (blobs, hashes, build info), nunca en nombres de directorios, tags ni intenciones.
- Foreign dirty se preserva siempre; jamás se "limpia" para que el build quede limpio.
- Un `vcs.modified=true` sin explicación ⇒ INCONCLUSIVE, no PASS.
- Si el release tooling exigiera modificar source o commit, STOP/BLOCKED.
