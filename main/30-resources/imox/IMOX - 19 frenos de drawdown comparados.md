---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - 19 frenos de drawdown comparados]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/laboratorio-a51b70/cuando-frenar-el-riesgo-19-frenos-de-drawdown-comparados"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - 19 frenos de drawdown comparados

## Síntesis vigente

Comparación de gestión de riesgo igualando la peor caída histórica al 7 %, para evitar que gane simplemente el método que menos arriesga.

## Conocimiento extraído

El post declara 12 carteras reales y 64 estrategias, 19 métodos y Monte Carlo de 2.000 caminos de tres años. Incluye edge recortado, reto de dos fases y tramo no usado para calibrar.

Familias mencionadas: escalones, CPPI, filtros de equity, pausas, volatilidad objetivo, freno por estrategia y corte diario.

Resultados reportados, todavía pendientes de reproducir:

- CPPI desde el máximo: 23–30 % más ganancia con la misma peor caída histórica.
- Con edge 0,10 R peor que el backtest: sin freno cae aproximadamente una de tres cuentas fondeadas en tres años, frente a 3–6 % con CPPI.
- Escalones que se detienen en mitad del riesgo protegen menos que continuar hasta ×0,1; reporta ocho veces menos cuentas perdidas.
- Cinco métodos rinden peor que no frenar, incluyendo algunas pausas tras rachas y filtros de equity.

El propio autor pide valorar la comparación relativa, no tomar cifras de backtest como promesas.

## Comentarios y matices

Un miembro relata una reducción de riesgo de 2 % a 1 % y una muestra de solo un mes. El autor está probando CPPI continuo, pero advierte que algunas carteras apenas mejoran con ese freno: necesita evaluación por cartera y elegir el intercambio entre recuperación y protección.

## Contraste con el informe descargado

Se revisó el informe de 30 páginas, con foco en diseño experimental, familias, resultados, límites y contrato del anexo; no se ejecutó su código.

### Diseño que cambia la interpretación

Declara unas 43.000 operaciones de backtest de 64 estrategias en 12 carteras, años 2015–2026 según cartera. Pondera estrategias inversamente a DD, retira mensualmente 80 % del exceso sobre capital inicial y toma decisiones de riesgo con el cierre del día anterior. Compara mediana entre carteras.

Monte Carlo remuestrea bloques de 20 días preservando coincidencia entre estrategias. Simula tres años, límites de 10 % total estático/5 % diario, estrés de −0,10 y −0,20 R y calibración temporal 60 %/40 %. Son supuestos del estudio, no condiciones de la cuenta de Rodrigo.

### Familias de las 19 variantes

Incluye riesgo fijo, proporcional al saldo, escalones de tres tramos, CPPI por pasos de uno y dos puntos, escalón con piso ×0,5, CPPI continuo, CPPI de suelo fijo, filtro de equity que reduce o para, pausa, volatilidad objetivo, freno por EA, corte diario solo/combinado y variantes de recuperación o ventana de referencia.

El CPPI desde máximo usa un multiplicador que disminuye al acercarse al límite, con un mínimo; el CPPI clásico de suelo fijo mide distancia al límite estático. No son intercambiables. El estudio atribuye buena parte de la protección al piso reducido, no solo al tamaño de paso.

### Límites e implementación descrita

La MAE se agrega suponiendo coincidencia intradía entre estrategias; operaciones multidiarias se ubican al cierre. La simulación decide diariamente y el gestor actúa al enviar órdenes. Con deterioro de −0,20 R ningún freno salva la mayoría de las cuentas.

El anexo propone una EA gestora que publica `SQ_FRENO_MULT` y parche de `FixedAmount_class.tpl` que multiplica riesgo de nuevas órdenes. No modifica posiciones abiertas; pendientes conservan su lote hasta recolocación. Usa balance, no equity. Si falta variable, opera con riesgo sin freno; si se detiene la gestora, permanece el último valor. El lote mínimo puede imponer más riesgo que el multiplicador pretendido. Son contratos críticos que habría que validar antes de una eventual implementación, no un parche aplicado a Forge.

## Adjuntos y cobertura

Post y dos comentarios revisados. Informe y anexo anunciados: https://academia.imoxtrading.com/documento/g0K7imSh-mFs; incluye parche SQX 144/145 y EA MT4/MT5. Ningún programa ejecutado. PDF recibido y revisado localmente con autorización.

## Interés para Forge

Prioridad de consulta: **Media**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/laboratorio-a51b70/cuando-frenar-el-riesgo-19-frenos-de-drawdown-comparados).
- Autor: Villarrubia. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - 19 frenos de drawdown comparados]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

No universalizar CPPI ni el 7 %. Faltan contraste independiente, sensibilidad y reglas completas del informe para reproducir sus resultados. Un drawdown histórico igualado no garantiza igual riesgo futuro.
