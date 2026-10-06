# PROVIDER RESILIENCE AUDIT · P8 final · MKE V2 Clutifx Ch01 · Run P7b

- **Run**: `e7bc387` · runtime `~/mke/clutifx-ch01-rerun2-20261004/run-rerun2/` · exit **4 INCOMPLETE**
- **Fuente única de verdad**: `run.db` (SQLite, 16 tablas). Los `journal-*.jsonl` en la raíz de chapter-01 son de una corrida anterior (Sep 30) y NO corresponden a este run.
- **Modelo**: `stealth/space-bunny-alpha` vía `https://openrouter.ai/api/v1` (strings del binario + `response_id gen-*`).
- **Duración total**: 20:03:16Z Oct 4 → 10:35:35Z Oct 5 = **14 h 32 m**, proceso único.

## 1. Veredicto ejecutivo

El candidato **sobrevivió una degradación de backend de 5 h 54 m (04:34:38Z → 10:29:18Z) sin babysitting**: cero crashes, cero hangs, cero resumes manuales, fail-closed por record, salida durable y exit diseñado (INCOMPLETE). El costo fue alto en superficie: **319/896 records (35.6%) terminaron `UNSUPPORTED_REVIEW_UNAVAILABLE`** y **38 ventanas (w0093–w0130) jamás se reconstruyeron** — ninguna fue recuperada después. El retry budget 2 + per-attempt timeout ~10 s es el ajuste **correcto** para proteger throughput (convirtió lo que la hipótesis "600 s/intento" proyectaba como ~3.2 días de freeze en **2.74 h** de dead time serializado), pero es **deuda operativa**: falta el mecanismo de *recovery* (reissue diferido post-tormenta), no el de *resistencia*.

## 2. Cronología del run (hecho 2)

| Hito | Timestamp (UTC) | Evidencia |
|---|---|---|
| Inicio real (1.ª fila budget_ledger) | 2026-10-04T**20:03:16.010Z** (w0001) | ledger #1 |
| 1.ª invocación (recon w0001) | 20:08:05.826Z | provider_invocations |
| Recon (claims.reconstruction) | 20:08:05Z → 05:30:26Z | 131 inv: 92 OK, 38 fail, 1 REJECTED semántico (w0028, 22:01Z) |
| Equivalence review | 20:30:15Z → 04:16:55Z | 59/59 VALIDATED, **0 fallos** |
| Grounding review | 05:33:37Z → 10:18:01Z | 870 inv/targets: 563 OK, 306 fail, 1 fatal |
| L2 composition | 10:25:16.935Z (1 llamada, VALIDATED, 28 objetos propuestos) | |
| L2 composition_review | 10:25:19Z → 10:34:26Z | 33 inv sobre 26 targets: 14 OK, 11 fail, 1 fatal, 7 REJECTED→reissue OK |
| Último ledger / última invocación | 10:34:21.721Z / 10:34:26.494Z | |
| Último commit de record | **10:35:35.940Z** | pipeline_records |
| Exit | `EXIT_CODE=4` — "553 supported, 343 non-supported records; durable partial output" | run-rerun2.log |

**Por qué el run continuó tras la tormenta**: el fallo de transporte es fail-closed **por record**, no aborta el pipeline. Cada request agotado se registra (`window w00XX: claims reconstruction unavailable: …` / record → `UNSUPPORTED_REVIEW_UNAVAILABLE`) y el pipeline avanza al siguiente target. El backend se recuperó (ver §4) con 2 h 37 m de run por delante, así que el pipeline siguió procesando targets nuevos — pero **nunca revisitó** los ya cerrados (0 targets fallidos re-validados después; cada target fallido tuvo exactamente 1 invocación).

## 3. Tormenta de transporte (hecho 1) — cuantificación exacta

**357 invocaciones fallidas de 1094 (32.6%)**. Desglose por clase (el brief decía "355 con `request timed out`"; corrección: 355 son retry-exhausted, de los cuales solo 309 terminaron en timeout):

| Clase | n | Detalle |
|---|---|---|
| `transport [retry-exhausted]` | **310** | 309 "request timed out" + 1 "network failure" |
| `parse [retry-exhausted]` | **44** | "response contains no choices" (respuesta vacía) |
| `read-body [retry-exhausted]` | **1** | "response body read failed" (09:56:53Z) |
| `parse-structured [fatal]` | **2** | "assistant content is not a valid JSON object" |

