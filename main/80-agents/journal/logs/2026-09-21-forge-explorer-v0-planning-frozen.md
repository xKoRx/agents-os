# Change Log — 2026-09-21: Forge Explorer v0 planning frozen

## Contexto

Mandato TOP Forge Explorer v0: preparar un único paquete de desarrollo para visualizar los resultados de Echo Forge (HOME/CAMPAIGN/RUN/STRATEGY/RELEASE), LOCAL y READ-ONLY, reutilizando los contratos F-05-I existentes sin duplicar SQL, sin segunda autoridad y sin tocar el carril de certificación (CERT-F05-01 PASS / CERT-F05-02 en curso quedan como contexto). No ejecutar certificaciones, no desplegar, no rediseñar Factory V2.

## Cambios

- Repo `xKoRx/symphony` (fuera del vault): baseline resuelto con `git fetch` — `origin/codex/f05-release-prep` == `745bc8b94e1f6148ddc16c02eb86a755088c2666` (release `0.2.105`, CERT-F05-01 PASS; `origin/master` `0b9742b` ancestro verificado). Branch nueva `codex/forge-explorer-v0` desde el SHA exacto + worktree independiente `/home/kor/aranea/work/forge-explorer-20260921/symphony`; commit docs-only `cc36c39` con `specs/FEAT-FORGE-EXPLORER-V0/`: SPEC.md v1.0.0 FROZEN (qué es/no es; decisiones D1–D7: paquete nuevo `sqx/cmd/forge-explorer` sólo stdlib, HTML server-rendered en loopback, exec de `sqx-flowkit` con allowlist cerrada de los 6 comandos read, `push-output` excluido por guard, mapping exec→render fail-closed, loopback-only/GET-only sin auth/CORS, cursor `next_cursor` opaco en pass-through; contrato por pantalla con semántica de vacío y error frozen; allowed files = sólo el directorio nuevo; gates con deps-only-stdlib y regresión de flowkit/forge/releasematrix; invariantes y STOP), PLAN.md (EX0…EX6 pequeños con objective/tests/done), NORMAL-PROMPT.md (mandato único autónomo). Push FF verificado (branch nueva en origin).
- Vault: nota nueva `10-projects/Echo/agentes/Echo Forge — Forge Explorer v0.md` materializada vía `materialize_schema_note.py` y llenada (owner agent, parent Factory V2 Completion, tablero EX0…EX6, bitácora, decisiones); `Echo Forge — Factory V2 Completion.md` actualizada por delta (subproyectos con el hijo, tarea en tablero, Docs/Links, bitácora 2026-09-21).
- Registro de ejecución: `80-agents/journal/agent-runs/2026-09-21-zcode-glm-5.3-flash-forge-explorer-v0-planning.md`.

## Verificación

- Baseline y ancestry verificados contra repos reales post-fetch (`rev-parse` local==origin; `merge-base --is-ancestor` master→baseline).
- Superficie F-05-I confirmada en source @ `745bc8b`: `sqx/cmd/sqx-flowkit/inspect.go`+`main.go` (6 comandos read, exit 0/2/4/10/50, stderr `<code>:<kind>:<mensaje>`, `release-matrix` cero DI, `latest` rechazado pre-boot), `sqx/core/forge/inspect.go` (shapes), refs UUID por `domain.Parse*Ref`; release matrix vigente 17×6 con veredictos CERT-F04-01/02/03 y CERT-E04-01 registrados.
- Inexistencia de frontend/HTTP en la ruta inspect verificada (los matches de grep eran falsos positivos de regex `gin.`/`echo.New` sobre `engine.`/`errors.New`); el boundary §7 de `f05-read-surface.md` sanciona explícitamente un wrapper local de los mismos read services.
- Cero escrituras a infraestructura; contratos F-05-I y `docs/echo-forge/**` sin modificar; campaña CERT-F05-02 no observada ni alterada; PHYSICAL CERTIFICATION NOT RUN.

## No-tocados

- Código de `xKoRx/symphony` (sólo docs specs en rama nueva), `codex/f05-release-prep`, master, worktrees ajenos, `internal/di`, `deploy/`, migraciones, `release-matrix.json`: sin intervención. F-01…F-05-I no reabiertos. Carril CERT (CERT-F04-*, CERT-E04-01, CERT-F05-01/02/03) intocado. Defectos abiertos de otros carriles intactos.
