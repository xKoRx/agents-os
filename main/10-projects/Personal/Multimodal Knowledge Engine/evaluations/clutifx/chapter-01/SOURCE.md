# SOURCE — Clutifx Chapter 01

## Identidad del curso

| Campo | Valor |
|---|---|
| Curso | CURSO DE TRADING CLUTIFX |
| Origen canónico | share SMB del TrueNAS `192.168.31.91` (`aranea_storage`): `cursos/trading/discre/cluti/CURSO DE TRADING  CLUTIFX` (la carpeta lleva doble espacio antes de CLUTIFX) |
| Episodios | 12 (mp4 1080p30 + audio; ~1.4 GB totales) + un PNG del proveedor |
| Copia local usada | `~/mke/course/` (sync verificado contra el share; el run no modificó el share) |

## Capítulo 1 — ordering evidence

La identidad del primer capítulo se resolvió con la mejor autoridad disponible (no lexicográfico ciego):

1. **Nombres originales en el share SMB** (listado físico 2026-09-30): `Episodio 1 - Introducción.mp4`, `Episodio 2 - Time.mp4`, … `Episodio 12 - Psicotrading.mp4` — numeración explícita de episodios en el nombre canónico del curso.
2. **Correspondencia byte-exacta** entre el nombre original y el archivo local: `Episodio 1 - Introducción.mp4` = 136,600,238 bytes = `ep01-intro.mp4`.
3. La copia local conserva el prefijo `epNN-` y el título en el nombre (ep01-intro … ep12-psicotrading), consistente 1:1 con los 12 originales.

Conclusión: `ep01-intro.mp4` es el capítulo 1 ("Episodio 1 - Introducción"). Sin ambigüedad razonable alternativa.

## Ficha física del fuente

| Campo | Valor |
|---|---|
| Archivo local | `~/mke/course/ep01-intro.mp4` |
| SHA-256 | `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` |
| Tamaño | 136,600,238 bytes |
| Duración (contenedor) | 2043.937 s (34:03.9) |
| Video | h264 High, 1920×1080, 30 fps, yuv420p/bt709, ~398.5 kbps, 61,318 frames |
| Audio | AAC LC, 44.1 kHz, stereo |
| Timebase video | 1/90000, start_pts 0 |

## Derechos y manejo

- El curso es material autorizado por el Owner para procesamiento por MKE (mismo origen usado en la certificación física V1 del 2026-09-28).
- El video original NO se copia al repo ni al vault; este bundle sólo referencia su SHA-256.
- El transcript y las imágenes de review se derivan del fuente y se publican como evidence de evaluación dentro del proyecto MKE.
