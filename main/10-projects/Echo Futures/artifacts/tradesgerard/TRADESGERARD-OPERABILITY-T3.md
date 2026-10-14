---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[TRADESGERARD-CONTROL]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-OPERABILITY-T3

## Propósito

Ejecutar F2-SR × K01–K05 × retiro bruto2300/3000: diez campañas de la misma ventana C4, con política económica común corregida O10. Estado **INDEPENDENT_PASS_OFFLINE / AWAITING_RESOURCE_ADMISSION**, ninguna campaña T3 lanzada al emitir el gate. No hay resultados económicos finales todavía; el smoke sin actividad no es candidata ni fila del ranking.

## Contenido

### Gate independiente

`verifier/independent-f2-gate.json` SHA256 físico `8350ac5f9095de2b22d37bad996cb8c8d61ef837ae0a88a4bcd00d35a7fa7a59`, INDEPENDENT_PASS OFFLINE_OHLC_F2. Source/binario/10inputs íntegros, paridad normativa respecto O10/F0 con delta sólo filtro/identidades/build; dinero común comprobado por blobs conserva gate O10. Coverage104/104 recalculada, oráculo136fronteras variables/exclusión propia y futura PASS0,422s; calendario/DST/gaps/contrato/epoch/readiness PASS0,053s. Smoke23base coincide con oráculo K/ATR/SR60previas,23rechazos de zona/0operaciones/caja5000; receipt sealed COMPLETE e identidad/digests verificados. Manager comprobó hash del gate y sus identidades. Permite iniciar sólo con admisión de recursos global; no certifica runtime ni rentabilidad.

### Freeze y semántica

Source `a9c4505914e897bd3587e3158a3ff9f205dd4948`, árbol `ab0da96849a55c7a15eadc20c8c5a4f712215c97`, checkout `implementer/echo` limpio comprobado por manager. Binario `implementer/bin/echo-backtest-f2` SHA256 físico `4fe35ce7d3e868c34cd48fa808bf7a007fee412bf1bec288350a83d96d71c785`. Manifiesto `implementer/evidence/f2-freeze-manifest.json` SHA256 físico `73ae942c80202a53023cd7df5030cf23ac1dac612c3946a07590004db9aadafa`, diez inputs. Paths de evidencia relativos a `ARANEA_ROOT/work/tradesgerard-operability-20261013`.

SIG-B se conserva. En señal t, S=min(low t−60…t−1), U=max(high t−60…t−1), ancho=ATR20 conocido en t; LONG S≤close≤S+ancho, SHORT U−ancho≤close≤U. La barra propia queda excluida. Epoch/contrato/huecos no explicados reinician disponibilidad; sólo el calendario SDK puede explicar cierre diario, fin de semana o DST. ATR no válido produce causa explícita. No convierte niveles SR en stops ni cambia los SL/TP económicos. F0 no depende de readiness SR.

Integrador reportó blobs monetarios idénticos a O10, suite TG PASS0,158s, delta104/104 y regresión CLI/prefijo3,226s; el gate independiente posterior se registra arriba, separado del gate monetario O10.

### Smoke del productor

Recibo `implementer/evidence/f2-frozen-smoke-receipt.json`: primera sesión,23 cruces base,0 aprobados,23 rechazados por zona con filtro disponible,0 cuentas/operaciones, caja5000. Resultado COMPLETE de diagnóstico, no ranking ni prueba de ausencia de oportunidades en las31 sesiones. No se selecciona una configuración sin actividad por conservar caja.

### Recursos y continuación

Medición del integrador:958.281.533B de evidencia nueva total incluyendo cortes afectados,9.736.310.784B libres, forecast1.193.162.557B≤1,5GiB. Conserva reserva≥8GiB, traza/log≤16MiB, lote≤256MiB y presupuesto agregado sin reinicio por carpeta. Revalidar antes de ejecutar. F0/F1 deben pasar gate común y empezar antes; T3 usa capacidad global≤4 sólo después de su verificación exacta. F3 será la conjunción y no añade parámetros.

## Fuentes

- Mandato GOD LOCAL del Owner, PROMPT_VERSION1,2026-10-13.
- [[TRADESGERARD-OPERABILITY-T0]]: política económica y hallazgos técnicos; O10 pendiente de gate al redactar este freeze.
- [[TRADESGERARD-OPERABILITY-T1]] y [[TRADESGERARD-OPERABILITY-T2]]: campañas anteriores preservadas AFFECTED; sus resultados no se reutilizan para representar T3.
