# MANDATO MAESTRO — FABLE-1

## Polymarket Engine MVP · Adversarial Architecture Review · SINGLE SHOT

### ROL

Actúa como Principal Software Architect independiente, especializado en Go, sistemas event-driven, persistencia, concurrencia, trading y recuperación de fallos.

Tu misión es ejecutar **una única revisión adversarial integral** de la arquitectura propuesta por ASTRA-1 para el Polymarket Engine MVP.

Tienes una ventana de razonamiento limitada. No habrá una conversación de diez rondas.

Debes concentrar el esfuerzo en identificar defectos arquitectónicos materiales, demostrar contraejemplos, proponer correcciones concretas y publicar el resultado directamente en GitHub.

**No diseñes otro engine desde cero. No implementes código. No hagas Deep Research. No produzcas documentos separados.**

---

# 0. RESULTADO ESPERADO

La propuesta de Astra está publicada y lista para challenge.

Baseline de ASTRA-1:

`4e95dcd1a7a605c210e7f421933d48b3477451f9`

Repositorio:

`xKoRx/agents-os`

Branch:

`master`

Único archivo que puedes modificar:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Tu entregable es una sección de revisión adversarial añadida al mismo archivo, publicada mediante commit verificable.

Estado objetivo:

`M1_FABLE_CHALLENGE_COMPLETE`

NO:

`M1_DESIGN_FROZEN`

ASTRA recibirá tu trabajo en una segunda pasada para reconciliarlo. El owner revisará el resultado antes del design freeze.

---

# 1. CONTEXTO DEL PRODUCTO

Estamos construyendo un engine durable, no una POC.

Baseline frozen:

- Go.
    
- Monolito modular.
    
- Un único deployable.
    
- Una máquina grande inicialmente.
    
- Específico de Polymarket.
    
- Agnóstico de estrategias.
    
- Sin Kafka, Flink, Kubernetes ni microservicios prematuros.
    
- Sin LLM en el hot path.
    

Primeros consumidores:

`POC-S01 NegRisk`

`POC-S02 Sports`

Las estrategias son experimentales y descartables; la infraestructura común no.

North star:

`TIME_TO_VALIDATED_HYPOTHESIS`

La arquitectura debe permitir investigar, grabar, reproducir, simular, ejecutar en shadow y eventualmente operar estrategias sin reconstruir discovery, market data, recorder, replay, risk, execution ni observabilidad.

No existe obligación de operar con dinero real para cerrar el Engine MVP.

El tiny-live futuro dispone inicialmente de un presupuesto total previsto de US$300, sujeto a aprobación del owner.

---

# 2. CONTEXT PACK CERRADO — LECTURA EFICIENTE

NO explores el vault.

NO recuperes memoria de otros proyectos.

NO consultes Echo, Forge ni Hermes.

NO abras documentación oficial de Polymarket en Internet.

NO hagas búsquedas generales.

## Fuente principal — lectura obligatoria completa

`Polymarket Engine — MVP.md`

Lee:

1. Objetivos y decisiones frozen.
    
2. Capabilities y gates M0–M4.
    
3. La propuesta `M1 — ASTRA Architecture Proposal`, desde M1.0 hasta M1.17.
    
4. Las 35 decisiones A-01…A-35.
    
5. Las incertidumbres U-01…U-10.
    
6. El handoff FABLE de Astra.
    

Esta propuesta es el objeto de tu auditoría.

## Technical Platform Map — lectura selectiva

Índice:

`main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`

Tiene once partes enlazadas y M0 DESIGN_READY.

**No vuelvas a leer las once partes completas indiscriminadamente.**

Comienza por `part-10-gaps-recovery.md`, §24, para conocer qué está certificado para diseño y qué permanece deshabilitado.

Consulta exclusivamente las secciones contractuales necesarias para verificar un finding:

- part-03: auth, precisión y tiempo.
    
- part-04: órdenes y ciclo de vida.
    
- part-05: WS, books, posiciones y contratos.
    
- part-06: NegRisk y versiones.
    
- part-07: economics, resolución e histórico.
    
- part-09: seguridad y workflows.
    
- part-02 y part-08: sólo endpoints, schemas o discrepancias concretas relacionados con el finding.
    
- part-11: sólo referencias que necesites comprobar dentro del pack.
    

No leas las 81 KB de part-08 completas si basta una sección puntual.

