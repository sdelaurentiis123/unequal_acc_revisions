# V3 Comment Tracker — Response to Z. Haiman March 2025 Review

**Last updated**: see git log (`git log --oneline`)
**Authors**: DeLaurentiis, Haiman, Siwek, Rafikov
**Working version**: v3 (this directory)
**Source-of-truth for status**: this file + git history

This document maps every Zoltan comment from his March 24, 2025 marked-up PDF (8 numbered comments + ~50 red-ink margin annotations) to the v3 line / section where it's addressed. It also lists open items pending coauthor input.

Status legend: ✅ closed; 🟡 partial; 🔴 open; 🔵 deferred to coauthor

---

## Section A — Numbered comments (#1–#8)

| # | Zoltan's ask (verbatim from March 25 cover email) | Status | v3 location | Commit | Notes |
|---|---|---|---|---|---|
| 1 | Insert duplicate of Roman-paper figure inline at cross-reference, not just reference. *"It's like you are saying 'Look! How interesting! I found that A and B are correlated! A is presented over here, and B is presented over there!'... I suggest to simply insert a copy of the pertinent figure from your paper with Roman here, even if it is a duplication."* | 🔴 | §3.1 lines 271 (Tab 1), 288 (Fig 18) | — | Bucket D Day 2: move from appendix to inline. Caption: "Reproduction of Figure 18 from \citet{DeLaurentiis25}, in preparation." |
| 2 | One-to-one mapping logic unclear. *"You say here that the e_b=0 sims 'break the one-to-one mapping' because lambda is constant. But what mapping is being broken? The previous paragraph concludes with a mapping from S23, but that is not about variable-vs-constant, that was about unity-vs-preferential."* | 🔴 | §3.1 lines 271-278 | — | DIFF 4: minimal disambiguation — name "time-variability mapping" vs "time-averaged ⟨λ⟩ framework" explicitly. Don't reframe Magda's paraphrase. |
| 3 | Diverging colormaps for Figs 4 and 7. *"In these figures, the sign is important, as well as the magnitude... use two colors -- say red and blue -- indicating the sign, and the darkness indicating the absolute value."* | 🔴 | Figs 4, 7 | — | Day 4: switch `lambda_fig2_heatmap.py` Fig 4 colormap to seismic centered at λ=1; same for `qdot_heatmap.py` Fig 7 centered at q̇=0. |
| 4a | Cartoon of cavity + binary at apocenter + r_1, r_2. *"It would be very useful to add an illustrative figure here, either directly a simulation snapshot, or a cartoon like in your GR precession paper."* | 🔴 | New figure in §3.1.1 | — | Day 7: TikZ scaffolding (Zoltan accepted both options). Default: TikZ. |
| 4b | Fourier-transform companion panels for Fig 6. *"I actually think it would be useful even to include a couple of example time-series curves, say upper right and middle right of Fig.6, and show them along with their Fourier transforms."* | 🔴 | New figure in §3.1.1 | — | Day 7: new script `fft_companion.py` using existing `magda_accretion_files/`. |
| 5a | Delete half-finished ballistic-orbits/shocks allusion. | ✅ | line 372 (commented out in v2) | (v2 baseline) | Already done in v2. |
| 6.4 | "is this still figure 6?" annotation | ✅ | line 367 | 36ee32e | DIFF 9 |
| C.1 | `\sod{...}` Bondi-Hoyle wrapper | ✅ | lines 350-364 | 36ee32e | DIFF 8 |
| C.5 | Phantom Miranda2015/Duffell2024 citations | ✅ | line 356 | 36ee32e | DIFF 8 → miranda_munoz_lai_2017, dorazio_duffel |
| C.6 | Duplicate Shi_2012/shi_2012 bib | ✅ | bib lines 410-422 deleted | ca79488 | DIFF 14 |
| C.7 | Duplicate Mangiagli+2020/Mangiagli_2020 bib | ✅ | bib block deleted | ca79488 | DIFF 15 |
| (new) | Bib hygiene: 10 case-sensitive + cross-case dupes | ✅ | bib | ca79488 | DIFF 28 |
| (new) | DeLaurentiis25 → "in preparation" | ✅ | bib lines 95-101 | ca79488 | DIFF 14b — no preprint exists |
| 2.1 / 3.1 | MNRAS section title sentence case | ✅ | 11 headings | f0f6c11 | DIFF 16 |
| 5b | Justify the jump from r_1, r_2 measurements at apocenter to CBD precession. *"It is not totally clear to me how you make the jump from measurements of r1 and r2 at apocenter only to CBD precession. I think this needs to be fleshed out in a paragraph, and justified."* | 🔴 | Insert before line 339 | — | DIFF 3: methodology bridge in plain language (no "stroboscopic" or "Nyquist" jargon). Three-step argument: cadence vs precession period; r_1=r_2 in period; period match licenses inference. |
| 6 | Mini Fig 8 panels for varying Ṁ_b. *"You could even redo Fig.8 for a few different Mdot,bins... show how the tapestry color boundaries move around as you increase/decrease Mdot,bin... I think this may really be the most interesting take-away for readers, other than for the ~10 people who will care about the minute details of the lambda."* | 🔴 | New figure after §4.1 | — | Day 5: jet-regime classification heatmap only (NOT time-series) at Ṁ_b ∈ {0.01, 0.1, 1, 10} Ṁ_Edd. |
| 7 | LISA tone-down — main concern. *"Surely a real binary won't stop evolving when the simulation does... such a 'bump' would be smeared out... we only expect ~100s of LISA detections."* | 🔴 | §4.2 lines 510-511 | — | DIFF 1: sharpen, not retreat. Use Stan's strain calc to scope the regime of validity (a₀ ≥ 800 R_S). Acknowledge pop-spread + LISA precision + N concerns explicitly. Use Zoltan's "dearth of strictly q=1 systems" phrasing. |
| 8 | Why does e→0.45 instead of GW circularization? *"Why does e→0.45? Surely in the LISA band, the binaries will circularize? Why is this not happening in the calculations?"* | 🔴 | §4.2 line 510 | — | Rolled into DIFF 1: explain that integration is at a₀=10³R_S (gas-dominated regime), GW circularization happens at smaller a but conserves q at leading order. Cite extended `peters_matthews_with_gas_effects.py` (Day 3 task). |

