---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[rio-playmaker]]"
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[SPEC técnica — Slice 4 — Relaciones y pipelines]]"
aliases: []
tags:
  - kind/doc
created: "2026-09-23"
updated: "2026-09-30"
---

# Descripción PR — rio-playmaker — Slice 4

`rio-playmaker` · branch `feature/operation-authorization-by-team-f4@99c51fe8b` · base `develop@0c9e9e3ee` · 53 commits · 53 files changed, 1724 insertions(+), 393 deletions(-) · SIG-616/SIG-621 · sin dependencias nuevas entre repos · suite y stacks locales PASS el 2026-09-30.

> [!warning] Pendientes
> **Aprobación humana, sub-SPEC formal y smoke no productivo.** dependencies FAIL; los demás checks publicados pasaron. GitHub `MERGEABLE` / `BLOCKED` / `REVIEW_REQUIRED`. La excepción sin equipo conserva el riesgo reconocido por el reviewer y aceptado expresamente por el owner.

## Propósito

Guardar la descripción verificable del PR como recurso de la iniciativa y publicar su contrato final autorizado.

## Contenido

---

## Descripción

feat(sig-616): autorización de operaciones de relaciones, pipeline y borrado en cascada

Fase 4 de SIG-616: agrega autorización configurable a nueve operaciones existentes. El control nuevo se activa por un par exacto de configuración cuando el DP tiene equipo y proyecto completos.

- **Relaciones:** crear/actualizar exige extremos del mismo DP. Eliminar permite limpiar relaciones cross-DP históricas, aplicando los controles configurados de cada responsable persistido antes de modificar la relación; una denegación o falla de ACME impide el borrado.
- **Pipeline:** protege reemplazo de topología, diseño, relaciones, creación de componentes y despliegue con `DEV_AND_UP`.
- **Cascada:** exige `DEPLOYER_AND_UP` para el responsable completo y conserva el excepción histórico de plataforma. Con equipo y sin proyecto, mantiene la comprobación heredada de pertenencia al equipo.
- **Validación local:** corrige el orden CHECK/DROP del bootstrap y la detección de puerto Jetty/Tomcat; OpenAPI se genera desde las anotaciones.

**Excepción acordada:** sin `teamName`, el borrado del DP omite ambos controles ACME. Un usuario autenticado sin permisos puede borrar si pasan los restricciones previas y validaciones de estado. El responsable acepta este riesgo para F4, sin exigir regularización masiva de DPs. [Decisión documentada](https://github.com/melisource/fury_rio-playmaker/pull/1181#discussion_r4146982952).

**Pendientes:** falló el check remoto de dependencias; build, cobertura, análisis estático y workflow pasaron. Faltan aprobación humana, sub-SPEC formal y pruebas de humo no productivas.

## Lista del desarrollador

- [x] Código, documentación, escenarios y manifiesto actualizados; cambios publicados en `99c51fe8b`.
- [x] Revisión propia, commits convencionales y sincronización con `develop`, sin conflictos.
- [x] Pruebas locales y limpieza de recursos verificadas.
- [ ] Definición de terminado y todos los checks remotos completos.
- [ ] Despliegue y pruebas de humo en preproducción.

## Revisión de código

- [ ] Aprobación humana del alcance y la implementación.

## Pruebas realizadas

- `./gradlew check jacocoTestReport --offline --no-daemon` — L0/UNIT + H2_INTEGRATION: 4.129 pruebas, cero fallas, dos omisiones preexistentes; cobertura de líneas 97,19%.
- `./scripts/run-agentic-testing-contract.sh` — 53 selectores y tres checks L0/LOCAL_STACK aprobados, con limpieza certificada.

## Contrato de pruebas

`.testing/impact.json` y el catálogo incluyen AT-050-S16 (limpieza cross-DP histórica) y AT-000-S10 (bootstrap y puerto local). La evidencia local no sustituye las pruebas de humo remotas. Zord omitido por instrucción del responsable; sin despliegue.

## Referencias

[SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) · [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621).

---

## Notas internas — NO van al PR

- D25: create/update conservan same-DP; delete admite limpieza histórica aplicando guards de owners persistidos distintos. D26: se mantiene explícitamente la excepción sin equipo y su riesgo, sin exigir backfill masivo. La SPEC local quedó alineada; no se afirma aprobación formal de Spellbook.
- La descripción y las respuestas de GitHub se actualizaron por autorización explícita del owner. Los hilos se resolvieron por fix probado o decisión documentada; la resolución no equivale a aprobación del reviewer.
- El merge de develop preservó escenarios y tests de ambas ramas. Se reparó el runner local sin alterar las migraciones SQL; también se corrigió su descubrimiento de puerto Jetty. Swagger deriva de las anotaciones y refleja la regla real de importación.

- El 2026-09-30 el owner pidió descripción en español y sintetizada. Se tradujeron las secciones y se agruparon los checklists del template por esa instrucción explícita; se conservaron alcance, excepción/riesgo, evidencia y pendientes reales.
