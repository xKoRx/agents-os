---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-05"
---

# BTG-S01-REAL-GERARD-RESULT

## Propósito

Conseguir el baseline histórico REAL de la Strategy Gerard exacta y GerardMM compartido, corregir defectos demostrados y entregar evidencia al Primary Manager para revisión. El submanager conserva continuidad; no acepta el gate Owner ni inicia S02.

## Contenido

### Estado observado

STATE = IN_PROGRESS — INVENTORY_AND_AUTHORITY_RESOLUTION
REAL_SMOKE = NOT_RUN
LONGITUDINAL_RUN = NOT_RUN
DETERMINISTIC_RERUN = NOT_RUN
ECONOMIC_STAGE_COVERAGE = NOT_DEMONSTRATED
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = NOT_MEASURED

El inventario previo del Primary es preparación documental; no acredita datos físicos ni una corrida. S00–S04 son ACCEPTED_INPUT para capacidades; D6, Generic20/GAU50 y simuladores previos son REFERENCE_ONLY. Otros runs permanecen UNREVIEWED.

### Autoridad recuperada y aislamiento

El paquete solicitado procede de `xKoRx/agents-os`, commit de rama documental `a16f4bb25cfb6882146f437f5913302a191313c2`, segundo padre del merge existente `d67319f0878610c786b94aa2ad31e5e4503e7efa`. La rama remota ya no aparece en `ls-remote`; su contenido existe en el checkout vigente. Esta sesión no ejecutó ni exigió el merge, ni alteró master. Evidencia nueva en rama `codex/btg-s01-evidence`; especialistas con ramas documentales propias y ownership disjunto. Sin intervención D6 ni cambios de infraestructura.

HEADs refrescados directamente por `git ls-remote` al inicio (2026-10-06 UTC, fecha local 2026-10-05):

| Autoridad | HEAD observado | Estado local |
| --- | --- | --- |
| Agents-OS master | `bb9fa98be22057e8468e83f72cb53fd147accc09` | limpio |
| Echo master | `372af59a7b83604781346613da01e3d510ea1360` | referencia remota |
| Backtester certificado | `cd451972b242c8933321e03001decd4b6d778c61` | worktree certificado limpio |
| D6 | `d08a30ce9815f820fda7132e20dc42cc345eb8e8` | referencia remota; intocado |

### Delegaciones en curso

- TOP LOCAL `gpt-6.1-sol`, ONE-SHOT: autoridad exacta de Strategy Gerard, configuración instalada y rows de GerardMM; producto read-only; resultado en [[BTG-S01-IDENTITY-CONFIG]].
- NORMAL LOCAL `gpt-6-luna`, ONE-SHOT: histórico físico, provenance, fidelidad, cobertura y boundary DatasetSource; originales intocados; resultado en [[BTG-S01-DATASET-INVENTORY]].

El harness expone ambos modelos. No expone una ejecución CLOUD Pro autónoma; las delegaciones presentes requieren inspección física LOCAL. Consumo confirmado Chat Pro = 0 (Codex). Cada worker debe registrar su segmento si aplica, feedback sólo ante fricción real y cierre ONE-SHOT; root no se autocierra.

### Findings y siguiente acción

No hay finding de producto adjudicado todavía. Resolver identidad/configuración y disponibilidad física antes de cualquier run certificatorio; después delegar el primer slice con warm-up suficiente. Si falta una decisión vigente, elevar sólo esa decisión y continuar trabajo independiente. No completar day3/FUNDED con importes arbitrarios ni mejorar rentabilidad cambiando señal o riesgo.

### Gaps para S02

Pendientes de inventario, sin inferencias económicas nuevas: unidad de `5k / 120k`; programa/prop/fees/settlement; stage config vigente; cuatro retiros netos cobrados y reinversión; preservar una cuenta operando a la vez salvo fuente posterior. S02 no iniciado.

## Fuentes

- [[BTG-PLAN]] y [[BTG-S01-SUBMANAGER-PROMPT]], commit de origen identificado arriba.
- [[Echo Futures]], autoridades master vigentes.
- [[Echo Futures — BT-S01 Backtester V1 Design]], enmiendas frozen.
- [[Echo Futures — BT-S04 Final Remediation and Certification]].
- [[Echo + Echo Forge — Environment Contract]], bootstrap y technical-project-manager.
