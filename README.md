# Causal Field trilogy — independent evaluation

Reproducible evaluation of three preprints deposited on Zenodo on 25 September
2026 by M. Mazgal and Gemini AI:

| | DOI | title |
|---|---|---|
| I | [10.5281/zenodo.22959886](https://doi.org/10.5281/zenodo.22959886) | The Causal Quaternionic Field Theory (CQFT) |
| II | [10.5281/zenodo.22962188](https://doi.org/10.5281/zenodo.22962188) | Photonic Causal Tensor Processor (PCTP) |
| III | [10.5281/zenodo.22962557](https://doi.org/10.5281/zenodo.22962557) | Spintronic Octonionic Tensor Processor (SOTP) |

The write-up is in [`PAPER.md`](PAPER.md), in Czech in [`PAPER.cs.md`](PAPER.cs.md).

**The algebra is correct**, which is a change from this author's earlier work: the
oriented Fano plane in SOTP Eq. (3) is one of only 16 of the 128 possible
orientations of those seven lines that yield a normed division algebra, and the
tensor-product obstruction in CQFT §2.1 is stated accurately. Every defect is in
the step from algebra to hardware, and the central one is that the associator —
which SOTP calls "a non-zero hardware observable" — is identically zero on exactly
the seven triples the Fano-mesh gate array is built from.

## Requirements

```
python3 -m pip install -r requirements.txt   # numpy only
```

No GPU, no network, no model downloads.

## Reproducing the results

```
./run_all.sh          # everything, about a minute on any CPU
```

| Script | What it computes | Time |
|---|---|---|
| `fano.py` | validity of the published Fano orientation; how many of the 128 orientations work | 20 s |
| `associator.py` | what the "Associator Verification Nodes" read; which triples vanish; trilinearity | 10 s |
| `closure.py` | whether the product of two physically admissible states is admissible, SOTP and PCTP | 25 s |
| `cqft.py` | ⊠ as a tensor product; entanglement representability; simulation of the Causal Hysteresis Test | 3 s |
| `hardware.py` | Landauer budget, isolation, NV photon energies, spin diffusion length, QCD scale, frame dragging | 1 s |

Full output of one run: [`results.log`](results.log).

## Key numbers

| what | published | measured / computed |
|---|---|---|
| Fano orientations giving a division algebra | — | 16 of 128; the published one is valid |
| associator at a node on three spin channels | "non-zero hardware observable" | **1.07·10⁻¹⁵, non-zero in 0.0000 % of 20 000 triples** |
| triples of imaginary units with vanishing associator | — | 7 of 35 — exactly the 7 Fano lines the gates are built from |
| SOTP: product of two admissible states is admissible | assumed | **0.0000 %** (Q_top of the product ranges over [−16.6, +16.5]) |
| PCTP: same, for the optical mapping | assumed | **0.0000 %** (OAM charge integer in 0.0000 %) |
| photon B's reduced state changes in the proposed experiment | "measurable phase shift" | **6.8·10⁻¹⁸**, and 4.6·10⁻¹⁶ worst case over 20 000 random pairs |
| PCTP energy per bit vs Landauer | "near-zero" | 925 ×, or 4.6·10³ × including the source |
| PCTP Faraday isolation | > 35 dB | 19.5 dB in its own cited reference |
| NV latch pumped at 1550 nm | works | 0.800 eV against a 1.946 eV zero-phonon line |
| SOTP spin routing distance | chip scale | spin diffusion length 2–3 nm, a factor 3·10⁵ short |
| SOTP chiral condensate modulation | feasible | 41 µeV against Λ_QCD ≈ 200 MeV, a factor 5·10¹² |
| SOTP flywheel frame dragging | measurable | 7·10⁷ below the Gravity Probe B result |

## Companion evaluations

- [`octonion-mppt-eval`](https://github.com/karagos01/octonion-mppt-eval) — the octonion two-layer/associator template and the magnon claims
- [`xternary-eval`](https://github.com/karagos01/xternary-eval) — the 2-bit LLM inference engine
- [`openql-eval`](https://github.com/karagos01/openql-eval) — the openQL / openOL tensor matrix architecture of October 2026
- [`cymatic-eval`](https://github.com/karagos01/cymatic-eval) — the cymatic stomatal stimulation and pulsed light proposal of October 2026
- [`reference-audit`](https://github.com/karagos01/reference-audit) — whether all 69 citations in all 16 deposits say what they are cited for

## Licence

Code (all `*.py` and `run_all.sh`): MIT, see `LICENSE`.
`PAPER.md` and `PAPER.cs.md`: CC BY 4.0.
