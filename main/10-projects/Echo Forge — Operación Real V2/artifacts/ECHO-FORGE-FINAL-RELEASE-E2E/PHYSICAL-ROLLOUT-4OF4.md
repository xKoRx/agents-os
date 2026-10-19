# PHYSICAL-ROLLOUT-4OF4 — Release 0.3.2 (2026-10-19)

## Veredicto

WORKER_ROLLOUT_4OF4_PASS — las cuatro superficies ejecutan físicamente los binarios 0.3.2 (PID correcto, path de release, SHA256 byte-exacto vs manifest, logs sanos, pollers activos, sin versiones mezcladas). El rollout fue aplicado por los stagers tras la publicación MinIO (16:53–16:55Z); la verificación es por canal SSH autorizado con credencial (el verificador automático del repo no tiene claves desde Daedalus — preexistente documentado).

## Matriz física

| Host | Superficie | PID | Evidencia |
|---|---|---|---|
| sqx-ulab-zeus-0 (192.168.31.101) | SQX worker 0.3.2 | 2933209 | exe=`/opt/stager/releases/0.3.2/bin/symphony`; SHA256 `6abfb00b…3491` byte-exacto; CURRENT=0.3.2; 699 refs `sqx-main-queue` en log; 0 procesos symphony fuera de 0.3.2 |
| sqx-ulab-hera-0 (192.168.31.111) | SQX worker 0.3.2 | 2158081 | exe y SHA idénticos; CURRENT=0.3.2; 2201 refs cola; 0 mezclados |
| sqx-ulab-kron-0 (192.168.31.121) | SQX worker 0.3.2 | 1132837 | exe y SHA idénticos; CURRENT=0.3.2; 2704 refs cola; 0 mezclados |
| worker-kronos (192.168.31.128) | MT5 worker Windows 0.3.2 | 10244 | PATH=`C:\ProgramData\Stager\releases\0.3.2\bin\sqx-mt5-worker.exe`; SHA256 `c65e4f5d…313c` byte-exacto; START 16:54:30Z (drain por stager) |

- Pollers verificados en Temporal `sqx-prop` al cierre del E2E: `sqx-main-queue` = 3 pollers (identidad `pid@sqx-ulab-<host>-0`), `sqx-mt5-queue` = 1 poller (`10244@worker-kronos@`), todos con lastAccess fresco.
- Releases antiguas permanecen en `/opt/stager/releases/` (rollback físico intacto); ningún proceso ejecuta binario distinto de 0.3.2.

## wave3f (mandato §5)

- `sqx-main-v1-ab32f685-7d14-482f-9d84-bd846339ec3f` (request `NDX_SQX_v1_wwave3f`, FlowRun `a7e7747a-…`): sigue RUNNING en namespace `sqx-dev` / cola `sqx-dev-queue`, historyLength 3, SIN pollers en su cola (los workers de flota operan `sqx-prop`/`sqx-main-queue`). **No cancelado ni modificado; aislado por namespace+cola; no interfirió con la campaña.**
