---
type: application
status: active
area: "[[Meli]]"
lang: Go
github: https://github.com/melisource/fury_vis-items-loader-tagging
path: ~/fuentes/vis-items-loader-tagging
aliases:
  - vis-items-loader-tagging
  - fury_vis-items-loader-tagging
  - loader tagging
tags:
  - area/meli
  - kind/application
created: 2026-06-24
updated: 2026-07-25
---

# vis-items-loader-tagging

> [!info]+ vis-items-loader-tagging
> **Lenguaje:** Go · **Área:** [[Meli]]
> **GitHub:** [melisource/fury_vis-items-loader-tagging](https://github.com/melisource/fury_vis-items-loader-tagging) · **Path local:** `~/fuentes/vis-items-loader-tagging`

## 📝 Descripción

- Productor de señales/tags de pricing para items Motors: `PREVIOUS_PRICE` (Bajó de Precio) y el futuro proceso de Destaques (`price_destaque_motors`). Maneja consumers, filtros de confianza y reproceso.
- El backfill retroactivo de Bajó de Precio Motors ingresa por `POST /price-drop-motors-backfill`, procesa cada ítem en `POST /consume-price-drop-motors-backfill` y agenda el apagado en el calendario productivo existente (`BIGQUEUE_TOPIC_PRICEDROP_BADGE_EXPIRE_TOPIC_NAME` → `/consume-price-drop-calendar-cleanup`).

## 🔧 Datos útiles

- **Repo:** `melisource/fury_vis-items-loader-tagging`
- **Path local:** `~/fuentes/vis-items-loader-tagging`
- **Stack / notas:** Go. Procesos: `price_before_discount_motors`, handlers/consumers.
- **Backfill Bajó de Precio Motors:** único tópico nuevo de trabajo nonprod `BIGQUEUE_TOPIC_PRICE_DROP_MOTORS_BACKFILL__NONPROD_TOPIC_NAME`, publicado con segmento BigQueue `nonprod`; no tiene tópico ni consumer de expiración propios.

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes vis-items-loader-tagging
short mode
hide task count
```

## 🔗 Links

- [Repo GitHub](https://github.com/melisource/fury_vis-items-loader-tagging)
