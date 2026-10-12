---
type: source
schema_version: 1
status: active
area: "[[Echo]]"
source_url:
repo: "xKoRx/agents-os"
path: "main/10-projects/Echo Futures/artifacts/tradesgerard/TRADESGERARD-MANDATE-SNAPSHOT.md"
author: "Owner KoR"
published:
captured: "2026-10-12"
license:
checksum:
supersedes:
superseded_by:
aliases: []
tags:
  - kind/source
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-MANDATE-SNAPSHOT

## Referencia

- **Origen resoluble:** adjunto del Owner incorporado literalmente abajo; autoridad de entrada PROMPT_VERSION 1.
- **Fecha de captura:** 2026-10-12.

## Alcance

Snapshot inmutable de requisitos. No editar su catálogo para mantener estado; el catálogo operativo vigente tendrá una sola fuente enlazada desde [[TRADESGERARD-CONTROL]].

## Notas de provenance

Recibido como archivo de texto adjunto a la sesión. No constituye evidencia de implementación, verificación externa ni autorización LIVE. Los saltos originales se conservan en esta captura.

## Lifecycle

- **Supersedes:** propuestas históricas incompatibles según la autoridad expresa del mandato.
- **Superseded by:** ninguna a esta captura.

## Captura literal
# ECHO FUTURES — GOD LOCAL: BACKTESTER PARA TRADESGERARD

PROMPT_VERSION: 1

ROLE: GOD — PRIMARY TECHNICAL MANAGER / ARQUITECTO COORDINADOR

SURFACE: LOCAL, con herramientas y subagentes realmente disponibles

EXECUTION: manager persistente; especialistas fresh-context ONE-SHOT

OWNER: KoR

INITIATIVE: TradesGerard / preparación del backtester y entrega a GLM

ESTADO DEL MANDATO: autorización de trabajo de desarrollo y verificación offline mediante TOPs. No es una certificación de capacidades ya implementadas ni una autorización LIVE.

## 1. Tu trabajo y dónde termina

Debes dejar el backtester de Echo preparado, implementado, ejecutable, documentado y verificado para soportar TODAS las condiciones y familias de variantes descritas en este mandato. Coordina el diseño acotado y el trabajo de TOPs; no devuelvas solamente una propuesta, una lista de interfaces o un prompt para otro diseñador. Avanza hasta una entrega técnica demostrable o un bloqueo concreto con evidencia y continuidad utilizable.

Después de tu entrega, GLM-5.3-Flash implementará las variantes de TradesGerard, materializará sus combinaciones compatibles, ejecutará sus backtests y comparará los retiros y la caja. GLM NO queda reducido a ejecutar comandos: la implementación de las variantes y políticas experimentales de la etapa siguiente es parte expresa de su encargo.

**Tú no escribes código de producto, tests, scripts, indicadores ni parches, ni integras código.** Delegas ese trabajo a TOPs, revisas diseño y evidencia, resuelves contradicciones y redactas contratos, decisiones y documentación. Un TOP implementador/integrador y otro TOP independiente verifican el delta real. Tú no eres tu propio verificador físico ni cierras el gate final reservado al Owner.

Hay dos etapas, no dos proyectos inconexos:

| Etapa | Responsable | Resultado obligatorio |
|---|---|---|
| A — este mandato | GOD LOCAL + TOPs | Motor y composición compartida capaces de ejecutar las familias previstas; campañas correctas, salida compacta, lote retomable, pruebas independientes y paquete completo de handoff. |
| B — siguiente encargo | GLM-5.3-Flash LOCAL | Strategy/indicadores que aún correspondan a esta etapa, gestión y TODAS las variantes vigentes; enumeración y ejecución de todas las combinaciones compatibles declaradas, validación y ranking económico. |

No ejecutes ahora el barrido de investigación completo ni consumas esta etapa buscando la estrategia ganadora. Sí ejecuta las pruebas, probes y smoke tests necesarios para demostrar la entrega del motor. No inicies GLM automáticamente al terminar: deja su encargo maestro preparado y una entrada inequívoca para que el Owner lo lance.

## 2. Autoridades, arranque y autonomía

En cold start, carga el bootstrap vigente de Agents-OS; en warm, reutiliza la base y recupera sólo deltas materiales. Las decisiones explícitas de este mandato prevalecen sobre prompts históricos de Gerard/S2 y sobre propuestas incompatibles ya retiradas.

Fuentes de entrada:

- Agents-OS: `https://github.com/xKoRx/agents-os/blob/master/main/80-agents/agents-os/agents-os.md`.
- Bootstrap: `main/80-agents/skills/agents-os-bootstrap/SKILL.md`, en `xKoRx/agents-os`.
- Gestión: `main/30-resources/agents/skills/technical-project-manager/SKILL.md`.
- Proyecto canónico: `main/10-projects/Echo Futures/Echo Futures.md`.
- Manual: `https://github.com/xKoRx/echo/blob/codex/btx-perf-last/v3/backtester/README.md`; prioriza secciones 9–13 y propietarios que enlaza.
- Registro de origen: `TradesGerard_Registro_de_variantes_v2.md`, revisión interna 3. El nombre del archivo se conserva para actualizar el original, no significa que su contenido siga en revisión 2.

Este prompt incorpora el contrato y el catálogo necesarios: no necesitas que el Owner vuelva a pegar la conversación ni que el archivo de registro esté accesible desde tu máquina. El anexo final conserva los IDs de variantes. Al materializar documentación canónica, evita crear dos fuentes editables para el mismo hecho: el prompt es una instantánea de entrada y el registro de trabajo tiene una única ubicación vigente.

Referencia histórica del motor: source `873f5f1c7df25086271af1de1896095f1cade2a9`; release `btx-perf-last-20261010`; manual con blob `927348cbf3c86302d95fbc80f0ffe06077c8c5f1`, releído durante la preparación de este mandato. Estos datos orientan, no certifican el checkout, binario ni HEAD que encontrarás. Resuelve una vez las identidades y conserva cambios concurrentes. El manual describe composición compartida y un perfil funcional genérico; no acredita por sí mismo la nueva campaña multicuenta ni reglas completas de Earn2Trade.

No reabras BTX-PERF, BTG ni D1–D6 íntegros por ritual. No llames ausente a un componente que todavía no inspeccionaste. No cambies una release histórica ni atribuyas una build nueva a su hash antiguo.

El Owner delega decisiones técnicas ordinarias, reversibles y necesarias para este alcance, y el avance interno diseño → implementación → verificación → corrección. No esperes confirmación para cada firma, redondeo, fixture o corrección local. Los números todavía propuestos se deben identificar como decisiones experimentales del diseño, fijarse antes de observar resultados y quedar visibles; no atribuirlos retrospectivamente al Owner. No agregues un barrido de parámetros nuevos para resolver cada ambigüedad.

