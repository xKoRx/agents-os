# Resumen de auditoría A1 — Capítulo 01 Clutifx, PARTE 1 (w0001–w0033)

Auditor: A1. Ventanas aceptadas auditadas: 30 de 33 (rechazadas y excluidas: w0003, w0005, w0028).
Claims auditados: 225. Verificación: claims hablados contra transcript (asr-NNNNN), claims visuales contra los frames PNG citados (se leyó al menos un frame citado por cada claim visual), MODEL_INFERRED contra su evidencia combinada.

## Tabla por ventana

| Ventana | Claims | CORRECT | PARTIAL | WRONG | OVERGEN | DUP | UNVER | MATERIAL=YES | Missing |
|---|---|---|---|---|---|---|---|---|---|
| w0001 | 15 | 14 | 1 | 0 | 0 | 0 | 0 | 5 | NONE |
| w0002 | 25 | 20 | 1 | 0 | 0 | 4 | 0 | 12 | NONE |
| w0004 | 12 | 9 | 0 | 0 | 0 | 3 | 0 | 3 | NONE |
| w0006 | 8 | 5 | 0 | 0 | 0 | 3 | 0 | 6 | NONE |
| w0007 | 4 | 3 | 0 | 0 | 0 | 1 | 0 | 3 | NONE |
| w0008 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 1 | NONE |
| w0009 | 3 | 1 | 0 | 1 | 0 | 1 | 0 | 2 | NONE |
| w0010 | 3 | 2 | 0 | 0 | 0 | 1 | 0 | 2 | NONE |
| w0011 | 5 | 4 | 0 | 1 | 0 | 0 | 0 | 5 | NONE |
| w0012 | 7 | 5 | 0 | 0 | 0 | 2 | 0 | 4 | NONE |
| w0013 | 12 | 9 | 0 | 0 | 0 | 3 | 0 | 1 | NONE |
| w0014 | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 2 | MISSING_NON_MATERIAL |
| w0015 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | MISSING_NON_MATERIAL |
| w0016 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | NONE |
| w0017 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 3 | NONE |
| w0018 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 7 | NONE |
| w0019 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 1 | MISSING_NON_MATERIAL |
| w0020 | 7 | 6 | 0 | 0 | 0 | 1 | 0 | 4 | NONE |
| w0021 | 8 | 6 | 0 | 0 | 0 | 2 | 0 | 7 | NONE |
| w0022 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | 5 | NONE |
| w0023 | 6 | 4 | 0 | 0 | 0 | 2 | 0 | 5 | NONE |
| w0024 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 4 | NONE |
| w0025 | 13 | 12 | 0 | 0 | 0 | 1 | 0 | 7 | NONE |
| w0026 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 5 | NONE |
| w0027 | 11 | 7 | 0 | 0 | 0 | 4 | 0 | 9 | NONE |
| w0029 | 9 | 4 | 0 | 0 | 0 | 5 | 0 | 9 | NONE |
| w0030 | 7 | 3 | 0 | 0 | 0 | 4 | 0 | 6 | NONE |
| w0031 | 6 | 4 | 0 | 0 | 0 | 2 | 0 | 2 | NONE |
| w0032 | 8 | 7 | 0 | 0 | 0 | 1 | 0 | 4 | NONE |
| w0033 | 4 | 3 | 0 | 0 | 0 | 1 | 0 | 2 | NONE |

## Conteo total

- **225 claims**: CORRECT **178** (79,1%) · PARTIAL **3** (1,3%) · WRONG **2** (0,9%) · OVERGENERALIZED **0** · DUPLICATE **42** (18,7%) · UNVERIFIABLE **0**.
- Materialidad: MATERIAL=YES 130 · MATERIAL=NO 95.
- Ventanas con missing: 3 × MISSING_NON_MATERIAL (w0014, w0015, w0019). Ninguna MISSING_MATERIAL.

## Hallazgos notables (errores)

### WRONG (2, ambos MATERIAL=YES)

1. **w0009 `cl-vela-negativa-mayoria`** — "La mayoría de las veces, la vela es negativa."
   El antecedente inmediato en el transcript es "probablemente una vela positiva" (asr-00014); asr-00015 "no tiene por qué, pero la mayoría de veces vais a ver que sí que es así" se refiere a que la vela suele ser **positiva** (pudiendo no serlo), y asr-00016 "y una vela negativa" introduce la alternativa (el frame p11160000 muestra la vela repintada en negro como contraejemplo). El claim invierte la polaridad del enunciado de frecuencia.

2. **w0011 `cl-entradas-sirven-para-encontrar-bias`** — "Encontrar las entradas sirve para encontrar el bias en general."
   asr-00021/00022 ("muy importante para encontrar las entradas para encontrar el bias para todo") enumera propósitos de los **rangos**; el claim invierte la relación afirmando una cadena entradas→bias que la fuente no dice.

### PARTIAL (3)

- **w0001 `cl-dos-zonas-rectangulares-azules`** y **w0002 `cl-dos-bandas-azules`** (MATERIAL=NO): hay dos zonas sombreadas a la derecha del gráfico 5M, pero sólo la inferior es claramente azul; la superior se ve gris (frames p540000/p720000/p1080000).
- **w0014 `cl-ejemplos-reales-rangos-claros`** (MATERIAL=NO): "ya ha quedado claro" se refiere al concepto/esquema previo, no a los "ejemplos reales de rangos", que se presentan justo después (asr-00025).

### DUPLICATE (42, 18,7%)

Concentrados donde el instructor reformula: bienvenida/curso (w0002, w0004), definición de rango re-extraída por componentes (w0006, w0007), re-observaciones de etiquetas (w0009, w0010, w0013), reafirmaciones en cadena (w0020–w0023, w0025), y sobre todo las ventanas de re-narración w0027/w0029/w0030/w0031 (21 duplicados entre ellas). Las proposiciones duplicadas son idénticas; la primera aparición queda etiquetada CORRECT en su ventana.

## Missing knowledge

- **w0014 MISSING_NON_MATERIAL**: banda vertical azul (12-jun) y zona gris de la demo 4h no extraídas (sólo ayudas visuales).
- **w0015 MISSING_NON_MATERIAL**: motivo del rango alcista ("la vela va por debajo y cierra adentro", asr-00028) no capturado en el claim.
- **w0019 MISSING_NON_MATERIAL**: matiz de que la nomenclatura de tipos de rango es acuñada por el propio instructor ("nosotros hemos llamado así", asr-00035).
- Resto de ventanas: NONE. No se detectó proposición material del contenido de trading (definición de rango, completación, cadena, bias/target, failure swing) ausente del L1 local.

## Observaciones de calidad (no afectan etiquetas)

- Los evidence_ids de claims hablados citan consistentemente segmentos asr que contienen la proposición (incluyendo solapes con ventanas previas, p. ej. w0002→asr-00001, w0027→asr-00051): sin referencias rotas en el rango auditado.
- Los niveles de precio extraídos (1,15728 / 1,15744 / 1,15797 / 1,16148 / 1,15803 / 1,14748 / 1,15352 / 1,14968 / 1,15179 / 1,14973 / 1,15160) coinciden con los rótulos de los frames.
- Varios claims de parámetro de gráfico (símbolo, temporalidad, diálogos de UI) son MATERIAL=NO y conviven con el contenido material sin desplazarlo; la proporción de trivia de UI por ventana es baja (máx. en w0019: 7 de 8 NO, pero la ventana solo contiene la transición 1D→15M y el announcement de más tipos de rango sí extraído como material).
