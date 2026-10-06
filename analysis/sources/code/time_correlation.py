"""Animated correlation matrix between the parties' 30-day poll averages, window moving through time.

Each frame shows the Pearson correlation of the parties' averages within a short window centred
on one date. Note: with a window this short the values are noisy; the animation is for
intuition, not for estimates.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FFMpegWriter, FuncAnimation

from common import PARTIES, PARTY_NAMES, THEMES, load_average, output_path

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
    image = ax.imshow(first.values, cmap="coolwarm", vmin=-1, vmax=1, interpolation="none")
    cbar = plt.colorbar(image)
    cbar.ax.tick_params(colors=theme.fg)
    ax.set_xticks(np.arange(n), labels, rotation=45, color=theme.fg)
    ax.set_yticks(np.arange(n), labels, color=theme.fg)
    texts = [[ax.text(j, i, "", ha="center", va="center", fontsize=8) for j in range(n)] for i in range(n)]
    plt.tight_layout()

    def update(frame):
        matrix = corr_matrix(df, dates[frame]).values
        image.set_data(matrix)
        title.set_text(dates[frame].strftime("%m-%Y"))
        for i in range(n):
            for j in range(n):
                texts[i][j].set_text(f"{matrix[i, j]:.2f}")
                # readable on both the saturated colours and the neutral centre of the colour map
                texts[i][j].set_color("white" if abs(matrix[i, j]) > 0.5 or theme.name == "dark" else "black")
        return [image, title] + [t for row in texts for t in row]

    ani = FuncAnimation(fig, update, frames=len(dates), interval=100, blit=False, repeat=False)
    mp4 = output_path("animations", f"time_correlation_{theme.name}.mp4")
    ani.save(mp4, writer=FFMpegWriter(fps=20, bitrate=1800))
    plt.close(fig)
    print(f"Saved {mp4}")


if __name__ == "__main__":
    averages = load_average(30)[list(PARTIES)]
    for theme in THEMES:
        render(averages, theme)
