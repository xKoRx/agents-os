---
type: project
schema_version: 1
owner: me
root: false
status: active
priority: P2
area: "[[Echo]]"
parent: "[[Echo Futures]]"
sprint: 2026-10-18--2026-10-20
start: 2026-10-18
due: 2026-10-20
progress: 70
repo: xKoRx/echo
jira:
prs:
aliases:
  - challenge history 26
tags:
  - kind/project
  - state/in-progress
created: "2026-10-19"
updated: "2026-10-19"
---

# Echo Futures — Challenge History 26 Continuity

## Objetivo

Ejecutar las 26 configuraciones challenge continuas (4 TG, 4 FBC, 3 ORB comparables, 10 MR, 5 ORB nativas) sobre toda la historia física utilizable NQ 2023-10→2026-10 en CHALLENGE_ONLY/CONTINUOUS_V1, auditar con el verificador externo y reportar. Continúa el WIP de GOD pausado 2026-10-18 (`outputs/PAUSA-HANDOFF.md` del workdir del encargo).

## Identidad congelada

- Rama `experiment/challenge-history-20261018` @ `48aaf5f7` (todos los commits pusheados); binario resultados `7d6e5e85…` (build `bbdd2f35`); preparación sellada `b72ff90b…` (13 contratos, 672/785 sesiones elegibles; etiqueta obligatoria `ALL_AVAILABLE_VALID_SESSIONS / PARTIAL_DATA_COVERAGE`).
- Runbook multi-máquina: `v3/backtester/tools/tradesgerard/challenge-history/RUNBOOK-CONTINUIDAD-20261019.md` en la rama (incluye ruta A auditor/cierre y ruta B re-ejecución, con gotchas probados).

## Estado (2026-10-19 22:45)

- **13/26 COMPLETE_RECONCILED**: 12 en r4 (TG×4, FBC×4, ORB×3, MR-01) + MR-03 en r5. FBC-15M +1.013,48 USD (6/26 pases, 23,1%) es la primera positiva; FBC-30M casi break-even. Snapshot ejecutivo en la rama: `verification/history-execution-20261019/RESULTS-SNAPSHOT.md`.
- **13 restantes en vuelo** en r5 (`/srv/echo-work/runs/challenge-history-20261018-r5`, jobs=4, setsid-desacopladas, ETA 20-oct 13:00–17:00): MR-02, MR-04..10, ORB-NATIVE C01–C05. Los 4 estados RUNNING de r4-execution-FULL.json son intentos INTERRUMPIDOS (cierre de app), nunca resultados.
- **Remoto**: release GitHub `challenge-history-20261018-evidence` con r4 (resultados completos+binarios+gates), preparación sellada (dereferenciada) e intentos r3; evidencia r5 la publica la automatización `automation-3979763f` (20-oct 19:00) o el próximo agente.
- Fix de reporting en `f6410404`: snapshots con `orders: null` (nil slice de Go) reventaban el analyzer; null-tolerante + RED→GREEN. No invalida resultados (sólo reporting).

## Próximos pasos

1. Al terminar r5: auditoría incremental (`audit_subset.py` apuntado a r5; reconstruir manifest antes), reporte FULL-ALL 26/26 consolidado de ambas raíces (misma identidad), suplemento descriptivo, conciliación compras=pases+perdidas+pendientes.
2. Actualizar `specs/FEAT-CHALLENGE-HISTORY/VERIFICATION.md` por delta; push de recibos compactos.
3. Reporte final al owner con la tabla de 26 (montos, costo por pase, cobertura); cierre del proyecto.
4. La continuación puede ocurrir en OTRA máquina: usar el RUNBOOK (ruta A) descargando el release.
