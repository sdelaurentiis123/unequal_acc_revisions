# v3 Changes — Side-by-side BEFORE/AFTER

This document walks through every substantive textual change between **v2** (the July 2025 working version) and **v3**. Organized by your numbered review comments + the most important red-ink margin annotations.

For figure regenerations (colors, captions, layouts) see the rendered v3 PDF directly. For tiny housekeeping (typos, section title casing, bib hygiene) see the bottom section.

GitHub: `git@github-personal:sdelaurentiis123/unequal_acc_revisions.git`
Working PDF: `v3_clean.pdf` in this directory.

---

## #1 — Insert Roman-paper figure inline (your: "even if it is a duplication")

**v2**: Roman's Table 1 + Figure 18 sat in the appendix, far from where they're discussed in §3.1.

**v3**: Both moved inline into §3.1, immediately after the table/figure they're being compared to. The appendix is empty and has been deleted entirely.

- **Table 2** (`tab:locked_precessing_grid`) now appears at the end of the V/S-table block in §3.1. Caption: *"Reproduction of Table 1 from \citet{DeLaurentiis25}, in preparation."*
- **Fig 3** (`fig:a_e_cav_heatmap`) now appears next to the σ_λ heatmap in §3.1. Same attribution.

---

## #2 — One-to-one mapping logic (your: "what mapping is being broken?")

**v2 (lines 271–278)**:

> *"It is of particular note how similar Tab 1, which depicts the time-variability of λ(t), is to Tab 2... It seems as though the simulations with time-stable λ(t) values map directly to the simulations that have a precessing CBD---suggesting that the preferential accretion of the binary is, in some part, determined by the behavior of the CBD and thereby the cavity. \citet{siwek_prefacc} described the disk as exhibiting three distinct regimes... Through symmetry arguments, \citet{siwek_prefacc} suggested that freely precessing or locked disks corresponded to a time-averaged λ of unity, while disks undergoing forced precession show preferential accretion.*
>
> *The e_b=0 simulations break this one-to-one mapping. ..."*

**v3**:

> *"...For non-circular binaries, time-varying λ(t) corresponds to a forced-precessing CBD and time-stable λ(t) corresponds to a locked CBD --- suggesting that the time-variability of preferential accretion is, in some part, paced by the behavior of the CBD and thereby the cavity. **This is a statement about time-variability, complementary to the time-averaged framework of \citet{siwek_prefacc}**, who classified disks into three regimes (free precession, forced precession, or locked) and applied symmetry arguments to predict the time-averaged ⟨λ⟩. The reader is referred to **their Section 3.5** for a discussion of the symmetry-breaking and 'preferential accretion switching' for the forced-precession regime.*
>
> *The e_b = 0 simulations break our **time-variability** mapping but not the time-averaged framework: their CBDs precess freely yet their λ(t) is constant. ..."*

**What changed**: explicitly named the two distinct mappings ("time-variability" vs "time-averaged"), added the cross-reference to Magda's Section 3.5 (which she had asked for in a commented-out MSS thread that didn't make it into v2), and reframed the e_b=0 case as a different branch of Magda's framework rather than a "breakdown."

---

## #3 — Diverging colormaps for Figs 4 and 7 (your "red and blue indicating the sign")

Both figures recolored:

- **Fig 5** (`lambda_mean_colormap.pdf`, ⟨λ⟩ heatmap) — diverging *seismic* colormap centered at λ=1. Red cells = preferential to secondary; blue cells = preferential to primary. The 9 of 80 cells with ⟨λ⟩ < 1 are now visually obvious (e.g., q=0.7-0.8, e=0.8 dark blue cells).
- **Fig 9** (`qdot_heatmap_new.pdf`, ⟨q̇⟩ heatmap) — same approach, centered at q̇=0. Most cells red (positive q̇, evolving toward q=1); the q_b=1 row is mostly near zero except (0.2, 1.0) and (0.3, 1.0) which are visibly positive.

Values now displayed in M-dot_b/M_b units (matching the v2 paper text), not the 1e-16 physical units that snuck in during my first regeneration.

---

## #4a — Cartoon of cavity geometry (your: "either snapshot or cartoon")

