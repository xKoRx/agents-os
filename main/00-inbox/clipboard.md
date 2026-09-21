# MANDATO — POLYMARKET RESEARCH HARDENING & FINAL READINESS

Fecha: 2026-09-21

## MISIÓN

Disponemos de una ventana limitada de trabajo con Grok 4.6.

Tu misión es aprovecharla para dejar Polymarket Engine técnicamente consolidado y preparado para investigación económica real.

NO reinicies el research.

NO rediseñes M0/M1.

NO reconstruyas las cinco POCs.

NO confundas certificación técnica con rentabilidad.

Tu punto de partida es el reality check PE-001 que acabas de completar.

**North star: reducir el tiempo hasta una hipótesis validada, no aumentar el volumen de código.**

## AUTORIDADES

Carga Agents-OS mediante el bootstrap canónico.

Lee el proyecto padre, la continuidad Five-POC, la guía operativa, las cinco POCs y el informe:

`polymarket-engine-datasets/pe001-reality-check-20260921/REPORT.md`

Engine baseline documentada:

`feature/five-poc-integration@85e27ff`

Certificación v07:

`c38f6c4`

Verifica el checkout antes de continuar.

Las decisiones del owner pendientes siguen pendientes. No te autoautorices a aceptar, publicar o habilitar trading.

---

## FASE 1 — ECONOMIC CORRECTNESS / U-02

Resolver hasta donde permita la evidencia la discrepancia entre la implementación de Economics y la configuración real de Polymarket.

Hallazgos que debes investigar:

- Sports fee rate 0.05, exponent 1 y takerOnly según la captura.
    
- Redondeo oficial a cinco decimales frente a TRUNCATE_6DP del engine.
    
- Fees cobradas en shares para BUY y USDC para SELL.
    
- Diferencias entre los parámetros de Gamma, CLOB, documentación y contratos.
    
- Distinción entre taker fees, maker fees y rebates.
    
- Demoras de ejecución deportiva y su efecto económico.
    

La documentación oficial presenta valores contradictorios de maker rebates para Sports. No asumir un valor único sin verificar la configuración pertinente al mercado y periodo.

Revisar las implementaciones y contratos canónicos del protocolo, no blogs como autoridad.

Construir vectores numéricos de referencia independientes.

Determinar si el engine calcula correctamente coste, cantidad recibida, payout neto y capital reservado.

No considerar el cálculo económico equivalente en USDC suficiente si la semántica real del BUY modifica shares recibidas.

### Gate

`U02_VERIFIED`: evidencia primaria suficiente y paridad demostrada.

`U02_PARTIAL`: diferencia acotada y documentada.

`U02_BLOCKED`: falta evidencia material exacta.

Si identificas un defecto real, documenta causa raíz, impacto y regresión. Un cambio mínimo de código sólo podrá ejecutarse con ownership y alcance explícitos; cualquier cambio invalida la certificación anterior hasta recertificar el SHA final.

No perseguir una equivalencia ficticia modificando tests.

---

## FASE 2 — PE-001 REAL MARKET DISCOVERY

El par WNBA anterior queda rechazado económicamente en su snapshot.

No dedicar la investigación a justificar cláusulas ambiguas.

Objetivo: determinar si existe un universo utilizable de pares Moneyline/Spread con reglas demostrables.

Reutilizar Catalog, Gamma y Books existentes.

Descubrir una cohorte acotada de mercados deportivos actuales.

Para cada par:

1. Verificar identidad contractual.
    
2. Comprobar alcance temporal y resolución.
    
3. Construir o rechazar la matriz terminal.
    
4. Obtener books contemporáneos.
    
5. Calcular capacidad por profundidad observada.
    
6. Aplicar costes y escenarios de ejecución.
    
7. Clasificar el motivo de admisión o rechazo.
    

No interpretar automáticamente la palabra basketball como prueba de OT.

No inventar contratos.

No implementar un crawler privado si Catalog ya resuelve discovery.

Un problema en un único par no demuestra que toda la familia sea inviable. Del mismo modo, un caso favorable no demuestra frecuencia.

Registrar denominadores: mercados descubiertos, pares candidatos, pares semánticamente válidos, frames temporalmente válidos, oportunidades económicas y capacidad.

