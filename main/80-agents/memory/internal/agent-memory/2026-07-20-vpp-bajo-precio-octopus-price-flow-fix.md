---
type: agent_memory
scope: agent
created: 2026-07-20
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - agent/internal
  - area/meli
  - app/vpp-backend
  - app/vis-octopus-lib
  - feature/bajo-de-precio
---

# VPP — corrección del precio anterior en el flujo Octopus de Motors

- Repositorio intervenido: `/Users/rjara/fuentes/vpp-backend`. La corrección validada en `feature/bajo-de-precio-motors-testt` fue trasladada a la rama oficial `feature/bajo-de-precio-motors` sin commit ni push.
- Corrección posterior de la causa raíz: el tráfico real Motors probado en test scope usa `PriceComponentTask.doGet()` porque `vpp/octopus-price` está apagado. La evidencia decisiva fue que propagar el valor desde `PriceDeprecatedComponentTask` sí funcionaba y enriquecer `PriceComponent`/`doGetOctopus()` no. La primera solución sólo probó artificialmente la rama Octopus y era insuficiente.
- Octopus publicado `vis-octopus-lib:3.4.1` fue inspeccionado desde el JAR de Gradle. `VisPriceDropMotorsService` ya calcula `previousPrice` e `isPriceDrop`, y `VisCouponSummaryComponent` ya muestra la pill. No se modificó `/Users/rjara/fuentes/vis-octopus-lib`.
- Corrección vigente: `PriceComponentTask`, punto común posterior a la selección legacy/Octopus, depende de `VisPriceDropMotorsTask` y copia `previousPrice` al `PriceComponentModel` sólo con baja real, experimento activo y valor no nulo. `PriceDeprecatedComponentTask` y el marshaller RE permanecen intactos. Se eliminó el dominio puente y `PriceComponent` volvió a `origin/develop`.
- Se quitó la integración Motors de `PriceCoreComponentTask`; el estado final combinado de ese task y su test queda idéntico a `origin/develop`.
- Prueba vertical corregida: servicio y task reales de Octopus → `VisCouponSummaryComponent` + `PriceComponentTask` forzando arquitectura legacy (`vpp/octopus-price=false`) → marshaller moderno. Cubre visible con `originalValue`, sin baja, experimento apagado y `previousPrice` ausente.
- Reproducción remota: el request iOS real entra por `https://frontend.mercadolibre.com/products/{id}` (no por `/frontend/products`); el deployment `0.0.25-previous-price-motors` devolvió `Price.value=13000` y `original_value=null`. El curl disponible no reprodujo la pill, aunque el tracking asignó `vis/item-dropprice-motors=288068`; para copiar exactamente la app se necesita su header `x-native-experiments` real. El servidor local levantó, pero el E2E quedó bloqueado por Mockster 403/falta de access group `mockster_devs`.
- Hallazgo definitivo tras `0.0.26`: el request Motors continúa por la rama legacy y usa `app/versioned/_default/v00_01/marshallers/PriceMarshaller`, no el marshaller moderno. La versión anterior que funcionó había modificado dos puntos: `PriceDeprecatedComponentTask` cargaba `priceDropPreviousPrice` y el marshaller legacy ejecutaba `assignOriginalValueByPriceDrop`. Mover sólo la carga del modelo al wrapper no basta: el legacy marshaller actual únicamente consume `priceDropRESModel` y descarta `priceDropPreviousPrice`. Sin tocar RE/legacy, la salida correcta exige enrutar Price Motors por `doGetOctopus()`/marshaller moderno o migrar el componente Price completo a Octopus.
- Implementación posterior: no se migró Price global ni se forzó todo Motors. `PriceComponentTask.shouldUseOctopusArchitecture()` conserva `vpp/octopus-price` y además selecciona Octopus únicamente cuando el `PriceDropMotorsModel` compartido tiene `isPriceDrop`, experimento visible y `previousPrice` no nulo. `PriceComponent` adapta el `com.mercadolibre.core.domains.price.PriceModel` ligero del `PriceDomain` a `PriceComponentModel`; el wrapper agrega `priceDropPreviousPrice`. El modelo Octopus conserva `baseMarshallerId=price`, garantizando selección del marshaller moderno. Negativos continúan por legacy sin tachado. RE y sus cuatro archivos restringidos permanecen idénticos a `origin/develop`.
- En la rama oficial se restauraron desde `origin/develop` `PriceDeprecatedComponentTask`, el marshaller legacy, `VipVISViewTrackingInfoTask` y sus tests asociados. La copia defensiva requerida por tracking Motors quedó encapsulada en `VipMotorsViewTrackingInfoTask`, usando `VISItemTrackingInfoModelCopyMapper`; el padre RE no aporta helpers nuevos.
- Validaciones finales en la rama oficial: tests focales en verde, suite completa ejecutada sin fallos de tests, `archTest` en verde, `pmdMain` en verde, `git diff --check` limpio y aplicación levantada con `GET http://127.0.0.1:8080/ping` → `200 pong`.
- Los cuatro archivos RE/legacy restringidos quedaron idénticos a `origin/develop` (`git diff --exit-code` = 0). No hubo commit ni push.
- `pr_descripcion.md` permaneció no trackeado. El worktree queda preparado como un único cambio lógico titulado `fix code review`, pero deliberadamente sin stage, commit ni push por instrucción del usuario.
- Para reproducir VIP nativo en un test scope, separar contratos: iOS usa `/products/{id}` con headers `X-CLIENT-*`; Android usa `/frontend/products/{id}` con `app=vip`, `x-platform=android`, `x-client-version` y `x-app-version`. El `x-deeplink` debe apuntar al mismo item del path.
- En Motors, la evidencia funcional de Bajó de Precio está en `Price` (`originalValue`/previous price) y `VisCouponSummary` después de `Price`; no esperar una pill visible `price_related_highlight`, que es el flujo genérico no-Motors.
- Decisión de refactor posterior: no corregir lateralmente `PriceComponent`/`PriceDomain` cross-vertical dentro del PR Motors. El plan durable es [[Refactor Bajó de Precio VPP]]: nuevo componente/eligibilidad Motors en Octopus con ID interno y `baseMarshallerId=price`, VPP reducido a routing/layout/mapping mínimo, con fallback task/factory si el spike del component resolver falla.
