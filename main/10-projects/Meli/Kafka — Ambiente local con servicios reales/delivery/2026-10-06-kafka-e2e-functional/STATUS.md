# Validación funcional CP Kafka — activa

Backend autorizado: mapa por instancia, Kafka real. Fury Sandbox retirado del alcance local por el owner. Playmaker/ecosistema y transportes/proveedores administrados se verifican aparte.

- PASS de prerrequisitos: 68 clases/880 unitarios, cero FAIL/error/skip; compilación E2E, harness,20 controles de evidencia y bootJar. No es PASS E2E.
- FAIL conservado: baseline `cc21725628c84592b64113606ff072e7`,348/87 FAIL/0 error/skip,cleanup PASS.
- FAIL conservado: candidato3661388 corrida `ba6f97e381c24319961fa0e36dfc1bd0`,360/211 FAIL/0 error/skip,cleanup RETAINED. Retiro manual separado de recursos propios, sin cambiar el veredicto.
- FAIL conservado: candidato4df8822 corrida `d01cf0fbd82442fd80158dfc898e75ff`,359/349 PASS/10 FAIL/0 error/skip,cleanup PASS.
- FAIL más reciente: candidato db7f279, corrida `7bbf862d57d648d0b3ca6ecafc9abcd1`, 359/350 PASS/9 FAIL/0 error/skip, cleanup PASS; Docker propio confirmado vacío.
- Corrección implementada por GPT-6 Luna, congelada en b791048: precondición PEEK visible al CP, dos causas distintas de repetición DELETE, cuatro matchers de interrupción y dos precondiciones de config para deadline RF real. Contratos canónicos y oráculos conservados; SPEC antes de código.
- Pendiente obligatorio: nueva corrida física completa sin filtros y reproducción independiente completa desde clone limpio.
- CI NOT_EXECUTED: workflow en rama de trabajo fuera de default develop; acceso repo pull/push confirmado, API runners404. Falta integración y runner calificado Docker≥5GiB/Java25/Maven interno; no inferir ausencia de runners ni falta VPN.

Fuentes canónicas revalidadas2026-10-06: CPmaster `f74e856ef3de881e2d504c6cb1ced573681c1058`, develop `4302481c69300074a85ea5eb051a27bbd505cdce` (ancestro del candidato), KLmaster `de7cde85f7dd83a673c918e22ae9f08a0f7e05bd`. Master leído confirma routing ambiguo first-match. Cambios nuevos WORK_BRANCH_PENDING. Coste/tokens desconocidos.

Sesión activa, sin cierre ni declaración de entrega completa. Paquetes baseline/,candidate-red-1/,candidate-red-2/,candidate-red-3/ conservan evidencia sanitizada y hashes.

Cuarto intento de suite: `b791048`, run `2d88001ba3e04d3495494415896328b2`, FAIL antes de ejecutar (0 tests): cinco brokers saludables dentro de Docker, host ports unreachable30s; cleanup PASS. No es FAIL de negocio ni PASS. Infra recuperó sólo Colima propio mediante gRPC soportado por Lima1.0.5; ApiVersions5/5 y cleanup probes PASS. Causa SIGKILL SSH desconocida. Sin tocar VPN/default. El quinto intento completo está activo desde mismas fuentes congeladas.


Quinto intento EN_EJECUCION, no certificado: `b7910487c6a5336e128f9452b96f1e1641aa1740`, run `c6e8062a5de64da7af9663e7f6cfa128`, sesión32754. Readiness Kafka PASS y pruebas nativas activas sin filtros. Revisión source/schema independiente PASS, clean-v4 497 archivos/15pins listo para replay después de terminar y limpiar root. `runtime-grpc-readiness/` conserva límites/comandos/hash; sólo acredita conectividad.
