---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[ECHO-FUTURES-RUNTIME-POOL-DESIGN]]"
  - "[[Echo Futures — Runtime Pools]]"
aliases:
  - "S02 W0 Contract Freeze"
  - "Runtime Pools Contract Freeze v1"
tags:
  - kind/doc
created: "2026-10-16"
updated: "2026-10-16"
---

# S02-W0 — Congelación de contratos Runtime Pools (T2.1)

**WORKER:** W0 — CONTRATOS. ROLE=NORMAL, SURFACE=LOCAL, MODEL=GLM local one-shot (GLM-5.3-Flash).
**AUTORIDAD:** R6 = `ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §§12–18 (G1 accepted). **BASE_SHA producto:** `xKoRx/echo@d74b652500e673fc2bf4289f9f195f11960ba26e`, branch `feature/ef-runtime-pools`, worktree verificado limpio y en HEAD exacto (lectura only, cero escritura de producto, cero tests de producto, cero red).
**ALCANCE:** este documento congela contratos v1 que W1–W6 copian literalmente. Todo ítem cita su sección R6 de origen. Lo no cubierto por R6 queda marcado `OPEN_QUESTION(n)` con propuesta, para escalamiento del submanager; W0 no declara PLAN_CONFLICT por su cuenta.
**Convención de nombres:** `NEW` = no existe en HEAD (verificado); `EXTEND` = adición additive a un tipo HEAD citado; `REUSE` = símbolo HEAD citado sin cambio funcional. Los mensajes nuevos llevan `schema_version:1`, IDs estables, validación estructural; sin reloj, random ni session_id NT como identidad lógica (R6 §12B).

---

## 1. Tipos Go normativos NEW/EXTEND

### 1.1 `config.PoolDef` NEW — fuente R6 §12B (tabla), §14

Archivo destino: `v3/sdk/futures/config/snapshot.go` (EXTEND, mapa §15 "Config / EXTEND").

```go
// PoolDef NEW (R6 §12B/§14): catálogo de cuentas de un pool. No duplica
// saldo, fase, economics ni credenciales: sólo identidad de membresía.
type PoolDef struct {
	ID         string   `json:"id"`
	AccountIDs []string `json:"account_ids"`
}

// Validate enforces the pool catalog shape (R6 §12B/§14).
func (p PoolDef) Validate() error {
	if p.ID == "" {
		return fmt.Errorf("futuresruntime: pool requires an id")
	}
	if strings.Contains(p.ID, ":") {
		return fmt.Errorf("futuresruntime: pool id %q must not contain ':'", p.ID)
	}
	if len(p.AccountIDs) == 0 {
		return fmt.Errorf("futuresruntime: pool %s requires at least one account_id", p.ID)
	}
	seen := map[string]bool{}
	for _, a := range p.AccountIDs {
		if a == "" {
			return fmt.Errorf("futuresruntime: pool %s has an empty account_id", p.ID)
		}
		if seen[a] {
			return fmt.Errorf("futuresruntime: pool %s lists account %s twice", p.ID, a)
		}
		seen[a] = true
	}
	return nil
}
```

### 1.2 `config.PoolAssociationDef` NEW — fuente R6 §12B (tabla), §14

```go
// PoolAssociationDef NEW (R6 §12B/§14): Pool + Strategy configurada +
// MM/config. El ID es INMUTABLE: cambiar pool o strategy bajo el mismo id
// es error de composición (R6 §12B: "ID inmutable. Cambiar pool/Strategy
// bajo mismo ID es error"); MM nuevo sólo prospectivo, conservando las
// versiones antiguas referidas por Operation.
type PoolAssociationDef struct {
	ID            string `json:"id"`
	PoolID        string `json:"pool_id"`
	StrategyID    string `json:"strategy_id"`
	MMConfigID    string `json:"mm_config_id"`
	ConfigVersion int64  `json:"config_version"`
	Enabled       bool   `json:"enabled"`
}

// Validate enforces the association shape; referential checks against
// pools/strategies/money_managers/accounts run in ConfigSnapshot.Validate.
func (a PoolAssociationDef) Validate() error {
	if a.ID == "" || a.PoolID == "" || a.StrategyID == "" || a.MMConfigID == "" {
		return fmt.Errorf("futuresruntime: pool association requires id, pool_id, strategy_id and mm_config_id")
	}
	if strings.Contains(a.ID, ":") {
		return fmt.Errorf("futuresruntime: pool association id %q must not contain ':'", a.ID)
	}
	if a.ConfigVersion < 1 {
		return fmt.Errorf("futuresruntime: pool association %s requires config_version >= 1", a.ID)
	}
	return nil
}

// ValidateAssociationIdentity NEW: inmutabilidad del id de asociación entre
// versiones del snapshot (R6 §12B). Se invoca al comparar la configuración
// previa persistida con la nueva; un mismo id con otro pool o strategy
// FALLA la composición (no se reasigna).
func ValidateAssociationIdentity(prev, next []PoolAssociationDef) error {
	byID := map[string]PoolAssociationDef{}
	for _, a := range prev {
		byID[a.ID] = a
	}
	for _, n := range next {
		if p, ok := byID[n.ID]; ok {
			if p.PoolID != n.PoolID || p.StrategyID != n.StrategyID {
				return fmt.Errorf("futuresruntime: pool association %s is immutable: pool/strategy changed from (%s,%s) to (%s,%s)",
					n.ID, p.PoolID, p.StrategyID, n.PoolID, n.StrategyID)
			}
		}
	}
	return nil
}
```

`ConfigSnapshot` EXTEND (R6 §12B, primera fila de la tabla) — campos additive:

```go
// ConfigSnapshot additions (R6 §12B/§14; ilustrativo §14, no desplegable):
Pools            []PoolDef                    `json:"pools"`
PoolAssociations []PoolAssociationDef         `json:"pool_associations"`
MoneyManagers    map[string]GerardMMDef       `json:"money_managers"`    // id -> GerardMMDef íntegro (§14)
ProviderRuleSets map[string]ProviderDef       `json:"provider_rulesets"` // clave "ruleset_id@version" (§12B)
```

`AccountDef` EXTEND (R6 §12B): `CreatedAt time.Time `json:"created_at,omitempty"``, `CreatedAtSourceRef string `json:"created_at_source_ref,omitempty"``, `ProgramTerms *domain.AccountProgramTerms `json:"program_terms,omitempty"``. Ausencia ⇒ `ACCOUNT_CREATION_UNKNOWN`, inelegible; no fabricar antigüedad (R6 §12B). Validación agregada en `ConfigSnapshot.Validate`: referencias cruzadas (pool↔accounts del catálogo, asociación↔pool/strategy/money_managers/strategies, unicidad de ids, dos aliases lógicos hacia la misma cuenta física inválidos — R6 §12A párrafo de catálogo y §14).

Legacy: sin `pools` el snapshot conserva forma HEAD (cfg.MM/cfg.Provider); pool incompleto NO se mapea silenciosamente a globals (R6 §14).

### 1.3 `pool.PoolState` NEW — fuente R6 §12B (tabla PoolState), §12A, §4.6, §12C

Archivo destino: `v3/sdk/futures/pool/state.go` (create, mapa §15 "Pool / NEW"). Reducer puro: SIN tipos monetarios (R6 §12B/§15 "selección sin tipos monetarios").

```go
// Package pool: reducer puro del owner echo/pool_manager (R6 §12A/§15).
// Sólo selección/turnos/hechos versionados; sin PnL, sin kernels financieros
// (R6 §12 párrafo de corrección de responsabilidad).
package pool

// PoolPhase es el ciclo de turno por asociación (R6 §12B:
// IDLE → CLAIMING → INSTALLING → ACTIVE → DRAINING → RELEASING → IDLE).
type PoolPhase string

