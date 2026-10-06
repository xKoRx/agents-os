---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
  - area/echo
  - project/echo-futures
  - tech/market-data
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 NT8 Candle Acquisition

## Propósito

Registrar evidencia RO sobre la lista y el formato de los exports físicos NinjaTrader 8 destinados al baseline NQ Last 1m de BTG-S01, y delimitar lo que falta para adquirir y validar los bytes originales.

## Contenido

**Estado de esta entrega:** `BLOCKED_ACQUISITION_POLICY`. La lista remota y las muestras de inicio/fin son legibles por `dev-win` viewer, pero los bytes completos no fueron adquiridos; no hay copias originales locales, SHA-256, conteos de filas ni validación exhaustiva del dataset.

**Origen declarado por el owner:** exports reales NT8 de NQ `Last` en `C:/Temp/history`, todas las velas disponibles, en `dev-win`. El destino local solicitado para las originales no se materializó. La ruta de origen se conserva como ruta remota relativa al host, no como autoridad de zona horaria.

**Proveniencia y corte:** lectura mediante `mcp__aranea_ssh__read_command` con profile `dev-win`, identificado por `list_connections` como conectado a `192.168.31.132`, identidad `echo-dev`, rol viewer. Corte: 2026-10-06, zona horaria del host no verificada. `ls C:/Temp/history` devolvió 13 archivos regulares con longitudes exactas; `cat -TotalCount 1` y `cat -Tail 1` leyeron únicamente los extremos de cada archivo; para `NQ 12-23.Last.txt` también se leyó una muestra de sus primeras ocho filas.

| Archivo remoto | Bytes reportados por `ls` | Primera fila observada | Última fila observada |
|---|---:|---|---|
| `NQ 03-24.Last.txt` | 4,675,351 | `20231207 030100;16011;16011;16010.5;16011;11` | `20240311 030000;18015.5;18015.5;18010.25;18010.5;60` |
| `NQ 03-25.Last.txt` | 4,619,576 | `20241212 032000;22028.75;22029;22028.75;22029;2` | `20250317 030000;19606.25;19609;19601.25;19602.5;167` |
| `NQ 03-26.Last.txt` | 4,643,433 | `20251211 030100;25803;25803;25798.5;25798.5;3` | `20260316 030000;24493;24493;24490.75;24492;10` |
| `NQ 06-24.Last.txt` | 5,116,132 | `20240307 030100;18195.25;18195.25;18195.25;18195.25;1` | `20240617 040000;19700.5;19700.75;19700.5;19700.5;7` |
| `NQ 06-25.Last.txt` | 4,748,996 | `20250313 030100;19802;19802;19802;19802;1` | `20250616 040000;21691.5;21693;21691;21691.25;6` |
| `NQ 06-26.Last.txt` | 4,717,302 | `20260312 030300;24953.25;24957.25;24945;24947.75;24` | `20260612 040000;29531;29531.25;29524;29528.5;53` |
| `NQ 09-24.Last.txt` | 4,786,556 | `20240613 040100;19898.5;19898.75;19897.25;19897.25;8` | `20240916 030000;19517;19518.25;19516.75;19518.25;13` |
| `NQ 09-25.Last.txt` | 4,763,462 | `20250612 040200;22037;22041;22037;22041;3` | `20250915 030000;24118.25;24118.5;24117.75;24118.25;13` |
| `NQ 09-26.Last.txt` | 4,946,204 | `20260608 040200;29502.5;29502.5;29502.5;29502.5;1` | `20260914 030000;29054.5;29057;29050.75;29053.5;53` |
| `NQ 12-23.Last.txt` | 3,617,895 | `20231001 220100;14965;15010;14957.25;14997.25;1421` | `20231211 030000;16053.5;16054;16053.25;16053.5;35` |
| `NQ 12-24.Last.txt` | 4,802,883 | `20240912 030100;19513.25;19513.25;19513.25;19513.25;1` | `20241216 030000;21815;21817;21814.25;21817;40` |
| `NQ 12-25.Last.txt` | 4,750,090 | `20250911 030400;24143;24143;24143;24143;1` | `20251215 030000;25261.75;25262.75;25261.75;25262.25;16` |
| `NQ 12-26.Last.txt` | 1,269,678 | `20260910 030400;29724.75;29725;29724.75;29725;2` | `20261006 035000;31349.75;31349.75;31348.75;31348.75;4` |

**Formato observado:** las filas de muestra no tienen encabezado y contienen seis campos delimitados por punto y coma: `YYYYMMDD HHMMSS;open;high;low;close;volume`. Las primeras ocho filas de `NQ 12-23.Last.txt` avanzan en intervalos de un minuto; esto es evidencia de muestra, no validación de todas las filas. Las marcas de tiempo no contienen offset ni zona horaria explícita.

**Manifiesto parcial:** los 13 nombres y tamaños anteriores son el inventario remoto del corte. `REMOTE_EXPORT_LIST_CONFIRMED=YES`; `SAMPLES_READABLE=YES`; `RAW_BYTES_ACQUIRED=NO`; `LOCAL_ORIGINALS=NONE`; `SHA256=NOT_AVAILABLE`; `ROW_COUNTS=NOT_AVAILABLE`; `FULL_VALIDATION=NOT_RUN`.

**Bloqueo de transferencia:** `sftp_download(profile="dev-win", remotePath="C:/Temp/history/NQ 12-23.Last.txt")` respondió `POLICY_DENIED: Profile "dev-win" is read-only, so "safe" commands are refused. Clear readOnly on the profile to allow them.` No se reintentó SFTP con otra identidad. Un intento acotado con `Get-Content -LiteralPath ... -TotalCount 8` también recibió `POLICY_DENIED`; no se repitió. El comando allowlisted simple `cat -TotalCount 8` sí fue aceptado y produjo la muestra indicada. Un intento `grep -m 8 '^' ...` ejecutó en PowerShell y falló porque `grep` no existe en el host. No se usaron comandos de mayor privilegio, shell alternativo, canal lateral, pipelines ni volcado base64.

**Límites de análisis:** al no disponer de bytes completos ni de un hash remoto aprobado, no se calcularon SHA-256, conteos de filas, orden, duplicados, rangos completos, validez OHLCV, tick size/grilla, distribución de gaps ni semántica de sesión/zona horaria. Las marcas first/last son extremos observados por archivo; las distancias entre ellas y los límites de expiries no se clasifican como gaps de datos. No se interpoló ni se atribuyó un timestamp UTC.

**Siguiente paso:** adquirir los 13 archivos completos y byte-exactos únicamente cuando el canal SFTP autorizado acepte la descarga RO o exista una decisión owner que habilite explícitamente un mecanismo de transferencia permitido. Luego registrar SHA-256 y tamaño por original, validar parser/formato y analizar cronología, duplicados, OHLCV, grid y gaps sin interpolación; conservar las discontinuidades como evidencia.

## Fuentes

- `30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md` — target `dev-win` pertenece al track Echo; la asignación no implica permisos físicos.
- `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` — selección de capability y autoridad mínima; no usar perfil alternativo para sortear denegaciones.
- `30-resources/runbooks/aranea-ssh-mcp.md` — comandos `read-command` allowlisted, límites por profile y tratamiento de `POLICY_DENIED` como frontera.
- `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTG-PLAN.md` — programa BTG-S01 y baseline histórico como gate previo.
