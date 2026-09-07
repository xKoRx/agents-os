---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[Descripción PR — rio-playmaker — Crear Context (zord authoring)]]"
aliases:
  - overview técnico de rio-playmaker
  - documento técnico Playmaker para Crear Context
tags:
  - kind/doc
  - project/crear-context
  - application/rio-playmaker
created: "2026-08-27"
updated: "2026-08-27"
---

# Documento técnico — rio-playmaker — visión general

## Propósito

Entregar una vista técnica de una hoja para que una persona que se incorpora a `rio-playmaker` entienda qué controla la aplicación, cómo se relacionan sus entidades y cómo una solicitud de despliegue llega al sistema que materializa infraestructura.

## Contenido

# Rio Playmaker: Technical Overview

## Purpose and ownership

Rio Playmaker is the control plane for a data product’s component lifecycle. It owns the product model, the configuration that describes deployable components, the environment-specific service instances, and the recorded history of deployment attempts.

Its observable role is to turn a declared component configuration into a deployment request while keeping the product’s intended state and deployment history queryable. It coordinates infrastructure provisioning with Materializer; it is not described as the infrastructure provisioner itself.

## Core mental model

```text
Data Product
├── Components
│   └── Component Definitions
├── Environments
│   └── Services (a definition instantiated in an environment)
│       └── Deployments
│           └── Deployment Logs
└── Component Relations
```

- A **Data Product** is the top-level product boundary, including ownership, status, and visibility.
- A **Component** is a named building block within that product; its template identifies the kind of component.
- A **Component Definition** supplies the deployable configuration for a component, including type, parameters, SLOs, state, and validity status.
- An **Environment** scopes where the product runs and records its type and criticality.
- A **Service** binds one component definition to one environment, with environment-specific configuration values.
- A **Deployment** is an attempt to materialize a service. It carries a Materializer correlation identifier, status, active flag, and configuration values.
- A **Deployment Log** records status changes or other deployment information against that attempt.

This separation matters because the same component can have different definitions and can be instantiated as separate services in multiple environments. A deployment is therefore not “deploy the component” in the abstract; it is “deploy this configured service in this environment.”

## Deployment flow

1. A client creates a data product, its components and component definitions, then declares target environments.
2. The client creates a service by selecting a component definition and an environment. Playmaker persists that desired service state in SQL.
3. The client creates a deployment for that service. Playmaker records the deployment and associates it with a `materializationId`.
4. Playmaker coordinates with **Materializer**, which is responsible for infrastructure management, resource provisioning, service configuration, and deployment administration.
5. Deployment status is recorded through deployment logs, allowing the service and deployment history to be observed after the request is made.

The causal split is deliberate: Playmaker retains the product intent and lifecycle record; Materializer performs the infrastructure-facing materialization. The `materializationId` connects those two views.

## Coordinated systems and boundaries

| System | Why Playmaker coordinates with it |
|---|---|
| Materializer | Provisions and administers infrastructure for deployments. |
| MySQL / SQL | Stores product models, configuration, service state, and deployment history. |
| Workqueue / BigQueue | Supports asynchronous task processing and job handling. The supplied sources use both names; whether they are the same integration is not established. |
| Secrets | Holds credentials, tokens, and sensitive configuration. |
| AWS S3 | Stores JARs, artifacts, logs, and static resources; the API also exposes JAR-upload and queued-upload processing endpoints. |
| Tiger Token / Spring Security | Authenticates requests; documentation states all endpoints except `/ping` and API documentation require authentication. |
| Nexus Repository and New Relic | Listed in the README as integrations for repository access and monitoring, respectively; their role in the deployment path is not specified. |

## Boundaries, risks, and open questions

Playmaker’s source material establishes the lifecycle model and the Materializer handoff, but not the exact completion mechanism. In particular, it does not establish whether deployment status is pushed by Materializer, polled by Playmaker, or written by another actor through the deployment-log API. It also does not define the rules that set `isActive`, retries, rollback behavior, or the semantics of component relations.

For onboarding, treat Playmaker as the authoritative record of **what should exist and what deployment history says happened**. Verify the live API contract and Materializer integration before relying on any stronger claim about orchestration, failure recovery, or production activation.

## Fuentes

- `rio-playmaker/README.md` — propósito, stack, estructura, endpoints y prácticas de desarrollo.
- `rio-playmaker/docs/guide/content/en/architecture.md` — arquitectura y sistemas coordinados.
- `rio-playmaker/docs/guide/content/en/data-model.md` — entidades y relaciones del dominio.
- `rio-playmaker/docs/guide/content/en/api.md` — superficie REST documentada.
