---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Cuánto arriesgar por operación]]"]
last_verified: "2026-10-24"
confidence: "high"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/axi-select/edge-score-a-fondo-que-mide-por-que-cuesta-tanto-llegar-a-90-y-que-podemos-hacer"
related: ["[[IMOX]]"]
---

# IMOX - Cuánto arriesgar por operación

## Síntesis vigente

Informe cuantitativo adicional suministrado por Rodrigo junto a las descargas de los posts, con permiso explícito para documentarlo. Compara sizing y distribución del riesgo, separando caso teórico, retos simulados, portfolios y perfiles de cola. Se relaciona con [[IMOX - 19 frenos de drawdown comparados]] y [[IMOX - Axi Select - Edge Score y límites de su interpretación]].

## Conocimiento extraído

El informe declara 1.266 estrategias de SQX, 12 activos y datos 2018–2026 para distintas partes del estudio. No todas las tablas usan esa muestra: distingue casos base, portfolios de 2–40 estrategias y un análisis específico de colas de 93 estrategias.

- Modelos: riesgo fijo monetario, porcentaje fijo, volatilidad/ATR y fracciones de Kelly/Optimal f; además evalúa reparto entre estrategias y activos. Los modelos de sizing de una EA y los pesos de portfolio son decisiones distintas.
- La unidad R permite comparar lotajes, pero un stop nominal no garantiza la pérdida real ante gap, slippage o salidas distintas.
- El caso base es ilustrativo: 100.000 de capital, 45 % de acierto y ganancia/pérdida 2:1. Un Kelly de 17,5 % no es riesgo recomendado para Rodrigo; la sensibilidad a pérdidas extremas lo reduce drásticamente.
- Reporta que diversificar de 2 a 40 estrategias mejora más el Calmar que elegir el mejor reparto, y detecta 27 de 93 estrategias con peor operación superior a 3R. No demuestra que contar más EAs siempre diversifique.
- Las tasas de aprobado de retos se calculan bajo supuestos del informe, no con cuentas reales futuras. Los riesgos 0,5–1 %, 2 % o Kelly fraccionado son parámetros comparados, no una recomendación de cuenta.
- Considera colas/CVaR para casos en que medir riesgo solo por stop subestima pérdidas; no sustituye validar calidad y comparabilidad del dato.

## Límites del diseño

Las estrategias son backtests; medias incluyen optimización y el autor separa algunas medianas OOS. Las simulaciones no incluyen flotante intradía, remuestrean días/operaciones sin preservar rachas largas y usan dispersión de 20 operaciones como proxy de volatilidad donde no hay ATR. Definir R con stop mediano puede subestimar pérdidas de trailing o salidas temporales.

Por esas razones, tasas de aprobación y rendimiento absoluto no se trasladan directamente a campañas o cuentas de Forge. No se reprodujeron cálculos ni se modificó riesgo.

## Evidencia y provenance

- [[IMOX - Fuente - Cuánto arriesgar por operación]] identifica el PDF `Cuanto arriesgar por operacion.pdf` recibido de Rodrigo.
- [Contexto relacionado de Circle: Edge Score y riesgo](https://comunidad.imoxtrading.com/c/axi-select/edge-score-a-fondo-que-mide-por-que-cuesta-tanto-llegar-a-90-y-que-podemos-hacer). El post menciona una guía de capital, pero no se verificó que ese sea el enlace de publicación original de este PDF.
- La URL exacta de descarga de Academia y el autor del archivo no están confirmados por la evidencia capturada; no se inventan.

## Límites y contradicciones

Documento suministrado por el usuario y leído localmente por autorización. Sirve como comparación de modelos y supuestos; queda pendiente resolver su locator original de Academia/Circle para provenance completa de origen.

## Origen candidato localizado — 2026-10-25

Ver [[IMOX - Publicación de asignación de riesgo por operación]] y su fuente. Falta cotejo de la descarga: esta nota conserva la lectura del PDF suministrado, no se convierte en otro post ni pierde su extracción anterior.
