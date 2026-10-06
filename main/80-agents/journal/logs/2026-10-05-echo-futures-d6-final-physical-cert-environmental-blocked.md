# Change log — D6 Final Physical Certification intento 2 (ENVIRONMENTAL_BLOCKED)

- **Fecha:** 2026-10-05 (lunes 19:05–19:20 CT; evidencia 00:05–00:20Z)
- **Entidad:** [[Echo Futures]] — sección D6 nueva "FINAL PHYSICAL CERTIFICATION intento 2: ENVIRONMENTAL_BLOCKED"
- **Artifact creado:** `10-projects/Echo Futures/artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION.md` (+ `evidence/g-final-evidence.txt`)
- **Delta del hecho canónico:** el ladder físico final autorizado (OD-D6-1) quedó `ENVIRONMENTAL_BLOCKED` por gate B `CURRENT_MARKET_FRESHNESS = STALE`: la conexión NT↔venue "Simulación" emitió `ConnectionLost @ 2026-10-05T04:40:54.675Z` y `MarketData RESET "NQ 12-26" @ 04:44:46.428Z` sin reconexión (evidencia del sink del relay); Kafka sin eventos desde 04:40:06Z pese al reopen de 17:00 CT. Ladder detenido antes de armar egress.
- **Integridad:** C0–H y G-REALTIME frozen intactos @ `d08a30ce`; G-EGRESS-0 preservado (unidad inactive+disabled, `:9771` free, ETCD 21 claves == baseline, `accounts` ABSENT); 0 órdenes; venue plano; 0 commits; cero mutaciones ETCD/config.
- **Próximo paso:** OD-D6-3 conditional — ciclo owner GUI reconecta "Simulación"/NQ 12-26; con probe §M verde, Manager re-despacha el ladder congelado completo en la primera ventana admisible.
