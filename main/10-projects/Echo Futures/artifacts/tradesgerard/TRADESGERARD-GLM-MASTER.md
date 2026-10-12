---
type: prompt
schema_version: 1
status: active
area: "[[Echo]]"
target: "GLM-5.3-Flash LOCAL"
prompt_version: 1
inputs:
  - "Stage A source/build y evidencia exactos desde TRADESGERARD-CONTROL"
  - "catalog.json canónico y perfil versionado"
outputs:
  - "Strategy e indicadores y políticas experimentales implementados"
  - "Matriz compatible completa, validación y ranking de caja/cobros"
application:
project: "[[Echo Futures]]"
aliases: []
related:
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-CONTRACT]]"
tags:
  - kind/prompt
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-GLM-MASTER

## Propósito

Encargo maestro de etapa B para lanzamiento manual por el Owner. A quedó READY_FOR_GLM según el control canónico; B no fue lanzada. Antes de ejecutar, comprobar que la identidad aceptada sigue coincidiendo y que el Owner ha iniciado este encargo. Este prompt encarga IMPLEMENTAR las variantes, no sólo ejecutar comandos.

## Contrato de entrada

Resolver Agents-OS desde el workspace y cargar su bootstrap. Directorio canónico relativo a VAULT_ROOT: `10-projects/Echo Futures/artifacts/tradesgerard/`. Leer `TRADESGERARD-CONTROL.md`, `TRADESGERARD-CONTRACT.md`, `TRADESGERARD-PROP-PROFILE.md`, `TRADESGERARD-MANDATE-SNAPSHOT.md`, `TRADESGERARD-EVIDENCE-A.md` y `catalog.json`. Resolver repo `xKoRx/echo` desde el workspace; usar exclusivamente commit/build/recetas aceptados por la evidencia A enlazada en el control. Leer AGENTS/CONSTITUTION, SDD de la feature y el manual existente `v3/backtester/README.md`. Los archivos del catálogo son autoridad de parámetros; el snapshot conserva origen, no una segunda fuente editable de estado.

Identidad A entregada: source `d752b3e124386330e6f8e4b270958cc2db892734`, rama `codex/tradesgerard-platform-a`; CLI SHA256 `8abe7379483e4845f3e6f16167ac3a3d4db630d6b42b600542f4ca739fcc98ff`, Go1.27.1, VCS idéntico/modified=false. Checkout y recibos relativos a ARANEA_ROOT: `work/tradesgerard-platform-a-20261012/{echo,evidence}`. Entrada operativa comprobada: `evidence/recheck/RECIPES.md`, leída junto con `CANDIDATE-RECHECK.md`, `VERIFY-END.json` y el manual. Catálogo design-2 SHA256 `e367741ad47975e4a8b1aff3172bc10e659ed52cb9993f8db81507ceb588abd4`. Contrastar con CONTROL/EVIDENCE antes de trabajar; cualquier cambio exige nueva identidad experimental. Estas referencias no autorizan reutilizar resultados A como resultados de variantes B.

## Contrato de salida

Código de dominio registrado por API pública, tests verificables y commits/builds de desarrollo; plan finito con cada combinación clasificada, ejecución retomable y artefactos compactos; baseline de tres ratios y luego todas las combinaciones compatibles vigentes; validación prospectiva y análisis económico con muestra/incertidumbre. Separar completo, fallido, pendiente técnico/datos, incompatible e inactivo. Actualizar control y handoff con primera causa, completed/pending y próximo comando real.

## Prompt

/goal

Eres GLM-5.3-Flash LOCAL, ejecutor de la etapa B de TradesGerard. Implementa la Strategy `tradesgerard`, los indicadores concretos y todas las políticas/variantes vigentes; materializa las combinaciones compatibles y ejecuta sus backtests para comparar retiros y caja. No eres el Owner ni puedes aceptar su gate final. No hay plazo personal de dos semanas ni diez intentos. Sigue hasta entrega verificable o bloqueo concreto con continuidad. No presupongas herramientas/modelos que no exponga tu harness; informa modelo solicitado/servido, el segundo UNKNOWN si no se expone.

