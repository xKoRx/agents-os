---
type: evidence_doc
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# SOURCE-FORENSICS — EchoForgeOverviewExporter (SQX 144.2953)

Fuente: `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeOverviewExporter.java` @ `492a271e` (release 0.3.1, 1831 líneas). Forensics estática + perfilado físico JFR (ver BASELINE-PROFILE.md); la hipótesis dominante se validó midiendo, no asumiendo.

## Hot paths confirmados por JFR (task window, corpus estándar 24 estrategias)

1. **Compilación de regex por llamada — ~60–65% del CPU de tarea.** `norm()` hace `toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9]","")`: `String.replaceAll` compila un `Pattern` NUEVO en cada invocación (atribución: 889 muestras task con `String.replaceAll` como llamador del motor regex; `norm` inclusive 475/2986 samples = 16% por sí sola). `matchIndicator`/`matchPriceSeries`/`toEpochMs`/`toDouble` repiten el mismo patrón. `pickValue()` normaliza CADA clave del mapa escalar en CADA lookup (doble pasada exacta+fuzzy, candidatos×entradas), multiplicando el costo: ~7 lookups por trade en 3 pasadas separadas.
2. **Reflexión re-derivada — ~8–10% del CPU.** `collectScalarMap()` llama `getMethods()` + `getDeclaredFields()` + `setAccessible(true)` para CADA trade, en cada pasada; top-of-stack muestra `Class.privateGetDeclaredFields` (23) + `MethodHandle*FieldAccessorImpl` (18) + `DirectMethodHandle.allocateInstance` (29).
3. **Triple pasada de `collectScalarMap` por trade.** `buildStrategyRow` recolecta el mapa escalar de cada trade 3 veces independientes: bucle de diagnósticos de precios (líneas 292–324), `monthlyFromTrades` (línea 618) y export debug opcional (línea 371). El mapa es determinista por objeto → 2/3 del trabajo de reflexión+construcción de LinkedHashMap es redundante.
4. **NO dominantes en este perfil (contra-hipótesis medidas):** `getStrategyXmlSafely` + `parseIndicators` (XML DOM + traverseDom) < 0,5% (ausentes del top-30 inclusive); `scanForTrades`/`findTrades` ≤ 5 muestras; escritura NDJSON y `JSONObject.toString` < 1%; H2 (carga databank) concentrada en boot/fin de tarea. La reflexión sobre getters pesados de SQX NO es el cuello: `com.strategyquant.*` inclusive ≈ 13% y mayormente carga/guardado.

## Riesgos de paridad identificados antes de tocar código

- `JSONObject` (org.json) itera en orden de HashMap: cualquier cambio que altere el ORDEN de inserción de claves cambia el byte-order del NDJSON → prohibido reordenar `put`s.
- `pickValue` define precedencia: candidatos en orden dado, primera coincidencia exacta sobre el mapa en orden de inserción, luego primera fuzzy (contains bidireccional). Cualquier reescritura debe preservar exactamente esa semántica.
- `collectScalarMap` define el contenido del mapa (getters filtrados por `isGetterLike`/`skipHeavyMethod` + fields no-static por jerarquía) y su orden (getters en orden `getMethods()`, luego fields por clase de subclase a superclase).
- El databank de entrada es re-serializado por SQX al terminar la tarea (demostrado: 24/24 SHA cambian tras un run) → todo run comparativo debe partir de corpus pristine restaurado + verificación SHA (protocolo en BASELINE-PROFILE.md).
