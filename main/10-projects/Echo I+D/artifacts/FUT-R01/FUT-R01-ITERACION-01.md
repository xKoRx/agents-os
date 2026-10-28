---
type: prompt
schema_version: 1
status: active
area: "[[Trading]]"
target: "Workers Cloud I01-A/I01-B; I01-C local diferido"
prompt_version: 1
inputs:
  - "Decisiones Owner y planner Futures vigentes"
  - "RV-01, expediente limitado y cobertura existente"
  - "Fuentes primarias decisivas y documentación oficial por programa"
outputs:
  - "Ficha determinista candidata, casos y observabilidad"
  - "Perfil contractual, caja y propuesta MM separados"
  - "Retorno técnico de datos sólo después de reanudación"
project: "[[Echo I+D — Futures]]"
aliases:
  - "FUT-R01 — Primera iteración después de RV-01"
related:
  - "[[FUT-R01-INDICE]]"
  - "[[FUT-R01-RV-01-CONSOLIDADO]]"
  - "[[Echo I+D — Cobertura Futures]]"
  - "[[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]]"
tags:
  - kind/prompt
  - area/trading
  - project/echo-rnd
created: "2026-10-28"
updated: "2026-10-28"
---

# FUT-R01 — Iteración 01: de RV-01 a una primera ficha revisable

## Propósito

Convertir la evidencia disponible en una unidad pequeña de trabajo útil para la fábrica permanente de estrategias. **Resultado inmediato propuesto: una ficha determinista de persistencia de cierre NQ y sus requisitos de campaña, con MR06 como alternativa existente.** No es otra investigación general ni un nuevo planner.

La prioridad, el backlog y los estados viven sólo en [[Echo I+D — Futures]]. Este documento posee los contratos de los siguientes encargos; [[Echo I+D — Cobertura Futures]] enlaza evidencia. La selección definitiva del experimento y los límites económicos permanecen con el Owner.

**Instrucción Owner 28-10-2026:** frente 1 pausado mientras el runtime está en proceso de merge a master. Es información Owner, no verificación de que el merge haya terminado. A/B pueden avanzar documentalmente; C y cualquier integración/implementación/prueba quedan en espera. Los prompts están **PREPARADOS, NO EJECUTADOS** por esta entrega.

## Contrato de entrada

- [[FUT-R01-RV-01-CONSOLIDADO]] conserva NO_APTO_AUN para una campaña definida y reproducible. Su §1/§10 permite especificar una hipótesis acotada.
- Integridad del expediente, especificación de señal, datos/ejecución y valoración de campaña tienen bloqueos distintos. No convertir H01 en una prohibición universal de escribir reglas, ni eliminarlo por continuar con una ficha propia.
- Capital Futures USD 4.000, Forex separado, NQ exclusivo, Strategy de tres bloques y MM independiente. La corrección Owner de campañas prop prevalece: esperanza por trade no positiva no es descarte universal; asimetría/riesgo alto tampoco demuestran utilidad.
- Superposición 5+5 admitida; meta de dos props simultáneas intacta. Un primer perfil experimental no cumple por sí solo la meta ni obliga a duplicar el piloto.
- Mandato v4 y retornos DR se conservan como entradas históricas sin reescribir sus bytes. No repetirlos ni abrir DR-05.
- Para entrar en una nueva identidad ejecutable: fuente/spec, datos, selección, perfil, presupuesto y gates vigentes. No llamarla lista mientras una ambigüedad material cambie operaciones.

## Contrato de salida

### Tres decisiones distintas

| Salida | Qué permite | Qué no acredita |
|---|---|---|
| Ficha lista para revisión | Revisar setup, filtro, riesgo/objetivo, causalidad, casos y aporte a cobertura | Implementación, datos físicos, PASS o rentabilidad |
| Perfil contractual documentado | Revisar reglas/costes/ruta por fase y escenarios de caja | Elección comercial, acceso físico, permiso de operar o gasto |
| Paquete técnico listo para decisión | Delimitar trabajo por identidad, evidencia y presupuesto después de reanudación | Ejecución automática ni omitir G0–G5 |

