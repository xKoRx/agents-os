# Kafka CP primero — checkpoint de fuente 2026-10-02

**La suite completa del CP todavía no está acreditada.** Implementación y controles locales PASS;
CP→Kafka→resultado→KVS y repetición independiente completa permanecen NOT_EXECUTED.

- CP `feature/kafka-real-e2e` commit local `5b038f52a8bf4c11deabb86143ff4d4decaefc60`; checkout limpio.
- Knowledge `docs/kafka-real-e2e` commit local `0c3448a14f3d8f2318a1c34d964ab57561917a20`; checkout limpio.
- `realIntegrationTest` compila. Setup `sandbox.py up --scope cp` usa sólo el alias KVS propio del CP.
  Launcher/Gradle verifican scope; no exige Playmaker/MySQL/Entity/Tiger/ACME ni OAuth/BigQueue administrados.
- Harness72 controles PASS. Revisión independiente source/metadata y documentación PASS; REDs preservados.
  No servicio/SDK de negocio se ejecutó en estos controles.
- Knowledge estructural/histórico/diff PASS; formal FAIL idéntico al baseline conocido,0 findings nuevos.

Bloqueo inmediato: renovar Fury interactivamente con
`/Users/rjara/.pyenv/versions/3.10.16/bin/fury login` en este equipo.
Después revalidar clone del KVS propio CP `triggers-status-nonprod`; autenticado antes devolvió403,
pero no se revalidó tras expirar la sesión. Si persiste, habilitar permiso o indicar otro alias propio.
Los dos BC anteriores se limpiaron; no hubo instancia ni escrituras KVS.

Desde `/Users/rjara/fuentes/rio-controlplane-kafka-e2e`, tras provisionar Sandbox propio:

```sh
"$E2E_FURY_PYTHON" e2e/sandbox.py up --scope cp --cp-service <alias-propio>
E2E_KVS_ENV_FILE=<directorio-privado-impreso>/sandbox.env ./e2e/run.sh realIntegrationTest
```

Revisar `e2e/README.md` para JDK25/Docker propio, correlación, startup y cleanup condicionado.
Probar create exclusivo, versión del servidor, CAS válido/obsoleto, incremento y TTL; ejecutar suite
completa y repetir desde checkout limpio con revisor independiente. CI real sigue NOT_EXECUTED;
el dispatcher vigente agrega cuatro familias, sin job CP-only separado todavía.

`delivery-index.json` y parches delta/completos fijan bases/heads. Los receipts conservan fallos
antes/después, fuentes exactas y hashes. El paquete anterior `2026-10-02-kafka-e2e-blocked` queda
histórico intacto. Esta sesión AGENTS OS continúa activa/parcial; sin push, PR ni release.
Tokens/coste atribuibles: desconocidos, la plataforma no los expone aquí.
