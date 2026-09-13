---
type: runbook
schema_version: 1
status: superseded
superseded_by: "[[signals-code-review-runbook]]"
scope: user
created: "2026-09-11"
updated: "2026-09-12"
area: "[[Meli]]"
project:
application:
entities:
  - "[[RIO]]"
  - "[[local-agents-pipeline-cli]]"
  - "[[ads-signals-knowledge-library]]"
related:
  - "[[signals-code-review]]"
  - "[[Fuentes — Workspace de repositorios]]"
  - "[[RIO Atlas]]"
  - "[[pr-description]]"
aliases:
  - runbook de code review Signals
  - RIO review runbook
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/user
  - action/code-review
  - area/meli
  - app/rio
  - tech/zord
---

# signals-code-review

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Ejecutar de forma read-only una revisión `signals-code-review`: fijar el diff, recuperar intención y contexto RIO con progressive disclosure, correr Zord, verificar impacto cross-app, ejecutar validaciones proporcionadas al riesgo y reunir evidencia reproducible. El criterio y el veredicto pertenecen a la skill [[signals-code-review]].

## Precondiciones

- Existe un repo local o referencia de PR resoluble y se conoce o puede demostrar la base real.
- `VAULT_ROOT` resuelve el marker `80-agents/agents-os/agents-os.md`; [[Fuentes — Workspace de repositorios]] resuelve el workspace externo sin persistir paths absolutos.
- La revisión es read-only. Si hay conflicto, cambios funcionales locales ambiguos o archivos trackeados no atribuibles, detenerse y pedir decisión.
- Para una ejecución `COMPLETE`, `zord`, Git y el provider asignado deben estar disponibles. Si `zord` falta, registrar `DEGRADED`; no instalarlo ni reemplazarlo sin autorización.

## Procedimiento

1. **Crear el checkpoint de baseline.** Capturar `git status --short --branch`, `git branch --show-current`, remotos, HEAD y base candidata. Resolver `BASE_SHA` con `git merge-base HEAD <base-ref>` y registrar `git diff --stat BASE_SHA...HEAD`, `git diff --name-status BASE_SHA...HEAD` y `git diff --check BASE_SHA...HEAD`. Para un PR, obtener title, body, head, base, files, commits y URL con `gh pr view`; no asumir que la rama por defecto es la base real.
2. **Congelar el alcance.** Identificar ticket/iniciativa, repos relacionados y cambios locales. Leer el diff completo si es razonable; si no, cuantificar lo omitido y priorizar contratos, dominio, persistencia y seguridad antes que tests o formato. No reportar como regresión lo que no aparece en `BASE_SHA...HEAD`.
3. **Recuperar intención.** Usar la descripción vigente del PR y buscar por ticket/branch sólo el proyecto relevante bajo `10-projects/`. Leer SPEC funcional, SPEC técnica, tasks, ADRs y criterios de aceptación enlazados; no cargar proyectos vecinos. Registrar por requisito `cumple`, `contradice`, `no implementado` o `sin evidencia`.
4. **Extraer seeds de impacto.** Desde archivos y hunks modificados listar cambios en APIs, schemas, eventos, topics/queues, estados, scopes, component types, tablas/queries, serialización, configuración, dependencias y orden de deploy. Cada seed debe llevar archivo/línea, contrato y owner inicial.
5. **Resolver la documentación oficial de RIO.** Leer primero `30-resources/knowledges/ads-signals-knowledge-library.md` y `30-resources/storage/fuentes-workspace.md`; desde el repo resoluble `ads-signals-knowledge-library`, obedecer `AGENTS.md`, entrar por `README.md` y `docs/00-start-here`, seleccionar un intent en `docs/06-skills/context-packs.md` y abrir sólo el flow, servicio, feature ID o `edge.*` aplicable. Usar `docs/08-governance/source-manifest.md` para frescura. Complementar con `30-resources/rio-atlas/00-index.md`, `architecture/integration-map.md` y las fichas de aplicaciones impactadas; no cargar todo el storage.
6. **Expandir el frente transversal.** Por cada seed, seguir productor → transporte → consumidor → persistencia/estado/observabilidad. Abrir un segundo edge sólo si el primero confirma la propagación. Detener el traversal cuando el siguiente componente no comparte el contrato o no cambia una decisión. Registrar cualquier superficie no resoluble como `UNKNOWN`, no como compatible.
7. **Contrastar con código owner.** Si una afirmación cambia severidad, rollout o compatibilidad, verificarla en el checkout/HEAD actual de ambos extremos. La knowledge library y RIO Atlas localizan la evidencia; el código owner decide. Ante drift del manifest, declarar SHA documentado, SHA observado y qué conclusión queda degradada.
8. **Preparar evidencia cross-repo.** Cuando existen PRs o branches relacionadas, guardar sus diffs en un directorio creado con `mktemp -d` y combinarlos mediante `--extra-diffs`. No fabricar un diff de una app sólo porque la documentación la marca como vecina; si falta el cambio counterpart, registrarlo como riesgo de coordinación.
9. **Ejecutar el preflight de Zord.** Correr `command -v zord`, `zord list` y el dry-run equivalente al input: `zord assemble --scope branch --dry-run` para branch o `zord assemble --pr <ref> --dry-run` para PR. Registrar zords habilitados, asignaciones y gaps; `cross-repo-validation` suele estar deshabilitado y sólo se invoca si `zord list` confirma su disponibilidad.
10. **Ejecutar Zord sin mutar el repo.** Para branch usar `zord assemble --scope branch --output-json --quiet`; para PR usar `zord assemble --pr <ref> --output-json --quiet`. Si hay diffs relacionados y están disponibles los reviewers, ejecutar además `zord summon io-boundaries cross-repo-validation --extra-diffs <archivo> --output-json --quiet`. Redirigir stdout al directorio temporal; no usar `zord fix`. En modo `--output-json`, parsear findings y síntesis: el exit code `0` no prueba ausencia de severidades altas.
11. **Hacer la revisión humana de control.** Revisar corrección y bordes; contratos/datos y backward compatibility; seguridad y mínimo privilegio; idempotencia, concurrencia y retry; resiliencia, escalabilidad y observabilidad; tests críticos; modularidad, SOLID y clean code; KISS/YAGNI, código muerto, documentación y estilo enforced. Buscar usos y productores en repos relacionados antes de afirmar ausencia.
12. **Reconciliar findings.** Para cada finding de Zord registrar `confirmado`, `duplicado`, `falso positivo` o `no verificable`; comprobar que archivo/línea estén en el diff y que el escenario sea alcanzable. Agregar findings propios sólo con el mismo estándar de evidencia. Clasificar impacto como introducido por branch, heredado o local.
13. **Verificar proporcionalmente al riesgo.** Ejecutar instrucciones del repo y tests que cubran primero los caminos críticos tocados; luego coverage si corresponde. Registrar comando y resultado observado. Comparar `git status` con el checkpoint después de cada comando; si una validación genera cambios, detenerse y no borrar ni revertir nada que no esté demostrado como efecto exclusivo de esa ejecución.
14. **Emitir y cerrar el review.** Aplicar el output de la skill, incluyendo matriz `seed → edge/app → evidencia → riesgo → confianza`, coherencia PR/specs, estado de Zord, tests y límites. Actualizar el estado del proyecto sólo si la revisión cambió un hecho real y el workflow activo lo exige. Hacer handoff a [[pr-description]] o a implementación únicamente por pedido explícito.

