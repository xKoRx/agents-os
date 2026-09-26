---
type: session_feedback
schema_version: 1
created: "2026-09-26"
updated: "2026-09-26"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[aranea-agent-dev]]"
severity: high
category: environment
load_policy: manual
indexable: false
tags:
  - kind/feedback
  - scope/session
---

# Feedback — Shot Precision: autoridad de flota degradada bloquea operación de campaña (2026-09-26)

## Observaciones

1. **El rol `operator` del MCP ssh ya no puede ejecutar comandos privilegiados en la flota** (`privileged-command` ⇒ `POLICY_DENIED` para host group `dev`), y `echo-dev` (uid 1001, sin grupos secundarios) no tiene escritura en `/home/kor/sqx/user/configs` (kor:kor 775). Las sesiones 8.ª/9.ª propagaron CFX Zeus→Hera/Kronos y hoy esa operación es imposible para el agente: el despacho wave1d de 727 Precision quedó gated a una acción manual del owner (§F del evidence pack) pese a tener todo lo demás listo (release 0.2.109 rollout 3/3, config SPEC_VALID). Recomendación: decidir el mecanismo durable — re-habilitar `privileged` acotado a `sqx` para operator, o un runbook owner de propagación de configs CFX a la flota (hoy no existe como runbook canónico; se improvisa scp ad-hoc cada campaña).
2. **El estado de `known_hosts` de la flota no persiste entre sesiones** (Zeus sin `~/.ssh/known_hosts` de echo-dev; el re-add de las sesiones 8.ª/9.ª desapareció): cada campaña repite la verificación anti-MITM y el re-add. Además el MCP redacta claves públicas/fingerprints (`[REDACTED:entropy]`), lo que impide verificar host keys por doble camino usando los hosts mismos como fuente. Sugerencia: persistir las host keys ed25519 de la flota como recurso de referencia (sin material privado, son públicas) o fijarlas en el provisioning del MCP.
3. **El screen `deployer` de Daedalus sigue muriendo/congelándose en silencio** (hallazgo recurrente BEFORE_C6): `deploy_release.sh` tuvo que detectarlo, respaldar log y re-levantarlo durante la publicación de 0.2.109. Tercera ocurrencia documentada.
4. **Tests de `sqx/workflows` con deuda de entorno (19 fallos preexistentes en master)**: varias suites de integración exigen actividades/infra no registradas en el harness (`flow_run_start` no registrado) y fixtures que se ensucian por corrida (`phase4_performance.json`, `f5_warning_example.json`); cualquier comparación de regresión debe hacerse por diff de fail-sets master↔rama, no por "suite verde". Funciona, pero conviene registrar el fail-set baseline canónico por release para no re-descubrirlo cada shot.
5. **La skill `sqx-instrument-sync`/`sync_user_data_zeus.sh` no fue encontrada en esta sesión** (ni en Zeus como echo-dev ni referenciada en el vault desde el router): la sync de datos del owner (26-sep, hash `07f1f285` EQUAL 3/3) existió pero su mecanismo no es reutilizable por el agente hoy; para propagación de CFX/datasets conviene ubicarla o canónica­rla junto al punto 1.

## Lo que funcionó bien

- El patrón "extensión mínima del registro contractual existente" (amendment Import ya probado) cerró el gap producer retester con 8 toques quirúrgicos y cero engine nuevo; los fail-sets por diff master↔rama dieron confianza de cero regresión sin suites de integración completas.
- El validador del propio repo (`runtime.ValidateWorkflowSpec`) como gate pre-dispatch de la config del FlowRun: `flow-wave1d.json` quedó probada SPEC_VALID sin tocar producción, eliminando una clase entera de fallos de despacho.
- El owner operando en vivo (despliegue de CFX nuevos en Zeus + cierre de GUI) se detectó por lectura de estado (SHAs, pgrep) en vez de asumir staleness — evitó tanto un bloqueo falso como una propagación innecesaria.