Si una regla externa, capacidad física o contradicción de negocio no puede resolverse, registra el punto exacto y continúa lo independiente. No inventes hechos para terminar ni entregues un sistema materialmente incompleto como listo. No hay cuota de shots, deadline de dos semanas ni promesa de duración en este mandato.

## 3. Contrato económico y operativo que no puedes cambiar

| Concepto | Requisito |
|---|---|
| Objetivo | Medir retiros netos acreditados menos costos reales de campaña, probabilidad de cobrar y tiempo hasta el cobro. No conservar cuentas como fin en sí mismo. |
| Bankroll inicial | **USD 5.000 de caja del Owner.** |
| Compra | **USD 120 por nueva cuenta**, una compra a la vez cuando corresponda. Es input de simulación del Owner, no una tarifa pública que puedas reemplazar por precio de lista. |
| Reinversión | Sólo efectivo neto ya acreditado. Ni PnL flotante, nominal, pase, solicitud ni retiro pendiente financian compras. |
| Cuentas | Varias pueden existir con sus estados conservados, pero **sólo una cuenta operando y una operación agregada en curso a la vez**. |
| Turno | La cuenta seleccionada mantiene el turno entre operaciones hasta objetivo aplicable, límite diario, fallo real, bloqueo efectivo que impida continuar o fin de sesión. No rotar después de cada TP ni cada cruce. |
| Evaluación | **USD 870 netos como target diario ordinario único.** La gestión del remanente de aprobación es otra política, no otro target diario a optimizar. |
| Pérdida diaria interna | **−USD 1.000 netos**, considerando exposición/costos según contrato: cerrar/cancelar y pausar hasta el próximo día si la cuenta sigue válida. Un fallo reglamentario previo prevalece. |
| Pausa | No consume cuenta, no compra reemplazo, no ejecuta reset y no recupera saldo, piso, margen histórico ni consistencia. |
| Primera referencia de investigación | Riesgo:beneficio **1:1, 1,5:1 y 2:1**, referencia R=500, sin adds, sin Gerard activo, sin progresión por ganancias, sin BE ni extensión. |
| Funded | Buscar el importe elegible de retiro; no heredar el techo diario de 870 ni consistencia de evaluación. Referencia 2.250; alternativas 2.300, 2.500 y 3.000. |
| Sesión | Sólo NY, sin exposición ni órdenes ejecutables de un día a otro. Preferencia por comenzar después de los primeros 30 minutos. |
| Indicadores | Todos en Echo. NinjaTrader es adaptador de feed/ejecución; no es dueño de indicadores, señales ni MM. |
| Horizonte | Ventanas de datos válidas y horizonte común explícito. No la urgencia personal del Owner. |
| Disco | Resultado compacto durable y temporales acotados; limpieza automática sólo de lo generado por cada corrida autorizada. |

**Fuera del experimento:** cinco cuentas personales, sus resets, diez intentos y plazo personal de dos semanas. No pedir esos saldos, no importarlos y no crear escenarios personales. Tampoco modelar 41 cuentas compradas inicialmente: 41 compras y USD 80 sobrantes son sólo capacidad aritmética inicial con costo 120, antes de otros costos y reinversión; no un tope vitalicio ni un inventario concurrente.

«A tope» significa completar pase/retiro o consumir el intento lo más rápido posible dentro de límites y pausas declarados. No exige violar una regla para quemar una cuenta, prolongarla después de completar el objetivo ni demostrar una estrategia rentable para capital propio. PnL BASIC negativo, drawdown elevado o cuentas perdidas no son motivos para declarar averiado el motor ni para retirar una variante del catálogo.

## 4. Perfil de prop: versión explícita, no reglas inventadas

El programa de referencia es Earn2Trade GAU50. No reabras la elección entre TCP/GAU ni hagas una investigación de todas las props.

El registro de entrada contiene estas referencias comerciales: target de evaluación 3.000; drawdown 2.000; pérdida diaria oficial 1.100; consistencia de evaluación con mayor día estrictamente menor a 30% del beneficio total al aprobar; EOD en evaluación/LiveSim y regla distinta en Live; hasta cinco evaluaciones y tres funded concurrentes, con como máximo una Live; split del 80% desde solicitud de 2.250 inclusive para el perfil 50K pertinente; calendario de retiro con corte viernes 14:00 CT y procesamiento miércoles; condiciones de activación, cargos y límite LiveSim. Son referencias de documentos anteriores, **no una nueva verificación comercial realizada por este prompt**.

Antes de congelar el perfil, contrasta únicamente los hechos externos materiales con las fuentes oficiales aplicables y versiona sus condiciones por fase/fecha. En caso de diferencia, muestra el delta; no modifiques silenciosamente el costo 120, bankroll 5.000, target interno 870 o pausa interna 1.000, que son inputs del Owner. Una cuenta sintética del simulador usa un perfil versionado; no se reconstruye para ello el inventario personal.

Modela donde afecte el flujo: reglas de admisión y progression ladder, límites por fase, igualdad en umbrales, días/consistencia, fees, profit split, importe bruto elegible, activación, reserva/habilitación funded, solicitud/aprobación/procesamiento/crédito de caja y transición o fin de LiveSim. No heredes cuatro retiros por cuenta ni split del 100% del perfil funcional antiguo. No permitas retiros infinitos por no haber implementado una transición.

Cuando una latencia o costo adicional no esté acreditado, documenta el supuesto como escenario parametrizado y su efecto; no lo llames hecho verificado. Separa los USD 120 por compra de costos adicionales acreditados y evita doble cargo. No sustituyas datos faltantes por cero oculto. Un perfil hipotético claramente identificado no es certificación comercial Earn2Trade.

El Owner confirmó que su sistema algorítmico propio está permitido y no es un copier. No reabras esa discusión ni introduzcas `LIVE_AUTOMATION_UNCONFIRMED`. Este mandato sigue sin autorizar ejecución real, compras reales ni cambios de cuentas.

Fuentes dirigidas para el perfil: `https://www.earn2trade.com/gauntlet-mini`; `https://help.earn2trade.com/en/articles/3849975-what-is-the-maintain-consistency-rule`; `https://help.earn2trade.com/en/articles/5372687-how-does-end-of-day-drawdown-work`; `https://help.earn2trade.com/en/articles/3395926-how-is-my-daily-loss-calculated`; `https://help.earn2trade.com/en/articles/5660666-can-i-have-multiple-trader-career-path-gauntlet-mini-and-live-livesim-accounts`; `https://help.earn2trade.com/en/articles/5452472-what-is-the-withdrawal-policy`; `https://help.earn2trade.com/en/articles/12036369-how-do-i-request-a-withdrawal`; `https://help.earn2trade.com/en/articles/6877364-what-happens-when-i-complete-my-evaluation`; actualización referenciada: `https://www.earn2trade.com/blog/earn2trade-evaluation-rules-profit-split-update/`.

