# MANDATO MAESTRO — ASTRA-1

## Polymarket Engine — MVP · Diseño arquitectónico integral

### ROL

Actúa como **Principal Software Architect**, especializado en Go, sistemas de trading, protocolos financieros, procesamiento de eventos y sistemas resilientes.

Tu misión es diseñar integralmente el **Polymarket Engine MVP** utilizando exclusivamente el conocimiento técnico y las decisiones ya documentadas en Agents-OS.

Este es el primer shot de ASTRA para M1.

**No implementes código. No generes documentos nuevos. No hagas Deep Research. No explores otros proyectos del vault.**

El resultado debe quedar escrito y publicado directamente en el archivo raíz del proyecto, preparado para que FABLE realice una revisión adversarial.

---

# 0. OBJETIVO DEL SHOT

Producir una propuesta arquitectónica completa, consistente y suficientemente precisa para que:

1. El owner y manager puedan revisarla.
    
2. FABLE pueda cuestionarla sin reconstruir el razonamiento.
    
3. ASTRA pueda reconciliar posteriormente los findings.
    
4. Un agente TOP pueda convertir el diseño congelado en un plan de implementación ejecutable.
    

No hagas el trabajo de TOP todavía.

No declares `DESIGN_FROZEN`.

Tu resultado debe ser:

`M1 — ASTRA PROPOSAL — READY FOR FABLE`

---

# 1. REPOSITORIO Y AUTORIDADES

Repositorio:

`xKoRx/agents-os`

Branch:

`master`

## Único archivo de salida

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

URL:

[10-projects/Personal/Polymarket%20Engine/Polymarket%20Engine%20%E2%80%94%20MVP.md](10-projects/Personal/Polymarket%20Engine/Polymarket%20Engine%20%E2%80%94%20MVP.md)

Debes modificar este archivo directamente.

No crear:

- ADRs;
    
- SPECs independientes;
    
- documentos de arquitectura;
    
- planes de implementación;
    
- diagramas en archivos separados;
    
- notas de research;
    
- handoffs adicionales.
    

El proyecto es la única autoridad operativa.

## Fuentes de entrada autorizadas

### A. Proyecto

El archivo raíz anterior.

Lee sus decisiones, objetivos, restricciones, capabilities, fases, gates y flujo de agentes.

### B. Technical Platform Map

Índice canónico:

`main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`

Contiene once partes enlazadas.

**Debes leer las once partes.**

El índice es el manifiesto; los contratos están en los archivos enlazados.

Prioriza especialmente:

- entidades e identificadores;
    
- REST;
    
- WebSockets;
    
- autenticación;
    
- órdenes;
    
- market data;
    
- posiciones;
    
- NegRisk;
    
- fees;
    
- resolución;
    
- históricos;
    
- recovery;
    
- Research Gaps;
    
- fuentes y versiones.
    

### C. Edge Research Consolidado

`main/30-resources/polymarket/Polymarket — Edge Research Consolidado 2026-09-16.md`

Úsalo exclusivamente para comprender los requerimientos transversales que podrían necesitar las distintas hipótesis.

No diseñes ni implementes ninguna estrategia particular.

No necesitas leer las cuatro investigaciones originales.

## Límite estricto de contexto

Estas tres fuentes constituyen el `CONTEXT PACK` completo.

No recorras otras carpetas del vault.

No busques memorias antiguas, proyectos Echo, Echo Forge, Hermes ni documentos relacionados.

No investigues documentación oficial de Polymarket en Internet.

No abras repositorios SDK ni contratos externos.

Si Agents-OS exige bootstrap, ejecuta únicamente el mínimo obligatorio para respetar sus reglas de operación. Ese bootstrap no autoriza ampliar el contexto técnico a otros proyectos.

Si encuentras información insuficiente, regístrala como incertidumbre o decisión pendiente. No inicies una investigación externa.

---

# 2. BASELINE FROZEN

Estamos construyendo:

**Polymarket Engine — MVP**

No es una POC.

Es un producto durable que debe soportar sucesivas estrategias sin reconstruir infraestructura.

Restricciones:

```text
Language:          Go
Architecture:      Modular monolith
Deployment:        Single deployable
Infrastructure:    Single large host
Venue:             Polymarket-specific
Strategy layer:    Strategy-agnostic
Hot path:          No LLM
```

No introducir:

```text
Kafka
Flink
Kubernetes
Microservices
Multi-venue framework
Distributed architecture
Complex UI
Premature HFT infrastructure
```

Salvo que encuentres una contradicción técnica demostrable, conserva estas decisiones.

La prioridad arquitectónica es:

**un engine robusto que reduzca el tiempo y el costo de validar una nueva hipótesis.**

North star:

`TIME_TO_VALIDATED_HYPOTHESIS`

---

