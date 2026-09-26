#!/usr/bin/env python3
"""Is the SOTP/PCTP state space closed under the operation the hardware executes?

A processor can only compute X (x) Y if the product is again a state the hardware
can hold.  Both papers map algebraic coordinates onto physical variables that
carry hard constraints: a skyrmion topological charge is an integer, a helicity
angle lives on a circle, a spin polarisation has |sigma| <= 1, an OAM charge is an
integer.  This script draws physically admissible states and asks how often the
product is admissible too.
"""
import numpy as np
from fano import PAPER, table, mul

S, T = table(PAPER)
rng = np.random.default_rng(0)
N = 200000


def sotp_state(n):
    """A state the SOTP substrate of Sec. 3/4 can physically hold."""
    X = np.zeros((n, 8))
    X[:, 0] = rng.normal(size=n)                        # mu_s, unconstrained
    v = rng.normal(size=(n, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    X[:, 1:4] = v                                       # |sigma| = 1
    X[:, 4] = rng.choice([-1.0, 1.0], size=n)           # Q_top = +-1 (Table 1)
    X[:, 5] = rng.uniform(0, 2 * np.pi, size=n)         # helicity angle gamma
    X[:, 6] = rng.uniform(-1, 1, size=n)                # valley polarisation
    X[:, 7] = rng.uniform(0, 2 * np.pi, size=n)         # edge current phase
    return X


def admissible(Z, tol=1e-9):
    """Same constraints, applied to the product."""
    ok_spin = np.abs(np.linalg.norm(Z[:, 1:4], axis=1) - 1.0) < 1e-6
    ok_q = np.minimum(np.abs(Z[:, 4] - 1.0), np.abs(Z[:, 4] + 1.0)) < 1e-6
    ok_val = np.abs(Z[:, 6]) <= 1.0
    return ok_spin, ok_q, ok_val


A, B = sotp_state(N), sotp_state(N)
Z = np.array([mul(S, T, A[i], B[i]) for i in range(N)])
ok_spin, ok_q, ok_val = admissible(Z)
print("SOTP: product of two physically admissible states (n = %d)" % N)
print(f"  |sigma| still 1 (e1,e2,e3):          {100*ok_spin.mean():8.4f} %")
print(f"  Q_top still +-1, i.e. an integer:    {100*ok_q.mean():8.4f} %")
print(f"  valley polarisation still in [-1,1]: {100*ok_val.mean():8.4f} %")
print(f"  all three at once:                   {100*(ok_spin&ok_q&ok_val).mean():8.4f} %")
q = Z[:, 4]
print(f"  Q_top of the product: mean {q.mean():+.4f}, sd {q.std():.4f}, "
      f"range [{q.min():+.3f}, {q.max():+.3f}]")
print(f"  fraction of products with |Q_top| > 1 (no such skyrmion exists): "
      f"{100*np.mean(np.abs(q) > 1.0):.2f} %")
print(f"  fraction with 0.1 < |Q_top| < 0.9 (a fractional winding number): "
      f"{100*np.mean((np.abs(q) > 0.1) & (np.abs(q) < 0.9)):.2f} %")

# ---- PCTP, Sec. 3: same question for the optical mapping -------------------
def quat_mul(a, b):
    w1, x1, y1, z1 = a.T
    w2, x2, y2, z2 = b.T
    return np.stack([w1*w2 - x1*x2 - y1*y2 - z1*z2,
                     w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2], axis=1)


def pctp_state(n, lmax=5):
    """PCTP Sec. 3: q_a = amplitude/phase, q_i,q_j = Stokes S2,S3, q_k = OAM charge l."""
    X = np.zeros((n, 4))
    X[:, 0] = rng.uniform(0, 1, size=n)                 # amplitude, normalised
    s = rng.normal(size=(n, 3)); s /= np.linalg.norm(s, axis=1, keepdims=True)
    X[:, 1:3] = s[:, 1:3]                               # S2, S3 of a unit Stokes vector
    X[:, 3] = rng.integers(-lmax, lmax + 1, size=n)     # topological charge l in Z
    return X


A, B = pctp_state(N), pctp_state(N)
Z = quat_mul(A, B)
l = Z[:, 3]
int_l = np.abs(l - np.round(l)) < 1e-9
print("\nPCTP: product of two physically admissible optical states (n = %d)" % N)
print(f"  OAM charge l of the product still an integer: {100*int_l.mean():8.4f} %")
print(f"  |(S2,S3)| of the product still <= 1:          "
      f"{100*np.mean(np.linalg.norm(Z[:, 1:3], axis=1) <= 1.0):8.4f} %")
print(f"  amplitude q_a of the product still in [0,1]:  "
      f"{100*np.mean((Z[:, 0] >= 0) & (Z[:, 0] <= 1)):8.4f} %")
print(f"  all three at once:                            "
      f"{100*np.mean(int_l & (np.linalg.norm(Z[:,1:3],axis=1)<=1) & (Z[:,0]>=0) & (Z[:,0]<=1)):8.4f} %")

# degrees of freedom actually available in one coherent wavepacket
print("\nPCTP Sec. 3, degree-of-freedom count for one wavepacket:")
print("  physical: amplitude E0 (1) + carrier phase phi0 (1) + Poincare sphere (2)"
      " + OAM charge l (1, discrete) = 4 continuous + 1 discrete")
print("  algebraic: q_a, q_i, q_j, q_k = 4 continuous reals")
print("  q_a is assigned BOTH amplitude and phase (Eq. 6), so the map is not")
print("  injective: 2 physical numbers collapse into 1 coordinate and cannot be")
print("  read back out.  S1 of the Stokes vector is dropped entirely.")
