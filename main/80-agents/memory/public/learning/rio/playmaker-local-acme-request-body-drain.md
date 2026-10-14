---
type: learning
schema_version: 1
scope: "application"
created: "2026-10-13"
updated: "2026-10-13"
area: "[[Meli]]"
project: "[[RIO E2E local]]"
application: "[[rio-playmaker]]"
entities: ["[[rio-playmaker]]"]
related: ["[[RIO E2E local — Diseño revisado]]"]
aliases: []
confidence: "verified"
source_session:
load_policy: "when_application_loaded"
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
---

# Playmaker — Cerrar peticiones incompletas del fixture ACME

## Aprendizaje

En el fixture ACME de Playmaker con JDK 25, drenar un body sin límite bloquea el único worker. Quitar transferTo y poner Connection: close no basta: HttpExchange.close, los streams y sendResponseHeaders con longitud negativa pueden leer el body pendiente.

El contrato local acepta GET sin body. Valida método/ruta/token primero; rechaza Content-Length positivo o Transfer-Encoding sin leerlos. Para GET/POST con body entrega una respuesta fija completa y aborta por IOException, dejando que ServerImpl cierre el canal sin drain. HEAD necesita una rama previa: JDK 25 fuerza close dentro de sendResponseHeaders aun con longitud positiva. HEAD con body se corta por EOF/reset antes de headers; HEAD sin body conserva 405. Mantener 405/404/403 para las demás peticiones rechazadas y 200/JSON para el GET autorizado sin body.

La regresión debe usar sockets reales con CL incompleto y chunked sin terminador, mantener abierto el sender, exigir otro GET autorizado y EOF/reset del rechazo antes del fallback. Si el test cierra primero al atacante, puede ocultar el bloqueo.

## Aplicabilidad

- **Cuándo cargarlo:** al cambiar el fixture HTTP local ACME o su teardown, con el JDK 25 fijado por Playmaker. Confirmar implementación y pruebas al cambiar de JDK.
- **Cuándo no cargarlo:** como receta general para servidores HTTP productivos o garantía frente a headers incompletos, saturación de conexiones u otros ataques. No autoriza propiedades globales, pools sin límite ni cambios de autorización.

## Entidades relacionadas

[[rio-playmaker]] y [[RIO E2E local]].

## Evidencia

- [Comentario 4263876597](https://github.com/melisource/fury_rio-playmaker/pull/1286#discussion_r4263876597); JDK 25 ExchangeImpl/LeftOverInputStream/ServerImpl inspeccionados en src.zip instalado.
- [[2026-10-13-rio-e2e-local-pr-comments]]: servidor publicado RED 5 tests/2 timeouts; primer fix todavía RED HEAD por timeout del GET posterior; final GREEN 26 locales/0 fallos/0 errores/0 skips, cobertura/aislamiento PASS. Challenge de fuente y estado de sockets calificado, sin ejecución propia del verificador.
