"""Party poll averages vs. three economic indicators: DAX (weekly), consumer prices (monthly), GDP (yearly).

For every indicator: a line plot of the indicator, one scatter plot with regression line per party,
and `output/correlations/economy_correlations.csv` with all Pearson r values.

Caveat: both series mostly trend over time, so these correlations largely reflect shared trends
(e.g. the AfD rising while prices and the DAX rose), not a causal relationship.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import DATA_DIR, PARTIES, PARTY_NAMES, THEMES, load_average, output_path, style_axes


def load_dax() -> pd.Series:
    """Weekly DAX opening value (investing.com export, German number format)."""
    df = pd.read_csv(DATA_DIR / "DAX_HISTORISCHE_DATEN.csv", parse_dates=["Datum"], date_format="%d.%m.%Y")
    values = df["Eröffn."].str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
    return pd.Series(values.values, index=pd.DatetimeIndex(df["Datum"], name="date")).sort_index()


def load_cpi() -> pd.Series:
    """Monthly consumer price index (2020=100), Destatis."""
    df = pd.read_csv(DATA_DIR / "VPI.csv", parse_dates=["date"], date_format="%Y-%m")
    df = df[df["value_unit"] != "%"].sort_values("date")  # drops the year-on-year change rows
    return pd.Series(df["value"].astype(float).values, index=pd.DatetimeIndex(df["date"], name="date"))


def load_gdp() -> pd.Series:
    """Yearly gross domestic product in billion EUR, Destatis (dated 1 January of the year)."""
    df = pd.read_csv(DATA_DIR / "BIP.csv", sep=";", parse_dates=["time"], date_format="%Y")
    df = df[df["value_variable_label"] == "Bruttoinlandsprodukt"].sort_values("time")
    values = df["value"].str.replace(",", ".").astype(float)
    return pd.Series(values.values, index=pd.DatetimeIndex(df["time"], name="date"))


INDICATORS = {
    # key: (loader, display name, axis label, file slug)
    "DAX": (load_dax, "DAX", "DAX points", "DAX"),
    "CPI": (load_cpi, "CPI", "Consumer price index (2020=100)", "CPI"),
    "GDP": (load_gdp, "GDP", "Gross domestic product (billion EUR)", "GDP"),
}


def plot_indicator(series: pd.Series, name: str, ylabel: str, slug: str, theme) -> None:
    fig, ax = plt.subplots(facecolor=theme.bg, figsize=(9, 6))
    style_axes(ax, theme, title=f"{name} over time", xlabel="Time", ylabel=ylabel)
    ax.plot(series.index, series.values, color="blue")
    plt.setp(ax.get_xticklabels(), rotation=45)
    fig.tight_layout()
    fig.savefig(output_path("line_plots", f"{slug}_over_time_{theme.name}.svg"))
    plt.close(fig)


def plot_party(combined: pd.DataFrame, party: str, r: float, name: str, ylabel: str, slug: str, theme) -> None:
    """Scatter of the indicator (x) against the party's poll average (y) with a regression line."""
    fig, ax = plt.subplots(facecolor=theme.bg)
    style_axes(ax, theme, title=f"{PARTY_NAMES[party]} vs {name} (r={r:.2f})",
               xlabel=ylabel, ylabel="Poll average (%)")
    dot_color = theme.scatter_color(party)
    line_color = theme.fg if PARTIES[party][1] == "red" else "red"  # SPD dots are red themselves
    sns.regplot(data=combined, x=name, y=party, ax=ax,
                scatter_kws={"color": dot_color, "alpha": 0.7, "s": 10},
                line_kws={"color": line_color, "alpha": 0.9, "linewidth": 2})
    ax.set_xlabel(ylabel, color=theme.fg)
    ax.set_ylabel("Poll average (%)", color=theme.fg)
    fig.savefig(output_path("correlations", f"{party.replace('/', '_')}_vs_{slug}_{theme.name}.svg"))
    plt.close(fig)


if __name__ == "__main__":
    polls_avg = load_average(30)[list(PARTIES)]
    summary = {}
    for key, (loader, name, ylabel, slug) in INDICATORS.items():
        series = loader().rename(name)
        combined = polls_avg.join(series, how="inner").dropna(subset=[name])  # dates where both exist
        corr = combined.corr()[name].drop(name)
        summary[name] = {"n": int(len(combined)), **corr.rename(index=PARTY_NAMES).round(2).to_dict()}
        print(f"{name} (n={len(combined)}):\n{corr.round(2).to_string()}\n")
        for theme in THEMES:
            plot_indicator(series, name, ylabel, slug, theme)
            for party in PARTIES:
                plot_party(combined, party, corr[party], name, ylabel, slug, theme)
    pd.DataFrame(summary).to_csv(output_path("correlations", "economy_correlations.csv"))
