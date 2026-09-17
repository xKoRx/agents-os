# MANDATO DE IMPLEMENTACIÓN — NORMAL

## Polymarket Engine · M2-S01 Foundation

### ROL

Actúa como **Senior Go Engineer / NORMAL coding agent**.

La arquitectura y el plan de implementación ya están congelados.

Tu misión es implementar exclusivamente:

`M2-S01 — Foundation`

Este es el **primer slice productivo del Polymarket Engine**.

No rediseñes arquitectura.

No adelantes slices.

No investigues nuevamente Polymarket.

No implementes market data, recorder, SQLite, strategies ni trading.

Si una instrucción necesaria contradice el diseño frozen:

`BLOCKED — DESIGN ISSUE`

No improvises.

---

# 0. ENTORNO

Trabajas exclusivamente sobre recursos locales.

Agents-OS está sincronizado externamente de manera automática.

No uses GitHub como autoridad operacional.

No busques commits remotos ni realices operaciones de sincronización.

Resuelve el root local de Agents-OS mediante su bootstrap canónico mínimo.

## Autoridad de proyecto

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Lee únicamente lo necesario:

- decisiones frozen D-*;
    
- estado `M1_DESIGN_FROZEN`;
    
- `M2 — TOP Implementation Plan`;
    
- especialmente:
    
    - M2.0;
        
    - M2.1;
        
    - M2.2;
        
    - `M2-S01`;
        
    - políticas de entrega a NORMAL;
        
    - gates asociados a S01.
        

No recorras otros proyectos del vault.

No abras Echo, Echo Forge, Hermes ni memorias ajenas.

Technical Platform Map no debería ser necesario para S01 salvo referencia explícita del slice.

---

# 1. IMPLEMENTATION REPOSITORY

Producto:

`Polymarket Engine`

Go module:

`github.com/xKoRx/polymarket-engine`

Primero localiza un checkout local existente del repositorio bajo el workspace habitual.

Si ya existe, úsalo.

Si todavía no existe y Agents-OS / entorno local define una ruta canónica de repos externos, créalo allí.

Preferencia operacional si no existe otra autoridad local:

`~/go/src/github.com/xKoRx/polymarket-engine`

No pongas el código productivo dentro del vault de Agents-OS.

Antes de modificar:

1. resuelve la ruta real;
    
2. verifica si existe contenido previo;
    
3. comprueba estado local;
    
4. evita sobrescribir trabajo ajeno;
    
5. registra la ruta resuelta en el proyecto Agents-OS si aún figuraba `REQUIRES_OWNER — REPO LOCATION ONLY`.
    

---

# 2. TOOLCHAIN GO — DECISIÓN OPERATIVA CERRADA

Usar Go 1.27.

Baseline:

```text
go 1.27.0
toolchain go1.27.1
```

Si la máquina no tiene Go 1.27.1 pero el mecanismo estándar de toolchain de Go puede obtenerlo, úsalo.

No reduzcas la versión para acomodarte al host.

Corrige en el M2 plan cualquier referencia histórica/propuesta a:

`go 1.23`

para dejar Go 1.27 como baseline del proyecto.

No hagas otras modificaciones al plan.

---

# 3. SCOPE DEL SLICE

Implementa exclusivamente la foundation congelada para los slices posteriores.

Debe entregar:

## Repository bootstrap

Como mínimo:

```text
go.mod
cmd/engine/
internal/foundation/
internal/config/
internal/archtest/
migrations/
testdata/
```

No crees todos los paquetes futuros vacíos sólo porque aparecen en M2.1.

Créelos cuando corresponda a su slice.

El binario puede ser mínimo, pero debe compilar.

---

# 4. FOUNDATION CONTRACTS

Implementa en:

`internal/foundation`

los contratos base necesarios por M2.

## A. IDs nominales

No utilizar `string` intercambiable para IDs de namespaces distintos.

Materializa tipos separados al menos para los identificadores internos frozen que ya puedan definirse sin contratos wire específicos.

