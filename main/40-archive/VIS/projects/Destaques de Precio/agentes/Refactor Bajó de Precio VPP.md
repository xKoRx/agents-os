---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Bajó de Precio]]"
sprint:
start: 2026-07-20
due:
progress: 50
repo: /Users/rjara/fuentes/vis-octopus-lib, /Users/rjara/fuentes/vpp-backend
jira:
prs:
aliases:
  - refactor bajo de precio vpp
  - refactor price drop motors vpp octopus
  - migracion price drop motors a octopus
tags:
  - project
  - area/meli
  - application/vpp-backend
  - application/vis-octopus-lib
  - feature/bajo-de-precio
created: 2026-07-20
updated: 2026-07-21
---

# Refactor Bajó de Precio VPP

%% Naming: Refactor Bajó de Precio VPP es el link canónico; aliases guarda variantes humanas. %%

> [!info]+ Refactor Bajó de Precio VPP
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Bajó de Precio]]
> Proyecto de agente para trasladar a Octopus la implementación nueva de Price Drop Motors y reducir VPP a integración explícita y mínima.

## 🎯 Objetivo

- Mantener la funcionalidad confirmada de **Bajó de Precio Motors**: pill, precio actual y precio anterior tachado bajo una única condición resuelta por Octopus.
- Conservar exactamente el comportamiento de Real Estate y de todas las demás verticales.
- Eliminar del PR de VPP la corrección lateral del contrato cross-vertical de `PriceComponent`/`PriceDomain`.
- Llevar a `vis-octopus-lib` el nuevo componente y la lógica específica de Price Drop Motors.
- Dejar en VPP solamente responsabilidades propias del consumer: bump de Octopus, routing explícito, composición de layouts y mapping al DTO Price.
- Aplicar los principios del owner: **SOLID, Clean Code, KISS y YAGNI**.

## 📊 Estado actual

- Fase 0 completada el 2026-07-20. VPP está en `feature/bajo-de-precio-motors`, HEAD `1b58056ec67`; frente a `origin/develop` el diff productivo existente es de 13 archivos y `pr_descripcion.md` permanece no trackeado. Octopus está en `master`, HEAD `f28d05d94`; el checkout de referencia 3.4.1 contiene Price Drop Motors y la rama remota exacta `feature/bajo-de-precio-motors` apunta a `593a1751c594`.
- Baseline focal: VPP `PriceComponentTaskTest`, `PriceMarshallerTest`, `PreviousPriceMotorsLayoutTest` y `VipMotorsViewTrackingInfoTaskTest` verdes. Octopus `VisPriceDropMotorsServiceTest` verde (11 tests).
- Discrepancia de documentación resuelta como rutas escritas con package incorrecto: las rutas reales de `PriceComponent.java`, `PriceDomain.java` y el marshaller moderno usan `com/mercadolibre/vpp/backend/...`; el marshaller legacy conserva `com/mercadolibre/vpp_backend/...`. Los hashes se verificarán contra esas rutas reales; no se asume equivalencia solo por nombre.

- La implementación vigente en `/Users/rjara/fuentes/vpp-backend`, rama `feature/bajo-de-precio-motors`, funciona en iOS: muestra la pill y el precio anterior tachado.
- El funcionamiento actual se obtuvo seleccionando Price Octopus para una baja Motors válida y adaptando en `PriceComponent` el modelo `com.mercadolibre.core.domains.price.PriceModel` a `PriceComponentModel`.
- Esa adaptación modifica un componente core cross-vertical creado por el equipo de Price y también afecta el camino del experimento general `vpp/octopus-price`; se considera demasiado amplia para esta iniciativa.
- Octopus ya es dueño de `PriceDropMotorsModel`, `VisPriceDropMotorsTask`, `VisPriceDropMotorsService` y `VisCouponSummaryComponent`.
- El checkout local de Octopus está en `develop`, pero las clases de Price Drop Motors existen en `feature/bajo-de-precio-motors` y en la versión publicada `3.4.1` consumida por VPP.
- No hay autorización para commit o push automático. Preservar cambios y archivos no relacionados en ambos repositorios.
- Corrección de review aplicada el 2026-07-21: `PriceComponent` y su test vuelven a coincidir con `origin/develop`; Motors ya no fuerza Price Octopus cuando el experimento global está apagado. `PriceComponentTask` conserva el routing existente y enriquece una copia del `PriceComponentModel` completo después de resolver cualquiera de sus dos ramas.

