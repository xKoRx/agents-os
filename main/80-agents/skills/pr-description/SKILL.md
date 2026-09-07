---
type: skill
schema_version: 1
name: pr-description
scope: global
description: Escribir la descripción de un Pull Request para cualquier repo de trabajo (Meli/RIO/Signals y equivalentes). Usar cuando el usuario pida "la descripción del PR", "arma el PR", "descripción para el pull request", o cuando termine una entrega y quiera el texto para GitHub. La descripción se materializa SIEMPRE como recurso del proyecto en el vault (`10-projects/<Área>/<Proyecto>/Descripción PR — <repo>.md`), NUNCA como archivo en la raíz del repo, y su estructura la manda el template `.github` del repo destino. NO crea, abre ni pushea el PR. NO hace code review (eso es signals-code-review).
created: 2026-08-24
updated: 2026-08-24
entities: []
related:
  - "[[Descripciones de PR — recurso del proyecto en el vault]]"
  - "[[signals-code-review]]"
aliases:
  - descripción de PR
  - descripcion pr
  - pull request description
  - armar descripción del PR
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - action/authoring
  - tech/git
  - tech/github
---

# pr-description

## Purpose

Producir la descripción de un PR con evidencia real, en el formato del repo destino, materializada como recurso del proyecto en el vault. Un repo por descripción.

## Inputs

Si falta alguno, resolverlo antes de escribir; no inventarlo:

- **Repo(s)** y **branch** de la entrega. Sin branch no hay descripción: no se sabe qué diff describe.
- **Proyecto del vault** al que pertenece (`10-projects/<Área>/<Proyecto>/`). Si no hay proyecto, preguntar; no crear la nota fuera de un proyecto.
- **Spec / issue** asociado, si existe.

## Procedure

### 1. Resolver el template del repo

```bash
ls .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE/ 2>/dev/null
```

Leerlo completo. Respetar sus secciones, su orden, sus checkboxes y su **idioma original**, aunque el idioma del template contradiga el `CODING_GUIDELINES.md` del mismo repo; en ese caso anotar la tensión en las notas internas. Los templates difieren entre repos: no reutilizar el de otro repo ni inventar secciones.

Sin template en el repo: usar las secciones mínimas —qué cambia, por qué, cómo se probó, issue/spec— y decirlo explícitamente en la nota.

### 2. Reunir evidencia

```bash
git -C <repo> rev-parse --abbrev-ref HEAD
git -C <repo> merge-base <base> <branch>
git -C <repo> log --oneline <base>..<branch>
git -C <repo> diff --stat <base>...<branch>
git -C <repo> status --short
```

Registrar: branch, base real y su SHA, commits, diffstat, y **archivos sin trackear** (un archivo nuevo sin `git add` es feature que no entra al PR: es bloqueante, no nota al pie).

Correr la suite del repo y usar los números reales (tests, fallas, skipped, gates de cobertura). Si no se corrió, decirlo; nunca escribir "todo verde" sin números.

### 3. Escribir con la barra de evidencia

- Nada se afirma sin evidencia observada en esta sesión.
- Los checkboxes del template se marcan **solo si son verdad**. Los que no, quedan sin marcar con una línea de por qué en la misma línea.
- Los bloqueantes van **arriba, visibles**, no escondidos en un checkbox: versión de artefacto de prueba, dependencia downstream no publicada, base desactualizada, trabajo sin commitear, ruido ajeno en el diff.
- Explicar las decisiones de diseño no obvias (por qué un filtro es igualdad exacta, por qué un gate cuelga de X y no de Y). Un reviewer que entiende el porqué revisa el qué.
- Sin hard-wrap: cada párrafo y cada bullet en una sola línea continua.

### 4. Materializar la nota

```bash
python3 80-agents/skills/_shared/scripts/materialize_schema_note.py doc "10-projects/<Área>/<Proyecto>/Descripción PR — <repo>.md"
```

Estructura de la nota, en este orden:

1. **Frontmatter** — `related` al proyecto, a la aplicación y a la descripción hermana del otro repo; `tags` con `project/<slug>`.
2. **Línea de identidad** — repo · branch @ SHA · base @ SHA · commits · diffstat · specs · dependencias entre repos · resultado de la suite con fecha.
3. **Callout de bloqueantes** — uno por bloqueante, en negrita el título.
4. **`## Propósito` y `## Contenido`** — por qué la nota vive en el vault y qué contiene.
5. **`---`, y luego el cuerpo del PR**: las secciones del template del repo, tal cual, listas para copiar y pegar.
6. **`---`, y `## Notas internas — NO van al PR`** — smells detectados, deuda, decisiones fuera de alcance, tensiones con los specs.

Si ya existe una nota con ese nombre para una entrega abandonada: renombrarla a `Descripción PR — <repo> (entrega descartada).md` y actualizar los enlaces del proyecto. No sobreescribirla ni borrarla sin pedirlo.

### 5. Cerrar referencias en ambas direcciones

- **Nota del proyecto:** enlazar la descripción y dejar escrita la branch de **cada** repo en el estado del proyecto. Con varios repos, se nombran todos: una sola branch mencionada es error de trazabilidad.
- **Bitácora del proyecto:** una línea con fecha, qué se describió y sobre qué branch.
- **Specs:** si el funcional o el técnico quedó desalineado con lo implementado, marcarlo en las notas internas.
- **`change_log`** consolidado en `80-agents/journal/logs/`.

## Output

Una nota por repo en la carpeta del proyecto, más el proyecto y su bitácora actualizados. Reportar al usuario: ruta de cada nota, branch descrita y la lista de bloqueantes, en dos o tres líneas.

## Hard Rules

- **Nunca** crear `descripcion_pr.md` ni equivalente en la raíz del repo. Si existe uno de una sesión anterior, migrarlo al vault y borrarlo del repo.
- **Nunca** crear, abrir, pushear ni comentar el PR. Esta skill produce texto, no ejecuta acciones sobre GitHub.
- Una descripción por repo. Un cambio cross-repo son N notas, cada una con el template de su repo y enlazada a las otras.
- No commitear ni modificar el código del repo para "arreglar" lo que se encuentre. Lo que esté mal se reporta como bloqueante.
- Versión de artefacto: una rama feature usa versión de prueba con sufijo; si el consumidor apunta a esa versión o a `mavenLocal()`, es **bloqueante del merge** y va en el callout.
- No marcar un checkbox del template por cortesía.
