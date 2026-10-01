# SCALE-ESTIMATE — proyección lineal naive a 200 h / 400 GB

> **SINGLE-CHAPTER LINEAR ESTIMATE — NOT A CAPACITY PLAN.**
> Derivado EXCLUSIVAMENTE de las métricas observadas de este capítulo (34:03.9 = 0.5678 h; fuente 136.6 MB). La etapa L1 live sólo alcanzó 3/130 ventanas antes del FATAL contractual: las proyecciones L1 que dependen de reviews **no están observadas** y se marcan como tales. Sin clustering, workers ni paralelización: extrapolo el run serial de este capítulo.

## Observado (por hora de video)

| Métrica | Observado en ch01 | Por hora de video |
|---|---|---|
| ASR wall | 6463.6 s | 11,384 s/h (3.16× realtime) |
| media wall | 2995.0 s | 5,275 s/h |
| plan+windows wall | ~5 s | ~9 s/h |
| acquire wall | 3248.9 s | 5,722 s/h |
| **L0 wall total** | **12,712 s (3.53 h)** | **22,390 s/h ≈ 6.22 h wall por hora de video** |
| Frames inspeccionados (stride 1s) | 2044 | 3,601/h |
| Evidence adquirido | 1040 | 1,832/h |
| Ventanas (8 frames) | 130 | 229/h |
| Tokens L1 (recon, 3 ventanas) | 100,725 | — (ver abajo) |
| Claims propuestos (3 ventanas) | 56 (≈18.7/ventana) | ≈4,280/h si la tasa se mantuviera |
| Relations propuestos (3 ventanas) | 4 | ≈306/h ídem |
| Wall recon (3 ventanas) | ~450 s útil (≈150 s/ventana) | — |

## Proyección 200 horas (serial, misma tasa)

| Métrica | Proyección 200 h |
|---|---|
| L0 wall (ASR+media+plan+acquire+windows) | ≈ 1,244 h ≈ 51.8 días serial |
| Ventanas totales | ≈ 45,800 |
| Recon calls (1/ventana) | ≈ 45,800 |
| Tokens sólo recon (33.6k/ventana observado) | ≈ 1.54 B tokens |
| Review calls (NO OBSERVADO; suponiendo 1 review/record y ~20 records/ventana) | ≈ 916,000 calls (rango 700k–1.1M) |
| Tokens de reviews | NO OBSERVADO (null) |
| Calls totales provider | ≈ 0.96 M (recon + reviews estimados) |
| L1+L2 wall | NO OBSERVADO; recon serial solo ≈ 1,910 h; con reviews (latencia no medida) mayor |
| Costo | `null` — el adapter no reporta costo; dependiente de tarifario del modelo elegido |

## Relación fuente → artifacts generados

| Relación | Observado |
|---|---|
| Source GB → L0 artifacts GB | 136.6 MB fuente → 362 MB `media-run` (frames inspección 531 + evidence 1040 PNG 1080p + DB) ≈ **2.65×** |
| Source GB → review bundle GB | 136.6 MB → 6.8 MB bundle (subset de review; no es el ratio de storage del pipeline) |
| L1/L2 outputs | 0 bytes (bloqueado) |

Extrapolación simple 400 GB fuente: ≈ **1.06 TB de artifacts L0** al mismo perfil de extracción (PNG 1080p domina). Los PNG de evidence/frame son el driver de storage; un perfil JPEG o thumbs reduciría este factor (optimización futura, fuera de scope).

## Advertencias

1. Las cifras L1 son **parciales por diseño del run** (fatal @ 3/130): la única tasa live plenamente observada es la de reconstrucción (~150 s/ventana, ~33.6k tokens/ventana).
2. La tasa de 18.7 claims/ventana viene de 3 ventanas iniciales (intro + gráfico); la densidad de conocimiento puede variar por segmento del curso.
3. Con el bloqueo de identidad vigente, ninguna proyección L1 es alcanzable sin corrección del contrato (decisión Owner/Primary Manager, fuera de este scope).
4. `reported_cost = null`: el bundle no inventa costo.
