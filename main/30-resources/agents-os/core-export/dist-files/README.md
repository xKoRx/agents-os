# AGENTS OS

AGENTS OS es un sistema de memoria y contexto para trabajar con agentes de código. Es una carpeta de archivos Markdown con reglas, procedimientos y contratos que un agente lee al empezar a trabajar, de modo que sepa quién sos, en qué proyectos andás, qué decisiones ya se tomaron y qué errores ya conocés — sin que se lo cuentes de nuevo en cada sesión.

No es un producto, ni un servicio, ni un plugin. No corre un proceso de fondo ni intercepta tus llamadas al modelo. Es documentación gobernada más un puñado de validadores en Python. Funciona con cualquier agente que pueda leer y escribir archivos locales: no está atado a un cliente ni a un modelo.

**Este paquete es el core compartible.** Trae el sistema, no el contenido de nadie: reglas, contratos, procedimientos, plantillas y un perfil de usuario con reglas semilla que vos confirmás o descartás. Al instalarlo, un agente te entrevista y construye tu contexto local.

---

## El problema

Los agentes de código no tienen memoria entre sesiones. Cada vez que abrís una conversación nueva, el agente arranca en cero.

Con tareas chicas eso no importa. Con trabajo real, sí. Un caso típico:

> Hace dos semanas dejaste a medias una migración que toca tres servicios. Uno expone la API, otro la consume, el tercero corre un job nocturno que también depende del contrato viejo. Ya descartaste dos enfoques por razones concretas, encontraste un bug de configuración que no es obvio, y acordaste con alguien que la parte del job se hace después.
>
> Hoy abrís una sesión nueva. El agente no sabe nada de eso. Tenés dos opciones: reexplicar veinte minutos de contexto, o dejar que el agente lea los tres repos completos y de todas formas repita uno de los enfoques que ya descartaste.

La respuesta obvia —"que lea toda mi documentación"— falla por el otro lado. Volcar todas tus notas al contexto es caro, lento y contraproducente: el modelo se distrae con lo irrelevante y las respuestas empeoran.

AGENTS OS apuesta a algo intermedio: si el conocimiento está escrito con estructura suficiente para ser **seleccionable**, el agente puede traer sólo las tres o cuatro notas que esta tarea necesita. En el caso de arriba: la nota del proyecto con su estado y sus decisiones descartadas, el error conocido de configuración, y el acuerdo sobre el job. No los tres repos.

Que eso funcione bien y de forma medible es otra discusión, y este documento la trata sin adornos más abajo.

---

## La idea central

Seis decisiones sostienen todo el sistema. Vale la pena entenderlas antes de mirar componentes.

**Markdown es la única fuente de verdad.** No hay base de datos. Todo el conocimiento vive en archivos que podés abrir, leer y editar a mano. Cualquier índice o grafo que se construya encima es derivado: si se corrompe, se borra y se reconstruye, y no se pierde nada.

**Una fuente canónica por hecho.** Cada afirmación vive en un solo lugar y el resto enlaza. Esto suena obvio y es la regla más difícil de sostener: cuando el mismo hecho está escrito en dos notas, tarde o temprano divergen y el agente carga la versión vieja creyéndola vigente.

**Procedimientos, conocimiento y estado se separan.** Son tres familias que se cargan en momentos distintos, y el sistema las distingue así:

| Tipo | Responde | Ejemplo |
|---|---|---|
| **Skill** | el *cómo* repetible | "cómo se cierra una sesión" |
| **Learning** | el *por qué importa* | "una búsqueda acotada no prueba ausencia" |
| **Decisión (ADR)** | el *por qué es así* | "por qué el índice es derivado y no autoridad" |
| **Error conocido** | una *falla repetible* | síntoma, causa, impacto, mitigación |
| **Runbook** | una *secuencia mecánica* validada | pasos exactos, verificación y rollback |
| **Entidad** | el *estado actual* de algo real | un proyecto, un servicio, un área |

