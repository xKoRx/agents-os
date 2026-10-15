---
type: change_log
schema_version: 1
scope: session
created: "2026-10-14"
updated: "2026-10-14"
area: "[[Meli]]"
project: "[[CP Flink local]]"
application:
entities: ["[[CP Flink local]]"]
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# PR 3 PythonDriver spike — STOP

## Cambio

- Actualizada [[CP Flink local]] con el resultado observado del spike y el siguiente paso propuesto.

## Evidencia

- Precondiciones PASS; imagen Flink 1.20.5 construida con PyFlink 1.20.5 mediante secret de BuildKit. Prueba binaria sin wheel arm64; toolchain requerido.
- Upload REST exitoso; run PythonDriver HTTP 400 por falta del ejecutable python, incluso con -pyexec python3. No hubo job id ni prueba de procesamiento Kafka.
- History e inspect: 0 coincidencias de furycloud cada uno. Logs sin credenciales expuestas.
- STOP antes de Java; sin commits, push, PR, gates ni E2E. Parche temporal conservado fuera del repo; worktree restaurado y limpio en 0728044c.
- Cleanup: 0 contenedores y 0 redes rio-*, contexto activo colima. Sin diff productivo contra base ni origin/develop.

## Próximo paso

- Evaluar alias python → python3 en la imagen y repetir el spike; alternativa no implementada.

## Rollback

- Revertir únicamente la entrada y fila de esta sesión en [[CP Flink local]].