## 🧭 Arquitectura objetivo

```text
VisPriceDropMotorsTask (Octopus)
  └── PriceDropMotorsModel
        ├── isPriceDrop
        ├── experimentVariationPrice
        └── previousPrice

PriceComponentTask (VPP)
  ├── conserva la selección de arquitectura existente
  │     ├── experimento general ON → layoutResolver.getComponent(PRICE)
  │     └── experimento general OFF → flujo existente del wrapper
  ├── recibe un PriceComponentModel completo
  ├── copia el modelo con PriceComponentModelMapper
  └── agrega priceDropPreviousPrice cuando corresponde

PriceMarshaller moderno
  └── priceDropPreviousPrice → Price.originalValue
```

### Regla de precedencia

```text
1. El experimento general vpp/octopus-price mantiene su semántica anterior.
2. Motors no altera la arquitectura seleccionada.
3. Price Drop Motors se agrega después de obtener el modelo Price completo.
```

La elegibilidad se calcula en Octopus. VPP consume un booleano/modelo resuelto; no replica la regla de negocio.

## ✅ Principios y límites de diseño

### SOLID

- Octopus es dueño del caso de uso Price Drop Motors y de su componente especializado.
- `PriceComponentTask` conserva una sola responsabilidad: seleccionar el proveedor del modelo Price.
- El mapper convierte modelos; el componente orquesta; el marshaller traduce a DTO.
- Las dependencias apuntan a contratos explícitos, no a efectos laterales entre componentes.

### Clean Code

- Nombres explícitos: `PriceDropMotorsPriceComponent`, `PriceDropMotorsPriceEligibilityTask`, `PriceDropMotorsPriceMapper`.
- Una sola función de elegibilidad.
- No usar nombres ambiguos como `PriceModel` sin imports claros en clases donde convivan las dos representaciones.
- No mutar modelos recibidos desde Observables; construir/copiar el resultado.

### KISS

- Reutilizar el marshaller moderno `price` de VPP.
- Un ID interno nuevo; no duplicar ni reemplazar el ID base `price`.
- No crear un marshaller completo en Octopus.
- No agregar plugin si el componente especializado resuelve el caso directamente.

### YAGNI

- No migrar Price completo a Octopus.
- No corregir el contrato general `PriceComponent`/`PriceDomain` en esta iniciativa.
- No crear una jerarquía genérica de Price Drop para dos verticales.
- No crear interfaces/factories adicionales salvo que el spike demuestre una necesidad concreta.

## 🚫 Archivos y comportamientos prohibidos en VPP

Estos archivos productivos deben quedar idénticos a `origin/develop`:

- `src/main/java/com/mercadolibre/vpp_backend/app/shared/tasks/components/PriceDeprecatedComponentTask.java`
- `src/main/java/com/mercadolibre/vpp_backend/app/versioned/_default/v00_01/marshallers/PriceMarshaller.java`
- `src/main/java/com/mercadolibre/vpp_backend/app/shared/tasks/vip/tracks/VipVISViewTrackingInfoTask.java`
- `src/main/java/com/mercadolibre/vpp/backend/app/presentation/price/PriceComponent.java`
- `src/main/java/com/mercadolibre/vpp/backend/app/domains/price/PriceDomain.java`

También restaurar a `origin/develop` los tests RE/legacy modificados solo para sostener implementaciones descartadas.

