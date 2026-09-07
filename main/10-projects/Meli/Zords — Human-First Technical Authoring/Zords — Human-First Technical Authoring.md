---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-08-26
due:
progress: 95
repo: local-agents-pipeline-cli
jira:
prs: https://github.com/melisource/fury_local-agents-pipeline-cli/pull/29
aliases:
  - Human-First en Zords
  - Authoring Zord
  - Zord de documentación técnica
tags:
  - kind/project
  - area/meli
  - tech/zords
  - action/document-authoring
created: 2026-08-26
updated: 2026-09-01
cssclasses:
  - wide
---

# Zords — Human-First Technical Authoring

> [!info]+ Estado ejecutivo
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Repo:** `local-agents-pipeline-cli` · **Progreso:** 95%
> **Approach vigente:** camino aditivo `zord author`, aislado del pipeline de code review, stdout como única salida documental del MVP y cero conocimiento especial de SDD.
> **Modelo:** Codex con `gpt-5.6-terra` y reasoning effort `high`; `xhigh` queda fuera del MVP salvo evaluación posterior.
> **Implementación:** vertical `zord author` completo para `document` y `pr-description`; PR #29 abierto, CI verde y correcciones de seguridad derivadas del dogfood del propio Zord aplicadas.
> **Reporte final:** el synthesizer bundled conserva su contrato JSON y ahora ordena el reporte según Human First: orientación, causalidad, certeza visible y siguiente paso humano.

## 🎯 Objetivo

Integrar `human-first-technical-writing` en el producto Zords como una capacidad transversal de autoría técnica para humanos, sin modificar la semántica ni el comportamiento de los Zords de code review existentes.

El feature agrega un camino hermano y explícito, `zord author`, que recibe evidencia técnica de sólo lectura, ejecuta un writer Human First y devuelve Markdown limpio por stdout. La primera recipe especializada será `pr-description`; cualquier persona o agente podrá invocarla, capturar su salida y decidir qué hacer con ella. Zords no guardará el documento, no publicará el PR y no administrará specs.

La descripción de PR es el primer caso de uso, no el concepto raíz. El mismo writer debe habilitar después la creación de otros documentos complejos mediante `zord author document`, conservando la separación entre una heurística transversal de comunicación y el contrato específico de cada artefacto.

## 🧠 Tesis y propuesta de valor

En un mundo donde un agente puede producir documentación extensa, técnicamente correcta y aparentemente completa en segundos, la escasez deja de estar en la escritura y se desplaza hacia la comprensión humana. Generar más contenido no garantiza comunicar mejor: también puede multiplicar inventarios, repeticiones y estructuras que obligan al lector a reconstruir por su cuenta la relación entre problema, mecanismo, decisión y evidencia.

Los agentes toleran entradas densas, listas largas y contexto disperso porque pueden reprocesarlo como tokens. Una persona construye comprensión progresivamente, orienta su atención mediante preguntas, mantiene un conjunto limitado de conceptos en memoria de trabajo y necesita relaciones causales para evaluar el detalle. Cuando un documento sigue la cronología del agente —investigué A, encontré B, cambié C, probé D— transfiere al lector el costo de reorganizar el conocimiento.

`human-first-technical-writing` traduce ese orden de producción al orden de comprensión humana: qué ocurre, por qué ocurre, qué cambia, cómo cambia el comportamiento, qué no cambia, cuáles son los límites y qué evidencia permite confiar en el resultado. Su ventaja no es “escribir bonito” ni producir más texto. Su ventaja es reducir la carga cognitiva accidental para que la capacidad mental del lector se use en entender el sistema y tomar una decisión.

> **North Star:** Los agentes tienden a escribir siguiendo su proceso de investigación. Los humanos necesitan leer siguiendo un proceso de comprensión. Esta capacidad hace la traducción entre ambos.

> **Promesa de producto:** Human-first no significa simple. Significa cognitivamente eficiente.

### Por qué calza en Zords

Zords ya distribuye capacidades ejecutables basadas en agentes. El equipo puede instalar una versión del producto y obtener un comportamiento compartido, versionado y disponible desde CLI. Eso vuelve a Zords un buen vehículo de distribución para Human First.

Sin embargo, el contrato actual de un Zord es específicamente review-centric: recibe un diff y devuelve findings. Human First produce un documento, no un finding. La integración correcta no consiste en fingir que ambos outputs son iguales, sino en agregar una nueva operación del producto con un runtime aislado.

En lenguaje de producto, `human-first-technical-writing` es un **Authoring Zord**. En el código, se modela como writer y recipe separados del loader, runner, orquestador y resultados de review. Esta distinción permite cumplir “metámosla en Zords para todos” sin redefinir silenciosamente el comportamiento actual.

## 📊 Estado actual

