# MODELO: TOP

## F-04 — MAGIC ALLOCATION, VERSION SEAL AND HANDOFF

**SPEC / PLANNING ONLY. NO SOURCE IMPLEMENTATION.**

Repo producto:sssss

`xKoRx/symphony`

Baseline obligatorio:

`382f4ba5d417371f778e21619ed9eb72624a23f4`

S0 certificado a consumir:

`xKoRx/echo@91671f6f46ffa889a79aed0979cb3b4e5821ed33`

Implementación S0 certificada por E-01:

`08a0eb9a83813cda2acbd7be5232e9e0370e12ab`

Antes de trabajar:

- `origin/master` Symphony debe seguir exactamente en `382f4ba...`;
    
- worktree Symphony CLEAN;
    
- recuperar Agents OS vigente;
    
- recuperar contrato/corpus S0 desde el pin certificado;
    
- registrar SHA real de Agents OS si está disponible;
    
- si Agents OS local continúa sin `.git`, documentar degraded provenance y continuar con authority durable.
    

NO modificar `symphony`.  
NO modificar `echo`.  
NO modificar SDK.

---

# 1. OBJETIVO FROZEN

F-04 materializa un único pipeline contractual:

```text
FINALIST V2
→ durable magic allocation
→ stamp efectivo
→ compile/readback
→ StrategyVersion seal
→ HandoffManifestV1 write-once
→ thin Forge→Echo delivery adapter
```

La salida canónica es:

- `StrategyVersion` sellada;
    
- `HandoffManifestV1` verificable/write-once;
    
- estado durable de delivery.
    

No crear un tercer dominio Integration.

---

# 2. INVARIANTES QUE NO SE REDISEÑAN

## Ownership

Forge posee:

- Finalist membership;
    
- magic allocation;
    
- artefactos;
    
- StrategyVersion sealing;
    
- handoff production.
    

Echo posee:

- validated ingestion;
    
- PromotionRecord;
    
- RuntimeBinding;
    
- provisioning;
    
- eligibility;
    
- capital;
    
- activation.
    

Forge **NO**:

- escribe DB Echo;
    
- calcula eligibility Echo;
    
- asigna capital Echo;
    
- activa estrategias;
    
- recalcula membership en Echo.
    

## F-01

IDs GENERATED ya son estables mediante `ExecutionIntentKey`.

No reabrir:

- HOST_KEY;
    
- canonical generation concurrency;
    
- adopted IDs;
    
- StrategyRef UUID.
    

## F-02

`Finalist != Top N`.

Membership estructural V2 es authority.

No usar rank/score como admisión al handoff.

## B1/B2/F-03

No tocar:

- MT5 ownership;
    
- Slot Pool;
    
- fencing;
    
- takeover;
    
- Temporal lifetime;
    
- SQX long-running.
    

---

# 3. S0 ES AUTHORITY DE WIRE

Leer directamente desde el pin S0 certificado:

- `StrategyVersion`
    
- `ArtifactRef`
    
- `HandoffManifestV1`
    
- digest/hash recipes
    
- canonical encoding
    
- write-once conflict semantics
    
- required capabilities
    
- G01–G36 corpus relevante
    

No copiar tipos “parecidos” dentro de Symphony si puede consumirse el módulo/adapter correcto.

Mantener estrictamente separados:

- `C()`
    
- `H()`
    
- tagged digests
    
- legacy Forge `HashIdentity`
    

**HashIdentity legacy con newline NO equivale a `H()`.**

---

# 4. INVESTIGACIÓN SOURCE OBLIGATORIA — SYMPHONY

Mapea qué existe hoy y qué falta realmente.

Inspecciona como mínimo:

## Magic

- usos actuales de `magic_number`;
    
- defaults/magic constants históricas;
    
- Apply Selected Run;
    
- MT5 export/compiler;
    
- registry PostgreSQL;
    
- cualquier allocation/reuse actual;
    
- uniqueness constraints existentes;
    
- Campaign/StrategyRef/StageExecution relations.
    

Determina la autoridad exacta para allocation durable.

## Stamp

Determina:

- dónde se escribe hoy magic en estrategia/EA;
    
- qué bytes/config constituyen effective inputs;
    
- cuándo ocurre Apply;
    
- qué evidencia existe antes/después;
    
- cómo leer de vuelta lo realmente aplicado.
    

No aceptar:

`requested magic == applied magic`

sin readback/evidencia.

## Compile / artifacts

Mapea:

- source `.mq5`;
    
- `.ex5`;
    
- config/effective input artifacts;
    
- content digests;
    
- compile evidence;
    