**v2**: nothing.

**v3**: new TikZ cartoon as Fig 7 (in §3.1.1, right after the r_1, r_2 definitions). Black cavity ellipse; small ✕ marker for COM; primary (blue) and secondary (red) BHs at apocenter for an illustrative q_b ≪ 1 binary; r_1 vector above the binary axis (blue), r_2 below (red); curved gray arrow indicating precession.

---

## #4b — Fourier panels for Fig 6 examples

**Deferred** — see "Things deferred" section. The methodology bridge in DIFF 3 (below) explains the period match qualitatively without the FFT figure.

---

## #5b — Methodology bridge: apocenter snapshots → CBD precession

This is the substantive fix you asked for: how do we go from r_1, r_2 measured only at apocenter to claims about the cavity's precession?

**v2**: missing. (You wrote *"this needs to be fleshed out in a paragraph and justified."*)

**v3**: new paragraph inserted in §3.1.1, just before the Fig 6 figure block:

> *"We pause to address a methodological subtlety. Our snapshots are recorded only at apocenter, every 10 binary orbital periods. This cadence is fast enough to resolve the cavity precession across our suite, since the precession period is always much longer than 20 orbits. Each snapshot therefore catches the cavity at a slightly rotated orientation, and the time-series r_1(t) and r_2(t) inherit the cavity's precession frequency. Two empirical checks confirm this. First, in every simulation r_1 and r_2 share the same FFT period --- which is exactly what we expect if both are sampling the same precessing cavity from different sides. Second, that shared period matches the period of λ(t) (Fig 6). The period match between λ(t) and r_1(t), r_2(t) therefore licenses the inference that λ(t) variability is paced by the cavity's apsidal precession, even though the precession itself is not directly resolved at our snapshot cadence."*

Plain-language argument: cadence vs precession period; r_1 and r_2 share frequency because they sample the same precessing structure; period match licenses the inference. No "stroboscopic" or "Nyquist" jargon.

---

## #6 — Mini Fig 8 panels at varying Ṁ_b

**v2**: nothing.

**Initial v3 attempt**: built a 4-panel figure at Ṁ_b ∈ {0.01, 0.1, 1, 10} Ṁ_Edd. The first two panels were entirely white (sub-Eddington = no jets), making the figure visually wasteful.

**Final v3**: dropped the figure entirely. Replaced with one new sentence in §4.1 (after the Fig 8 discussion):

> *"The qualitative tapestry of regimes therefore shifts continuously with Ṁ_b: at sub-Eddington rates (Ṁ_b ≪ Ṁ_Edd) no jets launch anywhere in (e_b, q_b) space, while at strongly super-Eddington rates (Ṁ_b ≫ Ṁ_Edd) dual jets dominate the parameter space. The fiducial diagram in Fig 8 represents one slice of this continuous family."*

Captures your #6 point ("the entire diagram will become purple at high Ṁ_b") in prose without burning a figure on it. Your #6 was hedged with "if it's not too much" — taking the out.

---

## #7 + #8 — LISA tone-down (your main concern)

Two changes here, plus a new figure to validate the physics.

### Conclusion item (vii) at line 523

**v2**:

> *"\item We find that e_b, q_b = (0.2, 1.0) and (0.3, 1.0) binaries do not have q_b=1.0 steady-states and preferentially accrete away from equal-mass. The steady-state of a (0.2, 1.0) system will be detectable by LISA as having unequal mass."*

**v3**:

> *"\item Equal-mass binaries at e_b = 0.2 and 0.3 are not long-lived equilibrium states: during the gas-dominated phase of evolution they preferentially accrete away from equal mass, reaching q ≈ 0.991 and 0.998 respectively. Because GW radiation conserves the mass ratio at leading order, this offset is preserved through inspiral. We therefore predict a relative dearth of strictly q = 1 systems in the LISA mass-ratio distribution; whether this is detectable depends on population statistics and forward-modelling we leave to future work."*

Used your drafted *"There are no long-lived q=1, e=0.2 binaries... will evolve to q<1 'or some such'"* phrasing and your *"dearth of strictly q=1"* language.

### §4.2 closing block

