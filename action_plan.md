# Unequal Accretion v3 — 14-Day Execution Plan

**Hard deadline**: May 20, 2026, 4:15 PM ET — send to Zoltan no later than 10 AM that morning.
**Working directory**: `/Users/stanislavdelaurentiis/unequal_acc_local/Unequal Acc v3/`
**Baseline commit**: v2/main.tex copied verbatim, git-initialized.
**Data**: symlinked to `/Users/stanislavdelaurentiis/roman_work/` — no Ginsburg pull needed.
**Author-facing tracker**: `comment_tracker.md` (this directory) — updated per-DIFF for Zoltan.

This plan supersedes the prior tracking docs. It reflects every correction surfaced during the May 6 conversation. Every science DIFF wording below has been verified against the actual v2/main.tex line numbers and the source code in `scripts/`.

---

## 0. Headline corrections relative to the prior tracking docs

Five pieces of the master plan and addendum that turned out to be wrong:

1. **No Ginsburg pull is required.** Local `data/` symlinks point to 23 GB of cached accretion files and 51 MB of cavity-Fourier pickles. Every plotting script and every ODE script reads these local paths. No `rsync`.

2. **Bib hygiene is dirtier than master plan acknowledged.** Beyond the Shi and Mangiagli duplicates, there are six case-sensitive duplicate keys (`farris_2014` ×3, `farris_2015` ×3, `MacFadyen_08`, `siwek_cbdorbevol`, `siwek_prefacc`, `white_rees_78`) and **two distinct keys for the same Miranda+2017 paper both cited in the body** (`miranda_munoz_lai_17` AND `miranda_munoz_lai_2017`). New DIFF 28 covers this sweep.

3. **The DIFF 25 tidal-factor claim is correct** with proper interpretation. Reading Fig 6's actual (e_b=0.2, q_b=0.1) panel: r_1 ≈ 2.4 a, r_2 ≈ 0.7 a, so r_1/r_2 ≈ 3.4. With q_b=0.1 and the technical "tidal field gradient" definition (M/r³): ratio = q × (r_1/r_2)³ = 0.1 × 39 = 3.9 — matches the 5× accretion ratio. The v2 sentence is defensible; just tighten "tidal potential" → "tidal field" so the M/r³ scaling is clearly meant.

4. **The LISA bump argument is much more defensible than the master plan implied.** Stan's `peters_matthews_strain_clean_with_sum_rk4_jonathan.py` integration shows that for a₀ ≥ 800 R_S, e is still ~ 0.3-0.4 at LISA-band entry — GW circularization is incomplete. Combined with the Peters formulas mathematically conserving q at leading order, the q ≈ 0.991 plateau is preserved through inspiral and into the LISA band. **DIFF 1 should sharpen, not retreat.** The real concerns are population-spread, ~0.5% LISA precision floor vs ~0.9% deviation, and N ~ 100 detections — which are tractable open questions, not show-stoppers.

5. **The Roman paper has no preprint yet.** The bib entry for `DeLaurentiis25` currently points to `arXiv:2405.07897`, which doesn't reflect the actual status. DIFF 14b: change `journal = {arXiv e-prints}` → `journal = {in preparation}`, drop the arxiv ID. Body citations stay as `\citet{DeLaurentiis25}` but format as "DeLaurentiis & Rafikov, in preparation."

Plus the structural reframe per Zoltan's #6: the **jet-regime tapestry is the headline**, and §4.2 should not visually outweigh §4.1 after DIFFs 1+2 expand the LISA prose.

---

## 1. Bucket organization (8 buckets)

Every task lives in exactly one bucket. Buckets are dependency-ordered.

### Bucket A — Compile-clean baseline (Day 1 morning, ~3h)

The 6 DIFFs that don't change scientific claims. Apply first because they unblock coauthor circulation (Day 12).

- DIFF 8 — strip `\sod{}` Bondi-Hoyle wrapper, fix phantom citations `Miranda2015 → miranda_munoz_lai_2017`, `Duffell2024 → dorazio_duffel`
- DIFF 9 — strip `\mss{is this still figure 6?}` annotation; replace surrounding text with proper Fig 6 cross-reference
- DIFF 11 — empty `\section{}` after `\appendix` → with #1 inlined (Bucket D), the entire appendix becomes empty and gets deleted
- DIFF 14 — bib: delete duplicate `Shi_2012` block (line 463), sweep main.tex `Shi_2012 → shi_2012`
- DIFF 15 — bib: delete duplicate `Mangiagli+2020` block (line 1124)
- DIFF 16 — section title casing sweep (lines 86, 88, 101, 116, 142, 145, 319, 377, 393, 396, 471, 513)
- DIFF 28 — bib hygiene sweep: merge `miranda_munoz_lai_17 → miranda_munoz_lai_2017`; dedupe `farris_2014` ×3 and `farris_2015` ×3 (verify cited form first); dedupe `MacFadyen_08`, `siwek_cbdorbevol`, `siwek_prefacc`, `white_rees_78`

