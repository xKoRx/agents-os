---
type: index
icon: 🗂️
tags:
  - index
  - kind/index
created: 2026-06-23
updated: 2026-06-27
aliases:
  - areas
  - Areas
  - Mis Areas
  - Mis Áreas
  - area-index
---

# 🗂️ Mis Áreas

> [!tip] Las áreas son los **ámbitos permanentes de tu vida** (no tienen fecha de fin, a diferencia de los proyectos). Cada una mantiene un estándar que querés sostener en el tiempo.

## Acceso rápido

- [[Meli|💼 Meli]] — trabajo, VIS, arquitectura y equipo
- [[Trading|📈 Trading]] — operativa, prop firms, journal y riesgo
- [[Echo|⚙️ Echo]] — trading algorítmico, Forge, Core y pipelines
- [[Finanzas|💰 Finanzas]] — patrimonio, gastos, inversiones y cuentas
- [[Aranea|🕸️ Aranea]] — infra, red, servicios y automatización
- [[Casa & Energía|🏠 Casa & Energía]] — domótica, solar, baterías y consumo
- [[Maker Lab|🧪 Maker Lab]] — prototipos, sensores, cultivo y hardware
- [[Personal|🌱 Personal]] — vida personal, administración y decisiones
- [[Familia|👨‍👩‍👧 Familia]] — momentos, colegio, planes y recuerdos
- [[Salud y Ejercicio|🏋️ Salud y Ejercicio]] — entrenamiento, hábitos y bienestar
- [[Aprendizaje|🎓 Aprendizaje]] — cursos, libros, skills y research

## Galería (vista Base)

Esta galería se llena sola con toda nota `type: area`. Clic en una tarjeta para abrir el área.

```base
filters:
  and:
    - 'type == "area"'
    - '!file.inFolder("70-templates")'
properties:
  note.status:
    displayName: Estado
  note.desc:
    displayName: ""
views:
  - type: cards
    name: Áreas
    image: note.banner
    imageFit: cover
    imageAspectRatio: 0.5
    cardSize: 300
    order:
      - note.desc
      - note.status
```

## Cómo usar esto

- **Crear un área:** nota nueva en `20-areas/` con la plantilla `70-templates/area.md`. El nombre del archivo es el link canónico, `slug:` es el identificador técnico y el tag debe ser `#area/<slug>`. Aparece sola acá arriba.
- **Relacionar un proyecto/recurso con un área:** pone `area: "[[Meli]]"` en su frontmatter. El campo usa link canónico, no slug.
- **Tareas por área:** escribí `- [ ] tu tarea #area/meli`. La query de la nota las recoge sola.
- **Aliases:** variantes como `meli`, `MELI`, `areas` o nombres históricos van en `aliases`; no crees links alternativos como `[[meli]]`.
- **Revisión:** todas las áreas tienen `review: weekly` para tu repaso PARA semanal.
