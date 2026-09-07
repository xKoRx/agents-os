---
type: runbook
schema_version: 1
scope: global
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Meli]]"
project:
application:
entities: []
related:
  - "[[pr-description]]"
  - "[[signals-code-review]]"
aliases:
  - runbook descripciones de PR
  - por qué la descripción del PR vive en el vault
  - donde va la descripcion de un pull request
confidence: high
source_session: 2026-08-24
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/global
  - tech/git
  - tech/github
---

# Descripciones de PR — recurso del proyecto en el vault

%% Cara humana (el *por qué*) de la skill [[pr-description]]. El procedimiento imperativo vive en ese SKILL.md; esta nota es el racional y la convención. Una fuente canónica por hecho: no duplicar el procedimiento acá. %%

## Propósito

Dejar escrito **dónde vive** la descripción de un Pull Request, **quién manda** sobre su forma y **por qué**. La versión ejecutable para agentes es la skill [[pr-description]].

## La regla en una línea

La descripción de un PR es documentación **del proyecto**, no un artefacto **del repo**: se escribe en `10-projects/<Área>/<Proyecto>/Descripción PR — <repo>.md`, con la estructura del template `.github` del repo destino, una nota por repo, siempre nombrando la branch.

## Por qué no en la raíz del repo

Un `descripcion_pr.md` en la raíz —la práctica que esta convención reemplaza— falla por cuatro razones distintas y todas caras:

- **Se cuela en el diff que describe.** El PR termina incluyendo el archivo que explica el PR. Ruido garantizado y un reviewer preguntando qué hace eso ahí.
- **Se pierde al cambiar de branch.** Vive con el checkout, no con el proyecto. Al mergear o abandonar la rama, la descripción desaparece con ella.
- **Queda fuera del grafo.** No enlaza al proyecto, a las specs ni a las aplicaciones; no aparece en ninguna búsqueda del vault y nadie la encuentra tres semanas después.
- **Contamina un repo compartido** con un artefacto personal de una sesión de trabajo.

En el vault sobrevive al merge, queda enlazada al proyecto y a los specs, y se lee junto al resto del expediente de la entrega.

## Por qué manda el template del repo

Cada repo negoció su propio template con su equipo: qué preguntas responde un PR, qué se checkea antes de pedir review, y en qué idioma. Inventar un formato propio —o copiar el de otro repo— le quita al reviewer las señales que espera encontrar. En RIO ya son distintos entre sí: `rio-playmaker` usa uno en inglés con checklist de dev y de reviewer; `rio-sdk-events` usa uno en español con las tres preguntas (comportamiento actual, comportamiento esperado, cómo probar). La única autoridad es el archivo `.github` del repo al que se le va a abrir el PR, leído en el momento; cualquier copia en el vault sería una fuente duplicada que se desactualiza.

Cuando el template está en un idioma y el `CODING_GUIDELINES.md` del mismo repo exige otro, se respeta el template y la contradicción se anota. No es del agente resolverla.

## Por qué una nota por repo

Un cambio cross-repo son PRs distintos, con templates distintos, tiempos distintos y bloqueantes distintos —típicamente el SDK se libera antes que el consumidor—. Una sola nota mezclada obliga al lector a filtrar qué le toca. Notas separadas, enlazadas entre sí, dicen además el orden de merge.

## Por qué los bloqueantes van arriba

Un bloqueante escondido en un checkbox sin marcar se pierde. Los que se repiten en este equipo son siempre los mismos: versión de prueba con sufijo que todavía no subió a semver real, dependencia downstream sin publicar, base desactualizada respecto de `origin`, trabajo sin commitear, y ruido ajeno en el diff. Van en un callout arriba de todo, con su razón, para que la decisión de "¿esto se puede abrir?" se tome antes de leer el resto.

## Qué NO hace este procedimiento

No crea el PR, no lo abre, no lo pushea, no lo comenta. Produce el texto y nada más. Tampoco es un code review: eso es [[signals-code-review]], y se corre antes, no en vez de esto.

## Procedimiento

- Ejecutar la skill [[pr-description]] con el repo, branch, proyecto y template del repositorio destino; esta nota explica la convención y no duplica la secuencia operativa.

## Validación

- Verificar que la nota resultante vive bajo `10-projects/<Área>/<Proyecto>/`, sigue el template del repo, incluye evidencia observada y deja explícitos los bloqueantes y pruebas realmente ejecutadas.

## Evidencia

- Primera aplicación completa: [[Descripción PR — rio-playmaker]] y [[Descripción PR — rio-sdk-events]] del proyecto [[Crear Context]] (2026-08-24).
