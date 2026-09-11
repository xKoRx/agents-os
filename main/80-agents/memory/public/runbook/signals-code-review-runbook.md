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

1. **Ejecutar el gate Meli.** Inspeccionar remoto/owner, metadata corporativa y relaciones canónicas del vault. Registrar evidencia positiva. Si el target es no Meli o la pertenencia queda incierta, devolver `NOT_APPLICABLE`, nombrar la evidencia faltante y terminar: no ejecutar Zord, no cargar RIO y no continuar con una revisión genérica.
2. **Crear el checkpoint de baseline.** Capturar `git status --short --branch`, `git branch --show-current`, remotos, HEAD y base candidata. Resolver `BASE_SHA` con `git merge-base HEAD <base-ref>` y registrar `git diff --stat BASE_SHA...HEAD`, `git diff --name-status BASE_SHA...HEAD` y `git diff --check BASE_SHA...HEAD`. Para un PR, obtener title, body, head, base, files, commits y URL con `gh pr view`; no asumir que la rama por defecto es la base real.
3. **Congelar el alcance.** Identificar ticket/iniciativa, repos relacionados y cambios locales. Leer el diff completo si es razonable; si no, cuantificar lo omitido y priorizar contratos, dominio, persistencia y seguridad antes que tests o formato. No reportar como regresión lo que no aparece en `BASE_SHA...HEAD`.
4. **Clasificar Meli estándar versus Signals/RIO.** Usar repo, owners, proyecto y contratos para registrar `MELI_STANDARD` o `MELI_SIGNALS_RIO`. Sólo el segundo habilita la documentación RIO y `rjara-rio-impact`; ante duda usar `MELI_STANDARD`, no inferir RIO por cercanía temática.
5. **Recuperar intención.** Usar la descripción vigente del PR y buscar por ticket/branch sólo el proyecto relevante bajo `10-projects/`. Leer SPEC funcional, SPEC técnica, tasks, ADRs y criterios de aceptación enlazados; no cargar proyectos vecinos. Registrar por requisito `cumple`, `contradice`, `no implementado` o `sin evidencia`.
6. **Extraer seeds de impacto sólo para Signals/RIO.** Desde archivos y hunks modificados listar cambios en APIs, schemas, eventos, topics/queues, estados, scopes, component types, tablas/queries, serialización, configuración, dependencias y orden de deploy. Cada seed debe llevar archivo/línea, contrato y owner inicial. En `MELI_STANDARD`, registrar `Impacto RIO: NO APLICA` y saltar los pasos 7–9.
7. **Resolver la documentación oficial de RIO.** Leer primero `30-resources/knowledges/ads-signals-knowledge-library.md` y `30-resources/storage/fuentes-workspace.md`; desde el repo resoluble `ads-signals-knowledge-library`, obedecer `AGENTS.md`, entrar por `README.md` y `docs/00-start-here`, seleccionar un intent en `docs/06-skills/context-packs.md` y abrir sólo el flow, servicio, feature ID o `edge.*` aplicable. Usar `docs/08-governance/source-manifest.md` para frescura. Complementar con `30-resources/rio-atlas/00-index.md`, `architecture/integration-map.md` y las fichas de aplicaciones impactadas; no cargar todo el storage.
8. **Expandir el frente transversal.** Por cada seed, seguir productor → transporte → consumidor → persistencia/estado/observabilidad. Abrir un segundo edge sólo si el primero confirma la propagación. Detener el traversal cuando el siguiente componente no comparte el contrato o no cambia una decisión. Registrar cualquier superficie no resoluble como `UNKNOWN`, no como compatible.
9. **Contrastar con código owner.** Si una afirmación cambia severidad, rollout o compatibilidad, verificarla en el checkout/HEAD actual de ambos extremos. La knowledge library y RIO Atlas localizan la evidencia; el código owner decide. Ante drift del manifest, declarar SHA documentado, SHA observado y qué conclusión queda degradada.
10. **Preparar evidencia cross-repo.** Cuando existen PRs o branches relacionadas, guardar sus diffs en un directorio creado con `mktemp -d` y combinarlos mediante `--extra-diffs`. No fabricar un diff de una app sólo porque la documentación la marca como vecina; si falta el cambio counterpart, registrarlo como riesgo de coordinación.
11. **Resolver y ejecutar el preflight de Zord.** Leer `30-resources/tools/local-agents-pipeline-cli.md` y fijar `ZORD_CMD` como el binario `zord` o como `node <FUENTES_ROOT>/local-agents-pipeline-cli/lib/cli.js`; no hacer discovery abierto. Ejecutar `${ZORD_CMD} list` y el dry-run equivalente al input. Para `MELI_STANDARD`, usar `${ZORD_CMD} assemble --scope branch --dry-run` o `${ZORD_CMD} assemble --pr <ref> --dry-run`. Para `MELI_SIGNALS_RIO`, verificar primero que `rjara-rio-impact` tenga source efectivo `global`, hook `manual` y estado disabled, y usar el mismo comando con `--include rjara-rio-impact`; si falta, no valida o está sombreado por repo, marcar `BLOCKED`. Registrar zords, asignaciones y gaps; `cross-repo-validation` sólo se invoca si el listado confirma su disponibilidad.
12. **Ejecutar Zord sin sesgar el revisor RIO.** Para `MELI_STANDARD`, usar `${ZORD_CMD} assemble --scope branch --output-json --quiet` o `${ZORD_CMD} assemble --pr <ref> --output-json --quiet`. Para `MELI_SIGNALS_RIO`, agregar `--include rjara-rio-impact` al comando correspondiente y, si existen, entregar los diffs relacionados sólo mediante `--extra-diffs`. No alterar el prompt global, no generar un brief y no pasar prioridades, sospechas, findings previos ni conclusiones del coordinador. Redirigir stdout al directorio temporal; no usar `zord fix`. En `--output-json`, parsear los resultados crudos —la síntesis Human First la hace esta skill— y no interpretar exit code `0` como ausencia de severidades altas.
13. **Hacer la revisión humana de control.** Revisar corrección y bordes; contratos/datos y backward compatibility; seguridad y mínimo privilegio; idempotencia, concurrencia y retry; resiliencia, escalabilidad y observabilidad; tests críticos; modularidad, SOLID y clean code; KISS/YAGNI, código muerto, documentación y estilo enforced. En Signals/RIO, buscar usos y productores en repos relacionados antes de afirmar ausencia.
14. **Reconciliar findings.** Para cada finding de Zord registrar `confirmado`, `duplicado`, `falso positivo` o `no verificable`; comprobar que archivo/línea estén en el diff y que el escenario sea alcanzable. Mantener identificable la procedencia `rjara-rio-impact` y no contaminar su ejecución con la reconciliación. Agregar findings propios sólo con el mismo estándar de evidencia. Clasificar impacto como introducido por branch, heredado o local.
15. **Construir la matriz de comportamiento crítico.** Derivar las funcionalidades críticas desde SPEC/PR, criterios de aceptación, contratos y diff. Para cada comportamiento registrar riesgo si falla, entrada o evento, resultado observable, estado/side effect esperado, test que lo demuestra y bordes negativos relevantes. Un test que sólo verifica calls, getters, branches internas o estructura de implementación no acredita el comportamiento salvo que esa interacción sea el contrato observable que protege.
16. **Verificar proporcionalmente al riesgo.** Ejecutar instrucciones del repo y tests que cubran primero todos los comportamientos críticos identificados. Sólo después revisar el coverage y agregar tests complementarios cuando el piso o ramas relevantes lo requieran. Coverage-driven tests son válidos, pero deben conservar una aserción útil y no convierten un comportamiento crítico no probado en `PASS`. Registrar comando y resultado observado. Comparar `git status` con el checkpoint después de cada comando; si una validación genera cambios, detenerse y no borrar ni revertir nada que no esté demostrado como efecto exclusivo de esa ejecución.
17. **Preparar la explicación y los comentarios.** Cargar [[human-first-technical-writing]]. Por cada finding publicable redactar un comentario corto en orden causa → efecto → acción, con lenguaje cordial y suficiente contexto para que el autor entienda el comportamiento afectado sin reconstruir toda la investigación. Presentar a Rodrigo ID, severidad, ubicación, explicación de por qué importa, evidencia y texto exacto propuesto; agrupar duplicados y excluir nits sin valor.
18. **Ejecutar el único gate humano.** Preguntar `¿Publico todos, sólo <IDs> o ninguno?` y detener toda escritura remota. Una aceptación total o por IDs habilita continuar sin una segunda confirmación; una corrección de contenido obliga a mostrar nuevamente sólo los textos cambiados. Silencio, ambigüedad o una reacción no explícita no son aprobación.
19. **Revalidar y publicar.** Tras aprobación, volver a leer head SHA y diff del PR y confirmar que cada `path`/`line`/`side` sigue vigente. Si cambió una posición, no publicar ese punto y volver al gate sólo para los comentarios afectados. Publicar los comentarios seleccionados preferentemente en una única review con `event: COMMENT`, comentarios inline de un párrafo corto y un body con una frase de veredicto más un máximo de tres bullets materiales; no usar `position` cuando están disponibles `line` y `side`. No publicar findings descartados, no aprobados ni ya comentados.
20. **Verificar y cerrar.** Leer la review creada, comprobar autor, head, body, comentarios y URLs, y reportar qué IDs se publicaron u omitieron. Aplicar el output de la skill con scope gate, matriz de comportamiento crítico, coherencia PR/specs, estado de Zord, tests y límites; agregar la matriz RIO sólo cuando aplique. Actualizar el proyecto o hacer handoff a [[pr-description]] o implementación únicamente por pedido explícito.