const (
	PoolPhaseIdle       PoolPhase = "IDLE"
	PoolPhaseClaiming   PoolPhase = "CLAIMING"
	PoolPhaseInstalling PoolPhase = "INSTALLING"
	PoolPhaseActive     PoolPhase = "ACTIVE"
	PoolPhaseDraining   PoolPhase = "DRAINING"
	PoolPhaseReleasing  PoolPhase = "RELEASING"
)

// PoolState es el keyed state completo de echo/pool_manager para un pool_id
// (R6 §12B fila PoolState). JSON serializable, restart-safe.
type PoolState struct {
	PoolID        string `json:"pool_id"`
	ConfigVersion int64  `json:"config_version"`
	// Associations: estado de turno por asociación (R6 §12B "mapa por
	// asociación"). Clave = PoolAssociationDef.ID.
	Associations map[string]*AssociationTurn `json:"associations"`
	// ProcessedDayBoundaries: fronteras account-day ya procesadas por
	// cuenta (R6 §12B "fronteras account-day ya procesadas"; §4.7: persistir
	// la frontera para que un reinicio no duplique el cambio diario).
	// Clave = execution_account_id, valor = último account_day_id procesado.
	ProcessedDayBoundaries map[string]string `json:"processed_day_boundaries,omitempty"`
}

// AssociationTurn es el turno de UNA asociación: máximo una candidata
// pendiente y una cuenta activa; ninguna segunda activa mientras drena
// (R6 §12B; §1 "Un turno activo": máximo un destino activo y una
// reclamación pendiente por asociación).
type AssociationTurn struct {
	AssociationID        string    `json:"association_id"`
	AssignmentGeneration int64     `json:"assignment_generation"`
	Phase                PoolPhase `json:"phase"`
	// Candidate es la reclamación pendiente (0..1) y Active la cuenta
	// activa (0..1). Candidate != nil sólo en CLAIMING/INSTALLING;
	// Active != nil en ACTIVE/DRAINING; jamás dos cuentas con exposición
	// simultáneas para la misma asociación (R6 §12B/§16.2).
	Candidate *TurnCandidate `json:"candidate,omitempty"`
	Active    *TurnCandidate `json:"active,omitempty"`
	// PendingRequestID: solicitud claim/release en vuelo; un crash
	// reenvía/consulta la MISMA solicitud (R6 §12D.7).
	PendingRequestID string `json:"pending_request_id,omitempty"`
	// LastFactRevision per cuenta: última revisión de hechos consumida
	// (R6 §12B "última revisión de hechos por cuenta").
	// Clave = execution_account_id, valor = revision_seq aceptado.
	LastFactRevision map[string]int64 `json:"last_fact_revision,omitempty"`
	// WaitCause: causa de espera visible (R6 §12B "causa de espera");
	// p.ej. NO_ELIGIBLE_ACCOUNT, ACCOUNT_FACTS_UNAVAILABLE, DRAIN_PENDING.
	WaitCause string `json:"wait_cause,omitempty"`
}

// TurnCandidate identifica una cuenta en turno (sin montos).
type TurnCandidate struct {
	AccountID            string `json:"account_id"`
	AccountStrategyID    string `json:"account_strategy_id"`
	ClaimEpoch           int64  `json:"claim_epoch"`
	AssignmentGeneration int64  `json:"assignment_generation"`
	RequestID            string `json:"request_id"`
}
```

Invariantes que `pool.Engine` valida en cada transición (R6 §16.2): ≤1 claim activo por cuenta; ≤1 ACTIVE por asociación; ninguna segunda activa mientras DRAINING; `RELEASING` sólo con ACK de release del provider (R6 §12D.7).

### 1.4 `pool.AccountClaim` NEW + `provider.OwnerState` EXTEND — fuente R6 §12B (fila provider.OwnerState), §12A, §12D.1/3

Archivo destino: struct en `v3/sdk/futures/pool/contracts.go` (create); campos additive en `v3/sdk/futures/provider/state.go` (EXTEND, mapa §15).

```go
// AccountClaimPhase es el ciclo del claim en el owner account-wide
// (R6 §12B "Claim{...,phase}"; §12D.1–3).
type AccountClaimPhase string

const (
	ClaimProvisional AccountClaimPhase = "PROVISIONAL" // excluye competidores aunque aún no haya afinidad (R6 §12B)
	ClaimConfirmed   AccountClaimPhase = "CONFIRMED"   // provider confirmó; pendiente instalación
	ClaimActive      AccountClaimPhase = "ACTIVE"      // instalación ACK'd; new-risk habilitado (R6 §12D.2)
	ClaimRevoked     AccountClaimPhase = "REVOKED"     // tombstone: epoch conservado, afinidad conservada (R6 §12D.7)
)

// AccountClaim es el claim durable que provider persiste atómicamente con
// su respuesta egress (R6 §12D.1). Campos exactos R6 §12B.
type AccountClaim struct {
	PoolID               string            `json:"pool_id"`
	AssociationID        string            `json:"association_id"`
	StrategyID           string            `json:"strategy_id"`
	AccountStrategyID    string            `json:"account_strategy_id"`
	RequestID            string            `json:"request_id"`
	AssignmentGeneration int64             `json:"assignment_generation"`
	ClaimEpoch           int64             `json:"claim_epoch"`
	Phase                AccountClaimPhase `json:"phase"`
}
```

`provider.OwnerState` EXTEND — campos nuevos, additive (R6 §12B):

```go
// --- Runtime pools additions (R6 §12B) ---
// AffinityStrategyID: afinidad permanente por Strategy configurada (ID),
// fijada ATÓMICAMENTE al primer permiso de nueva exposición (R6 §12B y
// §12D.3). Nunca se borra por release, cambio de día, phase ni reset
// normal (R6 §12B). Afinidad por strategy_id, no por módulo/programa/MM.
AffinityStrategyID string `json:"affinity_strategy_id,omitempty"`
// OriginAssociationID: asociación de origen, AUDITIVO (R6 §12B:
// "OriginAssociationID auditivo"). NO es una segunda regla de afinidad
// (R6 §12B).
OriginAssociationID string `json:"origin_association_id,omitempty"`
// Claim: claim provisional/activo vigente. Un claim PROVISIONAL ya
// excluye competidores aunque aún no haya afinidad (R6 §12B).
Claim *pool.AccountClaim `json:"claim,omitempty"`
// ClaimEpoch: contador durable que provider INCREMENTA por cada nuevo
// claim (R6 §12B "provider incrementa epoch durable por nuevo claim";
// §12D.1 "retry de la misma solicitud no crea otro epoch"). Epochs
// liberados conservan tombstone (R6 §12D.7).
ClaimEpoch int64 `json:"claim_epoch"`
// AccountAvailability: proyección tipada de hechos económicos/reglas/
// política MM hacia PoolManager (ver 1.5).
AccountAvailability *pool.AccountAvailability `json:"account_availability,omitempty"`
// FenceEpoch: máximo epoch revocado publicado en el stream M1 por la
// Operation y persistido por el bridge antes de ACK (R6 §12D.5).
FenceEpoch int64 `json:"fence_epoch,omitempty"`
// DrainEvidence: última evidencia de drenaje lógico recibida de la
// Operation para el epoch en curso (R6 §12D.6).
DrainEvidence *pool.DrainEvidence `json:"drain_evidence,omitempty"`
// PhysicalDrainEvidence: última evidencia física del bridge (R6 §12D.6).
PhysicalDrainEvidence *pool.PhysicalDrainEvidence `json:"physical_drain_evidence,omitempty"`
```

Semántica congelada (citada, no nueva): (i) la afinidad se fija con el primer permiso de exposición y se conserva aunque el submit sea rechazado o no produzca fill (R6 §12D.3); (ii) claim provisional excluye competidores (R6 §12B); (iii) `AccountAvailability` con estado PAUSED permanece account-wide bajo su policy/versión de origen aunque cambie asociación/MM — cambiar asociación nunca elude una pausa efectiva (R6 §12C); (iv) `RiskState.Breached` nunca se limpia por reloj (R6 §12C).

### 1.5 `pool.AccountAvailability` NEW — fuente R6 §12B (fila AccountAvailability), §12C

```go
// AccountAvailabilityState (R6 §12B):
// ELIGIBLE/PAUSED/TERMINAL/UNKNOWN. Stale/ausente ⇒ UNKNOWN para nueva
// exposición; la gestión física continúa (R6 §12B; §12C).
type AccountAvailabilityState string

