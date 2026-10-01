---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url: "https://github.com/melisource/fury_rio-controlplane-kafka/commit/ca180102dd23cb57137905da6b7dc0c8a96011a8"
repo: "https://github.com/melisource/fury_rio-controlplane-kafka"
path: "docker-compose.yml"
author:
published:
captured: "2026-10-01"
license:
checksum:
supersedes:
superseded_by:
aliases: ["Prueba Kafka local 2026-10-01"]
tags:
  - kind/source
  - area/meli
  - app/rio-controlplane-kafka
created: "2026-10-01"
updated: "2026-10-01"
---

# Kafka local — Historia y prueba de arranque (2026-10-01)

## Referencia

- **Origen resoluble:** historia Git y ejecución de una copia limpia de `develop@c9355395ef4b2bf438f0eb44528e24fa76ca498c` de [[rio-controlplane-kafka]].
- **Fecha de captura:** 2026-10-01.
- **Relación:** complementa [[Repositorios RIO — Ambientes locales (2026-09-30)]] con historia y evidencia runtime; no modifica su captura estática.

## Alcance

- Verificar cuándo se incorporó el Compose y si el broker y el control plane arrancan localmente, usando Kafka real.
- Máquina ARM64, Docker en Colima, imagen `apache/kafka:3.9.0`, JVM del broker `21.0.5+11`; control plane ejecutado con Java 25.

## Historia comprobada

- **Creación:** Felipe Caputo agregó `docker-compose.yml` y `scripts/kafka-seed.sh` el **2026-02-25 a las 10:02:49 −03:00**, commit [`ca180102`](https://github.com/melisource/fury_rio-controlplane-kafka/commit/ca180102dd23cb57137905da6b7dc0c8a96011a8). El commit también corrige el binding del listener controller y el stdin del productor.
- **Ajuste posterior:** [`301b7c96`](https://github.com/melisource/fury_rio-controlplane-kafka/commit/301b7c969bf1b85982eda63d1be9117dd663a8e3), el mismo día a las 11:13:31 −03:00, aclara los valores del Compose.
- **Entrada a develop:** merge [`cdeb9c02`](https://github.com/melisource/fury_rio-controlplane-kafka/commit/cdeb9c028620031113e5e614e187fc2e1fac928f), **2026-03-02 a las 12:38:29 −03:00**, [PR #1](https://github.com/melisource/fury_rio-controlplane-kafka/pull/1).

## Prueba realizada

| Paso | Resultado observado | Alcance |
|---|---|---|
| Compose original, `up -d --wait --wait-timeout 60` | FAIL: el contenedor sale con código 1, `SIGILL`, frame `java.lang.System.registerNatives()` en JVM Linux aarch64 | El arranque original falla en esta máquina. No demuestra que falle en todas las arquitecturas. |
| Control plane original, `SCOPE=local`, Java 25, `bootRun` | Compilación correcta; arranque FAIL por ausencia de `profiles/local/cloud-provider.json` y del fallback de configuración | La copia limpia requiere routing local adicional. |
| Broker con override temporal `JAVA_TOOL_OPTIONS: "-XX:UseSVE=0"` | PASS: contenedor `running`, healthcheck `healthy` | La misma imagen funciona con ese ajuste en esta máquina. El Compose del repo quedó intacto. |
| Control plane con archivo de routing AWS local | PASS: Jetty inicia en 8080; `/ping` devuelve HTTP 200 y `pong` | Archivo temporal con cluster `aws-local-verification`, template `aws-msk-topic`, bootstrap `localhost:9092`, teams `[all]`. |
| Script existente `kafka-seed.sh rio-local-verification-20261001 5` | Crea un topic con 3 particiones y RF=1; publica 5 mensajes | Broker real; ningún servicio Kafka simulado. |
| Kafka console consumer | Lee 5 mensajes, claves `key-1` a `key-5` e IDs 1 a 5 | Confirma que los mensajes quedaron en el broker. |
| `POST /kafka/topic/rio-local-verification-20261001/peek?offset=EARLIEST&num_msgs=5&timeout_ms=10000`, body `{"brokers_url":"localhost:9092"}` | PASS: HTTP 200, 5 mensajes, `value_format=JSON`, claves e IDs originales verificados | Endpoint real del control plane, conexión plaintext y lectura del broker real. |

La imagen ARM64 utilizada corresponde a `apache/kafka@sha256:fbc7d7c428e3755cf36518d4976596002477e4c052d1f80b5b9eafd06d0fff2f`. El override de diagnóstico sólo agrega la opción JVM; el routing sólo apunta a loopback. No se modificó código de los repositorios.

## Dependencias y límites observados

- El control plane arranca con routing AWS local aunque falten credenciales GCP: el warmup registra `resolved=false` como WARN y continúa. La documentación solicita una SA, pero su ausencia no fue un bloqueo de este arranque. No se probaron autenticación ni operaciones GCP.
- El runtime selecciona explícitamente `LocalFileBigQueueClient` para resultados y `NoOpKvsClient` para idempotencia. Por tanto, el arranque y PEEK comprobados no satisfacen todavía el requisito completo de servicios reales.
- PROVISION, UPDATE, DEPROVISION, acciones por trigger, entrega de resultados a Playmaker, CAS/TTL e idempotencia no se ejecutaron en esta prueba.
- La lectura PEEK comprobada usa el endpoint directo de depuración con `brokers_url`; no valida routing del flujo de acciones.
- Los procesos del control plane y el Compose de prueba se retiraron al terminar. Los checkouts originales y sus cambios locales se preservaron. La evidencia se resume aquí; las copias y logs temporales de máquina no son almacenamiento durable.

## Notas de provenance

- Evidencia obtenida con Git local, Docker, Gradle, el script original del repo y solicitudes HTTP locales. Se distinguieron el arranque original y las repeticiones con configuración temporal.
- La respuesta de PEEK devolvió `value` como objeto JSON; se verificaron los objetos serializados y sus claves e IDs.

## Lifecycle

- **Supersedes:** ninguna; evidencia complementaria del 2026-10-01.
- **Superseded by:** pendiente de una nueva ejecución documentada.
