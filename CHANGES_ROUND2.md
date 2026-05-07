# Round-2 Changes Since Your Overleaf Edits

What I changed by section, with science/logic content flagged separately from cosmetic.

## §1 Introduction

**Cosmetic / wording**:
- "Eccentric and unequal mass-ratio binaries too display..." → "...also display...". Missing space before "In order to study". `\citealt{Tiede_22}` → `\citet{Tiede_22}` (it's grammatical not parenthetical).
- "(e.g  \citealt{...})" → "(e.g.\ \citealt{...})" (double space, missing period after e.g).
- Straight quotes → LaTeX quotes on "symmetry breaking" passage. "(see Figure 7 in \citealt{...})" → "of \citealt{...}".
- "two and three dimensional smoothed particle" → "two- and three-dimensional smoothed-particle" (hyphenation). `\citealt` → `\citep` for the `\citep{Gunther_Kley_02, Ochi_05, Young_15}` list.
- "$\leq 100 \tau_b$" double-stated → kept as "$\sim 100$ binary orbital periods ($\tau_b$)".
- Roadmap-paragraph cleanup: removed double space, tightened the "we discuss how our results could suggest" run-on.

**Science (NEW addition flagged)**:
- **Closing paragraph (line 85)**: replaced the "% add 1-2 sentences describing tools" placeholder with a sentence naming the techniques we use: Fourier-based period extraction of $\lambda(t)$, comparison against per-BH Eddington thresholds, and the coupled gas-plus-GW integration of $\dot q$. This was your explicit ask.

## §2 Methods

**Cosmetic**:
- "uses Voronoi tessellations" → "use" (subject-verb).
- "$10,000$" → "$10\,000$" (LaTeX-correct thin space for thousands).
- Added missing $e_b = 0.0$ to the parameter set (was listed only $0.1$–$0.8$).

**Science**:
- None.

## §2.2 Disk theory

**Cosmetic**:
- "viscous damping \citep{Goodchild_2006} act to suppress it" → "viscous damping acts to suppress it \citep{Goodchild_2006}" (subject-verb + better citation placement).

**Science**:
- None.

## §3.1 Preferential accretion (S23 mapping section, pages 384–388)

**Science (rewrite, NOT cosmetic)** — this is the biggest content change:

You flagged the original prose ("complementary to the time-averaged framework of S23") as wrong. After looking up Siwek+2023a directly, I confirmed: **S23 already discusses time-variability** of accretion in forced-precessing CBDs on the precession timescale, invoking symmetry arguments to explain why circular binaries don't show $\lambda(t)$ variability while eccentric forced-precessing ones do. So the old framing — "S23 is time-averaged, we add time-variability" — was incorrect.

I rewrote the paragraph to say: **S23 first established the time-variability + symmetry argument; we extend it systematically to the full $(e_b, q_b)$ grid** by mapping every simulation onto the time-stable / time-varying dichotomy and comparing it directly to the locked / forced-precessing classification.

I also rewrote the **DeLaurentiis24 connection paragraph** (your "% spend 2-3 sentences explaining the setup" comment). After reading their paper, I clarified: **their setup is fundamentally different from ours.** They imposed GR apsidal precession on the binary itself; we hold the binary fixed and let the disk precess. The shared finding — that a non-zero binary eccentricity is required for any precession (binary or disk) to imprint itself on the relative accretion rates — connects the two results as analogues, not duplicates.

## §3.1 Mean-$\lambda$ figure (Fig 5, lambda_mean_colormap)

**Science (figure regen + interpretation change)**:
- You said "if it's below 1 we're not actually saying one BH is preferentially accreting over the other; it's about magnitude." I confirmed by looking at the code (`scripts/regen_fig4_fig7_diverging.py`): $\langle\lambda\rangle$ is the time-average of the median point-wise ratio $\dot M_2/\dot M_1$. For $q_b = 1$ sims, symmetry breaking can produce slight asymmetry either way; the apocenter labeling convention picks the BH that happens to fluctuate slightly less, so $\langle\lambda\rangle \lessgtr 1$ is essentially a coin flip.

- **Switched Fig 5's colormap** from diverging seismic (centered at $\lambda=1$, with red = secondary preferred / blue = primary preferred) to **sequential viridis on $|\log_{10}\langle\lambda\rangle|$** — the magnitude of preferential accretion regardless of direction. In-cell labels still display the actual $\langle\lambda\rangle$ value with a black-stroke outline so they're legible against any cell color.

- **Caption rewritten** to explain the new framing AND why some cells have $\langle\lambda\rangle < 1$: 71 of 80 cells have $\langle\lambda\rangle > 1$ (standard preferential-accretion-onto-secondary). The 9 cells with $\langle\lambda\rangle < 1$ are mostly $q_b = 1$ sims where the apocenter convention can be assigned either way, plus a few unequal-mass dimspots (notably $(e_b, q_b) = (0.5, 0.2)$ at 0.93) that the body text already calls out.

## §3.1.1 Preliminary analysis (r_cav definitions)

**Science (clarification, your %comment)**:
- Added the missing definition: $r_{\rm cav}(\theta)$ is measured from the **binary center of mass**. $r_1, r_2$ are the **shortest distances at the apocenter snapshot only**, NOT literal closest-approach distances over the full orbit. They serve as a proxy for cavity orientation, not a moment-by-moment proximity metric. (Your "where is r_cav measured from? not totally obvious BHs are closest at apocenter — comment?" comment.)

**Cosmetic**:
- Tuple notation cleanup: $(e_b=0.5, q_b=0.7)$ → $(e_b, q_b) = (0.5, 0.7)$ etc. throughout the paragraph.

## §3.2 Mass ratio

**Science**:
- None new (your edits stand).

**Cosmetic**:
- 3000-orbit footnote rewritten cleanly: **discard first $3000\tau_b$ as transient, average over orbits 3000–10\,000 ($N=700$ snapshots at the $10\tau_b$ cadence)**. Your "explain this footnote — N is the answer" comment.

## §4.1 Flickering jets

**Science (your %comment "this 50 tau stuff is not true at all")**:
- I dropped the bogus "$t_{\rm dyn} \sim \Omega_K^{-1}$, many dynamical times" justification. Per your direction, the $50\tau$ duration **stays unchanged**; the new justification is empirical: the duration filters out short-lived threshold excursions while preserving the alternating cadence we want to detect in the flickering regime. The dynamical-time comparison is now mentioned in a single, more honest line as context, not as the central argument.

**Cosmetic**:
- Eq 10: **stray period after `\end{equation}.` removed** (moved inside the equation as `,` or kept inline).
- $\dot M_{\rm Edd}$ defined at first instance: the physical-meaning sentence ("the rate at which radiation pressure on free electrons exactly balances gravity...") is now where the symbol first appears (next to the Muryel+21 cite), not several lines later. The formal definition (Eq.~\ref{eqn:mdot_edd}) remains in the next paragraph and is now cross-referenced.

## §4.2 Unequal-mass sources

**Cosmetic**:
- Function-arg ordering inside the gas/GW rate equations: $(q_b, e_b)$ → $(e_b, q_b)$ throughout (matching the rest of the paper).

**Science**:
- None.

## §5 Conclusions

**Cosmetic**:
- "this system" replaced with "the SMBBH–CBD system" (your %comment).

**Science**:
- None.

## Figures

**Fig 5 (lambda_mean_colormap)** — sequential viridis on $|\log_{10}\langle\lambda\rangle|$ with stroked text labels. **THIS IS A SCIENCE/INTERPRETATION CHANGE.** Caption rewritten to match.

**Fig 6 (lambda_rmin_panels)** — caption now explains $r_i$ explicitly (your %comment).

**Fig 8 (fourier_panels)** — caption now explains $r_i$ explicitly (same fix).

**Fig 10 (timescales)** — caption strengthened: "the black contours enclose the detection-friendly region in each panel" instead of vague "within black lines."

## What I did NOT touch

- Any block where the user's voice was clearly the present version (your Overleaf edits).
- The fundamental scientific claims (LISA bump, jet regimes, period match, etc.) — those stand from your previous round.
- Eq 11 (the align block) — you said it was fine, just the period in Eq 10 was the issue, which I fixed.

---

PDF: 16 pages clean (was 15), 18 pages diff (was 17). The growth is from the §3.1 S23/DeLaurentiis24 rewrite.
