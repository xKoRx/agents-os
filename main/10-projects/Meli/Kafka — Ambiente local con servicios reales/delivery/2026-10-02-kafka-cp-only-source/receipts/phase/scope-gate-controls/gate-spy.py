#!/usr/bin/env python3
# Scope forwarding control only. No SDK, backend, Kafka, HTTP or business invocation.
import json,os,sys
from pathlib import Path
Path(os.environ["CP_SCOPE_CAPTURE"]).write_text(json.dumps({"args":sys.argv[1:],"scope":"NEUTRAL_FORWARDING_ONLY"}))
print("SANDBOX_GATE_FAILED:SCOPE_CAPTURE_EXPECTED",file=sys.stderr)
raise SystemExit(43)
