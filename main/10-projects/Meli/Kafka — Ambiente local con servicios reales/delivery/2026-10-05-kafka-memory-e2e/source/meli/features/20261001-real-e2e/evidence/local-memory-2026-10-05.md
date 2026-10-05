# Local memory CP candidate — 2026-10-05

Owner explicitly replaced Fury Sandbox with a simple map for CP local E2E. Ecosystem is later. Base7f1720d950446638ff9b15a0e4e167f3e8e26e43, branchfeature/kafka-e2e-memory. Canonical master snapshot remainsf74e856ef3de881e2d504c6cb1ced573681c1058 (2026-10-01 audit); this is pending work, not production. Original worktrees preserved. No new dependencies, releases or deployed services.

## Implemented

Native per-instance LocalInMemoryKvsClient through memory-e2e+real-e2e+local, exclusive create/CAS/assigned local versions/TTL/defensivebytes/close. Production builder unchanged. Reuse existing sourceSet/fixtures and domain code. Default e2e/run.sh and explicit e2e/local.sh select CP local without Fury. Separate exact selection/exclusions in LOCAL.md and local-coverage-matrix.tsv; no disabled scenarios or mocks replacing Kafka/results.

## Evidence and actual limits

- PASS59 adapter/config/guard focused tests:17+14+28, zero failures/errors/skips; compileRealIntegrationTestJava PASS. Author log SHAe769a45f9dbabe7e660a9af54c49035714a6596e9001e0c39b17237a39231ce3.
- PASS845 full CP unit tests, zero failures/errors/skips; Java25/Gradle9.3.1. A different agent reproduced `test compileRealIntegrationTestJava` offline from a fresh detached clone of implementation commit7615b210e5b70667912b956c2f27cc0d1ebc80eb:65 classes/845 tests,0 failures/errors/skips,33 candidate paths without hash drift. Receipt SHA2c66dc4ea7a8cdc7040434ff6a4aa8d469681dc7b4a0f333b313c3671c11f033, log SHA11b5532664724e9202d30c138537c2d833b34e357743fd5caf275f9d3fa5c9f5. GenerateDocTest changed only its generated Swagger file in that own clone; the diff is preserved. Unit tests and compilation do not certify Kafka business effects.
- Real full attempt run48711a6c7ffa43dc88c44b2d4b1db4b1:343 invocations,309 failed,34 passed,0 skipped. Five Docker brokers healthy and internal metadata showed5 IDs. Host Kafka refused127.0.0.1:39092; first fixture describeCluster timed out, then its retained FAILED journal correctly blocked further fixtures. No completed business family. V1 launcher removed its own Docker resources after failure; UNKNOWN retention and native-result verification were subsequently strengthened, and that original result is not rewritten.
- Three KVS assertions failed because a test compared ErrorCode.CONFLICT(enum) with the SDK string conflict. Fixed to ErrorCode.CONFLICT.getCode(); operations/CAS oracles unchanged. Focused physical replay remains pending; the adapter unit layer is green.
- Own Colima0.8.1/Lima1.0.5 restart and foreground/gRPC-start attempts failed readiness after603s. Native SSH shell succeeds; SSH forwarding child41272 exited-9 at2026-10-05T18:52:39.412315Z, no stderr. Exact-window kernel reads did not establish a cause. Do not infer VPN/auth/permissions/AMFI. Own VM stopped after failure; no run containers remain. Shared colima runtime has2GiB and was not modified; default Docker is unavailable.
- Independent launcher review preserved false-accept REDs for missing/foreign native proof and UNKNOWN deletion. Corrected exact tuple/types/Instant/private receipt checks and no-down on retained work. Review receipts retain earlier versions; V5 independent peer PASS49 source/metadata/process controls with0 findings; review SHAe49f6388422a46a3a2a664188f2c9a6ef4a6552bfbc9ea80d0653983e8c5f397. This certifies only those controls, not a Kafka business run.

## Reproduction and external gates

`DOCKER_CONTEXT=<working-owned-context> JAVA_HOME=<jdk25> ./e2e/local.sh --offline` starts five brokers, runs all selected tests and cleans owned resources. Without offline, internal Maven access/cache is required. Local startup now explicitly checks all five host TCP listeners with a30s deadline. Reports contain source hashes, sanitized JUnit, native worker completion and result.json. Missing startup/test/nativeproof/cleanup requirements fail clearly.

BLOCKED local physical gate: restore a Docker runtime with >=5GiB and working host loopback ports39092–39096; rerun full local suite and independent clean replay, including expected Kafka/publication/process failures. No Fury login, KVS alias or Sandbox provisioning is needed. This packet records the SIGKILL symptom, not an established mechanism or unverified fix. Corporate workflow local-kafka-e2e.yml is implemented but NOT_EXECUTED; an owner-selected runner with Docker/JDK25/internal Maven access must execute the published candidate. Managed OAuth/BigQueue, Playmaker and durable/shared KVS remain outside this local family and unexecuted.

MeliSecurity tools are unavailable in this session. No MeliSecurity approval is claimed. Token usage/cost are unknown. AGENTS OS remains active/partial while physical and independent gates remain open.

Local matrix356:5 PASS at named adapter/config unit layer,226 local capacities BLOCKED by host Kafka and125 NOT_EXECUTED outside the local selection. Original351 matrix and its remote physical contract remain intact. No full local family PASS is declared.
