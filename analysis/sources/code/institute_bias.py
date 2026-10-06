"""How far does each institute deviate from the 30-day average of all polls?

For every institute and party, the deviation of each of its polls from the 30-day trailing
average (output/survey_averages/30D_survey_averages.csv, run survey_averages.py first) is
plotted as a histogram. A mean deviation away from 0 hints at a 'house effect'.
Caveat: the average contains the institute's own polls, so deviations are slightly understated.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import INSTITUTES, PARTIES, PARTY_NAMES, THEMES, load_average, load_polls, output_path


def deviations(polls: pd.DataFrame, average: pd.DataFrame, institute: str) -> pd.DataFrame:
    subset = polls[polls["institute_id"] == institute]
    out = pd.DataFrame()
    for party in PARTIES:
        out[party] = pd.to_numeric(subset[party], errors="coerce") - pd.to_numeric(average[party], errors="coerce")
    return out


def plot_institute(institute: str, dev: pd.DataFrame, n_polls: int, theme) -> None:
    name, slug = INSTITUTES[institute]
    fig, axes = plt.subplots(2, 3, figsize=(15, 11), facecolor=theme.bg, sharex=True, sharey=True)
    for ax, party in zip(axes.ravel(), PARTIES):
        sns.histplot(dev[party], bins=12, ax=ax, kde=True, edgecolor="white", linewidth=0.5, alpha=0.2,
                     label="deviation from 30-day average")
        ax.set_facecolor(theme.bg)
        ax.axvline(dev[party].mean(), color="red", label="mean deviation")
        ax.axvline(0, color=theme.fg, linestyle="dashed", linewidth=0.5, label="30-day average")
        ax.set_xlabel("Deviation from the aggregated mean (percentage points)", color=theme.fg)
        ax.set_ylabel("Number of polls", color=theme.fg)
        ax.tick_params(colors=theme.fg)
        ax.set_title(PARTY_NAMES[party], color=theme.fg)
        for spine in ax.spines.values():
            spine.set_color(theme.fg)
    axes.ravel()[-1].legend(facecolor=theme.bg, labelcolor=theme.fg)
    fig.suptitle(f"{name} (n={n_polls})", fontsize=20, color=theme.fg)
    sns.despine()
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output_path("survey_deviations", f"{slug}_{theme.name}.svg"))
    plt.close(fig)


if __name__ == "__main__":
    polls = load_polls().drop_duplicates()
    average = load_average(30)
    for institute in INSTITUTES:
        dev = deviations(polls, average, institute)
        n = int((polls["institute_id"] == institute).sum())
        for theme in THEMES:
            plot_institute(institute, dev, n, theme)
        print(f"{institute}: n={n}, mean deviation (pp):\n{dev.mean().round(2).to_string()}\n")
