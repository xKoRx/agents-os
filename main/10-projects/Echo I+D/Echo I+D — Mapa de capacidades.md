---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: echo-rnd-capabilities
area: "[[Trading]]"
project: "[[Echo — I+D de Estrategias]]"
created: "2026-10-27"
updated: "2026-10-27"
reviewed: "2026-10-27"
aliases:
  - Echo R&D capability map
  - mapa de skills y runbooks Echo I+D
cssclasses:
  - wide
tags:
  - kind/index
  - area/trading
  - project/echo-rnd
---

# Echo I+D — Mapa de capacidades

## 📊 De un vistazo

Entrada de navegación y auditoría de responsabilidades para [[Echo — I+D de Estrategias]]. El estado del programa y sus decisiones viven en el proyecto; este índice identifica qué autoridad usar en cada etapa. No es otro planner ni reproduce comandos, gates o resultados.

**Alcance de la revisión del 2026-10-27:** contratos de gestión, investigación, extracción, especificación, implementación, cualificación, operación técnica y continuidad que pueden intervenir en las dos líneas; runbook Futures y nueve runbooks Symphony/Forge localizados en `30-resources/runbooks/`. Base documental leída: `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`; los cambios de esta reorganización se trazan en su change log. No se auditó todo el software, todo Aranea ni toda la biblioteca de trading.

**Consolidación de duplicados:** los ocho runbooks bajo `30-resources/runbooks/symphony/` tenían copias con el mismo blob Git bajo `80-agents/memory/public/runbook/symphony/`. Las ocho rutas core se conservan como redirecciones de compatibilidad, sin procedimiento propio y fuera de recuperación normal; el procedimiento vigente se resuelve en la ruta federada. Son ocho procedimientos y ocho redirecciones, no dieciséis autoridades operativas. El runbook adicional `symphony-zeus-troubleshooting.md` tiene alcance propio y no pertenece a esos ocho pares.

Estados de esta auditoría:

- `CONTRATO_INSPECCIONADO`: se revisaron responsabilidad, trigger, entradas/salidas y fronteras documentales; no certifica ejecución actual.
- `NUEVO_CONTRATO`: capacidad creada en esta reorganización; requiere validación documental/forward-test y evidencia separada cuando se use físicamente.
- `NEEDS_REVALIDATION`: instrucciones o evidencia históricas deben contrastarse con fuente/runtime/versiones vigentes antes de ejecutar.
- `DEPENDENCIA_TÉCNICA`: conserva su owner y estado de producto; no es un experimento ni se declara aceptada por incluirla aquí.

Ninguna fila representa una certificación física realizada en esta sesión. Tener una skill o un runbook no concede permiso de campaña, gasto, mutación de infraestructura ni trading.

## 📂 Catálogo

### Gestión y ownership

| Responsabilidad | Procedimiento seleccionado | Estado durable y autoridad | Superficie | Evidencia de salida |
|---|---|---|---|---|
| Dirección global, prioridades entre mercados y decisiones Owner | [[30-resources/agents/skills/echo-rnd-manager/SKILL.md\|echo-rnd-manager]] + [[echo-rnd-cycle-runbook]] | [[Echo — I+D de Estrategias]]; Owner decide cambios materiales | CLOUD con Owner; coordinación directa sólo si existe la capacidad | Decisión aceptada/propuesta/bloqueada, prioridades, recursos autorizados y siguiente acción por línea |
| Investigación Forex/CFD | [[30-resources/agents/skills/imox-strategy-research/SKILL.md\|imox-strategy-research]] | [[Estrategias IMOX — Forex y CFD con Echo Forge]]; único planner Forex | Manager CLOUD; operación Forge LOCAL | Cobertura, hipótesis/preset/campaña/candidata diferenciados, evidencia y próxima investigación |
| Investigación Futures | [[30-resources/agents/skills/echo-futures-research-manager/SKILL.md\|echo-futures-research-manager]] | [[Echo I+D — Futures]]; NQ es alcance inmediato | Manager CLOUD; ejecución Hefesto | Celda/tesis falsable, fuente, especificación operativa, presupuesto y handoff al gate aplicable |
| Entrega técnica acotada y submanagers | [[30-resources/agents/skills/technical-project-manager/SKILL.md\|technical-project-manager]] | Proyecto de entrega correspondiente; no sustituye al programa evergreen | CLOUD para coordinación; LOCAL cuando exige ejecución | Mandato completo, baseline, límites, verificación independiente y entrega a revisión Owner |
| Estado de trabajo delegado | [[80-agents/skills/agents-os-agent-project-workflow/SKILL.md\|agents-os-agent-project-workflow]] | Cada proyecto `owner: agent` es su planner único; una tarea puente en su padre | Cualquier superficie con escritura autorizada | Tareas, bitácora y siguiente paso actualizados; puente como máximo en Review por el agente |