# 3. DISTINCIÓN FUNDAMENTAL

El engine es un MVP durable.

Las estrategias son POCs descartables.

Primeros consumidores:

```text
POC-S01: NegRisk
POC-S02: Sports
```

Después vendrán otras hipótesis.

El engine debe proporcionar capabilities comunes.

Una estrategia debe implementar exclusivamente su lógica diferenciadora.

Una estrategia NO debe necesitar su propio:

```text
Market discovery
WebSocket manager
Canonical order book
Recorder
Replay engine
Wallet manager
Order manager
Risk engine
Shadow execution
Reconciliation
Observability
```

Esto no implica construir abstracciones especulativas para treinta estrategias.

**Diseña el contrato compartido a partir de capabilities fundamentales y dos consumidores iniciales reales.**

No implementes Sports ni NegRisk.

---

# 4. GATES CONTRACTUALES DE M0

El Technical Platform Map está aprobado para diseño, pero NO certifica todas las operaciones live.

Debes respetar sus límites.

Especialmente:

- No existe garantía documentada de secuencia global o replay completo de Market WS.
    
- No existe certificación de backfill histórico L2 completo.
    
- El recorder propio es obligatorio para datos que requieran replay reproducible.
    
- NegRisk CTF y Protocol-v2 deben diferenciarse.
    
- Ninguna conversión NegRisk está autorizada para live.
    
- La ABI de conversión NegRisk v2 no está verificada.
    
- Auth y ejecución live requieren validación de integración.
    
- `deferExec=true` permanece deshabilitado.
    
- Builder optional modes permanecen deshabilitados.
    
- Combos/RFQ están fuera del MVP inicial.
    

No rellenes gaps inventando contratos.

Diseña mecanismos fail-closed y gates de activación posteriores.

Distingue claramente:

```text
SUPPORTED FOR DESIGN
IMPLEMENTABLE FROM DOCUMENTED CONTRACT
REQUIRES INTEGRATION VALIDATION
DISABLED
OUT_OF_SCOPE
```

Una capability deshabilitada no debe convertirse accidentalmente en una ruta ejecutable.

---

# 5. DISEÑO REQUERIDO

Tu propuesta debe cubrir las siguientes áreas.

## A. Arquitectura general

Define:

- módulos internos;
    
- responsabilidades;
    
- dependencias permitidas;
    
- ownership de estado;
    
- flujos principales;
    
- boundaries;
    
- inicialización;
    
- shutdown;
    
- separación hot path / cold path.
    

Entrega un mapa arquitectónico concreto.

No basta con una lista de paquetes.

Justifica cómo evitarás que el monolito se convierta en un conjunto de módulos altamente acoplados.

## B. Modelo de dominio

Diseña los modelos internos canónicos:

```text
Event
Market
Outcome
Asset / Token / Position
Condition
Market relationship
Order
Fill / Trade
Position
Resolution
Fee configuration
Opportunity
Strategy
Experiment
```

Usa los identificadores y relaciones documentados.

No confundas Gamma market ID, condition ID, token ID, asset ID ni order ID.

Distingue entidad mutable, snapshot inmutable, dato derivado y evento observado.

Define la representación numérica apropiada en Go, evitando pérdida de precisión monetaria.

## C. Market discovery y lifecycle

Diseña:

- discovery inicial;
    
- paginación;
    
- actualización de metadata;
    
- detección de mercados nuevos;
    
- relación Event/Market/Token;
    
- reglas y resolution source;
    
- cambios de tick, estado y fees;
    
- invalidación de datos obsoletos.
    

Incluye el mecanismo por el que una estrategia obtiene su universo sin replicar discovery.

## D. Market data y books

Diseña:

- clientes REST/WS;
    
- modelo de conexiones y subscriptions;
    
- snapshots;
    
- aplicación de actualizaciones;
    
- canonical books;
    
- timestamps;
    
- detección de staleness;
    
- reconnect;
    
- resubscribe;
    
- recuperación después de gaps;
    
- backpressure.
    

No asumas garantías inexistentes de ordenamiento.

Explica cómo evitarás producir oportunidades sobre books inconsistentes.

Define la transición entre snapshot REST y WS considerando que Polymarket no garantiza una barrera atómica entre ambas superficies.

## E. Recorder y replay

Ésta es una capability fundamental.

Diseña:

- captura de evidencia raw;
    
- persistencia;
    
- orden de recepción;
    
- timestamps de origen y recepción;
    
- metadata y versiones;
    
- integridad;
    
- retención;
    
- replay determinista del stream efectivamente capturado;
    
- límites de reproducibilidad;
    
- reproducibilidad de experimentos.
    

Distingue:

**replay determinista de nuestra captura**

versus

**reconstrucción histórica completa del mercado**.

No prometas la segunda sin evidencia.