const (
	AvailabilityEligible AccountAvailabilityState = "ELIGIBLE"
	AvailabilityPaused   AccountAvailabilityState = "PAUSED"
	AvailabilityTerminal AccountAvailabilityState = "TERMINAL"
	AvailabilityUnknown  AccountAvailabilityState = "UNKNOWN"
)

// AccountAvailability es el hecho versionado que Provider agrega desde
// revisión contable autorizada + reglas + trust/readiness + política MM
// (R6 §12B). SIN MONTOS para PoolManager (R6 §12B: "sin montos").
type AccountAvailability struct {
	AccountID string `json:"account_id"`
	// ContextID: identidad por (account, context) (R6 §12B "account/context
	// IDs"; §12C cambio de contexto vía AccountContextUpdate atómico).
	ContextID string `json:"context_id,omitempty"`
	// RevisionSeq: revisión MONOTÓNICA por cuenta/contexto (R6 §12B
	// "Revisión monotónica por cuenta/contexto"). Payload distinto con el
	// mismo revision_seq ⇒ CONFLICTO (R6 §12B; ver §4 negativos).
	RevisionSeq int64  `json:"revision_seq"`
	SourceRef   string `json:"source_ref"`
	AccountDayID string `json:"account_day_id"`
	// PolicyConfigID/Version: identidad de la política MM que originó el
	// hecho, cuando derive de MM (R6 §12B "policy_config_id/version y
	// association scope cuando el hecho derive de MM"; §12C "ALLOW calculado
	// para MM-X no autoriza automáticamente MM-Y").
	PolicyConfigID      string `json:"policy_config_id,omitempty"`
	PolicyConfigVersion int64  `json:"policy_config_version,omitempty"`
	AssociationScope    string `json:"association_scope,omitempty"`
	State               AccountAvailabilityState `json:"state"`
	Reason              string `json:"reason,omitempty"`
	// Authority: autoridad que produce el hecho (reglas/programa, política
	// MM, trust) — el campo identifica la fuente dominante (R6 §12B
	// "autoridad"; §12C combinación: terminal domina, pausa económica
	// impide entradas, falta de trust ⇒ UNKNOWN).
	Authority string `json:"authority"`
	DecisionID string `json:"decision_id"`
	// ResumeBoundary: frontera de reanudación explícita; ver
	// OPEN_QUESTION(2) sobre su tipo exacto.
	ResumeBoundary string `json:"resume_boundary,omitempty"`
	ObservedAt     time.Time `json:"observed_at"`
}
```

Regla de consumo: respuesta con scope distinto no habilita el claim; una pausa ya efectiva permanece account-wide bajo su policy/versión de origen hasta que ESA autoridad la reanude tras SU frontera (R6 §12C).

### 1.6 Mensajes idempotentes NEW — fuente R6 §12B (fila AccountTurn*/AssignmentControl), §12D, §13

Archivo destino: `v3/sdk/futures/pool/contracts.go` (create). Idempotencia congelada: repetición EXACTA de una solicitud devuelve el resultado anterior; generación obsoleta no revive turno (R6 §12B "Mensajes idempotentes... Repetición exacta devuelve resultado anterior; generación obsoleta no revive turno").

```go
// AccountTurnClaim (R6 §12D.1): solicitud de turno que el PoolManager
// envía a echo/provider_rules(key=execution_account_id). ClaimEpoch NO
// viaja: provider lo asigna durablemente por nuevo claim (R6 §12B).
type AccountTurnClaim struct {
	SchemaVersion        int    `json:"schema_version"` // 1
	RequestID            string `json:"request_id"`
	AccountID            string `json:"account_id"`
	PoolID               string `json:"pool_id"`
	AssociationID        string `json:"association_id"`
	StrategyID           string `json:"strategy_id"`
	AccountStrategyID    string `json:"account_strategy_id"`
	MMConfigID           string `json:"mm_config_id"`
	MMConfigVersion      int64  `json:"mm_config_version"`
	AssignmentGeneration int64  `json:"assignment_generation"`
}

// AccountTurnOutcome (R6 §12D.1: "Un loser recibe
// ACCOUNT_ALREADY_CLAIMED/AFFINITY_MISMATCH"; §12C elegibilidad).
type AccountTurnOutcome string

const (
	TurnConfirmed        AccountTurnOutcome = "CONFIRMED"
	TurnAlreadyClaimed   AccountTurnOutcome = "ACCOUNT_ALREADY_CLAIMED"
	TurnAffinityMismatch AccountTurnOutcome = "AFFINITY_MISMATCH"
	TurnIneligible       AccountTurnOutcome = "INELIGIBLE"
	TurnAborted          AccountTurnOutcome = "ABORTED"
	TurnReleased         AccountTurnOutcome = "RELEASED"
)

// AccountTurnResult: respuesta explícita del provider (R6 §12B "resultado
// explícito"). Repetición exacta del claim re-emite el MISMO ClaimEpoch y
// resultado (R6 §13.4: "Claim repetido idéntico devuelve mismo epoch").
type AccountTurnResult struct {
	SchemaVersion      int                `json:"schema_version"` // 1
	RequestID          string             `json:"request_id"`
	AccountID          string             `json:"account_id"`
	Outcome            AccountTurnOutcome `json:"outcome"`
	ClaimEpoch         int64              `json:"claim_epoch"`
	AffinityStrategyID string             `json:"affinity_strategy_id,omitempty"`
	DecisionID         string             `json:"decision_id"`
	Reason             string             `json:"reason,omitempty"`
}

// AccountTurnRelease (R6 §12D.5–7): revocación con barrera. ExpectedClaimEpoch
// es el fencing token: un release con epoch distinto al vigente no toca el
// turno (R6 §12B "expected claim epoch"). La variante PROVISIONAL_ABORT
// es el abort de un claim provisional: requiere ACK del provider ANTES de
// probar otra cuenta (R6 §12B; §12D.1).
type AccountTurnRelease struct {
	SchemaVersion        int    `json:"schema_version"` // 1
	RequestID            string `json:"request_id"`
	AccountID            string `json:"account_id"`
	PoolID               string `json:"pool_id"`
	AssociationID        string `json:"association_id"`
	ExpectedClaimEpoch   int64  `json:"expected_claim_epoch"`
	AssignmentGeneration int64  `json:"assignment_generation"`
	ReleaseReason        string `json:"release_reason"` // DAILY_PAUSE|TERMINAL|DAY_BOUNDARY|PROVISIONAL_ABORT|ASSOCIATION_DISABLED
	Drain                *DrainEvidence `json:"drain_evidence,omitempty"`
}

// AccountTurnReleaseResult (R6 §12D.6–7: provider confirma el release del
// claim exacto conservando tombstone y afinidad; sólo tras ese ACK el
// PoolManager inicia otro claim).
type AccountTurnReleaseResult struct {
	SchemaVersion int    `json:"schema_version"` // 1
	RequestID     string `json:"request_id"`
	AccountID     string `json:"account_id"`
	Released      bool   `json:"released"`
	ClaimEpoch    int64  `json:"claim_epoch"`
	DecisionID    string `json:"decision_id"`
	Reason        string `json:"reason,omitempty"`
}

// AssignmentAction (R6 §12D.2: instalar binding efectivo/MM/AssignmentControl
// en Operation; §12D.4: revocación invalida admissions/deferred OPEN del
// epoch, no los retargetea).
type AssignmentAction string

const (
	AssignmentInstall    AssignmentAction = "INSTALL"
	AssignmentInvalidate AssignmentAction = "INVALIDATE"
)