Las dos skills nuevas de manager y el runbook común son `NUEVO_CONTRATO`. IMOX y la gestión técnica son `CONTRATO_INSPECCIONADO`; se reutilizan con sus fronteras. El catálogo global de selección sigue siendo [[80-agents/skills/INDEX.md\|Skills Index]].

### Ciclo de investigación y especialistas

| Etapa/pregunta | Skill, runbook o contrato dueño | Estado durable | Superficie necesaria | Evidencia mínima que vuelve al manager |
|---|---|---|---|---|
| ¿Qué celda merece el siguiente experimento? | Manager del mercado + [[echo-rnd-cycle-runbook]] | Matriz/backlog del mercado | CLOUD | Mecanismo, incertidumbre, prioridad, coste, falsificador y condición de parada |
| Papers, libros, documentación y observación propia | Investigador acotado bajo el manager; contrato común de fuente→hipótesis | Ficha de investigación y fuentes canónicas enlazadas | CLOUD; LOCAL sólo si acceso/formato lo requiere | Fuente exacta, alcance leído, afirmaciones vs inferencias, contraevidencia; nada implica edge probado |
| Comunidad/foro como fuente | [[30-resources/agents/skills/community-knowledge-ingest/SKILL.md\|community-knowledge-ingest]] | Registro de conocimiento/source de la comunidad; la investigación sólo enlaza | Superficie autorizada para esa comunidad | Identidades, lectura real, utilidad/descarte, huecos y frontera de cobertura |
| Audio/video que exige Whisper/MKE | [[30-resources/agents/skills/course-knowledge-extraction/SKILL.md\|course-knowledge-extraction]] | Biblioteca canónica del curso y claims | Daedalus cuando hacen falta sus fuentes/herramientas | Segmentos citables, observación visual, incertidumbre y cambios/supersesiones trazables |
| Extracción/revisión/verificación de documental | [[30-resources/agents/skills/course-knowledge-worker/SKILL.md\|course-knowledge-worker]] | Workers devuelven evidencia; integrador posee la biblioteca | Workers acotados según fuente | Roles EXTRACTOR/MINUTE_REVIEWER/DOCUMENTATION_VERIFIER; fidelidad a la fuente, no rentabilidad |
| Fuente→regla determinista→código efectivo | Manager del mercado + [[30-resources/agents/skills/sdd-workflow/SKILL.md\|sdd-workflow]]; Futures añade [[30-resources/agents/skills/echo-retester-master/SKILL.md\|echo-retester-master]] | Especificación de estrategia/variante y entregable del repo owner | CLOUD para especificar; LOCAL para probar código | Claim/regla obligatoria u opcional, interpretación separada, configuración efectiva, fixture positivo/negativo, causalidad y trazas de señal/orden |
| Diseñar building blocks y presets Forex | [[30-resources/agents/skills/sqx144-campaign-design/SKILL.md\|sqx144-campaign-design]] | Contrato y registro de campañas IMOX | CLOUD con catálogo real; prueba de compatibilidad LOCAL | Versión SQX, preset sellado, hipótesis, compatibilidad, evaluación y presupuesto; no combinar bloques sin tesis |
| Implementar y verificar una entrega lista | [[30-resources/agents/skills/sdd-developer/SKILL.md\|sdd-developer]] y reglas del repo | SPEC/PLAN/TASKS y proyecto técnico | LOCAL; Futures en Hefesto | Código conforme, pruebas significativas, verificación independiente, correcciones y commit/evidencia exactos |
| Desarrollar y cualificar Futures antes de histórico | [[30-resources/agents/skills/echo-retester-master/SKILL.md\|echo-retester-master]] + [[echo-futures-strategy-qualification-runbook]] | Identidad Strategy × variante × MM y sus recibos | Hefesto / Echo Backtester | Corrección y conformidad con teoría, readiness, sesión, roundtrip reconciliado, admisión trimestral e histórico sólo cuando corresponde |
| Campañas y laboratorio económico Futures | [[Echo Futures — Optimización de Campañas]] y manual/catálogo del lab en `xKoRx/echo` | Una campaña/experimento y su provenance; producto sigue dueño del motor | Hefesto | Input sellado, builds/datos/policy, ledger completo, intentos, coste/tiempo/pases/supervivencia/retiros según fase |
| Ejecución y funnel Forex | Proyecto técnico Forge y skills app-owned en `xKoRx/symphony:.agents/skills/` | FlowRun/evaluaciones/artifacts del owner técnico; registro IMOX enlaza | Forge operacional, mediante LOCAL autorizado | Configuración, versiones, IDs, datos y resultados por etapa; finalista pre-Echo no implica admisión ni trading |
| Verificación física integrada | [[30-resources/agents/skills/e2e-gated-validation/SKILL.md\|e2e-gated-validation]] + runbook vigente del sistema | Proyecto/mandato de certificación | LOCAL | Ledger PASS/FAIL/INCONCLUSIVE/NOT_EXECUTED, IDs nuevos por corrida y versiones sin mezclar |
| Fuente→binario→proceso real | [[30-resources/agents/skills/release-certification/SKILL.md\|release-certification]] + [[30-resources/agents/skills/deployment-proof/SKILL.md\|deployment-proof]] | Manifest y evidencia del owner técnico | LOCAL | Commit/pins/hashes, entrega al host y prueba de proceso; exit 0 no basta |
| Fallo técnico, canales o integridad | [[30-resources/agents/skills/evidence-channel-discovery/SKILL.md\|evidence-channel-discovery]], [[30-resources/agents/skills/readonly-production-probe/SKILL.md\|readonly-production-probe]], [[30-resources/agents/skills/distributed-incident-triage/SKILL.md\|distributed-incident-triage]], [[30-resources/agents/skills/write-once-conflict-triage/SKILL.md\|write-once-conflict-triage]] | Incidente/evidencia técnica; campaña conserva resultado no-evaluable cuando corresponda | LOCAL si requiere sistemas reales | Canal real, primer punto de divergencia y causa demostrada; no confundir defecto con ausencia de ventaja |
| Decidir, aprender y seleccionar lo siguiente | Manager de mercado + manager global cuando cruza prioridades; [[echo-rnd-cycle-runbook]] | Ficha/celda y decisiones del proyecto | CLOUD con evidencia retornada | Continuar/corregir/archivar/descartar, incertidumbre restante, resultado negativo preservado, condición de reapertura y próxima acción |
| Continuidad y mejora de metodología | [[80-agents/skills/agents-os-session-close/SKILL.md\|agents-os-session-close]], [[80-agents/skills/agents-os-session-feedback/SKILL.md\|agents-os-session-feedback]], [[80-agents/skills/agents-os-skill-authoring/SKILL.md\|agents-os-skill-authoring]] | Proyecto para estado; skill/runbook para procedimiento; feedback/change log para evidencia del cambio | Superficie con escritura verificada o handoff explícito | Delta durable, revisión usada, caso de mejora, validación y próximo punto exacto |

