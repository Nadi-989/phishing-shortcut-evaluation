"""Builds Figures 2, 3 and 4 of the paper from the saved results.

Figure 2: 10-fold CV F1 of stacking and its base learners (results/tables/9_statistical_test.csv).
Figure 3: single feature ROC-AUC, full PhiUSIIL set vs lexical setting (results/tables/10_leakage_auc.csv).
Figure 4: RFECV curves, assembled from the notebook figures in results/figures.
Figure 1 (framework diagram) is provided as figures/fig1_framework.png.
"""
from pathlib import Path
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9})


def mean_sd(s):
    m, sd = re.findall(r"[\d.]+", s)[:2]
    return float(m), float(sd)


def fig2():
    df = pd.read_csv(ROOT / "results/tables/9_statistical_test.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.1))
    for ax, (ds, title, lim) in zip(axes, [("PhiUSIIL", "PhiUSIIL (lexical)", (99.3, 99.8)),
                                           ("WPD", "WPD", (95.5, 98.0))]):
        sub = df[df.Dataset == ds]
        rows = []
        for _, r in sub.iterrows():
            name = r.Comparison.replace("Stacking vs ", "").replace("RF", "Random Forest")
            rows.append((name, *mean_sd(r["Other F1 mean±std (%)"]), f"p = {r['Wilcoxon p']:.3f}"))
        rows.append(("Stacking", *mean_sd(sub.iloc[0]["Stacking F1 mean±std (%)"]), "reference"))
        for i, (m, mu, sd, p) in enumerate(rows):
            c = "#1f5fbf" if m == "Stacking" else "#8a8a85"
            ax.errorbar(i, mu, yerr=sd, fmt="o", color=c, capsize=4, ms=6, lw=1.5)
            ax.text(i + 0.12, mu, f"{mu:.2f}", va="center", fontsize=8,
                    fontweight="bold" if m == "Stacking" else "normal")
        ax.set_xticks(range(len(rows)))
        ax.set_xticklabels([r[0].replace(" ", "\n") + "\n" + r[3] if " " in r[0] else r[0] + "\n\n" + r[3]
                            for r in rows], fontsize=7.5)
        ax.set_ylim(*lim); ax.set_xlim(-0.5, 3.7)
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.grid(axis="y", color="#e3e3e0", lw=0.6); ax.set_axisbelow(True)
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("F1 (%)")
    plt.tight_layout(); plt.savefig(OUT / "fig2_cv_f1.png", dpi=300); plt.close()


def fig3():
    d = pd.read_csv(ROOT / "results/tables/10_leakage_auc.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.6))
    for ax, (key, title) in zip(axes, [("PhiUSIIL (all features)", "(a) PhiUSIIL, full set"),
                                       ("PhiUSIIL", "(b) PhiUSIIL, lexical setting")]):
        s = d[d.Dataset == key].sort_values("Single-feature AUC")
        cols = ["#c0392b" if v > 0.95 else "#8a8a85" for v in s["Single-feature AUC"]]
        ax.barh(s.Feature, s["Single-feature AUC"], color=cols, height=0.65)
        for y, v in enumerate(s["Single-feature AUC"]):
            ax.text(0.505, y, f"{v:.3f}", va="center", fontsize=7, color="white", fontweight="bold")
        ax.axvline(0.95, color="black", ls="--", lw=0.9); ax.set_xlim(0.5, 1.0)
        ax.text(0.95, 9.6, "0.95", fontsize=7, ha="center")
        ax.set_title(title, fontsize=9.5, fontweight="bold", pad=12)
        ax.tick_params(axis="y", labelsize=7.2); ax.set_xlabel("Single feature ROC-AUC")
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
    plt.tight_layout(); plt.savefig(OUT / "fig3_shortcut_auc.png", dpi=300, bbox_inches="tight"); plt.close()


def fig4():
    a = Image.open(ROOT / "results/figures/fig_rfecv_phiusiil.png")
    b = Image.open(ROOT / "results/figures/fig_rfecv_wpd.png")
    a = a.crop((0, 75, a.width, a.height)); b = b.crop((0, 75, b.width, b.height))
    s = Image.new("RGB", (a.width + b.width, a.height + 70), "white")
    s.paste(a, (0, 70)); s.paste(b, (a.width, 70))
    dr = ImageDraw.Draw(s)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 46)
    except OSError:
        f = None
    dr.text((a.width // 2 - 220, 10), "(a) PhiUSIIL, lexical", fill="black", font=f)
    dr.text((a.width + b.width // 2 - 80, 10), "(b) WPD", fill="black", font=f)
    s.save(OUT / "fig4_rfecv.png", dpi=(300, 300))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig2(); fig3(); fig4()
    print("Figures written to", OUT)
