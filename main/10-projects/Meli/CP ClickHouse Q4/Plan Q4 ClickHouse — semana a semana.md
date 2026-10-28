---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[CP ClickHouse Q4]]"
  - "[[Roadmap Q4 — CP ClickHouse]]"
aliases:
  - Plan semanal ClickHouse Q4
  - Plan Q4 ClickHouse para Flor
tags:
  - kind/doc
  - area/meli
  - app/rio-controlplane-clickhouse
created: "2026-10-28"
updated: "2026-10-28"
---

# Plan Q4 ClickHouse — semana a semana

## Propósito

Propuesta de calendario para el backlog de ClickHouse de Q4, para revisarla entre Rodrigo y Flor. Solo incluye ítems de la planilla, con sus responsables. Las estimaciones en días son una primera pasada.

## Contenido

### Resumen

- **Refreshable:** deprovision y start/stop ya están en `master` (CP #346 y #356). El import está desarrollado y certificado E2E; falta la última prueba.
- **Asignación:** se respeta la de la planilla. Lo que no tenía dueño se repartió para equilibrar la carga: vista normal a Rodrigo (es el mismo mecanismo de import) y Dictionary a Flor.
- **Estamos justos:** P0, P1 y P2 (sin Control) suman ≈ 55 días contra ≈ 56 disponibles entre los dos. No hay holgura.
- **Quedan fuera:** Control (no está definido) y multi-source (P3).

### Por qué estamos justos

- **Disponibilidad:** del 28-oct al 23-dic hay ≈ 40 días hábiles por persona, sin contar el 8-dic ni la semana del 24 al 31. Con un 30 % del tiempo en soporte, reviews y otros temas, quedan **≈ 28 días por persona, ≈ 56 entre los dos**.
- **Carga:** P0 + P1 + P2 suman **≈ 55 días**.
- **Riesgo:** cualquier imprevisto empuja primero a Dictionary, que es lo último de la fila. Los tres puntos con más riesgo de crecer son:
  - la API key de observabilidad y el contrato de aprobación del warehouse, porque dependen de terceros;
  - qué significa "migraciones" en la creación de base de datos;
  - qué es exactamente la lib de consumo.

### Desarrollos

Días hábiles de una persona, con tests incluidos.

**Rodrigo**

| Ítem de la planilla | Prioridad | Talla | Días | Nota |
|---|---|---|---|---|
| Import refreshable view | P0 | XL | 1 | Ya desarrollado: última prueba + push de PM (#1332 ya está mergeado) |
| Import refreshable view — credenciales | P0 | S | 0,5 | Pedir user/pass a los owners y cargarlos en el endpoint de precarga; el resto es espera |
| Cambio permisos de admin | P0 | N/A | 2 | Definir el nivel y aplicarlo |
| Context v2 — credenciales sin duplicidad | P0 | M | 4 | Devolver las keys en los ALTER de MergeTree, MV y RMV |
| Lib de consumo de permisos | P0 | N/A | 6 | Falta definir si es SDK, endpoint o UI |
| Implementación de lib (soporte) | P1 | N/A | 2,5 | — |
| Provision normal view | P1 | M | 4 | Antes, ver cuántos la usan en prod fuera de RIO (nota de la planilla) |
| Deprovision normal view | P1 | M | 1,5 | Reutiliza el `DROP VIEW` de las MV |
| Start-stop normal view | P2 | S | 1 | — |
| Import normal view | P2 | L | 3 | Reutiliza `ImportMatViewCommand` |
| Import normal view — credenciales | P2 | XL | 2 | Reutiliza la precarga; si es XL por el volumen de usuarios, es tiempo de espera |
| **Total** | | | **≈ 27,5** | |

**Flor**

| Ítem de la planilla | Prioridad | Talla | Días | Nota |
|---|---|---|---|---|
| Warehouse provision — recibir la request y validar | P0 | — | 1 | — |
| Warehouse provision — orquestar el comando de warehouse + service | P0 | — | 2 | — |
| Warehouse provision — armado de request + creación de infra + response | P0 | — | 3 | — |
| Warehouse provision — agregar componente a Playmaker | P0 | — | 1 | — |
| Warehouse provision — manejo de logs de error | P0 | — | 1 | — |
| Warehouse provision — observabilidad / API key | P0 | — | 1 | Depende de un acuerdo pendiente |
| Warehouse provision — creación de base de datos + migraciones | P0 | — | 2 | Falta definir qué son las migraciones |
| Warehouse start-stop | P0 | XL | 3 | Sobre el cliente Cloud que deja el provision |
| Warehouse deprovision | P0 | L | 4 | La planilla lo asigna a "Jarita/flor"; va con Flor porque usa el mismo cliente |
| Dictionary | P2 | N/A | ≈ 10 | Sin diseño; es lo último de la fila |
| **Total** | | | **≈ 28** | |

### Semana a semana

Supuesto: 3,5 días de desarrollo por semana de 5 días hábiles.

| Semana | Rodrigo | Flor | Hito |
|---|---|---|---|
| S1 · 28–30 oct | Cierre del import refreshable · pedido de credenciales · inicio de permisos admin | Provision: validar request · inicio de orquestar · pedir API key y aprobación | — |
| S2 · 2–6 nov | Permisos admin · inicio de Context v2 | Provision: orquestar · armado de request, infra y response | Import refreshable en prod |
| S3 · 9–13 nov | Context v2 · inicio de lib | Provision: cierre de infra · componente en PM · logs · API key | — |
| S4 · 16–20 nov | Lib | Provision: base de datos + migraciones · inicio de start-stop | Context v2 + crear warehouse |
| S5 · 23–27 nov | Cierre de lib · implementación y soporte | Start-stop · inicio de deprovision | Lib de consumo |
| S6 · 30 nov–4 dic | Provision normal view | Cierre de deprovision · inicio de Dictionary | Warehouse completo |
| S7 · 7–11 dic (feriado 8) | Cierre de provision · deprovision · start-stop normal view | Dictionary | — |
| S8 · 14–18 dic | Import normal view | Dictionary | Vista normal (provision, deprovision, start-stop, import) |
| S9 · 21–23 dic | Import normal view — credenciales | Cierre de Dictionary | Cierre y release desde `master` |
| 24–31 dic | Colchón | Colchón | — |

### Fuera del calendario

- **Control (P2):** la planilla no lo describe, así que no se puede estimar.
- **Multi-source (P3, tres ítems):** no entra con dos personas; la estimación es de ≈ 20 días. Como el supuesto de una sola fuente está en el código compartido por los tres tipos de vista, debería resolverse como un solo refactor.

### Hallazgos fuera de la planilla (para decidir si entran)

Salieron de revisar el código y no están en el backlog. Entran solo si se decide reemplazar algo, por ejemplo Dictionary.

- **Salud del refresh (≈ 5 días):** el CP no lee `system.view_refreshes`. Una refreshable cuyo refresh falla se sigue viendo RUNNING.
- **Limpieza al borrar una refreshable importada (≈ 1 día):** el deprovision no borra `import:{user}` de KVS ni revoca el token KMS, y hay un TODO explícito en el código.
- **Import explícito de MergeTree (≈ 5 días):** si la tabla ya existe, `DeployTableDeployment` hace diff y ALTER. Adoptar una tabla externa hoy significa modificarla.

### Para decidir juntos

1. ¿Calza la asignación de lo que no tenía dueño?
2. ¿Entra algún hallazgo en lugar de Dictionary? La salud del refresh parece la de más valor.
3. ¿Qué son las "migraciones" del provision de warehouse y qué es "Control"?
4. ¿Qué forma tiene la lib de consumo: SDK, endpoint o UI?

## Fuentes

- Backlog de la planilla del equipo (2026-10-27).
- Estado del código y estimaciones: [[Roadmap Q4 — CP ClickHouse]].
