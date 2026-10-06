"""Shared paths, party definitions and plot styling for all analysis scripts.

Every script can be run from any directory, e.g. `python analysis/sources/code/survey_averages.py`.
Figures are produced in a dark and a light variant (file suffix `_dark` / `_light`).
"""

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # scripts only write files, never open windows

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd
import seaborn as sns  # noqa: E402

CODE_DIR = Path(__file__).resolve().parent
DATA_DIR = CODE_DIR.parent / "data"
OUTPUT_DIR = CODE_DIR.parent.parent / "output"

# Column name in the poll CSVs -> (English display name, line/marker colour)
PARTIES = {
    "CDU/CSU": ("CDU/CSU", "black"),
    "SPD": ("SPD", "red"),
    "GRÜNE": ("Greens", "green"),
    "FDP": ("FDP", "yellow"),
    "LINKE": ("Left", "purple"),
    "AfD": ("AfD", "blue"),
}
PARTY_NAMES = {col: name for col, (name, _) in PARTIES.items()}

# Polling institutes: id in umfragen_wahlrecht.csv -> (display name, file name slug)
INSTITUTES = {
    "FORSA": ("Forsa", "forsa"),
    "DIMAP": ("Infratest dimap", "infratest_dimap"),
    "FOWA": ("Forschungsgruppe Wahlen", "forschungsgruppe_wahlen"),
    "ALLENS": ("Allensbach", "allensbach"),
    "GMS": ("GMS", "gms"),
    "INSA": ("INSA", "insa"),
    "YOUGOV": ("YouGov", "yougov"),
    "VERIAN": ("Verian (Emnid)", "verian"),
}

# Federal elections (Bundestag) since 2002
ELECTION_DATES = [
    "2002-09-22", "2005-09-18", "2009-09-27", "2013-09-22",
    "2017-09-24", "2021-09-26", "2025-02-23",
]


@dataclass(frozen=True)
class Theme:
    name: str  # used as file suffix
    bg: str
    fg: str

    def party_color(self, party: str) -> str:
        """Party colour; CDU/CSU is black, which is invisible on a dark background."""
        color = PARTIES[party][1]
        return self.fg if (color == "black" and self.name == "dark") else color


THEMES = [Theme("dark", "black", "white"), Theme("light", "white", "black")]


def style_axes(ax, theme: Theme, title: str | None = None, xlabel: str | None = None, ylabel: str | None = None):
    """Apply the theme to an axes object (background, spines, ticks, labels)."""
    ax.set_facecolor(theme.bg)
    for spine in ax.spines.values():
        spine.set_color(theme.fg)
    ax.tick_params(axis="x", colors=theme.fg)
    ax.tick_params(axis="y", colors=theme.fg)
    if title is not None:
        ax.set_title(title, color=theme.fg)
    if xlabel is not None:
        ax.set_xlabel(xlabel, color=theme.fg)
    if ylabel is not None:
        ax.set_ylabel(ylabel, color=theme.fg)
    sns.despine(ax=ax)


def load_polls() -> pd.DataFrame:
    """All Bundestag polls from wahlrecht.de (vote share in %, indexed by publication date)."""
    df = pd.read_csv(DATA_DIR / "umfragen_wahlrecht.csv", parse_dates=["date"])
    return df.set_index("date")


def load_average(days: int = 30) -> pd.DataFrame:
    """Trailing rolling average of the polls (see survey_averages.py); needs that script run first."""
    path = OUTPUT_DIR / "survey_averages" / f"{days}D_survey_averages.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} is missing - run survey_averages.py first")
    return pd.read_csv(path, parse_dates=["date"]).set_index("date")


def output_path(subdir: str, name: str) -> Path:
    path = OUTPUT_DIR / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path / name


def gif_from_mp4(mp4: Path, width: int = 640, fps: int = 15) -> Path:
    """Convert an mp4 to a small looping gif with ffmpeg (for embedding in the README)."""
    import subprocess

    gif = mp4.with_suffix(".gif")
    palette_filter = f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf", palette_filter, str(gif)], check=True)
    return gif


def corr_colormap(theme: Theme):
    """coolwarm, with masked cells (the diagonal, missing data) drawn in the background colour."""
    cmap = plt.get_cmap("coolwarm").copy()
    cmap.set_bad(theme.bg)
    return cmap


def mask_diagonal(matrix) -> "np.ma.MaskedArray":
    """Correlation matrix with the (always 1) diagonal and NaNs masked, so they get the background colour."""
    import numpy as np

    masked = np.ma.masked_invalid(np.asarray(matrix, dtype=float))
    masked[np.diag_indices(masked.shape[0])] = np.ma.masked
    return masked


def corr_text(value: float) -> str:
    """Cell annotation; empty for missing data (e.g. AfD before 2013)."""
    return "" if value != value else f"{value:.2f}"  # NaN != NaN


def label_diagonal(ax, labels: list[str], theme: Theme, fontsize: int = 8) -> None:
    """Write the variable names on the diagonal instead of on the axes."""
    for i, label in enumerate(labels):
        ax.text(i, i, label, ha="center", va="center", color=theme.fg, fontsize=fontsize, fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
