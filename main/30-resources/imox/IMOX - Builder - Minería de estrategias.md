---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - Builder - Minería de estrategias]]'
last_verified: '2026-10-24'
confidence: verified
aliases: []
tags:
- kind/resource
- area/trading
- topic/imox
created: '2026-10-24'
updated: '2026-10-26'
source_url: https://comunidad.imoxtrading.com/c/aportes-ia/builder-mineria-de-estrategias
related:
- '[[IMOX]]'
- '[[30-resources/applications/echo/echo-forge]]'
---

# IMOX - Builder - Minería de estrategias

## Síntesis vigente

Exploración con muchos builders cortos, dos vías de selección y cribado temporal previo al retester para reducir cómputo sin concentrar todas las candidatas en una sola firma de bloques.

## Conocimiento extraído

El autor observó que builders grandes con todos los bloques activos acababan concentrándose en pocos bloques. Propone varios builders pequeños en lugar de uno de 3.000–5.000 estrategias. Es observación de su experiencia con un generador estocástico, no un teorema sobre la cobertura del buscador.

- **P1:** selección por Net Profit, Ret/DD, Profit Factor y Sharpe.
- **P2:** selección por firmas únicas de indicadores/bloques y métricas, añadiendo candidatos que P1 descarta; eliminar duplicados entre vías.
- Filtros Genetic permisivos en IS; Ranking algo más exigente con IS/OOS. El autor corrigió su texto para aclarar que no usa un ranking agresivo.
- Antes del Retester, ejecuta MT5 en varias VMs y analiza informes HTML por año y mes para detectar rendimiento concentrado en pocos periodos.
- Caso principal: 301 candidatos → 77 consistentes; de 224 descartados, cinco sobrevivieron al retest pero el autor los juzga mediocres y 219 fallaron. Declara reducción aproximada de seis a dos días y supervivencia de 28 % en el grupo seleccionado.
- Comentario posterior: ocho builders de 500 estrategias; 200 por P1 y 200 por P2; tras deduplicar quedaron 345 y el cribado temporal seleccionó 54. Son casos distintos, no cifras de una misma corrida.
- Un caso analiza años completos 2022–2025 y otro 2019–2025. El umbral de consistencia 75 y riesgo fijo de 200 sobre 100.000 son ejemplos del autor; no parámetros aprobados para Rodrigo.

## Comentarios y matices

Asier describe builders de 20–40 minutos y sucesivas generaciones adaptadas por IA, y advierte que el ranking global puede expulsar familias de menor retorno aislado pero útiles para diversificar. Dice ocultar al agente el rendimiento del año reservado para no condicionar futuras propuestas. Edgar propone analizar los tipos supervivientes. La fórmula completa del score de consistencia no queda definida; se recalculan KPIs anuales y mensuales. El acuerdo útil es medir diversidad y coste, sin convertir un único score en verdad automática.

## Adjuntos y cobertura

Cuerpo, comentarios y respuestas adicionales revisados. Dos gráficos de dispersión anunciados; cifras extraídas del texto, sin reconstruir cada punto de las imágenes. No se recibió código de automatización.

## Interés para Forge

Prioridad de consulta: **Muy alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-ia/builder-mineria-de-estrategias).
- Autor: Edgar David Maldonado Acosta (@jaizdeda). Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Builder - Minería de estrategias]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

Faltan especificación reproducible del score, benchmark controlado de falsos descartes y evidencia fuera de muestra. Consultar un periodo reservado para elegir candidatos lo convierte en parte de selección; conservar un holdout independiente.

## Delta observado el 2026-10-26

Relectura del cuerpo y discusión accesible: Edgar aclara ranking algo más exigente que filtro genético, no agresivo; Asier advierte selección contra familias con menor métrica global. Queda verificar variedad real de supervivientes y respuestas anidadas. La revisita textual no renueva la verificación de todos los materiales previos.
