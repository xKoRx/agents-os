# P8 — OLD→NEW DELTA REPORT

Baseline `ef53530756a27009517030a1bd29f0472bb3ad48` (full-live-v2, INCOMPLETE ordenado, bundle `../full-live-v2/`) vs
Candidato `19b44c193e6ac5b9cd3be26c03792e43113fbe08` (P7 rerun `~/mke/clutifx-ch01-rerun-20261003/run-rerun/`, INCOMPLETE ordenado exit 4).
Fuentes: P1 audit (`../p1-audit/`), análisis canónico (`~/mke/clutifx-ch01-full-live-20261001/analysis-rerun/`), workers P8 (`results/`), journals durable de ambos runs.

| Métrica | Baseline ef53530 | Candidato 19b44c1 | Delta | Veredicto |
|---|---:|---:|---:|---|
| ventanas intentadas | 130 | 130 | = | — |
| ventanas aceptadas | 104 | 111 | +7 | mejora |
| ventanas rechazadas | 26 | 19 | −7 | mejora |
| — rechazo identidad determinista (kind/epistemic/estructural) | 16 (11 kind+2 epi+2 estr+1 otro) | 6 (2 kind + 4 epi + 0 estr) | −10 | mejora |
| — rechazo identidad semántica (DIVERGENT) | ~6 | 11 (10 review + 1 caché) | +5 | empeora (6 FALSE_DIVERGENT + 1 AMBIGUOUS + 4 TRUE) |
| — rechazo formato (bad-ref / id) | 4 bad-ref | 1 bad-ref + 1 relation-id | −2 | mejora; ventanas distintas = transientes |
| bad-evidence-ref windows | 4 | 1 | −3 | mejora |
| canonical claims | 803 | 1043 | +240 | más cobertura |
| canonical relations | 130 | 146 | +16 | más cobertura |
| records totales | 933 | 1189 | +256 | — |
| supported | 853 (91.4%) | 1125 (94.6%) | +272 | mejora |
| non-supported | 80 (8.6%) | 64 (5.4%) | −16 | mejora (<80 ✓) |
| material precision (audit fuente) | 98.0% | 98.2% (588/599) | +0.2pp | ≥97% ✓ |
| wrong claims MATERIALES publicados | 4 (0.50% del total) | 3 (0.27% total / ~0.5% material) | −1 | ≤0.5% ✓ / ≤1% material ✓ |
| MISSING_MATERIAL en aceptadas | 0 | **4** (2 ausencias reales + 1 recuperable por formato + 1 cubierto-luego) | +4 | **FALLA =0** |
| residuo material de rechazadas | 19 proposiciones / 10 ventanas | 10 proposiciones / 8 ventanas | −9 | <19 ✓ |
| grounding FN rate (semántico, fórmula P1) | 17.5% (14/80) | **25% (16/64)**; con causa-provider: 46.9% (30/64) | peor | **FALLA ≤10%** |
| — FN causa formato/provider (malformed 9 + parse-fatal 5) | (mezclado en otras clases) | 14 (recuperables: 9 con veredicto SUPPORTED EN el journal) | clase nueva | remediable |
| non-supported FALSE-POSITIVE check | 1/30 muestra + 1/112 relations | **0/61 muestra + 0/128 relations publicadas** | mejora | safety ✓ |
| identity false merges | 0 | **0** (61/61 EQUIVALENT humanos correctos) | = | invariante ✓ |
| identity false splits | 2 confirmados (w0028, w0078) | 0 confirmados (análogo w0078 mergea; inconsistencia modalidad queda) | mejora | ✓ |
| classification-instability divergences | 15/16 deterministas | 6/6 deterministas (todas inestabilidad; 0 estructurales) | −9 | mejora, no eliminada |
| acumulaciones aplicadas | 12 (sobre 7 records; E-02) | 38 (153 merges físicos: 59 live + 58 caché + 36 idénticos) | +26 | auditadas 38/38 PASS |
| fragmentación (pares statement idéntico entre ids) | 13 | **77 (29 grupos)** | +64 | **empeora** (MI-03, deuda) |
| correlación idioma | 803/803 es | 1043/1043 es | = | ✓ |
| manual resumes | 2 | **0** (14h48m unattended, verificado ×6) | −2 | gate escala ✓ |
| run fatals (run-killing) | 2 (empty-content) + 1 transport | **0** | −3 | ✓ |
| provider fatals per-record | (mezclados) | 5 parse-fatal fail-closed (0.42%) | clase nueva | fail-closed, sin matar run |
| L2 reached | NO (timeout transporte 3×120s) | **NO (propuesta composition REJECTED: 7 refs inválidas / 4 objetos de 23; 231.5s = 39% del timeout 600s)** | causa distinta | **FALLA SKOS>0** |
| SKOs | 0 | 0 | = | — |
| atomicity whole-window | PASS | PASS | = | ✓ |
| replay | PASS | **PASS** (1180/1190 idénticos; 10 razones con re-wrap) | = | ✓ |
| provider calls | 1194 | 1618 | +424 | más records |
| tokens | 8,600,403 | 12,045,055 | +40% | proporcional a +27% records |
| wall time | 9h27m | 14h48m | +5h21m | reconstruction secuencial más lento |

## Lectura del manager

El candidato es estrictamente superior al baseline en las dimensiones de corrección y operación (más conocimiento con igual o mejor precisión, 0 babysitting, 0 run-kills, ladder más sano en merges/deterministas), y **falla 3 sub-criterios congelados**: L2=0 SKOs (causa nueva: fail-closed por-proposición ante 7 refs malas de 164), MISSING_MATERIAL=4 (umbral 0), grounding FN rate (16 semánticos/64 = 25%; 14 adicionales de causa formato con veredicto SUPPORTED ya en journal).
