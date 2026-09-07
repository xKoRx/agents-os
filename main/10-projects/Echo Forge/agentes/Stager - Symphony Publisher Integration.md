---
type: project
owner: agent
root: false
status: completed
priority: P1
area: "[[Echo]]"
application: "[[echo-forge]]"
parent: "[[Echo Forge]]"
sprint: "[[A26Q2S7]]"
start: 2026-08-08
due:
progress: 100
repo: symphony
jira:
prs:
entities:
  - "[[stager-app]]"
  - "[[Stager]]"
aliases:
  - Symphony Stager Publisher Integration
  - Multi-platform Symphony Publisher
tags:
  - kind/project
  - area/echo
  - tech/go
  - tech/deployment
  - app/stager
created: 2026-08-08
updated: 2026-08-09
---

# Stager - Symphony Publisher Integration

> [!info]+ Proyecto cerrado
> **Área:** [[Echo]] · **Estado:** completed · **Prioridad:** P1 · **Parent:** [[Echo Forge]]
> El publisher y la integración Stager quedaron entregados; esta nota conserva el contrato y la evidencia para soporte o una futura iniciativa separada.

## 🎯 Objetivo

- Hacer que el publisher actual de Symphony construya y publique una release única con `linux-amd64` y `windows-amd64`, agregue metadata verificable al manifest y conserve el manifest como commit point remoto.
- Demostrar que [[stager-app|Stager]] puede descargar/verificar/instalar ambas plataformas desde MinIO sin retirar el Bash legacy ni tocar todavía quiesce, launcher o SCM.

## 📊 Estado actual

- **F5/G5 completa + cutover productivo (2026-08-09).** Shadow aislado PASS. Luego, por instrucción del owner: Stager Go + wrapper puente instalado en Zeus/Hera/Kronos; publicada release `0.2.40` (manifest aditivo) a `deploy`; validado `CURRENT=0.2.40`, `current→releases/0.2.40` y workers `active` en los tres. Bash queda como `.bash.bak`. Puente: symlink `current`, `PENDING` en `/var/lib/symphony`, permisos `a+rX` para `User=kor`.
- **Proyecto cerrado por el owner (2026-08-09).** La responsabilidad entregada es publicar y preparar releases verificables para ambas plataformas. Quiesce/drain y la supervisión Windows pertenecen al worker/supervisor de Symphony y sólo se abrirán como iniciativa separada si el owner lo solicita.
- Publicación aislada F5 fue artifact-first vía `mc`. El cutover usó el mismo patrón sobre bucket `deploy` (sin `deploy_release.sh`).
- **Incidente y remediación (misma sesión previa):** harness fallido publicó `9.9.10`; revertido a `0.2.39` antes del cutover `0.2.40`.
- Cambio preexistente del usuario: `deployer_screen.log` modificado; no tocar, restaurar ni incluir en commits.

## Cómo retomar — orden de lectura obligatorio

1. `AGENTS.md` y `CONSTITUTION.md` de Symphony; asumir rol implementor sólo con Allowed Files aprobados en el SDD.
2. [[stager-app]] — contrato del sistema y estado real.
3. [[2026-08-08-stager-mvp-boundary-and-activation]] — decisiones que no se rediseñan.
4. Repo Stager: `docs/ARCHITECTURE.md`, `docs/MANIFEST.md`, `docs/SYMPHONY.md` y `specs/STAGER-MVP/SPEC.md`.
5. Esta nota desde “Baseline confirmado” hasta “Paso a paso”.
6. Recién entonces abrir los archivos Symphony listados en cada fase; no hacer un scan amplio del monorepo.

## ✅ Tareas

> [!example]- Fuente de tareas del implementor
> Estados: `[ ]` To Do · `[/]` WIP · `[r]` Review · `[x]` Done · `[-]` Canceled. Actualizar esta lista y la bitácora a medida que avanza cada gate.

### G0 — Contrato y SDD

- [x] Confirmar/registrar D-P01: para esta integración Symphony publica Linux+Windows como release completa; Stager core sigue aceptando subconjuntos declarados #owner/agent #type/dev #area/echo
- [x] Crear `specs/FEAT-DEPLOYER-STAGER-PUBLISHER-INTEGRATION/{SPEC.md,PLAN.md,TASKS.md}` y registrar la feature en `specs/SPECS.md` #owner/agent #type/dev #area/echo
- [x] Mantener en SPEC el manifest objetivo, llevar Allowed Files exactos a PLAN y obtener gate G0 antes de código #owner/agent #type/dev #area/echo