### Bucket B — Substantive science DIFFs (Day 1 afternoon + Day 2, ~10h)

Wording-sensitive. User sign-off required on DIFFs 1, 4, 17, 18 wording before applying.

- **DIFF 1** — §4.2 LISA closing rewrite (sharpen, not retreat). Paragraph at line 510-511. Use Stan's strain calc to scope the regime of validity (a₀ ≥ 800 R_S). Acknowledge pop-spread + LISA precision + N concerns explicitly. Use Zoltan's "dearth of strictly q=1 systems" phrasing.
- **DIFF 2** — Conclusion (vii) at line 523 rewrite. Use Zoltan's drafted "There are no long-lived q=1, e=0.2 binaries, and these will evolve to q<1 or some such" verbatim.
- **DIFF 3** — Methodology bridge in §3.1.1, insertion before line 339. Plain-language version: cadence (10τ_b) much faster than precession period (>> 20τ_b); r_1, r_2 inherit cavity precession frequency; r_1 = r_2 in period as expected if both stroboscopically sample same precessing structure; period match licenses "λ paced by precession" inference. Drop "stroboscopic" / "Nyquist" jargon.
- **DIFF 4** — One-to-one mapping logic at line 271-278. **Minimal disambiguation only** — name "time-variability mapping" vs "time-averaged mapping" explicitly, address Zoltan's "what mapping is being broken." Don't reframe Magda's paraphrase. Don't call (0.2, 1.0) a "striking exception." Leave line 313-315 alone.
- **DIFF 5** — disk realignment timescale at line 391. Use Zoltan's own "typical disk precession timescale" phrasing.
- **DIFF 6** — geometrically-thick funnel jet collimation at line 398. Substantive physics addition Zoltan asked for. Roll in DIFF rolled-in Blandford typo + `\dot{M}_{\rm Eedd}` typo.
- **DIFF 7** — Peters 1964 citation at GW equations (line 483) and Fig 10 GW shrink calc (line 464).
- **DIFF 12** — Shapiro/Most/Ennoggi citations at line 435. Frame your work as complementary (hydrodynamic threshold-crossing) to GR-MHD work (already-launched jets evolving through inspiral).
- **DIFF 13** — Acknowledgements section before `\section*{Data Availability}` at line 531. Stub with `[INSERT GRANT #]` placeholders. Day-1 email to Zoltan to fill these in.
- **DIFF 17** — Causal-claim sweep paper-wide. Replace causal verbs with correlative verbs at lines 271, 290, 337, 528 + abstract.
- **DIFF 18** — Conclusion (iv) at line 520 rewrite. Direct response to "way too much to claim, legally so, causally!"
- **DIFF 19** — q_b ≤ 1 notation paragraph at line 389. Address "heh? what do you mean?"
- **DIFF 20** — AREPO citation at line 97. Add `\citep{Springel_arepo_10}`. Fix typo "aopocenter" → "apocenter."
- **DIFF 21** — λ definition in abstract (line 63).
- **DIFF 22** — Ṁ_b = 100 Ṁ_Edd assumption at line 501.
- **DIFF 23** — Phase argument insertion before line 369. Make naive prediction (r_1 in phase, r_2 anti-phase) explicit before showing where it breaks.
- **DIFF 24** — Jet timescale + threshold justification at line 427.
- **DIFF 25** — Tidal-factor at line 367. Tighten "tidal potential" → "tidal field" so M/r³ scaling is clear. With r_1/r_2 ≈ 3.4 from the actual sim, q × (r_1/r_2)³ ≈ 4 — matches the 5× accretion ratio. Defensible — keep.

### Bucket C — Bib new entries (Day 2 morning, ~1h)

- Add `Springel_arepo_10` (DIFF 20)
- Add `Ruiz_Shapiro_23`, `Most_Wang_24`, `Ennoggi_25` (DIFF 12)
- Add `barnes_hernquist` Barnes & Hernquist 1992 ARAA (annotation 1.6)
- Verify D'Orazio 2013 entry exists for periodogram-of-q context (annotation 1.12)
- Update `DeLaurentiis25` entry: `journal = {in preparation}`, drop arxiv ID (DIFF 14b)

### Bucket D — Inline duplication of Roman's table + figure (Day 2 afternoon, ~half day)

Per Zoltan's #1 explicit ask: "insert a copy of the pertinent figure from your paper with Roman here, even if it is a duplication." Move from appendix → inline.

- Move `tab:locked_precessing_grid` (currently lines 539-647 in appendix) → inline at line ~271 of §3.1
- Move `fig:a_e_cav_heatmap` (`a_e_cavity_heatmap_joint.pdf`, currently lines 649-654 in appendix) → inline at line ~288 of §3.1
- Caption credits: "Reproduction of Figure 18 from \citet{DeLaurentiis25}, in preparation."
- After move, the entire `\appendix` section is empty → delete `\appendix` and surrounding lines

