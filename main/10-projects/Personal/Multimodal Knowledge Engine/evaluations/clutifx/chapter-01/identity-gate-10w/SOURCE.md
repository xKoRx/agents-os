# SOURCE — Clutifx ep01

| Campo | Valor |
|---|---|
| Curso | CURSO DE TRADING CLUTIFX |
| Capítulo | `ep01-intro.mp4` — "Episodio 1 - Introducción" |
| SOURCE_SHA256 | `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` |
| Rehash físico en esta misión | 2026-10-01, `sha256sum` sobre `~/mke/course/ep01-intro.mp4` — **MATCH EXACTO** |
| Duración | ~2043.94 s (34:03.9; container 510984127/250000 ns) |
| Tamaño | 136,600,238 bytes |
| Streams | 0: video h264 1920×1080 (ver `media-run/source.json` del runtime L0) |
| Transcript | `mke.transcript.v1`, 323 segmentos, `source_sha256` = SOURCE_SHA (ASR faster-whisper large-v3, es p=1.00, corrida 2026-09-30) |

Binding verificado para L0 reuse:

1. Source rehasheado byte-exacto contra el SHA canónico.
2. `media-run/source.json` (`mke.source.v2`) declara el mismo `sha256`/`source_id`.
3. `transcript.json` declarado `bound` al mismo `source_sha256`.
4. Evidencia del media-run: 1040/1040 requests `COMPLETE`, 1040 filas `evidence` commiteadas (verificado read-only contra `media-run/run.db`).
5. El diff `cc13a121..ef53530` (remediation + F-ADV-01) no toca ningún archivo L0 (media/evidence/ASR/windows policy); el pipeline además re-hashea el video contra el manifest fail-closed al arrancar el run.

`L0_REUSED = YES`.