### F1 — Release local multi-plataforma

- [x] Extender `deploy_sqx.sh` para construir Linux y Windows dentro del mismo staging temp antes del único `mv` final #owner/agent #type/dev #area/echo
- [x] Mantener los cuatro artefactos Linux y agregar `windows-amd64/sqx-mt5-worker.exe` #owner/agent #type/dev #area/echo
- [x] Hacer fallar el release completo si cualquier build/copia falla; nunca promover una carpeta parcial #owner/agent #type/dev #area/echo

### F2 — Manifest aditivo verificable

- [x] Extender `update_manifest()` con `entrypoint` + `files[]` para ambas plataformas, preservando campos legacy Linux; el manifiesto base legacy no se falseó con hashes placeholder y se transforma sólo desde una release completa #owner/agent #type/dev #area/echo
- [x] Calcular `size` y SHA-256 desde los bytes finales del release local; no desde fuentes ni binarios temporales #owner/agent #type/dev #area/echo
- [x] Usar `object_key=worker/sqx/...` sin prefijo de bucket; conservar `deploy/worker/...` sólo en campos legacy #owner/agent #type/dev #area/echo
- [x] Fortalecer `release_layout_matches_manifest()` para validar ambas plataformas, keys, tamaños y hashes al reanudar #owner/agent #type/dev #area/echo
- [x] Actualizar `kick_release_for_upload()` para tocar los cinco artefactos y reescribir manifest al final #owner/agent #type/dev #area/echo

### F3 — Deployer multi-plataforma

- [x] Evolucionar config desde plataforma singular a lista permitida con fallback backward-compatible a `config/platform` #owner/agent #type/dev #area/echo
- [x] Hacer que `StaticLayout` acepte sólo `linux-amd64` y `windows-amd64` configuradas, manteniendo key remota `<base>/<version>/<platform>/<file>` #owner/agent #type/dev #area/echo
- [x] Extender el modelo/validator Go del manifest para tipar y validar el contrato aditivo completo #owner/agent #type/dev #area/echo
- [x] Configurar `run_deployer.sh`/JSON/ETCD docs para observar ambas plataformas con un solo watcher #owner/agent #type/dev #area/echo
- [x] Conservar sin cambio la regla watcher: todos los artifact PUT exitosos antes del manifest PUT #owner/agent #type/dev #area/echo

### F4 — Tests y builds

- [x] Agregar tests de pathing multi-plataforma, plataforma no permitida y compatibilidad singular #owner/agent #type/dev #area/echo
- [x] Agregar tests de manifest válido, hash/size/path inválidos, entrypoint ausente y legacy aditivo #owner/agent #type/dev #area/echo
- [x] Agregar test watcher con artefactos Linux+Windows que demuestre manifest-last #owner/agent #type/dev #area/echo
- [x] Agregar test donde falla Windows upload: manifest no se publica y snapshot queda pendiente para retry #owner/agent #type/dev #area/echo
- [x] Aislar `deployer/cmd/deployer-watcher/example_test.go` de ETCD real para que `go test ./deployer/...` sea hermético #owner/agent #type/dev #area/echo
- [x] Ejecutar shell syntax, tests, vet y builds Linux/Windows; `VERIFICATION.md` queda reservado al verifier para el gate pre-merge #owner/agent #type/dev #area/echo

### F5 — MinIO real y shadow

- [x] Publicar una release de prueba en bucket/prefix aislado con credenciales inyectadas, nunca versionadas — bucket `stager-publisher-int`, release `9.9.9`, upload `mc` artifact-first; watcher aislado no usado #owner/agent #type/dev #area/echo
- [x] Verificar por `mc stat/cat` que los cinco objetos existen y el manifest fue escrito después — clúster MinIO + lab local #owner/agent #type/dev #area/echo
- [x] Ejecutar Stager con root temporal y override Linux; verificar bytes, hashes, layout, `CURRENT` y `PENDING` — `staged` → `noop`; corrupción rechazada y `CURRENT` conservado #owner/agent #type/dev #area/echo
- [x] Ejecutar Stager con root temporal y override Windows; verificar `bin/sqx-mt5-worker.exe`, `CURRENT` y `PENDING` — `staged` → `noop` #owner/agent #type/dev #area/echo
- [x] Ejecutar shadow Linux con root/state separado en Zeus (`/tmp/stager-shadow-linux-9.9.9`); Bash sigue autoridad productiva (`/opt/symphony` = `0.2.39`) #owner/agent #type/dev #area/echo
- [x] Documentar rollback e incidente; tarea puente en Review; sin cutover intencional #owner/agent #type/dev #area/echo