**v2** (the "end values" paragraph + "number density bump" paragraph):

> *"Firstly, our numerical integration confirms the expectation that the binary evolves towards the expected e_b = 0.45 equilibrium eccentricity... we find that the two binaries initialized at e_b, q_b = (0.2, 1.0) and (0.3,1.0) do indeed evolve away from q_b=1, and have end values† of (0.45, 0.991) and (0.45, 0.998), respectively. These results suggest that BBHs... have equilibrium mass-ratios that are not equal to one. LISA is expected to have a precision in q_b of up to 0.5%. Thus, while the deviation from q_b=1 for the end state of (0.3, 1.0) binaries may not be detectable by LISA, that of (0.2, 1.0) will be will within detection limits. Thus, given enough LISA detections, a number density bump at q<1 could suggest the history of the binaries..."*

> *† footnote was the dangling "We note that"*

**v3** (three paragraphs replacing the above):

> *"In Fig 14 we display the evolution... Our numerical integration is performed at a_0 = 10^3 R_S, where the gas-driven terms ȧ_gas and ė_gas dominate over the GW terms \citep{peters_64}, and the binary settles toward the gas-driven equilibrium e ≈ 0.45 reported by..."*
>
> *"These plateau values are not the final pre-merger state. As the binary inspirals and a shrinks, the GW timescale τ_GW ∝ a^4 eventually becomes shorter than the gas-driven evolution timescale, and GW radiation begins to dominate the orbital dynamics. **Crucially, the Peters quadrupole formulas conserve the mass ratio q at leading order: GW radiation drives a → 0 and e → 0 but does not directly change q.** The mass-ratio offset established during the gas-dominated phase is therefore preserved through inspiral rather than driven back toward unity. We confirm this by extending the integration of Eq. 12 for the (e_b, q_b) = (0.2, 1.0) and (0.3, 1.0) cases (Fig 15). During the gas-dominated phase the binary reaches (e, q) ≈ (0.45, 0.99) for both cases. As GW takes over, e is rapidly circularized to e ≈ 0 but q stays essentially constant. A scan over initial separation finds that the bump effect activates by a_0 ≳ 250 R_S and reaches its asymptotic value by a_0 ≳ 400 R_S; for an M_tot = 10^7 M_sun binary entering inspiral with Ṁ_b = 100 Ṁ_Edd, the asymptotic mass-ratio offsets at LISA-band entry are Δq ≈ 0.014 and Δq ≈ 0.008 for the two cases, respectively."*
>
> *"**Two caveats apply to this prediction.** First, the simulation suite that supplies q̇_gas is gridded at Δq_b = 0.1 resolution. Once q drifts from 1.0 to ~0.99 during inspiral, our integration samples the q_b = 0.9 row of the lookup table, which corresponds to simulations of binaries that had q_b = 0.9 throughout — not binaries that started at q = 1 and drifted. We do not have direct simulation data in q ∈ (0.95, 1.0). Second, the cavity geometry depends on the binary's history: a binary that started at q = 1 has a CBD locked toward the spatially-defined 'secondary' (an apocenter convention), whereas a q_b = 0.9 simulation has a CBD locked toward the lower-mass BH from the start. As q drifts past unity, the cavity must reorient, which we argued in §3.2 proceeds on the disk's apsidal precession timescale — a quantity we have not compared to the gas-driven q-evolution timescale. If the cavity reorients faster than q evolves, the lookup remains applicable; if slower, the relevant q̇_gas during inspiral could differ from what our integration assumes. Resolving these caveats would require new simulations at finer q-grid resolution and live-binary runs through a sustained q̇ ≠ 0 phase, both of which we leave to future work.*
>
> *"Subject to these caveats, we predict that LISA-detectable binaries that passed through (e_b, q_b) = (0.2, 1.0) or (0.3, 1.0) during the gas-dominated phase of their formation should appear at q ≈ 0.99 rather than at q = 1, producing a relative dearth of strictly q = 1 systems in the LISA mass-ratio distribution. **Whether this leaves a measurable population-level signature depends on three open questions:** (i) the fraction of MBHB progenitors that pass through the relevant region of (e_b, q_b) parameter space and the duty cycle of the q ≠ 1 phase across the population, (ii) LISA's expected ~0.5% precision in q relative to the Δq ~ 0.01 deviation, and (iii) the expected O(100) MBHB events over the LISA mission. Confirming this prediction would require both a careful population synthesis accounting for the duty cycle of the q ≠ 1 phase and a forward-modelling of LISA's detection sensitivity for a near-equal-mass population."*

