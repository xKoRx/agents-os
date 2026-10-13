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

`verifier/oracle-summary.json`, `oracle-bars.csv`, `oracle-crosses.csv` y `oracle.py`, relativos a la raíz de evidencia nueva. Archivo físico SHA256 `700579b3b3c78e58ccceb39bd79e8d11aa3efab3e8457d92bee1833ef2686406`; Python stdlib lee filas originales y calcula indicadores sin llamar `tg` ni Echo. Resultado:42969 barras físicas,2959 cruces brutos,755 cruces dentro de la ventana operable del plan en31 fechas NY. Hay350 barras de entrada por fecha:10850 en total. El plan fija `trade_start=2025-10-14T13:30Z` (09:30NY), con entradas desde10:00NY; el prefijo efectivo contiene1118 barras y68 cruces. Quedan2891 cruces brutos posteriores a trade_start. La frontera de fuente es2025-10-13T17:51Z, primera barra cerrada17:52Z; último cierre físico2025-11-25T22:00Z, horizonte del plan23:00Z. Las horas restantes son cierre del calendario, no barras fabricadas.

Tolerancia inicial fijada por el independiente:1e−9 absoluta para K/ATR; no cambia decisiones estrictas20/80. El oráculo se fortaleció con aritmética racional exacta para K y los umbrales: conserva755 oportunidades; ATR usa float64 y tolerancia1e−9. Warmup matemático: rawK desde barra20, K desde22, primer par comparable23; primer TR=H−L si no existe cierre previo entregado, ATR semilla20; D informativa desde24 sin gate. Tabla por sesión conserva preparación y exclusiones.

| Oportunidad inicial | K previa → actual | ATR puntos |
|---|---:|---:|
| SHORT2025-10-14T14:33Z /10:33NY |82,5927452264→75,5520430532|22,9127492199|
| SHORT2025-10-14T14:48Z /10:48NY |82,6870807816→69,1052785069|20,3033672470|
| LONG2025-10-14T14:55Z /10:55NY |11,6913385991→22,8282828283|20,0757086495|

El independiente localizó sólo la primera evaluación MM de K01 en el histórico de esa jornada;14:48Z es la primera oportunidad posterior cuya omisión se investiga. Esto no declara todavía que el primer rechazo debiera haberse admitido ni que la primera divergencia de indicador ocurra en14:48Z.

Inspección de fuente corroborada por manager: `tg/tg.go:242–249` mantiene explícitamente un ciclo técnico por día y deriva `NewCycle` de `CycleOpen`; `tg.go:295/306` realimenta ATR cuantizado al tick; `platform_campaign.go:492` mantiene el veto global de compra por cualquier cuenta pausada. Las tres ramas contradicen aspectos del contrato actual. El implementador debe demostrar cada impacto con input mínimo, primera divergencia y regresión baseline/fix; el independiente conserva su propio oráculo.

TCR adjudicado por manager dentro del mandato del Owner: `specs/FEAT-TRADESGERARD-ENTRY-REPAIR/TEST_CHANGE_REQUEST.md` en el checkout de reparación. Se autoriza sustituir sólo la expectativa de ATR cuantizado por Wilder independiente (semilla20 y tolerancia1e−12), manteniendo asserts de K/replay; y la expectativa de veto por cuenta pausada por admisión con caja/cupo/sesión reales más negativos. El fixture heredado tiene una cuenta, no una quinta; descripción corregida solicitada. No se autoriza saltar tests ni debilitar límites.

### Rectificación I1 — ENTRY-REPAIR-C01

Readback independiente de los diez resultados físicos conservados: `verifier/baseline-reconciliation.json`. Todas las configuraciones emitieron755 señales OPEN, coincidentes en total con las755 oportunidades NY del oráculo. No se acredita todavía identidad uno a uno sólo con ese total; el contraste individual sigue en curso. Los números históricos llamados «cruces» eran intentos materializados, no el censo de cruces de mercado.

| Perfil, por retiro | OPEN emitidas | Operaciones creadas | Con fills | Registros FILL | Rechazos sizing |
|---|---:|---:|---:|---:|---:|
| K01 |755|31|0|0|31|
| K02 |755|36|18|36|18|
| K03 |755|36|7|14|29|
| K04 |755|31|1|2|30|
| K05 |755|35|6|12|29|

