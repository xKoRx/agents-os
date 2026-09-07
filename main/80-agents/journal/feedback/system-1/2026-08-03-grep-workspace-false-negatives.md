---
type: feedback
scope: tool
created: "2026-08-03"
updated: "2026-08-03"
kind: friction
confidence: medium
tags:
  - kind/feedback
  - scope/tool
  - tool/grep
source_session: "2026-08-03-echo-forge-robust-run-audit-deploy-0-2-31"
load_policy: manual
---

# Fricción: Grep del workspace devolvía `No matches found` en paths que sí contenían los patrones

## Síntoma

Durante la auditoría del plugin `EchoForgeRobustRunExporter.java`, las
siguientes invocaciones de la herramienta Grep del workspace devolvieron
`No matches found` con `path` acotado al repo:

- `pattern: setParameters(, path: /Users/rjara/go/src/github.com/xKoRx/symphony`
- `pattern: [diag], path: ...sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeRobustRunExporter.java`
- `pattern: System\.out\.println, path: ...sqx/exporter-plugin/src/SQ/CustomAnalysis/...`

Sin embargo:

- `wc -l` y `grep -c` desde shell sobre los mismos archivos sí encontraban
  los matches esperados (381 líneas, 20 `[diag]`, 20 `System.out.println`).
- `rg` (ripgrep) directo desde shell también funcionaba.

## Workaround aplicado

Bypass completo de la herramienta Grep: usar `Shell` con `rg` (`rg -n ...`)
o con `grep -c ...` para cualquier búsqueda dentro del repo Symphony.
Solo se volvió a usar Grep cuando el path target era claramente externo al
workspace (p.ej. `/Users/rjara/.cursor/...`).

## Hipótesis

- Probable problema de indexación / caché del wrapper Grep del workspace
  para rutas muy profundas dentro de `symphony/` o para archivos `.java`
  dentro de subdirs `src/SQ/CustomAnalysis/` (10+ niveles de profundidad).
- El wrapper podría estar respetando un `.gitignore` efectivo o un
  `.rgignore` no documentado, mientras `rg` directo usa los defaults.
- También podría ser que el wrapper use un patrón de `git ls-files` que
  excluya `untracked` files, y como `sqx/exporter-plugin/src/SQ/CustomAnalysis/`
  tiene archivos modificados, los filtra.

## Recomendación

1. **Inmediato**: cuando Grep workspace devuelva `No matches found` para un
   archivo que se sabe contiene el patrón, hacer fallback a `Shell rg`
   antes de concluir que el archivo está limpio.
2. **Estructural**: si esto se reproduce, abrir issue al mantenedor del
   wrapper Grep con: (a) patrón exacto probado, (b) salida de `rg` desde
   shell como contra-evidencia, (c) hash del archivo.

## Pain Pattern Candidate

> **"Grep workspace = silent miss for deep .java paths"** — falso
> negativo silencioso en búsquedas sobre archivos Java bajo
> `*/src/SQ/*/*/*/` con archivos modificados no commiteados.

Frecuencia: 1 sesión / 1 sesión (N=1, no significativo todavía). Esperar a
reproducción para promover a error canónico.