**Why this isn't a retreat**: I keep the prediction. I show via Peters' equations + numerical integration that q is preserved through inspiral. I add two new caveats explicitly (grid resolution + disk reorientation). I name the three open questions (pop synth + precision + N) you raised in your #7 — but as open questions for future work, not concessions of the physics.

### New supporting figure: Fig 15 (`q_evolution_to_LISA.pdf`)

3-panel figure showing (a, e, q) integration from a_0 = 10^3 R_S all the way to merger for both (0.2, 1.0) and (0.3, 1.0) cases. Top: a/R_S vs f_GW. Middle: e vs f_GW (rises to gas equilibrium 0.45, then circularizes to ~0 by LISA-band entry). Bottom: q vs f_GW (drops to 0.985–0.992 plateau and stays flat through LISA band).

Lines are red-solid + blue-dashed (overlapping where they would, distinguishable everywhere).

Generated by `scripts/run_q_evolution_to_LISA.py`. A separate stress test (`scripts/stress_test_q_evolution.py` over 27 (M, a_0, Ṁ_b) cases) confirms the result is robust for a_0 ≳ 400 R_S; a binary search (`scripts/binary_search_a0.py`) finds the threshold at a_0 ≈ 250 R_S.

---

## Item (iv) walkback (your "way too much to claim, legally so, causally")

**v2**:

> *"\item We find strong evidence that while the CBD precession and λ(t) oscillation have the same period, these time-series are not in phase."*

**v3**:

> *"\item Across precessing systems in our suite, the CBD apsidal precession period and the λ(t) oscillation period are equal. However, these time-series are not in phase, ruling out a simple causal interpretation in terms of cavity-wall distance."*

Cleaned the empirical period-match claim, made explicit what the phase mismatch *rules out*, claimed no more.

---

## Causal-claim sweep (paper-wide)

Replaced "determines / drives / regulates / tied to" with "tracks / paces / consistent with" at four locations:

| Location | v2 | v3 |
|---|---|---|
| Abstract | *"the accretion behavior onto one BH over the other is **strongly tied to** the precession of the CBD"* | *"the time-variability of the accretion-rate ratio onto the two BHs **tracks** the precession of the CBD"* |
| Abstract | *"there exists a regime where **the CBD can drive** the binary away from q_b = 1"* | *"there exists a regime where **the binary evolves toward q_b ≠ 1** during the gas-dominated phase"* |
| §3.1.1 | *"the precession of the CBD **determines** not only whether λ(t) varies but also the period at which it varies"* | *"the precession of the CBD and the variability of λ(t) **are tightly correlated** in both occurrence and period: we observe the same FFT period in both quantities and the same locked-vs-precessing partition"* |
| §5 closing | *"...it is still **intimately tied to** the CBD and can have profound observational consequences for SMBBH systems, such as jet-launching and LISA population studies."* | *"...Although our results are **consistent with** the CBD playing a regulating role, the most concrete observational handle is the flickering-jet regime; the population-level LISA signature is intriguing but conditional on the binary formation distribution."* |

The §3.1 line 271 location is rolled into the DIFF 4 paragraph rewrite (above).

---

## q_b ≤ 1 notation paragraph (your "heh? what do you mean?")

**v2**: an inline parenthetical footnote saying *"In the equal-mass case, 'secondary' and 'primary' merely identify the components which at apocenter are in the same spatial quadrant as the secondary and primary of an unequal mass binary."* — easy to miss, didn't address the convention-inversion.

**v3**: explicit paragraph in §3.2:

