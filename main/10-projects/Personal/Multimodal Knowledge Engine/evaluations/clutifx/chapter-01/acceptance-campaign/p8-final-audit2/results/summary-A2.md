# P8 Final Audit A2 — P7b (`e7bc387`, run-rerun2) · Ventanas w0034–w0066 · Source-grounded, sin muestreo

Auditoría de población completa de claims en ventanas **ACEPTADAS** de w0034 a w0066 del corpus
`p8-final-audit2/corpus/`. Verificación contra transcript (ASR) y, para todo claim visual
(niveles, colores, rectángulos, velas, etiquetas UI), lectura directa del frame PNG
(144 frames distintos citados leídos a 1280px; crops 2x puntuales para niveles finos).

## Disposición de ventanas (verificada antes de auditar)

- **28 ventanas aceptadas auditadas**: w0034–w0043, w0045–w0053, w0055–w0057, w0059–w0060, w0063–w0066.
- **5 ventanas REJECTED (0 claims, fuera de población)**: w0044, w0054, w0058, w0061, w0062 (todas `identity divergence`).

## Población y labels

| Métrica | Valor |
|---|---|
| Claims auditados | **279 / 279** (100% de la población aceptada; 0 duplicados, 0 faltantes, IDs verificados contra corpus) |
| CORRECT | **275 (98,6%)** |
| WRONG | **4 (1,4%)** |
| PARTIAL / OVERGENERALIZED / DUPLICATE / UNVERIFIABLE | 0 |
| Materialidad: YES 241 · NO 38 | — |
|**Precisión estricta (CORRECT/total)** | **98,6%** |
|**Precisión sobre claims MATERIAL (241)** | **99,6%** (1 material erróneo) |

### Los 4 WRONG

| Window | Claim | Material | Error |
|---|---|---|---|
| w0037 | `cl-objetivo-hoy-gbpusd` | **YES** | Objetivo de hoy GBPUSD = 1.37489 (es la REGRESIÓN baseline, ver abajo) |
| w0040 | `cl-eurusd-view-pans-earlier` | NO | Dirección de navegación invertida: la vista se desplaza hacia fechas **posteriores** (borde izquierdo may 22 → jun 4), no anteriores |
| w0040 | `cl-gbpusd-view-pans-earlier` | NO | Ídem en el panel GBPUSD |
| w0051 | `cl-line-horizontal-115000-drawn` | NO | La línea horizontal dibujada está en ~1,15024–1,15026 (alineada con esas etiquetas, verificado con crop 2x); «1,15000» es solo etiqueta de eje. La publicación `UNSUPPORTED_CONTRADICTED` del revisor fue **correcta** |

Observaciones de calidad: cero alucinaciones de contenido; los niveles finos (1,34155/1,35843,
3,394.75/3,388.10, 1,16148, 1,15803, 1,36238, 1,14569/1,15231, 1,14422/1,14697, 1,14565→1,14889,
1,15219→1,15641, opacidad 83%, temporalidades 1D/4h/8h/12h/15M/1h) fueron verificados uno a uno en
frame y todos coinciden salvo los 4 casos listados. Las reglas de rango (pendiente/reiniciado,
condiciones bajistas, turtle soup) se capturan fieles al ASR, incluidos hedges («normalmente»,
«podría ser», «posible»).

## Regression watch (w0037) — veredicto: **STILL_WRONG** (con recuperación parcial en w0038)

