"""'Racing line' animation: the 30-day centred average of each party is drawn year by year."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FFMpegWriter, FuncAnimation

from common import PARTIES, PARTY_NAMES, THEMES, gif_from_mp4, load_polls, output_path, style_axes

WINDOW_DAYS = 30  # centred rolling window
JUMP_DAYS = 45  # days added to the line from one frame to the next


def centred_average(polls: pd.DataFrame) -> pd.DataFrame:
    avg = pd.DataFrame()
    for party in PARTIES:
        daily = pd.to_numeric(polls[party], errors="coerce").resample("D").mean()
        avg[party] = daily.rolling(f"{WINDOW_DAYS}D", center=True).mean()
    return avg


def render(avg: pd.DataFrame, theme) -> None:
    fig, ax = plt.subplots(facecolor=theme.bg)
    style_axes(ax, theme, ylabel="Vote share (%)")
    ax.set_xlim(avg.index.min(), avg.index.max())
    ax.set_ylim(0, 55)
    lines = [ax.plot([], [], color=theme.party_color(p), label=PARTY_NAMES[p])[0] for p in PARTIES]
    ax.legend(loc="upper right", frameon=True, facecolor=theme.bg, labelcolor=theme.fg, edgecolor=theme.fg)

    n_frames = len(avg) // JUMP_DAYS

    def update(i):
        for line, party in zip(lines, PARTIES):
            line.set_data(avg.iloc[: i * JUMP_DAYS].index, avg[party].iloc[: i * JUMP_DAYS])
        return lines

    ani = FuncAnimation(fig, update, frames=n_frames, interval=100, blit=False, repeat=False)
    mp4 = output_path("animations", f"racing_average_{theme.name}.mp4")
    ani.save(mp4, writer=FFMpegWriter(fps=60, bitrate=3600))
    gif_from_mp4(mp4)
    plt.close(fig)
    print(f"Saved {mp4}")


if __name__ == "__main__":
    average = centred_average(load_polls())
    for theme in THEMES:
        render(average, theme)