## Baseline confirmado — no redescubrir

| Hecho | Evidencia en Symphony `9612f83` | Implicación |
|---|---|---|
| El orquestador prepara worker, actualiza manifest y espera confirmación MinIO | `deploy_release.sh:105-128`, `894-914` | Extender el flujo; no crear otro publisher paralelo |
| Build local sólo Linux y promoción de release es atómica | `deploy_sqx.sh:19-34`, `44-51`, `108-115` | Agregar Windows dentro del mismo staging antes del `mv` |
| Manifest actual se genera sólo para Linux | `deploy_release.sh:439-475` | Extender aditivamente; preservar legacy |
| Resume valida sólo keys Linux | `deploy_release.sh:477-490` | Reconciliar ambas plataformas e integridad |
| Kick toca sólo cuatro artefactos Linux | `deploy_release.sh:608-631` | Incluir Windows antes de reescribir manifest |
| Pathing acepta exactamente una plataforma | `deployer/adapters/pathing-staticlayout/pathing.go:13-55` | Convertir a allow-list, no wildcard |
| Config es singular | `deployer/core/config/options.go:5-29`, `cmd/deployer-watcher/main.go:38-49,90-173` | Agregar `platforms` con fallback legacy |
| Modelo manifest sólo conoce version/metadata | `deployer/core/capabilities/manifest.go:7-19` | Tipar contrato aditivo completo |
| Manifest se separa de artifact actions y publica al final | `deployer/watcher/watcher.go:111-205` | Invariante ya correcta; proteger con tests |
| Test manifest-last ya existe | `deployer/watcher/watcher_test.go:543-606` | Extender a dos plataformas, no reemplazar |
| Upload failure conserva snapshot para retry | `deployer/watcher/watcher.go:173-205`, test `608-646` | Agregar caso Windows+manifest |
| Pathing ya normaliza keys Windows a `/` | `pathing_test.go:227-239` | Reutilizar; falta multi-plataforma simultánea |
| Worker Windows real es `sqx-mt5-worker.exe` | `sqx/cmd/sqx-mt5-worker/main.go`, `deploy/windows/sqx-mt5-worker/README.md:7-15` | Nombre inicial del artifact Windows |
| Installer Windows legacy copia sobre current plano | `Install-EchoForgeMT5Worker.ps1:27-50` | No reutilizar para Stager ni modificar en este proyecto |

## Decisiones congeladas

### D-P01 — Completitud de release Symphony

**Default de implementación:** `deploy_release.sh` sólo publica el manifest cuando los artefactos Linux y Windows de la versión están completos. Esta obligación pertenece a la integración Symphony; [[stager-app|Stager]] sigue aceptando cualquier subconjunto explícitamente declarado.

Si el owner decide posteriormente permitir releases parciales, cambiar build/gate/manifest del publisher; no modificar el core Stager.

### D-P02 — Un watcher, no dos

Usar una sola instancia del deployer observando ambas plataformas. Dos watchers independientes sobre el mismo manifest introducirían una carrera de commit point.

### D-P03 — Wire contract sin dependencia Go cross-repo

Symphony genera JSON según `stager/docs/MANIFEST.md`; no importa paquetes internos de Stager. La prueba contractual es ejecutar el parser/Stager real contra el manifest producido.

### D-P04 — Bucket y key son distintos

Con bucket `deploy`:

```text
manifest key nuevo = worker/sqx/manifest.json
artifact object_key nuevo = worker/sqx/<version>/<platform>/<file>
legacy mc path = deploy/worker/sqx/<version>/<platform>/<file>
```

No copiar el prefijo `deploy/` a `files[].object_key`.

### D-P05 — Layout instalado

```text
linux-amd64:
  entrypoint: bin/symphony
  files:
    symphony                → bin/symphony              executable
    sqx-watcher             → bin/sqx-watcher           executable
    start-symphony-worker.sh→ bin/start-symphony-worker.sh executable
    promtail-worker.yaml    → etc/promtail-worker.yaml

windows-amd64:
  entrypoint: bin/sqx-mt5-worker.exe
  files:
    sqx-mt5-worker.exe      → bin/sqx-mt5-worker.exe
```

