---
type: runbook
schema_version: 1
scope: user
created: "2026-09-11"
updated: "2026-09-11"
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
  - "[[pr-description]]"
  - "[[human-first-technical-writing]]"
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

# signals-code-review-runbook

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Ejecutar una revisión `signals-code-review` exclusivamente para proyectos Meli: demostrar scope, fijar el diff, recuperar intención, correr la tool canónica Zord, verificar comportamientos críticos y preparar comentarios Human First antes del único gate de Rodrigo. En Signals/RIO se suma el Zord global independiente `rjara-rio-impact` y contexto oficial RIO con progressive disclosure. Sólo después de aprobación explícita se publican los puntos seleccionados y un resumen corto. El criterio y el veredicto pertenecen a la skill [[signals-code-review]].

## Precondiciones

- Existe un repo local o referencia de PR resoluble y se conoce o puede demostrar la base real.
- La pertenencia a Meli debe poder demostrarse mediante el remoto/owner, metadata corporativa o una relación canónica del vault. Un path local, nombre parecido o afirmación aislada no bastan. Si la identidad es no Meli o incierta, terminar `NOT_APPLICABLE` antes de invocar Zord.
- `VAULT_ROOT` resuelve el marker `80-agents/agents-os/agents-os.md`; [[Fuentes — Workspace de repositorios]] resuelve el workspace externo sin persistir paths absolutos.
- La revisión es read-only. Si hay conflicto, cambios funcionales locales ambiguos o archivos trackeados no atribuibles, detenerse y pedir decisión.
- Zord está registrado como [[local-agents-pipeline-cli]]. Resolver el ejecutable desde esa nota: preferir `zord` del `PATH` y, si no está expuesto, usar el checkout owner `local-agents-pipeline-cli` bajo [[Fuentes — Workspace de repositorios]] mediante su `node lib/cli.js` documentado. Si ninguna ruta registrada funciona, marcar `DEGRADED`; no buscar otra herramienta, instalar paquetes, crear prompts ni ejecutar `zord add` durante el review.
- Para Signals/RIO debe existir `~/.config/zords/agents/rjara-rio-impact.md`, con `enabled: false`, hook `manual` y source efectivo `global`. Si falta, no valida o una definición repo-local lo sombrea, bloquear ese review en vez de continuar sin el control transversal.
- Para publicar, debe existir un PR con head SHA y diff vigentes, una sesión GitHub autenticada y aprobación explícita de Rodrigo sobre IDs concretos o sobre todos los puntos presentados.

## Procedimiento

