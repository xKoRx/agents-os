# HANDOFF — Clutifx Strategy Implementation & Backtest (misión GOD)

Actualizado: 2026-10-25 · Estado: **CLF-Q02 EJECUTADO (catálogo viable completado y gateado; 0 pases ⇒ G5=∅)** · Ejecutor: manager ZCode (GLM-5.3)

## Dónde está el trabajo

- **Código:** `xKoRx/echo`, rama `experiment/clutifx-s01`, worktree `~/go/src/github.com/xKoRx/echo-clf` (base `ae1b09bc` = cierre R03). Commits: `f165ef08` (detectores P2), `1bbd798e` (checkpoint P3a), `710c86a0` (cierre P3a: STR-002+STR-006 sobre el contrato Strategy + factory ModuleCLF + conformance). Sin push, sin merge.
- **Resultados:** run root `~/echo-work/clutifx-backtest/` (checkpoint durable en `checkpoint/CLF-CHECKPOINT.md`).
- **Catálogo (esta carpeta):** STRATEGIES-MASTER, OBJECTIVE-DETECTORS, EXPERIMENT-MATRIX (34 IDs/35 sets), SOURCE-COVERAGE, HEFESTO-BASELINE-AUDIT, CLF-ID-INVENTORY — versión de implementación **RECONSTRUIDA** (el catálogo original no existía físicamente; ver BASELINE-AUDIT §hallazgo).

## Estado por gates

```text
P0 preflight físico        = PASS  (corpus sellado ba6f0985…, R03 cerrado/aislado)
P1 specs regularizadas     = PASS  (GATE P1 en EXPERIMENT-MATRIX)
P2 detectores + causalidad = PASS  (arnés anti-lookahead DST + 2 semanas; 95.4%)
P3a STR-002/STR-006        = PASS  (unit/conformance verdes; E2E motor real EN CURSO)
P3b sesión/refinado/rearme = PENDIENTE
Gate A smoke NQZ6          = EN CURSO (ventana sellada 2026-09-21→2026-10-05; FREQ90 si 0 señales)
Histórico ≤6 motores       = BLOQUEADO hasta congelar versión tras smoke
```

## Cómo continuar (próxima acción verificable)

1. Leer `/home/kor/clf-work/p3/e2e-smoke-report.md` (worker E2E-SMOKE) y `git -C ~/go/src/github.com/xKoRx/echo-clf log --oneline -5`.
2. Si smoke PASS + replay determinista: congelar versión (binario+plan+specs hashes en `checkpoint/`) y despachar el histórico TIER1 (gross R500, CHALLENGE_ONLY+CONTINUOUS_V1, horizonte 2023-10-02→2026-10-06) con supervisor ≤6 motores globales y admisión por RSS/PSI (patrón `r03_supervisor.py`; NUNCA el perfil al-límite de R03).
3. P3b en paralelo tras smoke: STR-001/003/004 (hipótesis de sesión versionadas), STR-005 (overlay), STR-009 (rearme técnico documentado).

## Decisiones de autoridad vigentes

- Mandato Owner 2026-10-24 ("REENCAMINAR") manda sobre la secuencia GOD anterior: DESARROLLAR→TEST→E2E→SMOKE→CONGELAR→HISTÓRICO→MÉTRICAS→CIERRE.
- R03 (`ae1b09bc`, 89/89) = autoridad READ-ONLY de comparación; no reejecutar.
- STR-007/008 BLOCKED_DATA (verificado físicamente: sólo NQ en Hefesto).
- Bases de fuente: biblioteca MKE (1.599 claims; sólo ACTIVE+SUPPORTED consumibles).

## No hacer

- No inventar un producto cartesiano; TIER2 = un eje por vez sobre controles medidos.
- No mezclar MMs como señales distintas; compras en denominador siempre.
- No promover LIVE ni aceptar G4: gates del owner.
