STATUS: `M1_ASTRA_PROPOSAL_READY_FOR_FABLE`

Publicación verificada en `master`; commit final [`4e95dcd`](https://github.com/xKoRx/agents-os/commit/4e95dcd1a7a605c210e7f421933d48b3477451f9). Contenido previo y M0 preservados; M1 no está congelado.

DESIGN:

- Propuestos: ownership único, SQLite + journal durable + Parquet, replay reproducible, runtime común y autorización live centralizada.
- Owner: límites de capital, wallet, retención/backups y aceptación de riesgos operacionales.
- Incertidumbres: continuidad WS, fees efectivas, auth, finality y contratos v2.
- Deshabilitados: conversiones NegRisk live, backfill L2, `deferExec=true` y Builder. Combo/RFQ fuera del MVP.
- Registradas 35 decisiones, 19 gates `NOT_RUN` y 10 incertidumbres.

FABLE HANDOFF:

- Cuestionar cutover REST/WS, durabilidad/determinismo, órdenes ambiguas, conciliación de capital, permisos y realismo de fills.

NEXT:

- FABLE adversarial challenge.s