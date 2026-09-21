# MANDATO — POLYMARKET PE-001 REALITY CHECK

**Fecha:** 2026-09-21

**Rol:** Principal Quant Researcher + Polymarket Protocol Auditor + Principal Go Architect.

## MISIÓN

Convertir PE-001 Sports Combinatorial desde una POC offline certificada en un experimento falsable sobre contratos reales.

No rediseñar el engine. No crear una sexta POC. No implementar trading real.

El objetivo es entregar evidencia que permita decidir si PE-001 puede comenzar su validación económica.

## 1. AUTORIDADES

Repositorios:

- `xKoRx/agents-os`
    
- `xKoRx/polymarket-engine`
    

Documentos obligatorios:

- Agents-OS bootstrap y constitución vigentes.
    
- `Polymarket Engine — MVP`.
    
- `Polymarket Engine — Continuidad Five-POC 2026-09-20`.
    
- `Polymarket Engine — Five-POC Guía Operativa 2026-09-20`.
    
- `POC-S03 — Sports Combinatorial`.
    
- Technical Platform Map vigente.
    
- `testdata/research-v07/experiment-drills/DRILLS.md`.
    

Baseline documentada: `feature/five-poc-integration@85e27ff`.

El código certificado corresponde a `c38f6c4`. Verificar físicamente ambos SHA, su relación y el estado real del checkout antes de trabajar.

No utilizar el remoto antiguo como sustituto del worktree local.

## 2. FASE A — PREFLIGHT

Verificar:

- HEAD, branch, worktrees y cambios pendientes.
    
- Certificado v07 y correspondencia con el código.
    
- Estado de los datasets RS v0.3.
    
- Contratos e interfaces reales de PE-001.
    
- Ausencia de modificaciones concurrentes sobre los mismos archivos.
    

No ejecutar operaciones destructivas ni modificar datos originales.

Si falla el preflight, entregar un diagnóstico reproducible y detener únicamente las acciones dependientes de él.

## 3. FASE B — CONTRATO REAL

Encontrar un par real Moneyline/Spread de un mismo evento.

Documentar:

- Event ID, Market IDs, Condition IDs y token IDs.
    
- Reglas completas de ambos contratos.
    
- Alcance temporal, overtime, empate y cancelaciones.
    
- Postponement, excepciones y resolución parcial.
    
- Fuente oficial, timestamp de consulta y evidencia preservada.
    
- Demostración formal de la implicación contractual.
    

No aceptar similitudes entre títulos como prueba.

Construir la matriz completa de estados terminales.

Si no existe un par admisible, documentar candidatos descartados y razones precisas. No inventar un par sintético para declarar éxito.

## 4. FASE C — ECONOMICS / U-02

Resolver la configuración efectiva de fees para los mercados elegidos.

Verificar fórmula, parámetros, vigencia, redondeo y provenance.

Consultar libros reales y calcular:

- Precios ejecutables por profundidad.
    
- VWAP de cada pata.
    
- Tamaño efectivamente cubierto.
    
- Peor payoff contractual.
    
- Fees y costes.
    
- Riesgo de ejecución parcial.
    
- Capital requerido y duración del bloqueo.
    

No utilizar midpoint como precio ejecutable.

No declarar rentabilidad si existen fees, estados terminales o costes desconocidos.

## 5. FASE D — EXPERIMENTO

Pre-registrar una única hipótesis, muestra y criterio de falsación.

Reutilizar exclusivamente el pipeline existente:

SCREEN → REPLAY → SHADOW → COMPARE.

Si la captura existente no contiene el par o carece de la evidencia necesaria, producir un plan de captura prospectiva ejecutable con los componentes actuales.

No fabricar datos históricos.

Registrar también cero oportunidades, rechazos, profundidad insuficiente y casos inconclusos.

## 6. FASE E — AUDITORÍA ADVERSARIAL

Intentar refutar la conclusión obtenida:

- ¿La relación contractual realmente garantiza el payoff?
    
- ¿Las dos patas pertenecen al mismo estado temporal?
    
- ¿El libro es suficientemente reciente?
    
- ¿La profundidad es ejecutable?
    
- ¿Las fees están verificadas?
    
- ¿El capital queda inmovilizado más tiempo del supuesto?
    
- ¿Los resultados dependen de un fixture sintético?
    
- ¿Existe sesgo retrospectivo?
    

Toda incertidumbre material debe reflejarse en el resultado.

## 7. ENTREGABLES

Entregar:

1. Estado físico del checkout y certificación.
    
2. Identidad y prueba del par contractual.
    
3. Evidencia de U-02 o bloqueo exacto.
    
4. Manifest y procedencia del dataset.
    
5. Resultados del experimento y condición de falsación.
    
6. Riesgos y evidencia faltante.
    
7. Decisión técnica `GO_RESEARCH`, `ITERATE`, `NO_GO` o `INCONCLUSIVE`, con justificación verificable.
    

`GO_RESEARCH` sólo autoriza continuar investigando. Nunca significa permiso live.

Actualizar las notas existentes de Agents-OS según sus procedimientos y ownership, sin duplicar proyectos ni borrar historia.

Si no hay evidencia suficiente para ejecutar el experimento, entregar el bloqueo concreto y el siguiente mandato mínimo, no un plan arquitectónico nuevo.

## RESTRICCIONES

- `LIVE_DISABLED` obligatorio.
    
- Sin wallet, firma ni órdenes.
    
- Sin push o merge.
    
- Sin modificaciones de código de producción.
    
- Sin refactor general.
    
- Sin reescribir evidencia histórica.
    
- Sin certificaciones inventadas.
    
- Sin autoaceptación del trabajo del owner.
    
- Sin cierre de sesión Agents-OS salvo instrucción explícita.
    

**Criterio de éxito:** nueva evidencia real y reproducible que reduzca la incertidumbre de PE-001, aunque el resultado sea negativo.