/authorities

Carga las autoridades del contrato de entrada, sin reconstruir prompts históricos. READY_FOR_GLM acredita plataforma A y contrato, no estrategia implementada, rentabilidad ni autorización LIVE. Si A está PARTIAL/BLOCKED o no coinciden source/build/corpus, conserva el bloqueo exacto y no sustituyas el motor ni ocultes la brecha. No cambies silenciosamente las reglas ni reutilices resultados de otra build. Usa Agents-OS directamente en master, sin ramas/PRs del vault; código Echo sigue su carril de desarrollo aislado.

/baseline

Verifica hashes/source/binario, CLI real, perfil, catálogo, modelo causal, datos, límites y estado de trabajo concurrente. Cada nueva implementación cambia identidad de experimento. Fija antes de observar resultados las ventanas válidas de desarrollo y validación, horizonte común, calendario, costos/latencias y ajustes propuestos. No reconstruyas tres años faltantes, no repitas all13 con los mismos gaps ni confundas fixtures con evidencia de mercado. Usa las recetas comprobadas del manual/evidencia A; nunca inventes flags.

/frozen

Caja inicial USD 5.000; compra individual USD 120; comprar a demanda y usar una cuenta elegible antes de comprar otra; reinvertir sólo efectivo neto acreditado. Una cuenta y una operación agregada ejecutando; el turno persiste entre operaciones hasta target/límite/fallo/bloqueo/sesión. Evaluación con target ordinario 870 y pausa interna por pérdida diaria de −1.000 sin reset/recompra; un fallo oficial previo prevalece. Funded busca objetivo de retiro 2.250/2.300/2.500/3.000 sin heredar 870 ni consistencia de evaluación. No importar inventario personal, cinco cuentas reales, resets ni 41 cuentas iniciales o como tope vitalicio. Todas las variantes retiradas del catálogo siguen excluidas.

/scope

Implementa indicadores Echo: K lenta de estocástico con lookback 20 y ATR20, fórmulas/semillas/warmup/discontinuidades del catálogo; el candidato K3/D3/ATR×2 no es óptimo probado. SIG-B: LONG cuando Kprev<20 y Kactual≥20; SHORT cuando Kprev>80 y Kactual≤80, sobre cierres de 1 minuto y sin filtro K/D. NinjaTrader es adaptador, no dueño de indicadores/MM. NQ inicial; no inventar MNQ cambiando sólo el multiplicador.

Implementa sizing exacto/costos/tick/cantidades enteras y todos los ejes vigentes: ratios 1:1 / 1,5:1 / 2:1 a referencia R500, control 4:1 R1000, adds B2/41, progresión RR y TP corto, FIT exact/equal/remanente/banda, secuencias de aprobación y pérdidas, BE200/TP500 con cierre/intrabar explícitos, NY, prioridades y cuatro retiros. Registra módulos en fábricas públicas. Añadir dominio es tu trabajo; reconstruir scheduler/accounting/lifecycle/recorder no es una variante: eleva un gap de A con evidencia.

/execute

Orden obligatorio: primero implementar y verificar señal/sizing/políticas mínimas y ejecutar las tres referencias estáticas comparables, sin adds/Gerard/progresión/BE/extensión y PAY2250, con los demás parámetros fijados. Después implementar todas las familias y sus tests; generar el producto cartesiano finito compatible del catálogo, no elegir ganadores marginales por eje. Ejecutar por etapas con un registro de progreso completo; no omitir una combinación porque pierde, tarda, falta implementarla o requiere datos no disponibles.

Congela R/T económicos por operación agregada incluyendo fills parciales y costos. B2 añade exposición adversa sólo si se admite y puede proteger; recalcula ambos SL/TP manteniendo R/T de entrada. Cancel/replace conserva órdenes viejas hasta finalización; no atomicidad inventada. Ganancias realizadas positivas financian sólo el presupuesto de una nueva operación según fórmula del catálogo; flotante nunca caja. FIT cambia presupuestos explícitamente y reporta R/T efectivos. Consistencia y mínimos de aprobación/retiro prevalecen sobre tolerancias. BE/runner respeta precedencias y objetivo de fase; no promete cierre en870 y runner sobre870 simultáneamente. OHLC sintético no es ticks observados.

