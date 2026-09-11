---
type: skill
schema_version: 1
name: signals-code-review
description: Revisar branches o Pull Requests de Rodrigo exclusivamente en proyectos Meli con evidencia del diff real, comportamiento crítico, specs y descripción del PR mediante la tool canónica Zord. En cambios de Signals/RIO agrega el Zord independiente rjara-rio-impact y contrasta posibles afectaciones transversales con la documentación oficial de RIO. Entrega findings breves con explicación, solicita una única validación humana y, sólo tras aprobación explícita, publica los puntos seleccionados y un resumen corto. No usar ni ejecutar Zord desde esta skill en proyectos no Meli o de identidad no demostrable.
scope: user
created: "2026-09-11"
updated: "2026-09-11"
entities:
  - "[[Meli]]"
  - "[[RIO]]"
  - "[[local-agents-pipeline-cli]]"
  - "[[ads-signals-knowledge-library]]"
related:
  - "[[rjara-agent-profile]]"
  - "[[rjara-meli-work-preferences]]"
  - "[[pr-description]]"
  - "[[signals-code-review-runbook]]"
  - "[[human-first-technical-writing]]"
aliases:
  - review de código Signals
  - RIO code review
  - revisión transversal RIO
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/user
  - action/code-review
  - area/meli
  - app/rio
  - tech/zord
  - tech/agents-os
---

# signals-code-review

## Purpose

Revisar cambios de Rodrigo exclusivamente en proyectos Meli combinando intención documentada, delta real de código, comportamientos críticos y revisión independiente de Zord. Cuando el cambio pertenece a Signals/RIO, sumar una pista aislada de impacto transversal mediante `rjara-rio-impact`, sin brief ni conclusiones del coordinador, y contrastarla con fuentes oficiales de RIO. El flujo es semiautomático: el agente investiga, verifica y redacta; Rodrigo es el único gate antes de publicar; una aprobación explícita habilita la publicación automática de los puntos seleccionados y un resumen corto. La skill decide alcance, prioridad, suficiencia y veredicto; el runbook enlazado posee la recolección y publicación mecánicas.

Trigger boundary:

- **Sí:** code review de una branch o PR cuya pertenencia a Meli puede demostrarse. Todo proyecto Meli usa Zord; Signals/RIO agrega revisión cross-app oficial.
- **No:** cualquier proyecto no Meli o cuya identidad Meli no pueda demostrarse, escritura de código, aplicación de fixes, creación/publicación de PR o redacción de su descripción. Fuera de Meli esta skill termina como `NOT_APPLICABLE` antes de invocar Zord y no cae a una revisión genérica.
- **Handoff:** descripción de PR → [[pr-description]]; correcciones → workflow de implementación autorizado; ejecución mecánica → `../../memory/public/runbook/signals-code-review-runbook.md`.

## Minimal Read

Leer sólo:

1. `../../memory/public/runbook/signals-code-review-runbook.md` al ejecutar una revisión.
2. `../../memory/public/user-preference/rjara-meli-work-preferences.md` si el contexto Meli no está cargado.
3. `../../../30-resources/tools/local-agents-pipeline-cli.md` antes de resolver o ejecutar Zord.
4. La skill [[human-first-technical-writing]] al explicar findings o redactar comentarios para el autor del PR.
5. La skill [[pr-description]] únicamente si el usuario también solicita la descripción del PR.
6. Las fuentes oficiales de RIO indicadas por el runbook únicamente cuando el scope demostrado sea Signals/RIO.

## Procedure

