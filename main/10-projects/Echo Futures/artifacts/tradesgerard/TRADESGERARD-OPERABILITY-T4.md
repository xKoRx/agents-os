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

# TRADESGERARD-OPERABILITY-T4

## Propósito

Ejecutar F3-TREND-SR × K01–K05 × retiro bruto2300/3000: diez campañas que completan la matriz cerrada de cuarenta. Estado **INDEPENDENT_PASS_OFFLINE / QUEUED_FOR_CAPACITY**, ninguna campaña T4 lanzada al emitir el gate. No existe todavía ranking final válido. Comparte la política económica O10 y la ventana/perfil C4.

## Contenido

### Gate independiente y cola

`verifier/independent-f3-gate.json` SHA256 físico `1922ab03e9ac2513ce345229cba7735292efe809a61b92fe1cd2c3f67e4008e3`, INDEPENDENT_PASS OFFLINE. Fuente limpia, binario/10inputs verificados, prefijo de los diez inputs idéntico F1/O10 y blobs monetarios comunes. Tabla de verdad independiente144casos pendiente+/−/igual, zonas LONG/SHORT, ausencia H1/ATR PASS0,323s; cobertura delta23/23. Smoke23base/0aprobados coincide con oráculo SMA∧SR, mismas K/ATR/extremos/SMA, caja5000sinactividad y receipt sealed íntegro. Manager comprobó hash del gate; no es validación económica ni runtime.

Manager habilita la cola F3×10 sin nueva aprobación del Owner. Límite global vigente6 después de medición de recursos, F0/F1 conservan CPU0–5 y F2 usa CPU6–8; F3 espera plazas reales sin interrumpir campañas saludables. La admisión original4 y la expansión medida se mantienen en recibos separados; no se afirma velocidad bajo contención.

### Freeze

Source `466e4f17b5b311adc74302417307452bc462d54a`, árbol `34607beaf86f5b59f74dfa6ad02abcbc7d7c7bf9`. Binario `implementer/bin/echo-backtest-f3` SHA256 físico `281a76e9ab84111749fd248b8eb10f435ef90990e0e83ce0286f51499ac4ac60`. Manifiesto `implementer/evidence/f3-freeze-manifest.json` SHA256 físico `4fc4d7dff30f0f8e5c587582a9a7d47cd4ae9126cd14297fd851257584512368`, diez inputs. Manager comprobó hashes y conteo. Evidencia relativa a `ARANEA_ROOT/work/tradesgerard-operability-20261013`.

F3 llama la conjunción exacta de F1 y F2 existentes: dirección de SMA24 sobre H1 totalmente cerradas y zona de extremos de60velas1m previas con ancho ATR20. Conserva ambos testigos de aceptación/rechazo. No añade condición de precio frente a la media, umbral de pendiente ni otro indicador. Prefijo H1 idéntico a F1; blobs monetarios idénticos a O10 según recibo del integrador. Debe verificarse independientemente la igualdad de identidades base y que sus aprobaciones sean subconjunto de F1 y F2.

Integrador reporta suite TG PASS0,177s y cobertura delta23/23. Smoke físico posterior COMPLETE:23cruces base/0aprobados/0operaciones/caja5000, con ambos motivos de filtro por cruce; recibo `implementer/evidence/f3-frozen-smoke-receipt.json`. Diagnóstico de primera sesión sin actividad, no candidata ni fila de ranking. Gate independiente exacto pendiente y lanzamiento sujeto a capacidad global≤4, reserva≥8GiB y presupuesto nuevo agregado1,5GiB incluyendo cortes anteriores.

### Persistencia y límites

Integrador preservó `source-o10-f2-f3.bundle` con tres refs y prerrequisito C4 exacto, comprobado por su recibo. Es persistencia Git local; origin de su checkout es otro checkout local, no se afirma push a GitHub de producto ni merge. Fuentes de los tres cortes quietas para verificación y ejecuciones.

Los resultados finales deben incluir las diez configuraciones, aunque ninguna cobre. Cobro acreditado y caja neta positiva se clasifican por separado. Sólo después del ranking de cuarenta se seleccionarán dos pares activos (filtro,perfil) conservando ambos retiros, con desempates prospectivos y el intervalo adicional ya reservado. No se promoverá un caso sin operaciones por un empate de caja intacta.

## Fuentes

- Mandato GOD LOCAL del Owner, PROMPT_VERSION1,2026-10-13.
- [[TRADESGERARD-OPERABILITY-T0]]: política económica común y gate pendiente.
- [[TRADESGERARD-OPERABILITY-T2]] y [[TRADESGERARD-OPERABILITY-T3]]: definiciones F1/F2 y evidencias; resultados históricos afectados no son filas de T4.