---

## Section B — Red-ink margin annotations by page

### Page 1 — title, abstract, intro

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 1.1 ZH affiliation "+ Physics + ISTA" | 🔵 | author block | — | Day-1 email to Zoltan — confirm intent |
| 1.2 Define λ explicitly in abstract | 🔴 | line 63 | — | DIFF 21: λ ≡ Ṁ_2/Ṁ_1, q̇ ≡ d/dt(M_2/M_1) |
| 1.3 Tighten abstract phrasing on q̇ | 🔴 | line 63 | — | Rolled into DIFF 21 |
| 1.4 "as functions of e_b and q_b" explicit | 🔴 | line 63 | — | Rolled into DIFF 21 |
| 1.5 Add "and binary stars" context to intro opening | 🔴 | line 68 | — | Day 9 prose sweep |
| 1.6 Barnes & Hernquist citation | 🔴 | line 68 | — | Bucket C Day 2: add Barnes & Hernquist 1992 ARAA |
| 1.7 Munoz et al. 2017 for eccentric variability | ✅ | line 68 | (v2 baseline) | `miranda_munoz_lai_2017` already cited |
| 1.8 Clarify "1.01 a_b" accretion horizon | 🔴 | line 72 | — | Day 9 prose sweep |
| 1.9 Use \citealt for narrative citations | 🔴 | various | — | Day 9 prose sweep — selective |
| 1.10 Farris+2014, Duffell+2017 verification | 🟡 | line 68 | — | Farris cited; Duffell+2017 — verify if needed |
| 1.11 "to date" wording fix | 🔴 | line 79 | — | Day 9 prose sweep |
| 1.12 D'Orazio 2013 in periodogram-of-q context | 🟡 | (need new placement) | — | `dorazio_2013` already cited generally; add specific cite in §3.1 where λ(t) variability discussed |