1. **Aplicar el gate Meli.** Demostrar la identidad del repo o PR mediante remoto/owner, metadata corporativa o una relación canónica del vault; la ubicación del checkout o una mención del usuario no bastan por sí solas. Si es no Meli o queda incierto, devolver `NOT_APPLICABLE`, explicar la evidencia faltante y terminar antes de leer documentación RIO o invocar Zord.
2. **Fijar la frontera.** Confirmar repositorio o PR, branch, base real, working tree y alcance solicitado. Separar regresión introducida, comportamiento heredado y cambios locales; no ampliar el PR para corregir problemas ajenos.
3. **Reconstruir la intención.** Contrastar descripción del PR, SPEC funcional, SPEC técnica, tasks y criterios de aceptación disponibles. Una fuente ausente o contradictoria es un gap explícito, no permiso para inventar intención.
4. **Clasificar el dominio.** Todo proyecto Meli ejecuta la revisión estándar de Zord. Sólo un cambio demostrado como Signals/RIO abre el frente transversal: extraer seeds del diff —contratos, eventos, endpoints, topics, scopes, estados, persistencia, configuración, dependencias y component types— y seguir sus relaciones confirmadas en RIO.
5. **Obtener revisión independiente.** Ejecutar Zord mediante el runbook y conservar su salida separada. En Signals/RIO incluir `rjara-rio-impact`, deshabilitado por defecto y de source global, sin modificar su prompt ni pasarle prioridades, sospechas o findings previos; el coordinador sólo selecciona el diff y activa el revisor. Si Zord estándar no puede correr, marcar `DEGRADED`; si el revisor RIO falta o está sombreado, bloquear la revisión Signals/RIO hasta restaurar su identidad.
6. **Revisar por riesgo.** Priorizar corrección, compatibilidad de contratos y datos, seguridad, idempotencia/concurrencia, resiliencia, escalabilidad y observabilidad; después modularidad, SOLID y clean code; cerrar con KISS/YAGNI, código muerto, documentación y estilo realmente enforced. Un argumento de escalabilidad necesita carga, cardinalidad o failure mode plausible; una abstracción para un caso futuro pierde contra KISS/YAGNI.
7. **Auditar comportamiento crítico.** Derivar desde intención, contratos y diff cuáles son las funcionalidades cuyo fallo rompería comportamiento de negocio, seguridad, datos, compatibilidad, disponibilidad o convergencia. Para cada una, comprobar tests que observen resultados, estados, contratos y side effects relevantes, no la estructura interna del código. Los tests motivados por coverage son válidos como complemento; no sustituyen la evidencia sobre comportamientos críticos.
8. **Reconciliar evidencia.** Validar cada finding de Zord y, sólo para Signals/RIO, cada hipótesis documental contra el diff y código vigente de productor y consumidor. Clasificarlo como confirmado, plausible, descartado o no verificable y declarar aplicaciones afectadas cuando corresponda.
9. **Preparar el gate humano.** Aplicar [[human-first-technical-writing]] y pasar a Rodrigo una lista breve de puntos con ID, severidad, ubicación, qué ocurre, por qué importa, evidencia y comentario propuesto. Preguntar una sola vez cuáles publicar: todos, IDs seleccionados o ninguno.
10. **Publicar sólo tras aceptación.** Una aprobación explícita autoriza publicar automáticamente únicamente los puntos aceptados, idealmente en una sola review con comentarios inline y un resumen corto. Después verificar el resultado remoto y devolver links; no pedir una segunda confirmación salvo que el PR haya cambiado y las posiciones ya no sean válidas.

## Output

```text
Scope gate: MELI | NOT_APPLICABLE — <evidencia>
Estado de ejecución: COMPLETE | DEGRADED | BLOCKED | NOT_APPLICABLE
Veredicto: APROBADO | APROBADO CON RESERVAS | BLOQUEADO | NO REVISADO — <razón>
Base: <head> ← <base real> · <commits/archivos/+add/-del>
Evidencia: <PR/specs/código/Zord/tests y, si aplica, docs RIO>

Findings:
  [severidad] <confirmado|plausible> · <archivo:línea> · <escenario> · <acción>

Impacto transversal Signals/RIO:
  <seed> → <productor/consumidor/app> · <contrato o edge> · <riesgo> · <confianza>
  <o NO APLICA para Meli no RIO>

Comportamientos críticos:
  <comportamiento> · <riesgo si falla> · <test observable> · CUBIERTO | GAP

Coherencia de intención: <alineada | gaps/contradicciones>
Verificación: <comandos y resultados observados>
No verificado: <límites concretos>
Decisiones a preservar: <aciertos relevantes>

Propuesta para publicar:
  <ID> · <por qué importa en una frase> · <comentario breve>
Gate: ¿Publico todos, sólo <IDs> o ninguno?

Tras aprobación:
  Publicación: <review URL> · <comentarios publicados/omitidos>
```

