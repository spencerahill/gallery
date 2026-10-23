"""One-panel cartoon of the tau ~ 1 emission 'sweet spot' (CO2).

Rules, checked by assertion before anything is drawn:
  * every molecule emits exactly one photon, straight up;
  * a photon stops at the first molecule directly above it (a clean hit on
    the glyph, never a graze);
  * every optically thin photon escapes; most tau~1 photons escape, and more
    escape from the tau~1 layer than from the thin layer; every optically
    thick photon is absorbed.
Writes sweetspot.tex (standalone TikZ).
"""
import numpy as np

import sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 5)

# ---------------- layout (cm) ----------------
W = 6.6                                  # column width
Y_THICK2, Y_THICK1, Y_SWEET, Y_THIN = 0.0, 1.6, 3.2, 4.8
Y_TOA = 6.6                              # top of atmosphere (dashed)
Y_SPACE = 7.35                           # escaping arrows end here, above the TOA

# CO2 glyph O=C=O (horizontal)
R_O, R_C, D = 0.105, 0.125, 0.222
HALF = D + R_O                           # 0.327
HIT = 0.28                               # photon must strike within +-HIT of centre
CLEAR = HALF + 0.08                      # min lateral gap for a photon passing a glyph

# hand-placed: thin layer (all escape) and tau~1 layer (5 of 8 escape)
THIN = [(1.45, 5.45), (5.05, 5.70)]
SWEET_ESC = [(0.55, 3.95), (2.40, 4.25), (3.30, 3.90), (4.20, 4.32), (6.02, 3.92)]
SWEET_ABS = [(1.38, 4.02), (5.12, 4.12), (3.47, 3.37)]
# optically thick layers: rows of (y, number of molecules)
THICK_ROWS = [(2.75, 5), (2.05, 6), (1.20, 8), (0.42, 8)]

# photon colour by source region, cold -> warm (thin, tau~1, thick)
COL = {"thin": "3399E0", "sweet": "7E1F86", "thick": "C62828"}
ATOM_C, ATOM_O, ATOM_O_EDGE = "3A3A3A", "B9CDE3", "6E8299"
SWEET_BAND = "EFE3EF"                    # light tint of the tau~1 photon colour
BAND_RIGHT = 3.15                        # band extends this far past the column, under its label


def atoms(m):
    x, y = m
    return [(x - D, y, R_O), (x, y, R_C), (x + D, y, R_O)]


def overlaps(m, others, gap=0.07):
    return any(np.hypot(a[0] - b[0], a[1] - b[1]) < a[2] + b[2] + gap
               for o in others for a in atoms(m) for b in atoms(o))


def fate(m, placed):
    x, y = m
    above = [o for o in placed if o[1] > y + 1e-9 and abs(o[0] - x) < CLEAR]
    if not above:
        return "escape", None
    first = min(above, key=lambda o: o[1])
    return ("hit", first) if abs(first[0] - x) <= HIT else ("graze", None)


placed = []
mols = []                       # (x, y, layer)


def add(m, layer, want):
    f, _ = fate(m, placed)
    assert f == want, (m, layer, f)
    assert not overlaps(m, placed), (m, layer)
    placed.append(m)
    mols.append((m[0], m[1], layer))


for m in THIN:
    add(m, "thin", "escape")
for m in sorted(SWEET_ESC + SWEET_ABS, key=lambda m: -m[1]):
    add(m, "sweet", "escape" if m in SWEET_ESC else "hit")

for (yrow, n) in THICK_ROWS:
    layer = "thick1" if yrow > Y_THICK1 else "thick2"
    targets = np.linspace(0.55, W - 0.55, n) + rng.uniform(-0.3, 0.3, n)
    for xt in targets:
        yt = yrow + rng.uniform(-0.17, 0.17)
        for dx in sorted(np.arange(-0.6, 0.601, 0.01), key=abs):   # nearest valid spot
            x = xt + dx
            if not (HALF + 0.1 < x < W - HALF - 0.1):
                continue
            m = (x, yt)
            if not overlaps(m, placed) and fate(m, placed)[0] == "hit":
                break
        else:
            raise RuntimeError(f"no slot near {xt:.2f}, {yt:.2f}")
        add(m, layer, "hit")


