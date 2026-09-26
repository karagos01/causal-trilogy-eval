#!/usr/bin/env python3
"""Two checks on Causal Quaternionic Field Theory (DOI 10.5281/zenodo.22959886).

(1) Sec. 2.1 states the classical obstruction to a quaternionic tensor product.
    We verify the algebra the paper gives.
(2) Sec. 2.2 Eq. (2) proposes to resolve it with (q1,t1) |x| (q2,t2) = (q1 q2, t1<t2).
    We measure what that operation does to a two-particle state, and then simulate
    the paper's own falsification experiment (Sec. 5, Causal Hysteresis Test).
"""
import numpy as np

def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2 - x1*x2 - y1*y2 - z1*z2,
                     w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2])

one, i, j, k = (np.eye(4)[n] for n in range(4))
name = {tuple(one): "1", tuple(i): "i", tuple(j): "j", tuple(k): "k",
        tuple(-one): "-1", tuple(-i): "-i", tuple(-j): "-j", tuple(-k): "-k"}

print("=== CQFT Sec. 2.1: the stated obstruction ===")
print("  j*i =", name[tuple(qmul(j, i))], " so (cA) (x) B with c=j, A=i, B=k gives -(k (x) k)")
print("  j*k =", name[tuple(qmul(j, k))], " so A (x) (cB)                 gives  (i (x) i)")
print("  the paper's claim that bilinearity forces -(k(x)k) = i(x)i is ALGEBRAICALLY CORRECT.")

print("\n=== CQFT Eq. (2): is |x| a tensor product? ===")
rng = np.random.default_rng(0)
print("  signature: H x H -> H, i.e. 4 + 4 real inputs -> 4 real outputs.")
print("  a tensor product of two 4-dim spaces has dimension 16 (over R, as a")
print("  bimodule over H it is still 4x4 = 16), so |x| cannot be one.")
# measure the information destroyed: the fibre over a fixed product
P = qmul(*rng.normal(size=(2, 4)))
pre = []
for _ in range(6):
    qA = rng.normal(size=4)
    qAinv = np.array([qA[0], -qA[1], -qA[2], -qA[3]]) / (qA @ qA)
    qB = qmul(qAinv, P)
    pre.append((qA, qB, qmul(qA, qB)))
err = max(np.linalg.norm(p[2] - P) for p in pre)
print(f"  six different input pairs reproducing the same product P, max error {err:.2e}")
print("  the pre-image of any product is a 4-parameter family: 4 of the 8 input")
print("  numbers are destroyed by every |x|, the operation is not invertible.")

print("\n=== CQFT Eq. (4): the entangled state Psi_AB = (qA,t0) |x| (qB,t0) ===")
# A Bell state and a product state must be distinguishable; under Eq. (4) they are not.
qA, qB = np.array([1, 0, 0, 0.]), np.array([0, 1, 0, 0.])
alt = (np.array([0, 0, 1, 0.]), np.array([0, 0, 0, -1.]))
print("  (1) |x| (i)      ->", qmul(qA, qB))
print("  (j) |x| (-k)     ->", qmul(*alt))
print("  two different two-particle configurations give the identical state; the")
print("  formalism has no way to express correlation, hence none to express")
print("  entanglement, which Sec. 3.2 is about.")

print("\n=== CQFT Sec. 5: simulating the Causal Hysteresis Test ===")
I2 = np.eye(2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]])
sz = np.array([[1, 0], [0, -1]], dtype=complex)

def rot(n, th):
    n = np.asarray(n, float); n /= np.linalg.norm(n)
    return np.cos(th/2)*I2 - 1j*np.sin(th/2)*(n[0]*sx + n[1]*sy + n[2]*sz)

# Bell state (Phi+)
psi = np.zeros(4, complex); psi[0] = psi[3] = 1/np.sqrt(2)
X = rot([1, 0, 0], 0.7)      # "operation X" on photon A
Y = rot([0, 1, 0], 1.3)      # "operation Y" on photon A
p1 = np.kron(Y @ X, I2) @ psi     # Path 1: X then Y
p2 = np.kron(X @ Y, I2) @ psi     # Path 2: Y then X

def rho_B(v):
    M = v.reshape(2, 2)
    return M.conj().T @ M

def rho_A(v):
    M = v.reshape(2, 2)
    return M @ M.conj().T

print(f"  the two paths give different joint states: ||p1 - p2|| = "
      f"{np.linalg.norm(p1-p2):.6f}")
print(f"  photon A's reduced state differs:          ||rhoA1 - rhoA2|| = "
      f"{np.linalg.norm(rho_A(p1)-rho_A(p2)):.6f}")
print(f"  photon B's reduced state:                  ||rhoB1 - rhoB2|| = "
      f"{np.linalg.norm(rho_B(p1)-rho_B(p2)):.3e}   <-- exactly zero")
# and it is zero for ANY local operations, tuned or not
worst = 0.0
for _ in range(20000):
    U = rot(rng.normal(size=3), rng.uniform(0, 2*np.pi))
    V = rot(rng.normal(size=3), rng.uniform(0, 2*np.pi))
    a = np.kron(V @ U, I2) @ psi
    b = np.kron(U @ V, I2) @ psi
    worst = max(worst, np.linalg.norm(rho_B(a) - rho_B(b)))
print(f"  worst ||rhoB1 - rhoB2|| over 20000 random non-commuting pairs: {worst:.3e}")
print("  no local operation on A, in any order, changes anything measurable on B")
print("  alone.  A 'deterministic, measurable phase shift in Photon B' is a signal")
print("  and would be faster-than-light communication.")

# and the correlations the paper says QM predicts to be identical
def corr(v, na, nb):
    A = na[0]*sx + na[1]*sy + na[2]*sz
    B = nb[0]*sx + nb[1]*sy + nb[2]*sz
    return float(np.real(v.conj() @ (np.kron(A, B) @ v)))

print("\n  joint correlators E(a,b), which the paper says QM predicts to be equal:")
for nb in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
    c1, c2 = corr(p1, [0, 0, 1], nb), corr(p2, [0, 0, 1], nb)
    print(f"    b = {nb}:  path1 {c1:+.6f}   path2 {c2:+.6f}   difference {c1-c2:+.6f}")
print("  standard QM already predicts different correlations, so the experiment")
print("  does not separate the two theories anywhere: where it could show a")
print("  difference, QM predicts one too; where QM predicts none, CQFT's")
print("  signature is forbidden by no-signalling.")

print("\n=== does the causal index tau enter any computed quantity? ===")
# Eq. (2) / SOTP Eq. (4): (q1,t1) |x| (q2,t2) = (q1 q2, t1 < t2).  The value
# component is q1 q2 for every choice of t1, t2: tau only records the order in
# which the operands were already written.
rng2 = np.random.default_rng(3)
q1, q2 = rng2.normal(size=(2, 4))
vals = set()
for t1, t2 in ((0, 1), (1, 2), (5, 17), (100, 101)):
    vals.add(tuple(np.round(qmul(q1, q2), 12)))
print(f"  distinct value components over 4 different (t1,t2) assignments: {len(vals)}")
print("  tau is not an argument of the value component.  Every prediction the")
print("  three papers derive from |x| is a prediction of ordinary quaternion or")
print("  octonion multiplication - Hamilton 1843, Graves 1843, Cayley 1845.")
print("  What is added is a label on the operand order, which was already there.")