No se permite:

- modificar `PriceDeprecatedComponentTask` o agregarle lógica Motors; se permite decorar en el wrapper el resultado de la rama que ya existía;
- modificar tracking RE;
- registrar dos `@BaseComponent` con ID `price`;
- renderizar el precio tachado dentro de `VisCouponSummary`;
- recalcular previous price en VPP;
- falsear `discount`, `originalPrice` u otros campos para engañar al marshaller;
- crear side effects entre la pill y Price;
- hacer commit o push sin autorización humana explícita.

## 🧪 Matriz funcional obligatoria

| Vertical / condición | Arquitectura Price esperada | Pill | `Price.originalValue` |
|---|---|---:|---:|
| Motors + baja + experimento ON + previousPrice | selección Price existente; con experimento global OFF usa la rama existente | sí | previousPrice |
| Motors sin baja | flujo existente | no | null |
| Motors + experimento OFF | flujo existente | no | null |
| Motors + previousPrice null | flujo existente | no | null |
| RE elegible | flujo RE de `develop` | comportamiento de `develop` | comportamiento de `develop` |
| RE no elegible | flujo RE de `develop` | comportamiento de `develop` | comportamiento de `develop` |
| Otra vertical + experimento Price Octopus OFF | flujo existente | no por Motors | sin cambio |
| Otra vertical + experimento Price Octopus ON | PriceComponent general existente | no por Motors | sin cambio |

## 🧪 Gate técnico antes de implementar

Antes de modificar VPP, comprobar en Octopus mediante un spike/test que:

1. Un `@BaseComponent` con ID interno `price_drop_motors_price` puede resolverse desde `LayoutResolver` aunque no esté directamente en el layout.
2. El modelo puede declarar `baseMarshallerId = "price"` y ser consumido por el marshaller moderno de VPP.
3. No se produce colisión con `@BaseComponent(id = "price")` de VPP.
4. El component resolver conserva el modelo como `PriceComponentModel`.
5. `Observable.empty()` o el comportamiento no elegible no deja al usuario sin Price; la selección debe ocurrir antes de resolver el componente.

Si cualquiera falla, **detener la implementación** y registrar evidencia. Usar el fallback mínimo:

```text
Octopus publica PriceDropMotorsPriceModelTask/factory
VPP lo consume desde PriceComponentTask
PriceComponent general permanece intacto
```

No inventar otro mecanismo ni ampliar el alcance sin revisión humana.

## ✅ Tareas

