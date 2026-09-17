```text
STATUS: M1_FABLE_CHALLENGE_COMPLETE

GITHUB:
- commit SHA: 23ed18145a0f2e0ddf1898a872e3693887df2036 (el cron de sync lo empaquetó como "sync 13:29"; contiene exclusivamente +244/−0 sobre el archivo permitido; baseline 4e95dcd / blob b78142b3 preservado íntegro)
- enlace: https://github.com/xKoRx/agents-os/blob/master/main/10-projects/Personal/Polymarket%20Engine/Polymarket%20Engine%20%E2%80%94%20MVP.md

REVIEW:
- P0: 0 (no se demostró ningún contraejemplo de doble efecto, ruta live no autorizada ni corrupción silenciosa)
- P1: 7
- P2: 5
- principales hallazgos:
  · FBL-001 intents UNKNOWN sin regla terminal → bankroll congelado indefinidamente
  · FBL-002 425/429/503 sin clasificar; "order timed out" re-firmado = doble orden; liberación tras cancel sin size_matched final
  · FBL-003 contradicción integridad DB↔journal vs GC 30 d y backup con DB por delante del journal → recuperación imposible o invariante vacío
  · FBL-004 revision_vector sin AccountView/RiskPolicy/liquidez → Evaluate irreproducible, G-07 inalcanzable
  · FBL-005 ledger virtual compartido entre POCs → falso NO_GO
  · FBL-006 ejecución multi-leg live sin owner → la POC reimplementaría secuenciación/unwind
  · FBL-007 cancel defensivo sin audit sin frontera contractual (DEGRADED_AUDIT / AUDIT_GAP)
  · P2: corte forward del Frame Builder, carriles EVIDENCE/RUNTIME + fsync por callback evitable, VOID de PREPARED/applied_seq por reducer/FillKey, redacción de `owner` + gate de imports, fee_rate_bps por trade como régimen

FREEZE:
- blockers exactos: FBL-001…FBL-007, cada uno con test de cierre (G-11/12, G-14 ext., G-07 SHADOW, G-10, drill G-13/14)
- owner decisions indispensables (M1 FREEZE): OD-1 modelo de confianza in-process; OD-2 partición FOUNDATIONAL NOW / IMPLEMENT LATER (F.7); OD-3 retención vida-proyecto de evidencia privada de cuenta. Live activation: A-06, A-20, A-23, A-24, parámetros FBL-001, U-06, U-08 permanecen deshabilitados sin decidir hoy
- deferred gates: G-05b, G-06b, G-07b, G-09b, G-10b, G-11b, G-12b, G-13b, G-15b (ninguno ejecutado)

ASTRA-2:
- orden de reconciliación: FBL-003 → FBL-010 → FBL-001/002 → FBL-007 → FBL-004/009 → FBL-006/005 → FBL-008/011/012 → actualizar M1.15/M1.16/M1.17
- criterio de aceptación: texto normativo integrado en la sección afectada + fila en M1.16 + test de cierre en M1.15 para cada FBL-001…007; OD-1…3 registradas como REQUIRES_OWNER; ninguna capability M0 deshabilitada reabierta; M1.0–M1.17 conservan autoría con enmiendas marcadas
```

Nota: la sección quedó en ~39 KB, sobre el presupuesto sugerido de 10–20 KB; lo justifican los 7 P1 con formato completo y las tablas F.3/F.7 que TOP necesita para acotar M2.