El object layout remoto puede seguir plano bajo cada plataforma; `files[].path` controla el layout instalado.

## Manifest objetivo exacto

Los hashes/tamaños son calculados, nunca placeholders en output real:

```json
{
  "app": "symphony",
  "feature": "sqx-worker-minio",
  "version": "<version>",
  "artifacts": {
    "linux-amd64": {
      "mode": "files",
      "entrypoint": "bin/symphony",
      "files": [
        {"path":"bin/symphony","object_key":"worker/sqx/<version>/linux-amd64/symphony","size":0,"sha256":"<sha256>","executable":true},
        {"path":"bin/sqx-watcher","object_key":"worker/sqx/<version>/linux-amd64/sqx-watcher","size":0,"sha256":"<sha256>","executable":true},
        {"path":"bin/start-symphony-worker.sh","object_key":"worker/sqx/<version>/linux-amd64/start-symphony-worker.sh","size":0,"sha256":"<sha256>","executable":true},
        {"path":"etc/promtail-worker.yaml","object_key":"worker/sqx/<version>/linux-amd64/promtail-worker.yaml","size":0,"sha256":"<sha256>"}
      ],
      "binary": "deploy/worker/sqx/<version>/linux-amd64/symphony",
      "watcher": "deploy/worker/sqx/<version>/linux-amd64/sqx-watcher",
      "runner": "deploy/worker/sqx/<version>/linux-amd64/start-symphony-worker.sh",
      "promtail_yaml": "deploy/worker/sqx/<version>/linux-amd64/promtail-worker.yaml"
    },
    "windows-amd64": {
      "mode": "files",
      "entrypoint": "bin/sqx-mt5-worker.exe",
      "files": [
        {"path":"bin/sqx-mt5-worker.exe","object_key":"worker/sqx/<version>/windows-amd64/sqx-mt5-worker.exe","size":0,"sha256":"<sha256>"}
      ]
    }
  },
  "update": {
    "strategy": "stage_mark_pending",
    "pending_file": "/var/lib/symphony/PENDING"
  }
}
```

En el JSON final todo `size` debe ser `>0` y todo SHA debe tener 64 hex.

## Paso a paso por fase

### F0 — Crear el paquete SDD antes de código

1. Crear SPEC/PLAN/TASKS bajo `specs/FEAT-DEPLOYER-STAGER-PUBLISHER-INTEGRATION/`.
2. Copiar objetivo, decisiones D-P01–D-P05, manifest y criterios de esta nota.
3. En TASKS declarar Allowed Files; no autorizar worker quiesce, launcher ni installer Windows.
4. Registrar feature en `specs/SPECS.md`.
5. Gate: arquitecto revisor aprueba antes de dispatch implementor.

### F1 — Empaquetar ambas plataformas atómicamente

En `deploy_sqx.sh`:

1. Reemplazar `PLATFORM` singular por constantes Linux/Windows.
2. Crear ambos dirs dentro de `STAGING_ROOT/<version>/`.
3. Conservar builds Linux actuales.
4. Agregar desde repo root:

```bash
ENV=production GOOS=windows GOARCH=amd64 CGO_ENABLED=0 \
  go build -ldflags="-w -s" \
  -o "${WINDOWS_DIR}/sqx-mt5-worker.exe" \
  ./sqx/cmd/sqx-mt5-worker
```

5. Copiar/generar auxiliares Linux como hoy.
6. Verificar los cinco archivos regulares y no vacíos.
7. Ejecutar el único `mv STAGING_ROOT/<version> → deploy/<version>` sólo al final.
8. Si Windows falla, trap limpia staging y `deploy/<version>` no aparece.

### F2 — Generar manifest con bytes verificables

En `deploy_release.sh`:

1. Agregar helpers portables `file_size` y `sha256_file`. Resolver hash en orden: `sha256sum`, `shasum -a 256`, `openssl dgst -sha256`; fallar si ninguno existe.
2. Enumerar descriptor central por plataforma para no repetir keys en `update_manifest`, resume y kick.
3. Antes de crear temp manifest, validar cinco archivos.
4. Calcular tamaño/hash de cada archivo final bajo `deploy/<version>`.
5. Con `jq`, preservar top-level y legacy Linux, reemplazar aditivamente `entrypoint/files` de Linux y Windows.
6. Validar el temp con `jq -e`: versión, platforms, entrypoints, cinco paths, keys sin `deploy/`, size >0, SHA regex y flags executable.
7. `mv` atómico del temp a `deploy/manifest.json`.
8. En resume, recalcular y comparar integridad contra manifest; si diverge, abortar sin sobrescribir release inmutable.
9. En kick, tocar cinco archivos, esperar el baseline si aplica y reescribir manifest al final.

