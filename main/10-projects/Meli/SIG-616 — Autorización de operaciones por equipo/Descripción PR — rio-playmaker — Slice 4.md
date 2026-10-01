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
updated: "2026-10-01"
---

# Descripción PR — rio-playmaker — Slice 4

`rio-playmaker` · branch `feature/operation-authorization-by-team-f4@226f21fb1` · base `develop@dc56a3de4` · SIG-616/SIG-621 · 64 selectores, suite y tres stacks locales PASS el 2026-10-01.

> [!warning] Pendientes
> **Aprobación humana, sub-SPEC formal y smoke no productivo.** Nueva CI iniciándose. Conflictos resueltos; MERGEABLE. La evidencia anterior del reporte de dependencias corresponde a los SHA investigados, no al resultado final de la CI nueva.

## Propósito

Guardar la descripción verificable del PR como recurso de la iniciativa y publicar su contrato final autorizado.

## Contenido

---

## Descripción

feat(sig-616): autorización de operaciones de relaciones, pipeline y borrado en cascada

Fase 4 de SIG-616: agrega autorización configurable a nueve operaciones existentes. El control nuevo se activa por un par exacto de configuración cuando el DP tiene equipo y proyecto completos.

- **Relaciones:** crear/actualizar exige extremos del mismo DP. Eliminar permite limpiar relaciones cross-DP históricas, aplicando los controles configurados de cada responsable persistido antes de modificar la relación; una denegación o falla de ACME impide el borrado.
- **Pipeline:** protege topología, diseño, relaciones, creación y despliegue con `DEV_AND_UP`; conserva el guard antes de la herencia signal→Kafka incorporada desde develop, con auditoría de la identidad autenticada.
- **Cascada:** exige `DEPLOYER_AND_UP` para el responsable completo y conserva la excepción histórica de plataforma. Con equipo y sin proyecto, mantiene la comprobación heredada de pertenencia al equipo.
- **Validación local:** corrige el orden CHECK/DROP del bootstrap y la detección de puerto Jetty/Tomcat; OpenAPI se genera desde las anotaciones.

**Excepción acordada:** sin `teamName`, el borrado del DP omite ambos controles ACME. Un usuario autenticado sin permisos puede borrar si pasan las restricciones previas y validaciones de estado. El responsable acepta este riesgo para F4, sin exigir regularización masiva de DPs. [Decisión documentada](https://github.com/melisource/fury_rio-playmaker/pull/1181#discussion_r4146982952).

**Pendientes:** CI del nuevo HEAD en curso. El nodo de dependencias reproduce un fallo de flags SBOM; Fury informa nueve avisos bajos y ninguno bloqueante en la ejecución investigada. Faltan aprobación humana, sub-SPEC formal y pruebas de humo no productivas.

## Lista del desarrollador

- [x] Código, documentación, escenarios y manifiesto actualizados; cambios publicados en `226f21fb1`.
- [x] Revisión propia, commits convencionales y sincronización con `develop`, sin conflictos.
- [x] Pruebas locales y limpieza de recursos verificadas.
- [ ] Definición de terminado y todos los checks remotos completos.
- [ ] Despliegue y pruebas de humo en preproducción.

## Revisión de código

- [ ] Aprobación humana del alcance y la implementación.

## Pruebas realizadas

- `./gradlew check jacocoTestReport --offline --no-daemon` — L0/UNIT + H2_INTEGRATION: 4.195 pruebas, cero fallas, dos omisiones preexistentes; cobertura de líneas 97,21%.
- `./scripts/run-agentic-testing-contract.sh` — 64 selectores y tres checks L0/LOCAL_STACK aprobados, con cleanup certificado, sobre el merge de `develop@dc56a3de4`.

## Contrato de pruebas

`.testing/impact.json` y el catálogo incluyen AT-050-S16 (limpieza cross-DP histórica), AT-000-S10 (bootstrap y puerto local) y AT-090-S21 (guard antes de herencia). La evidencia local no sustituye las pruebas de humo remotas. Zord omitido por instrucción del responsable; sin despliegue.

## Referencias

[SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) · [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621).