**Fases de degradación** (no fue un bloque homogéneo):

- **Fase A — black-out de transporte**: 04:34:38Z (recon **w0093**, primer fallo) → 07:57:20.966Z (último transport). 310 fallos. 100 % timeouts.
- **Fase B — flapping de cuerpo vacío**: 07:58 → 10:24. Backend responde pero devuelve `no choices` (44×) + 1 body-read + fatal #1 (08:15:58Z).
- **Fase C — flare final**: 10:25:19 → 10:29:18. 11 `no choices` en composition_review + fatal #2.

**¿Contigua o pulsante?** Las tres cosas, secuencialmente (fallos por cubo de 10 min):

```
04:30   # 1          06:50 ################## 18     09:00 ###### 6
04:40 #### 4          07:00 ################## 19     09:10 ############### 15
04:50 ####### 7       07:10 ################## 19     09:20 ##### 5
05:00 ####### 7       07:20 ################## 19     09:50 # 1
05:10 ###### 6        07:30 ################## 19     10:00 # 1
05:20 ############ 12 07:40 ################## 19     10:10 ### 3
05:30 ############# 13 07:50 ############## 14       10:20 ########### 11
05:40 ################### 19   (gap 07:50–08:40: 0)  10:30 (fatal 10:29:18)
05:50 ################### 19  08:40 ## 2
06:00–06:40 ###########19×5   08:50 # 1
```

- **Onset pulsante** 04:30–05:20 (mientras recon agotaba sus últimas ventanas: 12+26 fallos).
- **Muro contiguo saturado** 05:20–07:50: techo plano de ~19 fallos/10 min, **0 éxitos** en 05h y 06h. Recon y grounding afectados por igual en modo (mismo error), distinto volumen: recon 38 (onset), grounding 306 (muro). Equivalence escapó completa (terminó 04:16).
- **Aftershocks pulsantes** 08:40–09:20 y 10:20–10:29.

**¿Los 3 intentos colgaron a 600 s cada uno (900 s+ por record)? NO — refutado.** En la hora 06:00–07:00, 113 fallos consecutivos con espaciado **metronómico: p10=31.8 s, p50=31.8 s, p90=31.9 s, max=32.2 s**. El ciclo completo fallido (1 intento + 2 retries) costó **~32 s** ⇒ per-attempt timeout ≈ **10 s** (el binario expone el flag "per-attempt provider timeout in seconds"). Los `600` del config son otra cosa: `composition_timeout_seconds=600` (deadline de pipeline para composition) y `review_timeout_seconds=120`. Coste por record muerto: ~32 s en fase transporte, ~13–45 s en fase no-choices. **Dead time total serializado ≈ 2.74 h** (310 × 31.8 s), consistente con el span observado del muro (3.38 h onset→último transport). La hipótesis 900 s+/record habría proyectado ~3.2 días: ocurrió lo contrario.

## 4. Recuperación del backend (hechos 2 y 6)

- Último fallo de transporte: **07:57:20.966Z**. Primer éxito post-muro: **07:58:08.356Z** (10.7 s después, grounding `cl-grafico-rango-reiniciado`).
- 08h: **329 éxitos** (08:00:16 → 08:58:24) contra 4 fallos; 09h: 179 éxitos / 27 fallos; 10h: 54+13 éxitos / 16 fallos. Backend operational desde ~07:58Z, con flapping residual de cuerpos vacíos hasta 10:28:39Z.
- La composition VALIDATED a **10:25:16.935Z** fue **después** del último fallo de grounding (10:11:29.784Z) pero **antes** del flare de composition_review (10:25:19–10:28:39): aterrizó en una ventana sana y el flare empezó 0.1 s después de que se registrara su invocación.
- Tras el último fallo de todo el run (fatal, 10:29:18.766Z) hubo **13 invocaciones exitosas** (10:29:33 → 10:34:26), incl. 6 pares REJECTED→reissue→VALIDATED. El run terminó por diseño, no por proveedor.

## 5. Cero resumes manuales (hecho 3) — verificado