### F3 — Permitir ambas plataformas en un publisher

Cambio recomendado, limpio y backward-compatible:

1. `Options.Platforms []string`; parser trim/dedup/reject vacío.
2. Nueva config `platforms` como CSV y flag `-platforms`; mantener `-platform` como alias legacy singular durante migración.
3. Nueva ETCD `config/platforms`; fallback a `config/platform`; último default `linux-amd64`.
4. `StaticLayout` recibe allow-list y valida el segundo segmento contra ella. No wildcard.
5. `run_deployer.sh` pasa `-platforms linux-amd64,windows-amd64` para el caso Symphony.
6. Telemetría usa lista ordenada/join, sin cardinalidad por versión.
7. `Manifest` Go tipa artifacts/files/update y validator comprueba todas las plataformas declaradas.
8. `SimplePlanner` y `watcher.Runner` no requieren rediseño; sólo tests de regresión.

### F4 — Verificación hermética

Comandos mínimos:

```bash
bash -n deploy_sqx.sh
bash -n deploy_release.sh
bash -n run_deployer.sh
gofmt -w <archivos-go-modificados>
go test ./deployer/core/... ./deployer/adapters/... ./deployer/watcher/...
go test ./deployer/...
go vet ./deployer/...
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build ./sqx/cmd/sqx-worker
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build ./sqx/cmd/sqx-mt5-worker
```

Usar `GOCACHE` fuera del repo si el sandbox lo requiere. `go test ./deployer/...` debe quedar hermético; hoy `example_test.go` intenta ETCD real y es deuda explícita de esta fase.

### F5 — Contrato real MinIO → Stager

1. Usar bucket/prefix de integración aislado o MinIO local; credenciales sólo por environment/secret store.
2. Arrancar un único deployer multi-plataforma.
3. Preparar una versión nueva y observar PUT de cinco artifacts.
4. Confirmar que el manifest PUT ocurre después del último artifact PUT.
5. `mc stat` a cada key y `mc cat` al manifest; comparar tamaño/hash.
6. En repo Stager ejecutar dos veces con `STAGER_ROOT` temporal y overrides Linux/Windows.
7. Primera ejecución: `staged`; segunda: `noop`.
8. Corromper un objeto en el entorno aislado: Stager debe fallar y dejar `CURRENT` anterior.
9. Shadow Linux usa root/state separado; no escribir `/opt/symphony` ni `/var/lib/symphony` aún.

## Allowed Files propuestos para el SDD

```text
specs/FEAT-DEPLOYER-STAGER-PUBLISHER-INTEGRATION/**
specs/SPECS.md
deploy_sqx.sh
deploy_release.sh
run_deployer.sh
deploy/manifest.json
deployer/core/config/options.go
deployer/core/config/options_test.go
deployer/core/config/etcd_keys.go
deployer/core/capabilities/manifest.go
deployer/adapters/manifest-json/manifest.go
deployer/adapters/manifest-json/manifest_test.go
deployer/adapters/pathing-staticlayout/pathing.go
deployer/adapters/pathing-staticlayout/pathing_test.go
deployer/core/instrumentation/telemetry.go
deployer/core/instrumentation/telemetry_test.go
deployer/cmd/deployer-watcher/main.go
deployer/cmd/deployer-watcher/example_test.go
deployer/doc/demo/deployer.json
deployer/watcher/watcher_test.go
docs/deployment/stager-publisher-integration.md
```

`deployer/watcher/watcher.go` sólo se autoriza si un test demuestra un bug; su orden manifest-last actual debe preservarse.

## Fuera de alcance — no mezclar

- Cambios a `sqx-worker`/`sqx-mt5-worker` runtime o quiesce.
- Launcher Windows, SCM, Task Scheduler o installer Stager.
- Cutover Linux o eliminación del Bash.
- API/UI/DB/control plane/scopes.
- Self-update, auto-rollback o PKI.
- Modificar `deployer_screen.log` o usar credenciales versionadas.

