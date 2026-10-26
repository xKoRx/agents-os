---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# E — Executable Contract Examples

## Propósito

Ejemplos reproducibles derivados de los DTO reales del baseline, para que Shot2 no invente wire schemas. Son documentación ejecutable propuesta; no se compilaron ni enviaron durante Shot1.

## Contenido

### E1. Fuente y alcance

Tipos efectivos en xKoRx/echo@b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce: v3/sdk/contracts/strategy_ingestion_v2.go, strategy_history_v2.go, identity.go y v2_common.go. Receipt real: v3/sdk/postgres/strategy_history_v2_service.go, **IngestionReceiptV2**. Ejemplo de integración existente: v3/gateway/internal/lab_v4_gateway_test.go; su hash de definición repetido de fixture no debe copiarse como evidencia válida tras cerrar B3.

El siguiente generador usa esos tipos, computa hashes reales y emite un fixture NUM sin Magic, sin Q, sin órdenes ni fills. El movimiento económico sintético está declarado como tal y no acredita Forge. Instalar el instrumento NQ únicamente en catálogo del harness propio. HARNESS_PRODUCER_REF debe ser el principal autorizado por el harness. Ejecutar desde el módulo SDK candidato, guardar el programa y outputs en workspace externo de prueba; no insertar este programa en código productivo por obligación.

### E2. Generador de POST y oráculo de identidad

~~~go
package main

import (
    "encoding/json"
    "fmt"
    "os"

    "github.com/xKoRx/echo/v3/sdk/contracts"
)

func must(err error) { if err != nil { panic(err) } }
func declared(s string) contracts.TimeEvidenceV2 {
    return contracts.TimeEvidenceV2{State: "DECLARED", Value: s}
}
func main() {
    writer := os.Getenv("HARNESS_PRODUCER_REF")
    if writer == "" { panic("HARNESS_PRODUCER_REF propio requerido") }
    source := json.RawMessage("{\"dataset_kind\":\"NUM\",\"case_id\":\"E04-E08\"}")
    sourceDigest, err := contracts.DigestTagged("echo-design-fixture.v1", source)
    must(err)
    vd := contracts.VersionDefinitionV2{
        IdentityRecipe: "definition-v1", TargetPlatform: "ANALYTIC",
        ConstructionAt: "2026-01-01T00:00:00Z",
        ConstructionDataCutoff: "2025-12-31T00:00:00Z",
        AvailableAt: "2026-01-02T00:00:00Z",
        Package: contracts.VersionPackageV2{
            DefinitionManifest: json.RawMessage("{\"kind\":\"analytic\",\"fixture\":\"NUM\"}"),
        },
    }
    vd.Package.DefinitionSHA256, err = vd.DefinitionContentDigest()
    must(err)
    versionRef, err := vd.ComputeVersionRef("num-ingestion-v2-01")
    must(err)
    vd.DeclaredVersionRef = versionRef
    h := contracts.HistoryInputV2{
        SchemaVersion: contracts.SchemaStrategyHistoryV2,
        HistoryID: "num-history-01", SourceKind: contracts.SourceKindOtherDeclared,
        SourceInstanceRef: "num-producer-01", AccountAbsenceReason: "BACKTEST_DATASET",
        RunMode: contracts.RunModeBacktestV2, RunRef: "num-run-01",
        Role: contracts.RoleReferenceV2, ExpectedRevision: 0,
        TemporalMetadata: contracts.TemporalMetadataV2{
            ConstructionAt: declared(vd.ConstructionAt),
            ConstructionDataCutoff: declared(vd.ConstructionDataCutoff),
            AvailableAt: declared(vd.AvailableAt),
            EchoReferenceStartedAt: contracts.TimeEvidenceV2{
                State: "UNKNOWN", ReasonCode: "NOT_STARTED",
            },
        },
        Coverage: []contracts.CoverageIntervalV2{{
            From: "2025-06-01T00:00:00Z", To: "2025-06-03T00:00:00Z",
            State: "PARTIAL", Timezone: "UTC", EconomicTimePrecision: "INSTANT",
        }},
        Provenance: source,
        Operations: []contracts.OperationInputV2{{
            SourceOperationID: "num-cycle-1", Status: contracts.OpStatusClosedV2,
            InstrumentID: "NQ", Side: "LONG",
            OpenedAt: declared("2025-06-01T12:00:00Z"),
            CycleStartedAt: declared("2025-06-01T12:00:00Z"),
            ClosedAt: declared("2025-06-02T12:00:00Z"),
            Granularity: contracts.GranularityClosedSummaryV2,
            ClosedSummary: &contracts.ClosedSummaryV2{
                Net: contracts.MoneyV2{
                    Amount: "40", Currency: "USD", CurrencyStatus: "DECLARED",
                },
                CostDisclosure: contracts.CostDisclosureV2{
                    NetBasis: "PARTIAL_NET", Commission: "UNKNOWN", Fee: "UNKNOWN",
                    Swap: "UNKNOWN", OtherCosts: "UNKNOWN",
                },
            },
            Exposure: contracts.ExposureV2{State: "FLAT"},
            MissingFields: []string{"qi", "cost_evidence"},
        }},
    }
    req := contracts.StrategyIngestionV2{
        SchemaVersion: contracts.SchemaStrategyIngestionV2,
        ProducerRef: writer, ExternalStrategyRef: "num-external-01",
        Strategy: contracts.StrategyRegistrationV2{
            CanonicalStrategyID: "num-ingestion-v2-01", StrategyRef: "",
            DisplayName: "NUM ingestion contract", InstrumentIDs: []string{"NQ"},
            Direction: contracts.DirectionLongV2, Timeframe: "",
        },
        VersionDefinition: vd, Histories: []contracts.HistoryInputV2{h},
        OperationalRequest: &contracts.OperationalRequestV2{
            Mode: contracts.OperationalModeRegisterOnly, ExpectedBindingRevision: 0,
        },
        Provenance: contracts.IngestionProvenanceV2{Inputs: []contracts.NamedRef{{
            Role: "dataset", Ref: "num-fixture-01", SchemaVersion: "1",
            ContentDigest: sourceDigest,
        }}},
    }
    must(req.Validate())
    canonical, err := contracts.CanonicalJSONV2(req)
    must(err)
    requestDigest, err := contracts.CanonicalJSONV2Digest(canonical)
    must(err)
    must(os.WriteFile("request.json", canonical, 0600))
    oracle, err := json.Marshal(map[string]any{
        "dataset_kind": "NUM", "strategy_version_ref": versionRef,
        "definition_content_digest": vd.Package.DefinitionSHA256,
        "request_digest": requestDigest, "operation_count": 1, "movement_count": 0,
    })
    must(err)
    must(os.WriteFile("identity-oracle.json", oracle, 0600))
    fmt.Println("request.json e identity-oracle.json generados; ninguna red")
}
~~~