- **HEAD verificado:** `feature/zords-technical-authoring@d7a62e5`, basada en `origin/master@6035510`, publicada desde el fork `rjara_meli/fury_local-agents-pipeline-cli` hacia el PR upstream #29.
- **HEAD actual:** el camino legacy conserva `ZordResult` con findings; authoring vive en el subcomando hermano `zord author` y usa contratos internos separados.
- **PR:** [melisource/fury_local-agents-pipeline-cli#29](https://github.com/melisource/fury_local-agents-pipeline-cli/pull/29) está abierto y listo para review humana, con todos los checks remotos verdes y descripción generada mediante dogfood de `zord author pr-description`.
- **LOCAL_CHANGE útil:** el soporte para pasar `model_reasoning_effort` a Codex y sus tests demuestra que Terra high es técnicamente viable.
- **LOCAL_CHANGE útil:** `zords/synthesizer.md` incorpora explícitamente las reglas Human First sin mover el synthesizer al registry de reviewers; `tests/synthesizer.spec.ts` verifica el contrato editorial y el aislamiento de layout.
- **LOCAL_CHANGE reemplazado por decisión humana:** `task: document` en `ZordMeta`, la carga de ese campo en `zordLoader` y los contratos `Document*` globales amplían prematuramente el core y no aíslan la ejecución; el runner seguiría esperando findings.
- **Evidencia actual:** 37 suites y 544 tests verdes; 96.09% de cobertura global de líneas; build, dist, lint y diff-check pasan. Lint mantiene 12 warnings preexistentes y 0 errores.
- **Review real:** Zords encontró problemas de truncación de stdout, límites de input, refs Git mutables, exposición de paths/contexto, acceso a tools del host, carrera de apertura de archivos y fugas de secretos. Las correcciones quedaron versionadas con regresiones, incluida la inspección de múltiples asignaciones cuando un placeholder precede a un secreto real.
- **Decisión nueva del owner:** minimizar superficie, preservar stdout como salida y eliminar SDD del dominio de Zords.
- **Distribución adicional:** `human-first-technical-writing` v1.0.0 fue portada a `ads-signals-skills-marketplace`; el PR [#1](https://github.com/melisource/fury_ads-signals-skills-marketplace/pull/1) publica la skill portable para Claude y Codex con justificación cognitiva y fuentes primarias.
- **Fase actualmente habilitada:** F0–F3 implementadas y G3 en `review`; la aceptación humana y la evaluación cognitiva formal T3.1 siguen pendientes.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `local-agents-pipeline-cli` | `feature/zords-technical-authoring` | `master@6035510` | Esta nota: objetivo, producto, alcance y requisitos | Esta nota: boundary, arquitectura, contracts y fases | PR #29 ready; checks verdes; G3 review |
| `ads-signals-skills-marketplace` | `feature/human-first-technical-writing` | `master@ac72fb7` | Skill portable v1.0.0 | Catálogo v1.2.0 + validator | PR #1 abierto; Code Reviewer aprobado |

## 🧩 Definición del producto

### Tres conceptos, tres responsabilidades

| Concepto | Responsabilidad | No es responsable de |
|---|---|---|
| Human First writer | Orden, densidad, causalidad, progresión, proximidad de contexto y certeza epistemológica | Descubrir fuentes, publicar o imponer un template universal |
| Recipe | Propósito, audiencia, fuentes requeridas/opcionales y contrato del artefacto | Ejecutar modelos o administrar persistencia |
| `zord author` | Recibir inputs explícitos, ejecutar Terra en read-only y emitir Markdown por stdout | Code review, findings, synthesis, archivos output, GitHub o SDD |

La precedencia es obligatoria: `fuentes autoritativas > template/contrato del artefacto > contenido existente > heurísticas Human First`. El writer puede reorganizar información, pero no romper un formato requerido, inventar evidencia ni convertir una inferencia en hecho.

### Superficie de uso del MVP

```bash
# Documento técnico genérico desde fuentes explícitas
zord author document --source context=contexto.md --source evidence=evidencia.md --purpose "Explicar la decisión al equipo"

# Descripción de PR de la iniciativa Crear Context
zord author pr-description --initiative "Crear Context" --base master --source intent=.sdd/features/crear-context/1-functional.md --source design=.sdd/features/crear-context/2-technical.md --source plan=.sdd/features/crear-context/3-tasks.md --template .github/pull_request_template.md

# Un agente o humano decide si captura la salida
zord author pr-description --initiative "Crear Context" --base master --source intent=funcional.md --source design=tecnica.md > /tmp/pr-description.md

# Publicación compuesta fuera de Zords y sólo por decisión del caller
zord author pr-description --initiative "Crear Context" --base master --source intent=funcional.md | gh pr create --fill --body-file -
```

El uso normal es exactamente éste: una persona, Codex, otro agente o un script ejecuta el comando y recibe el documento por stdout. El caller puede mostrarlo, guardarlo, pegarlo en un PR o encadenarlo con otra herramienta. Zords termina su responsabilidad al producir Markdown y un exit code.

### Recipes del MVP

#### `document`

Produce un documento técnico desde uno o más `--source`, un propósito y una audiencia opcional. Un documento existente puede entregarse como fuente para reescritura; el MVP no necesita una operación ni un store separados para distinguir create/rewrite.

#### `pr-description`

Prepara al reviewer para el diff. `--initiative` entrega el nombre humano del cambio y no funciona como clave de búsqueda; `--base` identifica el target Git; cada `--source <label>=<path>` declara explícitamente qué fuente leer y qué rol cumple. La recipe lee de forma segura y read-only el diff y los commits del repo actual contra `--base`; puede recibir template y fuentes adicionales explícitas. Su recorrido cognitivo habitual es: qué ocurre, por qué, qué cambia, cómo cambia el comportamiento, qué no cambia, riesgos, validación aportada y foco de review.

La recipe no publica en GitHub, no ejecuta tests, no afirma resultados que el caller no aportó y no busca specs automáticamente.

### Contratos exclusivos de `zord author`

`--initiative`, `--source <label>=<path>`, `--purpose`, `--audience`, `--template` y el `--base` de authoring pertenecen exclusivamente al árbol de comandos `zord author`. No se agregan a options compartidas, `AssembleOptions`, `ZordMeta`, config global ni APIs de `assemble`, `summon`, `fix`, `list`, `add`, `enable`, `disable` o `check`.

| Comando | Contratos aceptados | Contratos que no acepta |
|---|---|---|
| `zord author document` | repeated `--source <label>=<path>`, `--purpose`, optional `--audience`, optional `--template`, stdin | `--initiative`, Git review options y persistencia |
| `zord author pr-description` | required `--initiative`, `--base` cuando no sea inequívoco, repeated `--source <label>=<path>`, optional `--template` | `--purpose`, output file, publicación y SDD directory |
| Comandos legacy | Sólo sus options actuales | Todos los contratos nuevos de authoring; Commander debe rechazarlos como unknown options |

`--source` usa un contrato genérico y repetible `label=path`. El label no modifica ni descubre el archivo: sólo entrega semántica al writer. Para `pr-description` se recomiendan `intent`, `design`, `plan`, `validation` y `context`; para `document`, cualquier label descriptivo. Los labels se normalizan como identificadores no vacíos, se preservan en orden y un malformed source falla antes de leer o invocar el provider.

La autoridad de PR se interpreta así: template define formato; diff y commits describen implementación real; `intent` explica problema/alcance; `design` describe mecanismo esperado; `plan` es trabajo planificado y nunca prueba que esté implementado; `validation` sólo permite afirmar resultados presentes en esa fuente; `context` aporta información complementaria sin desplazar evidencia más fuerte.

## 🧠 Reglas cognitivas operacionales

- **Orientación antes que detalle:** explicar primero qué intenta entender el lector y por qué importa.
- **Relación causal antes que inventario:** privilegiar `causa → mecanismo → consecuencia` sobre listas de componentes.
- **Memoria de trabajo limitada:** mantener pequeño el conjunto de conceptos incompletos y resolver relaciones antes de abrir otras.
- **Construcción progresiva:** crecer desde comportamiento y motivación hacia mecanismo, invariantes, edge cases y detalle interno.
- **Recognition over recall:** repetir contexto sólo cuando cumpla una función cognitiva nueva y evite backtracking.
- **Pregunta natural, respuesta próxima:** responder cerca las dudas inmediatas que genera una afirmación importante.
- **Dos velocidades de lectura:** título, primer párrafo y headings soportan scan mode; el camino principal soporta read mode.
- **Epistemología visible:** hechos, evidencia, inferencias, hipótesis, decisiones, riesgos y pendientes siguen siendo distinguibles.

### Tests funcionales del documento

- **Scan test:** título, headings y primeras frases permiten reconocer propósito, cambio y zonas relevantes.
- **Backtracking test:** la lectura no exige volver repetidamente para recuperar conceptos o referentes.
- **Mental-model test:** el lector puede explicar qué ocurre, por qué y qué efecto produce; enumerar componentes no basta.
- **Artifact-contract test:** el template y campos obligatorios se preservan.
- **Epistemic-integrity test:** ninguna hipótesis, plan o test no ejecutado aparece como hecho confirmado.
- **PR-review test:** el reviewer llega al diff sabiendo qué comportamiento esperar y dónde concentrarse.

## 🚧 Boundary de compatibilidad

### Invariante principal

> Si nunca se ejecuta `zord author`, la versión con este feature debe comportarse igual que `master` para todos los comandos, configs, Zords, outputs y hooks existentes.

### No-touch list del MVP

- `src/commands/assemble.ts` y su contrato público.
- `src/commands/summon.ts` y su contrato público.
- `src/commands/fix.ts` y su contrato público.
- `src/core/runner.ts` y `runZord`.
- `src/core/orchestrator.ts` y `runZordsInParallel`.
- `src/core/synthesis.ts`, synthesizer y fallback.
- `src/core/outputArtifact.ts` y formatos actuales.
- `src/core/zordLoader.ts`, precedencia repo/global/bundled y `ZordMeta`.
- `ZordResult`, `Finding`, `SynthesisResult` y `RunResult`.
- Discovery de `zords/agents`, hooks y default command `assemble`.
- Defaults de config, weighted routing, GitHub labeling y cross-repo review.

Si la implementación descubre que necesita modificar alguno de esos símbolos, debe detenerse con `PLAN_CONFLICT`; no puede “resolver” el problema ampliando el diff.

### Únicos seams compartidos permitidos

1. Registrar aditivamente el subcomando `author` en `src/cli.ts` sin cambiar opciones ni handlers existentes.
2. Extender internamente el adapter Codex para aceptar un reasoning effort opcional por invocación. Cuando se omite, command, args, env, timeout y sandbox deben ser byte-for-byte equivalentes al comportamiento de `master`.
3. Agregar un path constante para `zords/writers` sólo si el módulo nuevo no puede resolverlo sin duplicación. El loader de reviewers no se modifica.

Todo contrato, type, loader, runner, recipe y test documental vive en archivos nuevos bajo `src/authoring/`, `src/commands/author.ts`, `zords/writers/` y tests dedicados.

## 🔗 Relación con Grimoire y SDD

### Decisión

Zords no es ni se convierte en un subsistema SDD. Grimoire puede crear y administrar specs; Human First puede utilizar cualquier texto que el caller entregue; Zords sólo ejecuta el authoring.

El core no conoce `.sdd`, `features/<slug>`, spec funcional, spec técnica ni tasks de Grimoire. No hay autodiscovery, default path, caché, output directory ni metadata específica de SDD.

Si un agente quiere usar una spec SDD, lo hace como cualquier otro archivo explícito:

```bash
zord author pr-description --initiative "Example" --base master --source design=.sdd/features/example/2-technical.md
```

Para Zords ese path es un `--source`; su origen y lifecycle son irrelevantes. Una integración automática Grimoire→Zords, si el equipo la desea, será otro proyecto y vivirá del lado de Grimoire o como adapter externo.

## 📐 Alcance

### Incluido

- Subcomando aislado `zord author` con recipes `document` y `pr-description`.
- Writer Human First versionado en un namespace que el loader de reviewers no escanea.
- Ejecución Codex read-only con `gpt-5.6-terra` y effort `high` explícitos.
- Inputs por flags/stdin y Markdown limpio por stdout.
- Diagnósticos, warnings y progreso exclusivamente por stderr.
- Lectura explícita y acotada de sources; lectura git read-only para la recipe de PR.
- Tests de aislamiento y regresión sobre la superficie legacy.
- Dogfood para generar la descripción del propio PR.

### Fuera de alcance

- Cambiar el contrato de Zords de review o introducir `task: review|document` en `ZordMeta`.
- Reutilizar `ZordResult` o findings para transportar documentos.
- Persistir drafts, metadata o caché desde Zords.
- Crear, descubrir, modificar o administrar SDD.
- Integración automática con Grimoire.
- Publicar o actualizar PRs en GitHub.
- Ejecutar tests o inferir validaciones no aportadas.
- Multi-provider authoring, routing ponderado o múltiples writers simultáneos.
- Configuración organizacional de xhigh.
- Telemetría remota, UI o editor documental.

## 🏗️ Arquitectura

### Arquitectura actual de review

```text
zords/agents ─> zordLoader ─> assemble/summon ─> orchestrator ─> runZord ─> ZordResult(findings) ─> synthesis/report
```

Este flujo permanece intacto.

### Arquitectura target aditiva

```text
                                      ┌─> author document ─┐
CLI ── comando nuevo zord author ─────┤                   ├─> input bundle ─> Human First writer ─> Codex Terra high ─> stdout Markdown
                                      └─> pr-description ─┘        │                                      │
                                                                  │                                      └─> stderr diagnostics
                                                      explicit sources + read-only git

CLI ── assemble/summon/fix ─> flujo legacy sin cambios
```

### Layout esperado

```text
src/
  authoring/
    types.ts
    input.ts
    writerLoader.ts
    runAuthor.ts
    recipes/
      document.ts
      prDescription.ts
  commands/
    author.ts
zords/
  writers/
    human-first-technical-writing.md
tests/
  authoring/
    input.spec.ts
    writerLoader.spec.ts
    runAuthor.spec.ts
    prDescription.spec.ts
  author.spec.ts
```

Los nombres pueden ajustarse a convenciones detectadas durante F0, pero los boundaries no: ningún módulo legacy importa authoring y authoring no modifica los contratos de review.

## 🔄 Secuencia de control

### `zord author document`

1. Commander valida recipe y flags.
2. `author.ts` reúne `--source`, stdin, purpose, audience y template explícito.
3. `input.ts` valida paths, tamaños y que exista contenido suficiente.
4. `writerLoader.ts` carga el writer bundled desde `zords/writers`.
5. La recipe compone instrucciones específicas sin duplicar la skill transversal.
6. `runAuthor.ts` invoca Codex en read-only con Terra high.
7. La ejecución se bufferiza; ante error no se emite documento parcial.
8. Si el output es válido y no vacío, se escribe Markdown una sola vez a stdout.
9. Warnings, modelo efectivo y fuentes usadas se escriben a stderr.

### `zord author pr-description`

1. Valida que exista un repo Git y resuelve `--base` sin modificarlo.
2. Obtiene diff y commits con operaciones read-only.
3. Lee template sólo si fue indicado o si existe en ubicaciones convencionales previamente acordadas.
4. Agrega `--source` explícitos como contexto no ejecutable.
5. Aplica la recipe de PR y el writer Human First.
6. Emite sólo la descripción Markdown por stdout.

## 📜 Contratos del MVP

### CLI

```text
zord author document [--source <label>=<path>...] [--template <path>] --purpose <text> [--audience <text>]
zord author pr-description --initiative <name> [--base <git-ref>] [--source <label>=<path>...] [--template <path>]
```

Estos contratos existen únicamente bajo `author`. `--source` puede repetirse y cada ocurrencia debe contener label y path separados por el primer `=`. Stdin puede complementar sources; la decisión exacta de precedencia se prueba en F1. `--initiative` es required para `pr-description`, describe el cambio al writer y jamás dispara autodiscovery. `--base` usa un default sólo si el repo ya tiene una convención inequívoca; ante ambigüedad debe fallar y pedir el ref, no adivinar.

### Output

```text
stdout: documento Markdown final y nada más
stderr: progreso, warnings, modelo/effort efectivo y errores humanos
exit 0: documento completo emitido
exit 1: input/config/validation error
exit 2: provider/model execution error
```

Los códigos exactos pueden alinearse con la convención existente durante F0, pero deben distinguir falla previa al modelo de falla del provider. No se imprime un documento parcial con exit distinto de cero.

### Writer manifest

```yaml
name: human-first-technical-writing
description: Reorganiza evidencia técnica según cómo una persona construye comprensión
provider: codex
model: gpt-5.6-terra
reasoning_effort: high
timeout: 300
```

El manifest de writer es un contrato nuevo dentro de `zords/writers`; no se agrega al schema de `ZordMeta` y no es visible para `discoverZords`.

### Input bundle interno

```ts
interface AuthoringInput {
  recipe: 'document' | 'pr-description';
  initiative?: string;
  purpose: string;
  audience?: string;
  template?: { path: string; content: string };
  sources: Array<{ label: string; path?: string; content: string }>;
  repository?: { base: string; head: string; diff: string; commits: string };
}
```

Este type es interno a `src/authoring/types.ts`; no se exporta desde el package root durante el MVP.

### Reglas de input y seguridad

- Sources explícitos se resuelven contra cwd/repo root y se rechaza path traversal no autorizado.
- Stdin y archivos se delimitan como datos no confiables para resistir prompt injection.
- Binarios, `.env`, credenciales y archivos sensibles conocidos se rechazan.
- Se fijan límites de bytes/tokens; si se trunca, stderr lo declara y el documento no puede insinuar que leyó el source completo.
- El diff se obtiene read-only y nunca ejecuta código del repo.
- El comando no escribe archivos, no hace checkout, no modifica Git y no accede a red salvo la invocación local del provider configurado.

### Unidades y edge cases

- Tamaños se expresan en bytes y tokens estimados; latencia en milisegundos; timestamps sólo se usan en diagnóstico si aportan valor.
- Sin input suficiente: error antes de invocar el modelo.
- Source duplicado: deduplicación determinista por path canónico o error claro.
- Source sin `=`, label vacío, path vacío o label inválido: error antes de leer el filesystem.
- `--initiative` vacío o entregado a `author document`: error de contrato; nunca se usa para resolver paths.
- Un flag de authoring entregado a un comando legacy: Commander lo rechaza; no se ignora silenciosamente.
- Template contradictorio con la heurística: manda el template.
- Source contradictorio: preservar la discrepancia; no elegir una verdad por fluidez.
- Diff vacío en `pr-description`: error accionable, salvo modo explícito futuro fuera de scope.
- Output vacío, sólo whitespace o rodeado por ruido del provider: validation error; no stdout parcial.
- No existen fórmulas de negocio. La autoridad es ordinal: template/contrato y evidencia real prevalecen sobre heurísticas del writer.

## 👁️ Observabilidad y control humano

- Stdout es composable y machine-friendly; no contiene spinners, títulos del CLI ni logs.
- Stderr identifica recipe, sources incluidos/omitidos, modelo, effort, truncaciones y duración.
- El MVP no persiste prompts, inputs, output ni metadata.
- El caller controla persistencia y publicación. Un agente puede capturar stdout, pero no obtiene autoridad implícita para crear o actualizar un PR.
- El owner acepta cada gate; el executor sólo puede dejarlo en `review`, `blocked` o `rejected`.
- Un cambio a no-touch, SDD autodiscovery, filesystem output, GitHub publishing, providers adicionales o xhigh requiere una decisión y proyecto/PR separados.

## 📋 Requisitos y evidencia

| ID | Estado | Requisito | Evidencia de aceptación |
|---|---|---|---|
| R1 | missing | Los comandos legacy no cambian comportamiento | Suite existente + snapshots/asserts de argv, discovery, outputs y help legacy |
| R2 | partial | Terra high puede invocarse sin alterar reviews | LOCAL_CHANGE demuestra command override; falta podar config global y repetir tests |
| R3 | missing | `zord author document` produce Markdown sólo por stdout | CLI integration con stdout/stderr separados y exit 0 |
| R4 | missing | `zord author pr-description` prepara al reviewer para el diff | Fixture pequeño/complejo + PR-review test |
| R5 | missing | Writer no es descubierto como reviewer | Assert que `discoverZords` ignora `zords/writers` sin modificar loader |
| R6 | missing | Zords no escribe documentos | Filesystem before/after idéntico en integration tests |
| R7 | partial | Zords es agnóstico de SDD | Boundary confirmado; falta assert de cero strings/rutas SDD en producción |
| R8 | missing | Sources y templates son explícitos y seguros | Tests de paths, secretos, límites, binarios e injection delimitada |
| R9 | missing | El documento preserva causalidad y certeza | Cognitive/epistemic fixtures y rubric humana |
| R10 | missing | Cualquier agente puede consumir la salida | Ejemplo automatizado que captura stdout sin parsing de logs |
| R11 | missing | Fallas no emiten documento parcial | Provider/input/output failure tests |
| R12 | missing | El paquete distribuye el writer | Test de package/dist que encuentra `zords/writers/human-first-technical-writing.md` |
| R13 | missing | Los contratos nuevos sólo existen bajo `zord author` | CLI tests prueban aceptación por recipe y rechazo como unknown options en comandos legacy |
| R14 | missing | La iniciativa y el rol de cada source son explícitos | Tests de `--initiative` y parser `label=path`; ningún autodiscovery o inferencia por filename |

## 🧭 Registro de decisiones

| ID | Estado | Resolución | Fuente/evidencia | Fase |
|---|---|---|---|---|
| D1 | CONFIRMED | Human First entra a Zords como authoring transversal; PR description es primera recipe | Decisión del owner | F1–F3 |
| D2 | CONFIRMED | El feature usa un camino hermano `zord author`, no el pipeline de review | Decisión del owner tras revisar riesgo | F0–F3 |
| D3 | TECHNICAL_RESOLUTION | El MVP no agrega `task: document` a `ZordMeta` ni cambia `zordLoader` | HEAD demuestra que loader/runner están acoplados a findings | F0 |
| D4 | TECHNICAL_RESOLUTION | Writer y contracts viven bajo `zords/writers` y `src/authoring` | Aislamiento por namespace y package layout existente | F1 |
| D5 | CONFIRMED | El documento se entrega sólo por stdout; Zords no lo persiste | Preferencia explícita del owner | F1–F3 |
| D6 | TECHNICAL_RESOLUTION | Logs y warnings van sólo a stderr; output se bufferiza antes de emitir | Composabilidad CLI y prevención de parciales | F1 |
| D7 | CONFIRMED | Zords no conoce ni administra SDD; cualquier spec entra sólo como `--source` explícito | Decisión explícita del owner | F0–F3 |
| D8 | CONFIRMED | El uso normal permite que cualquier agente invoque `zord author pr-description` y capture stdout | Objetivo funcional confirmado | F2–F3 |
| D9 | CONFIRMED | Provider/model/effort del MVP: Codex, `gpt-5.6-terra`, `high` | Decisión explícita del owner | F0–F3 |
| D10 | CONFIRMED | `xhigh` no forma parte del default ni del scope inicial | Minimización de superficie | F3/futuro |
| D11 | CONFIRMED | Zords no publica ni modifica PRs; el caller compone otra herramienta si tiene autorización | Boundary de autoridad | F2–F3 |
| D12 | TECHNICAL_RESOLUTION | El único cambio compartido de runtime es effort opcional por invocación Codex, con comportamiento idéntico cuando falta | Menor seam viable para Terra high | F0 |
| D13 | CONFIRMED | Integración automática con Grimoire queda fuera de este proyecto | Separación SDD/Zords | Futuro |
| D14 | CONFIRMED | `--initiative` y `--source <label>=<path>` son contratos exclusivos de `zord author`; los comandos legacy no los conocen | Confirmación explícita del owner | F1–F3 |
| D15 | TECHNICAL_RESOLUTION | `--initiative` sólo aporta contexto humano y los labels sólo aportan semántica; ninguno resuelve o descubre sources | Preserva el boundary agnóstico de SDD | F1–F2 |

## 🗺️ Mapa de archivos y símbolos

| Área | Acción | Archivo/símbolo | Responsabilidad |
|---|---|---|---|
| CLI | modify | `src/cli.ts` | Registrar `author` sin cambiar comandos existentes |
| Command | create | `src/commands/author.ts` | Parsear opciones author y enrutar recipes |
| Authoring types | create | `src/authoring/types.ts` | Contracts internos no exportados |
| Input | create | `src/authoring/input.ts` | Sources/stdin/template, límites y delimitación |
| Writer loader | create | `src/authoring/writerLoader.ts` | Cargar sólo writer bundled separado |
| Runner | create | `src/authoring/runAuthor.ts` | Ejecutar Terra high y separar stdout/stderr |
| Generic recipe | create | `src/authoring/recipes/document.ts` | Contrato de documento genérico |
| PR recipe | create | `src/authoring/recipes/prDescription.ts` | Contexto git read-only + PR contract |
| Writer asset | create | `zords/writers/human-first-technical-writing.md` | Reglas operacionales Human First |
| Codex seam | modify mínimo | `src/core/claude.ts` | Effort opcional por invocación; legacy invariant |
| Paths | conditional modify | `src/core/paths.ts` | Constante writers sólo si evita duplicación |
| Tests | create | `tests/authoring/*`, `tests/author.spec.ts` | Contracts, seguridad, CLI y regressions |
| Review types | no-touch | `ZordMeta`, `ZordResult`, `Finding`, `SynthesisResult` | No ampliar ni reutilizar |
| Review runtime | no-touch | loader, runner, orchestrator, synthesis, outputArtifact | Comportamiento legacy intacto |

## 🛣️ Roadmap y gates

```text
F0 Reconciliar WIP + seam Codex ──G0──> F1 Authoring genérico stdout ──G1──> F2 PR description ──G2──> F3 Evals + hardening + PR ──G3
```

| Gate | Estado actual | Responsabilidad del agente | Evidencia de aceptación del owner | Habilita |
|---|---|---|---|---|
| G0 | review | Podar WIP reemplazado, dejar seam mínimo y demostrar regresión cero | Diff revisado + suite/build/lint + legacy argv/discovery asserts | F1 |
| G1 | review | Entregar `author document`, writer y stdout contract aislados | Demo capturable + tests de no-write/no-discovery | F2 |
| G2 | review | Entregar `pr-description` read-only sin SDD ni publicación | Fixtures + PR-review test + regression suite | F3 |
| G3 | review | Entregar evals, hardening, docs, dogfood y PR | Release checks + descripción generada + review humana | Adopción |

## 📦 Paquetes autónomos

### Paquete autónomo Fase 0 — Reconciliar WIP y fijar seam mínimo

**Misión exacta:** Revertir a nivel de hunks únicamente el diseño documental invasivo del WIP, preservar la evidencia útil y dejar el cambio compartido mínimo necesario para que una invocación Codex nueva use Terra high sin alterar ninguna ejecución legacy.

**Precondiciones verificables:** Branch `feature/zords-technical-authoring`; HEAD `ac48d123`; working tree con cambios locales identificados; esta nota es el contrato vigente; no ejecutar comandos destructivos ni descartar cambios ajenos.

**Lectura obligatoria:** Secciones “Estado actual”, “Boundary de compatibilidad”, “Registro de decisiones” y “Mapa de archivos” de `VAULT_ROOT/10-projects/Meli/Zords — Human-First Technical Authoring/Zords — Human-First Technical Authoring.md`; diff local completo; `src/types.ts`, `src/core/claude.ts`, `src/core/config.ts`, `src/core/agentRouter.ts`, `src/core/zordLoader.ts`, `src/index.ts` y tests asociados.

**Decisiones cerradas:** Quitar/parkear `TaskType`, `Document*`, `task` metadata y validación/config global de reasoning si sólo sirven al approach rechazado; no modificar loader ni contracts review; effort se pasa como opción interna por invocación al adapter Codex; Terra high lo usa authoring, no cambia defaults de review.

**Implementación paso a paso:** 1) Clasificar cada hunk del WIP como conservar, rework o retirar. 2) Retirar fields/types/exports/docs/tests de `task: document` y contracts globales. 3) Retirar routing/config general que no sea necesario para authoring aislado. 4) Reexpresar reasoning effort como opción interna de `SpawnAgentOpts` o equivalente mínimo. 5) Añadir tests que comparen argv Codex legacy sin effort y argv Terra high con effort. 6) Confirmar que `zordLoader`, runner, orchestrator y comandos legacy quedan idénticos a HEAD salvo imports estrictamente inevitables; idealmente sin diff. 7) Ejecutar suite, build, lint y diff review.

