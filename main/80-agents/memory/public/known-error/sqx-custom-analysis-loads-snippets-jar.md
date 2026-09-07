---
type: known_error
schema_version: 1
scope: application
created: 2026-08-15
updated: 2026-08-23
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-08-15-echo-forge-mt5-mmlots-session-feedback]]"
aliases:
  - Snippets.jar plugin SQX
  - EchoForgeAutomator.jar no carga
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
---

# SQX Custom Analysis carga Snippets.jar

## Síntoma

- Tras copiar `EchoForgeAutomator.jar` a `user/libs/`, `sqcli -project action=start name=EchoForgeMT5Exporter` sigue imprimiendo el mensaje viejo y el `.mq5` conserva `mmLots=0`.

## Causa

- El classpath headless de SQX Build 142 carga Custom Analysis desde `internal/libs/Snippets.jar` (y el source en `user/extend/Snippets/`), no desde `user/libs/EchoForgeAutomator.jar`.

## Impacto

- Un “deploy” del JAR de packaging no cambia el export real; los HTM siguen vacíos por volumen 0.

## Detección

- El log debe contener `MT5 code generated from` y un path `.sqx`; si dice `generated successfully` sin `from`, está el class viejo.
- `unzip -l internal/libs/Snippets.jar | grep EchoForgeMT5Exporter` y el tamaño/fecha del `.class`.

## Mitigación

- Compilar contra `SQX_DIR` y reemplazar sólo `SQ/CustomAnalysis/EchoForgeMT5Exporter.class` dentro de `internal/libs/Snippets.jar` con `jar uf`.
- Copiar también el `.java` a `user/extend/Snippets/SQ/CustomAnalysis/`.
- Canary: re-exportar un `.sqx` conocido y afirmar `input double mmLots = 0.1`.

## Evidencia

- Canary Zeus 2026-08-15: primer export post-`user/libs` → `mmLots=0`; tras parche de `Snippets.jar` → `mmLots=0.1` desde el `.sqx` de input.
- Reconfirmado 2026-08-23 (WFM Attempt 12): `ClassPathInspector` URLClassLoader carga `internal/libs/Snippets.jar` primero y `user/libs/EchoForgeAutomator.jar` segundo; el bytecode stale de `EchoForgeWFMExporter` en `Snippets.jar` omitía `schema_version`/`producer_version`; el JAR de packaging también estaba stale y no ganaba precedencia. Alignment quirúrgico de la class WFM + canary físico en Zeus/Hera/Kronos.
