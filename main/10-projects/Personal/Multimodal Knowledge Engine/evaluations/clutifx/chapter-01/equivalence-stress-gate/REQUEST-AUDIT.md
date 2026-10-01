# REQUEST-AUDIT — RequestJSON sanitizado de las 3 adjudicaciones live

Copias completas (request + response + usage + identidad) en `request-audit/*.json`, exportadas del journal durable `run-live/run.db` (`provider_invocations`, task `claims.equivalence_review`). Scan de secretos sobre el bundle: 0 hits (los requests viajan sin headers de transporte; la credencial nunca entra al journal).

Estructura común de los 3 requests (contrato congelado `claims.equivalence_review vmke.claims-equivalence-prompt.v1`, output schema `mke.claims-equivalence.v1`):

```text
target: claims-equivalence:<8-hex content-addressed>
review_contract: claims.equivalence_review vmke.claims-equivalence-prompt.v1
kind: <kind del canónico>
epistemic_class: <epistemic del canónico>
statement_a: <statement first-observed>
statement_b: <statement entrante>
Task: decide exactly one thing: do statement_a and statement_b express the same
material proposition... [clases materiales: negation, numbers, conditions,
qualifiers, direction, modality, scope; duda → DIVERGENT]
```

## 1. `cl-curso-intermedio-no-supone-problema@1` (o1→o4)

- Invocation: `17fcba74c1859c4631b1103f280679cf8ae25b62bd3ab75035b8b2593a427e1f`
- kind `claim`, epistemic `INSTRUCTOR_SAID`
- statement_a: "No haber realizado el curso intermedio no supone un problema."
- statement_b: "No haber hecho el curso intermedio no supone ningún problema."
- Respuesta: `{"schema":"mke.claims-equivalence.v1","verdict":"EQUIVALENT"}` — 1 intento, sin reissue
- usage: prompt 383 / completion 21 / total 404 tokens; response_id `gen-1790880482-uGw89jBS6Jwmfqk6T0da`

## 2. `cl-eurusd-subida-previa@1` (o1→o4)

- Invocation: `bce633373554cef50b0d77c34c4a8cca2aacfba70a98a4dd0927a181571780ba`
- kind `observation`, epistemic `VIDEO_OBSERVED`
- statement_a: "El EURUSD muestra una subida pronunciada en la parte previa de la gráfica."
- statement_b: "Antes de la caída reciente, el EURUSD muestra una subida pronunciada."
- Respuesta: `{"schema":"mke.claims-equivalence.v1","verdict":"EQUIVALENT"}` — 1 intento (los 196 completion tokens incluyen razonamiento breve previo al JSON; el parser exigió un único documento JSON y lo aceptó)
- usage: prompt 388 / completion 196 / total 584 tokens; response_id `gen-1790880484-Kyhahh6ILPDruE6eKUWA`

## 3. `cl-formato-similar-curso-intermedio@1` (o1→o4)

- Invocation: `10c13d82ff22399431709e3365f3f4935bf40a98e2f775b431854947658fc236`
- kind `claim`, epistemic `INSTRUCTOR_SAID`
- statement_a: "El formato del curso completo será parecido al del curso intermedio."
- statement_b: "El formato que seguirá el capítulo será algo similar al del curso intermedio."
- Respuesta: `{"schema":"mke.claims-equivalence.v1","verdict":"DIVERGENT"}` — 1 intento
- usage: prompt 386 / completion 132 / total 518 tokens; response_id `gen-1790880489-QkJ3D3QzidVnDXbjkewG`

## Observaciones de auditoría

- Los 3 targets del journal (`claims-equivalence:cl-…@1:w0002-o1->w0002-o4`) son etiquetas; el matcher de replay usa el marker content-addressed interno (`claims-equivalence:<8-hex>`), que hash-ea task+prompt+kind+epistemic+statement_a+statement_b — por eso el replay reusa los veredictos sin nuevas llamadas live.
- 0 reissues en equivalence (3/3 limpias al primer intento); 0 timeouts; 0 errores de provider.
- Ningún request de equivalence lleva imágenes (revisión puramente textual de las dos renderings, por contrato).