Especialistas existentes: `CONTRATO_INSPECCIONADO`, sin certificación física nueva. Fuente→spec→código es trazabilidad transversal que debe demostrarse en cada candidata; la presencia de MKE, SDD o fixtures previos no certifica por sí sola una estrategia nueva. Una estrategia de paper u observación propia puede ir directamente de CLOUD a Hefesto sin Daedalus.

### Economía, cobertura y frontera con producción

| Concern | Autoridad/registro | Qué aporta a la matriz |
|---|---|---|
| Celda Futures | [[Echo I+D — Cobertura Futures]] | Mecanismo/tesis × instrumento × horizonte/sesión relevantes, con fase challenge/funded, datos, estado de evidencia y siguiente falsificador; no producto cartesiano |
| Celda Forex | [[IMOX — Cobertura de investigación]] y [[IMOX — Registro de campañas]] | Producto/instrumento, lógica, dirección, TF y condiciones relevantes; preset/building blocks no equivalen a estrategias independientes |
| Reglas y universo de providers Futures | [[Echo Futures — Futures Prop Universe]] y perfiles versionados | Factibilidad económica/sesión por programa y fecha; fuente oficial vs decisión Owner vs supuesto vs desconocido |
| Economía de cuenta | Lab Futures y antecedentes [[Echo Futures — Prop Economics Experiment]] | Pases, capital/fees/tiempo, supervivencia y retirabilidad; aprobación aislada no demuestra economía completa |
| Runtime/ingesta/admisión | [[Echo Futures]], [[Echo]] y proyectos de integración correspondientes | Dependencias de producto; no se cubren asignando una celda de alpha ni se declaran cerradas por un backtest |
| Operación PROD | [[30-resources/agents/skills/echo-production-operational-audit/SKILL.md\|echo-production-operational-audit]] para auditoría RO; despliegue conserva su autorización propia | Fuera del arranque de I+D. Ni un manager ni un estado QUALIFIED autorizan cuentas, compras, egress, órdenes o despliegue |

