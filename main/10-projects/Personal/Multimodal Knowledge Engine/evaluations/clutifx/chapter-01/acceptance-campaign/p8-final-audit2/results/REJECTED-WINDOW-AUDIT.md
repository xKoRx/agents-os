# REJECTED-WINDOW-AUDIT — Capítulo 01 Clutifx, P7b @ `e7bc387` (49 ventanas rechazadas)

Auditoría de las 49 ventanas rechazadas fail-closed del candidato P7b (`clutifx-ch01-rerun2-20261004/run-rerun2`,
130 ventanas; 81 aceptadas / 49 rechazadas): **11 por identidad** (colisiones de identidad en reconstrucción de
claims) y **38 por transporte** (bloque contiguo w0093–w0130, `vlm provider transport [retry-exhausted]`).

- **Método**: idéntico al de `p8-final-audit/results/REJECTED-WINDOW-AUDIT.md` (@19b44c1). Para las 11 de identidad:
  razón exacta en `run-rerun2/run.db` → `pipeline_state.status_reasons` (array JSON de 719 entradas), material de la
  ventana leído del corpus (`p8-final-audit2/corpus/wNNNN.json`, claims/relations vacíos para las rechazadas), y
  cobertura probada contra el **store canónico** `run-rerun2/claims.jsonl` (766 claims + 104 relaciones) usando
  `records_introduced` por ventana de `analysis-p7b/coverage.json` (verificado: sus 130 dispositions reproducen
  exactamente las 49 rechazadas de este run — 38 `provider unavailable` + 11 `identity divergence` — y 870 records
  introducidos). Cada cobertura citada lleva record ID; los 81 ids citados se verificaron programáticamente contra
  `claims.jsonl` (100% existen). Frames visualmente inspeccionados: w0006 (p7920000: figura base pintada de negro
  junto a la vela blanca tomante con mecha) y w0008 (p10530000: esquema rotulado «rango alcista» con la figura
  duplicada seleccionada y paleta abierta). Para las 38 de transporte NO se auditó material en detalle: se registra
  window/reason y se cuantifica el material único del **bloque** (inventario de transcript deduplicado vs store).
- **Fecha**: 2026-10-05. Datos por ventana en `rejected-windows.jsonl` (mismo directorio).
- **Calibración**: método y granularidad de «proposición material» idénticos a los audits previos
  (baseline p1-audit 19 residuo; @19b44c1 10 residuo).

## Conteo de consecuencias

| Clase | Ventanas | N | Consecuencia |
|---|---|---|---|
| Transporte | w0093–w0130 (bloque contiguo) | **38** | `TRANSPORT_UNEXERCISED` (pérdida de extracción, no colisión semántica) |
| Identidad → NO_MATERIAL_LOSS | w0044, w0054, w0058, w0061, w0077 | **5** | todo el material vive en la ventana ganadora |
| Identidad → PARTIAL_MATERIAL_LOSS | w0006, w0008, w0023, w0062, w0073, w0084 | **6** | 1 proposición residual cada una |
| Identidad → MATERIAL_LOSS | — | **0** | — |

**Resultado global**: ninguna ventana rechazada por identidad perdió conocimiento material de forma íntegra
(0 MATERIAL_LOSS, igual que en los dos runs previos). El residuo **identidad-only = 6 proposiciones** (1 por
ventana en 6 ventanas), **bajo el umbral estricto de 19** (6 < 19 ✓) y el mejor de los tres runs auditados
(19 → 10 → 6).

### Ventanas de identidad con residuo (las 6)

