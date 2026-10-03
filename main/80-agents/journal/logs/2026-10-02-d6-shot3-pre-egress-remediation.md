# Change Log — 2026-10-02 — D6 Shot 3 pre-egress remediation (F-S2-01..10 PASS)

- **Fecha:** 2026-10-02
- **Entidad:** [[Echo Futures]]
- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/d6-shot3-20261002/D6-SHOT3-PRE-EGRESS-REMEDIATION.md` (nuevo: artefacto canónico de la remediación — STATUS/ROOT CAUSE/CHANGE/TEST/EVIDENCE/SHA por finding, cobertura, shadow-compile, handoff)
  - `10-projects/Echo Futures/Echo Futures.md` (nueva entrada de bitácora D6 Shot 3 + estado del proyecto actualizado)

## Motivo

- Encargo Shot 3 (fase pre-egress) del plan D6: cerrar los 10 findings aceptados del Shot 2 (`D6_SHOT2_ADVERSARIAL = REMEDIATION_REQUIRED`) en software/config y dejar el candidato listo para el gate físico del Owner. Sin ladder físico.

## Resolución aplicada

- `D6_SHOT3_REMEDIATION = READY_FOR_OWNER_PHYSICAL_EGRESS_GATE` — 10/10 findings PASS, 0 residuales. Repo `xKoRx/echo` `feature/d6-shot1-execution-vertical`: baseline `0e9741a5` → **`40102ea5`** (10 commits FF, push verificado `origin == HEAD`).
- F-S2-01/04: reconnect del AddOn de ejecución = nueva sesión por conexión (seq coherente) + fencing de sesión activa en ambas capas (server cierra la conexión supersedada; adapter rechaza frames de sesión no-activa).
- F-S2-02/03/08: freshness LIVE-only explícito (`SetRunMode` desde el runtime), timer checkpointed de re-evaluación por silencio (periodo = mitad del bound), guard de `event_ts` futuro con skew config (5s default, veneno contado sin clamp), frontier re-anclado en source switch y barrier con invalidación; BACKTEST/EXACT_REPLAY sirven el sentinel `""` D5 sin timers (invarianza testeada con salto de reloj).
- F-S2-05: ETCD DEV `binding/day-boundary-tz = America/Chicago` (read-back doble: writer + MCP RO; hermanas intactas); loader default Chicago + `LoadLocation` fail-closed; DST 2026 testeado.
- F-S2-06: bounded evidence repair first-party (2 artículos oficiales, verbatim en SourceRefs): el basis del DLL es el balance de inicio del día ⇒ **basis corregido `INITIAL_BALANCE → PREV_DAY_CLOSE`** (la fuente CONTRADIJO la implementación; config-act con provenance); verbatim consistency "30% or more" CONFIRMA el boundary `>=` sin cambio semántico; 7 SourceRefs; guard 16 mutaciones.
- F-S2-07: `Min5mPerH4Region` (default 8) — presencia ≠ completitud; corpus esparso 1-bucket/región ⇒ `WARMUP_INCOMPLETE` por Validate y por plan; corpora de fidelidad S09 declaran densidad explícita.
- F-S2-09: ELF 33.4MB des-trackeado + `.gitignore` (sin rewrite). F-S2-10: G-EGRESS-0 automatizado (4 tests failing-closed con auto-chequeo del detector).
- Hallazgo de la regresión completa: el decay F-S2-02 marcó STALE un stream con 60s sin hechos y MM denegó correctamente el new risk del rollover MKT07 (fail-closed congelado §4.2, verificado por bisect hasta `AnalyticalReady`); el escenario del test ajustado para modelar feed vivo — producto intacto.

## Validación

- Suites `go test -race -count=1` verdes sobre el SHA final: bridge 15 pkgs, sdk futures, core functions+futuresruntime+config/futures+futuresvertical (`-timeout 30m`, 1345s). Cobertura changed-logic (BASE `0e9741a5`, script aceptado): **raw 135/137 = 98.5% ≥ 95%** sin exclusiones (2 statements canónicos documentados). Shadow-compile físico NT 8.1.8.3: ambos AddOns 0 errores (feed byte-idéntico a Shot 1; execution `b2a29a36…` con 3 warnings preexistentes).
- `PHYSICAL_EGRESS = DISABLED`; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`; AddOn ejecución staged no instalado; única mutación ETCD DEV = la clave del binding; master y PROD intocados. OD-D6-1 NO solicitado.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, tokens, rutas de secretos ni credenciales.

## Rollback

- `git reset` FF a `0e9741a5` en el branch (push update --force con acuerdo del Manager) + revert de la entrada de bitácora + borrado del artefacto `d6-shot3-20261002/` + re-escritura de la clave ETCD `day-boundary-tz` a `America/New_York`. El candidato Shot 1/Shot 2 no depende del delta.
