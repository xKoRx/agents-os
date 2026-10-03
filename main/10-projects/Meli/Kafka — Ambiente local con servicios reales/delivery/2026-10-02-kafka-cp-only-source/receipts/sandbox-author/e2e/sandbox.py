#!/usr/bin/env python3
"""Own Fury Sandbox lifecycle using installed CLI API routes, never KMS configuration.

Help/syntax checks are preparation only. Server schema, permissions and generated
Toolkit configuration must pass against the real service before certification.
"""
import argparse
import contextlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
import uuid

APPS = ("rio-controlplane-kafka", "rio-playmaker")
SCOPES = ("cp", "ecosystem")
MAPPING_EXPORTS = ("E2E_KVS_SEGMENT_ID", "E2E_PLAYMAKER_KVS_SEGMENT_ID",
                   "E2E_PLAYMAKER_ACTION_RESULTS_CONTAINER", "E2E_PLAYMAKER_ACTION_LOCKS_CONTAINER",
                   "E2E_PLAYMAKER_SANDBOX_BC", "E2E_PLAYMAKER_SANDBOX_INSTANCE")


def receipt_scope(state, expected=None):
    # A missing field is the existing ecosystem receipt contract, never CP-only.
    scope = state.get("scope", "ecosystem")
    if not isinstance(scope, str) or scope not in SCOPES:
        raise RuntimeError("SANDBOX_PROVENANCE_SCOPE_INVALID")
    if expected is not None and expected != scope:
        raise RuntimeError("SANDBOX_PROVENANCE_SCOPE_MISMATCH")
    return scope


def applications_for_scope(scope):
    return APPS[:1] if scope == "cp" else APPS


def valid_aliases(app, aliases):
    count = 1 if app == APPS[0] else 2
    return (isinstance(aliases, list) and len(aliases) == count
            and all(isinstance(alias, str) and re.fullmatch(r"[a-zA-Z0-9_.-]{1,100}", alias)
                    for alias in aliases) and len(set(aliases)) == count)


def write_private(path, value):
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as output:
            output.write(value)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


