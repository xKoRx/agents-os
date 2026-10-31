---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo I+D — Futures]]"
sprint:
start:
due:
progress: 0
repo: "xKoRx/echo"
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/echo
created: "2026-10-20"
updated: "2026-10-30"
---

# Echo Futures — Optimización de Campañas

## Estado vigente — EF-CAMPAIGNS-FINAL

**Fecha: 30-10-2026, America/Santiago. CURRENT_TASK_STATE: CONTINUATION. Último mandato LOCAL: READY_FOR_DISPATCH / NOT_STARTED. C06_DELIVERY heredado: PARTIAL. Rama: feature/ef-campaigns-go@a22970c85d139c81c919aafac69f4bf6ceaf5dcd. Master observado: 2baf319ddcba622d9557bc9f23a13787b44c58a7. Histórico completo: reservado al siguiente agente. Merge, despliegue y operación real: pendientes de sus autorizaciones. Manager y programa abiertos.**

El Owner solicita una última sesión coordinadora para completar C06 Go-only, migrar todas las configuraciones aceptadas, demostrar paridad determinista runtime/backtester y comparar campaña anterior/nueva en el último contrato físico NQ de aproximadamente2–3meses. El siguiente agente debe poder ejecutar el histórico completo sin programar funcionalidades faltantes. Objetivo operativo Owner: candidata para el domingo1 de noviembre de2026; no constituye certificación automática ni permiso de órdenes reales.

**Modelos:** GLM-5.3-Flash exclusivamente coordinador. MiniMax M3.1 Flash ejecuta toda implementación, tests, harnesses, reparaciones y verificación. Confirmar modelo/provider efectivo de los workers con una tarea real antes de desarrollar; una etiqueta de rol no lo demuestra. El coordinador mantiene la cola y revisa evidencia, sin escribir código del producto.

## Fuentes y continuidad

Diseño único: [[EF-CAMPAIGN-MODES-DESIGN]] C06. Mandato completo vigente: [[EF-CAMPAIGN-MODES-I0-LOCAL]], cuyo path histórico se conserva. Los prompts GO-S02/S03/S04 anteriores quedan supersedidos como despachos activos, no sus resultados. Conservar los retornos [[EF-CAMPAIGN-MODES-GO-S02-RETURN]], [[EF-CAMPAIGN-MODES-GO-S03-RETURN]], [[EF-CAMPAIGN-MODES-GO-S03R1-RETURN]] y [[EF-CAMPAIGN-MODES-GO-S04-RETURN]].

El planner anterior íntegro permanece en Git: agents-os@bb51f2ecd228047abd31c63edf94c11517d65e8e, blob b089abcfa9a2eebffada261fe844ad2fc71f4624. Esta compactación no elimina evidencia ni crea otro planner. Runtime Pools/R6, retester e I+D conservan sus autoridades; ClutiFX y los demás frentes no cambian por esta nota.

## Situación de entrada y problemas concretos

Las refs fueron comprobadas en GitHub; las pruebas del host se conocen por los retornos, no se ejecutaron desde esta sesión CLOUD.

| Área | Situación |
|---|---|
| Campañas Go | CHALLENGE/FUNDED/SIMULATION y composición reportadas como implementadas; falta cerrar los residuales y la validación real |
| Universo inicial |26nativas+63SG=89configuraciones ejecutables;15aliases;104filas |
| Materialización general |27V2_ADMITTED;62SG bloqueadas por exposición de AccountPolicy;15aliases.26LEGACY_PATH_PRESERVED es otra dimensión de las mismas identidades |
| Configuración faltante |Los presets sellados R01/R03 contienen políticas por identidad: recuperarlas y validarlas; no pedir al Owner transcribir valores conocidos |
| Candidatas |FBC-CH300-15M-R500 y MR-09-R750 tienen una ruta específica de derivación; converger al migrador genérico y evitar doble conteo |
| Prueba mecánica |La factory de candidateMechanicalFixture sustituye Strategy por platformproof.NYStrategy; NO demuestra ejecución de FBC/MR reales |
| Calendario |El derivador candidato conserva CloseSafety como referencia pero no en el request: preservar restricciones efectivas; horizonte no sustituye calendario |
| Runtime |Núcleo SDK compartido; serving RG para modo real requiere integración y certificación de su owner, no simplemente cambiar la guarda |
| Calidad |79,6% coverage diff-aware reportado frente a piso95%; race pendiente;15PASS+5FAIL de21 requiere clasificación de cada fila |
| Economía |Refund necesita productor para una devolución comercial declarada/confirmada, sin inventar devolución automática |
| Validación histórica nueva |0campañas históricas reportadas; último contrato old/new todavía pendiente |

