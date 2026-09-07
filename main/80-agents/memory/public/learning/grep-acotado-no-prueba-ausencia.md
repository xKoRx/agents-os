---
type: learning
schema_version: 1
scope: global
created: "2026-08-25"
updated: "2026-08-25"
area:
project:
application:
entities: []
related:
  - "[[signals-code-review]]"
  - "[[rjara-agent-profile]]"
aliases:
  - un grep acotado no prueba ausencia
  - negativo parcial en code review
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
  - action/code-review
---

# Un `grep` acotado no prueba que algo no exista

## Aprendizaje

Un finding de code review que afirma "esta forma de dato no existe" o "este símbolo no se usa" necesita cubrir **a los productores**, no sólo a los consumidores. Buscar en `src/main` y concluir que un wrapper no existe es un negativo parcial: los productores pueden vivir en tests, fixtures, migraciones, seeds, o directamente en otro repo. En un ecosistema como RIO, donde un control plane escribe el dato que otro servicio lee, el productor casi nunca está en el repo que se está revisando.

La regla operativa: antes de reportar una ausencia, buscar en `src/test`, `src/*/resources`, `scripts/`, migraciones y los repos que consumen o producen el artefacto. Si no se puede cubrir todo eso, el finding se degrada de "no existe" a "no encontré productor en X", que es una afirmación distinta y honesta.

## Aplicabilidad

- **Cuándo cargarlo:** al hacer code review, buscar código muerto, o justificar la eliminación de una rama, un campo o un símbolo por "no tiene uso".
- **Cuándo no cargarlo:** trabajo que no argumenta desde una ausencia.

## Entidades relacionadas

- [[signals-code-review]] — §2 ya exige verificar código muerto por búsqueda y no por impresión; esto precisa qué tiene que cubrir esa búsqueda.

## Evidencia

Revisión de `feature/new-component-context` en [[rio-playmaker]], 2026-08-25. Se reportó como finding que el unwrap de `{"value": …}` en el resolver de outputs era especulativo, porque `grep sensitive src/main` no devolvía nada relevante. El wrapper `{type, value, sensitive}` sí existe: lo produce el control plane, aparece en `DestinationParseServiceImplTest`, y desenvolverlo replica un patrón ya establecido en `ParameterParseServiceImpl`. El finding era falso y, de haberse aplicado, habría roto la resolución de outputs.