## Validación

Success requiere:

```text
Baseline/base real:          PASS
Diff clasificado:            PASS
Intención PR/specs:          PASS | GAP declarado
Fuente oficial RIO:          PASS
Frescura/provenance:         PASS | DRIFT declarado
Impact frontier:             PASS
Zord preflight:              PASS
Zord execution:              PASS | DEGRADED declarado
Findings reconciliados:      PASS
Tests/verificación:          PASS | NO EJECUTADO declarado
Working tree preservado:     PASS
Resultado:                   COMPLETE | DEGRADED | BLOCKED
```

- `COMPLETE` exige Zord ejecutado, fuentes RIO navegadas con progressive disclosure, findings refutados y working tree sin mutaciones atribuibles al review.
- `DEGRADED` permite entregar evidencia útil cuando falta Zord, una fuente o una verificación, pero el límite debe aparecer en el encabezado y en `No verificado`.
- `BLOCKED` aplica si no se puede fijar la base, el diff mezcla cambios funcionales ambiguos o la evidencia contradice la identidad del cambio.

## Rollback / recuperación

- El runbook no modifica código ni estado remoto. No ejecutar `zord fix`, commits, pushes, comentarios ni creación de PR.
- Conservar el checkpoint inicial. Si una validación cambia el working tree, identificar el efecto exacto y pedir decisión cuando no sea inequívocamente generado por el comando actual; nunca usar una limpieza amplia.
- Los artefactos temporales de Zord se eliminan sólo al final y únicamente desde el path exacto retornado por `mktemp -d`; conservarlos si son necesarios para explicar un fallo o reanudar la revisión.
- Ante timeout o salida incierta de Zord, inspeccionar primero el JSON temporal y procesos activos; no relanzar hasta demostrar que la ejecución anterior terminó.

## Evidencia

```text
Review target:           <repo/PR/head>
Base ref / merge-base:   <ref> / <sha>
Working tree before:     <estado>
Intent sources:          <PR/specs/tasks>
RIO sources:             <library pages/feature IDs/edges/app notes>
Code SHAs:               <owner repos y HEADs observados>
Impact ledger:           <seeds y fronteras recorridas>
Zord preflight:          <zords/asignaciones>
Zord artifact:           <temp path o NOT CREATED>
Zord reconciliation:     <confirmed/rejected/unknown counts>
Verification:            <commands/results>
Working tree after:      <estado y delta vs checkpoint>
Result:                  COMPLETE | DEGRADED | BLOCKED
```
