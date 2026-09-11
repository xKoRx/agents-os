---
type: tool
schema_version: 1
status: active
scope: tool
area: "[[Personal]]"
project: "[[AGENTS OS]]"
source_url: https://github.com/melisource/fury_local-agents-pipeline-cli
command:
  - zord
  - zord assemble
  - zord summon
  - zord fix
  - zord list
  - zord add
  - zord check
entities:
  - "[[local-agents-pipeline-cli]]"
related:
  - "[[local-agents-pipeline-cli-source]]"
  - "[[AGENTS OS]]"
  - "[[agents-os-resource-wiki]]"
aliases:
  - "@local-agents-pipeline/zords"
  - Megazord
  - Zords
  - zord
  - Zord
load_policy: when_tool_loaded
indexable: true
index_priority: high
tags:
  - kind/tool
  - scope/tool
  - priority/high
created: 2026-08-26
updated: 2026-09-11
---

# local-agents-pipeline-cli

> [!info]+ local-agents-pipeline-cli
> **Tipo:** tool · **Estado:** active

## Descripcion

- `local-agents-pipeline-cli` es una CLI de Node.js/TypeScript publicada como `@local-agents-pipeline/zords`; su binario es `zord` y convierte un diff de Git en una revisión compuesta por varios agentes especializados llamados Zords.
- El pipeline separa cuatro responsabilidades: seleccionar el diff, cargar prompts Markdown con metadata YAML, ejecutar revisores en paralelo y sintetizar un reporte unificado en español.
- La unidad de extensión principal es un archivo `.md` con frontmatter (`name`, `description`, `model`, `timeout`, `hooks`, `tools`, `max_budget_usd`, `enabled`) y un prompt que obliga al agente a devolver JSON con `findings`.
- En el checkout verificado, `master` está en `ac48d12`, el paquete declara versión `1.0.2`, el remoto es `melisource/fury_local-agents-pipeline-cli` y el código disponible en `master` es la variante LLM; los zords deterministas mediante `run:` existen en `origin/feature/script-agents` y no deben tratarse como capacidad de `master`.

### Modelo mental

```text
Git diff o PR → descubrimiento de Zords → asignación a agentes → ejecución paralela → JSON por Zord → síntesis → terminal/artefactos → fix selectivo opcional
```

La herramienta es un orquestador local de procesos, no un modelo de IA ni un servidor central: delega el análisis a CLIs instaladas en el host y mantiene la configuración, prompts, estado del router y artefactos en archivos locales.

## Uso principal

- Revisar cambios antes de push o commit con revisores enfocados en security, anti-patterns, performance, contratos de I/O, idiomacy, simplification y riesgo de revisión humana.
- Revisar pull requests de GitHub mediante `gh pr diff`, incluyendo PRs de otro repositorio con `owner/repo#123` o URL completa.
- Ejecutar una revisión puntual con uno o varios Zords, hacer preview sin consumo de API, emitir JSON para automatizaciones y guardar reportes JSON/Markdown con IDs estables.
- Aplicar fixes seleccionados desde un artefacto JSON, agrupándolos por el agente que produjo cada finding o forzando un agente configurado.
- Reutilizar prompts versionables por repositorio (`.zords/agents/`) o globales (`~/.config/zords/agents/`) sin cambiar el código de la CLI.

## Operaciones / comandos

- `npm install -g @local-agents-pipeline/zords` instala el paquete publicado y expone `zord`; requiere Node.js compatible con el rango declarado por el paquete (`^20.12 || ^22.12 || ^24.11.1`), `git` y al menos una CLI de agente configurada.
- `zord assemble` descubre todos los Zords habilitados para el trigger `manual`, calcula el diff contra la rama remota por defecto y ejecuta el pipeline completo.
- `zord assemble --scope staged` revisa solo cambios staged; `--scope commit` revisa `HEAD~1..HEAD`; `--scope branch` usa `merge-base HEAD origin/<default-branch>...HEAD` y cae a `HEAD~1` si no puede resolverlo.
- `zord summon security performance` o `zord summon security,performance` restringe la ejecución a Zords concretos y mantiene las opciones de PR, scope, síntesis, timeout y artefactos.
- `zord assemble --pr 123`, `--pr owner/repo#123` o `--pr https://github.com/owner/repo/pull/123` obtiene el diff con GitHub CLI; la resolución de un número simple usa el repositorio actual.
- `zord assemble --dry-run` muestra Zords y asignaciones sin ejecutar agentes ni avanzar el cursor del router; `--no-synthesis` deja los resultados crudos; `--verbose` transmite stdout/stderr sanitizado.
- `zord assemble --out zord-review --outputs json,md` escribe `zord-review.json` y `zord-review.md` en el directorio actual; `--output-json` imprime JSON de resultados para consumo programático.
- `zord summon io-boundaries cross-repo-validation --extra-diffs /tmp/related.diff` agrega diffs relacionados al input y marca el contexto como multi-repo; la recolección de esos diffs es responsabilidad del usuario mediante `gh pr diff`.
- `zord list` lista Zords efectivos y su procedencia; la precedencia es repo → global → bundled, y el primer nombre repetido gana.
- `zord add mi-checker --repo` crea un scaffold en `.zords/agents/`; sin `--repo` crea uno global, por defecto bajo `~/.config/zords/agents/` o el directorio legacy detectado.
- `zord enable <name>` y `zord disable <name>` cambian `enabled` en Zords repo/global; los bundled no se modifican directamente y deben copiarse a una ubicación editable.
- `zord check <name>` valida presencia del prompt, hooks, modelo, timeout y metadata básica antes de incorporar un Zord al flujo.
- `zord fix --from zord-review.json --items ZORD-SECURITY-001` aplica solo IDs seleccionados; `--severity critical,high` permite seleccionar por severidad y `--dry-run` muestra el agrupamiento sin tocar archivos.

