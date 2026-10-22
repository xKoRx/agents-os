---
type: session_feedback
schema_version: 1
scope: project
created: "2026-10-22"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
entities:
  - "[[Echo Futures — Optimización de Campañas]]"
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

# Feedback — R01/último contrato (2026-10-21/22)

1. **Ventanas de contrato no preparables por tooling**: crear una ventana nueva (último contrato) exigió replicar a mano la derivación del generador (cuya ruta `/srv/echo-work` ni siquiera existe en Hefesto) y vencer 9 validaciones del motor una por una (close_safety, source_read_plan, schedule, exclusions...). Fricción: la preparación de ventanas no es un comando; es arqueología de spec. Sugerencia: un `prepare-window` sellado que derive base plan + availability + close_safety de un manifiesto de contrato.
2. **Tope de evidencia por tier no dimensionado para horizontes largos**: el tier longitudinal (2 GiB) se dimensionó con canarios; TG-F1 lo superó en campaña real. Sugerencia: dimensionar techos por sesiones declaradas en el plan, no por ventana de prueba.
3. **Reconciliador L3 mono-cuenta**: validado sólo con una cuenta viva; la primera campaña multi-cuenta real rompió la conciliación (D4). Sugerencia: fixture multi-cuenta en los tests del caracterizador.
4. **Estados de ejecución ambiguos en el adelanto al Owner**: mezclar «clasificadas/despachadas/completas/activas» indujo lectura errónea del avance. El censo exclusivo por intento físico (§3 del despacho) debió existir desde el primer reporte.
5. **D1 confirmó la lección de diseño**: un rechazo de admisión esperado no debe poder enlazarse con el replan del MM en un pump de efectos inmediatos sin acotación; el fix estructural (cap en sizing) es el dueño correcto, no el pump.
