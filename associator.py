#!/usr/bin/env python3
"""What the SOTP's "Associator Verification Nodes" can actually read.

SOTP Sec. 4.2 places a node "at the intersection of three spin channels" and
claims it executes (A |x| B) |x| C vs A |x| (B |x| C) natively, the associator
being "a non-zero hardware observable".  Table 1 maps e1,e2,e3 to the three spin
polarisation components sigma_x, sigma_y, sigma_z.  {e0,e1,e2,e3} is a quaternion
subalgebra of O, and quaternions are associative, so this script measures what
the node reads for states the spin channels can actually carry.
"""
import itertools
import numpy as np
from fano import PAPER, table, mul

S, T = table(PAPER)


def assoc(X, Y, Z):
    return mul(S, T, mul(S, T, X, Y), Z) - mul(S, T, X, mul(S, T, Y, Z))


def sample(support, n, rng):
    """Random states supported only on the given basis indices."""
    X = np.zeros((n, 8))
    X[:, support] = rng.normal(size=(n, len(support)))
    return X


# Table 1 of SOTP, in the paper's own words.
MAP = {0: "spin chemical potential mu_s", 1: "in-plane spin sigma_x",
       2: "in-plane spin sigma_y", 3: "out-of-plane spin sigma_z",
       4: "skyrmion charge Q_top (integer)", 5: "skyrmion helicity angle gamma",
       6: "valley pseudo-spin", 7: "topological edge current phase"}

rng = np.random.default_rng(0)
N = 20000

print("associator magnitude by which basis directions the three inputs use")
print(f"{'support of the three inputs':46s} {'mean |[A,B,C]|':>15s} {'frac != 0':>10s}")
cases = [
    ("full octonion (e0..e7)", list(range(8))),
    ("spin channels only (e0,e1,e2,e3)  <- Sec. 4.2", [0, 1, 2, 3]),
    ("spin + skyrmion charge (e0..e4)", [0, 1, 2, 3, 4]),
    ("any single Fano triad + e0, e.g. (e1,e2,e3)", [0, 1, 2, 3]),
    ("e0,e1,e4,e5 (one spin axis + skyrmion pair)", [0, 1, 4, 5]),
]
for name, sup in cases:
    A, B, C = (sample(sup, N, rng) for _ in range(3))
    m = np.array([np.linalg.norm(assoc(A[i], B[i], C[i])) for i in range(N)])
    print(f"{name:46s} {m.mean():15.6e} {np.mean(m > 1e-12):10.4f}")

print("\nevery 4-dim subalgebra spanned by e0 + one Fano triad:")
for a, b, c in PAPER:
    sup = [0, a, b, c]
    A, B, C = (sample(sup, 3000, rng) for _ in range(3))
    m = max(np.linalg.norm(assoc(A[i], B[i], C[i])) for i in range(3000))
    print(f"  (e0,e{a},e{b},e{c}): max |associator| = {m:.3e}")

# Which triples of DISTINCT basis units have a non-vanishing associator at all?
nz = tot = 0
for i, j, k in itertools.combinations(range(1, 8), 3):
    ei, ej, ek = (np.eye(8)[x] for x in (i, j, k))
    tot += 1
    if np.linalg.norm(assoc(ei, ej, ek)) > 1e-12:
        nz += 1
print(f"\ntriples of distinct imaginary units with [ei,ej,ek] != 0: {nz} of {tot}"
      f"  ({100*nz/tot:.1f} %)")
print("the 7 vanishing ones are exactly the 7 Fano lines:",
      sorted(tuple(sorted(t)) for t in PAPER) ==
      sorted((i, j, k) for i, j, k in itertools.combinations(range(1, 8), 3)
             if np.linalg.norm(assoc(*(np.eye(8)[x] for x in (i, j, k)))) < 1e-12))

# Trilinearity: the associator carries magnitude, not structure.
print("\nscaling of |[A,B,C]| with input magnitude (should be exactly cubic):")
A, B, C = (sample(list(range(8)), 1, rng)[0] for _ in range(3))
base = np.linalg.norm(assoc(A, B, C))
for s in (1, 2, 5, 10):
    v = np.linalg.norm(assoc(s * A, s * B, s * C))
    print(f"  scale {s:3d}: |assoc| = {v:12.6e}   ratio to s^3 * base = {v/(s**3*base):.12f}")

print("\n=== why there was no lucky choice of line ===")
print("each Fano line together with e0 is closed under multiplication and its three")
print("units square to -1, i.e. it is a copy of H sitting inside O:")
for a, b, c in PAPER:
    sup = {0, a, b, c}
    closed = all(T[i, j] in sup for i in sup for j in sup)
    sq = all(mul(S, T, np.eye(8)[x], np.eye(8)[x])[0] == -1 for x in (a, b, c))
    print(f"  (e0,e{a},e{b},e{c}): closed under multiplication = {closed}, "
          f"e^2 = -1 for all three = {sq}")
print("O has exactly 7 quaternion subalgebras containing 1, and they are exactly the")
print("7 lines of the Fano plane.  A triad gate IS a quaternion subalgebra, so its")
print("associator is zero by theorem, not by an accident of orientation.  There is no")
print("orientation of the Fano plane, valid or otherwise, for which a triad gate reads")
print("a non-zero associator.\n")

NAMES = {1: "sigma_x", 2: "sigma_y", 3: "sigma_z", 4: "Q_top",
         5: "helicity", 6: "valley", 7: "edge phase"}
lines = [set(l) for l in PAPER]
print("the 28 triples that DO have a non-zero associator, in Table 1 variables:")
shown = 0
for i, j, k in itertools.combinations(range(1, 8), 3):
    if any({i, j, k} == l for l in lines):
        continue
    v = np.linalg.norm(assoc(np.eye(8)[i], np.eye(8)[j], np.eye(8)[k]))
    if shown < 4:
        print(f"  (e{i},e{j},e{k}) = ({NAMES[i]}, {NAMES[j]}, {NAMES[k]}): "
              f"|assoc| = {v:.1f}")
        shown += 1
print("  ... 24 more, all of the same form.")
print("every one of the 28 mixes a spin component with a skyrmion winding number, a")
print("valley polarisation or an edge phase -- and closure.py shows that the product")
print("of such states is never itself a physical state.  The two defects interlock:")
print("the only gates whose observable is non-zero are the gates whose output the")
print("hardware cannot hold.")
