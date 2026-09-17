# Polymarket — Technical Platform Map — synced 2026-09-17

> **Índice canónico de un único documento, dividido en 11 partes para edición incremental.** Las partes son secciones consecutivas, sin resúmenes ni contenido inventado. La versión completa anterior permanece recuperable en el historial Git.

**Estado contractual:** M0 PARTIAL; RG-01…RG-07 abiertos. No habilita NegRisk Protocol-v2 live conversion.

**Fuente original:** blob Git `0e6f8856d23695fd28493ec5b861828af461dd1b` · 160164 bytes · SHA-256 `02566696b5bc9bd71f07ae73c47b6dbb950b2553cfd9aff5a6247a9663c5b9f5`. Concatenar las partes en orden reproduce exactamente estos bytes.

| Parte | Secciones | Tamaño | SHA-256 |
|---|---|---:|---|
| [part-01-foundations.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-01-foundations.md) | Introducción y §1–§2 | 10254 bytes | `09527ca5740beaab704434121a17e7db1ed0257131fda63bed011e89ddcdeed1` |
| [part-02-rest-catalog.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-02-rest-catalog.md) | §3 | 24785 bytes | `3f12606ea4e7b16e113e6106e203620aba0e454a27ae45db5cdb86cc33ec41b2` |
| [part-03-auth-precision-time.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-03-auth-precision-time.md) | §4–§6 | 10634 bytes | `accdb35a2afa714c5293318394581b68da60037b78e6f6c2e008b28692cdd7c2` |
| [part-04-orders-lifecycle.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-04-orders-lifecycle.md) | §7–§8 | 15867 bytes | `dc673c8d7a9784cc9db7f780ca62f359b4cf3398ca857de69d317d4f13b118b9` |
| [part-05-market-data-positions-contracts.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-05-market-data-positions-contracts.md) | §9–§11 | 18467 bytes | `15a4316f7b1f9c6369de974fa5c9fe384d5bb3004f504371b428ced0b428b210` |
| [part-06-negrisk-combos.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-06-negrisk-combos.md) | §12–§13 | 11465 bytes | `294c6467df9378073fd1966cd047b97777e6f6e16f37e0293b7c017bb46c9f99` |
| [part-07-economics-resolution-history-limits.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-07-economics-resolution-history-limits.md) | §14–§18 | 18390 bytes | `b2fdb4e51f3474f98e175016e6e3fe6a8ea44d372dfe604bd094cc864fb66b9e` |
| [part-08-specs-sdks-changelog.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-08-specs-sdks-changelog.md) | §19–§21 | 56619 bytes | `5a37b730c8607169e4a1f8a7e02023ee4bddbbcdcab38044bd828f88438800bc` |
| [part-09-security-workflows.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-09-security-workflows.md) | §22–§23 | 10842 bytes | `45094a5c26f59a0ac7ef4120717ca4d266a626058f3ce04a03e5b04a8a376251` |
| [part-10-gaps-recovery.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-10-gaps-recovery.md) | §24–§25 | 12711 bytes | `4b9f9bd6bfffaa1feb3472a35c69910c320418894a6e8d038861ba838f479fa1` |
| [part-11-sources.md](./Polymarket%20%E2%80%94%20Technical%20Platform%20Map%20%E2%80%94%20part-11-sources.md) | §26 | 14029 bytes | `94bde00ca50551c2bd835536f418a12e91bf0d146ea6beee2eb7d77c42cd832a` |

**Manifiesto vigente:** verificado 2026-09-17 14:39 UTC; concatenación actual de las 11 partes en orden: 204063 bytes; SHA-256 `243378201decd87c5b853437e07925d47f3573db8e2c9affc3f632ccce1314be`. Baseline original histórico inmutable: `02566696b5bc9bd71f07ae73c47b6dbb950b2553cfd9aff5a6247a9663c5b9f5`.

## Integridad y mantenimiento

- Concatenar las partes en orden numérico sin insertar separadores; comprobar SHA-256 contra el hash anterior.
- Editar sólo las partes afectadas y actualizar este manifest ante cambios. Los identificadores `[Sxx]` viven en §26. El estado real M0 se evalúa en §24: este split no cierra ningún Research Gap.