La matriz contiene hipótesis y evidencia, no promesas de “cobertura completa” de todos los comportamientos del mercado. Una celda puede cerrarse con refutación útil; una campaña rentable puede seguir inconclusa. El programa mantiene dos líneas, sin imponer dos motores ejecutándose permanentemente ni crear experimentos vacíos para cada combinación.

## Auditoría de runbooks aplicables

| Autoridad | Resultado de revisión documental | Uso correcto / condición pendiente |
|---|---|---|
| [[echo-rnd-cycle-runbook]] | `NUEVO_CONTRATO` | Gestión mecánica de una iteración, registro, evidencia, decisiones y handoff. No runner, scheduler ni duplicado de G0–G5. Su validación documental no prueba backtests ni hosts. |
| [[echo-futures-strategy-qualification-runbook]] | `CONTRATO_INSPECCIONADO` | Autoridad mecánica Futures. La reorganización reconcilia excepciones textuales heredadas sobre baja actividad con G2C y el gate vigente; comprobar la versión del runbook y del guard en cada ejecución. No bajar requisitos para fabricar aprobación. |
| [[30-resources/runbooks/symphony/echo-forge-golden-e2e.md\|echo-forge-golden-e2e]] | `NEEDS_REVALIDATION`; aplicabilidad aclarada | Flujo/documentación histórica de agosto con aviso del 27-10 enlazado a la autoridad Owner. La prohibición antigua de corregir/reintentar en la misma sesión no sustituye el mandato integrado vigente de ese proyecto. Preservar fallo y usar build/IDs/corrida nuevos; no patch-and-continue ni trasladar la excepción a otros proyectos. |
| [[30-resources/runbooks/symphony/symphony-release-certification.md\|symphony-release-certification]] | `NEEDS_REVALIDATION` | Reutilizar prueba source→artefacto; resolver baseline, scripts, flags y permisos de release vigentes. El comando histórico podía despachar intake: no ejecutarlo suponiendo que sólo compila. |
| [[30-resources/runbooks/symphony/symphony-worker-runtime-proof.md\|symphony-worker-runtime-proof]] | `NEEDS_REVALIDATION` | Jerarquía de evidencia reusable; tabla de canales y flota tiene observaciones de agosto. Revalidar hosts, procesos, hashes, participación y accesos; rotación/PID por sí solo no certifica contenido. |
| [[30-resources/runbooks/symphony/symphony-prod-probe.md\|symphony-prod-probe]] | `NEEDS_REVALIDATION` | Patrón RO y cleanup reusable. Firmas SDK, DI, schemas y rutas son snapshots históricos; contrastarlos con source y acceso actual antes de crear un probe. |
| [[30-resources/runbooks/symphony/echo-forge-cross-system-triage.md\|echo-forge-cross-system-triage]] | `NEEDS_REVALIDATION` | Timeline y causa por subsistema reutilizables. La afirmación histórica “workers sin logs accesibles” no puede imponerse al inventario actual; runtime-proof ya documentó acceso SSH posterior. |
| [[30-resources/runbooks/symphony/plugin-java-deployment-via-setup-echoforge-projects.md\|plugin Java / setup projects]] | `NEEDS_REVALIDATION` | El cuerpo describe Build 142. No declararlo procedimiento certificado para SQX 144 por similitud de nombres; usar la autoridad app-owned y pruebas efectivas de SDK/JAR/clases/carga. |
| [[30-resources/runbooks/symphony/echo-forge-workers-shared-access.md\|workers shared access]] | `CONTRATO_INSPECCIONADO` + alcance limitado | Wrapper documentado para macOS. No asumirlo instalado en CLOUD/Daedalus ni copiar credenciales; resolver acceso mediante router/owner técnico. Su existencia no prueba conectividad actual. |
| [[30-resources/runbooks/symphony/remote-worker-file-manipulation.md\|remote worker file manipulation]] | `NEEDS_REVALIDATION` | Reutilizar copia/inspección/verificación/recuperación; resolver ruta y ownership vigentes y autorización de mutación. No es procedimiento de campaña ni permite editar recursos ajenos. |
| [[30-resources/runbooks/symphony-zeus-troubleshooting.md\|Symphony / Zeus troubleshooting]] | `NEEDS_REVALIDATION` | Documento histórico amplio con topología, reinicios, kill, despliegue e inyección mock. No usar como arranque universal ni como permiso para alterar flota; el gate actual se toma del proyecto y repo owners. |