El primer resultado debe responder, sin interpretación discrecional: “dadas estas observaciones, ¿hay señal, cuándo existe, qué geometría queda fijada y qué evento provoca la salida?”. Incluye positivo, negativo y frontera; la traza efectiva permanece NOT_EXECUTED hasta comprobación técnica.

### Celda y reutilización

La propuesta pertenece a FUT-NQ-PERSIST, contexto de cierre. Contrastar FBC/ORB/MR08; no afirmar un hueco o familia independiente por cambiar horario. MR06 pertenece a FUT-NQ-REVERT y se recupera antes de pensar en otra implementación. Cada variante semántica conserva su identidad e historial de selección.

Reutilizar definiciones y artefactos cuando coincidan sus autoridades: datos/calendario, indicadores y causalidad, casos de unidades/tiempo, perfil contractual, caja, métricas y registros. Compartir datos no demuestra mecanismo común ni independencia; compartir módulo no transfiere gates. Cambiar el stop técnico definido por la Strategy cambia su geometría y exige identificar la configuración o variante correspondiente. Los límites y salidas protectoras económicos del MM conservan identidad propia; la traza debe distinguir qué regla produjo la salida. En esta comparación se mantiene fija la geometría técnica de Strategy.

### Condiciones de aceptación de una fábrica, para registrar antes de implementar

Son requisitos de investigación derivados del mandato Owner; **no afirmaciones sobre capacidades implementadas ni diseño nuevo del frente 1**:

1. Cada intento tiene identidad reproducible de Strategy/variante/config/MM/RuleSet/datos/calendario/build/modelo, resultado y causa de parada.
2. Preservar oportunidades y vetos además de fills/trades: distintos MM pueden admitir operaciones diferentes. No reutilizar una curva cerrada multiplicándola por contratos.
3. Preparación/analytics se reutilizan sólo con inputs y disponibilidad causal compatibles; cada cambio invalida exactamente la evidencia dependiente.
4. Agrupar trabajo por dependencias compartidas: calendario/ingesta, analytics o perfil. Mantener resultados, estados y gates por identidad; nada de producto cartesiano de indicadores×RR×MM×props.
5. Receipts válidos evitan corridas duplicadas. Reintentos/parciales conservan identidad y motivo. Comparación entre políticas requiere mismas oportunidades externas y estado propio de cada cuenta.
6. Reutilizar el supervisor y la admisión existentes. Capacidad se mide en Hefesto; techo global vigente no es objetivo obligatorio ni capacidad certificada. Frente 1 mantiene la pausa.
7. Cada iteración termina con continuar/corregir/aparcar/descartar, evidencia reutilizable y siguiente pregunta. Medir tiempo hasta decisión, coste/cómputo evitado y motivos de fallo antes de optimizar throughput.
8. Generalizar ante un segundo uso concreto o un requisito compartido demostrado. No construir por adelantado otro motor, catálogo universal de indicadores, scheduler, DSL o infraestructura de factory.

La integración posterior deberá contrastar estos requisitos con capacidades ya existentes y resolver sólo gaps concretos bajo el owner de producto.

## Prompt

### I01-A — Ficha, fuente y observabilidad (Cloud, preparado)

