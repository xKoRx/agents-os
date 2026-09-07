---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-sdk-events]]"
  - "[[Guía de implementación — Component Context]]"
aliases:
  - PR rio-sdk-events component context
  - descripción PR SDK SIG-573
tags:
  - kind/doc
  - project/crear-context
created: "2026-08-19"
updated: "2026-08-19"
---

# Descripción PR — rio-sdk-events

**Repo:** `rio-sdk-events` · **Branch:** `feature/SIG-573-component-context` · **Base:** `master` @ `9d86eb8` · **Commits:** 4 (`af9ea8d`, `f189c4e`, `b152143`, `d21001b`) · **Diff:** 5 archivos, +280/-4 · **Spec:** [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573) · **Consumido por:** `rio-playmaker` branch `feature/component-context` (ver [[Descripción PR — rio-playmaker]])

> [!warning] Bloqueantes abiertos
> **Versión.** `build.gradle` declara `0.0.1-component-context`, versión de prueba. Antes del merge tiene que subir a semver real — `1.4.0` según el tipo de cambio (aditivo y compatible) — y el consumidor en Playmaker debe apuntar a esa versión publicada.
> **CHANGELOG desalineado.** La entrada `[1.4.0]` describe el envelope rico descartado (`mappings`, `issues`, `completeness`, `output_path`/`consumer_path`, `schema version`) y afirma que el contrato "does not modify deployment trigger messages", que ya es falso. Hay que reescribirla contra el contrato entregado antes de abrir el PR.
> **Historia de la branch.** Los 4 commits incluyen un `wip(...)` que preserva el diseño abandonado. Conviene squashear a 1 commit con sujeto convencional en inglés — el HEAD actual (`nuevo contexto de componente`) además está en español, contra el `CODING_GUIDELINES.md` del propio repo.

## Propósito

Descripción del Pull Request de `rio-sdk-events` para SIG-573, lista para copiar y pegar en GitHub. Vive en el vault como recurso del proyecto, no como archivo en la raíz del repo: así no se cuela en el diff que describe, no se pierde al cambiar de branch y queda enlazada al proyecto y a las specs.

## Contenido

Identidad de la entrega (branch, base, commits, diff) · tres bloqueantes abiertos · las secciones del template `.github/PULL_REQUEST_TEMPLATE.md` de este repo, en su idioma original · notas internas que **no** van al PR.

> Nota de idioma: el template del repo está en español mientras su `CODING_GUIDELINES.md` pide inglés para toda contribución. Se respetó el template y queda la tensión anotada para que el equipo decida.

---

# Descripción del PR

## ¿Cuál es el comportamiento actual?

`DeploymentTriggerMessage` transporta identificadores, tipo de componente, criticidad y `params`: un mapa de variables ya resueltas por Playmaker. Un control plane que recibe `"broker:9092"` no tiene forma de saber de dónde salió ese valor. No conoce los componentes que lo rodean, qué publica cada uno, ni en qué versión quedó su propio último deployment. El SDK no expone ningún tipo para transportar esa información: el mensaje lleva valores, no contexto.

## ¿Cuál es el comportamiento esperado con el nuevo cambio?

El SDK expone `ComponentContext`, el contrato serializable del contexto efímero de un componente, y `DeploymentTriggerMessage` gana un campo `context` **nullable** para transportarlo.

`ComponentContext` es un `record` inmutable con cuatro campos — `data_product`, `last_version`, `sources[]` y `destinations[]` — donde cada elemento es un `RelatedComponent` (`name`, `type`, `outputs`). Los `outputs` llegan **ya resueltos** por Playmaker: el mismo valor efectivo que se sustituye en `params`, sin el sobre `{type,value,sensitive}` del almacenamiento. Un componente relacionado que todavía no publicó nada llega con `outputs` vacío, que es un estado ordinario durante un rollout topológico y no un error.

El cambio es **aditivo y compatible hacia atrás**, por diseño y en tres frentes:

