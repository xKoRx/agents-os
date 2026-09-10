---
type: known_error
scope: application
created: "2026-07-22"
updated: "2026-08-03"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqcli-builder-existing-portfolio-databank-unresolved]]"
aliases:
  - EchoForgeOverviewExporter class not found
  - Class with name 'EchoForgeOverviewExporter' doesn't exist
  - SQX plugin no carga en worker limpio
confidence: high
source_session: "2026-07-22-symphony-kronos-builder-failures"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/known-error
  - project/echo-forge
  - project/echoforge
  - scope/application
  - tool/strategyquant
---
# StrategyQuant CLI — EchoForge plugin class no encontrada en worker fresco

> Error que aparece en `02_optimize_wfm` (sub-flow `import_metadata`) cuando
> el worker no tiene el bytecode del plugin EchoForge precacheado en disco.

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- En el log SQX se observa:
  ```
  Error: Cannot load 'Custom analysis' settings.
  Class with name 'EchoForgeOverviewExporter' doesn't exist!, in setting: CustomAnalysis
  ```
  (también `EchoForgeWFMExporter`, `EchoForgeMT5Exporter`,
  `EchoForgeRobustRunExporter`, según el `CustomAnalysis` configurado).
- Provoca reintentos de la actividad en Temporal y eventual `TIMEOUT`
  (`sqcli` killed por SO_timeout) cuando el sub-flow `import_metadata`
  usa uno de estos exporters.

## Causa raíz (dos factores que se acumulan)

`SQX` no carga el JAR `EchoForgeAutomator.jar` directamente desde
`~/sqx/user/libs/`; en su lugar, en el arranque **extrae los `.class` a
`~/sqx/internal/tmp/compiled/`** y los referencia desde ese classpath.
El nombre de la carpeta `compiled` es engañoso: no es bytecode compilado,
es una **copia del classpath**. Esto fue verificado durante esta sesión:
los `.class` de `compiled/SQ/CustomAnalysis/EchoForgeOverviewExporter.class`
en Hera tienen el mismo SHA256 (`4138c3e2b058ecae5a7aff0dcae7cb2ae3e66b5a203aaed1bdf8a9b6ce6e2aa7`)
que los del JAR.

Para que esa extracción funcione, ambos deben cumplirse:

1. **El JAR debe ser legible y escribible por SQX.**
   SQX no necesita escribir el JAR, pero el script de arranque escribe
   `.bak` y temporales antes de aceptar una sustitución. Si los permisos
   del JAR son `0644` (`rw-r--r--`), el arranque **abre el proceso de SQX
   antes de que se complete la copia del classpath**, y el `tmp/compiled/`
   queda en estado inconsistente.

2. **Debe existir la carpeta `internal/tmp/compiled/` con los `.class`.**
   Si esta carpeta **no existe** o está vacía, SQX no intenta regenerarla
   proactivamente. Solo la crea con éxito si el JAR era escribible al
   momento del arranque. En un worker **limpio o recién provisionado** es
   el caso típico donde se observa `tmp/` y `tmp/compiled/` pero `compiled/`
   queda vacío.

## Por qué Hera / Zeus "pasan" y Kronos no (esta sesión 2026-07-22)

- Hera (estado anterior): JAR `0664`, `tmp/compiled/SQ/CustomAnalysis/` con
  timestamp `2026-07-22 16:59`, contains los 18 `.class` del JAR. Funciona.
- Zeus (estado anterior): JAR `0664`, `tmp/compiled/` **vacía** desde `2026-07-18`. **Aun así Zeus pasa** porque SQX, en su arranque del 2026-07-22 19:47, detectó el JAR escribible y rellenó el cache durante la primera ejecución real del día. `tmp/compiled/` permanece con timestamp antiguo únicamente porque el contenido es el mismo desde entonces.
- Kronos: JAR en `0644` (producido por el deploy de la v0.1.130 al instalar
  en una máquina limpia, probablemente heredado de la pipeline de packaging
  que asume un dígito de ejecución diferente), `tmp/compiled/` no existe
  o está vacía. Resultado: SQX arranca pero no encuentra el classpath, y
  falla con el error Java.

## Mitigación (recomendada)

Para cualquier worker recién provisionado, ejecutar antes del primer build:

```bash
JAR=/home/kor/sqx/user/libs/EchoForgeAutomator.jar
# 1) Permisos esperados por SQX (escribibles para el usuario kor:kor)
chmod 0664 "$JAR"

# 2) Extraer las clases al cache compilado igual que SQX en arranque
mkdir -p /home/kor/sqx/internal/tmp/compiled
cd /home/kor/sqx/internal/tmp/compiled
unzip -oq "$JAR"

# 3) Verificar que el class más crítico quedó copiado
sha256sum SQ/CustomAnalysis/EchoForgeOverviewExporter.class
# Esperado: 4138c3e2b058ecae5a7aff0dcae7cb2ae3e66b5a203aaed1bdf8a9b6ce6e2aa7
```

Para hacerlo a escala, idealmente añadir una `systemd unit` o un `postinst`
del paquete `symphony-worker` que ejecute los 3 comandos durante la
despliegue inicial.

## Solución estructural pendiente

- **Investigar el pipeline de packaging** (`./scripts/build-worker.sh` o
  equivalente) para entender por qué el JAR sale con `0644` en vez de
  `0664` cuando se buildea con el `deploy/manifest.json` versionado.
  Owner pendiente: SDD sobre el packaging del worker.
- **Evaluar promoción del fix a un skill `symphony-worker-bootstrap`**
  en `80-agents/skills/` para que cualquier nuevo worker entre al cluster
  con `internal/tmp/compiled/` ya poblado.

## Detección

- Buscar en `sqx_raw_log` del wf los strings:
  `Cannot load 'Custom analysis' settings` o
  `Class with name 'EchoForge.*' doesn't exist`
- Diagnosticar precedencia con `ls -la /home/kor/sqx/user/libs/EchoForgeAutomator.jar`
  y `ls -la /home/kor/sqx/internal/tmp/compiled/SQ/CustomAnalysis/`.

## Evidencia

- Sesión:
  [2026-07-22-symphony-kronos-builder-failures-and-fixes](../journal/sessions/2026-07-22-symphony-kronos-builder-failures-and-fixes.md)
- WID: `sqx-main-00_configs-v1-NDX-H1-L-1784762810`, paso `02_optimize_wfm/subflow/import_metadata`.
