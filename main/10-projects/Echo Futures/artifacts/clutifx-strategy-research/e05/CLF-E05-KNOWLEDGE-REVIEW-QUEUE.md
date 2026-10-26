# CLF-E05 — KNOWLEDGE REVIEW QUEUE (actualización E05)

Regla intacta: ninguna ficha se cierra por interpretación del ejecutor. Estado base: `q04/CLF-Q04-KNOWLEDGE-REVIEW-QUEUE.md` (KRR-001..007). Cambio estructural de este ciclo: **el handoff K05 no existe ⇒ `HANDOFF_REQUIRED` global** para toda corrección dependiente de conocimiento.

---

```text
REVIEW_ID: KRR-001..007 — DELTA_E05
DELTA: sin cambios de fondo. KRR-003 (conjunción Failure Swing) sigue abierta y queda explícitamente bloqueada por HANDOFF_REQUIRED (la fuente que la resuelve vive en K05). KRR-001/002/004 (anclas/sesión), KRR-005 (stop extra), KRR-006 (datos SMT/noticias) y KRR-007 (S08/T03) mantienen su pregunta al Owner.
BLOQUEO_NUEVO: ausencia física del handoff K05 (vault y Hefesto); ver CLF-E05-K05-FINDINGS-DISPOSITION.md.
```

```text
REVIEW_ID: KRR-008 (NUEVA E05 — hallazgo de cableado, no de lectura del curso)
identity: CLF-STR-002 / S03, S04, S05A, S05B · CURRENT_STATUS: MISWIRED_CONFIG (E05-01)
SOURCE: matriz de experimentos §7 (sustituciones de bias); claim exacto pendiente de K05 (handoff ausente).
EXPECTED_BEHAVIOR: el motor de bias configurado (ema/structure/dmi_adx) debe gobernar la condición de entrada según su configuración.
IMPLEMENTED_BEHAVIOR: los motores computan (bias_engines.go; fixtures en bias_test.go con agregado EMA propio) pero el gate de entrada consulta exclusivamente el control nativo: decision.go:196/390 y session_decision.go:140/246 llaman p.bias.NativeAggregate(); Aggregate() (bias.go:366) no tiene ninguna llamada en producción. El eje no puede diferenciarse de C02 en ningún mercado.
OBSERVED_LAST_CONTRACT: NQU6 — ejecución idéntica a C02 al céntimo (Q04 EXEC-MASTER), 3 rt 2W/1L por config.
FIRST_CAUSAL_DIVERGENCE: el gate (ReasonBiasNotFavoring) consume el agregado nativo, no el del motor configurado.
ROOT_CAUSE: CONFIRMED a nivel de cableado; la semántica correcta (sustitución pura vs conjunción con nativo vs sólo-diagnóstico) es UNKNOWN sin fuente.
KNOWLEDGE_QUESTION: ¿qué relation exacta debe tener el motor sustituido con el gate de entrada (reemplaza al rango nativo, se conjuga, o el nativo permanece como gate y el motor es sólo diagnóstico)? ¿Y qué papel juega bias_adx_threshold en esa relación?
VIDEO_REVIEW_TARGET: NOT_RESOLVED sin K05 — resolver desde CLF-K05 (capítulos de bias) cuando exista el handoff.
RECOMMENDED_ACTION: FIX_CODE tras decisión Owner; toda corrección crea identidades nuevas (S03'/S04'/S05' con sets A/B) y exige repetir G1→G2C→G3 propio antes de cualquier G4.
RETEST_SCOPE: G0–G3 de las identidades nuevas; jamás el histórico; los recibos existentes quedan como evidencia de lo que corrió (réplicas de facto de C02), no del eje.
```

## Estado de la cola

8 fichas (KRR-001..007 sin cambio de fondo + KRR-008 nueva); ninguna cerrada por interpretación; bloqueo transversal `HANDOFF_REQUIRED` registrado en `CLF-E05-K05-FINDINGS-DISPOSITION.md`.