- readback actual.
    

Determina exactamente qué bytes deben existir antes de sellar StrategyVersion.

## Version seal

Encuentra carriers actuales capaces de representar:

- StrategyRef;
    
- exact version identity;
    
- magic;
    
- artifacts;
    
- digests;
    
- requested/effective inputs;
    
- provenance/lineage.
    

Si no existe StrategyVersion durable en Forge, diseña la mínima autoridad necesaria.

## Handoff

Busca cualquier:

- exporter;
    
- ingestion client;
    
- handoff manifest;
    
- Echo adapter;
    
- “latest folder” lookup;
    
- implicit MinIO discovery.
    

El nuevo handoff debe ser explícito: **cero latest/folder query como autoridad**.

---

# 5. MAGIC ALLOCATION CONTRACT

Debe quedar completamente decidido para NORMAL.

Define:

- namespace;
    
- key;
    
- owner;
    
- durable store;
    
- allocation transaction/CAS;
    
- uniqueness;
    
- retry;
    
- replay;
    
- concurrency;
    
- conflict;
    
- crash before commit;
    
- crash after commit;
    
- no recycle;
    
- mapping StrategyVersion/StrategyRef ↔ magic;
    
- BWC de magic histórica.
    

El mismo logical allocation reintentado debe converger al mismo magic.

Dos identidades distintas nunca pueden recibir el mismo magic dentro del namespace aplicable.

No uses:

- random retry hasta “que resulte”;
    
- MAX+1 sin concurrency proof;
    
- memoria local;
    
- hostname;
    
- worker identity.
    

---

# 6. CATÁLOGO CC — OWNER GATE

Roadmap exige catálogo CC owner **antes de allocation física real**.

TOP debe recuperar si ya existe authority canónica para O2/CC.

Clasifica exactamente:

### `CC_READY`

Authority existe y puede ser consumida.

### `CC_MISSING_OWNER_GATE`

No existe todavía.

Si falta:

- NO inventar rangos;
    
- NO bloquear diseño/source que pueda quedar listo sin efectuar allocation física;
    
- dejar gate explícito para certificación/operación real.
    

La SPEC debe decir qué parte de NORMAL puede completarse antes del CC y cuál no.

---

# 7. STAMP + READBACK CONTRACT

Secuencia mínima obligatoria:

```text
ALLOCATE
→ APPLY/STAMP
→ READBACK
→ VERIFY
→ COMPILE
→ VERIFY ARTIFACT BYTES
→ SEAL
```

Fija exactamente:

- requested magic;
    
- allocated magic;
    
- effective/applied magic;
    
- readback source;
    
- mismatch behavior;
    
- retry;
    
- terminal error.
    

Si readback != allocation:

**FAIL CLOSED. NO SEAL. NO HANDOFF.**

No crear una StrategyVersion sobre valores sólo solicitados.

---

# 8. STRATEGYVERSION SEAL

El seal sólo puede ocurrir cuando estén disponibles los bytes/evidencias exigidos por S0.

Define:

- identity recipe exacta;
    
- inputs incluidos;
    
- artifact refs;
    
- digests;
    
- magic;
    
- effective inputs;
    
- provenance;
    
- lineage;
    
- immutability;
    
- same-input replay;
    
- different-content conflict.
    

Una versión sellada:

- no se muta;
    
- no se reseala con contenido diferente;
    
- no apunta a “latest”.
    

Determina store y constraints necesarios.

---

# 9. HANDOFFMANIFESTV1

Debe producirse usando S0 exactamente.

Define:

- producer;
    
- cuándo se crea;
    
- inputs;
    
- required capabilities;
    
- StrategyVersion refs;
    
- artifact refs/digests;
    
- Finalist V2 provenance;
    
- write-once key;
    
- payload digest;
    
- replay/idempotency;
    
- conflict semantics.
    

El manifest no activa nada en Echo.

`HANDOFF_CREATED != INGESTED != PROVISIONED != ACTIVE`

---

# 10. THIN FORGE → ECHO ADAPTER

Diseña el mínimo adapter de aplicación.

Debe:

- enviar un handoff individual explícito;
    
- usar contrato S0;
    
- no consultar internals Echo;
    
- no escribir DB Echo;
    
- no hacer provisioning;
    
- no hacer retries ambiguos tras timeout post-commit.
    

Investiga el estado actual de E-04 solamente para decidir boundary.

Si E-04 aún no ofrece endpoint certificado:

- NORMAL puede implementar producer + port/client boundary;
    
- integración real queda para join con E-04;
    
