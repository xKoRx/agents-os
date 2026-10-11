# BACKTEST-DOC-USABILITY-REPORT.md

**Prueba de uso del manual del backtester por agente nuevo, ONE-SHOT.**
Fecha: 2026-10-11 · Evaluador: agente LOCAL TOP Owner (GLM-5.3-Flash), fresh-context, sin subdelegación. El objeto evaluado es la documentación, no la rentabilidad.

## Resultado

**`EJECUTABLE_SOLO_CON_DOC`** — un agente nuevo sin conocimiento previo del proyecto ejecutó la instalación completa, un BASIC NQZ5, un CAMPAIGN NQZ5 y los dos replays oficiales usando exclusivamente las recetas del manual. Ambos replays: `IDENTICAL`. Todos los estados, archivos y cifras esperados según el manual se cumplieron. No hubo ningún bloqueo documental ni de entorno. Nota: **9/10**.

## Identidad de lo evaluado y probado

- **Manual evaluado:** `v3/backtester/README.md` @ commit `c75023c82dfc6609312f0f24dec731a9d9e6ee54` (2026-10-11T05:19:50Z, "docs(agents): route backtest operators directly to the verified package recipe"). Copia local de la lectura: `~/aranea/work/bt-doc-usability-20261011/README-manual-under-test.md` (SHA256 `0ae8eedd7d5e4540fb497bd10a46c1d09ffea9d9bf9e1cf6783b41e7d96e3cc1`). Nota de acceso: la URL `blob`/`raw` anónima devuelve 404 (repo privado); la descarga requirió `gh` autenticado, caso cubierto por la fila de diagnóstico §8 "GitHub404/permiso al descargar".
- **Paquete/binario:** release `btx-perf-last-20261010` de `xKoRx/echo`; source `873f5f1c7df25086271af1de1896095f1cade2a9`; binario `bin/echo-backtest` SHA256 `0320b80e78fbf12821eda4004c68c96175f770dedaac747dc306604e9280d83b` (verificado contra `PACKAGE-IDENTITY.json` y el valor declarado en §1 del manual). Instalación en `~/echo-backtest-873/package`.
- **Instalación nueva: SÍ fue probada de punta a punta** (no se reutilizó instalación previa): descarga de 5 assets (rc 0, ~1.327.842.399 bytes ≈ 1,33 GB, coincide con §2.1), `FINAL-ASSET-SHA256SUMS` 3/3 OK, extracción de los 3 tar, `SHA256SUMS` del paquete 3494/3494 OK, hash del binario OK.

## Pruebas realmente realizadas (CWD = `~/echo-backtest-873/package` en todos los casos)

| Paso | Comando (según sección del manual) | rc | Duración observada | Evidencia |
|---|---|---:|---:|---|
| §2.1 requisitos | `command -v gh tar sha256sum python3`, `uname -s -m`, `gh auth status` | 0 | instantáneo | Linux x86_64; 16G libres |
| §2.1 estructura | `mkdir $BT_HOME{,/download,/package}` | 0 | instantáneo | `~/echo-backtest-873/` |
| §2.2 descarga | `gh release download …` (5 assets) | 0 | ~60 s | `download/` |
| §2.2 verificación | `sha256sum -c FINAL-ASSET-SHA256SUMS` → 3× OK | 0 | ~10 s | — |
| §2.2 extracción | `tar -xzf` ×3 → `package/` | 0 | ~90 s | 3495 archivos físicos |
| §2.2 verificación paquete | `sha256sum -c SHA256SUMS` (3494 entradas) + hash binario | 0 | ~60 s | todos OK |
| §2.3 reapertura | `test -x/-f` ×4 + `mkdir -p runs replay reports logs` | 0 | instantáneo | — |
| §3.1 BASIC | `GOMAXPROCS=4 bin/echo-backtest experiment --input requests/basic-NQZ5.json --out runs/basic-NQZ5-01` | 0 | **858 s** | `runs/basic-NQZ5-01/` |
| §3.1 verificación | python assert `execution_state == "COMPLETE"` | 0 | instantáneo | manifest COMPLETE, artifact `basic/bt-b8a466…/result.json.gz` |
| §3.2 CAMPAIGN | `… experiment --input requests/campaign-NQZ5.json --out runs/campaign-NQZ5-01` | 0 | **604 s** | `runs/campaign-NQZ5-01/` |
| §3.2 verificación | assert COMPLETE + lectura `campaign-result.json` | 0 | instantáneo | COMPLETE/HORIZON_REACHED |
| §3.3 replay BASIC | `… reproduce --experiment runs/basic-NQZ5-01/experiment-manifest.json --nt-source-config corpus/nt-source-NQZ5-NQH6.json --out replay/basic-NQZ5-01` | 0 | **1185 s** | `verdict=IDENTICAL`, `identical=true` |
| §3.3 replay CAMPAIGN | análogo con manifest de campaña | 0 | **988 s** | `verdict=IDENTICAL`, `identical=true` |
| §4.1 reporte diario | lectura de `daily-report.json` de ambas corridas (92 filas c/u, schema `echo.backtest.daily-report.v1`) | 0 | instantáneo | contadores agregados |
| §4 verificación cifras | agregación de `daily-report.json` + `summary.economics` del artefacto + cuentas de `campaign-result.json` | 0 | instantáneo | tabla abajo |
| §8 spot-check | `bin/echo-backtest --help` | 0 | instantáneo | confirma la fila §8: la ayuda general NO lista `experiment`/`campaign` |

