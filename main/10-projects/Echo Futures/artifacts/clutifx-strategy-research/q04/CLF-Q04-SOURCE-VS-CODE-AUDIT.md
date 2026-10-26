# CLF-Q04 — SOURCE VS CODE AUDIT (FASE 5)

Alcance: muestra material STR-001..006, 009 sobre el HEAD de referencia `e8c2e47e` (worktree limpio). Método adversarial: reglas literales del curso (`chNN/rules.md` + `CLAIMS.md`) confrontadas con el código (`v3/sdk/futures/strategies/clf/`) y con el comportamiento económico observado en recibos. No se usan como evidencia los tests del propio implementador.

## 1. Inventario de fidelidad

| Estrategia | Reglas enseñadas (fuente) | Código | Veredicto |
|---|---|---|---|
| STR-001 London ideal (C01) | sopa previa a London, expansión en vela 01:00, DOL a favor, red flags, stop en la sopa, salida 05:00 (ch07 R2/R3/R14/R16/R27) | `session_decision.go::entryLondon` cita claim-a-claim; ventana `[01:00,05:00)` ET | FIEL. Emisiones 01:00 ET estructuralmente fuera de ventana E2T |
| STR-002 pendiente→DOL (familia maestra) | rango+pendiente, TS con reacción, stop en el sweep, DOL objetivo (ch01–ch04) | maquinaria STR-002 + rejilla 4h curso 21/17/1/5/9 ET DST-IANA (`session_ctx.go`) | FIEL. Sólo la vela 13:00 ET cae en la ventana operable — attrition 6/9 emisiones |
| STR-003 continuación NY (C03) | DOL no tomado tras London, vela 09:00 monta la sopa previa, cierre 05:00 no en contra (ch07 R12/R19, c-0166–c-0168) | `entryNYContinuation`, emisión en frontera de apertura 09:00 o cierre 13:00 | FIEL. Sólo la emisión de cierre-13:00 sobrevive la ventana (por eso C03 ⊂ fuente maestra) |
| STR-004 reversal NY (C04) | objetivo completado en London, vela 05:00 crea rango opuesto, entrada contraria (ch07 c-0147/R20) | `entryNYReversal`, ventana `[05:00,09:00]` ET | FIEL. 6/6 emisiones fuera de ventana — inoperable en E2T por construcción |
| STR-005 refinado (S12 15m / S13 30m) | procedimiento de refinamiento de TF (tensión fuente 15m vs 5m declarada) | refine compositor sobre maquinaria STR-002 | FIEL con eje de TF declarado; comportamiento propio (horas 13:15–13:45 / 11:30–15:30) |
| STR-006 failure swing (C06/S15/T04) | R3 definición; R11 identificación "reacción + UN motivo → entrada"; R12 order block **opcional** ("si quieres", c-0047); R6 entrada sin activación clásica; R9 el extremo-de-final-de-vela solo NO basta; R1/R2 no predecir | `failureswing.go`: exige **reacción Y order block Y motivo** dentro de la ventana de tolerancia (strict = 1 vela); motivos 1/3 por seam externo (ausentes) ⇒ sólo motivo 2 | **MÁS ESTRICTA QUE LA LECTURA SIMPLE DEL FUENTE** — ambigüedad genuina (la cita de R11/c-0046 incluye el OB en la frase). KRR-003 ⇒ video ch06. No se relaja sin evidencia |
| STR-009 reentrada (C07/S19) | intra-TS: tomar+reacción+cerrar dentro del mismo rango sobre TS hecho (ch01 R19) | módulo rearme con `max_reemissions` | FIEL; el eje quedó inactivo (sin eventos de reentrada calificados en NQU6) |

## 2. Operacionalizaciones declaradas (no enseñadas, honestas)

- `ApproachTicks` (aproximación sin tomar el extremo) — NOT_IN_SOURCE, fail-closed en 0.
- `EndMinutes` (ventana del motivo 2, final de vela) — acotado 1..60, fail-closed.
- `AsiaExpansion` numérico — NOT_IN_SOURCE (documentado).
- Tolerancias strict/wide y key hours — ejes experimentales pre-declarados [OP]/[HIP].

## 3. Condiciones enseñadas no aplicadas / aplicadas de más

- Aplicadas de más (única detectada): el order block como requisito de la conjunción FS (§1 STR-006) — pendiente de adjudicación por video, no corregible sin fuente.
- Enseñadas no aplicadas: ninguna encontrada en la superficie auditada.
- Restricciones posiblemente excesivas además de FS: la **no-adaptación de anclas** (correcta por mandato — toda adaptación exige identidad nueva y autorización Owner), no un defecto.

## 4. Horarios y sesiones: compatibilidad Forex→NQ (mandato FASE 5)

- Regla enseñada: velas del curso 21/17/1/5/9 (rejilla 4h NY del instructor; ch02 R3, ch07 R1).
- Hora de señal implementada: exactamente esas (verificado en 27 streams: emisiones a 01:00/05:00/09:00/13:00/17:00 ET).
- Hora ejecutable E2T: `[09:30, 15:55)` ET lun-vie + corte forzado 15:55.
- Intersección para la familia 4h: **sólo 13:00 ET** (1 de 6 anclas diarias). London (01:00) y reversal (05:00/09:00-cierre) quedan fuera por construcción.
- Adaptaciones expresamente autorizadas en la matriz: S06 (ancla NY-cash 09:30), S07 (CME 17:00 Chicago), T01 (CME×refine) — con identidad propia y sus gates. No se fabricó ninguna adaptación nueva en este shot.

## 5. Fixture verificable por contradicción material

Única contradicción material pendiente = FS (KRR-003). Fixture de verificación propuesto (para el ciclo post-video): repetir G2A de C06/S15/T04 con la conjunción que el Owner adjudique; el funnel actual (ready 12.060/14.037, 0 setups en 69+9 sesiones) queda como baseline de contraste. No se ejecutó en este shot (prohibido relajar el detector sin evidencia fuente).

## 6. Gobernanza de conocimiento

**`STRATEGIES-CATALOG.md` (catálogo canónico) no existe en el vault** en la ruta canónica `knowledge-library/clutifx/strategies/` ni en ninguna otra (`find` vault completo). El master de investigación lo declara re-domiciliado (2026-10-24) y el QA lo verificó "cuando vivía en este directorio". La capa por capítulo (rules/CLAIMS/frames, 12 carpetas) sí está completa y fue la base de esta auditoría. Acción Owner: restaurar el catálogo compilado desde la capa por capítulo o degradar formalmente su estatus de "canónico" en el master.
