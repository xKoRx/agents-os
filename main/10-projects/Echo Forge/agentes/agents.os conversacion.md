La iteración óptima no es agregar más rituales: es convertir AGENTS OS en un pipeline corto, incremental y silencioso. Hoy la arquitectura conceptual es buena, pero el camino caliente contradice su propia economía de tokens.

Apliqué en modo read-only la rúbrica `define == implement` de `agents-os-hygiene-review`. No modifiqué archivos.

## Diagnóstico principal

### 1. El arranque está sobredimensionado y no tiene una única receta

Actualmente hay al menos tres versiones del startup:

- Dos flujos casi repetidos en [[agents-os]].
- Otro procedimiento en
  [[80-agents/skills/agents-os-bootstrap/SKILL.md|agents-os-bootstrap]].
- Priorización adicional en `agents-os-context-retrieval`.

Además, se obliga a cargar una “memoria interna compacta”, pero no se define cómo seleccionarla. Hoy hay memorias de dominio marcadas `always`, incluyendo una de Symphony que no corresponde cargar en una sesión de AGENTS OS.

El conjunto potencial de guía, constitución, perfil, bootstrap, retrieval y memorias `always` pesa aproximadamente 21–24 mil tokens antes de cargar contexto específico. Es unas 7–8 veces el objetivo histórico cercano a 3.000 tokens registrado en [[AGENTS OS]].

También hay una contradicción directa en el Context Router: dice “nunca saltar capas”, pero su tabla comienza relaciones y código directamente en la capa 2. Está en [[80-agents/skills/agents-os-context-retrieval/SKILL.md|agents-os-context-retrieval]].

### 2. El cierre mezcla persistencia interna con UX

El cierre exige un inventario de doce campos —raw, summary, feedback, learnings, ADRs, known errors, runbooks, logs, Graphify, etc.— en [[80-agents/skills/agents-os-session-close/SKILL.md|agents-os-session-close]]. Eso explica que el usuario reciba un reporte que no necesita.

Además:

- `session-close` está marcado `always-load`, aunque solo debe ejecutarse por petición explícita.
- El cierre normal crea feedback general.
- Como Graphify se usa casi siempre, también tiende a crear un segundo feedback específico, según [[80-agents/skills/agents-os-session-feedback/SKILL.md|agents-os-session-feedback]].
- Hay 153 notas de feedback acumuladas, con aproximadamente 75 mil palabras.
- Las dos plantillas de feedback ya suman 663 palabras antes de rellenarlas.
- Incluso el cierre táctico conserva un L0 vacío cuya utilidad depende de que después alguien pegue una transcripción.

La falla de diseño es simple: el pipeline interno puede ser completo cuando se justifique, pero su inventario no debe convertirse en la respuesta al usuario.

## Propuesta: AGENTS OS “Hot Path”

### A. Un solo bootstrap canónico

Dejar esta autoridad:

- `AGENTS.md`: hook mínimo para iniciar AGENTS OS.
- `agents-os-bootstrap/SKILL.md`: único procedimiento ejecutable.
- `agents-os.md`: mapa conceptual y routing, sin pasos duplicados.
- Constitución: únicamente invariantes duras.
- Skills: procedimientos.
- Proyecto AGENTS OS: estado y backlog, nunca reglas operativas.
- Journal/snapshots: historia, nunca autoridad vigente.

El startup estándar sería:

1. Detectar si es inicio frío, turno caliente o cambio de entidad.
2. En inicio frío, cargar una cápsula corta de invariantes y preferencias globales.
3. Interpretar objetivo, entidad e intención antes de cargar memoria de dominio.
4. Cargar solamente memoria interna `always + global`.
5. Recuperar contexto de la entidad mediante la capa más barata aplicable.
6. Verificar únicamente las fuentes que afectarán la respuesta o un cambio.
7. Cargar una sola skill especializada cuando corresponda.
8. Continuar sin mostrar una “nota de orientación”, salvo retrieval degradado.

La corrección conceptual del Router debería ser:

> Empezar en la capa más barata relevante para la intención. Nunca abrir cuerpos sin una selección previa. Escalar solo cuando el contexto sea insuficiente.

Eso resuelve la contradicción sin convertir las cuatro capas en un waterfall obligatorio.

### B. Arranque incremental

Definir tres modos:

- **Cold start:** reglas base + perfil global + índice interno + contexto de entidad.
- **Warm turn, misma entidad:** reutilizar lo ya cargado; recuperar solo el delta.
- **Cambio de entidad:** conservar reglas base y reemplazar únicamente el paquete de entidad.