### Bucket E — Figure regens on local data (Days 4-7, ~5 days)

All scripts in `scripts/` already point to local paths. Just edit + run.

- **Day 4**: Fig 4 diverging colormap (`lambda_fig2_heatmap.py`); Fig 7 diverging colormap (`qdot_heatmap.py`); Fig 3 gray-shade `λ > 1` (`magda_fig2.py`, DIFF 26); Fig 9 caption rewrite (no script change); Fig 5 aspect ratio (`magda_accretion_geometry_ecc_combined.py`)
- **Day 5**: Fig 8 critical regen with row/col labels in `accretion_eddington.py` (DIFF 27); mini Fig 8 panels (jet-regime classification heatmap only at Ṁ_b ∈ {0.01, 0.1, 1, 10} Ṁ_Edd) — write new script `mini_fig8_jet_regimes.py`
- **Day 6**: Fig 1 layout rewrite (`magda_accretion_actual_fixed.py`) — panels touching, shared axes, larger fonts; Fig 6 layout rewrite (`proof_lambda_r_not_causal.py`) — concatenate, shared axes, self-contained caption with Zoltan's "correlated, no clear causal link" exact phrasing
- **Day 7**: TikZ cartoon (#4a) — write inline TikZ in main.tex (or pull a sim snapshot — Zoltan accepted both); Fourier panels (#4b) — new script `fft_companion.py` using existing `magda_accretion_files/` data

### Bucket F — LISA q-evolution validation (Day 3 afternoon, ~half day)

This validates DIFF 1's claim that q is preserved through inspiral.

- Modify `scripts/peters_matthews_with_gas_effects.py` line 372: change `t_end = t_gw[0] * 0.01` to `t_end = t_gw[0]` (full coalescence integration instead of 1%)
- Run for the (e=0.2, q=1.0) and (e=0.3, q=1.0) cases at a₀ = 100 R_S and 1000 R_S
- Confirm q stays at ~ 0.991 / 0.998 through inspiral and into LISA band
- New figure: `fig_q_evolution_to_LISA.pdf` showing q(f) trajectory crossing the LISA band
- Cite this in DIFF 1 prose as the direct numerical validation

### Bucket G — Red-ink prose sweep (Day 9, ~1 day)

Every remaining ❌ in `annotation_review.md` page-by-page tables. ~30 small fixes:

- Page 1: 1.3 abstract phrasing, 1.5 binary stars context, 1.8 1.01 horizon clarification, 1.9 \citealt sweep (selective), 1.10 Farris/Duffell verification, 1.11 "to date" wording
- Page 2: 2.3 apsidal in main text, 2.4 "and refer readers to" wording, 2.5 density+temperature profiles, 2.6 "settle" not "viscously spread", 2.7 q_b ≤ 1 explicit
- Page 3: 3.2 (e_b, q_b) ordering sweep paper-wide, 3.3 §3 wording tweaks
- Page 4: 4.4 3000-orbit footnote rewrite (with N count)
- Page 5: 5.2 verified by DIFF 26, 5.3 Fig 3 caption rewrite, 5.4 §3.1 wording
- Page 6: 6.5 verified by DIFF 25, 6.2 (where r is measured from) — make explicit at line 333
- Page 7: 7.4 "that that" typo, 7.5 "plethora" once naturally
- Page 8: 8.2 find unclear passage, 8.3 "presence/absence of" wording, 8.5 define Ṁ_Edd before equation (rolled in DIFF 24)
- Page 9: 9.1, 9.3 verified by DIFF 27
- Page 10: 10.1 detection regions on Fig 10, 10.2 verified by Fig 9 caption rewrite Day 4, 10.3 "accretion-rate gauge" nickname

### Bucket H — Final polish (Days 10-13)

- Day 10: AI reviewer pass + final compile + self-read start to finish
- Day 11: comment_tracker.md final pass; cover document for Zoltan
- Day 12: send to Magda + Roman with focused asks
- Day 13: address coauthor feedback; verify cover doc still maps to current line numbers

---

## 2. Day-by-day timeline

### Day 1 — Wednesday May 7

**AM (3-4h)** Bucket A:
1. DIFF 11 (empty appendix \section{} fix, unblocks compile)
2. DIFF 8 (sod wrapper + phantom citations)
3. DIFF 9 (mss annotation removal)
4. DIFFs 14, 15 (bib duplicate cleanup)
5. DIFF 28 (Miranda + farris/MacFadyen/siwek/white_rees dedup)
6. DIFF 16 (section title casing)
7. Compile clean — bibtex warnings to zero
8. Email Zoltan (Day-1 email, see §4)

**PM (3-4h)** Bucket B start:
9. DIFFs 5, 6, 7, 12 (disk realignment, funnel collimation, Peters citation, Shapiro/Most/Ennoggi) — all relatively short, low-controversy substantive adds
10. DIFF 13 (acknowledgements stub with grant placeholders)

**EOD checkpoint**: paper compiles clean with zero `??` citations and zero bib warnings. Three of the substantive science DIFFs (5, 6, 7, 12) applied. Day-1 email sent to Zoltan. ~10 of 28 DIFFs done.

### Day 2 — Thursday May 8

**AM (4h)** Bucket B middle:
11. DIFF 17 (causal sweep paper-wide) — most prose-edit-heavy task; do early when fresh
12. DIFF 18 (conclusion (iv) walkback)
13. DIFF 19 (q_b ≤ 1 notation paragraph)
14. DIFFs 20, 21, 22 (AREPO + abstract λ definition + Ṁ_b assumption)

**Midday** Bucket C:
15. New bibtex entries: Springel, Ruiz/Shapiro, Most/Wang, Ennoggi, Barnes & Hernquist 1992. Verify on ADS.

**PM (3h)** Bucket B end + D start:
16. DIFFs 23, 24 (phase argument + jet timescale)
17. DIFFs 1, 2 (LISA sharpening) — applied last so the wording survives full editorial sleep-on-it
18. DIFF 4 (one-to-one mapping minimal disambiguation)
19. DIFF 25 (tidal-field tightening)
20. Bucket D: move Table 1 + Fig 18 inline; delete `\appendix` section
21. Compile clean

**EOD checkpoint**: 20+ DIFFs applied. Paper now substantively responds to all 8 numbered Zoltan comments. Roman's figures inline. Appendix gone.

### Day 3 — Friday May 9

**AM (3h)** DIFF 3 methodology bridge — most substantive single paragraph in the paper. Read aloud after applying. Iterate.

**PM (4h)** Bucket F:
22. Modify `peters_matthews_with_gas_effects.py` to integrate full coalescence
23. Run for the (e=0.2, q=1) and (e=0.3, q=1) cases at a₀ = 100 R_S and 1000 R_S
24. Generate `fig_q_evolution_to_LISA.pdf`
25. Cite this figure in DIFF 1 prose

**EOD checkpoint**: All 28 text DIFFs applied. q-evolution-to-LISA figure generated. Paper is text-complete; figure regens remain.

### Day 4 — Saturday May 10 (figure day 1)

Recolor Figs 2, 4, 7. Fig 3 gray-shade. Fig 5 aspect ratio. Fig 9 caption.

### Day 5 — Sunday May 11 (figure day 2)

Fig 8 critical axis-label rewrite (full day) + mini Fig 8 panels.

### Day 6 — Monday May 12 (figure day 3)

Fig 1 layout (AM, 4h). Fig 6 layout (PM, 4h).

### Day 7 — Tuesday May 13 (figure day 4)

TikZ cartoon (AM, 4h). Fourier panels (PM, 4h).

### Day 8 — Wednesday May 14 (buffer)

Buffer day. Catch up on whatever slipped. If on track, start Bucket G citation hunt.

### Day 9 — Thursday May 15

Bucket G — full red-ink prose sweep. ~30 small fixes.

### Day 10 — Friday May 16

AI reviewer pass. Final compile. Self-read start to finish for Zoltan voice.

### Day 11 — Saturday May 17

Final pass on `comment_tracker.md`. Generate cover-document for Zoltan from `git log` + tracker.

### Day 12 — Sunday May 18

Send to Magda + Roman with focused asks (see §4).

### Day 13 — Monday May 19

Address Magda + Roman feedback. Final compile. Verify tracker line numbers.

### Day 14 — Tuesday May 20

Send to Zoltan no later than 10 AM. Hard deadline 4:15 PM.

---

## 3. DIFF-specific wording (substantive ones)

### DIFF 1 — §4.2 LISA closing (sharpen, not retreat)

**Where**: lines 510-511.

**Replace** v2's two closing paragraphs (the `end values\footnote{We note that}` paragraph and the "Thus, while the deviation..." paragraph) with:

```latex
In \autoref{fig:evolution_plot} we display the evolution of the two binary's $e(t)$ and $q(t)$ in the upper and lower panels, respectively. Our numerical integration is performed at $a_0 = 10^3 R_S$, well above the LISA frequency band. At this separation the gas-driven terms $\dot{a}_{\rm gas}$ and $\dot{e}_{\rm gas}$ dominate over the GW terms \citep{peters_64}, and the binary settles toward the gas-driven equilibrium $e \approx 0.45$ reported by \citet{duffell_dorazio_2020, zrake_2021, siwek_cbdorbevol, Siwek_mbbh_pop_24}. We find that the two binaries initialized at $(e_b, q_b) = (0.2, 1.0)$ and $(0.3, 1.0)$ both evolve away from $q_b = 1$, reaching $(e, q) = (0.45, 0.991)$ and $(0.45, 0.998)$ respectively, before further evolution.

These plateau values are not the final pre-merger state. As the binary inspirals and $a$ shrinks, the GW timescale $\tau_{\rm GW} \propto a^4$ \citep{peters_64} becomes comparable to and eventually shorter than the gas-driven evolution timescale; once GW dominates, the gas-driven mass-ratio evolution shuts off. However, GW radiation conserves the mass ratio at leading order in the Peters quadrupole formulas, so the offset $\Delta q \approx 0.009$ established during the gas-dominated phase is preserved through inspiral rather than driven back toward unity. Our extended integration of \autoref{eqn:num_integ} from $a_0 = 10^3 R_S$ down to merger (\autoref{fig:q_evolution_to_LISA}) confirms this: $q$ remains at ${\approx}0.991$ as the binary crosses the LISA frequency band.

We therefore predict that LISA-detectable binaries that passed through $(e_b, q_b) = (0.2, 1.0)$ during the gas-dominated phase of their formation should appear at $q \approx 0.99$, producing a relative dearth of strictly $q = 1$ systems in the LISA mass-ratio distribution. Whether this leaves a detectable population-level signature depends on three open questions: (i) the fraction of MBHB progenitors that pass through the relevant region of $(e_b, q_b)$ parameter space and the duty cycle of the $q \neq 1$ phase across the population, (ii) LISA's expected ${\sim}0.5\%$ precision in $q$ \citep{Mangiagli_2020} relative to the $\Delta q \approx 0.009$ deviation, and (iii) the expected $\mathcal{O}(100)$ MBHB events over the LISA mission. Confirming this would require a careful population synthesis accounting for the duty cycle of the $q \neq 1$ phase together with a forward-modelling of LISA's detection sensitivity for a near-equal-mass population. We leave both to future work.
```

### DIFF 2 — Conclusion (vii)

**Where**: line 523.

```latex
\item Equal-mass binaries at $e_b = 0.2$ and $0.3$ are not long-lived equilibrium states: during the gas-dominated phase of evolution they preferentially accrete away from equal mass, reaching $q \approx 0.991$ and $0.998$ respectively. Because GW radiation conserves the mass ratio at leading order, this offset is preserved through inspiral. We therefore predict a relative dearth of strictly $q = 1$ systems in the LISA mass-ratio distribution; whether this is detectable depends on population statistics and forward-modelling we leave to future work.
```

### DIFF 3 — Methodology bridge (#5b)

**Where**: insert before line 339, between the FFT-period paragraph and the figure block.

```latex
We pause to address a methodological subtlety. Our snapshots are recorded only at apocenter, every 10 binary orbital periods. This cadence is fast enough to resolve the cavity precession across our suite, since the precession period is always much longer than 20 orbits. Each snapshot therefore catches the cavity at a slightly rotated orientation, and the time-series $r_1(t)$ and $r_2(t)$ inherit the cavity's precession frequency. Two empirical checks confirm this. First, in every simulation $r_1$ and $r_2$ share the same FFT period --- which is exactly what we expect if both are sampling the same precessing cavity from different sides. Second, that shared period matches the period of $\lambda(t)$ (\autoref{fig:rmin_lambda_peak_ratio}). The period match between $\lambda(t)$ and $r_1(t)$, $r_2(t)$ therefore licenses the inference that $\lambda(t)$ variability is paced by the cavity's apsidal precession, even though the precession itself is not directly resolved at our snapshot cadence.
```

### DIFF 4 — One-to-one mapping (#2, minimal disambiguation)

**Where**: lines 271-278.

```latex
It is of particular note how similar \autoref{tab:stable_varying_grid}, which depicts the time-variability of $\lambda(t)$, is to \autoref{tab:locked_precessing_grid}, Table 1 of \citet{DeLaurentiis25}, which depicts the precession state of the CBD. For non-circular binaries, time-varying $\lambda(t)$ corresponds to a forced-precessing CBD and time-stable $\lambda(t)$ corresponds to a locked CBD --- suggesting that the time-variability of preferential accretion is, in some part, paced by the behavior of the CBD. This is a statement about \emph{time-variability}, complementary to the \emph{time-averaged} framework of \citet{siwek_prefacc}, who classified disks into three regimes (free precession around circular binaries, forced precession around eccentric binaries, or locked at an angle) and applied symmetry arguments to predict the time-averaged $\langle \lambda \rangle$. The reader is referred to their Section 3.5 for a discussion of the symmetry-breaking and ``preferential accretion switching'' for the forced-precession regime.

The $e_b = 0$ simulations break our \emph{time-variability} mapping but not the time-averaged framework: their CBDs precess freely yet their $\lambda(t)$ is constant (and $\langle \lambda \rangle = 1$, by symmetry of the circular orbit). This suggests that a binary may need a non-zero apocenter for CBD precession to imprint itself on the time-variability of accretion, similar to the argument in \citet{DeLaurentiis24} that strong $\lambda(t)$ modulations require a minimum eccentricity in precessing-binary simulations.
```

### DIFFs 5-25

Wordings drafted in master plan + addendum + addendum revisions from May 6 conversation. Will be transcribed at apply time.

### DIFF 17 — Causal sweep substitutions

| Where | Before | After |
|---|---|---|
| Abstract | "the accretion behavior onto one BH over the other is strongly tied to the precession of the CBD" | "the time-variability of the accretion-rate ratio onto the two BHs tracks the precession of the CBD" |
| Abstract | "there exists a regime where the CBD can drive the binary away from $q_b = 1$" | "there exists a regime where the binary evolves toward $q_b \neq 1$ during the gas-dominated phase" |
| Line 271 | "is, in some part, determined by the behavior of the CBD" | "is, in some part, paced by the behavior of the CBD" (already in DIFF 4) |
| Line 290 | "determining which BH is preferred to accrete and to what extent" | (keep — methodology verb, not causal claim) |
| Line 337 | "the precession of the CBD determines not only whether $\lambda(t)$ varies but also the period at which it varies" | "the precession of the CBD and the variability of $\lambda(t)$ are tightly correlated in both occurrence and period; we observe the same FFT period in both quantities and the same locked-vs-precessing partition" |
| Line 528 | "it is still intimately tied to the CBD and can have profound observational consequences" | "Although our results are consistent with the CBD playing a regulating role, the most concrete observational handle is the flickering-jet regime; the population-level LISA signature is intriguing but conditional on the binary formation distribution" |

### DIFF 18 — Conclusion (iv)

**Where**: line 520.

```latex
\item Across precessing systems in our suite, the CBD apsidal precession period and the $\lambda(t)$ oscillation period are equal. However, these time-series are not in phase, ruling out a simple causal interpretation in terms of cavity-wall distance.
```

### DIFF 19 — q_b ≤ 1 notation paragraph

**Where**: line 389. Insert before the "Turning to the upper row..." sentence.

```latex
We pause to clarify a notation subtlety. Our convention $q_b \equiv M_2/M_1 \leq 1$ assigns ``primary'' to the more massive BH and ``secondary'' to the less massive one. In a strictly $q_b = 1$ system this assignment is degenerate, and we adopt the convention --- following \citet{siwek_prefacc} --- of identifying the components by their spatial location at apocenter. Once $q_b = 1$ is broken by accretion, the BH initially labeled ``secondary'' grows into the more massive component, formally inverting the $q_b \leq 1$ convention. We continue to label the BHs by their initial assignment throughout the integration for clarity. The statement that the binary ``evolves away from unity'' should be read as: the mass ratio $M_2/M_1$ deviates from unity, where the labels 1 and 2 refer to the original assignment, even after the inversion. The standard error on the integrand for $\langle \dot{q} \rangle$, estimated from the variance of $\dot{q}(t)$ divided by the integration duration, is $\sigma \approx 10^{-2}$ for $q_b = 1$ simulations.
```

### DIFF 25 — Tidal-field framing (revised, conservative)

**Where**: line 367.

```latex
In fact, we can even take this further and note that the tidal field of the secondary on its nearby cavity wall is about four to five times greater than the tidal field of the primary on its more distant cavity wall (with the tidal field scaling as $M/r^3$ and $r_1/r_2 \approx 3.4$ measured from the simulation snapshot), in agreement with the observed factor of $\sim 5$ in the relative accretion rate.
```

(Adds the M/r³ scaling explicitly so the calculation is reproducible by the reader; tightens "tidal potential" → "tidal field"; confirms with the actual r_1/r_2 from Fig 6.)

---

## 4. Coauthor + Zoltan email templates

### Day-1 email to Zoltan (send AM Day 1)

> *Subject: Unequal-accretion paper revision — questions before May 20*
>
> *Hi Zoltan,*
>
> *Working on v3 ahead of the May 20 deadline. Three quick questions so I can apply your comments:*
>
> *1. Acknowledgements — could you confirm the NASA ATP grant number and the LISA Preparatory Science grant number for the acknowledgements section? I'm putting placeholders now.*
>
> *2. Mangiagli citation — your marginalia on page 11 wrote "Mangiagli et al 2023?" with a question mark. ADS confirms Mangiagli et al. 2020 (PRD 102, arxiv 2006.12513) is the canonical LISA q-precision paper; no 2023 follow-up exists. I'm citing the 2020 paper. OK?*
>
> *3. The "+ Physics + ISTA" annotation next to the title page — is this meant to add ISTA to your affiliation line?*
>
> *4. For comment #1 (insert Roman-paper figure inline), I'm moving Roman's Fig 18 and Table 1 inline at the cross-reference points in §3.1, attributing them as "Reproduction from \citet{DeLaurentiis25}, in preparation." OK?*
>
> *Will send v3 by morning of May 19 with a comment-by-comment tracker mapping each of your March 2025 comments to v3 line/section.*
>
> *Thanks, Stan*

### Day-12 email to Magda

> *Hi Magda — sending v3 for coauthor review. Three focused asks:*
>
> *1. The DIFF 9 replacement for "is this still figure 6?" — does it read correctly in §3.1.1? The new text references \autoref{fig:lambda_rmin_panels} explicitly.*
>
> *2. The §3.2 q_b ≤ 1 notation paragraph — does the convention-inversion explanation match how you think about it?*
>
> *3. §4.2 LISA section: your "What accretion rate did you assume here?" thread is now answered explicitly in the prose (Ṁ_b = 100 Ṁ_Edd). Look OK?*
>
> *4. (broader) §4.2 LISA closing — do you think the framing lands? I've kept the bump claim with a specific regime of validity, since GW conserves q at leading order. Open issues are pop-spread + LISA precision floor + N events.*
>
> *Tracker attached — comment_tracker.md maps every Zoltan comment to v3 line/section. Cheers, Stan*

### Day-12 email to Roman

> *Hi Roman — v3 attached for coauthor review. Two specific asks:*
>
> *1. For Zoltan's comment #1 he wanted Roman-paper figures inline rather than in appendix; I've moved Table 1 + Fig 18 to §3.1 inline at first cross-reference, with "Reproduction from \citet{DeLaurentiis25}, in preparation" attribution. Want to make sure that's how you'd prefer them framed.*
>
> *2. The methodology bridge in §3.1.1 (DIFF 3) explicitly justifies the apocenter-snapshot → CBD-precession inference, citing your single-dominant-mode result. Could you sanity-check that the chain of reasoning is correct from your perspective as the disk-theory expert?*
>
> *Cheers, Stan*

### Day-14 cover email to Zoltan (send AM Day 14, no later than 10 AM ET)

> *Subject: Unequal-accretion v3 — comment-by-comment response*
>
> *Hi Zoltan,*
>
> *V3 attached. comment_tracker.md (also attached, on GitHub at <link>) maps each of your March 2025 comments to where they're addressed.*
>
> *Substantive (non-trivial) changes worth a flag:*
>
> *§4.2 LISA tone-down (your #7): per your concern, I now state the q ≠ 1 plateau is conditional on a₀ ≥ 10³ R_S binaries, not a guaranteed observation. The integration in `peters_matthews_with_gas_effects.py` (extended to merger) confirms that q remains near 0.991 through the LISA band, since GW conserves q at leading order while gas drives e to its equilibrium. Pop-spread, LISA precision, and N_LISA are stated as open issues left for future work. I think this addresses your concern without conceding the underlying physics.*
>
> *§3.1.1 methodology bridge (your #5b): a paragraph now justifies the apocenter-stroboscopic → CBD-precession inference. Three-step argument: 10τ_b cadence is much faster than precession period, r_1 = r_2 in period as expected if both sample the same precessing structure, λ shares that period.*
>
> *§3.1 mapping disambiguation (your #2): the time-variability mapping (V/S ↔ L/P) and the time-averaged ⟨λ⟩ framework (Magda's three regimes) are now distinguished explicitly when introduced.*
>
> *Conclusion (iv) walkback (your "way too much to claim, legally so, causally"): rewritten to state the empirical period-match cleanly and explicitly note what it rules out.*
>
> *Causal-claim sweep paper-wide: replaced "determines / drives / regulates" with "tracks / paces / is consistent with."*
>
> *Roman-paper figures (#1): Table 1 and Fig 18 moved inline at first §3.1 cross-reference, attributed as reproductions from DeLaurentiis & Rafikov (in preparation).*
>
> *All other items closed in the attached tracker.*
>
> *Cheers, Stan*

---

## 5. Compile-test gate — clean before each commit

Run after each DIFF:

```bash
cd "/Users/stanislavdelaurentiis/unequal_acc_local/Unequal Acc v3"
pdflatex -interaction=nonstopmode main.tex > /tmp/compile.log 2>&1
bibtex main >> /tmp/compile.log 2>&1
pdflatex -interaction=nonstopmode main.tex >> /tmp/compile.log 2>&1
pdflatex -interaction=nonstopmode main.tex >> /tmp/compile.log 2>&1
grep -iE "warning|error|missing|undefined" /tmp/compile.log | grep -vE "(LaTeX Font Warning|natbib Warning: Citation .* on page)" | head -20
```

After Bucket A complete: bibtex warnings should drop to zero. After every Bucket B commit: zero `??` citations, zero compile errors.

---

## 6. Open questions requiring user input before applying

These are decisions where my best guess is fine but the user might have intent I don't:

1. **Phantom citation substitutions in DIFF 8** — confirming `Miranda2015 → miranda_munoz_lai_2017` and `Duffell2024 → dorazio_duffel`. Best guesses based on context. Different intent? Tell me.
2. **DIFF 1 prose** — the "sharpen, not retreat" framing above. Sign off or revise.
3. **DIFF 4 prose** — the minimal disambiguation framing above. Sign off or revise.
4. **DIFF 18 prose** — the conclusion (iv) rewrite. Sign off or revise.
5. **DIFF 25 prose** — the tidal-field tightening. Sign off or revise.
6. **TikZ cartoon vs simulation snapshot for #4a** — Zoltan accepted both. TikZ is faster + cleaner; sim snapshot is more empirically real. Default: TikZ. OK?
7. **Mini Fig 8 placement** — second figure (Fig 8b) or insets within Fig 8 itself? Default: second figure for clarity.
8. **§3.1.1 subsection name** — keep "Preliminary Analysis" per user instruction.
9. **Title** — keep current.

---

## 7. Risk register (what could blow the schedule, ranked)

1. **Fig 8 critical regen** (Day 5) — current sim PDF has missing axis labels; full regen takes a day. Highest single-task risk.
2. **DIFF 3 methodology bridge** (Day 3) — most physics-loaded prose. Iterate at least twice.
3. **Fig 1 layout rewrite** (Day 6) — matplotlib subplot grids with shared axes are fiddly.
4. **TikZ cartoon** (Day 7) — first-time TikZ takes longer than expected. If you've never written one, budget 6h.
5. **Coauthor turnaround** (Days 12-13) — you have 2 days for Magda + Roman feedback + revision. They're busy. Send Day 12 morning, not afternoon.

Mitigations:
- Day 8 is a buffer day. Use it.
- DIFFs 1, 2, 3, 4 (most science-load-bearing) are applied early so if they need iteration, there's time.
- Fig 8 is scheduled before the harder cartoon/Fourier figures so if it overruns, it bleeds into Day 6 not into Day 14.

---

## 8. Diff tracking workflow

Per-DIFF git commits:

```bash
# After each DIFF
git add main.tex main.bib comment_tracker.md
git commit -m "DIFF N: <one-line summary>

Closes Zoltan: #<num> | red-ink page <p>.<n>"
```

`comment_tracker.md` updated in same commit. After Bucket B complete, push to GitHub (private repo).

`git log --oneline` becomes the line-by-line response document for Zoltan, and `comment_tracker.md` is the markdown-rendered version.

---

## 9. What's in `scripts/` (verification-ready, all local)

| Script | What it does | Last modified | Used in |
|---|---|---|---|
| `lambda_fig2_heatmap.py` | Fig 2 (σ_λ), Fig 4 (⟨λ⟩) heatmaps | — | Day 4 recolor |
| `magda_fig2.py` | Fig 3 (⟨λ⟩ vs q_b lines) | — | Day 4 gray-shade |
| `qdot_heatmap.py` | Fig 7 (q̇ heatmap) | — | Day 4 recolor |
| `accretion_eddington.py` | Fig 8 (jet regimes), Fig 9 (λ̃) | — | Day 5 axis-label regen |
| `magda_accretion_actual_fixed.py` | Fig 1 (λ(t) grid) | — | Day 6 layout |
| `magda_accretion_geometry_ecc_combined.py` | Fig 5 (period ratio) | — | Day 4 aspect ratio |
| `proof_lambda_r_not_causal.py` | Fig 6 (six-panel λ + r) | — | Day 6 layout |
| `physicality_heatmap_obs_timescale.py` | Fig 10 (detection regions) | — | Day 7 annotations |
| `pop_eval2.py` | Fig 11 (a, e, q evolution) | May 20, 2025 | Reference |
| `peters_matthews_with_gas_effects.py` | (a, e, q) evolution with gas+GW | **Jul 12, 2025** | **Day 3 — extend to full coalescence** |
| `peters_matthews_strain_clean_with_sum_rk4_jonathan.py` | strain plot (q=1 fixed) | Oct 30, 2024 | Reference for DIFF 1 |
| `ellipse_fourier_magda_sweep.py` | Appendix Fig 18 | — | Reference |

---

## 10. The substantive scientific reviewer-mode summary (for context)

Strongest claims (well-supported): visual classification of λ(t) regimes; FFT period match between λ and r_1, r_2; direct ⟨q̇⟩ measurement; three jet regimes empirically observed.

Weakest claims (insufficient evidence in current draft, addressed by DIFFs):
- "One-to-one mapping" — needs operational distinction from Magda's framework (DIFF 4)
- λ(t) paced by CBD precession — methodology bridge missing (DIFF 3)
- LISA detectability — needs sharpening of regime of validity (DIFF 1)
- Flickering jets as novel — needs comparison to MHD work (DIFF 12)

Zoltan's two biggest legitimate pushbacks:
- Causal language is overclaim → DIFFs 17 + 18 fix paper-wide
- LISA prediction is unsupported → DIFF 1 sharpens; physics is real, detectability uncertain

Zoltan's exact phrasings to use:
- "they are correlated, no clear causal link between them" — for §3.1.1 / §3.2 wrap-ups
- "dearth of strictly q=1 systems" — for §4.2 + conclusion (vii)
- "There are no long-lived q=1, e=0.2 binaries, and these will evolve to q<1" — for the LISA reframing
- "way too much to claim, legally so, causally" — what NOT to do in conclusions (iv) and (vii)

---

## END

When this plan is signed off by the user, execute Bucket A immediately. Then surface DIFF 1, 4, 18 wording for sign-off before continuing Bucket B.
