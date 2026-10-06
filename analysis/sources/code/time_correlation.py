"""Animated correlation matrix between the parties' 30-day poll averages, window moving through time.

Each frame shows the Pearson correlation of the parties' averages within a short window centred
on one date. Note: with a window this short the values are noisy; the animation is for
intuition, not for estimates.
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FFMpegWriter, FuncAnimation

from common import (PARTIES, PARTY_NAMES, THEMES, corr_colormap, label_diagonal, load_average, mask_diagonal,
                    output_path)

JUMP_DAYS = 5  # days between two frames
CORR_WINDOW_DAYS = 30  # width of the window the correlation is computed on


def corr_matrix(df: pd.DataFrame, date: pd.Timestamp) -> pd.DataFrame:
    half = pd.Timedelta(days=CORR_WINDOW_DAYS // 2)
    return df.loc[date - half: date + half].corr(method="pearson")


def render(df: pd.DataFrame, theme) -> None:
    dates = df.index.tolist()[::JUMP_DAYS]
    first = corr_matrix(df, dates[0])
    labels = [PARTY_NAMES[c] for c in first.columns]
    n = len(labels)

    fig, ax = plt.subplots(facecolor=theme.bg)
    ax.set_facecolor(theme.bg)
    title = ax.set_title(dates[0].strftime("%m-%Y"), color=theme.fg)
    image = ax.imshow(mask_diagonal(first.values), cmap=corr_colormap(theme), vmin=-1, vmax=1, interpolation="none")
    cbar = plt.colorbar(image)
    cbar.ax.tick_params(colors=theme.fg)
    label_diagonal(ax, labels, theme)
    # value annotations for the off-diagonal cells only; the diagonal shows the party names
    texts = {(i, j): ax.text(j, i, "", ha="center", va="center", fontsize=8)
             for i in range(n) for j in range(n) if i != j}
    plt.tight_layout()

    def update(frame):
        matrix = corr_matrix(df, dates[frame]).values
        image.set_data(mask_diagonal(matrix))
        title.set_text(dates[frame].strftime("%m-%Y"))
        for (i, j), text in texts.items():
            text.set_text(f"{matrix[i, j]:.2f}")
            # readable on both the saturated colours and the neutral centre of the colour map
            text.set_color("white" if abs(matrix[i, j]) > 0.5 or theme.name == "dark" else "black")
        return [image, title] + list(texts.values())

    ani = FuncAnimation(fig, update, frames=len(dates), interval=100, blit=False, repeat=False)
    mp4 = output_path("animations", f"time_correlation_{theme.name}.mp4")
    ani.save(mp4, writer=FFMpegWriter(fps=20, bitrate=1800))
    plt.close(fig)
    print(f"Saved {mp4}")


if __name__ == "__main__":
    averages = load_average(30)[list(PARTIES)]
    for theme in THEMES:
        render(averages, theme)
