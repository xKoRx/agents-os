# CLF-K05 — STATUS

```text
CLF-K05 — KNOWLEDGE FINAL

HOST: DAEDALUS
CATALOG_SOURCE_SHA: 4c47131423ded9cf781915538ae06e2d7b7e5a12b2d76da0ea41995bda46907f (knowledge-library/clutifx/strategies/STRATEGIES-CATALOG.md — presente y verificado)
ECHO_AUDITED_SHA: e8c2e47ee5575698b83924ecbbc413ec2787ce6d (experiment/clutifx-s01, worktree limpio, READ-ONLY vía git archive)

STRATEGIES_AUDITED: 9 completas (STR-001..009) + STR-008b + 7 setups parciales + 24 componentes + 13 reglas de gestión + 4 red flags (universo completo del catálogo)
VARIANT_IDS: 34 (C01–C08, S01–S21, T01–T05)
PARAMETER_SETS: 35 (S05 con 2 sets S05A/S05B)
RULES_CHECKED: fuente ch01–ch12 confrontada claim-a-claim contra 18 archivos fuente de v3/sdk/futures/strategies/clf/ leídos completos (detectors + pipeline + decision + session + config + strategy)

SOURCE_MATCH: STR-002 maquinaria completa; sesiones C01/C03/C04 fieles con huecos declarados; STR-005 mecánica fiel con alcance reducido; STR-009 proxy declarado; SMT/noticias BLOCKED_DATA fiel; red flags y DOL fieles; anclas S06/S07 fieles
MISSING_RULES: 7 registradas (F-K05-01,05,06,07 P1 · F-K05-18,19,08 P2) — detalle en CLF-K05-MISSING-AND-EXTRA-RULES.md
EXTRA_RESTRICTIONS: 3 P0 en Failure Swing (OB obligatorio, predicado de reacción, ventana) + colapsos declarados OK
TEMPORAL_ERRORS: 0 nuevos (la secuencia motivo→fallo→reacción del FS está bien ordenada en el código; la ventana es restricción, no error de orden)
BOOLEAN_ERRORS: 1 confirmado (gate de bias nativo hace inertes S03/S04/S05 — F-K05-01, coincide con e05 MISWIRED_CONFIG E05-01) + conjunción FS (F-K05-02)
UNRESOLVED_SOURCE: 7 decisiones Owner vigentes (V-01..V-04, F-K05-12, KRR-001/002/004 anclas, KRR-005) — ninguna cerrada por interpretación del ejecutor
VIDEO_REVIEW_REQUIRED: 5 fichas acotadas con minuto exacto (CLF-K05-VIDEO-REVIEW-QUEUE.md; V-01/V-02 residuo KRR-003)

FAILURE_SWING_VERDICT: EXTRA_RESTRICTION_CONFIRMED_PARCIAL — OB opcional (c-0047), reacción=creación de rango opuesto (c-0029), ventana sin cota de 1 vela; la frecuencia 0-setups no puede atribuirse a rareza genuina mientras persista la conjunción; fix listo (H2–H5) + vídeo residual

CORRECTIONS_READY_FOR_HEFESTO: 8 (H1–H8 en CLF-K05-HEFESTO-IMPLEMENTATION-HANDOFF.md; H6–H8 como identidades nuevas pre-declaradas)
CORRECTIONS_BLOCKED_BY_OWNER: 6 grupos (anclas, T02, datasets SMT/noticias, salidas personales, ejes OB/PDM, semántica neutral del motor)

HANDOFF_PATH: 10-projects/Echo Futures/artifacts/clutifx-strategy-research/k05/CLF-K05-HANDOFF.json
HANDOFF_SHA256: fbce00c23940e7c05b52638241c174702e5971f218b165797d3a63c3daa91ccf

ENTREGABLES (SHA256):
  CLF-K05-SOURCE-CERTIFICATION.md            8e41e64698e347ac3c3d4a86d41cfdb92654e08b5289a25449feb8dcbffeff91
  CLF-K05-ALL34-35-CONFORMANCE.csv           d3517fd14374dfd2afbbec5760cc8eb3834406ab59fdf9eb3127dcf75515a464
  CLF-K05-MISSING-AND-EXTRA-RULES.md         10436824220da3b409ae0281944f19abbe1658c2a50e503cbed270e920546d8d
  CLF-K05-FAILURE-SWING-ADJUDICATION.md      fcee71776a97f886a6001eb30e5bfe3e4724694dffb21f74a126ce6641c4a959
  CLF-K05-VIDEO-REVIEW-QUEUE.md              51ff8743b05adf1c88ffd3f1fa0daf001e675796be6e138ce658308ee6d37c3d
  CLF-K05-FIXTURE-SPECIFICATIONS.md          add241212d6e18140cd388bce648aef8a2082730ab660996e9c9fd6ae97413c8
  CLF-K05-KNOWLEDGE-CORRECTIONS.md           816febc89c2233da6fdea0b9094a3088e95e7f50dba88bf04f03505871652fca
  CLF-K05-HEFESTO-IMPLEMENTATION-HANDOFF.md  4f9fe98386262be41c0981d5ae3053ff5b5e3ac09cebe1767e9d8ab09707e1e7
  CLF-K05-HANDOFF.json                       fbce00c23940e7c05b52638241c174702e5971f218b165797d3a63c3daa91ccf
  CLF-K05-STATUS.md                          (este documento)

AGENTS_OS:
  planner: actualizado (delta en 10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md)
  agent_run: registrado (80-agents/journal/logs/)
  change_log: registrado (80-agents/journal/logs/)
  feedback: 1 nota de sesión (lección KC-08: detectores deben componer los átomos estructurales del curso, no proxies de superficie)
  session_close: agents-os-session-close ejecutado por pedido explícito del mandato
  sync_verified: ver la sección Sync de abajo

OWNER_ACCEPTANCE: REVIEW
```