## Objetivo y reglas de aceptación

Una implementación reusable por tipo de Campaign, con Strategy/MM/Provider/Operation y contabilidad del SDK compartidos. Una asociación tiene inventario de cuentas y una activa; varias asociaciones pueden actuar en una trayectoria causal y caja comercial comunes. AccountSlots no es un límite de compras de por vida. La caja nueva SIMULATION conserva4000USD, cero aportes y reinversión del neto recibido; legacy mantiene sus condiciones para comparar.

**P0 determinismo:** repetir inputs/estado/configuración y obtener la misma traza causal de decisiones y negocio.

**P1 compatibilidad:** campaña anterior y nueva, mismo contrato/corpus/warmup/estado/fees/reglas/calendario/market-model. Comparar señales, decisiones, órdenes, fills, protección, cierres y caja por identidad; no sólo PnL agregado. Localizar la primera divergencia. Una corrección legítima del baseline se versiona y justifica, no se disfraza como igualdad exacta ni obliga a preservar un bug.

**P2 runtime replay:** misma operación con los mismos inputs, snapshots, eventos de mercado/control, ACK/fills y tiempo aplicado debe reproducir las mismas decisiones y resultados. Comparar las intenciones antes de aplicar las respuestas grabadas. Velas OHLC con fills simulados no demuestran reproducción exacta de fills del broker. Si falta un input, declararlo; no reducir la comparación para obtener PASS. Separar evidencia RUNTIME_SIM y LIVE observada.

Todos los canónicos aceptados se inventarían y migran, sin expansión cartesiana nueva ni exclusiones silenciosas. El catálogo89 es referencia, no una excusa para omitir módulos/configuraciones oficiales adicionales: conciliar cualquier delta. Aliases sólo con equivalencia demostrada.

## Plan único de cierre

| Ola | Worker MiniMax | Resultado |
|---|---|---|
| 0 |Contexto/código/preflight |Modelos efectivos, HEAD/WIP y fuentes verificados; sin repetir toda la historia |
| A |Configuración/datos |Policies selladas recuperadas, inventario entero, WINDOW_MANIFEST y baseline por identidad |
| B |Campañas/migración |Completar C06, requests genéricos reales, calendario y devolución confirmada; CLI Go |
| C |Runtime/replay |Integración compartida pendiente y P0/P2 mediante adaptadores reales en entorno no económico |
| D |Comparación/conformidad |P1 y reglas de entradas/no entradas/cierres; first-divergence y oráculos independientes |
| E |Verificador fresco |Corpus, adversarial, coverage/race y trazabilidad sin autorrevisión de cambios críticos |
| F |Lote último contrato |Gates por identidad, módulos reales, ejecución física y clasificación completa |
| G |Integración/handoff |FINAL_SHA, evidencia, cola y comandos para histórico; candidata y paquete runtime |

Los workers trabajan por archivos/owners disjuntos con checkout/TMPDIR/outputs propios. GLM integra y adjudica retornos; todos los conflictos de código se resuelven por MiniMax. Reutilizar infraestructura de delegación existente. Si una ruta falla por cuota, comprobar otra autorizada existente; si ninguna puede ejecutar MiniMax, reportar BLOCKED_PROVIDER y la intervención mínima. No sustituirlo por GLM ni inventar workers.

## Último contrato y alcance económico