Ejemplos conceptuales:

```text
GammaEventID
GammaMarketID
ConditionRef
AssetKey
Order/Intent local identifiers where applicable
RevisionRef
ExperimentID
RunID
StrategyID
```

No inventes conversiones entre IDs.

No introduzcas parsing wire específico de Polymarket; corresponde a S02.

Constructores deben validar invariantes estructurales que sean independientes del protocolo wire.

---

## B. Protocol identity

Materializa unión cerrada conceptual:

```text
CTF
PROTOCOL_V2
UNKNOWN
```

No agregues codecs ni ABI.

No conviertas UNKNOWN automáticamente a ninguna versión.

---

## C. Decimal exacto y unidades

Implementa representación monetaria exacta encapsulada.

La librería concreta puede ser:

`github.com/shopspring/decimal`

pero **no debe escapar de foundation como contrato público del engine**.

Crear tipos nominales apropiados, según M1/M2, tales como:

```text
Price
Shares
CollateralAmount
BasisPoints
FeeCoefficient
```

y primitives necesarias.

Requisitos:

- no `float64` en decisiones monetarias;
    
- parsing decimal exacto;
    
- signo sólo donde corresponda;
    
- operaciones de suma/resta/comparación;
    
- escala explícita;
    
- representación canónica;
    
- serialización determinista;
    
- errores en overflow/invariant violations;
    
- cero no se usa como sustituto de unknown.
    

No implementes todavía las reglas de rounding específicas de órdenes Polymarket; corresponden a S02/protocol.

---

## D. RevisionRef

Implementa un identificador/referencia inmutable para snapshots/revisions.

Debe permitir posteriormente referenciar de forma explícita una revisión de:

```text
catalog
book
regime
account
risk policy
universe
relationship
liquidity ledger
config
```

No construyas todavía dichos stores.

Evita un `map[string]any` como contrato principal.

---

## E. Time primitives

Implementa primitives suficientes para separar:

- source time;
    
- receive wall time;
    
- monotonic offset local cuando corresponda;
    
- virtual time;
    
- unknown/absent source time.
    

No conviertas timestamps en secuencia global.

No inventes precisión.

No implementes wire parsers de segundos/milisegundos específicos todavía.

Define `Clock` abstraction para testabilidad y virtual clock posterior.

No usar directamente `time.Now()` dentro del dominio cuando el clock inyectado sea aplicable.

---

## F. Error taxonomy

Materializa errores/códigos tipados compatibles con el diseño frozen.

Como mínimo distinguir:

```text
invalid input
unsupported
insufficient data
invariant violation
contract drift
disabled capability
not reproducible
transient failure
system failure
```

No conviertas todos los errores en strings.

Debe soportar:

```text
errors.Is
errors.As
```

o contrato idiomático equivalente.

No diseñes una jerarquía gigantesca.

---

## G. Capability registry fail-closed

Implementa registry cerrado/versionable.

Regla central:

**capability ausente o desconocida = DENIED/DISABLED.**

Representar explícitamente capabilities que ya están congeladas como no habilitables inicialmente, incluyendo al menos conceptos futuros como:

```text
LIVE_EXECUTION
NEGRISK_CTF_CONVERSION
NEGRISK_V2_CONVERSION
L2_HISTORICAL_BACKFILL
DEFER_EXEC
BUILDER_OPTIONAL
COMBO
RFQ
```

No implementar esas capabilities.

Sólo su identidad/estado fail-closed.

No debe existir:

```text
defaultAllow = true
```

ni fallback equivalente.

---

## H. ExecutionMode

Materializa únicamente el contrato frozen:

```text
SHADOW
LIVE_DISABLED
LIVE_ENABLED
```

Pero:

`LIVE_ENABLED`

no puede producir capacidad efectiva de trading en S01.

No existe aún gateway live.

No existe aún signer.

No existe aún ActivationLease operativo.