La revisión comprende estos runbooks del vault. El contenido ejecutable y las skills app-owned de `xKoRx/symphony/.agents/skills/` y del repo Echo **no se recertificaron en esta reorganización**; el manager técnico confirma su inventario y revisión antes del mandato que los use. Las reparaciones operativas se asignan al owner técnico, sin lanzar campañas de prueba durante el ordenamiento documental.

Las redirecciones preservadas usan exactamente los ocho basenames de la tabla bajo `80-agents/memory/public/runbook/symphony/`. Cada una enlaza su destino completo y registra el blob común verificado; `indexable: false`, `index_priority: never`, `load_policy: manual`. Su historia previa permanece en Git. Los alias/títulos históricos pueden encontrar una redirección de compatibilidad; para eliminar ambigüedad, los nuevos enlaces usan la ruta federada completa y no un basename compartido.

## Identidades, dependencias y recuperación

- **Programa y líneas:** [[Echo — I+D de Estrategias]] → [[Estrategias IMOX — Forex y CFD con Echo Forge]] / [[Echo I+D — Futures]]. Cada uno conserva el estado de su responsabilidad; no copiar tareas entre planners.
- **Producto Futures:** [[Echo Futures]] conserva runtime, arquitectura y entrega del Backtester. [[Echo Futures — Optimización de Campañas]] conserva la entrega acotada y el lab. El programa decide prioridades de investigación y enlaza las dependencias.
- **Producto Forex/Forge:** usar [[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md|Echo Forge — Operación Real V2 (autoridad técnica)]]. Hay otro archivo homónimo bajo `10-projects/Echo Forge/`; evitar el wikilink corto ambiguo. Esta reorganización no fusiona esas autoridades técnicas.
- **Specialists federados:** `release-certification`, `deployment-proof`, `e2e-gated-validation`, `readonly-production-probe` y `distributed-incident-triage` también aparecen en rutas core históricas. Este mapa y el Skills Index seleccionan `30-resources/agents/skills/`; no crear nuevas copias ni usar la coincidencia de basename como autoridad.
- **Ambientes y acceso:** [[30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md|Echo + Echo Forge — Environment Contract]] y [[30-resources/agents/skills/aranea-agent-dev/SKILL.md|aranea-agent-dev]] siguen gobernando superficies. El manager I+D no reemplaza al router ni agrega otro match de área en el registro.
- **Fuentes:** MKE/comunidades/recursos conservan provenance y owner de biblioteca. Una investigación enlaza los claims usados; no duplica cursos ni fusiona la biblioteca completa bajo una celda.

## Mejora y mantenimiento del mapa

Actualizar este índice cuando cambie el propietario de una etapa, se agregue una capacidad realmente nueva o una validación sustituya un estado histórico. La revisión del ciclo y la auto-mejora controlada se ejecutan mediante [[echo-rnd-cycle-runbook]] y la autoría canónica de skills; no hay edición automática por invocación ni permiso para cambiar gates, objetivos, riesgo o presupuestos.

El manager que retoma una línea lee su proyecto y carga sólo la skill/operación necesaria. Antes de ejecutar un runbook marcado `NEEDS_REVALIDATION`, resuelve el delta relevante con el owner técnico y deja evidencia en el trabajo correspondiente. No necesita reauditar todo este catálogo para cada experimento.

## 🔗 Links

- [[Echo — I+D de Estrategias]] — misión, decisiones y siguiente conversación global.
- [[Echo I+D — Futures]] / [[Estrategias IMOX — Forex y CFD con Echo Forge]] — entrada de los dos chats de mercado.
- [[80-agents/skills/INDEX.md|Skills Index]] — catálogo global; este mapa sólo enruta el dominio I+D.
- [[80-agents/skills/_shared/skill-contract.md|Skill Contract]] y [[80-agents/memory/public/runbook/agents-os-skill-authoring.md|Runbook de autoría de skills]] — validación y mejora canónicas.
