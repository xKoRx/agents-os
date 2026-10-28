# FUT-R01 / DR-02 — Contratos prop NQ, automatización y economía comercial

> **Tipo:** artefacto de investigación recibido, no nota canónica de RuleSet ni decisión comercial. **Fecha de mandato y recepción:** 2026-10-28. **Estado del retorno:** DR-02 | PARCIAL. **Fuente:** texto aportado por el Owner como retorno de Deep Research. **Aceptación Owner:** pendiente. **Proyecto:** [[Echo I+D — Futures]]. **Mandato:** [[FUT-R01-RESEARCH-MANDATE]] v4.

## Control de uso por agentes

- **HECHO documental:** se conserva el informe recibido como evidencia histórica, no como condiciones contractuales certificadas. No autoriza seleccionar proveedores, comprar cuentas, construir RuleSets ejecutables, integrar Echo ni operar.
- **DESCONOCIDO / BLOQUEO:** el texto pegado no contiene URLs oficiales exactas ni citas reproducibles por afirmación, fecha efectiva de cada cláusula o contraste completo de términos y help center. Revalidar cada cifra, elegibilidad, permiso de automatización y comisión por Provider/Program/Size/Stage/Platform/cohorte.
- **CONTRADICCIÓN:** atribuye buffer USD 2.100 a MFFU Rapid y luego lo presenta como «sin buffer». LucidFlex 50K declara cap USD 2.000 por solicitud, incompatible con un primer retiro único de USD 3.000 netos. No confundir cap, beneficio disponible y dinero recibido.
- **CIFRAS NO CERTIFICADAS:** OneUp 50K extrapola precio de 25K; LucidFlex usa precio no oficial; comisiones MFFU/OneUp y cargos de plataforma se suponen. Falta coste agregado verificable de funded con fallos/renovaciones; saldo posterior y ciclos de payout requieren reparación.
- **AUTOMATIZACIÓN NO CERTIFICADA:** bots, API, VPS, copia, distribución, posiciones contrarias, uso asimétrico, KYC y transición a live son cuestiones distintas. El informe no demuestra integración física de Echo ni elegibilidad del titular.
- **CLASIFICACIÓN PARA CONSUMO:** todas las rutas permanecen **CONDICIONADA A CONFIRMACIÓN** o **NO VERIFICADA** hasta revisión contractual. No heredar las etiquetas «ELEGIBLE» del informe. Strategy y MM por programa/etapa siguen separados.
- **RESPONSABLE SIGUIENTE:** submanager Futures debe verificar fuentes oficiales, reparar contradicciones y preparar decisión Owner; no se presume revisión independiente ni validación física por guardar este documento.

## Informe recibido — transcripción de referencia

# Resumen Ejecutivo  
Buscamos **firmas de prop-futures** que permitan operar *exclusivamente NQ* con política de **alto riesgo** y rápida resolución usando USD 4.000 de capital inicial. Tras investigar, las dos rutas más prometedoras son:  
- **MyFundedFutures – Rapid Plan 50K** (evaluación → cuenta simulada).  
- **Lucid Trading – LucidFlex 50K** (evaluación → cuenta simulada).  

Otras alternativas consideradas (a confirmar): **Topstep – Express 50K** y **OneUp Trader – Standard 50K**. Estas cumplen los requisitos de NQ pero pueden depender de elegibilidad geográfica, KYC o limitaciones de cuentas adicionales.

A continuación se presenta una matriz comparativa de cada programa, con indicadores faltantes marcados como **?(pendiente)** si no figura en fuentes oficiales, y el estado de elegibilidad:

