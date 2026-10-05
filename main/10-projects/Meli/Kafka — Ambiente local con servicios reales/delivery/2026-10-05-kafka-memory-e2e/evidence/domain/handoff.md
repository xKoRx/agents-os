# CP local memory adapter handoff

Four owned Java paths are frozen in freeze.json and frozen-source/. Targeted tests passed: 59 tests, 0 failures/errors/skips (adapter 17, config 14, existing guard 28). compileRealIntegrationTestJava passed. The log and JUnit XML are preserved; no E2E Kafka run is claimed. Gradle slot released. No commit created.

The explicit profile conjunction memory-e2e & real-e2e & local selects the named idempotencyKvsClient. Productive builder code remains unchanged and is excluded only by memory-e2e; the existing NoOp is also excluded in that profile. Incomplete memory profile combinations have no backend. This does not replace remote real-e2e.

LocalInMemoryKvsClient owns ConcurrentHashMap state, Clock, runId, UUID instanceId and native ownerPid. It supports raw byte CRUD with exclusive create v1, CAS +1, expiry and defensive snapshots. TTL -1 never expires, 0 expires immediately, positive seconds are refreshed by a successful write. Reads expose configured TTL, not server remaining TTL. Conflict=conflict; malformed input/unsupported=bad_request; closed=service_error. Typed/batch/bulk APIs explicitly fail. No Mockito backend and no shared/static map.

Root owns observer/preflight/profile/launcher/fixture orchestration. Different processes or contexts have different stores; restart loses state. Existing remote-backend/crash/shared-worker tests require explicit scope handling and must not be promoted by these unit results. Fault is the independent peer. No SDK identity spoofing or memory-as-Fury certification.
