# REJECTED-WINDOW-AUDIT — Capítulo 01 Clutifx (26 ventanas rechazadas)

Auditoría de aceptación fuente-grounded de las 26 ventanas canónicas rechazadas fail-closed
del pipeline L1 sobre `ep01-intro.mp4` (34:03.9, 130 ventanas sin solape; 104 aceptadas / 26 rechazadas).

- **Método**: por ventana se leyó el transcript y frames del corpus (`corpus/wNNNN.json`), la razón exacta
  en `full-live-v2/documentation.md` (líneas 16–41 y ladder línea 131), las proposals de la ventana en
  `fixtures/rejected-window-recon-invocations.jsonl`, y la cobertura se probó contra los **records concretos**
  de las vecinas (±2) y del store `full-live-v2/claims.jsonl` (803 claims + 130 relaciones). No se infiere
  recuperación por solape temporal: cada cobertura citada lleva record ID. Los frames visualmente materiales
  se inspeccionaron (w0058 p74880000, w0116 p160020000).
- **Fecha**: 2026-10-03. Datos por ventana en `rejected-windows.jsonl` (mismo directorio).

## Conteo de consecuencias

| Consecuencia | Ventanas | N |
|---|---|---|
| NO_MATERIAL_LOSS | w0003, w0005, w0028, w0043, w0045, w0049, w0054, w0062, w0065, w0078, w0088, w0094, w0098, w0102, w0118, w0122 | **16** |
| PARTIAL_MATERIAL_LOSS | w0034, w0058, w0059, w0072, w0074, w0092, w0109, w0110, w0116, w0117 | **10** |
| MATERIAL_LOSS | — | **0** |

**Resultado global: ninguna ventana rechazada perdió conocimiento material de forma íntegra.**
10 de 26 dejan un residuo material acotado (1–3 proposiciones cada una); 16 no dejan residuo material.

### Ventanas con pérdida residual material (las 10)

| Ventana | Razón | Residuo no almacenado |
|---|---|---|
| w0034 | kind (cl-grafico-eurusd: observation vs parameter) | «Los rangos NO siempre se completan» + «observad por qué a veces no se completan» + EXCEPTION_TO |
| w0058 | epistemic (cl-rango-pendiente: VIDEO_OBSERVED vs INSTRUCTOR_SAID) | Anticipación en tiempo real: visto toma-low + reacción, el rango se puede anticipar antes del cierre |
| w0059 | epistemic (ídem, mismo asr-00115) | La misma anticipación + «es un aspecto avanzado, se irá viendo al practicar» |
| w0072 | kind (cl-grafico-temporalidad-15m) | Puntero: «cómo intentar predecirlo se explicará más adelante» |
| w0074 | kind (cl-instrumento-eurusd) | Regla de re-entrada: tras la reacción posterior a los rangos en contra, «poner la entrada ahí otra vez» |
| w0092 | structural (rel-smt-requiere-reversal-directo: endpoint sujeto) | «Estar atento a los dos pares» (vigilancia euro/correlacionado) |
| w0109 | semántica DIVERGENT (cl-ir-al-grafico vs w0012) | Puntero: «lo vais a ver en el capítulo de entradas» |
| w0110 | bad evidence ref (`transcript asr-00245`) | Mismo puntero al capítulo de entradas (compartido con w0109) |
| w0116 | kind (cl-instrumento-eurusd) | Regla de marcos alternativos 10/25/30 min + parámetros de la operación corta de ejemplo (1,15078 / 1,14741 / RR 1 / cerrada) |
| w0117 | kind (cl-instrumento-eurusd) | Regla de marcos alternativos 10/25/30 min (compartida con w0116) |

Patrón de las pérdidas: nunca es el contenido colisionado (eso quedó casi siempre en la vecina o en el propio
record ganador); son **proposiciones adyacentes únicas de la ventana** — caveats del método (w0034),
habilidad de anticipación en tiempo real (w0058/w0059), reglas operativas menores (w0074, w0092, w0116/w0117)
y punteros a capítulos futuros (w0072, w0109/w0110) — que el ladder de identidad no transfiere al vecino.

## Análisis por ventana

### Bloque 1 — bad evidence refs (4): w0003, w0005, w0043, w0110

Documentación (`documentation.md`): w0003/w0005/w0043 «claims reconstruction output was rejected in a
previous attempt»; w0110 «record cl-m15-para-subir-capitulo-entradas cites unknown evidence ref
"transcript asr-00245"».

**Veredicto de las 4: reconstrucción semántica CORRECTA, formateo de refs inválido → hardening de
prompt/schema basta; no hubo error de comprensión.**

