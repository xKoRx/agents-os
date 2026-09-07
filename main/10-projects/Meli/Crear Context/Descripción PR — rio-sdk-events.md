---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-sdk-events]]"
  - "[[Descripción PR — rio-playmaker]]"
aliases:
  - PR rio-sdk-events component context
  - descripción PR SDK SIG-590
tags:
  - kind/doc
  - project/crear-context
  - application/rio-sdk-events
created: "2026-08-24"
updated: "2026-09-04"
---

# Descripción PR — rio-sdk-events

**PR:** [#46](https://github.com/melisource/fury_rio-sdk-events/pull/46) · **Repo:** `rio-sdk-events` · **Branch:** `feature/component-version-identity` @ `31b674d` · **Base:** `master` @ `8732ee4` · **Release objetivo:** `1.5.0` · **Versión de prueba:** `0.0.2-component-version-identity` · **Suite:** 703 tests, 0 fallas, 0 errores, 0 skipped; JaCoCo y `./gradlew check` PASS

## Propósito

Descripción oficial del Pull Request de `rio-sdk-events` para [[Crear Context]], redactada con [[human-first-technical-writing]] y alineada con el template del repositorio.

## Contenido

---

# ![alt text][description] Descripción del PR

## ¿Cuál es el comportamiento actual?

El contrato `1.4.0` no distingue la definición afectada por la operación de la última versión conocida y transporta `inputs` de componentes relacionados que los control planes no necesitan. Además, su documentación limita el Context al deploy, aunque el mismo mensaje representa deploy y undeploy.

## ¿Cuál es el comportamiento esperado con el nuevo cambio?

La versión objetivo `1.5.0` evoluciona `DeploymentTriggerMessage.context` como un snapshot opcional para deploy y undeploy. La configuración de la operación actual sigue viajando en `DeploymentTriggerMessage.params`, por lo que no se agrega `CurrentVersion`. Actions podrá reutilizar este contrato en una iteración posterior, pero no forma parte de este PR.

```text
ComponentContext
├─ username: String?                 Usuario que inició la operación.
├─ data_product: DataProduct        Data product al que pertenece el componente.
│  ├─ id: Long                        Identificador del data product.
│  ├─ name: String                    Nombre del data product.
│  ├─ team_name: String?              Equipo propietario.
│  └─ environment: String              Atributo de ambiente/modelo del data product.
├─ component: Component              Componente afectado por la operación.
│  ├─ id: Long                        Identificador del componente.
│  ├─ name: String                    Nombre del componente.
│  ├─ type: String                    Tipo usado para rutear al control plane.
│  ├─ version: Long                   Id de la component_definition afectada.
│  └─ latest_version: LatestVersion?  Última versión conocida del componente.
│     ├─ version: Long                Id de su component_definition.
│     ├─ inputs: Inputs               Configuración ingresada por el usuario.
│     └─ outputs: Outputs             Información generada por el control plane.
├─ sources: RelatedComponent[]       Componentes que alimentan al componente actual.
└─ destinations: RelatedComponent[]  Componentes alimentados por el componente actual.

RelatedComponent
├─ id: Long                         Identificador del componente relacionado.
├─ name: String                     Nombre del componente relacionado.
├─ type: String                     Tipo del componente relacionado.
└─ outputs: Outputs                 Información generada por su control plane.

ContextValues
├─ Inputs  -> objeto JSON plano Map<String, String>
└─ Outputs -> objeto JSON plano Map<String, String>
```

`inputs` y `outputs` son tipos Java distintos, pero conservan el objeto JSON plano existente. Las listas y mapas ausentes se normalizan a vacío para mantener compatibilidad durante el rollout.

# ![alt text][testing] Pruebas

## ¿Cómo probar el nuevo comportamiento?

- Ejecutar `./gradlew check`.

- Ejecutar `./gradlew test jacocoTestCoverageVerification`.

- Verificar el round-trip JSON de `ComponentContextTest` y `DeploymentTriggerMessageTest`: `latest_version.inputs` y `latest_version.outputs`, `RelatedComponent.outputs` directo, ausencia de `current`/`CurrentVersion` y compatibilidad del constructor sin Context.

- Resultado local: 703 tests, 0 fallas, 0 errores, 0 skipped; JaCoCo PASS.

# ![alt text][checkmark] Issue relacionado

- [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573) — especificación funcional.

- [SIG-590](https://spellbook.adminml.com/projects/SIG/specs/SIG-590) — especificación técnica.

# ![alt text][checklist] Checklist del PR

- [x] Revisé cuidadosamente el código antes de crear el PR.

- [x] Me aseguré que el `diff` claramente representa mis cambios.

- [x] Me aseguré que este PR no tiene sentido dividirlo en PRs más pequeños.

- [x] Verifiqué que el estilo de mi código y scaffolding adhieran al del proyecto.

- [x] Me aseguré de que mis cambios no afectan otra funcionalidad que no sea la de este PR.

- [x] Agregué/modifiqué los `tests` necesarios para el componente o funcionalidad que estoy implementando.

- [x] Corrí los `tests` y me aseguré de que funcionan.

- [x] Ajusté el fichero `CHANGELOG.md` con el cambio en `[Unreleased]` y la release objetivo `1.5.0`.

- [x] Me aseguré de modificar el README con el nuevo comportamiento, en caso de que aplique. No aplica: el contrato queda documentado en Javadoc y changelog.

[description]: https://img.icons8.com/material-sharp/24/000000/document.png
[checkmark]: https://img.icons8.com/material-sharp/24/000000/checkmark.png
[checklist]: https://img.icons8.com/material-sharp/24/000000/check-all.png
[testing]: https://img.icons8.com/material-sharp/24/000000/test-partial-passed.png
