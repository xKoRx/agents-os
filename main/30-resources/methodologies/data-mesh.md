---
type: methodology
schema_version: 1
status: active
area: "[[Meli]]"
slug: data-mesh
aliases:
  - data mesh
  - data monolith to mesh
  - malla de datos
tags:
  - kind/methodology
  - area/meli
  - topic/data
source: https://martinfowler.com/articles/data-monolith-to-mesh.html
sources:
  - https://martinfowler.com/articles/data-monolith-to-mesh.html
author: Zhamak Dehghani
created: 2026-08-10
updated: 2026-08-10
---

# Data Mesh

> [!info]+ Data Mesh
> **Fuente:** "How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh" — Zhamak Dehghani (martinfowler.com)
> **Por qué importa acá:** es el modelo mental que el equipo **Signals** aplica en la plataforma [[RIO]]. Lo compartieron como lectura de onboarding.

## Propósito

Ofrecer un marco para diseñar plataformas de datos self-serve con ownership distribuido y governance federada.

## Problema: los 3 modos de falla del data lake/warehouse centralizado

1. **Centralizado y monolítico** — una sola plataforma ingesta, limpia y sirve datos de todos los dominios. Se convierte en cuello de botella; no escala ni organizacional ni técnicamente al crecer fuentes y consumidores.
2. **Descomposición acoplada del pipeline** — se descompone por función técnica (ingesta → limpieza → agregación → serving) en vez de por dominio de negocio. Cualquier feature nueva toca todo el pipeline: dependencias y entrega lenta.
3. **Ownership hiper-especializado y en silo** — los data engineers quedan aislados de los dominios fuente y consumidor, sin contexto de negocio. Se vuelven gatekeepers que gestionan demandas que no entienden.

## Cambio de paradigma

De un modelo **"push & ingest"** centralizado a uno **"serve & pull"** distribuido: cada dominio **posee y sirve sus datos como producto**, habilitado por una **infraestructura self-serve compartida**, bajo **governance federada**.

## Los 4 principios

1. **Ownership de datos descentralizado por dominio** — cada dominio de negocio es dueño de sus datasets; el dominio pasa a ser el "quantum arquitectónico" en vez de las etapas del pipeline. Sirve datos *source-aligned* (hechos del negocio) y datasets *consumer-aligned* (agregados para casos de uso).
2. **Datos como producto** — los datasets se tratan como productos para sus consumidores. Deben ser: descubribles (catálogo), direccionables (naming estándar), confiables (SLOs de calidad), auto-descriptivos (schema + samples), interoperables (estándares federados) y seguros (control de acceso).
3. **Infraestructura de datos self-serve como plataforma** — plataforma compartida y agnóstica al dominio: storage poliglota, orquestación de pipelines, catálogo, governance, monitoreo de calidad y control de acceso. Baja el lead time de crear un data product nuevo.
4. **Governance computacional federada** — estándares globales para interoperabilidad (formatos de evento, identificadores de entidad *polysemes*, schemas) con implementación descentralizada. Permite correlacionar datos entre dominios sin control central.

## Conceptos clave

- **Data product:** dataset con SLOs de calidad, ownership, documentación y experiencia de consumo — pensamiento de producto aplicado a datos.
- **Source-aligned vs consumer-aligned:** dominios fuente emiten hechos inmutables como eventos; dominios consumidores los transforman en vistas agregadas (grafos, series de tiempo) para casos de uso específicos.
- **Data product owner:** rol responsable de visión, satisfacción del consumidor, SLOs y ciclo de vida del dataset del dominio.
- **Convergencia DevOps + datos:** embeber data engineers en los equipos de dominio (como DevOps en equipos de operación) elimina los silos de skills y habilita ownership end-to-end.

## Cómo se refleja en RIO ([[RIO]])

- **Self-serve platform:** los control planes ([[rio-controlplane-kafka]], [[rio-controlplane-flink]], [[rio-controlplane-clickhouse]], [[rio-controlplane-fury]]) son la infraestructura self-serve que provisiona storage/streaming por dominio.
- **Orquestación de data products:** [[rio-playmaker]].
- **Governance federada:** [[rio-controlplane-kms]] (seguridad), [[rio-controlplane-observability]] (calidad), contratos vía [[rio-sdk-events]].
- **Consumer-aligned:** [[rio-materializer]].

## Procedimiento reusable

1. Delimitar los dominios productores y consumidores y asignar ownership explícito de cada data product.
2. Definir contratos, SLOs, documentación y controles de acceso para que cada data product sea consumible de forma autónoma.
3. Proveer infraestructura self-serve y estándares federados que permitan a los dominios operar sin un cuello de botella central.

## Preguntas para el equipo (onboarding)

- ¿Qué dominios son productores vs consumidores en RIO hoy?
- ¿Dónde vive el catálogo/discoverability de los data products?
- ¿Qué SLOs de calidad se exigen a un data product para publicarse?
- ¿Cómo se modela la governance federada (quién define los estándares globales)?