> *"We pause to clarify a notation subtlety. Our convention q_b ≡ M_2/M_1 ≤ 1 assigns 'primary' to the more massive BH and 'secondary' to the less massive one. In a strictly q_b = 1 system this assignment is degenerate, and we adopt the convention --- following \citet{siwek_prefacc} --- of identifying the components by their spatial location at apocenter. Once q_b = 1 is broken by accretion, the BH initially labeled 'secondary' grows into the more massive component, formally inverting the q_b ≤ 1 convention. We continue to label the BHs by their initial assignment throughout the integration for clarity. The statement that the binary 'evolves away from unity' should be read as: the mass ratio M_2/M_1 deviates from unity, where the labels 1 and 2 refer to the original assignment, even after the inversion."*

Plus updated the σ ≈ 10⁻² footnote (your annotation 7.8): added *"estimated from the variance of q̇(t) divided by the integration duration"* — answers your "how did you determine this?" pointer.

---

## Disk realignment timescale (your annotation 8.4 — your own suggested wording)

**v2**: *"The details of the disk's reaction to this change in binary parameters would not only provide key insights into the mechanism behind CBD orientation, but could provide insight not only into how far away from unity the binary evolves..."*

**v3** (using your "typical disk precession timescale" verbatim):

> *"As the q_b = 1 case accretes away from unity, the BH initially identified as the 'secondary' grows into the primary; the disk, oriented toward the original secondary, must therefore realign itself, flipping in concert with the switch in primary and secondary identities. **We speculate that this realignment proceeds on the disk's apsidal precession timescale**, since the same precession dynamics that orient locked disks in the first place are the natural mechanism by which a locked disk can re-orient. ... Confirming this picture would require live-binary simulations through a sustained q̇ ≠ 0 phase, which we leave to future work."*

---

## Funnel collimation jet physics (your annotation 8.6 — your own physics suggestion)

**v2**: stops at "...could be extracted via the Blandford-Znajek mechanism."

**v3** (added two sentences):

> *"...could be extracted via the Blandford-Znajek mechanism. **In both regimes, the geometric thickness of the disk plays a second role beyond setting the radiative efficiency: the inflated inner walls form a funnel along the BH spin axis that channels magnetic flux and outgoing material into a collimated relativistic jet.** Given these criteria..."*

---

## Tidal-factor sentence (your annotation 6.5 "~3 times?")

**v2**: *"...the tidal potential on the gas by the secondary is about four to five times greater than its companion, the same factor difference as the accretion rate."*

**v3**: *"...the tidal field of the secondary on its nearby cavity wall is approximately four to five times stronger than the tidal field of the primary on its more distant cavity wall (with the tidal field scaling as M/r^3 and r_1/r_2 ≈ 3.4 measured from the simulation snapshot), in agreement with the observed factor of ~5 in the relative accretion rate."*

Same physical claim, but: tightened "tidal potential" → "tidal field" so the M/r³ scaling is unambiguous; added the actual r_1/r_2 ratio measured from Fig 8's (0.2, 0.1) panel; the 4-5× now falls out cleanly from q × (r_1/r_2)^3 = 0.1 × 3.4^3 ≈ 4.

---

## Phase-argument pedagogy (your annotation 7.7 "I didn't understand the reason")

**v3** added a new paragraph in §3.1.1, immediately before the "All simulations displayed..." discussion:

> *"Before discussing the deviations, we make the naive prediction explicit. If preferential accretion were governed solely by proximity to the cavity wall, then for a binary at apocenter with the cavity oriented toward the secondary, r_2 should be at its minimum (cavity wall closest to secondary) precisely when λ is at its maximum (secondary accreting most). As the cavity precesses, r_2 should rise to its maximum a half-precession-period later, when λ should be at its minimum. We therefore expect r_2(t) to be **exactly π out of phase** with λ(t), while r_1(t) --- by symmetry, since the cavity wall is then closest to the primary --- should be **exactly in phase** with λ(t)."*

States the naive prediction explicitly so the reader has a baseline before the deviation discussion.

---

## Jet timescale + threshold justification (your "justify..." annotation, page 8)

**v2**: *"We assigned jet-regimes by determining whether the accretion rate of each BH surpassed a threshold value of 1.1 Ṁ_Edd for greater than 50 τ, and whether those instances were temporally coincident for greater than 50 τ."*

