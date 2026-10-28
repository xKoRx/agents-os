---
type: resource
schema_version: 1
status: active
area: "[[Trading]]"
sources:
  - "[[echo-futures-dr01-deep-research-2026-10-28-source]]"
last_verified:
confidence: low
aliases:
  - "DR-01 campañas prop"
  - "DR-01 matemática de campañas"
tags:
  - kind/resource
  - area/trading
  - project/echo-rnd
  - tech/futures
created: "2026-10-28"
updated: "2026-10-28"
---

# Echo Futures — DR-01 matemática de campañas prop

## Síntesis vigente

**Estado: RECEIVED_WITH_MATERIAL_FINDINGS; no validado ni aceptado como conclusión científica.** Recurso de investigación para [[Echo I+D — Futures]]. El retorno DR-01 plantea que resolver rápidamente evaluaciones NQ puede mejorar la economía de campaña aun sin esperanza positiva por trade, pero sólo si la distribución conjunta de pases, activaciones, retiros efectivos, costes y tiempo compensa el agotamiento de caja. No hay evidencia empírica NQ, RuleSet comercial seleccionado ni simulación ejecutada. La política agresiva es hipótesis a contrastar, no recomendación aprobada.

**Mandato Owner vigente:** bankroll Futures USD 4.000 sin aportes adicionales; Forex separado; NQ exclusivo (MNQ no autorizado); USD 400/funded es referencia no verificada; primer retiro USD 3.000 a distinguir bruto/neto con splits 80/90%; metas 5 challenge + 5 funded con retiros en dos props al 31-12-2026 son aspiraciones. Strategy = setup + filtro opcional + objetivo/riesgo técnico; MM por prop/programa/etapa es entidad distinta. G0–G5 no cambian.

**Modelo mínimo:** separar distribución de trades; resultado de cuenta/etapa; campaña compra→pase→activación→retiro(s); caja real del Owner. Para cada intento medir P(pase), P(activación|pase), P(cobro|activación), tiempo hasta cobro y desembolsos. El embudo q = P(pase) × P(activación|pase) × P(cobro|activación) es identidad de probabilidad condicional, no hipótesis de independencia. Cash neto = retiros efectivamente recibidos menos todos los desembolsos externos; PnL SIM, saldo funded nominal y aprobación pendiente no son caja. Evitar doble descuento de comisiones ya incluidas en PnL.

**Frontera de decisión:** comparar velocidad de resolución, probabilidad e importe del primer cobro, posteriores cobros, capacidad de financiar el siguiente intento, déficit máximo y riesgo de agotamiento antes del horizonte; sin score ponderado arbitrario ni objetivo obligatorio de supervivencia indefinida.

## Evidencia y provenance

- [[echo-futures-dr01-deep-research-2026-10-28-source]] — captura editorial del informe entregado el 28-10-2026; fuente primaria de *lo que afirmó el worker*, NO de su veracidad matemática ni comercial. Captura en `30-resources/futures/_sources/` (excluida del índice derivado).
- [[FUT-R01-RESEARCH-MANDATE]] — mandato DR-01 v4 y límites de autoridad.
- [[echo-futures-astra-math-review]] — revisión matemática anterior (2026-09-24), válida sólo dentro de sus supuestos estáticos/continuos; no prueba contratos path-dependent ni economía con bankroll finito.
- [[Echo I+D — Futures]] — planner de investigación, no proyecto de implementación.

## Límites y contradicciones

1. **ERROR MATERIAL DE CAJA:** el ejemplo del worker con p=0,20, fee=100 y payout=500 calculó 0,2×500−0,8×100=+20. Si el fee se paga en cada compra, EV=0,2×500−100=0 antes de activación/otros costes. Con payout 250, EV=−50, no −30. Además p_pass no equivale a q de cobro.
2. **ERROR DE IDENTIDAD:** USD 400 de desembolso no es equity nominal E0 ni distancia a barreras de evaluación. La fórmula gambler's ruin requiere estado relativo y barreras coherentes, pasos discretos unitarios, ausencia de overshoot y horizonte adecuado; no se aplica automáticamente a trailing intradía/EOD.
3. **SELECCIÓN NO PREDICTIVA POR SÍ SOLA:** pasar challenge selecciona caminos favorables pasados, pero no demuestra P(cobro funded|pase) mayor que un contrafactual con futuros IID. La dependencia debe estimarse, no presumirse.
4. **RUINA EVENTUAL MAL GENERALIZADA:** en una evaluación con dos barreras existe probabilidad positiva de pase incluso con drift no positivo. La ruina a horizonte infinito en otros procesos no autoriza afirmar que cada cuenta o campaña necesariamente falle.
5. **SIZING:** riesgo mayor puede cambiar probabilidades con saltos, costes, límites, lotes enteros NQ y barreras móviles; no sólo el tiempo hasta absorción. No confundir agresividad con martingala progresiva.
6. **TIEMPO:** el retorno dijo «~2 años hasta fin de 2026» pese a estar fechado 2026-10-28; horizonte real pendiente debe calcularse desde fecha de experimento.
7. **FUENTES INSUFICIENTES:** el worker cita Wikipedia y sitios comerciales sin trazabilidad primaria, autor, fecha, sección leída ni RuleSet oficial. No certificar cifras, contratos o conclusiones como HECHO.
8. **CENSURA Y CORRELACIÓN:** intentos abiertos no desaparecen de denominadores; cuentas con mismas señales NQ no son independientes. F/p_pass es sólo caso geométrico IID con fee fijo, no coste agregado real por funded ni por cuenta que paga.

**Experimentos propuestos, NO ejecutados:** (E1) señal NQ congelada × MM (bajo/alto/distancia/tiempo/etapa) × RuleSet × estado inicial × horizonte, con controles nulos y adversos, métricas de payout/caja/agotamiento; (E2) misma señal/MM bajo contratos abstractos con fees, caps, splits y elegibilidad, incluyendo un contraejemplo que destruya la asimetría. El frente interno debe especificarlos y autorizarlos sin inventar motor nuevo.

**Interfaces:** DR-02 → RuleSets, tarifas, elegibilidad, payout caps y restricciones oficiales; DR-03 → distribución/dependencia empírica de señales NQ; DR-04 → operacionalización objetiva, controles y validación; RV-01 → revisión independiente y adjudicación. Ningún gate G0–G5 queda aprobado por este documento.
