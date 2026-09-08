MODELO: NORMAL

AGENTE/MODELO NUEVO.  
CONVERSACIÓN NUEVA.

ONE-SHOT OBLIGATORIO:

corregir los cinco findings → ejecutar todos los gates → commit → push → Agents OS delta → handoff corto → cerrar sesión → feedback → STOP.

# ECHO E-01 — CLOSE CONTRACT VERIFICATION FINDINGS

Repo:

`xKoRx/echo`

Branch:

`master`

Baseline exacto:

`bd681814b9ec697837360b840d55f659f195ca13`

Failed verification artifact:

`specs/FEAT-SDK-CANONICAL-CONTRACT/VERIFICATION.md`

Implementation previa certificada hasta gates:

`f403e6d76cf1c2777458cbfcd82ded3c26b7a01d`

Phase:

`E-01 — Canonical SDK Foundation S0`

## 0. MISIÓN

Corregir exclusivamente los findings materiales registrados por el Verifier.

NO reauditar S0.  
NO rediseñar FR-1…FR-5.  
NO modificar `VERIFICATION.md`.  
NO tocar Forge.  
NO añadir persistence/resolvers/I/O.  
NO abrir E-02/E-03/E-05.

Si cualquier corrección exige cambiar el contrato frozen:

`BLOCKED`

## 1. AUTORIDADES

Leer antes de editar:

- `SPEC.md`
    
- `TASKS.md`
    
- `VERIFICATION.md`
    
- Agents OS `[[Echo — E-01 Canonical SDK Foundation S0]]`
    

Precedencia:

`SPEC/freeze > verification finding > TASKS > source`

## 2. ALLOWED PRODUCTIVE FILES

Sólo cuando materialmente necesarios:

- `v3/sdk/contracts/analytics.go`
    
- `v3/sdk/contracts/catalog.go`
    
- `v3/sdk/contracts/status.go`
    
- `v3/sdk/contracts/scope.go`
    
- `v3/sdk/contracts/evidence.go`
    
- `v3/sdk/contracts/promotion.go`
    
- `v3/sdk/contracts/trading.go`
    

Tests permitidos:

- `v3/sdk/contracts/*_test.go`
    

NO tocar:

- `wire/**`;
    
- `fakeconsumer/**`;
    
- `schema/**`;
    
- `go.mod`;
    
- parent SDK;
    
- workspace;
    
- `specs/**`;
    
- `VERIFICATION.md`.
    

### Excepción corpus estrictamente condicionada

Después de corregir `requested_keys_digest`, si un fixture committed queda objetivamente incorrecto porque contiene un ref/digest derivado de **esa receta incorrecta**, puedes modificar exclusivamente los fixtures/expected values afectados bajo:

`v3/sdk/contracts/testdata/v1/**`

Condiciones:

- NO `CORPUS_REGEN`;
    
- NO cambiar IDs/casos/semántica del manifest;
    
- NO actualizar goldens para “hacer pasar” tests;
    
- cada valor modificado debe derivarse independientemente de la receta frozen;
    
- handoff debe listar los archivos exactos si ocurre.
    

Si falla un golden por cualquier otra razón:

`BLOCKED`.

## 3. FINDING A — requested_keys_digest

Autoridad exacta:

`requested_keys_digest = D("echo-metric-keys.v1", sorted_keys)`

NO:

`D("echo-metric-keys.v1", {"keys": sorted_keys})`

Corregir `RequestedKeysDigest`.

Requisitos:

1. copiar input;
    
2. ordenar keys por UTF-8;
    
3. hashear **el array directamente**;
    
4. no mutar input;
    
5. distinto orden inicial de las mismas keys → mismo digest;
    
6. distinto conjunto → digest distinto.
    

Añadir golden independiente con digest hardcoded calculado desde el byte recipe frozen, NO generado por `RequestedKeysDigest` durante el test.

`MetricSet.ref` debe usar exactamente este digest corregido.

