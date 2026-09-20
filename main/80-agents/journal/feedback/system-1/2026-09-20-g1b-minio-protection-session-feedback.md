---
type: session_feedback
schema_version: 1
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[agents-os-agent-run-register]]"
aliases:
  - feedback g1b minio 2026-09-20
confidence: verified
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
  - area/aranea
---

# 2026-09-20-g1b-minio-protection-session-feedback

## Fricción real detectada (G1B, sesión one-shot larga)

- **PBS 4.2.5 restore**: `--pattern` LEE el archivo pxar completo por cada restore parcial (44G leídos para extraer 20G) — drills por-bucket inviables; la solución fue restore completo 1 pasada + verificación posterior. Coste: ~1h extra. Documentado en skill de custodia.
- **Terminales con timeout del runtime (420s)**: procesos remotos (`mv`, `sha256sum`, guest-exec con tar) siguieron corriendo tras el corte del cliente → writers solapados corrompieron una parte del spool. Mitigación aplicada: re-stream con sha determinista; lección de spool/timeout en skill.
- **Múltiples iteraciones de scripts**: globs de doble prefijo, dash vs bash, `pkill -f` auto-matcheado (mató 2 sesiones SSH propias, benignas), comentario de authorized_keys con guion vs guion bajo (grep=0 falso). Todas corregidas en caliente; lecciones consolidadas en skill `custodia-claves-backup-g1a`.

## Pain Pattern Candidate

- Operaciones multi-host de larga duración dentro de un chat interactivo sin mecanismo de "job con presupuesto": los timeouts del runtime client vs procesos remotos vivos generan estado ambiguo que exige verificación cara. Candidato: wrapper `g1b-*`-style (spool + manifiesto + reanudación por bucket) ya demostrado esta sesión.