| **Proveedor/Programa (NQ)** | **Eval. (tamaño)** | **Funded (sim) / Live** | **Plataforma** | **Precio eval** | **Profit target / MLL** | **Drawdown diario** | **Stops adicionales** | **Consistency** | **Payout (split)** | **Buffer / Mín. retiros** | **Payout caps** | **Profit req. para +$3000** | **Estado** |
|---------------------------|-------------------|-----------------------|--------------|---------------|------------------------|---------------------|----------------------|-----------------|------------------|-------------------------|-----------------|-----------------------------|-----------|
| **MFFU Rapid 50K** | $50k, USD 3.000 | Sim (balance 0, EOD trl) → Live | Tradovate (Rithmic) | ~USD 153 | PT 3.000, MLL 2.000 (EOD) | No hay límite diario | Al cierre (EOD) tracciona, luego fijo $100 | 50% eval. (simulado no) | 90/10 | $2.100 buf. (saldo +2.100) | Sin límite (día>buf) | Ganancia bruta ≈5.433 → +$3.000 neto (90%) | ELEGIBLE (contrato permite bots y news) |
| **MFFU Builder 50K** | $50k, USD 3.000 | Sim (balance 0, EOD trl) → Live | Tradovate (Rithmic) | ~$153 (desc. $107) | PT 3.000, MLL 2.000 (EOD) | Lím. diario blando $1.000 | Trailing EOD, Lock $100; Mínimo balance $48.000 | 50% (eval)& 50% ciclos | 80/20 | Buffer = MLL+100 ($2.100) | Max retiro/ciclo $2.000 | Bruto ≈5.850 → +$3.000 neto (80%) | CONDICIONADA (pago escalonado, cap) |
| **Topstep Express 50K** | Combine (5d gan.≥$150) | Funded (0+$2.000 MLL) | TopstepX (Rithmic) | USD 149 (1-step; mensual?) | PT no divul., MLL $2.000 | $1.000 diario (Soft ban) | Cierre pos. 15:10CT | Ruta estándar o 40% (consis.) | 90/10 | N/A (sin buffer) | Request hasta 50% (Std: $5.000; Consis: $6.000) | Bruto ≈3.333 → +$3.000 neto (90%) | CONDICIONADA (KYC/territorio) |
| **OneUp Standard 50K** | PT 3.000, ≥10d | Funded (simulado) | R|Trader/CQG/etc. | ~$130 (50K; 25K = $65) | PT 3.000, Drawdown pico** | Lím. diario especul. | Reglas: trailing + límites contr. | N/A (pasan sin consist.) | 100%/$10k luego 90% | Sin buf. (solo días mín.) | Sin cap “teórico” (pero partner puede aplicar) | Neto $3.000 ≈ $3.000 bruto | CONDICIONADA (depende de partner) |
| **LucidFlex 50K** | PT 3.000, **consist. 50% al cierre** | Funded (balance 0) | Rithmic (Tradovate/Sierra) | ~USD 149 | PT 3.000, MLL 2.000 (EOD) | Ninguno (opcional) | Solo MLL $2.000 (cierra diarios) | 50% (evaluación) / **no en funded** | 90/10 | Sin buf. | Retiro ≤50% ganancias, máx $2.000 cada vez | Bruto ≈6.667 → +$3.000 neto (90%) | ELEGIBLE (poco buffer, bots OK) |

Notas de la matriz:
- **Precio eval**: costo único pagado para la evaluación. Ej. MFFU Rapid 50K ~$153. OneUp estandar 50K es doble de 25K ($65). Topstep Express ~$149 (1-step, sin prorrateo mensual). LucidFlex ~USD 149 (fuente no oficial, precio aproximado típico).
- **Profit target / MLL**: objetivo de ganancia y pérdida máxima (EOD). MFFU Builder/Eval: PT $3.000, MLL $2.000. LucidFlex Eval: PT $3.000, MLL $2.000. Topstep no publica PT en fuente, pero fija MLL $2.000.
- **Drawdown diario**: Topstep Express fuerza soft-stop $1.000. MFFU Builder y Topstep combinen tienen límites blandos de $1.000 diarios. LucidFlex y MFFU Rapid no imponen límite diario duro (solo MLL).
- **Consistency**: muchos programas exigen operar cierto número de días o no exceder % en un día. Ej. OneUp exige 10 días (5 días Express). LucidFlex Eval exige que ningún día supere 50% de las ganancias totales al pasar. MyFundedFutures Rapid exige 2 días de trading con 50% al día. En cuentas “sim funded” casi ninguno requiere consistencia adicional (LucidFlex tiene 0, Topstep Express hasta consis.path 40%).