- `effects` = 0 filas · `effect_log` = 0 · `reconciliation_log` = 0 · `requests.reused_effect_key≠''` = 0 (tabla requests vacía en este modo).
- `budget_ledger`: ids **contiguos 1..2529**, timestamps estrictamente monótonos, un solo hilo de facturación.
- Sin artefactos WAL/lock; un único `run.db`; una sola línea `EXIT_CODE=4` en el log. **Proceso único, ledger continuo, 0 effects/resume.**

## 6. Los 2 fatals (hecho 4)

| # | Timestamp | Target | Qué pasó | Destino del record/objeto |
|---|---|---|---|---|
| 1 | 08:15:58.815Z | `claims-grounding:cl-pattern-many-timeframes` | parse-structured fatal: contenido del assistant no es JSON válido; response_json vacío | **Fail-closed**: record_outcomes `INTEGRITY_PASS / REVIEW_UNAVAILABLE` → claim publicada `UNSUPPORTED_REVIEW_UNAVAILABLE`, committed 10:35:35.940Z (último commit del run) |
| 2 | 10:29:18.766Z | `sko-review:sko-range-completion` | fatal **en el intento de reissue correctivo** (intento previo 10:29:18.680Z REJECTED semántico → reissue inmediato → mismo parse fatal) | **Fail-closed**: `sko/review.jsonl` REVIEW_UNAVAILABLE con razones `[reviewer_unavailable, reviewer_malformed_output/corrective reissue]` → `sko-range-completion@1` publicada `UNSUPPORTED_REVIEW_UNAVAILABLE` |

**¿Dejó el fatal algún objeto sin revisar? NO.** Cadena L2 completa: 28 propuestos → 2 descartados en integridad de composition (`L2 composition object discarded: sko-range-chain-stra…`, `sko-turtle-soup`) → **26 entraron a review → 26 con outcome terminal** (13 COMPOSITION_SUPPORTED, 1 COMPOSITION_UNSUPPORTED, 12 REVIEW_UNAVAILABLE) → **26 publicados** (12 SUPPORTED_BY_AUTOMATED_REVIEW + 1 UNSUPPORTED_CONTRADICTED + 1 UNSUPPORTED_PARTIAL + 12 UNSUPPORTED_REVIEW_UNAVAILABLE). Los 12 targets fallidos = exactamente los 12 SKO `UNSUPPORTED_REVIEW_UNAVAILABLE` (match de nombres verificado). "26 de 28 + este" del brief: los 2 que faltan son descartes de integridad previos a review, no víctimas del fatal.

## 7. Correlación tamaño/latencia vs tormenta (hecho 5)

- `length(request_json)`: FAILED avg **4,766 B** (max 9,288) vs VALIDATED avg **4,674 B** (max **77,973**). Por hora en grounding, medias FAIL/OK indistinguibles (~4.3 KB ambas).
- Requests de 2–9 KB morían en el muro mientras requests de **78 KB** pasaban sin problema a las 08h. **Sin correlación de tamaño: el outage fue sistemático a nivel backend**, no dependiente de payload ni contenido.
- Contraste de cadencia: recon OK p50 **262 s**/llamada (8 imágenes), grounding OK p50 **6.5 s**, review OK ~10–30 s; ciclo fallido **31.8 s** plano. El fallo no era "request lento", era request muerto.

## 8. Evidencia de degradación pre-muerte del endpoint en el journal (hecho 7)

- **No hay ningún "404" ni "No endpoints found" literal en el journal** (el journal persiste solo el string del último fallo por invocación; los status HTTP por intento no se journalizan).
- **Pero el journal sí registra la cascada de degradación previa**, en orden de gravedad creciente:
  1. timeouts (black-hole L7) 04:34–07:57 ×310,
  2. "response contains no choices" (endpoint vivo, cuerpo vacío) 08:40–10:28 ×44,
  3. "response body read failed" 09:56 ×1,
  4. "assistant content is not a valid JSON object" (contenido vacío/malformado) fatal ×2 (08:15, 10:29).
- Esa secuencia timeout→vacío→malformado es la firma clásica de un endpoint en proceso de des-routing. El journal termina 10:34:26Z; el 404 definitivo se observó fuera del journal (~Oct 5 tarde; probe 00:36Z Oct 6). El run murió de viejo antes de que el endpoint muriera del todo.

## 9. Presupuesto — nunca fue el cuello

calls 1094/2400 (45.6%) · images 2106/8000 (26.3%) · tokens 6,694,704/60M (11.2%). El INCOMPLETE no tiene nada que ver con presupuesto.

