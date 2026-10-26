# Rio sunset update — reporte de ejecución

Todos los campos se llenan con valores observados durante la corrida. Nunca se emite un PR, un scope o un deployment ID planeado, supuesto o de relleno. Si una fase se detuvo antes, en lugar de sus valores va el motivo de la detención. Una corrida sin sunsets elegibles no genera reporte.

- Proyecto (nombre exacto de la aplicación en Fury): `<proyecto>`
- Ejecutado el: `<ISO-8601 con offset>`
- Horizonte de elegibilidad (sólo límite superior; el día de ejecución cuenta como día 1): todo lo que vence en o antes de `<fin ISO-8601 con offset>`, **incluidos los sunsets ya vencidos**
- Horizonte elegido por: `<la persona, entre N opciones>` / `<default aplicado, persona no disponible>`
- Zona horaria usada: `<zona IANA y offset>`
- Versión del artefacto inspeccionada: `<versión>`
- Checkout: `<preexistente | clonado durante la corrida>` en `<ruta>`
- Vencidos encontrados: `<n>` · En horizonte: `<n>` · Más allá del horizonte: `<n>`
- **Desenlace: `<NOTHING_ELIGIBLE | ALL_IN_FLIGHT | ACTION_REQUIRED | APPLIED | APPLIED_NO_DEPLOY | REDEPLOY_ONLY | STOPPED | MIGRATION_UNVERIFIED>`**
- Si es `ACTION_REQUIRED`: `<qué necesita decisión, el plazo más cercano, y si ya pasó>`
- Modo: `<normal | --attempt-migration>`

## Intento de migración

Se completa sólo cuando la corrida usó `--attempt-migration`. Si el desenlace es `MIGRATION_UNVERIFIED`, esta sección abre con el aviso, sin suavizarlo:

> No fue posible completar la actualización. Se hicieron 3 intentos y los 3 fallaron. Esta no es una
> actualización de versión: es una migración crítica que necesita atención humana dedicada.

| Intento | Cambio aplicado | Etapa que falló | `type_error` | Diagnóstico |
| --- | --- | --- | --- | --- |
| 1 | `<gestor y versión>` | `<etapa>` | `<valor>` | `preciso` / `grueso — sólo etapa y type_error` |
| 2 | `<gestor y versión>` | `<etapa>` | `<valor>` | `preciso` / `grueso` |
| 3 | `<gestor y versión>` | `<etapa>` | `<valor>` | `preciso` / `grueso` |

- Pull request: `<url>` — **draft, marcado como no verificado; el merge es decisión de una persona**
- Si ningún build terminó: deploy **no realizado**, y el sunset sigue sin resolverse conservando su fecha — `<componente>`, vence `<fecha>`
- Si un build terminó: la corrida siguió con todas las fases restantes, y el deploy a test aparece en su sección. **Que compile y corra en test no prueba que esté listo para productivo**: un build verde y un scope de test sano no cubren todos los caminos de runtime

## Sunsets mapeados

Todo sunset encontrado dentro del horizonte, se haya podido actualizar o no. Las filas `vencido` van primero.

| Bucket | ID del sunset | Componente/dependencia | Fecha de vencimiento | Versión anterior | Versión objetivo | Resultado | Gobernado por | Evidencia |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `vencido` / `en horizonte` | `<id>` | `<componente>` | `<ISO-8601 con offset>` | `<anterior>` | `<objetivo>` | `aplicado` / `sólo redeploy` / `ya en curso` / la clasificación que lo bloqueó | `<artefacto @ versión declarada, para las filas bloqueadas>` | `<referencia>` |

Para las filas `sólo redeploy`: el código ya satisface el objetivo y el sunset viene de artefactos viejos todavía desplegados. Se indica qué versión declara el manifest y qué scopes están afectados.

| ID del sunset | Componente | Versión que ya declara el manifest | Scopes afectados | Scopes desplegados por la skill | Scopes que requieren una persona (productivos o stage) |
| --- | --- | --- | --- | --- | --- |
| `<id>` | `<componente>` | `<versión>` | `<scopes>` | `<scopes>` | `<scopes>` |

## Ya en curso — excluidos del lote

Sunsets elegibles que otro trabajo ya está resolviendo. Se listan para que se vea que fueron vistos y omitidos a propósito, no olvidados. No se editaron, no se commitearon, y no contaron para decidir si valía abrir un PR.

| ID del sunset | Componente/dependencia | Fecha de vencimiento | Lo maneja | Ese trabajo lo lleva a |
| --- | --- | --- | --- | --- |
| `<id>` | `<componente>` | `<fecha>` | `<número de PR o branch>` | `<versión>` |

## Sunsets con fecha más allá del horizonte

Sólo informativo, para que nada con fecha quede invisible. Se listan todos, sin truncar.

| ID del sunset | Componente/dependencia | Fecha de vencimiento | Versión actual | Versión objetivo | Días hasta el vencimiento |
| --- | --- | --- | --- | --- | --- |
| `<id>` | `<componente>` | `<fecha>` | `<actual>` | `<objetivo>` | `<n>` |

## Cambio aplicado

- Archivos modificados: `<archivos>`
- Comandos nativos del proyecto ejecutados: `<comandos tomados de la configuración versionada del proyecto>`
- Resultados de validación: `<build/tests/lint/typecheck>`

## Pull request

Un solo pull request lleva todo el lote aplicado de este proyecto.

| Campo | Valor |
| --- | --- |
| Pull request | `<url o número>` |
| Reutilizó un PR abierto existente | `<sí | no>` |
| Branch base | `<leída del repositorio>` |
| Prefijo de branch usado | `<leído de las branches del repositorio>` |
| IDs de sunset aplicados | `<ids>` |
| SHA del commit del PR | `<sha>` |
| Build inmutable para ese SHA | `<id del build>` |

## Deploy a test

Si la aplicación no tiene ningún scope (una librería o un SDK), esta sección se reemplaza completa por el bloque siguiente y **no** se rellena la tabla: no hubo scope que pedir ni deploy que hacer, y eso no es un fallo.

> **Sin scope desplegable.** `<proyecto>` no tiene scopes en Fury, así que no existe ningún entorno
> propio al que desplegar. El cambio queda validado por build y tests, y el pull request es el
> entregable completo de esta corrida. Su efecto real se comprueba cuando las aplicaciones que
> consumen esta librería adopten la versión nueva: conviene avisar a quien la consuma, porque el
> alcance de un cambio en una librería es mayor que el de un servicio.

| Campo | Valor |
| --- | --- |
| Scope pedido por la persona | `<scope>` |
| `criticality` del scope, resuelta en modo lectura | `test` |
| Verificación de pertenencia | `pertenece a <proyecto>` |
| Señales contradictorias encontradas | `ninguna` |
| ID del pipeline | `<id>` |
| ID del deployment | `<id>` |
| Versión desplegada | `<build>` |
| Estado final del pipeline | `completed, 100%` |
| Estado final del deployment | `finished`, `active: false` (scope liberado) |
| Finish ejecutado | `sí` |

No se realizó ningún deploy productivo, promoción, finish sobre productivo, terminación instantánea ni auto-merge, y no se guardó ningún scope por defecto.

## Destino del documento

| Campo | Valor |
| --- | --- |
| Ruta local | `<ruta absoluta>` |
| Drive | `subido a "Sunsets history"` / `carpeta creada y subido` / `sin permiso configurado, sólo local` / `la persona declinó configurarlo` |

## Notas y bloqueos

- `<notas por fase, motivos de detención, o "ninguno">`

Nunca se incluyen en este documento credenciales, tokens ni respuestas crudas de las fuentes.