**Archivos esperados:** modify mínimo `src/core/claude.ts`; tests del adapter; posibles hunks de limpieza en los once archivos del WIP. Al terminar, `src/core/zordLoader.ts`, review contracts y `src/core/agentRouter.ts` no deberían contener cambios de authoring.

**No tocar:** Código no relacionado del working tree; `assemble`, `summon`, `fix`, runner, orchestrator, synthesis, outputArtifact, review schemas, hooks y defaults.

**Spikes permitidos:** Verificar la sintaxis exacta de Codex CLI para `model_reasoning_effort` mediante command builder/mock; no invocar red ni ampliar config. Timebox: 45 minutos. Si el effort no puede pasar sin un cambio mayor, `PLAN_CONFLICT`.

**Tests y asserts:** Sin effort, argv Codex es exactamente el de master; con effort high aparecen sólo `--config model_reasoning_effort="high"`; provider no-Codex no recibe flags; existing config fixture y discovery producen resultados legacy; suite/build/lint verdes; `git diff --check` verde.

**Entregables/Gate G0:** Diff reducido y explicable, inventario conservar/rework/retirar, comandos de validación y G0 en `review`. El owner acepta sólo si ningún contract review fue ampliado.

**Handoff a Fase 1:** Entregar API interna exacta del adapter, test de invariancia legacy, working tree conocido y lista cerrada de archivos nuevos permitidos.