## Validación

Success requiere:

```text
Scope Meli:                  PASS
Clasificación:               MELI_STANDARD | MELI_SIGNALS_RIO
Baseline/base real:          PASS
Diff clasificado:            PASS
Intención PR/specs:          PASS | GAP declarado
Fuente oficial RIO:          PASS | NO APLICA
Frescura/provenance:         PASS | DRIFT declarado | NO APLICA
Impact frontier:             PASS | NO APLICA
Zord preflight:              PASS
Zord execution:              PASS | DEGRADED declarado
RIO Zord identity:           GLOBAL/DISABLED/MANUAL | NO APLICA
RIO Zord execution:          PASS | NO APLICA
Findings reconciliados:      PASS
Critical behaviors mapped:   PASS
Critical behavior tests:     PASS | GAP material declarado
Coverage complement:         PASS | NO APLICA | GAP declarado
Human First comments:        PASS
Owner gate:                  PENDING | APPROVED <IDs> | REJECTED
Publication:                 NOT AUTHORIZED | PASS | PARTIAL | FAILED
Working tree preservado:     PASS
Resultado:                   COMPLETE | DEGRADED | BLOCKED | NOT_APPLICABLE
```

- `COMPLETE` exige scope Meli demostrado, Zord ejecutado, findings refutados, comportamientos críticos mapeados y working tree sin mutaciones atribuibles al review. En Signals/RIO exige además `rjara-rio-impact` global ejecutado y fuentes RIO navegadas con progressive disclosure; en Meli estándar ambos quedan `NO APLICA`. La publicación puede quedar `NOT AUTHORIZED` mientras espera el único gate humano.
- `DEGRADED` permite entregar evidencia útil cuando falta Zord, una fuente o una verificación, pero el límite debe aparecer en el encabezado y en `No verificado`.
- `BLOCKED` aplica si no se puede fijar la base, el diff mezcla cambios funcionales ambiguos, falta prueba efectiva de un comportamiento crítico con riesgo material, o en Signals/RIO falta o está sombreado `rjara-rio-impact`.
- `NOT_APPLICABLE` es la única salida permitida para un proyecto no Meli o cuya identidad Meli no puede demostrarse. No incluye análisis parcial ni ejecución de Zord.