> [!example]- Fuente de tareas — planificador único
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] Fase 0 — Leer reglas, estado Git y diffs de ambos repositorios; registrar archivos sucios/preexistentes #owner/agent #type/research #area/meli
> - [x] Fase 0 — Confirmar checkout/fuente exacta de Octopus 3.4.1 y comparar con `feature/bajo-de-precio-motors` #owner/agent #type/research #area/meli
> - [x] Fase 0 — Capturar baseline de tests y matriz funcional antes del refactor #owner/agent #type/research #area/meli
> - [x] Fase 1 — Ejecutar gate técnico del componente Octopus con ID interno y `baseMarshallerId=price` #owner/agent #type/research #area/meli
> - [x] Fase 1 — Registrar decisión componente vs fallback task/factory con evidencia #owner/agent #type/research #area/meli
> - [x] Fase 2 — Implementar elegibilidad única de Price Drop Motors en Octopus #owner/agent #type/dev #area/meli
> - [-] Fase 2 — Implementar mapper explícito core Price → PriceComponentModel en Octopus (no aplica al fallback task/model aprobado; el mapper existente de VPP se conserva) #owner/agent #type/dev #area/meli
> - [x] Fase 2 — Implementar componente especializado o fallback aprobado en Octopus #owner/agent #type/dev #area/meli
> - [x] Fase 2 — Agregar tests Octopus positivos, negativos, null-safety y marshaller ID (marshaller ID no aplica al fallback; spike documentó el bloqueo) #owner/agent #type/dev #area/meli
> - [x] Fase 2 — Ejecutar `test`, `archTest` y `pmdMain` en Octopus #owner/agent #type/dev #area/meli
> - [x] Fase 2 — Publicar versión local de Octopus para integración; no publicar remoto #owner/agent #type/dev #area/meli
> - [x] Fase 3 — Restaurar `PriceComponent.java` y todo RE/deprecated a `origin/develop` en VPP #owner/agent #type/dev #area/meli
> - [x] Fase 3 — Reducir `PriceComponentTask` a routing explícito sin condición de negocio duplicada #owner/agent #type/dev #area/meli
> - [x] Fase 3 — Mantener solo el contrato mínimo `priceDropPreviousPrice` y mapping a `originalValue` #owner/agent #type/dev #area/meli
> - [ ] Fase 3 — Mantener layouts Android/iOS con `Price` y `VisCouponSummary` juntos para `vip-motors` #owner/agent #type/dev #area/meli
> - [ ] Fase 3 — Revisar tracking Motors; mover lógica a Octopus solo si reduce lógica de negocio sin agregar abstracciones #owner/agent #type/dev #area/meli
> - [ ] Fase 4 — Agregar tests VPP de routing, marshalling, layouts, tracking y matriz negativa #owner/agent #type/dev #area/meli
> - [ ] Fase 4 — Probar que archivos prohibidos son idénticos por hash a `origin/develop` #owner/agent #type/dev #area/meli
> - [ ] Fase 4 — Ejecutar tests focales, suite completa, Jacoco, PMD y ArchTest en VPP #owner/agent #type/dev #area/meli
> - [ ] Fase 4 — Levantar VPP, validar `/ping` y respuesta real con pill + `originalValue` #owner/agent #type/dev #area/meli
> - [ ] Fase 5 — Revisar diff final por SOLID/Clean/KISS/YAGNI y eliminar código transitorio #owner/agent #type/pr-review #area/meli
> - [ ] Fase 5 — Actualizar `pr_descripcion.md` respetando el template de VPP #owner/agent #type/dev #area/meli
> - [ ] Fase 5 — Dejar ambos worktrees sin commit ni push y entregar evidencia para revisión humana #owner/agent #type/pr-review #area/meli

## 🪜 Ejecución paso a paso para una IA pequeña

### Fase 0 — Orientación y baseline

1. Leer `AGENTS.md` y reglas obligatorias de ambos repositorios.
2. Leer esta nota completa; es el único planificador durable.
3. Ejecutar `git status`, rama actual, merge-base y diff contra `origin/develop`.
4. No borrar, resetear ni sobrescribir cambios preexistentes.
5. Inspeccionar el JAR 3.4.1 realmente consumido por VPP y la rama Octopus que contiene Price Drop Motors.
6. Guardar en `## 📆 Bitácora` hashes, ramas y baseline relevante.
7. Ejecutar tests focales actuales para demostrar que la funcionalidad parte verde.

### Fase 1 — Spike arquitectónico obligatorio

1. Crear únicamente el mínimo test/spike requerido en Octopus.
2. Usar ID interno distinto de `price`.
3. Verificar resolución y selección del marshaller base `price`.
4. Probar integración con `publishToMavenLocal` y una versión local inequívoca.
5. Si el spike pasa, registrar la evidencia y continuar con componente.
6. Si falla, deshacer solo el spike propio y aplicar el fallback task/factory documentado.
7. No modificar todavía `PriceComponent.java` ni Price legacy en VPP.

### Fase 2 — Implementación Octopus

