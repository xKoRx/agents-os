---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Estandarización de Scopes RIO]]"
sprint:
start: 2026-09-16
due:
progress: 5
repo: https://github.com/melisource/fury_rio-playmaker
jira: SIG-599
prs:
aliases:
  - POC Playmaker scope alpha
  - Routing KISS de scopes en rio-playmaker
tags:
  - kind/project
  - area/meli
  - project/scopes-rio
  - tech/rio-playmaker
created: "2026-09-16"
updated: "2026-09-22"
---

# POC KISS — Routing de scopes en Playmaker

> [!danger] Regla básica
> **PIPELINE ENVIRONMENT ≠ FURY SCOPE.** La lane sale exclusivamente del scope Fury del runtime y sólo se usa como filtro BigQueue. No toca modelo, DB, idempotencia, history ni payloads.

> [!info]+ Estado ejecutivo
> **Ready phase:** Fase 0 · **Gate actual:** G0 `review` · **Baseline:** `origin/master@becd61f0c1f5bccea7ee75433003244cf59589df` · **Principio KISS:** derivación centralizada de lane/profile y defaults seguros; producers, filtros y timeout quedan fuera de esta fase.

## 🎯 Objetivo

Implementar la POC alpha mínima de SIG-599 en `rio-playmaker`:

- Resolver `RuntimeLane(alpha)` desde `alpha-api-nonprod` y `alpha-consumer-nonprod` al startup.
- Fallar el startup ante scope ausente, typo, uppercase, segmento incorrecto o error del accessor.
- Publicar `scope:alpha` desde los dos deployment trigger producers activos y el result producer.
- Deshabilitar timeout processing en alpha para no reclamar deployments de otra lane desde la DB compartida.
- Certificar deploy/undeploy existente, pipeline nuevo, batch N+1 y result; no certificar retry/restart.

## 📊 Estado actual

- `ScopeUtils.getScopeValue()` lee `SCOPE` y cae en `local`; ese fallback no es seguro para routing canónico.
- La resolución actual de profiles no cubre correctamente `prod/stage/alpha/beta/gamma`.
- Existen dos producers productivos de deployment trigger, no uno:
  - `restclient.impl.BigQueueDeploymentTriggerProducerImpl`.
  - `service.pipeline.impl.DeploymentTriggerProducerImpl`.
- `DeploymentResultProducerImpl` publica deployment results.
- Los tres usan hoy `producer.send(message)`.
- `DeploymentTimeoutJob` consulta la DB compartida sin lane y puede republicar desde otro runtime.
- mqclient 3.4.9 ya expone `Producer.send(message, Filters)`.
- Fury/BigQueue aún debe demostrar filtering server-side, envelope preservado y accessor oficial.

## Resultado esperado

```text
alpha-api-nonprod / alpha-consumer-nonprod
                    │
                    ▼ startup
             RuntimeLane(alpha)
                    │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
trigger legacy  trigger pipeline  result
       └────────── send(..., Filters([scope:alpha]))

timeout processing alpha: OFF
```

No existe publish sin filtro dentro de los beans canónicos. Local/tests usan sus implementaciones locales.

## Alcance

### Incluido

- Accessor Fury confirmado y lane estricta al startup.
- Mapping profile: `prod→production`; `stage/alpha/beta/gamma→stage`.
- Defaults stage/nonprod para scopes nuevos.
- Filtros en ambos trigger producers y el result producer.
- Un switch binario para apagar scan y resolución lazy de timeouts en alpha.
- E2E lane-affine con ambos caminos de trigger, batch N+1 y result.

### Fuera de alcance

- Retry/restart, ownership durable y reconciliación cross-lane.
- Lectura o propagación de `X-Rio-Scope`.
- `expectedScope`, carrier o modo legacy en el artefacto alpha.
- Cambios en controllers, dispatch, consumers, payloads, SDK, DB o migrations.
- Actions, runtime status, inactivation, DataProductChanged y Materializer.

## Matriz requisito → evidencia