## 10. Veredicto de escala y deuda operativa (hecho 8)

**¿Sobrevivió 6 h de degradación sin babysitting? SÍ.** Proceso único de 14 h 32 m, aislamiento de fallos por record, fail-closed verificable en las 319 superficies, sin hang (peor caso 32 s/request muerto), sin intervención humana, salida durable y exit diseñado. Esto es resistencia de provider de grado producción en su capa de *contención*.

**¿Es el retry budget 2 + timeout el ajuste correcto? SÍ para contención, y conviene NO subirlo.** Un budget mayor o timeout mayor solo habría multiplicado el dead time (cada request muerto colgaría más), con el mismo destino fail-closed. La evidencia: 310 requests muertos costaron 2.74 h, no días.

**¿Es deuda operativa? SÍ — tipo MI-08 (reissue/resume para transporte), en tres piezas:**

1. **Reissue diferido post-tormenta (la pieza que falta y la más barata)**: 306 targets de grounding fallaron DURANTE el muro y el backend se recuperó a 07:58Z con 2 h 37 m de run restante y ~560 llamadas exitosas después. Un pase final que drene la cola `UNSUPPORTED_REVIEW_UNAVAILABLE` (307 objetos) + ventanas no reconstruidas (38), gated por un health-probe del proveedor, habría recuperado la mayor parte de la superficie perdida. El mecanismo de reissue correctivo **ya existe** para respuestas REJECTED de review (7 usos en este run) y para outputs malformados — solo falta extenderlo a retry-exhausted, que hoy tiene exactamente una oportunidad en la vida del record (0 targets re-validados).
2. **Journalizar el intento, no solo el ciclo**: persistir status HTTP y duración por intento (hoy solo sobrevive el string del último fallo). Con eso, la pre-muerte del endpoint (404/unroute) habría sido visible EN el journal en vez de inferirse por la cascada timeout→vacío→malformado.
3. **Persistir duración por request**: la tabla `requests` está vacía en este modo; la latencia de este audit se infirió del espaciado entre invocaciones. `started_at`/`ended_at` por invocación eliminaría la ambigüedad de `at_utc`.

**Saldo final**: 553/896 records soportados (61.7%) publicados como salida durable pese a la tormenta; 343 no-soportados de los cuales 319 (93%) son directamente atribuibles a la tormenta; el resto (24) son veredictos semánticos (insufficient/contradicted/partial) y colisiones de identidad deterministas (11 ventanas).

## FEEDBACK (Agents-OS)

1. **El journal de run.db es de grado forense y sostuvo un audit completo sin stdout**: `provider_invocations` + `budget_ledger` + `record_stages` + `pipeline_records` + `record_outcomes` permitieron reconstruir un run de 14.5 h (timeline, coste por record, cadencia, fail-closed por objeto) con solo SQL. Mantener ese nivel en futuros pipelines; es la diferencia entre auditar y adivinar.
2. **Mejoras concretas al journal** (detectadas al cuantificar): (a) `at_utc` de invocación es ambiguo (fin-de-ciclo inferido, no declarado) — añadir `started_at`/`ended_at`; (b) no se journalizan intentos individuales ni status HTTP — el fallo de proveedor se ve como string agregado, lo que impide distinguir 404/unroute de timeout real; (c) `requests` vacío en modo v2 — la latencia por request no es medible directamente.
3. **Higiene de timestamps**: el log del run (`run-rerun2.log`) no tiene timestamps y los mtimes de archivos están en hora local (UTC-3) mientras el journal está en UTC; la primera lectura produjo una discrepancia aparente de ~3 h (exit "10:30Z" del brief vs commits 10:35Z). Recomendación: UTC en logs y mtimes documentados.
4. **El patrón del brief funcionó**: los hechos venían marcados como cuantificables-y-verificables y 3 resultaron imprecisos (355≠todos "timed out": solo 309; exit 10:30Z vs 10:35:35Z; "26 publicados de 28 + este" vs 26/26 revisados con 2 descartes previos). Verificar contra el journal en vez de asumir el brief es lo correcto — seguir así.
5. **Bootstrap**: procedimiento de startup invocado una vez (VAULT_ROOT resuelto, entidad proyecto, modo one-shot, delta mínimo); feedback capturado aquí según mandato. Sin otras fases tocadas.
