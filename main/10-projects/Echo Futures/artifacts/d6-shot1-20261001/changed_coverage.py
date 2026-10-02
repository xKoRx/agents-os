#!/usr/bin/env python3
"""D6 Shot 1 changed/new-logic coverage (F-MGR-01).

Method (reproducible):
  1. Enumerate Go source files added/modified by the shot:
     git diff <BASE>..HEAD --numstat -- '*.go'  (exclude _test.go)
  2. For each changed file, extract the ADDED line ranges in the NEW file:
     git diff <BASE>..HEAD -U0 -- <file>  (hunks on '+' side)
  3. Collect go coverprofiles from the scoped suites.
  4. A profile block (file:from,to) counts toward changed-logic coverage when
     it INTERSECTS any added range of that file (block granularity is the
     profile's; intersections are reported so nothing is hidden).
  5. Aggregate: covered statements / total statements over intersecting
     blocks, per file and overall. New files (added entirely) are pure
     new-logic; modified files report the added-hunks slice.
"""
import subprocess, sys, re, collections, json

BASE = sys.argv[1] if len(sys.argv) > 1 else "f0c82905"
REPO = sys.argv[2] if len(sys.argv) > 2 else "."
PROFILES = sys.argv[3:]

def run(*args, cwd=REPO):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True).stdout

def changed_files():
    out = run("git", "diff", BASE, "HEAD", "--numstat", "--", "*.go")
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            files.append(parts[2])
    return [f for f in files if not f.endswith("_test.go")]

def added_ranges(path):
    out = run("git", "diff", BASE, "HEAD", "-U0", "--", path)
    ranges = []
    new_line = None
    for line in out.splitlines():
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if m:
            start = int(m.group(1)); count = int(m.group(2) or 1)
            if count > 0:
                ranges.append((start, start + count - 1))
    return ranges

files = changed_files()
ranges = {f: added_ranges(f) for f in files}

total = covered = 0
per_file = collections.defaultdict(lambda: [0, 0])
for prof in PROFILES:
    for line in open(prof):
        if line.startswith("mode:"):
            continue
        loc, stmts, hits = line.rsplit(" ", 2)
        stmts = int(stmts); hits = int(hits)
        fname, span = loc.split(":", 1)
        m = re.match(r"(\d+)\.(\d+),(\d+)\.(\d+)$", span)
        if not m:
            continue
        start, end = int(m.group(1)), int(m.group(3))
        # profile paths are relative to their module dir; normalize against repo-relative changed files
        cands = [f for f in ranges if f.endswith(fname) or fname.endswith(f.split("v3/")[-1])]
        for f in cands:
            for (a, b) in ranges[f]:
                if start <= b and end >= a:  # intersects an added range
                    per_file[f][0] += stmts
                    per_file[f][1] += stmts if hits > 0 else 0
                    total += stmts
                    covered += stmts if hits > 0 else 0
                    break

result = {"aggregate": {"statements": total, "covered": covered, "pct": round(100*covered/total, 1) if total else None}}
result["files"] = {f: {"added_ranges": ranges[f], "statements": v[0], "covered": v[1],
                       "pct": round(100*v[1]/v[0], 1) if v[0] else None}
                   for f, v in sorted(per_file.items())}
print(json.dumps(result, indent=1))