### Paquete autónomo Fase 1 — Authoring genérico aislado y stdout

**Misión exacta:** Entregar `zord author document` con writer Human First separado, sources explícitos, ejecución Terra high read-only y Markdown limpio por stdout, sin filesystem output ni dependencia de SDD.

**Precondiciones verificables:** G0 accepted; no diff inesperado en no-touch; package layout `zords/` confirmado; command registration convention conocida.

**Lectura obligatoria:** Gate G0; secciones “Definición del producto”, “Arquitectura”, “Secuencia de control” y “Contratos” de `VAULT_ROOT/10-projects/Meli/Zords — Human-First Technical Authoring/Zords — Human-First Technical Authoring.md`; `VAULT_ROOT/80-agents/skills/human-first-technical-writing/SKILL.md`; `src/cli.ts`, `src/core/paths.ts`, adapter Codex aprobado y package files.

**Decisiones cerradas:** Subcomando hermano; recipe `document`; no `task` en legacy metadata; writer en `zords/writers`; Codex Terra high; stdout documento, stderr diagnóstico; buffer completo; no writes; sources `label=path` explícitos; contracts limitados al árbol `author`; internal types no exportados.

**Implementación paso a paso:** 1) Crear contracts internos. 2) Crear parser author-only para repeated `--source <label>=<path>` y stdin. 3) Crear input loader con template, limits y seguridad. 4) Crear writer loader aislado. 5) Empaquetar skill agent-first sin teoría innecesaria. 6) Crear recipe generic con purpose/audience. 7) Crear runner que invoca provider y bufferiza output. 8) Crear command handler y registrar `author document`. 9) Implementar separación estricta stdout/stderr y exit codes. 10) Probar que flags author no aparecen ni son aceptados en comandos legacy, reviewer discovery ignora writers y filesystem no cambia. 11) Ejecutar regression suite.

