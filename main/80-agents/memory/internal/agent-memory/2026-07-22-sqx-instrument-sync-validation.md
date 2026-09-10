---
type: agent_memory
scope: project
created: 2026-07-22
updated: 2026-09-09
memory_state: archived
project: "[[Symphony]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - agent/internal
  - kind/agentmemory
  - project/symphony
  - tech/sqx
---
# SQX instrument sync validation

- Canonical operational tool on Zeus: `/home/kor/sync_user_data_zeus.sh`; SHA-256 validated on 2026-07-22 as `c4a98fdee545483b5a4e88b3d771402156529970bcc66fb54774bd06a22b73e8`.
- It mirrors `~/sqx/user/data/` from Zeus to Hera and Kronos using keyless SSH and `rsync --delete-after`. It intentionally excludes live H2 databases, version files, locks, and temporary files; never copy those live DBs merely to force equality.
- The script uses rsync's normal size/mtime comparison, not `--checksum`. Before and after consequential runs, verify with a checksum dry-run; for instruments, compare `~/sqx/user/data/History/` with `rsync -a --dry-run --checksum --delete --omit-dir-times`.
- Verified instrument set: `DEUIDXEUR`, `EURUSD`, `GBPCAD`, `GBPJPY`, `GBRIDXGBP`, `JPNIDXJPY`, `USATECHIDXUSD`, `USATECHIDXUSD_darwinex`, `USDCAD`, `USDJPY`, `XAUUSD`, `XAUUSD_darwinex`; auxiliary directories: `sq_equity`, `sq_futures`.
- 2026-07-22 result: Zeus, Hera, and Kronos had identical per-instrument SHA-256 manifests, file counts, and byte counts. `History/` contained 59 entries (18 regular files) totaling 935,630,054 bytes. The script ran idempotently and transferred no regular files; post-run checksum dry-runs reported zero creates, deletes, or transfers.
- Worker health at validation: all three hosts reported `CURRENT=0.1.130` and no `PENDING` marker.
