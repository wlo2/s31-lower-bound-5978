#!/usr/bin/env python3
"""
dilate.py -- dilate a format-M measure certificate (sqverify-fast) to a larger side.

    python3 dilate2.py SRC.json[.gz] L_NEW STEP OUT.json.gz B_NEW [KAPPA]

As dilate.py, but the core side is B_NEW (at least B * lam) instead of B * lam: the finer net pays for a larger core.

Every rectangle coordinate is multiplied by lam = L_NEW / L, the masses are unchanged,
the core side becomes B * lam, and the declared half-angle net becomes
{step: STEP, last: J} with J the first index whose tangent J*STEP reaches tan(pi/8).

Premises checked here in exact rationals (sqverify-fast re-checks all of them):
  B(1 + D) < 1,  B(1 + D/(1 - D^2/4)) < 1,  tan(pi/8) <= last*D <= 1/2,  at most 2^16 directions.
Nothing about coverage carries over: the dilated certificate must be verified in full.
"""
import gzip
import json
import sys
from fractions import Fraction as F


def main():
    src, l_new, step, out = sys.argv[1], F(sys.argv[2]), F(sys.argv[3]), sys.argv[4]
    b_new = F(sys.argv[5])
    kappa = F(sys.argv[6]) if len(sys.argv) > 6 else F(1)   # optional: every mass times kappa
    op = gzip.open if src.endswith('.gz') else open
    with op(src, 'rt') as fh:
        d = json.load(fh)
    if set(d) - {'n', 'L', 'B', 'proof_net', 'total_mass', 'points', 'rectangles'}:
        raise SystemExit(f"unexpected fields {set(d)}")
    if d['points']:
        raise SystemExit("points present: not handled")
    L, B = F(d['L']), F(d['B'])
    lam = l_new / L
    Bn = b_new
    if Bn < B * lam: raise SystemExit('B_NEW below B * lam')
    D = step
    last = 0
    while (last * D + 1) ** 2 < 2:          # last*D >= sqrt(2) - 1 = tan(pi/8)
        last += 1
    checks = {
        'lam > 1': lam > 1,
        'B(1+D) < 1': Bn * (1 + D) < 1,
        'B(1+D/(1-D^2/4)) < 1': Bn * (1 + D / (1 - D * D / 4)) < 1,
        'last*D <= 1/2': last * D <= F(1, 2),
        'directions <= 2^16': last + 1 <= 2 ** 16,
    }
    for k, v in checks.items():
        print(f"  {k}: {v}")
    if not all(checks.values()):
        raise SystemExit("premise fails")
    mass0 = sum(F(r['mass']) for r in d['rectangles'])
    if mass0 != F(d['total_mass']):
        raise SystemExit(f"mass {mass0} does not match total_mass")
    rects = [{'rectangle': [str(F(c) * lam) for c in r['rectangle']], 'mass': str(F(r['mass']) * kappa)}
             for r in d['rectangles']]
    mass = sum(F(r['mass']) for r in rects)
    if mass >= d['n'] or kappa <= 0:
        raise SystemExit(f"scaled mass {mass} is not below n = {d['n']}")
    print(f"mass factor kappa = {kappa}; mass {mass0} -> {mass} (slack {float(d['n'] - mass):.3e})")
    new = {'n': d['n'], 'L': str(l_new), 'B': str(Bn),
           'proof_net': {'step': str(D), 'last': last},
           'total_mass': str(mass), 'points': [], 'rectangles': rects}
    with gzip.open(out, 'wt') as fh:
        json.dump(new, fh, indent=1)
    print(f"L {L} -> {l_new} (= {float(l_new):.6f}), lam = {lam} = {float(lam):.9f}")
    print(f"B {B} -> {Bn} = {float(Bn):.9f}; B(1+D) = {float(Bn * (1 + D)):.10f}")
    print(f"net step {D}, last {last} ({last + 1} directions, last tangent {float(last * D):.6f})")
    print(f"mass {mass} = {float(mass):.6f}; {len(rects)} rectangles -> {out}")


if __name__ == '__main__':
    main()
