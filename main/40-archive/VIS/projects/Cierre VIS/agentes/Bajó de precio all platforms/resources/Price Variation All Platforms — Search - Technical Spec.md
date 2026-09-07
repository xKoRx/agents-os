# Price Variation All Platforms — Search - Technical Spec

**Owner**: Sebastian Calderon
**Created**: 2026-07-22
**Last Updated**: 2026-07-22
**Based on**: https://spellbook.adminml.com/projects/VMDEM/specs/1c9f4d16-60de-4a8d-9437-820b20a043f4

---

## Spec Reference Annotations

<!-- extends: fury_search-middleware PR#13976 — bajó de precio Motors nativo -->
<!-- extends: fury_search-middleware PR#13767 — refactor drop price RES all platforms -->

---

## Executive Summary

Extensión del feature "Bajó de precio" para Motors a todas las plataformas (Desktop, WebMobile, nativo) en `fury_search-middleware`, delegando el control de plataforma al experimento `vis/item-dropprice-motors` configurado en Fury.

Actualmente Motors tiene tres restricciones de plataforma en código:

1. `PriceDropMotorsExperimentTask.isExperimentApplicable()` — la task solo evalúa si `polycardSingleMotorsExperiment` está activo (nativo-only).
2. `PriceDropExperimentHelper.isPriceDropExperimentActive()` — chequea `polycardSingleMotorsExperiment` para Motors, bloqueando web.
3. `PriceDecoratorFactory.shouldShowPriceDropLabel()` — rama web excluye Motors.
4. `PriceDecoratorFactory.isPriceDropGovernedItem()` — excluye Motors del gate de experimento para el precio tachado.

Los cuatro se eliminan. La audiencia por plataforma queda en la consola de Fury Experiments.

---

## Architecture Overview

```
Request (cualquier plataforma)
    └── SearchController
          ├── PriceDropMotorsExperimentTask
          │     ├── [HOY] isExperimentApplicable → gate: polycardSingleMotors (nativo-only)
          │     └── [POST] isExperimentApplicable → siempre true (Fury controla audiencia)
          └── PriceDecoratorFactory
                ├── isPriceDropGovernedItem()
                │     ├── [HOY] solo RES → tachado Motors sin gate
                │     └── [POST] RES + Motors → tachado gateado por experimento
                ├── shouldShowCrossedOutPrice()
                │     └── → PriceDropExperimentHelper.shouldShowPriceDropFeatures()
                │             └── isPriceDropExperimentActive()
                │                   ├── [HOY] Motors: polycardSingle && priceDropMotors.show
                │                   └── [POST] Motors: priceDropMotors.show (independiente)
                └── shouldShowPriceDropLabel()
                      ├── [HOY] !isNative → solo RES
                      └── [POST] !isNative → RES || (Motors && shouldShowPriceDropFeatures)
```

---

## Fury Services Used

Ninguno nuevo. Control de plataforma delegado al experimento `vis/item-dropprice-motors` en Fury Experiments — configurar audiencia para incluir Desktop y WebMobile.

---

## Design Decisions

### DD-1: Delegar control de plataforma a Fury Experiments

**Context**: El código actual restringe Motors a nativo en tres puntos distintos. Para extender a todas las plataformas, el código no debe evaluar plataforma — esa responsabilidad pasa al experimento.

**Decision**: Eliminar los gates de plataforma del código. Fury Experiments controla la audiencia.

**Rationale**: Consistente con el objetivo de la iniciativa ("quitar la restricción de plataforma del código"). Permite activar/desactivar plataformas sin deploy.

---

### DD-2: Independencia de `polycardSingleMotorsExperiment`

**Context**: `PriceDropMotorsExperimentTask` y `isPriceDropExperimentActive` encadenan `polycardSingleMotorsExperiment` como prerequisito. Ese experimento es nativo-only → bloquea price drop en web.