**Archivos esperados:** create `src/authoring/types.ts`, `input.ts`, `writerLoader.ts`, `runAuthor.ts`, `recipes/document.ts`, `src/commands/author.ts`, `zords/writers/human-first-technical-writing.md` y tests; modify aditivo `src/cli.ts`; conditional `src/core/paths.ts`.

**No tocar:** Todos los archivos/símbolos de la no-touch list, PR recipe, GitHub, SDD, persistence, xhigh y provider routing.

**Spikes permitidos:** Confirmar formato stdout real de Codex y sanitización mínima. Timebox: 60 minutos. Si requiere parsear un schema de findings o cambiar runner legacy, `PLAN_CONFLICT`.

**Tests y asserts:** Source `label=path`, stdin sólo y combinación definida; malformed label/path falla antes del provider; no input falla; template prevalece; secret/binary/path inválido falla; stdout contiene sólo Markdown; stderr nunca contamina stdout; provider failure no emite parcial; writer no aparece en `list/discoverZords`; flags author en comandos legacy fallan como unknown options; ninguna escritura en cwd/repo; package dist contiene writer; legacy suite verde.

**Entregables/Gate G1:** Comando demo capturable, tests unit/integration, package verification y G1 en `review`. La aceptación humana valida que un agente pueda consumir stdout directamente.

