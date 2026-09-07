---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
cssclasses:
  - wide
---
# Diagrama visual — Entidades y persistencia de Echo Forge

## Propósito

- Representación visual de referencia de las entidades de Echo Forge, sus relaciones y cómo se persisten a medida que el pipeline madura (control plane / result plane / artifacts).

## Contenido

Te dejo una versión **bien visual** de cómo yo veo las entidades, cómo se relacionan y cómo se van guardando a medida que el pipeline madura.

La idea base hoy es esta:

- **PostgreSQL** = control plane: identidad, lifecycle, decisiones, estado operacional.
    
- **MongoDB** = result plane: métricas, evidencia, comparaciones y resultados versionados.
    
- **MinIO** = artifacts raw/binarios, **sin cambiar la estructura actual**.
    
- **MT5** es el **primer vertical slice** que valida esta arquitectura, pero sigue siendo un proyecto funcional separado.
    

---

## 1) Vista general: quién guarda qué

```mermaid
flowchart LR
    A[Symphony / Temporal<br/>orquesta la ejecución] --> B[PostgreSQL<br/>Control Plane]
    A --> C[MongoDB<br/>Result / Evidence Plane]
    A --> D[MinIO<br/>Artifacts]

    B --> B1[Identidad]
    B --> B2[Lifecycle]
    B --> B3[Estado operacional]
    B --> B4[Decisiones]

    C --> C1[Stage results]
    C --> C2[Métricas]
    C --> C3[Comparaciones]
    C --> C4[Scoring]
    C --> C5[Provenance]

    D --> D1[HTM MT5]
    D --> D2[MQ5 / EX5]
    D --> D3[Logs]
    D --> D4[Reportes / imágenes]
```

---

## 2) Entidades conceptuales: cómo se separa el dominio

El principio clave del proyecto es separar:

```text
IDENTIDAD ≠ EJECUCIÓN ≠ RESULTADO ≠ ARTEFACTO ≠ DECISIÓN
```

Eso está explicitado en el documento de arquitectura.

Visualmente:

```mermaid
flowchart TD
    S[Strategy identity<br/>strategy_id compuesto]
    E[Stage execution<br/>identidad lógica mínima<br/>por definir en G0]
    R[Stage result<br/>resultado versionado]
    A[ArtifactRef<br/>bucket + key + size + sha256]
    D[Decision / lifecycle<br/>PASS / REVIEW / INVALID / PROMOTED]

    S --> E
    E --> R
    R --> A
    R --> D
```

---

## 3) Lo que existe seguro hoy vs lo que sigue siendo hipótesis

### Confirmado hoy

```mermaid
flowchart TD
    S1[strategy_id compuesto]
    S2[wave_key separado]
    S3[ArtifactRef completo<br/>debe sobrevivir]
    S4[StageResult lógico<br/>versionado]
    S5[Resultados append-heavy]

    S1 --> S4
    S2 --> S4
    S3 --> S4
```

- `strategy_id` es compuesto y **no hay que redefinirlo como `wave_key + strategy_id`**.
    
- Los resultados deben ser **append-heavy**, no overwrite silencioso.
    
- El `ArtifactRef` debe conservar bucket/key/size/sha256.
    

### Todavía en hipótesis / gate G0

```mermaid
flowchart TD
    H1[pipeline_run]
    H2[stage_run]
    H3[attempt table]
    H4[colección única stage_results]
    H5[colecciones especializadas]

    G0[G0 / T0<br/>identity gate + baseline físico] --> H1
    G0 --> H2
    G0 --> H3
    G0 --> H4
    G0 --> H5
```

## Eso está declarado tal cual: **no ejecutar literalmente antes de G0** y no inventar IDs nuevos sin demostrar qué identidad representan.

## 4) Entidad mínima recomendada para pensar el pipeline

Aunque algunos nombres sigan abiertos, la película conceptual hoy es esta:

```mermaid
erDiagram
    STRATEGY {
        string strategy_id
        string canonical_name
        string symbol
        string timeframe
        string side
    }

    STAGE_EXECUTION {
        string stage_identity
        string stage
        string wave_key
        string run_id
        string variant
        string sample_type
        string status
    }

    STAGE_RESULT {
        string result_identity
        int schema_version
        string stage
        string status
        datetime created_at
    }

    ARTIFACT_REF {
        string type
        string bucket
        string object_key
        string sha256
        int size
        string content_type
    }

    DECISION {
        string decision_type
        string status
        string reason
        datetime created_at
    }

    STRATEGY ||--o{ STAGE_EXECUTION : produces
    STAGE_EXECUTION ||--o{ STAGE_RESULT : yields
    STAGE_RESULT ||--o{ ARTIFACT_REF : references
    STAGE_RESULT ||--o| DECISION : may_influence
```

---

## 5) Cómo se guarda hoy y cómo debería evolucionar

### Etapa inicial / legacy incómodo

```mermaid
flowchart TD
    A[strategy document mutable]
    B[WFM escribe]
    C[MT5 escribe]
    D[ranking escribe]
    E[history crece adentro]
    F[overwrite por wave_key + strategy_id]

    B --> A
    C --> A
    D --> A
    A --> E
    A --> F
```

Problemas detectados:

- overwrite de historia;
    
- múltiples writers sobre el mismo documento;
    
- arrays que crecen;
    
- confusión entre identidad y ejecución.
    

---

### Modelo objetivo incremental

