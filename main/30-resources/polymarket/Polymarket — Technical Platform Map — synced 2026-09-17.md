# Polymarket — Technical Platform Map — synced 2026-09-17

> **Índice canónico de un único documento, dividido en 11 partes para edición incremental.** Las partes son secciones consecutivas, sin resúmenes ni contenido inventado. La versión completa anterior permanece recuperable en el historial Git.

**Estado contractual:** M0 DESIGN_READY (documental); RG-01…RG-07 cerrados para diseño con exclusiones explícitas. NO certifica trading live, backfill L2 ni conversión NegRisk live. Ver §24 en part-10.

**Baseline histórico, NO hash del contenido actual:** blob Git `0e6f8856d23695fd28493ec5b861828af461dd1b` · 160164 bytes · SHA-256 `02566696b5bc9bd71f07ae73c47b6dbb950b2553cfd9aff5a6247a9663c5b9f5`. Las 11 partes reproducían exactamente ese original al dividirse; después de las correcciones contractuales y del cierre M0 cambiaron legítimamente. Para verificar la versión actual, concatenar las partes en orden y comparar con el **Manifiesto vigente** inferior.

| Parte | Secciones | Tamaño | SHA-256 |
|---|---|---:|---|
| [part-01-foundations.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-01-foundations.md) | Introducción y §1–§2 | 10254 bytes | `09527ca5740beaab704434121a17e7db1ed0257131fda63bed011e89ddcdeed1` |
| [part-02-rest-catalog.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-02-rest-catalog.md) | §3 | 61012 bytes | `bac281fdecc3bd7c4dea30fcd60c686ce7117096d0e7690e0092e734f0fe6ab8` |
| [part-03-auth-precision-time.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-03-auth-precision-time.md) | §4–§6 | 10634 bytes | `accdb35a2afa714c5293318394581b68da60037b78e6f6c2e008b28692cdd7c2` |
| [part-04-orders-lifecycle.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-04-orders-lifecycle.md) | §7–§8 | 15877 bytes | `dd5d85314941a387270a6e3d54f074c721eb9a8ca34dca948988abeaf2a0c28b` |
| [part-05-market-data-positions-contracts.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-05-market-data-positions-contracts.md) | §9–§11 | 18467 bytes | `15a4316f7b1f9c6369de974fa5c9fe384d5bb3004f504371b428ced0b428b210` |
| [part-06-negrisk-combos.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-06-negrisk-combos.md) | §12–§13 | 15120 bytes | `e386cbdb8e404a1a288b60ed74290294bafd291636c892b809611c0da8ba983a` |
| [part-07-economics-resolution-history-limits.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-07-economics-resolution-history-limits.md) | §14–§18 | 19959 bytes | `46151736eb42d594b66d27b2249d6ad0829f0be297458d78ef0ea859c027854c` |
| [part-08-specs-sdks-changelog.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-08-specs-sdks-changelog.md) | §19–§21 | 81418 bytes | `8c1fd83fb568ca8c249adb4cff05bf6346419d4ade3af57d78f575061ebcb7a7` |
| [part-09-security-workflows.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-09-security-workflows.md) | §22–§23 | 10842 bytes | `45094a5c26f59a0ac7ef4120717ca4d266a626058f3ce04a03e5b04a8a376251` |
| [part-10-gaps-recovery.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-10-gaps-recovery.md) | §24–§25 | 16995 bytes | `d465778bafb405f3e9d70de264a934930a6266c2db1261db3e7e10261b50a637` |
| [part-11-sources.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-11-sources.md) | §26 | 27352 bytes | `2af1a29f4d6be2779d550fd26ad50f3967d319e442d466498ad16df6c58d53de` |


**Manifiesto vigente:** 2026-09-17 15:35 UTC; 287930 bytes; SHA-256 `ca7e3329b39f666fa0d383ffae194e6aa09f2e741b31cea61a4dc72136be8938`; historical baseline SHA-256 `02566696b5bc9bd71f07ae73c47b6dbb950b2553cfd9aff5a6247a9663c5b9f5`.
## Integridad y mantenimiento

- Concatenar las partes en orden numérico sin separadores y comparar con **Manifiesto vigente**; el SHA original de 160164 bytes es únicamente baseline histórico, no hash esperado después de correcciones.
- Editar sólo las partes afectadas y actualizar este manifest ante cambios. Los identificadores `[Sxx]` viven en §26. El estado real de M0 y las capacidades live bloqueadas se evalúan en §24 de part-10; el split por sí solo no cerró Research Gaps.
