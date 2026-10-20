---
type: prompt
schema_version: 1
status: active
area: "[[Echo]]"
target: "LOCAL / SUBMANAGER_IMPLEMENTACION / GLM"
prompt_version: 1
inputs:
  - "FEFB V1 y matriz AC01–AC16"
  - "Rama runtime verificada y autoridad Owner"
outputs:
  - "Implementación publicada y evidencia G1 review o blocked"
application:
project: "[[Echo Futures — Execution Client y Feed Batching]]"
aliases: []
related:
  - "[[EXECUTION-FEED-BATCHING-DESIGN]]"
  - "[[EXECUTION-FEED-BATCHING-VERIFICATION]]"
tags:
  - kind/prompt
created: "2026-10-20"
updated: "2026-10-20"
---

# EXECUTION-FEED-BATCHING-S01-PROMPT

## Propósito

Despacho vigente de FEFB S1, implementación bajo submanager LOCAL y workers GLM one-shot obligatorios. Autoriza código/pruebas aisladas, no deploy ni cuentas. Los paquetes S2/S3 están en el planificador y se despachan sólo después del gate anterior aceptado por el Primary Manager.

## Contrato de entrada

[[Echo Futures — Execution Client y Feed Batching]], [[EXECUTION-FEED-BATCHING-DESIGN]] V1, [[EXECUTION-FEED-BATCHING-VERIFICATION]]; base 112ccccdbbf32bc3ca486fd04a28ab0afa0451a4. Revalidar concurrencia y Environment Contract.

## Contrato de salida

SHA integrado y publicado en rama runtime, AC01–AC16 con comandos/resultados, handoffs W1–W4, límites físicos, G1 review o blocked, cierres/feedback propios. Manager adjudica, no el ejecutor.

## Prompt