La invalidación ocurre si cambia una fuente base, la entidad activa o la intención. No corresponde releer guía, constitución y bootstrap “cada vez que el usuario hable”, como ordenaba históricamente `AGENTS.md`.

Meta inicial —como benchmark blando, no límite—:

- Cold start: 3–5 mil tokens.
- Turno caliente: menos de 1.000 tokens nuevos.
- Cambio de entidad: 1–3 mil tokens.
- Reducción esperable del startup: 75–85%.

### C. Memoria interna enrutable

Mantendría la memoria interna, pero cambiaría su contrato:

- Exactamente una nota global de startup, idealmente 200–500 tokens.
- Memorias de proyecto/app con `when_project_loaded`, `when_application_loaded`, etc.
- Ninguna memoria de dominio puede usar `always`.
- El bootstrap filtra por metadata; nunca apunta al directorio completo.
- El mandamiento “toda sesión modifica memoria interna” pasa a “toda sesión con delta durable deja continuidad”. Una conversación sin nuevo estado no debería escribir por obligación.

Hay además un hallazgo de seguridad P0: una memoria interna de dominio marcada `always` contiene una credencial en texto plano. Viola [[agent-constitution]] y debe retirarse del vault y rotarse, sin reproducirla.

## Nuevo contrato de cierre

Separaría formalmente:

- **Persistencia:** qué necesita guardar AGENTS OS.
- **Reporte:** qué necesita saber Rodrigo.

Clasificador propuesto:

|Delta de la sesión|Acción|
|---|---|
|Sin conocimiento ni estado nuevo|No crear artefactos|
|Solo continuidad operacional|Actualizar proyecto/control o checkpoint interno, no ambos|
|Conocimiento reusable|L3 + log + reindex dirigido|
|Transcripción disponible o solicitada|L0; L1 solo si agrega navegación|
|Fricción real del sistema|Feedback breve|
|Auditoría explícita|Mostrar inventario completo|

Respuesta predeterminada:

> Sesión cerrada. Continuidad lista. Próximo paso: X.

Nada de listar memorias guardadas, descartadas o actualizadas. El inventario detallado queda disponible únicamente con `cierre con detalle` o si hubo un error/conflicto que requiera decisión.

También cambiaría el feedback a `event-driven`: solo ante fricción, degradación, gap o muestreo periódico. El feedback de Graphify debería agregarse durante higiene, no producir otra nota en cada cierre.

## Drift documental verificado

Los problemas más concretos son:

- `AGENTS.md` apuntaba a una ruta absoluta distinta de la máquina activa.
- El bootstrap hardcodea `rjara-agent-profile.md`, mientras el instalador permite resolver o crear otros nombres de perfil. Una instalación portable podría crear un perfil que bootstrap nunca encuentre.
- `session-close` está definido como always-load en la guía, pero simultáneamente requiere trigger explícito.
- El proyecto controlador todavía mostraba `session-close` como pendiente en [[AGENTS OS]].
- El snapshot para ChatGPT apuntaba a una ubicación antigua de constitución en `10-projects/AGENTS OS/chatgpt-pack/PROJECT-STATE.md`. Las fuentes live principales sí usan correctamente `80-agents/agents-os/agent-constitution.md`.
- `.graphifyignore` no excluye `outputs/agents-os-chatgpt/`; las consultas reales están devolviendo la fuente live y su copia exportada.
- `agents-os-skill-authoring` contiene referencias relativas rotas a `_shared/`.
- Los `SKILL.md` mezclan contrato ejecutable con `Finish Tasks` y `Progress Log`. Como deben leerse completos, cada agente paga tokens por historia de desarrollo que no cambia la ejecución.

## Iteración recomendada

La implementaría en cuatro cambios pequeños:

1. **P0 — reparación y seguridad:** corregir rutas, sacar/rotar la credencial, excluir outputs duplicados y corregir referencias rotas.
2. **P1 — hot path:** convertir bootstrap en la única máquina de estados; adelgazar guía, constitución y skills; enrutar perfil y memoria por metadata.
3. **P2 — silent close:** cierre por delta, feedback event-driven y reporte de una o dos líneas por defecto.
4. **P3 — doctor + benchmark:** validador automático de rutas, wikilinks, `always-load`, duplicación de procedimientos, tamaño del startup, outputs indexados y consistencia entre proyecto y skills.

El gate final debería probar cold start, turno caliente, cambio de entidad, Graphify degradado y los cuatro tipos de cierre. La métrica relevante no es cumplir un número rígido: es reducir tokens sin perder una fuente que cambie la decisión.