Tiempo total de cómputo financiero observado: 4 procesos secuenciales, ~60,6 min. Referencias de §11 (797,51 s / 548,69 s) resultaron consistentes como órdenes de magnitud en este host (858 s / 604 s); el manual advierte correctamente que son observaciones de otro host.

## Resultados obtenidos vs §4.3 (referencia de873)

| Métrica | BASIC NQZ5 nuevo | §4.3 | CAMPAIGN NQZ5 nuevo | §4.3 |
|---|---:|---:|---:|---:|
| `execution_state` / rc | COMPLETE / 0 | COMPLETE | COMPLETE / 0 (HORIZON_REACHED) | COMPLETE |
| Operaciones con fills | 39 | 39 ✓ | 15 | 15 ✓ |
| Días entrada / elegibles | 22 / 24 | 22/24 ✓ | 6 / 24 | 6/24 ✓ |
| Neto trading USD | −29.692,08 | −29.692,08 ✓ | −10.576,28 | −10.576,28 ✓ |
| Saldo nominal final USD | 70.307,92 | 70.307,92 ✓ | 98.000,12 | 98.000,12 ✓ |
| Caja / compras / burns | n/a | n/a | 4.400 / 5 / 4 | 4.400/5/4 ✓ |
| Cobros / inventario físico | — | — | 0 cobros; caja 5000−5×120=4400 ✓ | 0 ✓ |

Fuentes de cada cifra: fills y días desde `daily-report.json` (`operations_with_fill` y `eligible_5m>0` por `account_day_id`); neto/saldo BASIC desde `summary.economics` del `result.json.gz` (realized_net −29692.08 = gross −25230 + costos 4462.08; balance 70307.92); neto CAMPAIGN = suma de (saldo final − 100.000) de las 5 cuentas de `campaign-result.json` (−1999.10−2138.28−2274.58−2164.44−1999.88 = −10.576,28); saldo nominal = cuenta 5 (`ACTIVE_AT_HORIZON`) 98.000,12; caja/compras/burns desde `campaign-result.json` (`cash_final_usd` 4400, `purchases_applied` 5, 4 cuentas `BURNED_RISK_BREACH`, `collected_net_usd` 0).

Archivos por corrida, todos presentes como describe §4.1: `experiment-manifest.json` (con `request`, `identity`, `experiment_id`, `attempt_id`, `build`, `artifact` relativo, `coverage`, `streams`), `catalog-validation.json`, `daily-report.json`, `phase-wall.json`, artefacto en la ruta `artifact`, y en CAMPAIGN además `campaign-result.json`; replay emite `result.json.gz`, `runspec.json`, `execution-provenance.json`.

## Nota a la documentación: **9/10** (2+2+2+1+2)

