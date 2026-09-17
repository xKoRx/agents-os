# Runbook — Escribir specs funcionales en Signals (Spellbook / SIG)

Guía para humanos del equipo Signals/Ads. Su contraparte para agentes es la skill
`signals-func-spec-authoring` (misma carpeta): el `SKILL.md` es la versión imperativa
que un agente ejecuta; este runbook es el "por qué" y el onboarding.

> **Principio rector:** este documento **no copia templates**. Los templates de
> verdad son los specs reales en Spellbook, que están vivos y siempre al día. Aquí
> aprendes *cómo pensar* un spec y *a qué ejemplo real acudir*; el molde lo sacas
> del spec canónico con `spellbook specs view <id>`.

---

## 1. El punto de entrada: la CLI, no el navegador

Lo primero que hay que interiorizar —y lo que más tiempo hace perder si no se
sabe—: **no se entra por el navegador.** `spellbook.adminml.com` está detrás del
SSO de MercadoLibre (`auth-meli.adminml.com`); las herramientas de browser de un
agente chocan ahí y no pueden loguearse. La web es para personas.

La puerta es la **Spellbook CLI**, autenticada por token
(`spellbook login <token>` — ver `/spellbook.auth`). Comandos base:

```bash
spellbook specs list SIG          # listar (arg POSICIONAL: no existe --project)
spellbook specs view <specId>     # leer (el markdown viene en el campo .content)
spellbook specs create SIG --title "…" --type functional   # crear (devuelve UUID)
spellbook specs summary SIG       # panorama por estado/tipo
spellbook search "<query>"        # buscar
```

La salida es JSON por defecto (pensada para agentes); agrega `--human` cuando lo
vayas a leer tú. Para índice rápido de lo funcional en curso, hay un one-liner en
el `SKILL.md` (§0).

## 2. Cómo se divide el trabajo con lo que ya existe

Ya hay un ecosistema `/spellbook.*` para la **mecánica**: `start-spec`, `plan`,
`finish-spec`, `sync`, `auth`, `cli`, `.spellbookrc`. **No los reemplaces.** Esta
skill/runbook cubre lo que ellos no: **el contenido y las convenciones de un buen
spec funcional de Signals.**

## 3. Elegir la forma antes de escribir

No fuerces todo al mismo molde. La forma sale del trabajo:

- **Epic** — toca 3+ apps o tiene fases de rollout. Dueño del big picture, del
  desglose por app, del plan por fases y de las decisiones abiertas. Tiene specs
  hijas (una por app). Ejemplo vivo: **SIG-492**.
- **Spec de feature** — una feature acotada a 1–2 apps (un endpoint nuevo, un
  comportamiento nuevo). Ejemplo: **SIG-462**.
- **Spec chica / fix** — un arreglo puntual o cambio de contrato, con tabla
  `RF-N`. Ejemplos: **SIG-543**, **SIG-541**.
- **Epic de bug** — un incidente de producción que merece registro de root cause.
  Ejemplo: **SIG-547**.

El catálogo completo *patrón → spec real* está en
[`references/canonical-specs.md`](references/canonical-specs.md). **Abre el
ejemplo que más se parezca y léelo entero antes de escribir** — de ahí sacas la
estructura y la profundidad esperadas.

## 4. Las convenciones que hacen que "se vea como del equipo"

Detalle completo en [`references/conventions.md`](references/conventions.md). En
una línea cada una:

- **Idioma:** epics en español; specs de feature en inglés o español pero
  consistentes; nombres de apps/endpoints/métricas siempre en inglés.
- **Identificadores:** `US-N`, `BR-N`, `E2E-N` (con `🔴` para lo crítico),
  `RF-N`, `CA-N`, `SEC-N`, `E-N`. Escenarios en Given/When/Then.
- **Métricas:** `advertising.signals.{componente}.{nombre}{tag:valor}`.
  Distingue motivos de fallo por tag (`unconfigured` vs `resolved_null` vs
  `invalid_expression`). Nunca metas valores de payload ni IDs de alta
  cardinalidad en métricas.
- **Disciplina de alcance:** *Fuera de alcance* es obligatorio. Separa
  **Decisiones cerradas** (ya zanjadas) de **Gaps pendientes** (por decidir). Un
  gap no documentado es una sorpresa en el sprint.
- **Linking:** `SIG-N` en prosa + URL completa en Referencias/Specs hijas; enlaza
  Grid cuando ahí vive el detalle de escenarios.

## 5. El flujo, de principio a fin

1. `spellbook specs list SIG` → mira qué hay, evita duplicar.
2. Lee el spec canónico que corresponde (`canonical-specs.md` → `view`).
3. `spellbook specs create SIG --title "…" --type functional` (guarda el UUID).
   Si es epic: crea el padre y luego `children add` por cada app.
4. Redacta el cuerpo en Markdown siguiendo el esqueleto de secciones (SKILL.md §3)
   y las convenciones. Las personas suelen pegar el cuerpo en el editor web de
   Spellbook (con preview); un agente edita por CLI.
5. Pasa el **checklist pre-review** (SKILL.md §6).
6. `spellbook specs take <id>` y muévelo a `review` para el equipo.

## 6. Errores típicos que este runbook previene

Cosas que, sin esto, cada agente (y cada persona nueva) vuelve a sufrir:

- Perder tiempo intentando abrir la web y quedar atrapado en el SSO.
- Inventar `--project` en `specs list` (es posicional: `specs list SIG`).
- Escribir un spec sin sección *Fuera de alcance* → scope creep en review.
- Meter valores de payload en métricas → problema de privacidad y cardinalidad.
- Copiar un template viejo que ya no refleja cómo escribe hoy el equipo, en vez de
  leer el spec canónico vivo.
- Mezclar "decisiones cerradas" con "gaps", y que en el sprint aparezca una
  decisión que nadie tomó.

---

## Mantención

Este runbook y la skill se mantienen **re-listando, no copiando**. Si el estilo
del equipo evoluciona, el spec de mejor calidad de cada tipo pasa a ser el nuevo
referente: actualiza los IDs en `references/canonical-specs.md` en vez de reescribir
prosa. Así la documentación no se pudre.

*Base: SIG-462, SIG-492, SIG-518, SIG-527, SIG-541, SIG-543, SIG-547, SIG-551
(revisados 2026-08-12).*