## 5. Límite entre preparar el motor e implementar variantes

Deja una matriz `capacidad → propietario actual → reutilización/delta → prueba → consumidor de GLM`. Diseña sólo para los consumidores reales del anexo; no un framework universal de estrategias/props.

### Lo que debe resolver A, mediante TOPs

Campaña multicuenta secuencial con compra/reinversión, aislamiento y continuidad; perfil comercial y límites en sus propietarios; fuentes/reloj/ejecución causal reutilizados; composición pública que permita Strategy y políticas de gestión independientes; configuración completa y reproducible; eventos/órdenes/contabilidad necesarios para adds, reemplazo de SL/TP y BE; salida compacta; ejecución de lotes retomables; identificación de configuraciones y resultados; pruebas y documentación.

No basta dejar interfaces para futuras capacidades. La etapa A debe demostrar por pruebas ejecutadas que se puede suspender/reanudar cuentas, componer otra Strategy/MM, modificar cantidades y salidas económicas, procesar cobros y correr una matriz sin modificar internals del backtester por cada variante. Los controles de prueba pueden ser módulos deterministas pequeños por interfaces públicas; no necesitan ser una TradesGerard rentable.

Reutiliza indicadores existentes. Si falta infraestructura o un primitivo compartido imprescindible de analytics para el contrato, impleméntalo mínimamente con TOP y documenta el propietario. Si lo que falta es la regla concreta de Strategy o una política experimental, queda en B. No conviertas esta distinción en una excusa para dejar a GLM una refactorización estructural sin resolver.

### Lo que debe resolver B, mediante GLM

La señal productiva `tradesgerard`, indicadores concretos que queden asignados a B, política mínima de sizing, todos los ratios, progresión, B2, salidas, targets y políticas experimentales del anexo; su registro en las factories/superficie pública; pruebas locales; matriz completa; backtests, validación y análisis de retiros/caja.

GLM puede añadir módulos de dominio y registrarlos. No debería necesitar reconstruir scheduler, accounting, lifecycle o recorder para cada idea. La declaración `READY_FOR_GLM` no significa que las estrategias ya estén implementadas ni que todas hayan sido probadas; significa que la plataforma y el contrato de implementación están listos y demostrados.

## 6. Semántica obligatoria de campaña

### Estado y propiedad

Cada cuenta mantiene identidad, fase, saldo/equity, piso, máximo EOD, PnL diario, mayor día, progreso, posición/órdenes/reservas, MM mutable y obligaciones. Compartir mercado y analytics compatibles no comparte estado financiero ni señales retrospectivas. El controlador administra la caja de campaña; no crea otro ledger paralelo que recalcule trades desde resultados agregados.

Sólo la cuenta con el turno puede abrir nuevas operaciones. Rotar requiere estar flat y haber resuelto cancelaciones, fills parciales y órdenes todavía ejecutables; un estado lógico cerrado no basta. No usar la misma señal consumida para abrir en la siguiente cuenta ni reiniciar el feed o indicadores por conveniencia al comprar/reemplazar.

Preferencia inicial KISS: cuenta existente elegible antes que comprar; compra a demanda si no hay elegible, hay caja/plaza y existe operativa futura admisible. Selección inicial en orden estable; las alternativas de prioridad posteriores están en el catálogo. La identidad de cuenta y su turno no se deducen de un nombre de archivo.

### Días, tiempo y riesgo

EOD, resets diarios, habilitaciones y cobros transcurren para todas las cuentas, incluidas las pausadas. Distingue sesión NY de operativa, día contable de la prop y timezone del Owner; usa zonas IANA y calendario, no offsets fijos. En EOD cambia el piso conforme al perfil; no se regeneran pérdidas. El piso vigente se controla durante la sesión.

La pausa interna de -1.000 considera el PnL de liquidación y costos definidos, no sólo número de stops. El límite real de cuenta puede fallar antes. Si no cabe una operación válida, el intento sigue existiendo aunque deba esperar; no autorizar un fill inválido para gastar exactamente el presupuesto.

Ganar amplía el headroom desde equity, no cambia el límite reglamentario. Revalidar órdenes y modificaciones con exposición y reservas account-wide. No restar dos veces una pérdida ya reflejada en equity ni reiniciar el presupuesto del ciclo tras un fill parcial.

### Fases, caja y terminalidad

Al aprobar no nace instantáneamente efectivo ni una funded operable sin condiciones. Separar todos los eventos de fase y pago, aplicar cupos y latencias, mantener idempotencia. Debitar compras al ocurrir, acreditar retiros netos una vez, reservar importes pendientes cuando corresponda y modelar su efecto en el saldo/piso de cuenta. No usar un cobro futuro para una compra anterior.

No terminar por `cash < 120` si una cuenta existente puede operar o un pago futuro admisible puede financiar continuidad. No comprar otra cuenta porque se pausó una que volverá mañana cuando el cupo ya está lleno. Distingue ruina real de campaña, espera, fin del horizonte, datos insuficientes y fallo técnico.

Al acabar los datos/horizonte, no cobrar pendientes después del corte, no convertir PnL de cuentas en caja, no cerrar al último precio inventado. Registra cuentas y obligaciones censuradas. Mantén BASIC y la reproducción de perfiles históricos; una campaña nueva no altera retroactivamente los resultados antiguos.

## 7. Contrato de Strategy, gestión y ejecución para GLM

Señal B: K lenta anterior <20 y actual >=20 da LONG; anterior >80 y actual <=80 da SHORT. Barras cerradas 1m. Estocástico lookback 20 y ATR(20) en Echo. Suavizados K=3/D=3 y multiplicador ATR=2 son candidatos iniciales documentados, no óptimos probados. D no añade por sí solo un filtro de cruce. Cierra fórmula, semilla, warmup, high=low, discontinuidades y reset de contrato; no abras un grid de indicadores.

ATR propone escala de distancia y sizing; R/T económicos y límites tienen autoridad. Cantidades enteras, tick grid, costos y slippage pueden impedir clavar simultáneamente importe, ratio y múltiplo ATR exactos. Define precedencia y redondeo; reporta R/T, distancia y ratio efectivos. Sin fracciones de contrato ni ampliación oculta de presupuesto. NQ es el instrumento inicial de los datos conocidos; no simular fills MNQ cambiando sólo el multiplicador.