## Entradas y salidas

- **Input primario:** diff de Git recibido por stdin del proceso de agente; en modo PR proviene de `gh pr diff`; en modo multi-repo puede incorporar un archivo adicional con `--extra-diffs`.
- **Configuración:** `.zords/config.json` del repo y `~/.config/zords/config.json` global se fusionan profundamente, con la configuración repo ganando sobre la global; los arrays se reemplazan, no se concatenan.
- **Zord:** prompt Markdown + frontmatter YAML; los Zords bundled viven bajo `zords/agents/` y se empaquetan junto con `lib` mediante `package.json.files`.
- **Salida por revisor:** JSON compatible con `{ reviewer, findings, summary }`; el parser tolera JSON directo, wrappers de proveedor, bloques fenced y texto alrededor del objeto.
- **Salida sintetizada:** `verdict` (`PASS`, `WARNINGS`, `FAIL`), resumen, conteo por severidad, lista deduplicada/ordenada según el prompt de síntesis y reporte Markdown.
- **Artefacto persistido:** incluye timestamp, modo (`branch`, `commit`, `staged` o `pr`), contexto multi-repo, todos los Zords, findings con IDs `ZORD-<REVIEWER>-NNN` y síntesis opcional.
- **Exit code:** normalmente `1` si la síntesis o los resultados crudos contienen findings `critical`/`high`; en `--output-json` el código es `0` aunque existan findings, por lo que el JSON debe ser la autoridad del consumidor automatizado.

## Integraciones

- `claude`: proceso `claude -p` con salida JSON, prompt de sistema en archivo, modo `plan` para revisión y permisos de edición restringidos en fixes.
- `codex`: proceso `codex exec --sandbox read-only --ephemeral` para reviews y `workspace-write` para fixes; el prompt se pasa como argumento y el diff por stdin.
- `gemini`: proceso `gemini` en `plan` para review y `auto_edit` para fixes.
- `copilot`: `gh copilot` sin remoto/export, sin instrucciones custom, sin preguntas interactivas y con shell denegado; ejecuta un preflight cacheado de disponibilidad/autenticación.
- `custom`: provider configurable por comando y argumentos literales, habilitado solo con `ZORD_ENABLE_CUSTOM_AGENTS=true`; el comando se ejecuta sin shell, con placeholders `{promptFile}` y `{model}`.
- `git`: cálculo de diffs locales, detección de rama remota por `origin/HEAD` y fallback `main`/`master`/`develop`.
- `gh`: descarga de diffs de PR y aplicación de la etiqueta `needs human review` cuando el Zord `human-review` devuelve `needs_human_review=true`.
- Hooks Git: el README documenta wiring para `pre-push`, `post-commit` y Husky; el repositorio no instala hooks automáticamente.

## Arquitectura interna

- `src/commands/assemble.ts` orquesta ciclo de vida, selección de Zords, diff, router, ejecución, síntesis, output y exit code.
- `src/core/zordLoader.ts` parsea YAML, aplica precedencia y filtra por trigger/estado/selección; `src/core/config.ts` resuelve config global/repo y el prompt de síntesis.
- `src/core/agentRouter.ts` normaliza providers, descarta configuraciones inválidas, crea un pool ponderado y persiste `execution-router.json` en el estado global para repartir corridas sucesivas.
- `src/core/orchestrator.ts` ejecuta cada Zord en paralelo con `Promise.all`, heartbeat de progreso y callbacks de inicio/fin/error/output.
- `src/core/claude.ts` concentra el boundary de procesos: argv sin shell para providers, timeout con AbortController, decodificación UTF-8, entorno mínimo heredado y resolución uniforme de códigos `124`/`127`.
- `src/core/synthesis.ts` llama al sintetizador Claude con los resultados efectivos y tiene fallback determinista cuando no hay prompt, falla el proceso o el JSON de síntesis no parsea.
- `src/core/outputArtifact.ts` genera reportes reproducibles para revisión humana y para el comando `fix`; `src/commands/fix.ts` valida severidad, IDs y paths antes de pasar contexto mínimo al agente de escritura.
- La paralelización es por Zord, no por archivo ni por finding; un agente lento no bloquea el arranque de los demás, pero el proceso completo espera a todos los Zords para sintetizar.

