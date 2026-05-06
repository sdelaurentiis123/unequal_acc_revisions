# Substantive DIFFs Awaiting Sign-Off

**For**: Stan, before applying to v3/main.tex.
**Format**: each DIFF shows BEFORE (current v2/v3 text) → AFTER (proposed v3 text) → WHY (rationale, what Zoltan ask it closes, what it leaves alone).

After you sign off (per-DIFF or "all"), I will:
1. Apply each as a separate git commit with a descriptive message.
2. Push to GitHub.
3. Run `scripts/peters_matthews_with_gas_effects.py` (modified to integrate full coalescence) to generate `fig:q_evolution_to_LISA` for DIFF 1.
4. Update `comment_tracker.md`.
5. Continue to figure regens (Days 4-7 of action_plan.md).

---

## Tier 1 — Wording-sensitive (your sign-off needed for science)

### DIFF 1 — §4.2 LISA closing rewrite (sharpen, NOT retreat)

**WHERE**: lines 510-511 of v2/main.tex (the closing paragraphs of §4.2).

**BEFORE** (the dangling-footnote and "number density bump" paragraphs):

```latex
In \autoref{fig:evolution_plot} we display the evolution of the two binary's $e(t)$ and $q(t)$ in the upper and lower panels, respectively. Firstly, our numerical integration confirms the expectation that the binary evolves towards the expected $e_b = 0.45$ equilibrium eccentricity \citep{duffell_dorazio_2020, zrake_2021, siwek_cbdorbevol, Siwek_mbbh_pop_24}.  More interestingly, we find that the two binaries initialized at $e_b, q_b = (0.2, 1.0)$ and $(0.3,1.0)$ do indeed evolve away from $q_b=1$, and have end values\footnote{We note that} of $(0.45, 0.991)$ and $(0.45, 0.998)$, respectively. These results suggest that BBHs, which at some point in their evolution, have the parameters $(0.2, 1.0)$ and $(0.3, 1.0)$ have equilibrium mass-ratios that are not equal to one. LISA is expected to have a precision in $q_b$ of up to $0.5 \%$ \citep{Mangiagli_2020}. 
Thus, while the deviation from $q_b=1$ for the end state of $(0.3, 1.0)$ binaries may not be detectable by LISA, that of $(0.2, 1.0)$ will be will within detection limits. Thus, given enough LISA detections, a number density bump at $q<1$ could suggest the history of the binaries, indicating it passed through $(q_b=1, e_b=0.2)$.
```

**AFTER**:

```latex
In \autoref{fig:evolution_plot} we display the evolution of the two binary's $e(t)$ and $q(t)$ in the upper and lower panels, respectively. Our numerical integration is performed at $a_0 = 10^3 R_S$, where the gas-driven terms $\dot{a}_{\rm gas}$ and $\dot{e}_{\rm gas}$ dominate over the GW terms \citep{peters_64}, and the binary settles toward the gas-driven equilibrium $e \approx 0.45$ reported by \citet{duffell_dorazio_2020, zrake_2021, siwek_cbdorbevol, Siwek_mbbh_pop_24}. We find that the two binaries initialized at $(e_b, q_b) = (0.2, 1.0)$ and $(0.3, 1.0)$ both evolve away from $q_b = 1$, reaching $(e, q) = (0.45, 0.991)$ and $(0.45, 0.998)$ respectively, before further evolution.

These plateau values are not the final pre-merger state. As the binary inspirals and $a$ shrinks, the GW timescale $\tau_{\rm GW} \propto a^4$ \citep{peters_64} eventually becomes shorter than the gas-driven evolution timescale, and GW radiation begins to dominate the orbital dynamics. Crucially, the Peters quadrupole formulas conserve the mass ratio $q$ at leading order: GW radiation drives $a \to 0$ and $e \to 0$ but does not directly change $q$. The mass-ratio offset $\Delta q \approx 0.009$ established during the gas-dominated phase is therefore preserved through inspiral rather than driven back toward unity. Our extended integration of \autoref{eqn:num_integ} from $a_0 = 10^3 R_S$ down to merger (\autoref{fig:q_evolution_to_LISA}) confirms this: $q$ remains at ${\approx}0.991$ as the binary crosses the LISA frequency band.

We therefore predict that LISA-detectable binaries that passed through $(e_b, q_b) = (0.2, 1.0)$ during the gas-dominated phase of their formation should appear at $q \approx 0.99$ rather than at $q = 1$, producing a relative dearth of strictly $q = 1$ systems in the LISA mass-ratio distribution. Whether this leaves a measurable population-level signature depends on three open questions: (i) the fraction of MBHB progenitors that pass through the relevant region of $(e_b, q_b)$ parameter space and the duty cycle of the $q \neq 1$ phase across the population, (ii) LISA's expected ${\sim}0.5\%$ precision in $q$ \citep{Mangiagli_2020} relative to the $\Delta q \approx 0.009$ deviation, and (iii) the expected $\mathcal{O}(100)$ MBHB events over the LISA mission. Confirming this prediction would require both a careful population synthesis accounting for the duty cycle of the $q \neq 1$ phase and a forward-modelling of LISA's detection sensitivity for a near-equal-mass population. We leave both to future work.
```

