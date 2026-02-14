import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def corr_matrices():
    # fetches and cleans dawum-full.csv
    df = pd.read_csv('../data/dawum-full.csv', parse_dates=['survey_date'])
    df.dropna(subset=['parliament_name', 'institute_name'], inplace=True)
    df.drop(inplace=True,
    columns=['survey_id', 'survey_start', 'survey_end', 'parliament_name', 'institute_name', 'tasker_id', 'tasker_name', 'result_familie'])
    # define parliaments to plot (replace with a custom list if desired)
    parliaments = df['parliament_id'].unique().tolist()

    min_n=500 #minimum amount of surveys required
    remaining_elections = []
    for pid in parliaments:
        if not len(df[df['parliament_id'] == pid].index.tolist())<min_n:
            remaining_elections.append(pid)
        print(f"Election: {pid}; n:{len(df[df['parliament_id'] == pid].index.tolist())}")

    print(f"Remaining elections:{remaining_elections}")

    # layout settings
    cols = 1
    n = len(remaining_elections)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 4), constrained_layout=True)
    axes_flat = np.array(axes).flatten()

    last_im = None

    for idx, pid in enumerate(remaining_elections):
        ax = axes_flat[idx]
        df_p = df[df["parliament_id"] == pid].reset_index(drop=True)
        if df_p.empty:
            ax.axis('off')
            continue
        # result columns and drop very-sparse ones
        result_cols = [c for c in df_p.columns if c.startswith('result_')]
        if not result_cols:
            ax.text(0.5, 0.5, "no result_* columns", ha='center', va='center')
            ax.axis('off')
            continue
        non_null_frac = df_p[result_cols].notna().mean()
        cols_to_drop = non_null_frac[non_null_frac < 0.1].index.tolist()
        if cols_to_drop:
            df_p = df_p.drop(columns=cols_to_drop)
        # drop non-result columns if present
        drop_common = [c for c in ["survey_date", "survey_persons", "parliament_id", "institute_id"] if c in df_p.columns]
        corr_matrix = df_p.drop(columns=drop_common, errors='ignore').corr()

        if corr_matrix.shape[0] < 1:
            ax.text(0.5, 0.5, "not enough data", ha='center', va='center')
            ax.axis('off')
            continue

        labels = [name.replace("result_", "") for name in corr_matrix.columns]
        m = len(labels)

        # explicit tick positions/labels to avoid missing/misaligned labels
        im = ax.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
        last_im = im
        ax.set_xticks(np.arange(m))
        ax.set_yticks(np.arange(m))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
        ax.set_yticklabels(labels, fontsize=8)

        # annotations
        for i in range(m):
            for j in range(m):
                ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                        ha="center", va="center", color="w", fontsize=7)

        ax.set_title(f"Korrelationsmatrix der Sonntagsfrage (2017-2026; n={len(df_p)})")

    # hide any unused axes
    for ax in axes_flat[n:]:
        ax.axis('off')

    # replace the previous layout/colorbar section with tighter vertical spacing
    # tighten layout with smaller vertical padding and explicitly reduce hspace
    #fig.subplots_adjust(hspace=0.4)  # reduce vertical spacing between rows

    if last_im is not None:
        fig.colorbar(last_im, ax=axes_flat.tolist(), fraction=0.02, pad=0.1)
    plt.savefig("../../output/correlations/2017-2026_corr-matrix.png")
    plt.show()

corr_matrices()
