# CLF-Q04 — KNOWLEDGE REVIEW QUEUE (actualización de KRR-001..007)

Regla: ninguna ficha se cierra por interpretación del ejecutor; se actualiza cada ficha con la evidencia Q04 y se deja la pregunta exacta al Owner. Formato canónico del runbook; timestamps desde `CLAIMS.md` del knowledge library.

---

```text
REVIEW_ID: KRR-001 (ACTUALIZADA Q04)
identity: CLF-STR-001 / CLF-VAR-C01 · CURRENT_STATUS: SESSION_INCOMPATIBLE
SOURCE: ch07-setups (London ideal) + ch02-time (velas 21/17/01 ET); knowledge-path vigente.
DELTA_Q04: NQU6 completo: 1 emisión @01:00 ET (06-23), 0 compras. Fixture económico: sin intersección con [09:30,15:55) ET por construcción. Coste de oportunidad medido: la familia ancla-4h operable sería la 13:00 ET.
ROOT_CAUSE: CONFIRMED (estructural, no defecto).
KNOWLEDGE_QUESTION (sin cambios): ¿adaptación de ancla autorizada como identidad NUEVA, o C01 queda fiel-al-curso no-operable en E2T?
VIDEO_REVIEW_TARGET: ch07 CLAIMS.md (minutos del escenario 1).
RECOMMENDED_ACTION: CLARIFY_SPEC. RETEST_SCOPE: G2B de la identidad adaptada si se autoriza.
```

```text
REVIEW_ID: KRR-002 (ACTUALIZADA Q04)
identity: CLF-STR-004 / CLF-VAR-C04 · CURRENT_STATUS: SESSION_INCOMPATIBLE
DELTA_Q04: NQU6: 6 emisiones (4×05:00 + 2×09:00 ET), 0 compras; NQZ6: 3/3 fuera. Ventana 05:00–09:00 ET vs apertura E2T 09:30: intersección imposible.
KNOWLEDGE_QUESTION (sin cambios): ¿algún escenario del curso contempla entradas NY dentro de 09:30–15:55, o C04 es estructuralmente no-operable en E2T sin adaptación?
VIDEO_REVIEW_TARGET: ch07 escenario NY reversal; c-0113 [26:18–26:31] ch04.
RECOMMENDED_ACTION: CLARIFY_SPEC. RETEST_SCOPE: G2B de la identidad adaptada si se autoriza.
```

```text
REVIEW_ID: KRR-003 (ACTUALIZADA Q04 — CONJUNCIÓN AUDITADA, SIGUE ABIERTA)
identity: CLF-STR-006 / C06, S15, T04 · CURRENT_STATUS: VALID_RARE_NO_ACTIVITY
DELTA_Q04 (auditoría source-vs-code): el detector exige reacción Y order block Y motivo DENTRO de la ventana (strict = la única vela siguiente). El curso R11·c-0029 identifica con "reacción + UNO de los motivos"; R12·c-0047 trata el OB como OPCIONAL ("puedes esperar al order block si quieres"); R6 permite entrar sin activación clásica; R9 prohíbe anticipar por el extremo-de-final-de-vela solo (el gate de motivo es fiel). Con motivos 1 (SMT) y 3 (brokers) no disponibles en single-feed, la implementación queda en la conjunción máxima posible de una fuente ambigua. Números Q04: ready 12.060/14.037, 0 setups en 69 rt NQZ6 + 54 rt NQU6 de ventanas equivalentes y en el trimestre completo.
ROOT_CAUSE: HYPOTHESIS (sin resolver): rareza genuina vs conjunción excedida.
KNOWLEDGE_QUESTION: ¿la identificación en vivo exige OB además de reacción+motivo, y en qué vela debe confirmarse la reacción? ¿Es esperable 0 setups en 69+9 sesiones?
VIDEO_REVIEW_TARGET: ch06, minutos de R3/R11/R12 (c-0004, c-0029, c-0038, c-0047) en CLAIMS.md.
RECOMMENDED_ACTION: REVIEW_VIDEO (rara ⇒ KEEP_RARE definitivo; conjunción excedida ⇒ FIX_CODE con regresiones y G2A/G2C propios). NO se relajó nada en este shot.
RETEST_SCOPE: G2A/G2C del detector ajustado si procede; jamás el histórico.
```

