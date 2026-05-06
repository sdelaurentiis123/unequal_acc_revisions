# Annotation Review: *Preferential Accretion onto Eccentric and Unequal Binary Black Hole Systems*

**Manuscript date:** March 21, 2025 (compiled) / Mar 24, 2025 (uploaded version)
**Authors:** DeLaurentiis, Haiman, Siwek, Rafikov

---

## Sources of Comments

The PDF carries **two distinct layers** of feedback that need to be untangled when revising:

| Source | Format | Identity | Tone |
|---|---|---|---|
| **MSS** | Typed inline `[MSS: ...]` blocks already embedded in LaTeX | Magdalena Siwek (co-author, owner of simulation suite) | Detailed technical/structural co-author edits |
| **SOD** | Typed inline `[SOD: ...]` responses | Stan's own responses already drafted | Mostly already addressed, a few open questions |
| **Handwritten** | Red/orange ink throughout margins | Almost certainly **Zoltan Haiman** based on style (advisor-level critique, "Thank my NASA ATP" acknowledgment note, depth of physics challenge) | Pointed, often skeptical of overclaims; many notation/figure cleanups |

**Strategic note:** The handwritten reviewer is the harsher of the two — pushing back on causal claims, demanding self-contained captions, and challenging the disk-physics interpretation in Section 3.1.1. These need to be addressed *before* MSS's points are fully closed out, because several MSS comments are about presentation but the handwritten ones cut at scientific substance.

---

## Cross-Cutting Themes

These show up across multiple sections — fix them globally rather than piecemeal:

### 1. Notation consistency
- **Define `λ ≡ Ṁ₂/Ṁ₁`** explicitly in the abstract and intro (the handwritten note in the abstract margin makes this point: *"λ ≡ M₂/M₁"* — though this is slightly garbled in the margin, the intended definition is the accretion-rate ratio).
- **Define `q̇ ≡ d/dt(M₂/M₁)`** explicitly as a function of `e_b` and `q_b`.
- **Choose `q` or `q_b` and stick with it.** Page 11 explicitly flags: *"Also, be consistent, q or q_b?"*
- **Subscript convention**: `q_b ≡ M₂/M₁ ≤ 1` (margin reminder on page 2, with `q_b` constraint).
- **`(e_b, q_b)` ordering**: handwritten suggestion on page 3 says *"I suggest the notation `(e_b, q_b) = (0.3, 0.3)` throughout the paper"* — the manuscript currently flips between `q_b, e_b` and `e_b, q_b`. Pick one ordering and propagate.

### 2. Citations to add
A running list of references the reviewer flagged as missing:
- **Barnes & Hernquist (1996/199x)** — for material funneled to galactic center during merger (page 1).
- **D'Orazio (2013)** — *"Also cite Dan's 2013 paper (1st to look at periodogram of λ as a function of q)"* — first periodogram analysis of λ(q). Currently cited for other claims but not for this priority result. (Page 1)
- **Farris et al. 2014** and **Duffell et al. 2017** — for accretion variability in eccentric/unequal binaries (page 1).
- **Munoz et al. 2017** for eccentricity discussion (page 1).
- **Miranda, Muñoz et al. 2017** for disk *locking* discussion specifically (page 3 margin).
- **Artymowicz 1983** — confirm whether this is the same paper cited in Zrake+2023 (page 2 margin question). MSS confirmed she also couldn't find it.
- **Stu Shapiro's MHD binary jet sims** + **Elias Most** — for jet discussion in Section 4.1 (page 9 margin).
- **Peters 1964** — for the GW circularization/inspiral formulas (`ȧ_GW`, `ė_GW`) on page 11. The current formulas are stated without citation.
- **Mangiagli et al. 2023** — for LISA `q_b` precision claim (page 11). Stan's own SOD note says he was "unable to find/remember the source"; the handwritten note supplies it.
- **Siwek+2024** (population statistics paper) — MSS asked for this on page 11; SOD marked done but worth verifying it made it in.