| ID | Requisito | Estado | Gate |
|---|---|---|---|
| R1 | Pipeline Environment separado | confirmado | No-touch de dominio/DB |
| R2 | Accessor Fury soportado | pendiente | G0 |
| R3 | Scope canónico estricto y profile seguro | pendiente | G0 |
| R4 | Dos trigger producers filtrados | pendiente | G1 |
| R5 | Result producer filtrado | pendiente | G1 |
| R6 | Sin fallback a publish legacy | pendiente | G1 |
| R7 | Timeout processing off en alpha | pendiente | G1 |
| R8 | BigQueue filtra y preserva envelope | pendiente | G2 |
| R9 | E2E lane-affine alpha | pendiente | G2 |

## Roadmap dependency-ordered

| Fase | Resultado | Gate |
|---|---|---|
| F0 | Contratos Fury/BigQueue confirmados; lane/profile/startup seguros | G0 |
| F1 | Tres producers filtrados y timeout processing off en alpha | G1 |
| F2 | E2E alpha lane-affine y rollback | G2 |

## Fase 0 — Contratos y startup

### Misión

Cerrar los contratos externos y garantizar que un runtime canónico tenga una lane/profile seguros o no arranque.

### Trabajo

1. Confirmar con Fury el accessor Java/Kotlin y precedencia `scope`/`SCOPE`.
2. Demostrar con BigQueue filtering server-side y envelope preservado.
3. Escribir tests de naming/profile antes del código.
4. Resolver una `RuntimeLane` inmutable al startup.
5. Mapear profiles y defaults stage/nonprod.
6. Fallar cerrado ante missing, typo, uppercase y segmento incompatible.

### No tocar

- Producers, timeout job, dominio, DB, SDK y controllers.

### Gate G0

- Accessor y BigQueue documentados con evidencia real.
- Matriz scope→lane→profile verde.
- Ningún scope inválido cae en local/legacy.

## Fase 1 — Publicación filtrada completa

### Misión

Publicar siempre `scope:<lane>` desde todos los puntos de deployment de la POC y apagar el timeout cross-lane en alpha.

### Trabajo

1. Escribir tests de los tres producers.
2. Filtrar `service.pipeline.impl.DeploymentTriggerProducerImpl`.
3. Filtrar `restclient.impl.BigQueueDeploymentTriggerProducerImpl`.
4. Filtrar `DeploymentResultProducerImpl`.
5. Agregar un switch booleano de timeout processing, default `true`, y configurarlo `false` en alpha.
6. Probar que scan y resolución lazy no consultan DB ni publican cuando está apagado.
7. Verificar payloads intactos y ausencia de `producer.send(message)` en los beans canónicos incluidos.

### No tocar

- Callers, controllers, dispatch, consumers, DTOs, SDK, repositories y schema.
- Persistencia de lane y lógica de retry.

### Gate G1

- Tres producers publican exactamente `scope:alpha`.
- Scope inválido no arranca.
- Timeout processing alpha no ejecuta scan ni lazy resolution.
- Payloads y dominio permanecen intactos.

## Fase 2 — Certificación alpha lane-affine

### Misión

Certificar trigger/result alpha sin ejecutar caminos de ownership durable.

### Trabajo

1. Desplegar `alpha-api-nonprod` y `alpha-consumer-nonprod` con timeout processing off.
2. Capturar el envelope del producer legacy de deployment/undeployment.
3. Capturar trigger inicial y batch N+1 del pipeline nuevo.
4. Capturar deployment result.
5. Confirmar que todos contienen exactamente `scope:alpha` y payload intacto.
6. Confirmar que un consumer beta no recibe alpha.
7. Ejecutar rollback drenando primero el backlog filtrado.

### Prohibido

- Provocar timeout/retry o afirmar que restart está cubierto.
- Promover producción.
- Agregar estado durable para ampliar la evidencia.

### Gate G2

- Ambos triggers, batch N+1 y result llevan `scope:alpha`.
- BigQueue demuestra aislamiento alpha/beta y envelope intacto.
- Rollback ejecutado sin dejar mensajes filtrados para un consumer legacy.

## Mapa de archivos

| Acción | Superficie | Fase |
|---|---|---|
| `modify` | `ScopeUtils` o configuración de startup y tests | F0 |
| `modify` | `application.yml`/profiles y tests | F0 |
| `modify` | Dos trigger producers y tests | F1 |
| `modify` | Result producer y tests | F1 |
| `modify` | Timeout config/job y tests | F1 |
| `no-touch` | Controllers, services, dispatch, consumers, payloads, SDK, DB/schema | Todas |