```text
# ECHO FUTURES — I01-A: PRIMERA FICHA DE STRATEGY
## ONE-SHOT documental · FUT-R01 · FUT-NQ-PERSIST

PREGUNTA
¿Podemos convertir la persistencia de cierre NQ propuesta por RV-01 en una Strategy determinista, revisable y distinta de una duplicación del trabajo existente?

AUTORIDAD Y ENTRADAS
En sesión nueva, ejecuta el bootstrap de xKoRx/agents-os, branch master, vault main/, desde main/AGENTS.md. Carga echo-futures-research-manager y el ciclo de I+D. Lee sólo:
- main/10-projects/Echo I+D/Echo I+D — Futures.md.
- main/10-projects/Echo I+D/Echo I+D — Cobertura Futures.md, celdas/identidades pertinentes.
- main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-ITERACION-01.md.
- FUT-R01-RV-01-CONSOLIDADO.md, §§6, 9 y 10, en ese mismo expediente.
Consulta la fuente primaria de la regla y los fragmentos DR-03/04 necesarios. No reconstruyas todo el vault. Si no puedes acceder, solicita esos documentos concretos; no inventes su contenido.

DECISIONES FIJAS
NQ exclusivo. Strategy = setup + filtro + objetivo/riesgo técnico o RR. MM por prop/etapa es otra entidad. Capital Futures USD 4.000 sin aportes; Forex separado. El resultado económico se juzga por campaña/caja, sin exigir esperanza positiva por trade como admisión universal.
Frente 1 PAUSADO: runtime está en proceso de merge a master según el Owner. No tocar producto, integración, hosts ni ejecutar nada.
RV-01 conserva NO_APTO_AUN para campaña; su corpus es limitado. Una nueva ficha puede apoyarse en fuentes verificadas sin afirmar que los cuatro originales estén completos.

TRABAJO
1. Reconciliar esta propuesta con FBC/ORB/MR08. Clasificar aporte probable y posible duplicidad; no declarar independencia ni ausencia universal por el nombre.
2. Proponer UNA ficha baseline, con tres bloques:
   SETUP: referencias de precio, ventana predictora anterior al resultado, sesión/DST, evento de decisión, dirección/cero, emisión y validez de entrada.
   FILTRO: ninguno inicialmente; datos inválidos bloquean evaluación y no son un filtro de alpha optimizado.
   OBJETIVO/RIESGO: una geometría técnica explícita y salida temporal, con unidades, anclaje y precedencia. Distinguir condición de salida de fill.
   Si la fuente no define una regla necesaria, justificar UNA propuesta como HYPOTHESIS/OPERATIONALIZATION. No presentarla como regla del paper ni dejar “x”, “A o B” o parámetros libres en una ficha declarada cerrada.
3. Trazar cada regla a fuente/hipótesis y a casos positivos, negativos y límites. Son casos documentados; no código ni pruebas ejecutadas. Incluir causalidad, dato insuficiente, cero/igualdad, unidades y salida.
4. Separar lo identificable con barras cerradas M1, lo modelado y lo que necesita otros datos. Stops protectores, trailing, quotes y orden intrabar pueden seguir siendo relevantes aunque la señal use cierres. No fabricar recorridos “conservadores”, cotas o fills.
5. Registrar antecedentes/ventanas conocidos que influyeron en selección, dejando desconocidos explícitos. No declarar OOS virgen ni abrir una parrilla.
6. Definir el registro que deberá producir la futura ejecución: oportunidades/señales y sus rechazos, no sólo trades ejecutados. Especificar campos mínimos para comparar dos MM sobre las mismas oportunidades causales. Reutilizar contratos existentes; no diseñar otra base/scheduler.
7. Enlazar MR06 en FUT-NQ-REVERT como alternativa existente. No desarrollarla en este encargo ni cambiar de candidato silenciosamente.
8. En el anexo de investigación, fijar hipótesis falsable, explicación propuesta, evidencia/contraevidencia, control comparable y criterio de refutación antes de resultados. Completar datos, modelo de ejecución, coste/dependencias estimables y aporte a cobertura. Separar refutación de la regularidad de precios de valoración de campaña; no usar PF/Sharpe/esperanza positiva como admisión universal ni confundir falta de significación con refutación.

ENTREGABLE Y RETORNO
Una ficha candidata con anexos breves de evidencia, casos, observabilidad, selección y dependencias. Resultado: LISTA_PARA_REVISION_DE_SPEC, DUPLICIDAD_POR_RECONCILIAR o BLOCKED_SPEC, con motivo. Es estado documental, no G0/G1 PASS.
Explicar qué permite especificar ahora, qué requiere retorno técnico y qué depende de contrato/MM.
Devuelve al manager Futures. Si cuentas con escritura documental autorizada, materializa únicamente:
main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-I01-SPEC.md.
No edites planner, cobertura, retornos históricos ni el archivo del worker B; el manager integra. Usa master sin ramas/PRs y reconcilia HEAD. Si no puedes publicar, devuelve el contenido completo.

PRESUPUESTO, REFUTADOR Y PARADA
Un worker, una entrega y una adjudicación; hasta tres fuentes primarias decisivas, sin nuevo Deep Research general. Detente con ficha revisable o una dependencia que cambie operaciones. No añadir filtros, RR o ventanas para rescatar el resultado.
Sin código, backtests, simulaciones, campañas, cambios de MM ejecutable, gasto ni cierre formal. Mantén G0–G5 y declara NO_DELTA metodológico salvo evidencia concreta.
```

