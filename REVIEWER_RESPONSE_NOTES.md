# Reviewer-response notes — items flagged for author (round 2)

Branch: `review-round-2`. Edits applied commit-by-commit; this file lists the items that
need **your** science judgment or a decision I shouldn't make autonomously.

## Needs a decision / confirmation
- **Tiede & D'Orazio SED paper (p.1, #10):** the reviewer wants the light-curve/SED mention
  cited to a Tiede & D'Orazio paper that "computed SEDs." No such paper is in `main.bib`
  (`Tiede_dorazio_cbd` is the *retrograde-disc* paper; `Tiede_22` is the tracer-particle paper).
  I cited `dorazio_2013` + `dorazio_charisi` (2023 obs-signatures review, covers SEDs) as a
  stand-in. → Confirm/add the specific Tiede & D'Orazio SED reference.
- **Siwek affiliation → NYU (p.1, #2):** set affiliation 4 to NYU CCPP (726 Broadway). Confirm
  exact department/address. (Her contact e-mail in the author block is still `mss2334@columbia.edu` —
  likely stale.)
- **"delete the primary" (p.1):** I dropped "than the primary" for grammar ("accrete at a greater
  rate in what has become known as preferential accretion"). Confirm intent.
- **Mangiagli 2020 supplement (p.13, #20-ref):** reviewer wants a recent higher-harmonics+spin
  LISA precision ref added. NOT added (needs your pick + bib entry). Candidates from web:
  "Systematic biases in PE on LISA binaries (higher harmonics; spin-aligned high-mass)"
  arXiv:2502.12237 / 2602.09088; GPU/SNL LISA PE (Katz et al.).

## Low-confidence edits — NOT applied (reviewer flagged as uncertain)
- "fluctuate symmetrically around 1" → "asymmetrically"? (p.6) — reviewer asked "do you mean
  asymmetrically?"; current logic reads as *symmetric*. Left as-is pending your call.
- Delete "jets that periodically switch on and off" (p.2 roadmap) — reviewer "unsure about this".
  Left as-is.
- Drop plural "s" on "SMBBHs" (p.12) — disagrees with standard usage. Left as-is.

## Emphasis-only requests (cosmetic) — left as prose
- Abstract: emphasize the λ(t)≡Ṁ₂/Ṁ₁ sentence; p.9 "apsidal precession timescale"/"orient locked
  disks"; p.10 "unique to e_b≠0"/"few dual-jet"; p.13 "q=1"; p.15 "more complex than previously
  thought". Italics in these spots read oddly in MNRAS style; applied only where it aids clarity.

## Science items you said you'd revisit
- **#19 jet/Eddington normalization (p.10/11):** reviewer "how is this possible??". I derived the
  budget constraint: with Ṁ_b=1 Ṁ_Edd, x + q_b·y = 1+q_b (x≡Ṁ_1/Ṁ_Edd,1, y≡Ṁ_2/Ṁ_Edd,2), so both
  BHs can't sit *well* above the 1.1 super-Edd threshold at once. **Looked at Fig 11
  (mdot1_mdot2_1edd_both_truncated.pdf): the purple "dual-jet" cells are the near-equal-mass,
  low-e_b corner where M_1≈M_2≈0.5 Ṁ_Edd,b ⇒ both BHs sit right at x≈y≈1.0** (exactly Eddington),
  i.e. marginal, threshold-sensitive — not two BHs comfortably super-Edd. I softened the text to
  say this (marginal dual cells; robust dual jets need bracketing Ṁ_b) so it no longer contradicts
  the figure. **TODO (you):** decide whether to (a) regenerate Fig 11 (`accretion_eddington.py`)
  with a cleaner threshold so those marginal cells are not coloured "dual," or (b) keep + caption
  them as marginal. Also: reviewer's "single jet from primary at 5 Ṁ_Edd, wobbles less" (p.13) —
  I did NOT assert this (couldn't verify which BH dominates at 5 Ṁ_Edd); confirm against Fig 13.
- Sink r_s = 0.03 a_b same for both BHs (p.2): noted as a numerical choice; sensitivity untested.
- Threshold 0.05 (FFT amplitude) and jet 1.1 Ṁ_Edd / 50 τ_b sensitivity (p.8): not tested.
- Ṁ_b = 100 Ṁ_Edd (p.12): reviewer "why so big?" — kept, with note it only sets the timescale;
  consider lowering.
- Galaxy-feedback sentence (p.12): reviewer "???" — kept; decide keep/trim.
- Grant numbers (p.15): two `[INSERT NUMBER]` placeholders — need ZH's NASA ATP + LISA grant IDs.
