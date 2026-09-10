---
type: learning
scope: project
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Meli]]"
project: "[[Destaques de Precio]]"
application: search-middleware
entities:
  - "[[Meli]]"
related:
  - "[[Destaques de Precio]]"
  - "[[pr-branch-clean-reconstruction]]"
aliases:
  - auditar diff por código de diagnóstico ajeno
  - detectar leftover diagnostics con git log -S
confidence: verified
source_session: "2026-07-01-search-middleware-diagnostic-leftover-cleanup"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - workflow/git
  - workflow/code-review
  - scope/agent
---

# Auditar Diff Por Código De Diagnóstico Ajeno Antes De Cerrar Un PR

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Que una rama esté "limpia" en conteo de archivos (ver [[pr-branch-clean-reconstruction]]) no garantiza que cada archivo tocado solo contenga el delta funcional real. Commits exploratorios/de diagnóstico viejos (ej. `test(search): add motors price drop diagnostics`) pueden dejar código muerto o cambios de comportamiento no relacionados dentro de archivos que sí son legítimamente parte del feature, y sobrevivir intactos a reconstrucciones de rama posteriores porque nadie los mira línea a línea.
- Señales concretas de este tipo de ruido: variables locales que solo repiten una expresión booleana sin ganar claridad (ej. `shouldUsePriceV2 = shouldUsePriceV2Decorator(); return shouldUsePriceV2 && ...`), loggers (`LOGGER`) declarados y nunca usados, o wiring nuevo hacia un método existente que no tiene relación con el objetivo del PR.
- Cuando aparece ruido así, no basta con mirar el diff actual: usar `git log --all --oneline -S"<símbolo o línea sospechosa>" -- <archivo>` para encontrar el commit de origen exacto y confirmar que es ajeno al feature (por mensaje de commit, fecha, o área de negocio).
- La corrección es revertir esos fragmentos a paridad exacta con la rama base (`git diff origin/<base> -- <archivo>` debe quedar vacío o mostrar solo el delta real), incluyendo los tests que ese mismo commit haya agregado o alterado (versiones bumpeadas sin motivo, tests nuevos que validan el comportamiento ruidoso) — no solo el código productivo.
- Regla general: si un cambio en el diff no tiene relación con el objetivo del PR, se revierte, no se "adopta" ni se documenta como aceptado solo porque ya estaba ahí.

## Aplicabilidad

- **Cuándo cargarlo:** antes de responder a un code review humano o de GenAI que señale "cambios innecesarios" o "variables que no tienen sentido"; al revisar un diff de una rama reconstruida o de larga vida antes de mergear; cuando el diff toca un archivo compartido entre el feature actual y otra área de negocio (ej. price drop vs price V2/consumer credits en el mismo archivo).
- **Cuándo no cargarlo:** revisiones de PRs pequeños y recién creados sin historia de reconstrucción, donde el diff completo ya es autoexplicativo.

## Entidades relacionadas

- [[Meli]]
- [[Destaques de Precio]]
- search-middleware

## Evidencia

- Fuente: sesión `2026-07-01-search-middleware-diagnostic-leftover-cleanup`.
- Prueba: `git log --all -S` sobre un `LOGGER` sin uso en `SearchDecoratorRegistryV1.java` apuntó al commit `5996a3af99f4` ("test(search): add motors price drop diagnostics", área ajena Price V2); revertir a paridad con `origin/develop` (incluidos los tests del mismo commit) dejó el archivo sin diff y bajó el PR de 23→22 archivos.
