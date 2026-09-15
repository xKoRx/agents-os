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
updated: 2026-09-14
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
| `sources.list` | Qué se copia verbatim desde el vault, por categoría. Modos inclusivos `file`, `tree`, `globtree`; `exclude` retira un archivo scoped capturado por un árbol y falla si ese archivo deja de estar seleccionado |
| `dist-files/` | Lo que la distribución **escribe**, no copia: README, entrypoints de superficie, prompt de instalación, perfil estándar, área por defecto, proyecto de instalación, registro de superficies vacío, catálogo de aplicaciones vacío, semilla de continuidad global, `.gitignore` y `.graphifyignore` |

Las skills portables conservan su autoridad en `30-resources/agents/skills/`.
El builder proyecta sus filas en el `INDEX.md` distribuido y entrega un
`domain-router-registry.md` vacío: cada instalación registra sus dominios sin
modificar el core compartido.
| `build-core.py` | Ensamblado, verificación de hashes, scaffolding vacío, filtrado del índice de skills, validación semántica del artefacto, prueba de instalación DEFAULT y `MANIFEST.md` |

### Garantías del build

- Cada copia se compara por SHA-256 contra su fuente; una diferencia aborta el build.
- Cada exclusión debe resolver a un archivo incluido por otra regla. Así una
  refactorización de `sources.list` no convierte una exclusión scoped en deuda
  silenciosa.
- La memoria interna y el contenido del journal están prohibidos por prefijo, con una única excepción declarada: la semilla autorizada de continuidad global que viaja desde `dist-files/`.
- El índice de skills se filtra a lo que realmente viajó, porque un índice que lista skills ausentes hace fallar a `agents-os-doctor`.
- El artefacto completo se audita donde los literales de dominio tienen efecto: cuerpo de startup y templates, frontmatter de toda nota y resolución de cada `area` contra `20-areas/`. Los fixtures intencionalmente inválidos viven en un allowlist exacto dentro del builder; no existen exclusiones por patrón.
- El builder clona el resultado a un vault temporal DEFAULT y usa el
  materializador distribuido para crear una entidad de cada tipo canónico. Luego
  vuelve a auditar frontmatter y cuerpo renderizado, de modo que no basta con que
  el texto del template parezca portable: el resultado también debe serlo.
- El destino se limpia antes de escribir, preservando `.git/` y `.obsidian/`. Se niega a limpiar un directorio con contenido que no tenga el marker `AGENTS.md`, y se niega a construir dentro del vault de origen.
- El runtime del Doctor unificado y sus tres providers externos viaja en el artefacto. El registro de dominios vacío es un estado soportado: los escenarios scoped quedan SKIP y el baseline reporta sólo DEFAULT, sin requerir paquetes Meli/Aranea.

### Verificación posterior

Corrida sobre un destino limpio del 2026-09-14: build validado con 196 archivos canónicos, 37 skills, 7 exclusiones scoped y 44 tipos materializados. El Doctor unificado ejecutó los cuatro componentes con `execution_status: OK`; Context midió sólo DEFAULT y produjo `scope_pack: {}`. Los `FAIL/WARN/SKIP` del artefacto se preservan como findings, no como errores de ejecución.

## Relaciones

- `30-resources/agents-os/README.md` — guía de los recursos de instalación y distribución.
- `30-resources/agents-os/chatgpt-pack/` — el otro pack derivado, para iterar el sistema en un proyecto de ChatGPT.
