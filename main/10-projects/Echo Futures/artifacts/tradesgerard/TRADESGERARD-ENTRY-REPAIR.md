---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-B-RESULTADO]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-ENTRY-REPAIR

## Propósito

Reparar y verificar el recorrido de oportunidades TradesGerard KISS-1 bajo el mandato del Owner del 2026-10-13. El objetivo es funcionamiento correcto, no rentabilidad. Este es el único informe de reparación; los resultados históricos permanecen conservados.

## Contenido

### Estado vigente

IN_PROGRESS — identidad B comprobada y primer censo independiente terminado; diagnóstico/reparación y falsificación siguen activos. Restricciones contradictorias localizadas en fuente, pendientes de cerrar reproducción causal y regresiones. No hay corrección certificada ni comparación nueva. Aceptación final del Owner pendiente; ninguna autorización LIVE, release, merge productivo o despliegue.

### Identidades comprobadas por el manager

| Elemento | Evidencia física |
|---|---|
| Fuente B | `xKoRx/echo`, rama `codex/tradesgerard-b-glm`, HEAD `10d406b3cddbd9c738dbc64b5db38c16ff7527b9`; `git status --short` vacío al arranque. |
| Checkout B | `ARANEA_ROOT/work/tradesgerard-b-glm-20261012/echo`. |
| Binario B | `ARANEA_ROOT/work/tradesgerard-b-glm-20261012/bin/echo-backtest`, SHA256 `f00efd668eee8b121f7efb65b1b92923620e47beaac650a99491b425027486e8`. |
| Metadata ejecutable | `go version -m`: Go1.27.1, linux/amd64, vcs.revision igual al HEAD B, vcs.modified=false. |
| Evidencia histórica | `work/tradesgerard-b-glm-20261012/{inputs,prepared,runs}`, relativa a ARANEA_ROOT; T0/T1/T1-L/RESULTADO leídos. COMPLETE histórico no prueba corrección de señal. |
| Agents-OS | `xKoRx/agents-os`, checkout local master limpio al arranque. Escritura canónica mediante materializador; sincronización del nuevo informe todavía no verificada. |

La abreviatura `f00efd66…c4fed` de RESULTADO no es identidad válida del binario T1: el SHA completo físico anterior gobierna. No se ha recompilado ni modificado B.

### Ejecución y aislamiento

Manager: coordinación, inspección, adjudicación y documentación; sin código ni integración. Implementador único: `/root/entry_repair_implementer`; independiente: `/root/entry_repair_verifier`. Modelo solicitado para ambos `gpt-6.1-sol`; servido UNKNOWN mientras no exista metadata fiable. Primer dispatch del implementador falló por capacidad; el único reintento con el mismo modelo arrancó correctamente. Sin sustitución de modelo, sin consumo CLOUD Pro.

Evidencia nueva externa al vault: `ARANEA_ROOT/work/tradesgerard-entry-repair-20261013/{implementer,verifier}`. El implementador posee el carril Go/build/campañas; el verificador puede solapar el oráculo ligero sobre OHLC físico, sin usar `tg` como oráculo. Cada ejecución debe fijar source, build e inputs y drenar sus procesos.

Lectura inicial de recursos: disco aproximadamente16GiB disponibles y RAM64GiB available; es observación puntual, no permiso de consumo. Reserva disco≥8GiB, scratch≤2GiB, durable≤256MiB/lote, logs/trazas≤16MiB; presupuesto agregado y picos pendientes de recibo. No borrar corpus, caches, builds o evidencia ajena.

### Gates pendientes