Seleccionar el contrato físico NQ más reciente con cobertura efectiva suficiente, objetivo2–3meses y mínimo vigente45sesiones elegibles más warmup. Si no cumple, usar el anterior suficiente con fallback explícito y fechas exactas. No elegir por beneficio ni unir vencimientos para fabricar un trimestre. Canarios rollover acotados según el runbook.

El Owner autoriza el lote finito del último contrato del universo admitido, no el histórico completo. Conservar G0→G1→G2A/B/C→G3→G4; G5 queda preparado y no ejecutado. Recuperar receipts compatibles existentes. Ningún gate de una variante se transfiere a otra; no fabricar entradas para lograr un round-trip. D05 afecta sólo la evaluación funded correspondiente, no toda la implementación ni CHALLENGE.

Usar Strategy/MM reales; platformproof queda sólo como fixture técnico separado. Por cada identidad registrar el funnel y explicar cualquier cero relevante. Estrategia técnicamente correcta pero perdedora o rara no se retoca para aprobar: su clasificación económica y su elegibilidad al histórico permanecen separadas. No considerar completo el desarrollo si hay requests/configuraciones recuperables todavía omitidas.

Supervisor único y techo de motores vigente (hasta6incluidos oráculos, sujeto a recursos). Congelar build antes del lote; después de un fix reejecutar sólo evidencia afectada con prueba de alcance. Sin OOM ni procesos huérfanos, sin historia multianual como sustituto de tests.

## Matriz de cierre y entregables

Requisitos C06 R01–R12 y A01–A16 continúan por referencia al diseño y plan preservado; el paquete final detalla su ejecución. No cerrar por compilar, contar manifests o comparar nombres de tests fallidos.

Retorno canónico final a materializar: [[EF-CAMPAIGN-MODES-FINAL-RETURN]]. Evidencia pesada fuera del vault, con paths/hashes y artefactos legibles por máquina:

- Censo source→target y policies/configuración por identidad, aliases sin duplicar.
- WINDOW_MANIFEST y versiones/baselines efectivos old/new.
- P0/P1/P2 por operación; primer evento divergente o traza exacta.
- Funnel y resultados del último contrato, gates y clasificación por fila.
- Pruebas/corpus completo, coverage válido, race, Go-only y capacidad.
- Handoff del histórico: binario/FINAL_SHA, requests, datasets, receipts, queue elegibles/bloqueados y comandos validados sin ejecutar G5.
- Handoff de candidata a Runtime Pools: identidad/configuración real, readiness y bloqueos precisos; sin órdenes reales.

Estados separados: DELIVERY, CATALOG_MIGRATION, LAST_CONTRACT_VALIDATION, P0/P1/P2, FULL_HISTORY_HANDOFF, CANDIDATE_RUNTIME_CERTIFICATION, MERGE/DEPLOY/LIVE. La meta es READY_FOR_OWNER_REVIEW con capacidad completa y paquete ejecutable. Si una dependencia real lo impide, PARTIAL/BLOCKED con causa mínima, no un cierre optimista ni otro prompt para un fix ordinario.

## Permisos y continuidad

No nuevos motores, DSLs, contabilidades o managers. Python I0 permanece referencia, no vía de entrega. No cambiar políticas financieras o señales para empatar resultados. Integrar capacidades runtime con su owner existente y sin modificar entornos productivos por iniciativa. La fecha del domingo no cambia requisitos de seguridad.

Echo: commits en la rama de trabajo reconciliada, candidato y preparación de integración; master/release/deploy requieren su autorización. Agents-OS: master directo, HEAD reconciliado, change_log y lectura remota; sin ramas/PR ni force. Journal privado y secretos se respetan. Notas nuevas mediante materializador/skills. Cierre sólo del encargo local y workers; manager de conversación y programa quedan abiertos.

## Bitácora

2026-10-30 — Nueva instrucción Owner: sesión final GLM coordinador y MiniMax implementadores/verificadores; catálogo completo, determinismo de operaciones, validación último contrato y handoff de histórico. Se actualizan planner y paquete existentes; no se ejecuta código, campañas o despliegues desde esta actualización documental.
