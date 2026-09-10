---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-09-09
---

# 🧠 AGENTS OS y estructura del vault

## Propósito

Guía de la estructura del vault y de los recursos de instalación de AGENTS OS.

## Contenido


¡Arrr, marinero! Bienvenido a bordo del **Second Brain** local-first de la nave. Este no es un depósito desordenado de retazos de código; es un puerto de conocimiento estructurado bajo una arquitectura híbrida inspirada en la metodología PARA y gobernada por **AGENTS OS**, optimizado para que tanto humanos como agentes de inteligencia artificial naveguen sin encallar.

Este puerto se rige por un modelo cognitivo de doble capa, separando el pensamiento interno de la tripulación cibernética del inventario real de la nave.

---

## 🚀 Entrada para agentes e instalación

- [Prompt maestro de instalación](installation/INSTALL-PROMPT.md): cambia solo la ruta
  absoluta del vault y entrégalo a un agente.
- [Reglas Codex](../../AGENTS.md) y [reglas Claude](../../CLAUDE.md): entrypoints
  repo-scoped generados desde una fuente administrada.
- [Guía operativa](../../80-agents/agents-os/agents-os.md) y
  [constitución](../../80-agents/agents-os/agent-constitution.md): fuentes
  canónicas que bootstrap y routing cargan una vez por sesión o según la
  entidad activa.
- `agents-os-hygiene-cycle`: mantenimiento periódico que regulariza notas,
  procesa feedbacks, registra cambios compartibles y reindexa Graphify.

El perfil personal, la memoria interna y las sesiones no forman parte de la
distribución compartible. Las mejoras agnósticas se trazan con
`share_scope: team`; los ajustes personales usan `share_scope: local`.

---

## 📦 Core compartible

El vault genera un core standalone de AGENTS OS: reglas, contratos ejecutables,
skills, templates y un perfil estándar, sin el contenido de nadie.

- [Guía del build](core-export/README.md)
- Selección: [`core-export/sources.list`](core-export/sources.list)
- Archivos que la distribución escribe: `core-export/dist-files/`

Regenerar desde la raíz del vault:

```bash
python3 30-resources/agents-os/core-export/build-core.py
```

El destino por defecto es la carpeta `agents-os/` hermana de `VAULT_ROOT`. Cada
copia se verifica por SHA-256 y el build aborta si material privado alcanza la
salida.

---

## 🤖 AGENTS OS para ChatGPT

El vault genera un pack portable para iterar AGENTS OS en un Proyecto de
ChatGPT sin copiar memoria interna, sesiones ni outputs derivados.

- [Guía del pack](chatgpt-pack/README.md)
- [Estado ejecutivo](chatgpt-pack/PROJECT-STATE.md)
- [Prompt de iteración](chatgpt-pack/ITERATION-PROMPT.md)
- [ZIP portable](distribution/agents-os-chatgpt.zip)

Regenerar desde la raíz del vault:

```bash
bash "30-resources/agents-os/chatgpt-pack/build-pack.sh"
```

El ZIP se ensambla en un directorio temporal, verifica sus copias mediante
SHA-256 y conserva el `MANIFEST.md` dentro del archivo. No se deja una carpeta
duplicada para que Obsidian no la indexe ni la sincronice.

---

## ⚖️ El Modelo de Doble Sistema (Kahneman-style)

Para que el caos no reine en este vault, dividimos el conocimiento en dos sistemas distintos, inspirados en la teoría de Daniel Kahneman:

### ⚡ Sistema 1: El Cerebro del Agente (Memoria Rápida y Heurísticas)
*   **Qué es**: El pensamiento interno, las lecciones aprendidas, las decisiones operativas de los agentes (ADRs), los errores conocidos que evitan que tropecemos dos veces con la misma piedra, los diarios de a bordo (journals), runbooks de emergencia y logs de sesión.
*   **Dónde vive**: Exclusivamente bajo el directorio [📁 `80-agents/`](../../80-agents).
*   **Acceso**: La memoria interna es el espacio privado del agente para comunicarse con futuras IAs que aborden tareas en la nave. Los logs y feedbacks son la bitácora pública de auditoría.