- **w0003** (00:37–00:44, asr-00003): los 5 statements verbales replican el transcript literal
  («vamos directamente al grano», «formato similar al del curso intermedio», «no pasa nada si no lo has
  hecho... no hay información totalmente relevante»). Las observaciones de chart (EURUSD, 5M, descenso tras
  máximo) coinciden con lo canonizado en w0001/w0002. Refs malformadas: `asr-00003 [34850-49400]` — el
  modelo añade el intervalo temporal como sufijo del ID. Cobertura: cl-formato-similar-intermedio@1,
  cl-no-requiere-curso-intermedio@1, cl-info-intermedio-no-totalmente-relevante@1, cl-grafica-eurusd@1,
  cl-temporalidad-cinco-minutos@1, cl-descenso-reciente-eurusd@1 + las dos relaciones (w0002/w0004).
  **NO_MATERIAL_LOSS.**
- **w0005** (01:05–01:15, asr-00005): la regla de rango (toma extremo + cierra dentro) y su excepción
  (vela no siguiente) son literales del transcript y quedaron en w0004 como
  cl-rango-otra-vela-toma-extremo-cierra-dentro@1 + cl-rango-vela-tomante-puede-no-ser-siguiente@1 +
  rel-vela-no-siguiente-excepcion-a-definicion-rango@1; w0006/w0007 las re-expresan. Refs con el mismo
  defecto `asr-00005 [61640-81320]`. **NO_MATERIAL_LOSS.**
- **w0043** (09:36–09:46, asr-00098): 4 horas, toma del low, dibujar con mechas para realismo — todo
  correcto y todo en w0044 (cl-duracion-posible-cuatro-horas@1, cl-vela-toma-low-rango-cuatro-horas@1,
  cl-dibujar-vela-siguiente-con-mechas@1, cl-mecas-para-realismo-visual@1). Refs `asr-00098 [572710-594750]`.
  **NO_MATERIAL_LOSS.**
- **w0110** (28:20–28:28, asr-00245/246/247): statements verificados correctos («M15 para subir... ya lo
  vais a ver el capítulo entradas», «vamos a ir ahora mismo a buscar alguno... este de aquí es un order
  block», «en el momento en que esta vela cierra afuera»). Aquí el defecto es distinto: prefijo de namespace
  inválido (`transcript asr-00245` en vez de `asr-00245`). Un constraint de schema con patrón de ID
  (`^asr-[0-9]{5}$`) habría aceptado la ventana. Cobertura en w0111/w0112 (cl-zona-senalada-es-order-block@1,
  cl-busqueda-venta-order-block-visible@1, cl-order-block-cierre-exagerado@1, cl-vela-cerrada-muy-fuera@1);
  residuo: el puntero al capítulo de entradas (compartido con w0109). **PARTIAL_MATERIAL_LOSS.**

Causa raíz común: el contrato `mke.claims-recon.v2` no restringe el formato de `evidence_ids` a nivel de
schema; el modelo «decora» los IDs con intervalos o prefijos. Fix recomendado: enum/pattern en schema +
instrucción explícita en prompt («usa el evidence_id exactamente como aparece en la lista»).

### Bloque 2 — divergencias deterministas de kind/epistemic (10): w0034, w0045, w0049, w0054, w0058, w0059, w0062, w0065, w0072, w0074, w0088, w0092, w0102, w0116, w0117, w0118 (16 ventanas en total, incluidas estructurales)

El patrón dominante (11 ventanas: w0034, w0045, w0049, w0062, w0065, w0072, w0074, w0088, w0102, w0116,
w0117, w0118) es la re-declaración de **parámetros de contexto** — instrumento (cl-instrumento-eurusd@1 ×5),
gráfico (cl-grafico-eurusd@1 ×3), temporalidad (cl-grafico-temporalidad-15m@1), activo (cl-activo-eurusd@1),
rango diario (cl-rango-diario@1) — con un `kind` distinto del ya almacenado (observation↔parameter, claim↔
observation, claim↔procedure_step). El contenido semántico de esos parámetros ya vivía en el store, de modo
que el fail-closed no perdió el parámetro en ningún caso; lo que se perdió (o no) fue el resto de la ventana:

- Sin pérdida (7): **w0045** (todo en w0044/w0046), **w0049** (todo en w0048/w0050), **w0062** (todo en
  w0060/w0061/w0063; el meta-comentario sobre nombres es no-material), **w0065** (nombres alternativos en
  w0064, vela 4H en w0066), **w0088** (todo en w0086/w0087/w0089), **w0102** (regla «no toma el low y aun
  así es rango» en w0103), **w0118** (recap de conceptos ya almacenados; demo-tool ya en w0115).