## 4. FINDING B — METRIC KEY GRAMMAR

Crear una validación específica para metric keys.

Grammar exacta:

```text
[a-z0-9_]+(\.[a-z0-9_]+)*
```

Máximo:

`128 bytes`

Validar en TODOS los public boundaries de metric-key dentro del scope S0.

Como mínimo:

- `MetricV1.Validate`;
    
- `RequestedKeysDigest`;
    
- `MetricSelector.Validate`.
    

Haz un grep acotado de carriers `metric key` para no dejar otro boundary del mismo tipo sin la regla.

NO cambies `CheckSemanticKey` global: otros semantic keys tienen contratos diferentes.

Tests mínimos:

PASS:

- `win_rate`
    
- `return.total`
    
- `execution.missing_ratio`
    
- `a`
    
- `a_b.c2`
    

FAIL:

- `Return.total`
    
- `return-total`
    
- `.return`
    
- `return.`
    
- `return..total`
    
- `return total`
    
- unicode fuera de grammar
    
- > 128 bytes
    

## 5. FINDING C — REQUIRED CAPABILITIES

`required_capabilities` es una representación canónica de set:

- estrictamente ordenada por UTF-8;
    
- duplicate-free.
    

Enumera con grep todos los structs/carriers `RequiredCapabilities` bajo `v3/sdk/contracts/*.go`.

Corrige TODOS los carriers del mismo contrato, no sólo los cuatro nombres del Verifier.

Como mínimo revisar físicamente:

- `ScopeV1`;
    
- `EvaluationV1`;
    
- `TradingFactV1`;
    
- `HandoffManifestV1`.
    

Crear helper puro compartido si evita duplicación.

### Invariante

Un objeto/wire validado como contrato canónico NO puede aceptar:

`["b","a"]`

ni:

`["a","a"]`

como capability set canónico.

Orden válido:

`["a","b"]`

NO mutar silenciosamente el slice del caller.

Los encoders públicos tampoco pueden producir una representación order-dependent válida.

No cambiar la separación:

Scope capabilities ≠ envelope capabilities.

Tests:

- sorted unique PASS;
    
- unsorted FAIL;
    
- duplicate FAIL;
    
- same canonical set no produce identities/payloads distintos;
    
- Scope y envelope continúan independientes.
    

## 6. FINDING D — record_digest!

FR-5:

`record_digest! = D("echo-operation.v1", record without record_digest)`

Debe ser obligatorio en el **public sealed contract boundary**.

Corregir:

### Decode

`DecodeNormalizedOperationV1`:

`record_digest` REQUIRED.

### Validate

`NormalizedOperationV1.Validate()` debe:

1. exigir non-empty;
    
2. validar shape SHA-256;
    
3. recomputar `RecordDigestValue()`;
    
4. exigir igualdad exacta;
    
5. rechazar mutation del record con digest viejo.
    

### Encode / internal digest construction

NO crear recursión.

`RecordDigestValue()` necesita poder construir internamente el body **sin record_digest**.

Si hace falta, separar un helper privado:

`encode/fields without record digest`

del public sealed `Encode()`.

Public `Encode()` no debe emitir silenciosamente un `NormalizedOperationV1` contractualmente incompleto.

`SealRecord()` sigue siendo la vía para calcular y fijar digest.

Tests obligatorios:

- missing digest FAIL;
    
- malformed digest FAIL;
    
- correct sealed digest PASS;
    
- mutation económica con digest viejo FAIL;
    
- mutation price/time/source semantic field con digest viejo FAIL;
    
- `RecordDigestValue()` no incluye su propio digest;
    
- `SealRecord()` converge determinísticamente.
    

NO cambiar `operation_ref`.

## 7. FINDING E — supersedes_evidence_refs

Autoridad:

campo opcional **sólo cuando existe evidencia de supersession**.

S0 es validador puro; persistence/resolver está fuera de scope.

