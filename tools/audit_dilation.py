#!/usr/bin/env python3
"""
audit_dilation.py -- check, in exact rationals, that a format-M candidate is a dilation of a source.

    python3 -I audit_dilation.py SOURCE.json[.gz] CANDIDATE.json[.gz]

Independent of the tool that built the candidate: it reads both files and checks
  * same n, no points, same number of rectangles in the same order;
  * every coordinate of every rectangle equals lam times the source's, with lam = L_new / L_old > 1;
  * every mass is unchanged, and total_mass is the exact sum of the masses and is below n;
  * the declared net premises: B(1 + D) < 1, B(1 + D/(1 - D^2/4)) < 1,
    last*D >= tan(pi/8) (as (last*D + 1)^2 >= 2), last*D <= 1/2, at most 2^16 directions;
  * the core is at least B_old * lam (so it is larger than the dilated core, never smaller).
Exits 0 only if every check passes.
"""
import gzip
import json
import sys
from fractions import Fraction as F


def load(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as fh:
        return json.load(fh)


def main():
    src, cand = load(sys.argv[1]), load(sys.argv[2])
    ok = True

    def check(name, cond, detail=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  [{'pass' if cond else 'FAIL'}] {name}{(': ' + detail) if detail else ''}")

    n = cand['n']
    L0, L1 = F(src['L']), F(cand['L'])
    lam = L1 / L0
    B0, B1 = F(src['B']), F(cand['B'])
    D, last = F(cand['proof_net']['step']), int(cand['proof_net']['last'])
    print(f"source L = {L0}, candidate L = {L1}, lam = {lam}")
    check('same n', src['n'] == n, str(n))
    check('lam > 1', lam > 1)
    check('no points in source or candidate', not src.get('points') and not cand.get('points'))
    rs, rc = src['rectangles'], cand['rectangles']
    check('same number of rectangles', len(rs) == len(rc), f"{len(rc)}")
    coords_ok = all(len(a['rectangle']) == len(b['rectangle']) and
                    all(F(y) == lam * F(x) for x, y in zip(a['rectangle'], b['rectangle']))
                    for a, b in zip(rs, rc))
    check('every coordinate = lam * source coordinate', coords_ok)
    mass_ok = all(F(a['mass']) == F(b['mass']) for a, b in zip(rs, rc))
    check('every mass unchanged', mass_ok)
    total = sum(F(b['mass']) for b in rc)
    check('total_mass is the exact sum', total == F(cand['total_mass']), str(total))
    check('total_mass < n', total < n, f"n - total = {n - total}")
    check('B(1 + D) < 1', B1 * (1 + D) < 1, f"{B1 * (1 + D)}")
    check('B(1 + D/(1 - D^2/4)) < 1', B1 * (1 + D / (1 - D * D / 4)) < 1, f"{B1 * (1 + D / (1 - D * D / 4))}")
    check('last*D >= tan(pi/8)', (last * D + 1) ** 2 >= 2, f"last tangent {last * D}")
    check('(last-1)*D < tan(pi/8) (net not longer than needed)', ((last - 1) * D + 1) ** 2 < 2)
    check('last*D <= 1/2', last * D <= F(1, 2))
    check('directions <= 2^16', last + 1 <= 2 ** 16, f"{last + 1} directions")
    check('core >= B_old * lam', B1 >= B0 * lam, f"B = {B1}, B_old * lam = {B0 * lam}, ratio - 1 = {float(B1 / (B0 * lam) - 1):.3e}")
    print('AUDIT PASS' if ok else 'AUDIT FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
