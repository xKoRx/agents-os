# change_log — Echo Futures resource-safety incidents + Shot A P150

- date: 2026-09-24
- entity: "[[Echo Futures — D5 Prop Economics]]"
- actor: agent (senior Go simulation engineer)
- gate: D5_RESOURCE_SAFETY_PASS = PASS · D5_TOPSTEP_POLICY_IMPL_A = REVIEW

## Cambios

1. **Incidentes OOM #1/#2 (daedalus, dos reboots) — causa física y reparación.**
   - Forense kernel (`/var/log/syslog` dumps 17:44–19:43): 12 OOMs globales; firma
     `inactive_anon ≈ 67 GiB + pagetables 5.3 GiB + kernel_stack 1.1 GiB`; tabla de
     tareas → swarm de procesos `MainThread` (node/V8) del front Echo v3 en
     `aranea/work/d3-shot3-correction-20260924/echo/v3/front` (hasta 9,141 procesos,
     ~70 GiB anon). echo-futures EXONERADO por tabla del kernel + mediciones propias
     (máx 101 MB RSS en toda la sesión).
   - Episodio #3 capturado en vivo y contenido: SIGTERM a workers
     `esbuild --service` huérfanos (1,565 → 0) y el `vite build` activo murió;
     host 45 → 3.9 GiB usados. Acción owner pendiente: contener el respawn
     vite/esbuild con cgroup propio / eliminar el loop de rebuild.
   - Vector in-repo corregido: `internal/sim/cohort.go` retenía 3 slices O(N)
     (~24 B/cohort medidos) + sort full-retention → reemplazado por
     `resources.QuantileStore` (exacto ≤1e6, histograma arriba); resultados
     idénticos en toda escala certificada; orden RNG intacto; D4 47/47 verde.

2. **Simulation Resource Safety Contract (binding, project-wide).**
   - Nuevo `internal/resources`: Budget/Plan/Guard/RunBatched/WorkerBudget/
     QuantileStore (bounded quantiles + CDF); caps fail-closed via
     `ECHO_FUTURES_MAX_RUNS/MAX_COHORTS/...`; planes de recursos por stderr.
   - Nuevo `scripts/safe-run` + `safe-test/safe-sim/safe-validate`: systemd user
     cgroup (4G/6G/1G/128/400%/3GiB/4) autoverificado dentro del scope,
     FAIL-CLOSED sin fallback ilimitado.
   - Tests de regresión de complejidad: fallan si reaparece O(total_paths).
   - Secciones añadidas a README.md y a la Technical SPEC D5-M1A.

3. **Shot A P150 entregado (REVIEW).** `internal/p150` completo sobre D4
   (`d4f42a4`): engine de política discreta con los estados del dispatch,
   DP exacto (LU por ciclo sobre retícula $50), MC cuenta única sin censura,
   portafolio mensual 5 pipelines (INDEPENDENT/PERFECT_COPY, multi-MLL,
   slots), matriz NDJSON + break-even, CLI `sim p150|p150-matrix|p150-verify`.
   14 fixtures / 23 checks PASS; coverage 96.0%; race verde. Commits
   `321335f`, `1103002`, `1dc1fa6` en `feature/d5-m1a-p150`.

## Archivos

- Vault: planner D5 (bitácora + gates + evidencia), Technical SPEC D5-M1A
  (contrato), este log.
- Repo: ver commits; samples en `scenarios/p150/samples/`, matrices en
  `scenarios/p150/`.

## Métricas antes/después (cohort)

- Viejo: RSS ≈ 24 B × N cohorts (5e9 → ~120 GB, orden del incidente).
- Nuevo: exacto ≤1e6 (84 MB pico medido) → histograma (64 MB @2e6, plateau);
  O(workers×batch + bounded aggregators).
