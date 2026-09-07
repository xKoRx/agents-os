---
type: known_error
schema_version: 1
scope: application
created: "2026-07-22"
updated: "2026-08-11"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
application: "[[StrategyQuant X]]"
entities:
  - "[[sqx-instrument-sync]]"
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqcli-builder-existing-portfolio-databank-unresolved]]"
  - "[[sqcli-echoforge-class-not-found-fresh-worker]]"
  - "[[echo-forge-workers-shared-access]]"
aliases:
  - sqx-instrument-sync History-only gap
  - sync_user_data_zeus.sh no detecta símbolos fuera de History
  - XAUUSD_darwinex ausente en Kronos
  - ErrMetadataMissing causado por falta de instrumento
confidence: high
source_session: "2026-07-22-2022-symphony-kronos-sync-instruments-misdiagnosis"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/strategyquant-x
  - app/strategyquantx
  - area/symphony-portal
  - kind/known-error
  - project/symphony
  - scope/application
  - tool/strategyquant
---
# sqx-instrument-sync — gap de verificación: solo cubre History/, no todo user/data

> La skill `sqx-instrument-sync` y el script `sync_user_data_zeus.sh`
> verifican igualdad bit-a-bit **únicamente sobre `~/sqx/user/data/History/`**.
> Divergencias en otras subcarpetas (`Symbols/`, `Datasources/`,
> `tickdata/`, etc.) pasan inadvertidas y producen fallas operativas
> en builders/exporters con síntomas que se confunden con BUG-001.

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Un worker (típicamente Kronos o Hera) falla en `classify_and_rank`
  con `ErrMetadataMissing` non-retryable: `metadata missing for wave`.
- El builder corrió (`All tasks completed` en `sqx_raw_log`) pero no
  escribió documentos en `databank_metadata` para la wave.
- La UI de SQX en el worker afectado muestra el proyecto con
  **"unresolved resources"** o dependencias marcadas como ausentes.
- Ejemplo real 2026-07-22: Kronos reportó `XAUUSD_darwinex` como
  dependencia no creada, presente en Zeus y Hera.

## Causa

Dos capas:

1. **Datos**: el worker afectado no tiene un instrumento/símbolo que
   el proyecto SQX declara como dependencia. SQX no puede generar
   estrategias para un símbolo sin datos, así que el builder produce
   0 resultados y no persiste metadatos.
2. **Herramienta**: `sync_user_data_zeus.sh` replica TODO
   `~/sqx/user/data` con rsync, pero la skill `sqx-instrument-sync`
   solo verifica igualdad con SHA-256 maestro sobre la subcarpeta
   `History/`. La verificación pasa `EQUAL` aunque `Symbols/` u otras
   subcarpetas difieran.

Ubicaciones actuales:

- Skill: `.agents/skills/sqx-instrument-sync/SKILL.md` (repo Symphony).
- Script: `.agents/skills/sqx-instrument-sync/scripts/sync_user_data_zeus.sh`.
- Script remoto: `~/sync_user_data_zeus.sh` en cada worker (copia).

## Detección

Sospechar este gap cuando:

- Un solo worker falla recurrentemente con `ErrMetadataMissing` en
  `classify_and_rank` mientras los otros dos procesan el mismo flujo.
- `rsync -avzn --delete-after --checksum ~/sqx/user/data/ <destino>:...`
  reporta `0 archivos` pero el problema persiste.
- La UI de SQX del worker afectado lista "unresolved resources" o
  dependencias de proyecto marcadas como ausentes.
- Las strategies esperadas (por nombre, ej. `example_flow_22`) no
  aparecen en `forge.databank_metadata` para la wave.

### Diagnóstico diferencial rápido

Antes de concluir BUG-001 (`run_id`), verificar:

