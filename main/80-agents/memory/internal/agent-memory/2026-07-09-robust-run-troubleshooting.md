---
type: agent_memory
scope: internal
created: 2026-07-09
updated: 2026-07-09
tags:
  - kind/agent_memory
  - tech/go
  - app/symphony
  - topic/workflow
  - topic/testing
---

# Continuidad Operativa: Troubleshooting Robust Run, Mocks de Tests y Configuración Relativa

## Aprendizajes Clave

1. **Paralelismo y Concurrencia de Workers**:
   - Cada máquina física individual (Zeus, Hera, Kronos, etc.) aloja un único worker de SQX.
   - Cada worker procesa tareas en Temporal de manera secuencial (`concurrency = 1`).
   - El paralelismo es horizontal a nivel de múltiples servidores, no concurrente a nivel local sobre el mismo databank.
   - No hay colisiones de archivos a nivel local sobre la carpeta `custom/input` o `custom/output` de un mismo worker. Las optimizaciones o locks concurrentes locales sobre el mismo disco son innecesarios.

2. **Resolución de Rutas y Properties en Tests**:
   - `TestApplySelectedRunActivity_Execute` fallaba inicialmente en macOS porque `sqxExecBasePath` tiene el fallback Linux `"/home/kor/sqx"`, impidiendo crear directorios raíz no permitidos en macOS.
   - Se solucionó configurando `runtime.SetSQXExecBasePath(t.TempDir())` al inicio del test y pasando un mock de `etcd.CacheClient` con las propiedades requeridas para que se resuelvan en la ruta de prueba temporal.
   - También se ajustó `mockExecutor` en el test para que cree el directorio y archivo de databank de salida `custom/output/mock_strat.sqx` simulando la salida real de `sqcli`.

3. **Configuración Portable (Propuesta Relativa)**:
   - Para evitar dependencias con rutas absolutas de Windows (`C:/EchoForge/...`) que rompen en entornos Linux/Wine, la configuración `execution_params.properties` debe ubicarse en la carpeta de entrada del databank del proyecto custom: `user/projects/custom/databanks/input/execution_params.properties`.

## 🚀 Resultados del Troubleshooting Real en Zeus (2026-07-09)

Se ejecutó la prueba en caliente sobre el worker real Zeus invocando `/home/kor/test_apply_selected`.
Resultados de la auditoría física en caliente:

1. **Estado del Worker y Conectividad**:
   - El servicio `symphony-worker.service` está activo desde el 8 de julio de 2026 a las 11:22:17.
   - El worker no reportó nuevas entradas en `symphony-worker.log` simplemente porque no se le habían despachado nuevos workflows.
   - La conectividad física del worker de Zeus con Temporal (`192.168.31.46:7233`) y MinIO (`192.168.31.92:9000`) se encuentra 100% activa.

2. **Ejecución y Generación de EAs**:
   - La ejecución del binario `test_apply_selected` completó exitosamente (`Activity success!`).
   - `sqcli` en Zeus tardó ~22 segundos en procesar, mutar las variables, aplicar el parche de WFM y compilar la estrategia a MQL5.
   - El `.mq5` resultante fue subido correctamente a MinIO en:
     `wave_15/xauusd/l_h1/test1/v3/ea_export/XAUUSD_L_H1_test1_v3_Strategy_8_1_22_z0.mq5` (tamaño 263 KB).
   - El `.sqx` parchado final fue subido a:
     `wave_15/xauusd/l_h1/test1/v3/robust/XAUUSD_L_H1_test1_v3_Strategy_8.1.22.z0_robust.sqx`.

3. **Verificación de Rutas y Efecto Colateral (Gap de C:/)**:
   - Se evidenció el problema del path absoluto: en Linux, el worker resolvió la ruta `C:/EchoForge/Builds/MT5/` concatenándola al directorio de SQX, escribiendo el archivo físicamente en:
     `/home/kor/sqx/C:/EchoForge/Builds/MT5/XAUUSD_L_H1_test1_v3_Strategy_8_1_22_z0.mq5`
   - Esto crea de forma indeseada una carpeta literal llamada `C:` dentro del directorio de SQX en Linux.
   - Valida al 100% que usar un path relativo dentro del databank del proyecto custom (`user/projects/custom/databanks/input/`) o dentro de `{sqxDir}/config/` solucionará este efecto colateral.