**Decision**: Remover el check de `polycardSingleMotorsExperiment` de ambos. `vis/item-dropprice-motors` evalúa y activa de forma independiente en todas las plataformas.

**Rationale**: `polycardSingleMotorsExperiment` controla el renderizado del polycard de Motors; si está apagado, no hay card donde mostrar el label de todas formas. El gate en código es redundante para nativo y bloqueante para web.

---

## Data Model

No aplica.

---

## REST API Contracts

Sin cambios. `discount_label` y `crossed_out_price` ya existen en el contrato.

---

## Security

Sin cambios.

---

## Performance

Sin impacto. No se agregan llamadas externas.

---

## Testing Strategy

### Unit Tests

**Coverage target**: ≥85% líneas nuevas/modificadas.

**Archivo principal**: `PriceDecoratorFactoryTest`

**Casos nuevos — Label (`shouldShowPriceDropLabel`)**:

| Escenario | Platform | Vertical | PriceDrop exp | hasPriceVariation | Esperado |
|-----------|----------|----------|--------------|-------------------|----------|
| Motors Desktop, experimento activo | Desktop | MOTORS | show=true | true | label visible |
| Motors WebMobile, experimento activo | WebMobile | MOTORS | show=true | true | label visible |
| Motors Desktop, experimento apagado | Desktop | MOTORS | show=false | true | sin label |
| Motors Desktop, sin hasPriceVariation | Desktop | MOTORS | show=true | false | sin label |
| RES web no regresiona | Desktop | REAL_ESTATE | show=true | true | label visible |

**Casos nuevos — Precio tachado (`isPriceDropGovernedItem` / `shouldShowCrossedOutPrice`)**:

| Escenario | Vertical | PriceDrop exp | hasPriceVariation | Esperado |
|-----------|----------|--------------|-------------------|----------|
| Motors, experimento activo | MOTORS | show=true | true | tachado visible |
| Motors, experimento apagado | MOTORS | show=false | true | sin tachado |
| Motors, sin hasPriceVariation | MOTORS | show=true | false | sin tachado |
| RES no regresiona | REAL_ESTATE | show=true | true | tachado visible |

**Archivo secundario**: `PriceDropMotorsExperimentTaskTest` — verificar que la task evalúa en Desktop/WebMobile sin gate de `polycardSingleMotors`.

**Archivo secundario**: `PriceDropExperimentHelperTest` — verificar `isPriceDropExperimentActive` para Motors sin `polycardSingleMotors`.

---

## Deployment Strategy

**Rollout**: vía `vis/item-dropprice-motors` en Fury Experiments.
- Deploy sin cambios de audiencia.
- Para activar en web: agregar Desktop y WebMobile a la audiencia del experimento.
- Rollback: reducir audiencia en Fury, sin revert de código.

---

## Observability

Sin nuevas métricas. Validar en consola de Fury Experiments segmentando por plataforma.

---

## Code Ownership Map

| Component | Role | Archivos primarios | Archivos de soporte |
|-----------|------|--------------------|---------------------|
| Experiment task | Task | `PriceDropMotorsExperimentTask.java` | `PolycardSingleMotorsExperimentTask.java` |
| Experiment active check | Helper | `PriceDropExperimentHelper.java` | — |
| Label + tachado logic | Service | `PriceDecoratorFactory.java` | `PriceDropExperimentHelper.java` |
| Tests | Test | `PriceDecoratorFactoryTest.java` | `PriceDropMotorsExperimentTaskTest.java`, `PriceDropExperimentHelperTest.java` |

---

## Implementation Locations

| # | Cambio | Archivo | Método |
|---|--------|---------|--------|
| 1 | Remover gate `polycardSingleMotors` de la task | `PriceDropMotorsExperimentTask.java` | `isExperimentApplicable()` — eliminar override |
| 2 | Remover `polycardSingleMotors` del check de Motors | `PriceDropExperimentHelper.java` | `isPriceDropExperimentActive()` |
| 3 | Label Motors en web | `PriceDecoratorFactory.java` | `shouldShowPriceDropLabel()` |
| 4 | Tachado Motors gateado por experimento | `PriceDecoratorFactory.java` | `isPriceDropGovernedItem()` |