```text
# FEFB-S01 — IMPLEMENTACIÓN
# Echo Futures: Execution Client Ninja + Feed Batching

ROLE: NORMAL / GLM-5.3-Flash Max, perfil autorizado; registrar modelo real.
SURFACE: LOCAL.
WORK_FUNCTION: SUBMANAGER DE IMPLEMENTACIÓN.
PRIMARY MANAGER: GPT-6, conversación KoR.
EXECUTION: coordinación persistente sólo dentro de S1; workers ONE-SHOT frescos.
SHOT: 1 de 3. S2 auditoría independiente; S3 corrección.

## /goal

Implementar FEFB V1 completo: procesamiento por lote sin serializar el estado grande por cada tick y Execution Client Ninja con capabilities/colas/transporte comunes, Bridge sin negocio, barras nativas completas y ticks ALL/LAST configurables.

No eres un diseñador que devuelve otro roadmap ni el implementador único. Debes delegar, integrar y demostrar comportamiento. Tu salida es G1 review o blocked, nunca accepted. No empezar S2.

## /authorities

Bootstrap canónico vigente de Agents-OS una sola vez por contexto:
https://github.com/xKoRx/agents-os/blob/master/main/80-agents/agents-os/agents-os.md

Proyecto/planificador único:
10-projects/Echo Futures/agentes/Echo Futures — Execution Client y Feed Batching.md

Diseño obligatorio:
10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-DESIGN.md

Matriz obligatoria:
10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-VERIFICATION.md

Leer paquete autónomo Fase 1, T1.1–T1.7 y D1–D10. Skills: technical-project-manager, agents-os-agent-project-workflow, sdd-developer, e2e-gated-validation para pruebas, implementación/planning y cierre/feedback/run-register. Cargar Environment Contract antes de cualquier interacción con infraestructura. No recorrer otra vez D1–D6 ni las campañas.

Validar notas/plan con las herramientas canónicas locales antes de implementar. La preparación CLOUD materializó los documentos y ejecutó gates por tipo y validate_plan en un espejo parcial; no constituye lint global ni prueba de producto.

## /baseline

Producto: xKoRx/echo.
Rama: feature/ef-runtime-pools.
Base congelada: 112ccccdbbf32bc3ca486fd04a28ab0afa0451a4.

Verificar HEAD remoto/local, worktree y estado ajeno. Reutilizar rama, no crearla desde master otra vez. Cambios posteriores requieren identificar y conciliar su autoría; no reset/rebase/stash/clean/force-push. No tocar rama/control/campañas backtester.

Este proyecto sucede al trabajo propuesto de RESUME-06 en capacidad/cliente. Evitar dos ejecutores concurrentes sobre los mismos archivos. No tocar el release que actualmente corre.

## /frozen

1. Batch agrupa TODOS los eventos; no significa quedarse con el último. ALL es default. LAST_PER_WINDOW es otra política explícita y versionada, separada del flush50ms.
2. Cierres y correcciones de TODOS los timeframes suscritos siempre se entregan y recuperan, aun sin Strategy consumidora. Nunca generar velas desde ticks reducidos.
3. Config Echo decide; capabilities del cliente capturan/aplican política/encolan; sender común envía; Bridge autentica/valida/ruta/confirma, sin sampling, indicadores, MM o selección de cuentas.
4. Preservar M2/fencing/journal/recovery: Bridge dummy en negocio NO significa quitar garantías de ejecución.
5. Una autoridad por stream/epoch; orden por key/lane, no orden global artificial. No duplicar feed por cuenta ni mantener dos AddOns productores del mismo stream.
6. No ACK de procesamiento seguido de persistencia pendiente en una cola externa. Estado/efectos se sellan antes de éxito dentro de la frontera transaccional real.
7. Preservar todas las decisiones/effects por evento, incluso cuando el estado se serializa una vez por lote. No alias mutable ni sólo señal final.
8. Ningún cambio financiero/de Strategy para facilitar tests. Cuentas no detienen Strategy; pools/rotación/afinidad/presupuesto quedan como estaban.
9. No relajar freshness, reducir dedup, saltar offsets, aumentar timeout ni sampling oculto para dar PASS.
10. Compatibilidad MT4/MT5 aditiva. SnapshotIntervalMs legacy exige >=100ms; NO reutilizarlo como flush50ms.

## /scope

Allowlist de superficies en diseño §10. T1.1 fija archivos/símbolos y un writer por path, incluyendo contratos compartidos antes de delegarlos. Nombres nuevos sólo junto a propietarios existentes.

Sin servicios/bus/DSL nuevos, fork SDK, sharding de un stream, refactor masivo MT, cambio de infraestructura o despliegue. No tocar credenciales/seeds/ETCD/Kafka compartidos, terminal del Owner ni cuentas SIM/reales. Tests locales deben demostrar aislamiento antes de correr.

La verificación C# puede usar assemblies instaladas de sólo lectura y un staging/perfil aislado. No instalar el AddOn ni reiniciar Ninja del Owner.

## /execute

### Preflight y contratos — submanager, T1.1

Mapear source real: SendUnifiedBatch/MessageQueue, ClientConfig, negociación, productor Kafka, market_stream, AddOn y rutas. Reutilizar nombres/protocolos equivalentes. Congelar mapeo y ownership en el diseño por delta, no otra SPEC.

Inspeccionar SDK Go v3.3.0 para conocer la frontera real de estado/request. No inventar hooks. Camino obligatorio mínimo: lote de feed de una key preservado hasta Invoke, cargar una vez, aplicar todos secuencialmente, sellar efectos y guardar estado una vez antes de éxito. Sólo ampliar coalescencia a la request completa si un punto soportado lo permite y está probado. Sin fork. Si aún no alcanza capacidad, se autoriza representación compacta/versionada del mismo sequencer con compatibilidad/rollback, nunca menor ventana ni datos descartados.

### Delegación obligatoria

W1 CORE: T1.2. Batch, persistencia/serde, retry/restore, equivalencia y capacidad. No cliente/config compartida.
W2 CLIENTE: T1.3–T1.4. Contratos comunes/config, capabilities C#, colas/sender/outbox, ticks ALL/LAST y barras nativas/cobertura/backfill. Congelar schema antes de W3.
W3 BRIDGE: T1.5. Transporte/routing Kafka, ACK durable y orden, compatibilidad legacy/M2. Sin negocio ni filtros de datos.
W4 INTEGRACIÓN: T1.6–T1.7. Wiring/manifiestos source, analytics, E2E, compilación NT aislada, pruebas de fallo y carga. No redefine contratos.

Máximo dos workers simultáneos únicamente con paths y worktrees aislados; de lo contrario secuencial. W1/W2 pueden correr en paralelo. W3 consume contrato W2. W4 sólo tras W1–W3 revisados e integrados. Workers no subdelegan.

Cada prompt one-shot incluye tarea, SHA, archivos permitidos/prohibidos, D/AC aplicables, implementación, pruebas negativas, evidencia, cierre/feedback y STOP. No liberar al worker con un «hazlo como veas».

Submanager revisa diff, ejecuta/contrasta pruebas, registra DESPACHADO→RECIBIDO→REVISADO→INTEGRADO|RECHAZADO|BLOCKED y devuelve fallos al owner del código. Nunca aceptar por el resumen PASS del worker. Si no hay subagentes reales, SUBAGENTS_UNAVAILABLE y STOP, no implementación solitaria ficticia.

### Implementación: puntos que no pueden omitirse

- Lote50ms con límite de bytes/eventos; no sleep por evento; respetar seq al vaciar colas.
- Outbox limitada y durable antes del envío, ACK de publicación confirmada, retry byte-idéntico y dedup. No copiar al hot path el WriteAll de MT ni su límite64.
- Barras nativas con calendario/timeframe/revisión/coverage; missing history no se rellena ni se proclama completa.
- LAST por clase/ventana, original timestamps y omission metadata; ningún consumidor incompatible se degrada silenciosamente.
- Cliente NT como adaptador del patrón Execution existente; una clase instalada, configuración/negociación común, no otro catálogo o bridge.
- Preservar batch de feed hasta Core; un test que lo rompe en invocaciones costosas por item no cumple.
- Reutilizar los módulos de ejecución Futures: no reescribir o retirar M2.
- Usuario no debe inventar IDs, puertos o resolver cómo compilar dos copias: preparar documentación exacta de actualización in-place y rollback para certificación posterior.

## /verify

Completar AC01–AC16 y registrar resultados verdaderos sobre SHA exacto. Fixtures/oráculos independientes, rojo→verde donde aplique, tests permanentes por owner.

Pruebas indispensables: mezcla/orden de capabilities; batch1/2/50/1001 equivalente; crash/retry/restore en otra instancia; effects sin alias; Kafka parcial y ACK perdido; buffer lleno; hueco/barra corregida; LAST en borde temporal sin confundir QUOTE/TRADE; legacy min100 intacto; wrong account/epoch/fence; tipo/topic/target ausente hace FALLAR E2E.

Rendimiento con estado maduro, ALL, flush50ms real, productor open-loop independiente, captura1×/2× y ráfagas: medir records/batches/items, latency, lag y edad, CPU/GC/bytes serde. Recuperar backlog mientras siguen llegando eventos, sin salto al HWM. Incluir legado singleton pendiente, no sólo lotes recién vacíos. >=30min aislados para el candidato final; runtime Java/checkpoints aislados cuando disponibles. In-proc no certifica infraestructura ni terminal reales.

Cobertura >=95% del código nuevo después de cubrir comportamiento crítico. Race y regresiones baseline por nombre/causa, no contador agregado. Si S1 está incompleto no enviar la deuda a S3.

Compile del conjunto C# en staging/perfil aislado contra assemblies reales cuando accesibles. PHYSICAL_NOT_DEMONSTRATED donde falten pruebas; no inventar LIVE ni modificar una instalación compartida para llenar casillas.

## /reuse

Conservar harness/RequestReplyHandler y contratos existentes. Clasificar assets nuevos como regresión permanente, E2E candidato, testkit candidato o repro descartable. Hashes y scripts durables; no dejar evidencia sólo en /tmp ni otra implementación Live/Backtest.

## /improve

Defensas ejecutables para los fallos históricos: mismo contrato de batch no equivale a ACK durable, source que compila no equivale al perfil instalado, registro Kafka no equivale a items procesados, no-timeout no equivale a tiempo real. Registrar fricciones reales, sin inventar métricas o feedback.

## /close

Publicar commits atribuibles en feature/ef-runtime-pools sin merge/force; comprobar remoto y worktree. Mantener la matriz/evidencia en este planificador y docs relacionadas, no ocho planners.

Agents-OS directo a master, validar/readback. Cada worker y el submanager ejecutan agent-run, session-close y feedback autorizados para su propio contexto. No cerrar al Primary Manager ni el proyecto global.

G1 termina review o blocked. Nadie autoacepta. No iniciar S2 ni desplegar/armar ejecución.

## /output

STATUS: FEFB_S01_READY_FOR_MANAGER_REVIEW | FEFB_S01_BLOCKED
BASE_SHA / FINAL_SHA / REMOTE_VERIFIED:
WORKERS_W1_W4: estado, commits, tests y límites
CORE_BATCH_AND_DURABILITY:
CLIENT_CAPABILITIES_AND_BARS:
TICK_MODES:
BRIDGE_AND_LEGACY:
AC01_AC16: passed / failed / not_run
PERFORMANCE_AND_BACKLOG:
COVERAGE / RACE / BASELINE_REGRESSIONS:
NT_COMPILE / PHYSICAL_LIMITATIONS:
KNOWN_DEFECTS / BLOCKERS:
AGENTS_OS_READBACK:
G1: review | blocked
SESSION_CLOSE / FEEDBACK:
STOP: S2 NO INICIADO; SIN MERGE NI DEPLOY.

Máximo 500 palabras finales; detalle verificable en el planner.
por favor gracias
```

## Límites

Sin modificación automática de runtime compartido, sin trading, sin cambios en backtester, sin otro planner ni quinto shot implícito. El texto del prompt es un despacho ejecutable por un agente LOCAL; no afirma que estas capacidades hayan sido implementadas por la sesión CLOUD que lo creó.