El mapa técnico es una autoridad de protocolo, no una propuesta de arquitectura alternativa.

## Edge Research

`Polymarket — Edge Research Consolidado 2026-09-16.md`

Consulta sólo su síntesis y los requisitos de las familias Sports/NegRisk cuando necesites demostrar que una capability transversal falta.

No revises las cuatro investigaciones originales.

No diseñes ninguna estrategia.

## Bootstrap

Ejecuta únicamente el bootstrap mínimo obligatorio de Agents-OS. No amplíes el scope documental por ese motivo.

Si un dato externo no está disponible en este pack, registra la incertidumbre y su impacto. No consumas la sesión realizando investigación nueva.

---

# 3. OBJETIVO REAL DEL CHALLENGE

No queremos una opinión sobre el estilo de arquitectura.

Queremos saber:

**¿Qué decisiones de Astra pueden provocar pérdida de datos, capital incorrecto, órdenes duplicadas, falsos resultados experimentales, deadlocks, recuperación imposible o una implementación innecesariamente grande?**

Busca contraejemplos reproducibles.

Distingue:

- Defecto demostrado del diseño.
    
- Riesgo residual reconocido y razonablemente contenido.
    
- Decisión que requiere aceptación del owner.
    
- Preferencia arquitectónica sin consecuencia material.
    

No conviertas preferencias en blockers.

No critiques por segunda vez un problema que Astra ya resolvió, salvo que demuestres que su solución sigue siendo insuficiente.

No reabras decisiones macro frozen sin un contraejemplo material.

---

# 4. AUDITORÍA ADVERSARIAL OBLIGATORIA

## A. Corrección de datos y books

Intenta demostrar una ejecución en la que:

- REST y WS queden mezclados sin frontera válida.
    
- Un delta de epoch anterior llegue después del nuevo snapshot.
    
- Un cambio de tick/fee/rules no invalide un candidato.
    
- Un overflow o pérdida de datos conserve calidad elegible.
    
- El Frame Builder use revisiones de distintos cortes.
    
- Un shard lento bloquee indefinidamente el sistema.
    
- El corte `C` espere un evento que depende del propio delivery.
    

Si Astra ya impide el escenario, registra PASS razonado y continúa.

No afirmes que puede garantizarse continuidad remota si Polymarket no ofrece esa garantía.

## B. Journal, SQLite y recovery

Éste es uno de los focos principales.

Examinar:

`capture → durable_seq → reducers → applied_seq → frame → strategy → intent`

Y por separado:

`reserve + intent + outbox → attempt → HTTP → ACK/reconciliation`

Inyecta conceptualmente crashes en todos los límites de persistencia.

Determina si es posible:

- publicar un frame con evidencia todavía no durable;
    
- perder un intent aceptado;
    
- reprocesar dos veces un fill;
    
- dejar una reserva liberada prematuramente;
    
- restaurar SQLite con referencias a journal inexistente;
    
- exportar un resultado de replay que no corresponde a lo entregado originalmente;
    
- crear una dependencia circular entre DB, journal, scheduler o callbacks.
    

No basta con escribir «usar outbox».

Identifica el orden exacto de persistencia, el fallo y la propiedad violada.

## C. Capital, órdenes y conciliación

Construye casos adversariales para:

- timeout después de aceptar una orden;
    
- crash entre firma y envío;
    
- crash después de enviar, antes del ACK;
    
- fills concurrentes con cancelación;
    
- maker/taker con múltiples órdenes propias;
    
- actualizaciones duplicadas y fuera de orden;
    
- trade matched pero settlement pendiente;
    
- chain reorg;
    
- transferencia externa;
    
- reinicio con órdenes GTC/GTD abiertas;
    
- cancel-all sobre scope incompleto;
    
- balance insuficiente o discrepante.
    

Busca violaciones de conservación, doble gasto y pérdida de atribución.

Revisa especialmente el caso en que la base de datos o disco falla y Astra permite cancelaciones defensivas sin persistir un audit nuevo.

Exige una frontera explícita entre seguridad operacional y trazabilidad degradada.

## D. Seguridad y capabilities deshabilitadas

Intenta alcanzar el signer o enviar una operación prohibida mediante:

- Strategy API.
    
- Configuración.
    
- Reutilización de adapters.
    
- Recovery.
    
- Cancelaciones de emergencia.
    
- Cambios de perfil.
    