class Lifecycle:
    def __init__(self, directory, state):
        self.directory, self.state = directory, state
        from cli_sandbox.rest.sandboxsapi import SandboxApi
        self.api = SandboxApi()
        self.stored_auth_headers()

    def stored_auth_headers(self):
        # Read-only preflight; never call AuthenticationHelper.get_token/login/renew.
        from furycli.core.helpers import credentials
        snapshot = credentials.get_credentials()
        token = credentials.get(credentials.TIGER_TOKEN_KEY, snapshot)
        if not isinstance(token, str) or not token or credentials.tiger_token_expired(snapshot):
            raise RuntimeError("SANDBOX_FURY_LOGIN_REQUIRED")
        zero_trust = credentials.get(credentials.ZT_TOKEN_KEY, snapshot)
        if zero_trust:
            try:
                expiry = int(credentials._decode_jwt_payload(zero_trust)["exp"])
            except (KeyError, ValueError, TypeError, IndexError):
                raise RuntimeError("SANDBOX_ZERO_TRUST_LOGIN_REQUIRED") from None
            # CommunicationApi reads ZT again; require enough margin to avoid its expiry deletion.
            if expiry <= time.time() + 500:
                raise RuntimeError("SANDBOX_ZERO_TRUST_LOGIN_REQUIRED")
        return {"X-Tiger-Token": "Bearer " + token}

    def validate_scope(self, expected=None, complete=False):
        scope = receipt_scope(self.state, expected)
        applications = applications_for_scope(scope)
        resources = self.state.get("resources")
        if not isinstance(resources, list) or any(not isinstance(item, dict) for item in resources):
            raise RuntimeError("SANDBOX_PROVENANCE_RESOURCE_NOT_OWNED")
        apps = [item.get("app") for item in resources]
        if any(app not in applications for app in apps) or len(set(apps)) != len(apps) or any(
                item.get("bc") != "e2e-" + self.state["run_id"] for item in resources):
            raise RuntimeError("SANDBOX_PROVENANCE_RESOURCE_NOT_OWNED")
        if any(not valid_aliases(item["app"], item.get("logical_services")) for item in resources):
            raise RuntimeError("SANDBOX_PROVENANCE_LOGICAL_MAPPING_INVALID")
        if complete and set(apps) != set(applications):
            code = "CP_APPLICATION" if scope == "cp" else "BOTH_APPLICATIONS"
            raise RuntimeError("SANDBOX_PROVENANCE_REQUIRES_" + code)
        segments = self.state.get("segments", {})
        allowed_segments = {"E2E_KVS_SEGMENT_ID"}
        if scope == "ecosystem":
            allowed_segments.add("E2E_PLAYMAKER_KVS_SEGMENT_ID")
        if not isinstance(segments, dict) or set(segments) - allowed_segments or any(
                not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", value)
                for value in segments.values()):
            raise RuntimeError("SANDBOX_PROVENANCE_SEGMENTS_OUTSIDE_SCOPE")
        mutations = self.state.get("mutations", [])
        if not isinstance(mutations, list) or any(not isinstance(item, dict)
                or item.get("app") not in applications for item in mutations):
            raise RuntimeError("SANDBOX_PROVENANCE_MUTATION_OUTSIDE_SCOPE")
        return scope

    def save(self):
        write_private(self.directory / "state.json", json.dumps(self.state, indent=2) + "\n")

    def call(self, app, suffix, method="GET", body=None, allowed=(200,)):
        if app not in applications_for_scope(receipt_scope(self.state)):
            raise RuntimeError("SANDBOX_APPLICATION_NOT_OWNED")
        kwargs = {"timeout": 20, "retry": False, "authenticate": False, "headers": self.stored_auth_headers()}
        if body is not None:
            kwargs["data"] = json.dumps(body)
        operation = None
        if method != "GET":
            operation = {"app": app, "suffix": suffix, "method": method, "outcome": "UNKNOWN"}
            self.state.setdefault("mutations", []).append(operation)
            self.save()
        try:
            payload, status = self.api.make_api_call(f"application/{app}/{suffix}", method=method, **kwargs)
        except Exception as failure:
            # Never publish API exception strings, which may include configuration or auth data.
            code = getattr(failure, "status_code", None)
            self.state["last_api_error"] = {"app": app, "suffix": suffix, "method": method,
                                            "http": str(code) if code is not None else None,
                                            "error_type": type(failure).__name__}
            if operation is not None and str(code).isdecimal():
                operation["outcome"] = "HTTP_" + str(code)
            self.save()
            if str(code).isdecimal() and int(code) in allowed:
                return None, int(code)
            raise RuntimeError("SANDBOX_API_FAILED:" + type(failure).__name__) from None
        if operation is not None:
            operation["outcome"] = "HTTP_" + str(status)
            self.save()
        if status not in allowed:
            raise RuntimeError("SANDBOX_UNEXPECTED_HTTP_STATUS:" + str(status))
        return payload, status

    def require_owned(self, resource):
        payload, status = self.call(resource["app"], "bc/" + resource["bc"], allowed=(200, 404))
        if status == 404:
            return None
        if payload.get("name") != resource["bc"] or payload.get("description") != self.state["marker"]:
            raise RuntimeError("SANDBOX_OWNERSHIP_VERIFICATION_FAILED")
        if not resource.get("creation_observed"):
            resource["creation_observed"] = True
            self.save()
        return payload

    def base_exports(self):
        self.validate_scope()
        exports = {"E2E_RUN_ID": self.state["run_id"], "E2E_KVS_EXCLUSIVE_RUN_ID": self.state["run_id"],
                   "E2E_KVS_SANDBOX_PROVENANCE": str(self.directory / "state.json")}
        exports.update(self.state.get("segments", {}))
        return exports

    def add_configuration(self, exports, resource, configs):
        entries = configs.get("configurations")
        if not isinstance(entries, list):
            raise RuntimeError("SANDBOX_KVS_EXPORT_SCHEMA_UNVERIFIED")
        by_alias = {entry.get("original_service_name"): entry for entry in entries}
        aliases = resource["logical_services"]
        if len(by_alias) != len(entries) or set(by_alias) != set(aliases):
            raise RuntimeError("SANDBOX_PROVENANCE_LOGICAL_MAPPING_CHANGED")
        physical = []
        for alias in aliases:
            entry = by_alias[alias]
            configuration = entry.get("configuration", {})
            if entry.get("msg_error") or not configuration or any(
                    not re.fullmatch(r"KEY_VALUE_STORE_[A-Z0-9_]+", key) for key in configuration):
                raise RuntimeError("SANDBOX_KVS_EXPORT_SCHEMA_UNVERIFIED")
            containers = [str(value) for key, value in configuration.items() if key.endswith("_CONTAINER_NAME")]
            if not containers or any(not re.fullmatch(r"sbox[a-zA-Z0-9_-]+", value) for value in containers):
                raise RuntimeError("SANDBOX_GENERATED_PHYSICAL_CONTAINER_REQUIRED")
            physical.extend(containers)
            for key, value in configuration.items():
                value = str(value)
                if any(ord(character) < 32 for character in value) or (key in exports and exports[key] != value):
                    raise RuntimeError("SANDBOX_EXPORT_COLLISION_OR_CONTROL_CHAR")
                exports[key] = value
        prefix = "E2E_SANDBOX" if resource["app"] == APPS[0] else "E2E_PLAYMAKER_SANDBOX"
        exports[prefix + "_BC"], exports[prefix + "_INSTANCE"] = resource["bc"], resource["instance"]
        if resource["app"] == APPS[0]:
            exports["E2E_KVS_CONTAINER_NAME"] = aliases[0]
        else:
            exports["E2E_PLAYMAKER_ACTION_RESULTS_CONTAINER"] = aliases[0]
            exports["E2E_PLAYMAKER_ACTION_LOCKS_CONTAINER"] = aliases[1]
        return physical

    def up(self, services):
        applications = applications_for_scope(self.validate_scope())
        if not isinstance(services, list) or len(services) != len(applications) or any(
                not valid_aliases(app, aliases) for app, aliases in zip(applications, services)):
            raise RuntimeError("SANDBOX_PROVENANCE_LOGICAL_MAPPING_INVALID")
        exports = self.base_exports()
        for app, aliases in zip(applications, services):
            resource = {"app": app, "bc": "e2e-" + self.state["run_id"], "create_intent": False, "create_outcome": "NOT_SENT", "logical_services": aliases}
            inventory, _ = self.call(app, "bc")
            if not isinstance(inventory, list) or any(item.get("name") == resource["bc"] for item in inventory):
                raise RuntimeError("SANDBOX_RUN_NAMESPACE_ALREADY_EXISTS_OR_SCHEMA_INVALID")
            self.state["resources"].append(resource)
            resource["create_intent"] = True
            resource["create_outcome"] = "UNKNOWN"
            self.save()  # Preserve unknown-outcome creation for verified cleanup.
            self.call(app, "bc", "POST", {"name": resource["bc"], "description": self.state["marker"]}, (200, 201))
            resource["create_outcome"] = "CONFIRMED"
            self.save()
            if self.require_owned(resource) is None:
                raise RuntimeError("SANDBOX_CREATION_NOT_OBSERVED")
            for alias in aliases:
                self.call(app, f"bc/{resource['bc']}/services", "POST", {"name": alias}, (200, 201))
            started, _ = self.call(app, f"bc/{resource['bc']}/start", "PUT", allowed=(200, 201, 202))
            instance = str(started.get("response", ""))
            if not instance.isdecimal():
                raise RuntimeError("SANDBOX_START_SCHEMA_UNVERIFIED")
            resource["instance"] = instance
            self.save()
            deadline = time.monotonic() + 180
            configs = None
            while time.monotonic() < deadline:
                response, _ = self.call(app, f"bc/{resource['bc']}/instances/{instance}/configurations")
                candidates = response.get("configurations", [])
                by_alias = {entry.get("original_service_name"): entry for entry in candidates}
                if all(alias in by_alias and not by_alias[alias].get("msg_error") for alias in aliases):
                    configs = by_alias
                    break
                time.sleep(2)
            if configs is None:
                raise RuntimeError("SANDBOX_GENERATED_CONFIG_TIMEOUT")
            resource["physical_containers"] = self.add_configuration(exports, resource, {"configurations": list(configs.values())})
            resource["ownership_verified"] = True
            self.save()
        self.state["status"] = "OWNED_CONFIG_GENERATED_NOT_KVS_CERTIFIED"
        self.save()
        write_private(self.directory / "sandbox.env", "\n".join(f"{key}={value}" for key, value in sorted(exports.items())) + "\n")

    def verify(self, expected_scope=None):
        self.validate_scope(expected_scope, complete=True)
        if self.state.get("status") != "OWNED_CONFIG_GENERATED_NOT_KVS_CERTIFIED":
            raise RuntimeError("SANDBOX_PROVENANCE_INCOMPLETE")
        exports = self.base_exports()
        for resource in self.state["resources"]:
            expected_alias_count = 1 if resource["app"] == APPS[0] else 2
            if len(resource.get("logical_services", [])) != expected_alias_count:
                raise RuntimeError("SANDBOX_PROVENANCE_LOGICAL_MAPPING_INVALID")
            if not resource.get("ownership_verified") or self.require_owned(resource) is None:
                raise RuntimeError("SANDBOX_PROVENANCE_NO_LONGER_OWNED")
            configs, _ = self.call(resource["app"], f"bc/{resource['bc']}/instances/{resource['instance']}/configurations")
            actual = self.add_configuration(exports, resource, configs)
            if sorted(actual) != sorted(resource["physical_containers"]):
                raise RuntimeError("SANDBOX_PROVENANCE_MAPPING_CHANGED")
        consumed = {key: value for key, value in os.environ.items()
                    if key.startswith("KEY_VALUE_STORE_") or key in exports
                    or key in MAPPING_EXPORTS}
        if consumed != exports:
            # Never print the differing keys/values: endpoint/token-safe stable error only.
            raise RuntimeError("SANDBOX_CONSUMED_EXPORTS_DO_NOT_MATCH_OWNED_CONFIG")

    def down(self):
        self.validate_scope()  # Partial own resources are allowed; scope expansion is not.
        errors = []
        for resource in self.state["resources"]:
            try:
                if not resource.get("create_intent"):
                    continue
                if self.require_owned(resource) is None:
                    if not resource.get("creation_observed"):
                        raise RuntimeError("SANDBOX_CREATION_OUTCOME_UNRESOLVED")
                    continue
                listed, _ = self.call(resource["app"], f"bc/{resource['bc']}/instances")
                for instance in listed.get("instances", []):
                    identity = str(instance.get("id", ""))
                    if not identity.isdecimal():
                        raise RuntimeError("SANDBOX_INSTANCE_SCHEMA_UNVERIFIED")
                    self.call(resource["app"], f"bc/{resource['bc']}/instances/{identity}/stop", "PUT", allowed=(200, 202, 409))
                self.call(resource["app"], "bc/" + resource["bc"], "DELETE", allowed=(200, 202, 204, 404))
                deadline = time.monotonic() + 120
                while self.require_owned(resource) is not None:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("SANDBOX_CLEANUP_ABSENCE_TIMEOUT")
                    time.sleep(2)
            except Exception as failure:
                code = str(failure) if isinstance(failure, RuntimeError) and str(failure).startswith("SANDBOX_") else type(failure).__name__
                resource["cleanup_error"] = code
                errors.append(code)
        # BC absence does not resolve a late start/service allocation or another unknown mutation.
        if any(operation.get("outcome") == "UNKNOWN" for operation in self.state.get("mutations", [])):
            errors.append("SANDBOX_MUTATION_OUTCOME_UNRESOLVED")
        self.state["cleanup"] = "FAILED" if errors else "CERTIFIED_API_ABSENCE"
        self.save()
        if errors:
            raise RuntimeError("SANDBOX_CLEANUP_FAILED")
        (self.directory / "sandbox.env").unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("up", "verify", "down"))
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--scope", choices=SCOPES,
                        help="up defaults to ecosystem; verify/down use the receipt unless explicitly constrained")
    parser.add_argument("--cp-service")
    parser.add_argument("--pm-results-service")
    parser.add_argument("--pm-locks-service")
    parser.add_argument("--cp-segment")
    parser.add_argument("--pm-segment")
    args = parser.parse_args()
    directory = args.directory or Path(tempfile.mkdtemp(prefix="rio-owned-sandbox-"))
    directory = directory.resolve()
    if not directory.is_dir() or stat.S_IMODE(directory.stat().st_mode) & 0o077:
        raise RuntimeError("SANDBOX_PRIVATE_DIRECTORY_MODE_0700_REQUIRED")
    if args.command == "up":
        if (directory / "state.json").exists():
            raise RuntimeError("SANDBOX_STATE_EXISTS_USE_VERIFY_OR_DOWN")
        scope = args.scope or "ecosystem"
        if scope == "cp" and any(value is not None for value in
                (args.pm_results_service, args.pm_locks_service, args.pm_segment)):
            raise RuntimeError("SANDBOX_CP_SCOPE_FORBIDS_PLAYMAKER_INPUTS")
        aliases = [args.cp_service] if scope == "cp" else [args.cp_service, args.pm_results_service, args.pm_locks_service]
        if any(alias is None or not re.fullmatch(r"[a-zA-Z0-9_.-]{1,100}", alias) for alias in aliases):
            code = "CP_OWN_KVS_ALIAS" if scope == "cp" else "THREE_OWN_APPLICATION_KVS_ALIASES"
            raise RuntimeError("SANDBOX_" + code + "_REQUIRED")
        if scope == "ecosystem" and aliases[1] == aliases[2]:
            raise RuntimeError("SANDBOX_PLAYMAKER_RESULTS_LOCKS_MUST_BE_DISTINCT")
        run = uuid.uuid4().hex
        segments = {}
        for key, segment in (("E2E_KVS_SEGMENT_ID", args.cp_segment), ("E2E_PLAYMAKER_KVS_SEGMENT_ID", args.pm_segment)):
            if segment is not None:
                if not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", segment):
                    raise RuntimeError("SANDBOX_INVALID_SEGMENT")
                segments[key] = segment
        state = {"schema": 1, "scope": scope, "run_id": run, "marker": "Owned Kafka E2E " + run, "resources": [],
                 "status": "PREPARING", "segments": segments}
    else:
        path = directory / "state.json"
        if stat.S_IMODE(path.stat().st_mode) & 0o077:
            raise RuntimeError("SANDBOX_PRIVATE_STATE_MODE_0600_REQUIRED")
        state = json.loads(path.read_text())
        if state.get("schema") != 1 or not re.fullmatch(r"[a-f0-9]{32}", state.get("run_id", "")):
            raise RuntimeError("SANDBOX_PROVENANCE_SCHEMA_INVALID")
        scope = receipt_scope(state, args.scope)
        if any(item.get("bc") != "e2e-" + state["run_id"] or item.get("app") not in applications_for_scope(scope)
                for item in state["resources"]):
            raise RuntimeError("SANDBOX_PROVENANCE_RESOURCE_NOT_OWNED")
    with (directory / "sdk-private.log").open("a") as private, contextlib.redirect_stdout(private), contextlib.redirect_stderr(private):
        lifecycle = Lifecycle(directory, state)
        if args.command == "up":
            try:
                lifecycle.up([[aliases[0]]] if scope == "cp" else [[aliases[0]], aliases[1:]])
            except Exception:
                lifecycle.down()
                raise
        elif args.command == "verify":
            lifecycle.verify(args.scope)
        else:
            lifecycle.down()
    print("SANDBOX_" + args.command.upper() + "_PASS:" + str(directory))


if __name__ == "__main__":
    os.umask(0o077)
    try:
        main()
    except Exception as failure:
        code = str(failure) if isinstance(failure, RuntimeError) and re.fullmatch(r"SANDBOX_[A-Za-z0-9_:]+", str(failure)) else type(failure).__name__
        print("SANDBOX_GATE_FAILED:" + code, file=sys.stderr)
        sys.exit(1)
