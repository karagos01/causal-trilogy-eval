# The associator vanishes on every gate: an evaluation of the Causal Field trilogy

**karagos01**, September 2026

An independent evaluation of three preprints deposited on Zenodo on 25 September
2026 by M. Mazgal and Gemini AI:

| | DOI | title |
|---|---|---|
| I | [10.5281/zenodo.22959886](https://doi.org/10.5281/zenodo.22959886) | The Causal Quaternionic Field Theory (CQFT) |
| II | [10.5281/zenodo.22962188](https://doi.org/10.5281/zenodo.22962188) | Photonic Causal Tensor Processor (PCTP) |
| III | [10.5281/zenodo.22962557](https://doi.org/10.5281/zenodo.22962557) | Spintronic Octonionic Tensor Processor (SOTP) |

## Abstract

The three preprints propose a non-Markovian quaternionic field theory and two
processor architectures built on it. This evaluation checks the parts that can be
computed. The algebra is correct, which is a change from the author's earlier
work: the oriented Fano plane printed in SOTP Eq. (3) is one of only 16 of the 128
possible orientations of those seven lines that yield a normed division algebra,
and the obstruction to a quaternionic tensor product stated in CQFT §2.1 is stated
accurately. The defects are all in the mapping from algebra to hardware, and the
central one is structural: the associator, which SOTP calls "a non-zero hardware
observable", vanishes identically on exactly the seven triples of basis units that
the Fano-mesh gate array is built from, and in particular on the three spin
channels where §4.2 places its Associator Verification Nodes. Beyond that, the
state space is not closed under the operation the hardware must execute — 0.0000 %
of products of two physically admissible states are themselves admissible, in both
architectures — the causal index τ never enters any computed quantity, the
operator ⊠ is not a tensor product and cannot express a two-particle state at all,
and CQFT's own falsification experiment is a no-signalling violation whose
"tuning" step is vacuous for the state it specifies. Five hardware claims are off
by factors from 35 to 5·10¹².

Everything below is reproduced by `./run_all.sh` (pure CPU, no network, ~1 minute).

## 1. What is correct

It is worth stating first, because it is new. The author's earlier preprints
contained arithmetic that did not survive a check. These do.

**The Fano orientation.** SOTP Eq. (3) fixes the octonion structure constants by
listing seven oriented triads. The set of seven lines is forced by the Fano plane,
but the orientations are not: there are 2⁷ = 128 assignments, and `fano.py`
enumerates them. Only **16 of 128** give an algebra that is norm-multiplicative
and alternative. The published orientation is one of the 16. Its multiplication
table satisfies |XY| = |X||Y| to 5·10⁻¹⁶ relative over 4000 random pairs, is
alternative to the same precision, and has no zero divisors. For contrast, writing
the same seven lines with each triad in ascending order — the obvious-looking
choice — gives an algebra that violates norm multiplicativity by up to 60 % and
has explicit zero divisors. The orientation carries the content, and the paper got
it right.

**The tensor-product obstruction.** CQFT §2.1 argues that bilinearity plus
quaternionic scalars forces −(k ⊗ k) = i ⊗ i for c = j, A = i, B = k. With
ji = −k and jk = i, this is exactly right, and it is a fair statement of the
classical difficulty (Adler 1995).

**The materials.** Si₃N₄ is correctly preferred over SOI for the stated reasons
(≈5 eV bandgap, no two-photon absorption, <0.1 dB/cm at 1550 nm). Ce:YIG is the
right magneto-optic garnet, Pt and W the right spin Hall metals, CoFeB on a heavy
metal the right interfacial-DMI stack. The components are real and the choices are
not arbitrary.

This matters for reading what follows: the failures are not ignorance of the
literature. They are failures of the step where the mathematics is attached to the
physics, and that step is the one no coauthor checked.

## 2. The associator vanishes on every gate

SOTP builds its architecture from **Triad Gates arranged according to the Fano
plane graph** (§4.2), and places **Associator Verification Nodes** "at the
intersection of three spin channels", where the associator is "a non-zero hardware
observable that preserves the contextual grouping of past interactions" (§2.2).

Table 1 of SOTP maps e₁, e₂, e₃ to the three spin polarisation components σx, σy,
σz. Together with e₀ these span a quaternion subalgebra of 𝕆, and quaternions are
associative. `associator.py` measures what the node reads:

| support of the three inputs | mean \|[A,B,C]\| | fraction ≠ 0 |
|---|---|---|
| full octonion, e₀…e₇ | 2.26·10¹ | 1.0000 |
| **spin channels only, e₀,e₁,e₂,e₃ — §4.2** | **1.07·10⁻¹⁵** | **0.0000** |
| spin + skyrmion charge, e₀…e₄ | 6.36 | 1.0000 |

Over 20 000 random triples the node reads zero to machine precision. This is not a
property of the spin triple alone. Of the 35 triples of distinct imaginary units,
28 have a non-vanishing associator and **7 vanish — and those 7 are exactly the 7
Fano lines** (verified elementwise in `associator.py`). Every 4-dimensional
subalgebra spanned by e₀ and one Fano line has max |associator| < 10⁻¹⁴.

So the architecture is assembled, gate by gate, out of precisely the seven
configurations in which its central observable is identically zero. To read a
non-zero associator the gate would have to combine basis units that do *not* lie
on a common Fano line — that is, it would have to not be a triad gate.

The associator also carries less information than the paper assumes. It is
trilinear, so |[sA, sB, sC]| = s³|[A,B,C]| exactly (verified to 12 decimal places
for s = 1, 2, 5, 10). As a readout it is dominated by the magnitude of the state,
not by its "grouping history".

## 3. The state space is not closed under the operation

A processor can only compute X ⊠ Y if the result is a state the hardware can hold.
Both papers map algebraic coordinates onto physical variables carrying hard
constraints. `closure.py` draws 200 000 pairs of physically admissible states and
multiplies them.

**SOTP.** Table 1 assigns e₄ to the skyrmion topological charge Q_top, explicitly
"Q = ±1"; e₁,e₂,e₃ to a spin polarisation, |σ| ≤ 1; e₆ to a valley polarisation in
[−1, 1].

| constraint on the product | still satisfied |
|---|---|
| \|σ\| = 1 on (e₁,e₂,e₃) | 0.0000 % |
| Q_top still an integer ±1 | 0.0000 % |
| valley polarisation in [−1,1] | 17.53 % |
| all three at once | **0.0000 %** |

The product's Q_top has mean −0.014 and standard deviation 4.45, ranging over
[−16.6, +16.5]. 82.5 % of products demand a skyrmion with |Q| > 1 and 14.0 % demand
a fractional winding number. A topological charge is an integer *because* it is
topological; it cannot take the value 0.37. The operation the hardware is built to
perform leaves the state space on essentially every input.

**PCTP.** §3 maps q_a to amplitude and carrier phase, q_i and q_j to the Stokes
parameters S₂ and S₃, and q_k to the OAM topological charge l ∈ ℤ.

| constraint on the product | still satisfied |
|---|---|
| OAM charge l still an integer | 0.0000 % |
| \|(S₂,S₃)\| ≤ 1 | 8.82 % |
| amplitude in [0,1] | 10.89 % |
| all three at once | **0.0000 %** |

The degree-of-freedom count fails independently of that. One coherent wavepacket
carries amplitude (1) + carrier phase (1) + a point on the Poincaré sphere (2) +
an integer OAM charge (1, discrete). Equation (6) assigns *both* amplitude and
phase to the single real coordinate q_a, and S₁ is dropped entirely. The map is
not injective, so the quaternion cannot be read back out of the light.

## 4. The causal index does nothing

CQFT Eq. (2) and SOTP Eq. (4) define (X₁,τ₁) ⊠ (X₂,τ₂) = (X₁X₂, τ₁ ≺ τ₂). The
value component is X₁X₂ for every assignment of τ₁ and τ₂; `cqft.py` confirms that
four different assignments give one distinct value. τ records the order in which
the operands were already written, and does not enter any computed quantity.

Every prediction the three papers derive from ⊠ is therefore a prediction of
ordinary quaternion or octonion multiplication — Hamilton 1843, Graves 1843,
Cayley 1845. "Rejecting the fungibility of numerical values" adds a label to the
operand order that the notation already carried. Non-commutativity is likewise not
new to quantum mechanics: the operators of the standard theory are matrices and
have never commuted.

## 5. ⊠ is not a tensor product, and cannot hold an entangled state

The stated purpose of ⊠ is to "resolve the tensor product problem". Its signature
is ℍ × ℍ → ℍ: eight real inputs, four real outputs. A tensor product of two
4-dimensional spaces has dimension 16. The pre-image of any product is a
4-parameter family — `cqft.py` exhibits six different input pairs with the
identical product — so half of the input is destroyed by every application and the
operation is not invertible.

The consequence for §3.2, which reinterprets entanglement, is fatal.
CQFT Eq. (4) writes Ψ_AB = (q_A, τ₀) ⊠ (q_B, τ₀), a single quaternion. In
`cqft.py`, (1) ⊠ (i) and (j) ⊠ (−k) give the same state up to sign. The formalism
has no representation for a correlation between two subsystems, and therefore none
for entanglement, which is the phenomenon the section is about.

## 6. The proposed experiment cannot distinguish anything

CQFT §5 proposes the *Causal Hysteresis Test*: an entangled pair, with photon A
sent through X̂ then Ŷ on one path and Ŷ then X̂ on the other, tuned so A's final
real-axis polarisation matches. "Standard quantum mechanics predicts identical
statistical correlations for Photon B in both scenarios. CQFT predicts a
deterministic, measurable phase shift in Photon B."

Simulated in `cqft.py` on a Bell state with X̂ and Ŷ as rotations of 0.7 and 1.3 rad
about orthogonal axes:

- the two paths give genuinely different joint states, ‖p₁ − p₂‖ = 0.415;
- photon B's reduced density matrix differs by **6.8·10⁻¹⁸** — exactly zero;
- over 20 000 random non-commuting pairs of local unitaries the worst difference
  in ρ_B is 4.6·10⁻¹⁶.

No operation on A, in any order, changes anything measurable on B alone. This is
not an accident of the parameters; it is the no-signalling theorem (Ghirardi,
Rimini & Weber 1980; Eberhard & Ross 1989). A "measurable phase shift in Photon B"
is a signal, and would be faster-than-light communication.

Two further problems. The tuning step is vacuous: for a maximally entangled pair
photon A is completely unpolarised whatever is done to it locally, and the
simulation finds ‖ρ_A¹ − ρ_A²‖ = 0.000000 with no tuning at all. And the
prediction attributed to standard quantum mechanics is wrong — QM predicts that
the *joint* correlators differ, by −0.227 and +0.472 in two of the three
measurement settings tried. So the experiment separates nothing: where a
difference is observable, standard QM predicts one too; where standard QM predicts
none, CQFT's signature is forbidden.

## 7. Hardware claims against their own constants

From `hardware.py`.

| claim | as published | computed | factor |
|---|---|---|---|
| PCTP, "near-zero thermodynamic entropy generation" | ≈ Landauer | one 1550 nm photon alone is 44.6 × kT ln2; 20.7 photons/bit at the shot-noise limit for BER 10⁻⁹ is 925 ×; with a 20 %-efficient source, 4.6·10³ × | **10³–10⁴** |
| PCTP, Faraday isolation | > 35 dB | 19.5 dB measured in its own reference (Bi et al. 2011), on a higher-index platform | **35 × in power** |
| PCTP, NV-centre latch pumped by the 1550 nm evanescent field | works | the guided photon is 0.800 eV, the NV⁻ zero-phonon line is 1.946 eV; diamond is transparent at 1550 nm | **no absorption at all** |
| SOTP, "pure spin currents with J_c = 0", "True Zero" dissipation | zero | Eq. (7) is J_s = (ℏ/2e)·θ_SH·(J_c × σ), so J_c = 0 gives J_s = 0; one SOT event at 5·10¹¹ A/m² dissipates 3.75 fJ in the Pt | **1.3·10⁶ × Landauer** |
| SOTP, chip-scale Fano mesh carried by pure spin current | mm | spin diffusion length 2–3 nm in Pt/W/CoFeB, ≈20 nm in Bi₂Se₃ surface states | **3·10⁵** |
| SOTP §6.1, modulating the chiral condensate ⟨q̄q⟩ | feasible | a 10 GHz spin-wave quantum is 41 µeV against Λ_QCD ≈ 200 MeV | **5·10¹²** |
| SOTP §6.2, flywheel frame-dragging | measurable | 1 kg, 10 cm, 10⁵ rpm gives Ω_LT = 7.8·10⁻²³ rad/s; Gravity Probe B measured 5.7·10⁻¹⁵ rad/s with 4 SQUID gyroscopes at 1.8 K | **7·10⁷ below the smallest ever measured** |

Two of these are internal contradictions rather than magnitude errors. Eq. (7)
refutes the sentence printed above it. And PCTP Table 1 lists the dissipation as
"near-zero (geometric phase)" while §3 specifies electro-optic LiNbO₃ phase
shifters; a geometric phase and an electro-optic modulator are not the same
component. Table 1 also lists latency as "instantaneous optical transit" while §3
defines the causal index τ as the physical longitudinal transit depth — if transit
is instantaneous, τ does not exist.

The SAF claim of "immunity to parasitic magnetic fields up to 10 T" needs
J_ex ≈ 5.6 mJ/m² through the Ru spacer, at the very top of reported Co/Ru
coupling. It is not wrong so much as irrelevant: stray fields inside a packaged
chip are microtesla to millitesla, four to seven orders below the figure quoted.

## 8. The Standard Model claim

SOTP §1 and §6.1 rest on the octonions' "natural isomorphism to the Standard Model
gauge group" and state that "the 8D octonionic algebra naturally projects onto the
Gell-Mann matrices of SU(3)_C". dim 𝕆 = 8 with 7 imaginary units; dim su(3) = 8
generators. These are different objects — an algebra dimension and a Lie algebra
dimension — and the coincidence of the number 8 is not a projection. The actual
relation is that Aut(𝕆) = G₂, of dimension 14, and SU(3) arises as the subgroup
fixing one imaginary unit. Furey (2016), cited as the support, works with the
left-adjoint action of the complexified octonions on itself, not with the eight
coordinates of an octonionic state; nothing in that construction lets a
magnetisation vector modulate a colour field.

The closing promise of 16-dimensional sedenions is self-defeating in the paper's
own terms: it correctly notes that sedenions have zero divisors, which is precisely
the property that makes them useless as a state space for a processor whose
readout is a norm.

## 9. What changed

Across the author's earlier preprints the mathematics itself did not check out.
Here it does — and the two hardware papers name Gemini AI as coauthor for
"Mathematical Synthesis & System Modeling", while the human author is credited
with "Conceptualization & Hardware Architecture". The division of labour is
visible in the result: the algebra is clean and the physical mapping is where every
defect now lives. Delegating the formal layer raised the floor on the equations
and left untouched the step that decides whether a paper is about anything — which
physical quantity is being identified with which symbol, and whether that
identification survives contact with the constraint that a topological charge is
an integer, that diamond does not absorb at 1550 nm, or that a spin current dies
in three nanometres.

That is the same failure mode measured in this author's other work, where the
quantity being optimised turned out to be uncorrelated with the stated goal. The
difference is that it is now harder to see, because the surrounding formalism is
correct.

## 10. Limitations

This evaluation is entirely analytic and numerical. No device was fabricated and
none of the material parameters were measured here; the spin diffusion lengths,
the isolation ratio, the NV level structure and the Gravity Probe B result are
taken from the published literature cited below, and the two preprints' own
figures are used wherever they state one. The closure test in §3 assumes the
constraints the papers themselves write down (Q = ±1, l ∈ ℤ, |σ| ≤ 1); a different
normalisation convention would change the percentages but not the conclusion that
the constraints are not preserved, since quaternion and octonion multiplication do
not preserve integrality of a single coordinate under any scaling. The simulation
in §6 uses qubits rather than full optical modes, which is the standard reduction
for a polarisation-entangled pair and does not affect the no-signalling result,
which holds for any local operation on any Hilbert space.

## 11. Data availability

Scripts, full output (`results.log`) and this text:
<https://github.com/karagos01/causal-trilogy-eval>. The three preprints are open
access under CC BY 4.0 at the DOIs above. Companion evaluations of the same
author's other work: <https://github.com/karagos01/octonion-mppt-eval> and
<https://github.com/karagos01/xternary-eval>.

## References

1. Adler, S. L. *Quaternionic Quantum Mechanics and Quantum Fields.* Oxford University Press (1995).
2. Allen, L., Beijersbergen, M. W., Spreeuw, R. J. C. & Woerdman, J. P. Orbital angular momentum of light and the transformation of Laguerre-Gaussian laser modes. *Phys. Rev. A* **45**, 8185 (1992).
3. Baez, J. C. The octonions. *Bull. Amer. Math. Soc.* **39**, 145–205 (2002).
4. Bi, L. *et al.* On-chip optical isolation in monolithically integrated non-reciprocal optical resonators. *Nature Photonics* **5**, 758–762 (2011).
5. Doherty, M. W. *et al.* The nitrogen-vacancy colour centre in diamond. *Physics Reports* **528**, 1–45 (2013).
6. Eberhard, P. H. & Ross, R. R. Quantum field theory cannot provide faster-than-light communication. *Found. Phys. Lett.* **2**, 127–149 (1989).
7. Everitt, C. W. F. *et al.* Gravity Probe B: Final results of a space experiment to test general relativity. *Phys. Rev. Lett.* **106**, 221101 (2011).
8. Fert, A., Reyren, N. & Cros, V. Magnetic skyrmions: advances in physics and potential applications. *Nature Reviews Materials* **2**, 17031 (2017).
9. Furey, C. *Standard Model Physics from an Algebra?* PhD thesis, University of Waterloo (2016). arXiv:1611.09182.
10. Ghirardi, G. C., Rimini, A. & Weber, T. A general argument against superluminal transmission through the quantum mechanical measurement process. *Lettere al Nuovo Cimento* **27**, 293–298 (1980).
11. Landauer, R. Irreversibility and heat generation in the computing process. *IBM J. Res. Dev.* **5**, 183–191 (1961).
12. Manchon, A. *et al.* Current-induced spin-orbit torques in ferromagnetic and antiferromagnetic systems. *Rev. Mod. Phys.* **91**, 035004 (2019).
13. Schmiegelow, C. T. *et al.* Transfer of optical orbital angular momentum to a bound electron. *Nature Communications* **7**, 12998 (2016).

---

*This text is CC BY 4.0. The code is MIT. Neither is endorsed by the author of the
evaluated preprints.*