Mezclarlos es el error más común. Una skill llena de hechos narrativos, o un learning con un procedimiento de cinco pasos adentro, hacen que el agente cargue lo equivocado en el momento equivocado.

**El contexto se recupera de barato a caro, y se para cuando alcanza.** Primero metadata exacta (tipo, proyecto, etiquetas). Después el índice curado del dominio, si aporta. Después las relaciones entre notas. Y sólo al final el cuerpo de las notas seleccionadas. Este orden es el que hace la diferencia entre traer tres notas y traer trescientas.

**El presupuesto de contexto es un techo blando, no un corte.** Hay un objetivo de tamaño para el arranque, pero si la respuesta correcta necesita más, se trae más. Recortar contexto relevante para cumplir un número es el error de diseño que esta regla existe para evitar.

**Nada de lo importante se guarda sin dejar rastro.** Los cambios a reglas, contratos o memoria compartida dejan un registro con su motivo, su evidencia y cómo revertirlos.

---

## Cómo transcurre una sesión

Siete pasos. Marco cuáles son automáticos, cuáles dependen de tu cliente y cuáles siguen necesitando que una persona los pida.

**1. Instalación** *(una vez, guiada por el agente)*. Le mostrás la carpeta a un agente y le pegás un prompt. El agente te entrevista, descubre tus repos, arma tu catálogo local y valida que todo cargue. Detalle en la sección de instalación.

**2. Arranque (bootstrap)** *(automático si tu cliente respeta las reglas del proyecto)*. Al empezar una sesión nueva, el agente lee tres cosas y nada más: los invariantes del sistema, tu perfil, y una nota compacta de continuidad. Eso pesa unos 4.500 tokens en este paquete recién instalado. En los mensajes siguientes de la misma conversación no vuelve a leer nada de eso: reutiliza y trae sólo lo que falta.

**3. Recuperación de contexto** *(automático, pero depende de la calidad de tus notas)*. El agente identifica sobre qué entidad estás trabajando y trae el contexto mínimo suficiente, en el orden barato-a-caro descrito arriba. Si tu pregunta no depende de ninguna de tus notas, no trae nada.

**4. Ejecución mediante skills** *(automático cuando el agente encuentra la skill)*. Para tareas con procedimiento definido —planificar una implementación, revisar coherencia, crear una entidad, certificar un deploy— el agente carga una sola skill y la sigue. Acá hay una limitación real y conocida: en la mayoría de los clientes las skills no aparecen en el menú de comandos y el agente tiene que abrirlas por ruta.

**5. Persistencia por delta** *(automático, conservador por diseño)*. Durante el trabajo, el agente actualiza el estado de lo que cambió. Si no hubo nada durable que registrar, no escribe nada. Una sesión sin novedad no ensucia la memoria.

**6. Cierre** *(sólo si lo pedís)*. El cierre completo —resumen, feedback, promoción de aprendizajes reusables— no ocurre por inercia. Tenés que pedirlo. Esto es deliberado: evita que cada tarea trivial genere cinco artefactos.

**7. Higiene y mejora continua** *(hoy requiere que una persona lo pida)*. Un ciclo periódico revisa el corpus, procesa el feedback acumulado, promueve lo que se repite y reindexa. Es el paso más débil del sistema y está tratado en detalle más abajo.

---

## Componentes

Agrupados por responsabilidad. Las rutas son relativas a la raíz del **vault**: así se llama, en la jerga del sistema y de Obsidian, la carpeta de notas que estás mirando.

