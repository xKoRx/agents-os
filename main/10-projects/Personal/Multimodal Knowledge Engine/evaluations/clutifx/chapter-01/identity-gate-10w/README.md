# Identity Gate 10W — Clutifx chapter-01

Gate live acotado de la identity remediation MKE V2: micro-remediación F-ADV-01 + primeras 10 ventanas canónicas consecutivas de Clutifx ep01 con provider live (`openrouter` / `stealth/space-bunny-alpha`). Producto `ef53530` (F-ADV-01 cerrado sobre la remediation `71b5a21`). 2026-10-01.

**Veredicto:** `CLUTIFX_10W_LIVE_GATE = PASS_WITH_FINDINGS` — el run atravesó las 10 ventanas sin defecto de identidad y la atomicidad whole-window se verificó físicamente; findings: equivalence review sin ejercicio live (0 colisiones), L2 no alcanzado (composition unavailable por transporte), 20% de ventanas perdidas por output inválido del modelo.

## Contenido

| Archivo | Qué es |
|---|---|
| `METRICS.json` | métricas requeridas del gate (con nulls donde la métrica no existe) |
| `claims.jsonl` / `skos.jsonl` / `documentation.md` | artifacts canónicos del run live (copias byte-exactas) |
| `WINDOWS.md` | una fila por ventana: interval, status, propuestas, contribución canónica |
| `EQUIVALENCE-DECISIONS.md` | tabla vacía por ausencia de eventos (0 adjudicaciones) + contexto |
| `PROVENANCE.md` | cadena de custodia: SHAs, fingerprints, provider, credencial, runtime |
| `RUN.md` | procedimiento exacto, resume check y replay recorded con comparación física |
| `REQUEST-AUDIT.md` | auditoría de requests reales por clase de task |
| `MANAGER-REVIEW.md` | facts organizados para la adjudicación del Primary Manager |
| `SOURCE.md` | binding del source: rehash SHA exacto + evidencia de L0 reuse |

## Resumen de una línea

64 claims + 11 relations canónicas (100% en español), 66/75 supported, 0 colisiones de identidad, 583,313 tokens, L2 no alcanzado, replay recorded con contenido idéntico.

Runtime local completo: `~/mke/clutifx-ch01-10w-gate-20261001/` (no se sube: ni media pesado ni secretos).
