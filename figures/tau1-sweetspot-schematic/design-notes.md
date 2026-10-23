# Design notes: the τ ≈ 1 sweet-spot schematic

Why the figure looks the way it does. Useful for anyone adapting it, and as the record of decisions behind the current version.

## Starting point

The figure is adapted from Fig. 3 of Jeevanjee (2023), which shows the same atmospheric column three times, for the optically thin regime, the sweet spot and the optically thick regime. Two weaknesses motivated the redesign:

- **Equal escaping counts.** The thin and sweet-spot panels each show three escaping photons, so the drawing does not show that the $\tau \approx 1$ layer sends the *most* photons to space.
- **Three panels.** The reader has to combine three panels mentally to see one column.

## Governing constraint: one concept

The figure exists to make exactly one idea visually obvious: why the $\tau \approx 1$ layer is the "sweet spot" for photons escaping to space. Several elements were tried or proposed and deliberately left out because each adds a second idea:

- a panel of transmittance, absorption and their product versus height;
- a temperature-profile panel reading off $T_\text{em}$;
- a CO₂-doubling shift of the emission level;
- the spectral "emission triangle" (emission level versus wavelength);
- glyphs sized by effective cross-section, or a top-down "view from space". The effective-area interpretation of $\tau$ is planned as a separate figure shown *before* this one.

## Cartoon rules

`make_sweetspot.py` draws one vertical arrow per molecule, so the first rule holds by construction. The script checks the second as it places each molecule, against the molecules already placed, and asserts the photon counts in the last three once every molecule is placed:

- Every molecule emits exactly one photon, straight up. No photon is angled.
- A photon stops at the first molecule directly above it, with a clean hit on the glyph and never a graze.
- Every optically thin photon escapes.
- A majority of $\tau \approx 1$ photons escape, and more escape from that layer than from the thin layer.
- Every optically thick photon is absorbed, either within the thick region or by a molecule higher up.

## Specific choices

- **Five of eight $\tau \approx 1$ photons escape.** At $\tau = 1$ the transmittance straight up is $e^{-1} \approx 37\%$. Showing nearly every photon escaping would make the sweet-spot layer look like a second thin layer and hide the absorption side of the trade-off. With glyph widths read as effective area, the shaded layer spans $\tau \approx 0.2$–$1$, whose average escape probability is $\approx 57\%$. See the [instructor notes](https://spencerahill.github.io/gallery/figures/tau1-sweetspot-schematic/instructor-notes.html).
- **Layout.** Fully random placement produced clumps under these rules: every absorbed photon chains upward to one of only seven escaping photons. The thin and $\tau \approx 1$ molecules are therefore hand-placed. The thick-layer molecules sit in loose rows, each nudged sideways to the nearest position where its photon makes a clean hit on a molecule above. Seed 5 gives the current arrangement.
- **Colors.** There are three colors, one per region, ordered cold to warm: blue `3399E0`, purple `7E1F86`, red `C62828`. The colors identify a photon's source layer and hint at temperature without plotting it. An earlier blue/purple pair (`1F5FAD` / `7B3FA0`) was too similar: the CIEDE2000 difference between them was about 23, and about 3 under simulated deuteranopia, which is effectively indistinguishable. The current pair differs in lightness as well as hue, giving about 48 normally and about 24 under deuteranopia. Purple and red differ by about 34.
- **Emphasis on the sweet spot.**
  - The band is a light tint of the sweet-spot purple, so band, brace, label and photons share one hue.
  - The band extends past the column, behind its label, so that label is the only one inside a highlight.
  - The label is bold, one size larger than the other τ labels and two sizes larger than "optically thin" and "optically thick", and its brace is heavier.
  - If more emphasis is ever wanted, mute the other two regions rather than darkening the band, which would start to fight the purple photons.
- **Other details.** A dashed TOA line has every escaping photon's arrowhead above it. The surface is labeled. The thick region has no internal divider, so it reads as one regime.

## Reference

N. Jeevanjee, "Climate sensitivity from radiative-convective equilibrium: A chalkboard approach," *Am. J. Phys.* **91**, 731–745 (2023), https://doi.org/10.1119/5.0135727.
