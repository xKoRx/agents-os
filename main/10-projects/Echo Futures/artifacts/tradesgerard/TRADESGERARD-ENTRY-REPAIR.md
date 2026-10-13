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

IN_PROGRESS — identidad B comprobada; censo independiente y diagnóstico/reparación delegados a dos TOP LOCAL fresh-context. No hay aún defecto demostrado, corrección certificada ni comparación nueva. Aceptación final del Owner pendiente; ninguna autorización LIVE, release, merge productivo o despliegue.

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

Hechos confirmados: identidad física B y disponibilidad local. Hipótesis refutadas: ninguna todavía. Defectos corregidos: ninguno todavía. Decisiones nuevas pendientes: ninguna identificada; KISS-1 sigue vigente y design-2 es histórico.

## Fuentes

- Mandato del Owner `ECHO FUTURES — GOD LOCAL: DIAGNÓSTICO Y CORRECCIÓN DE ENTRADAS TRADESGERARD`, PROMPT_VERSION1, 2026-10-13.
- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-B-PLAN]], [[TRADESGERARD-B-T0]], [[TRADESGERARD-B-T1]], [[TRADESGERARD-B-T1L]], [[TRADESGERARD-B-RESULTADO]].
- `xKoRx/echo:AGENTS.md` y `v3/backtester/README.md`; `git status --short`, `git rev-parse HEAD`, `git branch --show-current`, `sha256sum` y `go version -m` ejecutados sobre las rutas anteriores.
