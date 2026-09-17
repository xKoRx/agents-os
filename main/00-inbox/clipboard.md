# MANDATO DE IMPLEMENTACIÓN — NORMAL

## Polymarket Engine · M2-S03 Capture Journal + Persistence

### MISIÓN

Implementa exclusivamente:

`M2-S03 — Capture journal, carriles y framework de persistencia`

Trabajas en paralelo con el resto de S02 **sólo después** de que el proyecto local indique:

`S02_SEAM_READY_FOR_S03`

No rediseñes.

No modifiques el package ownership de S0542.

No implementes reducers de dominio.

No implementes networking.

Si el seam de S02 resulta insuficiente:

`BLOCKED — S02 SEAM ISSUE`

No lo modifiques tú.

---

# 0. AUTORIDADES

Agents-OS local.

No GitHub como autoridad.

Proyecto:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Lee:

- M1.6;
    
- M1.7;
    
- FBL-003/FBL-009 reconciliados;
    
- M2.1;
    
- M2.2;
    
- `M2-S03`.
    

Repo:

`~/go/src/github.com/xKoRx/polymarket-engine`

Go:

`1.27.0`  
toolchain `1.27.1`

Technical Platform Map sólo cuando sea necesario para semantics de surface/redaction ya expuestas por S02.

No hagas research.

---

# 1. PRECONDICIÓN

Antes de modificar verifica:

- S01 PASS;
    
- `S02_SEAM_READY_FOR_S03`;
    
- protocol expone surface identity/version/redaction sin I/O;
    
- suite base verde.
    

No uses DTOs de S02 que todavía estén en construcción salvo el seam declarado estable.

---

# 2. OWNERSHIP

Tu scope exclusivo:

`internal/capture/**`  
`internal/persist/**`  
`migrations/0001–0009_*`  
`testdata/capture/**`

y únicamente el wiring CLI necesario para:

`journal verify`

No tocar:

`internal/protocol/**`

No tocar reducers futuros:

- catalog;
    
- regimes;
    
- books;
    
- account;
    
- strategy.
    

---

# 3. CAPTURE ENVELOPE

Implementa el envelope frozen de M1.6.

Como mínimo:

- capture_id;
    
- boot_id;
    
- capture_seq;
    
- surface;
    
- connection_id;
    
- epoch;
    
- frame_ordinal;
    
- request_id;
    
- received_wall;
    
- received_mono_offset;
    
- source_time_raw;
    
- source_unit;
    
- schema_version;
    
- normalizer_version;
    
- config_revision;
    
- content_hash;
    
- sanitized payload bytes;
    
- redaction policy/version;
    
- quality/control kind;
    
- segment_id;
    
- offset;
    
- length;
    
- checksum.
    

`capture_seq` es orden total **local**.

Nunca representa secuencia global Polymarket.

La sanitización debe pasar por el seam S02 **antes** de escribir payload.

Payload secreto no llega al journal.

---

# 4. DURABLE-BEFORE-PUBLISH

Regla central:

ningún consumer puede observar como aplicable un record con:

`capture_seq > durable_seq`

`durable_seq` sólo avanza tras persistencia durable conforme al contrato.

No simules durabilidad actualizando el watermark antes del fsync.

Batch/group commit es configurable y acotado.

Fallos deben ser visibles.

---

# 5. EVIDENCE / RUNTIME LANES

Implementa dos carriles hacia el mismo orden lógico:

`EVIDENCE`  
`RUNTIME`

Presupuestos separados:

- count;
    
- bytes.
    

EVIDENCE mantiene reserva propia.

Saturación RUNTIME:

- pausa/niega nuevos runtime records según política;
    
- nunca consume reserva EVIDENCE;
    
- nunca genera por sí misma pérdida de market-data;
    
- nunca revoca epochs.
    

Saturación EVIDENCE real:

- visible;
    
- produce discontinuidad declarable;
    
- Capture no inventa número de frames perdidos antes de admisión.
    

No `drop-oldest`.

No cola ilimitada.

---

# 6. JOURNAL

Formato segmentado append-only.

Requisitos:

- records length-prefixed;
    
- format version;
    
- envelope;
    
- payload sanitizado;
    
- CRC/checksum por record;
    
- límites de segmento por bytes/tiempo;
    
- footer con range/count/SHA-256;
    
- segmentos sellados inmutables;
    
- rename seguro;
    
- sync de directorio cuando corresponda.
    

No implementar todavía:

- compresión;
    
- GC;
    
- remote backup;
    
- hash-chain sofisticada si está diferida.
    

Mantén el contrato preparado sin introducir complejidad no foundational.

---

# 7. CRASH RECOVERY

Al recuperar:

- escanear hasta último record completo/checksum válido;
    
- preservar evidencia del sufijo inválido;
    
- no contabilizar record parcial;
    
- reconstruir índices derivados;
    
- recuperar `durable_seq`;
    
- abrir nuevo boot cuando corresponda;
    
- registrar discontinuidades.
    

No afirmar que frames en kernel/RAM existieron.

No afirmar que un crash preservó mensajes no fsynced.

No usar “latest file size” como sustituto de frontera durable.

---

# 8. SQLITE / PERSIST

Implementa framework SQLite de M2.

Driver previsto:

`modernc.org/sqlite`

