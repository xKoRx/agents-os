# CERT-NT-01 RESUME-04 — JSON SIM FINAL (paquete Owner, un solo dato pendiente)

Fecha: 2026-10-20 ~01:15Z · Submanager LOCAL GLM (mandato CERT-NT-01 / RESUME-04).

## Archivo entregado

`/home/kor/aranea/work/cert-nt-01-mgr/RESUME04-ADDON-JSON-SIM101-FINAL.json` (copia saneada en el vault:
`artifacts/runtime/cert-nt-01/RESUME04-ADDON-JSON-SIM101-FINAL.json`).

## Cambio respecto de la propuesta RESUME-03 (diff único y atribuible)

- `ntx_port: 9770 → 0` y `ntx_host` poblado (no vacío): **la lane de mercado del AddOn de ejecución queda DESHABILITADA**.
  Razón (mandato /execute §7, «resolver UNA autoridad de feed»): hoy el productor de mercado en :9770 es el AddOn D6
  (EchoFeedAddOn → relay `echo-nt-feed-relay`, PID 1388002, certificado N1, feed fluyendo). Con `ntx_port: 9770` existirían
  DOS productores simultáneos en :9770 (feed duplicado). Con `ntx_port: 0` el AddOn de ejecución NO diala mercado
  (`EchoExecutionAddOn.cs:422` — `marketPort <= 0 → return`, deshabilitación silenciosa y NO invalidante).
  Reversible: si el Manager designa a este AddOn como autoridad única de feed, bastan 2 líneas (`ntx_port: 9770` + retirar
  el AddOn D6) en un despacho de arming posterior.
- `ntx_host` DEBE quedar poblado: si estuviera vacío con bindings presentes, el parser hereda
  `bindings[0].host:port` = 9771 (`:184-188`) y la lane volvería a dialar el puerto de ejecución.

## Validación contra el parser real (ParseBindings, `EchoExecutionAddOn.cs`)

Validación estructural campo a campo contra el source del release (sha256 del `.cs` verificado abajo; la ejecución del
parser real NO fue posible: sin toolchain C# en host, 0/2 intentos documentados — la comprobación definitiva es la carga
en vivo del paso 2 del Owner):

| campo | valor | requisito del parser | estado |
|---|---|---|---|
| `auth_token` | placeholder «conservar el vigente» | no vacío (`:188`) | Owner conserva el suyo — jamás transitado por chat |
| `contracts` | NQZ6→«NQ 12-26» | ≥1 par (`contract_id`,`nt_name`) escaneo plano (`:278-288`) | OK |
| `snapshot_seconds`/`heartbeat_seconds` | 5/5 | >0 (`:189`) | OK |
| `bindings[]` | 1 binding | ≥1 (`:190`) | OK |
| `bindings[0].physical_binding` | `CERTNT01-SIM01` | no vacío + único (`:196,199`) | OK, coincide con snapshot ETCD (`sim:CERTNT01-SIM01`) |
| `bindings[0].host`/`port` | .161:9771 | host no vacío, port>0 (`:194-195`) | OK |
| `bindings[0].account_name` | `Sim101` | no vacío + único; resolución Name-primary (`:1029`) | OK |
| `bindings[0].account_id` | **PLACEHOLDER** | no vacío (`:195`); desigualdad con el Id real de la cuenta resuelta = `Drift=true` fail-closed (`:1073`) | **ÚNICO DATO PENDIENTE DEL OWNER** |
| `ntx_host`/`ntx_port` | .161 / 0 | port<=0 deshabilita lane sin invalidar (`:422`) | OK |
| `account_id`/`account_name` planos | placeholder/Sim101 | sólo identidad de feed; inertes con lane off | OK |

## Acción Owner (UNA sola, dos pasos mecánicos)

1. **Dar el dato:** en NinjaTrader (.132, Control Center → Accounts): ver la columna **ID** de la fila **Sim101**
   (clic derecho en el encabezado de la grilla → columnas, si no está visible) y reportar ese valor exacto.
   NO inferirlo de otra lista ni del orden.
2. **Instalar:** editar `C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json` reemplazando el contenido
   por el archivo entregado, sustituyendo los 3 placeholders (token vigente + ID de Sim101 en binding y en keys planos),
   y reiniciar NT. (Alternativa validada al armar: el submanager puede aplicar el archivo por staging TEMP si el Owner
   prefiere — el perfil KoR sigue ACL-bloqueado para el sandbox.)

## Verificación posterior (submanager, al armar)

- Log de carga del AddOn: `bindings=1`, resolución **RESOLVED** (no DRIFT/MISMATCH).
- Cero intentos de conexión del PID de NT hacia :9770 (lane de mercado off) y el dial :9771 sólo cuando exista listener.
- El feed D6 a :9770 sigue siendo el ÚNICO productor de mercado (HWM `echo.futures.market-feed-candidates.v1` avanzando con un solo emisor).
