# CLF-E05R1 — MATERIAL AXIS REGRESSIONS

Commit base `e8c2e47e` → commit corregido `3c0c683c` (rama `experiment/clutifx-s01`, sin merge, sin LIVE) · `OWNER_ACCEPTANCE: REVIEW`

## Identidades semánticamente modificadas

| Grupo | Identidades | Naturaleza del cambio | Recibos previos |
|---|---|---|---|
| Bias (H1) | S03, S04, S05A, S05B | El gate ahora consulta el motor configurado: las 4 configs dejan de ser réplicas estructurales de C02 (E05-01/MISWIRED_CONFIG corregido). Nueva identidad de comportamiento por config. | Los recibos Q03R1/E05 de S03/S04/S05A/B quedan como evidencia del código defectuoso (medición del camino económico, no del eje); preservados, NO reutilizados. |
| Failure Swing (H2-H5) | C06, S14, S15, T04 | OB opcional + predicado de reacción + ventana + adversos: la semántica del spec `CLF_FAILURE_SWING_V1` cambia (default `until_invalidation` + `optional` = nueva identidad de config; `fs_order_block_mode` hace explícito el eje). | Las campañas previas de C06/S15/T04 se preservan como baseline de contraste (Q04 §5). S14 se re-materializa como `strict`+`required` explícito (reproducción de la identidad histórica). |

## Identidades NO modificadas (regresión verde)

C01, C02, C03, C04, C05, S01, S02, S06-S13, S16-S21, T01, T02, T03, T05, C07, C08: la suite completa del paquete (STR-002 maquinaria, TS 4 modos, DOL taken/recompute/borrado, sesiones London/NY, red flags, reentradas, refinados, anclas, exits, determinismo/anti-lookahead/state round-trip) corre VERDE sobre `3c0c683c` sin cambio de comportamiento — los payloads de motor nativo conservan bytes planos idénticos (FX-08a). Provider/MM/contratos de cuenta: cero cambios.

## Errores fuente/código que permanecen (declarados, no maquillados)

- F-K05-06/07 (refinado en sesión; FS-activación de rangos) y F-K05-18/19 (entrada OB; PDM): NO implementados — requieren autorización Owner de eje (matriz congelada).
- F-K05-12 (base de salida C03/S08): sigue pendiente decisión Owner.
- KRR-001/002/004 (anclas), KRR-005 (stop extra), KRR-006 (datasets SMT/noticias): sin cambios.
- V-01/V-02: dudas residuales de vídeo, NO presentadas como resueltas (H2 implementa la lectura dominante y `required` preserva la alternativa).

## Campañas bit-idénticas: no re-ejecutadas

Las campañas Q03R1/E05 de las identidades no modificadas siguen siendo la evidencia vigente (su build `e8c2e47e`-lineage y sus resultados no cambian). Las 8 identidades corregidas se re-gatearon COMPLETO en este ciclo (G0→G2 propios, contrato NQZ6) — ninguna heredó el PASS de otra versión.
