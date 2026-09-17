# MANDATO — ASTRA-3

## Polymarket Engine MVP · Owner Decisions + Final Design Freeze

### MISIÓN

Actúa como arquitecto principal del Polymarket Engine.

ASTRA-1 produjo la arquitectura inicial.

FABLE ejecutó el challenge adversarial.

ASTRA-2 reconcilió los doce findings y dejó el proyecto en:

`M1_RECONCILED_PENDING_OWNER_REVIEW`

El owner ha revisado las tres decisiones pendientes y las aprueba según este mandato.

Tu misión es **cerrar M1 definitivamente**, no iniciar otra ronda de arquitectura.

Debes:

1. incorporar las decisiones del owner;
    
2. realizar una auditoría final de consistencia;
    
3. corregir únicamente contradicciones introducidas por la reconciliación o por estas aprobaciones;
    
4. congelar el diseño;
    
5. dejar un handoff inequívoco para M2/TOP.
    

No hagas Deep Research.

No implementes.

No produzcas el plan de implementación.

No vuelvas a challengear toda la arquitectura.

No generes documentos nuevos.

---

# 0. ENTORNO

Trabajas sobre Agents-OS local.

La sincronización externa es automática y no forma parte de tu responsabilidad.

No uses GitHub, commits remotos ni APIs de GitHub como autoridad operacional.

Resuelve `VAULT_ROOT` / Agents-OS local mediante el bootstrap canónico mínimo.

Único archivo de trabajo:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

No explores otros proyectos del vault.

No abras Echo, Echo Forge, Hermes ni memorias externas.

Fuentes permitidas sólo si necesitas comprobar consistencia:

- el mismo proyecto;
    
- `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`;
    
- `main/30-resources/polymarket/Polymarket — Edge Research Consolidado 2026-09-16.md`.
    

No vuelvas a leer el Technical Platform Map completo salvo que una contradicción concreta lo exija.

---

# 1. OWNER DECISIONS — APROBADAS

Estas decisiones dejan de ser `REQUIRES_OWNER`.

## OD-1 — APPROVED

### Trusted strategies in-process

El MVP ejecutará estrategias como código Go **confiable y revisado dentro del mismo proceso**.

Aceptamos explícitamente:

- no existe aislamiento fuerte de memoria/syscalls entre strategy y engine;
    
- los gates de imports, lint, API restringida y ausencia de secrets son defense-in-depth;
    
- no se presentan como sandbox;
    
- no se admiten plugins arbitrarios ni código no confiable;
    
- una strategy no obtiene network, signer, wallet, repositorios ni execution ports mediante su API;
    
- el puerto `Credentials/Signing` debe conservar un boundary que permita externalizarlo posteriormente sin cambiar dominio ni Strategy API.
    

Un futuro aislamiento por proceso es una evolución, no requisito del MVP.

Actualiza A-15/U-10 y referencias afectadas para reflejar:

`APPROVED`

No introduzcas procesos extra ahora.

---

## OD-2 — APPROVED

### FOUNDATIONAL NOW / IMPLEMENT LATER WITHOUT REDESIGN

Se aprueba la partición reconciliada de alcance.

### FOUNDATIONAL NOW

Debe incluir el núcleo necesario para cerrar M2–M4 sin trading real:

- dominio e IDs tipados;
    
- decimal exacto;
    
- Catalog/Universe known-at;
    
- Regimes/Resolution necesarios;
    
- market-data adapters read-only;
    
- Book shards y quality;
    
- Frame Builder;
    
- Capture journal y recovery;
    
- carriles EVIDENCE/RUNTIME;
    
- manifests;
    
- deterministic replay dentro de sus límites documentados;
    
- Strategy API;
    
- SCREEN;
    
- REPLAY;
    
- SHADOW;
    
- Experiment/Hypothesis framework;
    
- Simulator;
    
- liquidity ledger aislado por experimento;
    
- optimistic/base/stress models;
    
- multi-leg simulation;
    
- Account Coordinator;
    
- ledger/reservas;
    
- BasketPolicy/BasketExecution como contrato común necesario por Simulator/futuro live;
    
- SQLite operacional;
    
- datasets/scorecards con lineage;
    
- observabilidad/readiness;
    
- gates y fault fixtures;
    
- **backup/restore local consistente y medido** necesario para certificar crash recovery.
    

### IMPLEMENT LATER WITHOUT REDESIGN

Queda fuera de la implementación inicial:

- trading live;
    