- Se conserva un constructor de compatibilidad de 14 argumentos en `DeploymentTriggerMessage`, que delega con `context = null`. Los productores existentes compilan y publican exactamente el mismo mensaje que antes, sin tocar una línea.
- `@JsonIgnoreProperties(ignoreUnknown = true)` en el mensaje hace que un consumidor que ignora el campo se comporte igual que siempre. Ningún control plane necesita cambiar.
- El propio `ComponentContext` también ignora campos desconocidos, de modo que el contrato puede crecer sin romper a quien ya lo lee.

Dos propiedades del tipo que son parte del contrato, no detalles de implementación:

- **Inmutabilidad real.** El constructor compacto copia las listas y el mapa de outputs, y valida identidad no vacía y ausencia de nulos. Mutar la colección del caller después de construir no se filtra hacia adentro.
- **`toString()` redactado.** Emite identidad y conteos, nunca valores; `RelatedComponent` omite además las claves. Los outputs de un componente vecino pueden incluir credenciales, así que el tipo se diseñó para ser seguro de loguear por accidente.

## Pruebas

### ¿Cómo probar el nuevo comportamiento?

* `./gradlew test jacocoTestCoverageVerification` — **696 tests passed, 0 failed**, gate de cobertura del 88.8% superado
* `ComponentContextTest` — 7 tests: serialización `snake_case` con los cuatro campos del contrato; round-trip que conserva los outputs resueltos; tolerancia a campos desconocidos; `last_version` ausente para un componente que nunca desplegó; rechazo de `data_product` y de `name` en blanco; inmutabilidad frente a la mutación de la colección del caller; y redacción de `toString()`, verificada plantando el valor `sup3rs3cret` bajo la clave `password` y afirmando que ni el valor ni la clave aparecen
* `DeploymentTriggerMessageTest` — la suite existente sigue verde usando el constructor de compatibilidad, que es la prueba de que el cambio no rompe a los productores actuales
* Verificación end-to-end del campo en el wire: vive en `rio-playmaker` (`BigQueueDispatchAdapterTest`), que captura el mensaje publicado y afirma que el context viaja cuando existe y que el mensaje queda con `context == null` cuando no

# Issue relacionado

* Spec funcional: [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573)

# Checklist del PR

- [x] Revisé cuidadosamente el código antes de crear el PR.
- [ ] Me aseguré que el `diff` claramente representa mis cambios. — **pendiente**: la branch arrastra un commit `wip` con el diseño descartado; hay que squashear.
- [x] Me aseguré que este PR no tiene sentido dividirlo en PRs más pequeños.
- [x] Verifiqué que el estilo de mi código y scaffolding adhieran al del proyecto.
- [x] Me aseguré de que mis cambios no afectan otra funcionalidad que no sea la de este PR. — campo nullable + constructor de compatibilidad; ningún productor ni consumidor existente cambia.
- [x] Agregué/modifiqué los `tests` necesarios para el componente o funcionalidad que estoy implementando.
- [x] Corrí los `tests` y me aseguré de que funcionan. — 696 passed, 0 failed, cobertura OK.
- [ ] Ajusté el fichero `CHANGELOG.md` del repositorio. — **pendiente**: la entrada existe pero describe un contrato que ya no es el entregado, y declara una versión que el build no usa.
- [x] Me aseguré de modificar el README con el nuevo comportamiento, en caso de que aplique. — no aplica: el README no documenta el contrato de `DeploymentTriggerMessage` campo por campo.

---

## Notas internas (no van al PR)

- Findings abiertos del code review: el javadoc del campo `context` promete que los valores vienen "classified by sensitivity" y que los CP deben honrar esa clasificación, pero el contrato simplificado no transporta ninguna marca de sensibilidad — el builder la descarta al desenvolver. Hay que corregir el javadoc o reponer la clasificación. Además, los constraints `@NotBlank`/`@NotNull` del record son decorativos: ningún validador los ejecuta en el path de deserialización.
- Trazabilidad: [[Crear Context]] · [[Guía de implementación — Component Context]] · [[Descripción PR — rio-playmaker]]