// MMConfigRef identifica el módulo/config sellada de la asociación
// (R6 §12C: "el claim identifica MM/config/version de la asociación").
type MMConfigRef struct {
	MMModule      string `json:"mm_module"` // gerardmm | tgmm
	MMConfigID    string `json:"mm_config_id"`
	ConfigVersion int64  `json:"config_version"`
}

// AssignmentControl (R6 §12D.2): instalación/invalidación del binding
// efectivo en echo/operation para el epoch dado.
type AssignmentControl struct {
	SchemaVersion        int              `json:"schema_version"` // 1
	RequestID            string           `json:"request_id"`
	AccountID            string           `json:"account_id"`
	AccountStrategyID    string           `json:"account_strategy_id"`
	PoolID               string           `json:"pool_id"`
	AssociationID        string           `json:"association_id"`
	StrategyID           string           `json:"strategy_id"`
	ClaimEpoch           int64            `json:"claim_epoch"`
	AssignmentGeneration int64            `json:"assignment_generation"`
	Action               AssignmentAction `json:"action"`
	MM                   MMConfigRef      `json:"mm_ref"`
	RuleSetRef           string           `json:"ruleset_ref,omitempty"` // "ruleset_id@version"
}

// AssignmentControlAck (R6 §12D.2: "Operation ACK incluye
// config/contexto/generación... Provider recibe confirmación de
// instalación; sólo entonces habilita new-risk").
type AssignmentControlAck struct {
	SchemaVersion        int              `json:"schema_version"` // 1
	RequestID            string           `json:"request_id"`
	AccountID            string           `json:"account_id"`
	AccountStrategyID    string           `json:"account_strategy_id"`
	ClaimEpoch           int64            `json:"claim_epoch"`
	AssignmentGeneration int64            `json:"assignment_generation"`
	Action               AssignmentAction `json:"action"`
	Outcome              AccountTurnOutcome `json:"outcome"` // CONFIRMED | ABORTED(stale) | INELIGIBLE(unknown claim)
	ConfigDigest         string           `json:"config_digest,omitempty"`
	Reason               string           `json:"reason,omitempty"`
}

// TargetMode (R6 §12B fila AssociationTargetUpdate: modo
// "OPEN_ENABLED/MANAGE_ONLY/NO_TARGET").
type TargetMode string

const (
	TargetOpenEnabled TargetMode = "OPEN_ENABLED"
	TargetManageOnly  TargetMode = "MANAGE_ONLY"
	TargetNoTarget    TargetMode = "NO_TARGET"
)

// AssociationTargetUpdate (R6 §12B; §4.4: un solo versionador del conjunto
// completo por Strategy combina cambios de varios pools; ningún pool envía
// un FanoutTargetSet parcial que borre destinos ajenos). Fanout aplica por
// asociación, rechaza versión vieja y versiona internamente el set
// completo (R6 §12B).
type AssociationTargetUpdate struct {
	SchemaVersion        int        `json:"schema_version"` // 1
	PoolID               string     `json:"pool_id"`
	AssociationID        string     `json:"association_id"`
	StrategyID           string     `json:"strategy_id"`
	AssignmentGeneration int64      `json:"assignment_generation"`
	ClaimEpoch           int64      `json:"claim_epoch"`
	ConfigVersion        int64      `json:"config_version"`
	Mode                 TargetMode `json:"mode"`
	AccountID            string     `json:"account_id,omitempty"`          // vacío en NO_TARGET
	AccountStrategyID    string     `json:"account_strategy_id,omitempty"` // vacío en NO_TARGET
	InstrumentID         string     `json:"instrument_id,omitempty"`
	MM                   MMConfigRef `json:"mm_ref,omitempty"`
}

// AssociationTargetUpdateAck (R6 §12B "rechaza versión vieja y versiona
// internamente el set completo").
type AssociationTargetUpdateAck struct {
	SchemaVersion        int                `json:"schema_version"` // 1
	AssociationID        string             `json:"association_id"`
	StrategyID           string             `json:"strategy_id"`
	AssignmentGeneration int64              `json:"assignment_generation"`
	ClaimEpoch           int64              `json:"claim_epoch"`
	ConfigVersion        int64              `json:"config_version"`
	Outcome              AccountTurnOutcome `json:"outcome"`
	Reason               string             `json:"reason,omitempty"`
}
```

### 1.7 `pool.DrainEvidence` / `pool.PhysicalDrainEvidence` NEW — fuente R6 §12B (última fila), §12D.5–6, §5 drenaje

```go
// DrainEvidence (R6 §12B/§12D.6): Operation emite drenaje lógico SOLO sin
// admission/deferred entry, sin órdenes con efecto posible, sin exposición
// lógica ni acciones pendientes (R6 §12D.6). NO basta un booleano flat ni
// timeout (R6 §12B); PoolManager/Provider no fabrican finalidades (R6 §5).
type DrainEvidence struct {
	AccountID     string `json:"account_id"`
	ContextID     string `json:"context_id,omitempty"`
	ClaimEpoch    int64  `json:"claim_epoch"`
	// OperationOwnerSeq: owner input seq de echo/operation al emitir
	// (R6 §12B "operation owner seq").
	OperationOwnerSeq int64 `json:"operation_owner_seq"`
	// CommandFrontier: frontier de comandos M1 publicados (R6 §12B
	// "command frontier"; el fence se publica DESPUÉS de todos los
	// comandos previos, R6 §12D.5).
	CommandFrontier int64 `json:"command_frontier"`
	// UnresolvedCounts: contadores que DEBEN ser cero para que la evidencia
	// sea válida (R6 §12B "unresolved counts").
	UnresolvedCounts DrainUnresolvedCounts `json:"unresolved_counts"`
	// EvidenceRefs: referencias durables de las decisiones/hechos que
	// componen la conjunción (R6 §12B "evidence refs").
	EvidenceRefs []string `json:"evidence_refs"`
}

type DrainUnresolvedCounts struct {
	Admissions         int64 `json:"admissions"`          // pendientes
	DeferredEntries    int64 `json:"deferred_entries"`    // deferred OPEN del epoch
	OrdersWithPossibleEffect int64 `json:"orders_with_possible_effect"`
	LogicalExposureContracts int64 `json:"logical_exposure_contracts"` // unidades, NO dinero
	PendingActions     int64 `json:"pending_actions"`     // cancel/replace en vuelo del epoch
}

// PhysicalDrainEvidence (R6 §12D.6): bridge emite SÓLO después del fence,
// recovery barrier vigente, journal sin SUBMITTING/AMBIGUOUS/pendiente,
// reconciliación sin órdenes ajenas no resueltas ni posición pendiente y
// frontier completo (R6 §12B "bridge barrier ID, reconciliation
// generation").
type PhysicalDrainEvidence struct {
	AccountID       string `json:"account_id"`
	PhysicalBinding string `json:"physical_binding"`
	ClaimEpoch      int64  `json:"claim_epoch"`
	// FenceEpoch: fence vigente que esta evidencia cubre (R6 §12D.6).
	FenceEpoch int64 `json:"fence_epoch"`
	// RecoveryBarrierID: identidad de la recovery barrier vigente
	// (RunRecoveryBarrier, HEAD v3/futures-bridge/internal/session/session.go).
	RecoveryBarrierID string `json:"recovery_barrier_id"`
	// ReconciliationGeneration (R6 §12B).
	ReconciliationGeneration int64 `json:"reconciliation_generation"`
	UnresolvedCounts PhysicalDrainUnresolvedCounts `json:"unresolved_counts"`
	Frontier         int64 `json:"frontier"` // frontier completo (R6 §12D.6)
	EvidenceRefs     []string `json:"evidence_refs"`
}

