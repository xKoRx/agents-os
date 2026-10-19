import sys, collections

rec = "/home/echo-dev/forge-cert-20261018/rec/"
label = sys.argv[1] if len(sys.argv) > 1 else "g1-ca"

# CA window: from cpu.csv profile, boot settles at ~40s, save/exit starts ~250s.
# Derive precisely: first sample where 30s-trailing mean < 1.30 cores, and last
# sample before the final 15s (exit tail).
rows = []
prev = None
for line in open(rec + label + "-cpu.csv"):
    r = line.split()
    ns, s, th = int(r[0]), int(r[1]), int(r[2])
    if prev is not None:
        rows.append((ns, (s - prev[1]) / ((ns - prev[0]) / 1e9) / 100.0, th))
    prev = (ns, s, th)

t0 = rows[0][0]
tend = rows[-1][0]
# CA start: first index after t=25s where rate stays <=1.3 for 10 consecutive samples
start = None
for i in range(25, len(rows) - 10):
    if all(rows[j][1] <= 1.3 for j in range(i, i + 10)):
        start = i
        break
# CA end: last index before the final 12s where rate <=1.3 held backwards
end = len(rows) - 1
for i in range(len(rows) - 1, 25, -1):
    if all(rows[j][1] <= 1.3 for j in range(max(start or 0, i - 10), i + 1)):
        end = i
        break

t1 = rows[start][0] if start is not None else t0 + 40 * int(1e9)
t2 = rows[end][0] if end is not None else tend - 12 * int(1e9)
wall = (t2 - t1) / 1e9

jf = 0
for ns, s in []:
    pass
# integral over window from raw cumulative csv
prev = None
tot = 0
peak = []
for line in open(rec + label + "-cpu.csv"):
    r = line.split()
    ns, s = int(r[0]), int(r[1])
    if prev is not None and prev[0] >= t1 and ns <= t2:
        tot += s - prev[1]
    prev = (ns, s)
print("CA window: %.1fs -> %.1fs wall=%.1fs cpu_s=%.1f mean_cores=%.3f"
      % ((t1 - t0) / 1e9, (t2 - t0) / 1e9, wall, tot / 100.0, tot / 100.0 / wall))

# per-tid cumulative ticks: first & last value inside window
firstv = {}
lastv = {}
for line in open(rec + label + "-threads.csv"):
    p = line.strip().split(",")
    if len(p) < 5:
        continue
    ns, tid, state, cpu, tk = int(p[0]), p[1], p[2], p[3], int(p[4])
    if t1 <= ns <= t2:
        if tid not in firstv:
            firstv[tid] = tk
        lastv[tid] = tk
        tid_state = state
deltas = {}
for tid in lastv:
    d = lastv[tid] - firstv.get(tid, 0)
    if d > 0:
        deltas[tid] = d
top = sorted(deltas.items(), key=lambda kv: -kv[1])[:12]
print("== per-tid cpu-s inside CA window (top 12) ==")
for tid, d in top:
    print("tid %s: %.1f cpu-s" % (tid, d / 100.0))
busy = [d for d in deltas.values() if d > 100]
print("tids with >=1 cpu-s in CA window: %d ; >=10 cpu-s: %d"
      % (len(busy), len([d for d in deltas.values() if d > 1000])))
print("sum of per-tid deltas: %.1f cpu-s" % (sum(deltas.values()) / 100.0))
