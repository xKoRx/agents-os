---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-CLI-CURSOR-ONCE-REMEDIATION

## Propósito

Preservar el informe del worker con envoltura canónica del vault. Root añadió metadata y secciones requeridas; el informe original íntegro sigue debajo. Original commit `4d5612b958631c08a640a773c8d41e14fd753b49`, SHA256 `ee5a7a5656400abdbe4650ae93520d9fbf01494a7f69e4096d2cdc2f52b57512`; no se alteran resultados ni código.

## Contenido

# BTG-S01-CLI-CURSOR-ONCE-REMEDIATION

**Finding:** F11 LOW — el wrapper CLI conservaba el cursor tras su cierre por EOF y podía reenviar `Close` durante el cleanup después de fallar una re-admisión.

**Estado:** Corregido en `xKoRx/echo` branch `codex/btg-s01-cli-cursor-once`; commit de código/test `15422c2329164a33a76bf63912491168227660b7`. El tip final del branch es `e320fef9e98c514309505771331d831bfda4c4d1` e incluye, sin alterar bytes, la verificación previa F09/F10 preservada desde `a8e85129856b9ff2602e8e230b35b1d20684b927`.

## Reproducción y causa

El probe público válido combina un artefacto sellado CALLER_CONTROLLED con un `--spec` override CLOSED_SPEC. El replay avanza hasta EOF, el driver cierra el cursor subyacente y la re-admisión posterior devuelve `EnqueueControl requires CALLER_CONTROLLED mode`; como la fuente aún retenía el wrapper, el cleanup del error podía invocar un segundo `Close`. La cápsula de evidencia está identificada por SHA256 `74fe84bdca5709a250d9668756f8daed9e77b74b4ac70ca574076dfb896073d7`; el probe `TestReviewerOwnershipPublicValidSealedScriptOverride` registró Close=2, Peek=3 y Next=1 frente a Close=1 esperado, conservando el error original de modo. El log público de re-admisión EOF está identificado por SHA256 `855ed6bd8b283af9164b636b97155027e4dcc54d3bec5c2d51afd32c921c7276`.

El cursor nativo subyacente era idempotente y esta ruta no mostró fuga, divergencia económica ni alteración de causa; F11 es una corrección de ownership exactly-once, no un hallazgo histórico. El arreglo conserva el primer error de cierre y el error original del comando, sin añadir avances ni efectos de Finish.

## Cambio y regresiones

`sequenceCursor.Close` en `v3/backtester/cmd/echo-backtest/run.go` guarda el primer resultado de `inner.Close` bajo `sync.Once` y lo devuelve en llamadas posteriores. La API, `NewRun`, `ResultWriter`, el driver, Strategy/MM y el perfil funcional permanecen fuera de este cambio.

`v3/backtester/cmd/echo-backtest/native_cli_cursor_once_regression_test.go` contiene la regresión del seam EOF+error que falla con dos cierres antes del fix y pasa con uno después, la reproducción pública de un artefacto CALLER sellado con override CLOSED_SPEC, y el caso de cierre durante `Finish` normal. La prueba de error también comprueba que sobrevivan el error de admisión original y la causa del primer cierre.

## Verificación y límites

Pasaron las pruebas dirigidas bajo `go test -race` para F11, los cleanup/cause F09, autenticidad de scope y el pipeline nativo F08; también pasaron `go vet ./cmd/echo-backtest` y `git diff --check`. El método modificado `sequenceCursor.Close` obtuvo 100% de cobertura en el perfil dirigido; la cobertura total del paquete en esa ejecución fue 47.9% y no se interpreta como cobertura de los bloques cambiados.

La evidencia usa fixtures sintéticos. Los 13 originales NT estaban listados y sus endpoints eran legibles, pero la policy SFTP bloqueó la transferencia de los archivos; por ello no hay corrida histórica real, cierre de hallazgos históricos ni aceptación del Owner. No se repitió el full E2E cálido independiente que ya estaba en curso, dado el alcance LOW del fix.

**Contexto funcional vigente:** baseline compartido S2_H4_TREND_BB_PULLBACK_V1 + GerardMM, controles de riesgo uniformes autorizados para esta prueba y scaling NO_ADDS. Este fix no altera señales, economía, perfil, calendarios, datos ni ninguna autorización de trading físico.


## Fuentes

- [[BTG-S01-REAL-GERARD-RESULT]], [[BTG-S01-FINDINGS]] y [[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]].
