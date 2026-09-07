---
type: application
schema_version: 1
status: active
slug: rio-controlplane-kms
area: "[[Meli]]"
lang: Java
github: https://github.com/melisource/fury_rio-controlplane-kms
path: ~/fuentes/rio-controlplane-kms
aliases:
  - rio controlplane kms
tags:
  - kind/application
  - area/meli
  - app/rio-controlplane-kms
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
confidence: high
---

# rio-controlplane-kms

> [!info]+ rio-controlplane-kms
> **Rol:** Servicio de cifrado/descifrado de secretos para el control plane de RIO, delegando la criptografía en CKaaS · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-controlplane-kms) · **Local:** `~/fuentes/rio-controlplane-kms` · **Lang:** Java

## 🎯 Responsabilidad (estable)
- Expone operaciones de cifrado y descifrado de secretos (valores planos y JSON) para las aplicaciones de RIO.
- No implementa la criptografía: delega el cifrado/descifrado real en CKaaS (Crypto/Key Management as a Service) y persiste los registros de secretos cifrados.
- Actúa como capa de control plane: valida requests, gestiona metadata del secreto (environment, requester) y expone contrato HTTP estable hacia el resto de RIO.

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** `POST /kms/api/v1/secrets/encrypt`, `POST /kms/api/v1/secrets/encrypt-json`, `POST /kms/api/v1/secrets/decrypt`, `POST /kms/api/v1/secrets/decrypt-json`, `GET /ping`.
- **Consume / produce:** requests con valor/JSON a cifrar + metadata (`Environment`, `Requester`); responde el secreto cifrado o descifrado con su metadata asociada (`SecretRecord`).
- **Llama a / lo llaman:** cifra/descifra vía CKaaS (`java-toolkit-ckaas`); persiste registros de secretos en KVS (`java-toolkit-kvs`); consumido por aplicaciones del control plane de RIO.

## 🧩 Implementación (volátil · last_verified: 2026-08-10)
- **Stack:** Spring Boot 3.5.11, Java 25 (toolchain), Gradle, Jetty embebido.
- **Librerías / infra clave:** `com.fury.toolkit:java-toolkit-ckaas:0.3.5` (cifrado/descifrado), `com.fury.toolkit:java-toolkit-kvs:0.6.1` (persistencia de `SecretRecord`), `spring-boot-starter-secrets` (credenciales vía Fury Secret Manager), `resilience4j-spring-boot3`, OpenTelemetry + Datadog para telemetría, springdoc-openapi.
- **Patrón notable:** separación controller → service → repository; `EncryptionService`/`DecryptionService` orquestan CKaaS (`CKaaSService`) y `SecretRepository` (impl. `SecretKVSRepositoryImpl` sobre KVS); excepciones de dominio propias (`SecretNotFoundException`, `SecretStorageException`, `SecretThrottlingException`, etc.) manejadas por `ControllerExceptionHandler`.

## 🔗 Relaciones
- [[rio-playmaker]]
- [[rio-materializer]]

## 📌 Provenance
- Repo: `melisource/fury_rio-controlplane-kms` · Local: `~/fuentes/rio-controlplane-kms`
- Fuentes leídas: `README.md`, `build.gradle`, `graphify-out/GRAPH_REPORT.md`, listado de `src/main/java` (controllers, services, repository, exceptions)
- `last_verified: 2026-08-10` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-controlplane-kms
short mode
hide task count
```