- ActivationLease operativo para envío real;
    
- Execution HTTP real;
    
- User WS/Reconciler live completo cuando sólo sirvan ejecución real;
    
- operaciones on-chain activas;
    
- conversiones NegRisk;
    
- Protocol-v2 codecs no certificados;
    
- `deferExec=true`;
    
- Builder modes;
    
- Session Keys;
    
- auto-wallet / auto-approvals;
    
- Combo/RFQ;
    
- Bridge/funding automático;
    
- Sports WS o external adapters concretos hasta que una POC los requiera;
    
- queue maker calibrado;
    
- Parquet si un formato derivado más simple basta inicialmente;
    
- dashboards/UI;
    
- tracing live completo;
    
- alertas externas;
    
- compresión/GC automatizado no necesarios para el primer ciclo;
    
- disaster recovery fuera del host;
    
- restore desde infraestructura remota;
    
- rotación operacional de credenciales propia de live.
    

**Importante:** diferir implementación no permite dejar indefinido el contrato cuando incorporarlo después exigiría rediseñar ownership, dominio, Strategy API o persistencia.

El restore **local** sí es foundational.

El disaster recovery **off-host** no lo es.

Actualiza decisiones y gates para eliminar cualquier contradicción entre esta partición y M4.

---

## OD-3 — APPROVED

### Retención de evidencia privada de cuenta

Se aprueba:

`ACCOUNT_FACT` y la evidencia privada mínima necesaria para reconstrucción, auditoría y reconciliación se retienen durante **la vida del proyecto**.

Esta evidencia:

- queda fuera del GC normal del raw market-data;
    
- usa ACL mínima;
    
- se cifra cuando corresponda según el diseño;
    
- no almacena claves privadas, HMAC secrets ni secretos reutilizables;
    
- conserva lineage suficiente para intents, attempts, orders, fills, reservas, reconciliación y recovery;
    
- puede archivarse/compactarse en el futuro sin perder semántica.
    

Raw market-data y derivados mantienen políticas separadas.

La eliminación futura de esta evidencia requiere una política explícita de cierre/archivo del proyecto, no TTL accidental.

Actualiza A-11/A-12/A-13/U-08 y referencias relacionadas.

---

# 2. DECISIONES QUE NO BLOQUEAN EL FREEZE

NO solicites ahora decisiones del owner sobre:

- bankroll allocation;
    
- caps de exposición;
    
- worst-loss;
    
- settlement window;
    
- máximo de UNKNOWN simultáneos;
    
- GTC;
    
- riesgo residual live de books;
    
- wallet/account real;
    
- finality depth;
    
- allowances;
    
- live NegRisk;
    
- RPO/RTO de disaster recovery off-host;
    
- canal externo de alertas;
    
- credenciales reales.
    

Estas decisiones pertenecen a posteriores gates de live activation.

Mientras no estén resueltas:

`LIVE_DISABLED`

Eso es suficiente para M1.

No conviertas políticas live en blockers de M2.

---

# 3. FINAL CONSISTENCY AUDIT

Ejecuta una única auditoría estructural, no otra ronda de diseño.

Comprueba:

## Ownership

Cada estado mutable tiene exactamente un owner.

Especial atención:

- Catalog.
    
- Books.
    
- Capture.
    
- Runtime.
    
- Account Coordinator.
    
- BasketExecution.
    
- Simulator.
    
- Reconciliation observations.
    

## Persistence

Comprueba coherencia de:

`journal → durable_seq → reducer applied_seq → frame → decision`

y:

`reserve → intent → attempt → external effect → reconciliation`

Verifica que ASTRA-2 haya cerrado FBL-001…012 sin reglas mutuamente contradictorias.

## Replay

Confirma que:

- observation replay;
    
- delivery replay;
    
- decision audit;
    
- contrafactual simulation
    

siguen separados.

No debe existir sustitución por `latest state` cuando falta una revisión histórica.

## Strategies

Comprueba que una strategy no tenga que reimplementar:

- discovery;
    
- WS;
    
- books;
    
- recorder;
    
- replay;
    
- economics comunes;
    
- account/risk;
    
- basket execution infrastructure;
    
- observability.
    

Y tampoco que el core absorba lógica específica de Sports o NegRisk.

## Scope

Comprueba que FOUNDATIONAL NOW pueda implementarse y certificarse sin depender de elementos diferidos.

Comprueba que IMPLEMENT LATER pueda añadirse detrás de contracts existentes sin rediseñar las capas fundamentales.

