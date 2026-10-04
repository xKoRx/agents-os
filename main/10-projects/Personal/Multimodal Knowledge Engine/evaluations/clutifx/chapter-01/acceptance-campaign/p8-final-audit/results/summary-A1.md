# P8 Final Audit — A1 · FULL CLAIM AUDIT (w0001–w0033)

- Run auditado: **candidato rerun @ 19b44c1** (`/home/kor/mke/clutifx-ch01-rerun-20261003/run-rerun/claims.jsonl`), fuente: corpus P1 por ventana.
- Alcance: **27 ventanas aceptadas** de w0001–w0033. Excluidas por rechazo (cubiertas por otro worker): w0004, w0006, w0009, w0013, w0029, w0032.
- Método: sin muestreo. Cada claim verificado contra transcript (cita textual) y, para claims visuales (niveles de precio, colores, rectángulos, etiquetas de UI, temporalidad), lectura directa del PNG citado (~55 frames leídos, agrupados por ventana).

## Cifras

| Métrica | Valor |
|---|---|
| Claims auditados | **221** |
| CORRECT | **206** (93.2%) |
| DUPLICATE | **10** (4.5%) |
| PARTIAL | **4** (1.8%) |
| WRONG | **1** (0.5%) |
| OVERGENERALIZED / UNVERIFIABLE | 0 / 0 |
| MATERIAL=YES | 106 |
| **Precisión material parcial** (CORRECT+DUPLICATE sobre MATERIAL=YES) | **105/106 = 99.1%** |
| Precisión material sobre claims *publicados* | 105/105 = **100%** |
| MISSING_MATERIAL | **2** (w0010, w0033) |
| MISSING_NON_MATERIAL | 1 (w0014) |

## Claims no perfectos

- **WRONG (1):** `cl-nivel-eurusd-1-15067` (w0019) — afirma una línea horizontal en 1,15067; el frame p23400000 muestra solo las etiquetas del eje, sin línea. **No publicado** (GROUNDING_CONTRADICTED): el pipeline lo detectó correctamente; no contamina el store.
- **PARTIAL (4):**
  - `cl-campo-cambiar-intervalo-15` (w0019) — **publicado como SUPPORTED** pero el frame citado (p23490000) muestra «1 / 1 minuto», no «15». El resultado 15M es real (chart en 15M desde 262s); el valor tecleado no está capturado por la evidencia citada. Único claim publicado con evidencia que no sostiene el statement al pie de la letra.
  - `cl-referencia-inferior-1-14000` (w0028) — la caja azul está alineada con ~1,14066 y el texto está en edición («010600» ilegible); coherente con 1.14000 pero no verificable al dígito.
  - `cl-final-view-zoomed` (w0031) — la vista final cubre ≈ oct/nov 2024–abr 2025, no «sep 2024–mar 2025».
  - `cl-horizontal-level-104880` (w0031) — etiquetas de eje 1,04880 presentes, línea dibujada no visible; quedó sin publicar (correcto).
- **DUPLICATE (10):** repeticiones de la misma proposición por solape de segmentos ASR entre ventanas contiguas — w0002: `cl-curso-completo-estrategia-profundidad`, `cl-curso-intermedio-sienta-base` (→w0001); w0003: `cl-formato-similar-curso-intermedio`, `cl-sin-curso-intermedio-no-pasa-nada` (→w0002); w0011: `cl-la-estrategia-se-basa-principalmente-en-rangos` (→w0010); w0020: `cl-more-range-types` (→w0019); w0022: `cl-rangos-son-base-estrategia` (→w0021); w0027: `cl-rango-alcista-completo`, `cl-rango-bajista-completo`, `cl-rangos-van-completando` (→w0026). Ninguna es dañina; conviene política de dedup por utterance solapado.

## MISSING-KNOWLEDGE

- **w0010 (MATERIAL):** «tampoco tiene que ser negativa como tal» (asr-00017) — la flexibilidad de polaridad de la vela formadora del rango no está representada en ningún claim del store (0 hits de «negativa» en 1043 claims).
- **w0033 (MATERIAL):** «podrías hasta operar solo viendo el gráfico diario» (asr-00058) — el record existe (`cl-operar-solo-grafico-diario`) pero quedó **sin publicar** por fallo de schema del reviewer; el conocimiento publicado carece de él.
- **w0014 (no material):** «ejemplos reales de rangos» (puente dibujo→precio real); el contenido operativo sí está capturado.

## REGRESSION WATCH