Por tanto, implementar exclusivamente lo comprobable localmente:

### Ausente

`nil` / campo ausente:

PASS.

### Presente

Si el campo está presente:

- debe contener al menos 1 ref;
    
- cada ref debe pasar `CheckOpaqueRef`;
    
- duplicates FAIL.
    

JSON `[]` explícito NO representa “evidencia real”:

FAIL.

### PROHIBIDO INVENTAR

NO:

- DB lookup;
    
- network;
    
- resolver;
    
- existencia externa;
    
- requerir que sea subset de `source_evidence_refs` salvo que una autoridad frozen lo diga explícitamente;
    
- nueva identity/revision semantics.
    

La presencia de refs válidos es la evidencia estructural que S0 puede certificar; la veracidad/existencia material pertenece al productor/consumer posterior.

Preservar:

- present list roundtrip;
    
- absent no se defaulta a empty semantic.
    

Añadir tests para:

- absent PASS;
    
- valid present PASS;
    
- explicit empty FAIL;
    
- malformed ref FAIL;
    
- duplicate FAIL.
    

## 8. NO REGRESSIONS

Deben seguir pasando:

- FR-1 Evaluation/TradeSet/MetricSet result-independent refs;
    
- FR-2 basis/unit/formula/mappings;
    
- FR-3 Scope no valuation;
    
- FR-4 completo y WP-G byte boundary;
    
- operation_ref stable;
    
- duplicate operation_ref set rejection;
    
- unknown retention;
    
- write-once conflict;
    
- StrategyVersion/ArtifactRef;
    
- fakeconsumer;
    
- G01–G36;
    
- schema no drift.
    

## 9. GATES

Desde:

`v3/sdk/contracts`

ejecutar:

```bash
GOWORK=off go test ./...
GOWORK=off go test -race -cover ./...
GOWORK=off go vet ./...
gofmt -l .
```

Esperado:

- test PASS;
    
- race PASS;
    
- vet PASS;
    
- gofmt output vacío;
    
- contracts ≥95%;
    
- wire ≥95%;
    
- fakeconsumer ≥95%;
    
- stdlib-only;
    
- schema drift NONE.
    

Además:

```bash
git diff -- specs/FEAT-SDK-CANONICAL-CONTRACT/VERIFICATION.md
```

debe ser vacío.

## 10. COMMIT / PUSH

Un único source-correction commit:

`fix(sdk): close E-01 contract verification findings`

Parent exacto esperado:

`bd681814b9ec697837360b840d55f659f195ca13`

Push:

fast-forward a `origin/master`.

PROHIBIDO:

- amend;
    
- force;
    
- rebase;
    
- tag;
    
- release.
    

## 11. AGENTS OS

Registrar la corrección contra verification commit:

`bd681814b9ec697837360b840d55f659f195ca13`

E-01 continúa:

`implementation complete / verification pending`

NO marcar verified.  
NO cerrar el subproyecto técnico todavía.

## 12. HANDOFF — MÁXIMO 25 LÍNEAS

STATUS:  
`CORRECTED` | `BLOCKED`

COMMIT:

- full SHA
    
- parent
    
- origin/master
    
- dirty
    

FINDINGS:

- requested_keys recipe PASS/FAIL
    
- metric grammar PASS/FAIL
    
- capabilities canonical set PASS/FAIL
    
- record_digest required+verified PASS/FAIL
    
- supersession structural validation PASS/FAIL
    

CORPUS:

- unchanged YES/NO
    
- si NO: exact affected files + reason
    

TESTS:

- test
    
- race/cover
    
- vet
    
- coverage
    

SCOPE:

- outside allowed NONE/list
    
- VERIFICATION.md untouched YES/NO
    

VERDICT:  
una frase

SESSION: closed  
FEEDBACK: submitted

STOP.

NO Verifier.  
NO E-02/E-03/E-05.  
NO Forge F-04.  
NO continuar esta conversación después del handoff.