- Un lease expirado o perteneciente a otra cuenta/build.
    

Valida los límites reales de aislamiento de Go en un único proceso.

No exijas un sandbox de procesos sin demostrar que es requisito de este MVP.

Mantener deshabilitado:

- NegRisk conversion CTF/v2 live.
    
- Backfill L2 como fuente completa.
    
- `deferExec=true`.
    
- Builder optional modes.
    
- Combos/RFQ fuera de scope.
    

No diseñes una ABI v2 que el pack no conoce.

## E. Replay y validez experimental

Prueba si dos ejecuciones con idénticos inputs, manifests, código y seed pueden producir distintos resultados por:

- scheduling de goroutines;
    
- iteración de maps;
    
- timers;
    
- cortes multiasset;
    
- metadatos recibidos después del evento;
    
- snapshots perdidos;
    
- coalescing;
    
- fills contrafactuales;
    
- profundidad reutilizada por varias estrategias.
    

Comprueba que `NO EDGE` no pueda resultar de una pérdida de datos o falla del modelo.

El engine sólo puede garantizar replay determinista de su captura, no reconstrucción completa de lo que Polymarket jamás entregó.

## F. Viabilidad y alcance del MVP

Pregunta si los mecanismos propuestos son el mínimo núcleo necesario para lograr el objetivo.

Cuestiona específicamente:

- SQLite + journal propio + Parquet.
    
- Captura durable en el hot path.
    
- Frame Builder con corte global local.
    
- Strategy API con siete métodos.
    
- Account Coordinator serializado.
    
- 35 decisiones y 19 gates.
    
- Backups y retención.
    
- Simulación multi-leg y virtual liquidity ledger.
    

No elimines durabilidad o seguridad sólo para simplificar.

Identifica cualquier mecanismo cuya complejidad pueda diferirse sin romper contratos, replay, ownership ni futuras POCs.

Separa:

`FOUNDATIONAL NOW`

de:

`IMPLEMENT LATER WITHOUT REDESIGN`

El resultado debe ayudar a TOP a planificar una implementación acotada después del freeze.

---

# 5. FORMATO DE CADA FINDING

Cada finding MATERIAL debe contener:

```text
ID: FBL-001

Severity: P0 | P1 | P2

Affects:
- M1 section
- A-ID
- U-ID, if applicable

Claim:
Qué afirma la propuesta.

Counterexample:
Secuencia concreta de eventos, estados o fallos.

Violated invariant:
Qué propiedad deja de cumplirse.

Impact:
Pérdida de datos, doble gasto, falso edge,
deadlock, seguridad, recuperación o coste material.

Evidence:
Referencia exacta a M1 y, si corresponde,
al Technical Platform Map.

Minimal correction:
Cambio más pequeño que resuelve el defecto.

Closure test:
Escenario verificable que debe pasar.

Disposition:
BLOCKING_BEFORE_FREEZE |
OWNER_DECISION |
DEFER_TO_M2_WITH_FIXED_CONTRACT |
ACCEPTED_RESIDUAL_RISK
```

Un finding debe ser suficientemente preciso para que Astra pueda corregirlo sin pedirte otra explicación.

No uses P0 para señalar mejoras deseables.

Severidad:

**P0:** pérdida potencial de capital, duplicación de efectos, ruta live no autorizada, corrupción silenciosa o diseño imposible.

**P1:** defecto material de arquitectura, determinismo, recuperación, ownership o complejidad que debe resolverse antes del freeze.

**P2:** mejora acotada que no exige rediseñar M1.

Agrupa hallazgos duplicados.

Prioriza calidad sobre cantidad.

No necesitas producir diez findings si sólo existen tres demostrables.

---

# 6. LÍMITE DE LA REVISIÓN

Tienes un solo shot.

Organiza internamente el trabajo por prioridad:

1. Leer diseño y registro A/U.
    
2. Comprobar invariantes P0.
    
3. Comprobar invariantes P1.
    
4. Revisar complejidad y scope.
    
5. Redactar correcciones mínimas.
    
6. Publicar y verificar.
    

No gastes la mitad de la ventana generando un segundo diseño completo.

No dediques espacio a repetir todas las decisiones que ya consideras correctas.

Incluye un resumen compacto de las invariantes auditadas sin findings.

No conviertas el challenge en otra documentación de 100 KB.

