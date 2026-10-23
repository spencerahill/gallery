# Gallery

Teaching figures by Spencer A. Hill, each with the code that draws it,
published at <https://spencerahill.github.io/gallery/>.

Everything in this repository is in the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (see `LICENSE`):
copy, modify and use any of it for any purpose, without asking or giving
credit. Where a figure redraws someone else's, its page credits the original;
please keep that credit when you reuse the figure.

## Building

The environment is managed with [pixi](https://pixi.sh), and `pixi.lock` pins
every package for macOS and Linux.

```sh
pixi run figures   # rebuild every figure from its script
pixi run preview   # rebuild every figure, then serve the site locally
pixi run render    # rebuild every figure, then render the site into _site/
```

The built files (`.tex`, `.pdf`, `.svg` and `.png` in each figure's directory)
are not committed. On every push to `main`, GitHub Actions
(`.github/workflows/publish.yml`) rebuilds them all from the scripts and
deploys the site.

## Adding a figure

Each figure has its own directory, `figures/<slug>/`, containing two files:

- `make_<name>.py`, which writes `<name>.tex`, a standalone LaTeX document,
  when run from that directory;
- `index.qmd`, the figure's page, whose front matter gives `title`,
  `description`, `date` and `image: <name>.png`, and lists the built files under
  `resources` so the site includes them.

The directory can also contain further pages, such as notes for instructors,
as other `.qmd` files, which the site renders too, and plain Markdown notes
such as `design-notes.md`, which it does not. A figure that redraws a published
one credits it in a Credit section of its `index.qmd`.

`scripts/build_figures.py` runs every `make_*.py`, compiles each `<name>.tex` to
PDF with tectonic, and converts the PDF to SVG and to a 300 dpi PNG. The front
page lists every `figures/*/index.qmd` automatically.

## Styling

`styles.scss` and `styles.css` are unmodified copies of the files of the same
name in [spencerahill.github.io](https://github.com/spencerahill/spencerahill.github.io),
so the two sites look alike. Rules for this site only go in `gallery.css`.
