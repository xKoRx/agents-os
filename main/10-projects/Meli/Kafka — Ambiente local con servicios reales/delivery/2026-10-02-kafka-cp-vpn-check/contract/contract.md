# Own CP KVS inventory contract

The installed read-only inventory is `GET application/rio-controlplane-kafka/kvs`, implemented by `cli_services.services_commands.services.kvs_service.list_KVS` at lines 19–22. Its CLI table uses only `name`, `status`, `metadata.container_type` and `metadata.test_container` (commands logic lines 22–30).

Root can call that route once through the existing stored-auth guard, with GET and retries disabled. Keep only HTTP status, list shape, exact requested alias match count and that matching entry's three metadata fields. Omit all other aliases, raw responses, configurations and KMS fields.

A visible alias rules out absence in this caller-visible inventory. Its test-container flag does not certify Sandbox eligibility or clone permissions. Absence means not visible here; the installed CLI does not establish whether the API filters unauthorized aliases. A 403 from the clone cannot distinguish non-sandboxable from permission denial by itself.

`cli_sandbox` does not expose a list of eligible aliases or a typed 403 cause taxonomy. Its BC-template GET is not source-declared as such a list, and the CLI template command writes YAML. Do not invent a new listing route or use template generation for this read. SandboxApi preserves status and extracts message/error, with no machine-code mapping for these causes.

This lookup read installed source only: no network, auth values, SDK execution or external mutation. Detailed source pins and safe projection: [contract.json](contract.json).
