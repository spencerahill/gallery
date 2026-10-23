"""Build every figure in figures/ from its script.

Each figure lives in figures/<slug>/ with a script make_<name>.py, which writes
<name>.tex when run from that directory.  This compiles <name>.tex to <name>.pdf
with tectonic, then converts the PDF to <name>.svg for the web page and to
<name>.png for slide software that cannot import SVG.  All four outputs are
gitignored: the scripts are the source, and the GitHub Actions build makes the
published copies.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PNG_DPI = 300


def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True)


def build(script):
    fig_dir = script.parent
    name = script.stem.removeprefix("make_")
    out = {ext: fig_dir / f"{name}.{ext}" for ext in ("tex", "pdf", "svg", "png")}
    # Delete old outputs first, so a step that silently writes nothing fails
    # the check below instead of leaving the previous build in place.
    for path in out.values():
        path.unlink(missing_ok=True)

    run([sys.executable, script.name], cwd=fig_dir)
    run(["tectonic", "--chatter", "minimal", out["tex"].name], cwd=fig_dir)
    run(["pdftocairo", "-svg", out["pdf"].name, out["svg"].name], cwd=fig_dir)
    run(["pdftocairo", "-png", "-r", str(PNG_DPI), "-singlefile",
         out["pdf"].name, name], cwd=fig_dir)

    missing = [p.name for p in out.values() if not p.exists()]
    if missing:
        raise RuntimeError(f"{fig_dir.name}: build exited cleanly but did not write {missing}")
    print(f"built {fig_dir.name}: " + ", ".join(p.name for p in out.values()))


def main():
    scripts = sorted(ROOT.glob("figures/*/make_*.py"))
    if not scripts:
        raise RuntimeError(f"no figures/*/make_*.py under {ROOT}")
    for script in scripts:
        build(script)
    print(f"{len(scripts)} figure(s) built")


if __name__ == "__main__":
    main()
