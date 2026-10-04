# OWNER CHECKLIST W2 — Reinstalación EchoExecutionAddOn (fix parser config, 2026-10-03)

**Qué pasó:** el bundle anterior (d361008b) stageado en `C:\Temp\EchoD6Bundle` lleva un
`EchoExecutionAddOn.cs` cuyo parser numérico rechaza la config pretty-printed que el propio
bundle instala: con `"ntx_port": 9771` (espacio tras los dos puntos) el parser cae a `0` y el
gate fail-closed deja el AddOn HARD-DOWN con "config FAILED" en el log de NT, aunque el JSON
sea válido. Defecto reproducido físicamente en dev-win (.NET real): parser viejo 5/14
vectores, parser fixeado 14/14 (ver `PARSER-VERIFY.txt` en la carpeta del bundle).

**Qué cambia:** SOLO `EchoExecutionAddOn.cs` (hash nuevo `2c8ab2cf…`). `EchoFeedAddOn.cs` y
`echo-execution-addon.json` están byte-idénticos a lo anterior. Bundle re-stageado en la misma
carpeta `C:\Temp\EchoD6Bundle`; si ya habías instalado la versión anterior, estos comandos
reemplazan los archivos (idempotente). Si nunca instalaste, es la instalación normal.

**Pasos (≈2 min):**

1. Cerrar NinjaTrader si está abierto (el install lo verifica y aborta si no).
2. Instalar (PowerShell, sesión Owner):
   ```powershell
   & "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"
   ```
   Debe terminar en `INSTALL_ECHO_D6 = PASS` (verifica SHA256 de los 3 archivos contra el bundle).
3. Abrir NinjaTrader (compila los AddOns al arranque). **0 errores de compilación** esperados.
4. Verificar (read-only, no toca nada):
   ```powershell
   & "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"
   ```
   Debe terminar en `VERIFY_ECHO_D6 = PASS`.
5. (Nueva) Confirmar en el log de NinjaTrader la línea:
   `EchoExecutionAddOn config loaded: ntx=192.168.31.1*9771 account=****1551 contracts=1`
   — **NO** debe aparecer `EchoExecutionAddOn config FAILED`. Si aparece FAILED, copiar el
   output textual a `C:\Temp\compile-errors.txt` y avisar por el canal habitual.

**No enviar ninguna orden.** El AddOn sólo observa y se conecta; sin comandos del bridge no hace nada.

**Verificación externa posterior (agente):** hello del AddOn de ejecución en el bridge :9771 con
`expected_account_name RJARA114411201551` y snapshot venue real, cuando el bridge esté corriendo
con la sesión habilitada.
