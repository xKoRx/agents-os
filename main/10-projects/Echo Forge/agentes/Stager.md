---
type: project
owner: agent
root: false
status: completed
priority: P1
area: "[[Echo]]"
application: "[[stager-app]]"
parent: "[[Echo Forge]]"
sprint: "[[A26Q2S7]]"
start: 2026-08-08
due:
progress: 100
repo: stager
jira:
prs:
aliases:
  - Independent Stager
  - Deployment Stager
tags:
  - kind/project
  - area/echo
  - tech/go
  - tech/deployment
created: 2026-08-08
updated: 2026-08-10
---

# Stager

> [!info]+ Stager
> **Área:** [[Echo]] · **Estado:** completed · **Prioridad:** P1 · **Parent:** [[Echo Forge]]
> Proyecto Go independiente. [[Symphony]] es el primer consumer, no una dependencia.

## 🎯 Objetivo

- Construir el mínimo stager independiente que reconcilie un manifest remoto en MinIO con una instalación local versionada, para `linux-amd64` y `windows-amd64`, emita `CURRENT`/`PENDING` y termine.
- Demostrar el MVP con Symphony/SQX sin importar paquetes de Symphony ni retirar el stager Bash durante la coexistencia.

## 📊 Estado actual

- Repositorio Git local y módulo independiente creados: `Stager` / `github.com/xKoRx/stager`; no se creó remote ni commit.
- Slices 1–2 implementados: manifest tipado aditivo, MinIO, plataforma estricta, `RunOnce`, verificación streaming, release versionada, lock y activación recuperable con `PENDING.next`.
- Evidencia: `go test ./...`, `go vet ./...` y builds `linux-amd64` / `windows-amd64` pasan desde el source final; scan no encontró imports de Symphony ni secretos hardcodeados; lint del vault y consulta Graphify pasan.
- Validación externa sin acceso al código: aprobación para integrar (~9/10); confirma la frontera, `PENDING.next` y el corte YAGNI. Sus precisiones quedaron incorporadas en docs y en la entidad [[stager-app]].
- Listo para revisión humana. La siguiente iniciativa real comienza en Symphony: publisher aditivo, Linux shadow/parity, quiesce Windows y launcher SCM.
- **Cerrado por el owner (2026-08-09).** El MVP y su integración Symphony quedaron aceptados. La evolución productiva de activación durable, runtime Linux/Windows y retiro del bridge se ejecutará separadamente en [[Stager - Cross-Platform Deployment Lifecycle]]; no reabre este MVP ni incorpora Symphony al core.

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%

- [x] Auditar el contrato real de publisher, manifest, stager Bash, CURRENT/PENDING, workers y supervisores #owner/agent #type/research #area/echo
- [x] Elegir nombre, módulo, scope y arquitectura MVP independiente #owner/agent #type/research #area/echo
- [x] Crear repositorio Go local con documentación y scaffold mínimo #owner/agent #type/dev #area/echo
- [x] Implementar manifest tipado y selección estricta de plataforma #owner/agent #type/dev #area/echo
- [x] Implementar MinIO source y `RunOnce` #owner/agent #type/dev #area/echo
- [x] Implementar stage verificado, lock, `CURRENT`, `PENDING.next` y `PENDING` #owner/agent #type/dev #area/echo
- [x] Cubrir core/filesystem con tests de error e idempotencia #owner/agent #type/dev #area/echo
- [x] Verificar builds `linux-amd64` y `windows-amd64` #owner/agent #type/dev #area/echo
- [x] Documentar integración y slices pendientes de Symphony/Windows launcher #owner/agent #type/dev #area/echo
- [x] Reconciliar proyecto precursor, parent, change log y Graphify #owner/agent #type/admin #area/echo

## Contrato MVP

### Input

- Manifest remoto en MinIO.
- Plataforma local resuelta desde `runtime.GOOS` + `runtime.GOARCH`, con override sólo explícito.
- Configuración local: endpoint/bucket/key, credenciales e installation root.

### Process