Este helper genera valores con SDK para construcción del request; **no sustituye el oráculo independiente de QA**. Para el fixture ASCII/strings anterior, recomputar H con SHA256 del array JSON compacto de strings [tag,fields...] y D con canonical JSON como un string; comparar contra identity-oracle sin importar helpers SDK. Para payload general aplicar el perfil wire completo, no asumir que cualquier json.dumps es canonical.

### E3. Intercambio HTTP y receipt

Tras preflight/guard C1, enviar request.json por POST /api/v2/strategy-ingestions con Authorization Bearer del harness, Content-Type application/json e Idempotency-Key num-ingest-01. Guardar status/headers/body como evidencia. No se ejecuta curl en este diseño.

| Response real / valor esperado | Verificación |
|---|---|
|202 inicial;200 replay | Mismo receipt_id y accepted_at tras GET/restart |
|schema_version | Constante emitida por IngestionReceiptV2 del SDK; cliente valida valor efectivo, no inventa otro DTO |
|acceptance | INGEST_ACCEPTED |
|request_digest | identity-oracle.json, mismo hash que bytes normalizados aceptados |
|strategy_ref | UUID asignado y misma fila crosswalk/registry |
|strategy_version_ref | versionRef recomputado |
|runtime_strategy_id | Crosswalk sv2 de B2 y strategy_definitions |
|histories[0] | history_id num-history-01, history_ref, revision1, digest de revisión, content_digest, operation_count1, movement_count0 |
|binding_ref | Ausente REGISTER_ONLY |
|operational | state NOT_REQUESTED, revision/observed_at del snapshot; nunca READY implícito |
|analytics | state ANALYTICS_PENDING aunque worker detenido; requested_profiles si aplican |
|links / Location | Rutas recuperables del mismo scope; GET-by-id y GET-by-key devuelven snapshot íntegro |

Readback físico: echo.strategy_ingestion_receipts por namespace/writer/key; strategy_identity_crosswalk y strategy_identity_mappings; strategy_versions o tabla de receta analítica efectiva identificada por registry SQL; strategy_definitions/runtime_strategy_links; histories/history_revisions/history_operations/history_movements e history_dirty_outbox. Resolver nombres exactos desde migraciones del candidate, no crear tablas para acomodar nombres de este texto. Verificar artifact path/digest por receipt y contenido; query independiente no llama a AcceptIngestionV2.