```bash
# 1. ¿El builder realmente generó estrategias?
echo-forge-worker ssh <worker> \
  'tail -200 /var/log/symphony/symphony-worker.log | grep -iE "Loaded .* strategies to databank|unresolved|Cannot start project"'

# 2. ¿La skill actual declara EQUAL pero SQX UI muestra faltantes?
#    Comparar árboles manualmente, no solo History/:
for WORKER in zeus hera kronos; do
  echo-forge-worker ssh "$WORKER" \
    'find ~/sqx/user/data -mindepth 1 -maxdepth 3 -type d | sort | wc -l
     ls ~/sqx/user/data/Symbols 2>/dev/null | wc -l
     ls ~/sqx/user/data/Datasources 2>/dev/null | wc -l'
done

# 3. ¿Está el símbolo específico ausente?
for WORKER in zeus hera kronos; do
  echo "=== $WORKER ==="
  echo-forge-worker ssh "$WORKER" \
    'find ~/sqx/user/data -iname "*XAUUSD*" -o -iname "*darwinex*" 2>/dev/null'
done
```

Si los conteos o la lista difieren entre hosts, este es el gap. No
es BUG-001.

## Mitigación

```bash
# Sync manual forzado (ya cubre todo user/data, el problema es de verificación):
echo-forge-worker ssh zeus '~/sync_user_data_zeus.sh'

# Verificación manual completa (no solo History/):
for WORKER in zeus hera kronos; do
  echo-forge-worker ssh "$WORKER" \
    'cd ~/sqx/user/data &&
     find . -type f ! -name "data*.db" ! -name "brokers.version" \
            ! -name "connections.txt" ! -name "group_of_stocks.version" \
            ! -name "*.lock" ! -name "*.tmp" \
            -print0 | sort -z | xargs -0 sha256sum | sha256sum'
done
```

Los tres hashes maestros deben coincidir. Si difieren, aislar por
subcarpeta con el mismo comando pero `cd ~/sqx/user/data/<subcarpeta>`.

## Solución estructural pendiente

Reescribir la skill `sqx-instrument-sync` y el script
`sync_user_data_zeus.sh` para:

1. Verificar bit-a-bit **TODO** `~/sqx/user/data` (con las exclusiones
   runtime de DBs H2/locks), no solo `History/`.
2. Generar manifests deterministas (ruta + tamaño + mtime + SHA-256)
   antes y después del sync.
3. Reportar diffs estructurales legibles: `FAIL_MISSING`,
   `FAIL_EXTRA`, `FAIL_HASH`, `FAIL_SIZE` por subcarpeta.
4. Exigir `--delete --delete-excluded --checksum` en el rsync.
5. Definir `EQUAL` formalmente como "los 3 manifests maestros
   coinciden", no como "rsync reportó 0 transferencias".
6. Subcomandos: `audit`, `sync`, `verify`, `manifest`, `diff`.
7. Lock con `flock` para evitar syncs superpuestos.
8. Códigos de salida que nunca mientan sobre el resultado.

Existe un **prompt maestro** entregado al usuario al cierre de la
sesión `2026-07-22-2022-symphony-kronos-sync-instruments-misdiagnosis`
que detalla los entregables y criterios de aceptación.

## Lección de diagnóstico (también aplicable a otros bugs)

Cuando `classify_and_rank` falla con `ErrMetadataMissing` en un solo
worker, **antes** de culpar a `run_id` o cualquier bug de código,
verificar:

1. ¿El builder realmente escribió algo? (logs SQX, `Loaded N
   strategies to databank`).
2. ¿El proyecto SQX tiene dependencias resueltas en ese worker?
   (UI de SQX, "unresolved resources").
3. ¿Los instrumentos/símbolos del proyecto existen en disco en ese
   worker? (`find ~/sqx/user/data -iname "*SYMBOL*"`).

La raíz operativa (datos) suele estar antes que la raíz de código.

## Evidencia

- Sesión:
  [2026-07-22-2022-symphony-kronos-sync-instruments-misdiagnosis](../../journal/sessions/raw/2026-07-22-2022-symphony-kronos-sync-instruments-misdiagnosis-raw.md)
- WIDs afectados:
  - `sqx-main-00_configs-v1-NDX-H1-L-1784764719`
  - `sqx-main-00_configs-v1-NDX-H1-L-1784762810`
- Símbolo ausente: `XAUUSD_darwinex` (en Kronos, presente en Zeus/Hera).
- Skill con el gap:
  [`sqx-instrument-sync`](../../../../go/src/github.com/xKoRx/symphony/.agents/skills/sqx-instrument-sync/SKILL.md)
  (repo Symphony, ruta referencial).
