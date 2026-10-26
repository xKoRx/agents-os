---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Axi Select - Edge Score y límites de su interpretación]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/axi-select/edge-score-a-fondo-que-mide-por-que-cuesta-tanto-llegar-a-90-y-que-podemos-hacer"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Axi Select - Edge Score y límites de su interpretación

## Síntesis vigente

El autor distingue las descripciones atribuidas a Axi de sus hipótesis para mejorar Edge Score. La fórmula y pesos no son públicos en la fuente.

## Conocimiento extraído

Caso del autor: score 86, Habilidad 78, Riesgo 91, Consistencia 88 y Experiencia 100. Describe un promedio ponderado de los tres primeros con descuento por experiencia; el cálculo de pesos iguales es solo ilustrativo.

- **Habilidad:** ganancias frente a pérdidas y grandes drawdowns; propone estudiar colas de pérdidas y relación Avg Win/Avg Loss.
- **Riesgo:** tiempo con flotante negativo, pérdidas por volumen, concentración entre EAs y gestión variable; propone limitar MAE y permitir que las ganadoras corran.
- **Consistencia:** suavidad del P/L y dispersión; plantea riesgo estable, diversificación y no subir lotes por rachas.
- **Experiencia:** el post atribuye a Axi umbrales de operaciones y días positivos. No se verificaron aquí contra condiciones oficiales.
- Sugiere proxies de Builder: MAE, pérdidas extremas, Stability/R² y meses rentables. Los llama aproximaciones, no la fórmula del score.
- Advierte que subir riesgo para acelerar el score tiene sesgo de supervivencia y puede perder la etapa. El reinicio y sus efectos no están suficientemente documentados en el post.
- Propone estimar pesos con datos aportados por miembros; no presenta una regresión concluida.

## Comentarios y matices

Hay casos de score 91–92 con drawdown y otro de caída de 90 a 65 tras pérdidas fuertes. Una cuenta perdió la etapa aunque mantuvo un score alto. El autor distingue historial del score y límite de pérdida de etapa: un score bueno no equivale a seguridad de la cuenta.

## Adjuntos y cobertura

Cuerpo y 13 comentarios accesibles revisados. Se identificaron dos capturas del autor y dos de miembros; no se extrajeron ni archivaron datos personales de cuenta de las capturas.

## Interés para Forge

Prioridad de consulta: **Media**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/axi-select/edge-score-a-fondo-que-mide-por-que-cuesta-tanto-llegar-a-90-y-que-podemos-hacer).
- Autor: Jefté Villarreal Herenas. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Axi Select - Edge Score y límites de su interpretación]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

Todas las reglas de cuenta, umbrales y términos se conservan como afirmaciones de la publicación, no como política vigente ni asesoría. No se verificó la fórmula ni causalidad de sus proxies. No perseguir el score cambiando reglas de validación sin evidencia.