La suma es169 operaciones creadas y137 rechazos para cinco perfiles con un retiro;338 y274 al incluir ambos retiros. La cifra162/253 no concilia con esta población. No se publica un porcentaje sustitutivo mezclando cruces, intentos y callbacks. La baja actividad no queda explicada por los31 rechazos K01:724 señales emitidas no llegaron a una nueva materialización; su clasificación causal exacta está en reproducción. Los36 FILL de K02 pertenecen a18 operaciones con fill, no36 operaciones.

T1 conserva estado de ejecución COMPLETE10/10 y contabilidad conciliada. Validez analítica: AFFECTED para frecuencia, denominadores y explicación de oportunidades; reemplazo en este informe todavía IN_PROGRESS. T1-L conserva su selección histórica K01/K02 y COMPLETE4/4; no se reejecuta ni se transfiere automáticamente el nuevo resultado.

Observación adicional para adjudicar: el recibo corto baseline K01 registra compra inicial2025-10-14T13:30Z (09:30NY), anterior a la ventana10:00NY. Se pidió investigar la ruta de bootstrap y probar compra real a demanda/horario, sin dar por suficiente el test aislado de `canPurchase`.

### Reproducción y corrección en curso

El baseline corto K01 ejecutado con el binario B original terminó COMPLETE, intento1, recibo `implementer/evidence/baseline-short-K01/49fee730f22ec7d8545b21be2d3ddb9a9b88b079082fd66dcafcce8967e5c631/receipt.json`; resultado SHA256 `b07197241ce9e65dbe91f1c7e41e1de251936c3c5534a6391b738d15da843249`. Cero fills, una operación materializada y23 callbacks de gestión en esa jornada; caja4880. El baseline permanece sin cambios.

Regresiones nuevas RED sobre fuente defectuosa (`implementer/evidence/red-tg.log`): `TestEntryRepairEveryZoneExitStartsDistinctOpportunity` falla porque la nueva salida de zona no abre nueva oportunidad; `TestEntryRepairWilderSeedAndReadiness` observa19 TR en la barra20. Esto prueba defectos de señal/preparación, aún pendiente del gate físico completo y contraste de ATR por barra.

TCR adicional aprobado tras inspección: en `TestTG_CrossEmissionAndSingleConsumption`, el segundo LONG independiente debe marcar nueva oportunidad; se conservan dirección, cantidad de señales, stop y no duplicación. La supresión por operación ocupada pertenece a la capa que conoce exposición/finality y debe probar ausencia de backlog. El fixture heredado retrocede timestamps tras el segundo cruce; se autorizó corregir sólo su secuencia temporal con evidencia.

La ruta `purchaseInitial()` fue confirmada como bypass que factura a trade_start antes de10NY; la corrección de compra inicial a demanda está en curso. Tests quiet sin oportunidad deben conservar caja5000; los que realmente compran mantienen su débito. Cualquier ajuste heredado adicional requiere TCR concreto y negativos, no sustitución global de expectativas.

El independiente ejecutó por CLI original dos reproducciones sintéticas espejo, LONG y SHORT, con rechazo inicial10:01NY y un nuevo cruce de la misma dirección10:45NY tras descenso de ATR, sin visitar la banda contraria. Resultados baseline en `verifier/synthetic/{long-baseline,short-baseline}`: COMPLETE/conciliados, una operación materializada, cero fills; el segundo cruce llega como gestión. Estas series prueban funcionamiento y no sustituyen el censo real ni una campaña económica. Gate corregido pendiente.

TCR `TestTG_CycleBookkeeping` aprobado: el cruce instantáneo consumido no conserva un ciclo técnico hastaEOD. Se mantiene respuesta conservadora ante estado ilegible y se exige probar que rollover/activación no relajan las barreras de exposición/finality de Operation.

### Primera divergencia acreditada contra módulo público B

El independiente condujo42969 barras originales por `tg.Evaluate` público y las comparó por identidad con su oráculo externo. `verifier/comparison-baseline.json` demuestra cero diferencias de dirección en755 oportunidades; sólo31 se marcan `NewCycle=true`. Primera diferencia absoluta de ATR:2025-10-13T18:11Z, línea física30570; oráculo ya sembrado8,7875 y B aún vacío. Primera diferencia de valor:18:12Z, esperado8,573125 y B8,75. Error absoluto máximo ATR en la muestra:1,35505950137 puntos. Se separan semilla desplazada y cuantización recurrente; no se atribuye toda la desviación a una sola causa.