Distinguir explícitamente falta de datos de ausencia de oportunidades.

### Experimento

Pre-registrar la muestra y las condiciones de evaluación.

SCREEN → REPLAY → SHADOW → COMPARE.

Captura read-only.

Congelar el journal antes de SHADOW, utilizando un mecanismo de snapshot coherente con el store y sus WAL.

No copiar ni modificar archivos activos de forma insegura.

Preservar hashes, cutoff, manifiesto, secuencia y provenance.

Medir skew, antigüedad, latencia y duración de oportunidades. Modelar un escenario de repricing adverso durante la demora de órdenes deportivas.

No atribuir fills reales a un simulador.

---

## FASE 3 — READINESS DEL PROGRAMA COMPLETO

Realizar una auditoría operativa ligera de las cinco POCs utilizando el baseline vigente.

No repetir todas las pruebas si existe evidencia válida para el mismo SHA.

Para cada POC, entregar:

- Estado técnico.
    
- Disponibilidad de datos reales.
    
- Semántica contractual.
    
- Estado de fees/economics.
    
- Evidencia de experimento.
    
- Bloqueo material exacto.
    
- Próximo experimento mínimo.
    

Revisar especialmente:

**S01 NegRisk:** utilizar RS v0.3 y distinguir membership verificada de payout exhaustiveness todavía desconocida. No promover los 663 resultados inconclusos.

**S02 Sports Reversion:** conservar la captura deportiva existente. Identificar qué muestra adicional necesita para evaluar la frecuencia sin transformar una ausencia local de señales en NO_GO global.

**S03 Sports Combinatorial:** incorporar los resultados de la fase 2.

**S04 Weather:** inventariar contrato real, fuente de resolución, station ID y forecast vintages. No declarar calibración sin datos históricos point-in-time. Si no hay datos suficientes, producir el contrato de adquisición mínimo, no otro modelo.

**S05 Maturation:** verificar una cohorte real O/B con anclas causales. No usar `createdAt` como sustituto de `first_known_at`. Si no aparece un mercado nuevo durante la observación, registrar explícitamente la falta de cohorte.

W/SFG-06 permanece fuera de alcance salvo que se convierta en dependencia real de la investigación actual.

No fabricar oportunidades ni fills para estrategias descriptivas.

---

## FASE 4 — AUDITORÍA FINAL

Consolidar resultados verificables.

Revisar que:

- Los datasets originales estén intactos.
    
- Los manifests tengan procedencia y cutoff.
    
- Las pruebas reportadas realmente se hayan ejecutado.
    
- No exista mezcla de fixtures y datos reales.
    
- Los resultados inconclusos sigan siendo inconclusos.
    
- No existan cambios de código sin certificación nueva.
    
- LIVE_DISABLED permanezca intacto.
    
- La documentación refleje el estado real.
    

Auditar los pendientes reportados previamente: capitalLock legacy, gofmt drift, SFG-06, publicación y aceptación del owner.

Corregir únicamente defectos demostrados y autorizados que bloqueen el objetivo. No hacer refactors cosméticos.

No duplicar proyectos ni crear documentación paralela.

Actualizar los proyectos y recursos existentes de Agents-OS, registrar change log y evidencia. Mantener la sesión abierta.

---

## ENTREGABLE FINAL

Un único resumen ejecutivo:

POLYMARKET_FINAL_READINESS

ENGINE: estado y SHA

M4: certificado válido para qué baseline

DATA: disponibilidad y cobertura real

ECONOMICS: U-02 y precisión

POCS: matriz de cinco estados

RESEARCH: hipótesis contrastadas y resultados

BLOCKERS: únicamente pendientes materiales

DEBT: deuda no bloqueante

OWNER_DECISIONS: decisiones humanas pendientes

NEXT_ACTION: trabajo mínimo restante

Para cada bloqueo declarar evidencia faltante, impacto y condición concreta de resolución.

No declarar alpha, readiness de dinero real ni fin definitivo del research sin evidencia.

El objetivo es cerrar una etapa de ingeniería e iniciar investigación reproducible, aunque las cinco hipótesis continúen sin validación económica.