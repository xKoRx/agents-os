---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[AGENTS OS]]"
related: []
aliases:
  - core export
  - export del core compartible
tags:
  - kind/doc
  - tech/agents-os
created: 2026-09-09
updated: 2026-09-09
---

# Core export — build del AGENTS OS compartible

## Propósito

Ensamblar el core compartible de AGENTS OS desde las fuentes canónicas del vault, con verificación SHA-256 y sin filtrar material personal.

## Contenido

### Regenerar

Desde cualquier parte:

```bash
python3 30-resources/agents-os/core-export/build-core.py
```

El destino por defecto es la carpeta `agents-os/` hermana de `VAULT_ROOT`. Acepta un destino explícito como primer argumento. El script resuelve `VAULT_ROOT` desde su propia ubicación: no persiste ninguna ruta absoluta de máquina.

### Piezas

| Archivo | Rol |
|---|---|
| `sources.list` | Qué se copia verbatim desde el vault, por categoría. Modos `file`, `tree`, `globtree` |
| `dist-files/` | Lo que la distribución **escribe**, no copia: README, entrypoints de superficie, prompt de instalación, perfil estándar, área por defecto, proyecto de instalación, registro de superficies vacío, catálogo de aplicaciones vacío, semilla de continuidad global, `.gitignore` y `.graphifyignore` |
| `build-core.py` | Ensamblado, verificación de hashes, scaffolding vacío, filtrado del índice de skills y `MANIFEST.md` |

### Garantías del build

- Cada copia se compara por SHA-256 contra su fuente; una diferencia aborta el build.
- La memoria interna y el contenido del journal están prohibidos por prefijo, con una única excepción declarada: la semilla autorizada de continuidad global que viaja desde `dist-files/`.
- El índice de skills se filtra a lo que realmente viajó, porque un índice que lista skills ausentes hace fallar a `agents-os-doctor`.
- El destino se limpia antes de escribir, preservando `.git/` y `.obsidian/`. Se niega a limpiar un directorio con contenido que no tenga el marker `AGENTS.md`, y se niega a construir dentro del vault de origen.

### Verificación posterior

Corrida sobre el destino, tras el build del 2026-09-09: `doctor` `HIGH=0 MEDIUM=0 LOW=0` con startup ≈4466 tokens, `lint --check` `0 ERROR / 0 WARN` sobre 88 notas, contrato de schema `0 errores`, y cero apariciones de identidad del owner o de rutas absolutas de máquina.

## Relaciones

- `30-resources/agents-os/README.md` — guía de los recursos de instalación y distribución.
- `30-resources/agents-os/chatgpt-pack/` — el otro pack derivado, para iterar el sistema en un proyecto de ChatGPT.