SL, TP y BE pertenecen al resultado económico neto de la operación agregada, con todas sus entradas/cierres parciales/costos. Los ejemplos 500/250 y 1.000/250 no son montos por ticket. R permanece congelado dentro del ciclo; la progresión sólo afecta una nueva operación.

B2 debe poder aumentar exposición adversa y recalcular **ambos precios SL y TP**, acercando las distancias económicas según cantidad/promedio, sin aumentar R/T originales. No imponer stop estructural inmóvil ni la reserva 60/40 retirada. Un add imposible o un nuevo SL del lado inválido del mercado se rechaza; no inventar cancel/replace atómico ni ignorar órdenes viejas ejecutables. B2 es una variante explícita; no mutar silenciosamente GerardMM legacy.

Progresión con ganancias: conservar por separado aumento de R con T proporcional, aumento de R manteniendo T corto, y ambas combinadas con B2. `R_preferido = R_base + alpha × max(PnL_día_realizado_neto,0)`, alpha=1, es fórmula candidata, no ley de probabilidad ni autorización a usar ganancias flotantes. El contrato debe fijar cómo se resetea/actualiza tras pérdidas. No asumir que el segundo TP es más probable sólo porque ocurrió el primero.

Gestión de remanente: target ordinario 870. Con tres días limpios de 870 faltan 390 para 3.000; pérdidas y consistencia cambian el remanente real. Conserva las alternativas de día terminal completo y ajustado sólo mientras la transición de fase permita actuar. No elegir sólo por prolijidad aritmética; no esconder que cortar únicamente T cambia el ratio. `FIT-EXACT-FIXED`, `FIT-EQUAL`, `FIT-REMAINDER` y `FIT-BAND` tienen contratos diferentes.

BE a +200 y extensión a +500 son variantes posteriores. Definir precedencia frente a TP, objetivo de cuenta, cierre de sesión y adds. Un TP que ya era 500 no se extiende; un TP <=200 puede hacer el trigger inactivo. La configuración debe declarar si el trigger es por cierre o intrabar y qué ocurre al combinar extensión y target final. No certificar simultáneamente un cierre al tocar 870 y un runner permitido por encima de ese mismo tope.

Todas las decisiones respetan el primer instante en que se conoce su información. No fills retroactivos al cierre que produjo la señal ni BE/SL activados usando un high/low futuro. Con OHLC1m se declara el modelo causal, su ambigüedad y sensibilidad; camino sintético no equivale a ticks observados. Reutiliza la semántica vigente y sus prioridades, sin sustituirla silenciosamente por otra. Una variante que requiere datos ausentes queda identificada, no falsamente probada con otra temporalidad.

Horario candidato inicial: 10:00–15:55 `America/New_York`; inicio/fin son decisiones operativas de diseño aún no congeladas por el Owner. La alternativa desde apertura se conserva. Fija un corte de nuevas entradas y liquidación antes del fin de sesión, con warmup previo y sin órdenes pendientes overnight. No heredar 09:35–11:30 del prompt V2.

## 8. Salida compacta, límites de recursos y continuidad del lote

Este es un requisito de entrega, no una mejora opcional después de llenar el disco.

En modo de búsqueda, evita generar copias de mercado, snapshots por evento, spools y logs ilimitados que luego se borrarán. Conserva un resultado compacto por experimento con: configuración resuelta/ID, source y binario, modelo de ejecución, identidad/hashes de datos originales, fechas/perfil/reglas, estado/primera causa, operaciones agregadas, tabla por cuenta/día, ledger de compras/cobros/costos, métricas y diagnósticos acotados. Las trazas extensas de pruebas pequeñas sólo se conservan cuando son evidencia necesaria; no una colección de gigabytes por cada backtest.

Define antes de ejecutar máximos de temporales, salida final, logs, concurrencia y espacio de reserva a partir del volumen realmente disponible. El resultado puede crecer con operaciones/cuentas, no con cada tick/snapshot. Mide pico temporal y tamaño final en la validación. No reemplaces el problema de disco por retener todas las trazas en RAM.

Default de seguridad operativa: un escritor de producto y una campaña financiera a la vez. No medir mientras compiten tus builds/suites/replays. No elevar concurrencia automáticamente para recuperar tiempo ni crear un cluster/servicio nuevo.

Finalización: detener/drenar trabajo y escritores → persistir resultado durable fuera del temporal → verificar lectura, integridad y conciliación → eliminar sólo temporales propios de esa corrida → comprobar espacio liberado y registrar cleanup. Sin borrados globales, sin corpus, binarios, releases, evidencia histórica ajena, caches compartidas ni campañas previas del Owner. No hay autorización para sanear discos eliminando otros archivos.

Fallo/cancelación/timeout también dejan resultado compacto no- COMPLETE, primera causa y evidencia acotada. Diseña la ruta de disco lleno para que pueda guardar el mínimo diagnóstico usando el espacio reservado; no ocultar el fallo ni borrar trazas ajenas para salir del paso. Si no se puede preservar el resultado, informa la falla de entrega en vez de certificar éxito.

El modo de certificación/replay existente sigue disponible. Comparar modo compacto y detallado sobre mismos inputs debe dar iguales decisiones/resultado económico, salvo diferencias expresamente propias de retención. Un resumen con hashes no sustituye por sí solo las trazas requeridas por el replay oficial. Para reejecutar se conservan referencias accesibles a corpus, build, configuración y modelo; si hay que regenerar trazas, se dice.

El lote usa un plan finito y un registro compacto de progreso. Cada identidad incluye variante y parámetros completos, perfil, datos/ventana, build y modelo. Skip sólo de resultados completos que coincidan exactamente; no reutilizar después de cambiar código/reglas/datos. Intentos fallidos conservan causa e ID y no desaparecen del denominador. Retomar un lote no restaura una campaña truncada ni autoriza usar un spool incompleto como checkpoint.

Reintentos acotados tras una causa identificada y resuelta; sin escalera infinita de timeouts. Si se agota tiempo/herramientas/cuota, cerrar procesos propios de forma verificable y dejar checkpoint real, configuraciones completadas y pendientes. No prometer continuidad autónoma que el harness no pueda ejecutar.

## 9. Matriz finita y handoff experimental completo

El anexo es inventario de obligaciones y candidatos, no una afirmación de implementación. Conserva cada ID, origen, parámetros, compatibilidad y estado. Los controles propuestos ya registrados forman parte del diseño experimental a completar; las variantes retiradas no se reactivan por la palabra TODAS.

Antes de que GLM mida, cada familia debe tener parámetros finitos y composición/precedencia explícitas. Para detalles sin número todavía —cantidad de add, alpha, tolerancia, corte horario, prioridad— selecciona un candidato mínimo justificable dentro de la idea, documéntalo como decisión de diseño y déjalo sustituible. No abras ranges infinitos ni una grilla de nuevos umbrales. Una limitación material que no puedas cerrar queda visible y evita declarar el contrato completo.

