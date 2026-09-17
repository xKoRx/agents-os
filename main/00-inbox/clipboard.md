# MANDATO CORRECTIVO — NORMAL

## Polymarket Engine · M2-S01-C1 Numeric Boundary Completion

### MISIÓN

Corregir el único gap detectado en `M2-S01`.

El slice fue reportado `PASS`, pero el plan M2 frozen exige que S01 implemente también el boundary numérico puro de órdenes definido por P03 §5 y cierre su porción completa de `G-01`.

No rediseñes.

No abras S02/S03.

No implementes protocolo wire, transports, SQLite ni Regimes.

Trabaja sobre el mismo repo local:

`~/go/src/github.com/xKoRx/polymarket-engine`

Autoridad:

`main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`

Lee únicamente:

- M2-S01;
    
- M2-S05 para distinguir foundation numérica de integración con Regimes;
    
- TPM `part-03-auth-precision-time.md`, exclusivamente §5 y tablas relacionadas necesarias.
    

## IMPLEMENTAR

En `internal/foundation` o el subpackage ya establecido para primitives numéricas, implementar como funciones puras y tipadas:

- validación de precio contra grid/tick;
    
- validación de decimales permitidos;
    
- rounding/floor de size según P03 §5;
    
- secuencia exacta ceil/floor de amount según BUY/SELL;
    
- conversiones E6 correspondientes;
    
- revalidación posterior de invariantes;
    
- rechazo de:
    
    - overflow;
        
    - escala desconocida;
        
    - valores negativos no permitidos;
        
    - precio fuera de grid;
        
    - resultados que violen minimum representability.
        

No uses `float64`.

No hardcodees un “tick vigente del mercado”: la función recibe el tick/grid como value input. S05 será responsable de obtener/versionar el Regime correcto.

No implementes:

- REST;
    
- DTOs;
    
- Market/Order wire structs;
    
- FeeResolver;
    
- Regimes;
    
- min-size dinámico del mercado excepto como value/input cuando el contrato puro lo requiera.
    

## TESTS

Completar los vectores de `G-01` exigidos por M2-S01 usando exactamente P03 §5.

Incluir:

- todos los tick/grids documentados;
    
- límites y valores inmediatamente dentro/fuera del grid;
    
- BUY/SELL;
    
- floor/ceil;
    
- E6;
    
- cero;
    
- máximos representables relevantes;
    
- overflow;
    
- escalas inválidas;
    
- negativos;
    
- casos donde el rounding posterior invalida la operación.
    

Actualizar la evidencia física:

`testdata/foundation/evidence/g01.json`

Debe distinguir claramente:

`S01_G01_FOUNDATION = PASS`

S05 podrá posteriormente agregar evidencia de integración:

`G01_REGIME_INTEGRATION`

sin reescribir esta evidencia.

## VERIFICACIÓN

Ejecutar:

`go test ./...`  
`go test -race ./...`  
`go vet ./...`  
`go mod tidy`

Mantener el piso de coverage de Agents-OS.

No degradar gates ya verdes.

## AGENTS-OS

Corregir el estado documental para que no exista contradicción:

- antes de completar: G-01 no debe aparecer como PASS completo si falta P03 §5;
    
- después de completar y verificar: marcar `M2-S01_PASS`;
    
- registrar que S05 conserva únicamente integración de tick/regime, no las primitives numéricas;
    
- no modificar M1 ni rediseñar M2.
    

## RESPUESTA FINAL

STATUS: `M2-S01_PASS | PARTIAL | BLOCKED`

CORRECTION:

- numeric boundary:
    
- vectors:
    
- G-01:
    

QUALITY:

- tests:
    
- race:
    
- vet:
    
- coverage:
    

REGRESSION:

- previous S01 gates:
    
- scope creep:
    

NEXT:

- `M2-S02 + M2-S03`