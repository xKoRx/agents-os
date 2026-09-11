---
type: skill
schema_version: 1
name: signals-code-review
description: Revisar branches o Pull Requests de Rodrigo en Meli/Signals con evidencia del diff real, specs y descripción del PR, una revisión multiagente mediante Zord y un análisis de impacto transversal apoyado en la documentación oficial de RIO. Usar ante pedidos de code review, revisión de branch/PR, validación de implementación o búsqueda de afectaciones cross-app. No usar para implementar fixes, redactar la descripción del PR ni hacer una revisión genérica fuera de Meli/Signals.
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

Revisar cambios de Rodrigo en Meli/Signals combinando cuatro planos de evidencia: intención documentada, delta real de código, impacto transversal en RIO y revisión independiente de Zord. La skill decide alcance, prioridad, suficiencia y veredicto; el runbook enlazado posee la recolección mecánica y los comandos.

Trigger boundary:

- **Sí:** code review de una branch o PR de Meli/Signals, validación de una implementación, evaluación de calidad o búsqueda de afectaciones cross-app en RIO.
- **No:** revisión genérica fuera de Meli/Signals, escritura de código, aplicación de fixes, creación/publicación de PR o redacción de su descripción.
- **Handoff:** descripción de PR → [[pr-description]]; correcciones → workflow de implementación autorizado; ejecución mecánica → `../../memory/public/runbook/signals-code-review-runbook.md`.

## Minimal Read

Leer sólo:

1. `../../memory/public/runbook/signals-code-review-runbook.md` al ejecutar una revisión.
2. `../../memory/public/user-preference/rjara-meli-work-preferences.md` si el contexto Meli no está cargado.
3. La skill [[pr-description]] únicamente si el usuario también solicita la descripción del PR.

## Procedure

1. **Fijar la frontera.** Confirmar repositorio o PR, branch, base real, working tree y alcance solicitado. Separar regresión introducida, comportamiento heredado y cambios locales; no ampliar el PR para corregir problemas ajenos.
2. **Reconstruir la intención.** Contrastar descripción del PR, SPEC funcional, SPEC técnica, tasks y criterios de aceptación disponibles. Una fuente ausente o contradictoria es un gap explícito, no permiso para inventar intención.
3. **Abrir el frente transversal.** Extraer del diff los seeds de impacto —contratos, eventos, endpoints, topics, scopes, estados, persistencia, configuración, dependencias y component types— y seguir sólo sus relaciones confirmadas en RIO hasta identificar productores, consumidores, owners, rollout y estados afectados.
4. **Obtener revisión independiente.** Ejecutar Zord mediante el runbook y conservar su salida separada. Si Zord no puede correr, marcar la revisión `DEGRADED`; no sustituirlo silenciosamente por una opinión única.
5. **Revisar por riesgo.** Priorizar corrección, compatibilidad de contratos y datos, seguridad, idempotencia/concurrencia, resiliencia, escalabilidad y observabilidad; después tests, modularidad, SOLID y clean code; cerrar con KISS/YAGNI, código muerto, documentación y estilo realmente enforced. Un argumento de escalabilidad necesita carga, cardinalidad o failure mode plausible; una abstracción para un caso futuro pierde contra KISS/YAGNI.
6. **Reconciliar evidencia.** Validar cada finding de Zord y cada hipótesis documental contra el diff y, cuando cruza una frontera, contra código vigente de productor y consumidor. Clasificarlo como confirmado, plausible, descartado o no verificable y declarar las aplicaciones posiblemente afectadas.
7. **Emitir decisión.** Entregar findings accionables por severidad, matriz de impacto transversal, coherencia PR/specs, verificaciones ejecutadas, gaps de evidencia y decisiones correctas que conviene preservar. No implementar ni publicar comentarios sin autorización explícita.

## Output

```text
Estado de ejecución: COMPLETE | DEGRADED | BLOCKED
Veredicto: APROBADO | APROBADO CON RESERVAS | BLOQUEADO — <razón>
Base: <head> ← <base real> · <commits/archivos/+add/-del>
Evidencia: <PR/specs/docs RIO/código/Zord/tests>

Findings:
  [severidad] <confirmado|plausible> · <archivo:línea> · <escenario> · <acción>

Impacto transversal:
  <seed> → <productor/consumidor/app> · <contrato o edge> · <riesgo> · <confianza>

Coherencia de intención: <alineada | gaps/contradicciones>
Verificación: <comandos y resultados observados>
No verificado: <límites concretos>
Decisiones a preservar: <aciertos relevantes>
```

## Hard Rules

- Código vigente del servicio owner > `ads-signals-knowledge-library` > RIO Atlas y fichas del vault. La documentación orienta el traversal; nunca prueba por sí sola el comportamiento actual.
- Verificar frescura y confidence antes de usar documentación para una decisión sensible; si el manifest está stale, contrastar con los HEAD relevantes y declarar el drift.
- Cada finding requiere archivo y línea verificables, escenario concreto, evidencia y clasificación branch/heredado/local. Cero findings es un resultado válido.
- Zord es una señal independiente, no una autoridad. No copiar findings sin refutarlos ni declarar `COMPLETE` si la ejecución requerida de Zord faltó.
- Una búsqueda acotada no prueba ausencia: cubrir productores, consumidores, tests, fixtures, migraciones, recursos y repos relacionados, o redactar el límite exacto de lo buscado.
- No usar SOLID, clean code ni escalabilidad como excusa para sobrearquitectura. Preferir la solución más pequeña que satisface el contrato y los riesgos demostrados.
- Tests críticos primero y coverage después; un porcentaje verde no compensa un camino crítico sin prueba.
- La revisión es read-only. No aplicar `zord fix`, editar código, publicar comentarios, crear el PR ni cambiar su descripción sin pedido explícito.
- Todo comentario redactado en nombre de Rodrigo debe aplicar [[human-first-technical-writing]] y pasar auditoría de tono antes de publicarse.