type PhysicalDrainUnresolvedCounts struct {
	JournalSubmitting   int64 `json:"journal_submitting"`
	JournalAmbiguous    int64 `json:"journal_ambiguous"`
	JournalPending      int64 `json:"journal_pending"`
	ForeignOrdersUnresolved int64 `json:"foreign_orders_unresolved"`
	PendingPosition     int64 `json:"pending_position"`
}
```

Provider verifica además reservas/finalidad/capacity y facts causales que cubran el fence; cualquier UNKNOWN o discrepancia mantiene DRAINING; sin TTL liberador ni inferencia de cancel-ACK como finality (R6 §12D.6).

### 1.8 `SignalDelivery` / `AccountStrategyTarget` EXTEND — fuente R6 §12B (fila EXTEND), §4.5, §12D.3

`v3/sdk/futures/domain/fanout.go` (SignalDelivery) y `v3/sdk/futures/strategy/fanout.go` (AccountStrategyTarget), adición idéntica en ambos:

```go
// Runtime-pools routing (R6 §12B): opcionales. AUSENCIA = binding legacy
// fijo; NUNCA fallback a pool (R6 §12B "ausencia significa binding legacy,
// nunca pool fallback"; §8 "Pool-managed exige metadata/guards completos").
AssociationID        string `json:"association_id,omitempty"`
AssignmentGeneration int64  `json:"assignment_generation,omitempty"`
ClaimEpoch           int64  `json:"claim_epoch,omitempty"`
```

Semántica: destino sellado por delivery; el copy de una señal antigua no cambia generación (R6 §12B). `DeliveryDedupKey` HEAD (`account_strategy_id:signal_id`) queda intacto; el dedup por asociación al rotar añade el guard de decisión por asociación descrito en R6 §4 (conservar `(run, strategy_eval_seq, signal_seq)`/SignalID y destino fijado). La restricción `AccountStrategyID` sin `:` se mantiene (Validate HEAD `domain/fanout.go:35-37`); el ID derivado (1.9) es hex y no contiene `:`.

### 1.9 `DeriveAccountStrategyID` NEW (derivado) — fuente R6 §12B (fila AccountStrategy efectivo), §3

Archivo destino: `v3/sdk/futures/pool/contracts.go`. Sigue EXACTAMENTE el patrón de `domain.DeriveSignalID` (HEAD `v3/sdk/futures/domain/signal.go:125-142`): SHA-256, campos length-prefixed (uint64 big-endian) bajo tag de dominio, hex; sin `:`.

```go
// DeriveAccountStrategyID deriva el ID estable de la AccountStrategy
// efectiva pool-managed: hash length-prefixed SHA-256 de
// (account_id, association_id) bajo tag de dominio, sin ':' (R6 §12B:
// "ID derivado por hash length-prefixed (account_id,association_id) sin
// ':'"; §3: ID estable entre turnos de esa cuenta/asociación; no se
// configura manualmente).
func DeriveAccountStrategyID(accountID, associationID string) (string, error) {
	if accountID == "" || associationID == "" {
		return "", fmt.Errorf("pool: account strategy id requires account_id and association_id")
	}
	if strings.Contains(accountID, ":") || strings.Contains(associationID, ":") {
		return "", fmt.Errorf("pool: account strategy id components must not contain ':'")
	}
	h := sha256.New()
	write := func(fields ...string) {
		for _, f := range fields {
			var l [8]byte
			binary.BigEndian.PutUint64(l[:], uint64(len(f)))
			_, _ = h.Write(l[:])
			_, _ = h.Write([]byte(f))
		}
	}
	write("echo.futures.account_strategy_id.v1", accountID, associationID)
	return hex.EncodeToString(h.Sum(nil)), nil
}
```

No se mueve Operation/MMState al siguiente ID entre turnos (R6 §12B fila EXTEND).

### 1.10 Contrato puro `operation.AccountPolicy` NEW — fuente R6 §12C ("Política MM diaria"), §12F

Archivo destino: `v3/sdk/futures/operation/account_policy.go` (create, mapa §15 "MM / EXTEND").

```go
// AccountPolicyDecision (R6 §12C: "salida tipada
// ALLOW/PAUSE_UNTIL_BOUNDARY/COMPLETE/UNAVAILABLE, reason/decision_id y
// boundary explícita").
type AccountPolicyDecision string

const (
	PolicyAllow              AccountPolicyDecision = "ALLOW"
	PolicyPauseUntilBoundary AccountPolicyDecision = "PAUSE_UNTIL_BOUNDARY"
	PolicyComplete           AccountPolicyDecision = "COMPLETE"
	PolicyUnavailable        AccountPolicyDecision = "UNAVAILABLE"
)

// AccountPolicyInput (R6 §12C: "Input: cuenta/contexto, AccountEconomics,
// RuleSet/terms, config MM sellada, account-day/frontera y observaciones
// analíticas requeridas").
type AccountPolicyInput struct {
	AccountID string `json:"account_id"`
	ContextID string `json:"context_id,omitempty"`
	StageID   string `json:"stage_id,omitempty"`
	// AccountDayID + DayBoundary: identidad del día comercial y frontera
	// del binding (sin UTC global ni medianoche de servidor, R6 §5/§12C).
	AccountDayID string    `json:"account_day_id"`
	DayBoundary  time.Time `json:"day_boundary"`
	Economics    AccountEconomics
	// RuleSet/Terms: autoridad de reglas y términos de programa.
	RuleSet          domain.ProviderRuleSet
	RuleSetAvailable bool
	Terms            *domain.AccountProgramTerms
	// MMConfig: config MM sellada de la asociación (MMConfigSnapshot).
	MMConfig map[string]string `json:"mm_config"`
	// Analytics: vista causal fijada para ESTA evaluación (misma disciplina
	// de corte que MMInput.Analytics, HEAD v3/sdk/futures/operation/mm.go).
	Analytics          tgk.View
	AnalyticsInstalled bool
}

// AccountPolicyOutcome: decisión tipada publicable al provider (R6 §12C:
// "publica la misma decisión tipada/revisión al provider; éste deduplica
// contra el mismo policy evaluation, nunca deduce daily target desde
// TerminationIntent genérico").
type AccountPolicyOutcome struct {
	Decision   AccountPolicyDecision `json:"decision"`
	Reason     string                `json:"reason"`
	DecisionID string                `json:"decision_id"`
	// Boundary: frontera de reanudación explícita para
	// PAUSE_UNTIL_BOUNDARY (ver OPEN_QUESTION(2)).
	Boundary    string `json:"boundary,omitempty"`
	RevisionSeq int64  `json:"revision_seq,omitempty"`
	SourceRef   string `json:"source_ref,omitempty"`
}