## Hard Rules

- Esta skill es exclusivamente Meli. En proyectos no Meli o de identidad incierta no ejecutar Zord, no cargar RIO y no improvisar una revisión alternativa: devolver `NOT_APPLICABLE` y terminar.
- Todo proyecto Meli revisado por esta skill debe usar Zord. En Meli no RIO usar sólo el set estándar; en Signals/RIO agregar `rjara-rio-impact` mediante selección explícita.
- `rjara-rio-impact` debe permanecer global, manual y deshabilitado por defecto. Antes de usarlo verificar que `zord list` reporte source `global`; una copia repo-local con el mismo nombre lo sombrea y bloquea el flujo.
- El coordinador no puede enviarle a `rjara-rio-impact` un brief, áreas de preocupación, sospechas, findings de otros agentes ni conclusiones preliminares. Sólo puede activar el Zord y entregarle el diff y diffs relacionados como evidencia primaria.
- Para Signals/RIO: código vigente del servicio owner > `ads-signals-knowledge-library` > RIO Atlas y fichas del vault. La documentación orienta el traversal; nunca prueba por sí sola el comportamiento actual.
- `Zord` siempre significa la tool canónica [[local-agents-pipeline-cli]]. Resolverla desde su nota y source registrados; no buscar alternativas, reconstruirla ni ejecutar `zord add` salvo pedido explícito de desarrollo de la herramienta.
- Verificar frescura y confidence antes de usar documentación para una decisión sensible; si el manifest está stale, contrastar con los HEAD relevantes y declarar el drift.
- Cada finding requiere archivo y línea verificables, escenario concreto, evidencia y clasificación branch/heredado/local. Cero findings es un resultado válido.
- Zord es una señal independiente, no una autoridad. No copiar findings sin refutarlos ni declarar `COMPLETE` si la ejecución requerida de Zord faltó.
- Una búsqueda acotada no prueba ausencia: cubrir productores, consumidores, tests, fixtures, migraciones, recursos y repos relacionados, o redactar el límite exacto de lo buscado.
- No usar SOLID, clean code ni escalabilidad como excusa para sobrearquitectura. Preferir la solución más pequeña que satisface el contrato y los riesgos demostrados.
- La unidad de validación es el comportamiento crítico, no una clase, método o línea. Coverage puede justificar tests adicionales, pero nunca define por sí solo qué está suficientemente probado.
- Un comportamiento crítico sin test efectivo es un finding material aunque el coverage total esté verde; cada gap debe nombrar el escenario observable que falta.
- El análisis es read-only. No aplicar `zord fix`, editar código, crear el PR ni cambiar su descripción; la única mutación permitida por esta skill es publicar comentarios aprobados explícitamente por Rodrigo.
- Antes del gate humano no se publica nada. La aprobación puede ser total o por IDs y autoriza una sola ejecución; cambios posteriores del contenido requieren nueva aprobación.
- Todo comentario y resumen en nombre de Rodrigo debe aplicar [[human-first-technical-writing]], ser preciso, conciso, cordial y explicar causa → efecto → acción sin convertir el review en una guía extensa. Cada comentario usa un párrafo corto; el resumen usa una frase de veredicto y como máximo tres bullets de temas materiales.
