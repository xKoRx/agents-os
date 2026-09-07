---
type: idea
status: seed
priority: P3
area: "[[Echo]]"
project: "[[Stager]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
  - "[[echo-forge]]"
related:
  - "[[2026-08-08-stager-mvp-boundary-and-activation]]"
  - "[[Stager - Symphony Publisher Integration]]"
visibility: public
governed_by: user
promotion_target: project
source: Stager MVP design
aliases:
  - Stager deployment platform
  - Stager scopes and targets
tags:
  - kind/idea
  - area/echo
  - project/stager
  - app/stager-app
  - idea/opportunity
  - size/large
created: 2026-08-08
updated: 2026-08-08
---

# 💡 Stager como sistema pequeño de deployment

> [!tip]+ Futuro deliberadamente diferido
> El MVP sigue siendo one-shot y una configuración equivale a un target. Esta idea evita perder la dirección futura sin contaminar la integración actual.

## 🧠 La idea

- Evolucionar [[stager-app|Stager]] desde un reconciliador de un target hacia un sistema pequeño de deployment configurable cuando existan varios consumers o targets reales.
- El core actual permanece abajo y sin cambios conceptuales:

```text
Scope opcional futuro
  ├── target sqx-linux-prod
  ├── target sqx-windows-prod
  └── target otro-consumer-stage
          ↓
      Stager RunOnce actual
```

- Posibles conceptos, sólo después de evidencia: named configs, targets, environments, channels, groups/scopes, inventory y políticas de rollout.
- Un control plane, API/UI o agente de flota sería una capa superior; nunca se incrusta en el reconciliador filesystem.

## 🎯 Motivo / por qué

- El diseño actual permite crecer por composición: `manifest + platform + root` ya define un deployment target.
- Registrar la dirección evita que una futura IA reinvente o meta scopes prematuramente dentro de `RunOnce`.
- El valor sólo aparece cuando hay coordinación real de múltiples targets; antes sería costo y moving parts sin beneficio.

## Señales para promover

Promover a proyecto únicamente si ocurre al menos una:

1. Existe un segundo consumer productivo distinto de Symphony.
2. Un mismo host/agente debe reconciliar más de una configuración.
3. Operaciones necesita rollout coordinado por ambiente/grupo y no basta ejecutar varios timers.
4. La configuración manual por host se vuelve una fuente repetida de drift o incidentes.

No promover sólo porque el modelo “podría ser útil”.

## Guardrails si se promueve

- Mantener `RunOnce(targetConfig)` como unidad de ejecución.
- Scope agrupa targets; no cambia manifest ni estado local de un target.
- Scheduling y supervisión siguen externos o en una capa superior separada.
- No introducir DB hasta que exista historial/coordination que el filesystem no pueda resolver.
- No agregar un source nuevo sin consumer real.
- Migración incremental: una config actual debe seguir funcionando sin control plane.

## 🧭 Routing

- **Área:** [[Echo]]
- **Proyecto:** [[Stager]]
- **Aplicación:** [[stager-app]]
- **Entidades:** [[echo-forge]]

## 🏷️ Clasificación

- **Tamaño:** large.
- **Tipo:** opportunity.
- **Prioridad:** P3.
- **Estado:** seed.
- **Visibilidad:** public.
- **Gobernada por:** user.
- **Criterio de promoción:** una señal real de múltiples targets/consumers más una necesidad operacional que timers/configs independientes no resuelvan bien.

## 🔗 Relacionado

- [[2026-08-08-stager-mvp-boundary-and-activation]]
- [[Stager - Symphony Publisher Integration]]

## 🌱 Próximo paso

- [ ] Mantener en seed hasta que exista un segundo consumer o coordinación multi-target real #owner/me #type/research #area/echo

