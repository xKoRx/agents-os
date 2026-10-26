# CLF-Q04 — SUPERSEDED (PARCIAL) BY E05

Fecha: 2026-10-26. Los archivos sellados de este directorio NO se modifican (write-once). Dos correcciones de reporting del ciclo CLF-E05 afectan cifras publicadas aquí:

1. **Contabilidad S13**: los CSV derivados de Q04 contaban 2 operaciones `MM_NO_ACTION` sin órdenes como trades (`S13: 3 trades`). Lo correcto, demostrado desde fills y reconciliado con `q03r1/CLF-Q03R1-G4-QUALIFICATION.csv`: `S13: 1 trade completo, 0W/1L`; totales NQU6 = 54 round-trips = 32W/22L. Ver `e05/CLF-E05-Q04-ACCOUNTING-REPAIR.md` y los CSV corregidos en `e05/`.
2. **Control R03 (§9 del ROOT-CAUSE)**: "24 configuraciones con pases dentro de NQU6" queda corregida a **13** con timestamps reales por pase; el soporte citado (2026-09-28/2026-10-02) es posterior a la ventana. Ver `e05/CLF-E05-R03-TEMPORAL-CONTROL.md`.

Todo lo demás de este directorio permanece vigente (totales de compras/caja, timelines, funnel de emisiones, causa primaria 19/19 `MATHEMATICALLY_UNREACHABLE_WITH_OBSERVED_TRADES` — que se robustece con la corrección).
