#!/usr/bin/env python3
"""Order-of-magnitude checks on the hardware claims of PCTP and SOTP.

Every number below is either taken from the two preprints or from the standard
reference values cited in PAPER.md.  Nothing here needs a GPU or a lab; the point
is that the claims can be checked against the constants they are made of.
"""
import numpy as np

kB   = 1.380649e-23
hbar = 1.054571817e-34
h    = 6.62607015e-34
c    = 299792458.0
e    = 1.602176634e-19
G    = 6.67430e-11
T    = 300.0

def hdr(s): print(f"\n{'='*72}\n{s}\n{'='*72}")

# ---------------------------------------------------------------- PCTP -------
hdr("PCTP: 'near-zero thermodynamic entropy generation' (abstract, Table 1)")
E_land = kB * T * np.log(2)
E_ph   = h * c / 1550e-9
print(f"  Landauer bound at {T:.0f} K            : {E_land:.3e} J  = {E_land/e:.4f} eV/bit")
print(f"  one photon at 1550 nm                : {E_ph:.3e} J  = {E_ph/e:.4f} eV")
print(f"  -> a single photon already costs      : {E_ph/E_land:.1f} x the Landauer bound")
n_sql = -np.log(1e-9)                    # standard quantum limit, BER 1e-9, OOK
E_op  = n_sql * E_ph
print(f"  photons needed per bit at BER 1e-9   : {n_sql:.1f} (shot-noise limit)")
print(f"  -> energy per detected bit            : {E_op:.3e} J = {E_op/E_land:.0f} x Landauer")
for eta, lbl in ((0.20, "1550 nm DFB laser, 20 % wall-plug"), (0.05, "at 5 %")):
    print(f"  -> including the source, {lbl:34s}: {E_op/eta/E_land:.3e} x Landauer")
loss = 0.1                               # dB/cm, the paper's own Si3N4 figure
for L in (1, 10, 30):
    print(f"  Si3N4 at {loss} dB/cm over {L:2d} cm of mesh: "
          f"{100*10**(-loss*L/10):.1f} % of the light survives")
print("  the paper also specifies electro-optic LiNbO3 phase shifters (Sec. 3),")
print("  which dissipate, while Table 1 lists the loss as 'near-zero (geometric")
print("  phase)'.  Geometric phase and an electro-optic modulator are not the")
print("  same component.")

hdr("PCTP: the isolator")
print("  claimed in Sec. 4.2      : > 35 dB isolation, Ce:YIG / BIG on Si3N4, B0 = 0.1 T")
print("  measured in its own ref. : 19.5 dB (Bi et al., Nat. Photonics 5, 758 (2011),")
print("                             Ce:YIG bonded to a Si ring, 1550 nm)")
print(f"  -> 15.5 dB beyond the cited demonstration, i.e. {10**((35-19.5)/10):.0f}x more")
print(f"     rejection, on a different waveguide platform (Si3N4 has a lower index")
print(f"     contrast with the garnet than Si, which reduces the Faraday overlap)")

hdr("PCTP: the NV-centre 'causal memory latch' (Sec. 4.3)")
E_wg  = h * c / 1550e-9 / e
E_zpl = h * c / 637e-9 / e
E_pmp = h * c / 532e-9 / e
D_gs  = h * 2.87e9 / e
print(f"  waveguide photon, 1550 nm            : {E_wg:.3f} eV")
print(f"  NV- zero-phonon line, 637 nm         : {E_zpl:.3f} eV")
print(f"  NV- standard optical pumping, 532 nm : {E_pmp:.3f} eV")
print(f"  -> the guided photon is short of the ZPL by a factor {E_zpl/E_wg:.2f};")
print(f"     diamond is transparent at 1550 nm, so the evanescent field of the")
print(f"     Si3N4 waveguide cannot drive the 3A2 -> 3E transition at all.")
print(f"  NV- ground-state splitting (2.87 GHz): {D_gs*1e6:.2f} ueV -> addressed with")
print(f"     microwaves, {E_wg/D_gs:.0f}x below the optical photon the paper uses.")

# ---------------------------------------------------------------- SOTP -------
hdr("SOTP: Eq. (7) versus the sentence above it")
print("  text  : 'propagation mediated exclusively by pure spin currents (Js)")
print("           without net charge displacement (Jc = 0)'")
print("  Eq.(7): Js = (hbar / 2e) * theta_SH * (Jc x sigma)")
print("  -> setting Jc = 0 in the paper's own equation gives Js = 0.  The spin Hall")
print("     effect converts a charge current into a spin current; it does not")
print("     produce one from nothing, and the I^2 R loss is in the Pt/W layer that")
print("     carries Jc.  'True Zero' dissipation (Table 2) is the claim that the")
print("     drive current is free.")
rho  = 30e-8          # Pt resistivity at RT, ohm m
J    = 5e11           # A/m^2, typical SOT switching density for Pt/CoFeB
vol  = 100e-9 * 100e-9 * 5e-9
tau_p = 1e-9
E_sw = rho * J**2 * vol * tau_p
print(f"\n  one SOT switching event, Pt 5 nm, 100x100 nm, J = {J:.0e} A/m^2, 1 ns:")
print(f"    dissipated energy                  : {E_sw:.3e} J = {E_sw/1e-15:.2f} fJ")
print(f"    -> {E_sw/E_land:.3e} x the Landauer bound, against 'True Zero'")