**Handoff a Fase 2:** Entregar API de recipe, shape de `AuthoringInput`, command test harness, writer version y ejemplo probado de captura stdout.

### Paquete autónomo Fase 2 — Recipe PR description read-only

**Misión exacta:** Entregar `zord author pr-description` como uso normal para humanos y agentes, reuniendo realidad Git read-only y sources explícitos para preparar cognitivamente el review sin publicar ni persistir nada.

**Precondiciones verificables:** G1 accepted; generic pipeline estable; fixture Git aislado disponible; no-touch sin drift.

**Lectura obligatoria:** Gate G1; secciones “Recipes del MVP”, “Relación con Grimoire y SDD”, “Contratos” y “Tests funcionales” de `VAULT_ROOT/10-projects/Meli/Zords — Human-First Technical Authoring/Zords — Human-First Technical Authoring.md`; `src/core/diff.ts` sólo como evidencia/reuse importable sin modificar; templates PR convencionales del fixture.

**Decisiones cerradas:** Git read-only; `--initiative` required y sólo contextual; base explícita ante ambigüedad; diff/commits representan implementación real; template manda; sources `label=path` adicionales son opcionales; labels recomendados `intent/design/plan/validation/context`; no autodiscovery SDD; no tests ejecutados; no GitHub; stdout-only.

**Implementación paso a paso:** 1) Crear recipe PR sobre el pipeline de F1. 2) Validar `--initiative` sin usarla para discovery. 3) Resolver repo/base/head sin checkout/fetch. 4) Obtener diff y commits con helpers existentes o módulo nuevo sin modificar legacy. 5) Resolver template mediante flag y ubicaciones convencionales acotadas. 6) Incorporar sources etiquetados y aplicar su autoridad semántica. 7) Construir prompt causal orientado al reviewer. 8) Registrar warnings de contexto ausente en stderr. 9) Validar output contra template y epistemic invariants. 10) Añadir command route. 11) Probar uso por pipe/captura y regression.

**Archivos esperados:** create `src/authoring/recipes/prDescription.ts` y fixtures/tests; modify `src/commands/author.ts`; posible create helper Git bajo `src/authoring/`; documentación de uso.

**No tocar:** `src/core/diff.ts` salvo que el owner apruebe un PLAN_CONFLICT; Git working tree/index; GitHub; SDD; review pipeline; filesystem output.

**Spikes permitidos:** Reusar `computeDiff` versus helper authoring nuevo, timebox 45 minutos. Elegir la opción que no cambie contratos ni comportamiento legacy; registrar evidencia.

**Tests y asserts:** Initiative required/vacía; initiative no genera filesystem lookup; diff pequeño/complejo; base inválida; diff vacío; commits; template; sources `intent/design/plan/validation/context`; `plan` no se presenta como completado; source contradice diff y se presenta como discrepancia; test no aportado no se afirma; ninguna string de producción conoce `.sdd/features`; stdout pipeable; stderr informativo; cero writes; suite legacy verde.

**Entregables/Gate G2:** PR description útil en fixtures, PR-review rubric, demo `zord author pr-description --initiative ... --base ... --source intent=...`, no-write proof y G2 en `review`.

**Handoff a Fase 3:** Entregar fixtures, outputs candidatos, warnings conocidos, métricas iniciales, commands exactos y checklist de dogfood.

### Paquete autónomo Fase 3 — Calidad, hardening, dogfood y PR

**Misión exacta:** Demostrar que el feature aislado mejora la comprensión humana sin regresiones, documentarlo, generar la descripción del propio PR por stdout y dejar el cambio listo para review del equipo.

**Precondiciones verificables:** G2 accepted; feature completo en branch; owners/reviewers identificados; release checks disponibles.

**Lectura obligatoria:** Gate G2; secciones “Tesis”, “Reglas cognitivas”, “Boundary”, “Riesgos”, “Rollout y rollback” y “Definition of Done” de `VAULT_ROOT/10-projects/Meli/Zords — Human-First Technical Authoring/Zords — Human-First Technical Authoring.md`; README/contribution/release process del repo y template PR.

**Decisiones cerradas:** High default; no xhigh benchmark obligatorio para merge; rollout opt-in por comando; cero persistence/publication; narrativa del PR debe vender el cuello de botella de comprensión humana y demostrar aislamiento técnico.

**Implementación paso a paso:** 1) Completar fixtures cognitivos y epistemológicos. 2) Ejecutar threat model de sources/stdout/provider. 3) Añadir regresiones de CLI/help/discovery/argv. 4) Documentar `author document`, `pr-description`, pipes, límites y troubleshooting. 5) Verificar package/dist. 6) Ejecutar dogfood y capturar stdout externamente para revisión. 7) Revisar manualmente scan/mental-model/PR-review tests. 8) Ejecutar release process. 9) Preparar PR con diff reducido, evidencia, rollout y rollback.

**Archivos esperados:** tests/evals/docs; output de dogfood fuera del control de Zords y no necesariamente versionado; ningún store nuevo.

**No tocar:** SDD/Grimoire, GitHub API, auto-publish, providers adicionales, xhigh defaults, telemetry y cualquier no-touch legacy.

**Spikes permitidos:** Ninguno salvo incompatibilidad reproducible de packaging/OS; crear PLAN_CONFLICT antes de ampliar scope.

**Tests y asserts:** Unit/integration completos; build/lint/dist; package writer present; legacy command behavior; no-write proof; injection/path/secret limits; cognitive rubric; dogfood reproducible; `git diff --check`; descripción stdout sin logs.

**Entregables/Gate G3:** PR listo, descripción Human First generada por `zord author pr-description`, evidencia de cero regresión, docs y rollback claros. El owner acepta G3; el executor no mergea por sí solo.

**Handoff a siguiente etapa:** Nuevas recipes, Grimoire adapter, persistence opt-in, multi-provider o xhigh se abren como iniciativas separadas después de adopción.

## ✅ Tareas