Debe ser imposible que un test o config de S01 habilite un efecto externo.

---

## I. ActivationLease contract

Define sólo el value contract necesario por M1/M2 para que slices posteriores no cambien API.

Puede contener identities/revisions/hashes necesarios según el diseño frozen.

No implementar emisión de leases.

No implementar validación productiva completa.

No crear secretos.

No crear trading.

Cualquier intento de obtener una lease operacional en S01 debe terminar en:

`DISABLED`

---

# 5. CONFIG

Implementa en:

`internal/config`

configuración versionada y estricta.

Debe contener únicamente configuración transversal de foundation necesaria ahora.

Requisitos:

- versión de schema obligatoria;
    
- unknown fields rechazados;
    
- defaults sólo donde sean inequívocos;
    
- ningún `0` ambiguo como infinity/default;
    
- hash/revision determinista de la configuración validada;
    
- secrets no forman parte de la config pública;
    
- execution mode inicial debe ser fail-closed;
    
- ausencia de configuración para una capability dependiente no la habilita.
    

Formato:

TOML es aceptado según M2.

Librería propuesta:

`github.com/BurntSushi/toml`

Puede sustituirse por otra sólo si conserva exactamente este contrato y se documenta el motivo.

---

# 6. ARCHITECTURE TESTS

Implementa en:

`internal/archtest`

la primera versión de tests estructurales.

Como mínimo verificar:

- `internal/foundation` no importa paquetes superiores del engine;
    
- `internal/config` sólo depende de foundation y stdlib/dependencias de parsing permitidas;
    
- no existen paquetes genéricos `utils` o `common`;
    
- no existen dependencias circulares;
    
- futuros paquetes strategy podrán someterse al import gate frozen.
    

No necesitas implementar todavía toda la blacklist de strategies si los paquetes strategy aún no existen.

Deja el mecanismo extensible para S09/G-15b.

No uses una herramienta enorme si el AST/`go list` estándar basta.

---

# 7. CMD MINIMAL

Crear:

`cmd/engine`

Debe:

- compilar;
    
- exponer `--version` o equivalente mínimo;
    
- cargar configuración sólo si corresponde;
    
- no iniciar networking;
    
- no iniciar market data;
    
- no iniciar SQLite;
    
- no emitir órdenes;
    
- no contener lógica de negocio.
    

No anticipes la CLI completa.

---

# 8. DEPENDENCIES

Dependencias permitidas en S01 deben mantenerse mínimas.

Esperadas:

- decimal implementation encapsulada;
    
- TOML parser;
    
- property testing si ya se utiliza en tests.
    

No agregues:

```text
Kafka
Flink
gRPC
Kubernetes libraries
ORM
HTTP router framework
dependency injection framework
plugin framework
```

No agregues SQLite todavía salvo que el slice M2-S01 frozen lo exija literalmente; su implementación corresponde a S03.

Ejecuta:

```text
go mod tidy
```

y revisa dependencias transitivas inesperadas.

---

# 9. TESTS OBLIGATORIOS

Implementar tests unitarios/property según corresponda.

## IDs

- distintos namespaces no son intercambiables;
    
- constructor inválido falla;
    
- representación estable.
    

## Decimal / units

- parsing exacto;
    
- valores grandes;
    
- negativos permitidos/prohibidos según tipo;
    
- cero;
    
- igualdad;
    
- ordering;
    
- serialización round-trip;
    
- ninguna conversión silenciosa vía float.
    

## RevisionRef

- igualdad;
    
- canonical representation;
    
- invalid refs;
    
- deterministic serialization.
    

## Time

- unknown source time;
    
- wall vs virtual separados;
    
- fake clock determinista.
    

## Error taxonomy

- errors.Is / errors.As;
    
- wrapping conserva clasificación.
    

## Capabilities

Property/invariant:

```text
unknown capability -> DENIED
missing capability -> DENIED
explicit disabled -> DENIED
```

Nunca allow implícito.

## Config

- unknown field → FAIL;
    