| Componente | Función | Dónde vive | Estado |
|---|---|---|---|
| **Constitución** | Los invariantes del sistema. Reglas que ninguna skill puede contradecir. | `80-agents/agents-os/agent-constitution.md` | Estable |
| **Guía operativa** | El mapa conceptual. Qué hay y dónde, sin procedimientos. | `80-agents/agents-os/agents-os.md` | Estable |
| **Contratos ejecutables** | Qué campos exige cada tipo de nota, qué secciones, qué valores. Los valida un script. | `80-agents/skills/_shared/` | Estable, con validador |
| **Skills** | 37 procedimientos: arranque, recuperación, cierre, higiene, ciclo de vida de entidades, planificación, autoría de skills y varios de validación técnica. | `80-agents/skills/` | Funcionan; el descubrimiento por parte del cliente es el problema |
| **Perfil de usuario** | Quién sos y cómo querés que trabaje el agente. Es la única nota que se carga siempre además de la constitución. | `80-agents/memory/public/user-preference/` | Trae reglas semilla; la instalación las confirma y agrega tu identidad |
| **Memoria compartida** | Decisiones, aprendizajes, errores conocidos y runbooks. Este paquete trae los del sistema mismo, incluido lo aprendido a costa de fallar. | `80-agents/memory/public/` | Activa |
| **Continuidad privada** | Un espacio del agente para su propio hilo entre sesiones. Un único punto activo por tema, no una nota por sesión. | `80-agents/memory/internal/` | Trae una semilla con comportamientos transferibles |
| **Plantillas** | Todo documento canónico nace de una plantilla, nunca a mano. | `70-templates/` y `80-agents/templates/` | Estables |
| **Journal** | Registro de cambios, feedback de sesión y reportes de higiene. Auditoría, no autoridad. | `80-agents/journal/` | Viene vacío |
| **Validadores (gates)** | Scripts que revisan salud del sistema, cumplimiento del contrato y deuda del corpus. | `80-agents/skills/agents-os-doctor/scripts/`, `_shared/scripts/`, `agents-os-entity-lifecycle/scripts/` | Funcionan y son el mecanismo de detección más confiable |
| **Índice derivado** | Un grafo local opcional para resolver entidades y relaciones. Nunca es autoridad. | Fuera del vault, en una caché por máquina | Opcional y frágil |

Dos términos que vas a encontrar dentro de las fuentes: un **gate** es un script que revisa algo y falla si no cumple, y una **superficie** es el cliente o IDE desde el que trabaja un agente. Cuando algo "depende de la superficie", funciona distinto según el cliente que uses.

---

## Promesa y estado real

Esta sección existe porque el proyecto trata la transparencia como una característica, no como una concesión.

Antes de la tabla, tres tipos de evidencia que **no** valen lo mismo:

- **Observado.** Conteos verificables sobre el registro del entorno donde el sistema se usó a diario durante dos meses y medio. Ejemplo: cuántas notas de feedback existen y cuántas fueron citadas después.
- **Autoevaluación del agente.** Puntajes de 1 a 5 que los propios agentes se asignaron al cerrar sesión, sobre unas 240 sesiones. Es señal útil y sesgada: el agente evalúa su propia experiencia, no la satisfacción de la persona.
- **No medido.** Cosas que el diseño afirma y la instrumentación todavía no produce.

