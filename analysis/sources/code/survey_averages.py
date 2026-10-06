"""Rolling averages of the polls over windows of 5, 10, ... 5000 days.

Writes one CSV per window length to output/survey_averages/ (the 30-day one is used by most
other scripts) and an animation in which the window grows from 5 days to ~14 years.

Method: all polls of a day are averaged per party, days without a poll are NaN, then a trailing
rolling mean over `N` calendar days is taken (NaN days are skipped).
"""

import pandas as pd
from matplotlib.animation import FFMpegWriter, FuncAnimation

from common import PARTIES, PARTY_NAMES, THEMES, gif_from_mp4, load_polls, output_path, style_axes

WINDOW_STEP = 5  # days; window i has length WINDOW_STEP * i
N_WINDOWS = 1000


def compute_averages(polls: pd.DataFrame) -> list[pd.DataFrame]:
    daily = {}
    for party in PARTIES:
        daily[party] = pd.to_numeric(polls[party], errors="coerce").resample("D").mean()
    averages = []
    for i in range(1, N_WINDOWS + 1):
        window = f"{WINDOW_STEP * i}D"
        df = pd.DataFrame({party: series.rolling(window).mean() for party, series in daily.items()})
        df.index.name = "date"
        df.to_csv(output_path("survey_averages", f"{WINDOW_STEP * i}D_survey_averages.csv"))
        averages.append(df)
    print(f"Computed {len(averages)} rolling averages")
    return averages


def render_animation(averages: list[pd.DataFrame], theme) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(facecolor=theme.bg)
    style_axes(ax, theme)
    ax.set_xlim(averages[-1].index.min(), averages[-1].index.max())
    ax.set_ylim(0, 55)
    ax.set_ylabel("Vote share (%)", color=theme.fg)
    lines = [ax.plot([], [], color=theme.party_color(p), label=PARTY_NAMES[p])[0] for p in PARTIES]
    title = ax.set_title("", color=theme.fg)
    ax.legend(facecolor=theme.bg, labelcolor=theme.fg, edgecolor=theme.fg)

    def update(i):
        for line, party in zip(lines, PARTIES):
            line.set_data(averages[i].index, averages[i][party])
        title.set_text(f"Sonntagsfrage - {WINDOW_STEP * (i + 1)}-day rolling window")
        return lines + [title]

    ani = FuncAnimation(fig, update, frames=len(averages), interval=100, blit=True, repeat=False)
    mp4 = output_path("animations", f"sonntagsfrage_rolling_window_{theme.name}.mp4")
    ani.save(mp4, writer=FFMpegWriter(fps=60, bitrate=3600))
    gif_from_mp4(mp4)
    plt.close(fig)
    print(f"Saved {mp4}")


if __name__ == "__main__":
    averages = compute_averages(load_polls())
    for theme in THEMES:
        render_animation(averages, theme)
