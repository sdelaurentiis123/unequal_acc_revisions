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
- **#19 jet/Eddington normalization (p.10/11):** reviewer "how is this possible??" — both BHs
  cannot simultaneously exceed Ṁ_Edd when Ṁ_bin is normalized to 1 Ṁ_Edd (ΣṀ_Edd,i ≈ Ṁ_Edd,tot).
  A sustained dual jet at Ṁ_bin=1 must be one super-Edd (thick) + one ADAF jet, not two super-Edd.
  I added clarifying text + flagged; **verify Fig 11 (mdot_edd) upper-left panel** doesn't actually
  show two simultaneous super-Edd jets, and that "always the secondary at 1 Ṁ_Edd" / "primary at
  5 Ṁ_Edd (wobbles less)" is borne out by the data.
- Sink r_s = 0.03 a_b same for both BHs (p.2): noted as a numerical choice; sensitivity untested.
- Threshold 0.05 (FFT amplitude) and jet 1.1 Ṁ_Edd / 50 τ_b sensitivity (p.8): not tested.
- Ṁ_b = 100 Ṁ_Edd (p.12): reviewer "why so big?" — kept, with note it only sets the timescale;
  consider lowering.
- Galaxy-feedback sentence (p.12): reviewer "???" — kept; decide keep/trim.
- Grant numbers (p.15): two `[INSERT NUMBER]` placeholders — need ZH's NASA ATP + LISA grant IDs.
