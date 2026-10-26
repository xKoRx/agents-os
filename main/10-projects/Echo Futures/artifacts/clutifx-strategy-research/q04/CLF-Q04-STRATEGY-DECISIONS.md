# CLF-Q04 — STRATEGY DECISIONS (conclusión accionable por estrategia)

Por fuente de señal real (10 fuentes de 19 campañas pagadas; ver SIGNAL-EQUIVALENCE). Los veredictos Q03R1 de gates/clasificación se mantienen; esto añade la lectura económica Q04 y la decisión sugerida.

## 1. Familia maestra 4h-13:00 — C02, C07, S03, S04, S05A, S05B, S09, S19, S20, S21 (+subconjuntos C03, S11, S16)
- **Hechos**: una sola fuente de señal; 3 ejecuciones/trimestre; 2W/1L; +$335,08 neto por cuenta; pico 26,5% del target; expectancia +$112/trade (positiva); sequía 44 días.
- **Diagnóstico**: técnicamente válida (G2C PASS propio, reconciliada), comercialmente inalcanzable en este diseño de cuenta: 3 ejecuciones no pueden ser 7 ganadores.
- **Decisión sugerida al Owner**: elegir UN representante de la fuente y decidir uno de: (a) autorizar eje de anclas/sesiones adicional para subir frecuencia (identidad NUEVA con G0→G4 propio, precedentes S06/S07/T01); (b) declarar la familia "edge real, no-aprobable-en-GAU50-1:1" y reservarla para perfiles con target menor o ratio >1:1; (c) archivar. Re-ejecutar el trimestre NO aporta información (bit-idéntico).

## 2. Anclas London/NY-madrugada — C01, C04 (+S01/S02/S17 modos TS)
- **Hechos**: emisiones fieles al curso a 01:00/05:00/09:00 ET; 0% en ventana; nunca compraron.
- **Diagnóstico**: incompatibilidad estructural curso-vs-cuenta (no defecto). Fichas KRR-001/002/004.
- **Decisión**: (a) identidad adaptada de ancla (NUEVA, autorizada) o (b) declarar no-operables en E2T y archivar con evidencia. Decisión única para las tres fichas (misma raíz).

## 3. Failure Swing — C06, S15, T04
- **Hechos**: ready 12.060/14.037; 0 setups en 69+9 sesiones; conjunción implementada = reacción+OB+motivo en 1 vela (la más estricta de las lecturas posibles).
- **Diagnóstico**: la rareza puede ser fiel (el instructor lo advierte: "no obsesionarse") o amplificada por la conjunción. Sin video no se adjudica.
- **Decisión**: KRR-003 REVIEW_VIDEO (ch06, minutos de R3/R11/R12). Prohibido relajar antes. Con la lección Q04: aun operando, FS necesitaría frecuencia de ≥7 ejecuciones limpias/trimestre para ser aprobable.

## 4. Anclas alternativas autorizadas — S06 (09:30/13:30), S07 (10:00/14:00), T01 (10:30/11:15/14:15)
- **Hechos**: S06 6 rt (2W/4L, −594,82) — la más frecuente, la única que podría teóricamente llegar con 7+ ejecuciones, y perdió; S07 3 rt (2W/1L, +295,06); T01 3 rt (0W/3L, −1.089,94).
- **Diagnóstico**: subir la frecuencia vía anclas alternativas es viable mecánicamente (S06 lo demuestra), pero la muestra negativa de T01/S06 conserva su evidencia (no se cambió nada para fabricar ganadores).
- **Decisión**: si el Owner persigue aprobabilidad, la palanca es frecuencia (más días con 2–3 señales en ventana), no más variantes del mismo ancla. Sugerencia: estudiar combinación ancla-NY-cash (eje S06) con la fuente maestra como identidad nueva pre-declarada.

## 5. Refinados — S12 (15m), S13 (30m)
- **Hechos**: comportamiento propio pero igual de escaso (2–3 ejecuciones; S13 perdió 2 admisiones por `SIZE_BELOW_MIN_CONTRACT`).
- **Decisión**: sin acción separada de la decisión global de frecuencia/objetivo; el size-refusal es correcto por diseño (ATR×$20 > $500 ⇒ q=0) y es una fricción adicional a considerar si se autoriza MNQ o presupuesto mayor (identidad nueva).

## 6. Bloqueadas — T02 (BLOCKED_SPEC), C08/T05 (BLOCKED_DATA), S08/T03 (NEEDS_ITERATION)
- Sin corrida propia; decisiones KRR-005/006/007. Prioridad sugerida: resolver anclas (1) antes que materializar S08/T03, para no gastar otro ciclo en identidades inalcanzables.

## Decisiones Owner nuevas no-KRR (de esta auditoría)
1. **Costeo**: compra cobrada a $120 (config declarada) mientras `profile.provider_fee $50 (FACT)` no se consume en el modelo de cash — validar el costo intencional o alinear el perfil (no afecta pases; afecta el costo/pase proyectado: $6.480 gastados / 0 pases).
2. **Catálogo canónico ausente**: restaurar `STRATEGIES-CATALOG.md` desde la capa por capítulo o degradar su estatus en el master.
3. **Política de duplicación**: 10 campañas bit-distintas por fuente equivalente costaron ~$3.480; definir regla (1 campaña por fuente + alias declarado) para ciclos futuros.
4. **Objetivo vs geometría**: la pareja (gross $500, 1:1, ATR-M1) con target $3.000 exige ≥7 aciertos limpios/cuenta; decidir si el diseño de cuenta (target, ratio, presupuesto) es una hipótesis iterable del Owner (declared config) o se congela como regla del challenge.