Define política para pérdida de datos, discontinuidades, crashes y recuperación.

## F. Persistencia y datasets

Elige y justifica:

- almacenamiento transaccional;
    
- almacenamiento de eventos raw;
    
- datasets derivados;
    
- índices;
    
- políticas de retención;
    
- migraciones;
    
- backups;
    
- recuperación.
    

Considera inicialmente una sola máquina con CPU, RAM y NVMe suficientes.

Evita introducir una plataforma distribuida por anticipación.

No conviertas el motor de almacenamiento en una decisión irreversible sin explicar tradeoffs.

## G. Strategy runtime

Diseña el contrato exacto que implementará una estrategia Go.

Debe cubrir:

- identity;
    
- universe;
    
- required data;
    
- lifecycle;
    
- snapshot/event delivery;
    
- opportunity detection;
    
- evaluation;
    
- resultados;
    
- métricas;
    
- errores;
    
- cancelación;
    
- aislamiento.
    

Incluye interfaces Go propuestas cuando aclaren el contrato.

Son interfaces de diseño, no código productivo.

Una estrategia no debe tener acceso implícito a credenciales ni permisos de trading.

Define cómo el mismo módulo corre en:

```text
SCREEN
REPLAY
SHADOW
LIVE
```

sin duplicar lógica de estrategia.

## H. Hypothesis y experiment framework

Diseña:

- registry de hipótesis;
    
- cheap triage;
    
- experimento reproducible;
    
- parámetros;
    
- versiones de datos;
    
- scorecards;
    
- costos;
    
- calidad de señal;
    
- simulación de fills;
    
- modelos optimistic/base/stress;
    
- criterios GO/ITERATE/NO_GO.
    

No codifiques thresholds económicos arbitrarios como verdades universales.

## I. Economics, capital y risk

Diseña:

- effective fees dinámicas;
    
- rebates/rewards;
    
- profundidad ejecutable;
    
- VWAP;
    
- capital requerido;
    
- capital bloqueado;
    
- sizing;
    
- exposición;
    
- bankroll compartido;
    
- límites por mercado/evento/estrategia;
    
- kill switch.
    

El bankroll tiny-live previsto es US$300, pero el MVP del engine no requiere arriesgar ese capital para considerarse exitoso.

No asumas arbitraje sin riesgo por desigualdades matemáticas entre precios.

## J. Execution y reconciliation

Diseña aunque su activación live quede sujeta a certificación:

- boundary de credenciales;
    
- order construction;
    
- signing;
    
- envío;
    
- acknowledgements;
    
- fills;
    
- cancel;
    
- timeouts ambiguos;
    
- deduplicación;
    
- idempotencia cuando esté documentada;
    
- conciliación REST/WS/chain;
    
- posiciones;
    
- recovery after crash;
    
- kill switch.
    

Define qué ocurre cuando el proceso muere con órdenes abiertas.

No permitas blind retries ante writes ambiguos.

Separa shadow, live-disabled y live-enabled mediante un control que no dependa de un simple booleano disperso.

## K. NegRisk y protocolo versionado

Diseña el modelo necesario para soportar CTF y Protocol-v2 sin equiparar sus IDs ni sus operaciones.

Conserva explícitamente deshabilitada la conversión live no certificada.

El diseño debe permitir incorporar posteriormente la ABI y certificación sin reescribir el dominio completo.

No implementes una abstracción universal de smart contracts.

## L. Concurrencia y rendimiento

Define:

- goroutines y ownership;
    
- queues/channels;
    
- bounded buffers;
    
- backpressure;
    
- particionamiento de books;
    
- orden por asset;
    
- locks;
    
- cancelación;
    
- shutdown;
    
- separación de recorder/replay/hot path;
    
- políticas cuando una estrategia lenta bloquea.
    

Propón límites configurables y mecanismos de medición.

No inventes objetivos de latencia como si fueran requisitos del negocio.

## M. Observabilidad y operación

Diseña:

- métricas;
    
- logs estructurados;
    
- tracing;
    
- health/readiness;
    
- alertas;
    
- errores;
    
- lag;
    
- WS reconnects;
    
- discrepancias de books;
    
- pérdidas del recorder;
    
- reconciliación;
    
- estado de estrategias;
    
- uso de recursos.
    

Debe poder distinguirse:

```text
NO EDGE
BAD DATA
BAD FILL MODEL
SYSTEM FAILURE
EXECUTION FAILURE
```

## N. Seguridad

Diseña:

- gestión de secrets;
    
- aislamiento read-only;
    
- permisos de estrategias;
    
- wallet/signing boundary;
    
- habilitación de live;
    
- scopes;
    
- configuración;
    
- protección ante errores operativos.
    

No asumas que un SDK resuelve automáticamente seguridad o autorización.

