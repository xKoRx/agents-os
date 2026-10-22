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

## Rectificación LC26 (2026-10-22, segundo bloque)

6. **Sobredeclaración del gate**: publiqué `TECHNICAL_ACTIVITY_GATE: ACREDITADO` con el censo v1 contradiciendo a la frecuencia (0 compras vs 1 compra) — la conjunción de gates no puede apoyarse en filas sin conciliar. Lección: el gate se emite DESPUÉS de reconciliar las filas que lo sostienen, nunca en el mismo pase que las produce.
7. **Extractores inconsistentes**: dos scripts leyendo campos distintos del mismo resultado produjeron censos opuestos; el campo ausente se volvió cero por `.get(...,0)`. Lección: métricas requeridas sin default; null visible.
8. **Promedio no es cobertura**: presenté medias ≥1/sesión como cumplimiento del objetivo diario; la matriz por sesión con ceros y rachas era el compromiso real del despacho.
9. **`NOT_EXERCISED` no es despejado**: reporté D1 como no-disparado en NQZ6 sin marcar que la ruta quedaba sin ejercitar; el gate D1 debió quedar abierto desde el primer informe.
10. **Identidad de derivados**: derivé el spec de ventana sin distinguir hash de contenido nuevo vs parent hash (manifest_identity reutilizado como procedencia); el despacho lo exige explícito para todo derivado.
