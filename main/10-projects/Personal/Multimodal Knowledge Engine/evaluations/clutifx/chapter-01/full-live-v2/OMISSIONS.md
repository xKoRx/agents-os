# OMISSIONS — qué NO quedó en el conocimiento canónico

Distinción contractual: **MKE rechazó explícitamente** (decisión auditable con razón durable) vs **MKE nunca observó/extrajo** (no aplica aquí: las 130 ventanas fueron intentadas, 0 regiones no observadas).

## 1. Ventanas rechazadas por MKE (26) — el tramo NO aportó conocimiento de esa ventana

| Window | Time | Categoría | Razón (resumen) |
|---|---|---|---|
| w0003 | 00:37–00:44 | bad evidence ref | claims reconstruction output rejected: claims reconstruction output was rejected in a previous attempt |
| w0005 | 01:05–01:15 | bad evidence ref | claims reconstruction output rejected: claims reconstruction output was rejected in a previous attempt |
| w0028 | 06:06–06:13 | identity divergence | claims reconstruction output rejected: record cl-observar-formacion-rangos@1 identity collision: window w0027 proposed "Hay que ir viendo cómo se forman los … |
| w0034 | 07:32–07:42 | identity divergence | claims reconstruction output rejected: record cl-grafico-eurusd@1 identity collision: kind differs (observation vs parameter) (window w0031, then window w003… |
| w0043 | 09:36–09:46 | bad evidence ref | claims reconstruction output rejected: claims reconstruction output was rejected in a previous attempt |
| w0045 | 10:16–10:32 | identity divergence | claims reconstruction output rejected: record cl-nueva-vela-abre-aqui@1 identity collision: kind differs (observation vs claim) (window w0044, then window w0… |
| w0049 | 11:18–11:27 | identity divergence | claims reconstruction output rejected: record cl-rango-diario@1 identity collision: kind differs (claim vs observation) (window w0017, then window w0049); de… |
| w0054 | 12:45–12:57 | identity divergence | claims reconstruction output rejected: record rel-rango-bajista-depende-apertura-arriba@1 identity collision: structural relation divergence, subject endpoin… |
| w0058 | 13:39–13:56 | identity divergence | claims reconstruction output rejected: record cl-rango-pendiente@1 identity collision: epistemic differs (VIDEO_OBSERVED vs INSTRUCTOR_SAID) (window w0051, t… |
| w0059 | 14:00–14:12 | identity divergence | claims reconstruction output rejected: record cl-rango-pendiente@1 identity collision: epistemic differs (VIDEO_OBSERVED vs INSTRUCTOR_SAID) (window w0051, t… |
| w0062 | 14:41–14:56 | identity divergence | claims reconstruction output rejected: record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window … |
| w0065 | 15:44–15:57 | identity divergence | claims reconstruction output rejected: record cl-grafico-eurusd@1 identity collision: kind differs (observation vs parameter) (window w0031, then window w006… |
| w0072 | 17:47–18:03 | identity divergence | claims reconstruction output rejected: record cl-grafico-temporalidad-15m@1 identity collision: kind differs (observation vs parameter) (window w0070, then w… |
| w0074 | 18:25–18:52 | identity divergence | claims reconstruction output rejected: record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window … |
| w0078 | 19:54–20:07 | identity divergence | claims reconstruction output rejected: record cl-cierre-fuera-invalida-rango@1 identity collision: window w0077 proposed "Si la vela cierra fuera del rango, … |
| w0088 | 22:18–22:28 | identity divergence | claims reconstruction output rejected: record cl-ejemplos-capitulo-aparte@1 identity collision: kind differs (claim vs procedure_step) (window w0086, then wi… |
| w0092 | 23:18–23:36 | identity divergence | claims reconstruction output rejected: record rel-smt-requiere-reversal-directo@1 identity collision: structural relation divergence, subject endpoint differ… |
| w0094 | 23:56–24:12 | identity divergence | claims reconstruction output rejected: record cl-smt-no-requerida-entre-dos-velas@1 identity collision: window w0093 proposed "La SMT no tiene que aparecer e… |
| w0098 | 25:25–25:37 | identity divergence | claims reconstruction output rejected: record cl-euro-puede-llegar-arriba@1 identity collision: window w0097 proposed "Euro puede llegar hasta arriba." and w… |
| w0102 | 26:19–26:32 | identity divergence | claims reconstruction output rejected: record cl-activo-eurusd@1 identity collision: kind differs (observation vs parameter) (window w0055, then window w0102… |
| w0109 | 28:08–28:19 | identity divergence | claims reconstruction output rejected: record cl-ir-al-grafico@1 identity collision: window w0012 proposed "Vamos a ir ahora un momento al gráfico." and wind… |
| w0110 | 28:20–28:28 | bad evidence ref | claims reconstruction output rejected: claims reconstruction proposal rejected: record cl-m15-para-subir-capitulo-entradas cites unknown evidence ref "transc… |
| w0116 | 29:26–29:38 | identity divergence | claims reconstruction output rejected: record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window … |
| w0117 | 29:39–29:48 | identity divergence | claims reconstruction output rejected: record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window … |
| w0118 | 29:52–30:08 | identity divergence | claims reconstruction output rejected: record cl-smt-aplicada-estrategia@1 identity collision: kind differs (procedure_step vs claim) (window w0086, then win… |
| w0122 | 30:56–31:16 | identity divergence | claims reconstruction output rejected: record cl-vela-apertura@1 identity collision: window w0120 proposed "Una de las partes de la vela es la apertura." and… |

Consecuencia de cobertura: los tramos de esas 26 ventanas quedaron sin extracción de ESA ventana. El conocimiento persistente de tramos vecinos sí puede cubrir parte del contenido (los frames/transcript adyacentes se observaron en ventanas aceptadas).

## 2. Claims/relations canónicas no soportadas (80) — publicadas como UNSUPPORTED, no como verdad

- UNSUPPORTED_INSUFFICIENT: 74 (74 claims + 17 relations INSUFFICIENT a nivel grounding; el reviewer automated consideró la evidencia citada insuficiente)
- UNSUPPORTED_CONTRADICTED: 5
- UNSUPPORTED_REVIEW_UNAVAILABLE: 1 (1 claim: el reviewer falló por parse fatal del backend; `cl-rango-rectangular-vertical`)

Estos records ESTÁN en claims.jsonl/documentation.md marcados como no soportados — no son omisiones de extracción sino de soporte.

## 3. Omisión L2 completa

- Razón exacta durable: `L2 composition unavailable: vlm provider read-body [retry-exhausted]: retry budget of 2 exhausted; last failure: response body read failed`
- El capítulo no tiene SKOs: el conocimiento consolidado por conceptos (nivel L2) no pudo generarse por un fallo de transporte del backend en la única llamada de composition. Comportamiento contractual sin reintentos manuales.

## 4. Omisiones de budget

- Ninguna: no hubo BUDGET_EXHAUSTED en ninguna ventana (vlm_call 1194/2400, vlm_image 1941/8000, vlm_token 8.6M/60M).

## 5. Áreas de provider unavailable

- 2 intentos de reconstruction muertos por `assistant content is empty` (w0057, w0093): el run se recuperó por crash/resume contractual y ambas ventanas se re-invocaron con éxito; su tramo SÍ quedó extraído.
- 1 grounding con parse fatal → REVIEW_UNAVAILABLE (arriba).
- 1 composition con transport failure → L2 no alcanzado (arriba).

## 6. Conocimiento nunca observado

- Ninguna región del capítulo quedó sin intentar. Lo que el instructor haya dicho sin quedar en transcript/frames de las ventanas aceptadas no es observable por MKE; esa distinción la aporta el Owner con el checklist (marca MISSING).