**v3**: *"...a threshold value of 1.1 Ṁ_Edd for greater than 50 τ --- **a threshold chosen modestly above unity to allow for the disk thickness to inflate enough to support the funnel collimation discussed above** --- and whether those instances were temporally coincident for greater than 50 τ. **The 50 τ duration reflects the physical timescale over which jets are expected to launch and quench: jet activity follows the inner-disk dynamical time, t_dyn ~ Ω_K^-1, which for our 2D setup is of order a few binary orbital periods, so threshold-crossings sustained for ≳ 50 τ correspond to many dynamical times of stable launching.**"*

---

## Other citation additions (your annotations)

| Where | What | Why |
|---|---|---|
| §4.2 (line 489) and Fig 13 caption (line 480) | `\citep{peters_64}` | Your annotation 11.3 + 10.4 |
| §2.1 (line 99) | `\citep{Springel_arepo_10}` for AREPO | Your annotation 2.x |
| §4.1 (line 471) | `\citep{Ruiz_Shapiro_23, Most_Wang_24, Ennoggi_25}` for GR-MHD binary jet sims | Your annotation 9.2 (Stu Shapiro / Elias Most) |

The §4.1 dual-jet sentence was rewritten to frame our hydrodynamic threshold-crossing approach as **complementary** to the GR-MHD work (which typically begins from configurations where jet conditions are already satisfied at both BHs).

---

## Author affiliation update (your annotation 1.1 "+ Physics + ISTA")

**v2**:
- Stan: Columbia Astronomy + Cambridge DAMTP
- Zoltan: Cambridge DAMTP only
- Magda: Cambridge DAMTP
- Roman: Columbia Astronomy + IAS

**v3** (per your most recent paper, Bartos & Haiman 2025, arxiv:2508.08558):
- Stan: ¹,⁴ Columbia Astronomy + Cambridge DAMTP
- Zoltan: ¹,²,³ Columbia Astronomy + **Columbia Physics** + **ISTA**
- Magda: ⁴ Cambridge DAMTP
- Roman: ¹,⁵ Columbia Astronomy + IAS

Added: ²Department of Physics, Columbia University, 550 W. 120th Street, New York, NY 10027, USA; ³Institute of Science and Technology Austria (ISTA), Am Campus 1, 3400 Klosterneuburg, Austria.

If you'd prefer ISTA listed first as your primary affiliation (as in the GW231123 paper), tell me and I'll switch the numbering.

---

## Acknowledgements section (your annotation 12.3)

**v3** (new section before Data Availability):

> *"\section*{Acknowledgements}*
> *The authors thank the anonymous referees for helpful comments. ZH acknowledges support from NASA ATP grant **[INSERT NUMBER]** and LISA Preparatory Science grant **[INSERT NUMBER]**. SOD acknowledges support from [INSERT IF APPLICABLE]. MS acknowledges support from [INSERT IF APPLICABLE]. RR acknowledges support from [INSERT IF APPLICABLE]. The simulations were carried out on [INSERT CLUSTER] at [INSERT INSTITUTION]."*

Need from you: the two grant numbers.

---

## Bug fixes (v2 → v3)

| Bug | Fix |
|---|---|
| `\sod{...}` Bondi-Hoyle paragraph wrapper | Removed |
| `\mss{is this still figure 6?}` annotation | Removed; replaced with proper `\autoref{fig:lambda_rmin_panels}` cross-reference |
| Phantom `\citep{Miranda2015, Duffell2024}` (compile errors) | Replaced with `miranda_munoz_lai_2017` and `dorazio_duffel` |
| `\dot{M}_{\rm{Eedd}}` typo (extra 'e') | Fixed → `\dot{M}_{\rm Edd}` |
| "Blandform-Znajek" typo | Fixed → "Blandford-Znajek" |
| "aopocenter" typo | Fixed → "apocenter" |
| Empty `\section{}` after `\appendix` | Entire appendix removed (Roman content moved inline) |
| Dangling `\footnote{We note that}` | Removed (rolled into DIFF 1 prose rewrite) |

## Bibliography hygiene

