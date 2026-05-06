# Response to Your March 2025 Review — Unequal Accretion Paper v3

**Stan DeLaurentiis** — May 2026

Hi Zoltan,

Attached is v3 of the unequal-accretion paper. This document maps each of your March 2025 comments to where it's addressed. Two PDFs accompany this:

- **`v3_clean.pdf`** — the polished publication-ready PDF.
- **`v3_diff_v2_to_v3.pdf`** — same PDF with `latexdiff` markup: red strikethrough = removed v2 text, blue underline = added v3 text. Read this one if you want to see exactly what changed.

A more detailed item-by-item tracker (`comment_tracker.md`) is in the same directory and on the GitHub repo at `git@github-personal:sdelaurentiis123/unequal_acc_revisions.git`.

---

## Substantive (non-trivial) changes — flagged for your read

These are the ones I want you to push back on if anything feels wrong.

### 1. §4.2 LISA tone-down (your #7), with two new caveats added (Option X)

You were skeptical of the bump prediction. After re-deriving the physics carefully, I think the prediction is real but more heavily caveated than I'd presented in v2:

**The physics**: Peters' formulas conserve q at leading order during inspiral. So the q ≈ 0.99 plateau established in the gas phase doesn't get washed back to 1 by GW radiation. Confirmed by a new figure (`fig:q_evolution_to_LISA`) integrating from a₀ = 10³ R_S all the way to merger.

**Two caveats now stated explicitly in the text**:
1. **Grid-resolution caveat**: Magda's lookup is gridded at Δq_b = 0.1. Once q drifts from 1.0 to ≈0.99 during inspiral, our integration samples the q_b=0.9 row — but that row is for binaries that *always had* q=0.9, not binaries that drifted from 1. We don't have direct simulation data in q ∈ (0.95, 1.0).
2. **Disk-reorientation caveat**: As q crosses 1, the cavity must reorient from "locked toward original-secondary" to "locked toward new lower-mass BH." DIFF 5 argues this happens on the apsidal precession timescale, but I haven't quantitatively compared it to the gas-driven q-evolution timescale.

**Quantitative work I did**:
- A `peters_matthews_with_gas_effects.py`-style integration extended to merger confirms q stays at ~0.99 through the LISA band.
- A binary search over a₀ found the bump effect kicks in at a₀ ≈ 250 R_S and reaches its asymptote by a₀ ≈ 400 R_S (much more permissive than my earlier "10³ R_S" guess).
- A 27-case stress test (M ∈ {10⁵, 10⁶, 10⁷} M_sun × a_0 ∈ {10², 10³, 10⁴} R_S × Ṁ_b ∈ {1, 10, 100} Ṁ_Edd) showed the q ≈ 0.985 asymptote is robust across parameter space.

**The detection-statistics concerns you raised — pop-spread, ~0.5% precision floor, ~100 events** — are now stated explicitly in §4.2 as the three open questions. I left both detection forward-modeling and population synthesis to future work.

### 2. §3.1.1 methodology bridge (your #5b)

A new paragraph (~7 sentences) explicitly justifies the apocenter-stroboscopic → CBD-precession inference:
- 10τ_b cadence is fast enough vs. precession period (always >> 20τ_b).
- r_1 and r_2 share the same FFT period in every simulation — exactly what's expected if both are sampling the same precessing structure from different sides.
- That shared period matches λ(t)'s period (Fig 5).
- → period match licenses the inference even though we don't directly resolve the precession.

No "stroboscopic" or "Nyquist" jargon. Plain language. (This is what your "this needs to be fleshed out in a paragraph" was asking for.)

### 3. §3.1 mapping disambiguation (your #2)