1. **`cl-vela-negativa-mayoria` (viejo w0009, polaridad invertida) → ABSENT_AND_MISSING.** w0009 fue rechazada (identity divergence) y no genera claims. Busqué por semántica en todo mi rango: el conocimiento corregido («la vela tampoco tiene que ser negativa como tal», asr-00017, que vive en la fuente de w0010) **no está representado en ningún claim** del candidato; la única claim de polaridad del bloque es `cl-figura-derecha-vela-positiva` (w0008, CORRECT, sobre el dibujo). Registrado como MISSING_MATERIAL de w0010.
2. **`cl-entradas-sirven-para-encontrar-bias` (viejo w0011, relación invertida) → FIXED.** El candidato representa la relación correcta con dos claims: `cl-los-rangos-son-importantes-para-encontrar-entradas` (CORRECT vs asr-00021) y `cl-los-rangos-son-importantes-para-encontrar-el-bias` (CORRECT vs asr-00021/00022): el sujeto es «los rangos», no «las entradas». Caveat: la variante «entradas» quedó `UNSUPPORTED_REVIEW_UNAVAILABLE` (crash del proveedor de review) y no está publicada; la proposición invertida del run viejo no existe en el candidato.
3. **`cl-objetivo-hoy-rango-bullish-libra` (viejo w0037, 1.37489 vs 1.35843) → FUERA DE MI RANGO** (w0037 > w0033; pertenece al worker A2; mi rango no contiene claims de GBPUSD/Libra). En el store candidato los niveles están separados: `cl-gbpusd-borde-superior-rango-135843` / `cl-gbpusd-bullish-range-upper-135843` (borde superior 1,35843) vs `cl-gbpusd-objetivo-hoy-136031` y `cl-gbpusd-today-target-137489` (objetivo de hoy). **Flag para A2:** existen DOS claims de «objetivo de hoy» con cifras distintas (1,36031 y 1,37489), ambos publicados — ver cuál corresponde al dibujo.

## Hallazgos notables

1. **Fuga de publicación por artefactos del reviewer (8 claims con contenido CORRECTO sin publicar):** 4 por malformed verdict (schema `mke.claims-ground.v2` vs `v1`): w0003 `cl-informacion-curso-intermedio-no-relevante`, w0023 `cl-rango-bajista-completa-ordenes`, w0027 `cl-observar-rangos-diario-es-facil`, w0033 `cl-operar-solo-grafico-diario` (MATERIAL); 2 por strictness/composite: w0008 `cl-repeticion-sin-misterio`, w0015 `cl-vela-va-por-debajo-cierra`, w0031 `cl-evolution-many-timeframes`; 1 por crash del proveedor: w0011 `cl-los-rangos-son-importantes-para-encontrar-entradas` (MATERIAL). Es el mayor gap del run: ~3.6% de las claims de mi rango, incluida la mitad del fix de regresión #2.
2. **El mecanismo de rechazo funciona:** `cl-nivel-eurusd-1-15067` (CONTRADICTED) y `cl-horizontal-level-104880` (INSUFFICIENT) fueron correctamente retenidos.
3. **Higiene de evidencia:** varios claims citan evidencia fuera de su ventana (p.ej. w0017 usa asr-00052 y frames de 364–365s; los claims de parámetros de w0018/w0021/w0024/w0025/w0031 citan frames de minutos posteriores). No afecta la verdad (parámetros constantes del vídeo), pero debilita la trazabilidad por ventana.
4. **Calidad de niveles:** los 19 claims de niveles de precio verificados visualmente (1,15744/1,16148/1,15797/1,14748/1,15611/1.15803/1,13447/1,13572/1,14968/1,15352/1,15236/1,15365/1,15160/1,16148-d) coinciden todos con los dibujos; ningún error de dígito tipo run viejo en w0001–w0033.

## Veredicto A1

Población exhaustiva sin errores materiales publicados en w0001–w0033: 0 WRONG publicados, 1 PARTIAL publicado menor (`cl-campo-cambiar-intervalo-15`), 10 duplicados benignos. Los riesgos reales del rango son (a) la omisión material de w0010, (b) la no-publicación de 2 claims materiales correctos, y (c) los duplicados por solape ASR.

## FEEDBACK (Agents-OS)

- El run register del corpus P1 + digests generados por script hizo viable la auditoría exhaustiva de 221 claims en una pasada; mantener ese formato (window/claims/transcript/frames con `exists` y `cited_by_claim`).
- Fricción: las ventanas se solapan por segmentos ASR compartidos y el extractor vuelve a emitir la misma proposición en cada ventana (10 duplicados). Un dedup por hash de utterance+proposición en el extractor eliminaría la clase completa.
- Gap del pipeline de grounding: los malformed verdicts (schema id v2 vs v1) y el crash `vlm provider parse-structured` silencian claims correctos, incluidos 2 materiales. Conviene reintentar con el schema correcto y distinguir «insufficient evidence» de «reviewer malfunction» en `publication` (hoy ambos caen en UNSUPPORTED_*).
- Los frames citados por claims de parámetros incluyen miles de ítems fuera de ventana (p.ej. 70 frames para «EURUSD» en w0001); un límite de evidencia in-window para `observation` y un allowlist de parámetros constantes reduciría ruido y coste de auditoría.
- El encargo decía que w0037 estaba en mi rango para regression watch; está fuera (w0001–w0033). Sugerencia: derivar los 3 slugs de regresión a los workers por rango real y consolidar en el summary final.
