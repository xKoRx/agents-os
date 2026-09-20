# Change Log — Loom F3: watcher real certificado (G1) + writer experimental G2

**Fecha:** 2026-09-20
**Proyecto:** [[Loom]]
**Tipo:** ejecución de mandato (repo externo `xKoRx/loom`, rama experimental `feature/f3-integration-lab`); cero cambios canónicos del vault salvo esta bitácora + nota de proyecto + agent-run.

## Resumen

Mandato maestro "Real Watcher Integration & End-to-End Experimental Writer" (~8h, sin checkpoints owner): desde la POC F3 endurecida (SECURITY_READY @ `cfa0ebc`, rama `feature/f3-writer-poc @ 593f656`) hasta integración funcional adversarialmente validada sobre fixtures desechables.

## Hechos

- Rama nueva `feature/f3-integration-lab` creada desde la POC (relación POC→v0.6 verificada por merge-base); v0.6 (`36c760c`) congelada e intacta; sin merge; publicada en origin por push normal @ `62943d4`.
- **G1 (watcher real) PASS:** confirmación real por las 5 condiciones del contrato sobre una carga del snapshot publicado; `ContentSHA256` read-only en `internal/index`; abstracción `ConfirmSource` (dirección f3lab→writer, aislamiento de `cmd/loom` intacto); `poc/f3lab` con 12 casos obligatorios + crash SIGKILL; `TxnState`/`TxnStatus` (6 estados del contrato). Los 58 tests de la POC intactos.
- **Auditoría adversarial independiente 3 fases** (arsenal multi-proceso propio en /tmp, revisor ≠ implementador): baseline demostró el defecto de la confirmación simulada; veredicto G1 PASS sobre el SHA integrado (falsas 0/36) con 3 hallazgos (B-F2-01/02 HIGH, B-F2-03 MEDIUM); fase 3 verificó los 6 cierres y los fixes resisten ataques propios → PASS final.
- **Fixes con regresión RED→GREEN:** replay atestigua contenido (post-hash verificado, degradación honesta auditada); identidad de intención journalada + `ErrTxnIntentMismatch` (jamás pisa journal ni reutiliza desenlaces); journal corrupto diagnosticado y fail-closed. Harness R02/R03 corregido a re-envío genuino (expectativa intacta, aceptado por el auditor).
- **G2 experimental PASS:** server HTTP aislado en `poc/f3lab/serve` (mux propio, jamás en cmd/ ni internal/serve), tabla §2 congelada completa con no-mutación verificada, idempotencia estricta por requestId, recuperación tras reinicio, 409 busy real y 503 environment.
- **Gates finales íntegros con evidencia real:** gofmt/gofumpt, vet, suite 9/9 (536 runs), race, crash/recovery, secret scan 0, aislamiento `go list -deps ./cmd/loom` = 0, v0.6 intacta read-only.

## Decisiones

- Nada habilitado en producto: sin flags, sin endpoints en el binario normal, sin tocar el vault real. Los gates G2–G5 siguen pendientes del owner.
- Conflicto de contrato resuelto con el auditor: la estricta por-payload del mandato (§5 G2) se implementó a nivel writer (rechazo de colisión de TxnID vivo) corrigiendo el harness de R02/R03 al re-envío genuino — el auditor validó la corrección como legítima.

## Referencias

- `specs/FEAT-F3-INTEGRATION/RESULTS.md` (rama lab) — resultados completos.
- Evidencia: `poc/f3lab/evidence/{g1-run,g2-run,gates-final}.txt`.
- Nota de proyecto: [[Loom]] §Estado actual (2026-09-20).