| Issue | Fix |
|---|---|
| `Shi_2012` and `shi_2012` (same paper, both cited in body) | Body swept to `shi_2012`; duplicate entry deleted |
| `Mangiagli+2020` and `Mangiagli_2020` (same paper, body cites only `_2020`) | Duplicate entry deleted |
| `miranda_munoz_lai_17` and `miranda_munoz_lai_2017` (same paper, both cited in body) | Body swept to `_2017`; duplicate entry deleted |
| `farris_2014` × 3 entries, `farris_2015` × 3 entries, `MacFadyen_08`, `siwek_cbdorbevol`, `siwek_prefacc`, `white_rees_78` duplicates | All deduped to first occurrence (10 dupes total deleted) |
| `DeLaurentiis25` claimed `arXiv:2405.07897` (preprint that doesn't exist) | Changed to `journal = {in preparation}`; arxiv ID stripped |

Final bib: 188 unique entries (was 194).

## Section title casing (your annotations 2.1, 3.1)

11 headings updated to MNRAS sentence case:

`Analytic Tools and Numerical Methods` → `Analytic tools and numerical methods`
`Simulation Setup` → `Simulation setup`
`Disk Theory` → `Disk theory`
`Numerical Techniques` → `Numerical techniques`
`Preferential Accretion` → `Preferential accretion`
`Preliminary Analysis` → `Preliminary analysis`
`Mass Ratio` → `Mass ratio`
`Observational Implications` → `Observational implications`
`Flickering Jets` → `Flickering jets`
`Unequal Mass Sources` → `Unequal mass sources`
`Summary and Conclusions` → `Summary and conclusions`

---

## Caption rewrites for self-containment

Your repeated annotation: *"captions need to be self-contained."* Updated for:

- **Fig 1** (lambda_full): now defines λ explicitly, time in τ_b, "entire" 80-simulation suite.
- **Fig 2** (lambda_std_heatmap): self-contained, defines σ_λ.
- **Fig 4** (mean_lambda_lines): explicit gray-shading description for λ > 1 region.
- **Fig 5** (lambda_mean_heatmap): self-contained, explains diverging colormap.
- **Fig 9** (qdot_heatmap): self-contained, explains diverging colormap, highlights (0.2, 1.0) and (0.3, 1.0) anomalies.
- **Fig 12** (lambda_tilde_map): defines λ̃ explicitly with formula, names it the "accretion-rate gauge."

Fig 6 (rmin_lambda_peak_ratio) and Fig 8 (proof_of_lambda_r_not_causal) caption rewrites — deferred (would need full layout work).

---

## Things deferred (per `comment_tracker.md` Section F)

If any of these are deal-breakers, tell me and I'll do them before submission:

- **Fig 8 axis labels** — your annotations 9.1, 9.3 (most-flagged figure issue, you wrote labels in by hand). Full rewrite of `accretion_eddington.py`. Half-day to full-day task.
- Fig 1 layout (panels touching, larger labels) — annotation 4.1
- Fig 6 panel concatenation — annotation 7.1
- Fig 10 detection-region annotations — annotation 10.1
- Fourier panels for Fig 6 (#4b)
- Citation hunt: Barnes & Hernquist 1992 (annotation 1.6); D'Orazio 2013 in periodogram-of-q context (annotation 1.12)
- Page 1-2 small prose sweeps: 1.5, 1.8, 1.9, 1.10, 1.11; 2.2-2.6
- (e_b, q_b) ordering paper-wide sweep — annotation 3.2 (done in places, not as a sweep)

---

## Open items for you

1. **NASA ATP grant number** — `[INSERT]` placeholder in Acknowledgements.
2. **LISA Preparatory Science grant number** — `[INSERT]` placeholder.
3. **Confirm affiliation order**: ¹Columbia Astronomy ²Columbia Physics ³ISTA — or do you want ISTA listed first as primary?
4. **Email**: currently `zh2007@columbia.edu` — switch to `zoltan.haiman@ista.ac.at`?
5. **Push back on §4.2** if you think the LISA prediction is still overclaiming. The new caveats (grid resolution + disk reorientation) might satisfy you, or you might want me to demote it further.

---

## End

For the final-form view, see `v3_clean.pdf` (14 pages). For full per-comment tracker with commit references, see `comment_tracker.md`.

Cheers,
Stan
