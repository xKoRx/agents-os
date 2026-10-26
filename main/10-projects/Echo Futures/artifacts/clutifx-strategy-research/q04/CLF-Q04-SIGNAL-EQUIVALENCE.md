# CLF-Q04 — SIGNAL EQUIVALENCE (FASE 4)

Método: fingerprints de comportamiento independientes de identificadores de job y de hashes de señal (el `signal_id` incluye las citas de cada variante, por lo que difiere incluso con emisión idéntica). Dos niveles: **emisión** `(ts UTC, dirección, stop)` de señales OPEN y **ejecución** `(fecha ET, hora ET, dirección, precio entrada, qty, distancia stop)` de round-trips reconstruidos desde fills.

## Clases de emisión (OPEN signals, NQU6)

- `EMIT-MASTER` (idénticas 9 señales): **C02, C07, S03, S04, S05A, S05B, S09, S19, S21** → `SIGNAL_EQUIVALENT`.
- `EMIT-S20`: superconjunto de EMIT-MASTER (16 señales; 13 extra fuera de ventana por red-flags off); ejecución idéntica a la maestra → `SIGNAL_EQUIVALENT_AT_EXECUTION` (eje red-flags sin efecto en lo ejecutado).
- Individuales: C01 (1), C03 (3), C04 (6), S01 (4), S02 (4), S06 (12), S07 (10), S10 (17), S11 (8), S12 (9), S13 (9), S16 (5), S17 (4), T01 (10).
- Vacías: C06, S15, T04 (0 emisiones — Failure Swing).

## Clases de ejecución (round-trips, NQU6)

| Clase | IDs | Trades |
|---|---|---|
| EXEC-MASTER | **C02, C07, S03, S04, S05A, S05B, S09, S19, S20, S21** (10) | 06-23 13:00 SHORT@29863,25 (1; stop 21,50) · 08-06 13:00 SHORT@29556,50 (1; 19,25) · 08-26 13:00 SHORT@29215,25 (2; 11,00) → idénticos al céntimo (+335,08) |
| EXEC-C03 | C03 | subconjunto propio: 06-23 + 08-06 (sin 08-26) |
| EXEC-S16 | S16 | subconjunto: 06-23 + 08-26 |
| EXEC-S11 | S11 | subconjunto: 08-06 + 08-26 |
| EXEC-S06 | S06 | propio: 13:30/09:30 anclas, 6 rt |
| EXEC-S07 | S07 | propio: 10:00/14:00, 3 rt |
| EXEC-S10 | S10 | propio: 12:00/13:00/15:00, 3 rt (setup 1h) |
| EXEC-S12 | S12 | propio: 13:15/13:30, 2 rt |
| EXEC-S13 | S13 | propio: 1 rt (11:30) + 2 `SIZE_BELOW_MIN_CONTRACT` |
| EXEC-T01 | T01 | propio: 10:30/11:15/14:15, 3 rt perdedoras |

## Clasificación por variante

- `SIGNAL_EQUIVALENT`: C02, C07, S03, S04, S05A, S05B, S09, S19, S21 (emisión+ejecución demostradas idénticas).
- `SIGNAL_EQUIVALENT_AT_EXECUTION` (superconjunto de emisión fuera de ventana): S20.
- `VALID_VARIANT_SAME_SOURCE_PARTIAL` (subconjuntos de la fuente maestra): C03, S11, S16.
- `MATERIAL_AXIS_INACTIVE` (el eje de la variante no llegó a influir en ninguna decisión en NQU6): sesgo EMA (S03), estructura (S04), DMI/ADX (S05A/B), rearme STR-009 (C07, S19), red-flags off/hard (S20, S21) — todos colapsan a la fuente maestra en la práctica.
- `INSUFFICIENT_EVENTS_TO_DIFFERENTIATE`: cualquier eje cuyo efecto requeriría más de 9 emisiones/trimestre (no observable a esta densidad).
- `IMPLEMENTATION_DEFECT`: **ninguno detectado** (las equivalencias son consecuencia declarada de defaults compartidos del módulo, p. ej. `max_reemissions=0` S18≡C02 ya verificado en Q03).

## Consecuencia económica

19 campañas pagadas → **10 fuentes de señal realmente distintas** (EXEC-MASTER + C03, S06, S07, S10, S11, S12, S13, S16, T01). La deduplicación por ejecución reduce 19 evidencias económicas a 10; contando familias de señal (no MM), la familia maestra pesa como UNA. El costo de duplicación (10 compras + renovaciones de la fuente maestra) fue ~$3.480 de los $6.480 totales.