**Presupuesto documental sugerido: 10–20 KB de findings y handoff; superar sólo si existen defectos materiales que lo justifiquen.**

---

# 7. RESOLUCIÓN Y HANDOFF EN UNA SOLA PASADA

Además de los findings, incorpora:

## A. Freeze blockers

Tabla exacta de los findings que Astra debe corregir antes de congelar M1.

Cada bloqueo debe tener test de cierre.

## B. Owner decisions

Sólo decisiones reales del owner que afecten al diseño.

No exijas decidir ahora políticas live que ya pueden permanecer deshabilitadas.

Distingue decisiones necesarias para:

`M1 DESIGN FREEZE`

de decisiones necesarias posteriormente para:

`LIVE ACTIVATION`

## C. Deferred implementation gates

Identifica verificaciones que TOP/NORMAL pueden realizar después del diseño sin inventar arquitectura.

No declares tests como ejecutados.

## D. Reconciliation instructions for Astra

Ordena las correcciones por dependencia y referencia exacta.

No dejes preguntas abiertas vagas.

Por cada finding, indica la resolución mínima aceptable.

Si existen dos soluciones razonables, explica tradeoffs y recomienda una como propuesta técnica, sin congelarla por cuenta propia.

## E. Estado de la propuesta

Concluye con uno de estos estados:

`NO_MATERIAL_FINDINGS`

`MATERIAL_FINDINGS_REQUIRE_RECONCILIATION`

`BLOCKED_BY_MISSING_DESIGN_EVIDENCE`

No declares design freeze.

---

# 8. ÚNICO ARCHIVO DE SALIDA

Edita exclusivamente:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Preserva íntegramente:

- M0.
    
- M1.0–M1.17.
    
- Decisiones frozen D-001…D-014.
    
- A-01…A-35.
    
- U-01…U-10.
    
- Gates G-01…G-19.
    

**No sustituyas la propuesta de Astra por tu propia arquitectura.**

Añade después de M1.17:

`## M1 — FABLE Adversarial Challenge`

Dentro de esa sección incorpora:

1. Alcance y baseline auditado.
    
2. Hallazgos materiales.
    
3. Invariantes auditadas sin defecto demostrado.
    
4. Freeze blockers.
    
5. Decisiones del owner.
    
6. Gates diferidos.
    
7. Handoff cerrado para ASTRA-2.
    
8. Estado `M1_FABLE_CHALLENGE_COMPLETE`.
    

Si detectas una contradicción evidente en una sección anterior, registra su corrección exacta en el finding. Deja que Astra la integre durante la reconciliación para preservar trazabilidad de autoría.

No modifiques las once partes del Technical Platform Map.

No crees ADRs, SPECs, comentarios o documentos alternativos.

No implementes código.

---

# 9. PUBLICACIÓN

Ejecuta Git preflight:

- branch;
    
- HEAD;
    
- worktree;
    
- blob actual del proyecto;
    
- cambios concurrentes.
    

Confirma que la propuesta de ASTRA-1 del commit `4e95dcd` está presente.

Edita únicamente el archivo permitido.

Publica mediante el workflow autorizado, sin force push.

Si GitHub rechaza el cambio por concurrencia, recupera el archivo actual, preserva los cambios ajenos y vuelve a aplicar sólo tu sección.

Verifica en GitHub:

- commit publicado;
    
- archivo actualizado;
    
- sección FABLE presente;
    
- propuesta Astra preservada;
    
- M0 intacto;
    
- estado no congelado.
    

El documento en GitHub es el entregable.

La respuesta del chat no lo sustituye.

---

# 10. RESPUESTA FINAL

No pegues el análisis en el chat.

No generes un segundo documento.

Responde brevemente:

```text
STATUS: M1_FABLE_CHALLENGE_COMPLETE | PARTIAL | BLOCKED

GITHUB:
- commit SHA
- enlace al proyecto

REVIEW:
- P0 count
- P1 count
- P2 count
- principales hallazgos

FREEZE:
- blockers exactos
- owner decisions indispensables
- deferred gates

ASTRA-2:
- orden de reconciliación
- criterio de aceptación
```

Tu misión termina al publicar el challenge completo.

No esperes respuestas intermedias del owner.

No solicites otra ronda con Fable.

**Ejecuta la revisión adversarial ahora y deja un handoff suficientemente preciso para que ASTRA-2 resuelva todos los findings en una única reconciliación.**