# CLF-K05 — VIDEO REVIEW QUEUE (para el Owner)

La evidencia textual y de frames ya adjudicó la mayor parte de KRR-003 (ver `CLF-K05-FAILURE-SWING-ADJUDICATION.md`); lo que queda aquí es lo que SOLO audio/vídeo puede cerrar. Ninguna corrección se aplica antes de la decisión; los fixes de fuente (F-K05-02/03/04/05) quedan listos y son independientes de estas dudas residuales. Timestamps citados desde los CLAIMS.md; ninguno inventado.

```text
REVIEW_ID: V-01 (residuo KRR-003 · prioridad P0)
strategy_id: CLF-STR-006 · variantes C06/S14/S15/T04
chapter_window: ch06-failure-swing, minutos 09:37–09:55 (c-0046 y c-0047)
question: En el ejemplo espejo (low fallado), ¿el order block es requisito de la
  identificación en la vela de 1h, o la frase «vemos la reacción alcista, vemos
  cómo se crea un order block, y ahí decimos» es narración del ejemplo — de modo
  que c-0047 «puedes esperar si quieres al order block» confirma la OPCIONALIDAD
  en todos los casos?
evidence: c-0029 (procedimiento canónico SIN OB) vs c-0046 (espejo CON OB en la
  frase de identificación) vs c-0047 (opcionalidad explícita en el mismo ejemplo).
what_changes: si el Owner adjudica «OB requerido en 1h», la corrección F-K05-02
  pasa de «OB opcional» a «OB opcional fuera de 1h, requerido en la vela del
  motivo»; el resto del fix no cambia.
fragments: f-000959 (gráfico 15m 28/4/2025 del segundo ejemplo), s-000937–s-000954.

REVIEW_ID: V-02 (residuo KRR-003 · prioridad P1)
strategy_id: CLF-STR-006
chapter_window: ch06, minutos 02:49–03:12 y 06:03–06:31 (c-0012, c-0029) + frames
question: «reacciona ya para abajo creando algún rango bajista»: ¿el rango
  bajista de la reacción se lee en la MISMA temporalidad donde se observa el
  fallo (1h), o vale cualquier TF menor (el propio instructor dice «en 30 en 15
  seguramente ya hay rangos» c-0013)?
evidence: c-0012/c-0029 (sin TF especificada) + c-0013 (30/15) + c-0040 (motivo
  se ve en 1h, creencia dicha).
what_changes: define sobre qué cadena se computa la reacción del fix (1h por
  defecto propuesto); si vale TF menor, la emisión puede anticiparse.

REVIEW_ID: V-03 (parámetro Owner · prioridad P2)
strategy_id: CLF-STR-006 (motivo 2) · relaciona S14/S15
chapter_window: ch07-setups, minuto ~20:50–21:10 (c-0202) + ch06 c-0010/c-0014
question: El «final de vela» del motivo 2, ¿se fija como fracción de vela (el
  ejemplo dice «como en el 15% del final de la vela») o como ventana absoluta de
  minutos? Si es fracción, ¿15% es regla o dato visual del ejemplo?
evidence: c-0202 («15% del final de la vela», dato visual no verbalizado como
  regla); c-0014 («4.15/4.20… como la parte final»); c-0052 (16.20 en vela de 8h).
what_changes: semántica del parámetro EndMinutes (absoluta hoy) vs nueva
  EndFraction; sin respuesta, EndMinutes sigue como OP congelada.

REVIEW_ID: V-04 (fidelidad pendiente 8h · prioridad P3)
strategy_id: CLF-STR-002 (variante 8h del pendiente)
chapter_window: ch01, contexto de c-0054 (8h: pendiente sin tomar extremo)
question: La lectura implementada («abre más allá del CLOSE previo — gap —,
  respeta el extremo del rango y cierra adentro») es la operacionalización
  declarada; ¿el instructor dibuja el pendiente-8h como gap de apertura o como
  vela que abre dentro/desde el cuerpo anterior sin tocar el extremo?
evidence: c-0054 (enunciado sin geometría); pendiente.go scanEightHourVariant
  (lectura declarada).
what_changes: sólo el predicado de la variante 8h; sin respuesta, se mantiene.

REVIEW_ID: V-05 (entrada anticipada · prioridad P3, ya clasificada en el catálogo)
chapter_window: ch01 c-0052/c-0053
question: sin cambio — la «entrada anticipada del rango sin cierre» sigue
  INSUFFICIENT_SPECIFICATION (el método no se enseña); listada aquí sólo para
  cerrar el loop con la cola del catálogo §9.

## Decisión Owner NO-vídeo pendiente (recordatorio, no nueva)

- KRR-001/002/004 (anclas London/NY vs ventana E2T): CLARIFY_SPEC — identidad
  adaptada nueva (precedente S06/S07) o archivo fiel-al-curso no operable. Es la
  decisión de mayor impacto económico pendiente: sin ella, la familia 4h sólo
  puede operar la vela de las 13:00 ET.
- KRR-005 (ancho de stop de la entrada temprana): parámetro o archivo.
- F-K05-12 (base de salida de C03): target (código) o temporal (rótulo matriz).
- F-K05-06/07/18/19 (refinado en sesión, FS-activación, entrada OB, PDM):
  autorizar materialización como identidades nuevas pre-declaradas (todas
  fuente-backed) o dejarlas documentadas.
```