```mermaid
flowchart TD
    S[strategy_id]
    EX1[stage execution WFM]
    EX2[stage execution MT5]
    EX3[stage execution reconciliation]

    R1[stage_result WFM]
    R2[stage_result MT5]
    R3[stage_result reconciliation]

    M1[(MongoDB)]
    P1[(PostgreSQL)]
    O1[(MinIO)]

    S --> EX1 --> R1 --> M1
    S --> EX2 --> R2 --> M1
    S --> EX3 --> R3 --> M1

    EX1 --> P1
    EX2 --> P1
    EX3 --> P1

    R1 --> O1
    R2 --> O1
    R3 --> O1
```

---

## 6) Evolución temporal: cómo crece la historia

Esta es probablemente la parte más importante.

### A. Una strategy entra por primera vez

```mermaid
flowchart LR
    S[strategy_id]
    W1[WFM execution #1]
    R1[result v1]
    M[(Mongo)]
    P[(Postgres)]

    S --> W1
    W1 --> R1
    W1 --> P
    R1 --> M
```

---

### B. Retry técnico: NO debe crear una nueva evaluación lógica

```mermaid
flowchart LR
    P1[Postgres<br/>RUNNING]
    M1[Mongo<br/>RESULT existe]
    RY[Retry Temporal]
    P2[Postgres<br/>COMPLETED + result_ref]

    P1 --> RY
    M1 --> RY
    RY --> P2
```

Ese recovery dual-store está declarado como requisito de T1A.

---

### C. Nueva evaluación deliberada: SÍ crea nueva historia

```mermaid
flowchart LR
    S[strategy_id]
    E1[MT5 execution #1]
    R1[mt5_result v1]
    E2[MT5 execution #2<br/>reevaluación]
    R2[mt5_result v2]

    S --> E1 --> R1
    S --> E2 --> R2
```

No se pisa `R1`. Ambos resultados coexisten. Esa es la gracia del modelo append-heavy.

---

## 7) Qué se persiste por store, de forma súper concreta

```mermaid
flowchart LR
    subgraph PG[PostgreSQL]
        PG1[estado operacional]
        PG2[lifecycle]
        PG3[decisiones]
        PG4[relaciones aprobadas por G0]
    end

    subgraph MG[MongoDB]
        MG1[mt5 result]
        MG2[wfm result]
        MG3[reconciliation result]
        MG4[metrics]
        MG5[scoring components]
        MG6[provenance]
    end

    subgraph MI[MinIO]
        MI1[mt5-export.htm]
        MI2[mq5]
        MI3[ex5]
        MI4[logs]
        MI5[reportes]
    end
```

---

## 8) Primer vertical slice real: MT5

Lo que se quiere lograr primero es esto:

```mermaid
flowchart TD
    A[MT5 HTM en MinIO]
    B[Parser UTF-16LE fail-closed]
    C[MT5 normalized result]
    D[Reconciliation SQX vs MT5]
    E[Shadow scoring]
    F[Calibración]
    G[Enforce]

    A --> B --> C --> D --> E --> F --> G
```

Con gates:

- parser correcto;
    
- fixture con trades reales;
    
- scoring solo en `shadow`;
    
- `enforce` solo tras aprobación humana.
    

---

## 9) Roadmap visual: en qué orden aparecen las entidades “durables”

```mermaid
flowchart TD
    T0[T0 / G0<br/>descubrir identidad real]
    T1A[T1A<br/>contrato lógico mínimo<br/>+ ArtifactRef + recovery]
    T1B[T1B<br/>MT5 vertical slice shadow]
    T2[T2<br/>generalizar contrato]
    T3[T3<br/>migrar WFM / robustness / SQX]
    T4[T4<br/>hardening]

    T0 --> T1A --> T1B --> T2 --> T3 --> T4
```

Ese orden está explicitado en el proyecto de arquitectura.

---

## 10) Mi lectura práctica: qué entidades “vas a terminar teniendo”

Si lo bajo a lo más probable, sin dogmatismo arquitectónico, yo apostaría a terminar con algo así:

### En PostgreSQL

- `strategies` **o equivalente aprobado por G0**
    
- entidad operacional mínima para stage execution
    
- estado/lifecycle
    
- decisiones (`PASS`, `REVIEW`, `INVALID`, `PROMOTED`)
    
- referencias hacia evidencia
    

### En MongoDB

- `stage_results` **o varias colecciones especializadas**
    
- payloads versionados:
    
    - `wfm`
        
    - `mt5_backtest`
        
    - `mt5_reconciliation`
        
    - `ranking`
        
- `strategy_summary` o proyección de lectura, pero **solo después** y nunca como fuente histórica única.
    

### En MinIO

- exactamente tu estructura actual
    
- con indexación por DB vía `ArtifactRef`.
    

---

## 11) Resumen ultra corto

```mermaid
flowchart TD
    S[strategy_id compuesto]
    X[ejecución lógica de stage]
    R[resultado versionado]
    A[artifact ref]
    D[decisión]
    H[historia acumulada]

    S --> X --> R --> A
    R --> D
    R --> H
```

### En español simple:

- **`strategy_id`** identifica la strategy.
    
- Cada **stage** genera una o más **ejecuciones lógicas**.
    
- Cada ejecución lógica produce un **resultado versionado**.
    
- Cada resultado puede apuntar a uno o más **artefactos**.
    
- Las **decisiones** se apoyan en esos resultados.
    
- La **historia no se pisa**: se acumula.
    

---

Si quieres, en la siguiente te hago una **segunda versión más pro**, tipo:

1. **diagrama C4-ish**,
    
2. **ERD más serio**, y
    
3. **timeline visual “antes / durante / después de MT5”**.
    

Esa ya quedaría pa pegarla directo en tu vault, bien ricarda y sin olor a PowerPoint corporativo.
