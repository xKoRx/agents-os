# CLF-K05 — KNOWLEDGE CORRECTIONS (FASE 7 + correcciones documentales)

Correcciones a la capa de conocimiento/investigación. Los claims originales NO se tocan (autoridad intacta); se corrigen documentos derivados y decisiones registradas. Ninguna corrección modifica el curso para justificar una implementación.

## KC-01 — Catálogo canónico: presente y verificado (cierra decisión Owner nº 2 de Q04)

Q04 §6 declaraba `STRATEGIES-CATALOG.md` ausente del vault. Verificación K05: existe en `knowledge-library/clutifx/strategies/STRATEGIES-CATALOG.md` (SHA256 `4c47131423ded9cf781915538ae06e2d7b7e5a12b2d76da0ea41995bda46907f`, 387 líneas, encabezado con re-domiciliación 2026-10-24 y contrato de iteración). Estado Q04: RESUELTA; el maestro de investigación ya lo enlaza. Acción: actualizar la línea de Q04 con puntero a este documento (no reescribir Q04 histórico).

## KC-02 — «IMPLEMENTATION_DEFECT: ninguno detectado» de Q04 era falso para S03/S04/S05

`CLF-Q04-SIGNAL-EQUIVALENCE.md` atribuyó la equivalencia C02≡S03/S04/S05A/B a «defaults compartidos del módulo». Causa real: miswiring del gate (`decision.go:196/390`, `session_decision.go:140/246` consultan `NativeAggregate`; `Aggregate()` sin llamadas de producción) — registrado por el ciclo E05 como `MISWIRED_CONFIG (E05-01)` y confirmado por lectura directa del código en K05. Consecuencia documental: las clases `SIGNAL_EQUIVALENT` de S03/S04/S05A/B describen comportamiento observado, no equivalencia experimental válida; sus campañas no midieron el eje declarado. Las 10 fuentes de señal reales de Q04 siguen siendo correctas como hecho económico; la interpretación «el eje es inerte por defaults» se corrige a «inerte por cableado».

## KC-03 — Adjudicación KRR-003 (pasa de abierta a adjudicada-parcial)

La ficha queda: conjunción excedida CONFIRMADA por fuente en 3 ejes (OB, predicado de reacción, ventana) — ver `CLF-K05-FAILURE-SWING-ADJUDICATION.md`; residuo de vídeo V-01/V-02 acotado. `RECOMMENDED_ACTION` pasa a FIX_CODE (con regresiones y gates propios) + REVIEW_VIDEO residual. La regla «no relajar sin evidencia» se respeta: la relajación propuesta ESTÁ respaldada por claims concretos (c-0029, c-0047, c-0041, c-0048) y se aplica como corrección con fixtures, no como aflojamiento de parámetros.

## KC-04 — Discrepancia S08 (matriz vs código) registrada para decisión

Matriz: «S08 = salida DOL en estrategia de sesión (base temporal)»; código: C03 base exit = target. La fuente da ambas salidas sin fijar base. Ver F-K05-12. Acción: anotar en la matriz v1.1 cuando el Owner decida; entre tanto S08 queda NO_MATERIALIZADA_CON_DISCREPANCIA.

## KC-05 — Correcciones menores al catálogo derivado (delta, sin tocar claims)

El contrato del catálogo exige re-derivación cuando la biblioteca cambie; K05 no cambia la biblioteca, pero deja tres precisiones pendientes de la próxima re-derivación: (a) STR-006 debe reflejar la adjudicación (OB opcional; reacción=rango opuesto) en su ficha; (b) STR-005 debe decir explícitamente «transversal a STR-001..004» en la ficha (ya lo implica el texto del setup, hacerlo estructural); (c) la ficha STR-003/004 debe mencionar la activación de rangos por FS (ch07 c-0197–c-0206) como parte del escenario enseñado. Ninguna de las tres contradice un claim: precisan el derivado.

## KC-06 — Fichas KRR 1..7 — resolución K05

```text
KRR-001 CONFIRMADA (estructural). Sin video nuevo. La pregunta al Owner sigue:
  identidad adaptada de ancla (precedente S06/S07) o archivo como
  fiel-al-curso-no-operable. K05 añade el dato: coste de oportunidad medido
  (sólo la vela 13:00 ET es operable de la rejilla 4h del curso). Estado: CLARIFY_SPEC.
KRR-002 CONFIRMADA (estructural). Intersección [05:00,09:00]∩[09:30,15:55)=∅ por
  construcción. Misma decisión única que KRR-001. Estado: CLARIFY_SPEC.
KRR-003 ADJUDICADA-PARCIAL (KC-03). FIX_CODE listo (F-K05-02..05) + vídeo V-01/V-02.
  Tras el fix: G0→G2C propios de C06/S15/T04 con fixtures FX-01..05. Estado: FIX_CODE.
KRR-004 CONFIRMADA (el modo de resolución no desplaza el ancla). Misma decisión de
  ancla. Estado: CLARIFY_SPEC.
KRR-005 SIN CAMBIOS (re-verificada F-K05-15). Estado: BLOCKED_SPEC (parámetro Owner).
KRR-006 SIN CAMBIOS. Añadido: el seam de motivos externos del FS es la misma
  decisión de datos (SMT motivo-1 del FS también desbloquea). Estado: BLOCKED_DATA.
KRR-007 ACTUALIZADA: materialización S08 bloqueada por la discrepancia KC-04
  (decidir base de salida primero); T03 es implementable hoy con
  MidTermDOL().Taken (dol.go ya soporta scope midterm). Estado: FIX_CODE (post-decisión).
```

## KC-07 — Feedback a la regla de duplicación (decisión Owner nº 3 de Q04)

La política «1 campaña por fuente de señal + alias declarado» queda reforzada por K05: el caso S03–S05 demuestra que N campañas del mismo knob mal cableado compran la misma evidencia. Ampliación propuesta: además de la equivalencia por ejecución, verificar la EQUIVALENCIA POR CABLEADO antes de comprar una variante (auditoría de que el knob alcanza una decisión — el e05 ya lo hace; volverlo paso estándar del ciclo).

## KC-08 — Lección de método para la biblioteca

La extracción fue correcta (los claims sostienen la adjudicación); el hueco fue de SPEC DE DETECTOR: la «reacción» de ch01/ch06 quedó operacionalizada sin anclar cada sinónimo dicho («creando rango», «reacciona») al mismo predicado. Para futuras extracciones: cuando una palabra del instructor tenga definición estructural propia en el curso (aquí: rango), el detector debe componer ESE átomo, no un proxy de superficie. Registrado como feedback de sesión.
