# ch02-time — Notas de revisión (incertidumbres, adjudicaciones y limitaciones)

## Resultado de la revisión por minuto

18/18 minutos revisados (una llamada ONE-SHOT por minuto, transcript + frame base + frames bajo demanda + todos los claims del minuto). Resultado inicial: **94 SUPPORTED / 4 UNCERTAIN / 0 UNVERIFIED**, 0 contradicciones. Cobertura de keys verificada programáticamente (ningún claim sin resultado, ningún resultado huérfano).

## Adjudicaciones de integración (4 UNCERTAIN → SUPPORTED)

Todas las dudas fueron artefactos de frontera (evidencia citada que cae fuera del recorte de minuto del payload), no dudas de contenido. Cada claim lleva la nota en `claims.jsonl`:

1. **c-0067 (C-10)** — "la vela de las 5 es la que engloba ya todo New York": el payload del minuto 11 cortaba en s-001201; la cláusula completa está textual en s-001201+s-001203 [12:01–12:04].
2. **c-0072 (C-16)** — "la de la 1 te la ahorras": s-001304 [13:04–13:06] existe literal; caía en el payload del minuto 13.
3. **c-0047 (B-15)** — rango y objetivo en 3D: confirmado visualmente con f-000727 (extraído por el integrador sobre la duda del revisor; el revisor había capturado f-000730, ya en 2D).
4. **c-0048 (B-14)** — failure swing/SMT en semanal: f-000716 (00:07:16, chart 1W) muestra el bajo tomado (~1,4442) y el completado arriba; la causal "porque es un SMT que en Libra sí se llevó el bajo" es textual (s-000706) y la comparación con GBP es verbal — no visible en un frame único de EURUSD; anotado en el claim.

## Referencias visuales y preguntas abiertas

El deíctico de 8 horas de c-0056 quedó **parcialmente resuelto** en capas (B2, nota estructurada del claim): HECHOS (regla dicha y sustentada; niveles 8H 1,5803/1,4748 dibujados en f-000800/f-000806) · INTERPRETACIÓN VIGENTE (válido = 1,4748–1,5803, persistente tras el señalamiento; descartado = primera caja anclada ~1,5803) · INTERPRETACIÓN DESCARTADA (la lectura original del review M8 que invertía ambos papeles — refutada por el estado posterior en 08:06) · INCERTIDUMBRE RESIDUAL (referente exacto del rectángulo descartado no probado) → registrada como **q-ch02-001** en `OPEN-QUESTIONS.md`. La regla de invalidación (cierre fuera ⇒ inválido) conserva soporte textual independiente y no se degrada por la duda del deíctico.

## Particularidades del transcript preservadas

- **Enumeración de aperturas de 4 h** [02:22, [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0011|c-0011]]: el instructor lista 5 p.m., 9 p.m., 1 a.m., 5 a.m., 9 a.m. — omite la vela de la 1 p.m.; después usa esa vela dos veces ("la de 4 horas nos abre a la 1" [09:24, [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0060|c-0060]]; "abre una nueva vela de 4 horas a la 1" [16:32, [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0096|c-0096]]). **Resuelto en la verificación final**: la pirámide en pantalla SÍ incluye la 1 p.m. — 4H: 1700, 2100, 0100, 0500, 0900, 1300 (f-000240, legible; el diálogo "Cambiar intervalo" sólo tapa una esquina inferior en f-000258). La omisión fue oral del instructor; los claims conservan la enumeración hablada literal y la imagen corrige el dato.
- **c-0051 (B-25)**: se preserva literal "hasta que no se formaron rangos bajistas otra vez, no volvió a subir el precio" aunque la formulación suene invertida; el revisor confirmó fidelidad textual y la dejó sin "corregir" para no inventar.
- **s-000548, s-001552**: frases truncadas por el instructor; el segundo se continúa en s-001602 y c-0090 une ambas sin añadir contenido (verificado por el revisor del minuto 16).
- **c-0066 (C-01)**: único claim publicado con `epistemic: model_inference`; el condicional "si el DXY está bearish/bullish" resultó textual del instructor y fue **reclasificado a instructor_statement en P4** (ver abajo); hoy no queda ningún model_inference vigente.