1. Extraer una única función/task de elegibilidad.
2. Reutilizar `VisPriceDropMotorsTask`; no recalcular atributos ni porcentajes.
3. Implementar un mapper con nombres de tipos explícitos para las dos representaciones Price.
4. Construir un modelo nuevo; no mutar el modelo compartido.
5. Configurar `baseMarshallerId=price`.
6. Emitir un componente únicamente para el caso elegible.
7. Agregar tests antes de integrar en VPP.
8. Validar Octopus completo.

### Fase 3 — Integración mínima en VPP

1. Restaurar `PriceComponent.java` exacto a `origin/develop`.
2. Restaurar todos los archivos RE/deprecated prohibidos exactos a `origin/develop`.
3. Bump temporal a la versión Octopus publicada localmente.
4. En `PriceComponentTask`, consumir la elegibilidad resuelta por Octopus.
5. Elegir con `flatMap` solo un proveedor de Price; no ejecutar ambos con `zip` para luego descartar uno.
6. Mantener el experimento global Price Octopus con su semántica anterior.
7. Mantener el campo y mapping mínimo para `originalValue`.
8. No agregar otro marshaller ni otro DTO externo.

### Fase 4 — Pruebas de regresión

1. Ejecutar toda la matriz funcional de esta nota.
2. Confirmar respuesta final, no solo modelos unitarios.
3. Confirmar que `VisCouponSummary` y `Price` aparecen juntos.
4. Confirmar `Price.originalValue == previousPrice` en el caso positivo.
5. Confirmar ausencia de pill y tachado en los tres negativos.
6. Ejecutar tests RE existentes sin modificarlos para hacerlos pasar.
7. Agregar casos de otra vertical con experimento general ON/OFF.
8. Validar updates soportados por `PriceComponentTask` al menos por tests existentes.

### Fase 5 — Limpieza y entrega

1. Eliminar spike, flags temporales, duplicación y código muerto.
2. Revisar cada clase contra SOLID/Clean/KISS/YAGNI.
3. Comparar archivos prohibidos por hash contra `origin/develop`.
4. Ejecutar gates completos.
5. No commit, no push.
6. Actualizar esta nota, mover tareas terminadas y dejar la tarea puente en Review solo cuando todo esté verde.

## ✅ Criterios de aceptación

- [ ] La funcionalidad Motors positiva fue confirmada en DTO final y nativo.
- [ ] Los tres casos negativos no muestran pill ni precio tachado.
- [ ] RE conserva exactamente código y tests de `origin/develop`.
- [ ] Otras verticales conservan el routing anterior.
- [ ] `PriceComponent.java` y `PriceDomain.java` son idénticos a `origin/develop`.
- [ ] No se modificó ningún archivo deprecated para implementar Motors.
- [ ] La condición funcional existe una sola vez en Octopus.
- [ ] VPP no contiene cálculo de Price Drop Motors.
- [ ] No hay IDs base duplicados ni marshaller Price duplicado.
- [ ] Octopus: tests, ArchTest y PMD verdes.
- [ ] VPP: tests focales, suite completa, Jacoco, ArchTest y PMD verdes.
- [ ] Aplicación VPP arranca y `/ping` responde 200.
- [ ] `git diff --check` limpio en ambos repositorios.
- [ ] `pr_descripcion.md` conserva el template oficial.
- [ ] No hubo commit ni push sin autorización.

## 🔎 Comandos de validación sugeridos

### Octopus

```bash
./gradlew test archTest pmdMain --no-daemon --console=plain
./gradlew publishToMavenLocal --no-daemon --console=plain
```

### VPP focal

```bash
./gradlew :test \
  --tests 'com.mercadolibre.vpp.backend.app.presentation.price.PriceComponentTaskTest' \
  --tests 'com.mercadolibre.vpp.backend.app.presentation.price.marshallers.PriceMarshallerTest' \
  --tests 'com.mercadolibre.layout.PreviousPriceMotorsLayoutTest' \
  --tests 'com.mercadolibre.vpp_backend.app.shared.tasks.vip.tracks.VipMotorsViewTrackingInfoTaskTest' \
  --tests 'com.mercadolibre.vpp_backend.app.contingency.ContingencyManifestCoverageTest'
```

