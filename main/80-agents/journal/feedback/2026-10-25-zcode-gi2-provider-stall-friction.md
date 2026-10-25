---
type: session_feedback
schema_version: 1
scope: project
created: "2026-10-25"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
entities:
  - "[[Echo Futures — Runtime Pools]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - area/echo
---

# Feedback — cierre GI-2 vía workflow dinámico ZCode (2026-10-25)

1. **Cuota del plan interrumpe runs largos a mitad de especialistas**: el run dinámico (A+B en paralelo, ~7 h de fase) fue detenido por límite de 5 h del provider (code 1308) con trabajo a medio commitear en los worktrees. Lo que salvó la entrega: commits tempranos de los workers + notas de reanudación añadidas a los briefs en disco (lista de commits de corte + dirty files + «audita y continúa, no reinicies») para que el re-dispatch fresco auditará y continuara. Sugerencia operativa: en misiones con runs >4 h, exigir en el brief «commit cada avance verificable» y prever el brief de reanudación como artefacto de primera clase.
2. **Stall de 70 min por server_error del provider sin avance**: el runtime reintenta con backoff (correcto), pero el aviso de stall llegó después de más de una hora sin progreso y sin detalle de qué subagent estaba estancado; el snapshot de GetWorkflowRun sí lo mostraba. Sugerencia: el aviso de stall debería nombrar al subagent y al ask en curso para poder decidir esperar vs intervenir.
3. **Facademismos del workflow que costaron 3 reintentos de fill**: los specs de tabla (`TableSpec`) no aceptan `status`/`cardTitle`/`detail` (son de `BoardSpec`) y los nombres de actor deben ser únicos en TODO el run — re-preguntar a un especialista con su mismo nombre no compila; hay que despachar actores con nombre nuevo por etapa. Documentar el error con el campo culpable exacto acortaría el ciclo de diagnóstico.
4. **Doble registro de memoria del proyecto**: una compacción previa de la misma sesión había dejado una memoria «EN VUELO» del proyecto junto a la memoria canónica del proyecto; al cerrar hubo que consolidar dos archivos que describían el mismo estado. Sugerencia: al abrir una misión dentro de un proyecto con memoria canónica existente, actualizar ESA memoria (o enlazar la nueva como sub-estado) en vez de crear otra.
