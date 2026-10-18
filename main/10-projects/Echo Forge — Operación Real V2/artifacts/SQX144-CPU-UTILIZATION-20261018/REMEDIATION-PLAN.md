---
type: remediation_plan
schema_version: 1
status: final
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/plan
  - area/echo
  - tech/performance
---

# REMEDIATION-PLAN — SQX 144 CPU

## Cambios de flota aplicados en este mandato: NINGUNO (y ninguno requerido)

No existe restricción accidental demostrada que corregir (ver CPU-ROOT-CAUSE.md). La configuración Max Performance del owner ya estaba persistida y se demostró aplicándose en el CLI. Toda modificación adicional al runtime habría violado el principio "sólo corregir causas demostradas". Los ítems siguientes son higiene operacional y oportunidades de producto, con decisión pendiente del owner; ninguno bloquea producción.

## Higiene operacional (opcional, ventana owner)

1. **Permisos `user/log` en Zeus** (cosmético): `/home/kor/sqx/144/user/log` quedó `775 echo-dev:echo-dev`; el CLI corre como `kor` y desde el 14-oct no puede escribir launcher/StrategyQuant logs (los project logs, 777, sí se escriben). Si se quiere telemetría SQX en Zeus: `chown`/`chmod` del directorio (o `chgrp echo-dev` + añadir kor al grupo). Impacto actual: sólo pérdida de logs.
2. **Carrera boot-order worker vs mount SQXDATA** (transitoria, auto-recuperada): a las 05:07:09Z el worker arrancó antes que el mount `/home/kor/sqx` y registró `VersionNotFound` de 144; se recuperó solo al montar el disco. Si se quiere eliminar la línea de error: dependencia `RequiresMountsFor=/home/kor/sqx` en la unidad `stager-runtime.service` (requiere ventana con drenaje probado). Sin cambio, el efecto es una línea ERROR inocua al boot.
3. **Doble declaración de heap** (documental): `JAVA_TOOL_OPTIONS` de la unidad declara `-Xms34g` y `sqcli.config` declara `-Xms4g` (gana este por orden); `-Xmx55g` queda de JTO. Contrato actual efectivo `-Xms4g -Xmx55g -XX:+UseParallelGC` es el deseado; se recomienda NO tocar (cambiar JTO arriesga el heap de otros JVM hijos del worker por igual) y dejar esta nota como contrato único de referencia.

## Oportunidades de producto (fuera de este mandato — "no rediseñar Forge"; requieren decisión owner/manager)

4. **Paralelizar la CustomAnalysis del overview producer**: domina el 87% del wall time del builder (~60 min de 69 en w10) iterando estrategias en secuencia (~5,5 s/estrategia). Vías a evaluar en un proyecto propio: particionar el databank de entrada en N corridas candidate-local (patrón cola/prefijo existente), o evaluar si SQX 144 expone paralelismo en el API CustomAnalysis. Ganancia teórica en w10: de 69 min a ~10-12 min por builder en un host.
5. **Fast-fail de retry tras kill ("Project stopped")**: re-armar el proyecto (stop+start o limpieza del estado de proyecto) antes del retry ahorraría un intento quemado en re-despachos tras reboot/kill. Bajo riesgo, beneficio acotado a incidentes.
6. **Boot fijo de JVM en retests** (~10-15 s de 17-30 s por estrategia): amortizable sólo con un modo residente de SQX (cambio de arquitectura del contrato un-proceso-por-actividad); documentado como no viable sin rediseño.

## Rollback

No aplica (cero mutaciones de flota/repo en este mandato). El único efecto en el vault es este paquete de evidencia + notas de cierre.