1. Tomar un lock local cross-process.
2. Recuperar una activación incompleta si existe `PENDING.next`.
3. Descargar y decodificar el manifest.
4. Seleccionar exactamente la plataforma local; nunca hacer fallback.
5. Comparar desired release con `CURRENT`.
6. Descargar a un directorio temporal dentro del installation root.
7. Verificar path, tamaño y SHA-256 antes de promover.
8. Promover a `releases/<version>`.
9. Escribir `PENDING.next`, luego `CURRENT`, luego promover el intent a `PENDING`.
10. Salir con resultado `noop`, `staged` o error.

### Output

- Release local completa y versionada.
- `CURRENT` con la release seleccionada para el próximo arranque.
- `PENDING` con la intención de upgrade consumible por cualquier proceso externo.

## Fronteras

| Pieza | Hace | No hace |
|---|---|---|
| Publisher | Construye, calcula hash/size, sube archivos y publica manifest al final | No toca hosts |
| Stager | Resuelve, descarga, verifica, instala, selecciona y emite upgrade intent | No ejecuta ni mata workers |
| Consumer/worker | Decide cómo drenar al observar `PENDING` | No descarga releases |
| Supervisor | Mantiene el proceso vivo y ejecuta lo indicado por `CURRENT` | No selecciona ni descarga releases |

El core no conoce SQX, MT5, MetaTrader, Temporal, strategies, task queues ni workflows de Echo Forge.

## Modelo de release y manifest

El wire contract está diseñado para una migración aditiva compatible. Se preservan `app`, `feature`, `version`, `artifacts`, `update` y `notes`; cada plataforma agrega sólo lo necesario para el nuevo consumer. Symphony todavía no es compatible hasta que su publisher emita estos campos:

```json
{
  "app": "symphony",
  "feature": "sqx-worker-minio",
  "version": "0.3.0",
  "artifacts": {
    "linux-amd64": {
      "entrypoint": "bin/symphony",
      "files": [
        {
          "path": "bin/symphony",
          "object_key": "worker/sqx/0.3.0/linux-amd64/symphony",
          "size": 123,
          "sha256": "<64 hex>",
          "executable": true
        }
      ]
    },
    "windows-amd64": {
      "entrypoint": "sqx-worker.exe",
      "files": []
    }
  },
  "update": {
    "strategy": "stage_mark_pending"
  }
}
```

Los campos legacy Linux pueden coexistir durante la migración. El nuevo Stager requiere `files` verificables para activar; no degrada silenciosamente a artefactos sin integridad.

Stager requiere la plataforma local exacta y no obliga por sí mismo a declarar ambas. Antes de integrar, Symphony debe decidir explícitamente si una release soportada por la flota exige Linux+Windows o si admite un subconjunto declarado.

## Estado local mínimo y atomicidad

```text
<root>/
  releases/<version>/...
  tmp/...
  CURRENT
  PENDING
  PENDING.next
  stager.lock
```

- `CURRENT`: release seleccionada para el próximo arranque; puede diferir de la release que todavía está ejecutándose.
- `PENDING`: solicitud de upgrade. Su consumer decide el drain.
- `PENDING.next`: intent transitorio de activación, no un journal general.
- `stager.lock`: lock local; no usa ETCD/Redis/DB.

Protocolo:

```text
release verificada
→ atomic write PENDING.next=N+1
→ atomic write CURRENT=N+1
→ atomic rename PENDING.next→PENDING
```

Recovery al comienzo de cada `RunOnce`:

- `PENDING.next` inexistente: continuar normalmente.
- `PENDING.next=N+1` y release completa presente: completar `CURRENT` y promover `PENDING` idempotentemente.
- intent inválido o release ausente: fallar sin inventar estado ni borrar la instalación anterior.

Esto cierra la ventana `CURRENT=N+1 / crash / PENDING ausente` sin DB, event sourcing ni `ACTIVATION.json`.

## Arquitectura

```mermaid
flowchart LR
    Pub["Publisher"] --> MinIO["MinIO + manifest"]
    MinIO --> Run["stager RunOnce"]
    Run --> Stage["download + SHA-256/size"]
    Stage --> Rel["releases/version"]
    Rel --> State["PENDING.next → CURRENT → PENDING"]
    State --> Consumer["consumer drains and exits"]
    Consumer --> Supervisor["systemd or Windows launcher"]
```