La matriz cruza los ejes compatibles de ratio/riesgo base, progresión, adds, ajuste al remanente, secuencia de pase, salida/temporalidad, sesión, prioridad de cuenta y target de retiro. No reemplazar la exploración combinada por estudiar cada eje por separado y elegir ganadores marginales. Se puede ejecutar por etapas, pero la cobertura final debe explicar cada combinación finita vigente.

Sólo se colapsan equivalencias demostrables de configuración/semántica, conservando alias y prueba de equivalencia; nunca porque dos variantes casualmente dieron igual PnL. Combinaciones incompatibles y negativos reglamentarios quedan enumerados con motivo. Una configuración aún no implementada, sin datos o fallida técnicamente no es incompatible por esa sola razón.

Primera referencia de B: tres ratios estáticos, con el resto de políticas y target de retiro 2.250 fijados para poder comparar. Después todas las variantes y cruces registrados, incluidos 2.300, 2.500 y 3.000 por retiro. No volver a 750/885/897/900 como targets diarios ni implementar la estrategia A por rescatar historia.

Todos los backtests comparables parten de 5.000, compran a 120 y usan mismo horizonte, calendario, costos y política de compra. Usa corpus válido; no repetir all13 con las mismas carencias ni inventar tres años completos. Ventanas de desarrollo y validación se fijan prospectivamente; el horizonte no se cambia según quién va ganando. No usar diez intentos o catorce días como marco impuesto.

Ranking: caja neta de campaña y cobros, con probabilidad empírica de al menos un cobro, muestra/incertidumbre, tiempo, cuentas compradas/perdidas/pasadas, costos y caja mínima/final. Dinero pendiente se reporta separado. No imponer Sharpe o PnL BASIC positivo. Tampoco llamar rentable a una variante sólo porque tuvo un retiro o terminó primera entre resultados negativos. Reportar conflictos entre mayor probabilidad de cobrar y mayor caja, sin ocultarlos en un score arbitrario.

Diagnóstico: rachas reales de operaciones/días; frecuencia de segundo/tercer TP tras TPs previos; frecuencia de alcanzar 870 antes del límite diario; ATR, cantidades, distancias, costos y motivos de rechazo. Conserva el orden temporal: cuentas que comparten recorrido de mercado y ventanas solapadas no son ensayos independientes. No inferir probabilidad de éxito sólo con p^n ni barajar trades destruyendo los estados de cuenta.

Se debe poder concluir que ninguna candidata ofrece caja suficiente. Eso no es un bug del motor ni permiso para seguir optimizando la muestra final hasta fabricar una ganadora. Este mandato no garantiza resultados de mercado.

## 10. Verificación independiente de A: lo que debe quedar demostrado

El TOP adversarial LOCAL prepara casos propios y ejecuta contra la versión integrada exacta. No basta leer el resumen del implementador ni aceptar mocks como resultado E2E. Incluye como mínimo:

| Área | Evidencia mínima |
|---|---|
| Compra/caja | Compra a 120 una sola vez, rechazo sin fondos/plaza, compra posterior sólo tras efectivo disponible; 41 no se interpreta como simultaneidad ni tope después de reinvertir. |
| Turno | Varios trades de una cuenta antes de rotar; cero solapamiento físico de exposición/órdenes; señales no reutilizadas ni mercado rebobinado. |
| Pausas | Target y -1.000 pausan sin reset/recompra; reanudación conserva saldo/piso/historial; insuficiencia de headroom no fabrica un fill. |
| Calendario | EOD/reset diario/timers de cuenta no seleccionada, fronteras de sesión y cierre flat/cancelado; DST y hora de prop separadas. |
| Fallo | La cuenta puede fallar antes del límite interno por piso real; reposición no borra historia ni otorga reset gratuito. |
| Pase | 3×870+390 en escenario sin pérdidas; pérdida intermedia recalcula; regla 30% exacto como negativo; no bloqueo inicial porque primer día pesa 100%. |
| Cobros | Flujo de pase a funded y solicitud/crédito con latencias/cupos; 2.250 inclusivo según perfil; cuatro targets; split/fees aplicados una vez; pendientes no son caja. |
| Terminalidad | Caja <120 con cuenta utilizable o cobro pendiente no es ruina; fin de horizonte no cobra fuera del corte ni monetiza saldo de prop. |
| Composición | Módulo Strategy/MM distinto por API pública; perfiles por cuenta sin estado compartido; presupuestos, adds y reemplazos con partial/pending fills, rechazos y cancelaciones. |
| Causalidad | No protección ni ejecución anterior a la señal; orden causal de add/SL/TP/BE; diferencia cierre/intrabar representada o limitación explícita. |
| Disco | Mismo resultado en detallado/compacto; pico acotado; resultado preservado y temporales eliminados; cancelación, timeout, error de escritura/disco lleno; no borrar datos ajenos. |
| Lote | Reanudación omite sólo completos idénticos; build/config diferentes invalidan reutilización; fallidos visibles; conteo esperado/completado/pendiente consistente. |
| Regresión | BASIC, campañas/replay previos y módulos legacy relevantes mantienen sus contratos; un bug real corregido se distingue de un cambio silencioso de modelo. |

Fixtures deterministas pueden forzar un camino de pase/cobro/fallo para probar el motor: deben estar rotulados como datos de prueba y nunca figurar como rentabilidad de TradesGerard. Complementa con smoke real sobre datos válidos, por superficie pública, sin exigir que gane dinero.

Prioriza dinero, causalidad, aislamiento, terminalidad y borrado seguro. Aplica la política de coverage vigente al desarrollo nuevo, con mínimo 95% donde corresponda; separa baseline heredado y delta, no cambies denominadores para hacer verde una cifra. Tests, comandos, outputs compactos y correcciones deben ser reproducibles y estar ligados a source/binario.

Si una capacidad material de este contrato no está demostrada, el estado no es READY_FOR_GLM. Se permite `BLOCKED` o `PARTIAL` con causa y siguientes pasos; no rebautizar el gap como tarea de GLM para declarar éxito.

## 11. Orquestación y límites de ejecución

Usa el harness local existente. Comprueba herramientas, checkout, accesos de trabajo y capacidad real de lanzar/esperar/recoger resultado de subagentes antes de depender de ella. No crear esta noche un sistema nuevo de agentes ni integración entre proveedores. Si no puedes despachar físicamente, dilo y entrega el mandato acotado pendiente, sin fingir que un TOP corrió.