- Censo independiente completo T1 y prefijo efectivo: OHLC/timestamps→K/ATR→identidad de cada cruce, sesiones/NY/exclusiones y tolerancia prospectiva.
- Reproducción corta del primer rechazo K01 y cruces posteriores; cierre y nuevas señales K02/K03; primera divergencia causal.
- Parche mínimo en propietarios, regresiones red/green, liberación tras decline/finality, evolución continua de indicadores, compra a demanda con cuenta pausada y negativos reales.
- Observabilidad compacta: cruces, señales, supresiones, MM/Provider, órdenes, operaciones agregadas, fills, cierres, días, duración/rachas y economía conciliados. Reconciliar expresamente162/253 frente a137/274 históricos.
- Sizing dimensional de primeros rechazos/admisiones por perfil, sin alterar R/T, instrumento, costos ni multiplicadores.
- Comparación K01–K05 retiro2300; diez configuraciones corregidas con ambos retiros sobre T1 exacto, before reproducible y deltas absolutos.
- Falsificación independiente del commit/build exactos, cobertura nueva≥95% con denominador compatible, paridad offline afectada, recursos y cleanup.

### Adjudicación

Hechos confirmados: identidad física B y disponibilidad local; el censo independiente y las ramas causales inspeccionadas abajo. Hipótesis refutadas: ninguna todavía. Defectos corregidos: ninguno todavía. Decisiones nuevas pendientes: ninguna identificada; KISS-1 sigue vigente y design-2 es histórico.

### Censo independiente inicial — readback verificado

`verifier/oracle-summary.json`, `oracle-bars.csv`, `oracle-crosses.csv` y `oracle.py`, relativos a la raíz de evidencia nueva. Archivo físico SHA256 `700579b3b3c78e58ccceb39bd79e8d11aa3efab3e8457d92bee1833ef2686406`; Python stdlib lee filas originales y calcula indicadores sin llamar `tg` ni Echo. Resultado:42969 barras físicas,2959 cruces brutos,755 cruces dentro de la ventana operable del plan en31 fechas NY. Hay350 barras de entrada por fecha:10850 en total. El prefijo efectivo y los límites de horizonte del plan se están reconciliando explícitamente con la fecha abreviada del reporte histórico.

Tolerancia fijada por el independiente:1e−9 absoluta para K/ATR; no cambia decisiones estrictas20/80. Warmup matemático: rawK desde barra20, K desde22, primer par comparable23; ATR semilla20; D informativa desde24 sin gate. Tabla por sesión conserva preparación y exclusiones.

| Oportunidad inicial | K previa → actual | ATR puntos |
|---|---:|---:|
| SHORT2025-10-14T14:33Z /10:33NY |82,5927452264→75,5520430532|22,9127492199|
| SHORT2025-10-14T14:48Z /10:48NY |82,6870807816→69,1052785069|20,3033672470|
| LONG2025-10-14T14:55Z /10:55NY |11,6913385991→22,8282828283|20,0757086495|

El independiente localizó sólo la primera evaluación MM de K01 en el histórico de esa jornada;14:48Z es la primera oportunidad posterior cuya omisión se investiga. Esto no declara todavía que el primer rechazo debiera haberse admitido ni que la primera divergencia de indicador ocurra en14:48Z.

Inspección de fuente corroborada por manager: `tg/tg.go:242–249` mantiene explícitamente un ciclo técnico por día y deriva `NewCycle` de `CycleOpen`; `tg.go:295/306` realimenta ATR cuantizado al tick; `platform_campaign.go:492` mantiene el veto global de compra por cualquier cuenta pausada. Las tres ramas contradicen aspectos del contrato actual. El implementador debe demostrar cada impacto con input mínimo, primera divergencia y regresión baseline/fix; el independiente conserva su propio oráculo.

## Fuentes

- Mandato del Owner `ECHO FUTURES — GOD LOCAL: DIAGNÓSTICO Y CORRECCIÓN DE ENTRADAS TRADESGERARD`, PROMPT_VERSION1, 2026-10-13.
- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-B-PLAN]], [[TRADESGERARD-B-T0]], [[TRADESGERARD-B-T1]], [[TRADESGERARD-B-T1L]], [[TRADESGERARD-B-RESULTADO]].
- `xKoRx/echo:AGENTS.md` y `v3/backtester/README.md`; `git status --short`, `git rev-parse HEAD`, `git branch --show-current`, `sha256sum` y `go version -m` ejecutados sobre las rutas anteriores.
