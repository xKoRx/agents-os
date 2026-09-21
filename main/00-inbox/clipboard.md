# MANDATO P0 — U-02: V1/V2 PROTOCOL AUTHORITY AUDIT

**Objetivo:** determinar si el modelo `TAKER_PROCEEDS` implementado en `d5ce263` corresponde realmente al venue aplicable. No implementar otro parche ni integrar código hasta obtener el dictamen.

## Evidencia nueva obligatoria

Polymarket completó Exchange V2 el 28-04-2026.

V1 `ctf-exchange` está archivado y su `CalculatorHelper` cobra BUY sobre tokens recibidos.

En V2 `Trading.sol`, la ruta BUY transfiere tokens completos y cobra fee adicional en collateral. El operador proporciona `takerFeeAmount`; el contrato valida límites, pero la configuración `fd` no equivale por sí sola a una prueba completa de la fee efectiva.

El Help Center aún describe BUY fees en shares. Debes reconciliar esta discrepancia.

Fuentes:

- `github.com/Polymarket/ctf-exchange-v2`
    
- `src/exchange/mixins/Trading.sol`
    
- `src/exchange/mixins/Fees.sol`
    
- documentación oficial de Exchange Upgrade
    
- documentación oficial de Trading Fees
    

## Tareas

1. Identificar el exchange aplicable a los mercados reales de PE-001 y a la familia de mercados objetivo. Registrar dirección, versión, collateral y evidencia.
    
2. Analizar las rutas BUY y SELL de V2: `_matchBuyOrders`, `_settleComplementary`, `_settleTakerOrder` y `_chargeFee`.
    
3. Obtener evidencia pública de liquidación: transacción, eventos, transferencias y fee efectiva. No ejecutar órdenes ni solicitar credenciales.
    
4. Determinar si la diferencia con el Help Center se debe a documentación desactualizada, otra capa de ejecución, compatibilidad V1 o un mecanismo distinto. Si no se demuestra, conservar `UNKNOWN`.
    
5. Comparar los contratos reales con `USDC_CASH` y `TAKER_PROCEEDS`. Explicar qué modelo representa cada uno y cuáles son las unidades de `q`, cash, shares y fee.
    
6. Auditar el diff `85e27ff..d5ce263`: 14 archivos y +1487 líneas requieren justificar alcance, invariantes y ausencia de regresiones.
    
7. Auditar los gates faltantes: Economics 91,2%, Regimes 94,8%, suite completa, race y correspondencia exacta entre SHA de código y certificado. No rellenar cobertura con tests cosméticos.
    

## Resultado obligatorio

Emitir UNO:

- `V2_CASH_CONFIRMED`: la evidencia del mercado demuestra BUY fee en collateral.
    
- `V1_SHARES_CONFIRMED`: la evidencia del mercado demuestra BUY fee en shares.
    
- `MIXED_BY_MARKET`: se demuestra que ambos mecanismos aplican y se identifica el discriminador.
    
- `PROTOCOL_UNRESOLVED`: la evidencia no permite resolverlo.
    

Para cada resultado, entregar fuente primaria, pruebas, impacto sobre el código actual y cambio mínimo necesario.

Si encuentras una diferencia, prepara el plan de corrección, pero **no lo ejecutes en este mandato**.

No merge, push, live, órdenes, wallet ni signing. Mantener `REAL_FEE_READY=false`. Preservar v07/v08, actualizar continuidad y dejar la sesión Agents-OS abierta.