### 3. Figure formatting (recurring complaints)
- **Captions are not self-contained.** Specifically called out for **Fig. 6** (page 7: *"Explain these... captions need to be self-contained"*) and **Fig. 9** (page 10: *"Define for readers who haven't read the text"*). Fix this for *every* figure — assume a reader skimming figures has not read the surrounding prose.
- **Axis label sizes too small** — MSS flagged this for Fig. 8 (page 8); the handwritten reviewer flagged it for Fig. 1 (*"Also label must be at least the same size as the main text"*) and Fig. 10 (*"increase the size of the axis labels"*).
- **Panel grids should touch.** For Fig. 1 (page 4) and Fig. 6 (page 7), the reviewer wrote: *"Since x and y axis range and labels are the same in each panel, you don't need to include these in each panel. Instead, you can save a lot of space by making the panels touch."*
- **Aspect ratios inconsistent** — page 6 (Fig. 5): *"make aspect ratio the same as in Figs 2 and 4"*.
- **Recoloring requested** for Fig. 2 (#1) and Fig. 4 (#3) — the heatmap colormaps are flagged with circled "recolor" notes.

### 4. MNRAS style
- **Section/subsection capitalization**: page 2 — *"MNRAS does not capitalize title words except the first..."* — flagged on "Disk Theory" subheading. Audit *all* section headings: §3.1 "Preferential Accretion" → "Preferential accretion", §2.1 "Simulation Setup" → "Simulation setup", etc.
- **Use `\citealt`** for non-parenthetical citations (page 1 margin).

### 5. Overclaiming on causality
The single sharpest critique. Multiple instances:
- Page 7 margin: *"they are correlated, there is no clear causal link between them"* — re. CBD precession ↔ λ(t) period.
- Page 12 (Conclusions item iv) — handwritten: *"way too much to claim, legally so, causally!"* — re. statement that CBD precession and λ(t) oscillation share periods.
- Throughout Section 3.1.1, the reviewer is hammering on the same point: similar timescales are *not* a causal link.

**Action:** Soften causal language → "consistent with", "correlated with", "tied to" rather than "determines", "regulates", "causes". Especially in the Summary.

---

## Page-by-page detailed breakdown

### Page 1 — Title, Abstract, Introduction (start)

#### Title
- A handwritten *"+ Physics + STA"* appears next to the title — unclear if this is a category tag the reviewer added for filing or a content note. Likely just an author tag (Stan = STA?). **Treat as ignorable filing mark unless it recurs.**
- Several title words are circled (*Eccentric, Unequal, Binary, Black Holes*) — likely just the reviewer marking what they are about to comment on; no specific change implied.

#### Abstract
| Location | Annotation | Action |
|---|---|---|
| "...gravitational torques and accretion" | *"forces"* added | Consider "gravitational forces and accretion" or rephrase to be more general. |
| "circumbinary disks (CBDs)" | "ies" added | Plural — "consequences" later in sentence may need similar pluralization check. |
| "ratios (q_b)" definition | Margin: *"λ ≡ M₂/M₁ , and the corresponding rate of change of the mass ratio... this asymmetry q̇ ≡ d/dt(M₂/M₁) as functions of e_b and q_b"* | **Add an explicit definitional sentence to the abstract**: define λ and q̇ as the two key quantities reported, before describing what's measured. |
| "we report the most extensive series of measurements **for λ̇, the rate of change of the binary mass-ratio, and λ(t)**" | Strikethrough on "for λ̇... and λ(t)" — reviewer wants the abstract to flow into the *findings* directly without the parenthetical | Trim the appositive; let the definitions live in a preceding sentence. |
| "the ratio of the BH accretion rates" | underlined / kept | Keep but tied to the new definition sentence. |

#### Introduction (column 1)
| Location | Annotation | Action |
|---|---|---|
| "Cosmic structure forms hierarchically and galaxy mergers..." | *"and binary stars"* added in margin | Acknowledge that the same physics applies to binary stars / protoplanetary disks — broadens the relevance framing. |
| "with" — small insertion mark | minor edit | Just word-level cleanup. |
| "inter-stellar medium from the proto-galaxies are funneled to the galactic center" | *"Barnes & Hernquist (199x...)"* | Add Barnes & Hernquist citation here. |
| "Lubow 1991; Whitehurst 1994..." citation list | *"Use \citealt"* | Several citation lists need `\citealt` for non-parenthetical use. |
| "Tiede et al. 2020; Zrake et al. 2021..." citation list | *"Munoz et al (for eccentricity) 2017"* | Add Munoz 2017 to the list discussing CBD-driven eccentricity changes. |
| "Westernacher-Schneider et al. 2022)" end of paragraph | *"Also Farris+2014, Duffell+2017?"* | Add these two for accretion variability claims. |
| "(q_b > 0.7)" | Reviewer circled "> 0.7" with a query | Likely should be `≥ 0.7` based on the Siwek+23a result; verify and adjust. |
| Final paragraph margin | *"Also cite Dan's 2013 paper (1st to look at periodogram of λ as a function of q)"* | **Important historical credit** — D'Orazio 2013 was the first periodogram analysis of preferential accretion; cite as such, not just as a generic CBD reference. |
| "60+ citations" mark "(or 14?)" | Margin question on a citation count | Verify whatever number the prose claims. |

---

### Page 2 — Introduction (continued), §2.1, §2.2

#### Introduction column 1 (top)
| Location | Annotation | Action |
|---|---|---|
| Paragraph beginning "Siwek et al. (2023a) reported time averaged values..." | Margin "S23" / "S23" tags | Reviewer is marking these as Siwek+23a-specific paragraphs to track scope. |
| "the secondary tends to accrete, on average, at a greater rate than the primary" | *"found that can"* — a phrasing repair | Revise: e.g., "It has been found that the secondary tends to accrete..." or similar. |
| "For ≤ 100 τ_b they found that the primary can out-accrete the secondary" | *"to date"* / *"near the secondary"* | Add "to date" qualifier somewhere in this section to indicate the lit-review terminus. |
| "Despite these efforts we are still yet to fully characterize" | "primary (?)" margin | Reviewer questioning whether "primary" is the right framing here. |
| "Thus, in the following work we build on Siwek et al. (2023a) and, with the consent of the authors..." | *"add 1-2 sentence explanation of three"* (referring to the three findings to be reported) | **Add a roadmap sentence** spelling out the three contributions of the paper at this hinge point. |

#### §2.1 Simulation Setup
| Location | Annotation | Action |
|---|---|---|
| Heading | *"and refer readers to"* | Suggests phrasing like "we briefly describe... and refer readers to Siwek et al. (2023a,b) for...". |
| "Siwek et al. (2023a,b) performed 2D hydrodynamical simulations..." | *"density and temperature profiles"* | Note that the disk is initialized with density *and* temperature profiles, not just a power-law. |
| "$j∧{from rh3}$" in margin near sink particle equation γ₀(1 - r_ij/r_s)² | LaTeX scratchpad — likely the reviewer working out the formula structure | Verify the formula is rendered correctly; the reviewer wants to see clearly which gas-cell quantities are being summed. |
| "the moving-mesh code AREPO" | *"(REF)"* | Add AREPO citation (Springel 2010). |
| "linear momentum." | *"from the gas cells"* | Specify "linear momentum from the gas cells". |
| "Voronoi tessellation" | "Voronoi" — small clarification | Confirm phrasing. |
| "snapshots recorded at apocenter" | *"adjust settle?"* | Reviewer questioning whether the disk has actually relaxed by the time of recording — flag for §2 discussion of equilibration. |
| Paragraph end | "list these in Zrake 2023" | Possibly suggesting that one of the lists in this section be replaced/cited with Zrake+23's enumeration. |

#### §2.2 Disk Theory
| Location | Annotation | Action |
|---|---|---|
| Heading "Disk Theory" | *"MNRAS does not capitalize title words except the first..."* | **Style fix**: rename to "Disk theory". Audit ALL headings for this. |
| "Gas eccentricity within CBDs is expected to grow through mechanisms such as eccentric Lindblad resonances (ELRs) or spiral shock pumping" | *"maybe delete: this can only operate in test particles or do you mean shocks in gas stream crossings"* | **Substantive challenge**: the reviewer questions whether ELRs operate in a non-test-particle gas — they may want this clause replaced with the more accurate "shock pumping at stream crossings" mechanism. Either remove the ELR mention or qualify it carefully. |
| "have found significant eccentricity near the inner edge" | *"the inner regions of eccentric"* — phrasing edit | "have found significant eccentricity in the inner regions of the disk" probably the cleaner phrasing. |
| Paragraph on cavity precession | *"is this the one cited in Zrake+2023?"* (re Artymowicz 1983) | Flag — confirm or remove the Artymowicz reference. MSS already noted she couldn't find it. **Decision needed**: cite via secondary source or cut. |
| "DeLaurentiis & Rafikov (2025)" | Reviewer notes the cross-reference | This is Stan's companion paper — make sure both are submitted/available together. |
| Page bottom — handwritten: "$q_b = M_2/M_1 ≤ 1$" + "BH" | Notation reminder | Confirm `q_b ≤ 1` convention is stated in §2.1 explicitly. |

---

### Page 3 — §2.3 Numerical Techniques, §3 Results

#### §2.3 Numerical Techniques
| Location | Annotation | Action |
|---|---|---|
| Heading "Numerical Techniques" | *"lower case"* / *"orientation"* | Headings → sentence case (MNRAS style). The "orientation" note may refer to figure orientation elsewhere. |
| "is likewise" margin | minor | Phrasing repair near "the shape of the CBD is inherently time-dependent". |

#### §3.1 Preferential Accretion
| Location | Annotation | Action |
|---|---|---|
| Section opening "In Fig. 1 we plot our λ(t) time-series..." | *"The most striking feature"* — proposed opening rewrite | **Rewrite the lede**: e.g., "The most striking feature of Fig. 1 is the broad division of λ(t) into time-stable vs. time-varying regimes." (Punchier than "What first strikes us..."). |
| Notation throughout | *"I suggest the notation `(e_b, q_b) = (0.3, 0.3)` throughout the paper"* | **Global notation pass**: pick `(e_b, q_b)` ordering and use it everywhere. |
| "near-constant value" | *"constant"* — possibly "as much as" | Tighten language. |
| "(e_b = 0., q_b = 0.3)" footnote | *"noise"* — i.e. the modulation around constant value is just noise | Clarify whether the modulation in this case is statistically significant or just simulation noise. |
| "It is of particular note how similar Table 1... is to Table 1 of DeLaurentiis & Rafikov (2025)" | MSS: *"Can you clarify which table?"* — SOD says he meant to send that paper too | This needs the companion paper to be available; otherwise, **inline the relevant content** rather than relying on a cross-reference. |
| "Siwek et al. (2023a) described the disk as exhibiting three distinct regimes: free precession, forced precession, or a locked disk" | *"Also Miranda Munoz et al 2017 discussed locking, we should cite them too"* | Add Miranda+17 to this citation. |
| Comment thread MSS↔SOD on locking and λ=1 | SOD note: *"please correct me if I'm wrong, and let me know how it is best to approach this"* | **Open conversation with MSS** — the framing of how Siwek+23a's symmetry argument relates to your finding needs to be settled with her before submission. |
| Footnote 2 on dichotomy | *"some... might"* — softening | Hedge the strong dichotomy claim. |

#### Margin commentary about q_b=1 binaries
- Handwritten: *"a dearth of binaries with mass ratio precisely q_b = 1"* — proposed phrasing for the population claim. This is the formulation the reviewer prefers over "dearth of equal-mass binaries". **Use this language.**

---

### Page 4 — Figure 1 (full-page) and discussion

#### Figure 1
**Major formatting overhaul required:**
| Issue | Reviewer's exact note | Action |
|---|---|---|
| Repeated axis labels | *"Since x and y axis range and labels are the same in each panel, you don't need to include these in each panel. Instead, you can save a lot of space by making the panels touch."* | Remove per-panel axis labels; share axes; concatenate panels into a tighter grid. |
| Label size | *"Also label must be at least the same size as the main text."* | Bump font sizes. |
| Caption — y-axis | *"M₂/M₁"* and *"entire"* added | Caption should specify `λ ≡ Ṁ₂/Ṁ₁` and clarify "for our entire binary simulation suite". |
| Caption — x-axis | *"in units of binary orbital time"* | Add units explicitly: "time on the x-axis (in units of binary orbital time)". |
| Caption — axis growth direction | small edits | Fine-tune the description of column/row directions. |

#### Body text (after Fig. 1)
| Location | Annotation | Action |
|---|---|---|
| "we note that there seems to be a relationship between the amplitude..." | *"is a clear correlation"* — phrasing upgrade | Strengthen from "seems to be a relationship" → "There is a clear correlation between the amplitude of λ(t) oscillations and `e_b`." (But mind the causal-claim caution from earlier — *correlation* is fine.) |
| "the σ_λ" | *"the"* / "amplitude of" | Article and clarification edits. |
| Footnote 3: "we make a cut at 3000 orbits" | *"can you explain this? do you mean orbit #'s or 3000 t were used? N = ?"* | **Explain the cut**: how many time-points remain after the cut? Why 3000 specifically? Is this a physical timescale (viscous time?) or just empirical? |

---

### Page 5 — Figures 2, 3, 4

#### Figure 2 (σ_λ heatmap)
- Circled note: **"recolor #1"** — current colormap is unsatisfactory.
- Action: try a perceptually uniform sequential map (viridis, plasma) consistent with the publication's other heatmaps.

#### Figure 3 (⟨λ⟩ vs q_b, color = e_b)
- *"Time-averaged value of the accretion-rate ratio λ, as a function of..."* — proposed caption rewrite, more pedagogical.
- *"shade in gray (?)"* with hatching mark on the y > 1 region — **suggestion to gray-shade the regime above λ=1** to visually emphasize "preferential accretion onto secondary" region. Strong suggestion; do it.
- *"this figure"* — minor pointing.

#### Figure 4 (⟨λ⟩ heatmap across e_b, q_b)
- Circled: **"recolor #3"** — same colormap issue as Fig. 2.
- Caption critique: existing text "More eccentric, more unequal mass binaries seem to accrete more preferentially, though the trend is not monotonic" — reviewer marks this around the caption. Likely wants a tighter caption with self-contained definition of ⟨λ⟩.

#### Body text
| Location | Annotation | Action |
|---|---|---|
| "Namely, we find that σ_λ seems to display a modest trend" | *"display a modest"* — light edit | Consider "Namely, σ_λ increases with e_b, peaking at e_b = 0.6." |
| "We too find that the ⟨λ⟩ of the e_b = 0..." | *"In particular"* added | Add transition word. |
| "we ~~note that~~ all our unequal-mass simulations" | strike-through on "note that" | Tighten. |
| "should we actually do a regression and report error values on this?" (SOD's own note) | Margin: *"not sure if needed"* | **Don't bother with regression** — reviewer says it's not needed. |
| "biased towards the secondary" | minor edits | small phrasing fixes. |

---

### Page 6 — §3.1.1 Preliminary Analysis, Figure 5

#### Figure 5 (period ratio τ_λ / τ_r₁)
- Annotation: *"make aspect ratio the same as in Figs 2 and 4"* — currently this figure is taller/narrower than its siblings.
- *"variability"* — reviewer adds in caption.
- *"maybe 'unstable' B/c its periodic..."* — possibly suggesting different label for ratio = 1 cells.

#### §3.1.1 Body — substantive critiques
This is the section the handwritten reviewer is most agitated about. Document each:

| Location | Annotation | Severity |
|---|---|---|
| Definition of `r_cav(θ)` and r₁, r₂ | **"this is not defined. Where is 'r' measured from? The center of mass? Or from each BH?"** | **CRITICAL CLARITY ISSUE** — the entire geometric argument hinges on this distance metric. Define unambiguously which origin is used and why. |
| "Since our BH positions are fixed—as we only record snapshots at apocenter" | *"it is not totally obvious that BHs are always closest to the cavity at their apocenter"* | **Substantive challenge** — the reviewer doesn't accept that apocenter is necessarily the closest-approach configuration. Justify or reframe. |
| "A first step in determining the relationship between preferential accretion..." | *"determining the flow rates"* — tweak | Phrasing. |
| "We have already determined that, except for the e_b = 0 case..." | *"a is similar to that between"* | Rewriting suggestion for transition. |
| "To determine the period of each time-series we first calculate a fast Fourier transform (FFT)" | Highlighted, with question marks | Reviewer wants more rigor — possibly include error bars on the FFT period estimate, or describe windowing. |
| "though certain binaries have ratios that deviate from unity" | *"clear"* / *"unity"* — clean phrasing | Tighten. |
| "Thus, we find that the precession of the CBD determines not only whether λ(t) varies but also the period at which it varies." | The whole sentence is challenged in the next page's annotations as overclaiming | **Soften causal "determines" → "is correlated with"**. |
| "this holds also" margin | edit suggestion | minor. |
| Reviewer wraps the discussion of Fig. 6: *"Comment?"* + *"this section needs a clear/causal link"* | flagged | The whole §3.1.1 needs a thesis statement: "we find correlation but not causation between cavity geometry and λ(t)". |

#### Naive explanation paragraph
| Location | Annotation | Action |
|---|---|---|
| "if one black hole is significantly closer to the inner edge..." | *"could"* / *"tial"* (potential?) | Soften assertions. |
| "we see what we would expect from our naive explanation" | *"yes"* / *"I am"* — author voice | Reviewer marking what works. |
| "the tidal potential on the gas by the secondary is about four to five times greater" | *"~three times (?)"* — challenge to the factor | **Recheck the numerical estimate** — reviewer thinks 3× not 4–5×. Re-derive from M₂/M₁ ratio. |
| Footnote/end | *"why?"* / *"hypothesis"* / *"shortest"* | Reviewer wants the *causal hypothesis* to be made explicit in one sentence. |

---

### Page 7 — Figure 6, §3.2 Mass Ratio, Figure 7

#### Figure 6 (six-panel λ(t), r₁(t), r₂(t) comparison)
| Issue | Reviewer's note | Action |
|---|---|---|
| Panel size | *"make panels bigger by concatenating them"* | Same fix as Fig. 1 — share axes, remove per-panel labels. |
| Caption | *"Explain these... captions need to be self-contained"* | **Major caption rewrite required**. Currently caption assumes reader has read body text. Spell out: what colors mean, what dual y-axis represents, what the conclusion is. |
| Caption phrase "BH's position with respect to the cavity does not determine the components' relative accretion rates" | *"by the colour scale" / "in"* edits | Tighten phrasing. |

#### Body text
| Location | Annotation | Action |
|---|---|---|
| "From the above analysis it is clear that ~~that~~ the naive explanation..." | dup-word strike | minor. |
| "While the variability and periods of both are linked, they are far from causal." | **"they are correlated, there is no clear causal link between them"** | **Rewrite this sentence directly using the reviewer's language** — clearer than "far from causal". |
| "Preliminary further analysis has suggested that the deviations..." | "*not* this *interpretation*" / "*in*" / "determining the flow rates" | Reviewer doesn't like this teaser. Either commit to the result or remove the speculation. |
| "...will be explored in a forthcoming paper." | *"plethora"* in margin | Reviewer suggests describing the *zoo* of behaviors as a "plethora". Might be a stylistic preference. |
| MSS comment thread "section 3.5 in Siwek+23a" | already addressed by SOD | Verify the addition. |

#### §3.2 Mass Ratio — opening
| Location | Annotation | Action |
|---|---|---|
| First mention of `q̇` definition | *"Eq. 1"* margin | Reference Eq. 1 explicitly when first using `q̇`. |
| "What first strikes us in Fig. 7..." | *"A striking feature"* — same lede edit as before | Rewrite opener for punch. |
| "?" question marks | flagged | Several places where the reviewer wants more explanation. |
| Footnote on top row negative values | *"top row is negative I agree w/ Magda"* | Reviewer agrees with MSS's earlier suggestion of diverging colormap; *however*, SOD notes all values are positive. **Reconcile**: are the values in the q_b=1 row truly all-positive, or are some marginally negative? If marginally negative due to noise, a diverging colormap centered at zero makes sense. |
| "how did you determine this?" — re. footnote 6 about standard error | flagged | Show the calculation — what's the SE estimate? |

#### Discussion of the "naive explanation breaks down"
| Location | Annotation | Action |
|---|---|---|
| "...display such behavior. The former displays that both r₁ and r₂ are π/4 out of phase" | *"why opposite? this is in fact what you state two sentences earlier as the expectation (although I didn't understand the reason...)"* | **Reviewer is genuinely confused about the phase argument.** Walk through the geometry pedagogically: what would in-phase mean, what would out-of-phase mean, what does π/4 mean. Possibly add a small schematic. |
| "the latter displays the exact opposite to our naive expectation" | *"why? not clear to me why r₂ should be out of phase"* | Same confusion — make the naive prediction explicit before stating the deviation. |

---

### Page 8 — §3.2 (continued), §4.1 Flickering Jets

#### Top-of-page (q_b=1 binaries accreting away from unity)
| Location | Annotation | Action |
|---|---|---|
| First sentence "(q_b, e_b) = (1, 0.2) and (1, 0.3)" | *"equal-mass"* margin | Add "equal-mass" to clarify these are q_b=1 cases. |
| "the 'secondary' BH is growing more massive" | *"presence/absence of"* margin | Possibly suggesting the section heading or framing. |
| "this non-zero ⟨q̇⟩ means that the binary is in fact being fed in such a way that it is evolving away from unity" | *"heh? what do you mean? until now you said q_b = M₂/M₁..."* | **Notation crisis here** — if q_b ≤ 1 by convention, then "evolving away from unity" needs careful handling: the labels of "primary" and "secondary" *swap* mid-evolution. The reviewer is genuinely confused. **Add an explicit explanation**: "...the BH initially labeled secondary becomes more massive, formally inverting the q_b ≤ 1 convention. We continue to label them by their initial assignment for clarity." |
| "This makes sense especially in light of the results of DeLaurentiis & Rafikov (2025)..." | *"this is a very speculative"* | Soften the explanatory paragraph. |
| MSS comment "can you give some estimates here on the timescale of disk realignment?" | SOD: "Perhaps the viscous time? I'm not sure what do you think, Zoltan?" | **Open question to Zoltan** — likely answered by the handwritten note: *"I would speculate this occurs on a typical disk precession timescale (since 'flipping' will probably occur via precession)"* — **use this**: disk precession timescale, not viscous time. |
| "some potential" margin | minor | likely "some potential CBD..." phrasing. |

#### §4.1 Flickering Jets — physics framing
| Location | Annotation | Action |
|---|---|---|
| "When an accretion disk is radiatively efficient..." | *"yes"* / agreement | reviewer is OK with the high-level framing. |
| Section anchor | *"#6"* | Likely a numbering note. |
| Discussion of Blandford-Znajek and radiatively inefficient disks | **"I believe key is that these disks become geometrically thick and the inner parts form a 'funnel' that can collimate jets"** | **Substantive physics addition needed** — current text talks about magnetic buildup and pressure; reviewer wants the *geometric thick-disk → funnel → collimation* picture added explicitly. This is a Haiman-flavored intuition. Add 2–3 sentences. |
| "Radiatively inefficient, geometrically thick disks are commonly found at low accretion rates..." | *"define M_Edd"* | Define the Eddington accretion rate explicitly before using it. |
| The whole §4.1 framing | *"jets likely launch and quench on a few t_dyn"* | Add this timescale claim to motivate why "flickering" is plausible (the dynamical time is short enough relative to the precession that on/off cycles are physical). |
| "...above which jets are likely to launch" | *"justify..."* | Justify the 1·Ṁ_Edd threshold — citation or argument. |
| Three-color background scheme | *"stick to color scheme"* / *"make blue?"* | Color-scheme requests for Fig. 8 panels — make sure consistent across the paper. |

#### Body text general
| Location | Annotation | Action |
|---|---|---|
| "The flickering jet systems are clustered at higher q_b and e_b" | *"already said above"* | Trim — don't repeat earlier observation. |
| "plethora" margin | reviewer's preferred word for variety/zoo | Use it once if natural. |

---

### Page 9 — Figure 8 (full-page Eddington-normalized accretion rates)

#### Figure 8 layout issues
- The reviewer manually wrote in the **missing axis labels** in red along the left and bottom: `0, 0.1, 0.2, 0.3, 0.4, ...` along the y-axis (column labels) and `0, 0.1, 0.2, 0.3...` along the x-axis (row labels), and `q/e_b` axis label at the corner.
- **Implication**: the printed figure has missing or illegible axis labels. **Fix by re-rendering with proper labels.**
- *"parts form a 'funnel' that can collimate jets"* (carry-over from page 8 physics note)

#### Citations in Section 4.1 body
- *"also Stu Shapiro has old MHD sims on binary jets. Also Elias Most..."* — **citations to add** for the dual-jet/flickering-jet discussion. Specifically:
  - Stuart Shapiro group (early 2010s GRMHD binary BH papers)
  - Elias Most (recent binary BH GRMHD work, e.g. Most & Quataert papers)
  - The reviewer notes that *"flickering"* as a *new* term may already have antecedents in this MHD literature.

---

### Page 10 — Figures 9, 10

#### Figure 9 (λ̃ heatmap)
| Location | Annotation | Action |
|---|---|---|
| Caption | *"Define for readers who haven't read the text"* | **Major caption rewrite** — define λ̃ in the caption itself with the equation. |
| Caption text | *"('Accretion rate gauge'?)"* | Reviewer suggests an *intuitive name* for λ̃ — call it the "accretion-rate gauge" or similar mnemonic in the caption to make it digestible. |

#### Figure 10 (parameter space for observable flicker)
| Location | Annotation | Action |
|---|---|---|
| Layout | *"highlight/point to the detection regions"* | **Add visual annotation** — call out the detection regions explicitly with arrows or shaded boxes; currently it's hard to read. |
| Multiple `?` marks on red region | flagged | The detection-region demarcation is unclear. |
| Caption: "those" unclear referent | *"those"* | Pronoun cleanup. |
| Body text: "for jet flicker" insert | clarification | minor. |
| Body text: "common enough" | *"not exceedingly rare"* | Replace with "not exceedingly rare" — gentler hedge. |
| MSS: "increase the size of the axis labels and the text in the subplots indicating the binary mass" | already addressed by SOD? | Verify the figure was actually re-rendered with larger labels. |

#### Body text
| Location | Annotation | Action |
|---|---|---|
| "The gray lines represent the change in eccentricity and semi-major axis for the binary, due to 10 orbits worth of GW radiation" | *"Explain a few from Peters 1964 (?)"* | **Add Peters 1964 reference** for the GW shrinking calculation. Possibly also walk through the calculation briefly so the reader knows what "10 orbits worth" means. |

---

### Page 11 — §4.2 Unequal Mass Sources, Figure 11

#### Section heading
- *"I think you mean 'dearth of q=1 binaries.'"* — confirms earlier marginal note. **Use this exact phrasing somewhere prominent** (Section 4.2 opening or Conclusions).
- *"[Also, be consistent, q or q_b?]"* — **global notation pass needed**.

#### Body text
| Location | Annotation | Action |
|---|---|---|
| "we represent these as ė_gas..." | *"we"* margin | minor. |
| Eq. 9 (ė_GW formula) | *"(Peters 1964)"* | Cite Peters 1964 directly at this equation. |
| "where ~~we~~ include these effects" | strike | grammatical. |
| "Per Fig. 7, we solve the initial value problem..." | *"using (q̇ in Fig. 7)"* / *"(c)"* | Reference Eq. 12 / Fig. 7 explicitly. |
| Initial conditions listing | *"It late"* / *"It constants"* | Possibly suggesting tabular listing of initial conditions. |
| "More interestingly, we find that the two binaries initialized at q_b, e_b = (0.2, 1.0)..." | *"e_b, q_b ="* — note the ordering swap | Notation pass. |
| MSS: "you might also cite my 2024 paper on massive black hole binary population statistics" | SOD: done | Verify the citation made it in. |
| MSS: "What accretion rate did you assume here?" | SOD: 100*Eddington, "doesn't change strongly over this time" | Reviewer also asks about this — **make the assumption explicit in the text**. State: "We assume Ṁ_b = 100 Ṁ_Edd; the qualitative result is insensitive to this choice over the integration timescale." |
| MSS: "consider changing the x-axis in figure 11 to semi-major axis, if that's feasible" | SOD: pushed back politely | Add a sentence explaining why time is the chosen x-axis (it captures the relaxation to equilibrium more directly). |
| LISA precision claim | SOD: "Try as I might, I was unable to find/remember the source for the LISA q precision." Reviewer note: **"(REF... Mangiagli et al 2023)"** | **Cite Mangiagli et al. 2023** for the 0.5% LISA q_b precision figure. |
| "0.5%" | small "()" mark | Verify the precision figure matches the citation. |

---

### Page 12 — §5 Summary and Conclusions, References

#### Conclusions list — item-by-item
| Item | Annotation | Action |
|---|---|---|
| (i) "Across q_b and e_b, λ(t) can be split into time-varying and time-stable regimes" | *"constant"* / *"these"* | Replace "time-stable" with "constant" (or be consistent with body text). Reference Table 1. |
| (ii) "weak positive correlation" | *"(Fig. X)"* margin | Add figure reference. |
| (iii) "⟨λ⟩ is positively correlated with more eccentric CBDs" | *"(Fig X)"* | Add figure reference. |
| (iv) "We find strong evidence that while the CBD precession and λ(t) oscillation have the same period, these time-series are not in phase." | **"way too much to claim, legally so, causally!"** + circled "?-?" | **MAJOR**: This conclusion is overclaiming. The reviewer has made the same point in §3.1.1. **Rewrite as**: "We find that the CBD precession period and λ(t) oscillation period are equal across our sample of precessing systems; however, these time-series are not in phase, ruling out a simple causal interpretation in terms of cavity-wall distance." |
| (v) "We do not find evidence that a BH must be closer to the CBD cavity than its counterpart, to accrete preferentially." | *"only"* / *"preferentially at a higher rate"* | Tighten: "...closer to the cavity wall to accrete at a higher rate." |
| (vi) Jet regimes summary | *"(Fig.X)"* | Add figure reference. |
| (vii) "(0.2, 1.0) and (0.3, 1.0) binaries do not have q_b = 1.0 steady-states" | margin: *"q ≤ 1"* | Address the convention again. Note that the reviewer at top of page wrote: ***"There are no long-lived q=1, e=0.2 binaries, and these will evolve to q<1 'or' some such"*** — **use this language** for the conclusion. |

#### Forward-looking paragraph
| Location | Annotation | Action |
|---|---|---|
| "While our work has shed light on novel aspects of this system" | *"only"* | "shed light on only some aspects" — slight humility. |
| "we are still studying setups with simplified physics" | reviewer accepts | OK as is. |

#### Concluding sentence
- *"way too much to claim so causally!"* — circled around *"intimately tied to the CBD"*. **Soften** to "consistent with the CBD playing a regulating role".

#### Data Availability
- *"Thank my NASA ATP and LISA grants"* — **Add acknowledgments section** (currently missing or minimal): thank NASA ATP and LISA grants. This is Zoltan's own grant funding — be sure to format the grant numbers correctly per his instructions.

#### References
- Page 12 has scattered marks (e.g. "794 5ᵗʰ", "Catahigher rate N01") that look like the reviewer cross-checking specific reference details — but the marks aren't directionally clear. Spot-check by:
  - Verifying all DOIs / journal info on the reference list
  - Filling in any "arXiv e-prints" entries that have been published since (DeLaurentiis+Rafikov 2025; Calcino+; Dittmann+).

---

## MSS Open Threads (typed comments not yet fully addressed)

Even where SOD has marked threads "done", a few remain genuinely open:

1. **§3.1 locking framing** — SOD wrote: *"please correct me if I'm wrong, and let me know how it is best to approach this."* This needs a reply from MSS before submission.
2. **§3.2 disk realignment timescale** — SOD asked Zoltan; Zoltan answered in margin (precession timescale). Update the text accordingly.
3. **§4.2 LISA q precision source** — SOD couldn't find it; Zoltan supplied Mangiagli+2023. Update.
4. **§4.2 x-axis of Fig. 11** — MSS asked for semi-major axis; SOD declined. Add a one-line justification in the caption.
5. **§4.2 accretion rate assumption** — MSS asked, SOD answered in [SOD] block but the assumption is not in the manuscript prose. **Add it**.

---

## Priority-Ordered Action List

If revising under time pressure, attack in this order:

### Tier 1 — Scientific substance (cannot ship without)
1. Soften causal claims throughout (§3.1.1, §5 item iv, §5 closing). Replace "determines / regulates / causes" with "is correlated with / is consistent with".
2. Define `r_cav`, `r₁`, `r₂` unambiguously in §3.1.1 (origin of measurement).
3. Address the q_b ≤ 1 convention vs. "evolving away from unity" tension explicitly when introducing the q_b=1 result (page 8).
4. Add the Haiman geometric-funnel framing to the jet-launching physics in §4.1.
5. Walk through the phase-relationship argument pedagogically in §3.1.1 (the reviewer admits confusion).
6. Cite Mangiagli+2023 for LISA q_b precision; cite Peters 1964 for GW formulas.

### Tier 2 — Notation and citations
7. Pick `(e_b, q_b)` ordering and propagate.
8. Pick `q` or `q_b` and propagate.
9. Add Barnes & Hernquist, D'Orazio 2013 (periodogram credit), Farris+2014, Duffell+2017, Munoz+2017, Miranda+Munoz+2017 (locking), Stu Shapiro group, Elias Most.
10. Confirm or cut Artymowicz 1983.
11. Add NASA ATP / LISA grant acknowledgments.

### Tier 3 — Figures
12. Fig. 1 and Fig. 6: concatenate panels, share axes, larger labels.
13. Fig. 2 and Fig. 4: recolor with perceptually-uniform sequential colormap.
14. Fig. 3: gray-shade the y > 1 region.
15. Fig. 5: aspect ratio matched to Figs 2/4.
16. Fig. 8: re-render with proper axis labels (currently missing/illegible).
17. Fig. 9: rewrite caption to be self-contained, define λ̃.
18. Fig. 10: highlight detection regions with explicit visual call-outs.
19. Fig. 11: caption note on why time is x-axis; state Ṁ_b assumption.
20. **Every figure**: caption must be self-contained. This is the single most-repeated reviewer complaint.

### Tier 4 — Style
21. Audit all section headings for MNRAS sentence-case rule.
22. Use `\citealt` where appropriate.
23. Tighten openings ("What first strikes us..." → "The most striking feature is...").
24. Replace "not exceedingly rare" / softer hedges where flagged.

### Tier 5 — Open MSS threads
25. Resolve the §3.1 locking-framing disagreement with MSS.
26. Verify Siwek+2024 citation made it in.
27. Verify large-axis-label re-render of Fig. 10.

---

## Style notes worth carrying into future papers

A few of these comments are advisor-flavored process-level critiques that will recur if not internalized:

- **Figures should always be readable on their own.** The reviewer flagged this on at least 4 figures.
- **Causal claims need stronger evidence than correlation.** This is a recurring flag and a habit worth breaking.
- **Notation must be defined at first use, in the abstract if introduced there.** The fact that `λ` and `q̇` aren't formally defined in the abstract is the first thing the reviewer wrote.
- **MNRAS sentence case for headings.** Easy fix, but the reviewer caught it because journal-style errors signal carelessness.
- **When in doubt about whether to claim or hedge, hedge.** The "way too much to claim, legally so, causally!" note is the strongest emotional reaction in the entire markup.