### Page 2 — intro, §2.1, §2.2

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 2.1 MNRAS lowercase section titles | 🔴 | lines 86, 88, 101, 116, 142, 145, 319, 377, 393, 396, 471, 513 | — | DIFF 16 |
| 2.2 Statler 2001 — clarify "test particles vs gas stream crossings" | 🔴 | line 105 | — | Day 9 prose sweep |
| 2.3 "apsidal (not nodal) precession" in main text | 🔴 | (currently footnote only) | — | Day 9 prose sweep |
| 2.4 "and refer readers to" Siwek setup | 🔴 | line 89 | — | Day 9 prose sweep |
| 2.5 Mention density+temperature profiles in initial conditions | 🔴 | line 93 | — | Day 9 prose sweep |
| 2.6 "settle" not "viscously spread" | 🔴 | line 93 | — | Day 9 prose sweep |
| 2.7 Define q_b ≡ M_2/M_1 ≤ 1 explicitly | 🔴 | line 95 | — | DIFF 19 covers this |
| 2.x AREPO citation | 🔴 | line 97 | — | DIFF 20 |
| 2.x "aopocenter" typo | 🔴 | line 97 | — | DIFF 20 |
| 2.x Artymowicz 1983 — confirm or cut | 🔴 | line 113 | — | Day 9: cut (MSS also couldn't find it) |

### Page 3 — λ definitions, §3 intro

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 3.1 Lowercase section titles | 🔴 | (same as 2.1) | — | DIFF 16 |
| 3.2 (e_b, q_b) ordering throughout | 🔴 | paper-wide | — | Day 9 prose sweep — sed-like find/replace |
| 3.3 §3 wording tweaks | 🔴 | lines 155-160 | — | Day 9 prose sweep |
| 3.4 Miranda Muñoz 2017 for m=0 locking specifically | 🟡 | (currently general cite) | — | Day 9 — tie to specific case |

### Page 4 — Figure 1 (λ(t) grid)

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 4.1 Make panels touch, labels ≥ main text size | 🔴 | Fig 1 | — | Day 6: rewrite `magda_accretion_actual_fixed.py` |
| 4.2 Caption: define λ, time in τ_b, "entire" suite | 🔴 | line 150 | — | Day 9 prose sweep |
| 4.3 "is a clear correlation" body wording | 🔴 | line 278 | — | Day 9 prose sweep |
| 4.4 3000-orbit footnote ambiguity | 🔴 | lines 288, 378 | — | Day 9 prose sweep — both footnotes |
| 4.5 DeLaurentiis24 needs setup explanation | 🔴 | line 273 | — | DIFF 4 covers this implicitly |

### Page 5 — Figs 2, 3, 4

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 5.1 Recolor Fig 2 (#1) | 🔴 | Fig 2 | — | Day 4: viridis or perceptually uniform |
| 5.2 Fig 3: shade gray power-law region | 🔴 | Fig 3 | — | DIFF 26 / Day 4 in `magda_fig2.py` |
| 5.3 Fig 3 caption rewrite | 🔴 | line 297 | — | Day 4 caption |
| 5.4 §3.1 wording | 🔴 | lines 308-315 | — | Day 9 prose sweep |
| 5.5 Recolor Fig 4 (#3) | 🔴 | Fig 4 | — | Day 4: diverging seismic centered at λ=1 |

### Page 6 — Fig 5 + §3.1.1

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 6.1 Fig 5: same aspect ratio as Figs 2, 4 | 🔴 | Fig 5 | — | Day 4: rewrite `magda_accretion_geometry_ecc_combined.py` |
| 6.2 "Where is r measured from?" | 🔴 | line 333 | — | DIFF 3 + explicit r_1, r_2 origin definition |
| 6.3 "maybe 'unstable'?" — FFT-on-non-sinusoidal | 🔴 | line 337 | — | DIFF 3 covers via "FFT being unstable when applied to periodic non-sinusoidal" |
| 6.4 "is this still figure 6?" | 🔴 | line 367 | — | DIFF 9 |
| 6.5 "approximately three times" tidal-potential factor | 🔴 | line 367 | — | DIFF 25: tidal-field framing with M/r³ scaling, r_1/r_2 ≈ 3.4 |

### Page 7 — Fig 6 + §3.2 intro

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 7.1 Make Fig 6 panels bigger by concatenating | 🔴 | Fig 6 | — | Day 6: rewrite `proof_lambda_r_not_causal.py` |
| 7.2 Captions self-contained | 🔴 | line 343 | — | Day 6 caption rewrite |
| 7.3 "they are correlated, no clear causal link" | 🔴 | line 371 | — | DIFF 17: use Zoltan's exact phrasing |
| 7.4 Typo "that that" | 🔴 | line 371 | — | Day 9 prose sweep |
| 7.5 "plethora" instead of "zoo" | 🔴 | line 373 | — | Day 9 prose sweep — once naturally |
| 7.6 Diverging colormap for Fig 7 | 🔴 | Fig 7 | — | Day 4: seismic centered at q̇=0 |
| 7.7 "why opposite?" — phase argument | 🔴 | line 369 | — | DIFF 23: phase argument insertion |
| 7.8 "how did you determine this?" — σ ≈ 10⁻² | 🔴 | line 389 footnote | — | DIFF 19 covers this |

### Page 8 — §3.2 + §4 jets opening

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 8.1 Notation (q_b, e_b) = (1, 0.2) | 🔴 | line 389 | — | DIFF 19 |
| 8.2 "heh? what do you mean?" — confused passage | 🔴 | line 389 | — | DIFF 19 |
| 8.3 "presence/absence of" wording | 🔴 | line 389 | — | Day 9 prose sweep |
| 8.4 Disk realignment timescale | 🔴 | line 391 | — | DIFF 5: "typical disk precession timescale" |
| 8.5 Define Ṁ_Edd before equation | 🟡 | line 401 | — | Day 9 prose sweep + DIFF 24 |
| 8.6 Geometrically thick disks form "funnel" | 🔴 | line 398 | — | DIFF 6: substantive physics addition |
| 8.7 Typo Ṁ_{Eedd} extra 'e' | 🔴 | line 403 | — | DIFF 6 rolls in |

### Page 9 — Fig 8

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 9.1 Row q-value labels for Fig 8 | 🔴 | Fig 8 | — | DIFF 27 / Day 5 |
| 9.2 Stu Shapiro / Elias Most citations | 🔴 | line 435 | — | DIFF 12: Ruiz/Shapiro 2023, Most/Wang 2024, Ennoggi 2025 |
| 9.3 Larger axis labels for Fig 8 | 🔴 | Fig 8 | — | DIFF 27 |

### Page 10 — Figs 9, 10

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 10.1 Highlight detection regions on Fig 10 | 🔴 | Fig 10 | — | Day 7: annotate `physicality_heatmap_obs_timescale.py` output |
| 10.2 Fig 9 caption: define λ̃ | 🔴 | line 419 | — | Day 4 caption rewrite |
| 10.3 "Accretion-rate gauge" nickname | 🔴 | line 419 | — | Day 4 caption |
| 10.4 Cite Peters 1964 for GW timescale | 🔴 | line 464 | — | DIFF 7 |

### Page 11 — §4.2 + GW equations

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 11.1 "dearth of q=1 binaries" | 🔴 | line 471 + line 511 + conclusion (vii) | — | DIFFs 1, 2 use Zoltan's phrasing |
| 11.2 Be consistent: q vs q_b | 🔴 | paper-wide | — | DIFF 19 + Day 9 sweep |
| 11.3 Three Peters 1964 citations on GW equations | 🔴 | line 483 | — | DIFF 7 |
| 11.4 Mangiagli citation suggestion ("2023?") | ✅ | line 510 | (v2 baseline) | `Mangiagli_2020` correctly cited; ADS confirmed no 2023 follow-up. Mention in Day-1 email to Zoltan. |

### Page 12 — conclusions, references

| Annotation | Status | v3 location | Commit | Notes |
|---|---|---|---|---|
| 12.1 Zoltan's drafted "no long-lived q=1, e=0.2 binaries, will evolve to q<1" | 🔴 | line 523 conclusion (vii) | — | DIFF 2: use verbatim |
| 12.2 "way too much to claim casually" — (vii) | 🔴 | line 523 | — | DIFF 2 |
| 12.x "way too much to claim, legally so, causally" — (iv) | 🔴 | line 520 | — | DIFF 18 |
| 12.3 Acknowledgements — NASA ATP + LISA grants | 🔵 | new section before line 531 | — | DIFF 13: stub with placeholders. Day-1 email to Zoltan. |

---

## Section C — Bug fixes (v2 → v3)

| Bug | Status | Commit | Notes |
|---|---|---|---|
| `\sod{...}` Bondi-Hoyle wrapper | 🔴 | — | DIFF 8 |
| `\mss{is this still figure 6?}` annotation | 🔴 | — | DIFF 9 |
| Phantom `\citep{Miranda2015, Duffell2024}` | 🔴 | — | DIFF 8: substitute `miranda_munoz_lai_2017`, `dorazio_duffel` |
| `\dot{M}_{\rm{Eedd}}` typo | 🔴 | — | DIFF 6 |
| "Blandform-Znajek" typo | 🔴 | — | DIFF 6 |
| "aopocenter" typo line 97 | 🔴 | — | DIFF 20 |
| Empty `\section{}` after `\appendix` | 🔴 | — | DIFF 11 / appendix deleted entirely after Bucket D |
| Dangling `\footnote{We note that}` line 510 | 🔴 | — | DIFF 1 rolls in |
| Duplicate `Shi_2012` / `shi_2012` bib | 🔴 | — | DIFF 14 |
| Duplicate `Mangiagli+2020` / `Mangiagli_2020` bib | 🔴 | — | DIFF 15 |
| Duplicate `miranda_munoz_lai_17` / `miranda_munoz_lai_2017` bib (both cited!) | 🔴 | — | DIFF 28 |
| Duplicate `farris_2014` × 3 entries | 🔴 | — | DIFF 28 |
| Duplicate `farris_2015` × 3 entries | 🔴 | — | DIFF 28 |
| Duplicate `MacFadyen_08`, `siwek_cbdorbevol`, `siwek_prefacc`, `white_rees_78` bib entries | 🔴 | — | DIFF 28 |
| `DeLaurentiis25` bib entry: arxiv ID claims preprint that doesn't exist | 🔴 | — | DIFF 14b: change to `journal = {in preparation}`, drop arxiv |

---

## Section D — Open items requiring coauthor input

| Item | Asking | Sent | Received | Notes |
|---|---|---|---|---|
| NASA ATP grant # | Zoltan | (Day 1) | — | For DIFF 13 |
| LISA Preparatory Science grant # | Zoltan | (Day 1) | — | For DIFF 13 |
| ZH affiliation "+ Physics + ISTA" | Zoltan | (Day 1) | — | For author block |
| Confirm Mangiagli 2020 (no 2023 paper) | Zoltan | (Day 1) | — | Heads-up — already verified via ADS |
| Confirm "in preparation" framing for DeLaurentiis25 | Zoltan | (Day 1) | — | Heads-up |
| Roman acknowledgements | Roman | (Day 12) | — | For DIFF 13 |
| Magda acknowledgements | Magda | (Day 12) | — | For DIFF 13 |
| Magda — DIFF 9 mss replacement | Magda | (Day 12) | — | Sanity check |
| Magda — Ṁ_b = 100 Ṁ_Edd | Magda | (Day 12) | — | Sanity check |
| Roman — DIFF 3 methodology bridge | Roman | (Day 12) | — | Disk-theory expert sanity check |
| Roman — appendix-vs-inline preference | Roman | (Day 12) | — | Default: inline per Zoltan #1 |

---

## Section E — Substantive changes worth a flag in the cover email

When sending v3 to Zoltan on Day 14 morning, walk through these:

1. **§4.2 LISA tone-down (#7)** — sharpened, not retreated. Used `peters_matthews_with_gas_effects.py` extended to merger to validate q-preservation argument.
2. **§3.1.1 methodology bridge (#5b)** — apocenter sampling vs precession period explicitly justified.
3. **§3.1 mapping disambiguation (#2)** — time-variability vs time-averaged frameworks distinguished.
4. **Conclusion (iv)** — rewritten per "way too much to claim, legally so, causally."
5. **Causal-claim sweep paper-wide** — replaced "determines / drives / regulates" with "tracks / paces / is consistent with."
6. **Roman-paper figures (#1)** — moved inline, attributed as in-prep reproductions.

---

## END