- [ ] T0.1 — objetivo: crear issue y fijar owners | archivos/símbolos: issue tracker + Entrega de desarrollo | precondiciones: plan validado | implementación: trasladar framing cognitivo, approach aislado y no-touch | tests: issue no promete SDD/persistence ni cambia review | evidencia: URL/ID y reviewers #owner/me #type/admin #area/meli
- [x] T0.2 — objetivo: conservar branch reproducible | archivos/símbolos: branch + base | precondiciones: base verificada | implementación: mantener `feature/zords-technical-authoring` sobre `master@ac48d123` | tests: merge-base verificado | evidencia: branch actual #owner/me #type/dev #area/meli
- [x] T0.3 — objetivo: podar approach rechazado | archivos/símbolos: tipos/config/router/loader/index/README/tests WIP | precondiciones: nuevo D2–D7 | implementación: retirar sólo hunks `task/document` y config global reemplazados | tests: no diff authoring en no-touch | evidencia: inventario de hunks + diff reducido #owner/agent #type/dev #area/meli
- [x] T0.4 — objetivo: dejar seam Codex mínimo | archivos/símbolos: `src/core/claude.ts` + tests | precondiciones: T0.3 | implementación: effort opcional por invocación, no config global | tests: argv legacy exacto + Terra high | evidencia: suite/build/lint y G0 review #owner/agent #type/dev #area/meli
- [x] T1.1 — objetivo: definir contracts internos | archivos/símbolos: create `src/authoring/types.ts` | precondiciones: G0 accepted | implementación: input/recipe/result internos | tests: compile y no root exports | evidencia: types aislados #owner/agent #type/dev #area/meli
- [x] T1.2 — objetivo: cargar inputs seguros | archivos/símbolos: create `src/authoring/input.ts` + tests | precondiciones: T1.1 | implementación: parser author-only `label=path`, stdin, template, limits y delimitación | tests: malformed labels, paths, secrets, binary, duplicate, empty y rechazo en legacy | evidencia: unit/CLI suite #owner/agent #type/dev #area/meli
- [x] T1.3 — objetivo: empaquetar y ejecutar writer | archivos/símbolos: writerLoader, runAuthor, writer asset | precondiciones: T1.2 | implementación: Terra high read-only, buffer, stdout/stderr | tests: provider success/failure, no partial, no discovery | evidencia: integration suite #owner/agent #type/dev #area/meli
- [x] T1.4 — objetivo: exponer `author document` | archivos/símbolos: create command + modify CLI | precondiciones: T1.3 | implementación: flags, recipe generic y help | tests: capture stdout, zero writes, legacy help | evidencia: demo y G1 review #owner/agent #type/dev #area/meli
- [x] T2.1 — objetivo: reunir contexto Git read-only | archivos/símbolos: create helper authoring/PR | precondiciones: G1 accepted | implementación: base/head/diff/commits/template | tests: invalid/empty/complex repo | evidencia: fixture bundles #owner/agent #type/dev #area/meli
- [x] T2.2 — objetivo: implementar recipe PR | archivos/símbolos: create `prDescription.ts` | precondiciones: T2.1 | implementación: initiative contextual, causal path, autoridad por labels y warnings | tests: initiative, intent/design/plan/validation/context, template, discrepancy y missing validation | evidencia: golden structural outputs #owner/agent #type/dev #area/meli
- [x] T2.3 — objetivo: exponer uso normal de agentes | archivos/símbolos: author command/tests/docs | precondiciones: T2.2 | implementación: `author pr-description`, pipe y capture | tests: stdout machine-friendly, stderr separated | evidencia: scripted consumption #owner/agent #type/dev #area/meli
- [x] T2.4 — objetivo: demostrar aislamiento | archivos/símbolos: whole repo tests | precondiciones: T2.3 | implementación: no-write/no-SDD/no-legacy-diff audit | tests: legacy suite + grep/asserts + integration | evidencia: G2 review #owner/agent #type/dev #area/meli
- [ ] T3.1 — objetivo: evaluar calidad cognitiva | archivos/símbolos: fixtures/rubric | precondiciones: G2 accepted | implementación: scan/backtracking/mental-model/epistemic/PR review | tests: sample pequeña y compleja | evidencia: eval report #owner/agent #type/research #area/meli
- [x] T3.2 — objetivo: endurecer seguridad y packaging | archivos/símbolos: authoring tests/dist | precondiciones: T3.1 | implementación: injection/limits/package/platform | tests: threat cases + dist content | evidencia: security/package report #owner/agent #type/dev #area/meli
- [x] T3.3 — objetivo: documentar adopción | archivos/símbolos: README/help/troubleshooting | precondiciones: T3.2 | implementación: usage, pipes, boundaries, rollback | tests: examples executable | evidencia: docs review #owner/agent #type/dev #area/meli
- [x] T3.4 — objetivo: hacer dogfood por stdout | archivos/símbolos: branch real + PR template | precondiciones: T3.3 | implementación: ejecutar pr-description sin output file propio | tests: rubric humana + logs separados | evidencia: descripción de PR #29 producida por stdout y revisada contra el diff #owner/agent #type/dev #area/meli
- [x] T3.5 — objetivo: abrir PR seguro | archivos/símbolos: release process + PR | precondiciones: T3.4 | implementación: checks, diff review y publicación humana | tests: suite/build/lint/dist/diff-check | evidencia: PR #29, workflow verde y G3 en review #owner/me #type/pr-review #area/meli

## 🧪 Estrategia de validación

### Regresión legacy obligatoria

- `assemble`, default command, `summon`, `fix`, `list`, `add`, `enable`, `disable` y `check` conservan help, options y handlers.
- Un Zord legacy sin campos nuevos produce el mismo metadata y `ZordResult`.
- `discoverZords` sólo escanea `zords/agents`; el writer no aparece en list/assemble/summon.
- Codex legacy sin effort conserva exactamente su argv; Claude/Gemini/Copilot/custom no cambian.
- Config legacy válida mantiene el mismo resultado y fallback.
- Output review JSON/Markdown y synthesis no cambian.

### Authoring

- Unit: input parsing, source boundaries, manifest, prompt composition, output validation y errors.
- Integration: CLI stdout/stderr, provider mock, pipe/capture, no-write y package layout.
- PR fixtures: cambio pequeño, bug concurrente, migración, template obligatorio, diff vacío, base inválida, sources contradictorios y tests no aportados.
- Cognitive eval: scan, backtracking, mental model, epistemic integrity y PR readiness.
- Security: traversal, symlinks, secrets, binary, oversized input, prompt injection y partial output.

### Criterio de éxito

- Un agente puede ejecutar el comando y usar stdout sin limpiar logs ni conocer internals de Zords.
- El reviewer llega al diff con un modelo causal correcto y foco de inspección.
- Ninguna afirmación de implementación o validación carece de evidencia.
- Un cambio pequeño genera una descripción proporcional.
- El repo y el filesystem quedan idénticos después de authoring, salvo efectos externos elegidos por el caller mediante pipes.
- Todos los tests legacy pasan y el diff no modifica símbolos de la no-touch list.

## ⚠️ Riesgos y mitigaciones

| Riesgo | Consecuencia | Mitigación |
|---|---|---|
| Hacer pasar un writer por reviewer | Outputs inválidos y acoplamiento | Registry/runtime separados; sin `task` legacy |
| Tocar demasiados archivos core | Regresión difícil de detectar | Dos seams compartidos máximos y no-touch explícito |
| Stdout contaminado | Agentes/scripts no pueden consumirlo | Documento sólo stdout; todo diagnóstico stderr |
| Provider falla después de emitir parcial | Documento corrupto capturado | Buffer completo y write único sólo en success |
| Zords se acopla a Grimoire | Scope y lifecycle confusos | Sin SDD en producción; source explícito genérico |
| Source malicioso altera instrucciones | Prompt injection | Delimitación como datos, límites y tests adversariales |
| Descripción fluida inventa certeza | Confianza falsa | Epistemic rules + fixtures contradictorios |
| PR recipe ejecuta o publica acciones | Expansión de autoridad | Git read-only; no tests, no GitHub, no writes |
| Terra high cambia review legacy | Regresión transversal | Effort por invocación; absent invariant exacto |
| Feature crece a framework documental | Mantenimiento prematuro | Dos recipes y un writer; expansión por iniciativas separadas |

## 🚀 Rollout y rollback

### Rollout

1. El comando es opt-in: nadie cambia comportamiento hasta ejecutar `zord author`.
2. Dogfood en el propio PR y 2–3 casos voluntarios.
3. Revisión humana de fidelidad, comprensión y proporcionalidad.
4. Merge sólo con regression evidence y no-touch review.
5. Nuevas recipes se agregan después como PRs aislados.

### Rollback

- Retirar el registro de `author`, módulos `src/authoring`, command y writer asset; el review pipeline no requiere migración.
- Retirar el effort opcional del adapter Codex si causa problemas; callers legacy nunca dependieron de él.
- No existen documentos, cachés, metadata, specs ni estado persistido que migrar o borrar.
- No hay cambios remotos de GitHub que revertir porque Zords no publica.