## Rollback / recuperación

- El análisis no modifica código ni estado remoto. No ejecutar `zord fix`, commits, pushes ni creación de PR; publicar comentarios es la única mutación permitida y requiere el gate explícito del paso 18.
- Conservar el checkpoint inicial. Si una validación cambia el working tree, identificar el efecto exacto y pedir decisión cuando no sea inequívocamente generado por el comando actual; nunca usar una limpieza amplia.
- Los artefactos temporales de Zord se eliminan sólo al final y únicamente desde el path exacto retornado por `mktemp -d`; conservarlos si son necesarios para explicar un fallo o reanudar la revisión.
- Ante timeout o salida incierta de Zord, inspeccionar primero el JSON temporal y procesos activos; no relanzar hasta demostrar que la ejecución anterior terminó.
- Ante publicación parcial o incierta, leer primero reviews y comentarios existentes. No reintentar, editar ni borrar comentarios remotos hasta identificar los IDs realmente creados.

## Evidencia

```text
Review target:           <repo/PR/head>
Meli scope evidence:     <remote/owner/metadata/vault relation>
Review class:            <MELI_STANDARD | MELI_SIGNALS_RIO | NOT_APPLICABLE>
Base ref / merge-base:   <ref> / <sha>
Working tree before:     <estado>
Intent sources:          <PR/specs/tasks>
RIO sources:             <library pages/feature IDs/edges/app notes o NO APLICA>
Code SHAs:               <owner repos y HEADs observados>
Impact ledger:           <seeds y fronteras recorridas>
Zord preflight:          <zords/asignaciones>
RIO Zord identity:       <global/disabled/manual o NO APLICA>
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
