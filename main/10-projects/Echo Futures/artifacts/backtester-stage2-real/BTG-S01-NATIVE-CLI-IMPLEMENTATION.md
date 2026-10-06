---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-NATIVE-CLI-IMPLEMENTATION

## Propósito

Documentar la integración local del CLI BTG-S01 para preparar, ejecutar y reproducir datasets NT nativos OHLC de un minuto, junto con sus límites de evidencia.

## Contenido

El source freeze es `198f29f44bc6e58dd445c9a9b5ee1adfdade2ae9` en `codex/btg-s01-native-cli`, basado en C `e2e15a3559034a3ed08c04f247baf4919e20b2ff`. El CLI incorpora descriptor NT estricto, `prepare-functional-nt`, routing exclusivo del descriptor según el modo de mercado y la misma ruta de run, sellado, verificación e integridad que usa la reproducción. El recorder conserva el pliegue legacy en `Next`; para NT el driver añade `InputSequence` al cierre de fuente. El cambio F08 de identidad inicial de account-day se integró byte a byte desde `171fc712e56d731493befeef5c54a2620f25d31a`.

El manifiesto preparado declara `OHLC_1M_MODEL_V1` como fidelidad/modelo, y Scope explica NO_ADDS, la ausencia de equivalencia con BBO observado/operación LIVE y el límite `From=AvailableAt`: warmup queda a cargo del llamador; si comienza en el primer `AvailableAt`, el intervalo anterior no entra. No se infiere ni ajusta el warmup. Los fixtures de este trabajo son sintéticos; no certifican autenticidad ni resultados históricos. No se adquirieron originales NT ni se realizó publicación, trading o acción de infraestructura. El cambio queda como candidato a revisión TOP independiente; no implica aceptación del owner.

Las pruebas offline dirigidas cubrieron routing/identidad, preparación, integridad, reproducción en procesos frescos, fallo sellado y compatibilidad legacy. El mapa con denominadores, perfil bruto, rutas modificadas, exclusiones visibles y SHA-256 de los seis archivos F08 está fuera del vault en `/home/kor/aranea/work/btg-s01-20261006/reports/native-cli/coverage-map.md`; el resumen ejecutable está en `specs/btg-s01-nt-cli/VERIFICATION.md` del source branch.

## Fuentes

- [[Echo Futures — BT-S01 Backtester V1 Design]]
- Source freeze: `198f29f44bc6e58dd445c9a9b5ee1adfdade2ae9`; documentación de verificación: `6ef303f57739f0b2a44288f387b377d145eeceac`.
- F08 source y regression: `171fc712e56d731493befeef5c54a2620f25d31a`; hashes de bytes en el informe de cobertura enlazado arriba.