### I01-B — Contrato, caja y comparación MM (Cloud, preparado)

A y B pueden avanzar en paralelo dentro de una sola pregunta primaria. B puede cerrar reglas/costes antes de recibir A; **no puede congelar los dos MM hasta conocer la geometría y resolver decisiones materiales**.

```text
# ECHO FUTURES — I01-B: CONTRATO, CAJA Y DOS MM COMPARABLES
## ONE-SHOT documental · reparación focal de RV-01

PREGUNTA
¿Qué perfil contractual verificable y qué definiciones de caja permiten comparar dos MM sobre la misma Strategy NQ con USD 4.000 sin aportes?

AUTORIDAD Y ENTRADAS
En sesión nueva, bootstrap de xKoRx/agents-os, master, main/AGENTS.md. Recupera el planner Echo I+D — Futures y:
main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-ITERACION-01.md.
En ese expediente lee RV-01 §§5,7,9,10 y sólo el fragmento pertinente del mandato v4/DR-02. Usa I01-SPEC cuando exista; su ausencia no impide la verificación contractual.
Si no tienes acceso al vault, pide esos insumos concretos y no los reconstruyas.

CONTEXTO FIJO
USD 4.000 Futures, sin aportes ni respaldo Forex; NQ exclusivo. 5 challenge + 5 funded pueden coincidir; meta de dos firmas simultáneas permanece, pero este primer perfil no es todavía la cartera.
Se permite investigar resolución rápida y MM agresivos dentro de reglas. Expectativa por trade no positiva no descarta universalmente una campaña; tampoco la asimetría garantiza utilidad.
USD 3.000 bruto/neto, pago único/acumulado, horizonte, prioridad entre rapidez/caja y límites de desembolso siguen abiertos: mantener escenarios y no decidirlos por el Owner.
Frente 1 PAUSADO por merge. Sin inspección física ni cambios de arquitectura.

ALCANCE ACOTADO
Partir de My Funded Futures Rapid EOD 50K como candidato DOCUMENTAL a completar, no proveedor elegido ni recomendación de compra. Usar Rapid estándar sólo para evitar la mezcla detectada en RV-01.
Una alternativa focal puede ser LucidFlex 50K, sujeta al objetivo de payout; no ampliar a otras firmas sin nuevo mandato. La restricción TopstepX ya detectada es un antecedente de ruta, no permiso para rediseñar Echo.
Si el primer perfil queda suficientemente cerrado y hay presupuesto, completar la alternativa con las mismas columnas. Un bloqueo no autoriza una búsqueda interminable de firmas favorables.

TRABAJO
1. Construir un vector por Provider/Program/Size/Stage/Platform/cohorte. Separar evaluación, SIM funded y live.
2. Para cada fase: target, DD y actualización/enforcement, saldo que se observa, pérdida diaria, consistencia/días, noticias, cierre/horarios, contratos/escalamiento, inactividad y conductas pertinentes.
3. Documentar origen del disparador→proceso→bridge/API→plataforma→cuenta; permisos de automatización, copia/multicuentas y transición live. “Bots permitidos” no basta. Si la ruta interna exacta no está documentada, UNKNOWN; no inspeccionar servidores ni inferir compatibilidad.
4. Costes por evento: compra, reset, renovación, activación, datos/plataforma/API, operación y transferencia. Fuente oficial, fecha y ámbito por campo. No inventar precios ni extrapolarlos entre tamaños.
5. Función de payout: elegibilidad, solicitud, aprobación, abono, split, cap, saldo posterior y transición de fase. Una solicitud no es dinero disponible; SIM no se prolonga más allá de sus reglas.
6. Definir caja inicial 4.000, cobros recibidos, desembolsos externos y obligaciones pendientes, sin doble descuento de comisiones. Distinguir coste de la trayectoria ganadora de adquisición agregada con todos los fallos. Mantener cohortes, horizontes y pendientes.
7. Preparar dos políticas MM separadas con distinta agresividad por etapa, manteniendo idéntica geometría de Strategy. No elegir 1%/2% por costumbre ni alterar stop/objetivo técnicos. Distinguir salidas económicas/protectoras propias del MM. Bases de riesgo, contratos NQ enteros, admisión/vetos y continuidad deben ser explícitos. Mientras falte la ficha o una decisión material, entregar requisitos y escenarios, sin declararlas congeladas.
8. Comparar qué resultados se medirán: cobro temprano, caja neta, coste por activada/pagadora, agotamiento, calendario y cobros posteriores. No inventar probabilidades, score ni umbral universal de PF/Sharpe.

ENTREGABLE Y RETORNO
Perfil primario completo o matriz de campos RESUELTO / UNKNOWN / INCOMPATIBLE con fuente y efecto; alternativa sólo dentro del alcance. Anexo de caja y propuesta MM, dependencias de I01-A y decisiones Owner.
Admisibilidad documental e integración física son estados distintos. No declarar una prop elegida ni una ruta certificada.
Devuelve al manager. Si hay escritura documental autorizada, publica sólo:
main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-I01-CONTRATOS.md.
No edites la Strategy, planner, cobertura ni originales. Master sin ramas/PRs, HEAD reconciliado; si no puedes publicar, devuelve contenido íntegro.

PRESUPUESTO, REFUTADOR Y PARADA
Un worker, hasta doce páginas oficiales decisivas, una entrega y una adjudicación. Consulta condiciones vigentes y conserva URLs/fecha; términos ambiguos quedan como dependencia. Sin contacto con terceros.
Campo indispensable sin evidencia, incompatibilidad o límite del presupuesto: terminar con impacto y pregunta exacta. Sin DR-05, compras, código, simulaciones, backtests, pruebas físicas ni cierre formal.
```