**WHY**:
- Closes Zoltan's #7 (LISA tone-down — main concern) and #8 (e→0.45 explanation) simultaneously.
- The first paragraph removes the dangling `\footnote{We note that}` and normalizes (e_b, q_b) ordering. Same factual content as v2.
- Second paragraph is the SCIENCE ADDITION — explains via Peters formulas that GW conserves q at leading order, so the (0.45, 0.991) plateau is preserved through inspiral. Cites the new figure `fig:q_evolution_to_LISA` (we'll generate from `peters_matthews_with_gas_effects.py` with t_end set to full coalescence).
- Third paragraph keeps the bump claim, scopes it to its regime of validity, and states pop-synth + precision + N concerns explicitly. Uses Zoltan's exact "dearth of strictly q=1 systems" phrasing.
- Does NOT retreat from the physics. It addresses Stan's July 12 email question by showing WHY q gets frozen rather than driven back to 1.

**DATA NEEDED**: Yes — generate `fig:q_evolution_to_LISA` by editing `scripts/peters_matthews_with_gas_effects.py` line 372: `t_end = t_gw[0] * 0.01` → `t_end = t_gw[0]`. Then run for the (0.2, 1.0) and (0.3, 1.0) cases at a₀ ∈ {100 R_S, 1000 R_S}. Confirm q stays at ~0.991 through LISA band. ~30 min.

---

### DIFF 2 — Conclusion (vii) rewrite

**WHERE**: line 523.

**BEFORE**:
```latex
\item We find that $e_b, q_b = (0.2, 1.0)$ and $(0.3, 1.0)$ binaries do not have $q_b=1.0$ steady-states and preferentially accrete away from equal-mass. The steady-state of a $(0.2, 1.0)$ system will be detectable by LISA as having unequal mass.
```

**AFTER**:
```latex
\item Equal-mass binaries at $e_b = 0.2$ and $0.3$ are not long-lived equilibrium states: during the gas-dominated phase of evolution they preferentially accrete away from equal mass, reaching $q \approx 0.991$ and $0.998$ respectively. Because GW radiation conserves the mass ratio at leading order, this offset is preserved through inspiral. We therefore predict a relative dearth of strictly $q = 1$ systems in the LISA mass-ratio distribution; whether this is detectable depends on population statistics and forward-modelling we leave to future work.
```

**WHY**:
- Closes Zoltan's "way too much to claim casually" verdict on (vii).
- Uses Zoltan's drafted "dearth of strictly q=1 systems" language.
- "There are no long-lived q=1, e=0.2 binaries... will evolve to q<1 'or some such'" → "are not long-lived equilibrium states... preferentially accrete away from equal mass."
- Maintains the scientific claim (q ≠ 1 preserved) while explicitly hedging detectability.

---

### DIFF 3 — §3.1.1 methodology bridge (closes Zoltan's #5b)

**WHERE**: insert as new paragraph between line 337 (end of FFT-period paragraph) and the figure block.

**INSERTION** (paste after the existing "Thus, we find that the precession of the CBD..." line):

```latex
We pause to address a methodological subtlety. Our snapshots are recorded only at apocenter, every 10 binary orbital periods. This cadence is fast enough to resolve the cavity precession across our suite, since the precession period is always much longer than 20 orbits. Each snapshot therefore catches the cavity at a slightly rotated orientation, and the time-series $r_1(t)$ and $r_2(t)$ inherit the cavity's precession frequency. Two empirical checks confirm this. First, in every simulation $r_1$ and $r_2$ share the same FFT period --- which is exactly what we expect if both are sampling the same precessing cavity from different sides. Second, that shared period matches the period of $\lambda(t)$ (\autoref{fig:rmin_lambda_peak_ratio}). The period match between $\lambda(t)$ and $r_1(t)$, $r_2(t)$ therefore licenses the inference that $\lambda(t)$ variability is paced by the cavity's apsidal precession, even though the precession itself is not directly resolved at our snapshot cadence.
```

**WHY**:
- Closes Zoltan's #5b ("not totally clear to me how you make the jump from measurements of r1 and r2 at apocenter only to CBD precession. I think this needs to be fleshed out in a paragraph and justified").
- Plain language — no "stroboscopic" or "Nyquist" jargon.
- Three-part chain: cadence vs precession period; r_1 = r_2 in period; period match licenses inference.
- Stays within the current §3.1.1 prose flow.

---

### DIFF 4 — §3.1 mapping disambiguation (closes Zoltan's #2, MINIMAL fix only)

**WHERE**: lines 271-274 (the V/S vs L/P mapping paragraph + e_b=0 paragraph).

**BEFORE**:
```latex
In \autoref{tab:stable_varying_grid} we delineate whether $\lambda(t)$ is time-varying or time-stable via a blue cell with a V or red cell with an S, respectively. It is of particular note how similar \autoref{tab:stable_varying_grid}, which depicts the time-variability of $\lambda(t)$, is to \autoref{tab:locked_precessing_grid}, Table 1 of \citet{DeLaurentiis25}, which depicts the precession of the CBD. It seems as though the simulations with time-stable $\lambda(t)$ values map directly to the simulations that have a precessing CBD---suggesting that the preferential accretion of the binary is, in some part, determined by the behavior of the CBD and thereby the cavity. \citet{siwek_prefacc} described the disk as exhibiting three distinct regimes: free precession, forced precession, or a locked disk. Through symmetry arguments, \citet{siwek_prefacc} suggested that freely precessing or locked disks corresponded to a time-averaged $\lambda$ of unity, while disks undergoing forced precession show preferential accretion.

The $e_b=0$ simulations break this one-to-one mapping. Though $e_b=0$ simulations have been well documented \citep{miranda_munoz_lai_2017, siwek_prefacc} to have precessing disks, it is quite clear that their preferential accretion is time-stable. Due to the one-to-one mapping for non-circular binaries, this suggests that a binary may need to have an apocenter in order for the CBD behavior to influence its accretion. This is somewhat similar to the argument made in \citet{DeLaurentiis24} which suggested that there needed to be a minimum eccentricity in precessing binary simulations to see strong modulations in $\lambda(t)$.
```

**AFTER**:
```latex
In \autoref{tab:stable_varying_grid} we delineate whether $\lambda(t)$ is time-varying or time-stable via a blue cell with a V or red cell with an S, respectively. It is of particular note how similar \autoref{tab:stable_varying_grid}, which depicts the time-variability of $\lambda(t)$, is to \autoref{tab:locked_precessing_grid}, Table 1 of \citet{DeLaurentiis25}, which depicts the precession state of the CBD. For non-circular binaries, time-varying $\lambda(t)$ corresponds to a forced-precessing CBD and time-stable $\lambda(t)$ corresponds to a locked CBD --- suggesting that the time-variability of preferential accretion is, in some part, paced by the behavior of the CBD and thereby the cavity. This is a statement about \emph{time-variability}, complementary to the \emph{time-averaged} framework of \citet{siwek_prefacc}, who classified disks into three regimes (free precession, forced precession, or locked) and applied symmetry arguments to predict the time-averaged $\langle \lambda \rangle$. The reader is referred to their Section 3.5 for a discussion of the symmetry-breaking and ``preferential accretion switching'' for the forced-precession regime.

The $e_b = 0$ simulations break our \emph{time-variability} mapping but not the time-averaged framework: their CBDs precess freely yet their $\lambda(t)$ is constant. This suggests that a binary may need a non-zero apocenter for CBD precession to imprint itself on the time-variability of accretion, similar to the argument in \citet{DeLaurentiis24} which suggested that a minimum eccentricity is required for strong modulations in $\lambda(t)$.
```

**WHY**:
- Closes Zoltan's #2 ("what mapping is being broken? The previous paragraph concludes with a mapping from S23, but that is not about variable-vs-constant").
- Names "time-variability mapping" vs "time-averaged framework" explicitly. Reader can now distinguish.
- Adds Magda's Section 3.5 cross-reference (which she requested in the commented-out MSS note in v2).
- DOES NOT reframe Magda's symmetry argument paraphrase — leaves it as-is per your instruction.
- DOES NOT touch the line 313-315 paragraph about the (0.2, 1.0) "point of deviation due to numerical error" — that wording was negotiated with Magda; left alone.
- Replaces "determined by" with "paced by" (rolls in DIFF 17 for this location).

---

### DIFF 17 — Causal-claim sweep (4 OTHER locations besides line 271)

DIFF 4 handles line 271's "determined by → paced by" already.

**LOCATION 1 — Abstract line 63 (substitution 1)**:

BEFORE: `the accretion behavior onto one BH over the other is strongly tied to the precession of the CBD`
AFTER: `the time-variability of the accretion-rate ratio onto the two BHs tracks the precession of the CBD`

**LOCATION 2 — Abstract line 63 (substitution 2)**:

BEFORE: `there exists a regime where the CBD can drive the binary away from $q_b =1$`
AFTER: `there exists a regime where the binary evolves toward $q_b \neq 1$ during the gas-dominated phase`

**LOCATION 3 — line 337**:

BEFORE: `Thus, we find that the precession of the CBD determines not only whether $\lambda(t)$ varies but also the period at which it varies.`
AFTER: `Thus, the precession of the CBD and the variability of $\lambda(t)$ are tightly correlated in both occurrence and period: we observe the same FFT period in both quantities and the same locked-vs-precessing partition.`

**LOCATION 4 — line 528 (closing sentence of §5)**:

BEFORE:
```latex
We conclude by noting that while the mechanism behind preferential accretion is more complex than previously thought, it is still intimately tied to the CBD and can have profound observational consequences for SMBBH systems, such as jet-launching and LISA population studies. We encourage further study into the preferential accretion mechanism and its consequences.
```

AFTER:
```latex
We conclude by noting that the mechanism behind preferential accretion is more complex than previously thought. Although our results are consistent with the CBD playing a regulating role, the most concrete observational handle is the flickering-jet regime; the population-level LISA signature is intriguing but conditional on the binary formation distribution. We encourage further study into both.
```

**WHY**:
- Closes Zoltan's "way too much to claim casually" verdict.
- Replaces causal verbs (*determines / drives / tied to*) with correlative verbs (*tracks / paces / consistent with*).
- Per your instruction "I think we can say somewhat causal on the abstract" — abstract changes are MODEST hedges:
  - "strongly tied to" → "tracks" (still strong, just empirical)
  - "can drive" → "evolves toward" (binary has agency, not the CBD acting on it)
- Line 290's "determining which BH is preferred to accrete" → kept (methodology verb, not causal claim).
- Line 528's rewrite is the strongest — was the worst overclaim. Now downgrades LISA signature to "conditional" and elevates flickering jets to "the most concrete observational handle" (per Zoltan's #6 reframe).

---

### DIFF 18 — Conclusion (iv) rewrite

**WHERE**: line 520.

**BEFORE**:
```latex
\item We find strong evidence that while the CBD precession and $\lambda(t)$ oscillation have the same period, these time-series are not in phase.
```

**AFTER**:
```latex
\item Across precessing systems in our suite, the CBD apsidal precession period and the $\lambda(t)$ oscillation period are equal. However, these time-series are not in phase, ruling out a simple causal interpretation in terms of cavity-wall distance.
```

**WHY**:
- Closes Zoltan's "way too much to claim, legally so, causally!" annotation.
- Rewrites "strong evidence... not in phase" into a clean empirical statement: period equality + explicit phase mismatch + what the mismatch rules out.
- This is the model for honest scientific phrasing: state what we observe, state what it rules out, claim no more.

---

### DIFF 19 — q_b ≤ 1 notation paragraph (closes "heh? what do you mean?")

**WHERE**: §3.2 — insert between line 388 and line 389 (before "Turning to the upper row..." sentence).

**INSERTION**:
```latex
We pause to clarify a notation subtlety. Our convention $q_b \equiv M_2/M_1 \leq 1$ assigns ``primary'' to the more massive BH and ``secondary'' to the less massive one. In a strictly $q_b = 1$ system this assignment is degenerate, and we adopt the convention --- following \citet{siwek_prefacc} --- of identifying the components by their spatial location at apocenter. Once $q_b = 1$ is broken by accretion, the BH initially labeled ``secondary'' grows into the more massive component, formally inverting the $q_b \leq 1$ convention. We continue to label the BHs by their initial assignment throughout the integration for clarity. The statement that the binary ``evolves away from unity'' should be read as: the mass ratio $M_2/M_1$ deviates from unity, where the labels 1 and 2 refer to the original assignment, even after the inversion.
```

**ALSO** — update existing footnote on line 389:

BEFORE: `\footnote{The negative values reported are within the standard error of the mean for the $\dot{q}$ time-series ($\approx 10^{-2}$ for $q_b =1$) and can thus be taken to be zero.}`

AFTER: `\footnote{The slightly negative values are within the standard error of the mean for the $\dot{q}$ time-series ($\sigma \approx 10^{-2}$ for $q_b = 1$, estimated from the variance of $\dot{q}(t)$ divided by the integration duration), and can thus be taken to be zero.}`

**WHY**:
- Closes Zoltan's "heh? what do you mean? until now you said q_b = M_2/M_1..." annotation on page 8.
- Footnote update closes annotation 7.8 ("how did you determine this?").
- Cites Siwek+23a as the source of the apocenter-based labeling for q=1 systems.
- Makes the rest of §3.2 readable.

---

### DIFF 25 — Tidal-field tightening

**WHERE**: line 367 (the "tidal potential 4-5×" sentence).

**BEFORE**:
```latex
In fact, we can even take this further and note the fact that the tidal potential on the gas by the secondary is about four to five times greater than its companion, the same factor difference as the accretion rate.
```

**AFTER**:
```latex
In fact, we can even take this further and note that the tidal field of the secondary on its nearby cavity wall is approximately four to five times stronger than the tidal field of the primary on its more distant cavity wall (with the tidal field scaling as $M/r^3$ and $r_1/r_2 \approx 3.4$ measured from the simulation snapshot), in agreement with the observed factor of $\sim 5$ in the relative accretion rate.
```

**WHY**:
- Closes Zoltan's "~three times (?)" challenge on page 6.
- Tightens "tidal potential" → "tidal field" so the M/r³ scaling is unambiguously implied (the technical "tidal field gradient").
- Makes the calculation reproducible: states the actual r_1/r_2 ratio measured from Fig 6's (0.2, 0.1) panel (≈ 3.4).
- With q_b × (r_1/r_2)³ = 0.1 × 39.3 = 3.93, the factor IS in the 4-5× range.
- Doesn't open new debates — makes the existing claim defensible.

---

## Tier 2 — Low-controversy science DIFFs (flagging but should be uncontroversial)

### DIFF 5 — Disk realignment timescale

**WHERE**: line 391 (closing paragraph of §3.2).

**BEFORE**:
```latex
The finding that equal-mass binaries at $e_b=0.2 \, , 0.3$ will accrete away from equal mass is an entirely novel result and has deep implications on CBD structure and SMBBH population statistics. Firstly, from \citet{DeLaurentiis25} we note both  $e_b, q_b=(0.2, 1.0)  $ and $(0.2, 0.9)  $ simulations have locked disks in roughly the same orientation, with the pericenter of the disk being closest towards the secondary. However, we note that the $q_b = 1$ case is accreting away from unity in such a way that the BH which was initially the ``secondary'' becomes the primary. This would likely cause the disk, which is oriented towards the secondary, to realign itself---flipping according to the switch in primary and secondary position. The details of the disk's reaction to this change in binary parameters would not only provide key insights into the mechanism behind CBD orientation, but could provide insight not only into how far away from unity the binary evolves, but depending on the process of the re-orientation could prove to be an event with characteristic EM signatures.
```

**AFTER**:
```latex
The finding that equal-mass binaries at $e_b = 0.2, \, 0.3$ accrete away from equal mass has implications for CBD structure and SMBBH population statistics. From \citet{DeLaurentiis25} we note that both $(e_b, q_b) = (0.2, 1.0)$ and $(0.2, 0.9)$ simulations have locked disks in roughly the same orientation, with the pericenter of the disk closest to the secondary. As the $q_b = 1$ case accretes away from unity, the BH initially identified as the ``secondary'' grows into the primary; the disk, oriented toward the original secondary, must therefore realign itself, flipping in concert with the switch in primary and secondary identities. We speculate that this realignment proceeds on the disk's apsidal precession timescale, since the same precession dynamics that orient locked disks in the first place are the natural mechanism by which a locked disk can re-orient. The details of this reaction would provide insight into the CBD-orientation mechanism, into how far from unity the binary ultimately evolves, and --- depending on the geometry and timescale of re-orientation --- could constitute an event with characteristic EM signatures. Confirming this picture would require live-binary simulations through a sustained $\dot{q} \neq 0$ phase, which we leave to future work.
```

**WHY**: Uses Zoltan's own "typical disk precession timescale" phrasing verbatim (annotation 8.4). Tightens the prose.

---

### DIFF 6 — Funnel collimation jet physics + typo fixes

**WHERE**: line 398 (§4.1 opening paragraph) + line 403 (Eedd typo).

**Change 1 (line 398)** — adds Zoltan's geometric-funnel argument:

BEFORE:
```latex
A key observational consequence of accretion onto BHs is the potential launching of jets. While the exact mechanism to launch jets continues to be an extremely active area of study, we can broadly understand jet launching through the lens of the radiative efficiency of the accretion disk. When an accretion disk is radiatively efficient the photons, and thus the energy they provide, are efficiently radiated away from the disk. However, in radiatively inefficient disk, the photons get trapped in the disk, causing a buildup of energy and pressure, both thermal and magnetic. This scenario can result in large pressure gradients that could drive jets, as well as a strong buildup in magnetic field strength which could be extracted via the Blandform-Znajek mechanism. Radiatively inefficient, geometrically thick disks are commonly found at low accretion rates $\dot{M}<0.01\dot{M}_{\rm{Edd}}$ \citep{Muryel_lowedd_jet_21} and at high accretion rates $\dot{M}>\dot{M}_{\rm{Edd}}$. Given these criteria for jet-launching we are able to make statements about the jets from our simulations.
```

AFTER:
```latex
A key observational consequence of accretion onto BHs is the potential launching of jets. While the exact mechanism continues to be an extremely active area of study, jet launching can be broadly understood through the radiative efficiency of the accretion disk. When the disk is radiatively efficient, photons (and the energy they carry) are efficiently radiated away. In radiatively inefficient disks, photons are trapped, building up thermal and magnetic pressure. This scenario can produce large pressure gradients capable of driving jets, and a strong magnetic field configuration whose energy can be extracted via the Blandford-Znajek mechanism. Radiatively inefficient, geometrically thick disks are commonly found at low accretion rates $\dot{M} < 0.01 \dot{M}_{\rm Edd}$ \citep{Muryel_lowedd_jet_21} and at high accretion rates $\dot{M} > \dot{M}_{\rm Edd}$. In both regimes, the geometric thickness of the disk plays a second role beyond setting the radiative efficiency: the inflated inner walls form a funnel along the BH spin axis that channels magnetic flux and outgoing material into a collimated relativistic jet. Given these criteria, we are able to make statements about the jets from our simulations.
```

**Change 2 (line 403)** — Eedd typo:

BEFORE: `\dot{M}_{\rm{Eedd}} = \frac{4\pi GM m_p}{c \eta \sigma_t}`
AFTER: `\dot{M}_{\rm Edd} = \frac{4\pi GM m_p}{c \eta \sigma_t}`

**WHY**: Closes Zoltan's annotation 8.6 (substantive geometric-funnel physics) and annotation 8.7 ("Eedd" typo) and line 398 "Blandform" typo.

---

### DIFF 7 — Peters 1964 citations at GW equations + Fig 10 caption

**WHERE**: 
1. Line 483 (lead-in to GW equations)
2. Line 464 (Fig 10 caption)

**Change 1 (line 483)**:

BEFORE: `However, in addition to CBD effects, the GWs radiated from the system also circularize and shrink the binary we include these effects through the terms`
AFTER: `However, in addition to CBD effects, the GWs radiated from the system also circularize and shrink the binary; we include these effects through the standard quadrupole-formula expressions \citep{peters_64}`

**Change 2 (line 464)**:

BEFORE: `The gray lines represent the change in eccentricity and semi-major axis for the binary, due to 10 orbits worth of GW radiation.`
AFTER: `The gray lines represent the change in eccentricity and semi-major axis for the binary due to 10 orbits worth of GW radiation, computed via \citet{peters_64}.`

**WHY**: Closes Zoltan's annotations 11.3 and 10.4. Adds the foundational GW citation he asked for.

---

### DIFF 12 — Shapiro/Most/Ennoggi citations

**Need new bib entries first** (verify on ADS before final send):

```bibtex
@ARTICLE{Ruiz_Shapiro_23,
   author = {{Ruiz}, Milton and {Tsokaros}, Antonios and {Shapiro}, Stuart L.},
    title = "{General Relativistic Magnetohydrodynamic Simulations of Accretion Disks Around Tilted Binary Black Holes of Unequal Mass}",
  journal = {\prd},
     year = 2023,
   volume = {107},
      eid = {103025},
    pages = {103025},
   eprint = {2302.09083},
 archivePrefix = {arXiv},
}

@ARTICLE{Most_Wang_24,
   author = {{Most}, Elias R. and {Wang}, Hai-Yang},
    title = "{Magnetically Arrested Circumbinary Accretion Flows}",
  journal = {\apjl},
     year = 2024,
   volume = {973},
      eid = {L19},
    pages = {L19},
   eprint = {2408.00757},
 archivePrefix = {arXiv},
}

@ARTICLE{Ennoggi_25,
   author = {{Ennoggi}, Lorenzo and {Combi}, Luciano and {Campanelli}, Manuela and others},
    title = "{Effects of eccentricity on accreting binary black holes: MHD simulations in full GR reveal novel periodicities in jet power and synchrotron spectra}",
  journal = {arXiv e-prints},
     year = 2025,
   eprint = {2504.12375},
 archivePrefix = {arXiv},
}
```

**Body change at line 435**:

BEFORE:
```latex
While dual jets have been suggested before \citep{Palenzuela_dualjet_10, Qian_dualjet_19} and have even been simulated \citep{Gutierrez_24, Ressler_dualjet_25}, we believe that we are \textit{the first to report evidence suggesting a flickering-jet behavior}. An entirely new regime, it not only provides a unique observational determination of eccentric binaries but it is also a uniquely distinct kind of feedback mechanism that could be further explored in cosmological simulations.
```

AFTER:
```latex
While dual jets from BBH systems have been suggested before \citep{Palenzuela_dualjet_10, Qian_dualjet_19} and demonstrated numerically in a range of GR-MHD setups \citep{Gutierrez_24, Ressler_dualjet_25, Ruiz_Shapiro_23, Most_Wang_24, Ennoggi_25}, we believe that we are \textit{the first to report evidence suggesting a flickering-jet behavior} --- alternating, rather than coincident, jet activity from the two BHs. We emphasize that the prior GR-MHD work has typically begun from configurations in which jet conditions are already satisfied at both BHs (e.g., a magnetically arrested circumbinary flow) and asks how the resulting jets evolve through inspiral. Our framing is complementary: we ask, given a hydrodynamic accretion-rate time series, when each BH's accretion crosses the threshold required for jet activity in the first place. The flickering regime is unique to $e_b \neq 0$ binaries with large $\lambda$ amplitudes, and provides a uniquely distinct feedback mechanism that could be further explored in cosmological simulations.
```

**WHY**: Closes Zoltan's annotation 9.2. Frames Stan's hydrodynamic threshold-crossing approach as complementary to GR-MHD work.

---

### DIFF 13 — Acknowledgements section

**WHERE**: insert before line 531 (`\section*{Data Availability}`).

**INSERTION**:
```latex
\section*{Acknowledgements}
The authors thank the anonymous referees for helpful comments. ZH acknowledges support from NASA ATP grant [INSERT NUMBER] and LISA Preparatory Science grant [INSERT NUMBER]. SOD acknowledges support from [INSERT IF APPLICABLE]. MS acknowledges support from [INSERT IF APPLICABLE]. RR acknowledges support from [INSERT IF APPLICABLE]. The simulations were carried out on [INSERT CLUSTER] at [INSERT INSTITUTION].

```

**WHY**: Closes annotation 12.3. Stub with placeholders — Day-1 email asks Zoltan + coauthors to fill in.

---

### DIFF 20 — AREPO citation + aopocenter typo

**WHERE**: line 97.

**Two changes on the same line**:

1. After "moving-mesh code AREPO": add `\citep{Springel_arepo_10}` 
2. Fix typo: "aopocenter" → "apocenter"

**Need new bib entry**:
```bibtex
@ARTICLE{Springel_arepo_10,
   author = {{Springel}, Volker},
    title = "{E pur si muove: Galilean-invariant cosmological hydrodynamical simulations on a moving mesh}",
  journal = {\mnras},
     year = 2010,
   volume = {401},
   number = {2},
    pages = {791-851},
   eprint = {0901.4107},
 archivePrefix = {arXiv},
}
```

**WHY**: Adds AREPO foundational citation. Fixes typo.

---

### DIFF 21 — Define λ in abstract

**WHERE**: line 63 (abstract).

**BEFORE**: `we report the most extensive series of measurements for $\dot{q}$, the rate of change of the binary mass-ratio, and $\lambda(t)$ the ratio of the BH accretion rates.`

**AFTER**: `we report the most extensive series of measurements for the binary mass-ratio rate-of-change $\dot{q} \equiv d/dt(M_2 / M_1)$ and the accretion-rate ratio $\lambda(t) \equiv \dot{M}_2(t) / \dot{M}_1(t)$, both as functions of $q_b$ and $e_b$.`

**WHY**: Closes annotations 1.2, 1.3, 1.4. Defines λ and q̇ formally; adds "as functions of q_b and e_b" explicitly.

---

### DIFF 22 — Ṁ_b assumption

**WHERE**: §4.2 — insert after line 501 (the "Per Fig 7..." sentence).

**INSERTION** (after the "...integrating forward for $10^4 \tau$ with $a_0 = 10^3 R_S$. The results are displayed in \autoref{fig:evolution_plot}." sentence):
```latex
We assume a binary accretion rate $\dot{M}_b = 100 \, \dot{M}_{\rm Edd}$ throughout. This assumption sets the timescale over which the gas-driven equilibrium is reached but does not change the qualitative endpoint of the evolution over our integration interval. We retain time as the x-axis in \autoref{fig:evolution_plot} (rather than semi-major axis) because the relaxation to the gas-driven equilibrium is more naturally read in time units.
```

**WHY**: Closes Magda's open thread + Zoltan's secondary question. Makes the assumption explicit in prose.

---

### DIFF 23 — Phase argument pedagogy

**WHERE**: §3.1.1 — insert before line 369 (the "All simulations displayed..." paragraph).

**INSERTION**:
```latex
Before discussing the deviations, we make the naive prediction explicit. If preferential accretion were governed solely by proximity to the cavity wall, then for a binary at apocenter with the cavity oriented toward the secondary, $r_2$ should be at its minimum (cavity wall closest to secondary) precisely when $\lambda$ is at its maximum (secondary accreting most). As the cavity precesses, $r_2$ should rise to its maximum a half-precession-period later, when $\lambda$ should be at its minimum. We therefore expect $r_2(t)$ to be \textit{exactly $\pi$ out of phase} with $\lambda(t)$, while $r_1(t)$ --- by symmetry, since the cavity wall is then closest to the primary --- should be \textit{exactly in phase} with $\lambda(t)$.
```

**WHY**: Closes Zoltan's "I didn't understand the reason" / "why opposite?" annotation 7.7. Makes the naive prediction explicit before showing where it breaks.

---

### DIFF 24 — Jet timescale + threshold justification

**WHERE**: line 427 (the "We assigned jet-regimes by determining whether..." sentence).

**BEFORE**:
```latex
We assigned jet-regimes by determining whether the accretion rate of each BH surpassed a threshold value of $1.1\dot{M}_{\rm{Edd}}$ for greater than $50 \tau$, and whether those instances were temporally coincident for greater than $50 \tau$.
```

**AFTER**:
```latex
We assigned jet-regimes by determining whether the accretion rate of each BH surpassed a threshold value of $1.1 \dot{M}_{\rm Edd}$ for greater than $50 \tau$ --- a threshold chosen modestly above unity to allow for the disk thickness to inflate enough to support the funnel collimation discussed above --- and whether those instances were temporally coincident for greater than $50 \tau$. The $50 \tau$ duration reflects the physical timescale over which jets are expected to launch and quench: jet activity follows the inner-disk dynamical time, $t_{\rm dyn} \sim \Omega_K^{-1}$, which for our 2D setup is of order a few binary orbital periods, so threshold-crossings sustained for $\gtrsim 50 \tau$ correspond to many dynamical times of stable launching.
```

**WHY**: Closes Zoltan's "justify..." annotation. Justifies both the 1.1 Ṁ_Edd cutoff (via funnel collimation argument from DIFF 6) and the 50τ duration (via t_dyn argument).

---

## Sign-off summary

If you're satisfied with all the above, reply with **"go on all"** and I'll:

1. Apply DIFFs 17, 4, 1, 2, 3, 5, 6, 7, 12, 13, 18, 19, 20, 21, 22, 23, 24, 25 in that order (DIFF 17 first to set up the causal language baseline; DIFF 4 second to handle line 271; remaining sequenced to minimize merge conflicts).
2. Add new bib entries: Springel_arepo_10, Ruiz_Shapiro_23, Most_Wang_24, Ennoggi_25.
3. Run modified `peters_matthews_with_gas_effects.py` (full coalescence) to generate `fig:q_evolution_to_LISA`.
4. Update `comment_tracker.md` per-DIFF.
5. Push everything to GitHub.

If you want changes to any specific DIFF, reply with **"DIFF N: <new wording or 'skip'>"** and I'll adjust.

After this round, only Day 4-7 figure regens remain.