Negativos exactos: cambiar display_name conservando key→409; cambiar declared_version_ref→422; declarar digest de manifest incorrecto→422; duplicate key JSON→400; misma versión íntegra+historia nueva+key nueva reutiliza versión, no409. Variante sqx-v1 usa VersionPackageV2 real con cuatro hashes/executable/effective_inputs/dependencies y sus ArtifactRef verificados; no reemplazar la evidencia de ejecutable con manifest analítico para acreditar operación Forge. Este ejemplo ANALYTIC no certifica NATIVE_RUNTIME ni ejecución de estrategia.

### E4. Revisión N→N+1 sin inventar endpoint

Construir HistoryInputV2 completo desde h del ejemplo y receipt; ExpectedRevision=receipt.histories[0].revision, ExpectedDigest=receipt.histories[0].digest. Conservar HistoryID/source/run/account/role. Corrección NUM de40 a30:
1. oldDigest = h.Operations[0].OperationDigestV2().
2. operationRef = HashTaggedV2("echo-history-operation-id.v2", receipt.histories[0].history_ref, "num-cycle-1").
3. Cambiar sólo ClosedSummary.Net.Amount a "30"; calcular newDigest con OperationDigestV2.
4. Añadir Retractions con ChangeEntryV2{EntityRef: operationRef, Kind: "CORRECTION", PreviousRecordDigest: oldDigest, NewRecordDigest: newDigest, ReasonCode: "NUM_CORRECTION", SourceEvidenceRef: sourceDigest, EffectiveAt: "2025-06-02T12:00:00Z", KnownAt: "2026-01-03T00:00:00Z"}.
5. Serializar DTO completo y PUT /api/v2/strategy-versions/{version_ref}/histories/num-history-01 con nueva key num-history-correction-01 e If-Match igual expected digest.

Esperar revisión2 íntegra, N1=40 conservada y N2=30; replay key devuelve receipt2 aunque head avance. Dos PUT distintos expected1: uno gana y otro412, sin movimientos mezclados; falta precondición428. No modificar paquete StrategyVersion. Campos wrapper de metadata nuevos se describen en B3 y aún no existen en baseline; no usarlos antes del incremento E.

### E5. Binding/readiness — solicitud compatible y delta explícito

Después de integrar E y completar O, con profile propio resuelto por B5:
~~~json
{
  "mode": "PROVISION_REFERENCE",
  "deployment_profile_ref": "harness-observe-01",
  "expected_binding_revision": 0,
  "reference_account_id": "harness-reference-01",
  "run_id": "harness-run-01",
  "source_instance_ref": "harness-provider-01",
  "execution_accounts": [],
  "target_consumers": ["CORE:observer-01", "BRIDGE:reference-01"]
}
~~~

Estos nombres de campos ya se aceptan en lab_v4_gateway.go; los valores son sólo identifiers sintéticos del profile propio. El resolver TARGET obliga coincidencia, no confía en ellos. La grafía kind/id de target debe corresponder al enum de consumidores que implemente B6, con normalización única; no copiar el ejemplo para inventar consumers ausentes. Idempotency-Key num-binding-01, namespace/writer de auth. POST a /api/v2/strategy-versions/{version_ref}/operational-bindings, guardar binding_ref/revision/digest y consultar /api/v2/operational-bindings/{binding_ref}/readiness.

Retener consumer antes de apply: PROVISIONING aun con outbox publicado. Apply+checkpoint+ACK exactos de todos: ECHO_OPERATIONAL_READY. Retener renew hasta lease expira: DEGRADED. Slot/source/Magic ambiguo o ausencia de certificado: bloqueo explícito, nunca número ficticio. Para ANALYTIC sin capacidad externa autorizada, profile debe rechazar incompatibilidad; fixture operacional requiere estrategia/executable/evidencia correspondientes, no un cambio de etiqueta.

Este ejemplo no fabrica JSON de ACK desde producer: ACK lo emite el consumidor real tras lookup del estado aplicado. Es el caso que debe probar O02, no una petición manual que convierta desired en READY.


## Fuentes

- Mandato Owner 2026-10-26; [[F — Decision Register]] D25/D26.
- [[A — Source Baseline and Branch Integration]] contiene los SHAs y localizadores efectivos.
- Contratos compatibles de `10-projects/Echo/The Lab/V4 — Runtime Integration/` y [[Echo + Echo Forge — Environment Contract]].