### VPP completo

```bash
./gradlew test --no-daemon --console=plain
./gradlew jacocoTestReport --no-daemon --console=plain
./gradlew pmdMain archTest --no-daemon --console=plain
./gradlew run --no-daemon --console=plain
curl --fail http://127.0.0.1:8080/ping
```

### Invariantes por hash

```bash
git hash-object <archivo>
git rev-parse origin/develop:<archivo>
```

Los hashes deben coincidir para cada archivo prohibido.

## ⚠️ Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Colisión entre componente especializado y `price` | ID interno único + gate técnico antes de implementar |
| Resolver usa marshaller del ID interno | asignar y probar `baseMarshallerId=price` |
| VPP ejecuta dos proveedores Price | selección lazy con `flatMap`, nunca zip de ambos |
| Regla duplicada Octopus/VPP | eligibility task/model resuelto en Octopus |
| Caso inválido deja Price vacío | decidir elegibilidad antes de resolver el componente |
| Mutación/race condition | construir o copiar modelos; no mutar observables compartidos |
| Regresión del experimento general Price | mantener `PriceComponent` intacto + tests ON/OFF |
| Regresión RE | hashes exactos + tests existentes sin reescritura semántica |
| Acoplamiento Octopus→modelo VPP | mapper encapsulado; no filtrar tipos core fuera del componente |
| Diferencia checkout/JAR publicado | inspeccionar rama/tag y probar consumidor con Maven local |

## 🧾 Prompt maestro para IA pequeña

```text
Trabaja como agente implementador conservador sobre el proyecto canónico:

VAULT_ROOT/10-projects/Destaques de Precio/agentes/Refactor Bajó de Precio VPP.md

Tu objetivo es ejecutar ese proyecto paso a paso. La nota es tu ÚNICO planificador durable: léela completa antes de actuar, cambia cada tarea [ ] → [/] → [x] a medida que avances, actualiza progress, Estado actual y Bitácora después de cada hito. No mantengas decisiones importantes solo en el chat.

Repositorios:
- VPP: /Users/rjara/fuentes/vpp-backend
- Octopus: /Users/rjara/fuentes/vis-octopus-lib

Reglas obligatorias:
1. Lee y obedece los AGENTS.md y reglas locales de ambos repositorios antes de editar.
2. Preserva cambios preexistentes y archivos no relacionados. No uses reset --hard, checkout destructivo ni borrados masivos.
3. No hagas commit ni push. No publiques una versión remota. Maven local sí está permitido para validar integración.
4. No modifiques PriceDeprecatedComponentTask, el marshaller legacy, tracking RE ni sus tests para implementar Motors.
5. PriceComponent.java y PriceDomain.java de VPP deben terminar idénticos a origin/develop.
6. Mantén funcionalidad de Motors, RE y todas las verticales.
7. Aplica SOLID, Clean Code, KISS y YAGNI: responsabilidades explícitas, una sola condición de negocio, sin jerarquías genéricas innecesarias, sin duplicar marshallers ni migrar Price completo.
8. Toda lógica nueva de Price Drop Motors y el componente especializado viven en Octopus. VPP solo conserva bump, routing, layout y mapping DTO mínimo.
9. La pill sigue siendo VisCouponSummary y el tachado sigue siendo Price.originalValue. Nunca mezcles ambos componentes.
10. No asumas que un test unitario prueba runtime: valida el componente seleccionado y el DTO final.

Orden estricto:
A. Ejecuta Fase 0 y registra baseline.
B. Ejecuta el gate técnico de Fase 1 antes de modificar VPP.
C. Si el componente Octopus con ID interno y baseMarshallerId=price funciona, usa ese diseño.
D. Si no funciona, detente, registra evidencia y usa únicamente el fallback task/factory definido en la nota. No inventes una tercera arquitectura.
E. Implementa y valida Octopus completo.
F. Publica a Maven local y recién entonces integra VPP.
G. Restaura los archivos prohibidos de VPP a origin/develop y verifica hashes.
H. Ejecuta matriz funcional, tests completos y runtime.
I. Actualiza pr_descripcion.md respetando íntegramente el template oficial.
J. Deja ambos worktrees sin commit ni push y mueve la tarea puente a Review únicamente si todos los criterios están verdes.

Antes de cada edición explica brevemente qué archivo tocarás y por qué. Si encuentras una contradicción entre el código real y el proyecto, detente, documenta la evidencia en Bitácora y pide dirección; no amplíes el scope por tu cuenta.

Entrega final obligatoria:
- arquitectura implementada;
- diff productivo por repositorio;
- archivos prohibidos comparados por hash;
- matriz funcional con resultado por caso;
- comandos exactos y resultados;
- riesgos residuales;
- estado Git de ambos repositorios;
- confirmación explícita de que no hubo commit ni push.
```

