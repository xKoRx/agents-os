---
type: session_feedback
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]"
  - "[[2026-09-20-polymarket-fivepoc-session-close]]"
aliases: []
confidence: high
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
  - area/personal
  - project/polymarket-engine
---

# Session feedback — Polymarket Engine Five-POC (2026-09-20)

## Contexto y resultado

El owner necesitaba concluir **cinco POCs funcionales y utilizables para probar hipótesis**, con ventana horaria acotada, y después dejar continuidad autosuficiente para agentes nuevos. Los receipts del ejecutor registraron `FIVE_POC_FINAL_CERTIFIED_BASELINE_READY` offline: branch local `feature/five-poc-integration`, código `56e8fac`, evidencia/certificación `c38f6c4`, HEAD `85e27ff`, M4 27 PASS/0 FAIL/0 NOT_RUN in-scope/5 diferidos live. Estos resultados fueron **reportados por el ejecutor**, no re-ejecutados por esta sesión documental. El handoff, índice, change log y session close se publicaron en `xKoRx/agents-os/master`; el engine continúa sin push/merge según el último receipt.

## Fricciones y errores propios que no deben repetirse

1. **Confusión del rol manager:** inicialmente devolví al owner un mandato para “el manager” cuando yo estaba desempeñando esa coordinación. El owner tuvo que corregirlo explícitamente. Regla: quien recibe responsabilidad de manager decide prioridades, ownership, baseline y gates; delega únicamente la ejecución que no puede realizar en su entorno y declara esa frontera con precisión.
2. **Planificación después del arranque:** presenté prerrequisitos como si las tres nuevas POCs aún pudieran detenerse, cuando el owner ya había lanzado sus sesiones. Lo correcto fue reconciliar los gates sobre el trabajo activo, preservar worktrees y diseñar refactor sólo *después* de la implementación.
3. **Mandato poco visible en la respuesta:** el owner tuvo que pedir varias veces “sólo el prompt/mandato”. Para una instrucción de ejecución, entregar **el texto íntegro en la respuesta**, autocontenido y directamente copiable; no delegar contenido esencial a un elemento UI, resumen ni una invitación a pedirlo otra vez. Si solicita «sólo prompt», no incluir análisis ni preámbulo.
4. **Confundir snapshot con ejecución:** el primer manager local cerró un turno tras crear worktrees/lanzar subagentes, sin verificar inicialmente que existieran procesos trabajando; el snapshot siguiente reveló que las tres POCs estaban al 0%. Regla: un spawn no es prueba de agente vivo, y un `STATUS_SNAPSHOT` no completa la misión. Verificar proceso/actividad, recibir commits y seguir hasta los gates del DoD.
5. **Tres subagentes vs límite dos:** el manager detectó que subsesiones previas seguían vivas. Es obligatorio inventariar sesiones antes de lanzar más, limitar a dos subagentes activos y separar writers/worktrees; detener duplicados sólo en checkpoints seguros.
6. **Aceptación sólo por tests vs operabilidad:** 34/34 paquetes y M4 no-live no bastan para `RESEARCH_READY`. La validación valiosa fue ejecutar cinco verticales operacionales, diez BASE/VARIANT, guardar artifacts y comprobar que los parámetros cambian resultados sin editar core. Mantener `IMPLEMENTATION_PASS`, `PIPELINE_PASS`, `DATA_READY`, `REAL_DATA_READY` y `HYPOTHESIS_VALIDATED` como estados distintos.
7. **Aserciones históricas/documentación stale:** índice aún apuntaba a v06 después del cierre v07; frontmatter/progress de notas largas pueden conservar 0% e hitos anteriores. Un cierre debe actualizar el índice de entrada y registrar precedencia temporal sin sobrescribir historia ni usar reemplazos inseguros sobre archivos >450 KB con autosync.
8. **Cuidado con semántica de contadores y digests:** `accepted`, `baskets_planned` y `simulated_fills` son unidades distintas; `strategy_metrics` Weather es último bucket/frame, no agregado. `dataset_digest` identifica la serie de entrada; los bytes del contenedor pueden variar por `capture_id`/`boot_id`. Un cambio legítimo del reporting puede modificar `content_hash`: conservar evidence previa, versionar y explicar BEFORE/AFTER; no falsear hashes.
9. **No dejar bugs de reporting como deuda cosmética:** `notional_by_scenario` vacío y `reserve_held` leyendo una clave inexistente eran errores reales de resultados; se corrigieron en v07. Exigir datos interpretables antes de llamar a una POC instrumento de investigación.
10. **Adapter probado ≠ integrado:** PE-004 Catalog O tenía adapter verificado pero faltaba wiring de composición. El DoD debe comprobar camino CLI → composición → Catalog → ancla causal → observer → artifact/replay, no sólo tests aislados.
11. **Remoto ≠ local:** el engine final estaba únicamente en `feature/five-poc-integration` local. No afirmar publicación, review o certificación en origin a partir de un receipt local; primero verificar Git y obtener decisión del owner. En la sesión documental no se disponía de worktree engine; reportar los tests como `REPORTED`, no `REVERIFIED`.

## Qué funcionó y se debe repetir

- Base shared `9d0512a` congelada, worktrees independientes, manager único escritor de registries/composición, merge incremental y pruebas tras cada POC.
- Fixtures causales, clock seam determinista, registro único de factories, `engine fixture`, `experiment compare`, provenance `engine_sha`/`dataset_digest` y cinco mutation drills verificables.
- Correctivos finales separados, gates técnicos y M4 sobre SHA exacto, receipts-only commit sin delta de código, datos originales protegidos y LIVE_DISABLED.
- Nota de continuidad compacta junto a padre y guía, índice de recursos actualizado y journal de cierre; nueva sesión no depende del transcript de chat.

## Mejoras operativas propuestas para Agents-OS (NO implementadas aquí)

- En el contrato de manager: `AGENT_SPAWNED` y `AGENT_RUNNING_VERIFIED` como estados distintos; limitar la concurrencia y asignar escritor único por archivo compartido.
- En Session Close: checklist explícito `project snapshot → resource index → tasks/owners → code SHA vs receipt SHA → remote publish status → feedback → lint/Graphify` con `NOT_RUN` honesto cuando no existe runtime.
- En documentación pesada: un encabezado pequeño de estado vigente y nota de precedencia versionada; realizar ediciones quirúrgicas localmente bajo autosync, no reemplazar blobs largos truncados mediante API remota.
- Mantener una definición de research-ready sustentada en caso CLI real, artifact duradero, variante reproducible, comparación y costo marginal de experimentación; no convertir fixtures sintéticos en evidencia de edge.

## Pendientes / handoff

La próxima sesión debe entrar por [[Polymarket Engine — Continuidad Five-POC 2026-09-20]], confirmar HEAD local `85e27ff` y receipt v07, y preservar `LIVE_DISABLED`. Owner debe revisar `c915c11..85e27ff` y decidir merge/push. Después elegir **una** POC y un experimento falsable, validar datos reales point-in-time antes de afirmar `REAL_DATA_READY`; U-02, Weather/Catalog real y PE-004 W/SFG-06 continúan pendientes. No iniciar refactor general ni declarar `HYPOTHESIS_VALIDATED=YES` por resultados sintéticos.

**Feedback registrado por el agente documental; no se atribuyen estas observaciones textuales al owner salvo sus peticiones expresas de manager, prompt visible y cierre.**