## Acceptance criteria

1. Una versión se prepara localmente con cuatro archivos Linux y un exe Windows dentro de un único release inmutable.
2. Manifest conserva los campos que consume Bash y agrega el contrato completo que consume Stager.
3. Todos los `object_key` nuevos son relativos a bucket; size/hash coinciden con MinIO.
4. Un solo deployer publica ambas plataformas y el manifest siempre queda último.
5. Cualquier upload fallido impide manifest PUT y se reintenta sin tocar la versión.
6. Stager integra Linux y Windows desde MinIO real en roots temporales: `staged` y luego `noop`.
7. Bash Linux sigue funcionando con el mismo manifest.
8. `go test ./deployer/...`, vet, shell syntax y cross-builds pasan.
9. No hay secretos ni cambios fuera de Allowed Files.
10. No hubo cutover productivo.

## Rollback

- Antes del cutover no existe rollback host: Bash sigue siendo autoridad.
- Revertir cambios publisher/config y republicar el último manifest legacy conocido.
- No borrar objetos/versiones de MinIO durante el rollback; conservar evidencia hasta cerrar soak.
- Si el manifest aditivo rompe Bash, restaurar `deploy/manifest.json` legacy y reiniciar el único deployer después de baseline/kick controlado.
- Nunca restaurar ni incluir el cambio ajeno de `deployer_screen.log`.

## Evidencia que debe entregar el implementor

- Commit(s) y diff limitado a Allowed Files.
- SPEC/PLAN/TASKS + `VERIFICATION.md` con comandos y resultados.
- Manifest real redacted con versión, paths, sizes y hashes.
- Orden temporal o log de MinIO que demuestre artifacts-before-manifest.
- Árbol de ambos `STAGER_ROOT` temporales y contenido de `CURRENT/PENDING`.
- Evidencia de retry tras fallo de upload.
- Confirmación explícita de que legacy Bash no fue retirado y no hubo producción cutover.

## 📆 Bitácora