## 📆 Bitácora

- **2026-07-20** — Proyecto creado a solicitud del owner. Se define mover el nuevo componente/lógica Motors a Octopus y reducir VPP a integración mínima. El diseño queda condicionado a un spike de resolución por ID interno y `baseMarshallerId=price`; no se autoriza implementación ciega.
- **2026-07-20** — Fase 0 completada. Reglas/AGENTS OS y reglas locales leídas. VPP: `feature/bajo-de-precio-motors` @ `1b58056ec67`, merge-base `307bfd97e94`; solo `pr_descripcion.md` no trackeado preexistente. Octopus: `master` @ `f28d05d94`, archivos no trackeados preexistentes `.agents/`, `AGENTS.md`, `descripcion_pr.md`, `meli/wip/`. JAR consumido: `vis-octopus-lib:3.4.1`, contiene `PriceDropMotorsModel`, `VisPriceDropMotorsTask` y `VisCouponSummaryComponent`. Rama remota de implementación: `feature/bajo-de-precio-motors` @ `593a1751c594`. Baseline VPP focal verde; baseline Octopus focal requiere confirmación de salida completa. Se detectaron rutas documentales no literales para PriceMarshaller/PriceDomain y se resolverán por búsqueda.
- **2026-07-20** — Confirmación de Fase 0: `VisPriceDropMotorsServiceTest` terminó verde con 11 tests. Las rutas documentales no literales se resolvieron: `PriceComponent`, `PriceDomain` y marshaller moderno están bajo `com/mercadolibre/vpp/backend`; el marshaller legacy y `PriceDeprecatedComponentTask` bajo `com/mercadolibre/vpp_backend`. No se modificó código para resolver esta discrepancia.
- **2026-07-20** — Gate Fase 1 ejecutado en Octopus con spike test-only y eliminado después. Evidencia runtime: un `@BaseComponent(id="price_drop_motors_price")` que devuelve `ComponentModel.baseMarshallerId="price"` termina con `baseMarshallerId="price_drop_motors_price"`, porque `BaseComponentRecord.get()` lo sobrescribe y `getBaseMarshallerId()` es `final` en `vpp-backend-core-lib:7.3.0`. El diseño de componente no cumple el gate; decisión obligatoria: usar únicamente fallback task/model aprobado. VPP no fue modificado durante el gate.
- **2026-07-20** — Fase 2 Octopus parcial completada: se agregaron `PriceDropMotorsPriceModel` y `PriceDropMotorsPriceModelTask` en el paquete de `VisPriceDropMotorsTask`. La task produce un modelo inmutable con `eligible` y `previousPrice`, sin mutar el modelo compartido; tests positivo, experimento apagado/baja falsa y null verdes. Falta ejecutar gates completos y publicar Maven local.
- **2026-07-20** — Gates Octopus completos verdes: `./gradlew test archTest pmdMain --no-daemon --console=plain` terminó `BUILD SUCCESSFUL`. PMD dejó únicamente warning de regla deprecated en `config/pmd/pmd_rules.xml`, preexistente al cambio. Publicación Maven local queda WIP; no se hará publicación remota.
- **2026-07-20** — Octopus `3.5.0` publicado a Maven local (`publishToMavenLocal` verde). VPP integrado al fallback: `PriceComponent.java` restaurado byte-a-byte a `origin/develop`; `PriceComponentTask` consume `PriceDropMotorsPriceModelTask`, enruta Motors elegible a Price Octopus y conserva el experimento general; el marshaller moderno de presentación mantiene únicamente el mapping `priceDropPreviousPrice → originalValue`. `compileJava` verde. También se restauró el marshaller legacy real (`com/mercadolibre/vpp_backend/app/versioned/_default/v00_01/marshallers/PriceMarshaller.java`) a `origin/develop`; la discrepancia provenía de cambios preexistentes del branch. La suite de tests VPP quedó bloqueada antes de ejecutar casos por error preexistente/no relacionado en `SellerProfileMotorsComponentTaskTest:268`: constructor de `SellerGoodAttentionDomainModel` requiere 8 argumentos y el test usa 6. No se editó ese test.
- **2026-07-21** — Corrección cross-vertical aplicada sobre el PR oficial. Los cambios WIP previos quedaron preservados en `stash@{0}` con mensaje `wip refactor bajo de precio vpp antes de correccion cross-vertical`. Se retiró el adapter parcial de `PriceComponent` y se restauró su test exacto a `origin/develop`; hash verificado `08ed755a27abbde5c227b99847a0775c7fab55f2`. `PriceComponentTask` vuelve a seleccionar arquitectura solo mediante `OctopusPriceExperimentTask`, pero mantiene el enriquecimiento de la copia completa en `doGet()` y `doGetOctopus()`. El test integral verifica que, con experimento global OFF, no se consulta `LayoutResolver` y aun así se obtienen pill, precio actual y `originalValue`. El comando focal con `--rerun-tasks` terminó `BUILD SUCCESSFUL` en 2m09s. Sin commit ni push.

