"""Correlation matrix of party results (dawum.de surveys, 2017-2026) for every parliament with >= 500 surveys."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import THEMES, corr_colormap, label_diagonal, mask_diagonal, output_path
from survey_counts import load_dawum

MIN_SURVEYS = 500  # parliaments with fewer surveys are skipped
MIN_NON_NULL = 0.1  # result columns that are mostly empty (tiny parties) are dropped
META_COLUMNS = ["survey_date", "survey_persons", "parliament_id", "institute_id"]
DAWUM_PARTY_NAMES = {"cdu-csu": "CDU/CSU", "spd": "SPD", "gruene": "Greens", "fdp": "FDP", "linke": "Left",
                     "afd": "AfD", "bsw": "BSW", "sonstige": "Others"}


def correlation_matrices(theme) -> None:
    df = load_dawum()
    counts = df["parliament_id"].value_counts()
    parliaments = counts[counts >= MIN_SURVEYS].index.tolist()
    print(f"Parliaments with >= {MIN_SURVEYS} surveys: {parliaments}")

    rows = math.ceil(len(parliaments) / 1)
    fig, axes = plt.subplots(rows, 1, figsize=(6, rows * 5), constrained_layout=True, facecolor=theme.bg)
    axes = np.atleast_1d(axes)
    image = None
    for ax, pid in zip(axes, parliaments):
        df_p = df[df["parliament_id"] == pid].reset_index(drop=True)
        result_cols = [c for c in df_p.columns if c.startswith("result_")]
        sparse = [c for c in result_cols if df_p[c].notna().mean() < MIN_NON_NULL]
        corr = df_p.drop(columns=sparse + META_COLUMNS, errors="ignore").corr(numeric_only=True)
        labels = [name.replace("result_", "") for name in corr.columns]
        labels = [DAWUM_PARTY_NAMES.get(label, label) for label in labels]
        image = ax.imshow(mask_diagonal(corr.values), cmap=corr_colormap(theme), vmin=-1, vmax=1)
        label_diagonal(ax, labels, theme, fontsize=7)
        for i in range(len(labels)):
            for j in range(len(labels)):
                if i != j:
                    ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="white", fontsize=7)
        ax.set_title(f"Sonntagsfrage correlation matrix\n{pid.capitalize()}, 2017-2026 (n={len(df_p)})", color=theme.fg)
    if image is not None:
        cbar = fig.colorbar(image, ax=axes.tolist(), fraction=0.02, pad=0.1)
        cbar.ax.tick_params(colors=theme.fg)
    fig.savefig(output_path("correlations", f"party_correlation_matrix_2017_2026_{theme.name}.svg"))
    plt.close(fig)


if __name__ == "__main__":
    for theme in THEMES:
        correlation_matrices(theme)
