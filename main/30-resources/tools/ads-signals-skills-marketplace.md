---
type: tool
schema_version: 1
status: active
scope: tool
area: "[[Meli]]"
project: "[[Zords — Human-First Technical Authoring]]"
source_url: https://github.com/melisource/fury_ads-signals-skills-marketplace
command:
  - node scripts/validate-marketplace.mjs
entities:
  - "[[ads-signals-skills-marketplace]]"
related:
  - "[[ads-signals-skills-marketplace-source]]"
  - "[[Zords — Human-First Technical Authoring]]"
aliases:
  - "ads-signals-skills-marketplace"
load_policy: when_tool_loaded
indexable: true
index_priority: high
tags:
  - kind/tool
  - scope/tool
  - priority/high
created: "2026-09-01"
updated: "2026-09-01"
---

# ads-signals-skills-marketplace

> [!info]+ ads-signals-skills-marketplace
> **Tipo:** tool · **Estado:** active

## Descripcion

- `ads-signals-skills-marketplace` es el repositorio interno que publica skills portables para asistentes compatibles con `SKILL.md`; su catálogo es consumible por Claude y Codex y mantiene cada capacidad en `skills/<slug>/`.
- El contrato de publicación separa instrucciones, metadata y recursos opcionales: cada `SKILL.md` declara nombre, descripción, versión SemVer, compatibilidad, permisos y runtime; `catalog/skills.json` repite esa metadata como índice público.
- El marketplace no convierte una skill en código confiable por estar catalogada: exige declarar efectos, revisar scripts y evitar secretos, enlaces simbólicos, rutas externas y artefactos generados.

## Uso principal

- Descubrir una skill y sus requisitos desde `catalog/skills.json` antes de instalarla con el mecanismo del cliente.
- Compartir una misma instrucción portable entre Claude y Codex sin duplicar su núcleo ni depender de paths, credenciales o estado local del autor.
- Publicar y versionar capacidades de equipo con una revisión explícita de permisos, runtime, seguridad y compatibilidad.

## Operaciones / comandos

- `node scripts/validate-marketplace.mjs` valida el repositorio completo sin dependencias externas: catálogo, SemVer, slugs, paths internos, frontmatter, metadata alineada, archivos sensibles, symlinks y patrones comunes de secretos.
- Para publicar una skill, crear `skills/<slug>/SKILL.md`, agregar o actualizar su entrada en `catalog/skills.json`, mantener ambos contratos idénticos y ejecutar el validador.
- La instalación es responsabilidad del cliente: Codex usa su directorio configurado de skills y Claude incorpora la carpeta con el mecanismo habilitado por su entorno.

## Entradas y salidas

- **Input:** carpetas de skill con `SKILL.md` y recursos opcionales, más el catálogo JSON versionado.
- **Output:** un repositorio portable y validado que los clientes pueden inspeccionar e instalar; el marketplace no ejecuta automáticamente el contenido publicado.

## Integraciones

- **Claude y Codex:** plataformas admitidas por el catálogo; una skill puede soportar una o ambas y debe documentar cualquier adaptación específica.
- **GitHub:** repositorio y pull requests como superficie de revisión y distribución del contenido.
- **Node.js 20+:** runtime requerido únicamente por el validador del marketplace; cada skill declara su propio runtime por separado.

## Reglas de uso

- Tratar `SKILL.md` como instrucciones ejecutables desde el punto de vista del agente: revisar permisos, scripts, variables de entorno y conectores antes de instalar.
- No publicar tokens, llaves, datos personales, paths locales ni estado implícito; una skill debe poder entenderse desde su propia carpeta.
- La versión, compatibilidad, permisos y runtime deben coincidir exactamente entre el frontmatter y el catálogo.
- No asumir que estar en el catálogo equivale a autorización para ejecutar scripts o acceder a servicios externos.

## Links

- [[ads-signals-skills-marketplace-source]] — provenance del repo y del checkout verificado.
- [[Zords — Human-First Technical Authoring]] — proyecto que llevó `human-first-technical-writing` a esta superficie de distribución.
- `80-agents/skills/human-first-technical-writing/SKILL.md` — skill canónica del vault.
- [[30-resources/tools/00-index|Tools — Índice]] — catálogo curado del dominio.