### I01-C — Datos y recibos (diferido por pausa Owner)

Este contrato se prepara para continuidad; no se despacha durante la pausa. No amplía el diseño de integración.

```text
# ECHO FUTURES — I01-C: DATOS Y EVIDENCIA EXISTENTE
## MANDATO DIFERIDO — NO DESPACHAR DURANTE LA PAUSA DEL FRENTE 1

CONDICIÓN DE ENTRADA
Requiere confirmación Owner de reanudación y alcance read-only. El anuncio de un merge o la existencia de un nuevo master no autoriza por sí solo este encargo. Si el planner mantiene la pausa, devolver NO_DESPACHADO y detenerse.

PREGUNTA
¿Los datos y recibos ya existentes permiten cualificar la ficha I01 y estudiar el perfil contractual propuesto, y cuál es la menor brecha pendiente?

AUTORIDAD Y ENTRADAS
Bootstrap Agents-OS actual; planner Futures; FUT-R01-ITERACION-01, I01-SPEC y I01-CONTRATOS; echo-retester-master y su runbook. Leer el README Backtester y contratos necesarios del corte técnico aceptado por sus owners después del merge. No asumir que los SHAs históricos son el nuevo baseline.

TRABAJO READ-ONLY
1. Identificar baseline/estado WIP aceptado y recibos existentes aplicables, sin cambiar ramas, compilar o ejecutar.
2. Recuperar manifiestos NQ: contratos, cobertura elegible, sesiones/DST, roll, warmup, timestamps, resolución, gaps y fuente. Separar último contrato y contrato trimestral calificado según runbook; no concatenarlos.
3. Mapear requisitos I01 a datos realmente disponibles. Revisar si stop, trailing y payout dependen de eventos intrabar no identificables. No fabricar ticks, quotes, fills ni cotas.
4. Localizar pruebas/fixtures/trazas/registries ya existentes para reglas, datos, MM y programa. Reutilizar por identidad/semántica válida; no transferir PASS por semejanza.
5. Informar capacidad compartida con Echo Forge y límites vigentes mediante evidencia de lectura autorizada, sin iniciar jobs, capturas o supervisores.

ENTREGA
Matriz requisito→evidencia→disponible/faltante; ventana candidata elegida por cobertura, no por PnL; historial conocido de selección; recibos reutilizables; brecha mínima y alcance técnico propuesto. No veredicto de paridad ni de rentabilidad.
Un worker, una pasada enfocada, una entrega; acceso ausente o dato indispensable faltante = dependencia y parada.
Retorno único al manager, con publicación documental sólo si autorizada. No tocar servicios, merge, runtime, tests, replay, campañas, datos originales, compras ni cerrar formalmente el programa.
```

