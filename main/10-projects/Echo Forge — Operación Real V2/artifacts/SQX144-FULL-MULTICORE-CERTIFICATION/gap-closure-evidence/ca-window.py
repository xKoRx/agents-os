import sys

rec = "/home/echo-dev/forge-cert-20261018/rec/"
label = sys.argv[1] if len(sys.argv) > 1 else "g1-ca"
off_start = int(sys.argv[2])
off_end = int(sys.argv[3])

size = []
for line in open(rec + label + "-size.csv"):
    ns, b = line.split()
    size.append((int(ns), int(b)))

def tfor(off):
    for ns, b in size:
        if b >= off:
            return ns
    return None

t1 = tfor(off_start)
t2 = tfor(off_end)
wall = (t2 - t1) / 1e9
print("CA window epoch_ns: %d -> %d wall_s=%.2f" % (t1, t2, wall))

rows = []
prev = None
jf = 0
rates = []
threads_max = 0
for line in open(rec + label + "-cpu.csv"):
    r = line.split()
    ns, s, th = int(r[0]), int(r[1]), int(r[2])
    if prev is not None and prev[0] >= t1 and ns <= t2:
        dt = (ns - prev[0]) / 1e9
        dj = s - prev[1]
        if dt > 0:
            rates.append(dj / dt / 100.0)
        jf += dj
        threads_max = max(threads_max, th)
    prev = (ns, s, th)

mean = jf / wall / 100.0
rs = sorted(rates)
p5 = max(sum(rs[i:i+5]) / len(rs[i:i+5]) for i in range(0, max(len(rs) - 4, 1)))
peak1 = rs[-1] if rs else 0
print("CA: mean_cores=%.2f peak5=%.2f peak1=%.2f core_seconds=%.1f samples=%d threads_max=%d"
      % (mean, p5, peak1, jf / 100.0, len(rates), threads_max))
