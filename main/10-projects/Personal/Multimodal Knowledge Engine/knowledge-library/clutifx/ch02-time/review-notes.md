# ch02-time — Notas de revisión (incertidumbres, adjudicaciones y limitaciones)

## Resultado de la revisión por minuto

18/18 minutos revisados (una llamada ONE-SHOT por minuto, transcript + frame base + frames bajo demanda + todos los claims del minuto). Resultado inicial: **94 SUPPORTED / 4 UNCERTAIN / 0 UNVERIFIED**, 0 contradicciones. Cobertura de keys verificada programáticamente (ningún claim sin resultado, ningún resultado huérfano).

## Adjudicaciones de integración (4 UNCERTAIN → SUPPORTED)

Todas las dudas fueron artefactos de frontera (evidencia citada que cae fuera del recorte de minuto del payload), no dudas de contenido. Cada claim lleva la nota en `claims.jsonl`:

1. **c-0067 (C-10)** — "la vela de las 5 es la que engloba ya todo New York": el payload del minuto 11 cortaba en s-001201; la cláusula completa está textual en s-001201+s-001203 [12:01–12:04].
2. **c-0072 (C-16)** — "la de la 1 te la ahorras": s-001304 [13:04–13:06] existe literal; caía en el payload del minuto 13.
3. **c-0047 (B-15)** — rango y objetivo en 3D: confirmado visualmente con f-000727 (extraído por el integrador sobre la duda del revisor; el revisor había capturado f-000730, ya en 2D).
4. **c-0048 (B-14)** — failure swing/SMT en semanal: f-000716 (00:07:16, chart 1W) muestra el bajo tomado (~1,4442) y el completado arriba; la causal "porque es un SMT que en Libra sí se llevó el bajo" es textual (s-000706) y la comparación con GBP es verbal — no visible en un frame único de EURUSD; anotado en el claim.

## Referencias visuales sin resolver (1)

- **Deíctico en 8 horas** [07:58–08:05, c-0056]: qué rectángulo exacto es el descartado ("este no") y cuál el válido ("este rango de aquí") no queda 100 % concluyente en frame estático (f-000758, f-000800, f-000806). La REGLA (cierre fuera ⇒ inválido) sí está clara y SUPPORTED. Ampliable con el mecanismo de complemento de la skill: `ffmpeg -ss 00:07:58 …` y re-juicio puntual del claim.

## Particularidades del transcript preservadas

- **Enumeración de aperturas de 4 h** [02:22, c-0011]: el instructor lista 5 p.m., 9 p.m., 1 a.m., 5 a.m., 9 a.m. — omite la vela de la 1 p.m.; después usa esa vela dos veces ("la de 4 horas nos abre a la 1" [09:24, c-0060]; "abre una nueva vela de 4 horas a la 1" [16:32, c-0096]). **Resuelto en la verificación final**: la pirámide en pantalla SÍ incluye la 1 p.m. — 4H: 1700, 2100, 0100, 0500, 0900, 1300 (f-000240, legible; el diálogo "Cambiar intervalo" sólo tapa una esquina inferior en f-000258). La omisión fue oral del instructor; los claims conservan la enumeración hablada literal y la imagen corrige el dato.
- **c-0051 (B-25)**: se preserva literal "hasta que no se formaron rangos bajistas otra vez, no volvió a subir el precio" aunque la formulación suene invertida; el revisor confirmó fidelidad textual y la dejó sin "corregir" para no inventar.
- **s-000548, s-001552**: frases truncadas por el instructor; el segundo se continúa en s-001602 y c-0090 une ambas sin añadir contenido (verificado por el revisor del minuto 16).
- **c-0066 (C-01)**: único claim con `epistemic: model_inference` (escenario DXY); el condicional "si el DXY está bearish/bullish" es textual, pero parte de la proyección del precio es del extractor. El revisor lo dejó SUPPORTED por fidelidad al condicional; la etiqueta de epistemic conserva la distinción.

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

## Leve exceso de frames bajo demanda

Presupuesto orientativo de la skill: ~0,5–1 frame/minuto bajo demanda. Aquí fueron 44 en 17 min (~2,6/min): los revisores de minutos con gráfico en pantalla usan su tope (3) casi siempre. Coste asumible (16 MB total); registrado como punto de metodología en `../METHODOLOGY-FEEDBACK.md`.