| Promesa | Estado | Evidencia |
|---|---|---|
| Continuidad entre sesiones sin reexplicar contexto | **Cumplida** | *Autoevaluación:* claridad de arranque 4,62/5, la más alta del sistema. *Observado:* la memoria privada se consultó en 201 sesiones. El contrafáctico es lo más convincente: la única sesión que re-derivó un análisis completo desde cero fue una en la que el arranque no se ejecutó, y la información que necesitaba estaba a un enlace de distancia |
| Recuperación por capas que gasta el mínimo suficiente | **Parcial** | *Autoevaluación:* utilidad 4,36/5, y el orden de acceso observado es el que el diseño predice. *No medido:* no existe una sola medición de consumo de tokens en el registro. El campo está instrumentado desde septiembre de 2026 y vale `unknown` en todas las notas que lo traen. La economía de contexto es una hipótesis razonable, no un resultado demostrado |
| Procedimientos reusables como skills | **Parcial** | *Autoevaluación:* encaje 4,52/5, estable en tres meses: el contenido sirve. *Observado:* 36 de 40 skills no aparecen en el menú de comandos de ningún cliente y hay que abrirlas por ruta. El problema es el envase |
| Una fuente canónica por hecho | **Parcial** | *Observado:* sólo 7 casos de duplicación real de un hecho de dominio en 340 sesiones, y los agentes citan la regla como razón para *no* escribir. Pero en el sistema mismo falló: una skill llegó a existir en dos lugares con contenido distinto y la copia canónica era la vieja, sin ninguna señal de conflicto |
| Higiene y mejora continua automáticas | **No cumplida** | *Observado:* cero reportes de mejora en 67 días, mientras se acumulaban 340 notas de feedback — siete veces el umbral que el propio sistema fijó. El 61% de esas notas nunca fue citado por ningún artefacto. El bucle escribe con disciplina y no lee. Corre cuando una persona lo pide |
| Portabilidad entre clientes | **Parcial** | *Observado:* ocho clientes distintos produjeron registros bajo el mismo contrato, lo que es portabilidad real y no declarativa. Pero cada uno rompe algo diferente y el sistema no tiene forma de saber qué le falta al cliente en el que está corriendo |
| Delegación a subagentes | **Pendiente de prueba** | *Observado:* tres modos de falla distintos y documentados: reporte final vacío, muerte por inactividad, y ejecución sin señal de progreso ni resultado atribuible. Este paquete incluye el procedimiento y el error conocido que salieron de eso, pero todavía sin uso suficiente para saber si alcanzan |

Un dato más, y no favorable: **el cierre de sesión es el punto más débil del sistema**. Autoevaluación 3,38/5, el único indicador cuya moda es 3 y el único que no mejoró tras rediseñarse. La causa identificada es que el sistema decide *si* cerrar pero no *cuánto* documentar, así que en sesiones simples el formulario queda medio vacío.

---

## Qué puede hacer hoy

Sin exagerar, y sin contar lo que está sólo diseñado:

- Mantener continuidad entre sesiones y entre clientes distintos.
- Recuperar conocimiento por capas, priorizando metadata exacta sobre lectura de archivos.
- Organizar procedimientos como skills que el agente carga de a una.
- Validar por script que las notas cumplan el contrato: campos, secciones, valores, ciclo de vida.
- Detectar por gate una familia concreta de problemas: rutas rotas, notas que se cargarían siempre sin autorización, skills sin registrar, contradicciones de metadata, secretos en texto plano.
- Separar el core compartible del contenido local, con un build reproducible que verifica cada archivo por hash.
- Conservar trazabilidad: por qué se decidió algo, qué se descartó y qué falló antes.

---

## Ventajas y costos

Las dos columnas son reales. Si sólo te convence una, probablemente el sistema no es para tu caso.

| Ganás | Pagás |
|---|---|
| Continuidad: el agente retoma sin que reexpliques | Disciplina documental: si nadie escribe, no hay nada que recuperar |
| Trazabilidad: las decisiones y los errores quedan con su razón | Mantenimiento: el corpus se degrada si no se limpia periódicamente |
| Portabilidad: cambiás de agente o de IDE y el conocimiento se queda | Fricción de los gates: bloquean cuando el corpus está sucio, y a veces llegás con apuro |
| Inspección humana: es Markdown, lo abrís y lo entendés | Riesgo de metadata obsoleta: una nota mal etiquetada se vuelve invisible |
| Índices reconstruibles: nada crítico depende de una caché | Dependencia de runtime local para los validadores |
| Procedimientos reutilizables entre proyectos | Sobrecosto en tareas chicas: arranque y cierre no se pagan solos |

---

## Límites y problemas abiertos

Problemas que existen hoy, con su impacto conocido:

**El arranque es un punto único de falla.** Cuando se ejecuta, la memoria funciona. En cuatro sesiones registradas no se disparó y el sistema no lo detectó solo: el agente trabajó en frío sin darse cuenta. Toda la promesa de continuidad depende de ese único paso.

**El costo real en contexto no está medido.** Hay un campo para registrar consumo y está vacío en todos los casos. Cualquier afirmación sobre ahorro de contexto en este documento es cualitativa.