def hit_y(x, blk):
    return min(cy - np.sqrt(r**2 - (x - cx) ** 2) for (cx, cy, r) in atoms(blk) if abs(x - cx) < r)


# ---------------- TikZ ----------------
L = []
w = L.append
w(r"""\documentclass[tikz,border=6pt]{standalone}
\usepackage{amsmath}
\usetikzlibrary{arrows.meta,decorations.pathreplacing}
\definecolor{colthin}{HTML}{%s}
\definecolor{colsweet}{HTML}{%s}
\definecolor{colthick}{HTML}{%s}
\definecolor{atomC}{HTML}{%s}
\definecolor{atomO}{HTML}{%s}
\definecolor{atomOedge}{HTML}{%s}
\definecolor{sweetband}{HTML}{%s}
\tikzset{
  photon/.style={line width=1.0pt,-{Stealth[length=5pt,width=4.2pt]}},
  co2/.pic={
    \filldraw[fill=atomO,draw=atomOedge,line width=0.35pt] (-%.3f,0) circle (%.3f);
    \filldraw[fill=atomO,draw=atomOedge,line width=0.35pt] (%.3f,0) circle (%.3f);
    \filldraw[fill=atomC,draw=black,line width=0.35pt] (0,0) circle (%.3f);
  },
}
\begin{document}
\begin{tikzpicture}""" % (COL["thin"], COL["sweet"], COL["thick"], ATOM_C, ATOM_O, ATOM_O_EDGE, SWEET_BAND,
                          D, R_O, D, R_O, R_C))

w(r"\fill[sweetband] (0,%.3f) rectangle (%.3f,%.3f);" % (Y_SWEET, W + BAND_RIGHT, Y_THIN))
w(r"\draw[line width=1.0pt] (0,0) -- (%.3f,0);" % W)
for yl in (Y_SWEET, Y_THIN):
    w(r"\draw[line width=0.6pt] (0,%.3f) -- (%.3f,%.3f);" % (yl, W, yl))

# photons first, so each molecule sits on top of its arrow's tail
for (x, y, layer) in mols:
    f, blk = fate((x, y), placed)
    y_end = Y_SPACE if f == "escape" else hit_y(x, blk) - 0.015
    col = "colthick" if layer.startswith("thick") else "col" + layer
    w(r"\draw[photon,%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x, y + 0.03, x, y_end))
for (x, y, layer) in mols:
    w(r"\pic at (%.3f,%.3f) {co2};" % (x, y))

w(r"\draw[line width=0.7pt,dash pattern=on 4pt off 2.5pt] (0,%.3f) -- (%.3f,%.3f);" % (Y_TOA, W, Y_TOA))
w(r"\node[anchor=east,font=\small] at (-0.05,%.3f) {TOA};" % Y_TOA)
w(r"\node[anchor=east,font=\small] at (-0.05,0) {surface};")
w(r"\draw[-{Stealth[length=6pt]},line width=0.8pt] (-1.65,0) -- (-1.65,%.3f) node[above] {$z$};" % Y_SPACE)

XB = W + 0.3


def brace(y0, y1, text, color="black", lw=0.8, font=""):
    w(r"\draw[decorate,decoration={brace,amplitude=6pt},line width=%.1fpt,color=%s] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (lw, color, XB, y1 - 0.05, XB, y0 + 0.05))
    w(r"\node[anchor=west,align=center,color=%s,font=%s] at (%.3f,%.3f) {%s};" % (color, font, XB + 0.3, 0.5 * (y0 + y1), text))


brace(Y_THIN, Y_TOA, r"$\tau \ll 1$\\[1pt]{\small optically thin}", "colthin")
brace(Y_SWEET, Y_THIN, r"$\boldsymbol{\tau \approx 1}$\\[1pt]sweet spot", "colsweet", lw=1.2, font=r"\large\bfseries")
brace(Y_THICK2, Y_SWEET, r"$\tau \gg 1$\\[1pt]{\small optically thick}", "colthick")

w(r"\end{tikzpicture}")
w(r"\end{document}")
open("sweetspot.tex", "w").write("\n".join(L))

for layer in ("thin", "sweet", "thick1", "thick2"):
    ms = [m for m in mols if m[2] == layer]
    esc = sum(fate(m[:2], placed)[0] == "escape" for m in ms)
    print(f"{layer:7s} molecules={len(ms):2d} escape={esc}")
