%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `80-agents/memory/public/decision/symphony/2026-09-03-echo-forge-release-0288-cancel-smoke-certified.md` (nueva)
  - `80-agents/memory/public/known-error/symphony/2026-09-03-orphan-mt5-after-cancel.md` (resolución RESOLVED / PHYSICALLY_CERTIFIED con evidencia 0.2.88)
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (checkpoint append-only de la sesión)
  - `80-agents/journal/agent-runs/2026-09-03-zcode-glm-echo-forge-release-0288-release-only-cancel-smoke.md` (nueva)
  - `80-agents/journal/feedback/system-1/2026-09-03-echo-forge-release-0288-cancel-smoke-session-feedback.md` (nueva, pedido explícito del owner)
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` (delta de continuidad)

## Motivo

- Cierre de `ECHO-FORGE-RELEASE-0.2.88-RELEASE-ONLY-AND-MT5-CANCEL-SMOKE-NORMAL` (PASS / CLOSED): release 0.2.88 publicada `--release-only` con aislamiento de input probado, flota 4/4, smoke de cancelación MT5 físicamente PASS (drain 14s sin taskkill, cero huérfanos), replay ×2 sin no-determinismo, ORPHAN resuelto y lifecycle MT5 congelado.

## Fuentes usadas

- Runbooks symphony (release-certification, prod-probe, worker-runtime-proof, workers-shared-access) y decisiones 2026-09-03 previas (deploy-release-only, mt5-artifact-timeout-authority).

## Resolución aplicada

- Evidencia material persistida en la decisión canónica y el checkpoint; NEXT EXACT `ECHO-FORGE-C3-LEAN-RECERT-DESIGN-TOP`.

## Validación

- release-authority final CONSISTENT/EXACT_MATCH 0.2.88; cero 0.2.89; cero workflows abiertos; dirty foráneo del repo idéntico al preflight; herramientas scratch y worktree de replay eliminados.

## Compartibilidad

- **Scope:** project (Echo Forge)
- **Redacción revisión:** sin secretos; credenciales no mencionadas; IDs y hashes son referencias operacionales.

## Rollback

- No aplica (notas); el estado físico de producción 0.2.88 queda como release vigente.