## Linux y Windows

- Linux: systemd timer ejecuta Stager; systemd supervisa el worker. El Bash legacy permanece como rollback durante la paridad.
- Windows: Task Scheduler ejecuta Stager. Un launcher SCM mínimo adapta service lifecycle a un worker foreground, relee `CURRENT` después de cada salida y aplica backoff.
- El launcher no descarga, no consulta MinIO, no hace staging, no conoce MT5/Temporal y no se autoactualiza.
- No se requieren symlinks NTFS. El path activo se resuelve leyendo el archivo `CURRENT`.

## Plan de implementación

### Slice 1 — Manifest + MinIO + status/noop

- Modelo tipado compatible con el JSON actual y campos aditivos.
- Selección estricta `linux-amd64` / `windows-amd64`.
- Adapter MinIO real y source fake para tests.
- `same version → noop`.

### Slice 2 — Filesystem transaccional mínimo

- Descarga streaming, size/SHA-256, paths seguros y promotion.
- Lock cross-process.
- `PENDING.next → CURRENT → PENDING` y recovery.
- Idempotencia, partial-stage cleanup y fallos sin mutar `CURRENT`.

### Slice 3 — Paridad Linux

- Manifest publisher aditivo en Symphony.
- Shadow/dry-run y canary antes de reemplazar Bash.
- Units/timer verificados contra hosts reales.

### Slice 4 — Windows filesystem

- VM tests de rename/replace, lock, ACL, restart y paths bajo `%ProgramData%`.
- Publisher genera `windows-amd64` en la misma release.

### Slice 5 — Windows launcher + Symphony integration

- Launcher estable bajo SCM.
- Task Scheduler e instalador idempotente.
- Quiesce/drain completo en el worker, responsabilidad de Symphony.

### Slice 6 — Windows E2E

- Idle upgrade, worker ocupado, crash, retry, rollback manual y reboot.
- Cutover sólo después de evidencia; Linux legacy sigue disponible hasta fase explícita posterior.

## Criterios de aceptación MVP

- `same version → noop` sin escrituras de activación.
- `platform missing → error` explícito.
- Download/hash/size failure deja `CURRENT` intacto.
- Success deja release completa y `CURRENT/PENDING` consistentes.
- Repetir `RunOnce` es idempotente.
- Dos procesos no mutan la instalación simultáneamente.
- Build y tests pasan en Linux y Windows amd64.
- El módulo no importa `github.com/xKoRx/symphony/...`.

## Deliberate non-goals

- API/UI, daemon, base de datos, cola o control plane.
- Fleet management, targets múltiples, groups/scopes, channels o policies.
- Auto-rollback, health orchestration o historial de deployments.
- Self-update, PKI/signatures, OCI, GitHub Releases, Kubernetes o multi-cloud.
- Distributed locks o adapters ficticios para sources sin consumer.

## Riesgos y gates

- Las credenciales versionadas en Symphony deben rotarse antes de cualquier rollout.
- El publisher debe publicar todos los artifacts de las plataformas declaradas y sólo después actualizar el manifest; Symphony usa ambas en su integración inicial.
- El drain correcto del worker Windows es un cambio de Symphony, no de Stager.
- Semántica de replace/lock/ACL Windows requiere evidencia en VM real.
- Un repositorio remoto no se crea hasta decidir visibilidad y ownership en GitHub; el módulo y repo local no dependen de esa decisión.

## Validación externa

La IA validadora evaluó diseño y handoff sin acceso al código. Resultado: aproximadamente 9/10 y aprobación para continuar integración, no producción.

- **Confirmado:** frontera Stager/Symphony limpia, one-shot correcto, recovery antes de MinIO y estado mínimo suficiente.
- **Precisión aplicada:** decir “diseñado para migración aditiva compatible”, no “compatible con Symphony” hoy.
- **Precisión aplicada:** `files[].path` preserva el layout relativo real de Symphony; el scaffold ya lo implementa.
- **Gate abierto:** congelar en Symphony si release completa significa Linux+Windows obligatorios o sólo plataformas declaradas.
- **Límite:** no agregar plataforma, scopes ni nuevos estados antes de demostrar MinIO real, shadow Linux y E2E Windows con MT5 ocupado.