| Ventana | Razón | Residuo no almacenado |
|---|---|---|
| w0006 | determinista kind (w0004, `cl-range-taking-candle-closes-inside`: claim vs rule) | «Esta [figura base] sería una vela bajista probablemente, así que la pintaremos en negro» — el repintado a negro está (w0010 `cl-figura-rectangular-relleno-negro`) y la vela tomante negativa también (w0009 `cl-figura-presentada-como-vela-negativa`); falta la interpretación bajista de la vela base |
| w0008 | determinista epistemic (w0007, `cl-rango-alcista`: INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «Es lo mismo pero al revés» (espejo del rango bajista) con vela probablemente positiva — el rótulo «rango alcista» (w0007/w0009) y las ediciones de la figura duplicada (w0009) están; la relación de inversión no (en P7 la almacenaba la propia w0008) |
| w0023 | semántica DIVERGENT (w0015, `cl-precio-completa-rango-bajista`: «central» vs «ahora») | «El precio utiliza esto para ir completando las órdenes y aparejando todo» (mecanismo de órdenes; 0 hits en store) |
| w0062 | semántica DIVERGENT (w0007, `cl-fuente-forex-com`) | «Los nombres no tienen mucha importancia, es solo para concretar más» (meta-regla de nomenclatura; 0 hits) |
| w0073 | semántica DIVERGENT (w0015, `cl-divisa-usd`) | «¿Cómo se puede intentar predecir? Lo vais a ver más adelante» (promesa de método; 0 hits «predecir») |
| w0084 | determinista epistemic (w0059, `cl-timeframe-8h`: INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «No hace nuevo alto en libra» — la pierna divergente del ejemplo SMT (el lado euro sí está: `cl-eurusd-nuevo-alto` w0083; la lectura «podría ser señal de reversión» queda genérica vía w0035/w0092) |

Patrón (coherente con @19b44c1): lo colisionado siempre queda en la ventana ganadora; el residuo son
**proposiciones adyacentes únicas** — interpretaciones de dibujo (w0006, w0008), mecanismos (w0023),
meta-reglas y promesas (w0062, w0073), mitades de un ejemplo visual (w0084) — que el ladder de identidad
no transfiere.

### Las 5 de identidad sin residuo

- **w0044** ≡ w0043 (`cl-candle-takes-range-low`: «vela en cuestión» vs «vela dibujada») → cubren w0043
  (low tomado, posible 4h, mechas por realismo) + w0045 (`cl-nueva-vela-abre-aqui`,
  `cl-rango-pendiente-cierra-adentro`, `cl-rango-pendiente-reacciona-y-sube`) → NO_MATERIAL_LOSS.
- **w0054** kind vs w0053 (`cl-rango-pendiente-doble-alcista`) → el resumen completo vive en w0053 (19 records);
  «objetivo diario = el del ejemplo» en w0056 (`cl-objetivo-diario-ejemplo-anterior`); «quedado claro» en
  `cl-punto-ya-claro` (w0013) → NO_MATERIAL_LOSS.
- **w0058** ≡ w0043 → w0059 almacena casi literal el pasaje en tiempo real (`cl-vela-toma-low-tiempo-real`,
  `cl-vela-empieza-reaccionar`, `cl-rango-anticipable-antes-cierre`, `cl-anticipacion-rango-mas-avanzada`) →
  NO_MATERIAL_LOSS.
- **w0061** epistemic vs w0059 → la clasificación reiniciado/pendiente está íntegra en w0060
  (`cl-rango-bajista-objetivo-bullish-reiniciado`, `cl-rango-alcista-objetivo-bullish-pendiente`,
  `cl-rango-caso-contrario-tendencia`) → NO_MATERIAL_LOSS.
- **w0077** ≡ w0076 (la paráfrasis difería solo en la palabra «ahora») → w0076 + w0078 almacenan la regla,
  el cierre-fuera→ya-no-rango, la eliminación y hasta el gesto «la dejo aquí marcada»
  (`cl-referencia-espera-marcada`) → NO_MATERIAL_LOSS.

## Bloque de transporte w0093–w0130 (23:37–34:02)

- **Razón uniforme en las 38**: `claims reconstruction unavailable: vlm provider transport [retry-exhausted]:
  retry budget of 2 exhausted; last failure: request timed out`. Un único incidente de proveedor VLM agotó el
  presupuesto de 2 reintentos en todo el tramo final del capítulo: **~8m12s de contenido sin extracción**
  (546s sumados por ventana incluyendo solapes; medición de los workers de claims: 8m12s netos).
- **Material único del bloque NO presente en el store ≈ 29 proposiciones** (rango 27–31), inventariadas por
  transcript deduplicado y contrastadas contra el store (búsquedas por tema; 0 records de order block,
  power three, failure-swing-definición u horas NY):

| Tema | Proposiciones no extraidas (est.) |
|---|---|
| A. SMT aplicada a objetivos y formación de rango (w0093–w0097) | **5** — la SMT no tiene por qué ser entre dos velas (puede ser en la llegada a objetivos); también hay SMT para formar el rango (incl. pendientes); dibujo libra-con-mecha / euro-igual / extremo-de-libra-no-tomado; la SMT convierte el rango de GB en rango y esto en objetivo (euro sí tomó, libra no); caso SMT no visible a simple vista (libra crea el rango, euro llega arriba). *Lo ya almacenado por w0092 antes del bloque: long en libra + giro directo, condiciones SMT-objetivo.* |
| B. Failure swing (w0098–w0105) | **4** — definición («el precio no consigue hacer un nuevo bajo», varios casos); ya visto en curso intermedio; caso 1: alto/bajo al final de la vela (vía SMT) y rango por creado aunque no tome el low; caso del broker (Forexcom vs FXCM, la duda del zoom). *La promesa «se explicará más adelante» ya estaba (w0027–w0029).* |
| C. Order block / change in delivery (w0105–w0118) | **8** — concepto y su papel en el change in delivery (cambio de tendencia); uso del instructor para entradas/confirmaciones en TF baja (M15, capítulo de entradas); definición (vela alcista que cierra fuera de la última bajista); ejemplo 8h con cierre «exagerado»; M15 más fácil + la venta de hoy no visible en 15/10; regla de entrada tras cierre fuera (2 ejemplos); el long exacto del 23-jun; operativa en 10/25/30 y short anticipando el order block. **El store no tiene NI UN record de order block.** |
| D. Recap + Power of three + cierre (w0118–w0130) | **12** — recap de conceptos básicos; power 3 ya explicado en curso intermedio; anatomía de la vela (apertura-manipulación-distribución-cierre, ejemplo 4h); niveles 1:00 y 5:00 hora NY (5:00 = cierre); visualización de la vela pintada (mecha arriba); las compras ideales siempre en la manipulación; ejemplo 4:30 → esperar la vela de 5:00 y entrar en el power 3 (punto óptimo); preferir el power 3 de la vela nueva; rango alcista durante el power 3 = longs brutales; vela 4h vista en 15m = bajada muy agresiva; aléjate y pon el foco en 4h (naturaleza: manipular para ir a tu dirección); el power 3 se mencionará en entradas/salidas + cierre («este es el primer capítulo»). **0 records de power three en el store.** |

- **Clasificación**: `TRANSPORT_UNEXERCISED` — no es pérdida por colisión semántica (el pipeline no llegó a
  proponer nada), pero sí es **ausencia real del store**: el 59% del material no extraído del run (29 de ~35
  proposiciones) proviene de este bloque, y dos temas enteros (order block, power of three) quedan fuera del
  conocimiento del producto pese a anunciarse en el recap del propio capítulo.

## Métricas

| Métrica | full-live (P7b viejo) | rerun @19b44c1 | **P7b @`e7bc387`** |
|---|---|---|---|
| Ventanas rechazadas | 26 (104 aceptadas) | 19 (111 aceptadas) | **49 (81 aceptadas)** |
| Identidad / formato / transporte | 22 / 4 / — | 17 / 2 / — | **11 / 0 / 38** |
| (a) Residuo material identidad-only | 19 (10 ventanas) | 10 (8 ventanas) | **6 (6 ventanas)** — 6 < 19 ✓ |
| (b) Residuo incluyendo transporte | — | — | **≈35** (6 identidad + ≈29 bloque) |
| MATERIAL_LOSS íntegro | 0 | 0 | **0** (identidad); bloque transport = pérdida de extracción íntegra del tramo |

- **(a) Comparabilidad con el umbral**: excluyendo el bloque transport (cuyas ventanas no ejercieron el ladder),
  el residuo baja a 6 proposiciones: −40% vs @19b44c1 (10) y −68% vs full-live (19). En el eje identidad, el run
  `e7bc387` es el mejor de los tres: mismos modos de fallo (DIVERGENT semántico 6, epistemic 3, kind 2 — nota: la
  composición real difiere del encargo, que estimaba 5 DIVERGENT + 1 «otra»; no hay ninguna «otra») pero con menos
  caídas y menos residuo. Tres de los residuos nuevos (w0023, w0062, w0073) son ventanas que @19b44c1 aceptaba;
  a cambio, w0009/w0035 —rechazadas entonces— hoy se aceptan y **almacenan residuos del run anterior**
  (`cl-vela-negativa-frecuente`, `cl-vela-no-necesariamente-negativa`, `cl-existen-senales-reversion`,
  `cl-existen-senales-continuacion`), confirmando que la población de rechazo sigue rotando entre runs.
- **(b) Cobertura real del store**: sumando el bloque, faltan ≈35 proposiciones materiales (~6% del contenido del
  capítulo), el 83% de ellas concentradas en 8m12s de video no extraído por el incidente de transporte. Ninguna es
  recuperable por vecindad: son temas (order block, power of three, failure swing operativos) que solo se explican
  en ese tramo.

## Notas transversales

1. **El transporte, no la identidad, domina este run**: 38 de 49 rechazadas (78%) por un solo modo de fallo
   (`retry budget of 2 exhausted; request timed out`, 38/38). Con backoff/reintento posterior o reintento de
   ventana, el run habría quedado en 11 rechazadas y residuo 6 — mejor run auditado. El coste del incidente es
   +29 proposiciones ausentes y dos temas enteros fuera del store.
2. **El parámetro de contexto sigue generando rechazos espurios** (4 de 11 identidad colisionan sobre
   instrumento/fuente/divisa/timeframe: w0008, w0061, w0062, w0073, w0084), ahora ya no por kind determinista
   sino por epistemic/deterministic-divergence. El registro canónico de contextos por-ventana propuesto en los
   dos audits previos sigue pendiente y seguiría eliminando ~la mitad de las caídas de identidad.
3. **Cuantificadores y calificativos siguen siendo la pérdida sistemática** (w0023 «completando las órdenes»,
   w0062 «los nombres no importan», w0073 «se verá más adelante»): la re-canonicalización conserva la proposición
   colisionada pero no sus satélites. 6 de 6 residuos son de este tipo.
4. **Verificación de records**: 81/81 de los `surviving_record_ids` citados en `rejected-windows.jsonl` existen
   en `run-rerun2/claims.jsonl` (chequeo programático). 2 frames inspeccionados visualmente (w0006, w0008).
5. El solape de ventanas contiguas (w0093/w0094, w0098–w0100, w0122/w0123…) duplica transcript en el corpus; el
   inventario del bloque está deduplicado por contenido, no por ventana.

## FEEDBACK (Agents-OS)

1. **Bootstrap suficiente y sin fricción**: marker resuelto a la primera, stack mínimo cargado, y todas las rutas
   del encargo resolvieron sin explorar el vault. Sesión one-shot: las reglas de warm turn no aplicaron. Reiterar
   el patrón de los audits previos: para tareas de proyecto con rutas absolutas, el cold-start no necesita
   recuperación de entidad (se saltó el paso 7 sin degradación).
2. **`status_reasons` sigue siendo un blob de texto**: 719 razones como strings JSON en una sola clave de
   `pipeline_state`; las razones largas siguen truncándose con `…` embebido (w0077 pierde el final del veredicto).
   Además el encargo estimaba «5 DIVERGENT + 1 otra» y la realidad es 6 DIVERGENT / 3 epistemic / 2 kind / 0 otra:
   los subtotales deben derivarse del db, no del brief. Sugerencia reiterada: `reason_class` + `collision_window`
   + `statements` como JSON estructurado por ventana.
3. **Pairing cross-workspace sin documentar**: el coverage del run rerun2 vive en
   `clutifx-ch01-full-live-20261001/analysis-p7b/coverage.json` (workspace del run viejo). Verifiqué que sus
   dispositions reproducen rerun2 (49/49) antes de usarlo, pero un consumidor sin ese chequeo podría mezclar
   stores. Sugerencia: escribir el coverage junto al store del propio run (o declarar el pairing en un manifest
   del run).
4. **Sin CLI `sqlite3` en el host** (tercera vez): lectura de run.db requiere Python. Un dump JSONL del estado del
   run ahorraría fricción a cualquier auditor.
5. **Incidente de transporte = el 78% del rechazo del run**: un mismo modo de fallo (`vlm provider transport
   retry-exhausted`, budget 2) descartó 38 ventanas contiguas y dejó dos temas (order block, power of three) fuera
   del store. Recomendación de producto: reintentar ventanas transport-rejectadas al final del run (requeue) antes
   de fail-closed definitivo; es la palanca con mayor retorno de cobertura de todo el pipeline (29 proposiciones
   por 8m12s de video).
6. **Granularidad estable**: la unidad «proposición material» volvió a ser comparable entre runs (19 → 10 → 6) y
   permitió cuantificar el bloque transport (≈29) con el mismo rasero. Mantenerla como métrica canónica de
   residuo en las siguientes campañas.