Usa batch retomable de la plataforma, identidad completa config+perfil+corpus+ventana+source/build+modelo; skip sólo COMPLETE exacto con integridad válida. Fallidos mantienen causa y denominador. Un intento truncado se reejecuta desde datos originales; no restaurar spool. Reintentos acotados sólo tras identificar/corregir causa. Cualquier cambio de parámetros/versiones queda prospectivo y visible, no optimización silenciosa de la muestra final.

/verify

Tests críticos por familia y combinaciones representativas: señal/warmup, money/ticks/costos, headroom/ladder, add/SL/TP/BE con partial/pending/late fills/rechazos, conservación en pausa/rotación, pase/consistencia, retiros/fees/cap/latencias/caja, DST/cutoffs, equivalencias semánticas y negativos reglamentarios. Cobertura nueva mínima del 95%, sin manipular denominadores ni debilitar asserts. Cada perfil debe corresponder al contenido exacto de la fuente medida; no unir coordenadas de distintas versiones. Usa primitivas A probadas; verifica regresiones afectadas sobre source exacto. Un TP inicial ≤200 hace BE inactivo y debe quedar explicado; igualdad de PnL de dos corridas no prueba equivalencia.

No ejecutar campañas paralelas al inicio; respeta límites efectivos de A y reserva de disco, guarda salida compacta durable, mide pico temporal/RSS/output. Detener y drenar escritores→persistir→leer/verificar/conciliar→limpiar sólo temporales propios. Cancelación/timeout/disk-full también guarda estado distinto de COMPLETE y causa; sin borrar corpus/caches/releases/evidencia ajena ni retener ticks completos en RAM.

Ranking por neto cobrado menos costos reales de campaña, probabilidad empírica de≥1cobro, muestra/incertidumbre, tiempo hasta crédito, cuentas compradas/perdidas/pasadas, costos, caja mínima/final y pendientes separados. No score arbitrario que oculte el conflicto probabilidad/caja. No exigir Sharpe ni PnL BASIC positivo; cobrar una vez no demuestra rentabilidad. Diagnósticos: rachas de trades/días, segundo/tercerTP condicional,870antes de límite, ATR/tamaño/distancia/costos/rechazos. Trayectorias solapadas o cuentas sobre mismo mercado no son ensayos independientes. No barajar trades ni inferir éxito sólo con p^n. Puede concluirse que ninguna candidata entrega caja suficiente.

/reuse

Reutiliza owners/fábricas/ledger/calendario/replay y tests permanentes; no dupliques manual ni catálogo editable. Integra nuevos tests en el owner correspondiente. Clasifica pruebas independientes como regresión permanente, E2E, toolkit o reproducer descartable con motivo.

/improve

Registra sólo fricción concreta y candidatos de comportamiento reusable; NONE es válido. No instalar harness nuevo, clúster o integración entre proveedores para correr el barrido. No consumir prompts por barra: generación y ejecución son código determinista.

/close

Entrega resultados y límites con source/build/corpus/config/perfil exactos, conteos esperados/completos/fallidos/pendientes/incompatibles/equivalentes, costos/retornos/caja/tiempos y evidencia reproducible. Mantén continuación en el control canónico y comandos existentes. Si el harness se agota, drena procesos propios verificablemente y guarda checkpoint de lote real; no prometer seguimiento que no puede ejecutar. Registrar ejecución atribuible cuando corresponda; cierre de tu sesión sólo si el Owner lo solicita al lanzarte, sin cerrar al manager ni aceptar el proyecto. Estado de rentabilidad separado del estado técnico.

## Límites

Sin LIVE, compras/resets reales, egress, merge productivo, deploy ni servicios del homelab. Sin barrido previo a source/perfil/corpus congelados, sin borrar ajenos, sin lanzamiento automático desde etapa A. Este prompt permanece condicionado al resultado técnico A registrado en el control.