## Límites

- Mantener G0–G5 y los budgets actuales. El estado documental no inventa una nueva cadena de gates.
- Una pregunta primaria Futures, varios workers acotados cuando sus tareas son independientes. Un solo integrador escribe planner/cobertura; cada worker tiene artefacto propio.
- Una entrega por worker y una adjudicación del manager. Reparación focal sólo por una divergencia indispensable, con alcance explícito; sin bucle hasta obtener aprobación.
- El horizonte táctico sigue en 31-12-2026. Ventanas comparables de 30/60 días pueden proponerse como escenarios de análisis, nunca como plazos/cobros garantizados o requisito aceptado.
- La decisión de monto/payout, prioridad rapidez–caja, desembolso/pérdida y reinversión pertenece al Owner. No imponer una reserva o porcentajes MM.
- Un perfil con ruta/contrato incompleto no es una prop “apta”. Estudiar una fase SIM no autoriza extrapolar a live.
- Sin compras, operaciones, código, campañas, nuevas capturas físicas, integración ni cierre formal en esta entrega.

## Fuentes y verificación focal

- [[FUT-R01-RV-01-CONSOLIDADO]], §§1–3,6,9–11, corpus disponible leído en agents-os@7d2c44d7f0aa7a6d63daff7734d8efeb8147715d.
- [[Echo I+D — Futures]], [[Echo I+D — Cobertura Futures]], [[Echo I+D — Mapa de capacidades]] y [[30-resources/runbooks/echo-rnd-cycle-runbook]]: autoridades de trabajo/cobertura, reutilización y WIP.
- [[30-resources/agents/skills/echo-retester-master/SKILL]] y [[30-resources/runbooks/echo-futures-strategy-qualification-runbook]]: gates, contratos/datos y recursos.
- Verificación oficial focal el 28-10-2026: [Rapid estándar](https://help.myfundedfutures.com/en/articles/13134709-rapid-plan-50k-a-comprehensive-look) y [Rapid EOD](https://help.myfundedfutures.com/en/articles/16158363-rapid-eod-50k-a-comprehensive-look) mantienen programas distintos; [TopstepX API](https://help.topstep.com/en/articles/11187768-topstepx-api-access) distingue bots, origen de órdenes y live; [LucidFlex payouts](https://support.lucidtrading.com/en/articles/12945796-lucidflex-payouts) confirma cap 50K de USD 2.000 por solicitud y split 90%, máximo USD 1.800 antes de cargos. Esta comprobación no completa los perfiles, costes ni ruta física.