// AccountPolicy es el contrato PURO por cuenta implementado por cada MM
// soportado en pool (R6 §12C). Determinista para el mismo input ordenado;
// sin I/O. Se invoca DENTRO del owner provider, por revisión contable/
// frontera, AUN SIN Operation activa (R6 §12C); su estado diario vive por
// cuenta/contexto/config, separado del MMState de Operation (R6 §12C).
type AccountPolicy interface {
	EvaluateAccount(in AccountPolicyInput) (AccountPolicyOutcome, error)
}
```

Constantes de política de presupuesto (R6 §12F): `gerardmm.EntryBudgetUnclippedV1 = "MM_ENTRY_BUDGET_UNCLIPPED_V1"` (literal también en `TGMMDef.EntryBudgetPolicy`, HEAD ya tiene el campo JSON `entry_budget_policy` en `config/snapshot.go:118`). Semántica EXACTA §12F:

- **GerardMM** (HEAD `v3/sdk/futures/gerardmm/gerardmm.go`, `computeEconomics`: `e.effectiveBudget = ratMin(headrooms...)` con `ownerRemaining` + `HardMonetaryHeadroom` de economics + `HardMonetaryHeadroom` del RuleSet): la política elimina SÓLO el clamp `min(...)` contra el piso externo (`HardMonetaryHeadroom`); se conserva la fórmula MM de presupuesto/objetivo (`remaining = max(0, TP−P)`, `ownerRemaining = min(SL, max(0, SL+P))`), discretización, costes y reglas no relacionadas (R6 §12F).
- **TGMM** (HEAD `v3/sdk/futures/strategies/tgmm/tgmm.go`, `Evaluate` rama `if risk.Cmp(head) > 0` y `requestedBudget(pending)`): `requestedBudget(pending)` sigue determinando R/T; con la política se omite EXCLUSIVAMENTE la rama que compara con `headroom` para recortar/rechazar (R6 §12F).
- Casos cerrados R6 §12F: `R=300, floor_remaining=53` conserva R=300; `R=1000, floor_remaining=1` conserva R=1000. No implica cantidad fraccionaria ejecutable ni tamaño sobre límites del venue (R6 §12F).
- `TG_ENTRY_BUDGET_EXCEEDS_HEADROOM` / `LOST_ENTRY_BUDGET_BY_POLICY` son semántica legacy publicada (R3@95e9d10, R6 §7): `STRATEGIC_ENTRY_BUDGET_V1` no cambia de significado (R6 §12F); campo `entry_budget_policy` ausente conserva legacy fuera de pools; pool EXIGE la política explícita (R6 §12F). Política MM desconocida o módulo sin soporte falla composición (R6 §12F).
- Breach real independiente: al cruzar piso real el provider aplica sus reglas vigentes; la pausa económica ya efectiva sigue vigente aunque haya presupuesto (R6 §12F). `TG_CYCLE_OBJECTIVE_OR_SIGNAL`, cierre técnico y `MM_NO_ACTION` NO son daily pause (R6 §12C).

### 1.11 `analytics.AnalyticsObservation` NEW — fuente R6 §12E (párrafo 4)

Archivo destino: `v3/sdk/futures/analytics/observations.go` (create, mapa §15 "Analytics / REUSE + EXTEND").

```go
// AnalyticsObservation (R6 §12E): observación tipada con corte causal;
// market_analytics la emite hacia Operation/provider subscribers;
// consumidores sólo guardan read models (R6 §12E).
type AnalyticsObservation struct {
	ObservationID  string    `json:"observation_id"`
	StreamID       string    `json:"stream_id"`
	ContractID     string    `json:"contract_id"`
	RequirementKey string    `json:"requirement_key"`
	CloseBoundary  time.Time `json:"close_boundary"`
	Revision       int64     `json:"revision"`
	AuthorityEpoch int64     `json:"authority_epoch"`
	PublishedAt    time.Time `json:"published_at"`
	// Frontier: corte causal cubierto (cut at/seq del view, HEAD
	// analytics/tg/view.go Frontier()).
	CutAt  time.Time `json:"cut_at"`
	CutSeq int64     `json:"cut_seq"`
	// Payload/availability: payload calculado O marcador de disponibilidad
	// (R6 §12E "payload calculado/availability"). Ausencia nunca se
	// convierte en indicador cero (R6 §12E).
	Payload           json.RawMessage `json:"payload,omitempty"`
	Available         bool            `json:"available"`
	UnavailableReason string          `json:"unavailable_reason,omitempty"`
}
```

Contrato de corte causal (R6 §12E): en cada decisión Signal/quote/fill/economics se fija el cut causal y sólo valen observaciones publicadas y cubiertas por ese cut; NO se elige automáticamente "la última" tras un retry — el observation_id del input admitido se PERSISTE. Fill y capacidad se aplican siempre; si falta analytics, MM inhibe sólo las acciones que lo requieren y conserva reducciones independientes (R6 §12E). Nota HEAD verificada: `analytics.Engine.applyRequirements` HOY reemplaza demandas (`st.Demands = demands`), W4 debe extenderlo a unión por subscriber/config_version (R6 §12E).

---

## 2. Constantes StateFun a añadir (W6)

Fuente R6 §12A (`echo/pool_manager` nuevo), §12B (mensajes nuevos), §15 ("Wiring schemas / EXTEND": `v3/sdk/statefun/futures_constants.go`). Convención HEAD del archivo: `FnType*` = `TypeNameFrom("echo/<name>")`, `*Type` = `MakeJsonType("echo.types/<name>")`, topics `echo.<name>.v1`.

```go
// Nuevo function type (R6 §12A):
FnTypeFuturesPoolManager = statefun.TypeNameFrom("echo/pool_manager") // key = pool_id