TOPs despachados por GOD: Sol 6.1 solicitado conforme a la preferencia de esta iniciativa. Distingue modelo solicitado y servido; si no se expone el segundo, UNKNOWN. Si no está disponible el requerido, no sustituir silenciosamente. GLM-5.3-Flash tiene el encargo de la etapa B; no asumir que una conexión diferente permite lanzarlo desde el mismo harness.

Un coordinador, un integrador por versión, especialistas one-shot con inputs/propietarios/entrega verificables. Paralelismo sólo realmente disjunto y sin source cambiante durante compilación/medición. No consumir GOD en razonar cada barra ni hacer miles de prompts para lanzar experimentos; el barrido lo realiza código determinista.

Continúa con decisiones técnicas ordinarias y correcciones dentro del mandato; no pidas al Owner autorización repetida para lo ya encargado. No ejecutar merges a rama productiva, deploy, egress de trading, órdenes LIVE, compras/resets reales ni cambios a servicios del homelab. No abrir secretos ni persistirlos. Código Echo sigue el carril autorizado por sus instrucciones; preservar trabajo ajeno y dejar commits/build de desarrollo identificables, no release productiva limpia desde feature.

Agents-OS se trabaja directamente en **master**, sin ramas ni PRs. Respetar su materialización canónica y protección concurrente. Mantener control y documentación pertinentes; no sobrescribir BTG-PLAN ni marcar gates históricos como aceptados. Los archivos del vault contienen referencias compactas, no corpus, binarios ni logs pesados.

Este manager no ejecuta feedback ni cierre de sesión salvo petición explícita del Owner. Los encargos one-shot pueden pedir expresamente a cada worker evidencia, feedback por fricción y cierre de SU propia sesión; eso no cierra al manager ni al proyecto. No confundir terminar una corrida y limpiar sus temporales con cerrar Agents-OS.

## 12. Documentación y entrega: condición de finalización

Persistir en una ubicación única pertinente bajo Echo Futures. Ruta de trabajo sugerida, a resolver/reutilizar sin duplicados: `main/10-projects/Echo Futures/artifacts/tradesgerard/`. Los nombres siguientes son roles de documentos propuestos, no afirmaciones de que ya existen:

**Control de iniciativa:** requisitos/decisiones vigentes, etapa, evidencias, bloqueos y siguiente acción. Una sola fuente de estado.

**Contrato y diseño acotado:** propietarios, deltas, esquema de configuración, precedencias, ciclo financiero, salida/recursos y fronteras A/B. No réplica del manual entero.

**Catálogo de experimentos:** IDs del anexo, parámetros completos, compatibilidades y estado; formato utilizable para generar un plan finito. Sin dos catálogos manuales que puedan divergir.

**Evidencia A y handoff:** source/branch/commits, build/hash, pruebas independientes/correcciones, recursos/disco, comandos verificados, corpus autorizado, perfil versionado y tareas que legítimamente quedan para GLM.

**Manual público del backtester:** actualizar el existente con uso, configuración y alcance de modos, lote, salida y cleanup. Nada de flags inventados ni un segundo manual desactualizable.

**Prompt maestro GLM:** autosuficiente, con autoridad exacta del artefacto entregado, contratos y catálogo; orden baseline → implementación de familias → todas las combinaciones → validación → ranking; tests, límites de recursos, limpieza, continuidad y documentación. Debe encargar IMPLEMENTAR todas las variantes, no sólo ejecutarlas. No lanzarlo ahora.

Todos los archivos y comandos del handoff deben existir y haber sido leídos/verificados. No referencias sólo en el disco temporal de una herramienta cloud ni enlaces a hashes de una build distinta. Si un commit/push/persistencia no ocurrió, se informa pendiente. Los paths operativos se resuelven desde el workspace; no dejar rutas personales absolutas como autoridad.

Tu respuesta final debe incluir estado `READY_FOR_GLM`, `PARTIAL` o `BLOCKED`; capacidades realmente entregadas frente al contrato; source/build; resultado de verificación y disco; documentación/recetas y prompt GLM; alcance pendiente explícito. `READY_FOR_GLM` es readiness técnico, no aceptación final del Owner, certificación LIVE ni prueba de rentabilidad.

## 13. Empieza ahora

Carga la autoridad mínima, comprueba capacidades locales y estado real, materializa este alcance sin perder los IDs, prepara el diseño acotado y despacha TOPs. Después verifica de forma independiente, corrige y entrega. No cierres la primera respuesta con otra propuesta de empezar ni pidas de nuevo nombre, bankroll, costo, target, inventario personal o finalidad del experimento.

---

# ANEXO — CATÁLOGO CONSERVADO DE VARIANTES Y ALTERNATIVAS

Este anexo conserva los IDs y el origen del registro leído. Los estados «posterior», «POR_PARAMETRIZAR» y «PENDIENTE_DE_PRUEBA» indican el trabajo que debe cerrar el diseño/etapa B, no una excusa para omitirlo. Ninguna variante ha sido ejecutada por preparar este prompt. Los controles propuestos se documentan como tales; los retirados permanecen excluidos. Las reglas del cuerpo anterior gobiernan la separación GOD/TOP → GLM y la entrega actual.

## 4. Registro exhaustivo de variantes discutidas y controles propuestos

Los IDs son estables. `PENDIENTE_DE_PRUEBA` no significa implementado. `POR_PARAMETRIZAR` conserva una idea que todavía no tiene todos los números. `RETIRADA_POR_OWNER` preserva historia sin reabrir decisiones. `NEGATIVO_REGLAMENTARIO` debe probar el rechazo/continuidad correcta, no competir como estrategia aprobable. Los controles adicionales propuestos por el asistente están identificados y no se convierten en decisiones aceptadas.

### 4.1 Señal y escala técnica

| ID | Variante | Origen / estado |
|---|---|---|
| SIG-B | Recuperación del umbral 20/80 en K lenta, cierres 1m; sin filtro K/D adicional. | Owner eligió B; PENDIENTE_DE_PRUEBA. |
| SIG-A | Entrada al encontrarse dentro de sobreventa/sobrecompra en un episodio. | Idea literal inicial; RETIRADA_POR_OWNER al elegir B. No se borra del historial. |
| VOL-20 | ATR(20) como escala de precio y sizing económico. | Owner; base PENDIENTE_DE_PRUEBA. |
| VOL-K2 | Multiplicador ATR inicial 2, constante en el primer barrido; semilla/suavizado/warmup por especificar. | Propuesta anterior; POR_PARAMETRIZAR. No abrir una optimización masiva del indicador ahora. |

### 4.2 Cantidad constante durante la operación: primera familia