## Garbles de ASR (preservados y anotados en claims)

| ASR | Real |
|---|---|
| "tartle sub" / "tarde sub" / "cartel sub" / "TartelSoup" / "start el sub" | Turtle Soup |
| "intratar del sub" | intra Turtle Soup |
| "fellow swing" | failure swing |
| "el dol" / "el doble" | el DXY |
| "Pablo III" / "power 3" | Power of 3 |
| "59" | minuto 59 (salida antes del cierre de la hora) |
| "Libra" | GBP (libra esterlina) |
| "pilando el dominio" | "pillando el dominio" |
| "el doble está veris" | "el DXY está bearish" |
| "temporadas" (s-000838) | temporalidades |
| "me olvidado en 45 minutos" (s-000051) | "me había olvidado de 45 minutos" |
| "entrar desde todo" (s-000444) | posiblemente "desde arriba" |

## Nomenclatura de frames

Tres frames extraídos por revisores nacieron con nombres fuera del contrato (`f-044000`/`f-045000` del minuto 4; `f-004800`/`f-004806`/`f-004823` del minuto 8 — horas en lugar de minutos). Fueron re-extraídos/renombrados determinísticamente a `f-000444`, `f-000450`, `f-000800`, `f-000806`, `f-000823` y los `frames_extracted` de esos reviews fueron corregidos con nota. Los revisores del resto de minutos nombraron correctamente.

En la remediación P2 se detectó y corrigió un sexto caso: el frame final parcial `f-170903.png` parseaba como 17h09m (fuera de duración); renombrado a `f-001703.png` (00:17:03) con referencias actualizadas. Los cinco nombres históricos inválidos quedan declarados en `.deprecated_frame_names` (un `historical_invalid_name` en los .md es registro de auditoría, no cita vigente; el validador los distingue).

## Leve exceso de frames bajo demanda

Presupuesto orientativo de la skill: ~0,5–1 frame/minuto bajo demanda. Aquí fueron 44 en 17 min (~2,6/min) más 3 añadidos por la remediación P1 (f-000440, f-000735, f-001110) = 47 on-demand, 65 total: los revisores de minutos con gráfico en pantalla usan su tope (3) casi siempre. Coste asumible (17 MB total); registrado como punto de metodología en `../METHODOLOGY-FEEDBACK.md`.

## Remediación P1–P4 (2026-10-18, post-review del Owner)

- **P1 provenance visual**: 41 claims auditados físicamente (27 visual_observation ∪ 38 visual_hint). Resultado, en categorías separadas (B3): **auditados = 41 · que recibieron frames = 36 · epistemic realmente cambiada = 5** (c-0031, c-0045, c-0055, c-0059: visual_observation→instructor_statement; c-0066: model_inference→instructor_statement). Las demás clasificaciones instructor_statement ya lo eran en la publicación original (13 en P1 + c-0056 se confirmaron, no se cambiaron). 23 visual_observation permanecen, todas con frame verificado en `evidence`; 48 referencias f- estructuradas en total; 0 cambios de statement o veredicto. Frames nuevos: f-000440, f-000735, f-001110 (este último se extrajo para c-0070, se verificó que NO muestra lo afirmado y NO se adjuntó como evidencia).
- **P4 c-0066**: adjudicación A — el condicional DXY es proyección hablada del instructor (s-001005/s-001010): reclasificada instructor_statement, SUPPORTED se mantiene por fidelidad textual.
- **P4 c-0056**: parcialmente resuelto (PARTIALLY_RESOLVED tras la recalificación B2 — ver sección anterior y q-ch02-001).
- **Validador**: `course-knowledge-extraction/scripts/validate_library.py` — RED capturado sobre el estado pre-reparación (V07×27, V08×38, V05 f-170903, V10 conteos, V11 históricos) y PASS esperado tras la reparación; manifiesto en `repair/REPAIR-BASELINE.json`.