- fixtures/fake consumer S0 deben permitir CONTRACT PASS.
    

No inventar endpoint provisional incompatible.

---

# 11. FAILURE / RETRY MATRIX

La SPEC debe cerrar al menos:

- magic already allocated same identity;
    
- magic conflict;
    
- DB outage;
    
- commit outcome unknown;
    
- stamp failure;
    
- stamp/readback mismatch;
    
- compile failure;
    
- artifact missing;
    
- digest mismatch;
    
- seal replay;
    
- seal conflict;
    
- handoff replay;
    
- handoff conflict;
    
- Echo unavailable;
    
- Echo timeout pre-commit;
    
- Echo timeout post-commit/unknown receipt.
    

Para cada uno:

`STATE → RETRY? → AUTHORITY → TERMINAL/NON-TERMINAL → SIDE EFFECTS`

NORMAL no decide esto.

---

# 12. BWC

Investiga explícitamente:

- estrategias históricas con magic preexistente;
    
- StrategyVersion inexistente histórica;
    
- manifests antiguos/inexistentes;
    
- F-02 V1 history;
    
- old Apply outputs.
    

No backfill masivo salvo necesidad demostrada.

No reasignar/recycle magic histórica.

---

# 13. DATABASE MIGRATION

Determina mediante source real:

`DATABASE MIGRATION: NONE`

o lista exacta de migration(s).

Si requiere migration:

- tablas/columnas/constraints;
    
- UNIQUE/CHECK/FK;
    
- BWC;
    
- rollback/restart;
    
- brownfield test;
    
- no reescritura destructiva de historia.
    

No dejarlo para NORMAL.

---

# 14. CERTIFICACIÓN

Materializa gates concretos alineados con S0.

Cubrir como mínimo:

### SOURCE

- ownership boundaries;
    
- no latest lookup;
    
- no Echo DB writes;
    
- no ranking-as-membership.
    

### CONTRACT

- allocation uniqueness/CAS;
    
- allocation replay;
    
- stamp/readback exacto;
    
- seal determinista;
    
- seal conflict;
    
- manifest write-once;
    
- S0 corpus compartido.
    

Incluir fixtures S0 relevantes, especialmente rango:

`G04–G10` y `G19–G25`

y verificar el gate G22 aplicable definido por la authority S0.

### CONCURRENCY

- concurrent allocation;
    
- crash/unknown commit;
    
- same identity converges;
    
- different identities unique.
    

### PHYSICAL

Cuando CC esté READY:

- allocation real;
    
- stamp;
    
- compile;
    
- readback;
    
- artifact bytes;
    
- seal.
    

### INTEGRATION

Con E-04:

- mismo S0 pin;
    
- mismo manifest bytes/digest;
    
- handoff aceptado;
    
- receipt convergente.
    

No fingir INTEGRATION PASS con mock.

---

# 15. ENTREGABLES AGENTS OS

Crear canónicamente:

1. `Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract`
    
2. `Echo Forge — F-04 Magic allocation, version seal and handoff`
    
3. TASKS NORMAL atómicas.
    

TASKS:

```text
archivo/símbolo
→ cambio exacto
→ authority
→ failure/retry
→ tests
→ DONE
```

No decisiones arquitectónicas abiertas para NORMAL.

Si F-04 resulta demasiado grande para un único commit, puede dividirse en milestones internos:

```text
allocation → stamp/readback → seal → handoff/adapter
```

pero **continúa siendo una sola fase F-04**, no crear F-04A/F-04B como proyectos independientes.

---

# 16. STOP CONDITIONS

STOP para manager si aparece cualquiera:

- S0 contradice roadmap frozen;
    
- no existe una authority viable para magic sin nueva decisión estructural;
    
- uniqueness exige una decisión owner no documentada;
    
- Echo pretende poseer magic;
    
- StrategyVersion requiere cambiar S0;
    
- E-04 boundary obliga a modificar contrato S0;
    
- implementación requeriría reabrir F-01/F-02/B1/B2.
    

No improvisar.

---

# HANDOFF — MÁXIMO 15 LÍNEAS

- VERDICT
    
- Symphony baseline
    
- S0 pin
    
- CC status
    
- existing authorities
    
- magic allocation contract
    
- stamp/readback contract
    
- StrategyVersion seal
    
- HandoffManifest
    
- Echo adapter boundary
    
- migration
    
- SPEC path
    
- subproject/tasks
    
- planned source diff + certification
    
- blockers + session-close/feedback refs
    

Terminar con:

`NO NORMAL IMPLEMENTATION AUTHORIZED YET`

Después ejecutar session-close canónico y feedback.