## Resumen ejecutivo (5 líneas)

1. La extracción del curso fue correcta y el catálogo canónico existe; la brecha está en la ESPECIFICACIÓN de detectores: tres reglas de Failure Swing quedaron sobre-restrictivas respecto de la fuente (OB obligatorio vs opcional dicho en c-0047; reacción como cierre-bajo-nivel vs «creando rango opuesto» dicho en c-0029; ventana de 1 vela sin fuente) — adjudicadas por texto, con fix y fixtures listos.
2. Hallazgo P1 nuevo confirmado en código: el gate de entrada consulta SIEMPRE el bias nativo (`NativeAggregate`), por lo que las variantes S03/S04/S05 (EMA/estructura/DMI-ADX) son inertes por cableado — coincide con el registro E05 `MISWIRED_CONFIG` y corrige la lectura de Q04 («ningún defecto»).
3. Huecos de alcance fuente-backed: el refinado (STR-005) no es expresable en las estrategias de sesión (la entrada ideal de London/NY del curso es refinada), y el FS como activador de rangos en NY (el caso ensañado ch07 c-0197–c-0206) no produce señales — ambos listos como identidades nuevas pre-declaradas.
4. Las 35 configuraciones quedan cubiertas una a una en el CSV: 17 con comportamiento propio demostrado, 4 aliases verificados, 4 con restricción confirmada, 3 bloqueadas por datos/spec (sin cambio), 3 no materializadas con spec, y el resto en in-sample inerte documentado.
5. Sin modificación silenciosa del curso: toda corrección cita claims concretos; las 7 dudas restantes están formuladas para el Owner con minuto de vídeo exacto; el histórico completo sigue prohibido (0 pases, G5 eligible=0).

## Sync

Destinos disponibles desde Daedalus: el vault canónico local es la superficie de publicación (este directorio). No existe evidencia de un canal de sincronización automático k05→Hefesto en este host; el handoff se declara PUBLICADO EN VAULT (verificable por SHA) y NO ENTREGADO a Hefesto hasta que un ciclo de implementación lo consuma — no se declara recepción por Hefesto.
