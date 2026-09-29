---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Estandarización de Scopes RIO]]"
  - "[[ads-signals-frontend]]"
aliases:
  - "PR adminfrontend-rules alpha-nonprod"
tags:
  - kind/doc
  - project/scopes-rio
created: "2026-09-28"
updated: "2026-09-28"
---

# Descripción PR — adminfrontend-rules

PR: [#11182](https://github.com/melisource/adminfrontend-rules/pull/11182) · Estado: draft · Repositorio: `melisource/adminfrontend-rules` · Rama `feature/signals-alpha-nonprod-ingress` @ `ae67565a1aefe76f72fb0217af1cb8ba0c493cae` · Base `master` @ `2e8855466cdc8a30c46962919e9160db634108f1` · 1 commit · 2 archivos, 5 inserciones · Requisito relacionado: SIG-599 · Dependencia: scope Fury existente `ads-signals-frontend/alpha-nonprod` · Suite local: no ejecutada el 2026-09-28 · CI: `continuous-integration` PASS, `workflow` PASS, `Nginx Rule Check` PASS; `Edge Authentication Workflow` FAIL (`NOT_READY`).

> [!warning] Gate de merge
> El workflow de Edge Authentication clasifica la URL nueva como pública y devuelve `NOT_READY` para `alpha-nonprod.ads-signals-frontend`: `Pool has Deny by Default schema - rejects public traffic`. La acción bloquea el merge. El guard `X-Public` existe en `server`, fuera del `location` que inspecciona el clasificador; aún no se confirma si corresponde configurar un esquema AuthN de tráfico público. El ticket Shield 4357 sólo aplica si se decide habilitar ese acceso.

## Propósito

- Dejar una descripción revisable del PR con el template oficial y los gates observados.

## Contenido

- Mapeo exacto de `meliLab=alpha-nonprod` al pool frontend de ese scope y su caso de regresión en GET/POST.

---

# Pull request template

## Rules for internal admins using \*.adminml.com

**Title:** Route alpha-nonprod through signals.adminml.com

## Description

Route the exact `meliLab=alpha-nonprod` cookie value to `alpha-nonprod.ads-signals-frontend.melifrontends.com` from `signals.adminml.com`. Add a matching `all_fe` routing case for GET and POST. Branch: `feature/signals-alpha-nonprod-ingress`; base: `master`. The existing server-level `X-Public` 403 guard remains unchanged.

**Current merge gate:** Edge Authentication classifies the new upstream as public and its pool validation responds `NOT_READY`: `Pool has Deny by Default schema - rejects public traffic`. The scope exists and is active in Fury. The route's server-level `X-Public` guard is outside the location block inspected by the classifier. The appropriate configuration or workflow resolution is under investigation; no Shield ticket has been filed.

---

## Checklist

### 1. Type of Changes

Select the type of changes you are implementing:

- [ ] **New domain route**: You're adding a completely new domain.
- [x] **New route to existing domain**: You're adding a new path to an already defined domain.
- [ ] **Clean-up**: You're deleting an old rule or route that is no longer needed.

### 2. Environments Affected

Indicate which environments your changes will affect:

- [x] **Production**: Changes affect the live environment.
- [ ] **Test changes**: Changes affect the testing environment only.
- [ ] **Production and test changes**: Changes will affect both environments (not recommended)

### 3. Testing Coverage

Please confirm the following regarding testing:

- [x] **Adequate test cases**: This change is covered by test cases for all HTTP methods (GET, POST, etc.) related to the changed rule.
- [x] **Rollback strategy**: I have prepared a rollback strategy in case these changes negatively impact production.
- [x] **Rollback documentation**: The rollback strategy for this rule change has been documented.

### 4. Security Compliance

Ensure your changes adhere to security best practices:

- [ ] **Web security compliance**: The exposed domains/routes follow web security guidelines (e.g., role-based access control, rate limiting, vulnerability management).
- [x] **Preflight requests**: I am not modifying or decorating cross-origin preflight OPTIONS requests, nor am I using unsafe wildcards.
- [x] **Evaluation of other rules**: I am not interfering with rules outside of my team’s scope without explicit approval.

### 5. External Access Control

How will users access to this domain & rule?

- [ ] **VPN**: Users that will access this domain already have access to that domain through VPN

- [ ] **Zero Trust**: I already authorized & exposed the domain via zero trust following the producedure in this [guide](https://docs.google.com/document/d/1jUFKoKLPh8nh0okmRHMyVwpbYgJ4qomtHZOsg78oZEk/edit?tab=t.0#heading=h.n1933g7ku4e2) and validated consumers users can access this domain.

---
# Public Traffic & Edge Authentication (Critical) :rotating_light:

**IMPORTANT:** Given the EDGE initiative that prioritizes **Deny by Default** for all public traffic, all new Fury scopes will automatically **BLOCK 100%** of public traffic. This means any new scope without an applied authentication configuration model will return a **404 Error**.

Please mark the relevant option below and complete the necessary steps:
- [ ] **No Authentication Model Impact:** This PR does NOT introduce a new Fury scope and does NOT modify any existing authentication configuration model. *(No further action needed)*
- [ ] **Authentication Configuration Model Required:** This PR introduces a new Fury scope OR modifies an existing authentication configuration model.
    - [ ] I have read the [Edge Authentication documentation](https://furydocs.io/edge-authentication-docs/latest/guide/#/).
    - [ ] I have created a **[Shield Ticket](https://shield.adminml.com/requests/create?c=4357)** to enable/update the desired authentication model and confirmed its effectiveness.
    - [ ] I understand that failure to configure authentication model will result in a 404 Error (with a payload containing `code: not_found`  and `message: internal server error`) for affected scopes.
    - [ ] I have read the [Authorization Policies documentation](https://furydocs.io/authorization-policies-docs/latest/guide/#/).
    - [ ] I have created authorization policies defining clear rules (Policies) that determine what operations users can perform based on their permissions.
    - [ ] I understand that failing to configure the authorization policies will result in a 403 error for the affected scopes.

---

## Additional Notes

- `fury --application ads-signals-frontend list-infra` confirms `alpha-nonprod` is an active test scope. This PR does not change its Edge Authorization settings.
- Local suite status: not run. The initial `continuous-integration`, `workflow`, and `check-nginx-rules` checks passed; `edge-authentication-workflow` failed as described above.
- Rollback: revert this PR to remove the route and its test case. Production rules deploy Tuesday to Friday, 03:00–06:00 GMT-3.
Only leaders & upper managers can upload a [ticket in Shield](https://shield.adminml.com/requests/create?c=4874) to receive temporary permissions to merge this pull request. See [docs](https://furydocs.io/scm-platform/latest/guide/#/lang-en/user-access/how-to-guides/traffic-rules-access).
---

## Notas internas — NO van al PR

- El proyecto registró `test3` como entrada de la POC del 2026-09-25; este cambio agrega una selección adicional para `alpha-nonprod` y conserva intacta la ruta `test3`.
- La SPEC técnica vigente se centra en el routing del backend desde `ads-signals-frontend`; el detalle del ingreso Nginx queda soportado por esta solicitud, el bloque existente y el caso de routing.
- La suite local no se ejecutó. El `.drone.yml` apunta al runner bash antiguo; `make test` usa el runner asíncrono. `Nginx Rule Check` pasó y `Edge Authentication Workflow` bloquea el merge tras clasificar el nuevo upstream como público.
- El scope ya existe y la PR no cambia su authentication model. `fury --application ads-signals-frontend list-infra` muestra `alpha-nonprod` activo; `fury platsec public-authn get` devuelve 404 para `alpha-nonprod`, `test`, `test3` y `production`, por lo que esa lectura no distingue el scope alpha de los existentes. La clasificación pública proviene del workflow, que busca `http_x_public` sólo dentro de `location`; Signals lo define en `server`.
- El ticket de configuración Edge AuthN es Shield 4357 si se requiere aceptar tráfico público; Shield 4874 es para permisos de merge. No se abrió ningún ticket ni se cambió la configuración Fury.
- PR publicado desde el fork privado `rjara_meli/adminfrontend-rules` hacia `melisource/adminfrontend-rules:master`; el PR se mantiene en draft hasta resolver el gate.