Debe quedar encapsulado.

Config:

- WAL;
    
- synchronous FULL;
    
- busy deadline;
    
- schema version.
    

Migraciones:

`0001–0009`

Como mínimo:

- `schema_migrations`;
    
- `reducer_cursors`.
    

Forward-only.

Aplicación antigua contra schema futuro:

FAIL explícito.

No rollback mágico de migración después de efectos externos.

---

# 9. SINGLE WRITER / CURSORS

Framework provee single writer serializado para estado transaccional.

Transacciones breves.

Nunca mantener locks de DB durante:

- red;
    
- journal fsync;
    
- callbacks externos.
    

`applied_seq` debe ser por:

`reducer_id + namespace`

No global único.

Dos reducers pueden avanzar independientemente.

Un reducer nunca puede afirmar:

`applied_seq > durable_seq`

Helpers deben rechazarlo.

---

# 10. OUTBOX

Implementa pattern/framework, no negocio.

Los owners posteriores crearán sus tablas/eventos.

No existe generic worker autorizado a enviar efectos externos.

Outbox no significa:

`send anything`

Debe ser primitive transaccional/idempotente.

No implementar Execution.

---

# 11. INTEGRITY CLASSES

Materializa las clases congeladas:

`ACCOUNT_FACT`  
`RESEARCH_EVIDENCE`

En S03 sólo define/API y verificación básica.

No implementes GC.

La ausencia futura de RESEARCH_EVIDENCE podrá marcar:

`NOT_REPRODUCIBLE`

No debe confundirse con recuperación de account.

ACCOUNT_FACT real aparecerá en S11.

---

# 12. CLI

Agregar sólo:

`journal verify`

Debe poder inspeccionar un data-dir y reportar:

- segments;
    
- ranges;
    
- durable frontier;
    
- holes/discontinuities;
    
- corrupted suffix;
    
- integrity class information.
    

No devolver simplemente un booleano `PASS`.

Debe explicar qué verificó.

---

# 13. FAULT INJECTION / TESTS

Implementa fault injection controlable para:

- partial record write;
    
- failure before fsync;
    
- failure during/after fsync boundary;
    
- seal failure;
    
- manifest failure;
    
- corrupt CRC;
    
- corrupt footer;
    
- SQLite unavailable;
    
- reducer lag.
    

No dependas de matar el sistema operativo real para testear todos los casos.

Usa abstractions pequeñas para filesystem/writer boundaries donde sea necesario.

No construyas un filesystem framework gigante.

## Gates

G-06 parcial:

- prefijo válido recuperado;
    
- corrupt tail detectado;
    
- tail preservado;
    
- `durable_seq` correcto;
    
- discontinuidad explícita.
    

G-02b parcial:

- dos reducer cursors independientes;
    
- ninguno se adelanta mutuamente;
    
- `applied_seq > durable_seq` rechazado.
    

Inputs G-14:

- bundle/frontier suficientemente explícito para futuro backup/restore.
    

Property:

ninguna decisión/consumer test puede usar raw no durable.

---

# 14. CONCURRENCIA

Expected ownership:

- un admisor lógico;
    
- un writer secuencial de journal;
    
- queues bounded;
    
- un SQLite writer serial.
    

Race detector obligatorio.

No goroutine por record.

No mutex global abarcando fsync.

Shutdown debe poder drenar hasta una frontera conocida.

Supervisor completo corresponde a S12.

---

# 15. QUALITY

Ejecutar:

`go build ./...`  
`go vet ./...`  
`go test ./...`  
`go test -race ./...`  
`go mod tidy`

Coverage del código del slice ≥95%.

Persistir property seeds/counterexamples cuando fallen.

---

# 16. DEFINITION OF DONE

S03 PASS sólo si:

1. journal append/recovery funcional;
    
2. redaction S02 aplicada antes de persistencia;
    
3. durable-before-publish demostrable;
    
4. EVIDENCE/RUNTIME aislados por budgets;
    
5. corrupt/partial tail recuperable;
    
6. SQLite WAL FULL;
    
7. migrations 0001–0009 correctas;
    
8. cursor por reducer/namespace;
    
9. impossible applied_seq > durable_seq;
    
10. outbox framework sin sender;
    
11. G-06 parcial PASS;
    
12. G-02b parcial PASS;
    
13. race/vet/tests verdes;
    
14. coverage requerido;
    
15. cero reducers/transport posteriores.
    

---

# 17. RESPUESTA FINAL

STATUS: `M2-S03_PASS | PARTIAL | BLOCKED`

DEPENDENCY:

- S02 seam consumed:
    
- compatibility issues:
    

CAPTURE:

- envelope:
    
- journal:
    
- durable frontier:
    
- lanes:
    
- recovery:
    

PERSIST:

- driver:
    
- migrations:
    
- writer:
    
- reducer cursors:
    
- outbox:
    

FAULTS:

- scenarios covered:
    
- recovery evidence:
    

QUALITY:

- build:
    
- test:
    
- race:
    
- vet:
    
- coverage:
    

GATES:

- G-06:
    
- G-02b:
    
- G-14 inputs:
    
- NOT_RUN:
    

BLOCKERS:

- none | exact blocker
    

NEXT:

- S02/S03 integration barrier → M2-S04