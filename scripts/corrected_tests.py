"""Corrected resampled t-test (Nadeau and Bengio, 2003) and Holm adjustment.

Recomputes Table 10 of the paper from results/tables/9_statistical_test.csv,
which stores the uncorrected paired t-test and Wilcoxon p values of the
10-fold comparisons. For k folds with test/train ratio n2/n1, the corrected
statistic is t_c = t * sqrt((1/k) / (1/k + n2/n1)).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
K = 10
RATIO = 1 / 9  # test fold size / training fold size for 10-fold CV


def holm(pvals):
    p = np.asarray(pvals, float)
    n = len(p)
    adj = np.empty(n)
    running = 0.0
    for rank, i in enumerate(np.argsort(p)):
        running = max(running, min(1.0, (n - rank) * p[i]))
        adj[i] = running
    return adj


def main():
    df = pd.read_csv(ROOT / "results/tables/9_statistical_test.csv")
    scale = np.sqrt((1 / K) / (1 / K + RATIO))
    t_unc = stats.t.isf(df["Paired t-test p"] / 2, K - 1)
    df["Corrected t-test p"] = 2 * stats.t.sf(t_unc * scale, K - 1)
    df["Corrected t-test p (Holm)"] = holm(df["Corrected t-test p"])
    df["Wilcoxon p (Holm)"] = holm(df["Wilcoxon p"])
    cols = ["Dataset", "Comparison", "Mean diff (pp)", "Paired t-test p",
            "Corrected t-test p", "Corrected t-test p (Holm)", "Wilcoxon p", "Wilcoxon p (Holm)"]
    out = df[cols].round(5)
    out.to_csv(ROOT / "results/tables/10b_corrected_tests.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