- **w0037**: el error baseline reapareció como `cl-objetivo-hoy-gbpusd` — "El objetivo de GBPUSD
  para hoy es 1,37489" — publicado **SUPPORTED_BY_AUTOMATED_REVIEW**. Verificado en frames
  p46080000/p46170000: existe una línea horizontal en 1,37489 arriba del chart GBPUSD, pero el
  objetivo real del contexto es 1,35843 (borde superior del rango bullish, etiqueta azul) / 1,36031
  (zona del máximo), que es lo que el precio alcanza ("teníamos este objetivo para hoy" → "la libra
  fue directamente hasta su objetivo", máx ~1,3676). Mismo error numérico y misma asignación de rol
  errónea que el baseline `cl-objetivo-hoy-rango-bullish-libra` / `cl-gbpusd-today-target-137489`.
  **La regla v4 de omisión por ambigüedad NO se disparó**: ante el referente ambiguo ("este
  objetivo"), el recon asignó el rol a la línea 1.37489 en vez de omitir.
- **Mitigación**: el conocimiento correcto SÍ fue recuperado en **w0038** mediante
  `cl-gbpusd-objetivo-hoy-135843` ("El borde superior del rango bullish de GBPUSD, etiquetado en
  1,35843, era el objetivo de hoy", auditado CORRECT) y reforzado en w0039
  (`cl-gbpusd-target-136238`, CORRECT: nivel marcado 1,36238 por encima del rango). Es decir, la KB
  queda con el objetivo correcto Y con el claim erróneo a 1.37489 conviviendo (riesgo de
  contradicción interna no detectada).
- Clasificación final: **STILL_WRONG en w0037**, con `ABSENT_BUT_KNOWLEDGE_RECOVERED_ELSEWHERE`
  parcialmente aplicable por w0038/w0039 (el claim erróneo no fue omitido ni corregido).

## Missing knowledge (2 entradas en `MISSING-KNOWLEDGE-A2.jsonl`)

1. **w0037 · MISSING_MATERIAL** — La atribución correcta del objetivo de hoy (1,35843/1,36031) no se
   capturó en la ventana; se capturó la errónea (1.37489). Recuperada en w0038.
2. **w0038 · MISSING_NON_MATERIAL** — La regla causal "sin rango bajista → avance directo al
   objetivo" queda implícita en dos átomos sin relación explícita (matiz pedagógico).

Nota (no registrado como missing): el término «doble» (doble alcista/bajista) se usa en w0053 como
concepto previo sin definir en la ventana; el instructor no lo define aquí, por lo que no hay
proposición que capturar.

## Fortalezas del run P7b

- La trompa de transporte (38 ventanas muertas 04:34–10:28Z) no degradó la calidad del recon en las
  mitades: las 102 claims con `UNSUPPORTED_REVIEW_UNAVAILABLE` auditadas aquí resultaron
  correctas en contenido (el grounding automático falló, no la extracción).
- Cobertura de reglas de estrategia sobresaliente: definiciones de rango pendiente/reiniciado
  (w0045–w0053), condiciones de rango bajista (w0050), turtle soup + alias y contraejemplo
  (w0064–w0066) capturadas atómicamente y con relaciones DEPENDS_ON/EQUIVALENT_TO coherentes.
- Asignación de roles v4 bien aplicada en el resto de casos ambiguos («este es un rango», «esto sería
  una vela», «objetivo en la parte superior», línea 1,36238 en w0039).

## Debilidades

1. Único error material persistente = el objetivo de hoy GBPUSD (baseline no erradicado en su ventana).
2. Errores direccionales/detalle no materiales (2 de navegación, 1 nivel de línea auxiliar) — bajo
   impacto pero muestran que las observaciones de UI navigational siguen siendo el punto débil.
3. Claim erróneo SUPPORTED convive con el correcto (w0037 vs w0038) sin detección de contradicción.

---

## FEEDBACK (Agents-OS)

1. **Lo que funcionó**: el handoff one-shot con corpus pre-cortado por ventana + disposition +
   rutas de frames + procedimiento "sin muestreo" fue ejecutable de punta a punta sin volver a
   preguntar nada. El `REJECTED-WINDOWS.json` aparte y el campo `disposition` dentro de cada
   ventana evitaron auditar basura. El aviso previo de "tu rango puede tener REJECTED al final"
   era correcto (5/33 rechazadas) y cambió el denominador real (279, no ~330).
2. **Fricción**: (a) leer frames a full-res habría reventado el contexto; tuve que auto-gestionar
   copies a 1280px + crops 2x para niveles finos — sería útil que el preparador del corpus deje
   ya un `frames-read/` downscaled por campaña; (b) los IDs de claim son estables pero al
   transcribirlos a mano se cuelan typos (detectado y corregido 1: `cierre-fuerte`/`cierre-fuerza`);
   un diff automático IDs-auditados vs corpus al cerrar el audit ahorraría el ciclo de corrección;
   (c) el prompt decía "AUDITOR FUENTE-GROUNDED del P8 final" auditando el "run P7b": la nomenclatura
   P7/P7b/P8 mezclada obliga a inferir que P8-final-audit2 es el segundo pase sobre el run rerun2.
3. **Sugerencias Agents-OS**: (a) registrar el veredicto de regression como campo de primera clase
   (FIXED/STILL_WRONG/...) en el summary en vez de sección en prosa, para trending entre campañas;
   (b) cuando un claim erróneo SUPPORTED convive con uno correcto en otra ventana, añadir un check
   de contradicción numérica entre claims del mismo run (1.37489 vs 1.35843 habrían saltado);
   (c) para regression-watch, dar además del baseline ID los frames ground-truth ya recortados
   (ahorra re-derivación); (d) mantener el formato de digests: funcionó mejor que re-leer JSON crudo.
4. **Veredicto de sesión**: bootstrap de Agents-OS no re-invocado (subagente one-shot, skill no
   expuesta en este contexto); routing implícito al proyecto MKE correcto. Sesión lista para cierre.