**Las skills casi no se descubren solas.** 36 de 40 no tienen entrada en el menú de ningún cliente. El agente las encuentra si el prompt del proyecto le dice dónde buscar, no por sí mismo.

**El sistema no sabe qué puede hacer el cliente en el que corre.** Si un validador no puede ejecutarse porque el entorno no lo permite, no hay una forma declarativa de registrarlo. El riesgo concreto es que un agente afirme que un gate pasó cuando en realidad no corrió.

**La mejora continua no es autónoma.** Sin que alguien la pida, el feedback se acumula. Ya pasó: 340 notas en 67 días sin procesar.

**El índice derivado es frágil.** Su utilidad autoevaluada bajó de ~3,8 a 3,19 sobre 5. Sirve para resolver una entidad por título exacto; para búsqueda temática amplia, buscar directamente en el Markdown gana. En varios entornos quedó desactualizado porque el sandbox del cliente no pudo escribir su caché.

**El paquete todavía arrastra nombres del entorno del que se extrajo.** 48 de 170 archivos Markdown contienen nombres de proyectos, servicios o herramientas del vault de origen, casi siempre como ejemplos dentro de plantillas o como citas de evidencia en notas de aprendizaje. No hay identidad de personas, credenciales ni rutas absolutas de máquina — eso está verificado y da cero. Pero la limpieza de ejemplos está pendiente, y conviene saberlo antes de compartir el paquete hacia afuera.

Propuestas registradas que **todavía no están implementadas**, para que no se confundan con lo anterior: una decisión sobre cómo resolver el descubrimiento de skills, un diagnóstico de capacidades del cliente al arrancar, y un modo reducido del formulario de cierre.

---

## Cuándo conviene y cuándo no

**Probablemente conviene si** tu trabajo dura semanas o meses; cruza varios repositorios o servicios; acumula decisiones y errores que no querés volver a descubrir; se retoma después de días sin tocarlo; usás más de un agente o más de un IDE; o necesitás poder explicar por qué algo se hizo así.

**Probablemente no conviene si** trabajás en sesiones cortas y descartables; el repositorio es chico y lo conocés de memoria; la tarea no tiene continuidad; tu entorno no puede ejecutar scripts locales y necesitás los validadores; o nadie en el equipo va a mantener las fuentes canónicas. Este último es el que más veces mata la idea: el sistema no genera el conocimiento que nadie escribió.

---

## Instalación

Requisitos: Python 3, un agente con acceso de lectura y escritura a archivos locales, y una terminal. El índice derivado es opcional.

**La ruta corta es mostrarle la carpeta a un agente y pedirle que instale.** No tenés que entender el sistema antes de empezar; el instalador te lo explica mientras avanza.

1. Poné esta carpeta donde vayas a tener tu vault.
2. Abrí esa carpeta con tu agente — `codex` o `claude` en la terminal, la app de escritorio, o la extensión de tu IDE.
3. Abrí [`INSTALL-PROMPT.md`](INSTALL-PROMPT.md), reemplazá la ruta absoluta de la carpeta y pegá el bloque como primer mensaje.

A partir de ahí el agente hace el recorrido completo: te explica en lenguaje simple qué es cada pieza, te entrevista para armar tu perfil, te pregunta dónde viven tus proyectos, descubre los repositorios y te pide confirmar cuáles son los activos, crea la nota canónica de cada uno, configura las reglas de tu cliente, define contigo la cadencia de limpieza, instala el índice si tu entorno lo permite, corre los validadores y termina con un reporte. Sólo declara la instalación completa cuando cada criterio se validó **en tu máquina**; lo que no pudo verificar queda como pendiente explícito, no como aprobado.

El prompt sirve igual para otros clientes con acceso a archivos locales. En ese caso el agente registra lo que su entorno no puede hacer en vez de fingir que lo hizo.

### Verificación

