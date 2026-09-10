---
type: decision
scope: application
created: 2026-08-10
updated: 2026-08-10
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager]]"
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-08-stager-mvp-boundary-and-activation]]"
  - "[[Stager - Symphony Publisher Integration]]"
aliases:
  - Stager durable activation boundary
  - Stager product lifecycle decision
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - area/echo
  - app/stager
  - tech/deployment
  - scope/application
---

# Stager product boundary and durable activation

## Contexto

- El MVP [[Stager]] probó staging verificado Linux/Windows con `PENDING.next → CURRENT → PENDING` y dejó drain/supervisión fuera del core.
- El cutover Symphony `0.2.40` necesitó un wrapper no versionado que proyecta `current`, permisos y un `PENDING` legacy.
- Un `PENDING` canónico sticky puede redispararse en ticks `noop`; filtrar sólo por `result=staged` evita el loop normal, pero pierde la señal si el wrapper cae después de activar y antes de proyectar.

## Decisión

- Stager evoluciona como **producto** para poseer staging, activación durable, runtime adapters, packaging y compatibilidad legacy; el staging core permanece application-agnostic.
- Cada activación usa identidad, fases recuperables y acknowledgement. `noop` puede recuperar una transición incompleta, pero no republica una activación committed.
- El hotfix F0 usa un receipt de proyección `prepared|committed` y entrega at-least-once: elimina el redisparo normal por `noop`, pero puede duplicar tras crash entre replace legacy y commit del receipt. No promete exactly-once sin acknowledgement; el contrato completo y sus gates viven en `repo: stager`, `specs/STAGER-DEPLOYMENT-LIFECYCLE/SPEC.md`.
- El manifest remoto describe releases; el target config local describe root, supervisor, timeouts y projections.
- Linux y Windows comparten state machine/garantías mediante adapters systemd/SCM. La app sólo debe cumplir shutdown y health estándar.
- La implementación se gobierna en [[Stager - Cross-Platform Deployment Lifecycle]].

## Rationale

- `CURRENT` y una versión no distinguen estado durable, evento entregado y evento consumido.
- Llevar lifecycle host a Stager elimina scripts por aplicación sin importar Symphony, Temporal o MT5 al core.
- Shutdown/health no puede inferirse externamente; exigir el contrato estándar es la mínima cooperación necesaria para preservar trabajo activo.

## Consecuencias

- [[2026-08-08-stager-mvp-boundary-and-activation]] sigue explicando el MVP, pero su congelamiento de estados deja de gobernar la evolución productiva.
- `PENDING`, `current` y `symphony-stager-go` pasan a ser compatibilidad transitoria con retiro gateado.
- Stager conserva ejecución one-shot para reconciliar releases; un runtime/launcher estable separado gobierna el proceso y confirma `RUNNING`.
- No se promueven control plane, DB, fleet scopes, auto-rollback ni nuevas artifact sources.

## Alternativas descartadas

- Corregir sólo el wrapper con `if staged`: no cubre crash entre activación y projection.
- Introducir paths Symphony o drain Temporal en el core: rompe independencia y portabilidad.
- Exigir cero cooperación de la app: sólo permite terminación ciega, no drain seguro.
- Convertir Stager completo en daemon/control plane: excede la evidencia y el problema actual.