## Riesgos y controles

| Riesgo | Control KISS |
|---|---|
| Scope inválido publica sin filtro | Startup failure; cero fallback |
| Producer activo queda fuera | Inventario de dos triggers + result y test de ausencia de send simple |
| Timeout alpha reclama otra lane | Timeout processing off |
| BigQueue no filtra realmente | Gate real antes del rollout |
| Rollback pierde mensajes filtrados | Cerrar entrada y drenar antes de revertir consumer |
| Scope creep durable | Retry/restart explícitamente fuera |

## Definition of Done

- G0–G2 aceptados por el owner.
- `RuntimeLane(alpha)` se resuelve al startup y nombres inválidos no arrancan.
- Dos trigger producers y el result producer publican `scope:alpha`.
- Timeout processing está apagado en alpha.
- E2E cubre deploy/undeploy existente, pipeline nuevo, batch N+1 y result.
- No hay cambios de payload, SDK, DB ni pipeline environment.
- Retry/restart permanece como fase futura separada.

## Stop conditions

- Fury no confirma accessor.
- BigQueue no filtra server-side o elimina filtros del push.
- Queda un producer de deployment incluido publicando sin filtro.
- Scope inválido degrada a local/legacy.
- Timeout processing no puede apagarse sin tocar schema/ownership.
- E2E produce un mensaje sin filtro o una lane distinta.

## 🧭 Decisiones

- Runtime canónico estricto; sin modo legacy en la POC.
- Los dos trigger producers activos son parte obligatoria del diff.
- Timeout/retry se deshabilita y excluye; no se persiste lane.
- La generalización ocurre sólo después de un segundo caso real.
- `prod/stage/alpha/beta/gamma` son tokens runtime; `production/staging` son etiquetas funcionales.

## ✅ Tareas

- [ ] **F0.1** Confirmar accessor Fury y semántica BigQueue #owner/me #type/research #area/meli
- [r] **F0.2** Implementar lane/profile y defaults seguros; dejar fallback legacy cuando la lane no sea resoluble #owner/agent #type/dev #area/meli
- [ ] **F0.3** Trazar y aprobar el componente Flink lane-affine del golden deploy #owner/me #type/research #area/meli
- [ ] **F1.1** Filtrar ambos deployment trigger producers #owner/agent #type/dev #area/meli #waiting
- [ ] **F1.2** Filtrar result producer #owner/agent #type/dev #area/meli #waiting
- [ ] **F1.3** Deshabilitar timeout processing en alpha #owner/agent #type/dev #area/meli #waiting
- [ ] **F2.1** Certificar ambos triggers, batch N+1 y result #owner/me #type/dev #area/meli #waiting
- [ ] **F2.2** Ejecutar negativos, drain y rollback #owner/me #type/dev #area/meli #waiting

## 📆 Bitácora

- **2026-09-16** — Plan inicial creado.
- **2026-09-21** — Se adoptó derivación runtime sin carrier.
- **2026-09-22** — Review independiente detectó fallback fail-open, segundo trigger producer y timeout cross-lane. Se aplicó KISS: startup estricto, tres producers, timeout off y E2E lane-affine; no classifier complejo ni persistencia.
- **2026-09-22** — FASE 0 implementada en `feature/sig-599-playmaker-scope-filter-poc` sobre `origin/master@becd61f0c1f5bccea7ee75433003244cf59589df`: `ScopeUtils.getScopeLane()` centraliza la lane allowlisted, `calculateScopeSuffix()` mapea `prod→production` y `stage/alpha/beta/gamma→stage`, y `application.yml` queda con datasource `playmkrstg` y BigQueue `nonprod`. La instrucción vigente de ejecución define fallback legacy para lane ausente/malformed/unknown; producers y demás superficies de F1/F2 permanecen intactos. Tests focales y cobertura nueva verdes; la suite completa conserva 6 fallos H2 preexistentes en `DataProductControllerIntegrationTest`. Gate G0 queda en `review`.

## 🔗 Docs / Links

- [[SPEC técnica — Routing KISS por scope en rio-playmaker]]
- [[SPEC técnica — Continuidad de scope en control planes RIO]]
- [[scope-naming-standard]]
- [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599)

## 💡 Ideas

- Diseñar ownership durable de retry sólo después de cerrar la POC lane-affine.