Tres comandos, desde la raíz del vault:

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py
python3 80-agents/skills/_shared/scripts/validate_schema_contract.py
python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --gate
```

Recién descomprimido, sin instalar nada, deberías ver:

```text
AGENTS OS doctor: HIGH=0 MEDIUM=0 LOW=0 startup_tokens≈4466
AGENTS OS schema contract: version=1 types=45 ... errors=0
AGENTS OS lint gate: ERROR=0 WARN=0 ... new=0
GO: no-new-debt
```

`startup_tokens` es el peso aproximado de lo que el agente lee al arrancar. Es una estimación por caracteres, no un conteo de tokenizador; el objetivo de diseño está entre 3.000 y 6.000. Si el doctor reporta `HIGH`, algo del sistema está roto y conviene resolverlo antes de trabajar.

---

## Cómo contribuir

**Este paquete no tiene todavía un proceso formal de contribución**: no hay repositorio público, ni plantilla de issues, ni revisores designados. Lo que sigue son instrucciones mínimas, no una política.

Podés usarlo, modificarlo y compartir tus mejoras. Lo importante es cómo devolverlas para que sirvan a otra persona:

- **Reportar un problema.** Escribí una nota de error conocido: síntoma, causa, impacto y mitigación. La plantilla está en `80-agents/templates/known-error.md`. Un síntoma reproducible vale más que una descripción larga.
- **Mejorar una skill.** Editá el `SKILL.md` correspondiente. Antes, leé `80-agents/skills/_shared/skill-contract.md` y `80-agents/skills/agents-os-skill-authoring/SKILL.md`: hay reglas sobre qué va dentro de una skill y qué no, y romperlas hace que el agente cargue basura en cada invocación.
- **Proponer una decisión de diseño.** Usá el tipo `decision`: contexto, decisión, alternativas descartadas y consecuencias. Sin alternativas descartadas no es una decisión, es una preferencia.
- **Aportar un contrato o un validador.** Los contratos viven en `_shared/`, los scripts junto a la skill que los usa. Un contrato sin validador ejecutable se desincroniza; ese patrón ya se repitió y está documentado.
- **Compartir sin filtrar nada tuyo.** Todo registro de cambio declara obligatoriamente `share_scope`, y cualquier nota del sistema puede declararlo. Marcá `team` sólo lo agnóstico; lo que menciona tu empresa, tus repos o tus preferencias personales va como `local` y no viaja. Antes de compartir, revisá que tu aporte no traiga nombres de tu entorno — es el error más fácil de cometer, y este mismo paquete lo tiene pendiente.

Para verificar que tu cambio no rompió nada, corré los tres comandos de verificación. Si tocaste una fuente canónica, además:

```bash
python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --strict <tu-archivo>
```

Ese comando exige cero hallazgos en el archivo que cambiaste, independiente de la deuda que haya en el resto.

---

## Estado del proyecto

Funciona y se usa a diario, pero no está terminado y no lleva número de versión porque no hay un proceso de release que lo respalde.

Lo maduro es el núcleo: los invariantes, los contratos, las plantillas y los validadores llevan meses estables y son la parte que efectivamente atrapa errores. Lo inmaduro es todo lo que necesita que el sistema se observe a sí mismo: la medición de su propio costo, la mejora continua sin intervención humana, y el diagnóstico de en qué entorno está corriendo.

Tratalo como una base sólida para adaptar, no como una solución cerrada para adoptar.

---

## Si algo se contradice

Cuando dos fuentes dicen cosas distintas, este es el orden que manda:

1. La constitución y las decisiones vigentes.
2. Los contratos de `_shared/`.
3. Las skills, para comportamiento ejecutable.
4. La guía operativa y los documentos conceptuales.
5. Las notas canónicas de cada entidad, para el estado actual.
6. Los reportes y este README: son evidencia, nunca regla.

Ante una contradicción, identificala y proponé cómo resolverla. No fusiones las dos afirmaciones en silencio: eso es exactamente cómo se degrada un sistema de memoria.

`MANIFEST.md` lista cada archivo copiado con su ruta canónica y su hash, por si necesitás verificar procedencia.
