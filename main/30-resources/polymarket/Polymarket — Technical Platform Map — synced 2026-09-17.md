# Polymarket — Technical Platform Map — synced 2026-09-17

> **Índice canónico de un único documento, dividido en 11 partes para edición incremental.** Las partes son secciones consecutivas, sin resúmenes ni contenido inventado. La versión completa anterior permanece recuperable en el historial Git.

**Estado contractual:** M0 PARTIAL; RG-01…RG-07 abiertos. No habilita NegRisk Protocol-v2 live conversion.

**Fuente original:** blob Git `0e6f8856d23695fd28493ec5b861828af461dd1b` · 160164 bytes · SHA-256 `02566696b5bc9bd71f07ae73c47b6dbb950b2553cfd9aff5a6247a9663c5b9f5`. Concatenar las partes en orden reproduce exactamente estos bytes.

| Parte | Secciones | Tamaño | SHA-256 |
|---|---|---:|---|
| [part-01-foundations.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-01-foundations.md) | Introducción y §1–§2 | 10254 bytes | `09527ca5740beaab704434121a17e7db1ed0257131fda63bed011e89ddcdeed1` |
| [part-02-rest-catalog.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-02-rest-catalog.md) | §3 | 60238 bytes | `43f201286086bc5ae2e0dfdc934c72d1fabb8b952a1150c5037eb9550a504c8a` |
| [part-03-auth-precision-time.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-03-auth-precision-time.md) | §4–§6 | 10634 bytes | `accdb35a2afa714c5293318394581b68da60037b78e6f6c2e008b28692cdd7c2` |
| [part-04-orders-lifecycle.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-04-orders-lifecycle.md) | §7–§8 | 15867 bytes | `dc673c8d7a9784cc9db7f780ca62f359b4cf3398ca857de69d317d4f13b118b9` |
| [part-05-market-data-positions-contracts.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-05-market-data-positions-contracts.md) | §9–§11 | 18467 bytes | `15a4316f7b1f9c6369de974fa5c9fe384d5bb3004f504371b428ced0b428b210` |
| [part-06-negrisk-combos.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-06-negrisk-combos.md) | §12–§13 | 15120 bytes | `e386cbdb8e404a1a288b60ed74290294bafd291636c892b809611c0da8ba983a` |
| [part-07-economics-resolution-history-limits.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-07-economics-resolution-history-limits.md) | §14–§18 | 19959 bytes | `46151736eb42d594b66d27b2249d6ad0829f0be297458d78ef0ea859c027854c` |
| [part-08-specs-sdks-changelog.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-08-specs-sdks-changelog.md) | §19–§21 | 70505 bytes | `b3f4fa3c490753d6fb5f6395b2d4be7ca032eddc9c1b3932d00c495808fd953d` |
| [part-09-security-workflows.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-09-security-workflows.md) | §22–§23 | 10842 bytes | `45094a5c26f59a0ac7ef4120717ca4d266a626058f3ce04a03e5b04a8a376251` |
| [part-10-gaps-recovery.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-10-gaps-recovery.md) | §24–§25 | 13278 bytes | `64810507d72f0b69903420725751c5c42d900da55c78c343e0ea62f5a37d738e` |
| [part-11-sources.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-11-sources.md) | §26 | 15936 bytes | `ad103b90198cf46c8c8c5fb004d6578e55f3e04d9fec626d39c1c736209ff659` |


**Manifiesto vigente:** verificado 2026-09-17; 11 partes, 261100 bytes; SHA-256 `667f1786da5e4e10bcb2a21a9986a1ff900b848545f646c6eae8de904611189d`. Baseline histórico: `02566696b5bc9bd71f07ae73c47b6dbb950b2553cfd9aff5a6247a9663c5b9f5` (no comparar con digest corregido).
## Integridad y mantenimiento

- Concatenar las partes en orden numérico sin insertar separadores; comprobar SHA-256 contra el hash anterior.
- Editar sólo las partes afectadas y actualizar este manifest ante cambios. Los identificadores `[Sxx]` viven en §26. El estado real M0 se evalúa en §24: este split no cierra ningún Research Gap.
