# CLAUDE.md: the τ ≈ 1 sweet-spot schematic

A one-panel TikZ teaching cartoon of the τ ≈ 1 emission sweet spot for CO₂:
one column of molecules, each emitting one photon straight up. The schematic redraws
Fig. 3 of Jeevanjee (2023, *Am. J. Phys.* 91, 731). Spencer made it in Claude
desktop and called it finished on 2026-10-23. `design-notes.md` gives the
reason for each visual choice; read it before proposing a visual change.

The course repository `~/Dropbox/teaching/27sp_eas488` keeps a copy of
`make_sweetspot.py`, `sweetspot.tex` and `sweetspot.pdf` in
`figures/tau1-sweetspot-schematic/` for the radiative transfer lectures. After
changing the figure here, copy those three files there.

## Hard constraints (set by Spencer; don't relitigate without being asked)

- **One concept only:** why the τ ≈ 1 layer sends the most photons to space.
  No extra panels or insets.
- **Deliberately left out:** the temperature profile; transmittance or
  weighting-function curves; CO₂ doubling; spectral dependence; glyphs sized
  by effective area, which belong in a separate companion figure.
- **Photon rules:** every molecule emits one photon, straight up, with no
  angled photons; optically thin photons all escape; most τ ≈ 1 photons
  escape, and more of them than thin-layer photons; optically thick photons
  are all absorbed. The script checks all of these, the first by construction
  and the rest by assertion; keep the checks.
- **Colors:** three, one per region, ordered red (thick), purple (τ ≈ 1), blue
  (thin), warm to cold. Never a continuous temperature gradient. Blue and
  purple must stay clearly distinguishable, including for red–green
  color-blind viewers.

## Workflow

- **Source:** `make_sweetspot.py`. Edit the parameter block at its top,
  rebuild with `pixi run figures` (the gallery's CLAUDE.md gives the full
  command), and look at `sweetspot.png` before reporting a change as done.
- **Generated files:** `sweetspot.tex`, `.pdf`, `.svg` and `.png` are rebuilt
  from the script and gitignored.
- **Seeds:** the default seed, 5, gives the published figure. Some seeds find
  no valid placement and stop with an error. At seed 108 the script instead
  crashes with a TypeError while writing the TikZ code, because each photon's
  fate is checked only against the molecules placed before it. Spencer
  (2026-10-23): not worth fixing, since the figure is finished.
- **Keeping the text in sync:** if molecule or escape counts change, update
  `index.qmd` (its text and alt text) and `instructor-notes.qmd` (its caption,
  alt text, the τ values read off glyph widths, currently 0.20, 0.99 and 3.7,
  and the table of expected escaping photons).

## Writing conventions for the notes

- Math in LaTeX: inline `$...$`, display `$$...$$`. The plain-text caption and
  alt text use Unicode τ, because they get pasted outside LaTeX.
- Wavelength is the spectral coordinate, never wavenumber or frequency: the
  figure is for EAS 488, whose materials follow that rule (Spencer
  2026-10-16).
- At τ = 1 the escape probability is e⁻¹ ≈ 37%, so the caption says "many"
  τ ≈ 1 photons escape, never "most".
- Say so wherever a number is our own estimate rather than from the paper.

## Open items

- Spencer still has to confirm with Nadir Jeevanjee how he would like to be
  credited. The wording is in the Credit section of `index.qmd` and the credit
  line at the end of `instructor-notes.qmd`.
- The companion effective-area figure is
  `27sp_eas488/figures/optical-depth-absorber-area/`. Spencer (2026-10-23): not
  finished yet; it is the next candidate for this gallery once it is.
