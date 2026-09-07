---
type: agent_memory
schema_version: 1
scope: project
project: "[[Echo Forge]]"
area: "[[Echo]]"
application: "[[echo-forge]]"
created: 2026-08-02
updated: 2026-08-11
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[echo-forge-workers-shared-access]]"
load_policy: scoped
indexable: true
index_priority: high
tags:
  - kind/agent-memory
  - kind/continuity
  - scope/project
  - area/echo
  - project/echo-forge
  - release/0-2-31
  - plugin/echoforge-robust-run
---

# Continuidad — Deploy diag plugin EchoForgeRobustRun + bump 0.2.31

## Continuidad

## Hecho

Sesión táctica de despliegue. Plugin Java
`sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeRobustRunExporter.java`
modificado con 20 `System.out.println("[diag] ...")` para diagnosticar por qué
`setParameters` no muta variables en WFM (`+157 / -29` líneas, 17696 bytes).

Flujo end-to-end OK:

1. Compilación local simulator OK (58 archivos, `EchoForgeRobustRunExporter.class` = 13175 bytes).
2. `scp` del `.java` a los 3 workers (`Zeus .101`, `Hera .111`, `Kronos .121`)
   vía `sshpass` con user `kor / <keychain:agents.echo-forge.workers/kor>`. Backups del viejo (11397 bytes)
   dejados in-place como `EchoForgeRobustRunExporter.java.bak.20260803T0052{58,59,01}Z`.
   SHA256 verificado en los 3 = `fb151aea290f6413b68031c36ca1882149b7e1fb6ba17d676a417672fb1a37c2`.
3. `./deploy_sqx.sh 0.2.31` OK. `manifest.json` actualizado con `jq` a v0.2.31
   (SHA256 `ac145a871fbf6b8d3bb0eb1f086af22f0b1926a7a3310ae5b8acbfc7489f2896`).
4. `./deploy_release.sh 0.2.31` completo OK. Sesiones `deployer` y `watcher`
   activas. MinIO confirmó manifest. Espera 35s. `input/example/config.json`
   bumpeado a `strategy=example_flow_68`. 5 archivos copiados a `input/`.
   Workflow Temporal `sqx-main-00_configs-v1-NDX-H1-L-1785718733` disparado.
   Archivos movidos a `input/processed/20260802_205853_*`.

## Hallazgos clave

### Runtime real confirmado

SQX **regenera** `~/sqx/user/libs/EchoForgeAutomator.jar` al arrancar, a
partir de los `.java` en `~/sqx/user/extend/Snippets/SQ/CustomAnalysis/`.
Por eso NO se copia el JAR al deploy — SQX lo recompila solo contra las libs
reales de Build 142 (no contra stubs). El `.class`/`.jar` local compilado
en simulator sirve sólo como validación, no como artefacto desplegable.

### Release Go fue cosmético

Los binarios `symphony` y `sqx-watcher` en `0.2.31` son idénticos a `0.2.30`
(no hubo cambios Go). El bump sólo sirve como marca de trazabilidad del
deploy del plugin Java. **No aporta valor operacional** — los workers
drenan workflows y reinician sin cambio real en código Go. Documentar para
futuros bumps "Java-only".

### Deployer con OTel caído

`deployer_screen.log` muestra errores recurrentes `connection refused` a
`192.168.31.45:4317` (OpenTelemetry collector). Es ruido preexistente — no
bloquea manifest/trabajos. Métricas y traces del deployer NO se están
exportando.

## Hashes de referencia

