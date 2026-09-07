---
type: change_log
schema_version: 1
scope: session
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager]]"
related:
  - "[[Echo Forge]]"
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

# Stager F1.8-R — Windows directory sync blocked

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - repo `stager`: `internal/activation/store.go`, `internal/activation/state_unix.go`, `internal/activation/state_windows.go` y paquete SDD

## Motivo

- Registrar que F1.8-R ya tuvo ejecución Windows real y que el resultado fue FAIL antes de evaluar la matriz, sin declarar G1 como aprobado ni abrir F2.

## Fuentes usadas

- Salida adjunta de `activation.test.exe` ejecutada en Windows: los casos `TestEffectCrashWindowsRecoverWithSameID`, `TestFailuresAfterEveryDurableWriteRecoverWithSameID` y `TestTripleRunOnceConvergesForEachTarget` fallan al sincronizar el directorio de estado con `Access is denied`.
- Checkout F1 local recuperado desde el workspace histórico de Stager; el remoto `github.com/xKoRx/stager` en `1f8989c` sigue siendo F0 y no contiene `internal/activation`, por lo que el cambio queda pendiente de integrar/publicar junto con el resto de F1.
- Patrón equivalente inspeccionado en `internal/staging/state_windows.go` e `internal/compat/state_windows.go`: `MoveFileEx` con `MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH` y `syncDirectory` no-op.

## Resolución aplicada

- `activation` ahora tiene adapters por OS: Unix conserva `rename` y directory sync; Windows usa `MoveFileEx` con `REPLACE_EXISTING|WRITE_THROUGH` y omite sólo el directory sync no soportado. El control del proyecto y su tarea puente conservan F1.8-R en WIP, G1 bloqueado, F2 no autorizada y `progress: 52` hasta la repetición real en Windows.

## Validación

- FAIL reproducido en Windows. PASS tras el fix: `go test -count=1 ./...`, `go vet ./...`, `git diff --check`, builds Linux/Windows de `cmd/stager` y compilación Windows de `internal/activation` como `activation.test.exe`. Falta ejecutar ese binario en Windows.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, valores de entorno, paths absolutos de máquina ni secretos

## Rollback

- Revertir los tres archivos de adapter de `internal/activation` y las actualizaciones documentales si la evidencia Windows invalida el patrón; no presentar G1 como PASS sin una repetición exitosa de la matriz Windows.