// Nuevos JSON record types (R6 §12B; nombres espejan los structs §1):
FuturesPoolStateType                   = MakeJsonType("echo.types/futures_pool_state")
FuturesPoolConfigUpdateType            = MakeJsonType("echo.types/futures_pool_config_update")        // R6 §15 composición: main publica config por ingress SDK
FuturesAccountTurnClaimType            = MakeJsonType("echo.types/futures_account_turn_claim")
FuturesAccountTurnResultType           = MakeJsonType("echo.types/futures_account_turn_result")
FuturesAccountTurnReleaseType          = MakeJsonType("echo.types/futures_account_turn_release")
FuturesAccountTurnReleaseResultType    = MakeJsonType("echo.types/futures_account_turn_release_result")
FuturesAssignmentControlType           = MakeJsonType("echo.types/futures_assignment_control")
FuturesAssignmentControlAckType        = MakeJsonType("echo.types/futures_assignment_control_ack")
FuturesAssociationTargetUpdateType     = MakeJsonType("echo.types/futures_association_target_update")
FuturesAssociationTargetUpdateAckType  = MakeJsonType("echo.types/futures_association_target_update_ack")
FuturesAccountAvailabilityType         = MakeJsonType("echo.types/futures_account_availability")
FuturesDrainEvidenceType               = MakeJsonType("echo.types/futures_drain_evidence")
FuturesPhysicalDrainEvidenceType       = MakeJsonType("echo.types/futures_physical_drain_evidence")
FuturesAnalyticsObservationType        = MakeJsonType("echo.types/futures_analytics_observation")
```

- **NO se requieren topics ni egress nuevos.** El audit trail de claim/affinity/pause/target/drain viaja por los canales existentes (R6 §17 "Egress auditable en canales existentes"; los outcomes de provider son `ProviderDecisionFact` → `echo.futures.provider-events.v1`, HEAD `provider/effects.go`). Si un worker necesita un topic/egress nuevo, es delta de mapa → escalar al Manager (§15).
- **El EXTEND de `SignalDelivery`/`AccountStrategyTarget` NO requiere type nuevo**: JSON additive sobre `echo.types/futures_signal_delivery` y el target-set existente (campos `omitempty`; HEAD ya reserva el nombre).
- `module.yaml` (source): declarar los nuevos tipos en el ingress del source y los ValueSpecs del nuevo owner `echo/pool_manager` + extensiones de `echo/provider_rules`; sólo declaraciones, sin aplicar manifests (R6 §15 "Wiring schemas / EXTEND").

---

## 3. Matriz de identidad/routing (R6 §12A)

Propietario StateFun → key → mensajes que acepta (v1 congelada; EXTEND = additive a los ya aceptados en HEAD):

| Propietario (TypeName) | Key | Mensajes existentes (HEAD) | Mensajes NEW/EXTEND v1 | Responsabilidad (R6 §12A) |
|---|---|---|---|---|
| `echo/market_stream`, `echo/market_analytics` | stream canónico `instrument_id:contract_id` | sin cambio | — (AnalyticsObservation viaja de analytics hacia subscribers; no se ingresa aquí como input) | Feed, barras, unión de demandas, observaciones causales (§12A; §12E) |
| `echo/strategy_engine` | `strategy_id` | sin cambio | — | Evaluación única; Signal y cycle_seq intactos (§12A) |
| `echo/signal_fanout` | `strategy_id` | Signal, FanoutTargetSet | **NEW** `AssociationTargetUpdate`; emite `AssociationTargetUpdateAck` | Único serializador de targets combinados por asociación; no selecciona cuentas (§12A/§12B) |
| `echo/pool_manager` **NEW** | `pool_id` | — | `PoolConfigUpdate` (config bootstrap); `AccountTurnResult`, `AccountTurnReleaseResult` (de provider); `AssignmentControlAck` (de operation); `AssociationTargetUpdateAck` (de fanout); hechos de frontera account-day y disponibilidad proyectados por provider | Estado de turnos por asociación, FIFO, claim/release, retorno diario, proyección de destino (§12A) |
| `echo/provider_rules` | `execution_account_id` canónico | AdmissionRequest, ExposureReservationRequest, ReservationRevalidate, Release, CapacityUpdate, RuleSet, Binding, Account, Instrument, AccountContextUpdate, ClockFired (HEAD `provider/input.go`) | **NEW** `AccountTurnClaim`, `AccountTurnRelease`; **NEW** ingestión de revisión contable autorizada (`accounting.Revision` proyectada a `provider.EconomicObservation`) y fronteras de día; **NEW** `DrainEvidence`, `PhysicalDrainEvidence`; **NEW** `AssignmentControlAck` (instalación confirmada); emite `AccountTurnResult/ReleaseResult`, `AccountAvailability` | Exclusividad global, afinidad durable, fencing, admisión/reservas, lifecycle; ÚNICO lugar que confirma claim y liberación (§12A/§12C/§12D) |
| `echo/operation` | `account_id:account_strategy_id` | SignalDelivery, fact families | **NEW** `AssignmentControl` (INSTALL/INVALIDATE); emite `AssignmentControlAck`, `DrainEvidence`; delivery EXTEND con routing opcional | Admisión/pending-next-cycle, MMState aislado, evidencia de drenaje, MM por binding sellada (§12A/§12D) |
| Futures bridge / M2 | `execution_account_id` + `physical_binding` | comandos por cuenta, observaciones | fence M1 ordenado por cuenta + máximo epoch revocado persistido antes de ACK; emite `PhysicalDrainEvidence`; `CommandData` ya porta `physical_binding`+`provider_account_ref` (HEAD `ntx/frame.go`) | Gateway físico, journal/reconciliación, barrera; sin política económica (§12A/§12D.5–6) |

Identidad adicional (R6 §12A): `ExecutionAccountID` → `ProviderAccountBinding` → `(transport_id, provider_account_ref, physical_binding)`; unicidad validada en config agregada; dos aliases lógicos a la misma cuenta física = inválido; la misma cuenta en dos pools llega a la MISMA key del provider; exclusividad exige un único runtime StateFun autorizado por cuenta física (gate de egress lo comprueba).

---

## 4. Negativos estructurales (DEBEN fallar `Validate` o el guard de composición)

Oráculo: 2–4 casos inválidos por contrato, fail-closed (R6 §14 "Defecto estructural impide composición"; §16).

| Contrato | Caso inválido | Fallo esperado |
|---|---|---|
| `PoolDef` | account_ids vacío / duplicado / id con `:` | `PoolDef.Validate` error |
| `PoolAssociationDef` | `config_version < 1`; `pool_id` inexistente en `pools`; `strategy_id`/`mm_config_id` no configurados; mismo association id con otro pool/strategy vs snapshot previo | `Validate` / `ConfigSnapshot.Validate` / `ValidateAssociationIdentity` error (R6 §12B/§14) |
| Config | dos aliases lógicos hacia la misma cuenta física (mismo `provider_account_ref`+`physical_binding` en dos accounts) | error de composición ANTES de habilitar ejecución (R6 §12A; §13.4) |
| `PoolState` | dos cuentas Active en una asociación; Candidate fuera de CLAIMING/INSTALLING; transición a RELEASING sin ACK de release | invariante del reducer (R6 §12B/§16.2) |
| `AccountClaim` | `ClaimEpoch == 0` en claim persistido; `Phase` vacía/desconocida; `AccountStrategyID` vacío o con `:` | error estructural del claim (R6 §12B/§12D.1) |
| `AccountAvailability` | mismo `revision_seq` con payload distinto ⇒ CONFLICTO (no absorción silenciosa); estado fuera del enum; `decision_id`/`source_ref` vacíos; montos presentes (prohibidos) | conflicto tipado / `Validate` (R6 §12B) |
| `AccountTurnClaim` | `request_id` vacío; `assignment_generation < 1`; `mm_config_version < 1`; accountStrategyID ≠ derivado de (account, association) | `Validate` (R6 §12B/§12C) |
| `AccountTurnRelease` | `expected_claim_epoch` distinto al vigente (no toca turno); `release_reason` desconocida; release DRAINING sin DrainEvidence con counts en cero | fencing/guard del provider (R6 §12B/§12D.6) |
| `AssignmentControl` | acción desconocida; claim_epoch=0; MMConfigRef con módulo no registrado | `Validate`/composición (R6 §12D.2; §12F "política desconocida falla composición") |
| `AssociationTargetUpdate` | modo desconocido (≠ OPEN_ENABLED/MANAGE_ONLY/NO_TARGET); target no vacío en NO_TARGET; AccountStrategyID con `:`; config_version ≤ última aplicada por esa asociación (rechazo, no error de redelivery) | `Validate`/guard de fanout (R6 §12B) |
| `DrainEvidence` | cualquier `UnresolvedCounts` > 0 presentado como evidencia válida; claim_epoch ausente; evidence_refs vacío | el provider MANTIENE DRAINING / `Validate` (R6 §12D.6) |
| `PhysicalDrainEvidence` | fence_epoch no vigente; journal con SUBMITTING/AMBIGUOUS/pendiente > 0; reconciliation_generation sin barrier vigente | el provider MANTIENE DRAINING (R6 §12D.6) |
| `SignalDelivery` EXTEND | `claim_epoch`/`assignment_generation` presentes sin `association_id` (routing parcial); `association_id` vacía con generación > 0 | `Validate` additive (R6 §12B: ausencia=legacy, nunca mezcla) |
| `AccountPolicy` | decisión fuera del enum; PAUSE_UNTIL_BOUNDARY sin boundary; ALLOW con revisión contable ausente (debe ser UNAVAILABLE/`ECONOMICS_UNAVAILABLE`, R6 §12C) | `Validate`/fail-closed (R6 §12C) |
| `AnalyticsObservation` | payload y available=false simultáneos con unavailable_reason vacío; observation_id/close_boundary vacíos | `Validate` (R6 §12E) |

---

## 5. Spike P0-NT (read-only; 0 intentos de compile ejecutados)

**Precondición registrada:** en este host NO hay toolchain C# ni assemblies NinjaTrader (verificado por el submanager, planner "Evidencia S02" Paso 0). **Intentos de compile ejecutados: 0 de 2 permitidos** (T2.1/Paquete Fase 2). Evidencia separada en dos planos: contractual Go (leída) y C#/NT (AUSENTE).

### 5.1 Evidencia contractual (Go, HEAD d74b6525)

| # | Binding | Comando → cuenta | ACK | Fill → M2 (identidad) | Cancel/Replace | Reconnect | Evidencia HEAD |
|---|---|---|---|---|---|---|---|
| B1..B5 | una lane lógica por binding; hoy el AddOn resuelve UNA sola cuenta (`resolvedAccount`, AddOn.cs:64,855) y ntx.Server mantiene UNA `ActiveConn` por lane (server.go:97,184) con fencing de sesión (`session superseded`, server.go:270-273) | `CommandData` viaja por frame `command` con `PhysicalBinding`+`ProviderAccountRef`; el AddOn RECHAZA si `provider_account_ref != expectedAccountName` o drift (`ExecuteCommand`, AddOn.cs:535-565) | `command_result` ACCEPTED/REJECTED/ERROR con `command_id`+`nt_order_id` (frame.go:229-249); ACCEPTED ≠ venue binding (frame.go:224-228) | `ExecutionRecord{ExecutionID, OrderID, ClientOrderID}` (observations.go:78-87); fill dedup por `(execution_account_id, native provider_execution_id)` en `EventGate.Observe` (session/gate.go:88-100); correlación M2 por journal: `JournalCorrelationResolver` entrega `(operationID, orderID, accountStrategyID)` desde términos journalizados (gate.go:63-74; session.go handleSubmit) | CANCEL/REPLACE por `action_id`+`client_order_id`, NT `Change` in-place (AddOn.cs:676-715; frame.go:161-179); reductivos del epoch saliente siguen permitidos bajo fence (R6 §12D.5) | `RunRecoveryBarrier` conecta/auth/verify_binding/restore/journal (session.go:153-...); servidor hace fence de sesión vieja; guard `accountGuard` por sesión (session.go:327) | frame.go; server.go; observations.go; session.go; gate.go; bridge.go (SessionFactory por cuenta, bridge.go:24,58) |

Matriz command→account→ACK/fill→M2 exigida por R6 §15 (VERIFY): las 5 lanes se modelan con la identidad `(execution_account_id, physical_binding, operation_id, order_id, execution_id)`; hoy los tres primeros componentes existen en wire/journal (`CommandData.PhysicalBinding`, `session.Config.ExecutionAccountID`, `JournalRecord.Terms.OperationID/OrderID`) y los dos últimos en `ExecutionRecord.OrderID/ExecutionID`. **Brechas estructurales ya previstas por R6 §15** (trabajo W5, no hallazgo nuevo): (i) AddOn con `resolvedAccount` único y `expectedAccountName` único → requiere array de bindings/contexto per binding; (ii) main reutiliza un único listen-addr global → lane por binding con listener exclusivo; (iii) no multiplexar eventos sin identidad en socket compartido; feed canónico único (R6 §15 NT wire/AddOn).

### 5.2 Dictamen

- **PHYSICAL_NOT_DEMONSTRATED** para (a) compile del AddOn contra assemblies NT y (b) terminal/lanes reales: no hay toolchain ni assemblies en el host y no se ejecutó ningún intento (0/2). No se afirma que SIM pruebe NT (R6 §15; §18).
- Evidencia contractual Go: sí, leída y citada arriba (frame/server/session/gate/bridge). Reutilización confirmada de `Account.All/Submit/Cancel/Change` existentes; el diseño no depende de una API financiera nueva (R6 §15).
- Dato semántico imprescindible ausente: **ninguno identificado** en el plano contractual (identidad completa representable). La capacidad física concurrente de eventos/callbacks/reconnect sigue incertidumbre física a verificar (R6 §15). ⇒ **No se declara PLAN_CONFLICT desde W0**; el bloqueo físico queda reservado para G2/G4 (R6 §15/§18).

---

## 6. Interfaces compartidas inter-worker

Símbolos que cada worker consume de otro (fuente: §12B/§12D y matriz de workers del planner). Firma exacta = definiciones §1 de este documento.

| Consumidor | Proveedor | Símbolo/contrato compartido | Firma/uso exacto |
|---|---|---|---|
| W1 (pool/provider) | W0 | todos los tipos §1 | copia literal: `config.PoolDef`, `config.PoolAssociationDef`, `ValidateAssociationIdentity`, `pool.{PoolState,AssociationTurn,TurnCandidate,AccountClaim,AccountAvailability,...}`, mensajes §1.6, `DeriveAccountStrategyID`, `operation.AccountPolicy`, `analytics.AnalyticsObservation` |
| W1 (provider) | W1 mismo/W0 | ingestión contable | `provider.Input` EXTEND con revisión autorizada: `accounting.Revision` + identidad causal/contexto proyectada a `provider.EconomicObservation` (HEAD `risk_eval.go:25`) y fronteras de día (R6 §12C "Wiring cerrado"); ledger no se modifica en S02 salvo prueba de contrato insuficiente → Manager (R6 §15) |
| W2 (fanout) | W1 | API de claim/proyección | consume `pool.AssociationTargetUpdate` (aplica por asociación, rechaza versión vieja) y responde `pool.AssociationTargetUpdateAck`; extiende `domain.SignalDelivery`/`strategy.AccountStrategyTarget` con los 3 campos §1.8; cursor durable `(run_id, strategy_eval_seq, signal_seq)` (R6 §12E) |
| W3 (operation/MM) | W1/W2 | assignment + fence | consume `pool.AssignmentControl` (INSTALL/INVALIDATE) → emite `pool.AssignmentControlAck`; emite `pool.DrainEvidence` (sólo con conjunción completa); revalidación/admisión valida el tuple completo con `claim_epoch`/`assignment_generation` (R6 §12D.3) |
| W3 (MM) | W0/W1 | política por cuenta | implementa `operation.AccountPolicy` (gerardmm/tgmm account_policy.go); proyección `TGMMDef.EntryBudgetPolicy` = `MM_ENTRY_BUDGET_UNCLIPPED_V1` validando no contradicción con `GerardMMDef.entry_budget_policy` (R6 §12F) |
| W4 (analytics) | W0 | observación causal | emite `analytics.AnalyticsObservation`; extiende `applyRequirements` a unión de demandas por subscriber/config_version (R6 §12E); consumidores (W2/W3) nunca recomputan kernels |
| W5 (bridge/NT) | W1/W3 | fence/drain | recibe fence M1 ordenado por cuenta y persiste máximo epoch revocado antes de ACK (R6 §12D.5); emite `pool.PhysicalDrainEvidence` tras recovery barrier vigente (R6 §12D.6); `CommandData` sin cambios de esquema (ya porta binding identity) |
| W6 (composición) | W1–W5 | wiring | registra `FnTypeFuturesPoolManager` (key `pool_id`), los JSON types §2, ValueSpecs `echo/pool_manager` y extensiones `echo/provider_rules`; bootstrap idempotente de config; una sola WithSpec por TypeName con dispatcher (R6 §12A/§15) |
| W7 (QA) | todos | oráculos §4 y R6 §16 | negativos estructurales de §4 como tests de falsificación; sin modificar source productivo |

---

## OPEN_QUESTIONS (para escalamiento del submanager)

1. **OPEN_QUESTION(1)** — R6 §12F no dice si `MM_ENTRY_BUDGET_UNCLIPPED_V1` en TGMM exige el emparejamiento con `EconomicMinimumV2` que hoy exige `STRATEGIC_ENTRY_BUDGET_V1` (HEAD `tgmm.go:79-80`). *Propuesta W0:* exigir el mismo emparejamiento (el mínimo físico queda como restricción de admisión de cantidad entera bajo el presupuesto sin clip). Material para W3.
2. **OPEN_QUESTION(2)** — Tipo exacto de `ResumeBoundary` (R6 §12C "resume boundary" y §12B "resume boundary opcional"): R6 §12C prohíbe convertir timestamp en ALLOW y §5 exige frontera del día operativo del binding. *Propuesta W0:* `string` con `account_day_id` objetivo (identidad de frontera del calendario del binding), no wall-clock. Material para W1.
3. **OPEN_QUESTION(3)** — Granularidad de `PoolState.LastFactRevision` ("última revisión de hechos por cuenta", §12B): por `account_id` o por `(account_id, context_id)` dado que la disponibilidad es por (account, context). *Propuesta W0:* clave `(account_id, context_id)` serializada con `|`. Menor; decisión W1 con consistencia en `AccountAvailability`.

## UNVERIFIED

- Todo lo físico (§5): compile AddOn (0 intentos), terminal NT, lanes reales, capacidad concurrente de callbacks/reconnect.
- Propiedades de colisión del hash derivado (patrón establecido `DeriveSignalID`; sin tests ejecutados por W0).
- Ningún test de producto ejecutado; inspección de fuente only (§15/§18). Comportamiento de `go test` heredado: 5 fallos baseline documentados por el submanager (planner Paso 0), no reproducidos por W0.
- Comentarios C# del AddOn (p.ej. reflexión NT 8.1.8.3) no re-verificados: son evidencia histórica del AddOn, no prueba nueva.

## BLOCKERS

Ninguno. Sin PLAN_CONFLICT declarado: el mapa §15 cubre todos los archivos/creators referenciados; los datos semánticos del spike están representables en los contratos existentes.