## Recetas de adopción

| Necesidad | Receta | Resultado |
|---|---|---|
| Feedback rápido local | `zord summon security anti-patterns --scope staged --no-synthesis` | Dos revisiones focalizadas sobre lo staged, sin segunda llamada de síntesis. |
| Gate antes de push | Hook `pre-push` con `zord assemble --trigger pre-push --scope branch --quiet` | Exit `1` ante findings critical/high de los Zords habilitados para ese trigger. |
| Revisión profunda manual | `zord assemble --scope branch --out review --outputs json,md` | Reporte humano y artefacto estructurado para auditoría/fixes. |
| PR externo | `zord assemble --pr owner/repo#123 --verbose` | Diff descargado por `gh`, progreso y output de proveedores sanitizado. |
| Contratos entre repos | `gh pr diff owner/backend#89 > /tmp/backend.diff` + `--extra-diffs /tmp/backend.diff` | Contexto adicional para `io-boundaries`/`cross-repo-validation`; coordinación manual. |
| Reparación controlada | `zord fix --from review.json --items ZORD-SECURITY-001 --dry-run` y luego sin `--dry-run` | Preview del agente y posterior modificación selectiva del workspace. |

### Reviewer personal RIO

- `rjara-rio-impact` vive en `~/.config/zords/agents/rjara-rio-impact.md`; es una extensión personal, manual y `enabled: false`, por lo que no entra en revisiones normales ni hooks.
- Su único consumidor previsto es [[signals-code-review]] en cambios Meli de Signals/RIO, mediante `--include rjara-rio-impact`. La skill no aplica y no invoca Zord en proyectos no Meli.
- El revisor recibe el diff y diffs relacionados como evidencia, pero ningún brief, prioridad, sospecha o finding del coordinador. Investiga por separado contratos y afectaciones cross-app usando código owner, [[ads-signals-knowledge-library]] y RIO Atlas.
- Antes de cada uso, `zord list` debe mostrar source efectivo `global`; una definición `.zords/agents/rjara-rio-impact.md` dentro del repo tiene precedencia y obliga a bloquear la revisión hasta resolver el shadowing.
- La salida es JSON conciso en español y limita los findings a riesgos transversales materiales o gaps de tests sobre comportamientos críticos; la reconciliación y publicación continúan bajo el gate humano de la skill.

Configuración mínima útil para repartir providers sin tocar prompts: `{"execution":{"strategy":"weighted_round_robin","show_assignments":true,"agents":[{"name":"codex","provider":"codex","weight":2,"enabled":true},{"name":"claude","provider":"claude","weight":1,"enabled":true}]}}`.

Para el vault, lo más reutilizable del diseño es la frontera `prompt/config → ejecución aislada → artefacto estructurado → acción humana`: permite separar checks deterministas, análisis probabilístico y escritura, manteniendo una evidencia durable por commit o PR.

## Reglas de uso

- Para un primer uso, ejecutar `zord assemble --dry-run`, revisar el diff detectado y confirmar los agentes asignados antes de gastar presupuesto.
- En hooks bloqueantes conviene usar solo los Zords de mayor señal (`security`, `anti-patterns`, `io-boundaries`, `human-review`) y dejar performance/idiomacy/simplification para ejecución manual.
- El diff y los findings son input no confiable; mantener prompts que separen instrucciones del contexto analizado y no permitir que un finding controle rutas, comandos o agentes.
- No configurar secretos directamente en `.zords/config.json`; los providers usan un allowlist de entorno y los mapeos declarados por nombre rechazan nombres sensibles/protegidos.
- Revisar `git diff` después de `zord fix`: el comando permite escribir dentro del workspace, no crea commit, no hace push y no ejecuta una verificación automática de tests o compilación.
- No asumir que `cross_repo.enabled`, `ask_on_every_run` o `fetch_timeout` implementan coordinación automática: en `master` son campos del schema/config por defecto, pero el flujo operativo real usa `--extra-diffs` explícito.
- Distinguir la documentación de `master` de la rama remota `feature/script-agents`: los Zords deterministas son una evolución alpha/no integrada al checkout documentado aquí.

## Links

- [[local-agents-pipeline-cli-source]] — provenance del checkout local y del remoto.
- [[AGENTS OS]] — proyecto del vault al que aporta el patrón de revisión compuesta.
- [[30-resources/tools/00-index|Tools — Índice]] — catálogo curado de herramientas.
- [[2026-08-26-local-agents-pipeline-cli-review-gate]] — idea implementable derivada de esta investigación.
