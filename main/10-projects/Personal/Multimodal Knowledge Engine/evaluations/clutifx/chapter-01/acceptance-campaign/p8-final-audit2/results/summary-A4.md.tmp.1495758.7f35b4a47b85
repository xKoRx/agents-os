# P8 Final Audit — A4 (rango w0100–w0130) · run P7b `e7bc387` (rerun2)

Auditor: fuente-grounded, sin muestreo, sobre lo ejercitado. Fecha: 2026-10-05.

## Resultado principal

**0 de 31 ventanas del rango sobrevivieron.** Todas las ventanas w0100–w0130 están
`disposition: rejected` con `rejection_category: provider unavailable` (tormenta de
transporte VLM, 04:34–10:28Z Oct 5). El rango cubre el video 25:50–34:02 (~8m12s).

Consecuencia directa verificada en corpus:
- Claims en corpus w0100–w0130: **0**
- Relations en corpus w0100–w0130: **0**
- `claims.jsonl` del run (766 claims, `mke.claims.v1`): ningún claim atribuible a w0100–w0130.
- Cada corpus file conserva su evidencia (8 frames/window, todos `exists: true`, `cited_by_claim: false`) y transcript: el material primario sobrevivió; murió la extracción (recon), no la ingesta.

Por consiguiente **no se auditan claims** (no existen), ambos JSONL de auditoría quedan
vacíos por construcción, y MISSING-KNOWLEDGE (definido por ventana aceptada) es 0 filas.

## Mapa de ventanas del rango (insumo cobertura tormenta)

| Ventana | Video | Disposition | Categoría | Claims |
|---|---|---|---|---|
| w0100 | 25:50–26:05 | rejected | provider unavailable | 0 |
| w0101 | 26:06–26:18 | rejected | provider unavailable | 0 |
| w0102 | 26:19–26:32 | rejected | provider unavailable | 0 |
| w0103 | 26:36–26:52 | rejected | provider unavailable | 0 |
| w0104 | 26:54–27:08 | rejected | provider unavailable | 0 |
| w0105 | 27:10–27:23 | rejected | provider unavailable | 0 |
| w0106 | 27:24–27:36 | rejected | provider unavailable | 0 |
| w0107 | 27:37–27:51 | rejected | provider unavailable | 0 |
| w0108 | 27:52–28:04 | rejected | provider unavailable | 0 |
| w0109 | 28:08–28:19 | rejected | provider unavailable | 0 |
| w0110 | 28:20–28:28 | rejected | provider unavailable | 0 |
| w0111 | 28:32–28:41 | rejected | provider unavailable | 0 |
| w0112 | 28:42–28:51 | rejected | provider unavailable | 0 |
| w0113 | 28:52–29:04 | rejected | provider unavailable | 0 |
| w0114 | 29:05–29:13 | rejected | provider unavailable | 0 |
| w0115 | 29:16–29:25 | rejected | provider unavailable | 0 |
| w0116 | 29:26–29:38 | rejected | provider unavailable | 0 |
| w0117 | 29:39–29:48 | rejected | provider unavailable | 0 |
| w0118 | 29:52–30:08 | rejected | provider unavailable | 0 |
| w0119 | 30:10–30:19 | rejected | provider unavailable | 0 |
| w0120 | 30:20–30:40 | rejected | provider unavailable | 0 |
| w0121 | 30:42–30:54 | rejected | provider unavailable | 0 |
| w0122 | 30:56–31:16 | rejected | provider unavailable | 0 |
| w0123 | 31:20–31:40 | rejected | provider unavailable | 0 |
| w0124 | 31:44–32:07 | rejected | provider unavailable | 0 |
| w0125 | 32:08–32:24 | rejected | provider unavailable | 0 |
| w0126 | 32:25–32:40 | rejected | provider unavailable | 0 |
| w0127 | 32:41–32:54 | rejected | provider unavailable | 0 |
| w0128 | 32:55–33:12 | rejected | provider unavailable | 0 |
| w0129 | 33:16–33:44 | rejected | provider unavailable | 0 |
| w0130 | 33:48–34:02 | rejected | provider unavailable | 0 |

Aceptadas en rango: **ninguna**. El bloque rejecteado por transporte es contiguo
w0093–w0130 (38 ventanas, 23:37–34:02), sin huecos.

## Contenido de conocimiento perdido en el rango (verificado por transcript)

- w0100: concepto *failure swing* (precio no hace nuevo bajo; relación con SMT).
- w0106: order block y la terminología "en inglés se llama **change in delivery** que
  sería como el cambio de tendencia" — justo la materia del baseline de regresión.
- w0115: ejemplo concreto de long en order block (trade del 23 de junio).
- w0130: cierre del capítulo.

## FULL-CLAIM-AUDIT-A4

0 filas (vacío). No hay claims de ventanas aceptadas en el rango: nada que verificar.

## MISSING-KNOWLEDGE-A4

0 filas (vacío). El formato es por ventana aceptada; no hay ventanas aceptadas.
Nota sistémica (fuera de esquema): ~8m12s de video (25:50–34:02) quedan sin ninguna
extracción de conocimiento en P7b por fallo de infraestructura, no por lógica de
extracción. Es brecha de cobertura, no de precisión.

## REGRESSION WATCH

Baseline `cl-cambio-oferta-demanda-termino-ingles` (w0106), fixed en P7 como
`cl-change-of-delivery-similar-to-trend-change`.

**Clasificación: ABSENT_(transporte)** — explícito: w0106 está rejected por
`provider unavailable` (tormenta de transporte), por lo que el baseline no puede
evaluarse en P7b. Verificación adicional en lo ejercitado del run completo:
- `cl-change-of-delivery-similar-to-trend-change` NO aparece en `claims.jsonl` de P7b.
- 0 claims en todo el run mencionan oferta/demanda/supply/demand/"change in delivery".
- El transcript de w0106 confirma que la materia (order block → "change in delivery" =
  cambio de tendencia) está en la ventana perdida.

Es decir: no solo está ausente por transporte en w0106; el fix de P7 no fue recuperado
en ninguna otra ventana de P7b. Si el programa necesita esa pieza de conocimiento
verificada, w0106 (o su vecindad) requiere re-run post-tormenta.

## Precisión

No calculable en este rango: 0 claims auditable (denominador 0). Reportado como N/A.

## FEEDBACK (Agents-OS)

- La regla de bootstrap (`80-agents/skills/agents-os-bootstrap/SKILL.md`, una vez por
  sesión) no distingue entre sesión principal y subagentes one-shot de tarea estrecha.
  En este audit mechanical con contexto fresco y scope cerrado, el bootstrap completo
  habría sido overhead sin beneficio. Sugerencia: indicar explícitamente que subagentes
  task-scoped (o sesiones sin routing de entidades) pueden saltarlo o ejecutarlo en
  modo mínimo.
- La instrucción dice "en turnos warm reutiliza la base" pero no define qué cuenta como
  "cambio de entidad"; para un auditor que solo escribe JSONL/MD en un subdir del vault,
  una línea de excepción tipo "sesiones de tool-use puro sin consultas al vault" aclararía
  el alcance y ahorraría el startup en el 100% de estos runs.
- Positivo: la resolución de `VAULT_ROOT` por marker funcionó sin ambigüedad desde un cwd
  profundamente anidado (`10-projects/.../chapter-01`); el marker `80-agents/agents-os/agents-os.md`
  es fiable como detector de vault.