### Preparación: 2/2
§1–§2 son autocontenidas y funcionaron a la primera sin ningún paso no documentado: requisitos comprobables por comando, tamaño de descarga exacto (1,33 GB), tres niveles de verificación de integridad (assets, unión del paquete, binario), receta de reapertura §2.3 y tabla de directorios que coincide 1:1 con el paquete real. La identidad declarada en §1 coincide byte a byte con `PACKAGE-IDENTITY.json`. Única fricción cosmética: el conteo "3.494 archivos" (ver problemas #3).

### Comandos y directorios: 2/2
Todos los comandos de §3.1–3.3 se copiaron literales y todos terminaron rc 0. La separación stdout/stderr a `logs/`, la regla de conservar rc sin `tee`, el contrato de exit codes 0/1/2 (§4.1) y las rutas relativas al manifest funcionaron exactamente como escrito. No hizo falta inventar flags ni rutas.

### Ejecución/replay: 2/2
Los replays oficiales de ambos resultados nuevos devolvieron `IDENTICAL`. Las advertencias de §3.3 resultaron load-bearing y correctas: las claves son `verdict`/`identical` (no `status`) y `reproduce` acepta `--experiment` con el manifest para corridas nuevas. Los wall de §11 sirvieron para calibrar expectativa (858 s vs 797,51 s; 604 s vs 548,69 s; replays con wall propio, como advierte el manual). Ambigüedad menor registrada como problema #4.

### Interpretación de salidas: 1/2
§4.1/§4.2/§4.3 son precisos y las cifras de referencia se reconciliaron al 100% con la corrida nueva, incluyendo las distinciones de conteo (el BASIC nuevo registró 170 fills, 146 operaciones y 39 operaciones con fills: la lección de §4.2 se verifica en los datos). Se descuenta porque **el manual no dice dónde está el dinero de un BASIC nuevo**: `summary.economics` (gross/costs/net/saldo dentro de `result.json.gz`) hubo que descubrirlo inspeccionando el JSON del artefacto; `daily-report.json` no contiene campos monetarios; §4.1 dice genéricamente que el artefacto trae "summary, estado final e integridad" sin nombrar la clave `economics`. En CAMPAIGN el dinero sí está bien encaminado (`campaign-result.json`, §3.2), pero no se aclara que el "Neto trading" de §4.3 es la suma del neto de las 5 cuentas. Detalle en problemas #1, #2 y #5.

### Diagnóstico y autonomía: 2/2
El único fallo real encontrado (404 anónimo al bajar el manual) se resolvió aplicando literalmente la fila §8 "GitHub404/permiso al descargar → comprobar acceso autenticado al repo exacto": con `gh` autenticado funcionó. La fila §8 "`help` no muestra `experiment`/`campaign`" se verificó cierta por spot-check directo de `--help`. El manual además frena la autonomía en los puntos correctos (no recalcular hashes esperados, no bajar warmup, detener la receta ante error conservando rc/SHA/stderr, no rescatar con source). Lo no ejercitado de §8 (errores de ejecución reales) no ocurrió y no se penaliza.

## Problemas detectados (ninguno bloqueante; no se aplicaron cambios)

1. **§4.1 (tabla de salidas) — ubicación del dinero en BASIC.** Instrucción exacta: "`result.json.gz` en la ruta `artifact` — Evidencia causal íntegra, inputs, resolved spec, summary, estado final e integridad." Resultado: el gross/costs/net/saldo exigidos por §12 están en `summary.economics` de ese JSON, pero el manual no nombra la clave; descubrimiento costó inspección del artefacto (2–3 pasos, sin bloqueo). Impacto: menor (fricción de descubrimiento). Corrección textual mínima: añadir en esa fila "…; para BASIC, gross/costs/net/saldo en `summary.economics` del artefacto".
2. **§4.3 (tabla de referencia) — semántica del "Neto trading USD" de CAMPAIGN.** Instrucción exacta: fila "CAMPAIGN NQZ5 … Neto trading USD −10.576,28". Resultado: esa cifra es la suma del neto de las 5 cuentas (`campaign-result.json`, saldo final − 100.000 por cuenta); el manual no lo dice. Impacto: menor (un operador que lea solo la última cuenta obtendría −1.999,88 y dudaría). Corrección textual mínima: "Neto trading = suma de (saldo final − saldo inicial) de todas las cuentas de `campaign-result.json`".
3. **§2.2 — conteo de archivos.** Instrucción exacta: "la unión original contiene **3.494 archivos**". Resultado: `find . -type f` devuelve 3.495; la diferencia es el propio `SHA256SUMS` (3494 entradas verificadas OK + el manifiesto mismo). Impacto: cosmético (puede sembrar duda de integridad en un operador que cuente). Corrección textual mínima: "3.494 archivos cubiertos por el manifiesto (más el propio `SHA256SUMS`)".
4. **§3.1 — ambigüedad del repetir.** Instrucción exacta: "**Repetir con un nombre de salida nuevo**, por ejemplo `-02`". Resultado: leída como imperativo dentro de la receta sugiere una segunda corrida completa obligatoria (~14 min más); el replay de §3.3 ya acredita el determinismo. Impacto: menor (posible gasto doble). Corrección textual mínima: "Si quieres verificar repetibilidad con una segunda corrida, repite con un nombre de salida nuevo, por ejemplo `-02`; el replay de 3.3 ya compara la ejecución sellada".
5. **§4.3 — dónde se lee "elegibles".** Instrucción exacta: columna "Días entrada/elegibles" (22/24, 6/24). Resultado: el denominador se obtuvo contando `account_day_id` con `eligible_5m>0` en `daily-report.json`; el manual no indica esa fuente. Impacto: menor. Corrección textual mínima: "elegibles = account-days con `eligible_5m>0` en `daily-report.json`".

## Respuesta final

**¿Un agente nuevo pudo ejecutar ambos casos sin ayuda externa? SÍ.** Instalación nueva completa, BASIC NQZ5 (`runs/basic-NQZ5-01`, COMPLETE, rc 0, 858 s) y CAMPAIGN NQZ5 (`runs/campaign-NQZ5-01`, COMPLETE/HORIZON_REACHED, rc 0, 604 s) ejecutados con los comandos literales del manual, y ambos replays oficiales devolvieron **`IDENTICAL`** (rc 0; 1185 s y 988 s). Los reportes diarios se consultaron y todas las cifras de §4.3 se reconciliaron exactamente con la corrida nueva, incluida la conciliación de caja `5000−5×120=4400`, 5 compras, 4 burns y 0 cobros.

**Ayudas o inferencias necesarias (únicas):** (a) para descargar el manual desde la URL del encargo hubo que autenticarse con `gh`, aplicación directa del diagnóstico §8 y del requisito §2.1 "acceso GitHub ya autorizado"; (b) para el neto/saldo del BASIC se inspeccionó `summary.economics` dentro de `result.json.gz` (clave no nombrada por el manual, problema #1); (c) el "Repetir -02" de §3.1 se interpretó como opcional porque el encargo pedía una corrida por modalidad y el replay ya cubre la reproducción; (d) los días "elegibles" se contaron desde `eligible_5m` del reporte diario (problema #5). No se leyó source, no se usaron memorias del proyecto ni conversaciones previas para suplir pasos del manual, y no se ejecutó NQU6, all13 ni suites del repositorio.

**NO EVALUADO (fuera del alcance del encargo, sin puntos ni penalización):** §3.4 (replay/`daily-report` de resultados publicados), §3.5 y NQU6, §5 all13/`validate-catalog`, §9–11 (composición, API, suites, build), Live/publish, y el resto de filas de §8 no provocadas (p. ej. `DIVERGENT`, `ENOSPC`).

**Evidencia conservada fuera del source:** `~/aranea/work/bt-doc-usability-20261011/` (copia del manual con SHA) y todas las salidas del operador en `~/echo-backtest-873/package/{runs,replay,reports,logs}`; `reports/` quedó vacío porque §3.4 no estaba en alcance. Copia de este informe: `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BACKTEST-DOC-USABILITY-REPORT.md`.
