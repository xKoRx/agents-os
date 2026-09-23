# Agents resource log

## [2026-09-23] create | technical-project-manager

- Se creó `technical-project-manager` como skill transversal para convertir una iniciativa acotada en un horizonte corto de hitos diarios observables, atómicos y verificables.
- Cada día congela diseño/contratos justo a tiempo y ejecuta tres shots: implementación autónoma, verificación independiente adversarial y corrección + gate final.
- La skill separa `DAY_PASS` de promoción a producción y deriva release/deploy/E2E a `release-certification`, `deployment-proof` y `e2e-gated-validation`; no duplica SDD ni implementation planning.
- Forward-test de activación: proyecto multi-día con varios agentes → aplica; cambio trivial aislado → no aplica; certificación/deploy puro → handoff a las skills de release/validation.

## [2026-09-17] create | rio-sunset-update

- Se curó en el vault la propuesta `feat/rio-sunset-update@a7872cd` de `ads-signals-skills-marketplace`, incluyendo referencias y gates ejecutables de input, binding build→SHA y scope de test.
- La adaptación alineó la metadata con AGENTS OS, agregó routing desde `meli-agent-dev` y corrigió la contradicción que excluía Fury CLI aunque el flujo exige `fury create-version`.
- El validador del marketplace y los tests `validate-input.test.mjs` y `validate-gates.test.mjs` quedaron verdes antes y después de la importación.

## [2026-09-16] create | Hermes Agent operator

- Se creó `hermes-agent-operator` como skill federada de Aranea para diagnóstico/operación del propio runtime Hermes: perfiles, dashboard/serve, gateways, `systemd --user`, updates y recovery.
- `aranea-agent-dev` quedó actualizado para cargar esta skill sólo cuando Hermes es el target; si Hermes sólo actúa como operador de otro servicio, se mantiene la skill del dominio objetivo.
- La mecánica determinista de update/recovery quedó externalizada a `30-resources/runbooks/hermes-linux-update-recovery.md`; la skill conserva criterio, routing, guards y output contract.

## [2026-09-14] fix | Autoridad federada única y routing externo

- Se completó la migración de 13 skills retirando sus copias bajo `80-agents/skills/`; `30-resources/agents/skills/` queda como única autoridad federada.
- Se agregó `domain-router-registry.md` como configuración opcional de áreas, routers y evidencia: 0 matches → DEFAULT, 1 → router, más de 1 → fail-closed.
- El índice always-load conserva sólo las skills transversales necesarias; los routers y skills de dominio se descubren desde este dominio, no desde el core.

## [2026-08-10] ingest | AGENTS OS Fase 3 → dominio agents

- Se activó `30-resources/agents/` con su índice, contrato de prompt reusable y registro de migración F3.

## [2026-08-10] ingest | AGENTS OS Fase 3 → ownership y discovery

- Se migraron las dos skills app-owned pendientes a `xKoRx/symphony`, se actualizó el registry federado y el pack, y el forward-test terminó sin fallas.

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4

- Cobertura del índice completa; contrato superficie×modelo revisado; Graphify limpio y actualizado.

## [2026-09-11] ingest | Aranea MCP capability plane

- Se actualizó `aranea-mcps-expert` para seleccionar primero ambiente y luego capability: data PROD=RO y DEV=RW; se documentó explícitamente que los runbooks viven en `80-agents/memory/public/runbook/` y se alinearon los runbooks PostgreSQL, MongoDB, SSH y capability-plane con el estado verificado.

## [2026-09-12] ingest | Restructura de skills: core agents-os vs federadas

- Se movieron 13 skills no-agents-os desde `80-agents/skills/` a `30-resources/agents/skills/` (signals-*, pr-description, human-first-technical-writing, y las 8 de evidencia/validación); el core quedó reservado a comportamientos de AGENTS OS.
- Se crearon los routers de dominio `meli-agent-dev` y `aranea-agent-dev` (excluyentes entre sí); `aranea-mcps-expert` quedó subordinada a `aranea-agent-dev` como única puerta MCP de Aranea.
- `80-agents/skills/INDEX.md` se reescribió en formato índice wiki (core + registro federado enlazado); este `00-index.md` incorporó las 18 skills como filas del catálogo.

## [2026-09-13] update | Aranea MCP Kafka/Flink

- `aranea-agent-dev` y `aranea-mcps-expert` quedaron alineadas con las familias Kafka y Flink sin duplicar mecánica: la expert sigue siendo router central y deriva a runbooks de familia bajo `30-resources/runbooks/`.
- Flink DEV usa dos superficies complementarias: `aranea-flink-dev-admin` para control plane y `aranea-ssh` + `docker-echo-dev-operator` para host/runtime; PROD queda diferido strict-RO.
- El índice de agents y el índice/log de runbooks se actualizaron para incluir `aranea-kafka-mcp` y `aranea-flink-mcp` como autoridades mecánicas canónicas.

## [2026-09-15] create | observability-metrics-standard

- Se instaló el plugin corporativo `sentinels@sentinels-commands` (repo `melisource/fury_rio-observability-standard`) en Claude Code, además de Codex, para que `meli-agent-dev` pueda referenciarlo en esta superficie sin fork.
- Se creó la skill transversal `observability-metrics-standard` destilando el método de las skills `scan`/`migrate`/`pr-review` del plugin (checklist de límites de ciclo de vida, principios de tags/tipo/emisión, formato de hallazgos) sin copiar la gramática `signals.rio.*`/`fury_app`/catálogo de entidades, que es propiedad Meli y sigue evolucionando (`Status: Proposed`).
- Trigger boundary explícito: Aranea/homelab y proyectos personales; handoff a `meli-agent-dev` para todo trabajo Meli/RIO/Signals/Ads.
- `80-agents/skills/INDEX.md` y `30-resources/agents/00-index.md` se actualizaron con la fila y el conteo (13 federadas transversales).