Primera diferencia de identidad de ciclo: SHORT2025-10-14T14:48Z, línea31747, K69,1052785069 correcto; B entrega `NewCycle=false`, `TG_SIG_B_CROSS_SAME_CYCLE`, ATR20,75 frente20,3033672470 independiente. La hipótesis de que faltaban los cruces brutos o cambiaban entre perfiles queda refutada en el contraste del módulo/mercado; el fallo de recuperación está downstream del cruce. La evolución bajo exposición completa aún se prueba con la cadena integrada.

El probe independiente fuera de horario usa29 barras09:31–09:59NY y trade_start09:58NY, sin OPEN ni operaciones: B igualmente compra por120. Recibo `verifier/synthetic/outside-baseline-v3/c5162363206b6810cceccd934bdb462d2d4c2af99b79b19fb048e1b4bd6df357/receipt.json`. Se confirma defecto de compra inicial fuera de demanda/horario, distinto del veto por cuenta pausada.

TCR ON_DEMAND aprobado para tres fixtures heredados: quiet(Session999 sin OPEN en2sesiones), cancelado antes del primer input y cierre de recorder inyectado sobre quiet. Expected caja5000/cuentas0, preservando primera causa, FAILED/reconciliación y asserts financieros de los fixtures con oportunidades reales. El nuevo seam de compra debe preservar el guard público de frontier y finality; el fallo de esa integración detectado durante desarrollo no es PASS.

### Sizing: rechazo inicial legítimo no equivale a día inviable

`verifier/first-day-sizing-oracle.json` calcula geometría por cruce con headroom fresco explícito; no simula PnL posterior. Para K01, antes del primer fill esa hipótesis corresponde al caso observado sin operaciones previas. NQ: punto20USD, tick0,25=5USD; comisión ida/vuelta4,98USD y slippage modelado ida/vuelta10USD, total14,98USD por contrato. R/T250/250 yρ1 permanecen congelados.

| K01,2025-10-14 | ATR puntos | SL técnico | Distancia puntos | Pérdida estimada1contrato | Q |
|---|---:|---:|---:|---:|---:|
|10:33NY SHORT|22,91274922|24719,75|22,75|469,98USD|0|
|10:48NY SHORT|20,30336725|24719,50|20,25|419,98USD|0|
|14:12NY LONG|11,58918830|24888,50|11,50|244,98USD|1|

El primer rechazo es compatible con R250, pero la señal14:12NY del mismo día tiene cantidad geométrica1 sin cambiar R/T. Admisión/fill físico corregido aún pendiente. Para K02–K05 los cálculos con headroom fresco no sustituyen la trayectoria de pérdidas/pausas de una campaña; deben contrastarse con el estado efectivo.

Ampliar un multiplicador de ATR aumenta distancia y costo por contrato y reduce la cantidad admisible a presupuesto fijo; no resuelve este bloqueo de ciclo. El ejemplo sólo demuestra por qué hay que volver a evaluar nuevas señales cuando ATR cambia, sin recomendar nuevos parámetros.

El independiente observó además K02: fill de SL14:35:26Z deja exposición flat, pero la operación sólo llega a TERMINAL en15:55NY; el nuevo SHORT14:48Z queda afectado. Regresión y finality del candidato siguen pendientes.

Sincronización observada de Agents-OS: commit automático `a58ec551187749deaa6d3f0566e1c556d9b456b8`, master remoto igual según `git ls-remote` antes de este delta. No fue un push ejecutado por el manager; los deltas posteriores requieren nueva comprobación.

## Fuentes

- Mandato del Owner `ECHO FUTURES — GOD LOCAL: DIAGNÓSTICO Y CORRECCIÓN DE ENTRADAS TRADESGERARD`, PROMPT_VERSION1, 2026-10-13.
- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-B-PLAN]], [[TRADESGERARD-B-T0]], [[TRADESGERARD-B-T1]], [[TRADESGERARD-B-T1L]], [[TRADESGERARD-B-RESULTADO]].
- `xKoRx/echo:AGENTS.md` y `v3/backtester/README.md`; `git status --short`, `git rev-parse HEAD`, `git branch --show-current`, `sha256sum` y `go version -m` ejecutados sobre las rutas anteriores.