hdr("SOTP: how far a pure spin current actually travels")
for mat, lam in (("Pt (300 K)", 3.0e-9), ("W (300 K)", 2.0e-9), ("CoFeB", 2.0e-9),
                 ("Bi2Se3 surface", 20e-9), ("Cu (300 K)", 350e-9)):
    print(f"  spin diffusion length, {mat:16s}: {lam*1e9:7.1f} nm")
mesh = 1e-3
print(f"  a chip-scale Fano mesh                    : {mesh*1e3:7.1f} mm = {mesh*1e9:.0f} nm")
print(f"  -> the routing distance exceeds the spin diffusion length by ~{mesh/3e-9:.0e},")
print(f"     i.e. attenuation exp(-L/lambda) = exp(-{mesh/3e-9:.0e}). Nothing arrives.")

hdr("SOTP: 'immunity to parasitic magnetic fields up to 10 T' (Sec. 4.3)")
Ms, t = 1.4e6, 0.8e-9
for Jex in (0.5e-3, 1e-3, 2e-3, 6e-3):
    Bsf = 2*Jex/(Ms*t)          # J/m^2 / (A/m * m) = T
    print(f"  Ru RKKY coupling {Jex*1e3:4.1f} mJ/m^2, Co {t*1e9:.1f} nm: spin-flop field "
          f"{Bsf:6.2f} T")
print(f"  -> 10 T needs J_ex = {10*Ms*t/2*1e3:.1f} mJ/m^2, at the very top of the")
print("     strongest Co/Ru coupling ever reported.  More to the point:")
print("  stray fields inside a packaged chip are of order uT to mT, so a 10 T")
print("  immunity figure is 4-7 orders above anything the device would meet.")
print("  It is not a specification, it is decoration.")

hdr("SOTP Sec. 6.1: octonions, SU(3) and the chiral condensate")
print("  dim O = 8, of which 7 imaginary units; dim su(3) = 8 generators.")
print("  these are different objects: Aut(O) = G2 (dim 14), and SU(3) appears as")
print("  the subgroup of G2 fixing one imaginary unit.  The 8 coordinates of an")
print("  octonion do not 'project onto the Gell-Mann matrices'; the matching")
print("  count of 8 is a coincidence between an algebra dimension and a Lie")
print("  algebra dimension.  Furey (ref. [3]) works with the left-adjoint action")
print("  of the complexified octonions, not with the 8 coordinates.")
E_qcd = 200e6          # eV, Lambda_QCD
E_sw_q = h * 10e9 / e  # a 10 GHz spin wave quantum
print(f"\n  QCD scale Lambda_QCD                 : {E_qcd:.3e} eV")
print(f"  one 10 GHz spin-wave quantum         : {E_sw_q:.3e} eV = {E_sw_q*1e6:.2f} ueV")
print(f"  -> the excitation the SOTP can create is {E_qcd/E_sw_q:.2e} x too small to")
print(f"     touch the chiral condensate or nucleon deconfinement.")

hdr("SOTP Sec. 6.2: '3D flywheel gravitational deformers'")
m, r, rpm = 1.0, 0.10, 100000.0
I = 0.5*m*r**2
om = rpm*2*np.pi/60
J_ang = I*om
Om_LT = 2*G*J_ang/(c**2 * r**3)
GPB = 37.2e-3/3600/180*np.pi/(365.25*86400)   # Gravity Probe B frame dragging, rad/s
print(f"  flywheel: {m:.0f} kg, r = {r*100:.0f} cm, {rpm:.0f} rpm -> J = {J_ang:.1f} kg m^2/s")
print(f"  (rim speed {om*r:.0f} m/s, already above the strength limit of any alloy)")
print(f"  Lense-Thirring rate at the rim       : {Om_LT:.3e} rad/s")
print(f"  frame dragging measured by Gravity Probe B: {GPB:.3e} rad/s (19 % error)")
print(f"  -> the flywheel is {GPB/Om_LT:.2e} x below the smallest frame-dragging")
print(f"     effect ever measured, and that one needed a satellite and 4 SQUID")
print(f"     gyroscopes at 1.8 K.")
