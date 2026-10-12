---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-CONTRACT]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-EVIDENCE-A

## Propósito

Recibo de evidencia y handoff de la etapa A. El estado de iniciativa pertenece exclusivamente a [[TRADESGERARD-CONTROL]]. Este documento conserva identidades, alcance probado y límites; no acepta el gate del Owner. Mientras falten freeze y ejecución independiente, sus resultados parciales no habilitan GLM.

## Contenido

### Identidades y procedencia

Repo: `xKoRx/echo`. Baseline inspeccionado: `873f5f1c7df25086271af1de1896095f1cade2a9`, rama histórica `codex/btx-perf-last`. Desarrollo aislado: rama `codex/tradesgerard-platform-a`, checkout relativo al workspace Aranea `work/tradesgerard-platform-a-20261012/echo`. SDD: `specs/FEAT-TRADESGERARD-PLATFORM-A/`. Commit candidato, binario nuevo, SHA256 y procedencia embebida: pendientes de freeze; no hay sustitución por una build histórica.

El binario histórico tiene SHA256 `49957b660e0a248cd03fc9f321461b8f8ae190856f1bd7740950807c475b64af` y source embebido `48647d1ff9860bd4e1fff47e5fca7c9be273fb74`, distinto del baseline873. No certifica esta implementación. Manual baseline leído: blob `b66dacec9a0f6e0bc99ac13bde3a8e53cdb036e3`; el blob anterior citado por el mandato no se atribuye al checkout encontrado.

Modelo solicitado de cada TOP: `gpt-6.1-sol`; modelo servido: UNKNOWN. No se usó CLOUD Pro ni se lanzó GLM. Informes y logs pesados residen fuera del vault, bajo `work/tradesgerard-platform-a-20261012/evidence/` del workspace Aranea.

### Evidencia del autor recibida

El inventario confirmó reutilización de owners de provider, operación/MM, accounting, ejecución causal y replay. El delta incorpora registro preservado de cuentas, relojes de todas las cuentas, campaña y caja, reglas de fase, composición pública alternativa, salida compacta y lote. La lista siguiente recoge informes del autor; queda sujeta a repetición y falsificación independientes sobre el freeze exacto.

- Registro y relojes de cuentas pausadas, regresión ReplaceAccount, reglas de perfil/ladder/DST/feriados y piso Live intraday: PASS focalizado.
- Ruta causal pública de dos sesiones sintéticas: compra única de120, caja4880, saldo50000 y censura de horizonte conciliada. Cancelación preserva caja, marca fallo y drena Finish.
- Nueva Strategy/MM por fábricas públicas: entrada1, add1, salida física2; cancelación de protecciones y BE200/TP250→500. Proyección económica usa gross y costos del ledger autoritativo una vez.
- Paridad detallado/compacto y batch resume/retry/tamper: PASS informado. Fallos de disco, pico/cleanup y matriz completa todavía requieren recibo físico final.
- `lifecycle-final-dll-test.log`: PASS27,027s en23sesiones sintéticas; dos evaluaciones pasan con3090,24netos y6días, llegan aLiveSim; retiro2250 acredita1611; primer funded queda50325,2 sin breach DAILY_LOSS/TRAILING. Tres cuentas preservadas, una ejecutando. Ningún rendimiento del fixture se presenta como rentabilidad.

Defectos descubiertos y corregidos por el autor antes de ese milestone: fase desactualizada en `liveConfig.Accounts` tras cambiar binding; baseline diario/piso al iniciar funded; retiro contado indebidamente como pérdida diaria; compra nueva sin min-days0 explícito. El test de crédito inicial podía pasar pese a esos defectos secundarios; se añadieron asserts permanentes para ausencia de DLL espurio y aprobación de la cuenta comprada. Los logs fallidos previos permanecen en evidencia del integrador.

Revisión posterior: caja/ruina y search/fault/batch PASS8,946s antes de la última corrección. Manager detectó por lectura dos riesgos de durabilidad; el autor confirmó/corrigió la transición a FAILED con firstcause si falla el readback posterior a COMPLETE, y cambió temporales JSON a creación exclusiva/cleanup sólo del archivo creado por esa llamada, preservando sentinels ajenos. Repetición sobre esas correcciones y falsificación independiente pendientes; el PASS anterior no se atribuye a la fuente posterior.