```text
REVIEW_ID: KRR-004 (ACTUALIZADA Q04)
identity: CLF-STR-002 / S01, S02, S17 · CURRENT_STATUS: SESSION_INCOMPATIBLE
DELTA_Q04: NQU6: 4/4 señales por variante fuera de ventana (emisiones 17:00Z/21:00Z/05:00Z = 13:00/17:00/01:00 ET); el modo de resolución TS no desplaza el ancla. NQZ6: 0 señales en 9 sesiones.
KNOWLEDGE_QUESTION (sin cambios): ¿debe la reacción del TS emitir dentro de la sesión NY cash, o la confirmación por vela del curso implica horas fuera de la ventana E2T?
VIDEO_REVIEW_TARGET: ch02 R5; ch04 R23; ch09 c-0035/c-0036 (minutos en CLAIMS.md).
RECOMMENDED_ACTION: CLARIFY_SPEC (misma decisión de ancla que KRR-001/002). RETEST_SCOPE: trazas existentes; identidad nueva si se autoriza ancla.
```

```text
REVIEW_ID: KRR-005 (SIN CAMBIOS MATERIALES)
identity: CLF-STR-002 / T02 · CURRENT_STATUS: BLOCKED_SPEC
DELTA_Q04: re-verificado: ningún claim declara ancho extra de stop para la entrada temprana; la matriz prohíbe inventarlo. La geometría Q04 añade contexto: el riesgo ejecutado real es 20×ATR×q ($325–465), no $500 fijos — el parámetro extra del Owner definiría la desviación sobre esa base.
KNOWLEDGE_QUESTION: ¿qué ancho extra (ticks) declara el curso para el stop temprano, si lo declara?
VIDEO_REVIEW_TARGET: ch02 R5 y ch11 (minutos en CLAIMS.md); NOT_RESOLVED si ningún minuto lo declara.
RECOMMENDED_ACTION: CLARIFY_SPEC. RETEST_SCOPE: G0→G4 propio cuando exista el parámetro autorizado.
```

```text
REVIEW_ID: KRR-006 (SIN CAMBIOS)
identity: STR-007/008 / C08, T05 · CURRENT_STATUS: BLOCKED_DATA
DELTA_Q04: verificación física re-confirmada (sólo NQ en corpus; sin calendario con timestamp). Nota de viabilidad Q04: aún con datos, la lección de frecuencia aplica también a estas estrategias.
KNOWLEDGE_QUESTION: ¿adquiere el Owner ES/YM/DXY sincronizados + calendario económico con timestamp?
RECOMMENDED_ACTION: BLOCK_DATA (decisión de datos). RETEST_SCOPE: G0→G4 con datasets sellados.
```

```text
REVIEW_ID: KRR-007 (SIN CAMBIOS DE FONDO)
identity: STR-003/004 / S08, T03 · CURRENT_STATUS: NEEDS_ITERATION
DELTA_Q04: continúan declaradas sin materializar. Advertencia de viabilidad Q04: cualquier materialización nueva hereda el problema de frecuencia×objetivo (el funnel de C03/C04 muestra 2–6 ejecuciones/trimestre); conviene resolver primero la decisión de anclas (KRR-001/002/004) para no gastar otro ciclo en identidades inalcanzables.
KNOWLEDGE_QUESTION: ¿confirma el Owner materializar S08/T03 y en qué orden respecto a las decisiones de ancla?
RECOMMENDED_ACTION: FIX_CODE (materialización) en el ciclo siguiente. RETEST_SCOPE: G0→G4 propio.
```

## Estado de la cola

7 fichas; ninguna cerrada por interpretación; KRR-001/002/003/004 actualizadas con evidencia Q04 (números exactos y hallazgo de conjunción FS); KRR-005/006/007 sin cambio de fondo. Decisiones Owner nuevas no-KRR (costeo $120 vs provider_fee $50; catálogo canónico ausente; política de duplicación de campañas equivalentes) viven en `CLF-Q04-STRATEGY-DECISIONS.md`.