1. **Crear el checkpoint de baseline.** Capturar `git status --short --branch`, `git branch --show-current`, remotos, HEAD y base candidata. Resolver `BASE_SHA` con `git merge-base HEAD <base-ref>` y registrar `git diff --stat BASE_SHA...HEAD`, `git diff --name-status BASE_SHA...HEAD` y `git diff --check BASE_SHA...HEAD`. Para un PR, obtener title, body, head, base, files, commits y URL con `gh pr view`; no asumir que la rama por defecto es la base real.
2. **Congelar el alcance.** Identificar ticket/iniciativa, repos relacionados y cambios locales. Leer el diff completo si es razonable; si no, cuantificar lo omitido y priorizar contratos, dominio, persistencia y seguridad antes que tests o formato. No reportar como regresión lo que no aparece en `BASE_SHA...HEAD`.
3. **Recuperar intención.** Usar la descripción vigente del PR y buscar por ticket/branch sólo el proyecto relevante bajo `10-projects/`. Leer SPEC funcional, SPEC técnica, tasks, ADRs y criterios de aceptación enlazados; no cargar proyectos vecinos. Registrar por requisito `cumple`, `contradice`, `no implementado` o `sin evidencia`.
4. **Extraer seeds de impacto.** Desde archivos y hunks modificados listar cambios en APIs, schemas, eventos, topics/queues, estados, scopes, component types, tablas/queries, serialización, configuración, dependencias y orden de deploy. Cada seed debe llevar archivo/línea, contrato y owner inicial.
5. **Resolver la documentación oficial de RIO.** Leer primero `30-resources/knowledges/ads-signals-knowledge-library.md` y `30-resources/storage/fuentes-workspace.md`; desde el repo resoluble `ads-signals-knowledge-library`, obedecer `AGENTS.md`, entrar por `README.md` y `docs/00-start-here`, seleccionar un intent en `docs/06-skills/context-packs.md` y abrir sólo el flow, servicio, feature ID o `edge.*` aplicable. Usar `docs/08-governance/source-manifest.md` para frescura. Complementar con `30-resources/rio-atlas/00-index.md`, `architecture/integration-map.md` y las fichas de aplicaciones impactadas; no cargar todo el storage.
6. **Expandir el frente transversal.** Por cada seed, seguir productor → transporte → consumidor → persistencia/estado/observabilidad. Abrir un segundo edge sólo si el primero confirma la propagación. Detener el traversal cuando el siguiente componente no comparte el contrato o no cambia una decisión. Registrar cualquier superficie no resoluble como `UNKNOWN`, no como compatible.
7. **Contrastar con código owner.** Si una afirmación cambia severidad, rollout o compatibilidad, verificarla en el checkout/HEAD actual de ambos extremos. La knowledge library y RIO Atlas localizan la evidencia; el código owner decide. Ante drift del manifest, declarar SHA documentado, SHA observado y qué conclusión queda degradada.
8. **Preparar evidencia cross-repo.** Cuando existen PRs o branches relacionadas, guardar sus diffs en un directorio creado con `mktemp -d` y combinarlos mediante `--extra-diffs`. No fabricar un diff de una app sólo porque la documentación la marca como vecina; si falta el cambio counterpart, registrarlo como riesgo de coordinación.
9. **Resolver y ejecutar el preflight de Zord.** Leer `30-resources/tools/local-agents-pipeline-cli.md` y fijar `ZORD_CMD` como el binario `zord` o como `node <FUENTES_ROOT>/local-agents-pipeline-cli/lib/cli.js`; no hacer discovery abierto. Ejecutar `${ZORD_CMD} list` y el dry-run equivalente al input: `${ZORD_CMD} assemble --scope branch --dry-run` para branch o `${ZORD_CMD} assemble --pr <ref> --dry-run` para PR. Registrar zords habilitados, asignaciones y gaps; `cross-repo-validation` sólo se invoca si el listado confirma su disponibilidad.
10. **Ejecutar Zord sin mutar el repo.** Para branch usar `${ZORD_CMD} assemble --scope branch --output-json --quiet`; para PR usar `${ZORD_CMD} assemble --pr <ref> --output-json --quiet`. Si hay diffs relacionados y están disponibles los reviewers, ejecutar además `${ZORD_CMD} summon io-boundaries cross-repo-validation --extra-diffs <archivo> --output-json --quiet`. Redirigir stdout al directorio temporal; no usar `zord fix`. En modo `--output-json`, parsear findings y síntesis: el exit code `0` no prueba ausencia de severidades altas.
11. **Hacer la revisión humana de control.** Revisar corrección y bordes; contratos/datos y backward compatibility; seguridad y mínimo privilegio; idempotencia, concurrencia y retry; resiliencia, escalabilidad y observabilidad; tests críticos; modularidad, SOLID y clean code; KISS/YAGNI, código muerto, documentación y estilo enforced. Buscar usos y productores en repos relacionados antes de afirmar ausencia.
12. **Reconciliar findings.** Para cada finding de Zord registrar `confirmado`, `duplicado`, `falso positivo` o `no verificable`; comprobar que archivo/línea estén en el diff y que el escenario sea alcanzable. Agregar findings propios sólo con el mismo estándar de evidencia. Clasificar impacto como introducido por branch, heredado o local.
13. **Construir la matriz de comportamiento crítico.** Derivar las funcionalidades críticas desde SPEC/PR, criterios de aceptación, contratos y diff. Para cada comportamiento registrar riesgo si falla, entrada o evento, resultado observable, estado/side effect esperado, test que lo demuestra y bordes negativos relevantes. Un test que sólo verifica calls, getters, branches internas o estructura de implementación no acredita el comportamiento salvo que esa interacción sea el contrato observable que protege.
14. **Verificar proporcionalmente al riesgo.** Ejecutar instrucciones del repo y tests que cubran primero todos los comportamientos críticos identificados. Sólo después revisar el coverage y agregar tests complementarios cuando el piso o ramas relevantes lo requieran. Coverage-driven tests son válidos, pero deben conservar una aserción útil y no convierten un comportamiento crítico no probado en `PASS`. Registrar comando y resultado observado. Comparar `git status` con el checkpoint después de cada comando; si una validación genera cambios, detenerse y no borrar ni revertir nada que no esté demostrado como efecto exclusivo de esa ejecución.
15. **Preparar la explicación y los comentarios.** Cargar [[human-first-technical-writing]]. Por cada finding publicable redactar un comentario corto en orden causa → efecto → acción, con lenguaje cordial y suficiente contexto para que el autor entienda el comportamiento afectado sin reconstruir toda la investigación. Presentar a Rodrigo ID, severidad, ubicación, explicación de por qué importa, evidencia y texto exacto propuesto; agrupar duplicados y excluir nits sin valor.
16. **Ejecutar el único gate humano.** Preguntar `¿Publico todos, sólo <IDs> o ninguno?` y detener toda escritura remota. Una aceptación total o por IDs habilita continuar sin una segunda confirmación; una corrección de contenido obliga a mostrar nuevamente sólo los textos cambiados. Silencio, ambigüedad o una reacción no explícita no son aprobación.
17. **Revalidar y publicar.** Tras aprobación, volver a leer head SHA y diff del PR y confirmar que cada `path`/`line`/`side` sigue vigente. Si cambió una posición, no publicar ese punto y volver al gate sólo para los comentarios afectados. Publicar los comentarios seleccionados preferentemente en una única review con `event: COMMENT`, comentarios inline de un párrafo corto y un body con una frase de veredicto más un máximo de tres bullets materiales; no usar `position` cuando están disponibles `line` y `side`. No publicar findings descartados, no aprobados ni ya comentados.
18. **Verificar el resultado remoto.** Leer la review creada, comprobar autor, head, body, comentarios y URLs, y reportar a Rodrigo qué IDs se publicaron, cuáles se omitieron y por qué. Si la operación devuelve timeout o resultado incierto, inspeccionar el PR antes de reintentar para evitar duplicados.
19. **Cerrar el review.** Aplicar el output de la skill con matriz transversal, matriz de comportamiento crítico, coherencia PR/specs, estado de Zord, tests y límites. Actualizar el proyecto sólo si cambió un hecho real y el workflow activo lo exige. Hacer handoff a [[pr-description]] o a implementación únicamente por pedido explícito.

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
Critical behaviors mapped:   PASS
Critical behavior tests:     PASS | GAP material declarado
Coverage complement:         PASS | NO APLICA | GAP declarado
Human First comments:        PASS
Owner gate:                  PENDING | APPROVED <IDs> | REJECTED
Publication:                 NOT AUTHORIZED | PASS | PARTIAL | FAILED
Working tree preservado:     PASS
Resultado:                   COMPLETE | DEGRADED | BLOCKED
```

- `COMPLETE` para la fase de análisis exige Zord ejecutado, fuentes RIO navegadas con progressive disclosure, findings refutados, comportamientos críticos mapeados y working tree sin mutaciones atribuibles al review; la publicación puede quedar `NOT AUTHORIZED` mientras espera el único gate humano.
- `DEGRADED` permite entregar evidencia útil cuando falta Zord, una fuente o una verificación, pero el límite debe aparecer en el encabezado y en `No verificado`.
- `BLOCKED` aplica si no se puede fijar la base, el diff mezcla cambios funcionales ambiguos, falta prueba efectiva de un comportamiento crítico con riesgo material o la evidencia contradice la identidad del cambio.

## Rollback / recuperación

- El análisis no modifica código ni estado remoto. No ejecutar `zord fix`, commits, pushes ni creación de PR; publicar comentarios es la única mutación permitida y requiere el gate explícito del paso 16.
- Conservar el checkpoint inicial. Si una validación cambia el working tree, identificar el efecto exacto y pedir decisión cuando no sea inequívocamente generado por el comando actual; nunca usar una limpieza amplia.
- Los artefactos temporales de Zord se eliminan sólo al final y únicamente desde el path exacto retornado por `mktemp -d`; conservarlos si son necesarios para explicar un fallo o reanudar la revisión.
- Ante timeout o salida incierta de Zord, inspeccionar primero el JSON temporal y procesos activos; no relanzar hasta demostrar que la ejecución anterior terminó.
- Ante publicación parcial o incierta, leer primero reviews y comentarios existentes. No reintentar, editar ni borrar comentarios remotos hasta identificar los IDs realmente creados.

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
Critical behaviors:      <behavior/risk/observable/test/verdict>
Verification:            <commands/results/coverage complement>
Comment preview:         <IDs/texts shown to Rodrigo>
Owner decision:          <PENDING | APPROVED IDs | REJECTED>
Publication:             <review URL/comment URLs/result>
Working tree after:      <estado y delta vs checkpoint>
Result:                  COMPLETE | DEGRADED | BLOCKED
```
