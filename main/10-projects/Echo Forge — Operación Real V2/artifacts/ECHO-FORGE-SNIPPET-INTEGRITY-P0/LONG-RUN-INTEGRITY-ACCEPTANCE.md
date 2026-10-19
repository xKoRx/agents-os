# LONG-RUN-INTEGRITY-ACCEPTANCE — Snippet Integrity P0 (2026-10-19)

## Veredicto

`PASS_WITH_PENDING_OWNER_GATE` — el trigger identificado ya no puede producir la restauración/falso-éxito con el script corregido (demostrado candidate-local), la cadena fuente→bytecode está coherente y verificada en los 3 hosts, y los riesgos de drift de campañas largas están cubiertos por el gate pre-dispatch. El criterio §12 "observar el evento productivo indispensable" (un ciclo deploy→run productivo con el script nuevo) queda como gate abierto con procedimiento pasivo — no se certifica por anticipado.

## Evidencia de estabilidad post-incidente (producción real, sin intervención)

- El fuente S02 instalado 18:22:43Z sobrevivió sin drift: canary 3, E2E w11 completo (FlowRun `561267ed`, COMPLETED), 10 runs del cert CPU (proyecto flota, 19:05–19:27Z), 10 runs proyecto `custom` (19:35–19:49Z) y runs recurrentes del proyecto `EchoForgeMT5Exporter`.
- El mecanismo per-run de Build 144 (cada sqcli recompila y re-escribe cache + `Snippets.jar` desde el fuente) actúa como **convergencia hacia el fuente**, no como amenaza, cuando el fuente es el correcto: el rewrite masivo de 19:49:41Z dejó bytecode `3ec6e112…` verificado.
- Gates de integridad read-only finales: **PASS 3/3** (Zeus 23:0xZ, Kronos, Hera) — source `b5f85c4e…`, bytecode `3ec6e112…` en user/libs, Snippets.jar y cache, en los 3 hosts. Ver `RUNTIME-IDENTITY-MATRIX.csv`.

## Cobertura de los tres planos de código (§8)

| Plano | Estado | Verificación |
|---|---|---|
| Código cargado en una JVM en ejecución | Una JVM sqcli carga el bytecode una vez por corrida; no existe JVM long-lived que mezcle versiones. Campaña sana = bytecode de SU arranque, inmune a cambios de disco. | modelo de ejecución sqcli (proceso por corrida, verificado en logs: cada run es un `Bye`/`Exit app`) |
| Código en disco para la próxima actividad | Fuente + JARs + cache verificados coherentes por el gate (los 3 hosts). | `verify-plugin-integrity.sh` PASS 3/3 |
| Clases regeneradas en el próximo arranque | Se regeneran DESDE el fuente (autoridad). Fuente correcto ⇒ regeneración correcta; fuente divergente ⇒ gate lo detecta antes de despachar. | FASE B (precedencia) + Test D |

## Criterios long-run (§9) — cumplimiento

- Ningún proceso externo restaura código durante una ejecución: demostrado que jamás existió tal proceso; el único actor de escritura es el deploy (ahora fail-closed).
- Una actualización legítima no mata una ejecución sana: guard sqcli del deploy (probado: 3 aborts limpios en Kronos) + regla operacional de no-deploy con SQX activo.
- Mantenimiento respeta el singleton: invariantes vigentes; esta investigación corrió sin sqcli propio y respetando el activo.
- Runtime no mezcla versiones del exporter: fuente único por host + gate de coherencia total (source/JAR/JAR/cache).
- Cambio de source detectado ANTES de nuevas actividades: `verify-plugin-integrity.sh` (Test D detecta el estado exacto del incidente).
- Dos autoridades de despliegue compitiendo: NO — un solo script canónico propuesto; `sqx-instrument-sync` limitado a `user/data` (sin snippets); stager limitado a `/opt/symphony` con `ProtectSystem=full`.
- Rollout con estados verificables y rollback: sello live + `cmp` por superficie + `rollback.sh` con guard.

## Riesgo residual y su manejo

1. **Bug latente en otros scripts de deploy del workspace** (el patrón `&&` era específico del script; los scripts de release de binarios usan canales distintos — sin hallazgos, pero la regla general aplica: ninguna escritura sin verificación live). Mitigación: adoptar el patrón `swap_file` en cualquier futuro script de deploy.
2. **Ownership heterogéneo del dir de snippets (Zeus `echo-dev` vs Kronos/Hera `kor`)**: documentado como la diferencia causal; el gate es independiente del ownership. Normalización opcional al Owner.
3. **Deploys manuales fuera del script**: mitigación procedimental (gate obligatorio pre-dispatch).

## Procedimiento de observación pasiva (gate abierto — sin ejecutar)

En el próximo deploy de plugin autorizado por el Owner: (1) el operador corre `deploy-plugin.sh` con `EXPECTED_SRC_SHA256` del manifest; (2) corre `verify-plugin-integrity.sh` por host; (3) el primer run productivo siguiente queda observado por el gate repetido post-run (los 4 hashes deben seguir idénticos); (4) conservar sello + salida del gate en `backup/`. Con eso observado, LONG-RUN pasa de `PASS_WITH_PENDING_OWNER_GATE` a `PASS` sin nueva investigación.