## 🧭 Decisiones

- No perseguir cero líneas en VPP a costa de side effects: perseguir cero lógica de negocio Motors nueva en VPP.
- No migrar Price completo.
- No corregir el mismatch general de `PriceComponent`/`PriceDomain` en este PR.
- Nuevo componente en Octopus con ID interno único; reutilizar el marshaller Price de VPP.
- VPP mantiene routing porque el wrapper es owner de la selección de arquitectura.
- La condición de elegibilidad vive una sola vez en Octopus.
- Motors no fuerza la arquitectura Price Octopus; `shouldUseOctopusArchitecture()` conserva únicamente el experimento global.
- El adapter `com.mercadolibre.core.domains.price.PriceModel → PriceComponentModel` queda fuera del PR porque reconstruía parcialmente un componente cross-vertical.

## 🔗 Docs / Links

- [[Bajó de Precio]]
- [[vpp-backend]]
- [[vis-octopus-lib]]
- `/Users/rjara/fuentes/vpp-backend/pr_descripcion.md`

## 💡 Ideas

### Backlog de ideas

- Evaluar en una iniciativa separada el contrato general entre `PriceComponent` y `PriceDomain`; no mezclarlo con Price Drop Motors.

### Motivos / principios

- Minimizar blast radius en VPP core sin trasladar responsabilidades de presentación que realmente pertenecen al consumer.

### Memoria pública / interna

- **Memoria pública:** este proyecto canónico contiene el plan ejecutable y las decisiones aprobadas.
- **Memoria interna:** continuidad de diagnóstico/runtime de la sesión previa.
- **Motivo:** separar la fuente de verdad del proyecto de la evidencia táctica de sesiones.