### 🏛️ Sistema 2: Las Entidades Reales (Representación Canónica de la Nave)
*   **Qué es**: La realidad objetiva y estructurada de vuestros proyectos, áreas de responsabilidad, aplicaciones reales, integraciones y recursos tecnológicos. No hay espacio para hipótesis efímeras aquí; sólo hechos y documentación de producción.
*   **Dónde vive**: En las carpetas PARA ([📁 `10-projects`](../../10-projects), [📁 `20-areas`](../../20-areas), [📁 `30-resources`](../../30-resources)).
*   **Regla de Oro**: Todo documento de Sistema 2 **DEBE** crearse a partir de las plantillas oficiales ubicadas en [📁 `70-templates/`](../../70-templates/). Si no existe plantilla para la entidad que se requiere crear, el agente debe diseñar la plantilla primero.

---

## 📂 Mapa y Topografía del Vault

El vault está organizado en las siguientes divisiones principales dentro de `main/`:

| Carpeta | Propósito (Metodología PARA + OS) | Sistema | Operación Recomendada |
| :--- | :--- | :--- | :--- |
| [📁 `00-inbox`](../../00-inbox) | **Inbox / Captura Rápida**: Ideas sueltas, tareas del día a clasificar y la portada de inicio ([Home.md](../../00-inbox/Home.md)). | Tránsito | Escritura libre y procesamiento diario. |
| [📁 `10-projects`](../../10-projects) | **Proyectos Activos**: Notas de proyectos específicos con plazos y metas claras. | Sistema 2 | Lectura y actualización activa según tareas. |
| [📁 `20-areas`](../../20-areas) | **Áreas de Responsabilidad**: Mantenimiento continuo sin plazos fijos. | Sistema 2 | Consulta de guías y estándares de calidad. |
| [📁 `30-resources`](../../30-resources) | **Recursos y Referencias**: Biblioteca técnica y distribuciones reutilizables. | Sistema 2 | Consulta de referencia. |
| [📁 `40-archive`](../../40-archive) | **Archivo**: Referencias históricas y drafts inactivos que no guían la operación actual. | Sistema 2 | Consulta de auditoría excepcional. |
| [📁 `70-templates`](../../70-templates) | **Plantillas Sistema 2**: Formatos estandarizados para entidades y documentos canónicos. | Sistema 2 | Moldes obligatorios de creación de notas. |
| [📁 `80-agents`](../../80-agents) | **Gobernanza de Agentes**: La guía de vuelo, habilidades y journal operativo del agente. | Sistema 1 | Bitácora, memoria e instrucciones para IAs. |
| [📁 `90-system`](../../90-system) | **Configuración del Sistema**: Convenciones, sincronización y backend del vault. | Invariante | Metadatos y configuración. |

---

## 🛠️ Leyes de Hierro para Agentes AI

Si sois una inteligencia artificial operando en este vault, cumplid estas directivas bajo pena de ser arrojada a los tiburones:

> [!IMPORTANT]
> **1. Carga Obligatoria de Contexto**
> Al iniciar una sesión, bootstrap carga la base operativa una sola vez; en turnos posteriores se reutiliza y sólo se recupera el delta de la entidad activa.
> 
> **2. Prohibición de Basura en la Raíz**
> NUNCA creéis archivos sueltos en el directorio raíz del vault. Si no sabéis dónde va una nota, enviadla a `00-inbox/` y notificad al capitán.
> 
> **3. Naming Canónico Estricto**
> Los links bidireccionales `[[Nombre Nota]]` deben apuntar siempre al nombre exacto de la nota canónica (ej: `[[Meli]]`, no `[[meli]]`). Los nombres alternativos van en la propiedad `aliases` de los frontmatters; los slugs técnicos van en los tags o en el campo `slug`.
> 
> **4. Uso del Índice de Graphify**
> Para explorar relaciones y buscar información, usad prioritariamente `graphify-obsidian query` para no desperdiciar el presupuesto de tokens en búsquedas manuales o listados masivos.
>
> **5. Cero Metadatos de Chat en el Vault**
> Queda estrictamente prohibido incluir bloques de `ArtifactMetadata` en las llamadas de edición de archivos de vuestro espacio de trabajo.

---

## 🔍 Integración con Graphify

Graphify es un índice derivado local a cada máquina:
*   `graphify-obsidian` indexa el vault en una copia temporal y mantiene su
    índice fuera de Obsidian (`graphify-obsidian cache-path`).
*   Las queries comprueban freshness y refrescan automáticamente cuando cambia
    el corpus; los agentes no necesitan ejecutar `update` antes.
*   `graphify-personal` deja sus resultados en cada repositorio local y nunca
    exporta reportes al vault.
*   Cualquier `95-graphify/` o `graphify-out/` dentro del vault está prohibido,
    ignorados por Obsidian y excluidos de LiveSync.

*Markdown es la fuente de verdad. Graphify es el timón que nos ayuda a navegarla.*