`current-platform-tests.log` recoge PASS posterior de TestPlatform/TestSearch, incluido el ciclo público corregido. La regresión con coverage detectó un negativo heredado cuyo literal `INTRADAY_TRAILING` dejó de ser desconocido al implementar el contrato Live. Manager aprobó TCR acotado en el SDD: cambiar sólo ese literal a `UNKNOWN_TRAILING` en `TestEvaluateEconomicRisk_StaticLockNeverRatchets`, preservando todos los asserts. Aplicación/repetición por el integrador y comprobación independiente pendientes a este corte. Suites largas backtester/cmd agotaron180s; son NOT_PASS, con comparación de baseline en condiciones idénticas pendiente. No se modifican denominadores para ocultarlo.

### Verificación independiente

Catálogo: auditoría y reparación independientes completas. `design-2` conserva53 IDs y produce23040 configuraciones raw,7680 incompatibles,192 alias y15168 únicas compatibles;59 checks PASS. Cobertura de sentencias del generador119/121=98,3471%; no es cobertura del motor ni de branches. SHA256 del único catálogo editable `catalog.json`: `e367741ad47975e4a8b1aff3172bc10e659ed52cb9993f8db81507ceb588abd4`.

Producto: TOP verifier_a preparó15 grupos de casos propios en `evidence/verifier/preparation/ADVERSARIAL-MATRIX.md`. Preparación no ejecutada contra producto. Debe comprobar cada fila del §10, identidad source/binario antes y después, cobertura nueva mínima95% con baseline separado, smoke real, regresiones y fallos/limpieza. Recibo independiente final pendiente.

### Datos y recursos

Corpus legible relativo al workspace Aranea: `work/btx-perf-last-20261010/integrator/package/corpus`. La solicitud all13 permanece NOT_READY por gaps/prefijos; no se ha repetido para fingir cobertura. Los datos originales del otro workspace no son accesibles y no se cambiaron permisos. Smoke real requiere catálogo validado y ventana explícita fijada antes de resultados; todavía no se adjunta una receta validada para la nueva build.

Hashes inspeccionados: NQZ5.nt `700579b3b3c78e58ccceb39bd79e8d11aa3efab3e8457d92bee1833ef2686406`; NQH6.nt `31546615336370083b02ad7878cbd86a362d7bf3967b9a984478735b7598d643`; NQU6.nt `d4cbbdcdbe7bcb2932f1fbfb1418e8f12a52ef3305df29d5619a19cef6112be3`.

Límites fijados: reserva libre≥8GiB, scratch propio≤2GiB, salida durable≤256MiB, logs≤16MiB, GOMAXPROCS4 y un carril de build/prueba/campaña. Muestra administrativa posterior:11.568.177.152bytes libres y20.841bytes de evidencia. Esa muestra no acredita el pico de una campaña ni pruebas de ENOSPC; recibo final de recursos pendiente. No se borraron corpus, caches ni artefactos ajenos.

### Handoff y frontera con B

Manual único: `v3/backtester/README.md`, pendiente actualización/validación final por integrador. Comandos exactos, schemas públicos, configs reproducibles, commit/build final, resultados independientes y próximo comando se completan aquí con evidencia física; no se inventan flags.

[[TRADESGERARD-GLM-MASTER]] encarga implementar todos los indicadores y variantes de B, luego baseline y producto cartesiano compatible completo con continuidad de lote. B no absorbe capacidades estructurales de A pendientes de demostrar. [[TRADESGERARD-PROP-PROFILE]] distingue hechos oficiales y escenario sintético explícito; readiness técnico no certificaría términos comerciales UNKNOWN, operación LIVE ni rentabilidad.

## Fuentes

- [[TRADESGERARD-MANDATE-SNAPSHOT]], §§10–12; [[TRADESGERARD-CONTRACT]] y [[TRADESGERARD-PROP-PROFILE]].
- Informes físicos de TOP inventory, contract_audit y catalog_repair; logs y receipts del integrador bajo el workspace Aranea.
- `xKoRx/echo:specs/FEAT-TRADESGERARD-PLATFORM-A/`; matriz prospectiva del verificador independiente.
