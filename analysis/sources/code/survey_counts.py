"""How many surveys does the dawum.de dataset (2017-2026) contain, per institute and per parliament?"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import DATA_DIR, THEMES, output_path

DROP_COLUMNS = ["survey_id", "survey_start", "survey_end", "parliament_name", "institute_name",
                "tasker_id", "tasker_name", "result_familie"]


def load_dawum() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "dawum-full.csv")
    df = df.dropna(subset=["parliament_name", "institute_name"])
    return df.drop(columns=DROP_COLUMNS)


def bar_chart(counts: pd.Series, title: str, xlabel: str, filename: str, theme) -> None:
    fig, ax = plt.subplots(facecolor=theme.bg, figsize=(9, 6))
    ax.set_facecolor(theme.bg)
    sns.barplot(ax=ax, x=counts.index, y=counts.values, edgecolor=theme.bg, linewidth=0.5)
    ax.set_title(f"{title} (n={counts.sum()})", color=theme.fg, fontsize=28)
    ax.set_xlabel(xlabel, color=theme.fg)
    ax.set_ylabel("Number of surveys", color=theme.fg)
    plt.xticks(rotation=45, ha="right", color=theme.fg)
    plt.yticks(color=theme.fg)
    sns.despine()
    plt.tight_layout()
    fig.savefig(output_path("histograms", f"{filename}_{theme.name}.svg"))
    plt.close(fig)


if __name__ == "__main__":
    surveys = load_dawum()
    per_institute = surveys["institute_id"].value_counts()
    per_parliament = surveys["parliament_id"].value_counts()
    print(per_institute.to_string(), "\n", per_parliament.to_string())
    for theme in THEMES:
        bar_chart(per_institute, "Surveys per institute", "Institute", "surveys_per_institute", theme)
        bar_chart(per_parliament, "Surveys per election", "Parliament", "surveys_per_parliament", theme)