- invalid schema version → FAIL;
    
- live missing requirements → FAIL/DISABLED;
    
- mismo config → mismo revision hash;
    
- cambio material → revision distinta.
    

## Architecture

- import violations detectadas;
    
- foundation limpio.
    

Usa `-race` donde aplique.

---

# 10. GATES DE ESTE SLICE

Ejecuta exclusivamente los gates asociados por M2-S01.

Como mínimo foundation parcial de:

```text
G-01
G-02
G-15
```

y cualquier subgate que el M2 plan haya asignado explícitamente a S01.

No declares gates posteriores PASS.

No declares:

```text
G-03+
```

por inferencia.

Registra evidencia física de los tests ejecutados.

---

# 11. QUALITY

Ejecuta al menos:

```bash
go test ./...
go test -race ./...
go vet ./...
go mod tidy
```

Si Agents-OS tiene tooling/lint global obligatorio para Go, úsalo.

Coverage:

aplica el piso de Agents-OS correspondiente al código implementado.

No persigas coverage artificialmente mediante tests sin assertions útiles.

---

# 12. DOCUMENTACIÓN

No crees SPECs nuevos.

No crees ADRs.

No generes README gigantesco.

La documentación normativa sigue siendo Agents-OS.

Al terminar, actualiza únicamente el estado necesario en:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Registra:

- path real del repo;
    
- Go baseline `1.27 / toolchain 1.27.1`;
    
- S01 status;
    
- gates ejecutados;
    
- evidencias relevantes;
    
- blockers;
    
- next slice = S02/S03 según barrera M2.
    

No reescribas M1/M2.

---

# 13. PROHIBICIONES

NO implementar:

- protocol DTOs;
    
- Gamma;
    
- CLOB;
    
- WebSocket;
    
- HTTP;
    
- SQLite;
    
- capture journal;
    
- Catalog;
    
- Regimes;
    
- Books;
    
- Frames;
    
- Replay;
    
- Strategy API;
    
- Simulator;
    
- Account Coordinator;
    
- Risk;
    
- live execution;
    
- signing;
    
- wallets;
    
- NegRisk;
    
- Sports.
    

Aunque parezca fácil.

Eso pertenece a slices posteriores.

No anticipes código.

---

# 14. DEFINITION OF DONE

S01 sólo está `PASS` si:

1. repo Go existe y compila;
    
2. module path correcto;
    
3. Go baseline es 1.27;
    
4. toolchain fijada a 1.27.1;
    
5. foundation contracts anteriores están implementados;
    
6. config estricta funciona;
    
7. capability registry falla cerrado;
    
8. ninguna ruta puede habilitar live;
    
9. architecture tests pasan;
    
10. tests/race/vet pasan;
    
11. coverage requerido pasa;
    
12. no se implementó scope posterior;
    
13. Agents-OS refleja resultado real;
    
14. no queda blocker del slice.
    

Si falta una condición:

`PARTIAL` o `BLOCKED`.

No marques PASS parcial.

---

# 15. RESPUESTA FINAL

Responde únicamente:

```text
STATUS: M2-S01_PASS | PARTIAL | BLOCKED

REPO:
- path:
- module:
- Go:
- toolchain:

IMPLEMENTED:
- foundation:
- config:
- archtest:
- cmd:

QUALITY:
- go test:
- race:
- vet:
- coverage:

GATES:
- PASS:
- NOT_RUN:
- evidence:

SCOPE:
- files/packages created:
- explicit deferred work:

BLOCKERS:
- none | exact blocker

NEXT:
- M2-S02 + M2-S03 barrier
```

No pegues código completo en el chat.

El código local y el proyecto Agents-OS actualizado son los entregables.

---

# INSTRUCCIÓN FINAL

**Empieza el desarrollo del Polymarket Engine.**

Implementa únicamente `M2-S01 Foundation`.

Hazlo sólido, pequeño y verificable.

No adelantes arquitectura ni slices.