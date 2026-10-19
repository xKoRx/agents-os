import sys

rec = "/home/echo-dev/forge-cert-20261018/rec/"
label = sys.argv[1] if len(sys.argv) > 1 else "g1-ca"

# --- CPU profile in 10s buckets ---
rows = []
prev = None
for line in open(rec + label + "-cpu.csv"):
    r = line.split()
    ns, s, th = int(r[0]), int(r[1]), int(r[2])
    if prev is not None:
        dt = (ns - prev[0]) / 1e9
        dj = s - prev[1]
        rows.append((ns, dj / dt / 100.0, th, dj))
    prev = (ns, s, th)

t0 = rows[0][0]
buckets = {}
for ns, cores, th, dj in rows:
    b = int((ns - t0) / 1e10)  # 10s
    agg = buckets.setdefault(b, [0.0, 0, 0, th])
    agg[0] += cores
    agg[1] += 1
    agg[2] += dj
    agg[3] = max(agg[3], th)

print("== CPU profile (10s buckets): t_s | mean_cores | core_s | max_threads ==")
for b in sorted(buckets):
    m, n, dj, th = buckets[b]
    print("%4d  %6.2f  %7.1f  %4d" % (b * 10, m / n, dj / 100.0, th))

total = sum(dj for _, _, _, dj in rows) / 100.0
wall = (rows[-1][0] - rows[0][0]) / 1e9
print("TOTAL: wall=%.1fs cpu_s=%.1f mean=%.2f cores" % (wall, total, total / wall))

# --- per-tid tick totals ---
import collections
tid_ticks = collections.Counter()
tid_name_state = {}
for line in open(rec + label + "-threads.csv"):
    p = line.strip().split(",")
    if len(p) >= 5:
        tid_ticks[p[1]] += int(p[4])
print("== top-15 tids by total ticks (whole run) ==")
for tid, tk in tid_ticks.most_common(15):
    print("tid %s: %d ticks (%.1f cpu-s)" % (tid, tk, tk / 100.0))
busy = [t for t in tid_ticks.values() if t > 100]
print("tids with >100 ticks (>=1 cpu-s): %d" % len(busy))
busy5 = [t for t in tid_ticks.values() if t > 500]
print("tids with >500 ticks (>=5 cpu-s): %d" % len(busy5))
