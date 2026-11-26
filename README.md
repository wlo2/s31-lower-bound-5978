# s(31) ≥ 2989/500 = 5.978

A rectangle-measure certificate proving **s(31) ≥ 2989/500 = 5.978**: no 31 unit squares fit in a square of side 5.978.

The registered record at n = 31 is s(31) ≥ 2391/400 = 5.9775, Hiroaki Hosono's `mixed_n31_L59775` (T-232 in [jlevy/squares](https://github.com/jlevy/squares)). The upper bound is 6. Joost de Winter's open reports also cover n = 31, none of them registered yet: 5.977500696… in jlevy/squares#1039, then 59777257/10000000 in the #1042 supplement, and s(31) > 149447/25000 = 5.97788 in #1060's final table. This certificate is 1/2000 above T-232 and 3/25000 above the highest of those.

It is Hosono's measure, scaled. Nothing in the measure was re-optimized. The finer net's headroom goes into a larger core. Without that, the scaled measure fails at the walls (jlevy/squares#890 recorded that failure). A core larger than the dilated one is not new: Joost de Winter's T-327 (jlevy/squares#1018, n = 108) used one first. We found it independently for n = 31.

**Status.** The register's verifier, `sqverify-fast`, unmodified, decided every one of the 5,925 declared directions: all verified, none refused. That is the authors' own run. No independent replay, review or formalization has been done.

## Certificate and exact identities

- Format M; `n = 31`, `L = 2989/500`, similarity `λ = 11956/11955` from Hosono's `L = 2391/400`.
- Hosono's 536 rectangle orbits (D4; 4,244 rectangles after expansion), every coordinate multiplied by λ and every mass unchanged.
  - Total mass `3099999/100000 = 31 − 1/100000 < 31`. No points or segments.
- Core side `B = 99993/100000`, declared net step `D = 1/14300`, last index `5924`: **5,925 directions**. The last tangent `1481/3575` is past tan(π/8), and index 5923 is not.
- `B(1 + D) = 1429999893/1430000000 < 1`; `B(1 + D/(1 − D²/4)) = 27265331259869/27265333300000 < 1`.
  - So every unit square contains a concentric core at a net angle strictly inside its interior.
- `B` exceeds the dilated core `B_old · λ = 14942011/14943750` by a factor of `1 + 4.64 · 10⁻⁵`.
- Candidate gzip SHA-256, equal to the verifier's `input_sha256`: `d5b8d54ac0eeab94926e7c6296fbaf8a86b113ebf7bb19e5b480b534576e52d7`.
- Candidate uncompressed JSON SHA-256: `5aa1a25f6e4cfbc9607c358f41bb2ef0284fbcc14b4c25fe600891450640154b`.
- Hosono's source: [`wand125/square-packing@23e31862345c532d17ad2c896677a3a8d8821aa4`](https://github.com/wand125/square-packing/tree/23e31862345c532d17ad2c896677a3a8d8821aa4/problems/square-lower-bounds/certificates/mixed_n31_L59775), `problems/square-lower-bounds/certificates/mixed_n31_L59775/candidate.json`, JSON SHA-256 `4a7df269037a6449ba2d4bee2b6a76962df097c1515025545d4ca4cfcc39be3b` (its `files-sha256.json`).
  - The copy in `source/` is jlevy/squares' retained one (`packing/resources/web/wand125-fine-net-n31-2026-10-11/release/certificates/mixed_n31_L59775/candidate.json.gz` at `c5775bae40085f67f4c30f8916b0d6e998c304ab`). It decompresses to those same bytes.
- `tools/dilate2.py` regenerates the candidate from the source byte for byte (uncompressed; the gzip wrapper stores a timestamp).

## Why the core is larger than B·λ

Scaling the container, the measure and the core by λ keeps the mass every old core captured. Two things do not carry over:
- **The centre domain grows.** Unit squares do not scale, so the admissible centre domain grows toward the walls in old coordinates.
- **The net changes.** Hosono's 2,073-direction net (step 1/5002) does not admit the larger core. On the step-1/14300 net only direction 0 coincides with one of his, so 5,924 of the 5,925 directions are new.

Özden's dilations of a Hosono measure for n = 94 (T-262 and T-266) set the core to exactly `B_old · λ`. De Winter's T-327 at n = 108 did not: its finer net admits a larger core, and it uses one. jlevy/squares#890 reports that the same move at n = 31 fails: at L = 2989/500 on a step-1/8600 net, direction 529 is refused near a wall. That matches what we found with `B = B_old · λ`: 19 of 3,564 directions refused, a contiguous band near half-angle tangent 0.062.

Exact probes (`tools/wallscan.py`) of the cores at the extreme centre `x = L − r(a)` across that band show the size of the problem:

| core | net step | least capture found at the wall (567 probes) |
|---|---|---|
| `B_old · λ = 14942011/14943750` | 1/8600 | 0.99993 |
| `99993/100000` | 1/14300 | 1.0016 |

- The probe grid's least value is not a certified minimum. The certified check is the full run below. Outputs: `wallscan/`.
- A step of 1/14300 admits a core `4.6 · 10⁻⁵` larger than `B_old · λ`. A larger concentric core at the same pose contains the smaller one, so no capture falls.
- At the wall the capture rises by about 1.7 · 10⁻³, because the core's edge reaches a thin, dense rectangle of the measure.
- The scaled measure's whole mass slack is 1/100000, so no rescaling of masses could have covered the shortfall.

## Checking

1. **`sqverify-fast`, every declared direction.** Source: [`jlevy/squares@c5775bae40085f67f4c30f8916b0d6e998c304ab`](https://github.com/jlevy/squares/tree/c5775bae40085f67f4c30f8916b0d6e998c304ab/packing/sqverify_fast), `packing/sqverify_fast`, unmodified, embedded source SHA-256 `d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88`.
   - Build: `cargo build --release --locked --ignore-rust-version` with rustc 1.94.0 on aarch64-apple-darwin. The crate pins rustc 1.98.0, which was not used.
   - Command: `sqverify-fast --candidate candidate.json.gz --n 31 --directions all --threads 9 --confirm --receipts <dir>` (`verify/run_full.sh`).
   - Result (`verify/summary.json`): status `VERIFIED`, `refused_directions: []`.
     - All 5,925 unique indices 0..5924 have verdict `verified` at threshold exactly 1.
     - Least certified lower bound `1.0000000000026954`, at direction 1674.
     - 2,235,226,568 nodes.
   - Cost: 35,574 CPU-seconds, 3,956 s of wall on 9 threads of an Apple M4, 26 November 2026.
   - Per-direction records: `verify/directions.jsonl.gz` (uncompressed SHA-256 `907e84f4d2dfa3473e68b76f5469205a244c33cb72f736d37a29ba0475fab361`). Receipts: `verify/receipts.tar.gz`.
2. **Exact dilation audit** (`tools/audit_dilation.py`, written separately from the tool that built the candidate; output `audit/audit_dilation.txt`).
   - It checks in exact rationals that every coordinate is λ times the source's and every mass is unchanged.
   - It also checks that the total is the exact sum and below 31, the four net premises, and `B ≥ B_old · λ`. All pass.
3. **Negative control.** The same geometry with every mass multiplied by 99/100 (`controls/`) is refused at all four requested directions, 0, 895, 2962 and 5924: summary `REFUSED`.
   - At 895, 2962 and 5924 the refusal carries an exact admissible witness below 1. The lowest is 0.99296 at direction 5924.
   - This is a four-direction control, not a whole-net mutant replay.

## What the checks share

- Check 1 is this repository's authors running the register's own verifier, so it is not an independent implementation.
- Checks 2 and 3 are by the same authors. Check 2 decides no coverage at all; it audits only the exact identities.
- Hosono's original was decided by `sqverify-proof-net`, which shares the `sqverify_fast` crate apart from its declared-net reader.

## Not done

- No independent replay, second implementation, human review or proof-assistant formalization.
- No whole-net mutant control.
- No claim beyond 5.978.
  - At 5.9785, with core 0.99999 on a step-1/100100 net (41,464 directions), the wall probes pass with margin 4 · 10⁻⁴. The full net has not been run.
  - At 5.9786 the probes already fail.
  - No dilation of this measure can pass 2391/400 · 5000/4999 ≈ 5.97870.

## Reproduce

```
python3 -I tools/dilate2.py source/mixed_n31_L59775_candidate.json.gz 2989/500 1/14300 out.json.gz 99993/100000
python3 -I tools/audit_dilation.py source/mixed_n31_L59775_candidate.json.gz candidate.json.gz
bash verify/run_full.sh /path/to/sqverify-fast verify/out 9
```

- `gunzip -c out.json.gz | shasum -a 256` gives `5aa1a25f…154b`.
- The mutant is `dilate2.py … 99993/100000 99/100`.
- `SHA256SUMS` lists every file.

## Lineage and credit

The measure, its format and the declared-net method are Hiroaki Hosono's (wand125). They come after Tokoharu's rectangle-density certificates, and are checked with the Squares Project's `sqverify-fast`. Dilating a Hosono measure onto a finer net follows Doğa Özden's T-262 and T-266. Joost de Winter's T-327 had already used a core larger than the dilated one. We found that step independently. The contribution here is applying it at n = 31, where it lets the dilation pass where #890 found it refused.

Suggested credit: **wlo2 after Hosono, Tokoharu, Özden and Levy**, with de Winter's T-327 noted as the first use of the larger core.

## Licence

See [LICENSE.md](LICENSE.md). The source certificate and everything derived from it keep Hosono's MIT licence (`source/HOSONO-LICENSE`).

## AI assistance

Claude (Anthropic), working as an AI agent in Claude Code, did the research, found the enlarged-core fix, built and verified the certificate and drafted this repository, under the author's direction. The author chose the problem and approved each step.
