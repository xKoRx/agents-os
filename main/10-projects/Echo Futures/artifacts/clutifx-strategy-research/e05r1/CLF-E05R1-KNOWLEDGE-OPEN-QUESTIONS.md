# CLF-E05R1 — KNOWLEDGE OPEN QUESTIONS

Cola Owner vigente al cierre del ciclo · `OWNER_ACCEPTANCE: REVIEW`

```text
REVIEW_ID: E05R1-1 (H6 · refinado en sesión · prioridad P1)
identities: C01r/C03r/C04r (nuevas, hash propio)
question: ¿Autorizar el eje RefineTF en specs de sesión (relajar config.go:205-207/224-226,
  reutilizando pendingRefine/resolveRefine con la vela de sesión correspondiente)?
source: ch04 §2; ch07 c-0214 («súper clave»); catálogo STR-005 transversal a STR-001..004
what_changes: 3 identidades nuevas con ciclo G0→G4 propio cada una (fixtures FX-06 ya especificados en K05).
  Frecuencia potencialmente material en London/NY (la entrada ideal del curso ES refinada).
status: OWNER_AUTHORIZATION_REQUIRED — no implementado; cero campañas.

REVIEW_ID: E05R1-2 (H7 · FS como activador de rangos en sesión · prioridad P1)
identities: C03r/C04r variantes FS-activadas (depende de H2-H4, ya corregidos)
question: ¿Autorizar la premisa «rango claro activable por veredicto FS legítimo» además del sweep
  clásico en C03/C04 (el caso ensañado del curso, ch07 c-0197-c-0206)?
source: ch07 c-0197-c-0206; ch06 c-0028/c-0057
what_changes: fixture FX-07; día del curso produce señal hoy inexistente.
status: OWNER_AUTHORIZATION_REQUIRED.

REVIEW_ID: E05R1-3 (H8 · S08/T03 · prioridad P2)
question: (a) S08 sigue bloqueada por F-K05-12 (base de salida de C03: target [código] o temporal
  [rótulo matriz]) — decisión Owner primero; (b) T03 es implementable hoy (MidTermDOL().Taken) —
  ¿materializar con G0→G4 propio?
status: (a) BLOCKED_SPEC (F-K05-12); (b) OWNER_AUTHORIZATION_REQUIRED (KRR-007).

REVIEW_ID: E05R1-4 (F-K05-18/19 · entrada OB y PDM · prioridad P2)
question: ¿Autorizar los ejes de entrada «OB confirmado como 2º detonante» (ch04 c-0034/c-0036/c-0039)
  y PDM (ch04 c-0017, c-0096-c-0101; ch03 c-0092/c-0213)? Ambos fuente-backed, hoy sin camino de señal.
status: OWNER_AUTHORIZATION_REQUIRED.

REVIEW_ID: E05R1-5 (V-01/V-02 · residuo vídeo KRR-003 · prioridad P0/P1)
question: SIN CAMBIO respecto de CLF-K05-VIDEO-REVIEW-QUEUE: (V-01) ¿OB requerido en el espejo 1h
  (ch06 09:37-09:55)? (V-02) ¿TF de la reacción (ch06 02:49-03:12/06:03-06:31)?
what_changes: V-01 ⇒ el default fs_order_block_mode pasa a required-en-1h (H2 ya tiene el knob);
  V-02 ⇒ la cadena de la reacción podría bajar de TF (anticiparía emisiones).
status: REVIEW_VIDEO — la corrección implementada usa la lectura dominante y la alternativa
  queda reproducible con `required`.

REVIEW_ID: E05R1-6 (S03 QUARTER_NO_PASS · prioridad P2 — decisión comercial, no de conocimiento)
observation: la identidad bias-EMA opera con frecuencia real (14 rt/quarter, 2 cuentas) pero la
  muestra perdió (5W/9L, net -744,86). La meta era alcanzable (14 × techo 470,02 ≥ 3.000): la causa
  es NEGATIVE_EDGE de la muestra, no inalcanzabilidad. Sin cambios de código/parámetros para
  «conseguir» un pase (regla dura). Queda al Owner: repetir el quarter en otro contrato, archivar
  la identidad, o autorizar ejes de frecuencia (E05R1-1/2/4).
status: QUARTER_NO_PASS (NEGATIVE_EDGE) — evidencia preservada, G5 prohibido.

Sin cambio: KRR-001/002/004 (anclas), KRR-005 (stop extra), KRR-006 (datasets SMT/noticias),
V-03 (fracción del motivo 2), V-04 (geometría pendiente-8h), V-05.
```