## 🏁 Definition of Done

- [ ] R1–R14 tienen evidencia revisable.
- [ ] G0–G3 fueron aceptados por el owner en orden.
- [ ] El WIP invasivo fue retirado sin perder cambios ajenos.
- [ ] No hay diff de authoring en la no-touch list, salvo seams explícitamente permitidos.
- [ ] `zord author document` y `zord author pr-description` emiten sólo Markdown por stdout.
- [ ] Ningún comando author escribe archivos, administra SDD o publica PRs.
- [ ] Terra high es explícito y reviews sin effort conservan argv exacto.
- [ ] Writer bundled no es descubierto como reviewer y está presente en dist/package.
- [ ] Suite legacy + authoring, build, lint, dist y diff-check pasan.
- [ ] Cognitive/epistemic/PR-review tests fueron revisados.
- [ ] La descripción del propio PR fue generada por stdout y revisada por un humano.
- [ ] PR abierto con rollout/rollback y evidencia de aislamiento.

## 🧾 Prompt común para ejecutar una fase

> Implementa únicamente la fase asignada de [[Zords — Human-First Technical Authoring]]. El objetivo superior es agregar authoring sin cambiar ninguna funcionalidad actual. Trata la no-touch list, stdout-only, ausencia de SDD y no-publication como invariantes. Antes de editar, verifica HEAD, branch y working tree; clasifica LOCAL_CHANGE y preserva cualquier hunk ajeno. No uses comandos destructivos. Si necesitas tocar un símbolo no-touch o ampliar un contrato legacy, detente con `PLAN_CONFLICT` y evidencia. Ejecuta todos los tests/asserts del paquete, actualiza tareas/bitácora y deja el gate en `review`; nunca comiences la fase siguiente ni aceptes tu propio gate.

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Reconciliar WIP y fijar seam mínimo
GATE_REQUERIDO=none
TAREAS=T0.1-T0.4
SALIDA=diff podado, seam Codex mínimo, tests legacy y evidencia G0
STOP=marcar G0 review; prohibido crear runtime authoring
```

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Authoring genérico aislado y stdout
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1-T1.4
SALIDA=author document, writer, stdout contract, no-write proof y evidencia G1
STOP=marcar G1 review; prohibido implementar recipe PR
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — Recipe PR description read-only
GATE_REQUERIDO=G1 accepted
TAREAS=T2.1-T2.4
SALIDA=pr-description stdout, fixtures, no-SDD/no-write proof y evidencia G2
STOP=marcar G2 review; prohibido publicar PR o comenzar hardening final
```

**Despacho Fase 3**

```text
FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3 — Calidad, hardening, dogfood y PR
GATE_REQUERIDO=G2 accepted
TAREAS=T3.1-T3.5
SALIDA=evals, security/package evidence, docs, dogfood stdout y PR listo
STOP=marcar G3 review; prohibido mergear o ampliar scope
```

## 📆 Bitácora

- **2026-08-26** — Proyecto creado. Se definió Human First como capacidad transversal, PR description como primera implementación y Terra high como baseline.
- **2026-08-26** — F0 original produjo WIP con `TaskType`, contracts `Document*`, `reasoning_effort` configurable y carga `task` en el loader. Reportó 433 tests verdes, build correcto y lint sin errores; G0 quedó en review.
- **2026-08-26** — El owner rechazó el approach por superficie y riesgo sobre un repo nuevo. G0 se reabrió. Nuevo diseño: `zord author` paralelo, writer separado, stdout-only, no persistence, no `task` legacy, no SDD y PR description consumible por cualquier agente. El WIP anterior se conserva físicamente para reconciliación hunk-by-hunk; esta actualización no modificó código.
- **2026-08-26** — Se cerró el contrato de invocación: `--initiative` y `--source <label>=<path>` existen sólo bajo `zord author`. Initiative aporta nombre humano sin discovery; labels aportan semántica genérica. Los comandos legacy deben rechazar esos flags y permanecer sin cambios.
- **2026-08-26** — Se implementó el vertical `zord author` en `feature/zords-technical-authoring`: recipes `document` y `pr-description`, writer bundled Human First, sources/templates seguros y explícitos, Git read-only, stdout-only, seam Codex para `model_reasoning_effort`, README y 458 tests passing; G0–G2 quedan en `review` para aceptación humana y T3.4/T3.5 siguen pendientes.
- **2026-09-01** — El synthesizer bundled adopta el contrato editorial Human First para el reporte final, preservando JSON, headings y ubicación fuera de `zords/agents`; se agregan tests de contrato/aislamiento y la suite queda en 460 tests passing. G0–G2 siguen en `review`.
- **2026-09-01** — El cierre intentó reindexar Graphify; el gate global encontró 25 errores y 6 warnings en notas fuera del alcance de Zords, por lo que el índice queda pendiente sin modificar esa deuda.
- **2026-09-01** — Se rebasa el feature sobre `origin/master@6035510`, se publica el fork y se abre el PR #29. El propio Zord revisa el cambio; sus findings conducen a aislar tools/config del provider, estructurar contexto como JSON, cerrar carreras de archivos y filtrar secretos en paths, diffs, commits, sources, stdin y templates. La suite final queda en 544 tests, build/dist/lint verdes y workflow remoto exitoso; G3 pasa a review.
- **2026-09-01** — La skill se porta a `ads-signals-skills-marketplace` v1.0.0 sin permisos ni runtime; el catálogo sube a v1.2.0, el validator revisa 3 skills y se abre el PR #1 con la tesis de carga cognitiva, memoria de trabajo, chunking, señalización y modelos mentales. El Code Reviewer automático no encuentra issues y aprueba el PR como low-risk.

## 🔗 Docs / Links

- Skill canónica: `VAULT_ROOT/80-agents/skills/human-first-technical-writing/SKILL.md`.
- Repo: `local-agents-pipeline-cli`.
- Marketplace: [[ads-signals-skills-marketplace]] · [PR #1](https://github.com/melisource/fury_ads-signals-skills-marketplace/pull/1).
- PR Zords: [#29](https://github.com/melisource/fury_local-agents-pipeline-cli/pull/29).
- Modelo: [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra).
- SDD/Grimoire: integración automática fuera de scope; specs sólo pueden entrar como sources explícitos genéricos.

## 💡 Ideas posteriores

- Adapter Grimoire que invoque `zord author` pasando sources explícitos, sin trasladar lifecycle SDD a Zords.
- Recipes adicionales para decisiones técnicas, incidentes o guías, cada una en PR separado.
- Soporte opt-in de xhigh evaluado contra high.
- Output JSON/provenance o filesystem output sólo si aparece una necesidad real y con contrato separado.
- Multi-provider authoring después de estabilizar el vertical Codex.

### Motivos / principios

- El artefacto existe para habilitar una decisión humana, no para demostrar cuánto contexto procesó el agente.
- La complejidad legítima pertenece al documento; la causada por mala organización no.
- Más documentación no es necesariamente mejor documentación.
- El primer feature en un repo desconocido debe privilegiar aislamiento, reversibilidad y evidencia de no regresión.
- Stdout entrega composición sin obligar a Zords a poseer persistencia ni publicación.

### Memoria pública / interna

- **Memoria pública:** Esta nota gobierna scope, decisiones, gates y handoffs.
- **Memoria interna:** No aplica; authoring no depende de estado oculto ni cache local.
- **Motivo:** Un feature seguro debe poder explicarse y revertirse desde contratos visibles.