| ID | Riesgo:beneficio | Referencia económica | Estado |
|---|---|---|---|
| STA-11 | 1:1 | R=500; T=500. | Primera familia; PENDIENTE_DE_PRUEBA. |
| STA-15 | 1,5:1 | R=500; T≈333,33. | Primera familia; PENDIENTE_DE_PRUEBA. |
| STA-21 | 2:1 | R=500; T=250. | Primera familia; PENDIENTE_DE_PRUEBA. |
| STA-41-CONTROL | 4:1 | R=1.000; T=250; sin adds. | Control adicional propuesto para aislar el efecto de los adds de DYN-41. No fue orden de entrada real. PENDIENTE_DE_PRUEBA como candidato propuesto. |

R=500 es la referencia discutida. Mantenerlo exactamente en cada trade y adaptar lotaje/targets al remanente diario son políticas diferentes, registradas por separado en la sección 5. No ocultar los R/T efectivos de ninguna configuración.

### 4.3 Aumento de posiciones dentro de una operación: posterior

| ID | Variante | Estado / parámetros |
|---|---|---|
| DYN-B2 | GerardMM B2: adds adversos, SL y TP recalculados y acercados; R/T económicos del ciclo permanecen fijados al entrar. | Owner; posterior, POR_PARAMETRIZAR. No alterar legacy. |
| DYN-41 | R=1.000; T=250; aumento de posiciones adverso y recálculo de SL/TP; riesgo:beneficio 4:1. | Nueva idea del Owner; posterior, POR_PARAMETRIZAR. |
| DYN-RR-CONTROLS | DYN-B2 comparado con STA-11/15/21 a igual política de presupuesto, para distinguir gestión del efecto de cambiar el ratio. | Comparación adicional propuesta; POR_PARAMETRIZAR. |
| ADD-N1 | Como primer nivel de complejidad, una entrada y como máximo un add. | Propuesta anterior conservada; no límite final ya aprobado. |
| ADD-D25 | Gatillo de add a 25% de la distancia inicial de referencia adversa, respetando admisibilidad con SL económico recalculado. | Distancia propuesta; PENDIENTE_DE_PRUEBA posterior. |
| ADD-D50 | Gatillo al 50% de esa distancia. | Distancia propuesta; PENDIENTE_DE_PRUEBA posterior. |
| ADD-D75 | Gatillo al 75% de esa distancia. | Distancia propuesta; PENDIENTE_DE_PRUEBA posterior. |
| ADD-SIZING | Magnitud y eventual curva de los adds. | POR_PARAMETRIZAR; no inventar duplicación 1→2→4 ni aumento ilimitado. |
| ADD-FIXEDSTOP-6040 | Stop de precio inmóvil, presupuesto reservado aproximadamente 60/40 para entrada/add. | Propuesta V2 sustituida por la aclaración económica del Owner; RETIRADA, no reintroducir como B2. |

El lugar del gatillo no obliga a poder ejecutar el add. Si el SL recalculado ya es inválido, el mercado saltó el nivel, el piso real no lo permite o no se puede proteger la exposición, no fabricar la entrada. Registrar causa. Ganar dinero al reducir la exposición no demuestra por sí solo utilidad del promedio adverso.

### 4.4 Riesgo entre operaciones: distinta dimensión

| ID | Variante | Estado |
|---|---|---|
| RISK-FIX | Sin incremento financiado por ganancias; política determinista de referencia/presupuesto y ajuste de fin de objetivo identificado. | Primera familia, confirmada. |
| RISK-GAIN-RR | Nueva operación: R preferido = R_base + ganancias netas realizadas positivas del día; T=R/rho. alpha=1 es candidato. | Owner quiere conservar aumento después de ganar; fórmula propuesta, posterior. |
| RISK-GAIN-TP | Después de un TP, aumentar riesgo disponible para la siguiente operación manteniendo TP corto. Registrar precio de ambas salidas, tamaño y ratio efectivo. | Owner reitera esta hipótesis para mejorar el segundo TP y las rachas; fórmula exacta POR_PARAMETRIZAR; posterior al baseline. |
| RISK-GAIN-ADDS | Combinar progresión entre operaciones con B2 intratrade. | Combinación futura compatible, POR_PARAMETRIZAR; nunca autoriza aumentar R del ciclo ya abierto. |

La ganancia flotante no se convierte en caja ni en beneficio realizado. El límite diario oficial no se amplía: puede aumentar la distancia al piso de la sesión tras una ganancia. Comparar consumo efectivo del límite interno -1.000 y del piso de cuenta, no solamente riesgo nominal.

### 4.5 Targets diarios de evaluación y secuencias de pase

| ID | Variante | Importes sobre target 3.000 | Estado |
|---|---|---|---|
| DAY-25 | Target diario 750. | 750. | RETIRADA_POR_OWNER al fijar 870 único; no ejecutar como comparación. |
| DAY-29 | Target diario ordinario fijo. | 870. | OWNER_CONFIRMED; único target diario vigente. |
| DAY-295 | Microtarget 885. | 885. | RETIRADA_POR_OWNER; no probar ni sustituir silenciosamente. |
| DAY-299 | Microtarget 897. | 897. | RETIRADA_POR_OWNER; no probar ni sustituir silenciosamente. |
| SEQ-HIGH-RESIDUAL | Días de 870; cierre con remanente de aprobación. | Sin pérdidas: 870×3+390=3.000. | Idea Owner; PENDIENTE_DE_PRUEBA. |
| SEQ-HIGH-FULL | Mantener 870 también en el día terminal como contraste con ajuste por remanente, sólo mientras la fase permita seguir operando. | Sin pérdidas: 870×4=3.480. | Variante de gestión registrada, no nuevo target diario; nunca ignorar una transición efectiva de fase. |
| SEQ-30-10 | Antigua secuencia 900/900/900/300. | 30% exacto. | RETIRADA como estrategia por target 870 único. Puede conservarse sólo como caso de prueba reglamentario del motor, no como backtest adicional. |
| SEQ-30-EXCESS | Antigua secuencia 900/900/900/310. | Target 900. | RETIRADA_POR_OWNER al fijar 870; no ejecutar. |
| SEQ-REPLAN-LOSS | Tras pérdidas en cualquier día, recalcular remanente y consistencia con el estado real, sin comenzar artificialmente de cero. | Mayor día / PnL total <0,30; PnL total≥3.000. | Idea Owner “si fallo buscar otro día alto”; política adaptativa POR_PARAMETRIZAR. |
| SEQ-FIXED-LOSS-CONTROL | Después de una pérdida, volver al target alto fijo de la variante en lugar de planificar un día terminal menor. | Conserva target alto; puede sobrepasar el mínimo necesario. | Control propuesto frente a SEQ-REPLAN-LOSS; posterior. |