| Artefacto | SHA256 |
|---|---|
| `EchoForgeRobustRunExporter.java` (local y los 3 workers) | `fb151aea290f6413b68031c36ca1882149b7e1fb6ba17d676a417672fb1a37c2` |
| `EchoForgeRobustRunExporter.class` (simulator local) | `141df3899ee5cec1cc6c0878a5f47ffc533b789958f794f1ad28fdac839d0936` |
| `EchoForgeAutomator.jar` (simulator local) | `de7c95452a3c69cface611f7769dea4ec3fe92676e2f9a24985895c1e8ce4179` |
| `symphony` Go 0.2.31 | `f19ecc86c27f389fd33deeacd92b1ff9b445112c66a10a9052504933f5f4cbc6` |
| `deploy/manifest.json` v0.2.31 | `ac145a871fbf6b8d3bb0eb1f086af22f0b1926a7a3310ae5b8acbfc7489f2896` |

## Riesgos pendientes

1. **Si SQX no recompila `user/extend/Snippets/...` al arrancar**, el JAR
   viejo sigue cargándose y los `[diag]` no van a salir. Hay que verificar
   empíricamente viendo stdout de SQX en algún worker.

2. **`[diag]` son permanentes hasta que se quiten.** El reporte original
   dice "quitá los [diag] antes de cerrar Etapa 4 (o dejalos una corrida
   más)". Todavía están. Si la corrida en el workflow Temporal actual ya
   dio señal, se pueden apagar.

3. **Bug preexistente en `verify_build.sh`** (falso positivo no
   determinístico por `set -o pipefail` + SIGPIPE en `unzip | grep -q`).
   Mencionado en el reporte original, no se tocó. Fix sugerido:
   `unzip -l ... > /tmp/list && grep -q ... /tmp/list`.

4. **OTel collector en `192.168.31.45:4317` caído.** Sin exportar métricas
   ni traces del deployer. No bloquea flujo, pero impide visibilidad.

5. **Cambios Java sin commit.** `EchoForgeRobustRunExporter.java` (modified)
   y otros archivos del plugin (`trade_lists.go`, `trade_lists_test.go`,
   `EchoForgeRobustRunExporter.java` siguen en `M` en `git status`.

## Próximo para otra IA

1. **Capturar log del workflow Temporal `sqx-main-00_configs-v1-NDX-H1-L-1785718733`**
   corriendo en algún worker. Filtrar `EchoForgeRobustRun\[diag\]` y
   categorizar según las 3 ramas del reporte original:
   - `bestParameters` vacío/nulo → bug en `getBestParameters` (dump lastPeriod).
   - `bestParameters` OK pero `applied=0` → mismatch nombres paramMap vs XML.
   - `bestParameters` OK y `applied>0` pero retester falla → bug más adelante.
2. Una vez identificada la causa raíz, **remover los `[diag]`** del `.java`
   y commitear los cambios (plugin + bump a 0.2.31 + ajustes en Go si los hubo).
3. Resolver el bug preexistente del `verify_build.sh` en un PR aparte.
4. Investigar por qué `192.168.31.45:4317` (OTel) está caído.
5. Revisar el prompt de auditoría generado en esta sesión
   (entregado al usuario en chat) — tiene la lista completa de tareas
   de auditoría a aplicar.

## Archivos tocados (resumen git status)

- `M` `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeRobustRunExporter.java`
- `M` `deploy/manifest.json`
- `M` `input/example/config.json` (strategy `example_flow_67` → `example_flow_68`)
- `M` `sqx/adapters/storage-minio/trade_lists.go` (no relacionado con este deploy)
- `M` `sqx/adapters/storage-minio/trade_lists_test.go` (idem)
- `??` `deploy/0.2.23/` … `deploy/0.2.31/` (artefactos no commiteados)
- `??` `sqx/exporter-plugin/target/` (build output, no se commitea)
- `??` `input/processed/20260802_205853_*` (workflow ya procesado)

## Señales de carga

- Cargar al retomar el deploy `0.2.31`, diagnosticar `EchoForgeRobustRun[diag]` o revisar divergencias entre Zeus/Hera/Kronos.
- Para acceso remoto desde macOS usar [[echo-forge-workers-shared-access]]; el password no vive en esta memoria.
