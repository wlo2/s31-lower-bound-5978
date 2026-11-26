#!/usr/bin/env python3
"""wallscan.py CAND.json.gz SQV T_LO T_HI NT Y_LO Y_HI NY
For directions whose half-angle tangent lies in [T_LO, T_HI] (about NT of them), probe coverage of the
core at the extreme right-wall centre x = L - r(a), a = t_j - step/2, for NY values of y.  Prints the minimum."""
import sys, gzip, json, subprocess
from fractions import Fraction as F
from concurrent.futures import ThreadPoolExecutor
cand, sqv = sys.argv[1], sys.argv[2]
tlo, thi, nt, ylo, yhi, ny = float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), int(sys.argv[8])
d = json.load(gzip.open(cand, 'rt')); L = F(d['L']); step = F(d['proof_net']['step'])
j0, j1 = int(tlo / float(step)), int(thi / float(step)) + 1
js = sorted(set(j0 + (j1 - j0) * k // max(nt - 1, 1) for k in range(nt)))
def probe(j, y):
    a = (j - F(1, 2)) * step
    r = (1 - a * a + 2 * a) / (2 * (1 + a * a))
    x = float(L - r) - 1e-12
    out = subprocess.run([sqv, '--candidate', cand, '--n', str(d['n']), '--probe', f'{j},{x!r},{y!r}'], capture_output=True, text=True).stdout
    return json.loads(out)['exact_coverage_approx'], j, y
jobs = [(j, ylo + (yhi - ylo) * i / max(ny - 1, 1)) for j in js for i in range(ny)]
with ThreadPoolExecutor(9) as ex:
    res = list(ex.map(lambda t: probe(*t), jobs))
res.sort()
print(f"{cand.split('/')[-1]}: B={float(F(d['B'])):.9f} step={d['proof_net']['step']} probes={len(res)} "
      f"min coverage {res[0][0]:.12f} (deficit {1 - res[0][0]:.3e}) at j={res[0][1]} (t={res[0][1] * float(step):.6f}) y={res[0][2]:.5f}")
for c, j, y in res[:4]: print(f"   {c:.12f} j={j} y={y:.5f}")
