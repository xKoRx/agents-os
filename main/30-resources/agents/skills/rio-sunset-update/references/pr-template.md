## Rio sunset update

- Proyecto: `<proyecto>`
- Horizonte de elegibilidad: todo lo que vence en o antes de `<fin ISO-8601 con offset>`, **incluidos los sunsets ya vencidos**
- Horizonte elegido por: `<la persona, entre N opciones>` / `<default aplicado>`
- Estado de la fuente: `<verificada | bloqueada>`

Este pull request lleva **todas** las actualizaciones de sunset aplicadas para este proyecto, en un solo lote. Hay a lo sumo un pull request de sunsets abierto por proyecto: una nueva corrida actualiza este en lugar de abrir otro.

### Aplicado en este PR

Las filas marcadas `vencido` ya habían pasado su plazo, así que los builds que las usaban ya estaban bloqueados. Van listadas primero.

| Bucket | ID del sunset | Componente/dependencia | Fecha de sunset | Versión anterior | Versión objetivo | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| `vencido` / `en horizonte` | `<id>` | `<componente>` | `<fecha>` | `<anterior>` | `<objetivo>` | `<referencia>` |

### Ya en curso — excluidos de este PR

Sunsets elegibles que otro trabajo ya está resolviendo, así que este PR no los toca.

| ID del sunset | Componente/dependencia | Fecha de sunset | Lo maneja | Ese trabajo lo lleva a |
| --- | --- | --- | --- | --- |
| `<id>` | `<componente>` | `<fecha>` | `<número de PR o branch>` | `<versión>` |

### Encontrado y no aplicado — necesita una decisión humana

Están dentro del horizonte pero no se declaran con una versión literal en el manifest, así que no existe una actualización mecánica. Cada fila dice por qué.

| ID del sunset | Componente/dependencia | Fecha de sunset | Versión actual | Versión objetivo | Clasificación | Gobernado por (artefacto y versión declarada) | Evidencia |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<id>` | `<componente>` | `<fecha>` | `<actual>` | `<objetivo>` | `<gobernado por BOM / gobernado por plugin de build / sólo transitivo / objetivos en conflicto / versión objetivo inexistente>` | `<artefacto @ versión, según el manifest, o "no identificable desde el manifest">` | `<referencia>` |

Para cada fila, se cita la línea del manifest que declara al gestor, y el idioma de override que el proyecto ya use si tiene uno. No se afirma qué versión del gestor resolvería el sunset salvo que eso haya sido verificado.

### Cambio y validación

- Archivos modificados: `<archivos>`
- Comandos nativos del proyecto ejecutados: `<comandos tomados de la configuración versionada del proyecto>`
- Resultados: `<build/tests/lint/typecheck>`
- SHA del commit del PR: `<sha>`
- Build inmutable para ese SHA: `<build>`

Este PR no solicita ningún deploy. La selección del scope de test y la confirmación final son pasos aparte y explícitos, posteriores a que el build inmutable esté listo.

Si la aplicación no tiene scopes en Fury — una librería o un SDK — agregá en su lugar:

> **Sin deploy de prueba.** `<proyecto>` no tiene scopes, así que no hay entorno propio al que
> desplegar: la validación de este PR es el build y los tests. El comportamiento en runtime se
> verifica cuando las aplicaciones que consumen la librería adopten la versión nueva.
