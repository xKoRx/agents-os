# MANDATO — S02 SPORTS REVERSION / EXPERIMENTO REAL E2

## MISIÓN

Avanzar una sola POC: `PE-005-R1 / poc-sports`.

Objetivo: medir frecuencia y persistencia de señales de reversión sobre nuevos datos deportivos reales. No optimizar PnL ni implementar otra estrategia.

## AUTORIDADES

Bootstrap Agents-OS.

Leer proyecto padre, continuidad Five-POC, guía operativa S02, research PE-005-R1 y evidencia RS v0.3.

Baseline: integración `85e27ff`, verificando HEAD y limpieza. No utilizar el worktree U-02 como baseline hasta aceptación e integración explícitas.

## EXPERIMENTO

1. Inspeccionar el experimento anterior: captura MLB 2284198, seis horas y cero señales. Documentar ventana, parámetros, cobertura y posibles causas observables de exclusión.
    
2. Seleccionar antes de mirar los resultados una muestra acotada de otros partidos actuales con kickoff y mercados compatibles. Definir ventanas prepartido sin seleccionar retrospectivamente las que parezcan favorables.
    
3. Capturar Catalog y books en modo read-only. Conservar timestamps de fuente y recepción, gaps, secuencias y procedencia.
    
4. Congelar el journal antes de ejecutar SHADOW. Proteger originales y WAL; trabajar sobre un snapshot consistente o un dataset nuevo.
    
5. Ejecutar baseline con los parámetros canónicos. Si se evalúa una variante, cambiar sólo UN parámetro preregistrado y usar exactamente el mismo dataset para la comparación.
    
6. Ejecutar SCREEN → REPLAY → SHADOW → COMPARE cuando los datos y gates lo permitan.
    

## MÉTRICAS OBLIGATORIAS

- Partidos y mercados elegibles.
    
- Tiempo y frames realmente observados.
    
- Gaps, antigüedad y calidad de libros.
    
- Frames elegibles versus excluidos, por causa.
    
- Número de shocks y señales.
    
- Señales por hora elegible.
    
- Duración de cada señal.
    
- Profundidad y coste observable al detectar la señal.
    
- Sensibilidad a retraso y repricing.
    
- Efecto de la variante respecto del baseline.
    

Distinguir `0 señales` de `sin observaciones suficientes`.

## ECONOMICS

Mientras U-02 siga sin resolver, la economía de ejecución real permanece NO CERTIFICADA.

Puedes reportar señales, quotes, spreads, profundidad y costes de referencia, pero no declarar oportunidad neta ejecutable, fills reales ni alpha.

Maker permanece UNCALIBRATED. No atribuirle fills.

## GATES DE SALIDA

Entregar uno de estos resultados:

- `SIGNALS_OBSERVED`: señales registradas, con frecuencia y condiciones.
    
- `NO_SIGNALS_IN_SAMPLE`: captura válida, cero señales dentro de la muestra.
    
- `DATA_INSUFFICIENT`: no se cubrió la muestra o calidad requerida.
    
- `IMPLEMENTATION_BLOCKED`: defecto concreto impidió el experimento.
    

No declarar NO_GO global con una ventana pequeña.

## ENTREGABLES

Un dataset nuevo versionado, manifest, hashes, parámetros preregistrados, resultados reproducibles, comparación y un informe que responda:

«¿Qué observamos, cuánto observamos y qué experimento necesitamos después para evaluar la hipótesis?»

Actualizar las notas existentes de Agents-OS y registrar evidencia. No cerrar sesión.

Sin live, órdenes, wallet, signing, merge, push ni cambios al código compartido.