- **2026-08-09** — El owner confirmó que Symphony ya corre en Windows y cerró este proyecto. Se ratifica la frontera: Stager prepara la release y emite intención; quiesce/drain y launcher/SCM no forman parte de esta integración.
- **2026-08-09** — Cutover productivo autorizado: Stager Go + bridge en Zeus/Hera/Kronos; release `0.2.40` publicada y aplicada en los tres workers (`staged`→workers active→`noop`). Bash respaldado como `.bash.bak`. Sesión de cierre pedida por el owner.
- **2026-08-09** — F5/G5 cerrada en Zeus: bucket aislado `stager-publisher-int` con `9.9.9` (5 artefactos antes del manifest). Shadow Stager Go Linux/Windows `staged`→`noop`, hashes OK, corrupción rechazada. Incidente: harness accidental publicó `9.9.10` a `deploy` y Bash lo aplicó en Zeus/Hera; rollback a manifest/`CURRENT` `0.2.39` en Zeus/Hera/Kronos. Tarea puente → Review. Sin cutover intencional.
- **2026-08-08** — Proyecto creado como handoff implementable. Discovery focalizado congeló baseline `9612f83`, archivos exactos, contrato manifest, plan F0–F5, tests, rollback y límites. Implementación pendiente; tarea puente queda To Do.
- **2026-08-08** — F0/SPECIFY redactó `FEAT-DEPLOYER-STAGER-PUBLISHER-INTEGRATION/SPEC.md`; `verify-spec` quedó `READY` sin hallazgos. Por gobernanza anti-mezcla no se crearon PLAN/TASKS ni se registró `Spec-Active`: esperan aprobación del owner, incluida D-P01 Linux+Windows como release Symphony completa.
- **2026-08-09** — El owner aprobó la SPEC y D-P01. `SPEC.md` avanzó a `Spec-Active`, la feature se registró en `specs/SPECS.md` y PLAN quedó habilitado. Cierre pedido antes de iniciar PLAN; no se creó `PLAN.md`/`TASKS.md` ni se tocó código productivo.
- **2026-08-09** — F3/G3 completa: configuración CSV `platforms` con fallback singular de flags/JSON/ETCD, `StaticLayout` con allow-list, manifest Go aditivo validado y watcher único configurado para Linux+Windows. No se tocó `watcher.go`, tests existentes ni `deployer_screen.log`. `bash -n run_deployer.sh`, `go test` focalizado de los paquetes modificados y `git diff --check` PASS. F4 queda pendiente para las pruebas nuevas y verificación hermética.
- **2026-08-09** — Por instrucción explícita del owner se completó F0: `PLAN.md` y `TASKS.md` quedaron creados y el gate documental G0 aprobado. El plan congela allow-list Linux/Windows con fallback singular, manifest aditivo, pruebas nuevas sin modificar tests existentes, rollback y G1–G5. F1 puede empezar en `deploy_sqx.sh`; no se tocó código productivo en esta fase.
- **2026-08-09** — F1/G1 completada en `deploy_sqx.sh`: staging único crea `linux-amd64` y `windows-amd64`, construye los cuatro artefactos Linux y `sqx-mt5-worker.exe`, valida los cinco archivos no vacíos y ejecuta el único `mv` final. `bash -n` y `git diff --check` PASS; una release temporal `9999.0.1` confirmó los cinco artefactos y se retiró; un build Windows forzado a fallar no promovió `9999.0.2` ni dejó staging. No se tocó `deployer_screen.log`. Siguiente: F2, manifest aditivo verificable.
- **2026-08-09** — F2/G2 completa: `deploy_release.sh` publica el manifest aditivo desde un descriptor central de cinco artefactos, con size/SHA-256 calculados sobre la release final y validación de resume inmutable. El harness aislado generó un manifest Linux+Windows válido, verificó keys relativas al bucket y rechazó la alteración posterior del binario Windows. No se iniciaron watchers, no se tocó MinIO y el manifest base legacy no recibió metadata ficticia.
- **2026-08-09** — F4/G4 completa: siete archivos nuevos cubren configuración, manifest, pathing, telemetría, resolución del watcher y las invariantes manifest-last/retry con cinco artefactos. Con autorización explícita del owner, la prueba histórica que escribe ETCD real quedó bajo build tag `integration` (sin `Skip`) y se documentó el `TEST_CHANGE_REQUEST.md`; la suite unitaria queda hermética. PASS: `bash -n` de los tres scripts, `go vet ./deployer/...`, `go test -race -cover ./deployer/...`, builds Linux/Windows, `git diff --check` y anti-test-masking. `staticcheck` no estaba instalado. F5 requiere MinIO aislado y Stager real; no hubo cutover ni cambios a `deployer_screen.log`.
- **2026-08-09** — F5 iniciada: la discovery local no encontró `mc`, runtime MinIO local ni variables de integración disponibles. Se requieren el destino aislado y el mecanismo de inyección de credenciales antes de ejecutar publicación, `mc stat/cat`, Stager temporal y shadow Linux. No se publicó ningún objeto ni se tocó producción.
- **2026-08-09** — F5 parcial validada en laboratorio real local: MinIO+ETCD efímeros, bucket aislado y credenciales sólo de runtime. `deploy_sqx.sh 9.9.9` generó Linux+Windows y `update_manifest` produjo el contrato completo; los cinco objetos fueron visibles antes del manifest. Stager real: Linux `staged`→`noop`, Windows `staged`→`noop`; layout, hashes, `CURRENT`/`PENDING` verificados. Una corrupción del binario Linux produjo rechazo por tamaño y preservó el `CURRENT` previo. El `deployer-watcher` real quedó bloqueado durante inicialización después de cargar el caché ETCD incluso con claves temporales disponibles; no se empleó `deploy_release.sh` por su acoplamiento productivo. SSH a Zeus y el endpoint MinIO de clúster no respondieron desde esta máquina, por lo que shadow Linux remoto y G5 completo siguen pendientes. Operación y rollback: `docs/deployment/stager-publisher-integration.md`.

## 🧭 Decisiones

- D-P01 a D-P05 son defaults de implementación; cualquier cambio se registra aquí antes de editar código.
- La documentación canónica del sistema vive en [[stager-app]] y repo Stager; esta nota gobierna sólo la integración publisher Symphony.
- El proyecto termina en MinIO real + Stager roots temporales + shadow Linux. Worker lifecycle continúa en otro proyecto.

## 🔗 Docs / Links

- [[stager-app]]
- [[Stager]]
- [[echo-forge]]
- [[Echo Forge]]
- [[2026-08-08-stager-mvp-boundary-and-activation]]
- [[2026-08-08-stager-deployment-system]] — idea futura; no implementar aquí.
