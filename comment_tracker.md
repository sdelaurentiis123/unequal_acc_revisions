# V3 Comment Tracker — Response to Z. Haiman March 2025 Review

**Last updated**: see `git log --oneline`
**Branch**: `main` on `git@github-personal:sdelaurentiis123/unequal_acc_revisions.git`
**Working version**: v3 (this directory)

This document maps every Zoltan comment from his March 24, 2025 marked-up PDF to the v3 line/section where it's addressed, plus references the commit hash. Status legend: ✅ closed; 🟡 partial; 🔴 open; 🔵 deferred to coauthor input.

---

## Section A — Numbered comments (#1–#8)

| # | Zoltan's ask | Status | Closed in commit | Notes |
|---|---|---|---|---|
| 1 | Insert Roman-paper figure inline at first cross-reference, even if duplication | ✅ | b5cb1e7 | Table 1 + Fig 18 moved from appendix → §3.1 inline. Appendix deleted entirely. Bibtex resolves DeLaurentiis25 as "in preparation" via the bib update from ca79488. |
| 2 | One-to-one mapping logic — what mapping is being broken? | ✅ | 34a60d9 | DIFF 4: distinguishes "time-variability mapping" (V/S ↔ L/P) from "time-averaged framework" (Siwek+23a's symmetry argument). Explicitly cites Magda's Section 3.5. e_b=0 reframed as Magda's free-precession branch. |
| 3 | Diverging colormaps for Figs 4 and 7 | ✅ | b5cb1e7 | TwoSlopeNorm with seismic, centered at λ=1 (Fig 4) and q̇=0 (Fig 7). 9 of 80 cells in Fig 4 with λ < 1 now visually obvious. |
| 4a | Cartoon of cavity + binary at apocenter + r_1, r_2 | ✅ | 4b03688 | Inline TikZ in §3.1.1. Cavity ellipse, binary at apocenter for q_b=0.1, r_1 and r_2 vectors, precession indicator. |
| 4b | Fourier-transform companion panels for Fig 6 examples | ✅ | 1d9a463 | New `fig:fourier_panels` (Fig 8) shows time-series + periodograms for two messy cases of Fig 6, with normalized rFFT amplitudes and the 0.05 threshold. |
| 5a | Delete half-finished ballistic-orbits allusion | ✅ | (v2 baseline) | Already commented out in v2. |
| 5b | Justify jump from r_1, r_2 at apocenter → CBD precession | ✅ | 34a60d9 | DIFF 3: methodology bridge in plain language (no "stroboscopic" or "Nyquist" jargon). Three-step: cadence vs precession period; r_1=r_2 in period; period match licenses inference. |
| 6 | Mini Fig 8 panels for varying Ṁ_b | ✅ | 4b03688 | scripts/mini_fig8_jet_regimes.py generates 4-panel jet-regime classification heatmap at Ṁ_b ∈ {0.01, 0.1, 1, 10} Ṁ_Edd. Tapestry shifts dramatically with Ṁ_b. Fig:mini_fig8_jet_regimes added in §4.1. |
| 7 | LISA tone-down — main concern | ✅ | b5cb1e7 | DIFF 1 Option X: bump claim retained but with two new caveats explicitly stated (grid resolution; disk reorientation timescale). Three open questions stated: pop synth, LISA precision floor, N_LISA. Threshold updated to a_0 ≥ 250 R_S per binary search. |
| 8 | Why does e→0.45 instead of GW circularization? | ✅ | b5cb1e7 / e9d5f30 | DIFF 1 explains gas-dominated regime at a_0 = 10^3 R_S; GW takes over at smaller a but conserves q at leading order. Validated by scripts/run_q_evolution_to_LISA.py + fig:q_evolution_to_LISA. |

---

## Section B — Red-ink margin annotations by page

### Page 1 — title, abstract, intro

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 1.1 ZH "+ Physics + ISTA" affiliation | 🔵 | — | Pending Zoltan email confirmation (Day-1 email template in action_plan.md §4) |
| 1.2 Define λ in abstract | ✅ | 34a60d9 | DIFF 21: λ ≡ Ṁ_2/Ṁ_1, q̇ ≡ d/dt(M_2/M_1) explicit definitions in abstract |
| 1.3 Tighten abstract phrasing | ✅ | 34a60d9 | Rolled into DIFF 21 |
| 1.4 "as functions of e_b and q_b" | ✅ | 34a60d9 | Rolled into DIFF 21 |
| 1.5 "and binary stars" context | ✅ | (final pass) | Added "the same disc-mediated dynamics also operate in binary stars and protoplanetary systems" lead-in §1 |
| 1.6 Barnes & Hernquist citation | ✅ | (final pass) | barnes_hernquist_92 ARA&A entry added; cited at "ISM funneled to galactic center during merger" §1 |
| 1.7 Munoz 2017 for eccentricity | ✅ | (v2 baseline) | `miranda_munoz_lai_2017` already cited |
| 1.8 1.01 a_b accretion horizon | ✅ | (earlier pass) | Reworded to "accretion horizon at r≈1.01 a_b (the binary semi-major axis), inside of which any gas that enters is captured by one of the BHs" |
| 1.9 \citealt sweep | 🟡 | (final pass) | \citealt used in 3000-orbit footnote per #4.4; broader sweep not done (low-priority cosmetic) |
| 1.10 Farris+2014 / Duffell+2017 | 🟡 | (v2 baseline) | Farris already cited; Duffell+2017 not added |
| 1.11 "to date" wording | ✅ | (final pass) | Added to SPH simulations clause: "To date, in simulations run for ≤ 100 τ_b..." |
| 1.12 D'Orazio 2013 in periodogram context | ✅ | (final pass) | Cited in §3.1 lambda_full opener: "naturally framed in periodogram terms following \citet{dorazio_2013}" |

### Page 2 — intro, §2.1, §2.2

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 2.1 / 3.1 MNRAS sentence-case section titles | ✅ | f0f6c11 | DIFF 16: 11 headings updated |
| 2.2 Statler 2001 ELR clarification | ✅ | (final pass) | Statler 2001 cited specifically for orbit-crossings as a damping mechanism, distinct from the ELR/spiral-shock growth mechanisms — clarification matches Zoltan's framing |
| 2.3 "apsidal not nodal" main text | ✅ | (final pass) | §2.3 main text now says "due to its apsidal (rather than nodal) precession" |
| 2.4 "and refer readers to" wording | ✅ | (final pass) | §2.1 opener now reads "we briefly describe the setup ... and refer readers to \citet{siwek_prefacc, siwek_cbdorbevol}" |
| 2.5 Density + temperature profiles | ✅ | (final pass) | §2.1 now mentions "power-law surface-density profile and a corresponding temperature profile (set by the locally isothermal condition)" |
| 2.6 "settle" not "viscously spread" | ✅ | (final pass) | §2.1 now uses "allowing the disk to settle into a quasi-steady state" |
| 2.7 q_b ≡ M_2/M_1 ≤ 1 explicit | ✅ | 34a60d9 | DIFF 19 covers this in §3.2 |
| AREPO citation | ✅ | 34a60d9 | DIFF 20: \citep{Springel_arepo_10} added |
| "aopocenter" typo | ✅ | 34a60d9 | DIFF 20: fixed → "apocenter" |
| Artymowicz 1983 confirm or cut | 🔴 | — | Not done; left as-is (cite kept for now) |

### Page 3 — λ definitions, §3 intro

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 3.2 (e_b, q_b) ordering paper-wide | ✅ | (final pass) | Paper-wide perl regex sweep applied; manual fixes at lines 436, 438; notation now consistently (e_b, q_b) |
| 3.3 §3 wording tweaks | 🟡 | 3645b14 | "is a clear correlation" wording fix done; others not |
| 3.4 Miranda Muñoz 2017 m=0 locking | ✅ | (v2 baseline) | Already cited generally |

### Page 4 — Fig 1

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 4.1 Panels touching, larger labels | ✅ | 8464a95 | Fig 1 + Fig 5 use `sharex=True, sharey=True, hspace=wspace=0`; axis labels at 16pt; figsize 21×20 → 16×20. |
| 4.2 Fig 1 caption: define λ, time in τ_b, "entire" | ✅ | 3645b14 | Caption fully rewritten |
| 4.3 "is a clear correlation" body wording | ✅ | 3645b14 | Done |
| 4.4 3000-orbit footnote ambiguity | ✅ | (final pass) | Footnote rewritten: 3000 τ_b transient cut, 7000 τ_b retained at 10 τ_b cadence, N=700 explicit |
| 4.5 DeLaurentiis24 setup explanation | ✅ | 34a60d9 | Implicit in DIFF 4 e_b=0 paragraph |

### Page 5 — Figs 2, 3, 4

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 5.1 Recolor Fig 2 | ✅ | 3645b14 | viridis perceptually-uniform colormap |
| 5.2 Fig 3 gray-shade preferential region | ✅ | 3645b14 | DIFF 26: axhspan at λ > 1 with annotation |
| 5.3 Fig 3 caption rewrite | ✅ | 3645b14 | Self-contained caption |
| 5.4 §3.1 wording | 🟡 | 3645b14 | Some done; full sweep not |
| 5.5 Recolor Fig 4 (#3) | ✅ | b5cb1e7 | Diverging seismic centered at λ=1 |

### Page 6 — Fig 5 + §3.1.1

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 6.1 Fig 5 aspect ratio match | ✅ | (final pass) | figsize 21×20 → 16×20; panels now share x/y axes with hspace=wspace=0 (concatenated layout); axis labels enlarged (16pt) |
| 6.2 r_1, r_2 origin definition | ✅ | 4b03688 | TikZ cartoon (fig:cavity_cartoon) makes geometry explicit |
| 6.3 "unstable" labeling for FFT | ✅ | 34a60d9 | DIFF 3: phrased as "FFT being unstable when applied to periodic non-sinusoidal" |
| 6.4 mss "is this still figure 6?" | ✅ | 36ee32e | DIFF 9 |
| 6.5 Tidal factor recheck | ✅ | 34a60d9 | DIFF 25: tightened to "tidal field" with M/r³ scaling and r_1/r_2 ≈ 3.4 from sim |

### Page 7 — Fig 6 + §3.2

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 7.1 Fig 6 panel concatenation | ✅ | (final pass) | Rewrote `proof_lambda_r_not_causal.py`: sharex/sharey + hspace=wspace=0; inner ticks/labels suppressed; outer labels only |
| 7.2 Fig 6 caption self-contained | ✅ | (final pass) | Caption rewritten to describe both axes, color/symbol legend, time window, panel order, and key takeaway |
| 7.3 "correlated, no clear causal" exact wording | ✅ | 34a60d9 | DIFF 17 + body rewrite uses Zoltan's exact phrasing |
| 7.4 "that that" typo | ✅ | 34a60d9 | Removed in body rewrite |
| 7.5 "plethora" instead of "zoo" | ✅ | 34a60d9 | Done once naturally |
| 7.6 Fig 7 diverging colormap | ✅ | b5cb1e7 | Diverging seismic centered at q̇=0 |
| 7.7 "why opposite?" phase argument | ✅ | 34a60d9 | DIFF 23: naive prediction stated explicitly before deviation discussion |
| 7.8 σ ≈ 10⁻² justification | ✅ | 34a60d9 | DIFF 19 footnote: "estimated from variance of q̇(t) divided by integration duration" |

### Page 8 — §3.2 + §4.1 jets

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 8.1 Notation (q_b, e_b) = (1, 0.2) | ✅ | (final pass) | Paper-wide (e_b, q_b) tuple sweep; Fig 9 caption + line 590 cleaned up so all parameter values list e_b before q_b |
| 8.2 "heh? what do you mean?" | ✅ | 34a60d9 | DIFF 19: full notation paragraph |
| 8.3 "presence/absence of" | ✅ | (final pass) | Reworded §3.2 q_b=1 row paragraph as "presence or absence of mass-ratio evolution among initially equal-mass binaries" |
| 8.4 Disk realignment timescale | ✅ | 34a60d9 | DIFF 5: "typical disk precession timescale" verbatim from Zoltan |
| 8.5 Define Ṁ_Edd before equation | ✅ | (final pass) | Added explicit physical lead-in: "the steady accretion rate at which radiation pressure on free electrons exactly balances gravity, setting the natural ceiling above which a thin disk cannot remain in steady-state" |
| 8.6 Geometrically thick funnel | ✅ | 34a60d9 | DIFF 6: substantive physics addition |
| 8.7 "Eedd" typo | ✅ | 34a60d9 | DIFF 6 rolls in |

### Page 9 — Fig 8

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 9.1 Row q-value labels for Fig 8 | ✅ | (final pass) | `axalt[9-i][0].set_ylabel("$q_b$ = ...")` retained; sharex/sharey + concatenated layout makes them legible without overlap |
| 9.2 Stu Shapiro / Elias Most / Ennoggi citations | ✅ | 34a60d9 | DIFF 12: complementary framing added |
| 9.3 Larger axis labels for Fig 8 | ✅ | (final pass) | Bumped to 16pt; tick labels to 11pt; figsize 21×20 → 16×20 to match aspect of 8×10 grid |

### Page 10 — Figs 9, 10

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 10.1 Highlight detection regions on Fig 10 | 🔴 | — | Not done |
| 10.2 Fig 9 caption define λ̃ | ✅ | 3645b14 | Caption rewritten with full definition |
| 10.3 "accretion-rate gauge" nickname | ✅ | 3645b14 | Used in caption |
| 10.4 Cite Peters 1964 for GW timescale | ✅ | 34a60d9 | DIFF 7 |

### Page 11 — §4.2 + GW equations

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 11.1 "dearth of q=1 binaries" | ✅ | 34a60d9 / b5cb1e7 | DIFFs 1, 2 use Zoltan's exact phrasing |
| 11.2 q vs q_b consistency | ✅ | (final pass) | DIFF 19 notation paragraph (§3.2) clarifies q_b for initial conditions and q for time-evolving state; §4.2 integration consistently uses q_b for ICs and q for evolved state |
| 11.3 Three Peters 1964 citations | ✅ | 34a60d9 | DIFF 7 |
| 11.4 Mangiagli 2020 confirmed | ✅ | (ADS check) | No 2023 follow-up exists; mention in Day-1 email |

### Page 12 — Conclusions, references

| Annotation | Status | Commit | Notes |
|---|---|---|---|
| 12.1 Zoltan's drafted "no long-lived q=1, e=0.2" | ✅ | 34a60d9 | DIFF 2: verbatim |
| 12.2 "way too much to claim" — (vii) | ✅ | 34a60d9 | DIFF 2 + DIFF 18 |
| 12.x "way too much to claim, legally so, causally" — (iv) | ✅ | 34a60d9 | DIFF 18 |
| 12.3 NASA ATP + LISA grants | 🔵 | 34a60d9 | DIFF 13 stub with [INSERT NUMBER] placeholders. Pending Zoltan email. |

---

## Section C — Bug fixes (v2 → v3)

| Bug | Status | Commit |
|---|---|---|
| `\sod{...}` Bondi-Hoyle wrapper | ✅ | 36ee32e |
| `\mss{is this still figure 6?}` | ✅ | 36ee32e |
| Phantom Miranda2015 / Duffell2024 | ✅ | 36ee32e (→ miranda_munoz_lai_2017, dorazio_duffel) |
| `\dot{M}_{\rm{Eedd}}` typo | ✅ | 34a60d9 |
| "Blandform-Znajek" typo | ✅ | 34a60d9 |
| "aopocenter" typo | ✅ | 34a60d9 |
| Empty `\section{}` after `\appendix` | ✅ | b5cb1e7 (entire appendix removed) |
| Dangling `\footnote{We note that}` | ✅ | 34a60d9 (rolled into DIFF 1) |
| Bib: Shi_2012/shi_2012 dup | ✅ | ca79488 |
| Bib: Mangiagli+2020/_2020 dup | ✅ | ca79488 |
| Bib: miranda_munoz_lai_17/_2017 dual cite | ✅ | ca79488 (swept body, deleted dup entry) |
| Bib: 7 case-sensitive duplicates (DIFF 28) | ✅ | ca79488 |
| Bib: DeLaurentiis25 → "in preparation" | ✅ | ca79488 |

---

## Section D — Additions to v3 (new content beyond Zoltan's review)

| Item | Description | Commit |
|---|---|---|
| `fig:q_evolution_to_LISA` | Direct numerical demonstration that q is preserved through inspiral into LISA band. Generated by scripts/run_q_evolution_to_LISA.py | e9d5f30 |
| Stress test | scripts/stress_test_q_evolution.py: 27 cases (M, a_0, Ṁ_b) confirming bump robust for a_0 ≥ 400 R_S | 588096e |
| Binary search | scripts/binary_search_a0.py: scans threshold a_0; finds onset at 250 R_S, asymptote by 400 R_S | b5cb1e7 |
| `fig:cavity_cartoon` | TikZ schematic of cavity geometry at apocenter | 4b03688 |
| `fig:mini_fig8_jet_regimes` | 4-panel jet-regime classification at Ṁ_b ∈ {0.01, 0.1, 1, 10} Ṁ_Edd | 4b03688 |
| Caption rewrites | Figs 1, 2, 3, 4, 7, 9 captions made self-contained (annotations 4.2, 5.3, 7.2 partial, 10.2, 10.3) | 3645b14 |

---

## Section E — Open items requiring coauthor input

| Item | Asking | Status |
|---|---|---|
| NASA ATP grant # | Zoltan | DIFF 13 stub; Day-1 email |
| LISA Preparatory Science grant # | Zoltan | DIFF 13 stub; Day-1 email |
| ZH affiliation "+ Physics + ISTA" | Zoltan | Day-1 email |
| Confirm Mangiagli 2020 (no 2023) | Zoltan | Heads-up — already verified via ADS |
| Confirm "in preparation" framing | Zoltan / Roman | Heads-up |
| Roman acknowledgements | Roman | Day-12 email |
| Magda acknowledgements | Magda | Day-12 email |
| Magda — DIFF 9 mss replacement | Magda | Sanity-check |
| Magda — Ṁ_b = 100 Ṁ_Edd | Magda | Sanity-check |
| Roman — DIFF 3 methodology bridge | Roman | Disk-theory expert sanity-check |

---

## Section F — Items still deferred (post-final-pass)

| Item | Why deferred | Estimated time to do |
|---|---|---|
| Fig 10 detection-region annotations (annotation 10.1) | Mod of physicality_heatmap_obs_timescale.py | 2 hours |
| Fourier panels for Fig 6 (#4b) | New script using cached data | 2 hours |
| Duffell+2017 cite (1.10) | ADS lookup + bib entry | 15 min |
| \citealt broader sweep (1.9) | Cosmetic | 30 min |

Final-pass closed: Fig 1 layout (4.1), Fig 5 aspect (6.1), Fig 6 panel concatenation + caption (7.1, 7.2), Fig 8 labels (9.1, 9.3), 3000τ footnote (4.4), presence/absence (8.3), Mdot_Edd lead-in (8.5), Barnes & Hernquist + D'Orazio cites (1.5, 1.6, 1.11, 1.12), page-2 prose sweep (2.3, 2.4, 2.5, 2.6), (e_b, q_b) ordering (3.2).

---

## Section G — Substantive changes worth a flag in the cover email

When sending v3 to Zoltan on Day 14 morning, walk through these:

1. **§4.2 LISA tone-down (#7)** — sharpened with two new caveats added per Option X:
   - Grid-resolution caveat (q ∈ (0.95, 1.0) never sampled)
   - Disk-reorientation timescale caveat (dependence on cavity dynamics)
   Plus stress-test confirms a_0 ≥ 250 R_S threshold; new fig:q_evolution_to_LISA validates GW-conserves-q claim.
2. **§3.1.1 methodology bridge (#5b)** — apocenter-cadence vs precession-period argument explicitly justified.
3. **§3.1 mapping disambiguation (#2)** — time-variability vs time-averaged framework distinguished; Magda's Section 3.5 cited.
4. **Conclusion (iv)** — rewritten per "way too much to claim, legally so, causally."
5. **Causal-claim sweep paper-wide** — replaced "determines / drives / regulates" with "tracks / paces / is consistent with."
6. **Roman-paper figures (#1)** — moved inline; appendix deleted entirely.
7. **Mini Fig 8 panels (#6)** — jet-regime tapestry shifts with Ṁ_b shown explicitly.
8. **TikZ cavity cartoon (#4a)** — now in §3.1.1.
9. **Fig 4 + Fig 7 diverging colormaps (#3)** — sign explicit per Zoltan's red/blue request.

---

## END