**Diffs esperados**:

```java
// 1. PriceDropMotorsExperimentTask — eliminar dependency + isExperimentApplicable()
- @TaskDependency(PolycardSingleMotorsExperimentTask.class)
- public Observable<SearchBaseExperimentModel> polycardSingleMotorsExperimentTask;

- @Override
- protected Observable<Boolean> isExperimentApplicable() {
-     return polycardSingleMotorsExperimentTask.map(SearchBaseExperimentModel::isActive);
- }
// La task hereda el default (always true). Fury Experiments controla la audiencia.

// 2. PriceDropExperimentHelper.isPriceDropExperimentActive() — Motors
  if (isMotorsItem(polycardItem)) {
-     return SearchBaseExperimentModel.isActive(model.polycardSingleMotorsExperiment)
-             && nonNull(model.priceDropMotorsExperiment)
-             && model.priceDropMotorsExperiment.show;
+     return nonNull(model.priceDropMotorsExperiment)
+             && model.priceDropMotorsExperiment.show;
  }

// 3. PriceDecoratorFactory.shouldShowPriceDropLabel() — branch web
  if (!device.isNative()) {
-     return isRealEstate(polycardItem);
+     ItemModelBase itemModelBase = getItemModelBase(polycardItem);
+     return isRealEstate(polycardItem)
+         || (PriceDropExperimentHelper.isMotorsItem(polycardItem)
+             && PriceDropExperimentHelper.shouldShowPriceDropFeatures(model, polycardItem, itemModelBase));
  }

// 4. PriceDecoratorFactory.isPriceDropGovernedItem()
  private boolean isPriceDropGovernedItem(PolycardItem polycardItem) {
-     return isRealEstate(polycardItem);
+     return isRealEstate(polycardItem) || PriceDropExperimentHelper.isMotorsItem(polycardItem);
  }
```

---

## Custom Implementations

No aplica — el feature extiende lógica existente sin componentes construidos desde cero.

---

## Existing Data & Migrations

No aplica — sin cambios en persistencia ni modelos de datos.

---

## Dependencies

### Internas
- **`vis/item-dropprice-motors`** (Fury Experiments): experimento existente — requiere configuración de audiencia para incluir Desktop y WebMobile antes del rollout en web.
- **`PolycardSingleMotorsExperimentTask`**: se desacopla como prerequisito de `PriceDropMotorsExperimentTask`; sigue existiendo y siendo evaluado por otras features.

### Externas
Ninguna.

---

## Complexity Analysis

### Component Breakdown

| Componente | Complejidad | Dependencias |
|------------|-------------|--------------|
| `PriceDropMotorsExperimentTask` — remover dependency + override | Baja | — |
| `PriceDropExperimentHelper` — remover gate polycardSingle | Baja | Task anterior |
| `PriceDecoratorFactory` — label + tachado web | Baja | Helper |
| Unit tests | Media | Todos los cambios anteriores |

### Estrategia de ejecución
Cambios secuenciales en un único PR. Sin paralelización necesaria — superficie reducida, sin infraestructura nueva.

---

## Technical Risks

| Risk ID | Description | Impact | Probability | Mitigation |
|---------|-------------|--------|-------------|------------|
| TECH-1 | Regresión tachado RES web | Medio | Bajo | Test explícito no-regresión RES |
| TECH-2 | Price drop Motors activo cuando polycard está apagado en nativo | Bajo | Bajo | Si polycard está apagado no hay card donde renderizar — sin impacto visual |

---

## Open Questions

Ninguna bloqueante.

---

## References

- Functional spec: VMDEM-21
- Referencia Motors nativo: fury_search-middleware PR #13976
- Referencia RES all platforms: fury_search-middleware PR #12851
- Referencia RES refactor: fury_search-middleware PR #13767