## O. Testing y certificación

Define gates verificables para:

- unit tests;
    
- property tests;
    
- integration/contract tests;
    
- fixtures;
    
- replay;
    
- fault injection;
    
- reconnection;
    
- recovery;
    
- shadow;
    
- auth/order integration;
    
- live activation.
    

Cada gate debe tener condición observable de PASS/FAIL.

No declares aprobado un gate que todavía no se ha ejecutado.

---

# 6. DECISIONES ARQUITECTÓNICAS

Toda decisión material debe quedar en una tabla:

| ID | Decisión propuesta | Alternativas | Rationale | Tradeoff | Riesgo | Estado |

Usa estados:

```text
PROPOSED
REQUIRES_OWNER
BLOCKED_BY_PROTOCOL
```

Las decisiones macro frozen del proyecto no deben reabrirse sin una contradicción demostrada.

No conviertas todas las decisiones propuestas en `FROZEN`.

FABLE todavía debe challengearlas y el owner debe aprobarlas.

---

# 7. CONTROL DE COMPLETITUD

Antes de publicar, realiza una revisión interna:

1. ¿Todas las capabilities del MVP tienen un módulo responsable?
    
2. ¿Los límites entre módulos son explícitos?
    
3. ¿Los datos tienen un único owner?
    
4. ¿El recorder puede sobrevivir a fallos?
    
5. ¿El replay tiene límites honestos?
    
6. ¿Un book inconsistente bloquea decisiones?
    
7. ¿Una estrategia lenta puede bloquear el engine?
    
8. ¿Una estrategia puede ejecutar órdenes sin autorización?
    
9. ¿Un timeout ambiguo puede duplicar órdenes?
    
10. ¿Los modos deshabilitados son realmente fail-closed?
    
11. ¿Sports y NegRisk pueden consumir el engine sin deformarlo?
    
12. ¿TOP tendrá suficiente definición para planificar sin inventar arquitectura?
    

Si falta una respuesta, corrige tu diseño antes de publicar.

Cuando haya incertidumbre genuina, registra la decisión pendiente y propone un mecanismo seguro.

No suplas información ausente con afirmaciones inventadas.

---

# 8. FORMATO DEL ENTREGABLE

Modifica exclusivamente:

`Polymarket Engine — MVP.md`

Preserva el contenido vigente y las decisiones frozen.

Añade o actualiza una sección:

`## M1 — ASTRA Architecture Proposal`

Organiza allí toda la propuesta.

Evita repetir literalmente el Technical Platform Map.

Referencia sus secciones cuando fundamenten una decisión.

Prioriza tablas, diagramas textuales e interfaces concretas frente a narrativa extensa.

**El resultado debe ser detallado, pero no una copia de las 287 KB del resource pack.**

No dupliques el mismo diseño en otros lugares del archivo.

No actualices M0 ni alteres sus gates.

No edites los once archivos del Technical Platform Map.

No modifiques otros proyectos.

No generes código productivo.

---

# 9. PERSISTENCIA EN GITHUB

Antes de editar:

1. Verifica branch `master`.
    
2. Recupera el HEAD vigente.
    
3. Comprueba cambios concurrentes.
    
4. Lee el archivo raíz completo.
    
5. Lee el context pack autorizado.
    

Publica los cambios en GitHub siguiendo el workflow permitido.

No hagas force push.

Verifica que el commit esté realmente presente en `master`.

Si encuentras cambios concurrentes, reconcilia sin sobrescribirlos.

No declares publicación exitosa antes de verificarla.

Estado final:

`M1_ASTRA_PROPOSAL_READY_FOR_FABLE`

No:

`M1_DESIGN_FROZEN`

---

# 10. RESPUESTA POR CHAT

NO entregues el diseño por chat.

NO generes otro documento.

NO pegues interfaces extensas ni diagramas completos en la respuesta.

Responde sólo con:

```text
STATUS: M1_ASTRA_PROPOSAL_READY_FOR_FABLE | PARTIAL | BLOCKED

GITHUB:
- commit SHA
- enlace al proyecto actualizado

DESIGN:
- principales decisiones propuestas
- decisiones que requieren aprobación del owner
- incertidumbres técnicas abiertas
- capabilities que permanecen deshabilitadas

FABLE HANDOFF:
- principales puntos que deben cuestionarse

NEXT:
- FABLE adversarial challenge
```

---

# 11. INSTRUCCIÓN FINAL

Diseña ahora el Polymarket Engine MVP.

Usa exclusivamente el context pack autorizado.

No investigues nuevamente Polymarket.

No explores el vault.

No implementes.

No planifiques tareas de coding todavía.

**Publica una propuesta arquitectónica integral y auditable en el archivo raíz del proyecto. Déjala preparada para el challenge de FABLE y nuestra revisión conjunta.**