You correctly noticed v2 conflates two different mappings. v3 distinguishes them explicitly:
- **Time-variability mapping** (mine): V/S ↔ L/P. About when λ(t) varies.
- **Time-averaged framework** (Magda's): three regimes + symmetry argument. About the value of ⟨λ⟩.

The e_b=0 simulations don't break a "mapping" — they're Magda's free-precession branch (constant λ + ⟨λ⟩=1 by circular-orbit symmetry). v3 reframes accordingly. I added a cross-reference to Magda's Section 3.5, which she had asked for in a commented-out MSS thread that didn't make it into v2.

### 4. Conclusion (iv) walkback (your "way too much to claim, legally so, causally")

Rewrote from:
> *"We find strong evidence that while the CBD precession and λ(t) oscillation have the same period, these time-series are not in phase."*

to:
> *"Across precessing systems in our suite, the CBD apsidal precession period and the λ(t) oscillation period are equal. However, these time-series are not in phase, ruling out a simple causal interpretation in terms of cavity-wall distance."*

States the empirical period-match cleanly + states what the phase mismatch *rules out* + claims no more.

### 5. Causal-claim sweep (your repeated annotations)

Replaced "determines / drives / regulates / tied to" with "tracks / paces / is consistent with" at 5 paper-wide locations: abstract (×2), §3.1 line 271, §3.1.1 line 337, conclusion close. The conclusion close was the worst offender — I rewrote it to soften "intimately tied to the CBD" into "consistent with the CBD playing a regulating role" and to elevate the flickering-jet regime as the most concrete observational handle, per your #6 framing.

### 6. Roman-paper figures inline (your #1)

Moved Table 1 (locked/precessing grid) and Figure 18 (cavity heatmap) from the appendix to inline at first §3.1 cross-reference. Captioned as "Reproduction of Table 1 / Figure 18 from \citet{DeLaurentiis25}, in preparation." The appendix is now empty and has been deleted entirely.

**Note on Roman's paper**: it doesn't have a preprint yet, so the bibtex entry now says `journal = {in preparation}`. If you have concerns about citing it that way, let me know.

### 7. Mini Fig 8 panels (your #6)

A new four-panel figure (`fig:mini_fig8_jet_regimes`) shows the jet-regime classification heatmap at Ṁ_b ∈ {0.01, 0.1, 1, 10} Ṁ_Edd. Per your suggestion: just the regime tapestry, not time-series. The flickering regime is broadest at Ṁ_b = 10 Ṁ_Edd in the high-q + high-e corner.

### 8. Geometric thick-disk funnel jet collimation (your #8.6)

Added two sentences in §4.1 incorporating your suggested physics: inflated inner walls of geometrically thick disks form a funnel along the BH spin axis that channels magnetic flux and outgoing material into a collimated relativistic jet.

### 9. New cited works

Added per your annotations: Peters 1964 (at GW equations + Fig 10 caption), Springel 2010 (AREPO), Ruiz/Shapiro 2023 + Most/Wang 2024 + Ennoggi 2025 (GR-MHD binary jets — framed as complementary to our hydrodynamic threshold-crossing). Mangiagli 2020 verified via ADS as the canonical LISA q-precision paper; no 2023 follow-up exists.

### 10. Bug fixes

- Removed `\sod{...}` Bondi-Hoyle wrapper and `\mss{is this still figure 6?}` annotations.
- Replaced phantom citations `Miranda2015` and `Duffell2024` with real keys (`miranda_munoz_lai_2017`, `dorazio_duffel`).
- Fixed typos: "Blandform" → "Blandford", "Eedd" → "Edd", "aopocenter" → "apocenter".
- Bibliography hygiene: deleted 10 duplicate entries (case-sensitive + cross-case).
- 0 unbalanced braces, 0 orphan citations, 0 missing references in the compiled PDF.

---

## Things I need from you (filling these in is on you, not me)

1. **NASA ATP grant number** — placeholder `[INSERT NUMBER]` in Acknowledgements.
2. **LISA Preparatory Science grant number** — same.
3. **Confirm affiliation** I added for you. Per your "+ Physics + ISTA" annotation and your most recent paper (Bartos & Haiman 2025, arxiv:2508.08558), you now have:
   - Department of Astronomy, Columbia University
   - Department of Physics, Columbia University
   - Institute of Science and Technology Austria (ISTA), Am Campus 1, 3400 Klosterneuburg, Austria

   If you'd prefer ISTA listed first as primary (which is how your GW231123 paper has it) let me know and I'll switch.

4. **Email for the contact line** — currently `zh2007@columbia.edu`. Switch to `zoltan.haiman@ista.ac.at` or keep as Columbia?

---

## Things I deliberately deferred

I made the call to ship v3 with these still open rather than miss the deadline. If any of these are deal-breakers, tell me and I'll do them before submission:

| Item | What's missing | Why deferred |
|---|---|---|
| Fig 8 axis labels | Row q-value labels and column e-value labels (you wrote them in by hand on the marked-up PDF) | Full rewrite of `accretion_eddington.py` is ~ a full day's work |
| Fig 1 layout | Panels-touching grid, larger axis labels (your annotation 4.1) | Same — subplot grid rewrite is finicky |
| Fig 6 panel concatenation | Self-contained captioned panels (your annotation 7.1) | Layout rewrite |
| Fig 10 detection-region annotations | Arrows/shaded boxes calling out the parameter space (your annotation 10.1) | Mod of plotting script |
| Fourier panels for Fig 6 examples (your #4b) | New companion figure | Fits in a half-day if you want it |
| Page 1-2 small prose sweeps | Barnes & Hernquist citation; "and binary stars" addition; few wording tweaks (your annotations 1.5, 1.6, 1.8, 1.9, 1.11, 2.2, 2.3, 2.4, 2.5, 2.6) | Each is small but they add up; I prioritized the substantive science DIFFs |
| Citation hunt | D'Orazio 2013 in periodogram-of-q context (your 1.12); Farris+2014 / Duffell+2017 verification (your 1.10) | Small ADS work |
| (e_b, q_b) ordering paper-wide (your 3.2) | Done in places I rewrote, not done as a sweep | Mechanical; 30 min |

If the answer is "do them all before submitting" — that's another full day to half-day of work. Tell me and I'll do it.

---

## Repository

GitHub: `git@github-personal:sdelaurentiis123/unequal_acc_revisions.git`

Files in the repo:
- `main.tex` (725 lines) — current paper source
- `main.bib` (188 unique entries) — cleaned bibliography
- `v3_clean.pdf` — publish-ready compiled PDF
- `v3_diff_v2_to_v3.pdf` — latexdiff markup vs v2
- `comment_tracker.md` — full item-by-item tracker
- `action_plan.md` — original 14-day plan I worked from
- `COVER_FOR_ZOLTAN.md` — this document
- `scripts/` — all plotting + integration code (run_q_evolution_to_LISA, stress_test, binary_search, mini_fig8_jet_regimes, regen_fig4_fig7_diverging, regen_fig2_fig3, dedupe_bib, move_appendix_inline)
- `data/` — symlinks to local cached simulation data (no Ginsburg pulls required)

All commits in chronological order:

```
8a305e5 Final tracker update
3645b14 Final pass: Fig 2 viridis, Fig 3 gray-shade, caption rewrites
4b03688 TikZ cartoon (#4a) + mini Fig 8 panels (#6)
b5cb1e7 Option X DIFF 1 caveats + Bucket D inline + Fig 4/7 diverging
588096e Stress test for q evolution
e9d5f30 fig:q_evolution_to_LISA + DIFF 1 wording refined
34a60d9 18 substantive science DIFFs (1, 2, 3, 4, 5, 6, 7, 12, 13, 17–25)
8e530da DIFFS_FOR_REVIEW.md drafted
bb0d2ce tracker: mark Day-1 DIFFs closed
f0f6c11 DIFF 16: section sentence-case sweep
ca79488 Bib hygiene (10 dupes removed, DeLaurentiis25 → in prep)
36ee32e DIFF 8+9: strip sod/mss, fix phantom citations
865e45c Initial action_plan.md + comment_tracker.md
f035300 v3 baseline = exact copy of v2
```

Each commit message names exactly which Zoltan ask it closes.

---

## What I want from you (in order of importance)

1. **Read the diff PDF first.** It's the fastest way to see what changed.
2. **Push back on §4.2** if you think the LISA prediction is still overclaiming. The new caveats (Option X) might satisfy you, or you might want me to demote it further.
3. **Fill in grant numbers** + **confirm affiliation** at your earliest convenience.
4. **Tell me which of the deferred items you want done** before submission.

Cheers,
Stan
