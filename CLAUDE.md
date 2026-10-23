# CLAUDE.md

Guidance for Claude Code in this repository.

## What this repository is

Spencer Hill's public gallery of teaching figures, each with the code that
draws it, live at https://spencerahill.github.io/gallery/ and linked from the
Gallery entry in the navbar of his main site (repository
`spencerahill/spencerahill.github.io`). The GitHub repository is
`spencerahill/gallery`, and the local copy is `~/Dropbox/teaching/my-web-gallery`;
Spencer chose both names on 2026-10-23.

**The repository is public, and every push to `main` deploys the site.** Treat
each commit as a publication.

## Decisions Spencer made on 2026-10-23

- **A separate repository from the main site,** so that one license covers every
  file and a clone does not bring the paper PDFs along.
- **CC0 1.0 for everything, code and figures alike.** Never copy in a
  third-party image or a figure from a published paper. A figure redrawn from a
  published one, as the τ ≈ 1 schematic is from Fig. 3 of Jeevanjee (2023),
  credits the original in a Credit section of its page. When the original is
  CC BY, that section also gives the license and lists the changes, as CC BY
  requires of adaptations, and asks reusers to keep the credit. (Added by
  Claude on 2026-10-23, after the zip from Claude desktop showed the schematic
  was adapted from that figure; Spencer has not yet reviewed the wording.)
- **Figures are drafted inside the project that uses them,** usually a course
  repository, where the context about the topic lives, and copied here once
  finished. A figure made outside any project comes straight here; the τ ≈ 1
  sweet-spot schematic, made in Claude desktop, was the first.

## Build

`pixi.toml` defines the environment (Python, NumPy, tectonic for LaTeX, poppler
for `pdftocairo`, Quarto). pixi is not on the shell PATH:

```sh
~/.pixi/bin/pixi run --manifest-path <repo>/pixi.toml figures   # build every figure
~/.pixi/bin/pixi run --manifest-path <repo>/pixi.toml render    # figures, then the site
```

`scripts/build_figures.py` runs each `figures/<slug>/make_<name>.py` from its own
directory, then compiles `<name>.tex` and converts the PDF to SVG and PNG. The
built files are gitignored and must stay uncommitted: the Actions build in
`.github/workflows/publish.yml` makes the published copies from the scripts.
After pushing, watch that run (`gh run list --commit <full sha>`, then
`gh run watch <id> --exit-status`).

The README gives the layout of a figure's directory and its `index.qmd`. A
figure's directory can also contain its own `CLAUDE.md` with the constraints
Spencer set on that figure; the τ ≈ 1 schematic's does.

**Next candidate (Spencer, 2026-10-23):** the optical-depth absorber-area
figure, `~/Dropbox/teaching/27sp_eas488/figures/optical-depth-absorber-area/`,
once he calls it finished; the absorber-area figure is not finished yet.

## Styling

`styles.scss` and `styles.css` are unmodified copies of the main site's files.
When the main site is restyled, copy them again and confirm with `cmp`. Rules
for the gallery alone go in `gallery.css`.

## Writing

Page text is in Spencer's voice: first person, plain, no marketing tone. The
global writing rules in `~/.claude/CLAUDE.md` apply. Every physical claim on a
figure's page is public under his name, so check it (the `/double-check` skill)
before committing.
