# MANDATO DE IMPLEMENTACIÓN — NORMAL

## Polymarket Engine · M2-S02 Protocol Wire / DTOs / Parsers / Fixtures

### MISIÓN

Implementa exclusivamente:

`M2-S02 — Protocolo wire: DTOs, parsers y fixtures`

M1 y M2 están frozen.

M2-S01 está PASS.

No rediseñes.

No implementes networking.

No adelantes Catalog, Capture, SQLite, Books ni estrategias.

Si encuentras una contradicción material:

`BLOCKED — DESIGN ISSUE`

---

# 0. AUTORIDADES LOCALES

Agents-OS local es autoridad documental.

No uses GitHub ni commits remotos como autoridad.

Proyecto:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Lee sólo:

- M1.3;
    
- M1.6 en lo relativo a redaction;
    
- M1.11 únicamente contratos wire relevantes;
    
- M2.0–M2.3;
    
- `M2-S02`.
    

Technical Platform Map:

- `part-01-foundations.md`
    
- `part-02-rest-catalog.md`
    
- `part-03-auth-precision-time.md`
    
- `part-04-orders-lifecycle.md`
    
- `part-05-market-data-positions-contracts.md`
    
- `part-07-economics-resolution-history-limits.md`
    
- `part-08-specs-sdks-changelog.md`
    

Consulta sólo las secciones necesarias.

No navegues Internet.

No hagas nuevo research.

Repo:

`~/go/src/github.com/xKoRx/polymarket-engine`

Go baseline:

`go 1.27.0`  
`toolchain go1.27.1`

---

# 1. PRECONDICIÓN

Verifica que S01 está presente y verde.

Ejecuta preflight local y suite antes de modificar.

No alteres contracts de `internal/foundation` salvo que exista un bug demostrado.

Si necesitas cambiar Foundation:

`BLOCKED — S01 CONTRACT ISSUE`

y detente.

---

# 2. SCOPE

Crear e implementar:

`internal/protocol/**`

Fixtures:

`testdata/protocol/**`

No crear adapters de red.

No crear migraciones.

No tocar:

- capture;
    
- persist;
    
- catalog;
    
- regimes;
    
- transport;
    
- books;
    
- frames;
    
- strategy;
    
- account.
    

---

# 3. SEAM OBLIGATORIO PARA S03

Ésta es la primera prioridad del slice.

Materializa primero un seam pequeño y estable que S03 pueda consumir sin depender del resto de DTOs.

Debe incluir como mínimo contratos tipados para:

`SurfaceIdentity`  
`SchemaVersion`  
`NormalizerVersion`  
`RedactionPolicy`  
`RedactionResult`

y la API pura necesaria para:

- identificar la superficie de origen;
    
- asociar schema/normalizer version;
    
- sanitizar payloads antes de captura;
    
- indicar qué política/version de redaction se aplicó.
    

Debe cubrir desde el inicio la política frozen de secretos:

- `owner` cuando representa API key;
    
- `signature`;
    
- cookies;
    
- auth fields;
    
- headers `POLY_*`;
    
- material HMAC;
    
- cualquier campo explícitamente clasificado como secreto por el TPM.
    

La redacción debe ocurrir **antes de persistencia**.

No debe requerir red.

No debe depender de Capture.

No debe importar ningún paquete posterior.

## Gate intermedio

Cuando este seam:

- compile;
    
- tenga tests positivos/negativos;
    
- tenga API estable;
    
- pase race/vet;
    
- no exponga secretos;
    

registra:

`S02_SEAM_READY_FOR_S03`

Éste **no es S02 PASS**.

Después continúa implementando el resto de S02.

No rompas este seam durante el resto del slice salvo bug material demostrado.

---

# 4. CONTRATOS WIRE

Implementa DTOs separados por superficie.

No reutilices un mega-DTO universal.

Como mínimo:

## Gamma

- events;
    
- markets;
    
- IDs editoriales;
    
- arrays que puedan venir codificados como JSON string;
    
- keyset fields documentados;
    
- offset fallback fields documentados;
    
- fields necesarios posteriormente por Catalog.
    

No inventes envelope keyset ausente.

## CLOB REST read-only

Shapes necesarios para slices posteriores:

- `/book`;
    
- `/clob-markets/{condition_id}`;
    
- tick lookup;
    
- fee lookup;
    
- órdenes/trades shapes requeridos sólo como DTO/fixture para classifiers futuros.
    

No implementar requests HTTP.

## Market WS

DTOs/envelopes:

- `book`;
    
- `price_change`;
    
- `last_trade_price`;
    
- tick-size change;
    
- BBO extendido;
    
- initial dump semantics necesarias para parsing.
    

No implementar WebSocket.

## Data v2

Subset documentado necesario:

- positions;
    
- trades;
    
- activity;
    
- resolutions;
    
- order/orders sólo donde estén en el pack y sean necesarios para fixtures futuros.
    

No convertir Data v2 en ledger privado.

---

# 5. IDENTIDAD DE PROTOCOLO

Usa los tipos Foundation existentes.

Conserva:

`CTF`  
`PROTOCOL_V2`  
`UNKNOWN`

No implementes codecs Protocol-v2.

No hagas casts entre IDs CTF y v2.

Información insuficiente debe conservar:

`UNKNOWN`

Los consumers decidirán quarantine.

---

# 6. PRECISIÓN Y TIEMPO

Usa Foundation para decimal exacto.

No dupliques `orders.go`.

Implementa solamente parsing/normalización wire.

Debe preservarse:

- lexema original cuando corresponda;
    
- unidad original;
    
- precisión conocida;
    
- source time raw.
    

Tabla temporal mínima:

- Order EIP-712 timestamp: ms;
    
- expiration/auth: seconds;
    
- User WS: seconds;
    
- Market WS: ms;
    
- Data v2 según contrato específico.
    

No convertir timestamp en sequence.

No inventar nanosegundos.

Sentinels conocidos deben conservar raw + semántica contextual, no convertirse silenciosamente en cero válido.

---

# 7. PARSERS

Parsers deben ser:

- puros;
    
- totales sobre su input;
    
- deterministas;
    
- sin I/O;
    
- sin estado global.
    

JSON malformado:

error tipado.

Campo crítico incompatible:

contract drift / invalid según contrato.

Enum crítico desconocido:

raw preservado + clasificación explícita.

No:

“best effort success”

cuando falta un campo requerido para identidad o seguridad.

Unknown fields no críticos pueden preservarse sin bloquear si el contrato frozen así lo permite.

No conviertas toda aparición de campo nuevo en fallo si no afecta semántica crítica.

---

# 8. FIXTURES

Crear fixtures versionadas:

`testdata/protocol/<surface>/<version>/`

Cada fixture debe tener provenance suficiente:

- TPM part/section;
    
- fecha;
    
- schema/normalizer version;
    
- sanitización aplicada.
    

Crear manifest:

`testdata/protocol/manifest.json`

con SHA-256 de cada fixture.

Fixtures nunca contienen secretos reales.

Incluir positivas y negativas.

---

# 9. TESTS / GATES

Cerrar `G-03`.

Cubrir al menos:

- envelopes válidos;
    
- JSON malformado;
    
- unknown fields;
    
- enum divergente;
    
- Gamma string-arrays;
    
- longitudes incompatibles;
    
- sentinels;
    
- timestamps multiunidad;
    
- CLOB `success:false`;
    
- errores tipados;
    
- parsing decimal desde lexema;
    
- Protocol UNKNOWN;
    
- redaction recursiva.
    

Agregar fuzz/property no-panic sobre bytes corruptos.

Seeds/counterexamples deben persistirse cuando fallen según M2.

Redaction tests deben demostrar que después de sanitizar no aparecen:

- owner credential;
    
- signature;
    
- cookies;
    
- POLY_*;
    
- HMAC/auth material.
    

Archtest debe demostrar cero imports de red desde protocol.

---

# 10. QUALITY

Ejecuta:

`go build ./...`  
`go vet ./...`  
`go test ./...`  
`go test -race ./...`  
`go mod tidy`

Mantén coverage Agents-OS ≥95% en el código del slice.

No sacrifiques contract tests por coverage.

---

# 11. DEFINITION OF DONE

S02 PASS sólo si:

1. seam S03 estable;
    
2. DTOs requeridos implementados;
    
3. parsers deterministas;
    
4. redaction fail-closed;
    
5. fixtures manifest completo;
    
6. G-03 PASS;
    
7. G-01 extensión wire PASS;
    
8. fuzz/property verde;
    
9. build/vet/race verde;
    
10. coverage requerido;
    
11. cero network I/O;
    
12. cero scope posterior.
    

---

# 12. RESPUESTA FINAL

STATUS: `M2-S02_PASS | PARTIAL | BLOCKED`

SEAM:

- S02_SEAM_READY_FOR_S03:
    
- contracts:
    
- compatibility:
    

PROTOCOL:

- surfaces:
    
- DTOs:
    
- parsers:
    
- redaction:
    

FIXTURES:

- count:
    
- manifest:
    
- provenance:
    

QUALITY:

- build:
    
- test:
    
- race:
    
- vet:
    
- coverage:
    

GATES:

- G-03:
    
- G-01 wire extension:
    
- NOT_RUN:
    

BLOCKERS:

- none | exact blocker
    

NEXT:

- S03 may continue / barrier S02+S03