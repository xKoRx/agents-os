---
type: runbook
schema_version: 1
scope: application
created: "2026-08-03"
updated: "2026-08-11"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqcli-echoforge-class-not-found-fresh-worker]]"
  - "[[echo-forge-workers-shared-access]]"
aliases:
  - Cómo desplegar EchoForgeAutomator.jar en workers
  - Setup plugin Java SQX
  - sqx/scripts/setup_echoforge_projects.sh
confidence: high
source_session: "2026-08-03-echo-forge-robust-run-audit-deploy-0-2-31"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/runbook
  - project/echo-forge
  - project/echoforge
  - scope/application
  - tool/strategyquant
---

# Despliegue del plugin Java EchoForge en workers Symphony

> Procedimiento canónico y único para que un cambio en
> `sqx/exporter-plugin/src/SQ/CustomAnalysis/*.java` (p.ej. el fix de
> `setParameters` con `[diag]`) llegue a ser cargado por SQX Build 142 en los
> workers del cluster (Zeus / Hera / Kronos).

%% Routing: area/project/application/entities/related usan links canónicos. %%

## Propósito

- Desplegar el plugin Java EchoForge en Zeus, Hera y Kronos usando el acceso común `echo-forge-worker` sin repetir la contraseña en comandos o documentación.

## Por qué `scp` del `.java` no es suficiente

Copiar el archivo `.java` a
`/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/EchoForgeRobustRunExporter.java`
en el worker **no** hace que SQX lo cargue. SQX Build 142 compila ese snippet
solo al iniciar la GUI desde la máquina donde corre; en modo headless o entre
restarts largos, el bytecode activo se sirve desde
`/home/kor/sqx/user/libs/EchoForgeAutomator.jar`, que se mantiene inalterado.

Verificado el 2026-08-03 vía `sshpass` a los 3 workers:

| Worker | `.java` `user/extend/...` SHA | JAR `user/libs/EchoForgeAutomator.jar` SHA | Fecha JAR |
|---|---|---|---|
| Zeus (101) | `fb151aea…` (matchea local) | sin cambios | `2026-07-31 18:30` |
| Hera (111) | `fb151aea…` | `b8b9fbf12c81e017…` (stale) | `2026-07-31 18:30:03` |
| Kronos (121) | `fb151aea…` | `b8b9fbf1…` (stale) | `2026-07-31 18:30:04` |

JAR nuevo compilado en local:
`sq/exporter-plugin/target/EchoForgeAutomator.jar` = SHA
`de7c95452a3c69cface611f7769dea4ec3fe92676e2f9a24985895c1e8ce4179` (143655 bytes).

Diferencia: +2295 bytes consistente con el `+157 / -29` líneas del diff.

## Procedimiento

### 1. Compilar contra la SDK real de SQX (no simulator)

```bash
cd sqx/exporter-plugin
SQX_DIR=/home/kor/sqx INSTALL=1 ./build.sh
```

Esto usa `javac` con el `CP` apuntando a
`${SQX_DIR}/internal/libs/SQTradingLib.jar` y compañía (ver `build.sh` L41-42).
Produce `target/EchoForgeAutomator.jar` (143655 bytes aprox.) y **lo copia
directamente a `${SQX_DIR}/user/libs/`** gracias a `INSTALL=1`.

> ⚠️ Si se omite `SQX_DIR`, `build.sh` cae a modo simulator (compila contra
> stubs de `test-support/`), útil para CI, inútil para producción.

### 2. Empujar el JAR y los proyectos preinstalados a cada worker

`sqx/scripts/setup_echoforge_projects.sh` automatiza todo esto. Tiene 3 pasos
(canónicos, NO modificar):

1. Sube el JAR local a `${SQX_DIR}/user/libs/EchoForgeAutomator.jar`.
2. Crea (o actualiza) `user/projects/EchoForge{RobustRun,Overview,WFM,MT5,TradeList}Exporter/`
   con su `project.cfx` y `CustomAnalysis-Task1.xml` (referenciando
   `__PLUGIN_CLASS__` que se reemplaza con el nombre real).
3. Verifica con `ls -la` que todo quedó donde corresponde.

```bash
echo-forge-worker setup-projects zeus
echo-forge-worker setup-projects hera
echo-forge-worker setup-projects kronos
```

Pre-requisito: SSH keyless entre las 3 máquinas (o se pasa password).

### 3. Reiniciar la GUI de SQX (o ejecutar la cache pre-warm)

SQX Build 142 carga los `.class` desde
`/home/kor/sqx/internal/tmp/compiled/`, NO desde `user/libs/` directamente.
Para forzar que el JAR nuevo llegue al classpath:

**Opción A** (preferida, producción): reiniciar la GUI SQX en cada worker.
SQX extrae automáticamente los `.class` al directorio `compiled/` durante el
arranque, siempre que el JAR sea legible+y escribible (modo `0664`).

**Opción B** (headless, post-fix): ejecutar manualmente el procedimiento
documentado en `sqcli-echoforge-class-not-found-fresh-worker.md`:

```bash
JAR=/home/kor/sqx/user/libs/EchoForgeAutomator.jar
chmod 0664 "$JAR"
mkdir -p /home/kor/sqx/internal/tmp/compiled
cd /home/kor/sqx/internal/tmp/compiled
unzip -oq "$JAR"
```

## Validación

### 4. Verificar empíricamente

En cualquier worker, después del restart:

```bash
echo-forge-worker ssh hera \
  'shasum -a 256 /home/kor/sqx/user/libs/EchoForgeAutomator.jar \
            /home/kor/sqx/internal/tmp/compiled/SQ/CustomAnalysis/EchoForgeRobustRunExporter.class'
```

El SHA del `.class` extraído debe coincidir con el del JAR local. Si no,
repetir paso 3.

## Anti-patrones detectados

| Anti-patrón | Consecuencia |
|---|---|
| Copiar `.java` con `scp` a `user/extend/Snippets/` y dar por desplegado | SQX no recompila; JAR y `internal/tmp/compiled/` siguen stale. Bug "no se arregla" sin importar cuántas veces se copie. |
| Compilar con `./build.sh` sin `SQX_DIR=...` (modo simulator) | El bytecode lleva stubs en lugar de la SDK real de SQX; crashea al primer import_metadata. |
| Subir solo el `.java` y confiar en hot-reload de SQX | SQX Build 142 no hace hot-reload de `CustomAnalysis`-class snippets. Solo recompila al reinicio. |
| Confiar en `setup_echoforge_projects.sh` sin reiniciar después | El JAR nuevo queda en `user/libs/` pero `internal/tmp/compiled/` conserva el viejo hasta el próximo restart. |

## Evidencia

- Sesión: [2026-08-03-echo-forge-robust-run-audit-deploy-0-2-31](../journal/sessions/2026-08-03-echo-forge-robust-run-audit-deploy-0-2-31-summary.md) (a crear).
- Reporte de auditoría completo en chat.
- Workflow Temporal disparado sin efecto: `sqx-main-00_configs-v1-NDX-H1-L-1785718733` (run `019fc521-7bba-7e6e-afb9-ecffc33ba548`).
- Releaser companion: `[[sqcli-echoforge-class-not-found-fresh-worker]]` documenta la mecánica interna de extracción al `compiled/`.