## 📆 Bitácora

- **2026-08-10** — Creado [[Stager - Cross-Platform Deployment Lifecycle]] como iniciativa sucesora tras evidencia productiva de redisparo del bridge en `noop`. El MVP permanece cerrado; el nuevo proyecto amplía el producto con activación durable y runtime adapters sin cambiar la independencia del core.
- **2026-08-09** — Owner acepta y cierra el proyecto tras confirmar que Symphony corre en Windows. Se mantiene la frontera del MVP: Stager descarga/verifica/prepara y expresa `CURRENT`/`PENDING`; el worker y su supervisor gobiernan el lifecycle.
- **2026-08-08** — Proyecto creado desde el template vigente. El nuevo master prompt reemplaza la propuesta de alojar el binario dentro de Symphony por un módulo independiente `github.com/xKoRx/stager`. Se adopta `PENDING.next` como recuperación mínima y Symphony queda como primera integración.
- **2026-08-08** — Core inicial terminado: repo Git local, SDD mínimo, CLI/MinIO, manifest, staging, locks Unix/Windows, replace durable y tests de éxito/fallo/recovery. Test, vet y cross-build PASS. No se modificó Symphony ni se publicó remote.
- **2026-08-08** — Handoff listo: lint de cuatro fuentes canónicas con 0 errores; Graphify reconstruido con 13.821 nodos/13.836 aristas y recupera `Stager` más sus slices. Tarea puente movida de WIP a Review.
- **2026-08-08** — Validación externa (~9/10, sin acceso a código) aceptada. Se corrigió wording de compatibilidad, se dejó política multi-plataforma como gate Symphony y se creó [[stager-app]] como application canónica.
- **2026-08-08** — Documentación de sistema ampliada en [[stager-app]] y repo Stager (`ARCHITECTURE.md`, `MANIFEST.md`). Se creó [[Stager - Symphony Publisher Integration]] como handoff implementable y [[2026-08-08-stager-deployment-system]] como idea futura separada.

## 🧭 Decisiones

- **D1:** repo/módulo `stager`; nombre genérico, corto y alineado con la organización `xKoRx`.
- **D2:** one-shot con scheduling externo; no daemon.
- **D3:** MinIO es el único source del MVP; una interfaz pequeña existe para testear.
- **D4:** manifest actual evoluciona aditivamente con `entrypoint` y `files` verificables.
- **D5:** estado autoritativo mínimo: `CURRENT`, `PENDING`, `PENDING.next` y lock.
- **D6:** launcher Windows separado del Stager y fuera del core inicial.
- **D7:** coexistencia obligatoria; no se borra legacy en este ciclo.

## 🔗 Docs / Links

- [[Echo Forge]]
- [[stager-app]] — application canónica del repo/módulo.
- [[Stager - Symphony Publisher Integration]] — próximo proyecto ejecutable; publisher multi-plataforma y MinIO/shadow.
- [[Stager - Cross-Platform Deployment Lifecycle]] — implementación sucesora de activación durable, runtime Linux/Windows y retiro legacy.
- [[2026-08-08-stager-deployment-system]] — idea futura diferida hasta evidencia multi-target.
- [[Echo Forge - Cross-Platform Stager]] — discovery/diseño precursor, supersedido donde difiere por este proyecto independiente.
- [[Symphony]]

## 💡 Ideas

### Backlog de ideas

- Introducir targets/scopes sólo cuando exista un segundo target real o un agente que administre múltiples configuraciones.

### Motivos / principios

- KISS, YAGNI, fail-safe, idempotencia, portabilidad y composición.

### Memoria pública / interna

- **Memoria pública:** esta nota y la documentación versionada del repositorio.
- **Memoria interna:** ninguna específica por ahora.
- **Motivo:** el contrato debe poder retomarse sin depender de contexto conversacional.
