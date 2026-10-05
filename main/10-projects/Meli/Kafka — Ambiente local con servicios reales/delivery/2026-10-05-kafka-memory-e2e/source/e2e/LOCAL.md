# Kafka CP local E2E with instance memory

Owner decision2026-10-05 supersedes Fury Sandbox for this local family. Production storage is unchanged. This candidate extends the existing CP Gradle sourceSet and fixtures to avoid duplicating business logic. The dedicated profile/task keeps its backend and evidence separate from remote KVS and ecosystem suites.

Requirements: Java25, Gradle9.3.1 wrapper, Docker Compose runtime with >=5GiB, internal Maven dependencies available (network or cache), free loopback ports39092–39096. ARM brokers use `-XX:UseSVE=0`. Five pinned Kafka brokers cover AWS RF1–5 and GCP RF1–3/default2.

```sh
DOCKER_CONTEXT=<owned-context> JAVA_HOME=<jdk25> ./e2e/local.sh
# Optional cached build:
DOCKER_CONTEXT=<owned-context> JAVA_HOME=<jdk25> ./e2e/local.sh --offline
# A focused diagnostic run has partial coverage:
DOCKER_CONTEXT=<owned-context> JAVA_HOME=<jdk25> ./e2e/local.sh --tests '*RealKafkaTriggerBridgeIntegrationTest'
```

The launcher creates a unique Compose project/run, real trigger/result topics, loopback routing and private report directories. It runs `localKafkaE2eTest`, then stops/removes only that project's containers, volumes and network when reconciliation confirms that no work remains. Missing or unknown reconciliation and retained work leave the owned resources intact and return failure. Startup, tests and teardown are one command. Missing dependencies, empty selection, test failures, skips, worker-exit failure or cleanup failure return nonzero. Reports are in `build/local-e2e/<run>/`: sanitized JUnit, source hashes, Kafka readiness, result.json and native worker completion. Raw Gradle/broker logs remain private. A filtered invocation proves only its selected scenarios. Corporate CI uses `.github/workflows/local-kafka-e2e.yml`; a workflow definition is not an executed job.

`local,real-e2e,memory-e2e` selects the native `LocalInMemoryKvsClient`, real Kafka connection/result adapters and the existing CP controllers, validators, processors, provisioners and IdempotencyGuard. Maps belong to one application context. Exclusive create assigns1; update checks CAS then increments; expiry removes stale entries, and reads copy bytes. TTL/counters are local adapter behavior. Restart clears the map; separate JVMs do not share claims. No productive Toolkit, durable recovery, cross-JVM exclusivity, KVS network outage or exactly-once guarantee is certified.

Selection: RealControlplaneIntegrationTest, RealBoundaryVariantsIntegrationTest (excluding its three child routing/config tests), PhysicalProvisioningFailuresTest, RealFixtureCleanupIntegrationTest, RealInterruptedProvisionerIntegrationTest, RealKafkaClusterFaultIntegrationTest, RealPublicationFailureIntegrationTest, RealReplicationDeadlineIntegrationTest, RealKvsIntegrationTest and RealKafkaTriggerBridgeIntegrationTest. Their existing assertions observe HTTP, actual Kafka topics/partitions/config/RF/messages/consumer offsets, correlated real results and the injected map's guard state. The Kvs test class exercises memory semantics in this task; its legacy remote method names do not mean a server was tested. Supporting direct-provisioner/interruption tests keep their existing narrower layer.

Excluded remote families keep their own explicit tasks: realIntegrationTest requires the original remote prerequisites; e2eTest/managedIntegrationTest and completeE2e are ecosystem/provider scope. GCP business on plaintext local Kafka does not verify GCP OAuth; Kafka result delivery does not verify BigQueue. Excluded child routing/authorization/protocol and durable-recovery contracts remain separately visible in the matrix. No disabled test or green infrastructure skip substitutes for them.

Status: implementation/runtime evidence is tracked in `meli/features/20261001-real-e2e/evidence/local-memory-2026-10-05.md` and the local coverage matrix. Do not infer PASS from code preparation or broker readiness alone.
