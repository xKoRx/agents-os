---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[BTG-PLAN]]"
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
  - "[[2026-10-06-codex-gpt-6-luna-btg-s01-execution]]"
aliases: []
tags:
  - kind/doc
  - project/echo-futures
  - action/backtest
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 Real History Execution

## Propósito

Registrar el resultado atribuible de BTG-S01 sobre el candidato integrado y dejar la ejecución del histórico real lista para continuar apenas el Owner copie los originales a un directorio legible.

## Contenido

### Estado

`BLOCKED_EXTERNAL`: no se ejecutó un backtest histórico, no se emitió PnL y no se afirma cobertura de ningún horizonte. El origen designado en Daedalus devuelve `Permission denied` para el usuario `kor`; la inspección POSIX muestra que el directorio padre sólo permite atravesarlo a `hermes-ops`. El inventario vivo de perfiles SSH MCP tampoco contiene Daedalus/Hermes. No se intentó cambiar grupos, ACL, sudo, capabilities ni políticas. El Owner solicitó copiar los 13 archivos originales a un destino propiedad de `kor`; la preparación local ya existe y el smoke debe iniciar al verificarse esa copia.

### Candidato y CLI

Se preservó sin cambios el candidato `xKoRx/echo` `codex/btg-s01-cli-cursor-once-reviewed` en `fb210ac4afeab2315aaa3c424f287c2d9db5a7b3`; source worktree limpio al compilar. El CLI nativo compiló offline con el workspace Go explícito, `GOPROXY=off`, `GOSUMDB=off`, `GOFLAGS=-mod=readonly`; `echo-backtest --help` confirmó `prepare-functional-nt`, `run` con `--nt-source-config` y `reproduce` en proceso aparte. SHA256 del binario: `5a20ed5c34fa6bfb0e898aa1e39021bd2dcf1865a8fc93ef394964d538c2e945`; versión Go observada: `go1.27.1 linux/amd64`.

### Preparación de la ejecución

Los comandos, evidencia exacta de la denegación, esquema y plantillas explícitamente no reales quedaron en `xKoRx/echo:reports/real-history-execution/` del workspace BTG-S01. La carpeta de entrada de originales está preparada. El descriptor final debe derivarse de los trece originales: el mapping de contrato combina la secuencia trimestral NQ expresamente provista por el Owner con filenames y contenido verificados. Corpus ID/version/durable ref pueden asignarse de forma técnica y trazable; no se exige que el Owner entregue hashes adicionales. Los hashes completos de las copias locales se verificarán al recibirlas; los hashes físicos del origen quedarán expresamente no verificados porque la identidad `kor` no puede leer el directorio original. El horizonte, fechas de warm-up y ventana operada se seleccionarán autónomamente dentro de la cobertura suministrada por el Owner; no se presume que haya tres años disponibles. Las plantillas no son manifests ejecutables.

El siguiente orden queda preparado: inventariar nombres/bytes/SHA256 de los originales y comprobarlos contra la copia del Owner; adjudicar un mapping explícito para el smoke de un stream; materializar la entrada del perfil congelado; correr varios días posteriores al warm-up; investigar readiness/accounting ante una salida sin operaciones; medir costo del smoke; luego decidir cobertura longitudinal y finalmente reproducir el artefacto en proceso fresco. Un outcome de mercado negativo sería un resultado válido, pero todavía no existe observación.

El perfil de evaluación especificado para S01 permanece `BTG_FUNCTIONAL_NQ_EVAL_V1` con S2_H4_TREND_BB_PULLBACK_V1 y GerardMM EVALUATION. Este registro no certifica esa configuración contra bytes históricos, identidad de estrategia/productor ni completitud longitudinal. Campaña, retiros, optimización, FUNDED y ejecución real quedan fuera de la evidencia de este shot.

## Fuentes

- `xKoRx/echo` — branch `codex/btg-s01-cli-cursor-once-reviewed`, commit `fb210ac4afeab2315aaa3c424f287c2d9db5a7b3`; `v3/backtester/cmd/echo-backtest/` y build local documentado en `reports/real-history-execution/README.md`.
- [[BTG-PLAN]] — autoridad del mandato BTG-S01 y condición de evidencia histórica auténtica.
- [[Echo Futures — BT-S01 Backtester V1 Design]] — contrato de ejecución y artefactos.
- [[Echo + Echo Forge — Environment Contract]] — selección de ambiente, target y autoridad de acceso Aranea.
