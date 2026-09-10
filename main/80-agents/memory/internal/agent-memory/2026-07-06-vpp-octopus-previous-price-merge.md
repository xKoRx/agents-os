---
type: agent_memory
scope: agent
created: 2026-07-06
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - agent/internal
  - area/meli
  - app/vpp-backend
  - app/vis-octopus-lib
---

# VPP + Octopus previous price merge

When cleaning `feature/bajo-de-precio-motors`, the bad commits requested by Rodrigo were removed from the remote with `SKIP_VPP_REVIEW=1 git push --force-with-lease`. After merging `origin/develop` locally, resolving `build.gradle` to plain `visLibVersion = '3.3.0'` broke previous-price motors classes. Trying `3.3.0-previous-price-motors` restored `PriceDropMotorsModel` and `VisPriceDropMotorsTask`, but missed develop-side seller motors classes: `SellerGoodAttentionDomainModel` and `SellerReputationMotorsTask`.

For this branch, `0.0.21-previous-price-motors` contained both class sets and `./gradlew compileJava compileTestJava` plus `./gradlew test` passed after the merge. Future agents should validate the full consumer compile before pushing a VPP Octopus bump, especially after merging develop.