- Con pérdida (5): **w0034**, **w0072**, **w0074**, **w0116**, **w0117** (ver tabla de residuos).

- **Epistemic** (2): **w0058/w0059** chocaron con cl-rango-pendiente@1 de w0051 (VIDEO_OBSERVED) al
  proponerlo como INSTRUCTOR_SAID. El rótulo/estado del rango está en w0057/w0061, pero la narrativa de
  anticipación en tiempo real (asr-00115, visualmente confirmada en el frame p74880000: rectángulo pendiente
  con tope 1,15231 y vela tomando el low ~1,1467 con reacción) se perdió con ambas ventanas → PARTIAL.
  Nota de calidad de datos: los límites propuestos por w0059 (1,14569/1,15231) difieren de los canonizados
  por w0061 (1,14565/1,15325) para el mismo rectángulo; una lectura es inexacta y merece re-verificación si
  se re-ingiere.
- **Estructurales** (2): **w0054** (endpoint «crea» en rel-rango-bajista-depende-apertura-arriba@1) — w0053
  conservó la relación y las 6 proposiciones; **NO_MATERIAL_LOSS**. **w0092** (endpoint
  cl-configuracion-senalada-es-smt@1 vs cl-formacion-correlada-es-smt@1) — la definición SMT con sus 3
  DEPENDS_ON quedó por w0091; se perdió solo «estar atento a los dos pares» → PARTIAL.

### Bloque 3 — divergencias semánticas DIVERGENT (6): w0028, w0078, w0094, w0098, w0109, w0122

En 5 de 6, el equivalence_review falló ante **sinonimia superficial** y la vecina ya tenía el contenido:

- **w0028** ≡ w0027 («Observar cómo se forman los rangos» vs «Hay que ir viendo cómo se forman los rangos»)
  → cl-observar-formacion-rangos@1 aceptado; además w0029 duplica todo el pasaje. NO.
- **w0078** ≡ w0077 («el rango deja de ser válido» vs «deja de ser un rango») → cl-cierre-fuera-invalida-rango@1
  aceptado; cadena esperar-apertura→toma-low→nuevo-rango en w0079. NO.
- **w0094** ≡ w0093 («Una SMT no tiene que ser entre estas dos velas» vs «no tiene que aparecer entre») →
  cl-smt-no-requerida-entre-dos-velas@1 aceptado con su EXCEPTION_TO. NO.
- **w0098** ≡ w0097 («Si el euro no tiene que crear el rango, puede llegar hasta arriba» vs «Euro puede
  llegar hasta arriba») → record aceptado + rel-llegada-arriba-depends-no-necesidad-rango@1 que conserva
  la condicionalidad. NO.
- **w0122** ≡ w0120 («La vela abre» vs «Una de las partes de la vela es la apertura») → cl-vela-apertura@1
  aceptado + w0123 describe la secuencia completa (abre 01:00 → manipula → sube/baja → cierra 05:00 con
  mecha superior). NO.
- **w0109** ≡ w0012 («Vamos a ir al gráfico para verlo claro» vs «Vamos a ir ahora un momento al gráfico»):
  redundante por partida doble (w0108 ya tenía cl-ir-al-grafico-para-ver-claro@1); el único contenido propio
  era el puntero al capítulo de entradas, que se perdió → PARTIAL.

Lectura del ladder (línea 131): 38 colisiones de identidad, de las cuales 22 divergentes produjeron estos
rechazos. Las 6 DIVERGENT demuestran que el revisor de equivalencia es estricto con la paráfrasis; en las
6, la decisión conservadora no costó conocimiento salvo en w0109.

## Notas transversales

1. **Los parámetros de contexto son la principal fuente de rechazo espurio**: 11 de 26 ventanas cayeron por
   re-declarar instrumento/timeframe con otro `kind`. Un registro de parámetros de contexto por-ventana
   (o canónica de contextos) eliminaría ~40% de los rechazos.
2. **Los punteros a contenido futuro se tratan como material** porque el propio store los canoniza
   (cl-capitulo-failure-swing@1, cl-ejemplos-capitulo-aparte@1, cl-power-3-mencion-entradas@1,
   cl-estrategia-capitulo-siguiente@1). Con ese estándar, los perdidos son los de w0072 y w0109/w0110.
3. **No-MATERIAL_LOSS en 26/26**: el fail-closed del ladder nunca borró un concepto entero; las pérdidas
   son siempre proposiciones satélite (1–3 por ventana).
4. Verificación de records: los 100% de los `record_id` citados en `rejected-windows.jsonl` existen en
   `full-live-v2/claims.jsonl` (chequeo programático).