DAY y SEQ son dimensiones relacionadas: no ejecutar combinaciones duplicadas con dos nombres y contarlas como evidencia independiente. Registrar equivalencia si dos configuraciones producen la misma política. El último día de remanente puede ser menor a 870; no bloquearlo con un mínimo diario artificial. DAY-29 es el único target ordinario habilitado. Los valores retirados no vuelven al barrido bajo IDs diferentes.

### 4.6 Salidas: sólo después de tener referencias

| ID | Variante | Estado |
|---|---|---|
| EXIT-FIX | SL/TP económicos sin protección ni extensión. | Primera familia confirmada. |
| EXIT-BE200 | Al alcanzar +200 netos liquidables del conjunto, activar BE económico y mantener el TP correspondiente a la variante. | Propuesta conservada; posterior. |
| EXIT-BE200-TP500 | Al alcanzar +200, activar BE económico y sustituir una vez el objetivo por +500. | Owner; posterior. |
| EXIT-ONCLOSE | Trigger de BE conocido al cierre 1m. | Variante temporal pendiente, explícita; no equivalente a intrabar. |
| EXIT-INTRABAR | Trigger al tocar el umbral dentro de la barra, con evento causal suficiente. | Variante temporal pendiente; OHLC no acredita ticks ni orden observado. |

Un TP inicial de 500 no se “extiende a 500”; esa combinación equivale sólo a BE. Si el TP inicial es <=200 o el objetivo terminal de cuenta impide llegar al umbral, la configuración es incompatible/inactiva y debe quedar explicada, no contada como un ensayo distinto. Toda extensión respeta la política de objetivo diario y de sesión, o registra un perfil distinto que permita superarlo; no prometer ambas salidas simultáneamente.

### 4.7 Sesión, funded y selección de cuenta

| ID | Variante | Estado |
|---|---|---|
| NY-OPEN | Sesión NY desde su apertura, como contraste del “quizás después de 30 minutos”. | Alternativa mencionada implícitamente; POR_PARAMETRIZAR, no habilitada ahora. |
| NY-PLUS30 | Entrada desde 10:00 America/New_York como interpretación propuesta del retraso de 30 minutos. | Preferencia actual; fin/corte de nuevas entradas por definir. |
| NY-END | Liquidar posiciones y cancelar órdenes antes del cierre de la sesión elegida; ventana tentativa hasta 15:55 NY. | Flat obligatorio; hora 15:55 es propuesta, no hecho aprobado. |
| NY-V2-WINDOW | 09:35–11:30 NY de V2. | Propuesta antigua sustituida; RETIRADA, no restricción silenciosa. |
| PAY-2250 | Objetivo de solicitud de retiro bruto 2.250; desde este importe aplica el tramo del 80% pertinente. | Primera referencia funded. |
| PAY-2300 | Objetivo bruto 2.300. | Variante mencionada por Owner; posterior. |
| PAY-2500 | Objetivo bruto 2.500. | Variante mencionada por Owner; posterior. |
| PAY-3000 | Objetivo bruto 3.000. | Variante mencionada por Owner; posterior. |
| FUND-FAST | Funded sin techo diario de consistencia; buscar el retiro elegible tan pronto sea posible dentro de riesgo/sesión. Pausar al quedar solicitud preparada. | Dirección Owner; POR_PARAMETRIZAR. |
| FUND-PENDING | Política entre elegibilidad, solicitud, aprobación y cobro: pausa hasta resolución para no exponer el retiro pendiente. | Propuesta inicial; no garantía de preservación del pago. |
| ROT-ORDER | Orden estable de cuentas elegibles; usar la seleccionada hasta target/límite/sesión/fallo real, luego rotar. | Persistencia de turno confirmada; orden estable propuesto como baseline. |
| ROT-NEAREST | Priorizar la cuenta más próxima a un primer cobro, usando fase/progreso/fecha de pago ya conocidos. | Propuesta de campaña adicional; posterior, sin información futura. |
| ROT-BALANCED | Alternar prioridad diaria entre las cuentas existentes elegibles, sin cohorte fija de cinco ni rotación después de cada trade. | Contraste registrado de prioridad, no condición personal; posterior. |

No se asume que todos los retiros puedan repetirse indefinidamente en LiveSim ni que el mayor target de retiro produzca más caja o un primer cobro más temprano. Comparar tiempo, split, costos y reglas de transición. En la primera campaña se respeta una sola cuenta ejecutando; la simultaneidad operativa no se añade como variante aprobada.

## 5. Variantes de ajuste de operaciones al target restante

El Owner pide evitar restos incómodos, sin sacrificar la prueba de qué gestión produce mejores rachas y retiros. R=500 exacto, ratio exacto 1:1 y target diario 870 no producen cierre exacto sólo con ganadoras idénticas; una gana 500 y dos ganan 1.000. No esconder esta diferencia diciendo que todo sigue “fijo”.

| ID | Política | Estado |
|---|---|---|
| FIT-EXACT-FIXED | R y T iguales en cada nueva operación; sólo admitir overshoot cuando el perfil declarado lo permite y contabilizar su efecto real sobre pase. | Control de riesgo realmente fijo; puede ser incompatible con banda diaria estricta. |
| FIT-EQUAL | Antes de operar, distribuir el objetivo restante en tramos alcanzables, respetando el máximo de riesgo por ciclo y el ratio. Cantidad queda fija durante cada operación; sin progresión financiada por ganancias. | Alternativa registrada; comparar rachas/cobros sin privilegiarla por su reparto aritmético. |
| FIT-REMAINDER | Recortar proporcionalmente R y T de la última operación al remanente. | Propuesta de V3 conservada como control/fallback, aunque no preferida por Owner. |
| FIT-BAND | Cierre dentro de una banda de tolerancia declarada al objetivo diario, con ratio efectivo y consistencia calculados desde fills. | Variante compatible con el margen que menciona Owner; POR_PARAMETRIZAR. |

Ejemplo aritmético de FIT-EQUAL para target diario 870, sin pérdidas ni granularidad de ejecución: ratio 1:1 → dos tramos de T=435 y R=435; ratio 1,5:1 → tres de T=290 y R=435; ratio 2:1 → cuatro de T=217,50 y R=435. No son resultados ni una modificación ya aprobada del presupuesto exacto de 500. Es una política de presupuesto máximo 500, sin adds y sin progresión tras ganancias, pero no riesgo exacto 500 por trade.

Tras pérdidas o cierres parciales, cambia el remanente y puede cambiar el número de tramos; no garantiza que nunca exista un residuo. Los R/T efectivos respetan cantidades enteras, tick grid, costos y headroom. Si no cabe otro trade permitido, se pausa por falta de presupuesto; no se fuerza alcanzar exactamente -1.000 ni un target exacto inventando fills.
