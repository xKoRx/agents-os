---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-659 — RIO Bus (implementación)]]"
  - "[[rio-sdk-events]]"
  - "[[Descripción PR — rio-playmaker — RIO Bus]]"
aliases: []
tags:
  - kind/doc
  - project/sig-659
created: "2026-10-28"
updated: "2026-10-28"
---

# Descripción PR — rio-sdk-events — RIO Bus

**Identidad:** fury_rio-sdk-events · `feature/rio-bus` @ `332b0d9` · base `feature/discovery-v2-05-contract-hasher` @ `35b1a43` (PR #56, pila SIG-644) · 5 commits · 39 archivos, +2198/−23 · spec [SIG-718](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) · consumido por [[Descripción PR — rio-playmaker — RIO Bus]] · suite 2026-10-28 sobre `a38ff44`: 2.557 tests, 0 fallos, coverage gate PASS.

> [!warning] Bloqueantes del merge
> **Versión de prueba.** `build.gradle` declara `0.0.3-rio-bus`; antes del merge va el semver del release.
> **PR apilado.** La base es `feature/discovery-v2-05-contract-hasher` (#56); la pila de SIG-644 (#48 → #53 → #54 → #55 → #56) se mergea primero.

## Propósito

Cuerpo del PR del SDK del RIO Bus como recurso de [[SIG-659 — RIO Bus (implementación)]], con la estructura del template `.github/PULL_REQUEST_TEMPLATE.md` del repo (en español).

## Contenido

Cuerpo listo para pegar, seguido de notas internas que no van al PR.

---

[description]: https://img.icons8.com/material-sharp/24/000000/document.png
[checkmark]: https://img.icons8.com/material-sharp/24/000000/checkmark.png
[checklist]: https://img.icons8.com/material-sharp/24/000000/check-all.png
[testing]: https://img.icons8.com/material-sharp/24/000000/test-partial-passed.png

# ![alt text][description] Descripción del PR

> [!IMPORTANT]
> **PR apilado sobre #56** (`feature/discovery-v2-05-contract-hasher`, SIG-644 5/8): el diff contiene sólo el RIO Bus. **Antes del merge** hay que reemplazar la versión de prueba `0.0.3-rio-bus` de `build.gradle` por el semver del release y mergear primero la pila de SIG-644.

## ¿Cuál es el comportamiento actual?

rio-playmaker y los control planes se comunican por BigQueue con un tópico, un controller y un parseo propios por cada flujo. El SDK no ofrece nada para consumir: cada app escribe su controller y decide su política de ack.

Discovery V2 ([SIG-635](https://spellbook.adminml.com/projects/SIG/specs/SIG-635)) necesita que cada CP le mande su contrato a playmaker, y ese canal no existe. Tampoco hay en el SDK un reader que lea el contrato desde JSON aplicando las reglas de SIG-644 §7.3.

Además, `BigQueueClientImpl` arma un builder con `segment-id` y buffering, pero crea el producer sin ese builder: el segmento configurado nunca se aplica.

## ¿Cuál es el comportamiento esperado con el nuevo cambio?

**RIO Bus** ([SIG-718](https://spellbook.adminml.com/projects/SIG/doc/SIG-718)): un solo tópico `rio-bus` para todo lo que viaja entre playmaker y los CPs, con un mensaje de cuatro atributos.

```json
{ "envelope_version": 1, "process": "discovery", "scope": "test", "body": { } }
```

- **Publicar:** `RioBusPublisher.publish(process, body)` arma el mensaje con el `scope` de la app y deriva los filtros `process:<process>` y `scope:<scope>`. Quien publica no puede agregar ni cambiar filtros, así que el filtro y el mensaje no pueden divergir.
- **Consumir:** cada app tiene un solo consumer por scope hacia `POST /rio-bus` (`RioBusController`). `RioBusReader` valida el mensaje, elige el `RioBusProcess` suscrito por nombre, le pasa el body como texto JSON a `parse` y corre `run` dentro del request.
- **Ack:** todo responde 200, salvo una excepción transitoria de `run`, que responde 500 para que BigQueue reintente. Así un mensaje que nunca se va a poder procesar no se reintenta hasta el TTL.
- **Configuración:** `rio.bus.topic`, `rio.bus.scope` (`${SCOPE}`) y `rio.bus.segment-id` (`nonprod` o `nonsite`). `RioBusAutoConfiguration` se activa con `rio.bus.topic`. El publisher es `@Lazy`, así que una app que sólo consume no abre un producer.

**Discovery:**

- `DiscoveryContractPublisher` publica al arrancar (`ApplicationReadyEvent`) los contratos que entrega el `DiscoveryContractProvider` del CP. El CP no escribe código de publicación. Ninguna falla sale del listener, porque una excepción en `ApplicationReadyEvent` aborta el arranque: si el provider falla o devuelve `null`, si un contrato es inválido o si BigQueue falla, queda en log y métrica y el CP arranca igual.
- `DiscoveryMessageReader.read(byte[] | String)` lee el JSON del contrato sin envoltorio de transporte y devuelve `Accepted(message)` o `Rejected(reason, pointer)`, sin valores del payload. Agrega las razones `MESSAGE_TOO_LARGE`, `MALFORMED_JSON`, `DUPLICATE_KEY`, `UNKNOWN_ENUM_VALUE` e `INVALID_TIMESTAMP`.
- Los cuatro tipos V1 (`CPCapabilityMessage`, `ComponentTypeCapability`, `ActionCapability`, `FieldDescriptor`) vuelven sin cambios desde `1.5.0`, porque el consumer V1 de playmaker todavía los compila. Se retiran cuando la ingesta de SIG-671 reemplace ese consumer.

**BigQueue:** `BigQueueClientImpl` crea el producer desde el builder, con segmento y buffering. **Esto cambia el comportamiento de todos los usuarios del cliente**: el `segment-id` que ya tenían configurado empieza a aplicarse. El parámetro `ProducerFactory` del constructor se conserva para no romper el código fuente de quienes lo usan.

**Privacidad:** el body nunca va a logs, a métricas ni a la causa de una excepción. El tag `process` de las métricas sólo toma nombres suscritos; cualquier otro valor queda como `unknown`, para que un mensaje no pueda abrir series nuevas.

Decisiones que conviene tener a mano al revisar:

- **El process parsea su body**, en vez de usar polimorfismo de Jackson, porque la API no expone tipos de Jackson: playmaker usa Jackson 2 y el modelo V2 usa Jackson 3. Además Discovery necesita su propio reader.
- **El endpoint recibe `byte[]`** para no depender de los message converters de la app.

# ![alt text][testing] Pruebas

## ¿Cómo probar el nuevo comportamiento?

Sobre `feature/rio-bus` @ `a38ff44` (el commit siguiente, `332b0d9`, sólo cambia la versión), con JDK 21:

- `./gradlew check test jacocoTestCoverageVerification` → **2.557 tests, 0 fallos, 0 omitidos**; Checkstyle, PMD y el gate de coverage pasan. Las clases nuevas tienen 100% de líneas y ramas.
- `DiscoveryBusWireTest`: un contrato serializado con el `JsonUtils` de mqclient, que es lo que usa el producer real, pasa `RioBusReader` y `DiscoveryMessageReader` y llega con el mismo hash.
- `RioBusReaderTest` cubre cada fila de la tabla de outcomes y comprueba que el body no aparece en logs ni en tags.
- `DiscoveryContractPublisherTest` cubre un provider que falla, uno que devuelve `null` y contratos inválidos sin cortar el arranque.

La versión de prueba **`0.0.3-rio-bus`** está publicada en Fury desde `332b0d9` (estado `FINISHED`). rio-playmaker ya la consume en su rama `feature/rio-bus` (suite completa: 5.224 tests, 0 fallos); ese PR se abre aparte.

# ![alt text][checkmark] Issue relacionado

- Spec funcional y técnica: [SIG-718](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) (RIO Bus)
- Epic: [SIG-659](https://spellbook.adminml.com/projects/SIG/specs/SIG-659) Discovery & CLI · Modelo V2: [SIG-644](https://spellbook.adminml.com/projects/SIG/specs/SIG-644)
- PR base: #56

# ![alt text][checklist] Checklist del PR

- [x] Revisé cuidadosamente el código antes de crear el PR.
- [x] Me aseguré que el `diff` claramente representa mis cambios.
- [ ] Me aseguré que este PR no tiene sentido dividirlo en PRs más pequeños. — El fix de `BigQueueClientImpl` y la restauración de los tipos V1 podrían ir aparte; van acá porque el bus y el consumer de playmaker los necesitan para funcionar.
- [x] Verifiqué que el estilo de mi código y scaffolding adhieran al del proyecto.
- [ ] Me aseguré de que mis cambios no afectan otra funcionalidad que no sea la de este PR. — El fix de segmento cambia a propósito a todos los usuarios de `BigQueueClientImpl`.
- [x] Agregué/modifiqué los `tests` necesarios para el componente o funcionalidad que estoy implementando.
- [x] Corrí los `tests` y me aseguré de que funcionan.
- [ ] Ajusté el fichero `CHANGELOG.md` del repositorio con el cambio en la sección de `[Unreleased]` bajo el subgrupo de `Fixed` o `Added` según corresponda. — Está en `[Unreleased]`, pero el fix de segmento quedó bajo `Added` y corresponde a `Fixed`.
- [ ] Me aseguré de modificar el README con el nuevo comportamiento, en caso de que aplique. — El README todavía describe dos mecanismos de publicación y no documenta el bus.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Notas internas — NO van al PR

- `BigQueueClientImpl` conserva el parámetro `ProducerFactory` sin usarlo (`@SuppressWarnings`); el fix upstream `c67d65e` mantenía el factory como seam con una sobrecarga nueva. Autorizado por el owner como D-10.
- `RioBusController` es `@RestController` y además `@Bean` de la auto-configuración; no tiene la condición de Spring MVC en el classpath que pide SIG-718 técnica.
- `DiscoveryMessageReader` clasifica errores por el texto del mensaje de Jackson (`Number value length`, `Duplicate `); frágil ante upgrades de Jackson, hoy cubierto por tests.
- Los tipos V1 contradicen la decisión 1 de SIG-644; se retiran con SIG-671. `DiscoveryMessageReader` lo implementó Codex, no Brenda: avisarle para no duplicar.