## Security

Comprueba que:

- disabled means fail-closed;
    
- Strategy no acceda a signer;
    
- no calldata arbitrario;
    
- no retries automáticos ambiguos;
    
- no live accidental;
    
- owner decisions aprobadas no habiliten capacidades live.
    

## Gates

Comprueba que cada contrato arquitectónico introducido por FABLE/ASTRA-2 tenga un gate observable.

Los gates físicos siguen:

`NOT_RUN`

No declares PASS por existir el diseño.

---

# 4. CRITERIO PARA CORREGIR

Si la auditoría encuentra una contradicción:

corrígela directamente en la sección normativa correspondiente.

Sólo corrige problemas que:

- hagan imposible implementar el contrato;
    
- produzcan ownership ambiguo;
    
- contradigan otra regla frozen;
    
- puedan provocar pérdida/corrupción/doble efecto;
    
- hagan imposible un gate;
    
- obliguen a TOP a inventar arquitectura.
    

No hagas mejoras cosméticas.

No agregues sistemas porque “serían mejores”.

No abras decisiones nuevas salvo blocker material demostrado.

Si detectas un blocker material imposible de resolver con el contexto existente:

`BLOCKED — DESIGN ISSUE`

y no congeles M1.

---

# 5. DESIGN FREEZE

Si la auditoría pasa:

actualiza el estado de M1 a:

`M1_DESIGN_FROZEN`

Registra claramente:

- ASTRA-1 proposal;
    
- FABLE challenge;
    
- ASTRA-2 reconciliation;
    
- OD-1/OD-2/OD-3 approved;
    
- final audit passed;
    
- arquitectura frozen;
    
- physical gates NOT_RUN;
    
- live NOT certified;
    
- capabilities live/optional siguen disabled.
    

Las decisiones arquitectónicas reconciliadas pasan de:

`PROPOSED`

a:

`FROZEN`

cuando no dependan exclusivamente de un protocolo aún no disponible.

Conserva:

`BLOCKED_BY_PROTOCOL`

donde corresponda.

Las políticas exclusivas de live pueden permanecer:

`DEFERRED_LIVE_DECISION`

No congeles números de operación todavía desconocidos.

---

# 6. HANDOFF A M2 / TOP

Actualiza la sección de estado/tareas del proyecto.

Marca M1 cerrado.

Siguiente fase:

`M2 — TOP IMPLEMENTATION PLAN`

El TOP recibirá exclusivamente:

- este proyecto frozen;
    
- Technical Platform Map;
    
- Edge Research Consolidado sólo cuando una decisión de implementación necesite comprender requirements transversales.
    

TOP debe transformar FOUNDATIONAL NOW en un plan ejecutable:

- dependency order;
    
- slices;
    
- packages/files permitidos;
    
- schemas;
    
- storage setup;
    
- tests;
    
- gates;
    
- failure/recovery;
    
- definition of done.
    

TOP no rediseña.

Si encuentra una contradicción arquitectónica material:

`BLOCKED — DESIGN ISSUE`

y la devuelve al manager.

No escribas ese plan en este shot.

---

# 7. PERSISTENCIA

Trabaja directamente sobre:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

No generes otro documento.

No edites Technical Platform Map.

No crees ADRs ni SPECs.

No dependas de GitHub.

La sincronización ocurre fuera de tu responsabilidad.

Preserva FABLE y el historial ASTRA.

Puedes compactar únicamente estados/handoffs redundantes si no destruyes trazabilidad.

---

# 8. RESPUESTA FINAL

Devuelve sólo:

STATUS: `M1_DESIGN_FROZEN` | `BLOCKED_DESIGN_ISSUE`

OWNER:

- OD-1:
    
- OD-2:
    
- OD-3:
    

AUDIT:

- contradicciones materiales encontradas:
    
- correcciones finales:
    
- blockers restantes:
    

SCOPE:

- FOUNDATIONAL NOW:
    
- IMPLEMENT LATER:
    

GATES:

- architectural contracts:
    
- physical tests:
    
- live:
    

NEXT:

- M2 TOP implementation plan
    

No pegues nuevamente la arquitectura por chat.

---

# INSTRUCCIÓN FINAL

Las fases de exploración terminaron.

No optimices más el diseño.

No abras otra ronda adversarial.

**Incorpora OD-1/2/3, comprueba consistencia y congela M1 si no existe un blocker material demostrado.**